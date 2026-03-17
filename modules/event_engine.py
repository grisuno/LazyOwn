"""
LazyOwn Event Engine
====================
Tails sessions/LazyOwn_session_report.csv for new command executions,
matches them against rules in sessions/event_rules.json, and appends
structured events to sessions/events.jsonl for Claude (MCP) to consume.

Designed to run as a lightweight background loop (see skills/heartbeat.py).
"""

import csv
import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
SESSIONS   = BASE_DIR / "sessions"
CSV_FILE   = SESSIONS / "LazyOwn_session_report.csv"
EVENTS_FILE= SESSIONS / "events.jsonl"
RULES_FILE = SESSIONS / "event_rules.json"
LOGS_DIR   = SESSIONS / "logs"
WATERMARK  = SESSIONS / ".event_engine_watermark"   # last processed CSV byte offset


# ── Default rules ─────────────────────────────────────────────────────────────
DEFAULT_RULES = [
    {
        "id": "web_port_found",
        "description": "HTTP port open detected in nmap scan",
        "trigger": {"command": "lazynmap", "output_contains": "80/open"},
        "event_type": "WEB_PORT_FOUND",
        "severity": "info",
        "suggest": "Run lazywebscan or gobuster to enumerate web surface."
    },
    {
        "id": "smb_port_found",
        "description": "SMB port open",
        "trigger": {"command": "lazynmap", "output_contains": "445/open"},
        "event_type": "SMB_PORT_FOUND",
        "severity": "info",
        "suggest": "Run smbmap, enum4linux or crackmapexec."
    },
    {
        "id": "credentials_found",
        "description": "Credentials written to session",
        "trigger": {"command_contains": "echo", "args_contains": "credentials"},
        "event_type": "CREDENTIALS_CAPTURED",
        "severity": "high",
        "suggest": "Check sessions/credentials*.txt — try credential spraying."
    },
    {
        "id": "new_beacon",
        "description": "C2 beacon activity detected",
        "trigger": {"command": "c2"},
        "event_type": "C2_COMMAND_ISSUED",
        "severity": "info",
        "suggest": "Check lazyown_get_beacons() for connected implants."
    },
    {
        "id": "vuln_scan_done",
        "description": "Vulnerability scan completed",
        "trigger": {"command_contains": "vuln"},
        "event_type": "VULN_SCAN_COMPLETE",
        "severity": "info",
        "suggest": "Review scan output — check sessions/vulns_*.nmap for findings."
    },
    {
        "id": "privesc_attempt",
        "description": "Privilege escalation attempt detected",
        "trigger": {"command_contains": "priv"},
        "event_type": "PRIVESC_ATTEMPT",
        "severity": "high",
        "suggest": "Monitor for root shell — check beacon output."
    },
    {
        "id": "exfil_triggered",
        "description": "Data exfiltration command issued",
        "trigger": {"command_contains": "exfil"},
        "event_type": "EXFIL_TRIGGERED",
        "severity": "critical",
        "suggest": "Review sessions/ for exfiltrated data."
    },
    {
        "id": "ldap_enum",
        "description": "LDAP/AD enumeration started",
        "trigger": {"command_contains": "ldap"},
        "event_type": "AD_ENUM_STARTED",
        "severity": "info",
        "suggest": "Check for domain users, groups, and ACLs in output."
    },
]


# ── Rule loading ──────────────────────────────────────────────────────────────

def load_rules() -> list[dict]:
    """Load rules from event_rules.json, creating it with defaults if missing."""
    if not RULES_FILE.exists():
        save_rules(DEFAULT_RULES)
        return DEFAULT_RULES
    try:
        return json.loads(RULES_FILE.read_text())
    except Exception:
        return DEFAULT_RULES


def save_rules(rules: list[dict]):
    RULES_FILE.write_text(json.dumps(rules, indent=2))


def add_rule(rule: dict) -> str:
    """Add or replace a rule by id. Returns 'added' or 'updated'."""
    rules = load_rules()
    existing_ids = [r["id"] for r in rules]
    if rule["id"] in existing_ids:
        rules = [r if r["id"] != rule["id"] else rule for r in rules]
        save_rules(rules)
        return "updated"
    rules.append(rule)
    save_rules(rules)
    return "added"


# ── Watermark ────────────────────────────────────────────────────────────────

