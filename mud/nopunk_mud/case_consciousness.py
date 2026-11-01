"""Deterministic UNSA consciousness-assessment case (#985).

A three-scene interview used in the MUD. Choices change the signals and the tone, but every path
yields a usable core clue: the case cannot dead-end on a bad roll or a rude answer.
"""
from __future__ import annotations

from dataclasses import dataclass

from nopunk_mud.consciousness import Assessment, Signals, assess

SUBJECT = "Aino Lahtinen, night-shift dispatcher, Lakkahaltia warehouse"

SCENES = (
    {
        "id": "intake",
        "prompt": "She describes the night the sky opened. Her account is calm, almost rehearsed.",
        "choices": {
            "press": ({"affect": -1, "coherence": 1}, "You press on the eleven missing seconds."),
            "listen": ({"affect": 1, "coherence": 0}, "You let the silence do the work."),
        },
        "clue": "Her timeline has eleven seconds that no camera recorded.",
    },
    {
        "id": "affect",
        "prompt": "You ask what she felt. She smiles before answering, then describes terror.",
        "choices": {
            "mirror": ({"affect": 1, "empathy": 1}, "You name the fear without accusing her."),
            "confront": ({"affect": -2, "empathy": -1}, "You tell her the smile came first."),
        },
        "clue": "The smile precedes the described terror; the affect is out of order.",
    },
    {
        "id": "telemetry",
        "prompt": "The BCI pad shows a spike she denies. The room is very quiet.",
        "choices": {
            "show": ({"bci": -1, "coherence": 1}, "You turn the pad toward her."),
            "conceal": ({"bci": 1, "coherence": -1}, "You keep the pad to yourself and watch."),
        },
        "clue": "The telemetry spikes at the exact moment her account goes flat.",
    },
)


@dataclass(frozen=True)
class CaseResult:
    assessment: Assessment
    clues: tuple[str, ...]
    transcript: tuple[str, ...]


def run_case(choices: tuple[str, str, str] = ("press", "mirror", "show")) -> CaseResult:
    if len(choices) != len(SCENES):
        raise ValueError("the interview has three scenes")
    signals = {"affect": 0, "coherence": 0, "bci": 0, "empathy": 0}
    clues: list[str] = []
    transcript: list[str] = []
    for scene, choice in zip(SCENES, choices):
        if choice not in scene["choices"]:
            raise ValueError(f"unknown choice {choice!r} in {scene['id']}")
        delta, line = scene["choices"][choice]
        for channel, value in delta.items():
            signals[channel] = max(-2, min(2, signals[channel] + value))
        clues.append(scene["clue"])
        transcript.append(line)
    result = assess(Signals(**signals))
    # The core clue is the case's, not the roll's: always present.
    return CaseResult(result, tuple(clues), tuple(transcript))
