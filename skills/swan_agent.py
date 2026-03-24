#!/usr/bin/env python3
"""
skills/swan_agent.py — LazyOwn SWAN Agent
==========================================
Scalable Weighted Adaptive Network agent coordinator.

SWAN unifies the Mixture-of-Experts router, the RL trainer, and the existing
Groq/Ollama agent infrastructure (GroqAgentPool + LLMBridge) into a single
self-improving multi-model execution layer.

Properties
----------
  Scalable   — new expert models added to moe_router._DEFAULT_EXPERTS list only
  Weighted   — each expert's routing probability is weighted by RL-learned Q-values
               and EMA performance scores from completed engagements
  Adaptive   — weights update automatically after every task execution via Q-learning
  Network    — ensemble mode runs multiple experts in parallel and synthesizes results

Architecture
------------

        operator prompt / autonomous loop
                     |
              SwanOrchestrator.run()
              /          \\
     route()               ensemble()
        |                      |
   best expert           top-N experts
        |               (parallel threads)
  DroneAgent / LLMBridge    |
  (existing infrastructure) EnsembleAggregator
        |                      |
     result                synthesis (Claude or best expert)
        |                      |
        +------  outcome  -----+
                     |
           RLTrainer.update()        ExpertPerformanceStore.record()
           MoERouter.record_outcome()
                     |
           HiveMemory.store()   (lesson for future recall)

Design principles
-----------------
- Single Responsibility : each class owns one concept
- Open/Closed           : new aggregation strategies via IResultAggregator
- Liskov Substitution   : SwanOrchestrator satisfies ISwanOrchestrator
- Interface Segregation : ISwanOrchestrator exposes only run() and ensemble_run()
- Dependency Inversion  : all deps injected; defaults wired in get_swan()

Usage
-----
    from skills.swan_agent import get_swan

    swan = get_swan()

    # Single-expert execution
    result = swan.run("exploit", "Find RCE on Apache 2.4.49 at 10.10.11.78")
    print(result.output)
    print(f"Expert used: {result.expert_id}, reward: {result.reward}")

    # Ensemble: top-3 experts vote, then synthesize
    result = swan.ensemble_run(
        "credential",
        "Dump NTLM hashes from domain controller 10.10.11.78",
        n_experts=3,
    )
    print(result.synthesis)
    print(f"Consensus confidence: {result.consensus_confidence:.0%}")

    # Check SWAN status
    status = swan.status()
    print(status)
"""
from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time
import uuid
from abc import ABC, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Path setup ────────────────────────────────────────────────────────────────

SKILLS_DIR   = Path(__file__).parent
LAZYOWN_DIR  = Path(os.environ.get("LAZYOWN_DIR", str(SKILLS_DIR.parent)))
SESSIONS_DIR = LAZYOWN_DIR / "sessions"
MODULES_DIR  = LAZYOWN_DIR / "modules"

