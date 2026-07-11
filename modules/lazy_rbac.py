"""
modules/lazy_rbac.py
====================
Role-Based Access Control, Multi-Factor Authentication, and Multi-Tenancy
for the LazyOwn RedTeam Framework.

Provides:
- RBAC: admin, operator, viewer, auditor roles with permission enforcement
- MFA: TOTP-based multi-factor auth (self-hosted, pyotp, no external APIs)
- Multi-tenancy: payload profiles + session isolation per engagement
- Decorators: @require_role, @require_permission for Flask routes
- CLI integration: command-level permission checks

Architecture
------------
- Roles are defined as enums with permission bitmasks
- Users stored in users.json with role, mfa_secret, mfa_enabled fields
- Tenancy managed via payloads/ directory with named profiles
- Zero cost: pyotp is already a dependency, no external services needed
"""

from __future__ import annotations

import base64
import enum
import hashlib
import hmac
import json
import logging
import os
import secrets
import struct
import time
from dataclasses import dataclass, field, asdict
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union

import pyotp
from flask import abort, flash, jsonify, redirect, request, session, url_for

log = logging.getLogger("lazy_rbac")

DEFAULT_USERS_PATH = "users.json"
DEFAULT_PAYLOADS_DIR = "payloads"
DEFAULT_PAYLOAD_PATH = "payload.json"
DEFAULT_SESSIONS_DIR = "sessions"
DEFAULT_CONFIG_PATH = "config.json"
MFA_ISSUER = "LazyOwn"

RECOVERY_CODES_COUNT = 8
RECOVERY_CODE_LENGTH = 10

ROLE_DEFAULT = "operator"


class Role(enum.Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"
    AUDITOR = "auditor"

    @classmethod
    def valid_roles(cls) -> Set[str]:
        return {r.value for r in cls}


class Permission(enum.Enum):
    USER_MANAGE = "user_manage"
    CONFIG_EDIT = "config_edit"
    CMD_RUN = "cmd_run"
    CMD_DESTRUCTIVE = "cmd_destructive"
    REPORT_VIEW = "report_view"
    REPORT_GENERATE = "report_generate"
    SESSION_VIEW = "session_view"
    SESSION_MANAGE = "session_manage"
    AUDIT_VIEW = "audit_view"
    COLLAB_JOIN = "collab_join"
    COLLAB_PUBLISH = "collab_publish"
    COLLAB_LOCK = "collab_lock"
    TENANT_MANAGE = "tenant_manage"


ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.ADMIN: set(Permission),
    Role.OPERATOR: {
        Permission.CMD_RUN,
        Permission.CMD_DESTRUCTIVE,
        Permission.REPORT_VIEW,
        Permission.REPORT_GENERATE,
        Permission.SESSION_VIEW,
        Permission.SESSION_MANAGE,
        Permission.AUDIT_VIEW,
        Permission.COLLAB_JOIN,
        Permission.COLLAB_PUBLISH,
        Permission.COLLAB_LOCK,
    },
    Role.VIEWER: {
        Permission.REPORT_VIEW,
        Permission.SESSION_VIEW,
    },
    Role.AUDITOR: {
        Permission.REPORT_VIEW,
        Permission.SESSION_VIEW,
        Permission.AUDIT_VIEW,
    },
}

_ROLE_HIERARCHY: Dict[Role, List[Role]] = {
    Role.ADMIN: [Role.ADMIN, Role.OPERATOR, Role.VIEWER, Role.AUDITOR],
    Role.OPERATOR: [Role.OPERATOR, Role.VIEWER, Role.AUDITOR],
    Role.VIEWER: [Role.VIEWER],
    Role.AUDITOR: [Role.AUDITOR],
}


