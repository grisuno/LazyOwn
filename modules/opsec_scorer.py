"""OPSEC scoring engine — pre-execution noise assessment and gated scoring.

Single contract module for every OPSEC evaluation in the framework. It
exposes two complementary scorers that share one set of risk primitives:

- :class:`OpsecScorer` — lightweight pre-execution noise assessment that
  returns a :class:`OpsecScore` with a plain-text risk label. Used for
  advisory warnings before running a command.

- :class:`OpsecScorerV2` — real-time, context-aware scoring with action
  gating (allow / warn / confirm / block) and session trend tracking.
  Returns a :class:`GatedOpsecScore`.

Both share the risk-threshold mapping (see :func:`_risk_bucket`), so the
noise-to-risk translation is defined exactly once. The two command tables
— :data:`COMMAND_NOISE` and :data:`COMMAND_RISK_PROFILES` — remain distinct
by design: the former drives advisory noise scoring while the latter drives
gating with its own threat model and extra exfiltration payload profiles.

Usage:
    from modules.opsec_scorer import OpsecScorer, OpsecScorerV2, OpsecContext

    scorer = OpsecScorer(payload)
    score = scorer.score("secretsdump", rhost="10.10.11.5")

    gated = OpsecScorerV2(context=OpsecContext(killchain_phase="credential_access"))
    assessment = gated.assess("mimikatz")
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

log = logging.getLogger("opsec_scorer")

PHASE_NOISE: dict[str, int] = {
    "recon": 2,
    "scanning": 3,
    "enumeration": 3,
    "exploitation": 5,
    "post_exploitation": 7,
    "privesc": 7,
    "credential_access": 8,
    "lateral_movement": 8,
    "persistence": 6,
    "exfiltration": 9,
    "c2": 6,
    "evasion": 4,
    "reporting": 1,
}

PHASE_BASE_NOISE: dict[str, int] = {
    "recon": 1,
    "scanning": 3,
    "enumeration": 3,
    "exploitation": 5,
    "post_exploitation": 7,
    "privesc": 7,
    "credential_access": 8,
    "lateral_movement": 8,
    "persistence": 6,
    "exfiltration": 9,
    "c2": 5,
    "evasion": 4,
    "reporting": 0,
}

COMMAND_NOISE: dict[str, dict[str, Any]] = {
    "ping": {"noise": 1, "phase": "recon", "detectable_by": ["none"]},
    "lazynmap": {"noise": 4, "phase": "scanning", "detectable_by": ["IDS", "firewall_logs"]},
    "nmap": {"noise": 5, "phase": "scanning", "detectable_by": ["IDS", "firewall_logs", "EDR"]},
    "gobuster": {"noise": 5, "phase": "enumeration", "detectable_by": ["WAF", "web_logs"]},
    "ffuf": {"noise": 5, "phase": "enumeration", "detectable_by": ["WAF", "web_logs"]},
    "nikto": {"noise": 6, "phase": "enumeration", "detectable_by": ["WAF", "IDS", "web_logs"]},
    "whatweb": {"noise": 2, "phase": "enumeration", "detectable_by": ["web_logs"]},
    "enum4linux": {"noise": 4, "phase": "enumeration", "detectable_by": ["windows_event_logs"]},
    "smbmap": {"noise": 4, "phase": "enumeration", "detectable_by": ["windows_event_logs"]},
    "cme": {"noise": 5, "phase": "enumeration", "detectable_by": ["windows_event_logs", "EDR"]},
    "getnpusers": {"noise": 7, "phase": "credential_access", "detectable_by": ["windows_event_logs", "SIEM"]},
    "secretsdump": {"noise": 9, "phase": "credential_access", "detectable_by": ["EDR", "windows_event_logs", "SIEM"]},
    "bloodhound": {"noise": 7, "phase": "enumeration", "detectable_by": ["EDR", "windows_event_logs"]},
    "psexec": {"noise": 8, "phase": "lateral_movement", "detectable_by": ["EDR", "windows_event_logs", "SIEM"]},
    "wmiexec": {"noise": 8, "phase": "lateral_movement", "detectable_by": ["EDR", "SIEM"]},
    "evil": {"noise": 6, "phase": "lateral_movement", "detectable_by": ["windows_event_logs"]},
    "mimikatz": {"noise": 10, "phase": "credential_access", "detectable_by": ["EDR", "AV", "windows_event_logs", "SIEM"]},
    "kerberoast": {"noise": 5, "phase": "credential_access", "detectable_by": ["windows_event_logs"]},
    "asreproast": {"noise": 5, "phase": "credential_access", "detectable_by": ["windows_event_logs"]},
    "linpeas": {"noise": 7, "phase": "privesc", "detectable_by": ["EDR", "auditd"]},
    "winpeas": {"noise": 7, "phase": "privesc", "detectable_by": ["EDR", "AV"]},
    "chisel": {"noise": 5, "phase": "lateral_movement", "detectable_by": ["firewall_logs", "netflow"]},
    "socat": {"noise": 4, "phase": "lateral_movement", "detectable_by": ["netflow"]},
    "payload": {"noise": 6, "phase": "c2", "detectable_by": ["EDR", "AV", "SIEM"]},
    "venom": {"noise": 5, "phase": "c2", "detectable_by": ["none"]},
    "msf": {"noise": 7, "phase": "exploitation", "detectable_by": ["EDR", "AV"]},
    "sqlmap": {"noise": 6, "phase": "exploitation", "detectable_by": ["WAF", "web_logs"]},
    "searchsploit": {"noise": 1, "phase": "exploitation", "detectable_by": ["none"]},
    "lazynuclei": {"noise": 5, "phase": "scanning", "detectable_by": ["WAF", "IDS", "web_logs"]},
    "createrevshell": {"noise": 4, "phase": "c2", "detectable_by": ["none"]},
}

COMMAND_RISK_PROFILES: dict[str, dict[str, Any]] = {
    "ping": {"base_noise": 1, "detects": [], "phase": "recon"},
    "nmap": {"base_noise": 5, "detects": ["IDS", "firewall_logs", "netflow"], "phase": "scanning"},
    "lazynmap": {"base_noise": 4, "detects": ["IDS", "firewall_logs"], "phase": "scanning"},
    "gobuster": {"base_noise": 5, "detects": ["WAF", "web_logs"], "phase": "enumeration"},
    "ffuf": {"base_noise": 5, "detects": ["WAF", "web_logs"], "phase": "enumeration"},
    "nikto": {"base_noise": 6, "detects": ["WAF", "IDS", "web_logs"], "phase": "enumeration"},
    "nuclei": {"base_noise": 5, "detects": ["WAF", "IDS"], "phase": "scanning"},
    "mimikatz": {"base_noise": 10, "detects": ["EDR", "AV", "SIEM", "windows_event_logs"], "phase": "credential_access"},
    "secretsdump": {"base_noise": 9, "detects": ["EDR", "windows_event_logs", "SIEM"], "phase": "credential_access"},
    "psexec": {"base_noise": 8, "detects": ["EDR", "windows_event_logs", "SIEM"], "phase": "lateral_movement"},
    "wmiexec": {"base_noise": 8, "detects": ["EDR", "SIEM"], "phase": "lateral_movement"},
    "bloodhound": {"base_noise": 7, "detects": ["EDR", "windows_event_logs", "SIEM"], "phase": "enumeration"},
    "kerberoast": {"base_noise": 5, "detects": ["windows_event_logs"], "phase": "credential_access"},
    "asreproast": {"base_noise": 5, "detects": ["windows_event_logs"], "phase": "credential_access"},
    "smbmap": {"base_noise": 4, "detects": ["windows_event_logs"], "phase": "enumeration"},
    "enum4linux": {"base_noise": 4, "detects": ["windows_event_logs"], "phase": "enumeration"},
    "chisel": {"base_noise": 5, "detects": ["firewall_logs", "netflow"], "phase": "lateral_movement"},
    "payload_generate": {"base_noise": 2, "detects": [], "phase": "c2"},
    "payload_deliver": {"base_noise": 7, "detects": ["EDR", "AV", "SIEM"], "phase": "c2"},
    "exfil_http": {"base_noise": 6, "detects": ["proxy_logs", "DLP"], "phase": "exfiltration"},
    "exfil_dns": {"base_noise": 8, "detects": ["DNS_logs", "SIEM"], "phase": "exfiltration"},
    "exfil_icmp": {"base_noise": 7, "detects": ["netflow", "IDS"], "phase": "exfiltration"},
}

TARGET_SENSITIVITY_BONUS: dict[str, int] = {
    "dc": 3,
    "domain_controller": 3,
    "exchange": 2,
    "sql": 2,
    "database": 2,
    "fileserver": 2,
    "web": 1,
    "workstation": 0,
    "unknown": 1,
}

MITIGATIONS: dict[str, list[str]] = {
    "EDR": ["enable sleep jitter", "use process injection evasion", "enable AMSI bypass", "use certutil alt download"],
    "AV": ["use obfuscated payload", "enable sleep obfuscation", "compile custom implant", "use living-off-the-land"],
    "IDS": ["reduce scan speed (-T2)", "fragment packets (-f)", "use decoy scanning (-D)", "stagger port scan timing"],
    "WAF": ["rotate user-agent", "use request throttling", "encode payloads", "bypass WAF rules"],
    "firewall_logs": ["use ephemeral ports", "enable traffic morphing", "fragment packets", "use DNS tunneling"],
    "windows_event_logs": ["clear event logs post-execution", "use non-admin techniques", "limit lateral tool usage"],
    "SIEM": ["avoid high-volume enumeration", "operate during off-hours", "use low-and-slow approach"],
    "web_logs": ["rotate user-agent", "use URL encoding", "limit request rate", "use proxy chain"],
    "netflow": ["use beacon C2", "enable jitter", "use DNS/ICMP tunneling", "limit connection frequency"],
    "auditd": ["use LD_PRELOAD evasion", "use statically linked tools", "clear bash history"],
}

RISK_THRESHOLD_LOW = 2
RISK_THRESHOLD_MEDIUM = 4
RISK_THRESHOLD_HIGH = 7

RISK_LABELS = ("low", "medium", "high", "critical")


class RiskLevel(IntEnum):
    """OPSEC risk levels ordered by severity."""

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class GateAction(IntEnum):
    """Action gating decisions for command execution."""

    ALLOW = 0
    WARN = 1
    CONFIRM = 2
    BLOCK = 3


def _risk_bucket(noise: int) -> int:
    """Return a zero-based severity bucket (0..3) for a 0-10 noise score.

    Args:
        noise: A clamped 0-10 noise value.

    Returns:
        0 for low, 1 for medium, 2 for high, 3 for critical.
    """
    if noise <= RISK_THRESHOLD_LOW:
        return 0
    if noise <= RISK_THRESHOLD_MEDIUM:
        return 1
    if noise <= RISK_THRESHOLD_HIGH:
        return 2
    return 3


def _risk_label(noise: int) -> str:
    """Return the human-readable risk label for a noise score.

    Args:
        noise: A clamped 0-10 noise value.

    Returns:
        One of ``low``, ``medium``, ``high``, ``critical``.
    """
    return RISK_LABELS[_risk_bucket(noise)]


def _risk_level(noise: int) -> RiskLevel:
    """Return the :class:`RiskLevel` enum value for a noise score.

    Args:
        noise: A clamped 0-10 noise value.

    Returns:
        The matching :class:`RiskLevel`, never ``NONE`` for a scored command.
    """
    return RiskLevel(_risk_bucket(noise) + 1)


@dataclass
class OpsecContext:
    """Real-time operational context for gated OPSEC scoring.

    Attributes:
        killchain_phase: Current phase (recon, scan, enum, exploit, etc.).
        rhost: Target IP address.
        target_environment: Target environment type.
        access_level: Current access level on target.
        edr_detected: Whether EDR/AV was detected on target.
        siem_detected: Whether SIEM/correlation was observed.
        time_window: Operation time window.
        credential_type: Type of credentials in use.
        is_privileged: Whether running as privileged user on target.
        evasion_active: Whether evasion measures are active.
        artifacts_created: Count of artifacts left so far.
        session_uptime_minutes: Minutes since session start.
    """

    killchain_phase: str = "recon"
    rhost: str = ""
    target_environment: str = "unknown"
    access_level: str = "none"
    edr_detected: bool = False
    siem_detected: bool = False
    time_window: str = "business_hours"
    credential_type: str = "none"
    is_privileged: bool = False
    evasion_active: bool = False
    artifacts_created: int = 0
    session_uptime_minutes: int = 0


@dataclass
class OpsecScore:
    """Advisory OPSEC assessment for a single command.

    Attributes:
        command: Command being assessed.
        noise_score: 0-10 noise rating.
        detection_risk: Human-readable detection risk label.
        risk_level: Plain-text risk label (low/medium/high/critical).
        confidence: 0-1 confidence in the assessment.
        detectable_by: Detection systems that may observe the command.
        mitigation: Suggested mitigations.
        recommendation: Human-readable guidance.
    """

    command: str
    noise_score: int
    detection_risk: str
    risk_level: str
    confidence: float
    detectable_by: list[str] = field(default_factory=list)
    mitigation: list[str] = field(default_factory=list)
    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return the score serialized as a plain dictionary."""
        return {
            "command": self.command,
            "noise_score": self.noise_score,
            "detection_risk": self.detection_risk,
            "risk_level": self.risk_level,
            "confidence": self.confidence,
            "detectable_by": self.detectable_by,
            "mitigation": self.mitigation,
            "recommendation": self.recommendation,
        }


