"""
modules/reactive_engine.py
===========================
Parses command output and produces concrete next-action recommendations:
  - PrivEsc advice (GTFOBins / LOLBas / lazyaddons YAML)
  - Evasion advice when AV/EDR signatures detected in output
  - Parquet technique lookup (Atomic Red Team + MITRE)
  - Output-driven state inference (new creds, new host, shells)

Design (SOLID)
--------------
- Single Responsibility : OutputParser, PrivescAdvisor, EvasionAdvisor,
                          ParquetLookup each own one concern.
- Open/Closed           : new signal detectors via new SignalMatcher subclass.
- Liskov                : all SignalMatcher subclasses honour Optional[Signal].
- Interface Segregation : ReactiveEngine exposes only analyse() to callers.
- Dependency Inversion  : ReactiveEngine depends on AbstractSignalMatcher.
"""
from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_ROOT = Path(__file__).parent.parent
_log = logging.getLogger(__name__)

SEMANTIC_MIN_SCORE: float = 0.55
SEMANTIC_QUERY_LIMIT: int = 3
SEMANTIC_OUTPUT_LIMIT: int = 1000
SEMANTIC_REASON_LIMIT: int = 140
SEMANTIC_MITRE_TACTIC: str = "T1595"
SEMANTIC_PRIORITY: int = 5
SEMANTIC_FILENAME_PATTERN: re.Pattern = re.compile(
    r"command_(?P<verb>[A-Za-z0-9_\-]+)output"
)
SEMANTIC_PAYLOAD_KEY: str = "reactive_semantic_enabled"


def _default_config_loader() -> Dict[str, Any]:
    """Return the contents of ``payload.json`` as a dictionary.

    Imports are performed lazily so the reactive engine still loads in
    environments where ``core.config`` is not yet wired (early
    bootstrap, isolated unit tests). Any failure falls back to an empty
    dictionary, which behaves as "feature enabled by default" for
    :class:`SemanticContextAdvisor`.
    """

    try:
        from core.config import load_payload
    except ImportError:
        return {}
    try:
        return load_payload() or {}
    except Exception as exc:
        _log.debug("reactive_engine: payload load failed: %s", exc)
        return {}


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

@dataclass
class Signal:
    """A detected indicator in command output."""
    kind: str          # "cred", "av_blocked", "shell_error", "new_host",
                       # "privesc_hint", "version", "service"
    value: str
    confidence: float  # 0.0-1.0
    raw_match: str     # the matching substring for audit


@dataclass
class ReactiveDecision:
    """What the autonomous loop should do next given the signals."""
    action: str            # "run_command", "escalate_evasion", "switch_tool",
                           # "record_cred", "add_host", "mark_privesc_done"
    command: str           # ready-to-run LazyOwn command (may be empty)
    reason: str
    mitre_tactic: str = ""
    priority: int = 5      # 1=critical, 10=low
    signals: List[Signal] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Signal matchers
# ---------------------------------------------------------------------------

class AbstractSignalMatcher(ABC):

    @abstractmethod
    def match(self, output: str, context: Dict) -> List[Signal]:
        ...


class AVBlockedMatcher(AbstractSignalMatcher):
    """Detects AV/EDR blocking patterns in tool output."""

    _PATTERNS = [
        (r"access\s+is\s+denied", "windows_acl"),
        (r"operation\s+not\s+permitted", "linux_acl"),
        (r"virus\s+detected|malware\s+detected|threat\s+detected", "av_alert"),
        (r"windows\s+defender\s+(blocked|detected|prevented|quarantine)|microsoft\s+antivirus", "defender"),
        (r"(crowdstrike|carbonblack|sentinelone|cylance|symantec|mcafee|kaspersky)\s+(blocked|detected|prevented|alert)", "edr"),
        (r"amsi\.dll|amsi\s+bypass\s+blocked|antimalware\s+scan\s+interface\s+(blocked|detected)", "amsi"),
        (r"execution\s+policy|cannot\s+be\s+loaded\s+because\s+running\s+scripts",
         "powershell_policy"),
        (r"quarantine|blocked\s+by\s+security|security\s+alert", "quarantine"),
    ]

    # Lines containing these substrings are LazyOwn framework noise — skip them
    _NOISE_PATTERNS = (
        "registered from yaml",
        "register from lua",
        "registered from lua",
        "environment activated",
        "[+] command '",
    )

    def match(self, output: str, context: Dict) -> List[Signal]:
        # Strip LazyOwn framework registration noise before matching
        clean_lines = [
            ln for ln in output.splitlines()
            if not any(np in ln.lower() for np in self._NOISE_PATTERNS)
        ]
        lower = "\n".join(clean_lines).lower()
        signals: List[Signal] = []
        for pattern, kind in self._PATTERNS:
            m = re.search(pattern, lower)
            if m:
                signals.append(Signal(
                    kind="av_blocked",
                    value=kind,
                    confidence=0.85,
                    raw_match=m.group(),
                ))
        return signals


