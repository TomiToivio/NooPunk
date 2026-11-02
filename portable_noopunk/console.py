"""Run with: python -m portable_noopunk.console (stdlib only)."""
from pathlib import Path
from .campaign import Game, Action

SAVE_PATH = Path("noopunk_campaign_save.json")

def main() -> None:
    game = Game()
    print("NoöPunk: Lakkahaltia case (rules: src/rules/investigation.py)")
    print("Type an action, 'save', 'load', or 'quit'.")
    while True:
        print("\nAvailable:", ", ".join(game.available_actions()))
        try:
            command = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return
        if command == "quit":
            return
        if command == "save":
            SAVE_PATH.write_text(game.to_json(), encoding="utf-8")
            print("Saved.")
        elif command == "load":
            if not SAVE_PATH.exists():
                print("No save found.")
            else:
                try:
                    game = Game.from_json(SAVE_PATH.read_text(encoding="utf-8"))
                    print("Loaded.")
                except (ValueError, TypeError):
                    print("Save is invalid or incompatible.")
        else:
            result = game.apply(Action(command))
            print(result.message)
            if "case_completed" in result.events:
                print("Case recorded. Inspect status, save, or quit.")

if __name__ == "__main__":
    main()