@dataclass
class RBACUser:
    id: int
    username: str
    password_hash: str
    role: str = ROLE_DEFAULT
    mfa_enabled: bool = False
    mfa_secret: str = ""
    recovery_codes: List[str] = field(default_factory=list)
    elo: int = 0
    tenant_id: str = "default"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RBACUser":
        defaults = {
            "role": ROLE_DEFAULT,
            "mfa_enabled": False,
            "mfa_secret": "",
            "recovery_codes": [],
            "elo": 0,
            "tenant_id": "default",
        }
        merged = {**defaults, **data}
        return cls(
            id=merged["id"],
            username=merged["username"],
            password_hash=merged["password_hash"],
            role=merged["role"],
            mfa_enabled=merged["mfa_enabled"],
            mfa_secret=merged["mfa_secret"],
            recovery_codes=merged["recovery_codes"],
            elo=merged["elo"],
            tenant_id=merged["tenant_id"],
        )

    def get_role(self) -> Role:
        try:
            return Role(self.role)
        except ValueError:
            return Role.OPERATOR

    def has_permission(self, permission: Permission) -> bool:
        role = self.get_role()
        return permission in ROLE_PERMISSIONS.get(role, set())

    def can_manage_role(self, target_role: str) -> bool:
        """Check if this user can assign/manage the given role."""
        try:
            target = Role(target_role)
        except ValueError:
            return False
        return target in _ROLE_HIERARCHY.get(self.get_role(), [])

    def get_mfa_provisioning_uri(self) -> str:
        if not self.mfa_secret:
            return ""
        return pyotp.totp.TOTP(self.mfa_secret).provisioning_uri(
            name=self.username, issuer_name=MFA_ISSUER
        )

    def verify_totp(self, token: str) -> bool:
        if not self.mfa_secret or not self.mfa_enabled:
            return True
        return pyotp.TOTP(self.mfa_secret).verify(token, valid_window=1)

    def verify_recovery_code(self, code: str) -> bool:
        code = code.strip().replace("-", "").upper()
        for stored in self.recovery_codes:
            stored_clean = stored.strip().replace("-", "").upper()
            if hmac.compare_digest(code, stored_clean):
                return True
        return False

    def consume_recovery_code(self, code: str) -> bool:
        code = code.strip().replace("-", "").upper()
        for i, stored in enumerate(self.recovery_codes):
            stored_clean = stored.strip().replace("-", "").upper()
            if hmac.compare_digest(code, stored_clean):
                self.recovery_codes.pop(i)
                return True
        return False


