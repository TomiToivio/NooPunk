"""Optional local After-the-Fall / Crisis-Campaign state (#1045).

Original NoöPunk region-state adapter, not a replacement AWN or CWN engine.
No global material collapse is presumed by NHI disclosure.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict

STATES = ("functioning", "emergency", "after_the_fall", "contested", "recovering")
AXES = ("infrastructure", "safety", "supplies", "governance",
        "communications", "anomalies", "ontological_shock")
AWN_LOCAL_OVERLAYS = ("scarcity", "salvage", "enclaves", "crisis_sites")

@dataclass
class Region:
    id: str
    state: str = "functioning"
    axes: dict[str, int] = field(default_factory=lambda: {k: 0 for k in AXES})
    history: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.id or self.state not in STATES or set(self.axes) != set(AXES):
            raise ValueError("invalid region")
        if any(type(x) is not int or not 0 <= x <= 5 for x in self.axes.values()):
            raise ValueError("region axes must be integer severity 0..5")

    @property
    def local_overlays(self):
        return AWN_LOCAL_OVERLAYS if self.state in ("after_the_fall", "contested") else ()

    def transition(self, target: str, *, event_id: str, reason: str,
                   changes: dict[str, int] | None = None):
        if target not in STATES or not event_id or not reason:
            raise ValueError("transition requires valid state and provenance")
        changes = changes or {}
        if set(changes) - set(AXES):
            raise ValueError("unknown crisis severity axis")
        candidate = {**self.axes, **changes}
        if any(type(x) is not int or not 0 <= x <= 5 for x in candidate.values()):
            raise ValueError("invalid severity")
        self.history.append(dict(event_id=event_id, reason=reason,
                                 from_state=self.state, to_state=target,
                                 changes=changes.copy()))
        self.state, self.axes = target, candidate

@dataclass
class RegionalWorld:
    regions: dict[str, Region] = field(default_factory=dict)
    ontological_disclosure: bool = True

    def add_region(self, region: Region):
        if region.id in self.regions:
            raise ValueError("duplicate region")
        self.regions[region.id] = region

    def snapshot(self):
        return dict(version=1, ontological_disclosure=self.ontological_disclosure,
                    regions={name: asdict(region) for name, region in self.regions.items()})

    @classmethod
    def from_snapshot(cls, data):
        if data.get("version") != 1:
            raise ValueError("unsupported crisis snapshot")
        return cls(regions={name: Region(**item) for name, item in data["regions"].items()},
                   ontological_disclosure=data["ontological_disclosure"])
