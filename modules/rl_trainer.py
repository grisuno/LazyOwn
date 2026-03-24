#!/usr/bin/env python3
"""
modules/rl_trainer.py
======================
Reinforcement Learning trainer for expert routing in LazyOwn's MoE system.

Implements tabular Q-learning to improve which expert model is selected for
each (task_type, engagement_phase) state.  Over time, the policy learns to
route high-risk tasks to reasoning models and quick tasks to fast models.

Theory
------
MDP formulation:
  State  S  =  (task_type, engagement_phase, recent_success_bucket)
  Action A  =  expert_id (which model to invoke)
  Reward R  =  policy_reward - detection_penalty
  Transition: S → S' after the expert completes the task

Q-learning update (off-policy, model-free):
  Q(s, a)  ←  Q(s, a)  +  α  *  [ r  +  γ * max_a' Q(s', a')  -  Q(s, a) ]

Exploration strategy: ε-greedy with decay
  ε_t = ε_0 * decay^t   (minimum ε_min = 0.05)

Design principles
-----------------
- Single Responsibility : RL update logic only; no model invocation
- Open/Closed           : state encoding extended via StateEncoder
- Dependency Inversion  : RLTrainer depends on IStateEncoder interface
- Thread-safe           : RLock guards all Q-value mutations

Usage
-----
    from modules.rl_trainer import get_trainer

    trainer = get_trainer()

    # Before executing: select expert
    expert_id = trainer.select_action(
        state=trainer.encode_state("exploit", "exploitation", 0.7),
        candidates=["groq_powerful", "groq_deepseek_r1", "ollama_reason"],
    )

    # After executing: update Q-values
    next_state = trainer.encode_state("privesc", "post_exploitation", 0.8)
    trainer.update(
        state=current_state,
        action=expert_id,
        reward=6.0,          # from policy engine
        next_state=next_state,
        detection_prob=0.82, # from detection oracle
    )

    # Persist
    trainer.save()
"""
from __future__ import annotations

import json
import logging
import math
import os
import random
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

log = logging.getLogger("rl_trainer")

_BASE_DIR     = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"
_QVAL_FILE    = _SESSIONS_DIR / "expert_qvalues.json"
_EPS_FILE     = _SESSIONS_DIR / "rl_epsilon.json"


# ---------------------------------------------------------------------------
# Hyperparameters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RLConfig:
    """All tunable RL hyperparameters in one place."""

    learning_rate:    float = 0.10   # α — how quickly Q-values update
    discount_factor:  float = 0.90   # γ — value of future rewards
    epsilon_start:    float = 0.20   # initial exploration rate
    epsilon_min:      float = 0.05   # minimum exploration rate
    epsilon_decay:    float = 0.995  # per-update multiplicative decay
    optimistic_init:  float = 1.0    # initial Q-value (optimistic → explore all)
    detection_lambda: float = 0.50   # penalty weight for detection probability


# ---------------------------------------------------------------------------
# State encoder (Interface Segregation, Open/Closed)
# ---------------------------------------------------------------------------


class IStateEncoder(ABC):
    """Contract for encoding environment state into a hashable string key."""

    @abstractmethod
    def encode(
        self,
        task_type: str,
        engagement_phase: str,
        recent_reward_ema: float,
    ) -> str:
        """Return a string key representing the current state."""


class BucketedStateEncoder(IStateEncoder):
    """
    Encodes (task_type, phase, recent_reward_ema) into a discrete state key.

    Reward EMA is bucketed into 4 bins so that the Q-table stays finite:
        low       EMA <  0
        medium    0 <= EMA <  5
        high      5 <= EMA < 10
        excellent EMA >= 10
    """

    _REWARD_BINS: List[Tuple[float, str]] = [
        (0.0,  "low"),
        (5.0,  "medium"),
        (10.0, "high"),
    ]

    def encode(
        self,
        task_type: str,
        engagement_phase: str,
        recent_reward_ema: float,
    ) -> str:
        bucket = "excellent"
        for threshold, label in self._REWARD_BINS:
            if recent_reward_ema < threshold:
                bucket = label
                break
        return f"{task_type}:{engagement_phase}:{bucket}"


# ---------------------------------------------------------------------------
# Q-value store  (Single Responsibility: persistence only)
# ---------------------------------------------------------------------------


