from pathlib import Path

import streamlit as st

from src.social.simulation import SocialSimulation

DATA = Path(__file__).parent / "data" / "social_simulation" / "demo.json"


def dot(sim: SocialSimulation) -> str:
    lines = ['graph social {', 'node [shape=ellipse, style=filled, fillcolor="#dbeafe"];']
    for node, attrs in sim.graph.nodes(data=True):
        lines.append(f'"{node}" [label="{attrs["name"]}\\n{attrs["mood"]}"];')
    for source, target, attrs in sim.graph.edges(data=True):
        value = attrs["relationship"]
        color = "#15803d" if value >= 0 else "#b91c1c"
        lines.append(f'"{source}" -- "{target}" [label="{value}", color="{color}"];')
    return "\n".join(lines + ["}"])


st.set_page_config(page_title="Noöpunk Social Simulation", layout="wide")
st.title("Social Simulation Demo")
st.caption("Standalone NetworkX experiment — no RPG integration")
if "social_sim" not in st.session_state:
    st.session_state.social_sim = SocialSimulation.from_json(DATA)
sim = st.session_state.social_sim
left, right = st.columns([1, 2])
with left:
    event_id = st.selectbox("Social event", list(sim.events),
                            format_func=lambda key: sim.events[key].get("label", key))
    if st.button("Apply event", type="primary"):
        st.success(sim.apply_event(event_id).summary)
    if st.button("Run one automatic turn"):
        st.info(sim.auto_step().summary)
    if st.button("Reset"):
        st.session_state.social_sim = SocialSimulation.from_json(DATA)
        st.rerun()
    st.metric("Turn", sim.turn)
with right:
    st.graphviz_chart(dot(sim), use_container_width=True)
st.subheader("Inspectable state")
st.json(sim.snapshot(), expanded=False)

