# Killchain Gap Contracts (v3 — full per-file contracts)

Relocated from `CLAUDE.md` §16 (single source of truth lives in
`modules/killchain.py`; every display surface consumes its `snapshot()`).
These are the full per-file contracts for the v3 killchain unification, the
API authorization and structured logging contracts, and the v3.1 feature
polish pass (UX + hardening + debt removal over the last 22 commits).

## 16. Killchain Gap Contracts (v3 — unified killchain)

Closing the gap between kill-chain phases so suggesters are effective and friction is eliminated. Each file is a single contract.

### `modules/killchain.py` — Single Source of Truth for Kill-Chain (NEW v3)

**Contract:** ``KillChain`` is the canonical authority for kill-chain data. Every display surface (CLI, Flask dashboard, GUI2, Textual TUI, tips engine, recommendation signals, MCP) imports from here. No other file defines its own phases.

**Key types:**
- ``KillChainConfig`` — Centralised constants: ``phases`` (8-tuple), ``phase_labels``, ``phase_colors`` (hex), ``phase_rich_colors``, ``engagement_to_cli`` mapping, ``cli_to_host_state`` mapping, ``compact_phases`` (5-tuple).
- ``PhaseStatus`` — Immutable ``(key, label, color, status)`` tuple for UI renderers.
- ``KillChain`` — Stateless class: ``current_phase()``, ``advance_phase()``, ``get_progress()``, ``phases_for_display()``.

**Phase resolution order:**
1. ``WorldModel.get_phase()`` (host states — canonical).
2. Raw JSON ``current_phase`` (operator override, only when higher rank).
3. Raw JSON ``phase`` (legacy fallback).
4. ``"recon"`` as safe default.

**``advance_phase()``** atomically writes ``current_phase``, ``phase``, and ``completed_phases`` into ``world_model.json`` AND advances all WorldModel hosts to the matching ``HostState``. Called by CLI ``phase`` command, C2 beacon handler, and autonomous daemon.

**6 consumers refactored:** ``cli/ops_commands.py``, ``modules/kill_chain_viz.py``, ``cli/killchain.py``, ``lazygui/panels/killchain_panel.py``, ``cli/tips_engine.py``, ``cli/dashboard_tui.py``.

**Tests:** ``tests/test_killchain_unified_v2.py`` (33 tests, 10/10 mutants killed).

### `lazygui/services/teamserver_backend.py` — Auto-Poll Beacon Results (NEW v3)

**Contract:** ``_results_timer`` polls ``/get_results`` every 3s. On new or changed output, emits ``beacon_result`` signal to ``TerminalPanel`` and ``BeaconCommandModal``.

**New timing constant:** ``beacon_results_poll_interval_ms: int = 3000``.

**Dead code removed:** ``_http_post_json()``, ``_post_global_command()``, ``_poll_command_output()`` (never called). Also removed ``read_and_forward_pty_output_c2()`` from ``lazyc2.py`` and commented-out shellcode form from ``templates/nav.html``.

### `lazygui/widgets/beacon_command_modal.py` — Beacon Command Modal (NEW v3)

**Contract:** ``Ctrl+J`` or ``File > Beacon Command`` opens a modal with beacon selector, command input, history list, and output viewer. Auto-updates via ``beacon_result`` signal.

### `cli/tips_engine.py` — Full Killchain Auto-Display (NEW v3)

**Contract:** After ``lazynmap``, ``auto_populate``, ``auto_pwn``, ``hunt``, or ``pwntomate``, shows the full killchain progress bar via ``_print_phase()`` (not just the compact 5-phase bar). Defined in ``_FULL_KILLCHAIN_TRIGGERS``.

### `modules/world_model.py` — Engagement State Tracking

**Contract:** Persist host states (UNSCANNED → OWNED), credentials, vulnerabilities, and network graph. Derive engagement phase from aggregate host states. Thread-safe with RLock.