class QValueStore:
    """
    Persists the Q-table to sessions/expert_qvalues.json.
    Thread-safe via RLock.
    """

    def __init__(
        self,
        path: Path = _QVAL_FILE,
        optimistic_init: float = 1.0,
    ) -> None:
        self._path           = path
        self._lock           = threading.RLock()
        self._optimistic     = optimistic_init
        self._q: Dict[str, Dict[str, float]] = {}  # state_key → {expert_id → q_value}
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def get(self, state: str, action: str) -> float:
        with self._lock:
            return self._q.get(state, {}).get(action, self._optimistic)

    def set(self, state: str, action: str, value: float) -> None:
        with self._lock:
            self._q.setdefault(state, {})[action] = value

    def max_q(self, state: str, candidates: Sequence[str]) -> float:
        """Return max Q(state, a) over the given candidate actions."""
        if not candidates:
            return 0.0
        return max(self.get(state, a) for a in candidates)

    def argmax(self, state: str, candidates: Sequence[str]) -> str:
        """Return the action with highest Q(state, a)."""
        if not candidates:
            raise ValueError("Empty candidates list in argmax.")
        return max(candidates, key=lambda a: self.get(state, a))

    def save(self) -> None:
        with self._lock:
            self._persist()

    def _persist(self) -> None:
        tmp = self._path.with_suffix(".json.tmp")
        try:
            tmp.write_text(json.dumps(self._q, indent=2), encoding="utf-8")
            tmp.replace(self._path)
        except Exception as exc:
            log.warning("QValueStore._persist: %s", exc)

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            self._q = json.loads(self._path.read_text(encoding="utf-8"))
            log.debug("QValueStore: loaded %d state entries", len(self._q))
        except Exception as exc:
            log.warning("QValueStore._load: %s", exc)


# ---------------------------------------------------------------------------
# Epsilon tracker  (Single Responsibility: exploration rate management)
# ---------------------------------------------------------------------------


class EpsilonTracker:
    """Manages epsilon decay for epsilon-greedy exploration."""

    def __init__(
        self,
        start: float,
        minimum: float,
        decay: float,
        path: Path = _EPS_FILE,
    ) -> None:
        self._epsilon  = start
        self._minimum  = minimum
        self._decay    = decay
        self._path     = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    @property
    def epsilon(self) -> float:
        return self._epsilon

    def step(self) -> None:
        """Apply one decay step and persist."""
        self._epsilon = max(self._minimum, self._epsilon * self._decay)
        self._save()

    def _save(self) -> None:
        try:
            self._path.write_text(
                json.dumps({"epsilon": self._epsilon, "ts": time.time()}),
                encoding="utf-8",
            )
        except Exception:
            pass

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            loaded = float(data.get("epsilon", self._epsilon))
            if self._minimum <= loaded <= 1.0:
                self._epsilon = loaded
        except Exception:
            pass


# ---------------------------------------------------------------------------
# RLTrainer  (Liskov: substitutable for any policy that provides select/update)
# ---------------------------------------------------------------------------


class RLTrainer:
    """
    Q-learning trainer for expert routing.

    Provides:
      encode_state()    — convert environment observations to state key
      select_action()   — epsilon-greedy expert selection
      update()          — Q-learning update from observed reward
      save()            — persist Q-table and epsilon

    Detection penalty
    -----------------
    High detection probability reduces the effective reward seen by the trainer,
    encouraging selection of lower-noise experts over time:
        effective_reward = raw_reward - lambda * detection_prob * |raw_reward|
    """

    def __init__(
        self,
        config: Optional[RLConfig] = None,
        state_encoder: Optional[IStateEncoder] = None,
        q_store: Optional[QValueStore] = None,
        epsilon_tracker: Optional[EpsilonTracker] = None,
    ) -> None:
        cfg                  = config or RLConfig()
        self._cfg            = cfg
        self._encoder        = state_encoder or BucketedStateEncoder()
        self._q              = q_store or QValueStore(optimistic_init=cfg.optimistic_init)
        self._eps            = epsilon_tracker or EpsilonTracker(
            start=cfg.epsilon_start,
            minimum=cfg.epsilon_min,
            decay=cfg.epsilon_decay,
        )
        self._lock           = threading.RLock()

    # ── Public API ────────────────────────────────────────────────────────────

    def encode_state(
        self,
        task_type: str,
        engagement_phase: str,
        recent_reward_ema: float = 0.0,
    ) -> str:
        """Convert environment observations into a discrete state key."""
        return self._encoder.encode(task_type, engagement_phase, recent_reward_ema)

    def select_action(
        self,
        state: str,
        candidates: List[str],
        force_exploit: bool = False,
    ) -> str:
        """
        Epsilon-greedy expert selection.

        Parameters
        ----------
        state:          Current state key (from encode_state).
        candidates:     List of expert_id strings to choose from.
        force_exploit:  When True, always pick argmax (no exploration).

        Returns
        -------
        The selected expert_id.
        """
        if not candidates:
            raise ValueError("RLTrainer.select_action: empty candidates list.")

        with self._lock:
            eps = self._eps.epsilon

        if force_exploit or random.random() > eps:
            choice = self._q.argmax(state, candidates)
            log.debug("RL select EXPLOIT state=%s → %s (ε=%.3f)", state, choice, eps)
        else:
            choice = random.choice(candidates)
            log.debug("RL select EXPLORE state=%s → %s (ε=%.3f)", state, choice, eps)

        return choice

    def update(
        self,
        state: str,
        action: str,
        reward: float,
        next_state: str,
        candidates: List[str],
        detection_prob: float = 0.0,
    ) -> None:
        """
        Apply one Q-learning update.

        Parameters
        ----------
        state:          State at the time of action selection.
        action:         The expert_id that was selected.
        reward:         Raw reward from the policy engine.
        next_state:     State after the action completed.
        candidates:     Available experts in next_state (for max_Q calculation).
        detection_prob: Detection probability from the oracle.
        """
        # Apply detection penalty to effective reward
        effective_reward = self._penalize(reward, detection_prob)

        with self._lock:
            old_q     = self._q.get(state, action)
            max_next  = self._q.max_q(next_state, candidates)
            new_q     = old_q + self._cfg.learning_rate * (
                effective_reward
                + self._cfg.discount_factor * max_next
                - old_q
            )
            self._q.set(state, action, round(new_q, 4))
            self._eps.step()

        log.info(
            "RL update state=%s action=%s r=%.1f(eff=%.1f) Q:%.3f→%.3f ε=%.3f",
            state[:30], action, reward, effective_reward,
            old_q, new_q, self._eps.epsilon,
        )

    def best_expert_for_state(self, state: str, candidates: List[str]) -> str:
        """Return the highest Q-value expert for the given state (greedy)."""
        return self._q.argmax(state, candidates)

    def q_values_for_state(self, state: str, candidates: List[str]) -> Dict[str, float]:
        """Return {expert_id: q_value} for diagnostics."""
        return {a: self._q.get(state, a) for a in candidates}

    def save(self) -> None:
        """Persist Q-table to disk."""
        self._q.save()

    @property
    def epsilon(self) -> float:
        return self._eps.epsilon

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _penalize(self, reward: float, detection_prob: float) -> float:
        """
        Apply detection penalty:
            effective = reward - λ * detection_prob * |reward|
        High detection → effective reward is pulled toward 0.
        """
        penalty  = self._cfg.detection_lambda * detection_prob * abs(reward)
        return reward - penalty


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_trainer: Optional[RLTrainer] = None
_trainer_lock = threading.Lock()


