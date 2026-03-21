#!/usr/bin/env python3
"""
LazyOwn Parquet Knowledge Base
================================
Centralises session history and contextual knowledge in the parquets/ directory.

Two responsibilities
────────────────────
1. SESSION KNOWLEDGE  →  parquets/session_knowledge.parquet
   • Ingests sessions/LazyOwn_session_report.csv (which has no id/success/category)
   • Enriches each row with:
       - id           : stable UUID derived from (start, command, args, destination_ip)
       - category     : extracted from cmd2 @with_category decorators in lazyown.py
                        (parsed once at startup with a regex — no import needed)
       - success      : bool  (True by default from bootstrap; updated via annotate())
       - outcome      : "success" | "failure" | "unknown"
       - reward       : int from policy RewardCalculator
       - confidence   : float
       - tier         : classifier tier
       - reason       : why the outcome was chosen
   • Merges new CSV rows incrementally (existing rows preserved, not overwritten)
   • Supports annotate(row_id, success, category) to patch rows AFTER execution

2. KNOWLEDGE QUERY ENGINE  →  any .parquet in parquets/
   • query_knowledge(keyword, parquet, columns, limit) — generic keyword search
     over any parquet in parquets/  (binarios, lolbas_*, techniques, session_knowledge)
   • context_for_phase(phase, target) — rich context dict for MCP:
       * recent successes/failures in this phase
       * relevant GTFOBins binaries
       * relevant MITRE techniques
       * next recommended commands

Usage
─────
    python3 skills/lazyown_parquet_db.py sync          # ingest CSV → parquet
    python3 skills/lazyown_parquet_db.py query recon
    python3 skills/lazyown_parquet_db.py query --keyword smb
    python3 skills/lazyown_parquet_db.py annotate <row_id> --success --category recon

MCP integration
───────────────
    from lazyown_parquet_db import ParquetDB
    _pdb = ParquetDB(LAZYOWN_DIR)
    # In list_tools: add lazyown_parquet_query + lazyown_parquet_annotate
    # In call_tool:  _pdb.context_for_phase(phase, target)
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False

log = logging.getLogger("parquet_db")

# ── Paths ──────────────────────────────────────────────────────────────────────

BASE_DIR      = Path(__file__).parent.parent
PARQUETS_DIR  = BASE_DIR / "parquets"
SESSIONS_DIR  = BASE_DIR / "sessions"
CSV_PATH      = SESSIONS_DIR / "LazyOwn_session_report.csv"
SESSION_PKT   = PARQUETS_DIR / "session_knowledge.parquet"

# ── Cmd2 category → short policy phase mapping ─────────────────────────────────

_CMD2_TO_PHASE: Dict[str, str] = {
    "01. Reconnaissance":       "recon",
    "02. Scanning & Enumeration": "scanning",
    "03. Exploitation":          "exploit",
    "04. Post-Exploitation":     "post_exploit",
    "05. Persistence":           "persistence",
    "06. Privilege Escalation":  "privesc",
    "07. Credential Access":     "credential",
    "08. Lateral Movement":      "lateral",
    "09. Data Exfiltration":     "exfil",
    "10. Command & Control":     "c2",
    "11. Reporting":             "reporting",
    "12. Miscellaneous":         "other",
    "13. Lua Plugin":            "other",
    "14. Yaml Addon.":           "other",
    "15. Adversary YAML.":       "other",
}

# Broad keyword → phase, for commands not decorated or from addons/plugins
_KEYWORD_PHASE: Dict[str, str] = {
    "nmap": "recon", "lazynmap": "recon", "dig": "recon", "whois": "recon",
    "host": "recon", "dnsrecon": "recon", "dnsenum": "recon",
    "enum4linux": "scanning", "smbmap": "scanning", "smbclient": "scanning",
    "ldapsearch": "scanning", "ldapdomaindump": "scanning",
    "crackmapexec": "scanning", "nxc": "scanning", "rpcclient": "scanning",
    "kerbrute": "scanning", "gobuster": "scanning", "ffuf": "scanning",
    "nikto": "scanning", "dirb": "scanning", "wfuzz": "scanning",
    "searchsploit": "exploit", "msfconsole": "exploit", "exploit": "exploit",
    "sqlmap": "exploit", "commix": "exploit",
    "linpeas": "privesc", "winpeas": "privesc", "privesc": "privesc",
    "sudo": "privesc",
    "secretsdump": "credential", "hashdump": "credential", "mimikatz": "credential",
    "bloodhound": "lateral", "evil-winrm": "lateral", "psexec": "lateral",
    "impacket": "lateral",
    "hydra": "credential", "john": "credential", "hashcat": "credential",
    "wget": "exfil", "curl": "exfil",
    "report": "reporting",
}


def _build_cmd2_category_map(lazyown_py: Path) -> Dict[str, str]:
    """
    Parse lazyown.py with regex to build command→phase map.
    Requires no import — safe to call from any context.
    """
    result: Dict[str, str] = {}
    try:
        src = lazyown_py.read_text(errors="replace")

        # Step 1: resolve variable names → string values
        cat_vars: Dict[str, str] = {}
        for m in re.finditer(r'^(\w+_category)\s*=\s*["\'](.+?)["\']', src, re.MULTILINE):
            cat_vars[m.group(1)] = m.group(2)

        # Step 2: @cmd2.with_category(<var_or_string>) def do_<cmd>
        for m in re.finditer(
            r'@cmd2\.with_category\((["\']?[\w. ]+["\']?)\)\s+def do_(\w+)',
            src,
        ):
            raw_cat = m.group(1).strip("'\" ")
            cmd     = m.group(2)
            # raw_cat might be a var name or a literal string
            cat_str = cat_vars.get(raw_cat, raw_cat)
            phase   = _CMD2_TO_PHASE.get(cat_str, "other")
            result[cmd] = phase

    except Exception as exc:
        log.debug(f"cmd2 map parse failed: {exc}")

    return result


def _stable_id(start: str, cmd: str, args: str, dest_ip: str) -> str:
    """Generate a stable 16-char hex ID from row fields."""
    raw = f"{start}|{cmd}|{args}|{dest_ip}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ── Policy bridge ──────────────────────────────────────────────────────────────

_SKILLS_DIR = Path(__file__).parent
if str(_SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILLS_DIR))

try:
    from lazyown_policy import (  # type: ignore
        HeuristicClassifier as _HeuristicClassifier,
        RewardCalculator as _RewardCalculator,
        Config as _PolicyConfig,
        infer_category as _infer_category,
        OutcomeType as _OutcomeType,
    )
    _POLICY_OK = True
except Exception:
    _POLICY_OK = False


def _classify_row(command: str, args: str, phase_hint: str) -> Dict[str, Any]:
    """Return {category, success, outcome, reward, confidence, tier, reason}."""
    if _POLICY_OK:
        try:
            heuristic = _HeuristicClassifier()
            result    = heuristic.classify(command, args, args, exit_code=None)
            from lazyown_policy import Config as _Cfg, SessionsDir as _SD  # type: ignore  # noqa: F401
            cfg    = _Cfg(sessions=SESSIONS_DIR)
            calc   = _RewardCalculator(cfg)
            cat    = result.category.value if hasattr(result.category, "value") else str(result.category)
            out    = result.outcome.value  if hasattr(result.outcome, "value")  else str(result.outcome)
            reward = calc.calculate(result.category, result.outcome)
            return {
                "category":   cat,
                "success":    result.success,
                "outcome":    out,
                "reward":     reward,
                "confidence": result.confidence,
                "tier":       result.tier,
                "reason":     result.reason,
            }
        except Exception:
            pass

    # Fallback: use phase_hint + keyword map
    cat = phase_hint or "other"
    return {
        "category":   cat,
        "success":    True,    # unknown → optimistic
        "outcome":    "unknown",
        "reward":     0,
        "confidence": 0.3,
        "tier":       "keyword",
        "reason":     "keyword heuristic (policy engine unavailable)",
    }


# ── ParquetDB ─────────────────────────────────────────────────────────────────


class ParquetDB:
    """
    Parquet-backed session knowledge base + generic parquet query engine.
    """

    SCHEMA_COLS = [
        "id", "start", "end", "source_ip", "source_port",
        "destination_ip", "destination_port", "domain", "subdomain",
        "url", "pivot_port", "command", "args",
        "category", "success", "outcome", "reward", "confidence",
        "tier", "reason",
        # Enriched columns (v2 — added for training dataset quality)
        "output_snippet",    # first 300 chars of real command output (set by annotate_rich)
        "finding_type",      # credential / vulnerability / path / hash / user / none
        "mitre_id",          # MITRE ATT&CK technique ID inferred from category
        "target_service",    # service name at target port (from FactStore)
        "target_port",       # port number used (from FactStore)
        "campaign_id",       # campaign identifier for multi-engagement separation
    ]

    # Mapping from category → most common MITRE ATT&CK tactic/technique ID
    _CATEGORY_MITRE: Dict[str, str] = {
        "recon":        "TA0043",  # Reconnaissance
        "scanning":     "TA0007",  # Discovery
        "exploit":      "TA0002",  # Execution
        "post_exploit": "TA0002",
        "privesc":      "TA0004",  # Privilege Escalation
        "credential":   "TA0006",  # Credential Access
        "lateral":      "TA0008",  # Lateral Movement
        "persistence":  "TA0003",  # Persistence
        "exfil":        "TA0010",  # Exfiltration
        "c2":           "TA0011",  # Command and Control
        "reporting":    "",
        "other":        "",
    }

    def __init__(self, lazyown_dir: Path = BASE_DIR) -> None:
        if not _PANDAS_OK:
            raise RuntimeError(
                "pandas and pyarrow are required. "
                "Run: pip install pandas pyarrow"
            )
        self._root       = lazyown_dir
        self._parquets   = lazyown_dir / "parquets"
        self._parquets.mkdir(parents=True, exist_ok=True)
        self._session_pkt = self._parquets / "session_knowledge.parquet"
        self._cmd2_map   = _build_cmd2_category_map(lazyown_dir / "lazyown.py")
        log.info(f"cmd2 map: {len(self._cmd2_map)} commands mapped")

    # ── Session knowledge ─────────────────────────────────────────────────────

    def _load_session(self) -> "pd.DataFrame":
        """Load existing session_knowledge.parquet or return empty DataFrame."""
        if self._session_pkt.exists():
            try:
                return pd.read_parquet(self._session_pkt)
            except Exception as exc:
                log.warning(f"corrupt session parquet, starting fresh: {exc}")
        return pd.DataFrame(columns=self.SCHEMA_COLS)

    def sync(self, csv_path: Path = CSV_PATH) -> int:
        """
        Ingest sessions/LazyOwn_session_report.csv into session_knowledge.parquet.

        New rows are enriched with id/category/success/outcome.
        Existing rows (matched by id) are preserved — their manual annotations
        (success, category) are NOT overwritten.

        Returns the number of NEW rows added.
        """
        if not csv_path.exists():
            log.warning(f"CSV not found: {csv_path}")
            return 0

        existing = self._load_session()
        existing_ids: set = set(existing["id"].tolist()) if not existing.empty else set()

        new_rows: List[Dict[str, Any]] = []
        try:
            with csv_path.open(newline="", encoding="utf-8", errors="replace") as fh:
                reader = csv.DictReader(fh)
                for raw in reader:
                    cmd  = (raw.get("command") or "").strip()
                    if not cmd:
                        continue
                    args    = (raw.get("args") or "").strip()
                    dest_ip = (raw.get("destination_ip") or "").strip()
                    start   = (raw.get("start") or "").strip()
                    row_id  = _stable_id(start, cmd, args, dest_ip)
                    if row_id in existing_ids:
                        continue

                    # Phase hint from cmd2 map, then keyword fallback
                    phase_hint = self._cmd2_map.get(cmd, "")
                    if not phase_hint:
                        for kw, ph in _KEYWORD_PHASE.items():
                            if kw in cmd.lower() or kw in args.lower():
                                phase_hint = ph
                                break

                    classified = _classify_row(cmd, args, phase_hint)

                    cat = classified["category"]
                    new_rows.append({
                        "id":               row_id,
                        "start":            start,
                        "end":              (raw.get("end") or "").strip(),
                        "source_ip":        (raw.get("source_ip") or "").strip(),
                        "source_port":      str(raw.get("source_port") or ""),
                        "destination_ip":   dest_ip,
                        "destination_port": str(raw.get("destination_port") or ""),
                        "domain":           (raw.get("domain") or "").strip(),
                        "subdomain":        (raw.get("subdomain") or "").strip(),
                        "url":              (raw.get("url") or "").strip(),
                        "pivot_port":       (raw.get("pivot_port") or "").strip(),
                        "command":          cmd,
                        "args":             args,
                        "category":         cat,
                        "success":          classified["success"],
                        "outcome":          classified["outcome"],
                        "reward":           int(classified["reward"]),
                        "confidence":       float(classified["confidence"]),
                        "tier":             classified["tier"],
                        "reason":           classified["reason"],
                        # v2 enriched columns
                        "output_snippet":   "",
                        "finding_type":     "none",
                        "mitre_id":         self._CATEGORY_MITRE.get(cat, ""),
                        "target_service":   "",
                        "target_port":      str(raw.get("destination_port") or ""),
                        "campaign_id":      "",
                    })

        except Exception as exc:
            log.error(f"CSV parse error: {exc}")
            return 0

        if not new_rows:
            log.info("sync: no new rows")
            return 0

        new_df = pd.DataFrame(new_rows)
        merged = pd.concat([existing, new_df], ignore_index=True)
        merged.to_parquet(self._session_pkt, index=False, compression="snappy")
        log.info(f"sync: {len(new_rows)} new rows → {self._session_pkt.name}")
        return len(new_rows)

    def annotate(
        self,
        row_id: str,
        success: Optional[bool] = None,
        category: Optional[str] = None,
        outcome: Optional[str]  = None,
    ) -> bool:
        """
        Patch a row in session_knowledge.parquet by its id.
        Only supplied fields are updated.  Returns True if found.
        """
        df = self._load_session()
        mask = df["id"] == row_id
        if not mask.any():
            log.warning(f"annotate: id not found: {row_id}")
            return False

        if success is not None:
            df.loc[mask, "success"] = bool(success)
            df.loc[mask, "outcome"] = ("success" if success else "failure") if outcome is None else outcome
        if category is not None:
            df.loc[mask, "category"] = str(category)
        if outcome is not None:
            df.loc[mask, "outcome"] = str(outcome)

        df.to_parquet(self._session_pkt, index=False, compression="snappy")
        log.info(f"annotate: patched row {row_id}")
        return True

    def annotate_rich(
        self,
        row_id: str,
        output: str = "",
        finding_type: str = "",
        target_service: str = "",
        target_port: str = "",
        campaign_id: str = "",
        success: Optional[bool] = None,
        category: Optional[str] = None,
        outcome: Optional[str] = None,
    ) -> bool:
        """
        Full annotation after real execution: stores output snippet + all metadata.
        Use this instead of annotate() from the auto_loop for richer training data.
        """
        df = self._load_session()
        mask = df["id"] == row_id
        if not mask.any():
            return False

        if success is not None:
            df.loc[mask, "success"] = bool(success)
            df.loc[mask, "outcome"] = (
                ("success" if success else "failure") if outcome is None else outcome
            )
        if category is not None:
            df.loc[mask, "category"] = str(category)
            df.loc[mask, "mitre_id"] = self._CATEGORY_MITRE.get(category, "")
        if outcome is not None:
            df.loc[mask, "outcome"] = str(outcome)
        if output:
            df.loc[mask, "output_snippet"] = output[:300]
            # Infer finding_type from output if not supplied
            if not finding_type:
                out_lower = output.lower()
                if any(k in out_lower for k in ("password", "passwd", "cleartext")):
                    finding_type = "credential"
                elif any(k in out_lower for k in ("cve-", "osvdb-", "vulnerability")):
                    finding_type = "vulnerability"
                elif re.search(r"[0-9a-f]{32}:[0-9a-f]{32}", out_lower):
                    finding_type = "hash"
                elif any(k in out_lower for k in ("user:", "username:", "samaccountname")):
                    finding_type = "user"
                elif re.search(r"^\s*/[a-z]", output, re.MULTILINE):
                    finding_type = "path"
        if finding_type:
            df.loc[mask, "finding_type"] = finding_type
        if target_service:
            df.loc[mask, "target_service"] = target_service
        if target_port:
            df.loc[mask, "target_port"] = target_port
        if campaign_id:
            df.loc[mask, "campaign_id"] = campaign_id

        df.to_parquet(self._session_pkt, index=False, compression="snappy")
        return True

    def query_session(
        self,
        phase: Optional[str]  = None,
        target: Optional[str] = None,
        success_only: bool    = False,
        limit: int            = 20,
    ) -> List[Dict[str, Any]]:
        """
        Query session_knowledge.parquet.

        phase:        filter by category column (e.g. "recon", "scanning")
        target:       filter by destination_ip
        success_only: only return rows where success == True
        limit:        max rows returned
        """
        df = self._load_session()
        if df.empty:
            return []

        if phase:
            # Normalise: "01. Reconnaissance" → "recon" if full label passed
            norm = _CMD2_TO_PHASE.get(phase, phase).lower()
            df = df[df["category"].str.lower() == norm]
        if target:
            df = df[df["destination_ip"] == target]
        if success_only:
            df = df[df["success"] == True]  # noqa: E712

        # Most recent first
        if "start" in df.columns:
            df = df.sort_values("start", ascending=False)

        return df.head(limit).to_dict(orient="records")

    # ── Generic parquet query ─────────────────────────────────────────────────

    def query_knowledge(
        self,
        keyword: str,
        parquet_name: Optional[str] = None,
        columns: Optional[List[str]] = None,
        limit: int = 15,
    ) -> Dict[str, List[Dict]]:
        """
        Search for keyword across one or all parquets in parquets/.

        parquet_name: stem of the parquet file (e.g. "binarios", "techniques").
                      If None, searches all parquets.
        columns:      restrict search to these columns (default: all string columns).
        Returns dict {parquet_stem: [matching rows...]}.
        """
        results: Dict[str, List[Dict]] = {}

        if parquet_name:
            targets = [self._parquets / f"{parquet_name}.parquet"]
        else:
            targets = sorted(self._parquets.glob("*.parquet"))

        kw_lower = keyword.lower()

        for pkt_path in targets:
            stem = pkt_path.stem
            try:
                df = pd.read_parquet(pkt_path)
            except Exception as exc:
                log.debug(f"skip {pkt_path.name}: {exc}")
                continue

            # Search across string columns
            search_cols = columns or [c for c in df.columns if df[c].dtype == object]
            mask = pd.Series([False] * len(df), index=df.index)
            for col in search_cols:
                if col in df.columns:
                    try:
                        mask = mask | df[col].astype(str).str.lower().str.contains(
                            kw_lower, regex=False, na=False
                        )
                    except Exception:
                        pass

            matched = df[mask].head(limit)
            if not matched.empty:
                results[stem] = matched.to_dict(orient="records")

        return results

    # ── Atomic Red Team structured search ─────────────────────────────────────

    def query_atomic(
        self,
        keyword: str = "",
        mitre_id: str = "",
        platform: str = "",
        scope: str = "",
        has_prereqs: Optional[bool] = None,
        complexity: str = "",
        limit: int = 10,
        include_command: bool = False,
    ) -> List[Dict]:
        """
        Structured query over the enriched Atomic Red Team catalogue
        (parquets/techniques_enriched.parquet).

        Falls back to query_knowledge("techniques", keyword) if the enriched
        parquet is not yet built.

        Parameters
        ----------
        keyword      : free-text search over name + description + keyword_tags
        mitre_id     : exact or prefix (T1059 matches T1059, T1059.001, …)
        platform     : linux | windows | macos | freebsd | cloud
        scope        : local | remote | elevated | any
        has_prereqs  : True → only tests needing prereqs; False → no prereqs
        complexity   : low | medium | high
        limit        : max results (default 10)
        include_command : add command_preview to each result
        """
        if not _PANDAS_OK:
            return [{"error": "pandas not installed"}]
        try:
            sys.path.insert(0, str(self._root / "modules"))
            from atomic_enricher import query_atomic as _qa
            return _qa(
                keyword=keyword,
                mitre_id=mitre_id,
                platform=platform,
                scope=scope,
                has_prereqs=has_prereqs,
                complexity=complexity,
                limit=limit,
                include_command=include_command,
            )
        except Exception as exc:
            log.warning("query_atomic fallback to keyword search: %s", exc)
            if keyword:
                res = self.query_knowledge(keyword, "techniques", limit=limit)
                return res.get("techniques", [])
            return []

    # ── Context for current operation phase ───────────────────────────────────

    def context_for_phase(
        self,
        phase: str,
        target: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Return a rich context dict for MCP reasoning:

        {
          "phase":             "recon",
          "target":            "10.10.11.78",
          "successful_cmds":   [{"command": ..., "args": ..., "start": ...}, ...],
          "failed_cmds":       [...],
          "gtfobins_relevant": [...],   # from binarios.parquet
          "mitre_techniques":  [...],   # from techniques.parquet
          "lolbas_relevant":   [...],   # from lolbas_index.parquet
          "summary":           "3 recon successes, 1 failure. Top commands: ..."
        }
        """
        # Session data
        successes = self.query_session(phase=phase, target=target, success_only=True,  limit=limit)
        failures  = self.query_session(phase=phase, target=target, success_only=False, limit=limit)
        failures  = [r for r in failures if not r.get("success", True)]

        # Map phase → keyword for knowledge search
        phase_kw_map: Dict[str, str] = {
            "recon":       "reconnaissance",
            "scanning":    "enumeration",
            "exploit":     "exploit",
            "post_exploit":"post-exploitation",
            "privesc":     "privilege escalation",
            "credential":  "credential",
            "lateral":     "lateral movement",
            "persistence": "persistence",
            "exfil":       "exfiltration",
            "c2":          "command control",
        }
        kw = phase_kw_map.get(phase, phase)

        # GTFOBins
        gtf: List[Dict] = []
        try:
            df_bin = pd.read_parquet(self._parquets / "binarios.parquet")
            phase_bins = {
                "privesc":     ["sudo", "suid"],
                "credential":  ["file-read", "file-write"],
                "post_exploit":["reverse-shell", "bind-shell"],
                "exploit":     ["command", "shell"],
            }
            fn_kws = phase_bins.get(phase, [kw.split()[0]])
            mask = pd.Series([False] * len(df_bin), index=df_bin.index)
            for fkw in fn_kws:
                mask = mask | df_bin.apply(
                    lambda r: fkw.lower() in str(r).lower(), axis=1
                )
            gtf = df_bin[mask].head(5).to_dict(orient="records")
        except Exception:
            pass

        # MITRE techniques
        mitre: List[Dict] = []
        try:
            df_tech = pd.read_parquet(self._parquets / "techniques.parquet")
            mask = df_tech["name"].str.lower().str.contains(kw, na=False) | \
                   df_tech["description"].str.lower().str.contains(kw, na=False)
            mitre = (
                df_tech[mask][["mitre_id", "name", "description"]]
                .head(5)
                .to_dict(orient="records")
            )
        except Exception:
            pass

        # LOLBAS
        lolbas: List[Dict] = []
        try:
            df_lol = pd.read_parquet(self._parquets / "lolbas_index.parquet")
            mask = df_lol.apply(lambda r: kw.lower() in str(r).lower(), axis=1)
            lolbas = df_lol[mask].head(5).to_dict(orient="records")
        except Exception:
            pass

        # Summary text
        top_cmds = [r["command"] for r in successes[:3]]
        summary = (
            f"{len(successes)} {phase} successes, {len(failures)} failures "
            f"for target {target or 'all'}. "
            f"Top commands: {', '.join(top_cmds) or 'none yet'}."
        )

        return {
            "phase":             phase,
            "target":            target,
            "successful_cmds":   [_slim(r) for r in successes],
            "failed_cmds":       [_slim(r) for r in failures],
            "gtfobins_relevant": gtf,
            "mitre_techniques":  mitre,
            "lolbas_relevant":   lolbas,
            "summary":           summary,
        }

    # ── Stats ─────────────────────────────────────────────────────────────────

    def stats(self) -> str:
        df = self._load_session()
        if df.empty:
            return "session_knowledge.parquet: empty — run sync first."
        total     = len(df)
        success_n = int(df["success"].sum()) if "success" in df.columns else 0
        by_cat    = df["category"].value_counts().to_dict() if "category" in df.columns else {}
        cat_str   = "  ".join(f"{k}={v}" for k, v in sorted(by_cat.items()))
        return (
            f"session_knowledge: {total} rows, "
            f"{success_n} success, {total-success_n} failure/unknown\n"
            f"  by category: {cat_str}"
        )

    def list_parquets(self) -> List[str]:
        return [p.stem for p in sorted(self._parquets.glob("*.parquet"))]

    # ── Trained classifier (tier-0 — trained on the parquet itself) ───────────

    def train_classifier(self, min_rows: int = 50) -> Dict[str, Any]:
        """
        Train a lightweight RandomForest classifier on session_knowledge.parquet.

        Features: command name (hashed), first arg token (hashed), category label.
        Target:   success (bool).

        The trained model is saved to parquets/classifier.pkl.
        Returns a dict with {accuracy, n_train, n_test, model_path, feature_importance}.

        Auto-called by sync() when the parquet grows by more than 200 annotated rows.
        Requires: scikit-learn (pip install scikit-learn)
        """
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import LabelEncoder
            import pickle
        except ImportError:
            return {"error": "scikit-learn not installed. Run: pip install scikit-learn"}

        df = self._load_session()
        # Only use rows with real annotations (not the optimistic bootstrap default)
        annotated = df[df["outcome"].isin(["success", "failure"])].copy()
        if len(annotated) < min_rows:
            return {
                "error": f"Only {len(annotated)} annotated rows (need {min_rows}). "
                         "Run more operations and annotate outcomes first."
            }

        # Feature engineering — no NLP, just category codes
        le_cmd = LabelEncoder()
        le_cat = LabelEncoder()

        annotated["cmd_code"] = le_cmd.fit_transform(
            annotated["command"].str.split("/").str[-1].str.split().str[0].fillna("unknown")
        )
        annotated["cat_code"] = le_cat.fit_transform(annotated["category"].fillna("other"))
        annotated["reward_f"] = annotated["reward"].fillna(0).astype(float)
        annotated["conf_f"]   = annotated["confidence"].fillna(0.5).astype(float)

        X = annotated[["cmd_code", "cat_code", "reward_f", "conf_f"]].values
        y = annotated["success"].astype(int).values

        if len(set(y)) < 2:
            return {"error": "All rows have same success value — need both True and False samples."}

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
        clf.fit(X_train, y_train)
        accuracy = float(clf.score(X_test, y_test))

        # Save model + encoders
        model_path = self._parquets / "classifier.pkl"
        with model_path.open("wb") as fh:
            pickle.dump({"clf": clf, "le_cmd": le_cmd, "le_cat": le_cat}, fh)

        importances = dict(zip(
            ["cmd_code", "cat_code", "reward", "confidence"],
            clf.feature_importances_.tolist(),
        ))
        log.info(f"classifier trained: accuracy={accuracy:.2%} n={len(annotated)}")
        return {
            "accuracy":           f"{accuracy:.2%}",
            "n_train":            len(X_train),
            "n_test":             len(X_test),
            "n_annotated":        len(annotated),
            "model_path":         str(model_path),
            "feature_importance": importances,
        }

    def predict_success(self, command: str, category: str) -> Optional[float]:
        """
        Use the trained classifier to estimate probability of success.
        Returns float 0.0–1.0 or None if no model exists.
        """
        model_path = self._parquets / "classifier.pkl"
        if not model_path.exists():
            return None
        try:
            import pickle
            with model_path.open("rb") as fh:
                bundle = pickle.load(fh)
            clf    = bundle["clf"]
            le_cmd = bundle["le_cmd"]
            le_cat = bundle["le_cat"]

            cmd_tok = command.split("/")[-1].split()[0] if command else "unknown"
            # Handle unseen labels
            if cmd_tok not in le_cmd.classes_:
                cmd_code = 0
            else:
                cmd_code = int(le_cmd.transform([cmd_tok])[0])
            if category not in le_cat.classes_:
                cat_code = 0
            else:
                cat_code = int(le_cat.transform([category])[0])

            prob = clf.predict_proba([[cmd_code, cat_code, 0.0, 0.5]])[0][1]
            return float(prob)
        except Exception as exc:
            log.debug(f"predict_success failed: {exc}")
            return None


