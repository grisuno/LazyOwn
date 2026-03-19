#!/usr/bin/env python3
"""
LazyOwn Objective Store
=======================
Priority-queue for high-level attack objectives.

Claude Code (the frontier model operating the MCP) is the primary writer and
reader of this store.  Sub-systems (sessions_watcher, event_engine, auto_loop)
may inject objectives automatically when they detect new context.

File format  — sessions/objectives.jsonl
Each line    — one JSON object:
    {
        "id":         "<8-char hex>",
        "text":       "Enumerate SMB shares on 10.10.11.78 (port 445 confirmed open)",
        "priority":   "high",        # critical / high / medium / low
        "status":     "pending",     # pending / in_progress / done / blocked / skipped
        "source":     "claude",      # claude / watcher / event_engine / user
        "context":    { ... },       # arbitrary dict — facts, event ids, etc.
        "created_at": "<iso>",
        "updated_at": "<iso>",
        "notes":      ""
    }

Priority order for next_pending():  critical > high > medium > low
Within same priority: FIFO (oldest first).

Usage:
    python3 skills/lazyown_objective.py inject "Enumerate SMB" --priority high
    python3 skills/lazyown_objective.py next
    python3 skills/lazyown_objective.py list
    python3 skills/lazyown_objective.py complete <id>
    python3 skills/lazyown_objective.py block   <id> "reason"
    python3 skills/lazyown_objective.py report
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import secrets
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# ─── Config ──────────────────────────────────────────────────────────────────

BASE_DIR        = Path(__file__).parent.parent
SESSIONS_DIR    = BASE_DIR / "sessions"
OBJECTIVES_FILE = SESSIONS_DIR / "objectives.jsonl"
PLAN_FILE       = SESSIONS_DIR / "plan.txt"
SOUL_FILE       = SESSIONS_DIR / "soul.md"

PRIORITY_ORDER  = {"critical": 0, "high": 1, "medium": 2, "low": 3}
VALID_STATUSES  = {"pending", "in_progress", "done", "blocked", "skipped"}
VALID_PRIORITIES = set(PRIORITY_ORDER.keys())

# TTL in hours for pending objectives before they are auto-expired.
# None = never expire.
OBJECTIVE_TTL_HOURS: Dict[str, Optional[float]] = {
    "critical": None,
    "high":     None,
    "medium":   72.0,
    "low":      24.0,
}

DEFAULT_SOUL = """\
# LazyOwn Agent Soul

## Campaign Objective
Perform an authorized penetration test against the configured target (rhost).

## Priority Order
1. Recon — understand the attack surface fully before acting
2. Enum  — extract users, shares, services, software versions
3. Exploit / Intrusion — gain initial foothold
4. PrivEsc — elevate to root/SYSTEM
5. Lateral Movement — move to adjacent hosts if in scope
6. Credential Harvest — dump hashes, tickets, cleartext
7. Report — document all findings with evidence

## Hard Stops (always require human confirmation)
- Destructive payloads on production systems
- Data exfiltration beyond the agreed scope
- Pivoting to hosts outside the declared IP range

## Guardrails
- Never skip recon; new context always has priority over assumptions
- If blocked more than twice on the same objective, escalate to human operator
- Always record evidence (screenshots, tool output) before moving forward
- Prefer low-noise techniques unless stealth is not a requirement

