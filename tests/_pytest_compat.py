"""The two `pytest` features the root suite uses, without requiring `pytest`.

CI runs `python -m unittest discover -s tests`, and pytest is not installed there. Five test modules
imported pytest anyway, which made the whole `test` job fail at import time ("No module named
'pytest'") and hid every other test result behind it. Installing pytest instead would be worse: the
suite would go green while unittest silently skipped every module-level `test_*` function.

So this shim provides what those modules actually use — `pytest.raises` — and
:func:`register_module_functions` gives unittest something to discover in a pytest-style module.
Tests stay written the way their authors wrote them; CI runs them.
"""
from __future__ import annotations

import sys
import unittest
from contextlib import contextmanager

#: True only when pytest is already running us. The check has to happen *before* we import pytest
#: ourselves, otherwise both runners look identical.
_RUNNING_UNDER_PYTEST = "pytest" in sys.modules

try:  # a real pytest, when the suite is run under pytest
    import pytest as _real_pytest  # type: ignore[no-redef]
except ModuleNotFoundError:  # CI: `unittest discover`, no pytest installed
    _real_pytest = None


@contextmanager
def raises(exc_type, match: str | None = None):
    """`pytest.raises` semantics: the block must raise, and `match` must appear in the message."""
    case = unittest.TestCase()
    with case.assertRaises(exc_type) as caught:
        yield caught
    if match is not None:
        case.assertIn(match, str(caught.exception))


class _Mark:
    """`pytest.mark.parametrize`, reduced to what the suite uses: a name list and a value list."""

    @staticmethod
    def parametrize(argnames, values):
        names = ([part.strip() for part in argnames.split(",")] if isinstance(argnames, str)
                 else list(argnames))

        def decorate(function):
            function._parametrize = (names, list(values))  # type: ignore[attr-defined]
            return function

        return decorate


class _PytestShim:
    """Stand-in for the `pytest` module.

    Under pytest the two names delegate to the real implementation — a shadowed `mark.parametrize`
    that merely stores an attribute would make pytest call a parametrised function with no arguments.
    Without pytest, the local versions above are used.
    """

    # Delegate only while pytest is the runner. Under `unittest discover` the shim must own
    # `mark.parametrize`: a real pytest marker on a function that unittest calls directly just makes
    # the call fail on its missing arguments.
    raises = staticmethod(_real_pytest.raises
                          if (_real_pytest is not None and _RUNNING_UNDER_PYTEST) else raises)
    mark = (_real_pytest.mark
            if (_real_pytest is not None and _RUNNING_UNDER_PYTEST) else _Mark())

    @staticmethod
    def approx(value, rel: float = 1e-6, abs_: float = 1e-12):
        """A minimal `pytest.approx`: good enough for the float comparisons here."""
        return _Approx(value, rel, abs_)


class _Approx:
    def __init__(self, value, rel: float, abs_: float) -> None:
        self.value = value
        self.rel = rel
        self.abs = abs_

    def __eq__(self, other: object) -> bool:
        try:
            return abs(float(other) - float(self.value)) <= max(  # type: ignore[arg-type]
                self.abs, self.rel * abs(float(self.value)))
        except (TypeError, ValueError):
            return NotImplemented

    def __repr__(self) -> str:
        return f"approx({self.value!r})"


#: What the test modules import as `pytest`. Under pytest it delegates; without it, the shim runs.
pytest = _PytestShim()


def register_module_functions(namespace: dict) -> type:
    """Turn a module's pytest-style `test_*` functions into a unittest TestCase.

    Called at the bottom of a module with ``globals()``. Parameterised tests are not supported, and
    the shim does not pretend to be: if a module needs parametrisation it should use
    ``subTest``/``unittest`` directly.
    """
    case = type("ModuleLevelTests", (unittest.TestCase,), {})
    if _RUNNING_UNDER_PYTEST:
        # pytest already collects these functions; wrapping them would run each test twice and break
        # the parametrised ones, whose function objects pytest has replaced.
        return case
    module_name = namespace.get("__name__")
    for name in sorted(namespace):
        if not name.startswith("test_"):
            continue
        function = namespace[name]
        if not callable(function) or getattr(function, "__module__", None) not in (None, module_name):
            continue
        parametrize = getattr(function, "_parametrize", None)
        if parametrize is None:
            setattr(case, name, (lambda self, _fn=function: _fn()))
            continue

        names, values = parametrize

        def run(self, _fn=function, _names=names, _values=values):
            for value in _values:
                with self.subTest(value=value):
                    if len(_names) == 1:
                        _fn(value)
                    else:
                        _fn(*value)

        setattr(case, name, run)
    return case
