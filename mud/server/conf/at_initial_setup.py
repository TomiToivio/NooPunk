"""Initial game-world creation hook, called by Evennia once at installation."""
def at_initial_setup():
    from world.seed import seed_helsinki
    seed_helsinki()
