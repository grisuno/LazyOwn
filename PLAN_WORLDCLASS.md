# LazyOwn — World-Class Improvement Plan

Status: draft | Last updated: 2026-05-21

This document diagnoses the gap between "feature-complete" and "world-class" in terms of operator effectiveness and usability. Each item has a priority, a success metric, and an owner (default: open).

---

## 1. Architecture & Code Quality

### 1.1 Break the CLI Monolith (P0)

**Problem**: `lazyown.py` is 29,757 lines, 467 `do_*` methods, 1 class. It is unmaintainable.
**Impact**: Code review paralysis, impossible unit testing, contributor onboarding blocked, IDE lag.
**Metric**: `lazyown.py` < 2,000 lines; every command lives in `cli/commands/<phase>.py`.

**Plan**:
1. Define command categories by kill-chain phase: `recon.py`, `enum.py`, `exploit.py`, `postexp.py`, `privesc.py`, `cred.py`, `lateral.py`, `exfil.py`, `c2.py`, `report.py`.
2. Migrate 467 methods in batches of 50. Each batch is a standalone PR.
3. The main file becomes a thin router: imports all CommandSets and registers them with cmd2.
4. `cli/commands/_base.py` already exists; extend it with a `BaseCommandSet` that every phase inherits.

**Reference**: `cli/commands/` already holds 41 commands. Scale that pattern.

### 1.2 Enforce Linting on 100 % of Python Code (P0)

**Problem**: `tests/test_lint_quality.py` skips `lazyown.py`, `lazyc2.py`, and all of `modules/`. Dead code, inconsistent style, and circular imports accumulate silently.
**Metric**: `ruff check .` and `ruff format --check .` pass at CI with zero exclusions.

**Plan**:
1. Add `modules/`, `lazyown.py`, `lazyc2.py` to `LINT_TARGETS` and `FORMAT_TARGETS`.
2. Run `ruff check modules/ lazyown.py lazyc2.py --statistics` to get a violation histogram.
3. Fix the top 5 violation types in bulk (usually unused imports, bare excepts, line length).
4. Gate merges on the full-project lint.

### 1.3 Introduce Static Type Coverage Gates (P1)

**Problem**: Public APIs in `modules/` and `skills/` lack type hints. LLM agents (Hermes, Claude Code) hallucinate parameter shapes.
**Metric**: `mypy --strict` passes on `core/`, `cli/`, `modules/`, `skills/`.

**Plan**:
1. Add `mypy` to dev dependencies.
2. Start with `core/` and `modules/world_model.py` (already dataclass-heavy, easy win).
3. Generate stub files for `cmd2` if missing.
4. CI gate: mypy must pass on modified files.

---

## 2. Operator Effectiveness (The "Lazy" Promise)

### 2.1 Proactive Prompt Context (P0)

**Problem**: The operator must remember the active target, phase, and credentials. Cognitive load is high at 3 AM.
**Metric**: The shell prompt always shows: `[phase/target/creds_count] lazyown>`.

**Plan**:
1. Override `cmd2.Cmd.prompt` to read from `world_model.json` and `payload.json` on every loop.
2. Color-code phases: recon=cyan, enum=yellow, exploit=red, postexp=green.
3. If `c2_notes` has unread entries, append a subtle `(*3)` indicator.

### 2.2 Auto-Suggest Next Action Inline (P0)

**Problem**: `recommend_next` exists but the operator must remember to call it.
**Metric**: After every command execution, the CLI prints 1 line: "Next: <cmd> (confidence: 87%) — <reason>".

**Plan**:
1. Hook into `PostcommandData` (already imported in `lazyown.py`).
2. Cache the last recommendation to avoid API spam; refresh every N minutes or after state changes.
3. Make it toggleable via `set autosuggest on|off`.
4. If Groq is unreachable, fall back to `graph_suggest_next` (local, offline).

### 2.3 Expand Pre-Built Playbooks from 4 to 30 (P1)

**Problem**: Only 4 YAML pipelines exist. Operators must remember sequences manually.
**Metric**: One pipeline per common vector: web-initial-access, linux-privesc-suid, linux-privesc-sudo, windows-privesc-seimpersonate, ad-kerberoast, ad-asreproast, ad-bloodhound, mqtt-exploit, snmp-enum, etc.

**Plan**:
1. Audit the top 20 commands in `LazyOwn_session_report.csv` (most used).
2. Group them into 15-30 playbooks by attack vector.
3. Each playbook must declare `prerequisites`, `estimated_time`, and `risk_level`.
4. Add a `do_playbook` alias so `playbook linux-privesc` is discoverable.

