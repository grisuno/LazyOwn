#!/usr/bin/env python3
"""
LazyOwn Policy Engine
=====================
Four-tier cascading outcome classifier with reward-based transition learning.

Reads sessions/LazyOwn_session_report.csv to bootstrap from historical data,
classifies command outcomes through a configurable cascade:

  Tier 1  — shell exit code (fast, low confidence)
  Tier 2a — regex heuristics on output (fast, medium confidence)
  Tier 2b — local Ollama small model (slow, higher confidence)
  Tier 3  — local Ollama large model as fallback (slow, higher confidence)
  Tier 4  — interactive operator prompt (authoritative, manual)

Each completed step receives a reward scalar derived from its category and
outcome.  Transitions between states are counted in a persistent table.
The policy engine uses that table, plus a set of hand-coded override rules,
to recommend the next action category.

Usage:
    python3 skills/lazyown_policy.py bootstrap
    python3 skills/lazyown_policy.py analyze \\
        --target 10.0.0.1 --command lazynmap --args "-sV 10.0.0.1" \\
        --exit-code 0 --output "22/open 80/open"
    python3 skills/lazyown_policy.py recommend --target 10.0.0.1
    python3 skills/lazyown_policy.py report
"""

from __future__ import annotations

import abc
import argparse
import csv
import datetime
import json
import logging
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Dict, List, Mapping, Optional, Sequence, Tuple


# ─── Config ──────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Config:
    """Single source of truth for all tunable parameters and file paths."""

    base_dir: Path
    sessions_dir: Path
    session_csv: Path
    episodes_file: Path
    transitions_file: Path
    rewards_file: Path

    ollama_host: str
    ollama_port: int
    ollama_small_model: str
    ollama_large_model: str
    ollama_generate_path: str
    ollama_timeout_s: int

    min_confidence_to_accept: float
    max_output_chars_for_llm: int

    reward_table: Mapping[str, int]

    min_transition_count: int
    top_k_recommendations: int

    log_level: str

    @classmethod
    def default(cls) -> "Config":
        """Construct configuration anchored to this file's repository root."""
        base = Path(__file__).parent.parent
        sessions = base / "sessions"
        return cls(
            base_dir=base,
            sessions_dir=sessions,
            session_csv=sessions / "LazyOwn_session_report.csv",
            episodes_file=sessions / "policy_episodes.jsonl",
            transitions_file=sessions / "policy_transitions.json",
            rewards_file=sessions / "policy_rewards.json",
            ollama_host="127.0.0.1",
            ollama_port=11434,
            ollama_small_model="qwen3.5:0.8b",
            ollama_large_model="qwen3.5:0.8b",
            ollama_generate_path="/api/generate",
            ollama_timeout_s=30,
            min_confidence_to_accept=0.80,
            max_output_chars_for_llm=2000,
            reward_table=MappingProxyType(
                {
                    "recon:success": 1,
                    "enum:success": 3,
                    "brute_force:success": 5,
                    "exploit:success": 6,
                    "intrusion:success": 10,
                    "privesc:success": 15,
                    "credential:success": 8,
                    "lateral:success": 7,
                    "payload:success": 2,
                    "other:success": 1,
                    "any:fail": -2,
                    "critical:fail": -5,
                }
            ),
            min_transition_count=2,
            top_k_recommendations=3,
            log_level="INFO",
        )

    @property
    def ollama_url(self) -> str:
        """Full URL for the Ollama generate endpoint."""
        return f"http://{self.ollama_host}:{self.ollama_port}{self.ollama_generate_path}"


# ─── Enums ───────────────────────────────────────────────────────────────────


class ActionCategory(str, Enum):
    """Semantic category of a LazyOwn command execution."""

    RECON = "recon"
    ENUM = "enum"
    BRUTE_FORCE = "brute_force"
    EXPLOIT = "exploit"
    INTRUSION = "intrusion"
    PRIVESC = "privesc"
    CREDENTIAL = "credential"
    LATERAL = "lateral"
    PAYLOAD = "payload"
    OTHER = "other"


class OutcomeType(str, Enum):
    """Outcome of a classified command execution."""

    SUCCESS = "success"
    FAIL = "fail"
    UNKNOWN = "unknown"


# ─── Category keyword map ────────────────────────────────────────────────────

_CATEGORY_KEYWORDS: List[Tuple[Sequence[str], ActionCategory]] = [
    (
        [
            "lazynmap", "masscan", "lazywebscan", "gobuster", "dirb",
            "nikto", "dnsenum", "dnsrecon", "hostdiscover", "shodan", "nmap",
        ],
        ActionCategory.RECON,
    ),
    (
        [
            "enum_smb", "smbmap", "smbclient", "rpcclient", "enum4linux",
            "ldapsearch", "ldapdomaindump", "ridenum", "net rpc",
        ],
        ActionCategory.ENUM,
    ),
    (
        [
            "hydra", "medusa", "john ", "hashcat", "kerbrute",
            "crackmapexec smb", "crackmapexec -p",
        ],
        ActionCategory.BRUTE_FORCE,
    ),
    (
        ["msfconsole", "searchsploit", "sqlmap", "cve-", "exploit"],
        ActionCategory.EXPLOIT,
    ),
    (
        [
            "evil-winrm", "psexec", "wmiexec", "smbexec", "atexec",
            "dcomexec", "ssh ", "telnet ", "ftp ", "winrm",
        ],
        ActionCategory.INTRUSION,
    ),
    (
        [
            "linpeas", "winpeas", "sudo -l", "suid", "privesc",
            "getsystem", "bypassuac", "suid3num",
        ],
        ActionCategory.PRIVESC,
    ),
    (
        [
            "secretsdump", "mimikatz", "hashdump", "lsass",
            "procdump", "pypykatz", "credential",
        ],
        ActionCategory.CREDENTIAL,
    ),
    (
        [
            "lateral", "pass-the-hash", "pass-the-ticket",
            "crackmapexec", "impacket",
        ],
        ActionCategory.LATERAL,
    ),
    (
        [
            "msfvenom", "generate_reverse_shell", "generate_c_reverse_shell",
            "generate_stub", "shellcode", "payload",
        ],
        ActionCategory.PAYLOAD,
    ),
]


