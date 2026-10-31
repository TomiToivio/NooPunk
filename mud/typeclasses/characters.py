"""The MUD's character: an Evennia object that carries a CWN sheet (#946).

The sheet is stored as data (``db.cwn``) and read back through :class:`world.cwn.Sheet`.
Nothing on this object rolls anything itself — a command asks the sheet, the sheet asks
the shared kernel, and the shared kernel is the same one the tabletop and Godot rules use.

``at_object_creation`` is the only place a default character is minted, so a character
created by the admin, by the login flow or by a test all get the same legal CWN spread.
"""
from __future__ import annotations

from evennia.objects.objects import DefaultCharacter
from evennia.typeclasses.attributes import AttributeProperty

from world.cwn import Sheet
from world.factions import Faction, unsa


class CwnCharacter(DefaultCharacter):
    """A survivor with a CWN sheet and a place in the faction state."""

    #: One integer the player can see and spend: what they personally carry.
    supplies = AttributeProperty(0)

    def at_object_creation(self) -> None:
        super().at_object_creation()
        if not self.db.cwn:
            self.db.cwn = Sheet().to_dict()
        self.db.faction = self.db.faction or unsa().to_dict()
        #: Evennia stows a character away on logout and restores it from this room at home.
        #: Without a home, a player who types `home` ends up nowhere.
        try:
            from world.helsinki import start_room

            self.home = start_room()
        except Exception:  # the world may not be built yet; at_pre_puppet retries
            self.home = None

    @property
    def sheet(self) -> Sheet:
        """The sheet, rebuilt from stored data. A missing or corrupt sheet is repaired once."""
        try:
            return Sheet.from_dict(self.db.cwn)
        except Exception:
            self.db.cwn = Sheet().to_dict()
            return Sheet.from_dict(self.db.cwn)

    @property
    def faction(self) -> Faction:
        return Faction.from_dict(self.db.faction or unsa().to_dict())

    def save_faction(self, faction: Faction) -> None:
        self.db.faction = faction.to_dict()

    def at_pre_puppet(self, account, **kwargs):
        """Put the player back where they logged out, not where the framework parked them.

        Evennia stows a character away on logout: it sets ``location = None`` and remembers
        the room in ``db.prelogout_location``. Restoring *that* is the difference between a
        persistent world and a teleport on every reconnect. Limbo (the framework's own
        placeholder room) and "nowhere" both count as unplaced.
        """
        super().at_pre_puppet(account, **kwargs)
        from world.helsinki import start_room

        saved = self.db.prelogout_location
        try:
            placed = saved if saved and saved.pk and saved.key != "Limbo" else None
        except Exception:  # a deleted room leaves a dangling reference
            placed = None
        if not self.home or (self.home and self.home.key == "Limbo"):
            self.home = start_room()
        self.location = placed or start_room()