### 2.4 World Model Auto-Inference (P1)

**Problem**: The operator must manually interpret nmap banners (TTL, service versions, open ports).
**Metric**: After `auto_populate`, the world model stores inferred fields: `os_family`, `os_distribution`, `kernel_approx`, `confidence`.

**Plan**:
1. Extend `modules/obs_parser.py` with an `InferenceEngine`.
2. Rules: TTL 64 -> Linux; TTL 128 -> Windows; Apache 2.4.49 -> Ubuntu 22.04 probable; etc.
3. Store inferences as `inferred_*` keys, separate from `detected_*`, with a confidence float.
4. Surface inferences in `facts_show` and `campaign_sitrep`.

### 2.5 Graceful Degradation & Prerequisite Auto-Install (P1)

**Problem**: A command fails because `bloodhound-python`, `impacket`, or `neo4j` is missing. The operator must context-switch to `apt install`.
**Metric**: 80 % of "command not found" failures auto-resolve within 30 seconds.

**Plan**:
1. Maintain a `TOOLS_MANIFEST` mapping: command -> system package / pip package / github repo.
2. Before executing a command, check prerequisites via `shutil.which()`.
3. If missing, prompt: `<tool> is missing. Install via apt/pip? [Y/n]`.
4. In daemon/auto mode, auto-install after logging the action.

---

## 3. Usability & Onboarding

### 3.1 First-Run Zero-Config Wizard (P0)

**Problem**: New operators must manually edit `payload.json` and know what `lhost` means.
**Metric**: First launch detects VPN IP, suggests wordlist paths, and validates connectivity in < 60 seconds.

**Plan**:
1. On first run (no `payload.json` or all keys empty), auto-launch `run_wizard`.
2. Detect `tun0`/`eth0` IPs and pre-fill `lhost`.
3. Check `/usr/share/wordlists/` presence and suggest `rockyou.txt` / `directory-list-2.3-medium.txt`.
4. Validate with a `ping` to `rhost` before finishing.

### 3.2 Rich Structured Output (P1)

**Problem**: Raw nmap XML, raw gobuster output, and raw shell text flood the terminal. Operators scroll to find the signal.
**Metric**: Every recon/enum command that produces structured data renders as a Rich table or collapsible panel.

**Plan**:
1. Adopt `rich` library (already common in Python CLI tools).
2. `lazynmap` output -> Rich table: Port | Service | Version | State | Vuln hint.
3. `gobuster` output -> Live progress table + final summary.
4. `facts_show` -> Rich panels per host, grouped by phase.
5. Keep raw output always available in `sessions/`, but surface the summary.

### 3.3 Consistent Error UX with Actionable Hints (P1)

**Problem**: Errors are inconsistent. Some crash with traceback, others print "failed" with no next step.
**Metric**: 100 % of command failures print: (1) what failed, (2) why, (3) what to do next.

**Plan**:
1. Standardize on a `LazyOwnError` hierarchy in `core/errors.py`.
2. Every `do_*` method wraps execution in a try/except that maps exceptions to `LazyOwnError`.
3. Error handler prints: `[ERROR] <msg>` + `[HINT] <next_cmd>` or `[HINT] Check sessions/<file>.log`.

### 3.4 Interactive Command Discovery (P2)

**Problem**: 333 commands are discoverable via `help`, but the operator needs to know the name first.
**Metric**: An operator can type `find web login brute` and get a ranked list of relevant commands.

**Plan**:
1. Index all `do_*` docstrings into a local ChromaDB or even a simple inverted index JSON.
2. `do_find` (or `search`) takes natural language, returns top-5 commands with descriptions.
3. Use the existing `cli/reactive_hints.py` infrastructure.

---

## 4. Intelligence & Autonomy

### 4.1 Close the SWAN Feedback Loop (P1)

**Problem**: SWAN (Mixture-of-Experts + RL) routes tasks to Groq/Ollama, but there is no explicit reward signal when an expert succeeds or fails.
**Metric**: `swan_status` shows per-expert win rate, and the router improves accuracy by > 10 % over 100 tasks.

**Plan**:
1. After every `swan_run` or `groq_agent` task, record outcome: `success`, `partial`, `failure`.
2. Update Q-values in `sessions/swan_qtable.json` (or SQLite).
3. Reward signal: success = +1, credential found = +5, high-value event = +10, failure = -1.
4. Periodic epsilon-greedy exploration to avoid local optima.

### 4.2 Campaign Lesson Injection (P2)

**Problem**: `campaign_lessons.jsonl` accumulates insights, but `recommend_next` and `auto_loop` do not read it.
**Metric**: If a past campaign on a Windows host found that `evil-winrm` worked better than `psexec`, the recommender biases toward `evil-winrm` on future Windows targets.

