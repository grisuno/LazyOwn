#!/usr/bin/env python3
"""
LazyOwn Append-Only Session Transcripts (Claude Code style)

All writes are append-only JSONL. Lines are never modified.
Compact boundaries mark where old content was summarized.

Usage:
    transcript = get_transcript()          # global singleton
    transcript.append("tool_use", {...})
    transcript.append("tool_result", {...})
    fork = transcript.fork()               # new session, no inherited permissions
"""

import json
import os
import stat
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

_SENSITIVE_KEYS = {
    "password", "passwd", "secret", "token", "api_key", "apikey",
    "private_key", "private", "credential", "credentials", "session_token",
    "auth", "authorization", "cookie", "bearer", "hash", "ntlm", "nthash",
}


def _redact_sensitive(value):
    """Return ``value`` with known-sensitive keys redacted in-place by copy.

    Walks dicts/lists recursively. Strings/bytes for keys listed in
    ``_SENSITIVE_KEYS`` are replaced with ``"[REDACTED]"``. Non-string values
    on those keys are also redacted to avoid leaking structured secrets.
    """
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if isinstance(k, str) and k.lower() in _SENSITIVE_KEYS:
                out[k] = "[REDACTED]"
            else:
                out[k] = _redact_sensitive(v)
        return out
    if isinstance(value, list):
        return [_redact_sensitive(v) for v in value]
    return value


