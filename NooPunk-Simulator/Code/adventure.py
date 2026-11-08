"""Small, dependency-free detective interactive-fiction runner.

Only consumes reviewed scene JSON; never writes author Story/Paper or imports RPG code.
Run: python NooPunk-Simulator/Code/adventure.py
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_CASE = Path(__file__).resolve().parent.parent / "Graphs" / "fixtures" / "romppainen_development_case.json"
SAVE_VERSION = 1

#: The player's standing on a hypothesis. A hypothesis is the detective's reasoning, never a fact.
CONSIDERED = "considered"
DISMISSED = "dismissed"


def load_case(path=DEFAULT_CASE):
    case = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(case, dict) or not isinstance(case.get("scenes"), dict):
        raise ValueError("Case must contain scenes")
    if case.get("start") not in case["scenes"] or not case.get("id"):
        raise ValueError("Case needs id and a valid start scene")
    for key, scene in case["scenes"].items():
        if not isinstance(scene.get("choices"), list) or not isinstance(scene.get("text"), str):
            raise ValueError("Scene needs text and choices: " + key)
        for choice in scene["choices"]:
            if choice.get("to") not in case["scenes"] or not choice.get("label"):
                raise ValueError("Invalid destination or label in " + key)
            for clue in choice.get("requires", []) + choice.get("adds", []):
                if clue not in case.get("clues", {}):
                    raise ValueError("Unknown clue: " + clue)
    for hypothesis in case.get("hypotheses", []):
        for clue in hypothesis.get("requires", []):
            if clue not in case.get("clues", {}):
                raise ValueError("Unknown clue in hypothesis: " + clue)
    for contradiction in case.get("contradictions", []):
        if len(contradiction.get("between", [])) < 2:
            raise ValueError("A contradiction needs two clues")
        for clue in contradiction["between"]:
            if clue not in case.get("clues", {}):
                raise ValueError("Unknown clue in contradiction: " + clue)
    return case


def hypothesis_ids(case):
    """Stable ids for the case's hypotheses: the author's own id, or ``h1``, ``h2``, … by order."""
    return [str(item.get("id") or "h" + str(index + 1))
            for index, item in enumerate(case.get("hypotheses", []))]


class Adventure:
    """One tiny scene/choice notebook runner; no RNG, combat, levels or rules engine."""

    def __init__(self, case, state=None):
        self.case = case
        self.state = state if state is not None else {
            "version": SAVE_VERSION, "case_id": case["id"], "scene": case["start"],
            "clues": [], "flags": {}, "history": [], "finished": False, "hypotheses": {}
        }
        self.state.setdefault("hypotheses", {})
        self._validate_state()

    def _validate_state(self):
        state = self.state
        if state.get("version") != SAVE_VERSION or state.get("case_id") != self.case["id"]:
            raise ValueError("Save version or case mismatch")
        if state.get("scene") not in self.case["scenes"]:
            raise ValueError("Save refers to unknown scene")
        if not isinstance(state.get("clues"), list) or not isinstance(state.get("history"), list):
            raise ValueError("Invalid save state")
        if not isinstance(state.get("flags"), dict) or not isinstance(state.get("finished"), bool):
            raise ValueError("Invalid flags/ending state")
        if any(clue not in self.case.get("clues", {}) for clue in state["clues"]):
            raise ValueError("Save refers to unknown clue")
        standing = state.get("hypotheses")
        if not isinstance(standing, dict):
            raise ValueError("Invalid hypothesis state")
        known = set(hypothesis_ids(self.case))
        for hypothesis_id, value in standing.items():
            if hypothesis_id not in known or value not in (CONSIDERED, DISMISSED):
                raise ValueError("Save refers to unknown or invalid hypothesis")

    @property
    def scene(self):
        return self.case["scenes"][self.state["scene"]]

    def choices(self):
        if self.state["finished"]:
            return []
        return [c for c in self.scene["choices"]
                if set(c.get("requires", [])).issubset(self.state["clues"])]

    def choose(self, number):
        options = self.choices()
        if not isinstance(number, int) or number < 1 or number > len(options):
            raise ValueError("Choose a visible option number")
        selected = options[number - 1]
        previous = self.state["scene"]
        for clue in selected.get("adds", []):
            if clue not in self.state["clues"]:
                self.state["clues"].append(clue)
        self.state["flags"].update(selected.get("flags", {}))
        self.state["scene"] = selected["to"]
        self.state["history"].append({
            "from": previous, "choice": selected["label"], "to": selected["to"]
        })
        self.state["finished"] = bool(self.scene.get("ending"))
        return self.scene

    # -- the detective's reasoning ------------------------------------------------------------- #
    def available_hypotheses(self):
        """Hypotheses the collected evidence now makes it possible to hold, as ``(id, text)``."""
        available = []
        for hypothesis_id, hypothesis in zip(hypothesis_ids(self.case),
                                             self.case.get("hypotheses", [])):
            if set(hypothesis.get("requires", [])).issubset(self.state["clues"]):
                available.append((hypothesis_id, hypothesis["text"]))
        return available

    def consider(self, hypothesis_id):
        """Record that the detective is working with this hypothesis. Availability is evidence-gated."""
        if hypothesis_id not in dict(self.available_hypotheses()):
            raise ValueError("No such hypothesis available on this evidence: " + str(hypothesis_id))
        self.state["hypotheses"][hypothesis_id] = CONSIDERED

    def dismiss(self, hypothesis_id):
        """Mark a hypothesis as set aside. It stays visible in the notebook as a rejected line."""
        if hypothesis_id not in dict(self.available_hypotheses()):
            raise ValueError("No such hypothesis available on this evidence: " + str(hypothesis_id))
        self.state["hypotheses"][hypothesis_id] = DISMISSED

    def contradictions(self):
        """Conflicting records the evidence in hand exposes, as ``(id, text)``. Not a verdict."""
        found = []
        for index, contradiction in enumerate(self.case.get("contradictions", [])):
            if set(contradiction.get("between", [])).issubset(self.state["clues"]):
                found.append((str(contradiction.get("id") or "c" + str(index + 1)),
                              contradiction["text"]))
        return found

    def visited(self):
        scenes = {entry["from"] for entry in self.state["history"]}
        scenes.add(self.state["scene"])
        return scenes

    def leads(self):
        """Lines of inquiry the detective already knows about but has not followed, as ``(id, title)``."""
        seen = self.visited()
        open_leads = {}
        for scene_id in sorted(seen):
            for choice in self.case["scenes"][scene_id]["choices"]:
                target = choice["to"]
                if target in seen or not choice.get("label"):
                    continue
                if set(choice.get("requires", [])).issubset(self.state["clues"]):
                    open_leads.setdefault(target, self.case["scenes"][target]["title"])
        return sorted(open_leads.items())

    def notebook(self):
        lines = ["CASE NOTEBOOK", "-------------"]
        if not self.state["clues"]:
            lines.append("Evidence recorded: none yet.")
        else:
            lines.append("Evidence (collected, not proven):")
            for clue in self.state["clues"]:
                lines.append("* " + self.case["clues"][clue])
        conflicts = self.contradictions()
        if conflicts:
            lines.append("Records that conflict:")
            for _, text in conflicts:
                lines.append("* " + text)
        open_leads = self.leads()
        if open_leads:
            lines.append("Open leads:")
            for scene_id, title in open_leads:
                lines.append("* " + title + " (" + scene_id + ")")
        available = self.available_hypotheses()
        if available:
            lines.append("Hypotheses you could hold (not established facts):")
            for hypothesis_id, text in available:
                lines.append("* [" + hypothesis_id + "] " + text)
        held = self._standing(CONSIDERED)
        if held:
            lines.append("Recorded by you:")
            for text in held:
                lines.append("* " + text)
        rejected = self._standing(DISMISSED)
        if rejected:
            lines.append("Set aside:")
            for text in rejected:
                lines.append("* " + text)
        lines.append("Decisions logged: " + str(len(self.state["history"])))
        if self.state["flags"].get("disposition"):
            lines.append("Disposition: " + str(self.state["flags"]["disposition"]))
        return "\n".join(lines)

    def _standing(self, wanted):
        return [text for hypothesis_id, text in self.available_hypotheses()
                if self.state["hypotheses"].get(hypothesis_id) == wanted]

    def save(self, path):
        Path(path).write_text(json.dumps(self.state, indent=2, ensure_ascii=False) + "\n",
                              encoding="utf-8")

    @classmethod
    def restore(cls, case, path):
        return cls(case, json.loads(Path(path).read_text(encoding="utf-8")))


def case_status(case):
    """Display provenance without implying synthetic or unapproved cases are canon."""
    source = case.get("source", {})
    if source.get("kind") == "synthetic_development_fixture":
        return "DEVELOPMENT FIXTURE, NOT TOMI\'S CANON"
    if source.get("kind") == "author_story":
        return ("AUTHOR-WRITTEN ADAPTATION, AWAITING CANON APPROVAL"
                if source.get("author_reviewed") else
                "AUTHOR-WRITTEN ADAPTATION, NOT YET REVIEWED")
    return "UNVERIFIED CASE, NOT CANON"


def play(case_path=DEFAULT_CASE):
    case = load_case(case_path)
    game = Adventure(case)
    print(case["title"] + " [DEVELOPMENT FIXTURE, NOT TOMI'S CANON]")
    print("Commands: number, notebook, consider ID, dismiss ID, save PATH, load PATH, quit")
    while True:
        print("\n" + game.scene["title"] + "\n" + game.scene["text"])
        if game.state["finished"]:
            print("\nCASE CLOSED. " + game.notebook())
            break
        for index, choice in enumerate(game.choices(), 1):
            print(str(index) + ". " + choice["label"])
        try:
            command = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break
        if command == "quit":
            break
        if command == "notebook":
            print(game.notebook())
        elif command.startswith(("consider ", "dismiss ")):
            action, _, hypothesis_id = command.partition(" ")
            try:
                (game.consider if action == "consider" else game.dismiss)(hypothesis_id.strip())
                print("Noted.")
            except ValueError as exc:
                print(exc)
        elif command.startswith("save "):
            try:
                game.save(command[5:].strip())
                print("Saved.")
            except OSError as exc:
                print("Unable to save:", exc)
        elif command.startswith("load "):
            try:
                game = Adventure.restore(case, command[5:].strip())
                print("Loaded.")
            except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
                print("Unable to load:", exc)
        else:
            try:
                game.choose(int(command))
            except (ValueError, TypeError):
                print("Choose a listed number, notebook, consider ID, dismiss ID, save PATH, load PATH or quit.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NoöPunk detective interactive fiction")
    parser.add_argument("--case", type=Path, default=DEFAULT_CASE, help="Reviewed case JSON")
    args = parser.parse_args()
    play(args.case)
