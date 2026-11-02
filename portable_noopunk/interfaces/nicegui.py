"""Optional illustrated web UI. Install NiceGUI separately to use it.

Launch: python -m portable_noopunk.interfaces.nicegui
"""
from portable_noopunk.adapters import LocalAdapter
from portable_noopunk.campaign import Game


def main() -> None:
    try:
        from nicegui import ui
    except ImportError as exc:
        raise SystemExit("Install optional dependency: pip install nicegui") from exc

    adapter = LocalAdapter(Game())
    with ui.column().classes("w-full max-w-2xl mx-auto gap-4"):
        ui.label("NOÖPUNK / UNSA").classes("text-3xl font-bold")
        location = ui.label()
        status = ui.label()
        narrative = ui.label("A new UNSA case awaits.")
        actions = ui.row().classes("flex-wrap gap-2")

        def refresh(message: str = "") -> None:
            snap = adapter.snapshot()
            location.text = "Location: " + snap["location"]
            status.text = "Clues: " + (", ".join(snap["clues"]) or "none")
            if message:
                narrative.text = message
            actions.clear()
            with actions:
                for action in adapter.available_actions():
                    ui.button(action.replace("_", " ").title(),
                              on_click=lambda a=action: refresh(adapter.dispatch(a).message))

        refresh()
    ui.run(host="127.0.0.1", port=8080, title="NoöPunk")


if __name__ == "__main__":
    main()