class CredentialFoundMatcher(AbstractSignalMatcher):
    """Detects credentials in command output."""

    _PATTERNS = [
        r"(?:password|passwd|pwd)\s*[:=]\s*(\S+)",
        r"(?:username|user|login)\s*[:=]\s*(\S+)",
        r"(\w+):(\$[0-9a-fA-F$./]{20,})",   # shadow hash
        r"([a-fA-F0-9]{32}:[a-fA-F0-9]{32})",  # NTLM hash
        r"(\w+)\s*:\s*([a-fA-F0-9]{64})",       # SHA256-like
        r"(aad3b435b51404eeaad3b435b51404ee:[a-fA-F0-9]{32})",  # empty LM
    ]

    def match(self, output: str, context: Dict) -> List[Signal]:
        signals: List[Signal] = []
        for pattern in self._PATTERNS:
            for m in re.finditer(pattern, output, re.IGNORECASE):
                signals.append(Signal(
                    kind="cred",
                    value=m.group()[:120],
                    confidence=0.7,
                    raw_match=m.group(),
                ))
        return signals[:10]  # cap to avoid noise


class PrivescHintMatcher(AbstractSignalMatcher):
    """Detects indicators that privesc may be possible."""

    _PATTERNS = [
        (r"sudo\s+-l", "sudo_allowed"),
        (r"\(root\)\s+NOPASSWD", "sudo_nopasswd"),
        (r"suid\s+bit|s-isuid|setuid", "suid_binary"),
        (r"writable.*cron|cron.*writable|/etc/cron", "writable_cron"),
        (r"CVE-20[12][0-9]-\d{4,}", "cve_match"),
        (r"kernel\s+version.*[2-5]\.\d", "kernel_version"),
        (r"polkit|pkexec|pwnkit", "polkit"),
        (r"dirty.*cow|dirtycow", "dirtycow"),
        (r"token.*impersonat|seimpersonateprivilege", "token_impersonation"),
        (r"unquoted\s+service|unquotedsvc", "unquoted_service"),
        (r"writabledll|dll\s+hijack", "dll_hijack"),
        (r"alwaysinstallelevated", "always_install_elevated"),
    ]

    def match(self, output: str, context: Dict) -> List[Signal]:
        lower = output.lower()
        signals: List[Signal] = []
        for pattern, hint in self._PATTERNS:
            m = re.search(pattern, lower)
            if m:
                signals.append(Signal(
                    kind="privesc_hint",
                    value=hint,
                    confidence=0.75,
                    raw_match=m.group(),
                ))
        return signals


class NewHostMatcher(AbstractSignalMatcher):
    """Detects new IP addresses in command output."""

    _IP_RE = re.compile(
        r"\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b"
    )

    def match(self, output: str, context: Dict) -> List[Signal]:
        known = set(context.get("known_hosts", []))
        signals: List[Signal] = []
        for m in self._IP_RE.finditer(output):
            ip = m.group()
            if ip not in known:
                signals.append(Signal(
                    kind="new_host",
                    value=ip,
                    confidence=0.6,
                    raw_match=ip,
                ))
                known.add(ip)
        return signals