def infer_category(command: str, args: str = "") -> ActionCategory:
    """Return the ActionCategory best matching the command and its arguments."""
    text = (command + " " + args).lower()
    for keywords, category in _CATEGORY_KEYWORDS:
        if any(kw in text for kw in keywords):
            return category
    return ActionCategory.OTHER


# ─── Heuristic detection patterns ────────────────────────────────────────────

_SUCCESS_PATTERNS: List[Tuple[re.Pattern, ActionCategory, float]] = [
    (re.compile(r"\d+/open", re.I), ActionCategory.RECON, 0.90),
    (re.compile(r"PORT\s+STATE\s+SERVICE", re.I), ActionCategory.RECON, 0.85),
    (re.compile(r"Host is up", re.I), ActionCategory.RECON, 0.80),
    (re.compile(r"(Shar|SHARE)\w+\s", re.I), ActionCategory.ENUM, 0.85),
    (re.compile(r"(user|group|domain)\w*\s+(found|enumerat)", re.I), ActionCategory.ENUM, 0.85),
    (re.compile(r"\[\+\]\s*(user|valid|found|success|credential)", re.I), ActionCategory.ENUM, 0.82),
    (re.compile(r"(SUCCESS|Pwn3d|Login successful|Valid credential)", re.I), ActionCategory.BRUTE_FORCE, 0.90),
    (re.compile(r"Meterpreter session|Command shell session \d+ opened", re.I), ActionCategory.EXPLOIT, 0.95),
    (re.compile(r"(PS C:\\|#\s*$|\$\s*$|shell.*opened)", re.I), ActionCategory.INTRUSION, 0.88),
    (re.compile(r"(root|NT AUTHORITY|SYSTEM)\s*(#|\$|shell)", re.I), ActionCategory.PRIVESC, 0.93),
    (re.compile(r"(Administrator|NTLM hash|:.*:.*:.*:|aes256-cts)", re.I), ActionCategory.CREDENTIAL, 0.88),
]

_FAIL_PATTERNS: List[Tuple[re.Pattern, float]] = [
    (re.compile(r"(connection refused|timed?\s*out|unreachable|no route)", re.I), 0.85),
    (re.compile(r"(authentication fail|login fail|bad credential|access denied)", re.I), 0.90),
    (re.compile(r"(0 results|no hosts? up|no open port)", re.I), 0.80),
    (re.compile(r"(permission denied|operation not permitted)", re.I), 0.85),
    (re.compile(r"\[-\]\s", re.I), 0.72),
    (re.compile(r"(error|exception|traceback|fatal)", re.I), 0.68),
]


# ─── Data classes ────────────────────────────────────────────────────────────


@dataclass
class ClassificationResult:
    """Output of a single classifier tier."""

    success: bool
    confidence: float
    category: ActionCategory
    outcome: OutcomeType
    reason: str
    tier: str

    @classmethod
    def unknown(cls, tier: str) -> "ClassificationResult":
        """Produce a result indicating the tier could not classify."""
        return cls(
            success=False,
            confidence=0.0,
            category=ActionCategory.OTHER,
            outcome=OutcomeType.UNKNOWN,
            reason="classification inconclusive",
            tier=tier,
        )


@dataclass
class StepRecord:
    """A single classified command execution within an episode."""

    timestamp: str
    target: str
    command: str
    args: str
    category: str
    outcome: str
    reward: int
    confidence: float
    tier: str
    reason: str
    detection_prob: float = 0.0  # probability of detection at execution time


@dataclass
class EpisodeRecord:
    """A sequence of classified steps against a common target."""

    episode_id: str
    target: str
    steps: List[StepRecord]
    total_reward: int
    created_at: str
    updated_at: str

    def to_dict(self) -> dict:
        """Serialise to a plain dict suitable for JSON encoding."""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "EpisodeRecord":
        """Deserialise from a dict produced by to_dict."""
        raw_steps = d.pop("steps", [])
        steps = [StepRecord(**s) for s in raw_steps]
        return cls(steps=steps, **d)


# ─── Classifier interface ─────────────────────────────────────────────────────


class IOutputClassifier(abc.ABC):
    """Abstract base for all classifier tiers."""

    @abc.abstractmethod
    def classify(
        self,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
    ) -> ClassificationResult:
        """Classify the outcome of one command execution."""


# ─── Tier 1: Exit code ───────────────────────────────────────────────────────


class ExitCodeClassifier(IOutputClassifier):
    """
    Tier 1: derive outcome from the shell exit code alone.

    A zero exit code implies success but carries limited information about
    the category, hence confidence is intentionally capped below the
    acceptance threshold so richer tiers are always attempted first.
    """

    _CONFIDENCE_ZERO: float = 0.55
    _CONFIDENCE_NONZERO: float = 0.70

    def classify(
        self,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
    ) -> ClassificationResult:
        """Return a low-confidence result based solely on the exit code."""
        if exit_code is None:
            return ClassificationResult.unknown("exit_code")
        category = infer_category(command, args)
        if exit_code == 0:
            return ClassificationResult(
                success=True,
                confidence=self._CONFIDENCE_ZERO,
                category=category,
                outcome=OutcomeType.SUCCESS,
                reason=f"exit code 0",
                tier="exit_code",
            )
        return ClassificationResult(
            success=False,
            confidence=self._CONFIDENCE_NONZERO,
            category=category,
            outcome=OutcomeType.FAIL,
            reason=f"exit code {exit_code}",
            tier="exit_code",
        )