class RBACStore:
    """Persistence layer for RBAC users."""

    def __init__(self, users_path: str = DEFAULT_USERS_PATH):
        self._users_path = Path(users_path)
        self._lock = __import__("threading").RLock()

    def _read_users(self) -> list:
        if not self._users_path.exists():
            return []
        try:
            return json.loads(self._users_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError) as exc:
            log.warning("Failed to read users.json: %s", exc)
            return []

    def _write_users(self, users: list) -> None:
        self._users_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._users_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(users, indent=4, default=str), encoding="utf-8")
        tmp.replace(self._users_path)

    def load_all(self) -> List[RBACUser]:
        with self._lock:
            return [RBACUser.from_dict(u) for u in self._read_users()]

    def find_by_id(self, user_id: int) -> Optional[RBACUser]:
        for user in self.load_all():
            if user.id == user_id:
                return user
        return None

    def find_by_username(self, username: str) -> Optional[RBACUser]:
        for user in self.load_all():
            if user.username == username:
                return user
        return None

    def save(self, user: RBACUser) -> None:
        with self._lock:
            users = self._read_users()
            updated = False
            for i, u in enumerate(users):
                if u.get("id") == user.id:
                    users[i] = user.to_dict()
                    updated = True
                    break
            if not updated:
                users.append(user.to_dict())
            self._write_users(users)

    def create_user(
        self,
        username: str,
        password_hash: str,
        role: str = ROLE_DEFAULT,
        tenant_id: str = "default",
    ) -> RBACUser:
        with self._lock:
            users = self._read_users()
            new_id = max((u.get("id", 0) for u in users), default=0) + 1
            new_user = RBACUser(
                id=new_id,
                username=username,
                password_hash=password_hash,
                role=role if role in Role.valid_roles() else ROLE_DEFAULT,
                tenant_id=tenant_id,
            )
            users.append(new_user.to_dict())
            self._write_users(users)
            return new_user

    def delete_user(self, user_id: int) -> bool:
        with self._lock:
            users = self._read_users()
            new_users = [u for u in users if u.get("id") != user_id]
            if len(new_users) == len(users):
                return False
            self._write_users(new_users)
            return True

    def update_role(self, user_id: int, new_role: str) -> Optional[RBACUser]:
        if new_role not in Role.valid_roles():
            return None
        user = self.find_by_id(user_id)
        if not user:
            return None
        user.role = new_role
        self.save(user)
        return user

    def enable_mfa(self, user_id: int) -> Optional[RBACUser]:
        user = self.find_by_id(user_id)
        if not user:
            return None
        user.mfa_secret = pyotp.random_base32()
        user.mfa_enabled = True
        user.recovery_codes = _generate_recovery_codes()
        self.save(user)
        return user

    def disable_mfa(self, user_id: int) -> Optional[RBACUser]:
        user = self.find_by_id(user_id)
        if not user:
            return None
        user.mfa_enabled = False
        user.mfa_secret = ""
        user.recovery_codes = []
        self.save(user)
        return user

    def consume_recovery_code(self, user_id: int, code: str) -> bool:
        user = self.find_by_id(user_id)
        if not user:
            return False
        result = user.consume_recovery_code(code)
        if result:
            self.save(user)
        return result

    def ensure_admin(self, username: str, password_hash: str) -> RBACUser:
        """Ensure at least one admin exists, creating one if needed."""
        users = self.load_all()
        admins = [u for u in users if u.role == Role.ADMIN.value]
        if admins:
            return admins[0]
        return self.create_user(
            username=username,
            password_hash=password_hash,
            role=Role.ADMIN.value,
        )