class ServiceVersionMatcher(AbstractSignalMatcher):
    """Extracts service version strings for exploit matching."""

    _PATTERNS = [
        r"(OpenSSH[_\s]\d[\d.]+)",
        r"(Apache(?:/\d[\d.]+)?)",
        r"(nginx(?:/\d[\d.]+)?)",
        r"(IIS(?:/\d[\d.]+)?)",
        r"(SMBv[123])",
        r"(Windows Server \d{4}(?:\s+R2)?)",
        r"(Windows \d{1,2}(?:\.\d)?)",
        r"(Ubuntu \d{2}\.\d{2})",
        r"(Debian \w+)",
    ]

    def match(self, output: str, context: Dict) -> List[Signal]:
        signals: List[Signal] = []
        for pattern in self._PATTERNS:
            for m in re.finditer(pattern, output, re.IGNORECASE):
                signals.append(Signal(
                    kind="version",
                    value=m.group(1),
                    confidence=0.8,
                    raw_match=m.group(),
                ))
        return signals


class ShellErrorMatcher(AbstractSignalMatcher):
    """Detects tool errors that warrant switching techniques."""

    _PATTERNS = [
        (r"connection\s+refused", "conn_refused"),
        (r"no\s+route\s+to\s+host", "no_route"),
        (r"timed?\s*out|timeout", "timeout"),
        (r"authentication\s+fail", "auth_fail"),
        (r"permission\s+denied", "perm_denied"),
        (r"command\s+not\s+found", "cmd_not_found"),
        (r"no\s+such\s+file", "no_such_file"),
        (r"invalid\s+password|wrong\s+password", "bad_cred"),
    ]

    def match(self, output: str, context: Dict) -> List[Signal]:
        lower = output.lower()
        signals: List[Signal] = []
        for pattern, kind in self._PATTERNS:
            m = re.search(pattern, lower)
            if m:
                signals.append(Signal(
                    kind="shell_error",
                    value=kind,
                    confidence=0.9,
                    raw_match=m.group(),
                ))
        return signals[:3]  # only the first few errors


# ---------------------------------------------------------------------------
# Parquet lookup (GTFOBins + LOLBas + Atomic Red Team techniques)
# ---------------------------------------------------------------------------

class ParquetAdvisor:
    """
    Queries parquet DBs for binary-based privesc and LOLBas opportunities.
    Gracefully returns [] when pandas or parquet files are unavailable.
    """

    def __init__(self, root: Path = _ROOT) -> None:
        self._root = root
        self._binarios: Optional[object] = None   # DataFrame
        self._lolbas: Optional[object] = None
        self._techniques: Optional[object] = None
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        try:
            import pandas as pd
            b = self._root / "parquets" / "binarios.parquet"
            l = self._root / "parquets" / "lolbas_index.parquet"
            t = self._root / "parquets" / "techniques.parquet"
            if b.exists():
                self._binarios = pd.read_parquet(b)
            if l.exists():
                self._lolbas = pd.read_parquet(l)
            if t.exists():
                self._techniques = pd.read_parquet(t)
        except Exception as exc:
            _log.debug("ParquetAdvisor load failed: %s", exc)

    def gtfobins_for(self, binary: str) -> List[str]:
        self._load()
        if self._binarios is None:
            return []
        try:
            df = self._binarios
            mask = df["Binary"].astype(str).str.lower() == binary.lower()
            rows = df[mask]
            return [r["Function Name"] for _, r in rows.iterrows()]
        except Exception as exc:
            _log.debug("ParquetAdvisor.gtfobins_for(%s) failed: %s", binary, exc)
            return []

    def lolbas_for(self, binary: str) -> List[Tuple[str, str]]:
        """Returns [(function_name, att&ck_technique), ...]."""
        self._load()
        if self._lolbas is None:
            return []
        try:
            df = self._lolbas
            mask = df["Binary"].astype(str).str.lower().str.contains(binary.lower())
            rows = df[mask].head(5)
            return [(r["Function Name"], r.get("ATT&CK", "")) for _, r in rows.iterrows()]
        except Exception as exc:
            _log.debug("ParquetAdvisor.lolbas_for(%s) failed: %s", binary, exc)
            return []

    def technique_commands_for(self, platform: str, keyword: str) -> List[str]:
        """Return atomic test commands for platform matching keyword."""
        self._load()
        if self._techniques is None:
            return []
        try:
            df = self._techniques
            p_mask = df["platforms"].astype(str).str.lower().str.contains(
                platform.lower()
            )
            k_mask = (
                df["name"].astype(str).str.lower().str.contains(keyword.lower()) |
                df["description"].astype(str).str.lower().str.contains(keyword.lower())
            )
            rows = df[p_mask & k_mask].head(3)
            cmds: List[str] = []
            for _, r in rows.iterrows():
                cmd = str(r.get("command", "")).strip()
                if cmd and cmd.lower() != "nan":
                    cmds.append(cmd[:200])
            return cmds
        except Exception as exc:
            _log.debug(
                "ParquetAdvisor.technique_commands_for(%s, %s) failed: %s",
                platform, keyword, exc,
            )
            return []


