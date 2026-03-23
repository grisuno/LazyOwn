#!/usr/bin/env python3
"""
modules/detection_oracle.py
============================
Blue Team Mirror — predicts detection probability for a given action before
it is executed by the autonomous loop or a hive-mind drone.

Maps LazyOwn action categories and specific command patterns to sigma-lite
detection rules, predicted log sources, and an aggregated detection probability
score in [0.0, 1.0].

Design principles
-----------------
- Single Responsibility : detection prediction only; no command execution
- Open/Closed           : new sigma rules added via _SIGMA_RULES list only
- Liskov Substitution   : IDetectionOracle defines the contract
- Interface Segregation : IDetectionOracle exposes only assess() and probability()
- Dependency Inversion  : callers depend on IDetectionOracle, not DetectionOracle

Usage
-----
    from modules.detection_oracle import get_oracle

    oracle = get_oracle()
    assessment = oracle.assess("mimikatz", "sekurlsa::logonpasswords", "credential")
    if assessment.is_high_risk:
        print(f"High detection risk ({assessment.probability:.0%}): "
              f"{assessment.sigma_names}")
        print(assessment.recommendation)
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SigmaRule:
    """Lightweight representation of a Sigma-compatible detection rule."""

    rule_id: str
    name: str
    log_source: str           # e.g. "windows/security", "network/firewall"
    mitre_technique: str      # e.g. "T1003.001"
    base_probability: float   # inherent detection probability in [0.0, 1.0]
    keywords: Tuple[str, ...]
    category_tags: Tuple[str, ...]  # action category labels that trigger this rule


@dataclass
class DetectionAssessment:
    """Result returned by DetectionOracle.assess()."""

    command: str
    action_category: str
    probability: float               # final score in [0.0, 1.0]
    triggered_rules: List[str]       # matched rule_ids
    predicted_log_sources: List[str] # log sources where evidence would appear
    sigma_names: List[str]           # human-readable rule names
    recommendation: str              # operator-facing mitigation advice

    @property
    def is_high_risk(self) -> bool:
        """Return True when detection probability is 70% or higher."""
        return self.probability >= 0.70

    @property
    def is_critical_risk(self) -> bool:
        """Return True when detection probability is 90% or higher."""
        return self.probability >= 0.90


# ---------------------------------------------------------------------------
# Interface (I — Interface Segregation, D — Dependency Inversion)
# ---------------------------------------------------------------------------


class IDetectionOracle(ABC):
    """Read-only contract for detection probability assessment."""

    @abstractmethod
    def assess(
        self,
        command: str,
        args: str,
        action_category: str,
    ) -> DetectionAssessment:
        """Return a full DetectionAssessment for the given action."""

    @abstractmethod
    def probability(self, command: str, args: str, action_category: str) -> float:
        """Return only the probability score in [0.0, 1.0]."""


# ---------------------------------------------------------------------------
# Sigma-lite rule catalog (O — Open/Closed: extend this list, not the class)
# ---------------------------------------------------------------------------

_SIGMA_RULES: List[SigmaRule] = [
    # ── Credential Access ────────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-001",
        name="LSASS Memory Access",
        log_source="windows/security",
        mitre_technique="T1003.001",
        base_probability=0.95,
        keywords=("mimikatz", "sekurlsa", "lsass", "procdump", "pypykatz"),
        category_tags=("credential",),
    ),
    SigmaRule(
        rule_id="LAZ-002",
        name="SAM / NTDS Dump",
        log_source="windows/security",
        mitre_technique="T1003.002",
        base_probability=0.90,
        keywords=("secretsdump", "hashdump", "ntds.dit", "reg save sam"),
        category_tags=("credential",),
    ),
    SigmaRule(
        rule_id="LAZ-003",
        name="Kerberoasting / AS-REP Roasting",
        log_source="windows/security",
        mitre_technique="T1558.003",
        base_probability=0.80,
        keywords=("kerberoasting", "asrep", "kerbrute", "getuserspns"),
        category_tags=("credential", "enum"),
    ),
    # ── Lateral Movement ─────────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-004",
        name="Pass-the-Hash Activity",
        log_source="windows/security",
        mitre_technique="T1550.002",
        base_probability=0.85,
        keywords=("pass-the-hash", "wmiexec", "psexec", "smbexec", "atexec", "dcomexec"),
        category_tags=("lateral",),
    ),
    SigmaRule(
        rule_id="LAZ-005",
        name="Evil-WinRM / Remote PowerShell",
        log_source="windows/powershell",
        mitre_technique="T1021.006",
        base_probability=0.75,
        keywords=("evil-winrm", "winrm", "powershell remoting"),
        category_tags=("intrusion", "lateral"),
    ),
    # ── Privilege Escalation ─────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-006",
        name="Suspicious Sudo / SUID Execution",
        log_source="linux/syslog",
        mitre_technique="T1548.003",
        base_probability=0.65,
        keywords=("sudo -l", "suid", "gtfobins", "suid3num", "linpeas", "winpeas"),
        category_tags=("privesc",),
    ),
    SigmaRule(
        rule_id="LAZ-007",
        name="UAC Bypass / Token Impersonation",
        log_source="windows/security",
        mitre_technique="T1548.002",
        base_probability=0.82,
        keywords=("bypassuac", "getsystem", "impersonatetoken", "token duplication"),
        category_tags=("privesc",),
    ),
    # ── Exploitation ─────────────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-008",
        name="Meterpreter / Metasploit Session",
        log_source="network/ids",
        mitre_technique="T1059",
        base_probability=0.92,
        keywords=("meterpreter", "msfconsole", "msfvenom", "metasploit"),
        category_tags=("exploit", "payload"),
    ),
    SigmaRule(
        rule_id="LAZ-009",
        name="SQLMap / SQL Injection Probe",
        log_source="network/webserver",
        mitre_technique="T1190",
        base_probability=0.85,
        keywords=("sqlmap", "union select", "1=1--", "sql injection"),
        category_tags=("exploit",),
    ),
    # ── Reconnaissance ───────────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-010",
        name="Aggressive Network Scan",
        log_source="network/firewall",
        mitre_technique="T1046",
        base_probability=0.60,
        keywords=("masscan", "-sv -sc", "--script vuln", "lazynmap"),
        category_tags=("recon",),
    ),
    SigmaRule(
        rule_id="LAZ-011",
        name="LDAP / BloodHound Enumeration",
        log_source="windows/security",
        mitre_technique="T1069.002",
        base_probability=0.55,
        keywords=("ldapsearch", "ldapdomaindump", "bloodhound", "bloodhound-python"),
        category_tags=("enum", "recon"),
    ),
    # ── Payload / C2 ─────────────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-012",
        name="Reverse Shell Connection",
        log_source="network/firewall",
        mitre_technique="T1105",
        base_probability=0.87,
        keywords=("reverse_shell", "bash -i", "nc -e", "socat", "mkfifo /tmp"),
        category_tags=("payload", "intrusion"),
    ),
    SigmaRule(
        rule_id="LAZ-013",
        name="AMSI / AV Bypass Attempt",
        log_source="windows/security",
        mitre_technique="T1562.001",
        base_probability=0.88,
        keywords=("amsi", "disableav", "darkarmour", "bypass defender",
                  "add-mppreference", "set-mppreference"),
        category_tags=("payload",),
    ),
    # ── Brute Force ──────────────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-014",
        name="Password Brute Force (Multiple Failures)",
        log_source="windows/security",
        mitre_technique="T1110",
        base_probability=0.75,
        keywords=("hydra", "medusa", "crackmapexec -p", "password spray", "kerbrute"),
        category_tags=("brute_force",),
    ),
    # ── SMB Enumeration ──────────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-015",
        name="SMB Share Enumeration",
        log_source="network/smb",
        mitre_technique="T1021.002",
        base_probability=0.45,
        keywords=("smbmap", "smbclient", "enum_smb", "enum4linux", "rpcclient"),
        category_tags=("enum",),
    ),
    # ── Stealth / Evasion ────────────────────────────────────────────────────
    SigmaRule(
        rule_id="LAZ-016",
        name="Polymorphic / Obfuscated Payload",
        log_source="windows/security",
        mitre_technique="T1027",
        base_probability=0.70,
        keywords=("obfusc", "encode", "xor", "base64 -d", "iex", "invoke-expression"),
        category_tags=("payload",),
    ),
    SigmaRule(
        rule_id="LAZ-017",
        name="Process Hollowing / Injection",
        log_source="windows/sysmon",
        mitre_technique="T1055",
        base_probability=0.88,
        keywords=("process hollow", "inject", "shellcode", "virtualalloc",
                  "writeprocessmemory"),
        category_tags=("payload", "exploit"),
    ),
]

# ---------------------------------------------------------------------------
# Category-level fallback probabilities (used when no rule keyword matches)
# ---------------------------------------------------------------------------

_CATEGORY_BASE_PROBABILITY: Dict[str, float] = {
    "recon":       0.20,
    "enum":        0.30,
    "brute_force": 0.70,
    "exploit":     0.82,
    "intrusion":   0.60,
    "privesc":     0.65,
    "credential":  0.85,
    "lateral":     0.75,
    "payload":     0.80,
    "other":       0.25,
}

# ---------------------------------------------------------------------------
# Mitigation advice per risk tier
# ---------------------------------------------------------------------------

_STEALTH_ADVICE: Dict[str, str] = {
    "credential":  "Consider using DCSync over LDAP instead of direct LSASS access.",
    "lateral":     "Use native LOLBas tools (e.g. msiexec, regsvr32) to blend with "
                   "legitimate traffic.",
    "payload":     "Apply polymorphic encoding and stage payload in memory only; "
                   "avoid dropping files to disk.",
    "privesc":     "Prefer service misconfigurations over known-CVE exploits to "
                   "reduce detection rule hits.",
    "brute_force": "Use password-spraying with slow intervals (one attempt per 30 min) "
                   "to stay below lockout and SIEM thresholds.",
    "exploit":     "Fingerprint the target first and select a PoC that avoids "
                   "known AV/EDR signatures.",
    "recon":       "Limit scan rate; use passive OSINT sources before active probing.",
    "enum":        "Favour read-only LDAP and Kerberos queries over noisy SMB enumeration.",
    "intrusion":   "Use encrypted channels (SSH, HTTPS-based C2) to reduce cleartext "
                   "signatures in network logs.",
    "other":       "Review the detection rules matched and consult the evasion advisor.",
}


# ---------------------------------------------------------------------------
# DetectionOracle (L — Liskov-substitutable via IDetectionOracle)
# ---------------------------------------------------------------------------


class DetectionOracle(IDetectionOracle):
    """
    Maps a (command, args, action_category) triple to a detection probability.

    Matching algorithm
    ------------------
    1. Scan all sigma rules for keyword hits in the lowercased command+args.
    2. Include rules whose category_tags overlap with action_category.
    3. Boost matched rule probabilities by 10% when both keyword AND category hit.
    4. Aggregate using the OR-probability formula:
           P = 1 - prod(1 - effective_p_i)
    5. Clamp result to [0.0, 1.0].
    6. Fall back to _CATEGORY_BASE_PROBABILITY when no rules matched.
    """

    def __init__(self, rules: Optional[List[SigmaRule]] = None) -> None:
        self._rules: List[SigmaRule] = rules if rules is not None else _SIGMA_RULES

    # IDetectionOracle --------------------------------------------------------

    def assess(
        self,
        command: str,
        args: str,
        action_category: str,
    ) -> DetectionAssessment:
        text = (command + " " + args).lower()
        matched = self._match_rules(text, action_category)
        probability = self._aggregate_probability(matched, action_category)
        recommendation = self._build_recommendation(probability, matched, action_category)

        return DetectionAssessment(
            command=command,
            action_category=action_category,
            probability=probability,
            triggered_rules=[r.rule_id for r in matched],
            predicted_log_sources=list(dict.fromkeys(r.log_source for r in matched)),
            sigma_names=[r.name for r in matched],
            recommendation=recommendation,
        )

    def probability(self, command: str, args: str, action_category: str) -> float:
        return self.assess(command, args, action_category).probability

    # Internal helpers --------------------------------------------------------

    def _match_rules(self, text: str, action_category: str) -> List[SigmaRule]:
        """
        A rule matches when EITHER condition holds:
        - A keyword from the rule appears in the command text (direct evidence), OR
        - The action category matches AND at least one keyword was found globally.

        Category-only matches (no keyword in command text) are NOT included
        because that would assign high detection probability to low-noise commands
        that merely belong to a broadly-defined category (e.g. 'dig' as recon).
        The category tag is used exclusively to boost the probability of already-
        matched rules via _effective_probability().
        """
        matched: List[SigmaRule] = []
        for rule in self._rules:
            keyword_hit = any(kw.lower() in text for kw in rule.keywords)
            if keyword_hit:
                matched.append(rule)
        return matched

    @staticmethod
    def _effective_probability(rule: SigmaRule, action_category: str) -> float:
        """
        Return the effective probability for a matched rule.
        Applies a 10% boost when the action category also matches the rule's
        category_tags, reflecting higher confidence when both signals align.
        """
        if action_category in rule.category_tags:
            return min(1.0, rule.base_probability * 1.10)
        return rule.base_probability

    def _aggregate_probability(
        self,
        matched: List[SigmaRule],
        action_category: str,
    ) -> float:
        """
        Aggregate per-rule probabilities using the OR-probability formula so
        that each additional rule increases (rather than replaces) the total risk.
        """
        if not matched:
            return _CATEGORY_BASE_PROBABILITY.get(action_category, 0.25)
        complement = 1.0
        for rule in matched:
            complement *= 1.0 - self._effective_probability(rule, action_category)
        return round(min(1.0, 1.0 - complement), 4)

    @staticmethod
    def _build_recommendation(
        probability: float,
        matched: List[SigmaRule],
        action_category: str,
    ) -> str:
        if probability < 0.40:
            tier_label = "Low detection risk — proceed normally."
        elif probability < 0.70:
            tier_label = f"Moderate detection risk ({probability:.0%})."
        else:
            tier_label = (
                f"High detection risk ({probability:.0%}) — "
                "consider an evasive alternative."
            )

        category_advice = _STEALTH_ADVICE.get(action_category, _STEALTH_ADVICE["other"])

        if matched:
            log_sources = ", ".join(dict.fromkeys(r.log_source for r in matched))
            techniques  = ", ".join(dict.fromkeys(r.mitre_technique for r in matched))
            return (
                f"{tier_label} "
                f"Evidence predicted in: [{log_sources}]. "
                f"MITRE: {techniques}. "
                f"Stealth advice: {category_advice}"
            )

        return f"{tier_label} Stealth advice: {category_advice}"


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_oracle: Optional[DetectionOracle] = None


def get_oracle() -> DetectionOracle:
    """Return (or create) the module-level singleton DetectionOracle."""
    global _default_oracle
    if _default_oracle is None:
        _default_oracle = DetectionOracle()
    return _default_oracle


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="LazyOwn Detection Oracle — predict detection probability"
    )
    parser.add_argument("command",  help="Command name (e.g. mimikatz)")
    parser.add_argument("args",     help="Command arguments")
    parser.add_argument("category", help="Action category (e.g. credential, lateral)")
    cli_args = parser.parse_args()

    oracle     = DetectionOracle()
    assessment = oracle.assess(cli_args.command, cli_args.args, cli_args.category)

    print(f"Detection probability : {assessment.probability:.1%}")
    print(f"Risk level            : {'CRITICAL' if assessment.is_critical_risk else 'HIGH' if assessment.is_high_risk else 'LOW/MODERATE'}")
    print(f"Triggered rules       : {', '.join(assessment.triggered_rules) or '(none)'}")
    print(f"Sigma rule names      : {', '.join(assessment.sigma_names) or '(none)'}")
    print(f"Predicted log sources : {', '.join(assessment.predicted_log_sources) or '(none)'}")
    print(f"Recommendation        : {assessment.recommendation}")
    sys.exit(0)