def _generate_recovery_codes(count: int = RECOVERY_CODES_COUNT) -> List[str]:
    codes = []
    for _ in range(count):
        code = "-".join(
            secrets.token_hex(RECOVERY_CODE_LENGTH // 4).upper()[:5]
            for _ in range(2)
        )
        codes.append(code)
    return codes


_TENANCY_STORE: Dict[str, "TenantConfig"] = {}


@dataclass
class TenantConfig:
    tenant_id: str
    name: str
    payload_path: str
    sessions_dir: str
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, tenant_id: str, name: str, payload_path: str) -> "TenantConfig":
        sessions_dir = os.path.join("sessions", tenant_id)
        return cls(
            tenant_id=tenant_id,
            name=name,
            payload_path=payload_path,
            sessions_dir=sessions_dir,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TenantConfig":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class TenantManager:
    """Multi-tenancy engine: payload profiles + session isolation."""

    def __init__(
        self,
        payloads_dir: str = DEFAULT_PAYLOADS_DIR,
        config_path: str = DEFAULT_CONFIG_PATH,
        default_payload: str = DEFAULT_PAYLOAD_PATH,
    ):
        self._payloads_dir = Path(payloads_dir)
        self._config_path = Path(config_path)
        self._default_payload = default_payload
        self._active_tenant: Optional[str] = None
        self._tenants: Dict[str, TenantConfig] = {}
        self._load_config()

    def _load_config(self) -> None:
        if self._config_path.exists():
            try:
                data = json.loads(self._config_path.read_text(encoding="utf-8"))
                self._active_tenant = data.get("active_tenant")
                for t in data.get("tenants", []):
                    tc = TenantConfig.from_dict(t)
                    self._tenants[tc.tenant_id] = tc
            except (json.JSONDecodeError, IOError) as exc:
                log.warning("Failed to load tenancy config: %s", exc)

    def _save_config(self) -> None:
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "active_tenant": self._active_tenant,
            "tenants": [t.to_dict() for t in self._tenants.values()],
        }
        tmp = self._config_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=4), encoding="utf-8")
        tmp.replace(self._config_path)

    def list_tenants(self) -> List[TenantConfig]:
        return list(self._tenants.values())

    def get_active(self) -> Optional[TenantConfig]:
        if self._active_tenant:
            return self._tenants.get(self._active_tenant)
        return None

    def get_active_payload_path(self) -> str:
        active = self.get_active()
        if active:
            return active.payload_path
        return self._default_payload

    def get_active_sessions_dir(self) -> str:
        active = self.get_active()
        if active:
            return active.sessions_dir
        return DEFAULT_SESSIONS_DIR

    def get_payload_for_tenant(self, tenant_id: str) -> str:
        tc = self._tenants.get(tenant_id)
        if tc:
            return tc.payload_path
        return self._default_payload

    def create_tenant(self, name: str, base_payload: Optional[str] = None) -> TenantConfig:
        tenant_id = _slugify(name)
        if tenant_id in self._tenants:
            raise ValueError(f"Tenant '{tenant_id}' already exists")

        self._payloads_dir.mkdir(parents=True, exist_ok=True)
        target_payload = self._payloads_dir / f"{tenant_id}.json"

        if base_payload and os.path.exists(base_payload):
            target_payload.write_text(Path(base_payload).read_text(encoding="utf-8"))
        elif os.path.exists(self._default_payload):
            target_payload.write_text(Path(self._default_payload).read_text(encoding="utf-8"))
        else:
            target_payload.write_text("{}")

        sessions_dir = os.path.join("sessions", tenant_id)
        os.makedirs(sessions_dir, exist_ok=True)

        tc = TenantConfig.from_payload(
            tenant_id=tenant_id,
            name=name,
            payload_path=str(target_payload),
        )
        self._tenants[tenant_id] = tc
        if not self._active_tenant:
            self._active_tenant = tenant_id
        self._save_config()
        return tc

    def switch_tenant(self, tenant_id: str) -> TenantConfig:
        if tenant_id not in self._tenants:
            raise ValueError(f"Tenant '{tenant_id}' not found")
        self._active_tenant = tenant_id
        self._save_config()
        sessions_dir = self._tenants[tenant_id].sessions_dir
        os.makedirs(sessions_dir, exist_ok=True)
        return self._tenants[tenant_id]

    def delete_tenant(self, tenant_id: str) -> bool:
        if tenant_id not in self._tenants:
            return False
        del self._tenants[tenant_id]
        if self._active_tenant == tenant_id:
            self._active_tenant = None
        self._save_config()
        return True

    def ensure_default_tenant(self) -> TenantConfig:
        slug = _slugify("Default Engagement")
        if slug in self._tenants:
            return self._tenants[slug]
        try:
            return self.create_tenant("Default Engagement")
        except ValueError:
            return self._tenants.get(slug, self.create_tenant("default_tenant"))


def _slugify(name: str) -> str:
    import re
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug)
    return slug.strip("_") or "default"


def init_rbac_store(users_path: str = DEFAULT_USERS_PATH) -> RBACStore:
    return RBACStore(users_path)


def init_tenant_manager(
    payloads_dir: str = DEFAULT_PAYLOADS_DIR,
    config_path: str = DEFAULT_CONFIG_PATH,
    default_payload: str = DEFAULT_PAYLOAD_PATH,
) -> TenantManager:
    return TenantManager(
        payloads_dir=payloads_dir,
        config_path=config_path,
        default_payload=default_payload,
    )


