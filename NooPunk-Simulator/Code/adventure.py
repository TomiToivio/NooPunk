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
    return case


class Adventure:
    """One tiny scene/choice notebook runner; no RNG, combat, levels or rules engine."""

    def __init__(self, case, state=None):
        self.case = case
        self.state = state if state is not None else {
            "version": SAVE_VERSION, "case_id": case["id"], "scene": case["start"],
            "clues": [], "flags": {}, "history": [], "finished": False
        }
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

    def notebook(self):
        lines = ["CASE NOTEBOOK", "-------------"]
        if not self.state["clues"]:
            lines.append("No evidence recorded yet.")
        else:
            for clue in self.state["clues"]:
                lines.append("* " + self.case["clues"][clue])
        lines.append("Hypotheses (not established facts):")
        for hypothesis in self.case.get("hypotheses", []):
            if set(hypothesis.get("requires", [])).issubset(self.state["clues"]):
                lines.append("* " + hypothesis["text"])
        lines.append("Decisions logged: " + str(len(self.state["history"])))
        return "\n".join(lines)

    def save(self, path):
        Path(path).write_text(json.dumps(self.state, indent=2, ensure_ascii=False) + "\n",
                              encoding="utf-8")

    @classmethod
    def restore(cls, case, path):
        return cls(case, json.loads(Path(path).read_text(encoding="utf-8")))


def play(case_path=DEFAULT_CASE):
    case = load_case(case_path)
    game = Adventure(case)
    print(case["title"] + " [DEVELOPMENT FIXTURE, NOT TOMI'S CANON]")
    print("Commands: number, notebook, save PATH, load PATH, quit")
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
                print("Choose a listed number, notebook, save PATH, load PATH or quit.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NoöPunk detective interactive fiction")
    parser.add_argument("--case", type=Path, default=DEFAULT_CASE, help="Reviewed case JSON")
    args = parser.parse_args()
    play(args.case)
