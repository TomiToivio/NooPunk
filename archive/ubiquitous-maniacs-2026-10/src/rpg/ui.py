"""Minimal Streamlit renderer; core logic remains UI-independent."""

from __future__ import annotations

from .engine import RPGSession


def render_rpg_session(st, session: RPGSession, state_key: str = "rpg_last_result") -> None:
    scene = session.scene
    st.header(scene.title)
    st.caption(" · ".join(filter(None, (scene.location, scene.phase))))
    st.write(scene.description)
    if scene.participants:
        st.caption("NPC: " + ", ".join(scene.participants))

    node = session.dialogue_node
    if node:
        st.markdown(f"**{node.speaker}:** {node.text}")

    last_result = st.session_state.get(state_key)
    if last_result:
        check = last_result.check
        if check:
            st.info(f"{check.tier.value.upper()} · 4dF {check.dice} · {check.total} vs {check.difficulty}")
        st.write(last_result.outcome.text)

    left, right = st.columns([2, 1])
    with left:
        st.subheader("Actions")
        if session.is_complete:
            st.success("Päivä 1 on valmis. Tila on säilytetty; päivää 2 ei ole vielä toteutettu.")
        for interaction in session.available_interactions():
            label = interaction.label
            if interaction.check:
                skill = f" + {interaction.check.skill}" if interaction.check.skill else ""
                label = f"[{interaction.check.attribute}{skill}] {label}"
            if st.button(label, key=f"rpg_{scene.id}_{interaction.id}", use_container_width=True):
                st.session_state[state_key] = session.perform_interaction(interaction.id)
                st.rerun()
    with right:
        st.subheader(session.character.name)
        relevant = {item.check.attribute for item in session.available_interactions() if item.check}
        st.json({name: session.character.attribute(name) for name in relevant})
        st.caption("Conditions")
        st.write(", ".join(sorted(session.state.conditions)) or "—")
        st.caption("Aspects")
        st.write(", ".join(sorted(session.character.aspects)) or "—")
        st.caption("Consequences")
        st.write(", ".join(session.state.consequences) or "—")
        st.caption("Relationships")
        st.json(session.state.relationships)
        st.caption("Discovered information")
        st.write(", ".join(sorted(session.state.known_information)) or "—")

