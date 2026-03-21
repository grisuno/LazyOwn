"""
threat_model.py — Blue team threat model builder for LazyOwn.

Reads LazyOwn_session_report.csv + sessions/ artefacts, maps commands to
MITRE ATT&CK tactics/techniques, and produces a structured JSON threat model
consumable by a blue team application.

Outputs: sessions/reports/threat_model.json

Schema (threat_model.json)
--------------------------
{
  "generated_at": "ISO-8601",
  "assets": [
    {
      "ip": str, "domain": str, "ports": [int, ...],
      "risk_score": 0-100,
      "compromise_indicators": [str, ...]
    }
  ],
  "ttps": [
    {
      "technique_id": str,        # T1234.001
      "tactic": str,              # Initial Access
      "technique_name": str,
      "commands": [str, ...],     # LazyOwn commands that map here
      "occurrences": int,
      "first_seen": ISO-8601,
      "last_seen":  ISO-8601,
      "severity": "low|medium|high|critical",
      "description": str
    }
  ],
  "ioc_registry": [
    {
      "type": "ip|domain|hash|credential|url|path",
      "value": str,
      "context": str,
      "first_seen": ISO-8601
    }
  ],
  "detection_rules": [
    {
      "rule_id": str,             # LO-001
      "name": str,
      "tactic": str,
      "technique_id": str,
      "condition": str,           # Sigma-lite condition expression
      "log_source": str,          # e.g. "process_creation"
      "fields": {str: str},       # field: pattern
      "severity": str,
      "response": str             # recommended blue team action
    }
  ],
  "summary": {
    "total_events": int,
    "unique_targets": int,
    "unique_commands": int,
    "highest_risk_asset": str,
    "dominant_tactic": str
  }
}

Public API
----------
get_builder()                   singleton
ThreatModelBuilder.build()      build + save + return dict
ThreatModelBuilder.load()       load last saved model
"""

from __future__ import annotations

import csv
import json
import os
import re
import logging
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SESSIONS_DIR    = Path(__file__).parent.parent / "sessions"
REPORT_CSV      = SESSIONS_DIR / "LazyOwn_session_report.csv"
REPORTS_DIR     = SESSIONS_DIR / "reports"
OUTPUT_FILE     = REPORTS_DIR / "threat_model.json"

