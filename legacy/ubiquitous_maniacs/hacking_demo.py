"""Streamlit presentation for the RPG-compatible layered hacking demo."""

from pathlib import Path

import streamlit as st

from src.hacking import HackingAction, LayeredHackingSession
from src.rpg import load_character


ROOT = Path(__file__).parent
SCENARIO = ROOT / "data" / "hacking" / "sleeping_patient.json"
CHARACTER = ROOT / "data" / "rpg" / "characters" / "romppainen_day_1.md"

LAYER_COLORS = {
    "cybernetic": "#bae6fd",
    "psychic": "#e9d5ff",
    "social": "#fde68a",
    "biological": "#bbf7d0",
}


def new_session() -> LayeredHackingSession:
    actor = load_character(CHARACTER)
    actor.resources.setdefault("fate_points", 3)
    return LayeredHackingSession.from_json(actor, SCENARIO)


def dot(session: LayeredHackingSession) -> str:
    lines = ["graph target {", "rankdir=LR;", "node [shape=box, style=filled];"]
    for node in sorted(session.known_nodes):
        attrs = session.graph.nodes[node]
        color = LAYER_COLORS[attrs["layer"]]
        label = f"{attrs['label']}\\n{attrs['layer']} · {session.access[node].name}"
        border = "3" if node == session.current_node else "1"
        lines.append(f'"{node}" [label="{label}", fillcolor="{color}", penwidth={border}];')
    for source, target in sorted(session.discovered_edges):
        attrs = session.graph.edges[source, target]
        label = attrs.get("edge_type", "connection")
        lines.append(f'"{source}" -- "{target}" [label="{label}"];')
    return "\n".join(lines + ["}"])


st.set_page_config(page_title="Noöpunk: Nukkuva potilas", layout="wide")
st.title("Kyberneettis–psykotroninen hakkerointi")
st.caption(
    "Nukkuva potilas · nelikerroksinen fiktiivinen RPG-demo. "
    "Psyykkinen kerros ei ole väite neurotieteestä tai kvanttifysiikasta."
)

if "layered_hack" not in st.session_state:
    st.session_state.layered_hack = new_session()
if "hack_message" not in st.session_state:
    st.session_state.hack_message = None

session: LayeredHackingSession = st.session_state.layered_hack
snapshot = session.snapshot()

st.info(f"**Tavoite:** {session.objective}")
metrics = st.columns(5)
metrics[0].metric("Tila", session.status)
metrics[1].metric("Hälytys", f"{session.alert}/8")
metrics[2].metric("Trace", f"{session.trace}/8")
metrics[3].metric("Feedback", f"{session.feedback}/8")
metrics[4].metric("Tavoitteet", f"{len(session.completed_objectives)}/2")

if st.session_state.hack_message:
    kind, message = st.session_state.hack_message
    getattr(st, kind)(message)

controls, graph_view = st.columns([1, 2])
nodes = sorted(session.known_nodes)

with controls:
    st.subheader("Toiminto")
    action = st.selectbox(
        "Toiminto",
        [
            HackingAction.OBSERVE.value,
            HackingAction.CREATE_ACCESS.value,
            HackingAction.CREATE_ADVANTAGE.value,
            HackingAction.EXPLOIT.value,
            HackingAction.DEFEND.value,
            HackingAction.OVERCOME.value,
            HackingAction.ATTACK.value,
            HackingAction.RETREAT.value,
        ],
        disabled=session.is_terminal,
    )
    target = st.selectbox(
        "Kohdenode",
        nodes,
        format_func=lambda node: f"{session.graph.nodes[node]['label']} [{session.graph.nodes[node]['layer']}]",
        disabled=session.is_terminal or action == HackingAction.RETREAT.value,
    )
    source = st.selectbox(
        "Lähtönode lateral movementille",
        nodes,
        index=nodes.index(session.current_node) if session.current_node in nodes else 0,
        disabled=session.is_terminal or action != HackingAction.CREATE_ACCESS.value,
    )
    aspect = st.text_input(
        "Luotava etu",
        "SUOJELUTARKOITUS VAHVISTETTU",
        disabled=session.is_terminal or action != HackingAction.CREATE_ADVANTAGE.value,
    )
    tool_options = [None, *sorted(session.tools)]
    tool_id = st.selectbox(
        "Työkalu tai protokolla",
        tool_options,
        format_func=lambda item: "Ei työkalua" if item is None else session.tools[item].label,
        disabled=session.is_terminal or action == HackingAction.RETREAT.value,
    )
    invokable = [None, *sorted(session.actor.aspects | session.aspects)]
    invoke_aspect = st.selectbox(
        f"Kutsu aspektia (+2, Fate-pisteitä {session.actor.resources.get('fate_points', 0)})",
        invokable,
        format_func=lambda item: "Ei kutsua" if item is None else item,
        disabled=session.is_terminal or action == HackingAction.RETREAT.value,
    )
    deterministic = st.checkbox("Valitse 4dF-tulos käsin", value=False)
    roll = st.slider("4dF", -4, 4, 0, disabled=not deterministic)

    if st.button("Suorita", type="primary", disabled=session.is_terminal):
        try:
            chosen_roll = roll if deterministic else None
            kwargs = {"roll": chosen_roll, "tool_id": tool_id, "invoke_aspect": invoke_aspect}
            if action == HackingAction.OBSERVE.value:
                result = session.observe(target, **kwargs)
            elif action == HackingAction.CREATE_ACCESS.value:
                result = session.create_access(source, target, **kwargs)
            elif action == HackingAction.CREATE_ADVANTAGE.value:
                result = session.create_advantage(target, aspect, **kwargs)
            elif action == HackingAction.EXPLOIT.value:
                result = session.exploit(target, **kwargs)
            elif action == HackingAction.DEFEND.value:
                result = session.defend(target, **kwargs)
            elif action == HackingAction.OVERCOME.value:
                result = session.overcome(target, **kwargs)
            elif action == HackingAction.ATTACK.value:
                result = session.attack(target, **kwargs)
            else:
                result = session.retreat()
            tier = f" ({result.check.check.tier.value})" if result.check else ""
            st.session_state.hack_message = (
                "success" if result.success else "warning",
                result.summary + tier,
            )
            st.rerun()
        except (KeyError, ValueError) as exc:
            st.session_state.hack_message = ("error", str(exc))
            st.rerun()

    if st.button("Aloita alusta"):
        st.session_state.layered_hack = new_session()
        st.session_state.hack_message = None
        st.rerun()

    st.subheader("Tunnetut aspektit")
    st.write(", ".join(sorted(session.aspects)) or "Ei luotuja etuja")

with graph_view:
    st.subheader("Kohdegraafi")
    st.graphviz_chart(dot(session), width="stretch")
    st.caption("Sininen: cyber · violetti: Psyche · keltainen: social · vihreä: biology")

state_tab, log_tab, transfer_tab = st.tabs(["Näkyvä tila", "Toimintaloki", "RPG-siirto"])
with state_tab:
    st.json({key: value for key, value in snapshot.items() if key not in {"history", "rpg_transfer"}}, expanded=False)
with log_tab:
    st.json(snapshot["history"], expanded=True)
with transfer_tab:
    st.json(snapshot["rpg_transfer"], expanded=True)
    st.caption("Nämä muutokset voidaan kirjoittaa tavallisen RPG:n RPGState-tilaan adapterilla.")