**New methods (v2):**
- `set_os_hint(ip, os_hint)` — Set OS hint for a host (auto-called by C2 on beacon connect and by `do_ping`).
- `get_host(ip)` → `HostEntry | None` — Query a single host entry.
- `get_hosts_summary()` → `dict[str, str]` — IP → state mapping for all hosts.

**Phase derivation:** `max(host.state)` → engagement phase. All OWNED → COMPLETE.

**Tests:** `tests/test_world_model_extended.py` (7 tests)

### `modules/conditional_hooks.py` — Beacon Automation Triggers

**Contract:** Match events against operator-defined rules and execute actions (run_command, run_local, notify, credential_reuse_check). Supports platform filtering and cooldown.

**New in v2:**
- `_contains` suffix keys for substring matching (case-insensitive).
- Case-insensitive exact matching for string trigger values.
- Case-insensitive list matching.
- `run_local` action type — executes commands on the C2 server (subprocess).
- Hook action handler wiring in `lazyc2.py` — queues beacon commands via `cmd_<client_id>.json`.

**New default rules:**
| Rule | Trigger | Action |
|------|---------|--------|
| `auto-privesc-on-beacon-linux` | beacon_connected + linux | Queues linpeas download+exec |
| `auto-privesc-on-beacon-windows` | beacon_connected + windows | Queues winPEAS download+exec |
| `auto-crystal-ball-on-peas-output` | command_executed containing linpeas | Notifies to run crystal_ball |
| `auto-crystal-ball-on-winpeas-output` | command_executed containing winpeas | Notifies to run crystal_ball |
| `auto-loot-on-owned` | host_owned | Queues lazydump + netstat + arp |

**Tests:** `tests/test_conditional_hooks_extended.py` (11 tests)

### `cli/recommendation_signals.py` — KillchainGapSignal

**Contract:** `KillchainGapSignal` inspects `world_model.json` host states and detects missing steps in the kill chain. Returns `Proposal` objects with high confidence (0.85-0.95 weight).

**Gap detection rules:**
| Condition | Recommendation | Category |
|-----------|---------------|----------|
| Host EXPLOITED, no privesc | linpeas / winpeas (OS-aware) | privesc |
| Host OWNED, no credentials | lazydump | cred |
| Scan exists, no enumeration | gobuster | enum |
| Credentials exist, no lateral | crackmapexec | lateral |

**Weight:** 0.8 in `EngineWeights.signal_weights` (second only to RECON at 1.0).

**Tests:** `tests/test_killchain_gap_signal.py` (12 tests)

### `cli/tips_engine.py` — Phase Derivation + OS Hint (v3 refactored)

**Contract:** ``_resolve_phase()`` now derives phase from ``modules.killchain.KillChain.current_phase()`` as canonical source. ``_read_os_id_from_session()`` reads OS from ``sessions/os.json`` as fallback when ``payload.json`` has no ``os_id``. ``_derive_phase_from_hosts()`` removed (dead code — replaced by KillChain).

**New methods:**
- ``_read_os_id_from_session()`` — Reads ``os.json`` for Linux/Windows detection.
- ``_render_killchain_progress()`` — Compact killchain progress bar ``[R>E>X>P>L]``.
- ``_maybe_show_full_killchain(cmd)`` — Shows full killchain after ``lazynmap``, ``auto_populate``, ``auto_pwn``, ``hunt``, ``pwntomate``.
- ``_check_badges()`` — ``first_owned`` badge when world_model contains OWNED hosts.

### `lazyc2.py` — World Model + Killchain Advancement on Beacon Events (v3 refactored)

**Contract:** On ``beacon_connected`` → advance host to ``EXPLOITED`` + call ``KillChain.advance_phase("exploit")``. On privesc detection (uid=0/root/System) → advance to ``OWNED`` + call ``KillChain.advance_phase("privesc")`` + fire ``host_owned`` event.

**Detection patterns:** ``uid=0(root)``, ``NT AUTHORITY\SYSTEM``, ``user == "root"``.

