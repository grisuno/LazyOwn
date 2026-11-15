"""Single-responsibility contract for the autonomous daemon's RL step reward.

Extracted verbatim (behaviour-preserving) from the ``_run_objective`` god
coroutine in ``skills/autonomous_daemon.py`` so the reward computation and the
Q-learning feedback it drives are unit-testable in isolation rather than buried
in a thousand-line loop.

Two responsibilities, one per public symbol:

``compute_step_reward``
    Map one executed step to a multi-dimensional scalar reward in
    ``[FAILURE_REWARD, MAX_REWARD]``. Finding quality, a canonical shell-session
    signal, a novelty penalty for repeated commands and a phase multiplier each
    contribute. The shell tier is decided by the one precise detector
    (``modules.atomic_exploit_bridge.shell_output_evidence``) that the engine,
    ``auto_pwn`` and every gym share, so the daemon's reward can never disagree
    with the verdict engine on whether a Metasploitable vector produced a shell.

``record_rl_feedback``
    Apply one honest temporal-difference update to the shared RL trainer: carry
    a reward exponential moving average so the pre-action state reflects recent
    performance and the post-action state reflects the step's outcome. The
    trainer is injected, so a test drives the full path without a live daemon.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

FAILURE_REWARD: float = -2.0
BASE_REWARD: float = 2.0
MAX_REWARD: float = 15.0

CREDENTIAL_TIER: float = 10.0
SHELL_TIER: float = 9.0
HASH_TIER: float = 8.0
CVE_TIER: float = 5.0
HOST_TIER: float = 3.5
KEYWORD_HOST_TIER: float = 3.0

NOVELTY_FLOOR: float = 0.3
NOVELTY_DECAY_PER_REPEAT: float = 0.2

REWARD_EMA_ALPHA: float = 0.3
REWARD_ROUND_DIGITS: int = 4
REWARD_VALUE_DIGITS: int = 2

SELECTOR_SOURCES: tuple[str, ...] = (
    "reactive",
    "cred_spray",
    "parquet",
    "bridge",
    "swan",
    "llm",
    "fallback",
)

_PHASE_MULTIPLIER: dict[str, float] = {
    "recon": 1.0,
    "enum": 1.2,
    "exploit": 1.5,
    "privesc": 1.8,
    "lateral": 1.6,
    "cred": 1.7,
    "exfil": 2.0,
}

_CREDENTIAL_KEYWORDS: tuple[str, ...] = (
    "password",
    "passwd",
    "credentials found",
    "login successful",
)
_PRIVESC_KEYWORDS: tuple[str, ...] = (
    "uid=0",
    "root shell",
    "nt authority",
    "system privilege",
)
_HASH_KEYWORDS: tuple[str, ...] = ("hash", "ntlm", "lm:", "aad3b435", "krb5tgs")
_DISCOVERY_KEYWORDS: tuple[str, ...] = ("open", "found", "200 ok", "login page")


class _Trainer(Protocol):
    """Structural contract for the injected RL trainer dependency."""

    def encode_state(self, task_type: str, engagement_phase: str, recent_reward_ema: float = 0.0) -> str: ...

    def update(
        self,
        state: str,
        action: str,
        reward: float,
        next_state: str,
        candidates: list[str],
        detection_prob: float = 0.0,
    ) -> None: ...

    def save(self) -> None: ...


@dataclass(frozen=True)
class RLStepResult:
    """Outcome of one RL feedback step.

    Attributes:
        step_reward: Raw reward granted to this step before EMA smoothing.
        reward_ema: Updated reward exponential moving average for the next step.
    """

    step_reward: float
    reward_ema: float


def _shell_evidence(output: str) -> bool:
    """Return whether the output carries a genuine interactive-shell signal."""
    try:
        from modules.atomic_exploit_bridge import shell_output_evidence

        return bool(shell_output_evidence(output))
    except Exception:
        return False


def compute_step_reward(
    output: str,
    command: str,
    phase: str,
    success: bool,
    findings: list[dict[str, Any]],
    prev_cmds: list[str],
) -> float:
    """Compute the multi-dimensional RL reward for one executed step.

    Args:
        output: Raw command output text.
        command: Command string that was executed.
        phase: Current engagement phase.
        success: Basic success flag from keyword detection.
        findings: Parsed ObsParser findings for this step.
        prev_cmds: Command names from previous steps, for the novelty penalty.

    Returns:
        Reward scalar in the range ``[FAILURE_REWARD, MAX_REWARD]``.
    """
    if not success:
        return FAILURE_REWARD

    low = output.lower()

    score = BASE_REWARD
    for finding in findings:
        ftype = finding.get("type", "")
        if ftype in ("credential",):
            score = max(score, CREDENTIAL_TIER)
        elif ftype in ("root_shell", "privesc"):
            score = max(score, SHELL_TIER)
        elif ftype in ("hash",):
            score = max(score, HASH_TIER)
        elif ftype in ("cve", "service_version"):
            score = max(score, CVE_TIER)
        elif ftype in ("host", "ip", "open_port"):
            score = max(score, HOST_TIER)

    if score < CVE_TIER:
        if any(k in low for k in _CREDENTIAL_KEYWORDS):
            score = max(score, CREDENTIAL_TIER)
        elif any(k in low for k in _PRIVESC_KEYWORDS):
            score = max(score, SHELL_TIER)
        elif any(k in low for k in _HASH_KEYWORDS):
            score = max(score, HASH_TIER)
        elif any(k in low for k in _DISCOVERY_KEYWORDS):
            score = max(score, KEYWORD_HOST_TIER)

    if _shell_evidence(output):
        score = max(score, SHELL_TIER)

    cmd_base = command.strip().split()[0] if command.strip() else ""
    repeat_count = prev_cmds.count(cmd_base)
    if repeat_count > 0:
        score = score * max(NOVELTY_FLOOR, 1.0 - repeat_count * NOVELTY_DECAY_PER_REPEAT)

    score = score * _PHASE_MULTIPLIER.get(phase, 1.0)

    return round(min(score, MAX_REWARD), REWARD_VALUE_DIGITS)


def record_rl_feedback(
    trainer: _Trainer,
    source: str,
    command: str,
    phase: str,
    output: str,
    success: bool,
    findings: list[dict[str, Any]],
    prev_cmds: list[str],
    prior_ema: float,
    detection_prob: float = 0.0,
) -> RLStepResult:
    """Apply one honest temporal-difference update for an executed step.

    The pre-action state is encoded from ``prior_ema`` (recent performance) and
    the post-action state from the freshly updated EMA, so state and next_state
    differ by the step's outcome rather than collapsing to the same key.

    Args:
        trainer: Shared RL trainer (injected for testability).
        source: Selector source that proposed the command (the RL action).
        command: Command string that was executed.
        phase: Current engagement phase.
        output: Raw command output text.
        success: Basic success flag.
        findings: Parsed findings for this step.
        prev_cmds: Previous command names, for the novelty penalty.
        prior_ema: Reward EMA carried from the previous step.
        detection_prob: Detection probability from the oracle.

    Returns:
        The step reward and the updated reward EMA for the next step.
    """
    raw_reward = compute_step_reward(output, command, phase, success, findings, prev_cmds)
    new_ema = round(REWARD_EMA_ALPHA * raw_reward + (1.0 - REWARD_EMA_ALPHA) * prior_ema, REWARD_ROUND_DIGITS)
    state = trainer.encode_state(phase, phase, prior_ema)
    next_state = trainer.encode_state(phase, phase, new_ema)
    trainer.update(
        state=state,
        action=source,
        reward=raw_reward,
        next_state=next_state,
        candidates=list(SELECTOR_SOURCES),
        detection_prob=detection_prob,
    )
    trainer.save()
    return RLStepResult(step_reward=raw_reward, reward_ema=new_ema)
