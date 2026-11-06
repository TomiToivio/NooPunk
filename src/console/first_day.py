"""#1217: Tony German's first-day *interaction adapter*.

This is intentionally not another game loop or character generator. The canonical
WorldSession owns flags, actor identity, story scene and physical position. Every
step below is from Tomi's explicit opening brief; dreams, dialogue and lifepath
prose are not fabricated by an agent.
"""
from __future__ import annotations

try:
    from src.console.world_session import WorldSession
    from src.world.graphs import (
        CyberGraph,
        LocationNode,
        PhysicalGraph,
        PhysicalRoute,
        SocialGraph,
        SocialNode,
        StoryGraph,
        StoryLink,
        StoryNode,
        WorldGraphs,
    )
    from src.world.items import Kit, first_day_kit
except ModuleNotFoundError:  # installed with src/ on PYTHONPATH
    from world.graphs import (
        CyberGraph,
        LocationNode,
        PhysicalGraph,
        PhysicalRoute,
        SocialGraph,
        SocialNode,
        StoryGraph,
        StoryLink,
        StoryNode,
        WorldGraphs,
    )
    from world.items import Kit, first_day_kit

    from .world_session import WorldSession

ACTOR = "tony.german"
SHEET = "sheet.tony.german"
NAME = "Tony German"
DISPATCH_LINE = "Field Agent Tony German reporting for duty."

#: The issued kit is defined once, in `world.items`, so the intro cannot drift from the inventory.
KIT = tuple(item.id for item in first_day_kit() if not item.worn)
# Abstract user-interface connections only, not operational police protocols.
LINKED = tuple(item for item in KIT if item not in ("police_radio", "phone"))

HOME = "loc.sornainen_home"
ROUTE = "loc.helsinki_route"
OFFICE = "loc.ratakatu_12"


class FirstDayError(ValueError):
    """Invalid first-day operation, never an alternate dice rule."""


def create_first_day(session: WorldSession | None = None) -> WorldSession:
    """Attach Tony's authored starting facts to the canonical WorldSession.

    The three location nodes are a deliberately coarse route, not a second
    Helsinki map or a claim about street-level geography. The first approved
    episode can replace this graph with its canonical authored locations.
    """
    if session is None:
        physical = PhysicalGraph(
            nodes={
                HOME: LocationNode(HOME, "Europol-provided Sörnäinen home"),
                ROUTE: LocationNode(ROUTE, "Helsinki commute"),
                OFFICE: LocationNode(OFFICE, "Europol Field Office, Ratakatu 12"),
            },
            routes=(
                PhysicalRoute(HOME, ROUTE, directed=True, kind="commute"),
                PhysicalRoute(ROUTE, OFFICE, directed=True, kind="commute"),
            ),
            occupants={ACTOR: HOME},
        )
        story = StoryGraph(
            nodes={
                "scene.nightmare": StoryNode("scene.nightmare", "Nightmare", "scene",
                                              scene_types=("Exploration",)),
                "scene.morning": StoryNode("scene.morning", "First morning", "scene",
                                            scene_types=("Exploration",)),
                "scene.commute": StoryNode("scene.commute", "Motorcycle commute", "scene",
                                            scene_types=("Exploration",)),
                "scene.reporting": StoryNode("scene.reporting", "First report", "scene",
                                              scene_types=("Social",)),
            },
            links=(
                StoryLink("scene.nightmare", "scene.morning"),
                StoryLink("scene.morning", "scene.commute"),
                StoryLink("scene.commute", "scene.reporting"),
            ),
        )
        session = WorldSession(WorldGraphs(
            physical=physical, cyber=CyberGraph(),
            social=SocialGraph(nodes={ACTOR: SocialNode(ACTOR, NAME, "character")}),
            story=story,
        ))
        session.register(ACTOR, SHEET)
        _kit(session)
        session.enter_scene("scene.nightmare")
    else:
        if session.sheet_for(ACTOR) != SHEET:
            raise FirstDayError("Tony must use his original canonical character sheet")
        if session.where(ACTOR) not in (HOME, ROUTE, OFFICE):
            raise FirstDayError("Tony is not on his first-day route")
    return session