**Dead code removed:** ``read_and_forward_pty_output_c2()`` (never started as background task).

### `cli/commands/privilege_escalation.py` — New Commands

| Command | Purpose |
|---------|---------|
| `whoami_priv` | OS-aware privilege enumeration (id, sudo -l, whoami /priv) |
| `sudo_privesc` | Analyse sudo -l output with GTFOBins parquet |
| `printspoofer` | Serve PrintSpoofer64.exe over HTTP |
| `juicypotato` | Serve JuicyPotato.exe over HTTP |

### `cli/reactive_hints.py` — Updated Tables

`_KILL_CHAIN_NEXT` extended with entries for `whoami_priv`, `sudo_privesc`, `printspoofer`, `juicypotato`, `crystal_ball`.
`_PHASE_PRIORITY["privesc"]` includes all new commands.

### `cli/command_chain.py` — Updated Prerequisites

Added prerequisites: `whoami_priv:(ssh,)`, `crystal_ball:(linpeas,)`, `printspoofer:(evil-winrm,)`, `juicypotato:(evil-winrm,)`.

### `cli/tips_engine.py` — Updated ELO Table

ELO bonuses: `juicypotato:20`, `sudo_privesc:20`, `whoami_priv:10`, `crystal_ball:18`.

---

## 16.1 Unified kill-chain contract (single source of truth)

**Canonical state:** `modules/killchain.py` is the only component that computes the
kill-chain. Every display surface (CLI `/killchain`, Flask `/api/killchain`,
C2 `/api/data`, `/api/dashboard`, GUI2 `KillChainPanel`) consumes
`KillChain.snapshot()` — a single render-agnostic, JSON-serializable payload:

```python
{
  "current_phase": "recon",
  "completed_phases": [],
  "progress": [{"key": "recon", "label": "Recon", "color": "...", "status": "..."}],
  "host_states": [], "compact": "...", "updated_at": "ISO8601"
}
```

**I/O transport:** `modules/world_model.py` owns all session state reads/writes.
`read_state_dict()` transparently decrypts `sessions/world_model.json.encrypted`
(left as plaintext `.json` while a surface is running), so the snapshot always
reflects the real persisted state — no surface should ever guess a phase.

**Beacon history:** `modules/beacon_history.py` appends one JSONL record per
beacon result to `sessions/<client>.records.jsonl` (pathworld-safe). `lazyc2`
delegates all beacon record I/O to this single module.

**HTTP surface:**
- `GET /api/killchain` — snapshot (auth + limiter).
- `GET /api/beacon_results/<client_id>` — JSONL beacon history (auth + limiter).
- `GET /api/data` and `GET /api/dashboard` — include both `killchain` and
  `beacon_records`.

**CLI command:** `/killchain` prints the snapshot; `/killchain auto on|off|N`
toggles live auto-refresh. Flags `killchain_auto_every` and
`killchain_auto_on_phase_change` live in `payload.json`.

**C2 run-time state:** `lazyc2.py` decrypts session files on boot and re-encrypts
on clean exit (same derived key as the CLI), so beacons can decrypt `key.aes`
and the kill-chain reflects the true phase while the server runs.

**Test contract:** `tests/test_killchain_snapshot.py`,
`tests/test_beacon_history.py`, `tests/test_killchain_auto_refresh.py`.
Mutation gate: `tests/run_mutation_killchain.py` (no surviving mutants).

---

## 16.2 Command queue path confinement (`_secure_command_queue_path`)

**Contract:** ``_secure_command_queue_path(client_id)`` in ``lazyc2.py`` is the single
authority for building safe command-queue file paths for beacons. Every read/write
of ``cmd_<client_id>.json`` goes through it.

**Pipeline:**
1. Sanitise ``client_id`` via ``modules.beacon_history.sanitize_client_id`` (only
   ``[a-zA-Z0-9_-]`` survive).
