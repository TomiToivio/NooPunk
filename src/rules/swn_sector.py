"""NoöPunk sector movement: original SWN-inspired travel planning.

This module intentionally does not simulate the proprietary spike-drive rules
as a substitute for the sourcebook. It handles routes, capability and fuel
budgets using scenario-provided travel times and distances.
"""
from dataclasses import dataclass, field


class SectorError(ValueError):
    pass


@dataclass(frozen=True)
class Route:
    origin: str
    destination: str
    distance: int
    travel_days: int
    fuel_units: int
    required_drive: int = 1
    hazard: str = ""

    def __post_init__(self):
        if not self.origin or not self.destination or self.origin == self.destination:
            raise SectorError("route endpoints must be distinct")
        if any(type(n) is not int or n < 1 for n in
               (self.distance, self.travel_days, self.fuel_units, self.required_drive)):
            raise SectorError("route budgets and requirements must be positive integers")


@dataclass
class Ship:
    name: str
    location: str
    drive: int
    fuel: int
    fuel_capacity: int
    days_elapsed: int = 0
    log: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.name or not self.location or type(self.drive) is not int or self.drive < 0:
            raise SectorError("invalid ship")
        if type(self.fuel) is not int or type(self.fuel_capacity) is not int:
            raise SectorError("fuel must be an integer")
        if not 0 <= self.fuel <= self.fuel_capacity:
            raise SectorError("invalid fuel budget")
        if type(self.days_elapsed) is not int or self.days_elapsed < 0:
            raise SectorError("invalid elapsed time")

    def can_travel(self, route: Route) -> bool:
        return (self.location == route.origin and self.drive >= route.required_drive
                and self.fuel >= route.fuel_units)

    def travel(self, route: Route) -> dict:
        if not self.can_travel(route):
            raise SectorError("ship cannot traverse route with current drive, location or fuel")
        self.fuel -= route.fuel_units
        self.days_elapsed += route.travel_days
        self.location = route.destination
        event = {"from": route.origin, "to": route.destination,
                 "days": route.travel_days, "fuel_used": route.fuel_units,
                 "hazard": route.hazard}
        self.log.append(event)
        return event

    def refuel(self, units: int) -> None:
        if type(units) is not int or units <= 0 or self.fuel + units > self.fuel_capacity:
            raise SectorError("invalid refuel amount")
        self.fuel += units