@dataclass
class GatedOpsecScore:
    """Context-aware, gated OPSEC assessment for a single command.

    Attributes:
        command: Command being assessed.
        risk_level: Numeric risk level.
        risk_label: Human-readable risk label.
        noise_score: 0-10 noise rating.
        detection_surface: Detection systems triggered.
        gate_action: Whether to allow, warn, confirm, or block.
        mitigations: Suggested mitigations ranked by effectiveness.
        alternative_commands: Lower-noise alternatives if available.
        explanation: Human-readable rationale for the score.
        timestamp: Unix timestamp of the assessment.
    """

    command: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    risk_label: str = "LOW"
    noise_score: int = 0
    detection_surface: list[str] = field(default_factory=list)
    gate_action: GateAction = GateAction.ALLOW
    mitigations: list[str] = field(default_factory=list)
    alternative_commands: list[str] = field(default_factory=list)
    explanation: str = ""
    timestamp: float = 0.0


class OpsecScorer:
    """Pre-execution OPSEC evaluator for LazyOwn commands.

    Scores commands on base noise, phase-appropriate tool usage, target
    sensitivity, evasion status, and detection tool coverage.

    Attributes:
        payload: Configuration dict from payload.json.
        world_model: Optional world model for target context.
        evasion_active: Whether any evasion mechanism is enabled.
    """

    def __init__(
        self,
        payload: dict[str, Any] | None = None,
        world_model: Any = None,
    ) -> None:
        self._payload = payload or {}
        self._world_model = world_model

    @property
    def evasion_active(self) -> bool:
        sleep = self._payload.get("sleep") or self._payload.get("sleep_start")
        return bool(sleep and int(sleep) > 0)

    @property
    def traffic_morphing_active(self) -> bool:
        urls = [
            self._payload.get("url_traffic_1", ""),
            self._payload.get("url_traffic_2", ""),
            self._payload.get("url_traffic_3", ""),
        ]
        return any(u.startswith("http") for u in urls)

    def score(
        self,
        command: str,
        rhost: str = "",
        phase_override: str | None = None,
    ) -> OpsecScore:
        """Score an OPSEC risk for ``command`` against ``rhost``.

        Args:
            command: LazyOwn command alias to evaluate.
            rhost: Target IP for sensitivity analysis.
            phase_override: Force a phase context (default: from world_model).

        Returns:
            OpsecScore with risk assessment and recommendations.
        """
        cmd_lower = command.lower().strip()
        info = COMMAND_NOISE.get(cmd_lower)
        if info is None:
            info = self._estimate_noise(cmd_lower)

        base_noise = info["noise"]
        phase = info["phase"]
        detectable = info.get("detectable_by", [])

        phase_penalty = self._phase_mismatch_penalty(phase, phase_override)
        target_bonus = self._target_sensitivity_bonus(rhost)
        evasion_bonus = self._evasion_reduction(detectable)

        final_noise = base_noise + phase_penalty + target_bonus - evasion_bonus
        final_noise = max(0, min(10, final_noise))

        risk_level = self._noise_to_risk(final_noise)
        mitigations = self._gather_mitigations(detectable, final_noise)
        detection_risk = self._detection_risk_label(detectable, final_noise)
        recommendation = self._build_recommendation(risk_level, mitigations)

        return OpsecScore(
            command=cmd_lower,
            noise_score=final_noise,
            detection_risk=detection_risk,
            risk_level=risk_level,
            confidence=0.7 if info != COMMAND_NOISE.get(cmd_lower) else 0.85,
            detectable_by=detectable,
            mitigation=mitigations,
            recommendation=recommendation,
        )

    def score_batch(self, commands: list[str], rhost: str = "") -> dict[str, OpsecScore]:
        """Score multiple commands and return {command: OpsecScore}."""
        return {cmd: self.score(cmd, rhost=rhost) for cmd in commands}

    def suggest_mitigations(
        self,
        command: str,
        detectable_by: list[str] | None = None,
    ) -> list[str]:
        """Return mitigation suggestions for a given command."""
        detectable = detectable_by or COMMAND_NOISE.get(command, {}).get("detectable_by", [])
        return self._gather_mitigations(detectable, COMMAND_NOISE.get(command, {}).get("noise", 5))

    def _estimate_noise(self, command: str) -> dict[str, Any]:
        """Heuristically estimate noise for unknown commands."""
        high_noise_keywords = ["exploit", "pwn", "dump", "inject", "bypass", "hook"]
        medium_noise_keywords = ["scan", "enum", "search", "fingerprint", "list", "show"]
        low_noise_keywords = ["cat", "read", "help", "info", "status", "notes"]

        noise = 5
        for kw in high_noise_keywords:
            if kw in command:
                noise = 8
                break
        for kw in medium_noise_keywords:
            if kw in command and noise == 5:
                noise = 5
                break
        for kw in low_noise_keywords:
            if kw in command:
                noise = 2
                break

        return {"noise": noise, "phase": "unknown", "detectable_by": ["SIEM"]}

    def _phase_mismatch_penalty(self, tool_phase: str, override: str | None) -> int:
        phase = override
        if phase is None and self._world_model is not None:
            try:
                phase = self._world_model.get_phase().value
            except Exception:
                pass
        if phase is None:
            try:
                from modules.killchain import KillChain
                phase = KillChain.current_phase()
            except Exception:
                phase = self._payload.get("current_phase", "recon")
        phase_noise = PHASE_NOISE.get(phase, 3)
        tool_noise = PHASE_NOISE.get(tool_phase, 5)
        if tool_noise > phase_noise + 2 and phase_noise < 5:
            return 3
        if tool_noise > phase_noise:
            return 1
        return 0

    def _target_sensitivity_bonus(self, rhost: str) -> int:
        if not rhost:
            return 1
        host_purpose = self._get_host_purpose(rhost)
        for label, bonus in TARGET_SENSITIVITY_BONUS.items():
            if label in host_purpose.lower():
                return bonus
        return TARGET_SENSITIVITY_BONUS["unknown"]

    def _get_host_purpose(self, rhost: str) -> str:
        if self._world_model is not None:
            try:
                host = self._world_model.get_host(rhost)
                if host and hasattr(host, "purpose"):
                    return host.purpose or ""
            except Exception:
                pass
        from modules.db import LazyOwnDB
        try:
            db = LazyOwnDB()
            hosts = db.host_search(address=rhost)
            if hosts:
                return hosts[0].get("purpose", "")
        except Exception:
            pass
        return "unknown"

    def _evasion_reduction(self, detectable: list[str]) -> int:
        reduction = 0
        if self.evasion_active:
            for detector in detectable:
                if detector in ("EDR", "AV", "SIEM"):
                    reduction += 1
        if self.traffic_morphing_active:
            for detector in detectable:
                if detector in ("firewall_logs", "netflow", "web_logs", "WAF"):
                    reduction += 1
        return min(reduction, 3)

    def _gather_mitigations(self, detectable: list[str], noise: int) -> list[str]:
        mitigations: list[str] = []
        seen: set[str] = set()
        for detector in detectable:
            for m in MITIGATIONS.get(detector, []):
                if m not in seen:
                    mitigations.append(m)
                    seen.add(m)
        if noise >= 8:
            fallback = "consider a lower-noise alternative technique"
            if fallback not in seen:
                mitigations.append(fallback)
        if not mitigations:
            mitigations.append("standard OPSEC: monitor execution, have cleanup ready")
        return mitigations

    @staticmethod
    def _noise_to_risk(noise: int) -> str:
        """Return the plain-text risk label for a noise score."""
        return _risk_label(noise)

    @staticmethod
    def _detection_risk_label(detectable: list[str], noise: int) -> str:
        if not detectable or detectable == ["none"]:
            return "minimal"
        if noise <= 3:
            return "low"
        if noise <= 6:
            return "moderate"
        if noise <= 8:
            return "significant"
        return "near-certain"

    @staticmethod
    def _build_recommendation(risk_level: str, mitigations: list[str]) -> str:
        prefix = {
            "low": "Safe to proceed.",
            "medium": "Proceed with awareness.",
            "high": "Mitigations recommended before execution.",
            "critical": "EXTREME CAUTION: full OPSEC review required before execution.",
        }
        base = prefix.get(risk_level, "Evaluate context before running.")
        if len(mitigations) > 1:
            base += f" Top mitigation: {mitigations[0]}. {len(mitigations) - 1} more available."
        elif mitigations:
            base += f" Suggested: {mitigations[0]}."
        return base


