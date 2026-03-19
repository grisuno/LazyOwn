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
import json
import os
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
