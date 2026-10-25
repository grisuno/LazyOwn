"""Reaction bridge between the reactive engine and the loop planner.

Two products:

- Saved reactive decisions: after each worker step fails or reveals a
  fresh opportunity, the reactive engine's top decisions are parked in a
  per-task JSON buffer. The next planning round drains them as
  ``reaction`` triggers so the loop reacts instead of observing. One-shot
  consumption, dedupe by command, bounded size.
- Credential reuse: worker outputs that plainly contain login pairs
  (``user:pass`` lines, hash strings) feed back into the autonomous
  exploit engine's credential retry so a captured cred is tried in the
  same session, not next shift. Placeholder values (CHANGE_ME, admin...)
  are rejected loudly, not silently guessed.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from modules.lazy_loop import _load_json, _save_json, _store_path


_MAX_DECISIONS_PER_TASK = 6
_MAX_CRED_PAIRS = 8
_MIN_TOKEN = 1
_EXPIRE_SECONDS = 3600

_PAIR_RE = re.compile(r"^(?P<user>[A-Za-z0-9._@\\/\-]{1,32})\s*:\s*(?P<pass>[^\s:]{4,64})$")
_SLOT_RE = re.compile(r"^\s*(?P<user>\S{1,32})\s*[:|]\s*(?P<pass>\S{4,64})\s*$")
_PLACEHOLDERS = frozenset(
    {
        "change_me",
        "changeme",
        "your_api_key_here",
        "your_password",
        "username",
        "user",
        "user account",
        "password",
        "motdepasse",
        "pass",
        "admin",
        "administrator",
        "root",
        "authorization",
        "authorization basic",
        "somewhere",
        "here",
        "password:",
        "pass:",
        "user:",
        "value",
        "email",
        "admin@somewhere",
        "123456",
        "password123",
        "xorغيرون",
    }
)


class ReactionPick:
    """One reactive-engine decision parked for the next planning round."""

    def __init__(self, command: str, reason: str = "", priority: int = 3, mitre: str = "") -> None:
        self.command = command
        self.reason = reason
        self.priority = priority
        self.mitre = mitre


def _buffer_path(task_id: str) -> Path:
    return _store_path(f"reactions_{task_id}.json")


def save_decisions(task_id: str, decisions: list[ReactionPick]) -> int:
    """Park picks into the per-task buffer; returns the saved count."""
    if not str(task_id).strip() or not decisions:
        return 0
    payload = _load_buffer(task_id)
    existing = {entry.get("command", "") for entry in payload.get("decisions", [])}
    now = int(time.time())
    for pick in decisions[:_MAX_DECISIONS_PER_TASK]:
        command = str(getattr(pick, "command", "") or pick).strip()
        if not command or command in existing:
            continue
        existing.add(command)
        payload.setdefault("decisions", []).append(
            {
                "command": command,
                "reason": str(getattr(pick, "reason", "") or ""),
                "priority": int(getattr(pick, "priority", 3) or 3),
                "mitre": str(getattr(pick, "mitre", "") or ""),
                "ts": now,
            }
        )
    payload["decisions"] = sorted(
        payload.get("decisions", []), key=lambda e: int(e.get("priority", 3))
    )[:_MAX_DECISIONS_PER_TASK]
    _write_buffer(task_id, payload)
    return len(payload.get("decisions", []))


def load_reaction_triggers(task_id: str, consumer: str = "") -> list[dict]:
    """Drain the buffer into planner trigger dicts (one-shot, one per round)."""
    payload = _load_buffer(task_id)
    now = int(time.time())
    fresh: list[dict] = []
    for entry in payload.get("decisions", []):
        if now - int(entry.get("ts", 0)) > _EXPIRE_SECONDS:
            continue
        command = str(entry.get("command", "")).strip()
        lowered = command.lower()
        if lowered.startswith("assign rhost"):
            tokens = command.split()
            value = tokens[-1] if len(tokens) > 2 else ""
            text = f"probe ip {value}" if value else ""
        else:
            text = f"reactive hint: {command}"
        if not text:
            continue
        if entry.get("reason"):
            text += f" — {entry['reason'][:120]}"
        fresh.append(
            {
                "kind": "reaction",
                "text": text[:280],
                "command": entry.get("command", ""),
                "priority": int(entry.get("priority", 3)),
                "mitre": entry.get("mitre", ""),
                "id": int(entry.get("ts", 0)),
            }
        )
    if consumer:
        _write_buffer(task_id, {"decisions": []})
    return fresh


def _load_buffer(task_id: str) -> dict:
    payload = _load_json(_buffer_path(task_id), {"decisions": []})
    if isinstance(payload, dict) and isinstance(payload.get("decisions", []), list):
        return payload
    return {"decisions": []}


def _write_buffer(task_id: str, payload: dict) -> None:
    _save_json(_buffer_path(task_id), payload)


def _placeholder_value(value: str) -> bool:
    lower = value.lower().strip()
    return lower in _PLACEHOLDERS or (len(lower) > 6 and any(piece in lower for piece in ("change_me", "changeme", "your_")))


def find_credentials(output: str) -> list[dict]:
    """Extract user:pass pairs and hashes; placeholder values are dropped."""
    pairs: list[dict] = []
    seen: set[tuple[str, str]] = set()
    hash_blob = re.compile(r"^[0-9a-fA-F]{32}$|^[0-9a-fA-F]{40}$|^[0-9a-fA-F]{64}$")
    for line in str(output or "").splitlines():
        line = line.strip()
        match = _PAIR_RE.match(line) or _SLOT_RE.match(line)
        if match:
            user, password = match.group("user").strip(), match.group("pass").strip()
            if user.lower() in ("password", "pass", "user") or password.lower() in ("user", "password"):
                continue
            if _placeholder_value(user) or _placeholder_value(password):
                continue
            key = (user, password)
            if key not in seen:
                seen.add(key)
                pairs.append({"username": user, "password": password})
        hash_match = hash_blob.match(line.strip())
        if hash_match and not _placeholder_value(line.strip()) and len(pairs) < _MAX_CRED_PAIRS + 4:
            existing = {p.get("hash", "") for p in pairs}
            if line.strip() not in existing:
                pairs.append({"hash": line.strip()})
        if len(pairs) >= _MAX_CRED_PAIRS:
            break
    return pairs[:_MAX_CRED_PAIRS]
