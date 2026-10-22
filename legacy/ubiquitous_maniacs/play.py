#!/usr/bin/env python3
"""Noöpunk: Ubiquitous Maniacs — kaksipäiväinen terminaalikampanja.

Käyttö:
    python play.py                  Pelaa päivä 1 oletusasetuksin
    python play.py --seed 42        Deterministinen siemen
    python play.py --load save.json Lataa tallennus
    python play.py --help           Näytä kaikki valinnat

Komennot pelin aikana:
    1, 2, 3...     Valitse toiminto
    s              Sosiaalinen verkko
    i              Löydetty tieto
    c              Hahmon tila
    h              Psykotroninen hacking-konsoli (kun saatavilla)
    m              NPC-muistit (mitä he muistavat sinusta)
    n              Anna NPC:iden toimia sosiaalisessa verkossa
    save           Tallenna peli
    quit           Poistu

16 Psyche · C.G. Jung City and University · UFAB
"Die C.-G.-Jung-Kolonie der Europäischen Union auf dem Asteroiden 16 Psyche"
"""

from __future__ import annotations

import argparse
import json
import random as _random
from pathlib import Path

from src.game import GameState
from src.hacking import LayeredHackingSession
from src.rpg import ResultTier


BANNER = r"""
  ╔══════════════════════════════════════════════════════════════╗
  ║  N Ö Ö P U N K :  U B I Q U I T O U S   M A N I A C S       ║
  ║  ─────────────────────────────────────────────────────────── ║
  ║  1974→2026 — PSI / AGI / DISCLOSURE / QIP                  ║
  ║  16 Psyche · UFAB · [PLAYABLE CAMPAIGN]                    ║
  ╚══════════════════════════════════════════════════════════════╝
"""

INSTITUTIONAL_OPENING = """  16 Psyche ei rakennettu sairaalaksi.
  Ensin louhittiin metallit, sitten muistot ja lopuksi potilaat.
  C.G. Jung City kutsuu tätä hoitoketjuksi.
  UFAB kutsuu sitä vertikaaliseksi integraatioksi."""

# Kosminen kertoja — Maniacin tyylinen avaus joka yhdistää mikrotason
# (CAN, tietoisuus) ja makrotason (C.G. Jung City, potilas). Kertoja
# puhuu hypoteeseja ja korollaareja kuin tieteellinen paperi, mutta
# liukuu sitten arkeen. Näytetään INSTITUTIONAL_OPENINGin jälkeen.
COSMIC_OPENING = """  ┌──────────────────────────────────────────────────────────────┐
  │  HYPOTEESI: Jokainen sielu etsii yhteyttä.                   │
  │  KOROLLAARI: Mielimme eivät tiedä tästä etsinnästä.          │
  │                                                              │
  │  4,6 miljardia vuotta sitten Pallas-kappale törmäsi          │
  │  protoplaneettaan. Metallisydän levisi painovoimaan          │
  │  kuin pisara maitoa kahvissa. Tuhannet tonnit platinaa      │
  │  ja rautaa jähtyivät pimeyteen. Ehkä se oli sattumaa.        │
  │  Ehkä se oli välttämätöntä.                                  │
  │                                                              │
  │  16 Psyche. Asteroidivyöhyke. C.G. Jung City.                │
  │  Sairaala, lääketehdas, yliopisto — sama käytävä,            │
  │  sama budjetti, sama valhe.                                  │
  │                                                              │
  │  Tämä totuus ulottuu myös ihmisen sydämeen.                  │
  └──────────────────────────────────────────────────────────────┘"""

UFAB_ADS = [
    "UFAB 80MG — Kun minä pitää, minä pitää. (UFAB Pharma GmbH)",
    "C.G. Jung -yliopisto — Tie itseen alkaa tästä. Hae nyt.",
    "UFAB Buddy™ — Maksamme ostoksesi. Kuuntelemme mielellämme.",
    "Proxy Ystävä™ — Yksin ei tarvitse olla. Vuokrataan ystävä.",
    "EURODEF Terveyssalaisuus™ — Tietosi ovat turvassa. Todennäköisesti.",
    "Toiveiden Rekisteri — He tietävät teidät paremmin kuin te.",
    "Puhdas Menneisyys — Puhdistamme tiedoston. Muisto laskutetaan erikseen.",
]