# ---------------------------------------------------------------------------
# Evasion advisor
# ---------------------------------------------------------------------------

class EvasionAdvisor:
    """
    Maps detected AV/EDR signals to concrete LazyOwn evasion commands.
    Uses lazyaddons YAML (adversary_yaml) for Windows; native commands for Linux.
    """

    _WINDOWS_EVASION = [
        ("amsi",        "adversary_yaml amsi",         "T1562", "AMSI bypass via amsi.yaml"),
        ("defender",    "disableav",                   "T1562", "Disable Windows Defender"),
        ("powershell_policy", "adversary_yaml persist", "T1562", "Bypass PowerShell execution policy"),
        ("edr",         "aes_pe",                      "T1027", "AES-encrypt PE for EDR bypass"),
        ("av_alert",    "ofuscatorps1",                "T1027", "Obfuscate PowerShell payload"),
        ("quarantine",  "scarecrow",                   "T1027", "ScareCrow EDR bypass"),
        ("default",     "darkarmour",                  "T1027", "DarkArmour PE crypter"),
    ]

    _LINUX_EVASION = [
        ("default",     "ofuscatesh",                  "T1027", "Obfuscate shell script"),
    ]

    # ACL-only signals (kernel permission errors, not AV) — never trigger evasion
    _ACL_ONLY_KINDS: frozenset = frozenset({"linux_acl", "windows_acl"})

    def suggest(self, signals: List[Signal], platform: str) -> List[ReactiveDecision]:
        # Only real AV/EDR blocks trigger evasion — not generic kernel ACL errors
        # ("operation not permitted" / "access is denied" are normal scan noise)
        av_signals = [
            s for s in signals
            if s.kind == "av_blocked" and s.value not in self._ACL_ONLY_KINDS
        ]
        if not av_signals:
            return []

        decisions: List[ReactiveDecision] = []
        evasion_map = self._WINDOWS_EVASION if platform == "windows" else self._LINUX_EVASION

        for sig in av_signals:
            for av_kind, command, mitre, reason in evasion_map:
                if av_kind in (sig.value, "default"):
                    decisions.append(ReactiveDecision(
                        action="escalate_evasion",
                        command=command,
                        reason=f"{reason} (triggered by: {sig.value})",
                        mitre_tactic=mitre,
                        priority=1,
                        signals=[sig],
                    ))
                    break  # one evasion per signal

        return decisions


# ---------------------------------------------------------------------------
# PrivEsc advisor
# ---------------------------------------------------------------------------

