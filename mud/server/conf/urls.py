"""URL conf for the NoöPunk MUD.

The MUD is telnet-first; there is no website to serve. Evennia's default settings point `ROOT_URLCONF` at a
`web` package that a full game template ships and this scaffold does not, so the conf is redirected here and
left empty rather than shipping a stub site.
"""
from django.urls import path  # noqa: F401  (kept so the module reads like a urlconf)

urlpatterns: list = []
