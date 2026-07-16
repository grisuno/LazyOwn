"""User management utilities for the C2 auth module.

Provides load/save helpers for both the legacy JSON user store and
the RBAC-backed store. The RBAC path falls through to lazyc2.py
globals during the migration period.
"""

from __future__ import annotations

import json
import os

USER_DATA_PATH = "users.json"


def configure(users_path: str = "users.json") -> None:
    """Set the path for the legacy JSON user file.

    Args:
        users_path: Path to the users JSON file.
    """
    global USER_DATA_PATH  # noqa: PLW0603
    USER_DATA_PATH = users_path


def load_users() -> list[dict]:
    """Load users from the JSON store or RBAC store.

    Returns:
        A list of user dicts.
    """
    try:
        from lazyc2 import _RBAC_AVAILABLE
        if _RBAC_AVAILABLE:
            from lazyc2 import get_rbac_store
            store = get_rbac_store()
            return [u.to_dict() for u in store.load_all()]
    except (ImportError, AttributeError):
        pass
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH) as f:
            return json.load(f)
    return []


def save_users(users: list[dict]) -> None:
    """Persist users to the JSON store or RBAC store.

    Args:
        users: List of user dicts.
    """
    try:
        from lazyc2 import _RBAC_AVAILABLE
        if _RBAC_AVAILABLE:
            from lazyc2 import get_rbac_store
            from modules.lazy_rbac import RBACUser
            store = get_rbac_store()
            for u_dict in users:
                user = RBACUser.from_dict(u_dict)
                store.save(user)
            return
    except (ImportError, AttributeError):
        pass
    with open(USER_DATA_PATH, "w") as f:
        json.dump(users, f, indent=4)