RAGNAROK_COMMENTS = [
    "Ragnarök tietää. Ragnarök aina tietää.",
    "Ragnarök on seurannut 882 mieltä. Tämä on mielen 883.",
    "Lomake ei ole byrokratiaa. Lomake on rukous.",
    "Suomalainen. Ruotsalainen. Saksalainen. Kaikki potilaita.",
    "Podi humisee. C.G. Jung -instituutti ei koskaan nuku.",
]

# Päivän 1 genreominaisuudet: byrokraattinen komedia + Jungilainen
# surrealismi + psykotroniikka. Tekstit ovat suomeksi, koska Romppainen
# on suomalainen ja UFABin virallinen kieli on ruotsi/saksa/englanti —
# mutta pelaajan sisäinen monologi on äidinkieli.

ROOT = Path(__file__).resolve().parent
CHARACTER_PATH = ROOT / "data/rpg/characters/romppainen_day_1.md"
SCENARIO_PATH = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"
DAY_2_SCENARIO_PATH = ROOT / "data/rpg/scenarios/day_2_kiimaiset_poliisit.json"
HACKING_SCENARIO_PATH = ROOT / "data/hacking/sleeping_patient.json"
SAVE_DIR = ROOT / "saves"

CAMPAIGN_SCENARIOS = {
    "day_1_arrival_and_entanglement": SCENARIO_PATH,
    "day_2_kiimaiset_poliisit": DAY_2_SCENARIO_PATH,
}
CAMPAIGN_NEXT = {
    "day_1_arrival_and_entanglement": DAY_2_SCENARIO_PATH,
}


