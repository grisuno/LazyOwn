#!/usr/bin/env python3
"""
modules/moe_router.py
======================
Mixture-of-Experts (MoE) Router for LazyOwn.

Routes penetration-testing tasks to the most capable available LLM expert
based on task type, learned performance history, and detection risk.

Architecture
------------
                     task_type + goal
                           |
                     MoERouter.route()
                     /       |       \\
           groq_fast  groq_powerful  ollama_reason  ...
                     \\       |       /
               ExpertPerformanceStore (JSON)
                           |
                    SoftmaxSelector
                (temperature-scaled softmax
                 over RL-adjusted weights)

Design principles
-----------------
- Single Responsibility : each class owns one concept
- Open/Closed           : new experts added to _DEFAULT_EXPERTS list only
- Liskov Substitution   : IExpertSelector defines the routing contract
- Interface Segregation : separate read/write interfaces for performance store
- Dependency Inversion  : MoERouter depends on IExpertSelector, not on concrete impl

Expert selection algorithm
--------------------------
1. Filter experts whose capabilities include the requested task_type.
2. Retrieve per-(expert, task_type) performance score from store.
3. Compute adjusted_weight = base_weight * (1 + performance_bonus).
4. Apply temperature-scaled softmax to get selection probabilities.
5. Sample from distribution (or return argmax for deterministic mode).

Usage
-----
    from modules.moe_router import get_router

    router = get_router()
    expert = router.route("exploit", "Find a shell on Apache 2.4.49")
    print(expert.expert_id, expert.backend, expert.model)

    # Ensemble: top-3 experts for a critical decision
    experts = router.ensemble("credential", "Dump hashes from DC", n=3)

    # Record outcome after execution
    router.record_outcome("groq_powerful", "exploit", reward=6, detection_prob=0.82)
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

log = logging.getLogger("moe_router")

_BASE_DIR          = Path(__file__).resolve().parent.parent
_SESSIONS_DIR      = _BASE_DIR / "sessions"
_PERF_FILE         = _SESSIONS_DIR / "expert_performance.json"
_AVAIL_CACHE_TTL_S = 120  # re-check availability every 2 minutes


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


@dataclass
class ExpertProfile:
    """Static description of a single expert model."""

    expert_id:   str
    backend:     str            # groq | ollama
    model:       str
    capabilities: List[str]    # task types this expert handles
    base_weight: float         # prior weight in [0.0, 1.0]
    cost_tier:   int           # 0=free/local, 1=cheap, 2=normal, 3=expensive
    latency_ms:  int           # expected median latency
    description: str           = ""

    @property
    def is_local(self) -> bool:
        return self.backend == "ollama"


@dataclass
class ExpertPerformance:
    """Mutable per-(expert_id, task_type) performance record."""

    expert_id:          str
    task_type:          str
    total_calls:        int   = 0
    total_reward:       float = 0.0
    avg_reward:         float = 0.0
    avg_detection_prob: float = 0.0
    ema_reward:         float = 0.0   # exponential moving average
    last_updated:       str   = ""

    _EMA_ALPHA: float = 0.3           # EMA smoothing factor

    def update(self, reward: float, detection_prob: float) -> None:
        self.total_calls        += 1
        self.total_reward       += reward
        self.avg_reward          = self.total_reward / self.total_calls
        # Detection-penalized EMA: high detection → lower effective reward
        effective = reward * (1.0 - min(1.0, detection_prob))
        if self.ema_reward == 0.0:
            self.ema_reward = effective
        else:
            self.ema_reward = (
                self._EMA_ALPHA * effective
                + (1.0 - self._EMA_ALPHA) * self.ema_reward
            )
        n = self.total_calls
        self.avg_detection_prob = (
            self.avg_detection_prob * (n - 1) / n + detection_prob / n
        )
        self.last_updated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ---------------------------------------------------------------------------
# Default expert registry
# Extend this list to add new experts — no other code changes required.
# ---------------------------------------------------------------------------

_DEFAULT_EXPERTS: List[ExpertProfile] = [
    ExpertProfile(
        expert_id="groq_fast",
        backend="groq",
        model="llama-3.1-8b-instant",
        capabilities=["recon", "enum", "other", "brute_force"],
        base_weight=0.70,
        cost_tier=1,
        latency_ms=500,
        description="Fast Groq model for quick recon and enumeration decisions.",
    ),
    ExpertProfile(
        expert_id="groq_powerful",
        backend="groq",
        model="llama-3.3-70b-versatile",
        capabilities=[
            "exploit", "credential", "lateral", "intrusion",
            "privesc", "enum", "brute_force", "payload",
        ],
        base_weight=0.82,
        cost_tier=2,
        latency_ms=2000,
        description="Powerful Groq model for complex attack decisions and full kill-chain.",
    ),
    ExpertProfile(
        expert_id="groq_deepseek_r1",
        backend="groq",
        model="deepseek-r1-distill-llama-70b",
        capabilities=["exploit", "privesc", "credential", "lateral"],
        base_weight=0.78,
        cost_tier=2,
        latency_ms=3500,
        description=(
            "DeepSeek R1 reasoning model via Groq for multi-step exploit analysis, "
            "CVE research, and privilege escalation path planning."
        ),
    ),
    ExpertProfile(
        expert_id="ollama_reason",
        backend="ollama",
        model=os.environ.get("OLLAMA_DEFAULT_MODEL", "deepseek-r1:1.5b"),
        capabilities=["exploit", "privesc", "analyze", "credential", "payload"],
        base_weight=0.55,
        cost_tier=0,
        latency_ms=8000,
        description=(
            "Local reasoning model (Ollama). Privacy-safe, offline-capable. "
            "Good for detailed step-by-step exploit reasoning."
        ),
    ),
    ExpertProfile(
        expert_id="groq_gemma",
        backend="groq",
        model="gemma2-9b-it",
        capabilities=["analyze", "report", "enum"],
        base_weight=0.65,
        cost_tier=1,
        latency_ms=800,
        description=(
            "Gemma 2 9B for output analysis, log parsing, and report synthesis."
        ),
    ),
]


# ---------------------------------------------------------------------------
# Interface (Interface Segregation)
# ---------------------------------------------------------------------------


class IExpertSelector(ABC):
    """Contract for expert selection strategies."""

    @abstractmethod
    def select(
        self,
        candidates: List[ExpertProfile],
        task_type: str,
        performance_store: "ExpertPerformanceStore",
        deterministic: bool = False,
    ) -> ExpertProfile:
        """Return the selected expert from candidates."""


# ---------------------------------------------------------------------------
# Performance store  (Single Responsibility: persistence only)
# ---------------------------------------------------------------------------


class ExpertPerformanceStore:
    """
    Persists per-(expert_id, task_type) performance records to JSON.

    Thread-safe via RLock.
    """

    def __init__(self, path: Path = _PERF_FILE) -> None:
        self._path  = path
        self._lock  = threading.RLock()
        self._data: Dict[str, ExpertPerformance] = {}
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    # ── Key helper ────────────────────────────────────────────────────────────

    @staticmethod
    def _key(expert_id: str, task_type: str) -> str:
        return f"{expert_id}::{task_type}"

    # ── Write ─────────────────────────────────────────────────────────────────

    def record(
        self,
        expert_id: str,
        task_type: str,
        reward: float,
        detection_prob: float,
    ) -> ExpertPerformance:
        """Update performance for (expert, task_type) and persist."""
        key = self._key(expert_id, task_type)
        with self._lock:
            if key not in self._data:
                self._data[key] = ExpertPerformance(
                    expert_id=expert_id, task_type=task_type
                )
            self._data[key].update(reward, detection_prob)
            self._save()
        return self._data[key]

    # ── Read ──────────────────────────────────────────────────────────────────

    def get(self, expert_id: str, task_type: str) -> Optional[ExpertPerformance]:
        key = self._key(expert_id, task_type)
        with self._lock:
            return self._data.get(key)

    def all_for_task(self, task_type: str) -> List[ExpertPerformance]:
        with self._lock:
            return [v for v in self._data.values() if v.task_type == task_type]

    def performance_bonus(self, expert_id: str, task_type: str) -> float:
        """
        Return a bonus scalar in [-0.3, +0.5] based on EMA reward history.
        Positive for above-average performance, negative for below-average.
        """
        perf = self.get(expert_id, task_type)
        if perf is None or perf.total_calls < 2:
            return 0.0  # no data yet — neutral
        # Normalise EMA to [-0.3, +0.5] using a tanh-like sigmoid
        # ema_reward typically in [-5, +15] range
        normalized = perf.ema_reward / 10.0
        bonus = 0.4 * math.tanh(normalized)
        return round(bonus, 4)

    # ── Persistence ───────────────────────────────────────────────────────────

    def _save(self) -> None:
        tmp = self._path.with_suffix(".json.tmp")
        try:
            raw = {k: asdict(v) for k, v in self._data.items()}
            tmp.write_text(json.dumps(raw, indent=2), encoding="utf-8")
            tmp.replace(self._path)
        except Exception as exc:
            log.warning("ExpertPerformanceStore._save: %s", exc)

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
            for key, val in raw.items():
                ep = ExpertPerformance(**{
                    k: v for k, v in val.items()
                    if not k.startswith("_")
                })
                self._data[key] = ep
            log.debug("ExpertPerformanceStore: loaded %d records", len(self._data))
        except Exception as exc:
            log.warning("ExpertPerformanceStore._load: %s", exc)


# ---------------------------------------------------------------------------
# Softmax selector  (Single Responsibility: probabilistic selection only)
# ---------------------------------------------------------------------------


class SoftmaxSelector(IExpertSelector):
    """
    Selects an expert using temperature-scaled softmax over adjusted weights.

    Higher weight → higher probability. Temperature controls exploration:
    - High temperature (>1.0): near-uniform distribution (more exploration)
    - Low temperature (<1.0): sharpened towards best expert (exploitation)
    """

    def __init__(self, temperature: float = 1.0) -> None:
        self._temperature = max(0.1, temperature)

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        self._temperature = max(0.1, value)

    def select(
        self,
        candidates: List[ExpertProfile],
        task_type: str,
        performance_store: ExpertPerformanceStore,
        deterministic: bool = False,
    ) -> ExpertProfile:
        if not candidates:
            raise ValueError("No expert candidates provided to SoftmaxSelector.")
        if len(candidates) == 1:
            return candidates[0]

        weights = self._compute_weights(candidates, task_type, performance_store)

        if deterministic:
            return candidates[weights.index(max(weights))]

        # Softmax sampling
        probs = _softmax(weights, self._temperature)
        return random.choices(candidates, weights=probs, k=1)[0]

    @staticmethod
    def _compute_weights(
        candidates: List[ExpertProfile],
        task_type: str,
        store: ExpertPerformanceStore,
    ) -> List[float]:
        weights: List[float] = []
        for expert in candidates:
            bonus  = store.performance_bonus(expert.expert_id, task_type)
            weight = expert.base_weight * (1.0 + bonus)
            weights.append(max(0.01, weight))  # floor at 0.01
        return weights


def _softmax(values: Sequence[float], temperature: float = 1.0) -> List[float]:
    """Numerically stable temperature-scaled softmax."""
    scaled = [v / temperature for v in values]
    max_v  = max(scaled)
    exps   = [math.exp(v - max_v) for v in scaled]
    total  = sum(exps)
    return [e / total for e in exps]


# ---------------------------------------------------------------------------
# Availability checker  (Single Responsibility: availability only)
# ---------------------------------------------------------------------------


class ExpertAvailabilityChecker:
    """
    Checks whether the backend for an expert is reachable.
    Results are cached for _AVAIL_CACHE_TTL_S seconds to avoid hammering APIs.
    """

    def __init__(self) -> None:
        self._cache: Dict[str, Tuple[bool, float]] = {}  # backend → (available, ts)
        self._lock  = threading.Lock()

    def is_available(self, expert: ExpertProfile, api_key: str = "") -> bool:
        with self._lock:
            cached = self._cache.get(expert.backend)
            if cached and time.time() - cached[1] < _AVAIL_CACHE_TTL_S:
                return cached[0]
        available = self._check(expert, api_key)
        with self._lock:
            self._cache[expert.backend] = (available, time.time())
        return available

    @staticmethod
    def _check(expert: ExpertProfile, api_key: str) -> bool:
        if expert.backend == "groq":
            key = api_key or os.environ.get("GROQ_API_KEY", "")
            return bool(key)
        if expert.backend == "ollama":
            try:
                import urllib.request
                host = os.environ.get("OLLAMA_HOST", "127.0.0.1")
                port = int(os.environ.get("OLLAMA_PORT", "11434"))
                urllib.request.urlopen(
                    f"http://{host}:{port}/api/tags", timeout=3
                )
                return True
            except Exception:
                return False
        return False


# ---------------------------------------------------------------------------
# MoE Router  (Open/Closed: extend via experts list, not code changes)
# ---------------------------------------------------------------------------


class MoERouter:
    """
    Top-level Mixture-of-Experts router.

    Maintains the expert registry, availability cache, and performance store.
    Provides route() for single-expert selection and ensemble() for multi-expert.

    Dependency Inversion: accepts IExpertSelector so the selection strategy
    can be swapped (e.g., replace SoftmaxSelector with Q-learning selector).
    """

    def __init__(
        self,
        experts: Optional[List[ExpertProfile]] = None,
        selector: Optional[IExpertSelector] = None,
        performance_store: Optional[ExpertPerformanceStore] = None,
        api_key: str = "",
    ) -> None:
        self._experts   = experts if experts is not None else list(_DEFAULT_EXPERTS)
        self._selector  = selector or SoftmaxSelector(temperature=1.2)
        self._store     = performance_store or ExpertPerformanceStore()
        self._avail     = ExpertAvailabilityChecker()
        self._api_key   = api_key or _load_groq_key()

    # ── Public routing API ────────────────────────────────────────────────────

    def route(
        self,
        task_type: str,
        goal: str = "",
        deterministic: bool = False,
    ) -> ExpertProfile:
        """
        Return the single best expert for the given task_type.

        Parameters
        ----------
        task_type:    Action category (recon/exploit/credential/lateral/…)
        goal:         The task description (used for future prompt-aware routing)
        deterministic: When True, return argmax instead of sampling.
        """
        candidates = self._available_for_task(task_type)
        if not candidates:
            # Fall back to any available expert
            candidates = self._available_for_task("other")
        if not candidates:
            raise RuntimeError(
                f"No available expert for task_type={task_type!r}. "
                "Check API keys and Ollama connectivity."
            )
        expert = self._selector.select(
            candidates, task_type, self._store, deterministic=deterministic
        )
        log.info(
            "MoERouter: routed task_type=%s → %s (%s)",
            task_type, expert.expert_id, expert.model,
        )
        return expert

    def ensemble(
        self,
        task_type: str,
        goal: str = "",
        n: int = 2,
    ) -> List[ExpertProfile]:
        """
        Return up to *n* distinct experts for ensemble execution.
        Experts are sorted by adjusted weight (best first).
        """
        candidates = self._available_for_task(task_type)
        if not candidates:
            candidates = self._available_for_task("other")

        # Sort by adjusted weight descending
        def adjusted_weight(ep: ExpertProfile) -> float:
            bonus = self._store.performance_bonus(ep.expert_id, task_type)
            return ep.base_weight * (1.0 + bonus)

        ranked = sorted(candidates, key=adjusted_weight, reverse=True)
        selected = ranked[:n]
        log.info(
            "MoERouter: ensemble task_type=%s → [%s]",
            task_type,
            ", ".join(e.expert_id for e in selected),
        )
        return selected

    def record_outcome(
        self,
        expert_id: str,
        task_type: str,
        reward: float,
        detection_prob: float = 0.0,
    ) -> None:
        """
        Record the outcome of an expert execution.
        Updates the performance store and adjusts the selector temperature.
        """
        self._store.record(expert_id, task_type, reward, detection_prob)
        self._anneal_temperature()

    def top_experts_for_task(
        self,
        task_type: str,
        top_k: int = 3,
    ) -> List[Tuple[ExpertProfile, float]]:
        """
        Return (expert, adjusted_weight) sorted descending for diagnostics.
        """
        result: List[Tuple[ExpertProfile, float]] = []
        for ep in self._experts:
            if task_type in ep.capabilities or task_type == "other":
                bonus = self._store.performance_bonus(ep.expert_id, task_type)
                w = ep.base_weight * (1.0 + bonus)
                result.append((ep, round(w, 4)))
        return sorted(result, key=lambda t: -t[1])[:top_k]

    def get_expert(self, expert_id: str) -> Optional[ExpertProfile]:
        """Return expert by ID, or None."""
        return next((e for e in self._experts if e.expert_id == expert_id), None)

    def status_report(self) -> dict:
        """Return a diagnostic snapshot of all experts and their weights."""
        rows = []
        for ep in self._experts:
            available = self._avail.is_available(ep, self._api_key)
            all_tasks: List[ExpertPerformance] = []
            for cap in ep.capabilities:
                p = self._store.get(ep.expert_id, cap)
                if p:
                    all_tasks.append(p)
            rows.append({
                "expert_id":   ep.expert_id,
                "backend":     ep.backend,
                "model":       ep.model,
                "capabilities": ep.capabilities,
                "base_weight": ep.base_weight,
                "available":   available,
                "total_calls": sum(p.total_calls for p in all_tasks),
                "avg_ema_reward": round(
                    sum(p.ema_reward for p in all_tasks) / len(all_tasks), 3
                ) if all_tasks else 0.0,
            })
        return {
            "experts":     rows,
            "temperature": round(self._selector.temperature if
                                 isinstance(self._selector, SoftmaxSelector) else -1, 3),
        }

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _available_for_task(self, task_type: str) -> List[ExpertProfile]:
        return [
            ep for ep in self._experts
            if task_type in ep.capabilities
            and self._avail.is_available(ep, self._api_key)
        ]

    def _anneal_temperature(self) -> None:
        """
        Gradually lower the softmax temperature as more data accumulates.
        More data → more confident routing → lower temperature (exploitation).
        Minimum temperature is capped at 0.5 to preserve some exploration.
        """
        if not isinstance(self._selector, SoftmaxSelector):
            return
        total_calls = sum(
            ep.total_calls
            for ep in self._store._data.values()
        )
        # Decay: T = T_max / (1 + calls / 50)
        new_temp = max(0.5, 1.5 / (1.0 + total_calls / 50.0))
        self._selector.temperature = round(new_temp, 3)
        log.debug("MoERouter: temperature annealed to %.3f", new_temp)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_groq_key() -> str:
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        return key
    try:
        payload = json.loads((_BASE_DIR / "payload.json").read_text())
        return payload.get("api_key", "") or payload.get("groq_api_key", "")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_router: Optional[MoERouter] = None
_router_lock = threading.Lock()


def get_router(api_key: str = "") -> MoERouter:
    """Return (or create) the module-level singleton MoERouter."""
    global _default_router
    if _default_router is None:
        with _router_lock:
            if _default_router is None:
                _default_router = MoERouter(api_key=api_key or _load_groq_key())
    return _default_router


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse, sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="LazyOwn MoE Router CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_route = sub.add_parser("route", help="Route a task to an expert")
    p_route.add_argument("task_type", help="e.g. exploit, recon, credential")
    p_route.add_argument("goal", nargs="?", default="", help="Optional task description")

    p_ens = sub.add_parser("ensemble", help="Get top-N experts for a task")
    p_ens.add_argument("task_type")
    p_ens.add_argument("--n", type=int, default=3)

    sub.add_parser("status", help="Show all experts and performance weights")

    args = parser.parse_args()
    router = get_router()

    if args.cmd == "route":
        expert = router.route(args.task_type, args.goal)
        print(f"Expert    : {expert.expert_id}")
        print(f"Backend   : {expert.backend}")
        print(f"Model     : {expert.model}")
        print(f"Cost tier : {expert.cost_tier}")
        print(f"Latency   : ~{expert.latency_ms}ms")

    elif args.cmd == "ensemble":
        experts = router.ensemble(args.task_type, n=args.n)
        for i, ep in enumerate(experts, 1):
            print(f"{i}. [{ep.expert_id}] {ep.backend}/{ep.model}")

    elif args.cmd == "status":
        report = router.status_report()
        print(f"Temperature: {report['temperature']}")
        print(f"{'Expert':20s}  {'Backend':8s}  {'Available':10s}  "
              f"{'Calls':6s}  {'EMA reward':12s}  Capabilities")
        for row in report["experts"]:
            avail = "yes" if row["available"] else "no"
            caps  = ",".join(row["capabilities"][:4])
            print(
                f"{row['expert_id']:20s}  {row['backend']:8s}  {avail:10s}  "
                f"{row['total_calls']:6d}  {row['avg_ema_reward']:12.3f}  {caps}"
            )
    else:
        parser.print_help()