## Current Focus
Target: (set by lazyown_set_config rhost)
Phase:  recon
Notes:  (updated automatically by sessions_watcher)
"""

# ─── Data model ──────────────────────────────────────────────────────────────


@dataclass
class Objective:
    id: str
    text: str
    priority: str
    status: str
    source: str
    context: Dict
    created_at: str
    updated_at: str
    notes: str = ""

    def sort_key(self) -> tuple:
        return (PRIORITY_ORDER.get(self.priority, 99), self.created_at)


# ─── ObjectiveStore ──────────────────────────────────────────────────────────


class ObjectiveStore:
    """
    Append-only JSONL store with full rewrite on status changes.

    The file stays small (pentest campaigns rarely exceed a few hundred
    objectives).  Thread safety is handled by atomic rename on write.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or OBJECTIVES_FILE
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def _now(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    def _load_all(self) -> List[Objective]:
        if not self._path.exists():
            return []
        objs: List[Objective] = []
        for line in self._path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                objs.append(Objective(**d))
            except Exception:
                continue
        return objs

    def _save_all(self, objs: List[Objective]) -> None:
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text("\n".join(json.dumps(asdict(o)) for o in objs) + "\n")
        tmp.replace(self._path)

    @staticmethod
    def _text_hash(text: str) -> str:
        """8-char hex fingerprint of objective text for deduplication."""
        return hashlib.sha256(text.strip().lower().encode()).hexdigest()[:8]

    def cleanup(self) -> int:
        """
        Expire pending objectives whose TTL has passed.
        Returns the number of objectives marked skipped.
        """
        objs = self._load_all()
        now = datetime.datetime.now(datetime.timezone.utc)
        expired = 0
        for o in objs:
            if o.status != "pending":
                continue
            ttl = OBJECTIVE_TTL_HOURS.get(o.priority)
            if ttl is None:
                continue
            try:
                created = datetime.datetime.fromisoformat(o.created_at)
                if created.tzinfo is None:
                    created = created.replace(tzinfo=datetime.timezone.utc)
                age_h = (now - created).total_seconds() / 3600
                if age_h > ttl:
                    o.status = "skipped"
                    o.updated_at = now.isoformat()
                    o.notes = f"auto-expired after {age_h:.1f}h (ttl={ttl}h)"
                    expired += 1
            except (ValueError, TypeError):
                pass
        if expired:
            self._save_all(objs)
        return expired

    def inject(
        self,
        text: str,
        priority: str = "medium",
        source: str = "claude",
        context: Optional[Dict] = None,
        notes: str = "",
    ) -> Objective:
        if priority not in VALID_PRIORITIES:
            priority = "medium"

        # Expire stale objectives before adding new ones
        self.cleanup()

        # Deduplication: reject if a pending objective with same text hash exists
        text_hash = self._text_hash(text)
        for o in self._load_all():
            if o.status == "pending" and self._text_hash(o.text) == text_hash:
                return o  # already queued — return existing without re-inserting

        now = self._now()
        obj = Objective(
            id=secrets.token_hex(4),
            text=text,
            priority=priority,
            status="pending",
            source=source,
            context=context or {},
            created_at=now,
            updated_at=now,
            notes=notes,
        )
        with open(self._path, "a") as f:
            f.write(json.dumps(asdict(obj)) + "\n")
        return obj

    def _update_status(self, obj_id: str, status: str, notes: str = "") -> bool:
        objs = self._load_all()
        found = False
        for o in objs:
            if o.id == obj_id:
                o.status = status
                o.updated_at = self._now()
                if notes:
                    o.notes = notes
                found = True
        if found:
            self._save_all(objs)
        return found

    def complete(self, obj_id: str, notes: str = "") -> bool:
        return self._update_status(obj_id, "done", notes)

    def block(self, obj_id: str, reason: str = "") -> bool:
        return self._update_status(obj_id, "blocked", reason)

    def skip(self, obj_id: str, reason: str = "") -> bool:
        return self._update_status(obj_id, "skipped", reason)

    def start(self, obj_id: str) -> bool:
        return self._update_status(obj_id, "in_progress")

    def next_pending(self) -> Optional[Objective]:
        pending = [o for o in self._load_all() if o.status == "pending"]
        if not pending:
            return None
        return sorted(pending, key=lambda o: o.sort_key())[0]

    def list_pending(self, limit: int = 10) -> List[Objective]:
        pending = [o for o in self._load_all() if o.status == "pending"]
        return sorted(pending, key=lambda o: o.sort_key())[:limit]

    def list_all(self, status: str = "all", limit: int = 20) -> List[Objective]:
        objs = self._load_all()
        if status != "all":
            objs = [o for o in objs if o.status == status]
        return sorted(objs, key=lambda o: o.sort_key())[:limit]

    def summary(self) -> str:
        objs = self._load_all()
        counts: Dict[str, int] = {}
        for o in objs:
            counts[o.status] = counts.get(o.status, 0) + 1
        total = len(objs)
        parts = [f"total={total}"] + [f"{k}={v}" for k, v in sorted(counts.items())]
        lines = ["Objective Store — " + "  ".join(parts), ""]
        pending = [o for o in objs if o.status == "pending"]
        pending = sorted(pending, key=lambda o: o.sort_key())[:5]
        if pending:
            lines.append("Next up:")
            for o in pending:
                lines.append(f"  [{o.priority:8s}] [{o.id}] {o.text[:80]}")
        return "\n".join(lines)


# ─── Soul helpers ─────────────────────────────────────────────────────────────


def read_soul() -> str:
    if not SOUL_FILE.exists():
        SOUL_FILE.write_text(DEFAULT_SOUL)
    return SOUL_FILE.read_text()


def write_soul(content: str) -> None:
    SOUL_FILE.write_text(content)


def current_plan() -> str:
    if not PLAN_FILE.exists():
        return "(no plan yet — run lazynmap to generate one)"
    return PLAN_FILE.read_text().strip()


def full_context_for_claude(target: Optional[str] = None) -> Dict:
    """
    Return a single dict with everything Claude Code needs to reason about
    the next objective:  soul + pending objectives + current plan + soul.
    """
    store = ObjectiveStore()
    soul = read_soul()
    plan = current_plan()
    pending = store.list_pending(limit=5)
    next_obj = pending[0] if pending else None

    return {
        "soul":     soul,
        "plan":     plan[:4000],
        "next_objective": asdict(next_obj) if next_obj else None,
        "pending_count":  len(store.list_pending(limit=100)),
        "pending_preview": [
            {"id": o.id, "priority": o.priority, "text": o.text[:120]}
            for o in pending
        ],
    }


# ─── SoulUpdater ──────────────────────────────────────────────────────────────


class SoulUpdater:
    """
    Smart section-level patcher for sessions/soul.md.

    Instead of rewriting the whole file, it patches only the relevant
    ## section when new intelligence arrives (new credential, OS detected,
    access level achieved, vulnerability found).

    Each ## section is delimited by the next ## header or end-of-file.
    If a section doesn't exist yet it is appended.

    Usage (called by sessions_watcher after parsing):
        su = SoulUpdater()
        su.update_credentials([{"username": "admin", "password": "P@ss"}])
        su.update_phase("exploit")
        su.update_os("Windows Server 2019", "10.10.11.78")
        su.update_access("admin", "10.10.11.78", method="evil-winrm")
        su.update_vulnerabilities([{"vuln_id": "CVE-2021-34527", "severity": "critical", ...}])
    """

    def __init__(self) -> None:
        self._path = SOUL_FILE

    # ── internals ─────────────────────────────────────────────────────────────

    def _read(self) -> str:
        if not self._path.exists():
            write_soul(DEFAULT_SOUL)
        return self._path.read_text(errors="replace")

    def _patch_section(self, header: str, new_body: str) -> None:
        """Replace the body of ## header section; append if missing."""
        text = self._read()
        pattern = re.compile(
            rf"(## {re.escape(header)}\n)(.*?)(?=\n## |\Z)",
            re.DOTALL,
        )
        replacement = f"## {header}\n{new_body.rstrip()}\n"
        if pattern.search(text):
            new_text = pattern.sub(replacement, text)
        else:
            new_text = text.rstrip() + f"\n\n## {header}\n{new_body.rstrip()}\n"
        self._path.write_text(new_text)

    def _patch_line(self, key: str, value: str) -> None:
        """Replace `key: <old>` with `key: value` anywhere in the file."""
        text = self._read()
        pattern = re.compile(rf"^({re.escape(key)}:\s*).*$", re.MULTILINE)
        if pattern.search(text):
            new_text = pattern.sub(rf"\g<1>{value}", text)
        else:
            new_text = text.rstrip() + f"\n{key}: {value}\n"
        self._path.write_text(new_text)

    # ── public API ────────────────────────────────────────────────────────────

    def update_phase(self, phase: str) -> None:
        """Update the `Phase:` line inside ## Current Focus."""
        self._patch_line("Phase", phase)

    def update_target(self, target: str) -> None:
        """Update the `Target:` line inside ## Current Focus."""
        self._patch_line("Target", target)

    def update_os(self, os_name: str, target: str) -> None:
        """Record detected operating system for a target."""
        self._patch_section(
            "Detected OS",
            f"- {target}: {os_name}",
        )

    def update_credentials(self, creds: List[dict]) -> None:
        """
        Replace the ## Known Credentials section with discovered credentials.
        Accepts list of dicts with keys: username, password, hash_value (optional).
        """
        if not creds:
            return
        seen: set = set()
        lines: List[str] = []
        for c in creds[:15]:
            user   = (c.get("username") or "").strip()
            passwd = (c.get("password") or "").strip()
            hv     = (c.get("hash_value") or "").strip()
            if not user:
                continue
            if user in seen:
                continue
            seen.add(user)
            if passwd:
                lines.append(f"- {user}:{passwd}")
            elif hv:
                lines.append(f"- {user}:{hv[:16]}… (NTLM)")
            else:
                lines.append(f"- {user} (username only)")
        if lines:
            self._patch_section("Known Credentials", "\n".join(lines))

    def update_access(self, level: str, target: str, method: str = "") -> None:
        """Update achieved access level for a target."""
        note = f"- {target}: {level}"
        if method:
            note += f" via {method}"
        self._patch_section("Achieved Access", note)

    def update_vulnerabilities(self, vulns: List[dict]) -> None:
        """Replace ## Key Vulnerabilities with the most severe findings."""
        if not vulns:
            return
        sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        sorted_v = sorted(vulns, key=lambda v: sev_order.get(v.get("severity", "info"), 5))
        lines: List[str] = []
        for v in sorted_v[:15]:
            sev = (v.get("severity") or "info").upper()
            vid = v.get("vuln_id") or "?"
            title = (v.get("title") or "")[:80]
            lines.append(f"- [{sev}] {vid}: {title}")
        if lines:
            self._patch_section("Key Vulnerabilities", "\n".join(lines))


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LazyOwn Objective Store",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_inj = sub.add_parser("inject", help="Add a new objective")
    p_inj.add_argument("text", help="Objective text")
    p_inj.add_argument("--priority", default="medium",
                       choices=list(VALID_PRIORITIES))
    p_inj.add_argument("--source", default="user")
    p_inj.add_argument("--notes", default="")

    sub.add_parser("next", help="Print next pending objective")

    p_list = sub.add_parser("list", help="List pending objectives")
    p_list.add_argument("--status", default="pending")
    p_list.add_argument("--limit", type=int, default=20)

    p_done = sub.add_parser("complete", help="Mark objective done")
    p_done.add_argument("id")
    p_done.add_argument("--notes", default="")

    p_blk = sub.add_parser("block", help="Mark objective blocked")
    p_blk.add_argument("id")
    p_blk.add_argument("reason", nargs="?", default="")

    sub.add_parser("report", help="Print objective summary")
    sub.add_parser("soul", help="Print current soul")
    sub.add_parser("plan", help="Print current attack plan")
    sub.add_parser("context", help="Print full context for Claude Code")

    args = parser.parse_args()
    store = ObjectiveStore()

    if args.cmd == "inject":
        obj = store.inject(args.text, args.priority, args.source, notes=args.notes)
        print(f"Injected [{obj.id}] priority={obj.priority}: {obj.text}")
    elif args.cmd == "next":
        obj = store.next_pending()
        if obj:
            print(json.dumps(asdict(obj), indent=2))
        else:
            print("No pending objectives.")
    elif args.cmd == "list":
        for o in store.list_all(status=args.status, limit=args.limit):
            print(f"[{o.status:11s}] [{o.priority:8s}] [{o.id}] {o.text[:80]}")
    elif args.cmd == "complete":
        ok = store.complete(args.id, args.notes)
        print("done" if ok else f"id {args.id} not found")
    elif args.cmd == "block":
        ok = store.block(args.id, args.reason)
        print("blocked" if ok else f"id {args.id} not found")
    elif args.cmd == "report":
        print(store.summary())
    elif args.cmd == "soul":
        print(read_soul())
    elif args.cmd == "plan":
        print(current_plan())
    elif args.cmd == "context":
        print(json.dumps(full_context_for_claude(), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
