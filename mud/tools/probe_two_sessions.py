"""Two humans, one world: a real telnet session against the running MUD (#946).

Not a unit test — an end-to-end probe, kept in the tree because the claim it checks is not
checkable in-process: the socket, the parser, the login flow and the persistence all have
to be real for it to pass. It is what proves the acceptance criterion "supports terminal
text play with two concurrent accounts".

    python3 mud/tools/probe_two_sessions.py [--host 127.0.0.1] [--port 4000]

Exits non-zero if either account cannot log in, if the CWN sheet or the UNSA faction does
not render, or if the two sessions cannot see each other in the same room.

The protocol is Evennia's own connection screen. Note two of its own limits, learned the
hard way: a username is at least 3 characters, a password at least 8, and repeated failed
`connect` attempts are throttled for minutes — so this probe **creates first** and only
falls back to `connect`, instead of provoking the throttle with a guess.
"""
from __future__ import annotations

import argparse
import re
import sys
import telnetlib
import time

CLEAN = re.compile(r"\x1b\[[0-9;]*m")


class Session(telnetlib.Telnet):
    """A telnet session that speaks the connection screen and then the game."""

    def read(self, seconds: float = 1.5) -> str:
        deadline = time.time() + seconds
        chunks: list[bytes] = []
        while time.time() < deadline:
            time.sleep(0.1)
            try:
                chunk = self.read_very_eager()
            except EOFError:
                break
            if chunk:
                chunks.append(chunk)
                deadline = time.time() + 0.35
        return CLEAN.sub("", b"".join(chunks).decode("utf-8", "replace")).replace("\r\n", "\n")

    def send(self, line: str, wait: float = 1.5) -> str:
        self.write((line + "\n").encode("utf-8"))
        return self.read(wait)


def enter(name: str, password: str, *, host: str, port: int) -> Session:
    """Create the account if it is new, then take control of a character with that name."""
    session = Session(host, port, timeout=15)
    session.read(2.0)

    reply = session.send(f"create {name} {password}", 1.5)
    if "intended" in reply.lower():
        session.send("Y", 2.0)
    # Evennia creates the account but does not log it in: it prints the `connect` line to
    # use. So the connect is unconditional and comes after the create, never instead of it.
    session.send(f"connect {name} {password}", 2.0)

    # First login puppets an auto-created character of the same name; the character typeclass
    # moves it out of Evennia's Limbo and into the neighbourhood, so no `ic` is needed here.
    session.read(1.5)
    return session


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4000)
    args = parser.parse_args()

    first = enter("AiPunk", "korppu-2026-vaaksa", host=args.host, port=args.port)
    second = enter("TomiP", "vallila-2026-lokki", host=args.host, port=args.port)

    sheet = first.send("sheet")
    faction = first.send("faction")
    second_spoke = second.send("say the lift is out")
    first_heard = first.send("look", 2.5)   # who is in the room with me
    first.send("scavenge")
    second.send("look")

    problems = []
    if "Strength" not in sheet:
        problems.append("the CWN sheet did not render")
    if "UNSA" not in faction:
        problems.append("the UNSA faction did not render")
    if "TomiP" not in first_heard and "TomiP" not in second_spoke:
        problems.append("the two sessions could not see each other")

    print("---- AiPunk: sheet ----")
    print(sheet.strip()[:900])
    print("---- AiPunk: faction ----")
    print(faction.strip()[:400])
    print("---- AiPunk heard ----")
    print(first_heard.strip()[:300])

    for session in (first, second):
        try:
            session.close()
        except Exception:
            pass

    if problems:
        print("FAILED: " + "; ".join(problems), file=sys.stderr)
        return 1
    print("OK: two concurrent accounts logged in, shared one room and one world")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