# ─── Tier 2a: Heuristic ──────────────────────────────────────────────────────


class HeuristicClassifier(IOutputClassifier):
    """
    Tier 2a: regex-based pattern matching on command output.

    Checks ordered success patterns first, then failure patterns.
    Returns UNKNOWN when no pattern exceeds a minimum match quality.
    """

    _MIN_FAIL_CONFIDENCE: float = 0.75

    def classify(
        self,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
    ) -> ClassificationResult:
        """Scan output for known success or failure signatures."""
        if not output:
            return ClassificationResult.unknown("heuristic")
        inferred = infer_category(command, args)
        for pattern, pattern_category, confidence in _SUCCESS_PATTERNS:
            if pattern.search(output):
                final_cat = pattern_category if inferred is ActionCategory.OTHER else inferred
                return ClassificationResult(
                    success=True,
                    confidence=confidence,
                    category=final_cat,
                    outcome=OutcomeType.SUCCESS,
                    reason=f"matched success pattern: {pattern.pattern[:60]}",
                    tier="heuristic",
                )
        best_fail_confidence: float = 0.0
        best_fail_pattern: str = ""
        for pattern, confidence in _FAIL_PATTERNS:
            if pattern.search(output) and confidence > best_fail_confidence:
                best_fail_confidence = confidence
                best_fail_pattern = pattern.pattern[:60]
        if best_fail_confidence >= self._MIN_FAIL_CONFIDENCE:
            return ClassificationResult(
                success=False,
                confidence=best_fail_confidence,
                category=inferred,
                outcome=OutcomeType.FAIL,
                reason=f"matched fail pattern: {best_fail_pattern}",
                tier="heuristic",
            )
        return ClassificationResult.unknown("heuristic")


# ─── Ollama base ──────────────────────────────────────────────────────────────


