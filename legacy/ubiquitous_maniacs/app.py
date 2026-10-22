from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.cyber import build_cyber_graph
from src.cyber import graph_to_dot as cyber_to_dot
from src.cyber import graph_to_gexf_bytes as cyber_to_gexf
from src.noetic import build_noetic_graph
from src.noetic import graph_to_dot as noetic_to_dot
from src.noetic import graph_to_gexf_bytes as noetic_to_gexf
from src.physical import build_physical_graph
from src.physical import graph_to_dot as physical_to_dot
from src.physical import graph_to_gexf_bytes as physical_to_gexf
from src.interaction import EnrollmentStatus, ReceptionGame, apply_choice, get_node
from src.hacking import LayeredHackingSession
from src.game.day1_web_save import from_dict as day1_from_dict
from src.game.day1_web_save import to_dict as day1_to_dict
from src.rpg import (
    RPGSession,
    apply_social_graph_effect,
    load_character,
    load_scenario,
)
from src.rpg.ui import render_rpg_session
from src.social import (
    build_social_graph,
    get_person_relationships,
    graph_to_dict,
    graph_to_dot,
    graph_to_gexf_bytes,
    list_people,
    list_relationships,
    load_people_records,
    load_relationship_records,
)
from src.sim.social import SocialSimulation, ACTIONS as SOCIAL_ACTIONS
from src.sim.hacking import HackingSimulation, NODE_TYPES as HACK_NODE_TYPES, EDGE_TYPES as HACK_EDGE_TYPES


DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def get_people_records() -> list[dict[str, object]]:
    return load_people_records(DATA_DIR / "lab_people.csv")


@st.cache_data
def get_relationship_records() -> list[dict[str, object]]:
    return load_relationship_records(DATA_DIR / "lab_relationships.csv")


def render_empty_graph_tab(graph, to_dot, to_gexf, filename: str) -> None:
    st.caption("Moduuli on valmis, mutta graafin sisältöä ei ole vielä määritelty.")
    st.graphviz_chart(to_dot(graph), width="stretch")
    st.download_button(
        "Lataa graafi Gephiä varten (.gexf)",
        data=to_gexf(graph),
        file_name=filename,
        mime="application/gexf+xml",
    )


def render_reception_interaction() -> None:
    """Renderöi vain ensimmäinen vastaanottokeskustelu."""
    st.header("Saapuminen C.G. Jung -instituuttiin")
    st.caption("16 Psyche · vastaanotto / testihuone · päivä")

    if "reception_game" not in st.session_state:
        st.session_state.reception_game = ReceptionGame()
        st.session_state.reception_history = []
    game = st.session_state.reception_game

    status_col, suspicion_col, trust_col = st.columns(3)
    status_col.metric("Peitehenkilöllisyys", game.player.cover_identity)
    suspicion_col.metric("Epäily", game.receptionist.suspicion)
    trust_col.metric("Luottamus", game.receptionist.trust)

    for turn in st.session_state.reception_history:
        st.markdown(f"**Romppainen:** {turn['player_text']}")
        if turn["attribute"] is not None:
            result_label = "onnistui" if turn["success"] else "epäonnistui"
            st.caption(f"{turn['attribute']} — {result_label}")
        if turn["response"]:
            st.markdown(f"**Dr. Elin Dahl:** {turn['response']}")

    if game.is_finished:
        status = game.scene.enrollment_status
        if status is EnrollmentStatus.ACCEPTED:
            st.success(
                "**Teidät on valittu kokeeseen.**\n\n"
                "CUT. Kohtaus päättyy lomakkeisiin ennen podille siirtymistä."
            )
        elif status is EnrollmentStatus.REJECTED:
            st.error("**Eteneminen estetty vastaanotossa**\n\nKohtaus päättyy vastaanottoon.")
        else:
            st.warning("**Lisäselvitys vaaditaan**\n\nKohtaus päättyy vastaanottoon.")
        if st.button("Aloita vastaanottokeskustelu uudelleen"):
            st.session_state.reception_game = ReceptionGame()
            st.session_state.reception_history = []
            st.rerun()
        return

    node = get_node(game.scene.current_node)
    if node is None:
        st.error("Dialoginodia ei löytynyt.")
        return
    st.subheader(node.id.replace("_", " ").title())
    st.write(node.narration)
    st.markdown(f"**{node.npc_name}:** {node.npc_text}")

    for option in node.choices:
        if st.button(option.text, key=f"reception_{node.id}_{option.id}", use_container_width=True):
            response, success = apply_choice(game, option)
            st.session_state.reception_history.append(
                {
                    "player_text": option.text,
                    "response": response,
                    "attribute": option.attribute,
                    "success": success,
                }
            )
            st.rerun()


