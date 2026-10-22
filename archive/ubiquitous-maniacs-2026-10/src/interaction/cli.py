"""CLI-käyttöliittymä vastaanottokohtaukselle.

Minimaalinen tekstipohjainen esitystapa, Citizen Sleeper -henkinen.
"""

from __future__ import annotations

from .state import EnrollmentStatus, ReceptionGame
from .dialogue import Choice, DialogueNode, get_node, apply_choice


def render_scene(game: ReceptionGame, node: DialogueNode) -> None:
    """Näytä kohtauksen tilanne pelaajalle."""
    print()
    print("=" * 60)
    print()

    if node.narration:
        print(node.narration)
        print()

    if node.npc_name:
        print(f"  {node.npc_name}:")
        print(f"  \"{node.npc_text}\"")
        print()

    print(f"  Romppainen — Suspicion: {game.receptionist.suspicion}  "
          f"Trust: {game.receptionist.trust}")
    print()

    for i, choice in enumerate(node.choices, 1):
        label = f"  [{i}] {choice.text}"
        print(label)
    print()


def run_reception_scene(seed: int | None = None) -> EnrollmentStatus:
    """Suorita vastaanottokohtaus. Palauta lopputuloksen.

    Args:
        seed: Jos annettu, aseta random seed determinististä testausta varten.
    """
    if seed is not None:
        import random
        random.seed(seed)

    game = ReceptionGame()

    while not game.is_finished:
        node = get_node(game.scene.current_node)
        if node is None or not node.choices:
            break

        render_scene(game, node)

        # Pelaajan valinta
        while True:
            try:
                raw = input("  Valinta > ").strip()
                idx = int(raw) - 1
                if 0 <= idx < len(node.choices):
                    break
                print("  Epäkelpo valinta.")
            except (ValueError, EOFError):
                print("  Epäkelpo valinta.")

        choice = node.choices[idx]
        text, success = apply_choice(game, choice)

        # Näytä väliteksti
        if text:
            print()
            print(f"  {text}")
            if success is True:
                print("  [ONNISTUI]")
            elif success is False:
                print("  [EPÄONNISTUI]")
            print()

    # Lopputulos
    status = game.scene.enrollment_status
    print()
    print("=" * 60)
    print()
    if status == EnrollmentStatus.ACCEPTED:
        print("  TULOS: TEIDÄT ON VALITTU KOKEESEEN")
        print("  Dahl laskee lomakenipun eteesi. Kohtaus päättyy ennen podia.")
    elif status == EnrollmentStatus.ADDITIONAL_SCREENING:
        print("  Tuloksen: LISÄSELVITYSTÄ VAADITAAN")
        print("  Dahl katsoo sinua epäillen. 'Tarvitsemme "
              "lisätietoja ennen kuin voimme jatkaa.'")
    elif status == EnrollmentStatus.REJECTED:
        print("  Tuloksen: HYLÄTTY")
        print("  Dahl sulkee näytön. 'Valitettavasti en voi "
              "hyväksyä teitä tähän ohjelmaan.'")
    print()
    print(f"  Lopullinen Suspicion: {game.receptionist.suspicion}")
    print(f"  Lopullinen Trust: {game.receptionist.trust}")
    print()
    print("=" * 60)

    return status
