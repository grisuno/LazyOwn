---
name: adversary-yaml-creator
description: "Create LazyOwn adversary YAMLs in one shot: APT playbooks (playbooks/apt_*.yaml), orchestration chains (chains/*.yaml) and exploit definitions (exploits/*.yaml). Knows the exact schemas, token grammars and the four validation gates. For lazyaddons use /lazyaddon-creator instead."
trigger: /adversary-yaml-creator
---

# /adversary-yaml-creator

Given an adversary name, a target service, or a CTF goal, write the YAML that makes
LazyOwn act on it: one exploit definition, one orchestration chain, and (for APT
groups) one playbook. No iteration: copy the real schema below, run the self-checks,
write the files. The three engines reload catalogs on load, so a valid file is
production on the next rank/sweep.

## What to create for each input

| Input | Files |
|-------|-------|
| APT group (not yet in playbooks/) | `playbooks/apt_<slug>.yaml` + `chains/apt_<slug>.yaml` |
| Exploitable service/CVE (not yet in exploits/) | `exploits/<id>.yaml` |
| CTF goal / lab path (not yet in chains/) | `chains/<goal>.yaml` (+ paired fallback chain when the path has a quieter variant) |
| Operator tool (installed CLI, GitHub tool) | use `/lazyaddon-creator` instead |

Naming: `^[a-z][a-z0-9_]{0,63}$`, filename equals the identifier. One file per
artifact. Never guess versions or exploit outcomes: `versions: []` means any.

## File 1 — playbooks/apt_<slug>.yaml

Schema consumed by modules/apt_playbooks.py (AptPlaybookEngine). Keys are slugified
(`Sandworm Team` -> `sandworm_team`), so chain `defaults.playbook` uses the slug.

```yaml
apt_name: Crowdstrike-Threat
aliases: []
source_urls: [https://attack.mitre.org/groups/G0000]
description: One paragraph, who/why/how.
platforms: [windows, linux]
phases:
- name: initial_access            # killchain-style phase name
  technique_id: T1190
  technique_name: Exploit Public-Facing Application
  description: What this phase does for this group.
  atomic_tests:
  - atomic_id: T1190              # ART guideline id; manual:true means operator pastes the command
    name: Short label
    manual: true
  caldera_abilities:              # optional
  - ability_id: "<uuid>"
  detection_hints:
  - Concrete observable behaviour
```

Set `manual: true` unless the technique maps to a lab-runnable atomic test you have
verified exists under an `atomic_id` that emulation knows.

## File 2 — chains/<name>.yaml

Schema v2, consumed by modules/chain_registry.py + modules/chain_runner.py via
`apt_chain <name> <target>`. Validation is strict: unknown enabled/chains fail to load;
`fallback` and `extends` targets must exist as sibling files; a chain is never its own
fallback; self-extends is an error.

```yaml
name: ctf_mymachine            # == filename
version: 2
description: One line goal.
enabled: true
tags: [ctf, golden-path]
platforms: [linux]
total_timeout: 3600            # seconds, <= 86400
vars:                          # optional; every var becomes a shell-quoted token
  wordlist: /usr/share/wordlists/dirb/common.txt
fallback: ctf_mymachine_quiet  # optional; file MUST exist
extends: apt_chain             # APT chains only; own steps replace the parent wholesale
defaults:
  playbook: <apt-slug>
steps:
- id: bind                     # ^[a-z][a-z0-9_]{0,63}$
  phase: recon                 # recon | enum | exploit | post_exploitation | ...
  run: assign target {target}  # {target}, {playbook}, vars, later captures all resolve; shell-quoted
  timeout: 300                 # seconds, <= 3600
  retries: 1                   # 0-5
  continue_on_error: true      # keep the chain alive on soft failures
  parallel: true               # runs concurrently with other parallel steps
  skip_if_exists: sessions/scan_{target}.nmap.xml
  capture: step_output         # exposes 2000-char stripped output to later steps
  expect: "SHELL"              # step fails when the capture lacks this text
```

Rules that break chains:
- First token of `run` matching a live shell verb (assign, lazynmap, atomic_exploit,
  c2_server, c2_deploy, c2_loot, apt_playbook, attack_plan, atomic_emulate,
  create_session_json, lazycreds, hydra, nuclei, gobuster, ...) executes through cmd2;
  anything else runs as a raw safe-subprocess shell line. Pipes work; keep each line
  one pipeline.
- Single braces only. `{{` never validates (`render_text_token_braces`).
- Evidence fields are optional (evidence, evidence_sha256, required_fields,
  benign_alternatives, budget, depends_on) — hunting verdicts only apply when set.
- Validate dry: `apt_chain <name> <target> --dry-run`.

## File 3 — exploits/<id>.yaml

Schema v1 consumed by modules/atomic_exploit_bridge.py. Services/products/versions
are lowercased substrings matched against sessions/scan_<target> nmap results.

```yaml
id: generic_<vector>           # == filename
mitre_id: T1190
cve: ''                        # '' when the vector has no CVE
title: One-line what it proves
severity: critical|high|medium|low
confidence: 0.0-1.0            # >0.7 requires a proven lab run
platforms: [linux]
services: [redis]
products: [redis]
versions: []
requires_binaries: [redis-cli, curl]
commands:                      # ordered; first SHELL signal stops the chain
- run: printf 'id\n' | nc -w 8 {rhost} {port}
  timeout: 15                  # 5-600
shell_indicators: [uid=0]      # merged with engine defaults
enabled: true
```

Tokens: `{rhost}` target, `{lhost}` attacker, `{lport}` callback, `{port}` resolved
service port. Optional `exec:` block (trigger/shell_port/probe/timeout) turns the
exploit into a multiplexed session usable by emulation; without it the exploit can
sweep but never emulate. Confidence above 0.7 without a proven run is a violation of
the no-guessing rule.

## One-shot self-check (run before declaring done)

```bash
python3 -c "from modules.apt_playbooks import AptPlaybookEngine; e=AptPlaybookEngine(); print(bool(e.get('<slug>')))"
python3 -c "from modules.chain_registry import validate_chain, CHAINS_DIR; import yaml, sys; \
  data=yaml.safe_load(open(CHAINS_DIR/'<name>.yaml')); print(validate_chain(data, filename='<name>', chains_dir=CHAINS_DIR))"
python3 modules/atomic_exploit_bridge.py validate
python3 -m pytest tests/test_placeholder_coverage.py -q
```

All four must pass. A failing chain file never loads: the loop silently loses the
path; the bridge refuses the exploit; the playbook engine warns and skips the file.
Do not paper over schema errors with defaults — fix the YAML.

## Completion contract

- Every new adversary gets both the playbook and its `defaults.playbook` chain
  (six-line `extends: apt_chain` file), so `apt_chain apt_<slug> <target>` works.
- Every new exploit declares only services/products the box truly exposes.
- Every new CTF chain declares `continue_on_error` on soft steps and `retries`
  where the target is noisy, plus an explicit `vars:` wordlist when content
  discovery is included (never embed lists inline).
- Artifacts land in `sessions/`; nothing writes to payload.json here.
