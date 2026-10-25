# `modules.guardrails`

> Source: [modules/guardrails/__init__.py:1](../../modules/guardrails/__init__.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Operator-facing guardrail harness: tiers, capacity, checkpoints.

Exposes the harness contracts used by the autonomous loop, the APT
chain and the orchestrator admin console:

    from modules.guardrails import TaskClass, global_harness

    harness = global_harness()
    result = harness.run_guarded(
        TaskClass.MISSION, worker.execute, node, executor=executor
    )