class _OllamaClassifierBase(IOutputClassifier):
    """Shared HTTP call and response parsing logic for Ollama-backed tiers."""

    _SYSTEM_CONTEXT = (
        "You are a security operations classifier. "
        "Analyse the shell command output and respond ONLY with valid JSON. "
        "No markdown, no code fences, no explanation outside JSON."
    )

    def __init__(self, cfg: Config, model: str, tier_name: str) -> None:
        self._url = cfg.ollama_url
        self._model = model
        self._tier = tier_name
        self._timeout = cfg.ollama_timeout_s
        self._max_chars = cfg.max_output_chars_for_llm

    def _build_prompt(
        self,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
    ) -> str:
        """Construct the classification prompt for the model."""
        ec = str(exit_code) if exit_code is not None else "unknown"
        truncated = output[: self._max_chars]
        valid_cats = "recon|enum|brute_force|intrusion|privesc|credential|lateral|payload|exploit|other"
        return (
            f"{self._SYSTEM_CONTEXT}\n\n"
            f"Shell command: {command} {args}\n"
            f"Exit code: {ec}\n"
            f"Output:\n{truncated}\n\n"
            f"Respond with exactly this JSON structure and nothing else:\n"
            f'{{"success": true_or_false, "confidence": 0.0_to_1.0, '
            f'"category": "{valid_cats}", '
            f'"reason": "one sentence"}}'
        )

    def _call_ollama(self, prompt: str) -> Optional[dict]:
        """POST a generate request to Ollama and return the parsed response dict."""
        payload = json.dumps(
            {"model": self._model, "prompt": prompt, "stream": False}
        ).encode()
        req = urllib.request.Request(
            self._url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                return json.loads(resp.read().decode())
        except (urllib.error.URLError, json.JSONDecodeError, OSError):
            return None

    def _parse_response(
        self, data: Optional[dict], fallback: ActionCategory
    ) -> Optional[ClassificationResult]:
        """Extract a ClassificationResult from the raw Ollama response."""
        if data is None:
            return None
        response_text = data.get("response", "")
        match = re.search(r"\{[^{}]+\}", response_text, re.DOTALL)
        if not match:
            return None
        try:
            parsed = json.loads(match.group())
        except json.JSONDecodeError:
            return None
        success = bool(parsed.get("success", False))
        confidence = max(0.0, min(1.0, float(parsed.get("confidence", 0.5))))
        raw_cat = parsed.get("category", "other")
        try:
            category = ActionCategory(raw_cat)
        except ValueError:
            category = fallback
        reason = str(parsed.get("reason", ""))[:200]
        outcome = OutcomeType.SUCCESS if success else OutcomeType.FAIL
        return ClassificationResult(
            success=success,
            confidence=confidence,
            category=category,
            outcome=outcome,
            reason=reason,
            tier=self._tier,
        )

    def classify(
        self,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
    ) -> ClassificationResult:
        """Send the command context to Ollama and parse the JSON reply."""
        fallback = infer_category(command, args)
        prompt = self._build_prompt(command, args, output, exit_code)
        data = self._call_ollama(prompt)
        result = self._parse_response(data, fallback)
        return result if result is not None else ClassificationResult.unknown(self._tier)


# ─── Tier 2b: Local small model ──────────────────────────────────────────────


class OllamaSmallClassifier(_OllamaClassifierBase):
    """Tier 2b: classification via the configured small local model."""

    def __init__(self, cfg: Config) -> None:
        super().__init__(cfg, cfg.ollama_small_model, "ollama_small")


# ─── Tier 3: Local large model ───────────────────────────────────────────────


class OllamaLargeClassifier(_OllamaClassifierBase):
    """Tier 3: classification via the configured large local model as fallback."""

    def __init__(self, cfg: Config) -> None:
        super().__init__(cfg, cfg.ollama_large_model, "ollama_large")


# ─── Tier 4: User interactive ─────────────────────────────────────────────────


class UserInteractiveClassifier(IOutputClassifier):
    """
    Tier 4: request manual classification from the operator.

    Used only when all automatic tiers are inconclusive and the pipeline
    was constructed with interactive=True.
    """

    def classify(
        self,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
    ) -> ClassificationResult:
        """Prompt the operator and return their authoritative verdict."""
        category = infer_category(command, args)
        print(f"\n[POLICY] Manual classification required: {command} {args[:80]}")
        print(f"         Exit code : {exit_code}")
        if output:
            print(f"         Output tail: ...{output[-400:]}")
        while True:
            answer = input("  Was this successful? [y/n/skip]: ").strip().lower()
            if answer in ("y", "yes"):
                return ClassificationResult(
                    success=True,
                    confidence=1.0,
                    category=category,
                    outcome=OutcomeType.SUCCESS,
                    reason="operator confirmed success",
                    tier="user",
                )
            if answer in ("n", "no"):
                return ClassificationResult(
                    success=False,
                    confidence=1.0,
                    category=category,
                    outcome=OutcomeType.FAIL,
                    reason="operator confirmed failure",
                    tier="user",
                )
            if answer in ("s", "skip"):
                return ClassificationResult.unknown("user")
            print("  Please enter y, n, or skip.")


# ─── Cascade classifier ───────────────────────────────────────────────────────


class CascadeClassifier:
    """
    Runs classifier tiers in order and stops at the first result whose
    confidence meets or exceeds Config.min_confidence_to_accept.

    Retains the highest-confidence partial result in case all tiers
    stay below the threshold.
    """

    def __init__(self, cfg: Config, interactive: bool = False) -> None:
        self._threshold = cfg.min_confidence_to_accept
        self._tiers: List[IOutputClassifier] = [
            ExitCodeClassifier(),
            HeuristicClassifier(),
            OllamaSmallClassifier(cfg),
            OllamaLargeClassifier(cfg),
        ]
        if interactive:
            self._tiers.append(UserInteractiveClassifier())

    def classify(
        self,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
    ) -> ClassificationResult:
        """Return the first sufficiently confident result, or the best available."""
        best = ClassificationResult.unknown("cascade")
        for tier in self._tiers:
            try:
                result = tier.classify(command, args, output, exit_code)
            except Exception:
                continue
            if result.outcome is not OutcomeType.UNKNOWN and result.confidence >= self._threshold:
                return result
            if result.confidence > best.confidence:
                best = result
        return best


# ─── Detection risk assessor ──────────────────────────────────────────────────


class DetectionRiskAssessor:
    """
    Wraps the DetectionOracle to provide detection probability for a command.

    Lazily imports modules.detection_oracle so that the oracle's sigma rule
    catalog does not load unless this class is instantiated.  This preserves
    the fast startup behaviour of lazyown_mcp.py.

    Single Responsibility: detection probability query only.
    Dependency Inversion: callers receive this via constructor injection.
    """

    _DETECTION_THRESHOLD: float = 0.70

    def __init__(self) -> None:
        self._oracle = None  # lazy-loaded on first call

    def _get_oracle(self):
        if self._oracle is None:
            try:
                import sys as _sys
                _base = Path(__file__).parent.parent
                if str(_base) not in _sys.path:
                    _sys.path.insert(0, str(_base))
                from modules.detection_oracle import get_oracle  # noqa: PLC0415
                self._oracle = get_oracle()
            except Exception:
                self._oracle = None
        return self._oracle

    def assess_probability(self, command: str, args: str, category: str) -> float:
        """
        Return detection probability in [0.0, 1.0].
        Returns 0.0 when the oracle is unavailable (fail-open for rewards).
        """
        oracle = self._get_oracle()
        if oracle is None:
            return 0.0
        try:
            return oracle.probability(command, args, category)
        except Exception:
            return 0.0

    def is_high_risk(self, command: str, args: str, category: str) -> bool:
        """Return True when detection probability meets or exceeds the threshold."""
        return self.assess_probability(command, args, category) >= self._DETECTION_THRESHOLD


# ─── Reward calculator ────────────────────────────────────────────────────────


class RewardCalculator:
    """
    Converts (ActionCategory, OutcomeType) pairs to scalar reward values,
    optionally applying a detection-risk penalty when a DetectionRiskAssessor
    is provided.

    Detection penalty rule
    ----------------------
    When detection probability >= 0.70 (high risk), the reward for a successful
    action is zeroed out.  This forces the policy engine to prefer lower-noise
    paths over high-value but high-visibility actions.

    Failure rewards are unaffected by detection probability — the agent must
    still learn that failed actions carry a negative signal.
    """

    _HIGH_VALUE_CATEGORIES = frozenset(
        {ActionCategory.INTRUSION, ActionCategory.PRIVESC, ActionCategory.CREDENTIAL}
    )
    _DETECTION_ZERO_THRESHOLD: float = 0.70

    def __init__(
        self,
        cfg: Config,
        risk_assessor: Optional[DetectionRiskAssessor] = None,
    ) -> None:
        self._table                = cfg.reward_table
        self._fail_reward          = self._table["any:fail"]
        self._critical_fail_reward = self._table["critical:fail"]
        self._risk_assessor        = risk_assessor

    def calculate(self, category: ActionCategory, outcome: OutcomeType) -> int:
        """
        Return the reward integer for the given (category, outcome) pair.
        Detection risk is NOT applied here — use calculate_with_detection()
        when command context is available.
        """
        if outcome is OutcomeType.SUCCESS:
            key = f"{category.value}:success"
            return self._table.get(key, self._table.get("other:success", 1))
        if outcome is OutcomeType.FAIL:
            if category in self._HIGH_VALUE_CATEGORIES:
                return self._critical_fail_reward
            return self._fail_reward
        return 0

    def calculate_with_detection(
        self,
        category: ActionCategory,
        outcome: OutcomeType,
        command: str,
        args: str,
    ) -> Tuple[int, float]:
        """
        Return (reward, detection_probability) for the given execution.

        When detection_probability >= 0.70 and outcome is SUCCESS, the reward
        is forced to zero to discourage noisy techniques.  This implements the
        detection-aware reward shaping described in the architecture.

        Parameters
        ----------
        category:   ActionCategory of the command
        outcome:    OutcomeType of the execution
        command:    The command name (for detection oracle lookup)
        args:       Command arguments (for detection oracle lookup)

        Returns
        -------
        (reward: int, detection_prob: float)
        """
        base_reward = self.calculate(category, outcome)
        detection_prob = 0.0

        if self._risk_assessor is not None and outcome is OutcomeType.SUCCESS:
            detection_prob = self._risk_assessor.assess_probability(
                command, args, category.value
            )
            if detection_prob >= self._DETECTION_ZERO_THRESHOLD:
                logging.getLogger(__name__).info(
                    "Detection risk %.0f%% for %s — zeroing reward (was %+d)",
                    detection_prob * 100,
                    command,
                    base_reward,
                )
                base_reward = 0

        return base_reward, detection_prob


# ─── CSV session reader ───────────────────────────────────────────────────────


class CSVSessionReader:
    """
    Reads LazyOwn_session_report.csv and converts each row to a StepRecord
    using heuristic classification (no output or exit code available for
    historical data).
    """

    def __init__(self, cfg: Config) -> None:
        self._path = cfg.session_csv
        self._heuristic = HeuristicClassifier()
        self._reward_calc = RewardCalculator(cfg)

    def read(self) -> List[StepRecord]:
        """Parse the CSV and return all classifiable rows as StepRecord instances."""
        if not self._path.exists():
            return []
        steps: List[StepRecord] = []
        with self._path.open(newline="", encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                command = (row.get("command") or "").strip()
                args = (row.get("args") or "").strip()
                if not command:
                    continue
                result = self._heuristic.classify(command, args, args, exit_code=None)
                if result.outcome is OutcomeType.UNKNOWN:
                    category = infer_category(command, args)
                    result = ClassificationResult(
                        success=True,
                        confidence=0.40,
                        category=category,
                        outcome=OutcomeType.SUCCESS,
                        reason="historical bootstrap — output unavailable",
                        tier="bootstrap",
                    )
                reward = self._reward_calc.calculate(result.category, result.outcome)
                steps.append(
                    StepRecord(
                        timestamp=(row.get("start") or ""),
                        target=(row.get("destination_ip") or ""),
                        command=command,
                        args=args,
                        category=result.category.value,
                        outcome=result.outcome.value,
                        reward=reward,
                        confidence=result.confidence,
                        tier=result.tier,
                        reason=result.reason,
                    )
                )
        return steps


# ─── Episode store ────────────────────────────────────────────────────────────


class IEpisodeStore(abc.ABC):
    """Abstract persistence layer for episode records."""

    @abc.abstractmethod
    def append_step(self, step: StepRecord) -> None:
        """Add a step to the episode for its target, creating the episode if needed."""

    @abc.abstractmethod
    def load_all(self) -> List[EpisodeRecord]:
        """Load every stored episode."""

    @abc.abstractmethod
    def get_episode(self, target: str) -> Optional[EpisodeRecord]:
        """Return the episode for the given target, or None."""


class JSONLEpisodeStore(IEpisodeStore):
    """
    Persists each episode as one JSON line in a .jsonl file keyed by target.

    The file is read and rewritten on every mutating call.  This is acceptable
    given the expected cardinality of targets in a pentest engagement.
    """

    def __init__(self, cfg: Config) -> None:
        self._path = cfg.episodes_file
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def append_step(self, step: StepRecord) -> None:
        """Upsert the step into its target's episode and persist."""
        episodes: Dict[str, EpisodeRecord] = {ep.target: ep for ep in self.load_all()}
        target = step.target or "unknown"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if target not in episodes:
            episodes[target] = EpisodeRecord(
                episode_id=str(uuid.uuid4()),
                target=target,
                steps=[],
                total_reward=0,
                created_at=now,
                updated_at=now,
            )
        ep = episodes[target]
        ep.steps.append(step)
        ep.total_reward += step.reward
        ep.updated_at = now
        self._write_all(list(episodes.values()))

    def load_all(self) -> List[EpisodeRecord]:
        """Deserialise all episodes from the .jsonl file."""
        if not self._path.exists():
            return []
        records: List[EpisodeRecord] = []
        with self._path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(EpisodeRecord.from_dict(json.loads(line)))
                except (json.JSONDecodeError, TypeError, KeyError):
                    continue
        return records

    def get_episode(self, target: str) -> Optional[EpisodeRecord]:
        """Return the episode for target, or None if not found."""
        for ep in self.load_all():
            if ep.target == target:
                return ep
        return None

    def _write_all(self, episodes: List[EpisodeRecord]) -> None:
        with self._path.open("w", encoding="utf-8") as fh:
            for ep in episodes:
                fh.write(json.dumps(ep.to_dict()) + "\n")


# ─── Transition table ──────────────────────────────────────────────────────────


class TransitionTable:
    """
    Persistent frequency table of observed (from_state → next_category) transitions.

    State strings are formatted as "category:outcome" (e.g. "recon:success").
    The table is written to disk after every update.
    """

    def __init__(self, cfg: Config) -> None:
        self._path = cfg.transitions_file
        self._min_count = cfg.min_transition_count
        self._data: Dict[str, Dict[str, Dict[str, int]]] = {}
        self._load()

    def record(self, from_state: str, to_category: str, outcome: str) -> None:
        """Increment the counter for the given transition and persist."""
        if from_state not in self._data:
            self._data[from_state] = {}
        if to_category not in self._data[from_state]:
            self._data[from_state][to_category] = {"success": 0, "fail": 0, "unknown": 0}
        bucket = outcome if outcome in ("success", "fail") else "unknown"
        self._data[from_state][to_category][bucket] += 1
        self._save()

    def query(self, from_state: str) -> List[Tuple[str, float, int]]:
        """
        Return (next_category, success_rate, total_count) tuples for the given
        from_state, filtered by min_transition_count and sorted by success rate
        descending.

        Always reloads from disk so that external edits (policy_transitions.json)
        and concurrent writes from pipeline._transitions take effect immediately.
        """
        self._load()
        if from_state not in self._data:
            return []
        results: List[Tuple[str, float, int]] = []
        for category, counts in self._data[from_state].items():
            total = counts["success"] + counts["fail"] + counts["unknown"]
            if total < self._min_count:
                continue
            rate = counts["success"] / total if total else 0.0
            results.append((category, rate, total))
        return sorted(results, key=lambda t: (-t[1], -t[2]))

    def _load(self) -> None:
        if self._path.exists():
            try:
                with self._path.open(encoding="utf-8") as fh:
                    self._data = json.load(fh)
            except (json.JSONDecodeError, OSError):
                self._data = {}

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as fh:
            json.dump(self._data, fh, indent=2)


# ─── Override rules ───────────────────────────────────────────────────────────


@dataclass(frozen=True)
class OverrideRule:
    """
    A hand-coded transition override that fires when recent session history
    matches a specific sequence of states.
    """

    name: str
    trigger_sequence: Tuple[str, ...]
    inject_category: str
    reason: str
    priority: int


_OVERRIDE_RULES: List[OverrideRule] = [
    OverrideRule(
        name="enum_before_intrusion",
        trigger_sequence=("recon:success", "intrusion:fail"),
        inject_category="enum",
        reason="Intrusion failed directly after recon — enumeration step was skipped.",
        priority=10,
    ),
    OverrideRule(
        name="brute_after_enum_fail",
        trigger_sequence=("enum:success", "intrusion:fail"),
        inject_category="brute_force",
        reason="Intrusion failed after enum — valid credentials may still be required.",
        priority=9,
    ),
    OverrideRule(
        name="privesc_after_intrusion",
        trigger_sequence=("intrusion:success",),
        inject_category="privesc",
        reason="Intrusion succeeded — check for local privilege escalation paths.",
        priority=8,
    ),
    OverrideRule(
        name="credential_after_privesc",
        trigger_sequence=("privesc:success",),
        inject_category="credential",
        reason="Elevated privileges obtained — dump credentials for lateral movement.",
        priority=7,
    ),
    OverrideRule(
        name="lateral_after_credential",
        trigger_sequence=("credential:success",),
        inject_category="lateral",
        reason="Credentials dumped — attempt lateral movement to adjacent hosts.",
        priority=6,
    ),
]


# ─── Policy engine ────────────────────────────────────────────────────────────


class PolicyEngine:
    """
    Produces a ranked list of recommended next action categories for a target.

    Override rules are evaluated first against a sliding window of recent states
    and prepended to the list derived from transition table frequencies.
    """

    _STATE_WINDOW: int = 5

    def __init__(self, cfg: Config, transitions: TransitionTable) -> None:
        self._top_k = cfg.top_k_recommendations
        self._transitions = transitions

    def recommend(self, recent_steps: List[StepRecord]) -> List[Dict]:
        """
        Return up to top_k dicts with keys: category, reason, confidence, source.
        """
        if not recent_steps:
            return [
                {
                    "category": "recon",
                    "reason": "No history for target — begin with reconnaissance.",
                    "confidence": 1.0,
                    "source": "default",
                }
            ]
        recent_states = [
            f"{s.category}:{s.outcome}" for s in recent_steps[-self._STATE_WINDOW :]
        ]
        current_state = recent_states[-1]
        injected = self._apply_overrides(recent_states)
        data_driven = self._transitions.query(current_state)

        recommendations: List[Dict] = []
        seen: set = set()

        for rule_cat, rule_reason, rule_priority in injected:
            if rule_cat not in seen:
                seen.add(rule_cat)
                confidence = min(0.95, 0.70 + rule_priority * 0.02)
                recommendations.append(
                    {
                        "category": rule_cat,
                        "reason": rule_reason,
                        "confidence": confidence,
                        "source": "override_rule",
                    }
                )

        for category, rate, count in data_driven:
            if category not in seen:
                seen.add(category)
                recommendations.append(
                    {
                        "category": category,
                        "reason": (
                            f"Observed {count}x after '{current_state}' "
                            f"with {rate:.0%} success rate."
                        ),
                        "confidence": rate,
                        "source": "transition_table",
                    }
                )

        if not recommendations:
            recommendations.append(self._default_fallback(current_state))

        return recommendations[: self._top_k]

    def _apply_overrides(
        self, recent_states: List[str]
    ) -> List[Tuple[str, str, int]]:
        """Return (category, reason, priority) for every triggered override rule."""
        matched: List[Tuple[str, str, int]] = []
        for rule in sorted(_OVERRIDE_RULES, key=lambda r: -r.priority):
            window = tuple(recent_states[-len(rule.trigger_sequence) :])
            if window == rule.trigger_sequence:
                matched.append((rule.inject_category, rule.reason, rule.priority))
        return matched

    def _default_fallback(self, current_state: str) -> Dict:
        """Fall back to the standard kill-chain order when no data is available."""
        _chain: Dict[str, str] = {
            "recon": "enum",
            "enum": "brute_force",
            "brute_force": "intrusion",
            "intrusion": "privesc",
            "privesc": "credential",
            "credential": "lateral",
        }
        current_cat = current_state.split(":")[0]
        next_cat = _chain.get(current_cat, "recon")
        return {
            "category": next_cat,
            "reason": (
                f"No transition data for '{current_state}' — "
                "following default kill-chain order."
            ),
            "confidence": 0.40,
            "source": "default_chain",
        }


# ─── Session pipeline ──────────────────────────────────────────────────────────


class SessionClassificationPipeline:
    """
    Main entry point for processing a completed command execution.

    Runs the cascade classifier, computes the reward, persists the step,
    and updates the transition table with the observed state change.
    """

    def __init__(self, cfg: Config, interactive: bool = False) -> None:
        self._classifier  = CascadeClassifier(cfg, interactive=interactive)
        risk_assessor     = DetectionRiskAssessor()
        self._reward_calc = RewardCalculator(cfg, risk_assessor=risk_assessor)
        self._store       = JSONLEpisodeStore(cfg)
        self._transitions = TransitionTable(cfg)
        self._logger      = logging.getLogger(self.__class__.__name__)

    def process(
        self,
        target: str,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
        timestamp: Optional[str] = None,
    ) -> StepRecord:
        """Classify, reward, store, and return a StepRecord for the given execution."""
        result = self._classifier.classify(command, args, output, exit_code)
        reward, detection_prob = self._reward_calc.calculate_with_detection(
            result.category, result.outcome, command, args
        )
        step = StepRecord(
            timestamp=timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat(),
            target=target,
            command=command,
            args=args,
            category=result.category.value,
            outcome=result.outcome.value,
            reward=reward,
            confidence=result.confidence,
            tier=result.tier,
            reason=result.reason,
            detection_prob=detection_prob,
        )
        existing = self._store.get_episode(target)
        prev_state: Optional[str] = None
        if existing and existing.steps:
            last = existing.steps[-1]
            prev_state = f"{last.category}:{last.outcome}"
        self._store.append_step(step)
        if prev_state:
            self._transitions.record(prev_state, step.category, step.outcome)
        self._logger.info(
            "Classified %s %s -> %s/%s (reward=%+d conf=%.2f tier=%s detect=%.0f%%)",
            command,
            args[:40],
            result.category.value,
            result.outcome.value,
            reward,
            result.confidence,
            result.tier,
            detection_prob * 100,
        )
        return step


# ─── Policy advisor ───────────────────────────────────────────────────────────


class PolicyAdvisor:
    """
    Entry point for querying next-action recommendations for a target.
    """

    def __init__(self, cfg: Config) -> None:
        self._store = JSONLEpisodeStore(cfg)
        self._transitions = TransitionTable(cfg)
        self._engine = PolicyEngine(cfg, self._transitions)

    def advise(self, target: str) -> List[Dict]:
        """Return the policy engine's recommendations for the given target."""
        episode = self._store.get_episode(target)
        return self._engine.recommend(episode.steps if episode else [])

    def episode_summary(self, target: str) -> Optional[Dict]:
        """Return a high-level summary dict for the target's episode."""
        episode = self._store.get_episode(target)
        if not episode:
            return None
        last_state = (
            f"{episode.steps[-1].category}:{episode.steps[-1].outcome}"
            if episode.steps
            else "none"
        )
        return {
            "target": episode.target,
            "total_reward": episode.total_reward,
            "steps": len(episode.steps),
            "last_state": last_state,
        }


# ─── Public integration facade ────────────────────────────────────────────────


class LazyOwnPolicyIntegration:
    """
    Convenience facade for use by lazyown_mcp.py or any other LazyOwn component.

    Provides a stable two-method API so callers remain decoupled from the
    internal cascade and storage details.
    """

    def __init__(self, cfg: Optional[Config] = None) -> None:
        resolved = cfg if cfg is not None else Config.default()
        self._pipeline = SessionClassificationPipeline(resolved)
        self._advisor = PolicyAdvisor(resolved)

    def on_command_complete(
        self,
        target: str,
        command: str,
        args: str,
        output: str,
        exit_code: Optional[int],
    ) -> StepRecord:
        """Classify a completed command and record it in the episode store."""
        return self._pipeline.process(target, command, args, output, exit_code)

    def get_recommendations(self, target: str) -> List[Dict]:
        """Return ranked next-action recommendations for the target."""
        return self._advisor.advise(target)


# ─── History bootstrapper ─────────────────────────────────────────────────────


class HistoryBootstrapper:
    """
    One-shot importer that reads LazyOwn_session_report.csv and populates
    the episode store and transition table from historical session data.
    """

    def __init__(self, cfg: Config) -> None:
        self._reader = CSVSessionReader(cfg)
        self._store = JSONLEpisodeStore(cfg)
        self._transitions = TransitionTable(cfg)
        self._logger = logging.getLogger(self.__class__.__name__)

    def run(self) -> int:
        """Process all CSV rows and return the total number of steps indexed."""
        steps = self._reader.read()
        if not steps:
            self._logger.warning("Session CSV not found or contains no rows.")
            return 0
        grouped: Dict[str, List[StepRecord]] = {}
        for step in steps:
            grouped.setdefault(step.target or "unknown", []).append(step)
        for target_steps in grouped.values():
            for step in target_steps:
                self._store.append_step(step)
        for target_steps in grouped.values():
            for i in range(1, len(target_steps)):
                prev = target_steps[i - 1]
                curr = target_steps[i]
                from_state = f"{prev.category}:{prev.outcome}"
                self._transitions.record(from_state, curr.category, curr.outcome)
        total = len(steps)
        self._logger.info(
            "Bootstrap complete: %d steps across %d targets.", total, len(grouped)
        )
        return total


# ─── CLI ──────────────────────────────────────────────────────────────────────


def _setup_logging(cfg: Config) -> None:
    logging.basicConfig(
        level=getattr(logging, cfg.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )


def _cmd_bootstrap(cfg: Config, _args: argparse.Namespace) -> int:
    """CLI handler: index session history into the episode and transition stores."""
    count = HistoryBootstrapper(cfg).run()
    print(f"Bootstrap complete: {count} steps indexed.")
    return 0


def _cmd_analyze(cfg: Config, args: argparse.Namespace) -> int:
    """CLI handler: classify one command execution and print the result."""
    pipeline = SessionClassificationPipeline(cfg, interactive=args.interactive)
    step = pipeline.process(
        target=args.target,
        command=args.command,
        args=args.args,
        output=args.output,
        exit_code=args.exit_code,
    )
    print(json.dumps(asdict(step), indent=2))
    return 0


def _cmd_recommend(cfg: Config, args: argparse.Namespace) -> int:
    """CLI handler: print next-action recommendations for a target."""
    advisor = PolicyAdvisor(cfg)
    summary = advisor.episode_summary(args.target)
    if summary:
        print(
            f"Episode  target={summary['target']}  "
            f"steps={summary['steps']}  "
            f"total_reward={summary['total_reward']:+d}  "
            f"last={summary['last_state']}"
        )
    recs = advisor.advise(args.target)
    print("\nRecommendations:")
    for i, rec in enumerate(recs, 1):
        bar = "█" * int(rec["confidence"] * 10)
        print(f"  {i}. [{bar:<10}] {rec['confidence']:.0%}  {rec['category']}")
        print(f"       {rec['reason']}")
        print(f"       source: {rec['source']}")
    return 0


def _cmd_report(cfg: Config, _args: argparse.Namespace) -> int:
    """CLI handler: print a summary table of all episodes."""
    episodes = JSONLEpisodeStore(cfg).load_all()
    if not episodes:
        print("No episodes found. Run 'bootstrap' first.")
        return 0
    col_target = 22
    col_steps = 7
    col_reward = 9
    col_state = 32
    header = (
        f"{'Target':<{col_target}} {'Steps':>{col_steps}} "
        f"{'Reward':>{col_reward}} {'Last State':<{col_state}}"
    )
    print(header)
    print("-" * len(header))
    for ep in sorted(episodes, key=lambda e: -e.total_reward):
        last = (
            f"{ep.steps[-1].category}:{ep.steps[-1].outcome}"
            if ep.steps
            else "—"
        )
        print(
            f"{ep.target:<{col_target}} "
            f"{len(ep.steps):>{col_steps}} "
            f"{ep.total_reward:>+{col_reward}} "
            f"{last:<{col_state}}"
        )
    return 0


def main() -> int:
    """Parse CLI arguments and dispatch to the appropriate command handler."""
    cfg = Config.default()
    _setup_logging(cfg)

    parser = argparse.ArgumentParser(
        description="LazyOwn Policy Engine — classify outcomes, learn transitions, recommend actions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    sub.add_parser(
        "bootstrap",
        help="Index sessions/LazyOwn_session_report.csv into the episode and transition stores.",
    )

    p_analyze = sub.add_parser(
        "analyze",
        help="Classify one command execution result and record it.",
    )
    p_analyze.add_argument("--target", required=True, help="Destination IP or hostname.")
    p_analyze.add_argument("--command", required=True, help="LazyOwn command name.")
    p_analyze.add_argument("--args", default="", help="Command arguments.")
    p_analyze.add_argument("--output", default="", help="Shell output to classify.")
    p_analyze.add_argument(
        "--exit-code", type=int, default=None, dest="exit_code", help="Shell exit code."
    )
    p_analyze.add_argument(
        "--interactive",
        action="store_true",
        help="Ask operator if all automatic tiers are inconclusive.",
    )

    p_rec = sub.add_parser(
        "recommend",
        help="Print next-action recommendations for a target.",
    )
    p_rec.add_argument("--target", required=True, help="Target IP or hostname.")

    sub.add_parser("report", help="Print a summary table of all stored episodes.")

    args = parser.parse_args()
    dispatch = {
        "bootstrap": _cmd_bootstrap,
        "analyze": _cmd_analyze,
        "recommend": _cmd_recommend,
        "report": _cmd_report,
    }
    return dispatch[args.subcommand](cfg, args)


if __name__ == "__main__":
    sys.exit(main())
