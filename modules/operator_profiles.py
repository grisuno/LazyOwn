"""Multi-operator profile management for LazyOwn team server.

Each operator gets an isolated profile directory with its own:
- config (payload subset: lhost, lport, listeners)
- generated TLS certificates (per-operator C2 identity)
- command history and audit log

Design
------
- Profiles stored under ``sessions/operators/<username>/``
- Master ``payload.json`` is the team-wide baseline
- Per-operator overrides in ``operator.json`` inside each profile
- Certificates auto-generated on profile creation (CA + operator cert)
- All actions attributed to the operator who performed them
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("operator_profiles")

_SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"
_OPERATORS_DIR = _SESSIONS_DIR / "operators"
_TEAM_CA_KEY = _SESSIONS_DIR / "team_ca.key"
_TEAM_CA_CERT = _SESSIONS_DIR / "team_ca.pem"


@dataclass
class OperatorProfile:
    """Per-operator configuration and state."""

    username: str
    display_name: str = ""
    role: str = "operator"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_active: str = ""
    lhost: str = ""
    lport: int = 0
    listener_port: int = 0
    c2_port: int = 0
    c2_malleable_route: str = ""
    user_agent: str = ""
    cert_file: str = ""
    key_file: str = ""
    audit_log: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "username": self.username,
            "display_name": self.display_name,
            "role": self.role,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "lhost": self.lhost,
            "lport": self.lport,
            "listener_port": self.listener_port,
            "c2_port": self.c2_port,
            "c2_malleable_route": self.c2_malleable_route,
            "user_agent": self.user_agent,
            "cert_file": self.cert_file,
            "key_file": self.key_file,
            "audit_log": self.audit_log,
            "attributes": self.attributes,
        }


class OperatorProfileManager:
    """CRUD for operator profiles with certificate generation.

    Usage::

        mgr = OperatorProfileManager()
        mgr.create_profile("grisun0", display_name="Gris Iscomeback")
        profile = mgr.load_profile("grisun0")
        mgr.set_attribute("grisun0", "elo", 1500)
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        _OPERATORS_DIR.mkdir(parents=True, exist_ok=True)
        self._ensure_team_ca()

    def _ensure_team_ca(self) -> None:
        """Generate a team CA certificate if none exists."""
        if _TEAM_CA_KEY.exists() and _TEAM_CA_CERT.exists():
            return

        log.info("Generating team CA certificate...")
        try:
            subprocess.run(
                [
                    "openssl", "req", "-new", "-x509", "-days", "3650",
                    "-nodes",
                    "-subj", "/C=XX/ST=LazyOwn/L=RedTeam/O=LazyOwn/CN=LazyOwn Team CA",
                    "-keyout", str(_TEAM_CA_KEY),
                    "-out", str(_TEAM_CA_CERT),
                ],
                capture_output=True,
                check=True,
            )
            os.chmod(str(_TEAM_CA_KEY), 0o600)
            os.chmod(str(_TEAM_CA_CERT), 0o644)
        except subprocess.CalledProcessError as exc:
            log.warning("Failed to generate team CA: %s", exc.stderr)

    def _profile_dir(self, username: str) -> Path:
        return _OPERATORS_DIR / username

    def _profile_path(self, username: str) -> Path:
        return self._profile_dir(username) / "operator.json"

    def _generate_operator_cert(self, username: str) -> tuple[str, str]:
        """Generate per-operator TLS cert signed by team CA.

        Returns:
            Tuple of (cert_path, key_path).
        """
        profile_dir = self._profile_dir(username)
        key_path = profile_dir / "operator.key"
        csr_path = profile_dir / "operator.csr"
        cert_path = profile_dir / "operator.pem"

        if not _TEAM_CA_KEY.exists():
            return str(cert_path), str(key_path)

        try:
            subprocess.run(
                [
                    "openssl", "req", "-new", "-nodes",
                    "-subj", f"/CN={username}/O=LazyOwn Operator",
                    "-keyout", str(key_path),
                    "-out", str(csr_path),
                ],
                capture_output=True,
                check=True,
            )

            subprocess.run(
                [
                    "openssl", "x509", "-req", "-days", "365",
                    "-in", str(csr_path),
                    "-CA", str(_TEAM_CA_CERT),
                    "-CAkey", str(_TEAM_CA_KEY),
                    "-set_serial", f"0x{int(datetime.now().timestamp())}",
                    "-out", str(cert_path),
                ],
                capture_output=True,
                check=True,
            )

            csr_path.unlink(missing_ok=True)
            os.chmod(str(key_path), 0o600)
            os.chmod(str(cert_path), 0o644)
        except subprocess.CalledProcessError as exc:
            log.warning("Failed to generate operator cert: %s", exc.stderr)

        return str(cert_path), str(key_path)

    def create_profile(
        self,
        username: str,
        display_name: str = "",
        role: str = "operator",
        lhost: str = "",
        lport: int = 0,
        listener_port: int = 0,
        c2_port: int = 0,
        c2_malleable_route: str = "",
        user_agent: str = "",
        attributes: dict[str, Any] | None = None,
    ) -> OperatorProfile:
        """Create a new operator profile.

        Args:
            username: Unique operator identifier.
            display_name: Human-readable name.
            role: RBAC role (``operator``, ``admin``, ``viewer``).
            lhost: Operator's C2 listener IP override.
            lport: Operator's reverse shell port override.
            listener_port: Operator's listener port override.
            c2_port: Operator's C2 dashboard port override.
            c2_malleable_route: Per-operator malleable route.
            user_agent: Per-operator user agent.
            attributes: Arbitrary key-value metadata.

        Returns:
            The created :class:`OperatorProfile`.

        Raises:
            ValueError: If the profile already exists.
        """
        with self._lock:
            profile_dir = self._profile_dir(username)
            if profile_dir.exists():
                raise ValueError(f"Operator profile '{username}' already exists")

            profile_dir.mkdir(parents=True, exist_ok=True)
            cert_file, key_file = self._generate_operator_cert(username)

            audit_log = str(profile_dir / "audit.jsonl")

            profile = OperatorProfile(
                username=username,
                display_name=display_name or username,
                role=role,
                lhost=lhost,
                lport=lport,
                listener_port=listener_port,
                c2_port=c2_port,
                c2_malleable_route=c2_malleable_route,
                user_agent=user_agent,
                cert_file=cert_file,
                key_file=key_file,
                audit_log=audit_log,
                attributes=attributes or {},
            )

            self._save_profile(profile)
            log.info("Created operator profile: %s", username)
            return profile

    def _save_profile(self, profile: OperatorProfile) -> None:
        path = self._profile_path(profile.username)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(profile.to_dict(), indent=2))

    def load_profile(self, username: str) -> OperatorProfile | None:
        """Load an operator profile.

        Returns:
            :class:`OperatorProfile` or None.
        """
        path = self._profile_path(username)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text())
            return OperatorProfile(**data)
        except (json.JSONDecodeError, TypeError) as exc:
            log.warning("Corrupt profile %s: %s", username, exc)
            return None

    def update_profile(
        self, username: str, **kwargs: Any
    ) -> OperatorProfile | None:
        """Update fields on an existing profile."""
        profile = self.load_profile(username)
        if profile is None:
            return None

        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        self._save_profile(profile)
        return profile

    def delete_profile(self, username: str) -> bool:
        """Delete an operator profile and its directory."""
        profile_dir = self._profile_dir(username)
        if not profile_dir.exists():
            return False
        import shutil
        shutil.rmtree(profile_dir)
        log.info("Deleted operator profile: %s", username)
        return True

    def list_profiles(self) -> list[OperatorProfile]:
        """Return all operator profiles."""
        profiles: list[OperatorProfile] = []
        if not _OPERATORS_DIR.exists():
            return profiles
        for entry in sorted(_OPERATORS_DIR.iterdir()):
            if entry.is_dir():
                profile = self.load_profile(entry.name)
                if profile:
                    profiles.append(profile)
        return profiles

    def touch_activity(self, username: str) -> None:
        """Update last_active timestamp."""
        self.update_profile(
            username,
            last_active=datetime.now(timezone.utc).isoformat(),
        )

    def set_attribute(self, username: str, key: str, value: Any) -> bool:
        """Set a custom attribute on an operator profile."""
        profile = self.load_profile(username)
        if profile is None:
            return False
        profile.attributes[key] = value
        self._save_profile(profile)
        return True

    def get_attribute(self, username: str, key: str, default: Any = None) -> Any:
        """Get a custom attribute from an operator profile."""
        profile = self.load_profile(username)
        if profile is None:
            return default
        return profile.attributes.get(key, default)

    def log_action(
        self, username: str, action: str, details: dict[str, Any] | None = None
    ) -> None:
        """Append an audited action to the operator's audit log.

        Args:
            username: Operator identifier.
            action: Action name (e.g. ``"issue_command"``, ``"modify_config"``).
            details: Optional structured context.
        """
        profile = self.load_profile(username)
        if profile is None:
            return

        audit_path = Path(profile.audit_log)
        audit_path.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "operator": username,
            "action": action,
            "details": details or {},
        }

        with open(audit_path, "a") as fh:
            fh.write(json.dumps(entry) + "\n")

    def effective_config(self, username: str) -> dict[str, Any]:
        """Merge team baseline (payload.json) with per-operator overrides.

        Operator-specific fields (lhost, lport, listener_port, c2_port,
        c2_malleable_route, user_agent) take precedence over the team
        baseline. All other fields come from the team config.

        Args:
            username: Operator identifier.

        Returns:
            Merged configuration dict.
        """
        from core.config import load_payload

        team_config = load_payload()

        profile = self.load_profile(username)
        if profile is None:
            return {**team_config, "_operator": None}

        overrides = {
            "lhost": profile.lhost or team_config.get("lhost"),
            "lport": profile.lport or team_config.get("lport"),
            "c2_port": profile.c2_port or team_config.get("c2_port"),
            "c2_malleable_route": profile.c2_malleable_route or team_config.get("c2_malleable_route"),
            "user_agent_lin": profile.user_agent or team_config.get("user_agent_lin"),
            "user_agent_win": profile.user_agent or team_config.get("user_agent_win"),
        }

        merged = {**team_config, **{k: v for k, v in overrides.items() if v}}
        merged["_operator"] = username
        return merged


_GLOBAL_PROFILE_MANAGER: OperatorProfileManager | None = None


def get_operator_profile_manager() -> OperatorProfileManager:
    """Return the singleton :class:`OperatorProfileManager`."""
    global _GLOBAL_PROFILE_MANAGER
    if _GLOBAL_PROFILE_MANAGER is None:
        _GLOBAL_PROFILE_MANAGER = OperatorProfileManager()
    return _GLOBAL_PROFILE_MANAGER