def require_role(*roles: str):
    """Flask decorator: require one of the given roles. Must be used WITH @login_required."""

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            from flask_login import current_user

            if not current_user.is_authenticated:
                return redirect(url_for("login"))

            rbac_user = _get_rbac_user(current_user)
            if not rbac_user:
                abort(403)

            if rbac_user.role not in roles:
                flash("Access denied: insufficient role.", "error")
                abort(403)

            return f(*args, **kwargs)

        return decorated

    return decorator


def require_permission(*permissions: str):
    """Flask decorator: require specific permissions."""

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            from flask_login import current_user

            if not current_user.is_authenticated:
                return redirect(url_for("login"))

            rbac_user = _get_rbac_user(current_user)
            if not rbac_user:
                abort(403)

            for perm_name in permissions:
                try:
                    perm = Permission(perm_name)
                except ValueError:
                    continue
                if not rbac_user.has_permission(perm):
                    flash(f"Access denied: missing permission '{perm_name}'.", "error")
                    abort(403)

            return f(*args, **kwargs)

        return decorated

    return decorator


def require_mfa(f: Callable) -> Callable:
    """Decorator that enforces MFA before accessing protected routes."""

    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        from flask_login import current_user

        if not current_user.is_authenticated:
            return redirect(url_for("login"))

        rbac_user = _get_rbac_user(current_user)
        if not rbac_user:
            abort(403)

        if rbac_user.mfa_enabled and not session.get("mfa_verified"):
            session["mfa_pending_route"] = request.path
            return redirect(url_for("mfa_verify"))

        return f(*args, **kwargs)

    return decorated


def _get_rbac_user(flask_user: Any) -> Optional[RBACUser]:
    """Extract RBACUser from Flask-Login current_user."""
    try:
        store = _get_rbac_store()
        return store.find_by_id(int(flask_user.id))
    except (AttributeError, ValueError, TypeError):
        return None


_rbac_store: Optional[RBACStore] = None
_tenant_manager: Optional[TenantManager] = None


def _get_rbac_store() -> RBACStore:
    global _rbac_store
    if _rbac_store is None:
        _rbac_store = RBACStore()
    return _rbac_store


def get_rbac_store() -> RBACStore:
    return _get_rbac_store()


def set_rbac_store(store: RBACStore) -> None:
    global _rbac_store
    _rbac_store = store


def get_tenant_manager() -> TenantManager:
    global _tenant_manager
    if _tenant_manager is None:
        _tenant_manager = TenantManager()
    return _tenant_manager


def set_tenant_manager(tm: TenantManager) -> None:
    global _tenant_manager
    _tenant_manager = tm


def check_cli_permission(username: str, permission: str) -> bool:
    """Check if a CLI user has the given permission."""
    store = _get_rbac_store()
    user = store.find_by_username(username)
    if not user:
        return False
    try:
        return user.has_permission(Permission(permission))
    except ValueError:
        return False


def get_user_role(username: str) -> str:
    store = _get_rbac_store()
    user = store.find_by_username(username)
    if not user:
        return ROLE_DEFAULT
    return user.role


def generate_mfa_qr_url(secret: str, username: str) -> str:
    """Generate a QR code data URI for MFA setup (local, no external API).

    Uses the /mfa/qr/<username> endpoint which generates the QR code
    server-side as an SVG image. Zero external dependencies.
    """
    return f"/mfa/qr/{username}"