def render_day_1() -> None:
    """Render the complete Day 1 vertical slice."""
    if "day_1_session" not in st.session_state:
        character = load_character(DATA_DIR / "rpg/characters/romppainen_day_1.md")
        scenario = load_scenario(DATA_DIR / "rpg/scenarios/day_1_arrival_and_entanglement.json")
        st.session_state.day_1_session = RPGSession(character, scenario, seed=1601)
        st.session_state.day_1_social = SocialSimulation.from_lab_data(
            get_people_records(), get_relationship_records()
        )
        st.session_state.day_1_social_effects = 0

    session = st.session_state.day_1_session
    social = st.session_state.day_1_social
    applied = st.session_state.day_1_social_effects
    for effect in session.state.graph_effects[applied:]:
        apply_social_graph_effect(
            social.graph,
            effect,
            aliases={"romppainen_day_1": "sven_olof_romppainen"},
        )
    st.session_state.day_1_social_effects = len(session.state.graph_effects)

    render_rpg_session(st, session, "day_1_last_result")

    with st.expander("Day 1 social graph"):
        st.caption("Dialogue effects are applied to the same live relationship graph.")
        st.dataframe(pd.DataFrame(social.state()["relationships"]), hide_index=True, width="stretch")
        recent = [event for event in session.events if event.type == "relationship_changed"][-5:]
        st.json([{"type": event.type, **event.payload} for event in recent])

    hacking_unlocked = session.scene.id in {"d1_ufab_heist", "d1_night_signal", "d1_complete"}
    if hacking_unlocked:
        with st.expander("Psychotronic investigation", expanded=session.scene.id == "d1_ufab_heist"):
            st.caption("Optional four-layer graph investigation; failure raises trace and feedback pressure.")
            if "day_1_hack" not in st.session_state:
                st.session_state.day_1_hack = LayeredHackingSession.from_json(
                    session.character, DATA_DIR / "hacking/sleeping_patient.json"
                )
            hack = st.session_state.day_1_hack
            snap = hack.snapshot()
            a, b, c = st.columns(3)
            a.metric("Status", snap["status"])
            b.metric("Alert", snap["alert"])
            c.metric("Feedback", snap["feedback"])
            st.write("Known nodes:", ", ".join(sorted(hack.known_nodes)))
            if not hack.is_terminal:
                action = st.selectbox(
                    "Graph action", ["observe", "create_access", "exploit", "resonate", "retreat"],
                    key="d1_hack_action",
                )
                roll = st.slider("4dF total", -4, 4, 0, key="d1_hack_roll")
                source = None
                target = None
                can_execute = True
                if action == "resonate":
                    options = snap["resonance_options"]
                    if options:
                        option = st.selectbox(
                            "Cross-layer route",
                            options,
                            format_func=lambda item: (
                                f"{snap['current_node']} → {item['target']} "
                                f"[{item['edge_type']}; {item['target_layer']}]"
                            ),
                            key="d1_hack_resonance_route",
                        )
                        source = snap["current_node"]
                        target = option["target"]
                    else:
                        st.info("Nykyisestä solmusta ei avaudu cross-layer-resonanssia.")
                        can_execute = False
                elif action != "retreat":
                    target = st.selectbox("Target", sorted(hack.known_nodes), key="d1_hack_target")
                if action == "create_access":
                    source = st.selectbox("Source", sorted(hack.known_nodes), key="d1_hack_source")
                if st.button("Execute graph action", key="d1_hack_execute", disabled=not can_execute):
                    try:
                        if action == "observe":
                            result = hack.observe(target, roll=roll)
                        elif action == "create_access":
                            result = hack.create_access(source, target, roll=roll)
                        elif action == "exploit":
                            result = hack.exploit(target, roll=roll)
                        elif action == "resonate":
                            result = hack.resonate(source, target, roll=roll)
                        else:
                            result = hack.retreat()
                        st.session_state.day_1_hack_result = result
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            result = st.session_state.get("day_1_hack_result")
            if result:
                st.info(result.summary)
            if hack.is_terminal and not st.session_state.get("day_1_hack_applied"):
                hack.transfer.apply(session.state, session.character)
                st.session_state.day_1_hack_applied = True
                st.success("Investigation consequences transferred into the Day 1 RPG state.")

    save_document = day1_to_dict(
        session,
        social,
        st.session_state.day_1_social_effects,
        st.session_state.get("day_1_hack"),
        st.session_state.get("day_1_hack_applied", False),
    )
    save_data = json.dumps(save_document, ensure_ascii=False, indent=2)
    st.download_button("Save Day 1", save_data, "noopunk-day-1-save.json", "application/json")
    uploaded = st.file_uploader("Load Day 1 save", type="json", key="day_1_save_upload")
    if uploaded is not None and st.button("Restore uploaded save"):
        try:
            save_document = json.loads(uploaded.getvalue().decode("utf-8"))
            restored = day1_from_dict(
                save_document,
                DATA_DIR / "rpg/characters/romppainen_day_1.md",
                DATA_DIR / "rpg/scenarios/day_1_arrival_and_entanglement.json",
                get_people_records(),
                get_relationship_records(),
            )
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError, KeyError) as exc:
            st.error(f"Save could not be loaded: {exc}")
        else:
            st.session_state.day_1_session = restored.rpg
            st.session_state.day_1_social = restored.social
            st.session_state.day_1_social_effects = restored.social_effects
            for key in (
                "day_1_last_result",
                "day_1_hack_result",
            ):
                st.session_state.pop(key, None)
            if restored.hacking is None:
                st.session_state.pop("day_1_hack", None)
            else:
                st.session_state.day_1_hack = restored.hacking
            st.session_state.day_1_hack_applied = restored.hacking_applied
            st.rerun()
    if st.button("Aloita päivä 1 uudelleen"):
        del st.session_state.day_1_session
        st.session_state.pop("day_1_last_result", None)
        st.session_state.pop("day_1_social", None)
        st.session_state.pop("day_1_social_effects", None)
        st.session_state.pop("day_1_hack", None)
        st.session_state.pop("day_1_hack_result", None)
        st.session_state.pop("day_1_hack_applied", None)
        st.rerun()