def scenario_path_for_save(path: str | Path, fallback: str | Path = SCENARIO_PATH) -> Path:
    """Resolve a campaign scenario from an integrated or legacy RPG save."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rpg = data.get("rpg", data) if isinstance(data, dict) else {}
    scenario_id = rpg.get("scenario_id") if isinstance(rpg, dict) else None
    return CAMPAIGN_SCENARIOS.get(str(scenario_id), Path(fallback))


def advance_campaign_if_ready(state: GameState) -> bool:
    """Advance a completed campaign chapter while preserving integrated state."""
    if not state.rpg.is_complete:
        return False
    next_scenario = CAMPAIGN_NEXT.get(state.rpg.scenario.id)
    if next_scenario is None:
        return False
    state.transition_to_scenario(next_scenario)
    return True


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def print_separator(char: str = "─", width: int = 60) -> None:
    print(char * width)


def tier_label(tier: ResultTier) -> str:
    """Noöpunk-tyyliset tulosten nimet — Fate + Jungilainen sävy."""
    labels = {
        ResultTier.CRITICAL_SUCCESS: "★ SINKKO — Kollektiivinen alitajunta myötäilee",
        ResultTier.SUCCESS: "✓ ONNISTUMINEN — Persona pitää",
        ResultTier.COSTLY_SUCCESS: "⚠ ONNISTUMINEN KUSTANNUKSIN — Halkeama peitepersoonassa",
        ResultTier.FAILURE: "✗ EPÄONNISTUMINEN — UFAB 80MG kutsuu",
        ResultTier.CATASTROPHIC_FAILURE: "✗✗ KATASTROFI — Varjo irtoaa",
    }
    return labels.get(tier, str(tier))


def render_scene(state: GameState) -> None:
    scene = state.rpg.scene
    node = state.rpg.dialogue_node

    print_separator("═")
    print(f"  {scene.title}")
    print(f"  {scene.location} · {scene.phase or ''}")
    print_separator("═")
    print()

    if scene.description:
        print(scene.description)
        print()

    if node:
        if node.speaker:
            print(f"  [{node.speaker}]")
        if node.text:
            print(f"  {node.text}")
        print()

    if state.rpg.seed is not None:
        ad_rng = _random.Random(state.rpg.seed + state.social.turn)
        if ad_rng.random() < 0.3:
            print(f"  ▌ {ad_rng.choice(UFAB_ADS)}")
            print()

        comment_rng = _random.Random(state.rpg.seed * 7 + state.social.turn * 3)
        if comment_rng.random() < 0.2:
            print(f"  ⟨Ragnarök⟩ {comment_rng.choice(RAGNAROK_COMMENTS)}")
            print()

    # NPC-muistit: osallistujat, jotka muistavat pelaajan, viittaavat
    # viimeisimpään muistoonsa jo scenen alussa ("reference them in later
    # scenes"). Koko muistilokin näkyy erillisellä m-komennolla.
    memory_lines = state.participant_memory_lines()
    for name, memory in memory_lines:
        sign = "+" if memory["valence"] > 0 else "−" if memory["valence"] < 0 else "·"
        print(f"  ↳ {name} muistaa [{sign}]: {memory['summary']}")
    if memory_lines:
        print()


def render_interactions(state: GameState) -> None:
    interactions = state.rpg.available_interactions()
    if not interactions:
        print("  (Ei valittavia toimintoja. Odota tai kokeile komentoa.)")
        return

    for i, interaction in enumerate(interactions, 1):
        label = interaction.label
        if interaction.check:
            skill = f" + {interaction.check.skill}" if interaction.check.skill else ""
            label = f"[{interaction.check.attribute}{skill}] {label}"
        print(f"  [{i}] {label}")
    print()


def render_status(state: GameState) -> None:
    char = state.rpg.character
    print_separator("─")
    print(f"  Hahmo: {char.name}")
    print(f"  Mietentilat: {', '.join(sorted(state.rpg.state.conditions)) or '—'}")
    print(f"  Aspektit: {', '.join(sorted(char.aspects)) or '—'}")
    if state.rpg.state.consequences:
        print(f"  Seuraukset: {', '.join(state.rpg.state.consequences)}")
    if state.rpg.state.relationships:
        rels = ", ".join(f"{k} {v:+d}" for k, v in sorted(state.rpg.state.relationships.items()))
        print(f"  Suhteet: {rels}")
    if state.hacking.available:
        print(f"  Psykotroniikka: SAATAVILLA (hälytys={state.hacking.alert_level})")
    print_separator("─")
    print()


def render_social(state: GameState) -> None:
    print_separator("─")
    print("  SOSIAALINEN VERKKO — C.G. Jung City")
    print_separator("─")

    observer = state._id_map.get(state.rpg.character.id, state.rpg.character.id)
    print("\n  Tunnetut hahmot:")
    for char in state.social.known_characters(observer):
        mem_count = len(state.social.memories(char["id"]))
        mem_str = f"  muistoja={mem_count}" if mem_count else ""
        print(f"    {char['id']:20s}  {char['name']:30s}  mieliala={char['mood']}{mem_str}")

    print("\n  Suhteet (sinun näkökulma):")
    for rel in state.social.visible_relationships(observer):
        if rel["source"] == observer:
            dims = [f"{k}={v}" for k, v in rel.items()
                    if k in ("trust", "attraction", "fear", "suspicion", "authority", "familiarity")
                    and v != 0]
            if dims:
                print(f"    -> {rel['target']:20s}  {', '.join(dims)}")

    recent = state.social.recent_changes(5)
    if recent:
        print("\n  Viimeisimmät muutokset:")
        for change in recent:
            print(f"    K{change['turn']}: {change['source']} -> {change['target']} "
                  f"{change['dimension']} {change['delta']:+d} (={change['new_value']})")

    remembered = []
    for char in state.social.known_characters(observer):
        if char["id"] == observer:
            continue
        memories = state.social.memories(char["id"], limit=1)
        if memories:
            remembered.append((char["name"], memories[0]))
    if remembered:
        print("\n  Mitä he muistavat sinusta:")
        for name, memory in remembered:
            sign = "+" if memory["valence"] > 0 else "−" if memory["valence"] < 0 else "·"
            print(f"    {name}: [{sign}] {memory['summary']}")

    hidden_count = state.social.hidden_edge_count
    if hidden_count:
        print(f"\n  Piilossa olevia suhteita: {hidden_count} (Ragnarök valvoo?)")
    print()


def render_info(state: GameState) -> None:
    print_separator("─")
    print("  LÖYDETTY TIETO — Arkisto ja havainnot")
    print_separator("─")
    info = sorted(state.rpg.state.known_information)
    if not info:
        print("  (Et ole vielä löytänyt mitään merkittävää.)")
    for item in info:
        print(f"  • {item}")
    print()

    flags = state.rpg.state.campaign_flags
    if flags:
        print("  LIPUT (Campaign Flags):")
        for key, value in sorted(flags.items()):
            print(f"    {key} = {value}")
        print()


def render_memories(state: GameState) -> None:
    """Näytä kaikkien NPC:iden muistit pelaajasta."""
    print_separator("─")
    print("  MUISTIJÄLKET — Mitä he muistavat sinusta")
    print_separator("─")

    observer = state._id_map.get(state.rpg.character.id, state.rpg.character.id)
    any_memories = False

    for char in state.social.known_characters(observer):
        cid = char["id"]
        if cid == observer:
            continue
        memories = state.social.memories(cid)
        if not memories:
            continue
        any_memories = True
        name = char["name"]
        print(f"\n  {name} ({cid}):")
        for mem in memories:
            sign = "+" if mem["valence"] > 0 else "−" if mem["valence"] < 0 else "·"
            tags = ", ".join(mem.get("tags", []))
            print(f"    K{mem['turn']} [{sign}] {mem['summary']}")
            if tags:
                print(f"      tagit: {tags}")

    if not any_memories:
        print("\n  (Kukaan ei muista sinua vielä. Anna heidän nähdä jotain.)")
    print()


def render_hacking(state: GameState) -> None:
    print_separator("─")
    print("  PSYKOTRONIIKKA — Conscious Agent Network")
    print_separator("─")
    if not state.hacking.available:
        print("  Psykotroniikka ei ole vielä saatavilla.")
        print("  Saatavuus avautuu, kun löydät todisteita")
        print("  piilevistä kyberneettisistä tai noetoottisista järjestelmistä.")
        print()
        return

    session = get_or_create_hacking_session(state)
    sync_hacking_state_from_session(state, session)
    snapshot = session.snapshot()

    print("  Status: SAATAVILLA")
    print(f"  Yritykset: {state.hacking.attempts}  Onnistuneet: {state.hacking.successes}  "
          f"Epäonnistuneet: {state.hacking.failures}")
    print(f"  Hälytystaso: {state.hacking.alert_level}")
    print(f"  Sessio: {snapshot['status']}  ·  Nykyinen node: {snapshot['current_node']}")
    if state.hacking.discovered_nodes:
        print(f"  Löydetyt solmut: {', '.join(sorted(state.hacking.discovered_nodes))}")
    if state.hacking.hacked_nodes:
        print(f"  Hackatut solmut: {', '.join(sorted(state.hacking.hacked_nodes))}")
    print()
    print("  Komento h avaa interaktiivisen hacking-konsolin.")
    print()


def get_or_create_hacking_session(state: GameState) -> LayeredHackingSession:
    session = getattr(state, "_layered_hacking_session", None)
    if session is None:
        session = LayeredHackingSession.from_json(state.rpg.character, HACKING_SCENARIO_PATH)
        setattr(state, "_layered_hacking_session", session)
    return session


def sync_hacking_state_from_session(state: GameState, session: LayeredHackingSession) -> None:
    state.hacking.available = True
    state.hacking.alert_level = session.alert
    state.hacking.attempts = len([entry for entry in session.history if entry["action"] != "retreat"])
    state.hacking.successes = len([entry for entry in session.history if entry["success"]])
    state.hacking.failures = len([entry for entry in session.history if not entry["success"]])
    state.hacking.discovered_nodes = set(session.known_nodes)
    state.hacking.hacked_nodes = set(session.exploited_nodes)


def apply_hacking_transfer_once(state: GameState, session: LayeredHackingSession) -> bool:
    key = f"hacking_transfer_applied_{session.metadata.get('id', 'default')}"
    if state.rpg.state.campaign_flags.get(key):
        return False
    session.transfer.apply(state.rpg.state, state.rpg.character)
    state.rpg.state.campaign_flags[key] = True
    state._sync_social_from_rpg()
    return True


def _select_node(snapshot: dict, prompt: str) -> str | None:
    nodes = snapshot["known_nodes"]
    if not nodes:
        print("  Ei näkyviä nodeja.")
        return None
    print("\n  Nodet:")
    for idx, node in enumerate(nodes, 1):
        desc = node.get("description", "")
        if desc:
            desc = f" — {desc[:60]}"
        print(f"    [{idx}] {node['id']} ({node['layer']} / {node['access']}){desc}")
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        choice = int(raw) - 1
    except ValueError:
        print("  Epäkelpo valinta.")
        return None
    if choice < 0 or choice >= len(nodes):
        print("  Epäkelpo valinta.")
        return None
    return str(nodes[choice]["id"])


def _prompt_roll() -> int | None:
    raw = input("  4dF-tulos [-4..4, Enter=automaattinen] > ").strip()
    if not raw:
        return None
    try:
        roll = int(raw)
    except ValueError:
        print("  Epäkelpo heitto, käytetään automaattista.")
        return None
    if roll < -4 or roll > 4:
        print("  Heiton oltava välillä -4..4, käytetään automaattista.")
        return None
    return roll


def _select_tool(snapshot: dict, action: str) -> str | None:
    """Valinnainen työkalun valinta. Palauttaa None jos ei valita."""
    tools = snapshot.get("tools", [])
    if not tools:
        return None
    print("\n  Työkalut (valinnainen):")
    print("    [0] Ei työkalua")
    for idx, tool in enumerate(tools, 1):
        print(f"    [{idx}] {tool['label']} (+{tool['bonus']}) — {', '.join(tool['layers'])} / {', '.join(tool['actions'])}")
    raw = input("  Työkalu # > ").strip()
    if not raw or raw == "0":
        return None
    try:
        choice = int(raw) - 1
    except ValueError:
        print("  Epäkelpo valinta, ei työkalua.")
        return None
    if choice < 0 or choice >= len(tools):
        print("  Epäkelpo valinta, ei työkalua.")
        return None
    return str(tools[choice]["id"])


def _select_aspect(snapshot: dict, character) -> str | None:
    """Valinnainen aspektin invokointi. Vaatii Fate-pisteen."""
    aspects = sorted(set(character.aspects) | set(snapshot.get("aspects", [])))
    if not aspects:
        return None
    fate_points = character.resources.get("fate_points", 0)
    if fate_points < 1:
        print(f"\n  Ei Fate-pisteitä (tarvitaan invokointiin).")
        return None
    print(f"\n  Aspektit (Fate-pisteitä: {fate_points}):")
    print("    [0] Ei invokointia")
    for idx, asp in enumerate(aspects, 1):
        print(f"    [{idx}] {asp}")
    raw = input("  Aspekti # > ").strip()
    if not raw or raw == "0":
        return None
    try:
        choice = int(raw) - 1
    except ValueError:
        print("  Epäkelpo valinta, ei invokointia.")
        return None
    if choice < 0 or choice >= len(aspects):
        print("  Epäkelpo valinta, ei invokointia.")
        return None
    return aspects[choice]


def _render_hacking_map(snapshot: dict) -> None:
    """Näytä nykyinen hacking-tila: solmut, kaaret, resonanssivaihtoehdot."""
    print_separator("─")
    print("  VERKKOKARTTA")
    print_separator("─")
    nodes = snapshot["known_nodes"]
    if nodes:
        print("  Solmut:")
        for node in nodes:
            marker = " ◀" if node["id"] == snapshot["current_node"] else ""
            vulns = node.get("vulnerabilities", [])
            vuln_str = f" [haavoittuvuudet: {', '.join(vulns)}]" if vulns else ""
            print(f"    {node['id']:30s} {node['layer']:12s} {node['access']:12s}{vuln_str}{marker}")
    else:
        print("  (Ei tunnettuja solmuja.)")

    edges = snapshot.get("discovered_edges", [])
    if edges:
        print("\n  Löydetyt kaaret:")
        for edge in edges:
            print(f"    {edge['source']} — {edge['target']} ({edge.get('edge_type', '?')})")

    resonance = snapshot.get("resonance_options", [])
    if resonance:
        print("\n  Resonanssivaihtoehdot nykyisestä solmusta:")
        for opt in resonance:
            known = "" if opt["target_known"] else " (paljastamaton)"
            print(f"    → {opt['target']:30s} {opt['edge_type']:30s} → {opt['target_layer']}{known}")
    print()


def _render_hacking_result(result) -> None:
    print(f"\n  {result.summary}")
    if result.check:
        check = result.check.check
        print(f"  {tier_label(check.tier)}")
        print(f"  Heitto {check.roll:+d} · summa {check.total} vs {check.difficulty} · marginaali {check.margin:+d}")
    if result.revealed_nodes:
        print(f"  Paljastui: {', '.join(result.revealed_nodes)}")
    if result.objective_updates:
        print(f"  Tavoitteet: {', '.join(result.objective_updates)}")
    if result.created_aspect:
        print(f"  Luotu aspekti: {result.created_aspect}")
    if result.access_level:
        print(f"  Pääsytaso: {result.access_level.name}")
    print(f"  Paine: alert +{result.alert_delta}, trace +{result.trace_delta}, feedback +{result.stress_delta}")


def run_hacking_console(state: GameState) -> None:
    if not state.hacking.available:
        render_hacking(state)
        input("  [Paina Enter jatkaaksesi...]")
        return

    session = get_or_create_hacking_session(state)

    while True:
        clear_screen()
        print(BANNER)
        print_separator("═")
        print("  PSYKOTRONINEN HACKING-KONSOLI")
        print_separator("═")
        snapshot = session.snapshot()
        sync_hacking_state_from_session(state, session)
        print(f"  Tavoite: {snapshot['objective']}")
        print(f"  Status: {snapshot['status']}  |  Node: {snapshot['current_node']} ({snapshot['current_layer']})")
        print(f"  Alert={snapshot['alert']}  Trace={snapshot['trace']}  Feedback={snapshot['feedback']}  Instability={snapshot['instability']}")
        if snapshot["completed_objectives"]:
            print(f"  Valmiit tavoitteet: {', '.join(snapshot['completed_objectives'])}")
        if snapshot.get("aspects"):
            print(f"  Aktiiviset aspektit: {', '.join(snapshot['aspects'])}")
        print()

        _render_hacking_map(snapshot)

        print("  [1] Observe       — Tutki solmua, paljasta naapurit")
        print("  [2] Create access — Pääsy solmuun (vaatii yhteyden)")
        print("  [3] Exploit       — Hyödynnä solmu (vaatii Access-tason)")
        print("  [4] Resonate      — Psykotroninen resonanssi (cross-layer)")
        print("  [5] Create advantage — Luo tilanneetu/aspekti")
        print("  [6] Defend        — Vähennä hälytystä/jäljet")
        print("  [7] Overcome      — Ohita este")
        print("  [8] Attack        — Hyökkää kohdejärjestelmää")
        print("  [9] Retreat       — Irrottaudu, säilytä seuraukset")
        print("  [0] Takaisin peliin")

        if session.is_terminal:
            if apply_hacking_transfer_once(state, session):
                print("\n  Seuraukset siirrettiin RPG-tilaan.")
            print("\n  Sessio on päättynyt. Paina Enter palataksesi.")
            input("  > ")
            return

        raw = input("\n  Valinta > ").strip().lower()
        if raw in {"0", "q", "quit", "exit"}:
            return

        result = None
        try:
            if raw == "1":
                target = _select_node(snapshot, "  Observe node # > ")
                if target is None:
                    continue
                tool = _select_tool(snapshot, "observe")
                aspect = _select_aspect(snapshot, state.rpg.character)
                result = session.observe(target, roll=_prompt_roll(), tool_id=tool, invoke_aspect=aspect)
            elif raw == "2":
                source = _select_node(snapshot, "  Source node # > ")
                if source is None:
                    continue
                target = _select_node(snapshot, "  Target node # > ")
                if target is None:
                    continue
                tool = _select_tool(snapshot, "create_access")
                aspect = _select_aspect(snapshot, state.rpg.character)
                result = session.create_access(source, target, roll=_prompt_roll(), tool_id=tool, invoke_aspect=aspect)
            elif raw == "3":
                target = _select_node(snapshot, "  Exploit node # > ")
                if target is None:
                    continue
                tool = _select_tool(snapshot, "exploit")
                aspect = _select_aspect(snapshot, state.rpg.character)
                result = session.exploit(target, roll=_prompt_roll(), tool_id=tool, invoke_aspect=aspect)
            elif raw == "4":
                source = _select_node(snapshot, "  Source node # > ")
                if source is None:
                    continue
                target = _select_node(snapshot, "  Resonance target # > ")
                if target is None:
                    continue
                tool = _select_tool(snapshot, "resonate")
                aspect = _select_aspect(snapshot, state.rpg.character)
                result = session.resonate(source, target, roll=_prompt_roll(), tool_id=tool, invoke_aspect=aspect)
            elif raw == "5":
                target = _select_node(snapshot, "  Create advantage on node # > ")
                if target is None:
                    continue
                aspect_name = input("  Aspektin nimi > ").strip()
                if not aspect_name:
                    print("  Aspektin nimi puuttuu.")
                    input("  [Paina Enter jatkaaksesi...]")
                    continue
                tool = _select_tool(snapshot, "create_advantage")
                invoke = _select_aspect(snapshot, state.rpg.character)
                result = session.create_advantage(target, aspect_name, roll=_prompt_roll(), tool_id=tool, invoke_aspect=invoke)
            elif raw == "6":
                target = _select_node(snapshot, "  Defend node # > ")
                if target is None:
                    continue
                tool = _select_tool(snapshot, "defend")
                aspect = _select_aspect(snapshot, state.rpg.character)
                result = session.defend(target, roll=_prompt_roll(), tool_id=tool, invoke_aspect=aspect)
            elif raw == "7":
                target = _select_node(snapshot, "  Overcome node # > ")
                if target is None:
                    continue
                tool = _select_tool(snapshot, "overcome")
                aspect = _select_aspect(snapshot, state.rpg.character)
                result = session.overcome(target, roll=_prompt_roll(), tool_id=tool, invoke_aspect=aspect)
            elif raw == "8":
                target = _select_node(snapshot, "  Attack node # > ")
                if target is None:
                    continue
                tool = _select_tool(snapshot, "attack")
                aspect = _select_aspect(snapshot, state.rpg.character)
                result = session.attack(target, roll=_prompt_roll(), tool_id=tool, invoke_aspect=aspect)
            elif raw == "9":
                result = session.retreat()
            else:
                print("  Epäkelpo valinta.")
                input("  [Paina Enter jatkaaksesi...]")
                continue
        except ValueError as exc:
            print(f"\n  Toiminto estetty: {exc}")
            input("  [Paina Enter jatkaaksesi...]")
            continue

        if result is not None:
            _render_hacking_result(result)
            sync_hacking_state_from_session(state, session)
            input("\n  [Paina Enter jatkaaksesi...]")


def handle_result(state: GameState, result) -> None:
    if result.check:
        check = result.check
        print(f"\n  {tier_label(check.tier)}")
        print(f"  4dF: {check.dice} = {check.roll:+d}")
        print(f"  Attribuutti: {check.attribute:+d}  Taito: {check.skill:+d}  "
              f"Tilanne: {check.situational_modifier:+d}")
        print(f"  Summa: {check.total}  vs  Vaikeus: {check.difficulty}  "
              f"Marginaali: {check.margin:+d}")
        print()

    if result.outcome.text:
        print(f"  {result.outcome.text}")
        print()

    new_info = result.outcome.add_information
    if new_info:
        print("  » Uutta tietoa:")
        for item in sorted(new_info):
            print(f"    • {item}")
        print()

    if result.outcome.relationship_changes:
        print("  » Suhteet muuttuivat:")
        for target, delta in result.outcome.relationship_changes.items():
            print(f"    {target}: {delta:+d}")
        print()

    if result.outcome.add_conditions:
        print("  » Uudet mietentilat:")
        for cond in sorted(result.outcome.add_conditions):
            print(f"    • {cond}")
        print()


def play_game(state: GameState) -> None:
    clear_screen()
    print(BANNER)
    print(INSTITUTIONAL_OPENING)
    print()
    print(COSMIC_OPENING)
    print()
    print("  Olet Sven-Olof. Olet juuri herännyt.")
    print("  C.G. Jung -instituutti, asteroidi 16 Psyche.")
    print("  UFAB 80MG. Tarvitset sitä.")
    print()
    print("  Kirjoita numero valitaksesi toiminnon, tai:")
    print("  s=verkko  i=tieto  c=tila  h=psykotroniikka  m=muistit  n=NPC-vuoro")
    print("  save=tallenna  quit=poistu")
    print()

    if advance_campaign_if_ready(state):
        print("  Tallennus jatkuu automaattisesti päivästä 2.")
        print()

    while not state.rpg.is_complete:
        render_scene(state)
        render_status(state)
        render_interactions(state)

        try:
            raw = input("  Valinta > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Näkemiin. Ragnarök muistaa sinua.")
            return

        if not raw:
            continue

        if raw in ("quit", "exit", "q"):
            print("  Näkemiin. Ragnarök muistaa sinua.")
            return

        if raw == "s":
            render_social(state)
            input("  [Paina Enter jatkaaksesi...]")
            clear_screen()
            continue

        if raw == "i":
            render_info(state)
            input("  [Paina Enter jatkaaksesi...]")
            clear_screen()
            continue

        if raw == "c":
            render_status(state)
            input("  [Paina Enter jatkaaksesi...]")
            clear_screen()
            continue

        if raw == "h":
            run_hacking_console(state)
            clear_screen()
            continue

        if raw == "m":
            render_memories(state)
            input("  [Paina Enter jatkaaksesi...]")
            clear_screen()
            continue

        if raw == "n":
            actions = state.perform_npc_turn()
            print("\n  » NPC-vuoro")
            if not actions:
                print("    Verkosto pysyy tällä hetkellä vakaana.")
            for action in actions:
                actor = state.social.graph.nodes[action.actor].get("name", action.actor)
                target = state.social.graph.nodes[action.target].get("name", action.target)
                print(
                    f"    {actor} → {target}: "
                    f"{action.dimension} {action.delta:+d} ({action.goal})"
                )
            input("  [Paina Enter jatkaaksesi...]")
            clear_screen()
            continue

        if raw == "save":
            SAVE_DIR.mkdir(exist_ok=True)
            save_path = SAVE_DIR / f"{state.rpg.scenario.id}_{state.rpg.state.current_scene}.json"
            state.save_to_file(save_path)
            print(f"  Tallennettu: {save_path}")
            input("  [Paina Enter jatkaaksesi...]")
            clear_screen()
            continue

        try:
            idx = int(raw) - 1
        except ValueError:
            print("  Epäkelpo valinta. Kirjoita numero tai komento.")
            continue

        interactions = state.rpg.available_interactions()
        if idx < 0 or idx >= len(interactions):
            print("  Epäkelpo valinta.")
            continue

        interaction = interactions[idx]
        result = state.perform_rpg_interaction(interaction.id)

        clear_screen()
        print(BANNER)
        handle_result(state, result)

        if state.rpg.is_complete:
            next_scenario = CAMPAIGN_NEXT.get(state.rpg.scenario.id)
            if next_scenario is not None:
                print_separator("═")
                print("  PÄIVÄ 1 ON PÄÄTTYNYT — KAMPANJA JATKUU.")
                print("  Sama Psyche, samat suhteet, uusi reterritorialisaatio.")
                print("  Helsinki ei ole takauma eikä simulaatio ennen kuin järjestelmä todistaa sen.")
                print_separator("═")
                advance_campaign_if_ready(state)
                input("  [Paina Enter aloittaaksesi päivän 2...]")
                clear_screen()
                continue

            print_separator("═")
            print("  NOÖPUNK: UBIQUITOUS MANIACS — KAMPANJA PÄÄTTYNYT.")
            print(f"  Lopullinen tila: {state.rpg.scene.title}")
            print_separator("═")
            print()
            print("  AGI luokitteli tapahtuman. PSI muutti havaitsijaa.")
            print("  Disclosure ei ratkaissut mitään. Noösfääri muistaa loput.")
            return

        input("  [Paina Enter jatkaaksesi...]")
        clear_screen()

    print("\n  Peli päättyi.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Noöpunk: Ubiquitous Maniacs — pelattava Day 1–2 -kampanja"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Deterministinen siemen (kokonaisluku)"
    )
    parser.add_argument(
        "--character", type=str, default=str(CHARACTER_PATH),
        help="Polku hahmon Markdown-tiedostoon"
    )
    parser.add_argument(
        "--scenario", type=str, default=str(SCENARIO_PATH),
        help="Polku skenaarion JSON-tiedostoon (esim. data/rpg/scenarios/day_2_kiimaiset_poliisit.json)"
    )
    parser.add_argument(
        "--load", type=str, default=None,
        help="Lataa tallennettu peli JSON-tiedostosta"
    )
    args = parser.parse_args()

    if args.load:
        scenario_path = scenario_path_for_save(args.load, args.scenario)
        state = GameState.load_from_file(
            args.load, args.character, scenario_path
        )
    else:
        state = GameState.from_files(
            args.character, args.scenario, seed=args.seed
        )
        state.start()

    play_game(state)


if __name__ == "__main__":
    main()