def _read_watermark() -> int:
    try:
        return int(WATERMARK.read_text().strip())
    except Exception:
        return 0


def _write_watermark(offset: int):
    WATERMARK.write_text(str(offset))


# ── Rule matching ─────────────────────────────────────────────────────────────

def _row_matches(row: dict, trigger: dict) -> bool:
    cmd  = row.get("command", "").lower()
    args = row.get("args", "").lower()

    if "command" in trigger and cmd != trigger["command"].lower():
        return False
    if "command_contains" in trigger and trigger["command_contains"].lower() not in cmd:
        return False
    if "args_contains" in trigger and trigger["args_contains"].lower() not in args:
        return False
    if "output_contains" in trigger:
        # Check the per-command output file for this domain
        domain = row.get("domain", row.get("destination_ip", "None"))
        log_file = LOGS_DIR / f"command_{row.get('command', '')}output{domain}.txt"
        if log_file.exists():
            try:
                content = log_file.read_text(errors="replace").lower()
                if trigger["output_contains"].lower() not in content:
                    return False
            except Exception:
                return False
        else:
            return False  # output file doesn't exist yet — skip
    return True


# ── Event writing ─────────────────────────────────────────────────────────────

def _append_event(event: dict):
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


# ── Core: process new CSV rows ────────────────────────────────────────────────

def process_new_rows() -> int:
    """
    Read new rows from the session CSV since last watermark.
    Match against rules and emit events to events.jsonl.
    Returns the number of events emitted.
    """
    if not CSV_FILE.exists():
        return 0

    offset   = _read_watermark()
    rules    = load_rules()
    emitted  = 0

    with open(CSV_FILE, "r", newline="", errors="replace") as f:
        # If first run (offset=0) skip header but set watermark to after it
        if offset == 0:
            f.readline()  # skip header
            _write_watermark(f.tell())
            return 0

        f.seek(offset)
        reader = csv.DictReader(
            f,
            fieldnames=["start","end","source_ip","source_port",
                        "destination_ip","destination_port","domain",
                        "subdomain","url","pivot_port","command","args"]
        )

        for row in reader:
            for rule in rules:
                if _row_matches(row, rule.get("trigger", {})):
                    event = {
                        "id":        str(uuid.uuid4())[:8],
                        "timestamp": datetime.now().isoformat(),
                        "type":      rule.get("event_type", "UNKNOWN"),
                        "severity":  rule.get("severity", "info"),
                        "rule_id":   rule["id"],
                        "source": {
                            "command":  row.get("command"),
                            "args":     row.get("args"),
                            "target":   row.get("destination_ip"),
                            "domain":   row.get("domain"),
                            "ts":       row.get("start"),
                        },
                        "suggest":   rule.get("suggest", ""),
                        "status":    "pending",
                    }
                    _append_event(event)
                    emitted += 1

        _write_watermark(f.tell())

    return emitted


# ── Event reading (for MCP) ───────────────────────────────────────────────────

def read_events(limit: int = 20, status: str = "pending") -> list[dict]:
    """Return up to `limit` events matching `status` (pending/processed/all)."""
    if not EVENTS_FILE.exists():
        return []
    events = []
    lines = EVENTS_FILE.read_text().splitlines()
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
            if status == "all" or ev.get("status") == status:
                events.append(ev)
                if len(events) >= limit:
                    break
        except Exception:
            continue
    return list(reversed(events))


def ack_event(event_id: str) -> bool:
    """Mark an event as processed. Returns True if found."""
    if not EVENTS_FILE.exists():
        return False
    lines = EVENTS_FILE.read_text().splitlines()
    updated = []
    found = False
    for line in lines:
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
            if ev.get("id") == event_id:
                ev["status"] = "processed"
                ev["acked_at"] = datetime.now().isoformat()
                found = True
            updated.append(json.dumps(ev))
        except Exception:
            updated.append(line)
    if found:
        EVENTS_FILE.write_text("\n".join(updated) + "\n")
    return found


# ── CLI for quick testing ─────────────────────────────────────────────────────

if __name__ == "__main__":
    n = process_new_rows()
    print(f"[event_engine] {n} event(s) emitted.")
    pending = read_events(limit=5)
    if pending:
        print(f"[event_engine] Latest pending events:")
        for ev in pending:
            print(f"  [{ev['severity'].upper()}] {ev['type']} — {ev['suggest']}")