2. Reject empty sanitised ids with ``ValueError``.
3. Join with ``ALLOWED_DIRECTORY`` → ``cmd_{safe_id}.json``.
4. Resolve with ``os.path.realpath`` (handles symlink escapes).
5. Verify the resolved path starts with ``os.path.realpath(ALLOWED_DIRECTORY) + os.sep``.
6. Return the validated absolute real path.

**CodeQL rationale:** The combination of character-level sanitisation + ``realpath``
path confinement makes CodeQL's taint-tracking recognise the result as safe for use
in ``open()``, ``os.path.isfile()``, and ``json.load/dump``. The ``+ os.sep`` guard
prevents prefix-matching bypasses (e.g. ``/tmp/sessions`` matching ``/tmp/sessions-backdoor``).

**Consumers (3 call-sites refactored):**
- ``send_command()`` GET handler — auto-privesc queue on first GET (was inline, now uses helper).
- ``send_command()`` else-branch — dequeue next command for the beacon (was inline with own check, now DRY'd).
- ``receive_result()`` POST handler — queue privesc on first check-in (was inline, now uses helper).

**Duplicated sanitization removed:** The inline ``''.join(c for c in str(client_id) if c.isalnum() or c in '-_')``
pattern existed in 3 places. All unified behind the single helper.

**Dead variants removed:**
- Inline ``sanitized = ''.join(...)`` → ``_queue_path = os.path.join(ALLOWED_DIRECTORY, ...)``
  at 2 call-sites without ``realpath`` confinement (CodeQL alerts #843-#848).

**Tests:** ``tests/test_security_lazyc2.py::TestSecureCommandQueuePath`` (6 tests).
**Mutation gate:** 3 mutant classes killed (empty-check removal, confinement-check removal, missing-os.sep bypass).

---

## 16.3 Phase 1 Data-Gap Closure Contracts (NEW)

Closing five critical data-flow gaps where information was collected but not
consumed. Each contract is a single file or a targeted fix in an existing module.

### ``modules/obs_parser.py`` — Finding.metadata + _ServiceVersionExtractor + _EmailExtractor

**Contract:** ``Finding`` carries an optional ``metadata: dict[str, Any]`` so
extractors can pass structured data (port, protocol) alongside the string
``value``. ``_ServiceVersionExtractor`` now captures ``port`` and ``protocol``
in metadata (was lost before — only ``name version`` string was stored).
``_EmailExtractor`` is a new extractor that finds email addresses in tool output
and emits ``FindingType.EMAIL`` findings. Registered in ``ObsParser.__init__``.

**Before:** NMAP service port/protocol lost on ObsParser output; emails ignored.
**After:** Structured service data flows through Finding -> WorldModel.add_service();
emails flow through Finding -> WorldModel.add_email().

**Tests:** ``tests/test_phase1_data_gaps.py::TestFindingMetadata`` (2),
``TestServiceVersionExtractor`` (4), ``TestEmailExtractor`` (4),
``TestObsParserIncludesEmailExtractor`` (2).

### ``modules/world_model.py`` — EmailEntry, DomainEntry, Corrected Handlers, consume_policy_facts

**Contract:** Three new value objects: ``EmailEntry``, ``DomainEntry``. Three
new public methods: ``add_email()``, ``add_domain()``, ``consume_policy_facts()``.
``update_from_findings()`` corrected:

| Finding type | Before (broken) | After (fixed) |
|---|---|---|
| ``service_version`` | Extracted parts to local variables, stored as unstructured note | Calls ``add_service(host, port, name, version, protocol)`` using port/protocol from ``metadata`` |
| ``domain`` | Silently dropped | Calls ``add_domain(value, host=host)`` |
| ``email`` | Silently dropped | Calls ``add_email(value, host=host)`` |
| ``error`` | Silently dropped | Calls ``add_note(host, f"error: {value}")`` or sentinel host for global errors |

**``consume_policy_facts()``** reads ``sessions/policy_facts.json`` (FactStore output)
and ingests hosts, services, credentials, vulnerabilities, domains, and emails into
the WorldModel, closing the FactStore-WorldModel divergence gap. Returns ingested
count. Thread-safe.

**Persistence:** ``_save()``, ``_load()``, ``reset()``, ``snapshot()``, and
``to_context_string()`` all updated to carry emails and domains through the
full lifecycle.

**Tests:** ``tests/test_phase1_data_gaps.py::TestEmailAndDomainEntries`` (2),
``TestWorldModelEmailDomain`` (3), ``TestUpdateFromFindings`` (6),
``TestConsumePolicyFacts`` (4), ``TestWorldModelPersistence`` (4).

### ``cli/recommendation_signals.py`` — GraphTopologySignal

**Contract:** ``GraphTopologySignal`` reads ``pivot_candidates`` (degree centrality
from WorldModel NetworkGraph) and emits lateral-movement / credential-spray
``Proposal`` objects. Previously the ``pivot_candidates()`` data was computed
but never consumed by the recommendation engine. Now it feeds directly into
``build_default_engine()``.

**Node handling:**
- ``host:<ip>`` → ``crackmapexec smb <ip>`` proposals (category: lateral)
- ``cred:<prefix>`` → ``credential_spray`` proposals (category: lateral)
- ``service:<name>`` → ``enum_<name>`` proposals (category: enum)

**Fallback centrality computation:** When no precomputed ``pivot_candidates``
exist in the snapshot but ``network_graph`` data is available, computes
degree centrality independently.

**Tests:** ``tests/test_phase1_data_gaps.py::TestGraphTopologySignal`` (5).

### ``modules/autonomous_exploit_engine.py`` — Credential-Aware Exploit Retry

**Contract:** ``AutonomousExploitEngine.retry_with_credentials(target, credentials)``
re-executes the exploit chain using newly-captured credentials. When credentials
are discovered and stored in the WorldModel, this method re-ranks exploit
candidates via ``_credential_aware_rank()`` which boosts strategies usable with
available credentials:

| Credential type | Strategy boost |
|---|---|
| Plaintext (user+pass) | ``brute_force`` ×2.5, ``credential_reuse`` ×3.0, ``null_session`` ×2.2 |
| Hash only | ``brute_force`` ×1.8 |
| Any | All ``requires_auth`` candidates ×2.0 |

**Before:** Credentials stored in WorldModel but never triggered re-exploitation.
**After:** When credentials arrive via ``update_from_findings`` or
``consume_policy_facts``, the engine can re-attempt previously-failed exploits
with authentication.

**Tests:** ``tests/test_phase1_data_gaps.py::TestCredentialAwareRetry`` (4).

### Mutation Gate

**Runner:** ``tests/run_mutation_phase1.py`` — 8 mutants covering all four gaps.
Each mutant reverts the fix (e.g., ``service_version`` back to ``add_note``,
domain handler removed, credential boost neutralized) and verifies at least
one test fails.

**Results:** 8/8 mutants killed (0 survived).

---

## 16.4 Killchain Unification — Single Source Enforcement (NEW)

**Contract:** Every consumer that needs the current kill-chain phase MUST call
``KillChain.current_phase()`` or ``KillChain.snapshot()``. Reading raw
``world_model.json`` keys (``"phase"``, ``"current_phase"``) directly is
**forbidden** — it produces inconsistent values across surfaces because those
keys can carry either EngagementPhase or CLI-phase vocabulary.

**Consumers fixed (6 files, 8 locations):**

| File | Before | After |
|------|--------|-------|
| ``cli/ops_commands.py:render_target_bar`` | ``world.get("phase") \|\| world.get("current_phase")`` | ``read_phase()`` (delegates to KillChain) |
| ``cli/dashboard_tui.py:render_content`` | ``get_world_model().get_phase()`` + raw JSON fallback | ``KillChain.current_phase()`` |
| ``cli/dashboard_tui.py:_cycle_phase`` | Raw JSON + ``_PHASES`` | ``KillChain.current_phase()`` + ``KillChain.phase_order()`` |
| ``skills/lazyown_mcp.py`` (2x) | Raw ``wm.get("current_phase")`` | ``KillChain.current_phase(world_model_path=...)`` |
| ``cli/commands/ai.py`` | Raw ``world.get("phase")`` | ``KillChain.current_phase()`` |
| ``cli/recon_plan.py:_resolve_phase`` | ``payload.get("phase")`` | ``KillChain.current_phase()`` with payload fallback |
| ``modules/opsec_scorer.py`` | Raw ``payload.get("current_phase")`` | ``KillChain.current_phase()`` with payload fallback |

**Also wired into runtime:**

| Contract | Where | Trigger |
|----------|-------|---------|
| ``consume_policy_facts()`` | ``cli/commands/mcp_bridge.py:auto_populate`` | After nmap XML parsing |
| ``retry_with_credentials()`` | ``skills/lazyown_mcp.py`` (2x) | After ``update_from_findings`` detects credential/hash findings |

**Security fix:** ``/push_notification`` route now has ``@requires_auth``,
input size limit (4096 bytes), HTML sanitization via ``sanitize_html``,
atomic writes via ``os.replace``, and ``try/except`` around file I/O.
``load_notifications()`` handles corrupted/malformed JSON.

---

## 16.5 API Authorization & Health Contracts (NEW)

### `core/api_authz.py` — Tenant-Bound API Key Authorization

**Contract:** ``ApiKeyStore`` manages SHA-256-hashed API keys scoped to tenants.
``require_api_auth`` decorator enforces key validation, permission checks, and
tenant membership on Flask routes. Keys are never stored in plaintext; the
one-time secret is returned only at creation.

**Key types:**
- ``ApiAuthzConfig`` — centralised settings: token header name, query param,
  bearer prefix, default bytes, max keys per tenant, rotation grace period,
  seconds per day.
- ``ApiKey`` — immutable record: hash, tenant_id, label, permissions (frozenset),
  expiration, last_used, retired_at. ``has_permission()`` /
  ``has_all_permissions()`` for set-based checks. ``is_expired()`` for TTL
  enforcement. ``is_retired()`` marks a rotated key inside its grace window.
- ``ApiKeyStore`` — persistence with atomic ``.tmp + os.replace`` writes.
  ``create_key`` returns ``(ApiKey, plaintext_token)`` — caller displays token once.
  ``validate_key`` hashes input, looks up record, checks expiration AND rotation
  grace, updates ``last_used_at``, and lazily prunes retired keys whose grace
  window closed. ``revoke_key`` removes every record with a label (active and
  retired). ``rotate_key`` retires the old key (valid for
  ``key_rotation_grace_seconds``), copies permissions and expiration from the
  rotated record — never from an arbitrary record — and returns the new
  plaintext. ``list_keys`` hides retired keys.
- ``require_api_auth`` — decorator extracts key from ``Authorization: Bearer``,
  ``X-API-Key`` header, or ``api_key`` query param. Sets ``g.api_key_record``
  and ``g.api_tenant_id`` on success. Returns 401/403 as JSON bodies (never
  ``abort()``) so the contract holds even with ``TRAP_HTTP_EXCEPTIONS`` on.
  ``require_tenant`` defaults from ``ApiAuthzConfig.require_tenant_scope``.

**Security properties:**
- SHA-256 hashing with ``hmac.compare_digest`` for constant-time verification.
- Atomic writes prevent corrupted key stores.
- Max-keys-per-tenant prevents DoS via key exhaustion (retired keys pruned
  before counting).
- Rotation grace window keeps live clients working during key rotation, then
  the retired key is rejected and pruned.
- ``_read`` drops non-dict records and records without ``key_hash``.

**Tests:** ``tests/test_api_authz.py`` (34 tests, including rotation
permissions regression and grace-period behaviour). **Mutation gate:**
``tests/run_mutation_api_authz.py`` (7/7 mutants killed).

### `core/logging.py` — Structured JSON-Lines Logging

**Contract:** Drop-in replacement for ``core.console.print_msg`` / ``print_warn`` /
``print_error``. Every call produces both ANSI-coloured console output AND a
machine-parseable JSON line written to a rotating file. ``StructuredLogConfig``
centralises every tunable; no magic values elsewhere.

**Key types:**
- ``StructuredLogConfig`` — level, json_output toggle, log directory, rotation
  size/count, console/file enablement, redacted fields (frozenset).
- ``_JsonLineFormatter`` — emits ``{"timestamp": "...", "level": "...", "logger":
  "...", "message": "...", ...extra_kwargs}``. Sensitive fields in
  ``redacted_fields`` are replaced with ``[REDACTED]``. Includes exception
  traceback when ``exc_info`` is set.
- ``_ConsoleFormatter`` — ANSI-coloured output matching ``core.console`` style
  for operator CLIs.
- ``StructuredLogger`` — subclass of ``logging.Logger`` that promotes ``extra``
  kwargs to top-level JSON fields via ``_extra_`` prefixed record attributes.
- ``get_logger(name)`` — cached factory; subsequent calls return the same instance.
- ``install_json_handler(name, config)`` — idempotent wiring. Cold loggers get
  the standard console + file wiring; warm loggers keep every pre-existing
  handler and only append the JSON file handler (no ``handlers.clear()``).
- ``reconfigure(config)`` — replaces global config and refreshes all cached loggers.

**Usage pattern:** ``_log = get_logger("lazyc2.api"); _log.info("beacon checked in", extra={"client_id": "abc", "rhost": "10.0.0.5"})``

**Tests:** ``tests/test_structured_logging.py`` (13 tests, including the
handler-preservation contract). **Mutation gate:**
killed via ``run_mutation_api_authz.py`` (redaction bypass killed).

### `lazyc2/blueprints/api.py` — Health-Check Endpoints (enforced)

**Contract:** ``/api/health`` returns JSON subsystem status (database, listeners,
beacons, uptime). ``/api/ping`` is a liveness probe. ``/api/health/tenant`` is
protected by ``require_api_auth_with_store``: it requires a tenant-scoped API
key (resolved from ``app.config["lazyown_api_key_store"]``, seeded by
``lazyc2/app_factory.py`` from ``payload.json`` ``api_keys_path``) and returns
401/403 JSON when the key is missing, invalid, or not tenant-scoped.

**Health states:** ``healthy`` (all components ok), ``degraded`` (beacon count at
threshold), ``unhealthy`` (any required component unavailable).

**Config:** ``HealthConfig`` dataclass with ``required_components`` tuple and
``degraded_threshold_beacons`` integer.

---

## 16.6 Feature Polish Contracts (v3.1 — UX + hardening + debt removal)

SDD+TDD+BDD pass over the features added in the last 22 commits. Every
change below ships with tests and a mutation gate. Contracts are one file
each; no magic numbers, no silent failures, no raw ANSI in rich surfaces.

### `cli/noise_verbs.py` — Canonical Non-Actionable Verb Registry (NEW)

**Contract:** Single source of truth for the near-identical skip lists used by
the inline hints, the tips engine, and the chain prompt. Each surface composes
its exported set from ``BASE_NOISE_VERBS`` plus its extras
(``HINTS_EXTRA_VERBS``, ``TIPS_EXTRA_VERBS``, ``CHAIN_EXTRA_VERBS``). The three
surfaces can never drift apart again; exported names
(``SKIP_COMMANDS`` / ``CHAIN_SKIP_VERBS``) are unchanged.

### `cli/reactive_hints.py` — Evidence Hints + DRY Command Hints

**Contract changes:**
- ``confidence_from_score`` now floors instead of rounds: confidence lives in
  ``[0, 99]`` and never displays a dishonest 100%.
- ``command_hints`` / ``render_command_hints`` share one
  ``_collect_command_hints`` implementation; the dead ``limit * 2`` overscan
  in the render path is gone (output was sliced to ``limit`` anyway).
- ``read_run_commands(sessions_dir)`` is now public and shared with
  ``cli/tips_engine.py`` (one transcript parser, not two).

### `cli/chain_mode.py` — Chain Prompt UX + Safe Store

**Contract changes:**
- An out-of-range numeric choice re-prompts instead of silently skipping;
  the whole read/interpret loop lives in ``_prompt_loop``.
- Terminal control bytes are named module constants (``KEY_ESC``,
  ``KEY_CTRL_C``, ...); the menu prompt moved into ``ChainModeConfig``.
- ``ChainModeStore`` logs read/write failures via the ``cli.chain_mode``
  logger instead of swallowing them silently. Writes stay atomic
  (``mkstemp`` + ``os.replace``).

### `cli/tips_engine.py` — Rich Rendering + Config-Driven Killchain Display

**Contract changes:**
- All raw ANSI escape rendering (curiosity reveal, karma up, badges, VRI
  rewards) replaced by rich ``Text`` composition; separator widths, phase
  labels, and streak labels are module constants.
- ``TipsConfig.killchain_display`` is a real config field (callable or
  ``None``); the engine no longer uses ``getattr`` on the dataclass.
- ``render_session_start`` renders registry tips as plain rich ``Text`` so
  tip content containing markup brackets cannot break the render pass;
  curated ``session_tips`` keep their markup.
- VRI reward selection degrades to uniform when the weight vector is void
  (``random.choices`` rejects all-zero weights).
- ``_compute_command_hints`` no longer overscans; ``_compute_evidence_hints``
  overscan uses ``EVIDENCE_OVERSCAN_FACTOR``.

### `cli/recommendation_signals.py` — Shared World-Model Loader + Named Constants

**Contract:** ``_load_world_model(sessions_dir)`` is the single reader shared by
``KillchainGapSignal`` and ``GraphTopologySignal``. Gap weights, topology
multipliers, the neighbor cap, the owned-host cap, and the playbook description
limit are named module constants. ``PlaybookSignal`` skips non-dict entries
instead of raising.

### `lazyc2/addon_creator.py` — Secure Atomic Persistence

**Contract:** ``AddonStore.save`` writes through ``tempfile.mkstemp`` with the
store file mode applied via ``os.fchmod`` before the first byte is written,
flushes + fsyncs, then ``os.replace`` promotes the file — no reader can ever
observe a permissive partial document. YAML dump width moved to
``AddonCreatorConfig.yaml_width``.

### `core/api_authz.py` — Rotation Grace + Decorator Hardening

See section 16.5. New in this pass: the rotation grace window is actually
implemented (previously documented but revoked immediately), the
``rotate_key`` permissions bug (copied from an arbitrary record) is fixed,
and the decorator returns JSON instead of ``abort()``.

### `cli/engagement_hooks.py` — Store Bound to Module Contract

**Contract:** ``_sync_user_elo`` writes through an ``RBACStore`` bound to the
module's own ``USERS_PATH`` instead of the global singleton, so redirected
paths (tests, alternate deployments) are honoured. The test suite stubs
``modules.cli_auth.get_current_operator`` so results never depend on host
login state.

**Test/mutation status for this pass:**
- ``tests/test_chain_mode.py`` 62 passed (re-prompt contract).
- ``tests/test_evidence_hints.py`` 60 passed with tips engine (99-confidence
  contract).
- ``tests/test_api_authz.py`` 34 passed; ``run_mutation_api_authz.py``
  7/7 mutants killed.
- ``tests/test_addon_creator.py`` 71 passed; ``run_mutation_addon_creator.py``
  9 killed / 0 survived.
- ``tests/test_structured_logging.py`` 13 passed (handler-preservation).
- ``tests/test_engagement_elo_and_methodology.py`` 45 passed (was 4 failing
  due to host login state — now deterministic).
- ``run_mutation_killchain.py`` 4/4 killed.

---

