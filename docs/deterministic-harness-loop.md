# Deterministic harness loop

Contract: the autonomous loop runs reproducibly in development. No LLM
guessing, one command per decision, attack paths solved from data, and
every foothold captured as a verifiable artefact.

## Layers

### Single-source state

`modules/killchain.py` is the only phase authority; `modules/factsio.py`
saves state snapshot-first and merges the network graph before the model
cache refresh. Consumers (intelligence_engine, compliance, misp_export)
read the canonical shape; nothing re-derives phases on its own.

### Beacon recon as a sink-outcome bus

`modules/beacon_recon.py` ingests Go-side port scans (`result_portscan`)
and discovery reports (`discovered_ips`), spooling into
`sessions/policy_facts.json`, `sessions/discoveries.jsonl` (idempotent
ledger keyed by host:port prefix), and `outcome_bus` events (kind
`discovery`). Sinks fan out to intel_graph and attack_graph.
`lazyc2` queues `discover:` on first check-in and one `portscan:` per
discovered host using `sessions/<safe_id>/c2/recon_state.json` markers.

### Golden path solver

`modules/golden_path.py` runs a severity-weighted Dijkstra from the
operator (anchors cost 0; exploit edges cost by severity; confirmed
credentials are credentials with confirmed=0.6; relationships are graph
relations). Resolver output persists to `sessions/attack_paths.json`
and each path becomes an `auto chain gym_ms2_foothold <target>`
objective queue line. Display helpers using underscore-prefixed node
labels are mildly syntactic; the same labels resolve across surfaces.

```text
golden_paths build | show | push          cli/commands/golden_paths.py
```

### Gym matrix + CTF capture

`modules/gym_matrix_runner.py` plans Metasploitable-2 exercises in
severity order and executes each one with `ChainRunner`, then
`modules/ctf_capture.py` verifies the chain outputs (root shell, shadow
dump, credentials, per-flag) and stores `sessions/ctf/<vuln>/record.json`
plus one `outcome_bus` `ctf_capture` event. The final CVE report merges
the records into `professional_report.py` findings
(`_collect_ctf_captures` / `_classify_ctf_captures`).

```text
gym_metasploitable plan | run | report | verify [--only <id>] [--dry-run]
```

### Chain hardening

`modules/chain_runner.py` seals a per-verb watchdog (`_run_shell_verb`)
with a SIGALRM timeout that reports `status: timeout` separately from
failures — verbs never hang the loop. `modules/chain_facts.py` spools
every step output into `sessions/chain_facts/<run_id>/<target>_<step>.txt`
and `FactStore` ingests them for path enumeration. LLM recovery in
`do_apt_chain` is opt-in (`--replan`) and therefore off by default.

### Harness gates

`modules/harness.py` exposes `harness_enabled()` (env
`LAZYOWN_HARNESS` in the payload's orchestrator section, or profile
`harness`) and `gate(name)`. Gated surfaces: `plan_llm`,
`worker_agentic`, and `worker_llm_steps` inside `lazy_loop.py`, along
with the SWAN/LLM streaming stages in the config. LLMs are locked to
local-only dev by the harness: `modules/llm_factory.py` blocks
groq/openai/anthropic/deepseek during the harness, so the fallback
`auto` escalates into ollama/llama.cpp as usual. Config lives in
`config/orchestrator.yaml` (profile `harness`) and the payload toggle
through `modules/orchestrator_config.set_harness` (also surfaced as a
lazy_orchestrator knob).

### Dual C2 client profiles

`modules/c2_agent.py` deploys two independent clients per box:
`msf-<slug>` (lowpriv) and `msf-<slug>-root`. Root deploys are restricted
to `ROOT_SHELL_EXPLOITS` primitives (`modules/atomic_exploit_bridge.py`)
and stage `/tmp/.sysagent-r` so an existing low-priv agent keeps running.
Command queues and beacon logs are separate per id. On the shell:

```text
c2_deploy <target> [--sleep 10] [--privilege lowpriv|root]
```

Chain defaults carry `privilege` (`chains/gym_ms2_foothold.yaml`), so a
root path can render `--privilege root` without editing the YAML.

### Toasts

`cli/toast_bus.py` renders textual-style notifications: severity icons
on every line, prominent events as rounded panels with a timestamp, and
sonner ephemeral toasts behind the `toast_ephemeral` payload flag
(auto-dismiss per duration).

## Tests

```text
pytest tests/test_single_source_of_truth.py \
       tests/test_beacon_recon_sink.py \
       tests/test_golden_path.py \
       tests/test_gym_matrix_ctf.py \
       tests/test_f4_hardening.py \
       tests/test_harness_mode.py \
       tests/test_opencode_mcp_harness.py \
       tests/test_c2_agent_dual.py \
       tests/test_toast_bus.py tests/test_toastr_unify.py
```

Read-menator follow-up: rebuild the KB after new module land (`readmenator . --rebuild`)
to sweep modules/beacon_recon, golden_path, gym_matrix_runner, ctf_capture,
harness, and llm_factory into INDEX/API.