def generate_qr_svg(data: str) -> str:
    """Generate an SVG QR code image from text data.

    Pure Python implementation. Automatically selects the appropriate
    QR version based on data length. Zero external dependencies.
    """
    data_str = data.encode("latin-1", errors="replace").decode("latin-1")
    version = _qr_choose_version(data_str)
    if version is None:
        return _qr_svg_error("Data too long for QR code (max version 6)")

    bit_list = _qr_encode_alphanumeric(data_str, version)
    modules, size = _qr_blank_matrix(version)
    data_positions = _qr_data_bits_positions(modules, size)

    total_data_bits = len(data_positions)
    ec_words = _qr_ec_codewords(version)
    data_bytes = total_data_bits // 8

    bit_idx = 0
    for pos in data_positions:
        if bit_idx < total_data_bits:
            modules[pos[0]][pos[1]] = bit_list[bit_idx] if bit_idx < len(bit_list) else 0
            bit_idx += 1

    codewords = _bits_to_bytes(
        [modules[p[0]][p[1]] for p in data_positions], total_data_bits
    )
    ec_bytes = _reed_solomon_encode(codewords, ec_words)
    final = codewords + ec_bytes

    bit_idx = 0
    for pos in data_positions:
        if bit_idx < len(final) * 8:
            byte_idx = bit_idx // 8
            bit_offset = 7 - (bit_idx % 8)
            val = (final[byte_idx] >> bit_offset) & 1
            modules[pos[0]][pos[1]] = val
            bit_idx += 1

    mask = _qr_best_mask(modules, size)
    modules = _qr_apply_mask(modules, size, mask)
    _qr_add_format_info(modules, size, 0b01, mask)

    return _qr_render_svg(modules, size)


_QR_CAPACITY_ALPHANUM_L = {
    1: 25, 2: 47, 3: 77, 4: 114, 5: 154, 6: 195,
}


def _qr_choose_version(data: str) -> int | None:
    chars = len(data)
    for v in sorted(_QR_CAPACITY_ALPHANUM_L.keys()):
        if chars <= _QR_CAPACITY_ALPHANUM_L[v]:
            return v
    return None


def _qr_ec_codewords(version: int) -> int:
    ec_table = {1: 7, 2: 10, 3: 15, 4: 20, 5: 26, 6: 18}
    return ec_table.get(version, 10)


def _qr_encode_alphanumeric(data: str, version: int) -> list:
    ALPHANUMERIC = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
    capacity = _QR_CAPACITY_ALPHANUM_L.get(version, 47)

    chars = list(data.upper())
    bits = []

    bits.append(0)
    bits.append(0)
    bits.append(1)
    bits.append(0)

    num_chars = len(chars)
    length_bits = 9 if version <= 9 else 11
    for b in range(length_bits - 1, -1, -1):
        bits.append((num_chars >> b) & 1)

    i = 0
    while i < len(chars):
        v1 = ALPHANUMERIC.find(chars[i])
        if v1 < 0:
            v1 = 0
        if i + 1 < len(chars):
            v2 = ALPHANUMERIC.find(chars[i + 1])
            if v2 < 0:
                v2 = 0
            val = v1 * 45 + v2
            for b in range(10, -1, -1):
                bits.append((val >> b) & 1)
            i += 2
        else:
            for b in range(5, -1, -1):
                bits.append((v1 >> b) & 1)
            i += 1

    data_bits = _qr_data_bits_for_version(version)
    if len(bits) >= data_bits:
        bits = bits[:data_bits]

    terminator_added = False
    while len(bits) < data_bits:
        if len(bits) + 4 <= data_bits and not terminator_added:
            bits.extend([0, 0, 0, 0])
            terminator_added = True
        elif (len(bits) % 8) != 0:
            bits.append(0)
        else:
            pad = 0
            bits.append((0xEC >> (7 - (len(bits) % 8))) & 1)
            if (len(bits) + 1) % 8 == 0 and len(bits) + 8 <= data_bits:
                for _ in range(8):
                    bits.append((0x11 >> (7 - (len(bits) % 8))) & 1)

    return bits[:data_bits]


def _qr_data_bits_for_version(version: int) -> int:
    size = 17 + 4 * version
    total = size * size
    finder_area = 3 * (7 * 7) + (7 * 6) * 2 + 6 * 6
    timing = 2 * (size - 2 * 8)
    dark_module = 1
    format_info = 30
    reserved = finder_area + timing + dark_module + format_info
    return total - reserved