**Plan**:
1. Add a `lessons` field to the recommender prompt context.
2. Filter lessons by `topic` and `tags` matching current target OS/services.
3. Inject top-3 relevant lessons into the Groq prompt for `recommend_next`.

### 4.3 Obsidian / Second-Brain Integration (P2)

**Problem**: Operators take notes in Obsidian during long engagements, but LazyOwn findings live in `sessions/`.
**Metric**: `obsidian_push` exports host summary, creds, and timeline to a daily note in the operator's vault.

**Plan**:
1. Use the existing `obsidian` Hermes skill pattern.
2. Create `do_obsidian_push` which formats `campaign_sitrep` as Markdown frontmatter.
3. Append to `Vault/Engagements/YYYY-MM-DD-lazyown.md`.
4. Optionally pull from Obsidian: read a recon checklist note and inject items into `objectives.jsonl`.

---

## 5. Observability & Metrics

### 5.1 Command Effectiveness Dashboard (P2)

**Problem**: Operators do not know which commands waste time vs. which reliably produce findings.
**Metric**: A `metrics` command prints: top 10 commands by success rate, average runtime, and findings-per-run.

**Plan**:
1. Extend `LazyOwn_session_report.csv` with a `findings_count` column.
2. `modules/metrics.py` aggregates CSV data into tables and time-series.
3. Output: "Command X has a 12 % success rate but an average runtime of 8 min. Consider skipping."

### 5.2 Operator Performance Benchmarks (P3)

**Problem**: There is no way to compare operator efficiency across shifts or teams.
**Metric**: Each `campaign_complete` emits a scorecard: time per phase, creds found, false positives, tool switches.

**Plan**:
1. Define KPIs: Time-to-first-foothold, time-to-privesc, recon-vs-exploit ratio, credential reuse rate.
2. Store in `sessions/scorecards/<campaign>.json`.
3. Compare against previous campaigns in the same scope.

---

## 6. Integration & Ecosystem

### 6.1 Publish Skill to Hermes Hub (P2)

**Problem**: The LazyOwn skill lives only in this repo. Other Hermes users cannot discover it.
**Metric**: `hermes skills install lazyown` works from any Hermes instance.

**Plan**:
1. Ensure `skills/lazyown/SKILL.md` passes the Hermes skill validator.
2. Submit PR to the Hermes skills registry (or publish to a public git repo).
3. Version the skill with the framework release cycle.

### 6.2 Claude Code Native Support (P2)

**Problem**: Claude Code can edit LazyOwn's source, but it does not understand the CLI command structure or the kill chain.
**Metric**: Running `claude` inside `/home/grisun0/LazyOwn` auto-loads a `.claude/CLAUDE.md` that teaches commands, phases, and the `sessions/` layout.

**Plan**:
1. Create `.claude/CLAUDE.md` summarizing the architecture, command phases, and coding standards.
2. Add `.claude/settings.json` with permissions: allow `Bash(git *)`, `Bash(ruff *)`, deny `Bash(rm -rf *)`.
3. Add `.claude/agents/` for: security-reviewer, exploit-developer, docs-writer.
4. This enables any contributor to onboard Claude Code in seconds.

---

## Priority Summary

| Priority | Theme | Count | Key Deliverables |
|----------|-------|-------|------------------|
| P0 | Architecture & OpUX | 4 | Monolith split, linting, proactive prompt, zero-config wizard |
| P1 | Effectiveness & Quality | 6 | Type coverage, 30 playbooks, auto-inference, graceful degradation, Rich output, error UX |
| P2 | Intelligence & Ecosystem | 6 | SWAN feedback, lesson injection, Obsidian, metrics dashboard, Hermes hub, Claude Code support |
| P3 | Benchmarks | 1 | Operator scorecards |

Total: 17 workstreams.

---

## How to Start (Next 48 Hours)

1. **Day 1**: Run `ruff check modules/ lazyown.py lazyc2.py --statistics > lint_report.txt`. Fix the top 3 violation types.
2. **Day 1**: Add `lazyown.py`, `lazyc2.py`, `modules/` to `LINT_TARGETS`/`FORMAT_TARGETS`.
3. **Day 2**: Migrate the first 20 `do_*` methods from `lazyown.py` to `cli/commands/recon.py` using the existing `_base.py` pattern.
4. **Day 2**: Implement the proactive prompt (`[phase/target/creds] lazyown>`) in `cli/status_bar.py`.

---

*This plan is a living document. Update it after each milestone.*
