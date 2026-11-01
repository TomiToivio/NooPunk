from evennia import DefaultCharacter

class Survivor(DefaultCharacter):
    """Persistent player character; CWN rules rather than a bespoke RPG chassis."""
    def at_object_creation(self):
        super().at_object_creation()
        for name in ("strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"):
            setattr(self.db, name, 10)
        self.db.hp = 5
        self.db.skills = {"notice": 0, "survive": 0, "talk": 0}
        self.db.food = 1
        self.db.water = 1
        self.db.faction = "UNSA"  # legacy compatibility
        self.db.reputation = 0  # legacy compatibility; scoped reputation lives separately
        from nopunk_mud.faction_tags import initial_state
        self.db.faction_tags = initial_state()