def _qr_blank_matrix(version: int) -> tuple:
    size = 17 + 4 * version
    matrix = [[0] * size for _ in range(size)]
    _qr_place_finders(matrix, size)
    _qr_place_timing(matrix, size)
    _qr_place_dark_module(matrix, size, version)
    return matrix, size


def _qr_place_dark_module(matrix, size, version=2):
    matrix[4 * version + 9][8] = 1


def _qr_add_format_info(modules, size, ecl_bits, mask):
    fmt = (ecl_bits << 3) | mask
    fmt_val = fmt << 10
    fmt_poly = 0b10100110111
    for i in range(4, -1, -1):
        if fmt_val & (1 << (i + 10)):
            fmt_val ^= fmt_poly << i
    fmt_final = (fmt << 10) | (fmt_val & 0x3FF)
    fmt_final ^= 0b101010000010010

    for i in range(6):
        modules[i][8] = (fmt_final >> i) & 1
    modules[7][8] = (fmt_final >> 6) & 1
    modules[8][8] = (fmt_final >> 7) & 1
    modules[8][7] = (fmt_final >> 8) & 1
    for i in range(6):
        modules[8][5 - i] = (fmt_final >> (9 + i)) & 1
    for i in range(7):
        modules[size - 1 - i][8] = (fmt_final >> i) & 1
    for i in range(8):
        modules[8][size - 8 + i] = (fmt_final >> (14 - i)) & 1
    modules[8][size - 8] = 1


def _qr_svg_error(msg: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" width="200" height="50">'
        f'<rect width="200" height="50" fill="#fee"/>'
        f'<text x="10" y="30" font-size="12" fill="red">{msg}</text>'
        f'</svg>'
    )


def _qr_place_finders(matrix, size):
    for r, c in [(0, 0), (0, size - 7), (size - 7, 0)]:
        for i in range(7):
            for j in range(7):
                matrix[r + i][c + j] = 1 if (
                    i == 0 or i == 6 or j == 0 or j == 6
                    or (2 <= i <= 4 and 2 <= j <= 4)
                ) else 0


def _qr_place_timing(matrix, size):
    for i in range(8, size - 8):
        matrix[6][i] = (i % 2 == 0)
        matrix[i][6] = (i % 2 == 0)


def _qr_data_bits_positions(matrix, size):
    positions = []
    col = size - 1
    going_up = True
    done = {}
    while col > 0:
        if col == 6:
            col -= 1
        for row in (range(size - 1, -1, -1) if going_up else range(size)):
            for c in [col, col - 1]:
                key = (row, c)
                if key not in done and matrix[row][c] == 0:
                    positions.append(key)
                    done[key] = True
        going_up = not going_up
        col -= 2
    return positions


def _bits_to_bytes(bits, data_bits):
    result = []
    for i in range(0, data_bits, 8):
        val = 0
        for j in range(8):
            if i + j < len(bits) and bits[i + j]:
                val |= 1 << (7 - j)
        result.append(val)
    return result


def _reed_solomon_encode(data, ec_words):
    GF = [0] * 256
    LOG = [0] * 256
    x = 1
    for i in range(255):
        GF[i] = x
        LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x11D
    GF[255] = GF[0]
    LOG[GF[255]] = 255

    def gf_mul(a, b):
        if a == 0 or b == 0:
            return 0
        return GF[(LOG[a] + LOG[b]) % 255]

    generator = [1]
    for i in range(ec_words):
        term = [0] * (len(generator) + 1)
        for j in range(len(generator)):
            term[j] ^= gf_mul(generator[j], GF[i])
            term[j + 1] ^= generator[j]
        generator = term

    msg = list(data) + [0] * ec_words
    for i in range(len(data)):
        factor = msg[i]
        if factor == 0:
            continue
        for j in range(len(generator)):
            msg[i + j] ^= gf_mul(generator[j], factor)
    return msg[len(data):]


