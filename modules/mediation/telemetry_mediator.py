"""Specialised mediator for loop telemetry coordination.

Owns every ``modules.loop_ai_bridge`` interaction: loop event publish,
detection annotation, step recording, MoE/RL member selection, and SWAN
consultation. Consumers request these through the mediator instead of
importing the bridge directly.
"""

from __future__ import annotations

from typing import Any


class TelemetryMediator:
    """Mediate learning and event telemetry for the autonomous loop."""

    domain: str = "loop.telemetry"

    def describe(self) -> dict[str, Any]:
        """Return mediator metadata for diagnostics."""
        return {"domain": self.domain}

    def publish_event(self, task_id: str, worker: str, kind: str, text: str, severity: str = "info") -> None:
        """Publish one loop activity event to listeners.

        Args:
            task_id: Loop task identifier.
            worker: Emitting worker name.
            kind: Event kind.
            text: Cleaned event text.
            severity: Severity label.
        """
        try:
            from modules.loop_ai_bridge import publish_loop_event

            if severity == "info":
                publish_loop_event(task_id, worker, kind, text)
            else:
                publish_loop_event(task_id, worker, kind, text, severity=severity)
        except Exception:
            pass

    def annotate_detection(self, command: str) -> dict:
        """Return the detection annotation for one command.

        Args:
            command: Shell command line.

        Returns:
            Annotation mapping, empty dict when unavailable.
        """
        try:
            from modules.loop_ai_bridge import annotate_detection

            return annotate_detection(command) or {}
        except Exception:
            return {}

    def assess_opsec(self, command: str, rhost: str = "") -> dict | None:
        """Return the pre-execution OPSEC gate assessment for one command.

        Args:
            command: Shell command line.
            rhost: Target host for sensitivity context.

        Returns:
            Gate mapping (gate/noise/risk_label/explanation/mitigations),
            or None when the stage is disabled or scoring failed.
        """
        try:
            from modules.loop_ai_bridge import assess_opsec

            return assess_opsec(command, rhost=rhost)
        except Exception:
            return None

    def record_outcome_quality(self, worker: str, intent_summary: str, facts: int, findings: int) -> None:
        """Record one intent's net yield as a decision-quality reward.

        Args:
            worker: Emitting worker name.
            intent_summary: Summary of the finished intent.
            facts: Facts persisted by the intent's writeback.
            findings: Findings persisted by the intent's writeback.
        """
        try:
            from modules.loop_ai_bridge import record_outcome_quality

            record_outcome_quality(worker, intent_summary, facts, findings)
        except Exception:
            pass

    def tool_class_yields(self, summaries: list[str], phase: str = "engage") -> dict[str, float]:
        """Return learned decision-quality yields for candidate summaries.

        Args:
            summaries: Candidate summaries the planner is about to rank.
            phase: Engagement phase key the reward was recorded under.

        Returns:
            Mapping of summary to its tool-class Q-value, empty when the
            stage is off or the trainer is unavailable.
        """
        try:
            from modules.loop_ai_bridge import tool_class_yields

            return tool_class_yields(summaries, phase=phase)
        except Exception:
            return {}

    def record_step(self, task_id: str, worker: str, command: str, output: str, detection_prob: float = 0.0) -> None:
        """Record one executed step for learning stores.

        Args:
            task_id: Loop task identifier.
            worker: Emitting worker name.
            command: Executed command.
            output: Command output extract.
            detection_prob: Detection likelihood of the command.
        """
        try:
            from modules.loop_ai_bridge import record_step

            record_step(task_id, worker, command, output, detection_prob=detection_prob)
        except Exception:
            pass

    def swan_available(self) -> bool:
        """Return True when the SWAN ensemble is ready."""
        try:
            from modules.loop_ai_bridge import swan_available

            return bool(swan_available())
        except Exception:
            return False

    def swan_consult(
        self,
        prompt: str,
        task_type: str = "recon",
        phase: str = "enumeration",
        timeout: float = 120.0,
    ) -> str:
        """Consult the SWAN ensemble with one prompt.

        Args:
            prompt: Question text.
            task_type: Task typing for routing.
            phase: Kill-chain phase label.
            timeout: Seconds before giving up.

        Returns:
            Ensemble reply, or an empty string when unavailable.
        """
        try:
            from modules.loop_ai_bridge import swan_consult

            return swan_consult(prompt, task_type=task_type, phase=phase, timeout=timeout)
        except Exception:
            return ""

    def moe_route(self, task_type: str) -> Any:
        """Return the preferred MoE expert for a task type.

        Args:
            task_type: Task typing for routing.

        Returns:
            Expert object or None when routing is unavailable.
        """
        try:
            from modules.loop_ai_bridge import moe_route

            return moe_route(task_type)
        except Exception:
            return None

    def rl_select(
        self,
        task_type: str,
        phase: str,
        candidates: list[str],
        deterministic: bool = False,
    ) -> str:
        """Return the RL-preferred candidate name.

        Args:
            task_type: Task typing for routing.
            phase: Kill-chain phase label.
            candidates: Member name candidates.
            deterministic: Force deterministic selection.

        Returns:
            Preferred candidate name, empty when unavailable.
        """
        try:
            from modules.loop_ai_bridge import rl_select

            return rl_select(task_type, phase, candidates, deterministic=deterministic)
        except Exception:
            return ""

    def moe_record_outcome(self, expert_id: str, task_type: str, reward: float, detection_prob: float = 0.0) -> None:
        """Record one MoE outcome for learning.

        Args:
            expert_id: Member name.
            task_type: Task typing for routing.
            reward: Reward signal.
            detection_prob: Detection likelihood.
        """
        try:
            from modules.loop_ai_bridge import moe_record_outcome

            moe_record_outcome(expert_id, task_type, reward, detection_prob=detection_prob)
        except Exception:
            pass

    def rl_update(
        self,
        task_type: str,
        phase: str,
        action: str,
        reward: float,
        candidates: list[str],
        detection_prob: float = 0.0,
    ) -> None:
        """Apply one Q-learning update for an executed action.

        Args:
            task_type: Task typing for routing.
            phase: Kill-chain phase label.
            action: Executed member name.
            reward: Reward signal.
            candidates: Member name candidates.
            detection_prob: Detection likelihood.
        """
        try:
            from modules.loop_ai_bridge import rl_update

            rl_update(task_type, phase, action, reward, candidates, detection_prob=detection_prob)
        except Exception:
            pass