def _slim(row: Dict[str, Any]) -> Dict[str, Any]:
    """Return compact view of a session row for MCP context."""
    return {
        "id":      row.get("id", ""),
        "start":   row.get("start", ""),
        "target":  row.get("destination_ip", ""),
        "command": row.get("command", ""),
        "args":    (row.get("args") or "")[:80],
        "outcome": row.get("outcome", ""),
        "reason":  row.get("reason", ""),
    }


# ── Singleton for MCP use ─────────────────────────────────────────────────────

_pdb: Optional[ParquetDB] = None


def get_pdb(lazyown_dir: Path = BASE_DIR) -> Optional[ParquetDB]:
    global _pdb
    if _pdb is None and _PANDAS_OK:
        try:
            _pdb = ParquetDB(lazyown_dir)
        except Exception as exc:
            log.warning(f"ParquetDB init failed: {exc}")
    return _pdb


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="LazyOwn Parquet Knowledge Base")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("sync",  help="Ingest CSV → session_knowledge.parquet")
    sub.add_parser("stats", help="Show stats")
    sub.add_parser("list",  help="List available parquets")

    p_tr = sub.add_parser("train", help="Train RandomForest classifier on annotated rows")
    p_tr.add_argument("--min-rows", type=int, default=50,
                      help="Minimum annotated rows required (default 50)")

    p_q = sub.add_parser("query", help="Query session knowledge")
    p_q.add_argument("phase",   nargs="?", help="Phase filter (recon, scanning, exploit...)")
    p_q.add_argument("--target", default=None)
    p_q.add_argument("--success", action="store_true")
    p_q.add_argument("--limit",  type=int, default=10)
    p_q.add_argument("--keyword", default=None, help="Keyword search across parquets")
    p_q.add_argument("--parquet", default=None, help="Target parquet name")

    p_a = sub.add_parser("annotate", help="Annotate a row's success/category")
    p_a.add_argument("row_id")
    p_a.add_argument("--success",  action="store_true",  default=None)
    p_a.add_argument("--failure",  action="store_true",  default=False)
    p_a.add_argument("--category", default=None)
    p_a.add_argument("--outcome",  default=None)

    p_ctx = sub.add_parser("context", help="Full context for a phase")
    p_ctx.add_argument("phase")
    p_ctx.add_argument("--target", default=None)

    args = parser.parse_args()

    if not _PANDAS_OK:
        print("ERROR: pandas and pyarrow not installed. Run: pip install pandas pyarrow")
        return

    db = ParquetDB()

    if args.cmd == "sync":
        n = db.sync()
        print(f"Synced {n} new rows.")
        print(db.stats())

    elif args.cmd == "stats":
        print(db.stats())

    elif args.cmd == "list":
        for p in db.list_parquets():
            print(f"  {p}")

    elif args.cmd == "query":
        if args.keyword:
            results = db.query_knowledge(args.keyword, args.parquet, limit=args.limit)
            for stem, rows in results.items():
                print(f"\n── {stem} ({len(rows)} matches) ──")
                for r in rows[:5]:
                    print(json.dumps({k: str(v)[:80] for k, v in r.items()}, indent=2))
        else:
            rows = db.query_session(
                phase=args.phase,
                target=args.target,
                success_only=args.success,
                limit=args.limit,
            )
            for r in rows:
                print(json.dumps({k: str(v)[:80] for k, v in r.items()}, indent=2))

    elif args.cmd == "annotate":
        success: Optional[bool] = None
        if args.success:
            success = True
        elif args.failure:
            success = False
        ok = db.annotate(args.row_id, success=success,
                         category=args.category, outcome=args.outcome)
        print("patched" if ok else "id not found")

    elif args.cmd == "context":
        ctx = db.context_for_phase(args.phase, args.target)
        print(json.dumps(ctx, indent=2, default=str))

    elif args.cmd == "train":
        result = db.train_classifier(min_rows=args.min_rows)
        print(json.dumps(result, indent=2, default=str))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