class PrivescAdvisor:
    """
    Suggests privilege escalation commands based on:
    - detected privesc hints in output
    - platform (linux vs windows)
    - GTFOBins / LOLBas parquet lookup
    - lazyaddons YAML (adversary_yaml)
    """

    _LINUX_QUICK = [
        ("sudo_nopasswd",    "adversary_yaml",   "sudo -l && sudo /bin/bash",       "T1548", 1),
        ("suid_binary",      "find",             "find / -perm -4000 -type f 2>/dev/null", "T1548", 2),
        ("writable_cron",    "find",             "find /etc/cron* -writable 2>/dev/null",  "T1053", 2),
        ("polkit",           "lazypwn",          "lazypwn",                         "T1068", 1),
        ("dirtycow",         "download_exploit", "download_exploit CVE-2016-5195",  "T1068", 2),
        ("kernel_version",   "nuclei",           "nuclei -u http://127.0.0.1 -t lpe", "T1068", 3),
        ("default",          "lynis",            "lynis",                           "T1518", 5),
    ]

    _WINDOWS_QUICK = [
        ("token_impersonation", "adversary_yaml",  "adversary_yaml amsi",          "T1134", 1),
        ("unquoted_service",    "wmiexecpro",       "wmiexecpro",                   "T1574", 2),
        ("dll_hijack",          "createdll",        "createdll",                    "T1574", 2),
        ("always_install_elevated", "msfshellcoder", "msfshellcoder",               "T1548", 2),
        ("cve_match",           "download_exploit", "download_exploit",             "T1068", 3),
        ("default",             "rubeus",           "rubeus",                       "T1558", 4),
    ]

    def suggest(
        self,
        signals: List[Signal],
        platform: str,
        parquet: Optional[ParquetAdvisor] = None,
    ) -> List[ReactiveDecision]:
        priv_signals = [s for s in signals if s.kind == "privesc_hint"]
        decisions: List[ReactiveDecision] = []

        quick_map = self._LINUX_QUICK if platform != "windows" else self._WINDOWS_QUICK
        matched: set = set()

        for sig in priv_signals:
            for hint, tool, cmd, mitre, prio in quick_map:
                if hint == sig.value and hint not in matched:
                    decisions.append(ReactiveDecision(
                        action="run_command",
                        command=cmd,
                        reason=f"PrivEsc hint '{hint}' detected — running {tool}",
                        mitre_tactic=mitre,
                        priority=prio,
                        signals=[sig],
                    ))
                    matched.add(hint)
                    break

        # If no specific hint matched, suggest generic escalation check
        if not decisions and priv_signals:
            default_cmd = "lynis" if platform != "windows" else "rubeus"
            decisions.append(ReactiveDecision(
                action="run_command",
                command=default_cmd,
                reason="Generic privesc check triggered by output analysis",
                mitre_tactic="T1518",
                priority=5,
                signals=priv_signals[:1],
            ))

        # GTFOBins enhancement: if a binary name appears in output, suggest abuse
        if parquet:
            for common_bin in ("python3", "python", "perl", "ruby", "find",
                               "awk", "nmap", "vim", "less", "tar", "zip"):
                funcs = parquet.gtfobins_for(common_bin)
                if "Sudo" in funcs or "SUID" in funcs:
                    decisions.append(ReactiveDecision(
                        action="run_command",
                        command=f"find / -perm -4000 -name {common_bin} 2>/dev/null",
                        reason=f"GTFOBins: {common_bin} has SUID/Sudo abuse vectors",
                        mitre_tactic="T1548",
                        priority=3,
                        signals=[],
                    ))
                    break

        return decisions


# ---------------------------------------------------------------------------
# Semantic context advisor
# ---------------------------------------------------------------------------

