"""CLI authentication module — login against users.json with remember-me.

Authenticates CLI operators against the same ``users.json`` database
used by lazyc2.py, using werkzeug's scrypt password verification.

Supports a "remember me" token stored in ``payload.json`` under
``cli_remember_token`` so operators can skip login on subsequent
shell starts. The token is a random 48-byte URL-safe string bound to
the username and stored both in ``payload.json`` and per-user in
``users.json`` entries.
"""

from __future__ import annotations

import json
import os
import secrets
import time
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
USERS_PATH = BASE_DIR / "users.json"
PAYLOAD_PATH = BASE_DIR / "payload.json"
SESSIONS_DIR = BASE_DIR / "sessions"
CLI_SESSION_PATH = SESSIONS_DIR / "cli_session.json"

_TOKEN_BYTES = 48
_TOKEN_KEY = "cli_remember_token"
_AUTO_LOGIN_KEY = "cli_auto_login"


def _load_users() -> list[dict]:
    """Load the users.json database.

    Returns:
        List of user dicts, or empty list on any error.
    """
    if not USERS_PATH.exists():
        return []
    try:
        with open(USERS_PATH) as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def _save_users(users: list[dict]) -> bool:
    """Atomically write the users.json database.

    Refuses to overwrite an existing database with an empty list (a read
    failure upstream must never wipe the store), keeps the file readable
    only by its owner, and preserves the previous owner when running as
    root so mixed root / operator processes never lock each other out.

    Args:
        users: List of user dicts to persist.

    Returns:
        True on success.
    """
    if not users and USERS_PATH.exists():
        return False
    try:
        tmp = USERS_PATH.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(users, f, indent=4)
        os.chmod(tmp, 0o600)
        previous_owner = None
        if USERS_PATH.exists():
            previous_owner = USERS_PATH.stat().st_uid
        os.replace(tmp, USERS_PATH)
        os.chmod(USERS_PATH, 0o600)
        if os.geteuid() == 0 and previous_owner is not None:
            os.chown(USERS_PATH, previous_owner, -1)
        return True
    except Exception:
        return False


def _load_payload() -> dict:
    """Load payload.json.

    Returns:
        Payload dict, or empty dict.
    """
    if not PAYLOAD_PATH.exists():
        return {}
    try:
        with open(PAYLOAD_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_payload(payload: dict) -> bool:
    """Atomically write payload.json.

    Args:
        payload: Payload dict to persist.

    Returns:
        True on success.
    """
    try:
        tmp = PAYLOAD_PATH.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(payload, f, indent=2)
        os.replace(tmp, PAYLOAD_PATH)
        return True
    except Exception:
        return False


def user_exists(username: str) -> bool:
    """Check if a username already exists in users.json or RBAC store.

    Args:
        username: Username to check.

    Returns:
        True if the username already exists.
    """
    try:
        from modules.lazy_rbac import _RBAC_AVAILABLE as RBAC
        from modules.lazy_rbac import get_rbac_store
        if RBAC:
            store = get_rbac_store()
            return store.find_by_username(username) is not None
    except ImportError:
        pass

    users = _load_users()
    return any(isinstance(u, dict) and u.get("username") == username for u in users)


def register(username: str, password: str) -> dict[str, Any]:
    """Register a new operator in users.json.

    Follows the same logic as the lowazyc2.py /register endpoint.
    First user becomes admin; subsequent users get the default role.
    Minimum 12-character password.

    Args:
        username: Desired username.
        password: Cleartext password.

    Returns:
        Dict with ``success``, ``username``, ``role`` keys.
    """
    if not username or not password:
        return {"success": False, "error": "Username and password are required."}

    if len(password) < 12:
        return {"success": False, "error": "Password must be at least 12 characters."}

    if user_exists(username):
        return {"success": False, "error": "Username already exists."}

    try:
        from werkzeug.security import generate_password_hash
    except ImportError:
        return {"success": False, "error": "werkzeug not available — install with: pip install werkzeug"}

    try:
        from modules.lazy_rbac import _RBAC_AVAILABLE as RBAC
        from modules.lazy_rbac import Role, get_rbac_store

        if RBAC:
            store = get_rbac_store()
            role = Role.ADMIN.value if not any(
                u.role == Role.ADMIN.value for u in store.load_all()
            ) else Role.OPERATOR.value
            store.create_user(
                username=username,
                password_hash=generate_password_hash(password),
                role=role,
            )
            return {"success": True, "username": username, "role": role}
    except ImportError:
        pass

    users = _load_users()
    role = "admin" if not users else "user"

    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password_hash": generate_password_hash(password),
        "elo": 0,
        "role": role,
        "mfa_enabled": False,
        "mfa_secret": "",
        "recovery_codes": [],
        "tenant_id": "default",
    }
    users.append(new_user)
    if not _save_users(users):
        return {"success": False, "error": "Could not save users.json."}

    return {"success": True, "username": username, "role": role}


