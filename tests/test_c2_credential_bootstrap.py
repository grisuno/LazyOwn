"""C2 boot credential contract: file, console and RBAC registration.

SDD: the operator boot credentials must always (1) land in
``.c2_credentials.txt`` mode 0600 and (2) be registered in the RBAC
store, so a fresh lab run is never locked out of its own C2.
"""

from __future__ import annotations

import os
from pathlib import Path

from lazyc2.security.cli_credentials import (
    register_cli_user,
    resolve_boot_credentials,
    write_credentials_file,
)


class _FakeUser:
    def __init__(self, username: str, password_hash: str = "", role: str = "operator"):
        self.username = username
        self.password_hash = password_hash
        self.role = role


class _FakeStore:
    def __init__(self, users: list[_FakeUser] | None = None, unreadable: bool = False):
        self._users = users if users is not None else []
        self._unreadable = unreadable
        self.saved: list = []
        self.created: list = []

    def find_by_username(self, username):
        if self._unreadable:
            raise RuntimeError("unreadable")
        for user in self._users:
            if user.username == username:
                return user
        return None

    def save(self, user):
        self.saved.append(user)

    def create_user(self, username, password_hash, role="operator"):
        created = _FakeUser(username, password_hash, role)
        self.created.append(created)
        self._users.append(created)
        return created


def test_credentials_file_written_owner_only(tmp_path: Path) -> None:
    path = write_credentials_file("operator1", "s3cret-pass-123", path=tmp_path / ".c2_credentials.txt")
    content = path.read_text(encoding="utf-8")
    assert "USERNAME=operator1" in content
    assert "PASSWORD=s3cret-pass-123" in content
    assert os.stat(path).st_mode & 0o777 == 0o600


def test_register_cli_user_updates_existing(tmp_path: Path) -> None:
    store = _FakeStore(users=[_FakeUser("op", "old-hash")])
    action = register_cli_user(store, "op", "new-pass-1234", hash_password=lambda p: f"hash({p})")
    assert action == "updated"
    assert store.created == []
    assert store.saved and store.saved[0].password_hash == "hash(new-pass-1234)"


def test_register_cli_user_creates_when_new(tmp_path: Path) -> None:
    store = _FakeStore(users=[_FakeUser("someone-else", "hash-x", "operator")])
    action = register_cli_user(store, "fresh-lab-op", "random-pass-1234", hash_password=lambda p: f"hash({p})")
    assert action == "created"
    assert store.created[0].role == "admin"


def test_register_cli_user_skips_unreadable_store() -> None:
    store = _FakeStore(unreadable=True)
    action = register_cli_user(store, "op", "whatever-pass-123", hash_password=str)
    assert action == "skipped_unreadable"
    assert store.created == [] and store.saved == []


def test_register_cli_user_never_touches_other_accounts(tmp_path: Path) -> None:
    untouched = _FakeUser("admin", "original-hash", "admin")
    store = _FakeStore(users=[untouched])
    register_cli_user(store, "new-cli-op", "fresh-pass-1234", hash_password=lambda p: f"hash({p})")
    assert untouched.password_hash == "original-hash"
    assert store.saved == []


REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYC2_SRC = (REPO_ROOT / "lazyc2.py").read_text(encoding="utf-8")


def _resolve(user: str, password: str, rotate: bool) -> tuple[str, str, str]:
    """Resolve through the real helper with deterministic seams."""
    return resolve_boot_credentials(
        user,
        password,
        rotate_on_boot=rotate,
        generator=lambda: ("fresh-user-42", "fresh-pass-9876"),
        is_insecure=lambda u, p: u == "admin" and p == "admin123",
    )


def test_resolve_rotates_insecure_credentials() -> None:
    user, password, action = _resolve("admin", "admin123", rotate=False)
    assert action == "rotated_insecure"
    assert (user, password) == ("fresh-user-42", "fresh-pass-9876")


def test_resolve_keeps_strong_credentials() -> None:
    user, password, action = _resolve("7yzaiitom2gv", "2a4C7IRvn2I601yTfRHD", rotate=False)
    assert action == "kept"
    assert (user, password) == ("7yzaiitom2gv", "2a4C7IRvn2I601yTfRHD")


def test_resolve_on_boot_flag_wins_over_strong_creds() -> None:
    user, password, action = _resolve("7yzaiitom2gv", "2a4C7IRvn2I601yTfRHD", rotate=True)
    assert action == "rotated_on_boot"
    assert (user, password) == ("fresh-user-42", "fresh-pass-9876")


def test_boot_block_applies_rotation_flag() -> None:
    """The boot block must consult rotate_c2_creds_on_boot before keeping creds."""
    start = LAZYC2_SRC.index("if _RUN_MAIN and len(sys.argv) > 3:")
    block = LAZYC2_SRC[start : start + 4000]
    assert "rotate_c2_creds_on_boot" in block
    assert "_resolve_boot_credentials(" in block


def test_revshell_listener_is_not_login_gated() -> None:
    """The background listener must not wear the login_required decorator."""
    assert "@login_required\ndef start_reverse_shell" not in LAZYC2_SRC


def test_boot_block_writes_file_and_registers_cli_user() -> None:
    """The boot block must persist and register the effective credentials."""
    start = LAZYC2_SRC.index("if _RUN_MAIN and len(sys.argv) > 3:")
    block = LAZYC2_SRC[start : start + 4000]
    assert "_write_c2_credentials_file(USERNAME, PASSWORD)" in block
    assert "_register_cli_user(" in block
    assert "skipping creation" not in block


def test_boot_starts_revshell_listener_thread() -> None:
    """The C2 main block must start the reverse-shell listener thread."""
    start = LAZYC2_SRC.index('if __name__ == "__main__":')
    block = LAZYC2_SRC[start:]
    assert 'threading.Thread(target=start_reverse_shell, daemon=True, name="revshell-listener")' in block


def test_revshell_listener_accepts_multiple_sessions() -> None:
    """The listener must loop over incoming connections, not accept once."""
    start = LAZYC2_SRC.index("def start_reverse_shell():")
    block = LAZYC2_SRC[start : LAZYC2_SRC.index("@app.route", start)]
    assert "while True:" in block
    assert "server_socket.accept()" in block
