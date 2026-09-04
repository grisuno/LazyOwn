"""Global pytest isolation hooks.

Resets module-level singleton state that otherwise leaks between tests and
causes order-dependent failures (the world-model singleton cached by
``modules.world_model.get_world_model``). Each test starts from a clean
singleton so a test can never observe engagement state written by an
earlier test.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _reset_world_model_singleton() -> None:
    """Drop the cached WorldModel before and after every test."""
    import modules.world_model as wm

    wm._default_wm = None
    yield
    wm._default_wm = None