class OpsecScorerV2:
    """Real-time OPSEC scoring engine with action gating.

    Evaluates each command against the current operational context,
    producing a :class:`RiskLevel` and :class:`GateAction`.

    Attributes:
        context: Current operational context.
        score_history: Chronological list of past scores for trend analysis.
        risk_threshold: Maximum allowed risk before blocking.
        environment_profiles: Predefined risk profiles per target type.
    """

    ENVIRONMENT_PROFILES: dict[str, dict[str, Any]] = {
        "enterprise": {
            "edr_likely": True,
            "siem_likely": True,
            "base_noise": 3,
            "threat_hunting_likely": True,
            "description": "Well-defended enterprise with EDR + SIEM",
        },
        "smb": {
            "edr_likely": False,
            "siem_likely": False,
            "base_noise": 1,
            "threat_hunting_likely": False,
            "description": "Small business with little security",
        },
        "government": {
            "edr_likely": True,
            "siem_likely": True,
            "base_noise": 5,
            "threat_hunting_likely": True,
            "description": "Government/military with aggressive monitoring",
        },
        "critical_infrastructure": {
            "edr_likely": True,
            "siem_likely": True,
            "base_noise": 4,
            "threat_hunting_likely": True,
            "description": "OT/ICS environment with segregation",
        },
        "cloud": {
            "edr_likely": True,
            "siem_likely": True,
            "base_noise": 3,
            "threat_hunting_likely": False,
            "description": "Cloud-native environment (AWS/Azure/GCP)",
        },
        "dark_web": {
            "edr_likely": False,
            "siem_likely": False,
            "base_noise": 0,
            "threat_hunting_likely": False,
            "description": "Anonymous/dark web target - low monitoring",
        },
    }

    def __init__(self, context: OpsecContext | None = None):
        self.context = context or OpsecContext()
        self.score_history: list[GatedOpsecScore] = []
        self.risk_threshold = RiskLevel.HIGH

    def assess(self, command: str, extra_context: dict[str, Any] | None = None) -> GatedOpsecScore:
        """Assess OPSEC risk for a command in the current context.

        Args:
            command: The command string to evaluate.
            extra_context: Additional context overrides.

        Returns:
            GatedOpsecScore with risk assessment and gating decision.
        """
        cmd_base = command.split()[0].lower() if command else ""
        profile = COMMAND_RISK_PROFILES.get(cmd_base, {"base_noise": 3, "detects": ["unknown"], "phase": "unknown"})

        env_profile = self.ENVIRONMENT_PROFILES.get(
            self.context.target_environment, self.ENVIRONMENT_PROFILES["enterprise"]
        )

        base_noise = profile.get("base_noise", 3)
        phase_noise = PHASE_BASE_NOISE.get(self.context.killchain_phase, 3)
        env_modifier = env_profile.get("base_noise", 3)
        edr_mod = 2 if self.context.edr_detected else 0
        siem_mod = 2 if self.context.siem_detected else 0
        priv_mod = -1 if self.context.is_privileged else 0
        evasion_mod = -2 if self.context.evasion_active else 1
        artifact_mod = min(self.context.artifacts_created // 10, 3)
        uptime_mod = min(self.context.session_uptime_minutes // 60, 4)

        noise_score = max(0, min(10, (
            base_noise + phase_noise + env_modifier +
            edr_mod + siem_mod + priv_mod + evasion_mod +
            artifact_mod + uptime_mod
        ) // 3))

        detection_surface = list(profile.get("detects", []))
        if self.context.edr_detected and "EDR" not in detection_surface:
            detection_surface.append("EDR")
        if self.context.siem_detected and "SIEM" not in detection_surface:
            detection_surface.append("SIEM")

        risk_level = self._noise_to_risk(noise_score)
        gate_action = self._risk_to_gate(risk_level)
        mitigations = self._generate_mitigations(noise_score, detection_surface)
        alternatives = self._find_alternatives(cmd_base)
        explanation = self._build_explanation(cmd_base, noise_score, detection_surface, gate_action)

        score = GatedOpsecScore(
            command=command,
            risk_level=risk_level,
            risk_label=risk_level.name,
            noise_score=noise_score,
            detection_surface=detection_surface,
            gate_action=gate_action,
            mitigations=mitigations,
            alternative_commands=alternatives,
            explanation=explanation,
            timestamp=time.time(),
        )

        self.score_history.append(score)
        return score

    def should_allow(self, command: str) -> tuple[bool, GatedOpsecScore]:
        """Quick gating check - returns (allowed, score).

        Args:
            command: Command string to check.

        Returns:
            Tuple of (is_allowed: bool, assessment: GatedOpsecScore).
        """
        score = self.assess(command)
        allowed = score.gate_action == GateAction.ALLOW
        return allowed, score

    def get_trend(self) -> dict[str, Any]:
        """Analyze OPSEC risk trend over the session.

        Returns:
            Dict with trend data: escalating, stable, or improving.
        """
        if len(self.score_history) < 3:
            return {"trend": "insufficient_data", "sample_count": len(self.score_history)}

        recent = self.score_history[-5:]
        avg_recent = sum(s.noise_score for s in recent) / max(len(recent), 1)
        avg_overall = sum(s.noise_score for s in self.score_history) / max(len(self.score_history), 1)

        if avg_recent > avg_overall + 2:
            trend = "escalating"
        elif avg_recent < avg_overall - 2:
            trend = "improving"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "recent_avg_noise": round(avg_recent, 1),
            "overall_avg_noise": round(avg_overall, 1),
            "total_operations": len(self.score_history),
            "high_risk_ops": sum(1 for s in self.score_history if s.risk_level >= RiskLevel.HIGH),
            "critical_risk_ops": sum(1 for s in self.score_history if s.risk_level >= RiskLevel.CRITICAL),
        }

    @staticmethod
    def _noise_to_risk(noise: int) -> RiskLevel:
        """Return the RiskLevel enum for a noise score."""
        return _risk_level(noise)

    def _risk_to_gate(self, risk: RiskLevel) -> GateAction:
        if risk < RiskLevel.HIGH:
            return GateAction.ALLOW
        if risk == RiskLevel.HIGH:
            return GateAction.WARN
        if risk == RiskLevel.CRITICAL:
            return GateAction.CONFIRM
        return GateAction.BLOCK

    @staticmethod
    def _generate_mitigations(noise: int, detects: list[str]) -> list[str]:
        mitigations = []

        if noise >= 7:
            mitigations.append("Consider spacing operations over longer intervals (10+ min between commands)")
            mitigations.append("Use lower-noise enumeration before noisy operations")
        if "EDR" in detects:
            mitigations.append("Enable evasion measures (syscall direct, API unhooking) before execution")
            mitigations.append("Verify payload obfuscation and padding before delivery")
        if "SIEM" in detects:
            mitigations.append("Use multiple source IPs or rotate through proxies")
            mitigations.append("Avoid command patterns that trigger common SIEM correlation rules")
        if "windows_event_logs" in detects:
            mitigations.append("Plan log cleanup immediately after operation")
        if "WAF" in detects:
            mitigations.append("Rate-limit requests and randomize User-Agent headers")
        if "netflow" in detects:
            mitigations.append("Randomize beacon intervals and add jitter")
        if not mitigations:
            mitigations.append("Operation within acceptable noise parameters")

        return mitigations

    @staticmethod
    def _find_alternatives(cmd: str) -> list[str]:
        alternatives: dict[str, list[str]] = {
            "mimikatz": ["Use procdump + pypykatz", "Use handle duplication + lsass minidump", "Use nanodump (loader)"],
            "secretsdump": ["Use reg save + pypykatz locally", "Use ntdsutil locally", "Use Volume Shadow Copy + esentutl"],
            "psexec": ["Use wmiexec (less detection)", "Use dcomexec", "Use schtasks_exec"],
            "nmap": ["Use masscan (faster, less signature)", "Use zmap (stateless)", "Use lazynmap (custom timing)"],
            "bloodhound": ["Use SharpHound stealth options", "Use ldapsearch + manual mapping", "Use recon only (no data collection)"],
        }
        return alternatives.get(cmd, [])

    @staticmethod
    def _build_explanation(cmd: str, noise: int, detects: list[str], gate: GateAction) -> str:
        parts = [f"Command '{cmd}' scored {noise}/10 noise."]
        if detects:
            parts.append(f"Detectable by: {', '.join(detects)}.")
        if gate == GateAction.ALLOW:
            parts.append("Operation within safe risk thresholds.")
        elif gate == GateAction.WARN:
            parts.append("WARNING: Elevated detection risk. Review mitigations.")
        elif gate == GateAction.CONFIRM:
            parts.append("HIGH RISK: Operator confirmation required before execution.")
        elif gate == GateAction.BLOCK:
            parts.append("BLOCKED: Operation exceeds maximum risk threshold.")
        return " ".join(parts)


def score_command(
    command: str,
    payload: dict[str, Any] | None = None,
    rhost: str = "",
) -> OpsecScore:
    """Convenience function: score a single command without creating a scorer instance.

    Args:
        command: LazyOwn command to evaluate.
        payload: Configuration dict (loaded from payload.json if None).
        rhost: Target IP for sensitivity.

    Returns:
        OpsecScore dataclass instance.
    """
    if payload is None:
        try:
            from core.config import load_payload
            payload = load_payload()
        except Exception:
            payload = {}
    scorer = OpsecScorer(payload)
    return scorer.score(command, rhost=rhost)


__all__ = [
    "OpsecScorer",
    "OpsecScorerV2",
    "OpsecScore",
    "GatedOpsecScore",
    "OpsecContext",
    "RiskLevel",
    "GateAction",
    "score_command",
    "COMMAND_NOISE",
    "COMMAND_RISK_PROFILES",
    "PHASE_NOISE",
    "PHASE_BASE_NOISE",
    "MITIGATIONS",
    "TARGET_SENSITIVITY_BONUS",
]
