"""C2 data models extracted from lazyc2.py.

Breaking the circular dependency between lazyc2.py and blueprints.
"""

from flask_login import UserMixin

try:
    from modules.lazy_rbac import _RBAC_AVAILABLE, ROLE_DEFAULT, get_rbac_store
except ImportError:
    _RBAC_AVAILABLE = False
    get_rbac_store = None
    ROLE_DEFAULT = "operator"


class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data["id"]
        self.username = user_data["username"]
        self.password_hash = user_data["password_hash"]
        self.elo = user_data.get("elo", 0)
        self.role = user_data.get(
            "role", ROLE_DEFAULT if _RBAC_AVAILABLE else "operator"
        )
        self.mfa_enabled = user_data.get("mfa_enabled", False)
        self.mfa_secret = user_data.get("mfa_secret", "")
        self.recovery_codes = user_data.get("recovery_codes", [])
        self.tenant_id = user_data.get("tenant_id", "default")
