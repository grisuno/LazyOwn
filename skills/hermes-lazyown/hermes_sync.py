"""
Hermes-native synchronization layer.

Bridges LazyOwn session state with Hermes agent primitives:
  - todo list sync (Hermes todo tool <-> objectives.jsonl)
  - checkpoint serialization for resume across turns
  - delegation hints for parallel intel gathering

Follows the Observer pattern: LazyOwn state changes are observed and
reflected into Hermes-native constructs.
"""

import json
import time
from pathlib import Path
from typing import Any

from constants import Defaults, Paths


class HermesSyncError(Exception):
    """Raised when a sync operation cannot complete."""

    pass


class CheckpointSerializer:
    """
    Serialize the current engagement state into a compact checkpoint
    that Hermes can inject at the start of a new turn.
    """

    def __init__(self, sessions_dir: Path | None = None) -> None:
        self._sessions_dir = sessions_dir or Paths.sessions_dir()
        self._checkpoint_file = self._sessions_dir / "hermes_checkpoint.json"

    def write(self, state: dict[str, Any]) -> None:
        """Write a checkpoint to disk."""
        payload = {
            "version": Defaults.CHECKPOINT_VERSION,
            "timestamp": time.time(),
            "state": state,
        }
        try:
            self._checkpoint_file.write_text(
                json.dumps(payload, indent=2, default=str), encoding="utf-8"
            )
        except OSError as exc:
            raise HermesSyncError(f"Failed to write checkpoint: {exc}") from exc

    def read(self) -> dict[str, Any] | None:
        """Read the latest checkpoint, or None if absent / stale."""
        try:
            if not self._checkpoint_file.exists():
                return None
            data = json.loads(self._checkpoint_file.read_text(encoding="utf-8"))
            if data.get("version") != Defaults.CHECKPOINT_VERSION:
                return None
            ts = data.get("timestamp", 0)
            if time.time() - ts > Defaults.FRESHNESS_THRESHOLD_SECONDS:
                return None
            return data.get("state")
        except (json.JSONDecodeError, OSError):
            return None

    def clear(self) -> None:
        """Remove the checkpoint file."""
        try:
            if self._checkpoint_file.exists():
                self._checkpoint_file.unlink()
        except OSError:
            pass


class ObjectiveTodoSync:
    """
    Bidirectional sync between LazyOwn objectives and Hermes todo items.

    LazyOwn objectives are stored in objectives.jsonl (append-only JSON lines).
    Hermes todo items are ephemeral per-turn. This bridge allows the agent
    to surface LazyOwn objectives as Hermes todos and ack them back.
    """

    def __init__(self, objectives_path: Path | None = None) -> None:
        self._objectives_path = objectives_path or Paths.objectives_file()

    def pending_objectives(self) -> list[dict[str, Any]]:
        """Return all pending objectives from objectives.jsonl."""
        objectives: list[dict[str, Any]] = []
        if not self._objectives_path.exists():
            return objectives
        try:
            with self._objectives_path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if obj.get("status") in (None, "pending", "new"):
                        objectives.append(obj)
        except OSError:
            pass
        return objectives

    def mark_done(self, objective_text: str) -> bool:
        """
        Mark an objective as done by appending a completion record.

        LazyOwn objectives.jsonl is append-only; we do not mutate existing
        lines. Instead we append a new line with status=done referencing
        the original text.
        """
        record = {
            "text": objective_text,
            "status": "done",
            "timestamp": time.time(),
            "source": "hermes_sync",
        }
        try:
            with self._objectives_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, default=str) + "\n")
            return True
        except OSError as exc:
            raise HermesSyncError(f"Failed to ack objective: {exc}") from exc

    def inject_objective(self, text: str, priority: str = "high", notes: str = "") -> bool:
        """Inject a new objective into the LazyOwn queue."""
        record = {
            "text": text,
            "priority": priority,
            "notes": notes,
            "status": "pending",
            "timestamp": time.time(),
            "source": "hermes_sync",
        }
        try:
            with self._objectives_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, default=str) + "\n")
            return True
        except OSError as exc:
            raise HermesSyncError(f"Failed to inject objective: {exc}") from exc


class DelegationPlanner:
    """
    Produces structured delegation plans that Hermes can execute via
    delegate_task or cronjob.

    Given a discovery (e.g., new service found), returns a list of
    parallel subtasks suitable for Hermes-native delegation.
    """

    def plan_for_service(self, service: str, port: int, rhost: str) -> list[dict[str, Any]]:
        """
        Return a list of delegation task descriptors for a discovered service.

        Each descriptor has keys: goal, context, toolsets.
        """
        plans: list[dict[str, Any]] = []
        normalized = service.lower()

        if "smb" in normalized or "microsoft-ds" in normalized or port == 445:
            plans.append({
                "goal": f"Enumerate SMB shares and users on {rhost}:{port}",
                "context": f"Target {rhost} port {port} ({service}). Run enum4linux, crackmapexec smb, and list shares.",
                "toolsets": ["terminal", "file"],
            })
            plans.append({
                "goal": f"Search known exploits for SMB service on {rhost}:{port}",
                "context": f"Search exploitdb and CVE databases for SMB-related vulnerabilities.",
                "toolsets": ["web", "terminal"],
            })

        if "http" in normalized or "https" in normalized or port in (80, 443, 8080, 8443):
            plans.append({
                "goal": f"Perform web enumeration on {rhost}:{port}",
                "context": f"Target {rhost}:{port} ({service}). Run whatweb, gobuster, nikto.",
                "toolsets": ["terminal", "file"],
            })
            plans.append({
                "goal": f"Search known web exploits for {rhost}:{port}",
                "context": f"Identify framework/version and search for CVEs and exploits.",
                "toolsets": ["web", "terminal"],
            })

        if "ssh" in normalized or port == 22:
            plans.append({
                "goal": f"Enumerate SSH on {rhost}:{port}",
                "context": f"Check banner, version, and test key-based or credential auth.",
                "toolsets": ["terminal", "file"],
            })

        if "ldap" in normalized or port == 389:
            plans.append({
                "goal": f"Enumerate LDAP on {rhost}:{port}",
                "context": f"Run ldapdomaindump, search for naming contexts and users.",
                "toolsets": ["terminal", "file"],
            })

        if "kerberos" in normalized or port == 88:
            plans.append({
                "goal": f"Enumerate Kerberos on {rhost}:{port}",
                "context": f"Run GetNPUsers, kerbrute, and search for AS-REP roastable accounts.",
                "toolsets": ["terminal", "file"],
            })

        if not plans:
            plans.append({
                "goal": f"Enumerate {service} on {rhost}:{port}",
                "context": f"Generic enumeration for discovered service {service} on port {port}.",
                "toolsets": ["terminal", "file", "web"],
            })

        return plans

    def plan_for_credential(self, cred_type: str, value: str, rhost: str) -> list[dict[str, Any]]:
        """
        Return delegation tasks triggered by a newly found credential.
        """
        plans: list[dict[str, Any]] = []

        plans.append({
            "goal": f"Validate credential on {rhost}",
            "context": f"Test the found {cred_type} against common services (SSH, SMB, WinRM, LDAP) on {rhost}.",
            "toolsets": ["terminal", "file"],
        })

        plans.append({
            "goal": f"Assess lateral movement potential with new {cred_type}",
            "context": f"Check where else this credential works across the target scope.",
            "toolsets": ["terminal", "web"],
        })

        return plans