# ---------------------------------------------------------------------------
# MITRE ATT&CK command → (technique_id, tactic, technique_name) mapping
# This covers the most common LazyOwn + pentest commands.
# ---------------------------------------------------------------------------
COMMAND_TTP_MAP: Dict[str, Tuple[str, str, str]] = {
    # Recon
    "lazynmap":          ("T1046",     "Discovery",          "Network Service Discovery"),
    "nmap":              ("T1046",     "Discovery",          "Network Service Discovery"),
    "hosts_discover":    ("T1018",     "Discovery",          "Remote System Discovery"),
    "enum4linux":        ("T1087.002", "Discovery",          "Account Discovery: Domain Account"),
    "smbmap":            ("T1083",     "Discovery",          "File and Directory Discovery"),
    "smbclient":         ("T1021.002", "Lateral Movement",   "SMB/Windows Admin Shares"),
    "ldapsearch":        ("T1069.002", "Discovery",          "Permission Groups Discovery: Domain Groups"),
    "gobuster":          ("T1083",     "Discovery",          "File and Directory Discovery"),
    "ffuf":              ("T1083",     "Discovery",          "File and Directory Discovery"),
    "nikto":             ("T1595.002", "Reconnaissance",     "Active Scanning: Vulnerability Scanning"),
    "wfuzz":             ("T1595.002", "Reconnaissance",     "Active Scanning: Vulnerability Scanning"),
    "dnsrecon":          ("T1590.002", "Reconnaissance",     "Gather Victim Network Information: DNS"),
    "dig":               ("T1590.002", "Reconnaissance",     "Gather Victim Network Information: DNS"),
    # Credential access
    "hydra":             ("T1110.001", "Credential Access",  "Brute Force: Password Guessing"),
    "kerbrute":          ("T1110.003", "Credential Access",  "Brute Force: Password Spraying"),
    "kerberoasting":     ("T1558.003", "Credential Access",  "Steal or Forge Kerberos Tickets: Kerberoasting"),
    "asreproasting":     ("T1558.004", "Credential Access",  "Steal or Forge Kerberos Tickets: AS-REP Roasting"),
    "crackmapexec":      ("T1110",     "Credential Access",  "Brute Force"),
    "bloodhound":        ("T1069.002", "Discovery",          "Permission Groups Discovery: Domain Groups"),
    # Exploitation
    "msf":               ("T1203",     "Execution",          "Exploitation for Client Execution"),
    "msfconsole":        ("T1203",     "Execution",          "Exploitation for Client Execution"),
    "sqlmap":            ("T1190",     "Initial Access",     "Exploit Public-Facing Application"),
    "commix":            ("T1059.004", "Execution",          "Command and Scripting Interpreter: Unix Shell"),
    # Post-exploitation
    "venom":             ("T1587.001", "Resource Development","Develop Capabilities: Malware"),
    "payload":           ("T1587.001", "Resource Development","Develop Capabilities: Malware"),
    "nc":                ("T1059",     "Execution",          "Command and Scripting Interpreter"),
    "netcat":            ("T1059",     "Execution",          "Command and Scripting Interpreter"),
    "ligolo":            ("T1572",     "Command and Control","Protocol Tunneling"),
    "chisel":            ("T1572",     "Command and Control","Protocol Tunneling"),
    "socat":             ("T1090",     "Command and Control","Proxy"),
    "lazypwn":           ("T1068",     "Privilege Escalation","Exploitation for Privilege Escalation"),
    "sudo_exploit":      ("T1548.003", "Privilege Escalation","Abuse Elevation Control Mechanism: Sudo"),
    "suid":              ("T1548.001", "Privilege Escalation","Abuse Elevation Control Mechanism: Setuid"),
    "pspy":              ("T1057",     "Discovery",          "Process Discovery"),
    "linpeas":           ("T1082",     "Discovery",          "System Information Discovery"),
    "winpeas":           ("T1082",     "Discovery",          "System Information Discovery"),
    # Persistence
    "cron":              ("T1053.003", "Persistence",        "Scheduled Task/Job: Cron"),
    "persist":           ("T1546",     "Persistence",        "Event Triggered Execution"),
    # Exfil
    "exfil":             ("T1048",     "Exfiltration",       "Exfiltration Over Alternative Protocol"),
    "download":          ("T1041",     "Exfiltration",       "Exfiltration Over C2 Channel"),
    # C2
    "beacon":            ("T1095",     "Command and Control","Non-Application Layer Protocol"),
    "lazync2":           ("T1095",     "Command and Control","Non-Application Layer Protocol"),
    # Reporting / misc
    "report":            ("T1119",     "Collection",         "Automated Collection"),
    "screenshot":        ("T1113",     "Collection",         "Screen Capture"),
    "whoami":            ("T1033",     "Discovery",          "System Owner/User Discovery"),
    "hostname":          ("T1082",     "Discovery",          "System Information Discovery"),
    "echo":              ("T1059",     "Execution",          "Command and Scripting Interpreter"),
    "set":               ("T1059",     "Execution",          "Command and Scripting Interpreter"),
}

SEVERITY_TACTIC: Dict[str, str] = {
    "Exfiltration":          "critical",
    "Credential Access":     "critical",
    "Privilege Escalation":  "high",
    "Lateral Movement":      "high",
    "Command and Control":   "high",
    "Persistence":           "high",
    "Execution":             "medium",
    "Initial Access":        "medium",
    "Discovery":             "low",
    "Reconnaissance":        "low",
    "Collection":            "medium",
    "Resource Development":  "low",
}