def render_social_sim() -> None:
    """Standalone social simulation demo."""
    st.subheader("Sosiaalinen simulaatio — C.G. Jungin hahmoverkko")
    st.caption("Erillinen demo. Ei integroitu RPG-moduuliin.")

    if "social_sim" not in st.session_state:
        people = load_people_records(DATA_DIR / "lab_people.csv")
        rels = load_relationship_records(DATA_DIR / "lab_relationships.csv")
        st.session_state.social_sim = SocialSimulation.from_lab_data(people, rels)

    sim = st.session_state.social_sim
    state = sim.state()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Tick", state["tick"])
        st.metric("Hahmoja", len(state["characters"]))
        st.metric("Suhteita", len(state["relationships"]))

        st.write("**Hahmot:**")
        for c in state["characters"]:
            st.text(f"  {c['name']} ({c['role']})")

        st.write("**Interaktiot:**")
        for action_id, action_def in SOCIAL_ACTIONS.items():
            if st.button(action_id, key=f"social_action_{action_id}", use_container_width=True):
                pass  # selected below

    with col2:
        st.write("**Suhteet (-100..+100):**")
        rel_df = pd.DataFrame(state["relationships"])
        st.dataframe(rel_df, width="stretch", hide_index=True)

        st.write("**Interaktio:**")
        chars = [c["id"] for c in state["characters"]]
        src = st.selectbox("Lähde", chars, key="social_src")
        tgt = st.selectbox("Kohde", [c for c in chars if c != src], key="social_tgt")
        action = st.selectbox("Toiminto", list(SOCIAL_ACTIONS.keys()), key="social_action_sel")
        if st.button("Suorita", key="social_run"):
            events = sim.interact(src, tgt, action)
            for e in events:
                st.text(f"  [{e.type}] {e.source} -> {e.target}: {e.action} ({e.delta:+d}) {e.description}")
            st.rerun()

        if st.button("Step (ambient tick)", key="social_step"):
            events = sim.step()
            for e in events:
                st.text(f"  [{e.type}] {e.source} -> {e.target}: {e.action} ({e.delta:+d})")
            st.rerun()

    with st.expander("Tapahtumahistoria"):
        hist = sim.history()
        if hist:
            st.dataframe(pd.DataFrame(hist), width="stretch", hide_index=True)
        else:
            st.text("Ei tapahtumia vielä.")