def get_trainer(config: Optional[RLConfig] = None) -> RLTrainer:
    """Return (or create) the module-level singleton RLTrainer."""
    global _default_trainer
    if _default_trainer is None:
        with _trainer_lock:
            if _default_trainer is None:
                _default_trainer = RLTrainer(config=config)
    return _default_trainer


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse, sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="LazyOwn RL Trainer CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_sel = sub.add_parser("select", help="Select best expert for a state")
    p_sel.add_argument("task_type")
    p_sel.add_argument("phase", nargs="?", default="exploitation")
    p_sel.add_argument("--candidates", nargs="+",
                       default=["groq_fast", "groq_powerful",
                                "groq_deepseek_r1", "ollama_reason"])

    p_upd = sub.add_parser("update", help="Manual Q-learning update")
    p_upd.add_argument("task_type")
    p_upd.add_argument("action")
    p_upd.add_argument("reward", type=float)
    p_upd.add_argument("--detection", type=float, default=0.0)
    p_upd.add_argument("--phase", default="exploitation")

    p_qv = sub.add_parser("qvalues", help="Show Q-values for a state")
    p_qv.add_argument("task_type")
    p_qv.add_argument("phase", nargs="?", default="exploitation")
    p_qv.add_argument("--candidates", nargs="+",
                      default=["groq_fast", "groq_powerful",
                               "groq_deepseek_r1", "ollama_reason"])

    args = parser.parse_args()
    trainer = get_trainer()

    if args.cmd == "select":
        state  = trainer.encode_state(args.task_type, args.phase)
        choice = trainer.select_action(state, args.candidates)
        print(f"State    : {state}")
        print(f"Epsilon  : {trainer.epsilon:.3f}")
        print(f"Selected : {choice}")

    elif args.cmd == "update":
        state      = trainer.encode_state(args.task_type, args.phase)
        next_state = trainer.encode_state("privesc", "post_exploitation")
        candidates = ["groq_fast", "groq_powerful", "groq_deepseek_r1", "ollama_reason"]
        trainer.update(state, args.action, args.reward, next_state,
                       candidates, args.detection)
        trainer.save()
        print(f"Updated Q({state!r}, {args.action!r})")
        print(f"New epsilon: {trainer.epsilon:.4f}")

    elif args.cmd == "qvalues":
        state = trainer.encode_state(args.task_type, args.phase)
        qvals = trainer.q_values_for_state(state, args.candidates)
        print(f"State: {state}")
        for expert, qval in sorted(qvals.items(), key=lambda kv: -kv[1]):
            print(f"  {expert:25s}  Q = {qval:.4f}")

    else:
        parser.print_help()