# Sigma-lite detection rule templates per technique
DETECTION_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "T1046": {
        "name": "Network Port Scan Detected",
        "log_source": "network_traffic",
        "fields": {"dest_ports_count": ">100", "time_window": "60s"},
        "response": "Block scanning source IP at perimeter firewall.",
    },
    "T1110": {
        "name": "Brute Force Authentication Attempt",
        "log_source": "authentication",
        "fields": {"event_id": "4625|4771", "failure_count": ">5"},
        "response": "Lock account and alert SOC. Enable MFA if not present.",
    },
    "T1558.003": {
        "name": "Kerberoasting — SPN Ticket Request",
        "log_source": "windows_security",
        "fields": {"event_id": "4769", "ticket_encryption": "0x17"},
        "response": "Rotate service account passwords. Enforce AES-only tickets.",
    },
    "T1558.004": {
        "name": "AS-REP Roasting — Pre-Auth Disabled",
        "log_source": "windows_security",
        "fields": {"event_id": "4768", "pre_auth": "false"},
        "response": "Enable Kerberos pre-authentication on all accounts.",
    },
    "T1572": {
        "name": "Tunneling Protocol Detected",
        "log_source": "network_traffic",
        "fields": {"protocol": "tcp|udp", "dest_port": "443|8080|1080"},
        "response": "Inspect TLS traffic. Correlate with endpoint process creation.",
    },
    "T1048": {
        "name": "Data Exfiltration Over Non-Standard Channel",
        "log_source": "network_traffic",
        "fields": {"bytes_out": ">10MB", "dest_country": "!internal"},
        "response": "Block destination. Initiate DLP investigation.",
    },
    "T1068": {
        "name": "Privilege Escalation Exploit Attempt",
        "log_source": "process_creation",
        "fields": {"parent_process": "bash|sh|python", "integrity": "high|system"},
        "response": "Isolate endpoint. Patch affected kernel/service immediately.",
    },
    "T1053.003": {
        "name": "Suspicious Cron Job Created",
        "log_source": "file_creation",
        "fields": {"path": "/etc/cron*|/var/spool/cron*", "event": "create|modify"},
        "response": "Review cron entries. Remove unauthorized jobs. Audit /etc/crontab.",
    },
    "T1190": {
        "name": "Public-Facing Application Exploited",
        "log_source": "web_application",
        "fields": {"status_code": "500|200", "uri_pattern": ".*(['\";]|UNION|SELECT).*"},
        "response": "Apply WAF rule. Patch or isolate vulnerable service.",
    },
    "T1095": {
        "name": "C2 Beacon — Non-HTTP Protocol",
        "log_source": "network_traffic",
        "fields": {"protocol": "tcp|udp", "beacon_interval": "regular"},
        "response": "Block C2 IP. Memory-forensic the implanted host.",
    },
}


# ---------------------------------------------------------------------------
# IOC extraction helpers
# ---------------------------------------------------------------------------
_RE_IP     = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
_RE_DOMAIN = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+(?:htb|com|net|org|local|lan|internal)\b', re.IGNORECASE)
_RE_CRED   = re.compile(r'(?i)(password|passwd|pass|hash|ntlm|secret)[=:\s]+(\S+)', re.IGNORECASE)
_RE_PATH   = re.compile(r'(?:/[a-zA-Z0-9_./-]{4,}|[A-Z]:\\[a-zA-Z0-9_.\\-]{4,})')
_RE_HASH   = re.compile(r'\b[a-fA-F0-9]{32,64}\b')


def _extract_iocs(text: str, first_seen: str) -> List[Dict[str, str]]:
    iocs: List[Dict[str, str]] = []
    for m in _RE_IP.finditer(text):
        ip = m.group()
        octets = ip.split(".")
        if octets[0] in ("127", "0", "255"):
            continue
        iocs.append({"type": "ip", "value": ip, "context": text[:80], "first_seen": first_seen})
    for m in _RE_DOMAIN.finditer(text):
        iocs.append({"type": "domain", "value": m.group(), "context": text[:80], "first_seen": first_seen})
    for m in _RE_CRED.finditer(text):
        iocs.append({"type": "credential", "value": m.group(2)[:50], "context": m.group(1), "first_seen": first_seen})
    for m in _RE_HASH.finditer(text):
        h = m.group()
        if len(h) in (32, 40, 64):
            iocs.append({"type": "hash", "value": h, "context": text[:80], "first_seen": first_seen})
    return iocs