def render_hacking_sim() -> None:
    """Standalone psychotronic/cybernetic hacking demo."""
    st.subheader("Psykotrooninen/Kyberneettinen hakkerointisimulaatio")
    st.caption("Erillinen demo. Ei integroitu RPG-moduuliin.")

    if "hack_sim" not in st.session_state:
        st.session_state.hack_sim = HackingSimulation()
        st.session_state.hack_sim.build_default_target()

    hack = st.session_state.hack_sim
    state = hack.state()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Tick", state["tick"])
        st.metric("Solmuja", len(state["nodes"]))
        st.metric("Edgejä", len(state["edges"]))

        st.write("**Solmut:**")
        for n in state["nodes"]:
            st.text(f"  {n['label']} [{n['type']}] stab={n['stability']} state={n['state']}")

    with col2:
        st.write("**Toiminnot:**")
        node_ids = [n["id"] for n in state["nodes"]]
        node_labels = {n["id"]: f"{n['label']} [{n['type']}]" for n in state["nodes"]}

        action_type = st.selectbox(
            "Toiminto", ["inspect", "trace", "strengthen", "weaken", "inject", "suppress", "resonate", "entangle", "isolate", "collapse"],
            key="hack_action_sel"
        )
        node_a = st.selectbox("Solmu A", node_ids, format_func=lambda x: node_labels.get(x, x), key="hack_node_a")

        if action_type in ("trace", "strengthen", "weaken", "resonate", "entangle"):
            node_b = st.selectbox("Solmu B", [n for n in node_ids if n != node_a], format_func=lambda x: node_labels.get(x, x), key="hack_node_b")
        elif action_type == "inject":
            pattern = st.text_input("Pattern", "fear_pattern", key="hack_pattern")

        if st.button("Suorita", key="hack_run"):
            try:
                if action_type == "inspect":
                    info = hack.inspect(node_a)
                    st.json(info)
                elif action_type == "trace":
                    path = hack.trace(node_a, node_b)
                    st.text(f"Path: {' -> '.join(path) if path else 'no path'}")
                elif action_type == "strengthen":
                    hack.strengthen(node_a, node_b)
                elif action_type == "weaken":
                    hack.weaken(node_a, node_b)
                elif action_type == "inject":
                    hack.inject(node_a, pattern)
                elif action_type == "suppress":
                    hack.suppress(node_a)
                elif action_type == "resonate":
                    hack.resonate(node_a, node_b)
                elif action_type == "entangle":
                    hack.entangle(node_a, node_b)
                elif action_type == "isolate":
                    removed = hack.isolate(node_a)
                    st.text(f"Removed {len(removed)} edges")
                elif action_type == "collapse":
                    result = hack.collapse(node_a)
                    st.json(result)
                st.rerun()
            except Exception as e:
                st.error(str(e))

    with st.expander("Tapahtumahistoria"):
        hist = hack.history()
        if hist:
            st.dataframe(pd.DataFrame(hist), width="stretch", hide_index=True)
        else:
            st.text("Ei tapahtumia vielä.")


