"""NoöPunk MUD settings (isolated from the Godot project)."""
from evennia.settings_default import *  # noqa: F401,F403

SERVERNAME = "NoöPunk MUD"
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Survivor"
BASE_ROOM_TYPECLASS = "typeclasses.rooms.ApocalypseRoom"
CMDSET_CHARACTER = "commands.default_cmdsets.NoopunkCharacterCmdSet"
AT_INITIAL_SETUP_HOOK_MODULE = "server.conf.at_initial_setup"
