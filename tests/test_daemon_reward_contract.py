"""Contract tests for the extracted daemon RL reward module.

Guards the behaviour that used to be buried in the ``_run_objective`` god
coroutine: the multi-dimensional step reward and the honest temporal-difference
feedback (pre-action state != post-action state, reward EMA carried forward).
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "modules"))

from modules.loop.daemon_reward import (  # noqa: E402
    FAILURE_REWARD,
    SELECTOR_SOURCES,
    SHELL_TIER,
    compute_step_reward,
    record_rl_feedback,
)


class _FakeTrainer:
    """Records every encode/update/save call for assertion."""

    def __init__(self) -> None:
        self.encoded: list[tuple[str, str, float]] = []
        self.updates: list[dict] = []
        self.saved: int = 0

    def encode_state(self, task_type: str, engagement_phase: str, recent_reward_ema: float = 0.0) -> str:
        self.encoded.append((task_type, engagement_phase, recent_reward_ema))
        return f"{task_type}|{engagement_phase}|{recent_reward_ema}"

    def update(self, state, action, reward, next_state, candidates, detection_prob=0.0) -> None:
        self.updates.append(
            {
                "state": state,
                "action": action,
                "reward": reward,
                "next_state": next_state,
                "candidates": candidates,
                "detection_prob": detection_prob,
            }
        )

    def save(self) -> None:
        self.saved += 1


def test_failure_returns_failure_reward():
    assert compute_step_reward("whatever", "cmd", "exploit", False, [], []) == FAILURE_REWARD


def test_real_shell_reaches_shell_tier():
    reward = compute_step_reward("uid=0(root) gid=0(root)", "run exploit", "exploit", True, [], [])
    assert reward >= SHELL_TIER


def test_novelty_penalty_lowers_repeated_command():
    once = compute_step_reward("200 OK", "curl x", "recon", True, [], [])
    twice = compute_step_reward("200 OK", "curl x", "recon", True, [], ["curl", "curl"])
    assert twice < once


def test_record_rl_feedback_uses_distinct_states():
    trainer = _FakeTrainer()
    result = record_rl_feedback(
        trainer=trainer,
        source="llm",
        command="run exploit",
        phase="exploit",
        output="uid=0(root)",
        success=True,
        findings=[],
        prev_cmds=[],
        prior_ema=0.0,
        detection_prob=0.1,
    )
    update = trainer.updates[0]
    assert update["state"] != update["next_state"], "TD update must not collapse state and next_state"
    assert update["action"] == "llm"
    assert update["candidates"] == list(SELECTOR_SOURCES)
    assert update["detection_prob"] == 0.1
    assert trainer.saved == 1
    assert result.reward_ema > 0.0
    assert result.step_reward >= SHELL_TIER


def test_record_rl_feedback_carries_ema_forward():
    trainer = _FakeTrainer()
    first = record_rl_feedback(
        trainer=trainer,
        source="bridge",
        command="nmap t",
        phase="recon",
        output="22/tcp open",
        success=True,
        findings=[{"type": "open_port"}],
        prev_cmds=[],
        prior_ema=0.0,
        detection_prob=0.0,
    )
    second = record_rl_feedback(
        trainer=trainer,
        source="bridge",
        command="nmap t",
        phase="recon",
        output="22/tcp open",
        success=True,
        findings=[{"type": "open_port"}],
        prev_cmds=[],
        prior_ema=first.reward_ema,
        detection_prob=0.0,
    )
    assert trainer.updates[1]["state"] == trainer.encoded[2][0] + "|recon|" + str(first.reward_ema)
    assert second.reward_ema >= first.reward_ema