class SessionTranscript:
    """
    Append-only JSONL session transcript.

    Each line is a JSON object:
        {"ts": "...", "type": "...", "uuid": "...", "data": {...}}

    Types: user_prompt | tool_use | tool_result | compact_boundary |
           permission_decision | hook_event | system
    """

    def __init__(self, sessions_dir: Path, session_id: Optional[str] = None):
        self.session_id = session_id or uuid.uuid4().hex[:12]
        self.sessions_dir = sessions_dir
        self.path = sessions_dir / f"transcript_{self.session_id}.jsonl"
        self.meta_path = sessions_dir / f"transcript_{self.session_id}.meta.json"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        self._init_meta()

    def _init_meta(self):
        if not self.meta_path.exists():
            meta = {
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "version": "1.1",
                "forked_from": None,
            }
            self.meta_path.write_text(json.dumps(meta, indent=2))
            try:
                os.chmod(self.meta_path, stat.S_IRUSR | stat.S_IWUSR)
            except OSError:
                pass

    # ── append (the only write operation) ────────────────────────────────────

    def append(self, event_type: str, data: dict) -> str:
        """Append a single event. Returns the event UUID.

        Sensitive fields (passwords, tokens, hashes) are redacted before the
        event is written to disk. The transcript file is chmod 600 so it is
        only readable by the operator that produced it.
        """
        event_uuid = uuid.uuid4().hex[:16]
        event = {
            "ts": datetime.now().isoformat(),
            "type": event_type,
            "uuid": event_uuid,
            "data": _redact_sensitive(data) if isinstance(data, (dict, list)) else data,
        }
        try:
            existed = self.path.exists()
            with open(self.path, "a") as f:
                f.write(json.dumps(event) + "\n")
            if not existed:
                try:
                    os.chmod(self.path, stat.S_IRUSR | stat.S_IWUSR)
                except OSError:
                    pass
        except OSError:
            pass
        return event_uuid

    # ── read operations ───────────────────────────────────────────────────────

    def get_recent(self, n: int = 100) -> list[dict]:
        """Return the last n events."""
        if not self.path.exists():
            return []
        lines = []
        try:
            with open(self.path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            lines.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except OSError:
            pass
        return lines[-n:]

    def get_all(self) -> list[dict]:
        return self.get_recent(n=999_999)

    def count(self) -> int:
        if not self.path.exists():
            return 0
        try:
            return sum(1 for _ in open(self.path))
        except OSError:
            return 0

    # ── auto-compact (Layer 5 trigger) ────────────────────────────────────────

    def maybe_auto_compact(self, threshold: int = 200) -> Optional[str]:
        """
        If event count since the last compact_boundary exceeds threshold,
        generate a template summary of those events and write a new boundary.
        Returns the new boundary's UUID or None if no compaction was needed.
        Append-only: original events stay on disk.
        """
        events = self.get_recent(threshold + 200)
        if len(events) < threshold:
            return None

        # Find last compact_boundary index
        last_idx = -1
        for i in range(len(events) - 1, -1, -1):
            if events[i].get("type") == "compact_boundary":
                last_idx = i
                break

        events_since = len(events) - last_idx - 1
        if events_since < threshold:
            return None

        # Generate template summary using ContextCompactor
        try:
            from lazyown_context import ContextCompactor
            older = events[last_idx + 1:]
            summary = ContextCompactor.auto_compact_session(older)
            preserved = [e.get("uuid", "") for e in older]
            return self.add_compact_boundary(summary, preserved)
        except Exception:
            return None

    # ── compact boundary ──────────────────────────────────────────────────────

    def add_compact_boundary(self, summary: str,
                              preserved_uuids: Optional[list[str]] = None) -> str:
        """
        Mark a compaction point. The summary replaces older events logically
        but they remain on disk (append-only guarantee).
        """
        return self.append("compact_boundary", {
            "summary": summary,
            "preserved_uuids": preserved_uuids or [],
            "head_uuid": (preserved_uuids[0] if preserved_uuids else ""),
            "tail_uuid": (preserved_uuids[-1] if preserved_uuids else ""),
            "note": "Events before this boundary were summarized. Original lines remain.",
        })

    # ── fork ──────────────────────────────────────────────────────────────────

    def fork(self, new_id: Optional[str] = None) -> "SessionTranscript":
        """
        Create a new transcript forked from this one.
        Permissions are NOT inherited (security decision matching Claude Code).
        Recent history IS copied for context continuity.
        """
        new = SessionTranscript(self.sessions_dir, new_id)

        # Update meta to record parent
        meta = json.loads(new.meta_path.read_text())
        meta["forked_from"] = self.session_id
        new.meta_path.write_text(json.dumps(meta, indent=2))

        # Copy recent events (no permissions carried over)
        for event in self.get_recent(200):
            if event.get("type") == "permission_decision":
                continue  # intentionally drop all permission grants
            new.append(event["type"], event.get("data", {}))

        new.append("system", {
            "message": f"Forked from {self.session_id}",
            "permissions_reset": True,
        })
        return new

    # ── human summary ─────────────────────────────────────────────────────────

    def status_text(self) -> str:
        events = self.get_recent(500)
        tool_uses = [e for e in events if e["type"] == "tool_use"]
        results   = [e for e in events if e["type"] == "tool_result"]
        compacts  = [e for e in events if e["type"] == "compact_boundary"]
        denied    = [e for e in events if e["type"] == "permission_decision"
                     and e.get("data", {}).get("decision") == "deny"]
        return (
            f"Session: {self.session_id}\n"
            f"  Events:         {len(events)}\n"
            f"  Tool calls:     {len(tool_uses)}\n"
            f"  Tool results:   {len(results)}\n"
            f"  Compact marks:  {len(compacts)}\n"
            f"  Denials:        {len(denied)}\n"
            f"  File:           {self.path}\n"
        )


# ── Global singleton management ───────────────────────────────────────────────

_active_transcript: Optional[SessionTranscript] = None


def get_transcript(sessions_dir: Optional[Path] = None,
                   session_id: Optional[str] = None) -> SessionTranscript:
    """
    Return the active transcript singleton.
    On first call, sessions_dir must be provided to initialize it.
    """
    global _active_transcript
    if _active_transcript is None:
        if sessions_dir is None:
            raise RuntimeError("sessions_dir required for first get_transcript() call")
        _active_transcript = SessionTranscript(sessions_dir, session_id)
    return _active_transcript


def reset_transcript(sessions_dir: Path,
                     session_id: Optional[str] = None) -> SessionTranscript:
    """Force a new transcript (e.g., after fork or session reset)."""
    global _active_transcript
    _active_transcript = SessionTranscript(sessions_dir, session_id)
    return _active_transcript