# ---------------------------------------------------------------------------
# ThreatModelBuilder
# ---------------------------------------------------------------------------
class ThreatModelBuilder:
    """Builds and serialises the blue team threat model."""

    def build(self) -> Dict[str, Any]:
        rows = self._load_csv()
        assets       = self._build_assets(rows)
        ttps         = self._build_ttps(rows)
        ioc_registry = self._build_iocs(rows)
        det_rules    = self._build_detection_rules(ttps)
        purple_team  = self._build_purple_team(ttps, det_rules)
        summary      = self._build_summary(rows, assets, ttps)

        model: Dict[str, Any] = {
            "generated_at":    datetime.now(timezone.utc).isoformat(),
            "assets":          assets,
            "ttps":            ttps,
            "ioc_registry":    ioc_registry,
            "detection_rules": det_rules,
            "purple_team":     purple_team,
            "summary":         summary,
        }
        self._save(model)
        return model

    # ------------------------------------------------------------------

    def load(self) -> Optional[Dict[str, Any]]:
        if OUTPUT_FILE.exists():
            try:
                return json.loads(OUTPUT_FILE.read_text())
            except Exception:
                pass
        return None

    # ------------------------------------------------------------------
    # Internal builders
    # ------------------------------------------------------------------

    def _load_csv(self) -> List[Dict[str, str]]:
        if not REPORT_CSV.exists():
            return []
        rows: List[Dict[str, str]] = []
        try:
            with REPORT_CSV.open(newline="", errors="replace") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    rows.append(row)
        except Exception as exc:
            log.warning("threat_model: CSV read error: %s", exc)
        return rows

    def _build_assets(self, rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        asset_map: Dict[str, Dict[str, Any]] = {}
        for row in rows:
            ip = row.get("destination_ip", "").strip()
            if not ip:
                continue
            if ip not in asset_map:
                asset_map[ip] = {
                    "ip":                   ip,
                    "domain":               row.get("domain", ""),
                    "ports":                set(),
                    "risk_score":           0,
                    "compromise_indicators": [],
                    "_commands":            [],
                }
            dst_port = row.get("destination_port", "").strip()
            if dst_port.isdigit():
                asset_map[ip]["ports"].add(int(dst_port))
            cmd = row.get("command", "").strip().lower()
            asset_map[ip]["_commands"].append(cmd)

        assets = []
        for ip, data in asset_map.items():
            cmds      = data.pop("_commands")
            risk      = self._risk_score(cmds, data["ports"])
            indicators = self._compromise_indicators(cmds)
            data["ports"]                 = sorted(data["ports"])
            data["risk_score"]            = risk
            data["compromise_indicators"] = indicators
            assets.append(data)

        assets.sort(key=lambda a: a["risk_score"], reverse=True)
        return assets

    def _risk_score(self, commands: List[str], ports: set) -> int:
        score = 0
        high_risk_cmds = {
            "exfil", "beacon", "payload", "venom", "lazypwn",
            "kerberoasting", "asreproasting", "hydra", "crackmapexec",
        }
        med_risk_cmds = {
            "smbclient", "nc", "netcat", "ligolo", "chisel",
            "msf", "sqlmap", "commix",
        }
        for c in commands:
            if c in high_risk_cmds:
                score += 20
            elif c in med_risk_cmds:
                score += 10
            else:
                score += 1
        if 445 in ports or 3389 in ports:
            score += 10
        if 88 in ports:  # Kerberos
            score += 15
        return min(score, 100)

    def _compromise_indicators(self, commands: List[str]) -> List[str]:
        indicators: List[str] = []
        if any(c in commands for c in ("beacon", "lazync2")):
            indicators.append("C2 implant activity observed")
        if any(c in commands for c in ("kerberoasting", "asreproasting")):
            indicators.append("Kerberos ticket harvesting")
        if any(c in commands for c in ("exfil", "download")):
            indicators.append("Data exfiltration commands executed")
        if any(c in commands for c in ("hydra", "crackmapexec", "kerbrute")):
            indicators.append("Brute-force credential attack")
        if any(c in commands for c in ("lazypwn", "sudo_exploit", "suid")):
            indicators.append("Privilege escalation attempted")
        if any(c in commands for c in ("persist", "cron")):
            indicators.append("Persistence mechanism installed")
        return indicators

    def _build_ttps(self, rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        ttp_map: Dict[str, Dict[str, Any]] = {}
        for row in rows:
            cmd = row.get("command", "").strip().lower()
            if not cmd:
                continue
            # normalise: take first token
            base_cmd = cmd.split()[0]
            ttp_info = COMMAND_TTP_MAP.get(base_cmd)
            if ttp_info is None:
                continue
            tid, tactic, tname = ttp_info
            ts = row.get("start", "")
            if tid not in ttp_map:
                ttp_map[tid] = {
                    "technique_id":   tid,
                    "tactic":         tactic,
                    "technique_name": tname,
                    "commands":       set(),
                    "occurrences":    0,
                    "first_seen":     ts,
                    "last_seen":      ts,
                    "severity":       SEVERITY_TACTIC.get(tactic, "low"),
                    "description":    f"Technique {tname} observed via LazyOwn session.",
                }
            entry = ttp_map[tid]
            entry["commands"].add(base_cmd)
            entry["occurrences"] += 1
            if ts < entry["first_seen"]:
                entry["first_seen"] = ts
            if ts > entry["last_seen"]:
                entry["last_seen"] = ts

        ttps = []
        for entry in ttp_map.values():
            entry["commands"] = sorted(entry["commands"])
            ttps.append(entry)
        ttps.sort(key=lambda t: t["occurrences"], reverse=True)
        return ttps

    def _build_iocs(self, rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
        seen: set = set()
        iocs: List[Dict[str, str]] = []

        def _add(ioc: Dict[str, str]) -> None:
            key = (ioc["type"], ioc["value"])
            if key not in seen:
                seen.add(key)
                iocs.append(ioc)

        for row in rows:
            ts   = row.get("start", "")
            args = row.get("args", "")
            # IPs from destination
            ip = row.get("destination_ip", "").strip()
            if ip:
                _add({"type": "ip", "value": ip, "context": "target", "first_seen": ts})
            # Domain
            dom = row.get("domain", "").strip()
            if dom:
                _add({"type": "domain", "value": dom, "context": "engagement", "first_seen": ts})
            # URLs
            url = row.get("url", "").strip()
            if url and url.startswith("http"):
                _add({"type": "url", "value": url, "context": "target url", "first_seen": ts})
            # Inline IOCs from args
            for ioc in _extract_iocs(args, ts):
                _add(ioc)

        return iocs

    def _build_detection_rules(self, ttps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rules: List[Dict[str, Any]] = []
        rule_id = 1
        seen_tids: set = set()

        for ttp in ttps:
            tid = ttp["technique_id"]
            # Also check parent technique (strip sub-technique)
            parent_tid = tid.split(".")[0]
            tmpl = DETECTION_TEMPLATES.get(tid) or DETECTION_TEMPLATES.get(parent_tid)
            if tmpl is None or tid in seen_tids:
                continue
            seen_tids.add(tid)
            rules.append({
                "rule_id":      f"LO-{rule_id:03d}",
                "name":         tmpl["name"],
                "tactic":       ttp["tactic"],
                "technique_id": tid,
                "condition":    " AND ".join(f"{k}=={v}" for k, v in tmpl["fields"].items()),
                "log_source":   tmpl["log_source"],
                "fields":       tmpl["fields"],
                "severity":     ttp["severity"],
                "response":     tmpl["response"],
            })
            rule_id += 1

        return rules

    def _build_purple_team(
        self,
        ttps: List[Dict[str, Any]],
        detection_rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Purple team mapping: pair each observed TTP with its detection rule.

        Each entry exposes:
          red:   commands used, first/last seen, occurrences
          blue:  detection rule (log_source, condition, response) — or None if gap
          gap:   True when no detection rule covers this technique
        """
        # Build lookup: technique_id -> detection rule
        rules_by_tid: Dict[str, Dict[str, Any]] = {}
        for rule in detection_rules:
            rules_by_tid[rule["technique_id"]] = rule

        purple: List[Dict[str, Any]] = []
        for ttp in ttps:
            tid        = ttp["technique_id"]
            parent_tid = tid.split(".")[0]
            rule = rules_by_tid.get(tid) or rules_by_tid.get(parent_tid)
            gap  = rule is None

            entry: Dict[str, Any] = {
                "technique_id":   tid,
                "technique_name": ttp["technique_name"],
                "tactic":         ttp["tactic"],
                "severity":       ttp["severity"],
                "gap":            gap,
                "red": {
                    "commands":   ttp["commands"],
                    "occurrences": ttp["occurrences"],
                    "first_seen": ttp["first_seen"],
                    "last_seen":  ttp["last_seen"],
                },
                "blue": None if gap else {
                    "rule_id":    rule["rule_id"],
                    "name":       rule["name"],
                    "log_source": rule["log_source"],
                    "condition":  rule["condition"],
                    "response":   rule["response"],
                },
                "coverage": "none" if gap else "partial",
            }
            purple.append(entry)

        # Sort: gaps first (need attention), then by severity, then occurrences
        sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        purple.sort(
            key=lambda e: (0 if e["gap"] else 1, sev_order.get(e["severity"], 4))
        )
        return purple

    def _build_summary(
        self,
        rows: List[Dict[str, str]],
        assets: List[Dict[str, Any]],
        ttps: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        targets     = {r.get("destination_ip") for r in rows if r.get("destination_ip")}
        commands    = {r.get("command", "").split()[0] for r in rows if r.get("command")}
        top_asset   = assets[0]["ip"] if assets else "N/A"
        dom_tactic  = ttps[0]["tactic"] if ttps else "N/A"
        return {
            "total_events":       len(rows),
            "unique_targets":     len(targets),
            "unique_commands":    len(commands),
            "highest_risk_asset": top_asset,
            "dominant_tactic":    dom_tactic,
        }

    def _save(self, model: Dict[str, Any]) -> None:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        tmp = OUTPUT_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(model, indent=2, default=str))
        os.replace(tmp, OUTPUT_FILE)
        log.info("threat_model: saved to %s", OUTPUT_FILE)


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------
_builder_instance: Optional[ThreatModelBuilder] = None


def get_builder() -> ThreatModelBuilder:
    global _builder_instance
    if _builder_instance is None:
        _builder_instance = ThreatModelBuilder()
    return _builder_instance


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LazyOwn Threat Model Builder")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("build",  help="Build and save threat_model.json")
    sub.add_parser("show",   help="Pretty-print the last saved model")
    sub.add_parser("ttps",   help="List TTPs only")
    sub.add_parser("iocs",   help="List IOCs only")
    sub.add_parser("rules",  help="List detection rules only")
    sub.add_parser("purple", help="Show full purple team mapping (red + blue)")
    sub.add_parser("gaps",   help="Show detection coverage gaps (TTPs with no rule)")

    args = parser.parse_args()
    b    = get_builder()

    if args.cmd == "build":
        model = b.build()
        print(f"Built: {len(model['ttps'])} TTPs, {len(model['ioc_registry'])} IOCs, "
              f"{len(model['detection_rules'])} rules, {len(model['assets'])} assets")
        print(f"Saved: {OUTPUT_FILE}")
    elif args.cmd == "show":
        m = b.load()
        if m:
            print(json.dumps(m, indent=2))
        else:
            print("No model found — run: python3 modules/threat_model.py build")
    elif args.cmd == "ttps":
        m = b.build()
        for t in m["ttps"]:
            print(f"{t['technique_id']:12s} {t['tactic']:30s} {t['technique_name']}  (x{t['occurrences']})")
    elif args.cmd == "iocs":
        m = b.build()
        for i in m["ioc_registry"][:20]:
            print(f"{i['type']:12s} {i['value']}")
    elif args.cmd == "rules":
        m = b.build()
        for r in m["detection_rules"]:
            print(f"{r['rule_id']}  [{r['severity']:8s}]  {r['name']}")
    elif args.cmd == "purple":
        m = b.build()
        for p in m["purple_team"]:
            gap_marker = " [GAP]" if p["gap"] else ""
            print(f"{p['technique_id']:12s} [{p['severity']:8s}]  {p['technique_name']}{gap_marker}")
            print(f"  RED : {', '.join(p['red']['commands'])}  (x{p['red']['occurrences']})")
            if p["blue"]:
                print(f"  BLUE: {p['blue']['rule_id']} — {p['blue']['name']}")
                print(f"        {p['blue']['response']}")
            else:
                print("  BLUE: NO DETECTION RULE — coverage gap")
            print()
    elif args.cmd == "gaps":
        m = b.build()
        gaps = [p for p in m["purple_team"] if p["gap"]]
        print(f"Coverage gaps: {len(gaps)} / {len(m['purple_team'])} TTPs undetected")
        for p in gaps:
            print(f"  {p['technique_id']:12s} [{p['severity']:8s}]  {p['technique_name']}")
    else:
        parser.print_help()