def verify_password(username: str, password: str) -> bool:
    """Verify a username/password against users.json using werkzeug.

    Args:
        username: Operator username.
        password: Clear-text password attempt.

    Returns:
        True if the credentials match a user in users.json.
    """
    try:
        from werkzeug.security import check_password_hash
    except ImportError:
        return False

    users = _load_users()
    for user in users:
        if isinstance(user, dict) and user.get("username") == username:
            pw_hash = user.get("password_hash", "")
            if not pw_hash:
                continue
            return check_password_hash(pw_hash, password)

    return False


def login(username: str, password: str, remember: bool = False) -> dict[str, Any]:
    """Authenticate a CLI operator and optionally persist a remember-me token.

    Args:
        username: Operator username.
        password: Clear-text password.
        remember: If True, persist a remember-me token in payload.json
            and users.json for auto-login on future shell starts.

    Returns:
        Dict with ``success``, ``username``, ``elo``, ``role``, ``remember`` keys.
    """
    if not verify_password(username, password):
        return {"success": False, "error": "Invalid username or password."}

    users = _load_users()
    user_entry = None
    for user in users:
        if isinstance(user, dict) and user.get("username") == username:
            user_entry = user
            break

    if user_entry is None:
        return {"success": False, "error": "User not found in database."}

    result: dict[str, Any] = {
        "success": True,
        "username": username,
        "elo": user_entry.get("elo", 0),
        "role": user_entry.get("role", "operator"),
    }

    if remember:
        token = secrets.token_urlsafe(_TOKEN_BYTES)
        user_entry["cli_remember_token"] = token

        if _save_users(users):
            payload = _load_payload()
            payload[_TOKEN_KEY] = token
            payload[_AUTO_LOGIN_KEY] = username
            _save_payload(payload)
            result["remember"] = True
        else:
            result["remember"] = False
            result["error_remember"] = "Could not persist remember-me token."
    else:
        result["remember"] = False

    _write_cli_session(username, user_entry.get("elo", 0), user_entry.get("role", "operator"))

    return result


def logout() -> dict[str, Any]:
    """Log out the current CLI operator and clear the remember-me token.

    Returns:
        Dict with ``success`` key.
    """
    session = _read_cli_session()
    if not session:
        return {"success": True, "message": "No active session."}

    username = session.get("username", "")

    payload = _load_payload()
    had_remember = _TOKEN_KEY in payload or _AUTO_LOGIN_KEY in payload

    if _TOKEN_KEY in payload:
        del payload[_TOKEN_KEY]
    if _AUTO_LOGIN_KEY in payload:
        del payload[_AUTO_LOGIN_KEY]
    if had_remember:
        _save_payload(payload)

    if username:
        users = _load_users()
        for user in users:
            if isinstance(user, dict) and user.get("username") == username:
                user.pop("cli_remember_token", None)
                break
        _save_users(users)

    _clear_cli_session()

    return {"success": True, "message": f"Logged out {username}."}


