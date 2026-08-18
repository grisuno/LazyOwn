"""OPSEC real-time scoring and action gating — v2 with contextual risk assessment.

Evaluates operational security in real-time for every proposed action.
Integrates kill-chain phase, noise level, detection surface, target
environment factors, and historical detection data to produce actionable
OPSEC scores. Enforces action gating — blocking or warning on operations
that exceed configured risk thresholds.

Extends modules/opsec_scorer.py with: real-time context integration,
action gating (block/warn/allow), environment-aware scoring, mitigation
suggestion ranking, and opsec trend tracking.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"

log = logging.getLogger("opsec_v2")


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


@dataclass
class OpsecContext:
    """Real-time operational context for OPSEC scoring.

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
    """Detailed OPSEC risk assessment for a single command.

    Attributes:
        command: Command being assessed.
        risk_level: Numeric risk level.
        risk_label: Human-readable risk label.
        noise_score: 0-10 noise rating.
        detection_surface: List of detection systems triggered.
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


class OpsecScorerV2:
    """Real-time OPSEC scoring engine with action gating.

    Evaluates each command against the current operational context,
    producing a RiskLevel and GateAction. Integrates with the shell
    to block operations that would burn the engagement.

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
            "description": "Anonymous/dark web target — low monitoring",
        },
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

    def __init__(self, context: OpsecContext | None = None):
        self.context = context or OpsecContext()
        self.score_history: list[OpsecScore] = []
        self.risk_threshold = RiskLevel.HIGH

    def assess(self, command: str, extra_context: dict[str, Any] | None = None) -> OpsecScore:
        """Assess OPSEC risk for a command in the current context.

        Args:
            command: The command string to evaluate.
            extra_context: Additional context overrides.

        Returns:
            OpsecScore with risk assessment and gating decision.
        """
        cmd_base = command.split()[0].lower() if command else ""
        profile = self.COMMAND_RISK_PROFILES.get(cmd_base, {"base_noise": 3, "detects": ["unknown"], "phase": "unknown"})

        env_profile = self.ENVIRONMENT_PROFILES.get(
            self.context.target_environment, self.ENVIRONMENT_PROFILES["enterprise"]
        )

        base_noise = profile.get("base_noise", 3)
        phase_noise = self.PHASE_BASE_NOISE.get(self.context.killchain_phase, 3)
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

        score = OpsecScore(
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

    def should_allow(self, command: str) -> tuple[bool, OpsecScore]:
        """Quick gating check — returns (allowed, score).

        Args:
            command: Command string to check.

        Returns:
            Tuple of (is_allowed: bool, assessment: OpsecScore).
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
        if noise <= 2:
            return RiskLevel.LOW
        if noise <= 4:
            return RiskLevel.MEDIUM
        if noise <= 7:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

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
