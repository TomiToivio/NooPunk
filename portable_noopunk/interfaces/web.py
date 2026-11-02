"""Dependency-free browser frontend: python -m portable_noopunk.interfaces.web.

Local-only reference web application. It is not an authenticated public server.
"""
from __future__ import annotations

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import RLock
from urllib.parse import parse_qs
from portable_noopunk.adapters import LocalAdapter
from portable_noopunk.campaign import Game


def render(adapter: LocalAdapter, message: str = "") -> str:
    state = adapter.snapshot()
    controls = "\n".join(
        '<form method="post"><button type="submit" name="action" value="%s">%s</button></form>'
        % (escape(action, quote=True), escape(action.replace("_", " ").title()))
        for action in adapter.available_actions()
    )
    clues = ", ".join(state["clues"]) or "None"
    return """<!doctype html><html lang="en"><meta charset="utf-8">
<title>NoöPunk: UNSA</title>
<style>body{background:#171329;color:#e4ddf3;font:18px system-ui;max-width:780px;margin:3rem auto;padding:1rem}
button{background:#37265c;color:#fff;border:1px solid #ab87d9;padding:.7rem 1rem;cursor:pointer}
form{display:inline-block;margin:.25rem} .panel{border:1px solid #66588b;padding:1rem;margin:1rem 0}</style>
<h1>NoöPunk / UNSA</h1>
<div class="panel"><p>Location: %s</p><p>Clues: %s</p><p>Case: %s</p><p>Sidequest: %s</p></div>
<div role="status" class="panel">%s</div><div class="panel">%s</div></html>""" % (
        escape(state["location"]), escape(clues),
        "Closed" if state["finished"] else "Open",
        "Done" if state["sidequest_done"] else "Open",
        escape(message), controls
    )


def handler_factory(adapter: LocalAdapter):
    """Share exactly one local campaign session; do not expose on public networks."""
    lock = RLock()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/":
                self.send_error(404)
                return
            self.respond("")

        def do_POST(self):
            if self.path != "/":
                self.send_error(404)
                return
            size = int(self.headers.get("Content-Length", "0"))
            if size > 4096 or size < 0:
                self.send_error(413)
                return
            form = parse_qs(self.rfile.read(size).decode("utf-8"))
            action = form.get("action", [""])[0]
            with lock:
                message = adapter.dispatch(action).message if action in adapter.available_actions() else "Invalid action."
                self.respond(message)

        def respond(self, message: str):
            with lock:
                payload = render(adapter, message).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

    return Handler


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8765), handler_factory(LocalAdapter(Game())))
    print("NoöPunk local browser: http://127.0.0.1:8765/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