class SemanticContextAdvisor:
    """Suggest follow-up commands by semantic similarity to past sessions.

    Last-resort hint that only fires when the regex-based matchers and
    advisors produce nothing useful. Relies on
    :class:`modules.session_rag.SessionRAG` (ChromaDB when available,
    keyword fallback otherwise) so it carries no extra runtime
    dependency. When the RAG layer is missing or the operator disabled
    it via ``payload.json[reactive_semantic_enabled]``, the advisor
    silently returns an empty list — never breaking the regex pipeline.
    """

    def __init__(
        self,
        rag: Optional[Any] = None,
        config_loader: Optional[Any] = None,
        min_score: float = SEMANTIC_MIN_SCORE,
        query_limit: int = SEMANTIC_QUERY_LIMIT,
    ) -> None:
        """Initialise the advisor.

        Args:
            rag: Optional pre-built RAG instance. Injected in tests; in
                production the singleton from ``modules.session_rag`` is
                loaded lazily on first :meth:`suggest` call.
            config_loader: Callable returning a payload dictionary. Used
                only to gate the advisor via
                :data:`SEMANTIC_PAYLOAD_KEY`. Falsy return values disable
                the advisor for that call.
            min_score: Minimum cosine similarity score to keep a hit.
            query_limit: Maximum number of RAG hits to request per call.
        """

        self._rag = rag
        self._rag_loaded = rag is not None
        self._config_loader = config_loader
        self._min_score = float(min_score)
        self._query_limit = int(query_limit)

    def _load_rag(self) -> Optional[Any]:
        """Resolve the RAG singleton on first use.

        Returns:
            The shared :class:`SessionRAG` instance, or ``None`` when the
            module cannot be imported.
        """

        if self._rag_loaded:
            return self._rag
        self._rag_loaded = True
        try:
            from session_rag import get_rag
        except ImportError:
            try:
                from modules.session_rag import get_rag
            except ImportError as exc:
                _log.debug("SemanticContextAdvisor: session_rag unavailable: %s", exc)
                return None
        try:
            self._rag = get_rag()
        except Exception as exc:
            _log.debug("SemanticContextAdvisor: get_rag failed: %s", exc)
            self._rag = None
        return self._rag

    def _enabled(self) -> bool:
        """Return whether the operator has the advisor turned on.

        When no config loader is wired, the advisor is assumed enabled.
        When the loader raises or the key is absent, defaults to
        enabled to preserve the historical "best-effort hints" UX.
        """

        if self._config_loader is None:
            return True
        try:
            payload = self._config_loader() or {}
        except Exception as exc:
            _log.debug("SemanticContextAdvisor: config load failed: %s", exc)
            return True
        return bool(payload.get(SEMANTIC_PAYLOAD_KEY, True))

    @staticmethod
    def _extract_verb(source: str) -> str:
        """Pull the originating command verb from a ``command_*`` filename.

        Args:
            source: Relative path returned by the RAG hit, typically
                ``logs/command_<verb>output<domain>.txt``.

        Returns:
            The extracted verb, or the empty string when the path does
            not follow the expected pattern.
        """

        if not source:
            return ""
        match = SEMANTIC_FILENAME_PATTERN.search(source)
        if not match:
            return ""
        return match.group("verb")

    def suggest(
        self,
        output: str,
        command: str = "",
        platform: str = "unknown",
        context: Optional[Dict[str, Any]] = None,
    ) -> List[ReactiveDecision]:
        """Return semantic next-step hints derived from past sessions.

        Args:
            output: Raw stdout+stderr from the executed command.
            command: The command that produced *output*.
            platform: Target platform tag (informational; not currently
                used to filter hits).
            context: Reserved for future extensions.

        Returns:
            Zero or more :class:`ReactiveDecision` with action
            ``"suggest_next"`` and priority
            :data:`SEMANTIC_PRIORITY` so regex-based decisions always
            outrank the semantic hint.
        """

        del platform, context

        if not output or not self._enabled():
            return []

        rag = self._load_rag()
        if rag is None or not getattr(rag, "_ready", False):
            return []

        try:
            hits = rag.query(
                output[:SEMANTIC_OUTPUT_LIMIT], n=self._query_limit
            )
        except Exception as exc:
            _log.debug("SemanticContextAdvisor: rag.query failed: %s", exc)
            return []

        decisions: List[ReactiveDecision] = []
        seen_verbs: set = set()
        for hit in hits or []:
            score = hit.get("score") if isinstance(hit, dict) else None
            if score is not None and score < self._min_score:
                continue
            source = hit.get("source", "") if isinstance(hit, dict) else ""
            verb = self._extract_verb(source)
            if not verb or verb == command or verb in seen_verbs:
                continue
            snippet = (hit.get("text") or "").strip()
            snippet = snippet.replace("\n", " ")[:SEMANTIC_REASON_LIMIT]
            score_label = (
                f"{score:.2f}" if isinstance(score, (int, float)) else "n/a"
            )
            decisions.append(
                ReactiveDecision(
                    action="suggest_next",
                    command=verb,
                    reason=(
                        f"Similar past output (score={score_label}): {snippet}"
                    ),
                    mitre_tactic=SEMANTIC_MITRE_TACTIC,
                    priority=SEMANTIC_PRIORITY,
                    signals=[],
                )
            )
            seen_verbs.add(verb)
        return decisions


# ---------------------------------------------------------------------------
# Reactive engine
# ---------------------------------------------------------------------------

