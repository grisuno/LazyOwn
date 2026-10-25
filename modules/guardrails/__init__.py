"""Operator-facing guardrail harness: tiers, capacity, checkpoints.

Exposes the harness contracts used by the autonomous loop, the APT
chain and the orchestrator admin console:

    from modules.guardrails import TaskClass, global_harness

    harness = global_harness()
    result = harness.run_guarded(
        TaskClass.MISSION, worker.execute, node, executor=executor
    )
"""

from __future__ import annotations

from modules.guardrails.advisories import (
    ADVISORY_LIMIT,
    SUSPENDABLE_FEATURES,
    AdvisoryLedger,
    FeatureGate,
)
from modules.guardrails.budget import (
    DEFAULT_CAPACITY_CORE,
    DEFAULT_CAPACITY_MISSION,
    DEFAULT_CAPACITY_SUPPORT,
    DEFAULT_SATURATION_THRESHOLD,
    CapacityEnvelope,
)
from modules.guardrails.checkpoints import CHECKPOINT_HISTORY_PER_KEY, CheckpointLedger
from modules.guardrails.contracts import (
    CONFIG_SECTION,
    GuardrailContract,
    HarnessAdminPort,
    RunTicket,
    TaskClass,
)
from modules.guardrails.harness import GuardHarness, global_harness, reset_global_harness

__all__ = [
    "ADVISORY_LIMIT",
    "CHECKPOINT_HISTORY_PER_KEY",
    "CONFIG_SECTION",
    "DEFAULT_CAPACITY_CORE",
    "DEFAULT_CAPACITY_MISSION",
    "DEFAULT_CAPACITY_SUPPORT",
    "DEFAULT_SATURATION_THRESHOLD",
    "SUSPENDABLE_FEATURES",
    "AdvisoryLedger",
    "CapacityEnvelope",
    "CheckpointLedger",
    "FeatureGate",
    "GuardHarness",
    "GuardrailContract",
    "HarnessAdminPort",
    "RunTicket",
    "TaskClass",
    "global_harness",
    "reset_global_harness",
]