def _qr_best_mask(modules, size):
    best_mask = 0
    best_penalty = float("inf")
    for mask in range(8):
        m = [row[:] for row in modules]
        m = _qr_apply_mask(m, size, mask)
        penalty = _qr_penalty(m, size)
        if penalty < best_penalty:
            best_penalty = penalty
            best_mask = mask
    return best_mask


def _qr_apply_mask(modules, size, mask):
    result = [row[:] for row in modules]
    for r in range(size):
        for c in range(size):
            if result[r][c] in (-1, 2):
                continue
            if mask == 0:
                if (r + c) % 2 == 0:
                    result[r][c] ^= 1
            elif mask == 1:
                if r % 2 == 0:
                    result[r][c] ^= 1
            elif mask == 2:
                if c % 3 == 0:
                    result[r][c] ^= 1
            elif mask == 3:
                if (r + c) % 3 == 0:
                    result[r][c] ^= 1
            elif mask == 4:
                if ((r // 2) + (c // 3)) % 2 == 0:
                    result[r][c] ^= 1
            elif mask == 5:
                if (r * c) % 2 + (r * c) % 3 == 0:
                    result[r][c] ^= 1
            elif mask == 6:
                if ((r * c) % 2 + (r * c) % 3) % 2 == 0:
                    result[r][c] ^= 1
            elif mask == 7:
                if ((r + c) % 2 + (r * c) % 3) % 2 == 0:
                    result[r][c] ^= 1
    return result


def _qr_penalty(modules, size):
    p = 0
    for r in range(size):
        run = 0
        prev = -1
        for c in range(size):
            v = modules[r][c]
            if v in (-1, 2):
                continue
            if v == prev:
                run += 1
            else:
                if run >= 5:
                    p += 3 + run - 5
                run = 1
                prev = v
        if run >= 5:
            p += 3 + run - 5

    for c in range(size):
        run = 0
        prev = -1
        for r in range(size):
            v = modules[r][c]
            if v in (-1, 2):
                continue
            if v == prev:
                run += 1
            else:
                if run >= 5:
                    p += 3 + run - 5
                run = 1
                prev = v
        if run >= 5:
            p += 3 + run - 5

    for r in range(size - 1):
        for c in range(size - 1):
            vals = [modules[r+i][c+j] for i in range(2) for j in range(2)]
            if all(v not in (-1, 2) for v in vals) and len(set(vals)) == 1:
                p += 3

    for r in range(size):
        for c in range(size - 10):
            pattern = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
            if all(modules[r][c+k] not in (-1, 2) and modules[r][c+k] == pattern[k] for k in range(11)):
                p += 40

    for c in range(size):
        for r in range(size - 10):
            pattern = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
            if all(modules[r+k][c] not in (-1, 2) and modules[r+k][c] == pattern[k] for k in range(11)):
                p += 40

    dark = sum(1 for r in range(size) for c in range(size) if modules[r][c] not in (-1, 2) and modules[r][c])
    total = sum(1 for r in range(size) for c in range(size) if modules[r][c] not in (-1, 2))
    if total > 0:
        ratio = dark * 100 / total
        p += abs(int(ratio - 50) // 5) * 10
    return p


def _qr_render_svg(modules, size, modules_per_pixel=8):
    total = size * modules_per_pixel
    quiet = modules_per_pixel * 4
    svg_total = total + quiet * 2

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_total} {svg_total}" '
        f'width="250" height="250">',
        f'<rect width="{svg_total}" height="{svg_total}" fill="white"/>',
    ]

    for r in range(size):
        for c in range(size):
            v = modules[r][c]
            if v in (-1, 2):
                v = 0
            if v:
                x = quiet + c * modules_per_pixel
                y = quiet + r * modules_per_pixel
                lines.append(
                    f'<rect x="{x}" y="{y}" width="{modules_per_pixel}" '
                    f'height="{modules_per_pixel}" fill="black"/>'
                )

    lines.append("</svg>")
    return "\n".join(lines)
