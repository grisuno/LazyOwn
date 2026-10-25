# Autonomous Operations: Contract Specifications

I describe the autonomous-operation contracts integrated into the
existing flows. Each contract maps to exactly one module file and one
integration point. I state scope, inputs, outputs, and acceptance
criteria so tests derive mechanically from this text.

## C01 Safety Gate

File: `modules/intercept.py`
Integrated at: `EngageOrchestrator._run_step` and `_run_objective`
in `skills/autonomous_daemon.py`
Nouns: `InterceptRule`, `PendingApproval`, `InterceptVerdict`,
`Interceptor`, `Guard`.
Verbs: `matches`, `evaluate`, `decide`, `check`, `record_failure`.
Scope: pre-execution gate for autonomous commands with actions
allow, deny, ask. Denied commands never execute and surface as
`STEP_DENIED` with the blocking rule. Asks route through the
existing operator approval flow and skip when unapproved.
Accept: destructive and exfiltration patterns ask by default,
priority order holds, expired asks resolve to deny.

## C02 Step Transcript

File: `modules/traffic_recorder.py`
Integrated at: `EngageOrchestrator._run_step` and `_run_objective`,
stored under `sessions/`
Nouns: `Exchange`, `TrafficRecorder`.
Verbs: `record`, `query`, `get_body`, `count`.
Scope: append-only exchange log of executed steps with file bodies
plus SQLite index, picked up by the sessions RAG like every other
sessions artefact.
Accept: record then query returns the exchange, body round-trips,
path traversal on get_body raises, count increments.

## C03 Evidence Vault

File: `modules/evidence.py`
Integrated at: `EngageOrchestrator._run_step` and `_run_objective`
finding write-back, blobs under `sessions/`
Nouns: `EvidenceStore`.
Verbs: `put`, `get`, `exists`, `garbage_collect`.
Scope: content-addressed SHA-256 vault for full step outputs. The
hash rides on finding dicts and lands in the campaign database refs.
Accept: put returns a stable hash, get verifies integrity, invalid
hash raises, unreferenced old blobs are collected.

## C04 Asset Graph

File: `modules/asset_graph.py`
Integrated at: campaign database plus world model via
`mirror_to_campaign`
Nouns: `AssetNode`, `ExplorationNode`, `Anchor`, `AssetGraph`.
Verbs: `upsert_asset`, `add_fact`, `add_finding`, `anchor`,
`coverage`, `mirror_to_campaign`.
Scope: deduplicated working graph of assets and exploration chains
joined by anchors. Persistence is the campaign database and the
world model, reached through the existing db_hosts and world model
surfaces.
Accept: same asset upserted twice yields one node, anchors resolve
both directions, mirror creates db hosts and world hosts.

## C05 Frontier and Todos

File: `modules/planner.py`, classes `Frontier`, `TodoList`
Integrated at: `_run_objective` step selection
Scope: the planner stays the sole intent generator. In the daemon
objective loop each step serves one queued intent, and an empty
refill with unchanged facts ends the objective instead of repeating
fallbacks. In the engage plan, steps with no new direction are
skipped visibly: duplicates of successful steps and scans already
held under `sessions/`. After the fixed plan, a changed world wakes
the planner for up to two extra intents mapped to LazyOwn verbs
through the bridge catalog (MITRE-aligned); an unchanged world
narrates `NO_NEW_DIRECTION` and adds nothing.
Accept: tried techniques never re-emit, lateral tactics wait for
the credential chain step, empty refills stop the loop.

## C06 Finding Lifecycle

File: `modules/finding_lifecycle.py`
Integrated at: campaign `vulns` table, surfaced by db_vulns,
vuln_list and the report flow
Scope: findings are campaign vulns with a `status:` marker in refs.
Retests append to `sessions/retests.jsonl`. Only a fixed conclusion
flips status automatically.
Accept: fixed retest flips status, other conclusions keep it,
markdown orders critical first.

## C07 Provider Pool

File: `modules/llm_pool.py`
Integrated at: `LLMSelector` in `skills/autonomous_daemon.py`
Nouns: `PoolMember`, `HealthRegistry`, `LLMPool`.
Verbs: `complete`, `report_success`, `report_failure`.
Scope: ordered failover across providers for command suggestions.
Failover happens only before the first token.
Accept: dead head falls to the next member, exhausted chain raises,
unhealthy members are skipped.

## C08 Notifier

File: `modules/notify.py`
Integrated at: `_run_objective` high-value findings, journal at
`sessions/notifications.jsonl`
Scope: severity filter plus secret redaction for finding events,
next to the existing event stream.
Accept: below-threshold severity drops, secrets mask, unknown
channel raises.

## C09 Isolated Questions

File: `modules/sidequestion.py`
Integrated at: `ask snapshot` in `cli/commands/ai.py`
Scope: questions answered from a frozen context snapshot without
touching session state.
Accept: asking without a snapshot raises, answers never mutate the
main loop.

## C10 Verified Updates

File: `modules/selfupdate.py`
Scope: SHA-256 verification, smoke test, staged swap and rollback
for the future `update` verb. No binary-release flow exists yet, so
this module stays a tested library until that verb activates.
Accept: bad checksum aborts without touching the live binary,
failed smoke aborts, rollback restores the previous binary.