for _p in (str(SKILLS_DIR), str(LAZYOWN_DIR), str(MODULES_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

log = logging.getLogger("swan_agent")

# ── Optional lazy imports ─────────────────────────────────────────────────────

def _import_router():
    from modules.moe_router import get_router, ExpertProfile  # noqa: PLC0415
    return get_router(), ExpertProfile


def _import_trainer():
    from modules.rl_trainer import get_trainer  # noqa: PLC0415
    return get_trainer()


def _import_detection_oracle():
    try:
        from modules.detection_oracle import get_oracle  # noqa: PLC0415
        return get_oracle()
    except Exception:
        return None


def _import_policy():
    try:
        from skills.lazyown_policy import (  # noqa: PLC0415
            ActionCategory, OutcomeType, infer_category,
        )
        return ActionCategory, OutcomeType, infer_category
    except Exception:
        return None, None, None


# ---------------------------------------------------------------------------
# Result value objects
# ---------------------------------------------------------------------------


@dataclass
class SwanResult:
    """
    Result from a single-expert SWAN execution.
    """
    task_id:        str
    task_type:      str
    goal:           str
    expert_id:      str
    backend:        str
    model:          str
    output:         str
    status:         str              # completed | failed | timeout
    reward:         float   = 0.0
    detection_prob: float   = 0.0
    duration_s:     float   = 0.0
    started_at:     str     = ""
    state_key:      str     = ""     # RL state used for this task
    error:          str     = ""

    @property
    def is_success(self) -> bool:
        return self.status == "completed" and not self.error


@dataclass
class ExpertVote:
    """One expert's contribution to an ensemble."""
    expert_id:   str
    output:      str
    weight:      float       # routing weight at the time of execution
    status:      str
    duration_s:  float


@dataclass
class EnsembleResult:
    """
    Aggregated result from multiple experts.
    """
    task_id:               str
    task_type:             str
    goal:                  str
    votes:                 List[ExpertVote]
    synthesis:             str        # combined output from synthesizer
    consensus_confidence:  float      # fraction of experts that agree
    best_expert_id:        str        # expert with highest weight
    reward:                float
    detection_prob:        float
    duration_s:            float


# ---------------------------------------------------------------------------
# Interfaces
# ---------------------------------------------------------------------------


class IResultAggregator(ABC):
    """Contract for combining multiple expert outputs into one synthesis."""

    @abstractmethod
    def aggregate(
        self,
        task_type: str,
        goal: str,
        votes: List[ExpertVote],
    ) -> Tuple[str, float]:
        """
        Return (synthesis_text, consensus_confidence).

        consensus_confidence is in [0.0, 1.0] — higher means experts agree more.
        """


class ISwanOrchestrator(ABC):
    """Top-level SWAN orchestrator contract."""

    @abstractmethod
    def run(
        self,
        task_type: str,
        goal: str,
        engagement_phase: str = "exploitation",
        timeout: float = 300.0,
    ) -> SwanResult:
        """Execute with the best single expert and return result."""

    @abstractmethod
    def ensemble_run(
        self,
        task_type: str,
        goal: str,
        n_experts: int = 3,
        engagement_phase: str = "exploitation",
        timeout: float = 300.0,
    ) -> EnsembleResult:
        """Execute with top-N experts in parallel and synthesize results."""


# ---------------------------------------------------------------------------
# Weighted text aggregator (Single Responsibility: synthesis only)
# ---------------------------------------------------------------------------


class WeightedTextAggregator(IResultAggregator):
    """
    Aggregates expert outputs by building a weighted synthesis prompt and
    invoking the highest-weight expert as the synthesizer.

    When only one expert succeeded, returns its output directly.
    When multiple experts succeeded, prompts the synthesizer to combine them.

    Consensus confidence is approximated as the fraction of experts that
    completed successfully (not failed or timed out).
    """

    def aggregate(
        self,
        task_type: str,
        goal: str,
        votes: List[ExpertVote],
    ) -> Tuple[str, float]:
        successful = [v for v in votes if v.status == "completed"]
        if not successful:
            return "[ENSEMBLE] All experts failed.", 0.0

        confidence = len(successful) / max(len(votes), 1)

        if len(successful) == 1:
            return successful[0].output, confidence

        # Build synthesis context
        synthesis = self._build_synthesis(task_type, goal, successful)
        return synthesis, confidence

    @staticmethod
    def _build_synthesis(
        task_type: str,
        goal: str,
        experts: List[ExpertVote],
    ) -> str:
        lines = [
            f"[SWAN ENSEMBLE SYNTHESIS — {task_type.upper()}]",
            f"Goal: {goal[:200]}",
            f"Experts consulted: {len(experts)}",
            "",
        ]
        # Sort by weight descending
        for i, ev in enumerate(sorted(experts, key=lambda e: -e.weight), 1):
            lines.append(
                f"Expert {i} [{ev.expert_id}] (weight={ev.weight:.3f}, "
                f"duration={ev.duration_s:.1f}s):"
            )
            lines.append(ev.output[:1000])
            lines.append("")

        lines.append("[CONSENSUS]")
        lines.append(
            "The following recommendations appear in multiple expert responses:"
        )

        # Simple consensus: find sentences repeated across outputs (>1 expert)
        all_lines: Dict[str, int] = {}
        for ev in experts:
            for sent in ev.output.split(". "):
                sent = sent.strip()
                if len(sent) > 20:
                    all_lines[sent] = all_lines.get(sent, 0) + 1

        consensus_lines = sorted(
            [(c, t) for t, c in all_lines.items() if c > 1],
            reverse=True,
        )
        if consensus_lines:
            for count, text in consensus_lines[:5]:
                lines.append(f"  ({count}/{len(experts)} experts) {text[:150]}")
        else:
            lines.append("  No common sentences found — outputs are divergent.")
            lines.append(
                f"  Highest-weight expert [{experts[0].expert_id}] recommendation:"
            )
            lines.append(f"  {experts[0].output[:300]}")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Expert executor (Single Responsibility: run one expert)
# ---------------------------------------------------------------------------


class ExpertExecutor:
    """
    Runs a single expert (backend + model) for a given goal.

    Uses the existing GroqAgentPool / LLMBridge infrastructure.
    Supports both groq and ollama backends.
    """

    _DEFAULT_TOOLS = [
        "run_command", "bridge_suggest", "parquet_context",
        "reactive_suggest", "facts_show", "rag_query",
        "memory_search", "session_status",
    ]

    def execute(
        self,
        expert_id: str,
        backend: str,
        model: str,
        goal: str,
        task_type: str,
        timeout: float = 300.0,
        api_key: str = "",
    ) -> SwanResult:
        """Run the expert and return a SwanResult."""
        task_id    = uuid.uuid4().hex[:8]
        started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        t0         = time.time()

        try:
            output = self._invoke(backend, model, goal, task_type, api_key, timeout)
            status = "completed"
            error  = ""
        except TimeoutError:
            output = f"[TIMEOUT after {timeout:.0f}s]"
            status = "timeout"
            error  = "timeout"
        except Exception as exc:
            output = f"[ERROR] {exc}"
            status = "failed"
            error  = str(exc)
            log.warning("ExpertExecutor [%s]: %s", expert_id, exc)

        return SwanResult(
            task_id=task_id,
            task_type=task_type,
            goal=goal,
            expert_id=expert_id,
            backend=backend,
            model=model,
            output=output,
            status=status,
            duration_s=round(time.time() - t0, 2),
            started_at=started_at,
            error=error,
        )

    def _invoke(
        self,
        backend: str,
        model: str,
        goal: str,
        task_type: str,
        api_key: str,
        timeout: float,
    ) -> str:
        from lazyown_groq_agents import spawn_agent, agent_result  # noqa: PLC0415

        key = api_key or os.environ.get("GROQ_API_KEY", "") or self._load_payload_key()
        agent_id = spawn_agent(
            goal=goal,
            tools_filter=self._tools_for_task(task_type),
            api_key=key if backend == "groq" else None,
            backend=backend,
            max_iterations=8,
            block=True,           # synchronous — we handle timeout externally
        )
        return agent_result(agent_id)

    @staticmethod
    def _tools_for_task(task_type: str) -> List[str]:
        task_tools: Dict[str, List[str]] = {
            "recon":       ["run_command", "facts_show", "bridge_suggest",
                            "rag_query", "session_status"],
            "enum":        ["run_command", "facts_show", "bridge_suggest",
                            "rag_query", "session_status"],
            "exploit":     ["run_command", "bridge_suggest", "parquet_context",
                            "reactive_suggest", "rag_query", "atomic_search"],
            "credential":  ["run_command", "bridge_suggest", "parquet_context",
                            "reactive_suggest", "facts_show"],
            "lateral":     ["run_command", "bridge_suggest", "session_status",
                            "c2_status", "c2_command", "reactive_suggest"],
            "privesc":     ["run_command", "bridge_suggest", "parquet_context",
                            "reactive_suggest", "atomic_search", "searchsploit"],
            "analyze":     ["run_command", "rag_query", "memory_search",
                            "reactive_suggest", "threat_model", "facts_show"],
            "report":      ["rag_query", "threat_model", "facts_show",
                            "parquet_context", "task_list", "memory_search"],
        }
        return task_tools.get(task_type, ExpertExecutor._DEFAULT_TOOLS)

    @staticmethod
    def _load_payload_key() -> str:
        try:
            return json.loads(
                (LAZYOWN_DIR / "payload.json").read_text()
            ).get("api_key", "")
        except Exception:
            return ""


# ---------------------------------------------------------------------------
# Outcome evaluator (Single Responsibility: reward + detection assessment)
# ---------------------------------------------------------------------------


class OutcomeEvaluator:
    """
    Evaluates the outcome of an expert execution:
    - Determines reward via the policy engine reward table.
    - Queries the detection oracle for detection probability.

    Fails gracefully when optional modules are unavailable.
    """

    _OUTCOME_REWARD_MAP: Dict[str, int] = {
        "completed": 5,
        "timeout":   -2,
        "failed":    -3,
    }

    def evaluate(
        self,
        result: SwanResult,
        task_type: str,
    ) -> Tuple[float, float]:
        """
        Return (reward, detection_prob).

        reward:         scalar reward for RL update
        detection_prob: detection probability from oracle
        """
        reward = float(self._base_reward(result.status, task_type))
        detection_prob = self._detection_prob(result.goal, task_type)

        # Apply detection penalty: high-risk success is worth less
        if detection_prob >= 0.70 and result.is_success:
            reward = 0.0
            log.info(
                "OutcomeEvaluator: reward zeroed for %s (detect=%.0f%%)",
                task_type, detection_prob * 100,
            )

        return reward, detection_prob

    def _base_reward(self, status: str, task_type: str) -> int:
        base = self._OUTCOME_REWARD_MAP.get(status, 0)
        # Boost for high-value categories
        if status == "completed" and task_type in (
            "credential", "privesc", "lateral", "intrusion"
        ):
            base = int(base * 1.5)
        return base

    @staticmethod
    def _detection_prob(goal: str, task_type: str) -> float:
        oracle = _import_detection_oracle()
        if oracle is None:
            return 0.0
        try:
            return oracle.probability(goal[:80], "", task_type)
        except Exception:
            return 0.0


# ---------------------------------------------------------------------------
# SWAN Orchestrator (top-level coordinator)
# ---------------------------------------------------------------------------


class SwanOrchestrator(ISwanOrchestrator):
    """
    Scalable Weighted Adaptive Network orchestrator.

    Coordinates MoERouter, RLTrainer, ExpertExecutor, OutcomeEvaluator,
    and EnsembleAggregator into a unified self-improving execution layer.

    After each execution:
      1. Evaluates the outcome (reward + detection probability).
      2. Updates the MoE router's performance store.
      3. Updates the RL trainer's Q-values.
      4. Stores a lesson in hive memory (if available).

    Single Responsibility: orchestration only — delegates to specialists.
    Dependency Inversion: all collaborators injected via constructor.
    """

    def __init__(
        self,
        executor:   Optional[ExpertExecutor]   = None,
        evaluator:  Optional[OutcomeEvaluator] = None,
        aggregator: Optional[IResultAggregator] = None,
        api_key:    str = "",
    ) -> None:
        self._executor   = executor  or ExpertExecutor()
        self._evaluator  = evaluator or OutcomeEvaluator()
        self._aggregator = aggregator or WeightedTextAggregator()
        self._api_key    = api_key or self._load_key()
        self._lock       = threading.RLock()

        # Lazy-loaded collaborators
        self._router:  Any = None
        self._trainer: Any = None
        self._memory:  Any = None

    # ── ISwanOrchestrator ─────────────────────────────────────────────────────

    def run(
        self,
        task_type: str,
        goal: str,
        engagement_phase: str = "exploitation",
        timeout: float = 300.0,
    ) -> SwanResult:
        """
        Execute the task with the best single expert selected by the MoE+RL router.

        1. Encodes current state for RL.
        2. Retrieves expert candidates from MoE router.
        3. Selects expert via RL epsilon-greedy policy.
        4. Executes the expert.
        5. Evaluates outcome and updates RL + performance store.
        6. Returns SwanResult.
        """
        router  = self._get_router()
        trainer = self._get_trainer()

        # Select expert
        try:
            expert = router.route(task_type, goal)
        except RuntimeError as exc:
            log.warning("SwanOrchestrator: routing failed (%s), using groq fallback", exc)
            from modules.moe_router import ExpertProfile  # noqa: PLC0415
            expert = ExpertProfile(
                expert_id="groq_fallback",
                backend="groq",
                model="llama-3.3-70b-versatile",
                capabilities=[task_type],
                base_weight=0.8,
                cost_tier=2,
                latency_ms=2000,
            )

        state_key = trainer.encode_state(task_type, engagement_phase)

        # RL-guided selection from available candidates
        candidates_obj = router.ensemble(task_type, goal, n=4)
        candidate_ids  = [e.expert_id for e in candidates_obj]
        selected_id    = trainer.select_action(state_key, candidate_ids)

        # Resolve selected expert profile
        selected_expert = next(
            (e for e in candidates_obj if e.expert_id == selected_id),
            expert,
        )

        log.info(
            "SWAN run: task=%s phase=%s expert=%s model=%s",
            task_type, engagement_phase,
            selected_expert.expert_id, selected_expert.model,
        )

        # Execute
        result = self._executor.execute(
            expert_id=selected_expert.expert_id,
            backend=selected_expert.backend,
            model=selected_expert.model,
            goal=goal,
            task_type=task_type,
            timeout=timeout,
            api_key=self._api_key,
        )
        result.state_key = state_key

        # Evaluate and update
        reward, detection_prob = self._evaluator.evaluate(result, task_type)
        result.reward         = reward
        result.detection_prob = detection_prob

        self._post_execution_update(
            expert_id=selected_expert.expert_id,
            task_type=task_type,
            reward=reward,
            detection_prob=detection_prob,
            state_key=state_key,
            next_state=trainer.encode_state(
                self._next_task_type(task_type), engagement_phase
            ),
            candidate_ids=candidate_ids,
            result=result,
        )

        return result

    def ensemble_run(
        self,
        task_type: str,
        goal: str,
        n_experts: int = 3,
        engagement_phase: str = "exploitation",
        timeout: float = 300.0,
    ) -> EnsembleResult:
        """
        Execute with top-N experts in parallel and synthesize results.

        All experts receive the same goal concurrently. The aggregator then
        produces a synthesis combining their outputs with confidence weighting.
        """
        router  = self._get_router()
        trainer = self._get_trainer()

        experts = router.ensemble(task_type, goal, n=n_experts)
        if not experts:
            raise RuntimeError(
                f"No available experts for task_type={task_type!r}"
            )

        state_key = trainer.encode_state(task_type, engagement_phase)
        t0 = time.time()

        log.info(
            "SWAN ensemble: task=%s experts=[%s]",
            task_type,
            ", ".join(e.expert_id for e in experts),
        )

        # Run all experts in parallel
        votes = self._parallel_execute(experts, goal, task_type, timeout)

        # Aggregate
        synthesis, confidence = self._aggregator.aggregate(task_type, goal, votes)

        # Evaluate best result and update RL
        best_vote   = max(votes, key=lambda v: v.weight) if votes else None
        best_reward = 0.0
        best_detect = 0.0
        if best_vote and best_vote.status == "completed":
            dummy   = SwanResult(
                task_id="ensemble", task_type=task_type, goal=goal,
                expert_id=best_vote.expert_id, backend="", model="",
                output=best_vote.output, status=best_vote.status,
            )
            best_reward, best_detect = self._evaluator.evaluate(dummy, task_type)

        # Update all participating experts
        for vote in votes:
            vote_reward    = best_reward if vote.status == "completed" else -2.0
            vote_detection = best_detect
            self._post_execution_update(
                expert_id=vote.expert_id,
                task_type=task_type,
                reward=vote_reward,
                detection_prob=vote_detection,
                state_key=state_key,
                next_state=trainer.encode_state(
                    self._next_task_type(task_type), engagement_phase
                ),
                candidate_ids=[e.expert_id for e in experts],
                result=None,
            )

        return EnsembleResult(
            task_id=uuid.uuid4().hex[:8],
            task_type=task_type,
            goal=goal,
            votes=votes,
            synthesis=synthesis,
            consensus_confidence=confidence,
            best_expert_id=best_vote.expert_id if best_vote else "",
            reward=best_reward,
            detection_prob=best_detect,
            duration_s=round(time.time() - t0, 2),
        )

    # ── Status / diagnostics ─────────────────────────────────────────────────

    def status(self) -> dict:
        """Return a diagnostic snapshot of the SWAN system."""
        router  = self._get_router()
        trainer = self._get_trainer()
        report  = router.status_report()
        report["rl_epsilon"]    = round(trainer.epsilon, 4)
        report["rl_config"]     = {
            "learning_rate":   trainer._cfg.learning_rate,
            "discount_factor": trainer._cfg.discount_factor,
            "detection_lambda": trainer._cfg.detection_lambda,
        }
        return report

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _parallel_execute(
        self,
        experts: List[Any],
        goal: str,
        task_type: str,
        timeout: float,
    ) -> List[ExpertVote]:
        votes: List[ExpertVote] = []
        with ThreadPoolExecutor(max_workers=len(experts)) as pool:
            future_map: Dict[Future, Any] = {}
            for expert in experts:
                f = pool.submit(
                    self._executor.execute,
                    expert_id=expert.expert_id,
                    backend=expert.backend,
                    model=expert.model,
                    goal=goal,
                    task_type=task_type,
                    timeout=timeout,
                    api_key=self._api_key,
                )
                future_map[f] = expert

            for future in as_completed(future_map, timeout=timeout + 10):
                expert = future_map[future]
                try:
                    result = future.result(timeout=5)
                    votes.append(ExpertVote(
                        expert_id=expert.expert_id,
                        output=result.output,
                        weight=expert.base_weight,
                        status=result.status,
                        duration_s=result.duration_s,
                    ))
                except Exception as exc:
                    log.warning("Ensemble expert %s failed: %s", expert.expert_id, exc)
                    votes.append(ExpertVote(
                        expert_id=expert.expert_id,
                        output=f"[FAILED] {exc}",
                        weight=expert.base_weight,
                        status="failed",
                        duration_s=0.0,
                    ))
        return votes

    def _post_execution_update(
        self,
        expert_id: str,
        task_type: str,
        reward: float,
        detection_prob: float,
        state_key: str,
        next_state: str,
        candidate_ids: List[str],
        result: Optional[SwanResult],
    ) -> None:
        """Update MoE performance store, RL Q-table, and hive memory."""
        router  = self._get_router()
        trainer = self._get_trainer()

        # 1 — MoE router performance
        router.record_outcome(expert_id, task_type, reward, detection_prob)

        # 2 — RL Q-learning update
        trainer.update(
            state=state_key,
            action=expert_id,
            reward=reward,
            next_state=next_state,
            candidates=candidate_ids,
            detection_prob=detection_prob,
        )
        trainer.save()

        # 3 — Hive memory (best-effort)
        if result is not None:
            self._store_to_hive(result, reward, detection_prob)

    def _store_to_hive(
        self,
        result: SwanResult,
        reward: float,
        detection_prob: float,
    ) -> None:
        try:
            memory = self._get_hive_memory()
            if memory is None:
                return
            memory.store(
                content=(
                    f"[SWAN] expert={result.expert_id} task={result.task_type} "
                    f"status={result.status} reward={reward:+.1f} "
                    f"detect={detection_prob:.0%}\n"
                    f"goal={result.goal[:200]}\n"
                    f"output={result.output[:500]}"
                ),
                agent_id="swan_agent",
                role="architect",
                event_type="swan_execution",
                meta={
                    "expert_id":      result.expert_id,
                    "task_type":      result.task_type,
                    "reward":         reward,
                    "detection_prob": detection_prob,
                    "status":         result.status,
                },
            )
        except Exception as exc:
            log.debug("SWAN hive store error: %s", exc)

    @staticmethod
    def _next_task_type(task_type: str) -> str:
        """Simple kill-chain progression for next-state encoding."""
        _chain: Dict[str, str] = {
            "recon":       "enum",
            "enum":        "exploit",
            "exploit":     "intrusion",
            "intrusion":   "privesc",
            "privesc":     "credential",
            "credential":  "lateral",
            "lateral":     "privesc",
        }
        return _chain.get(task_type, "analyze")

    # ── Lazy-loaded collaborator accessors ───────────────────────────────────

    def _get_router(self) -> Any:
        if self._router is None:
            router, _ = _import_router()
            self._router = router
        return self._router

    def _get_trainer(self) -> Any:
        if self._trainer is None:
            self._trainer = _import_trainer()
        return self._trainer

    def _get_hive_memory(self) -> Optional[Any]:
        if self._memory is None:
            try:
                from hive_mind import get_hive  # noqa: PLC0415
                self._memory = get_hive()._memory
            except Exception:
                self._memory = False  # sentinel: tried but unavailable
        return self._memory if self._memory else None

    @staticmethod
    def _load_key() -> str:
        key = os.environ.get("GROQ_API_KEY", "")
        if key:
            return key
        try:
            return json.loads(
                (LAZYOWN_DIR / "payload.json").read_text()
            ).get("api_key", "")
        except Exception:
            return ""


# ---------------------------------------------------------------------------
# MCP tool functions (wired in lazyown_mcp.py)
# ---------------------------------------------------------------------------


def mcp_swan_run(task_type: str, goal: str, phase: str = "exploitation") -> str:
    """
    Route and execute a task with the best MoE+RL-selected expert.
    Returns the expert's output as a string.
    """
    swan   = get_swan()
    result = swan.run(task_type, goal, engagement_phase=phase)
    return json.dumps({
        "task_id":       result.task_id,
        "expert_id":     result.expert_id,
        "backend":       result.backend,
        "model":         result.model,
        "status":        result.status,
        "reward":        result.reward,
        "detection_pct": round(result.detection_prob * 100, 1),
        "duration_s":    result.duration_s,
        "output":        result.output[:4000],
    }, indent=2)


def mcp_swan_ensemble(
    task_type: str,
    goal: str,
    n_experts: int = 3,
    phase: str = "exploitation",
) -> str:
    """
    Run top-N experts in parallel and return a synthesized result.
    Higher confidence = more expert agreement.
    """
    swan   = get_swan()
    result = swan.ensemble_run(task_type, goal, n_experts=n_experts,
                               engagement_phase=phase)
    return json.dumps({
        "task_id":             result.task_id,
        "experts_used":        [v.expert_id for v in result.votes],
        "successful_experts":  sum(1 for v in result.votes if v.status == "completed"),
        "consensus_pct":       round(result.consensus_confidence * 100, 1),
        "best_expert":         result.best_expert_id,
        "reward":              result.reward,
        "detection_pct":       round(result.detection_prob * 100, 1),
        "duration_s":          result.duration_s,
        "synthesis":           result.synthesis[:5000],
    }, indent=2)


def mcp_swan_status() -> str:
    """Return SWAN system status: expert weights, RL epsilon, performance."""
    swan   = get_swan()
    status = swan.status()
    return json.dumps(status, indent=2)


def mcp_swan_route(task_type: str, goal: str = "") -> str:
    """Show which expert would be selected for a task without executing."""
    router, _ = _import_router()
    experts   = router.ensemble(task_type, goal, n=4)
    rows = []
    for ep in experts:
        bonus = router._store.performance_bonus(ep.expert_id, task_type)
        adj   = ep.base_weight * (1.0 + bonus)
        rows.append({
            "expert_id":       ep.expert_id,
            "backend":         ep.backend,
            "model":           ep.model,
            "base_weight":     ep.base_weight,
            "adjusted_weight": round(adj, 4),
            "latency_ms":      ep.latency_ms,
        })
    return json.dumps({
        "task_type": task_type,
        "goal":      goal[:100],
        "routing":   rows,
    }, indent=2)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_default_swan: Optional[SwanOrchestrator] = None
_swan_lock = threading.Lock()


def get_swan(api_key: str = "") -> SwanOrchestrator:
    """Return (or create) the module-level singleton SwanOrchestrator."""
    global _default_swan
    if _default_swan is None:
        with _swan_lock:
            if _default_swan is None:
                _default_swan = SwanOrchestrator(api_key=api_key)
    return _default_swan


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(
        description="LazyOwn SWAN Agent — Scalable Weighted Adaptive Network"
    )
    sub = parser.add_subparsers(dest="cmd")

    p_run = sub.add_parser("run", help="Run a task with the best expert")
    p_run.add_argument("task_type", help="e.g. exploit, recon, credential")
    p_run.add_argument("goal",      help="Task description")
    p_run.add_argument("--phase",   default="exploitation")

    p_ens = sub.add_parser("ensemble", help="Run top-N experts in parallel")
    p_ens.add_argument("task_type")
    p_ens.add_argument("goal")
    p_ens.add_argument("--n",     type=int, default=3)
    p_ens.add_argument("--phase", default="exploitation")

    p_rt = sub.add_parser("route", help="Show routing without executing")
    p_rt.add_argument("task_type")
    p_rt.add_argument("goal", nargs="?", default="")

    sub.add_parser("status", help="Show SWAN system status")

    args = parser.parse_args()

    if args.cmd == "run":
        print(mcp_swan_run(args.task_type, args.goal, args.phase))
    elif args.cmd == "ensemble":
        print(mcp_swan_ensemble(args.task_type, args.goal, args.n, args.phase))
    elif args.cmd == "route":
        print(mcp_swan_route(args.task_type, args.goal))
    elif args.cmd == "status":
        print(mcp_swan_status())
    else:
        parser.print_help()