class ReactiveEngine:
    """
    Analyses command output and produces prioritised ReactiveDecisions.
    Wire into the auto_loop after each step to close the reasoning cycle.
    """

    def __init__(
        self,
        matchers: Optional[List[AbstractSignalMatcher]] = None,
        evasion: Optional[EvasionAdvisor] = None,
        privesc: Optional[PrivescAdvisor] = None,
        parquet: Optional[ParquetAdvisor] = None,
        semantic: Optional[SemanticContextAdvisor] = None,
    ) -> None:
        self._matchers = matchers or [
            AVBlockedMatcher(),
            CredentialFoundMatcher(),
            PrivescHintMatcher(),
            NewHostMatcher(),
            ServiceVersionMatcher(),
            ShellErrorMatcher(),
        ]
        self._evasion = evasion or EvasionAdvisor()
        self._privesc = privesc or PrivescAdvisor()
        self._parquet = parquet or ParquetAdvisor()
        self._semantic = semantic or SemanticContextAdvisor(
            config_loader=_default_config_loader,
        )

    def analyse(
        self,
        output: str,
        command: str = "",
        platform: str = "unknown",
        context: Optional[Dict] = None,
    ) -> List[ReactiveDecision]:
        """
        Parse *output* and return prioritised ReactiveDecisions.

        Parameters
        ----------
        output   : raw stdout+stderr from the executed command
        command  : the command that produced the output (for context)
        platform : "linux", "windows", or "unknown"
        context  : dict with optional keys: known_hosts, credentials, phase
        """
        ctx = context or {}
        all_signals: List[Signal] = []
        for matcher in self._matchers:
            try:
                all_signals.extend(matcher.match(output, ctx))
            except Exception as exc:
                _log.debug(
                    "reactive_engine: matcher %s failed: %s",
                    matcher.__class__.__name__, exc,
                )
                continue

        decisions: List[ReactiveDecision] = []

        decisions.extend(self._evasion.suggest(all_signals, platform))

        decisions.extend(self._privesc.suggest(all_signals, platform, self._parquet))

        # New credentials found
        cred_signals = [s for s in all_signals if s.kind == "cred"]
        for sig in cred_signals[:3]:
            decisions.append(ReactiveDecision(
                action="record_cred",
                command=f"createcredentials {sig.value[:80]}",
                reason="Credential found in output — storing in session",
                mitre_tactic="T1552",
                priority=2,
                signals=[sig],
            ))

        # New hosts discovered
        host_signals = [s for s in all_signals if s.kind == "new_host"]
        for sig in host_signals[:5]:
            decisions.append(ReactiveDecision(
                action="add_host",
                command=f"set rhost {sig.value}",
                reason=f"New internal host {sig.value} detected in output",
                mitre_tactic="T1018",
                priority=3,
                signals=[sig],
            ))

        # Connection refused / tool error → suggest switch
        err_signals = [s for s in all_signals if s.kind == "shell_error"]
        for sig in err_signals[:1]:
            if sig.value in ("conn_refused", "no_route"):
                decisions.append(ReactiveDecision(
                    action="switch_tool",
                    command="portdiscover",
                    reason=f"Connection error ({sig.value}) — re-check reachability",
                    mitre_tactic="T1046",
                    priority=4,
                    signals=[sig],
                ))
            elif sig.value == "auth_fail":
                decisions.append(ReactiveDecision(
                    action="switch_tool",
                    command="passwordspray",
                    reason="Authentication failure — try password spray",
                    mitre_tactic="T1110",
                    priority=3,
                    signals=[sig],
                ))

        decisions.extend(
            self._semantic.suggest(output, command, platform, ctx)
        )

        decisions.sort(key=lambda d: d.priority)
        return decisions

    def top_decision(
        self,
        output: str,
        command: str = "",
        platform: str = "unknown",
        context: Optional[Dict] = None,
    ) -> Optional[ReactiveDecision]:
        """Return only the single highest-priority decision, or None."""
        decisions = self.analyse(output, command, platform, context)
        return decisions[0] if decisions else None


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------

_engine: Optional[ReactiveEngine] = None


def get_engine() -> ReactiveEngine:
    global _engine
    if _engine is None:
        _engine = ReactiveEngine()
    return _engine
