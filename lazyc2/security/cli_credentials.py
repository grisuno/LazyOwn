"""CLI boot credentials: owner-only credential file and RBAC registration.

The C2 boot block resolves one effective (user, password) pair and must
persist it for the operator and register it in the RBAC store, so a
fresh lab run is never locked out of its own C2. No Flask imports here
so tests import this module directly.
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from pathlib import Path

log = logging.getLogger(__name__)

CREDENTIALS_FILE = ".c2_credentials.txt"
_FILE_MODE = 0o600


def write_credentials_file(username: str, password: str, path: str | Path = CREDENTIALS_FILE) -> Path:
    """Persist the effective boot credentials owner-only.

    Args:
        username: Effective C2 username.
        password: Effective C2 password.
        path: Destination (``.c2_credentials.txt`` by default).

    Returns:
        The written file path.

    Raises:
        OSError: When the file cannot be written.
    """
    target = Path(path)
    target.write_text(
        f"# LazyOwn C2 Credentials - Generated {datetime.now(UTC).isoformat()}\n"
        f"USERNAME={username}\n"
        f"PASSWORD={password}\n",
        encoding="utf-8",
    )
    os.chmod(target, _FILE_MODE)
    return target


def resolve_boot_credentials(
    user: str,
    password: str,
    rotate_on_boot: bool,
    generator,
    is_insecure,
) -> tuple[str, str, str]:
    """Resolve the effective boot credentials.

    Rotation wins over keeping: an explicit ``rotate_on_boot`` flag
    regenerates the pair every run, then insecure pairs are regenerated,
    and only strong pairs without the flag are kept as-is.

    Args:
        user: Incoming username.
        password: Incoming password.
        rotate_on_boot: Force regeneration every boot (config flag).
        generator: Callable returning a fresh ``(user, password)``.
        is_insecure: Predicate ``(user, password) -> bool``.

    Returns:
        ``(user, password, action)`` with ``action`` in
        ``{"kept", "rotated_insecure", "rotated_on_boot"}``.
    """
    if rotate_on_boot:
        new_user, new_password = generator()
        return new_user, new_password, "rotated_on_boot"
    if is_insecure(user, password):
        new_user, new_password = generator()
        return new_user, new_password, "rotated_insecure"
    return user, password, "kept"


def register_cli_user(
    store,
    username: str,
    password: str,
    hash_password,
    create_role: str = "admin",
) -> str:
    """Register or update the boot CLI user in an RBAC store.

    An existing account for the username gets its password refreshed;
    a new username is created with ``create_role``. An unreadable store
    is left untouched so corrupted operator state is never overwritten.

    Args:
        store: RBAC store exposing ``find_by_username``/``save``/
            ``create_user``.
        username: Effective boot username.
        password: Effective boot password (plain).
        hash_password: Callable turning a plain password into a hash.
        create_role: Role for accounts created here.

    Returns:
        ``"updated"``, ``"created"`` or ``"skipped_unreadable"``.
    """
    try:
        existing = store.find_by_username(username)
    except Exception as exc:
        log.error("[rbac] users store unreadable; boot credentials not registered: %s", exc)
        return "skipped_unreadable"
    hashed = hash_password(password)
    if existing is not None:
        existing.password_hash = hashed
        store.save(existing)
        log.info("[rbac] Updated CLI user password in RBAC store")
        return "updated"
    store.create_user(username=username, password_hash=hashed, role=create_role)
    log.info("[rbac] Registered CLI user in RBAC store as %s", create_role)
    return "created"


__all__ = ["CREDENTIALS_FILE", "register_cli_user", "resolve_boot_credentials", "write_credentials_file"]
