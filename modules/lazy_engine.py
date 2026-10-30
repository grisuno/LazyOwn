"""Lazy autonomous loop engine: single orchestrator for lazy_* commands.

Every subsystem keeps exact behavior under operator-facing ``lazy_*``
names. Storage lives under ``sessions/lazy/``.
"""

from __future__ import annotations

from modules.lazy_loop import (
    TOOL_DEFAULTS,
    ActivityLog,
    AssetGate,
    AssetGraph,
    Budget,
    ColdCompactor,
    CompanyScope,
    EvidenceStore,
    ExplorationGraph,
    FindingService,
    Frontier,
    Guard,
    InterceptQueue,
    LazyLoopEngine,
    LlmPool,
    Notifier,
    Planner,
    Retester,
    RuntimeTracker,
    SideQuestions,
    TaskArchive,
    TaskCategory,
    TaskChat,
    TaskStore,
    TaskTemplate,
    TodoStore,
    ToolCatalog,
    TrafficLog,
    TriggerStore,
    Worker,
    build_prompt_context,
    constraint_block,
    decompose_goals,
    enrich_asset,
    extract_constraint_items,
    extract_scope_items,
    finding_severity,
    judge_command,
    load_intel_scores,
    parse_judge_output,
    resolve_target,
    settlement_prompt,
    terminal_hint,
)


class LazyEngine(LazyLoopEngine):
    """Single orchestrator exposed under the lazy_* command surface."""


__all__ = ["LazyEngine", "LazyLoopEngine", "AssetGraph", "AssetGate", "ExplorationGraph",
           "Frontier",
           "Planner", "Worker", "Guard", "Retester", "TodoStore", "TaskStore",
           "ActivityLog", "TrafficLog", "ColdCompactor", "Budget", "RuntimeTracker",
           "InterceptQueue", "FindingService", "EvidenceStore", "Notifier",
           "TriggerStore", "LlmPool", "ToolCatalog", "SideQuestions", "CompanyScope",
           "TaskArchive", "TaskTemplate", "TaskCategory", "TaskChat",
           "TOOL_DEFAULTS", "constraint_block", "decompose_goals",
           "enrich_asset", "extract_scope_items", "extract_constraint_items",
           "finding_severity", "resolve_target", "load_intel_scores",
           "judge_command", "parse_judge_output", "settlement_prompt",
           "terminal_hint", "build_prompt_context"]