def main() -> None:
    st.set_page_config(page_title="Noöpunk: Askel 1", page_icon=":hospital:", layout="wide")

    graph = build_social_graph(get_people_records(), get_relationship_records())
    people = list_people(graph)
    relationships = list_relationships(graph)
    graph_state = graph_to_dict(graph)

    st.title("Noöpunk: Ubiquitous Maniacs")
    st.caption("Neljä erillistä NetworkX-graafimoduulia")
    st.info(
        "Sosiaaligraafi sisältää laboratorion ydinkastin: 2 potilasta, 3 työntekijää "
        "ja 1 tekoälyn (C.G. Jung). Kyberneettinen, noeettinen ja fyysinen "
        "graafi ovat vielä tyhjiä rakenteita. Graafeja ei yhdistetä tässä vaiheessa."
    )

    render_reception_interaction()
    st.divider()

    with st.expander("Pelattava päivä 1", expanded=True):
        render_day_1()
    st.divider()

    sim_tab, hack_tab = st.tabs(["Sosiaalinen simulaatio", "Hakkerointisimulaatio"])
    with sim_tab:
        render_social_sim()
    with hack_tab:
        render_hacking_sim()
    st.divider()

    counts = pd.Series(person["role"] for person in people).value_counts()
    patient_count = int(counts.get("patient", 0))
    staff_count = int(counts.get("staff", 0))
    ai_count = int(counts.get("ai", 0))

    count_col, patient_col, staff_col, edge_col = st.columns(4)
    count_col.metric("Hahmoja", graph.number_of_nodes())
    patient_col.metric("Potilaita", patient_count)
    staff_col.metric("Henkilökuntaa", staff_count)
    edge_col.metric("Suhde-edgejä", graph.number_of_edges())

    st.subheader("Maailman NetworkX-graafit")
    social_tab, cyber_tab, noetic_tab, physical_tab = st.tabs(
        ["Sosiaalinen", "Kyberneettinen", "Noeettinen", "Fyysinen"]
    )
    with social_tab:
        st.caption("Sininen = potilas, vihreä = henkilökunta, keltainen = tekoäly. Edgen numero on relationship-arvo.")
        st.graphviz_chart(graph_to_dot(graph), width="stretch")
        st.download_button(
            "Lataa graafi Gephiä varten (.gexf)",
            data=graph_to_gexf_bytes(graph),
            file_name="noopunk_social_graph.gexf",
            mime="application/gexf+xml",
        )
    with cyber_tab:
        render_empty_graph_tab(
            build_cyber_graph(), cyber_to_dot, cyber_to_gexf, "noopunk_cyber_graph.gexf"
        )
    with noetic_tab:
        render_empty_graph_tab(
            build_noetic_graph(), noetic_to_dot, noetic_to_gexf, "noopunk_noetic_graph.gexf"
        )
    with physical_tab:
        render_empty_graph_tab(
            build_physical_graph(), physical_to_dot, physical_to_gexf, "noopunk_physical_graph.gexf"
        )

    people_df = pd.DataFrame(people)
    relationships_df = pd.DataFrame(relationships)

    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader("Henkilöt")
        st.dataframe(people_df, width="stretch", hide_index=True)
    with right_col:
        st.subheader("Suhteet")
        st.dataframe(relationships_df, width="stretch", hide_index=True)

    st.subheader("Yksittäisen henkilön suhteet")
    person_options = {person["name"]: person["id"] for person in people}
    selected_name = st.selectbox("Valitse henkilö", options=list(person_options.keys()))
    selected_id = person_options[selected_name]
    selected_relationships = get_person_relationships(graph, selected_id)

    st.dataframe(pd.DataFrame(selected_relationships), width="stretch", hide_index=True)

    st.subheader("Graafin koko tila")
    st.json(graph_state)


if __name__ == "__main__":
    main()