def _done(session: WorldSession, action: str) -> bool:
    return "first_day:" + action in session.flags


def _require_first_day(session: WorldSession) -> None:
    if session.sheet_for(ACTOR) != SHEET:
        raise FirstDayError("Tony German is not bound to his canonical sheet")


def _kit(session: WorldSession) -> Kit:
    """Use the session's actual inventory; upgrade pre-inventory saves in place."""
    if session.kit is None:
        session.kit = Kit(actor=ACTOR)
        for item in first_day_kit():
            session.kit.issue(item)
        # Old snapshots stored completed equipment actions as flags only.
        for item in KIT:
            if _done(session, "connect:" + item) or (
                item in ("police_radio", "phone") and _done(session, "inspect:" + item)
            ):
                session.kit.activate(item)
    if session.kit.actor != ACTOR:
        raise FirstDayError("Tony's kit must belong to his canonical actor")
    return session.kit


def available_first_day_actions(session: WorldSession) -> tuple[str, ...]:
    """Actions only; no prose choices or unpublished character benefits."""
    _require_first_day(session)
    kit = _kit(session)
    if _done(session, "report"):
        return ()
    if not _done(session, "wake"):
        return ("wake",)
    actions: list[str] = []
    if not _done(session, "uniform"):
        actions.append("uniform")
    actions.extend("inspect:" + item for item in KIT if not _done(session, "inspect:" + item))
    if _done(session, "inspect:police_radio") and _done(session, "inspect:phone"):
        actions.extend(
            "connect:" + item
            for item in LINKED
            if _done(session, "inspect:" + item) and not _done(session, "connect:" + item)
            and kit.get(item).usable
        )
    ready = _done(session, "uniform") and all(
        _done(session, "inspect:" + item) for item in KIT
    ) and all(
        _done(session, "connect:" + item) or not kit.get(item).usable
        for item in LINKED
    ) and not kit.missing()
    if ready and not _done(session, "dispatch"):
        actions.append("dispatch")
    if _done(session, "dispatch") and not _done(session, "ride"):
        actions.append("ride")
    if _done(session, "ride") and not _done(session, "arrive"):
        actions.append("arrive")
    if _done(session, "arrive"):
        actions.append("report")
    return tuple(actions)


def first_day_action(session: WorldSession, action: str) -> str:
    """Advance existing story/physical graphs. No rolls or alternate session."""
    if action not in available_first_day_actions(session):
        raise FirstDayError(f"unavailable first-day action: {action}")
    if action == "wake":
        session.enter_scene("scene.morning")
        message = "Tony wakes in his Europol-provided home in Sörnäinen."
    elif action == "uniform":
        message = (
            "Black Hussar-inspired Europol uniform, silver insignia, EU emblem and "
            "Tony German name tag; Cossack haircut and moustache."
        )
    elif action.startswith("inspect:"):
        item = action.split(":", 1)[1]
        carried = _kit(session).get(item)
        if item in ("police_radio", "phone") and carried.usable:
            _kit(session).activate(item)
        diagnostic = f" Fault: {carried.fault}." if carried.fault else ""
        message = f"Inspected issued equipment: {item.replace('_', ' ')}.{diagnostic}"
    elif action.startswith("connect:"):
        item = action.split(":", 1)[1]
        _kit(session).activate(item)
        message = f"Connected {item.replace('_', ' ')} through the abstract Europol kit interface."
    elif action == "dispatch":
        message = DISPATCH_LINE
    elif action == "ride":
        session.move(ACTOR, ROUTE)
        session.enter_scene("scene.commute")
        message = "Tony rides his heavy Adlerwerke Polizeimotorrad toward Ratakatu."
    elif action == "arrive":
        session.move(ACTOR, OFFICE)
        session.enter_scene("scene.reporting")
        message = "Tony arrives in uniform at Europol Field Office, Ratakatu 12."
    else:
        message = "Tony reports to Dr. Harri Romppainen on his first day."
    session.flags.add("first_day:" + action)
    return message