def try_auto_login() -> dict[str, Any]:
    """Attempt auto-login using the remember-me token from payload.json.

    Called at shell startup (preloop). If ``cli_auto_login`` is set in
    payload.json and the token matches a user's stored token, logs in
    silently without prompting for credentials.

    Returns:
        Dict with ``success``, ``username``, ``elo``, ``role``.
    """
    payload = _load_payload()

    if not payload.get(_AUTO_LOGIN_KEY) or not payload.get(_TOKEN_KEY):
        return {"success": False, "error": "No remember-me token configured."}

    username = payload[_AUTO_LOGIN_KEY]
    token = payload[_TOKEN_KEY]

    users = _load_users()
    for user in users:
        if isinstance(user, dict) and user.get("username") == username:
            stored_token = user.get("cli_remember_token")
            if stored_token and stored_token == token:
                _write_cli_session(
                    username,
                    user.get("elo", 0),
                    user.get("role", "operator"),
                )
                return {
                    "success": True,
                    "username": username,
                    "elo": user.get("elo", 0),
                    "role": user.get("role", "operator"),
                }

    return {"success": False, "error": "Remember-me token expired or invalid."}


def whoami() -> dict[str, Any]:
    """Return the currently logged-in CLI operator's identity.

    Returns:
        Dict with ``logged_in``, ``username``, ``elo``, ``role``.
    """
    session = _read_cli_session()
    if not session:
        return {"logged_in": False, "username": None}

    username = session.get("username", "")
    elo = session.get("elo", 0)
    role = session.get("role", "operator")

    try:
        from cli.engagement_hooks import get_karma_name

        karma = get_karma_name(elo)
    except ImportError:
        karma = ""

    return {
        "logged_in": True,
        "username": username,
        "elo": elo,
        "role": role,
        "karma": karma,
    }


def get_current_operator() -> str | None:
    """Return the current operator username, or None if not logged in.

    Returns:
        Username string or None.
    """
    session = _read_cli_session()
    if not session:
        return None
    return session.get("username")


def sync_elo_from_session(elo: int) -> None:
    """Update the CLI session ELO from engagement state.

    Args:
        elo: New ELO value to store in the session.
    """
    session = _read_cli_session()
    if session:
        session["elo"] = elo
        _write_cli_session_raw(session)

    username = session.get("username") if session else None
    if username:
        users = _load_users()
        for user in users:
            if isinstance(user, dict) and user.get("username") == username:
                user["elo"] = elo
                break
        _save_users(users)


def _read_cli_session() -> dict | None:
    """Read the CLI session file.

    Returns:
        Session dict or None.
    """
    if not CLI_SESSION_PATH.exists():
        return None
    try:
        with open(CLI_SESSION_PATH) as f:
            return json.load(f)
    except Exception:
        return None


def _write_cli_session(username: str, elo: int, role: str) -> None:
    """Write the CLI session file.

    Args:
        username: Operator username.
        elo: Current ELO score.
        role: RBAC role.
    """
    _write_cli_session_raw(
        {
            "username": username,
            "elo": elo,
            "role": role,
            "logged_in_at": time.time(),
        }
    )


def _write_cli_session_raw(data: dict) -> None:
    """Write arbitrary dict to the CLI session file.

    Args:
        data: Session data dict.
    """
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        tmp = CLI_SESSION_PATH.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, CLI_SESSION_PATH)
    except Exception:
        pass


def _clear_cli_session() -> None:
    """Remove the CLI session file."""
    try:
        if CLI_SESSION_PATH.exists():
            CLI_SESSION_PATH.unlink()
    except Exception:
        pass


def needs_login() -> bool:
    """Check if the current session has a logged-in operator.

    Returns:
        True if no valid session exists.
    """
    return whoami().get("logged_in") is not True


__all__ = [
    "login",
    "logout",
    "register",
    "try_auto_login",
    "user_exists",
    "whoami",
    "needs_login",
    "verify_password",
    "get_current_operator",
    "sync_elo_from_session",
]
