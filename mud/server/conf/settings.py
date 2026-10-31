r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "NoöPunk MUD"

######################################################################
# NoöPunk MUD (#946)
#
# This is a MUD, not the Godot RPG. It shares canon and the CWN rules kernel
# (`<repo>/src/rules`, imported in world/cwn.py) and shares no runtime with Godot.
######################################################################

#: The character typeclass that carries a CWN sheet. One typeclass, so a character
#: created by the login flow, by the admin or by a test is the same kind of thing.
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.CwnCharacter"

#: Rooms and exits are ours, so the map can grow a rule without touching framework code.
BASE_ROOM_TYPECLASS = "typeclasses.rooms.NoopunkRoom"
BASE_EXIT_TYPECLASS = "typeclasses.exits.NoopunkExit"

#: Players read one screenful; the default banner assumes a browser client we do not ship.
#: Terminal play is the MVP (issue #946: "browser and/or terminal").
DEFAULT_HOME = "#2"



######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
