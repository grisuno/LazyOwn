"""OPSEC scoring engine — evaluates command risk before execution.

Scores commands on noise level, detection likelihood, evasion coverage,
and operational context. Integrates with the EventBus and PolicyEngine
to provide pre-execution warnings and auto-recommend mitigations.

Design (SOLID):
- Single Responsibility: OpsecScorer only scores commands.
- Open/Closed: new noise rules added via NOISE_RULES dict.
- Liskov: all scorers return OpsecScore.
- Interface Segregation: score() and suggest_mitigations() are the surface.
- Dependency Inversion: depends on abstract config dict, not concrete shell.

Usage:
    from modules.opsec_scorer import OpsecScorer

    scorer = OpsecScorer(payload, world_model)
    score = scorer.score("secretsdump", rhost="10.10.11.5")
    if score.risk_level == "critical":
        print(score.recommendation)
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("opsec_scorer")

PHASE_NOISE = {
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

@dataclass
class OpsecScore:
    command: str
    noise_score: int
    detection_risk: str
    risk_level: str
    confidence: float
    detectable_by: list[str] = field(default_factory=list)
    mitigation: list[str] = field(default_factory=list)
    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
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


class OpsecScorer:
    """Pre-execution OPSEC evaluator for LazyOwn commands.

    Scores commands on:
    - Base noise from COMMAND_NOISE mappings
    - Phase-appropriate tool usage
    - Target sensitivity (DC > workstation)
    - Evasion status (sleep, user-agent, traffic morphing)
    - Detection tool coverage (EDR, AV, SIEM)

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
        if noise <= 2:
            return "low"
        if noise <= 4:
            return "medium"
        if noise <= 7:
            return "high"
        return "critical"

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
    "OpsecScore",
    "score_command",
    "COMMAND_NOISE",
    "PHASE_NOISE",
    "MITIGATIONS",
]
