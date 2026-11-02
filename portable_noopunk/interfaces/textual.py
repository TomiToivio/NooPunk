"""Optional terminal GUI. Launch: python -m portable_noopunk.interfaces.textual."""
from portable_noopunk.adapters import LocalAdapter
from portable_noopunk.campaign import Game


def main() -> None:
    try:
        from textual.app import App, ComposeResult
        from textual.widgets import Header, Footer, Static, Button
        from textual.containers import VerticalScroll
    except ImportError as exc:
        raise SystemExit("Install optional dependency: pip install textual") from exc

    class NoopunkApp(App):
        TITLE = "NoöPunk / UNSA"

        def __init__(self):
            super().__init__()
            self.adapter = LocalAdapter(Game())

        def compose(self) -> ComposeResult:
            yield Header()
            yield Static("", id="state")
            yield Static("UNSA awaits your report.", id="narrative")
            yield VerticalScroll(id="actions")
            yield Footer()

        def on_mount(self) -> None:
            self.refresh_view()

        def refresh_view(self, message: str = "") -> None:
            state = self.adapter.snapshot()
            self.query_one("#state", Static).update(
                f"Location: {state['location']} | Clues: {', '.join(state['clues']) or 'none'}"
            )
            if message:
                self.query_one("#narrative", Static).update(message)
            actions = self.query_one("#actions", VerticalScroll)
            actions.remove_children()
            for action in self.adapter.available_actions():
                actions.mount(Button(action.replace("_", " ").title(), id="action-" + action))

        def on_button_pressed(self, event: Button.Pressed) -> None:
            action = event.button.id.removeprefix("action-")
            self.refresh_view(self.adapter.dispatch(action).message)

    NoopunkApp().run()


if __name__ == "__main__":
    main()
