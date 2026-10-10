---
name: marketplace-contributor
description: "Contribute YARA rules, Nuclei templates, and pwntomate tools to the LazyOwn marketplace from a GitHub URL in one shot. Knows the yara_rules/, nuclei-templates, and tools/*.tool layouts, naming rules, and validation."
trigger: /marketplace-contributor
---

# /marketplace-contributor

Given a GitHub URL, contribute detection content or tooling to the LazyOwn
marketplace on the first try. No iteration: fetch facts, pick the contribution
type, fill the template, run the self-check, write the file(s).

Related: `/lazyaddon-creator` (generic tool -> `lazyaddons/*.yaml`). This skill
covers the three marketplace content types that are NOT plain lazyaddons.
For a Nuclei wrapper that needs `repo_url`/`install_path` semantics, this skill
reuses the lazyaddon schema — see Type N below.

## Usage

```
/marketplace-contributor https://github.com/user/repo [--type yara|nuclei|tool] [--name <name>]
```

`--type` is auto-detected when omitted (see Step 2). `--name` overrides the
default file stem.

## Step 1 — Fetch repo facts

```bash
REPO=user/repo
curl -fsSL "https://api.github.com/repos/$REPO" | python3 -c "import json,sys; m=json.load(sys.stdin); print(m['name'], '|', m['owner']['login'], '|', m['language'], '|', (m['description'] or '')[:200])"
curl -fsSL "https://api.github.com/repos/$REPO/contents/" | python3 -c "import json,sys; print([e['name'] for e in json.load(sys.stdin)])"
curl -fsSL "https://raw.githubusercontent.com/$REPO/HEAD/README.md" | head -c 4000
```

You need: repo name, owner, primary language, root file list, README usage
section. Then classify the content:

- `.yar` / `.yara` files present -> Type Y.
- Nuclei template markers (`id:`, `info:`, plus `http:` / `requests:` /
  `network:` / `dns:` stanzas, `severity:` field) in `*.yaml` under dirs like
  `http/`, `cves/`, `network/`, `ssl/` -> Type N.
- Executable scanner / enumerator with a CLI -> Type T.
- Ambiguous -> ask the operator with `/marketplace-contributor` question tool.

## Step 2 — Pick the contribution type

| # | Type | When | Output file(s) | Reference |
|---|------|------|----------------|-----------|
| Y | YARA rule | Repo ships `.yar`/`.yara` detection rules (malware, webshell, C2, packer, privesc) | `yara_rules/<name>.yar` (one rule file per contribution) | `yara_rules/cobalt_strike_beacon.yar`, `yara_rules/webshell_detection.yar` |
| N | Nuclei templates | Repo is a template collection (e.g. `projectdiscovery/nuclei-templates`) | `lazyaddons/<name>.yaml` wrapper (clone + `nuclei -t`) + optional `tools/<name>-*.tool` | `tools/nuclei-ad.tool`, `lazyaddons/trivy.yaml` (release-wrapper pattern) |
| T | Pwntomate tool | Repo is a runnable scanner whose output maps to a service trigger | `tools/<name>.tool` JSON (+ optional `/lazyaddon-creator` addon) | `tools/_example.tool`, `tools/nikto.tool` |

Never vendor thousands of upstream files into the repo. Type N clones at
runtime via `repo_url`; Type Y copies exactly ONE rule file; Type T writes
exactly ONE `.tool` JSON.

## Step 3 — Type Y: YARA rule file

Target: `yara_rules/<name>.yar` where `<name>` matches `^[A-Za-z0-9_]{1,64}$`
(lowercase preferred, e.g. `my_webshell.yar`).

```yar
rule MarketplaceRuleName {
    meta:
        description = "One-line detection summary. Max 120 chars."
        author = "Repo Owner"
        reference = "https://github.com/user/repo"
        date = "2026-10-09"
    strings:
        $s1 = "suspicious literal" ascii wide
        $re1 = /suspicious_regex_[0-9]+/ ascii
    condition:
        2 of them
}
```

Rules:

1. ONE file per contribution. Multi-rule repos: extract the single requested
   rule, or the highest-signal rule family, into one file.
2. `rule` identifier matches `^[A-Za-z_][A-Za-z0-9_]{0,127}$`.
3. `meta` MUST include `description`, `author`, `reference` (source repo URL).
4. No `include` directives (breaks `yara_rules/` flat scanning).
5. No `private` rules without a consuming public rule in the same file.
6. Validate: `yara <file> /bin/ls` must exit 0 when `yara` is installed;
   otherwise assert balanced braces and the presence of `rule`, `strings:`,
   `condition:` literals.
7. The rule is picked up automatically: `AddonRegistry.scan("yara")` globs
   `yara_rules/*.yar|*.yara`, and `yara_scan` runs against it. No registry
   edit needed.

## Step 4 — Type N: Nuclei wrapper (lazyaddon + optional .tool)

Template collections are NEVER vendored. Write a wrapper addon following the
`/lazyaddon-creator` schema (all of its Steps 4–9 apply verbatim:
single braces, live-params-only placeholders, no secrets, `enabled: true`,
`^[a-z][a-z0-9_]{0,63}$` name, digits-and-dots version, `.git` repo_url).

Template (archetype A — cloned data repo, local execute):

```yaml
name: nuclei_templates            # do_<name>. MUST match ^[a-z][a-z0-9_]{0,63}$
description: |                    # Max 500 chars. Usage + requirements.
  Nuclei template collection by Owner. Runs nuclei against {target} with the
  cloned templates. Requires the nuclei binary (installed by the nuclei
  command). Extra flags append as free args, e.g. nuclei_templates -severity critical.
author: Repo Owner                # Max 80 chars
version: "1.0"                    # MUST match ^\d+(\.\d+){0,3}$
enabled: true
params:                           # Max 20. Every {token} used MUST be declared...
  - name: target                  # ...and MUST exist in live shell params
    type: string
    required: true
    description: Target URL or host to scan. Max 200 chars, never empty.
os: any
trigger:
  - http
  - https
category: "02. Scanning & Enumeration"
tool:
  name: Nuclei Templates
  repo_url: https://github.com/user/templates.git   # MUST end with .git
  install_path: external/.exploit/templates         # relative, no spaces, no '..'
  execute_command: nuclei -u {target} -t http/cves/ -t network/cves/ -severity critical,high,medium -stats -silent -o ../../../sessions/nuclei_{target}.txt
```

Rules specific to Type N:

1. `install_command` is OMITTED (template repos need no build).
2. `execute_command` runs from `install_path`, so template paths are relative
   (`-t http/cves/`). Output stages to `../../../sessions/` (three levels up
   from `external/.exploit/<dir>`), stable name `nuclei_{target}.txt`.
3. Default template subset MUST be bounded (e.g. `http/cves/`, severity
   filter). Full-corpus scans (`-t .`) are free-args only — document them.
4. Placeholders: `{target}` (live in `payload.json`). Severity/tag selection
   travels via FREE ARGS (`-severity critical -tags cve`), never via new
   placeholders (new keys require the 4-place registration from
   `/lazyaddon-creator` Step 4).
5. Requires the `nuclei` binary — state this in `description`, do not chain
   installers with `;` in `execute_command`.
6. Optional companion: `tools/<name>-<profile>.tool` pwntomate wrapper so
   future scans auto-apply it on matching services (see Step 5 for schema).
   The `.tool` command uses PWNtomate placeholders (`{ip}`, `{port}`,
   `{outputdir}`), NOT shell placeholders — the two systems never mix.
7. Register the collection in `modules/nuclei_templates_sync.py` `SOURCES`
   (see Step 4c) so `download_nuclei_templates` syncs it on every operator
   machine — the wrapper alone only helps fresh clones.

## Step 4c — Type N: register the source in the sync script

Every new template collection MUST be added to the `SOURCES` registry in
`modules/nuclei_templates_sync.py`, otherwise `download_nuclei_templates`
never delivers it to operator machines:

```python
SOURCES = {
    "nuclei-templates": {
        "repo": "https://github.com/projectdiscovery/nuclei-templates.git",
        "subdir": "nuclei-templates",
        "validate_subset": "http/cves",
    },
    "<name>": {
        "repo": "https://github.com/user/repo.git",
        "subdir": "<dirname>",  # == external/.exploit/<dirname>
        "validate_subset": "<dir>",  # relative subset for nuclei -validate
    },
}
```

Rules:

1. One entry per collection: `repo` (`.git` URL), `subdir` (destination
   dirname, no spaces, no `..`), `validate_subset` (must exist in the repo).
2. New sources sync immediately: `python3 modules/nuclei_templates_sync.py
   --source <name>` — same Step 4b guarantees (tmp staging, `.git` strip,
   count guard, `find .git` == 0).
3. Implants, binaries, and runnable scanners (archetypes B/C/D) are NEVER
   registered here — they ship as plain lazyaddons only. This registry is
   exclusively for template/rule collections consumed from disk.

## Step 4b — Type N: immediate ingestion (the skill DOES this now, not later)

The wrapper alone only clones on first use — the operator would still see the
old templates. The skill MUST ingest immediately following this procedure
(clone in tmp, copy the working tree, strip every `.git` trace to avoid
mixed-repo contamination):

```bash
DEST=external/.exploit/<dirname>   # canonical dir: matches AddonRegistry
                                   # _NUCLEI_CANDIDATES + nuclei_bridge
git clone --depth 1 https://github.com/user/repo.git /tmp/<name>-ingest
rm -rf /tmp/<name>-ingest/.git     # strip ALL git traces BEFORE copying
mkdir -p "$DEST"
cp -a /tmp/<name>-ingest/. "$DEST"/
find "$DEST" -name .git -maxdepth 2 | wc -l   # MUST print 0
rm -rf /tmp/<name>-ingest
```

Rules:

1. NEVER clone directly into `external/` or the repo root — always stage in
   `/tmp/<name>-ingest` first. A nested `.git` inside the LazyOwn checkout
   breaks git operations and submodule detection.
2. NEVER copy the `.git` directory. `rm -rf` it in tmp BEFORE `cp -a`.
   Verify with the `find` above (must be 0).
3. `external/.exploit` is gitignored — ingested content never pollutes
   `git status`.
4. If a first-priority candidate dir already exists as a clean clone of the
   SAME remote (e.g. `~/nuclei-templates`), refresh it with
   `git pull --ff-only` there instead of duplicating — but ONLY when
   `git status -sb` is clean and `remote -v` matches. Never force-push,
   never touch dirty trees.
5. Verify after ingest: template count (`find "$DEST" -name '*.yaml' | wc -l`),
   `AddonRegistry.scan("nuclei")` non-empty, and
   `nuclei -t "$DEST/<subset>" -validate -silent` exits 0.

## Step 5 — Type T: pwntomate .tool file

Target: `tools/<name>.tool` where `<name>` matches `^[a-z0-9][a-z0-9\-_]{0,63}$`.

```json
{
  "toolname": "my_scanner_http",
  "command": "my_scanner -u http{s}://{ip}:{port} > {outputdir}/my_scanner_http.txt",
  "trigger": ["http", "https"],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: my_scanner_http — triggers on ['http', 'https']"
}
```

Rules:

1. Placeholders are PWNtomate-only: `{ip}`, `{port}`, `{s}` (s/s scheme
   suffix), `{outputdir}`, `{toolname}`. NEVER shell placeholders (`{target}`,
   `{rhost}`, `{lhost}`) — pwntomate substitutes its own set.
2. `trigger`: lowercase nmap service names (`http`, `smb`, `ldap`), or
   `["all"]` for service-agnostic tools. Max 40 entries.
3. `active: true` to run on future scans; `false` for opt-in only.
4. `category` MUST match `^\d{2}\. [name]$` (same table as lazyaddons).
5. Validate JSON parses and every `{token}` is in the PWNtomate allowlist
   `{ip} {port} {s} {outputdir} {toolname}`.
6. If the tool also deserves an interactive shell command, run
   `/lazyaddon-creator` for the same repo afterwards — the `.tool` and the
   `.yaml` coexist.

## Step 6 — One-shot self-check (run before writing)

Type Y:

```bash
python3 -c "import re,sys; src=open('yara_rules/<name>.yar').read(); assert re.search(r'rule\s+[A-Za-z_]\w*', src), 'no rule'; assert 'condition:' in src and 'strings:' in src; assert src.count('{')==src.count('}'), 'unbalanced braces'; assert 'include' not in src.lower(), 'no includes'; print('YARA OK')"
```

Type N (same gate as `/lazyaddon-creator` Step 9):

```bash
python3 -m pytest tests/test_placeholder_coverage.py -q
```

Plus manual assertions: `enabled: true`; name regex; version
digits-and-dots; `repo_url` ends `.git`; no `{{`/`}}`; every `{token}`
resolves from live shell params; `execute_command` bounded and complete with
zero free args; no `;`-chaining; description documents the `nuclei` binary
requirement + free-args examples.

Type T:

```bash
python3 -c "import json,re; d=json.load(open('tools/<name>.tool')); assert re.match(r'^[a-z0-9][a-z0-9\-_]{0,63}$', d['toolname'].replace('_','-').lower()); print(set(re.findall(r'\{(\w+)\}', d['command'])) <= {'ip','port','s','outputdir','toolname'}, d['command'])"
```

## Step 7 — Write and register

- Type Y: write `yara_rules/<name>.yar` — visible via `marketplace_config show`
  (YARA Rules tab) and `yara_scan` immediately. No reload needed.
- Type N: write `lazyaddons/<name>.yaml` (+ optional `tools/<name>-*.tool`),
  then EXECUTE the Step 4b ingestion immediately (clone in /tmp, strip .git,
  copy to `external/.exploit/<dirname>`), then in the LazyOwn shell run
  `reload_addons`. Verify with `list_addons` and `help <name>`.
- Type T: write `tools/<name>.tool` — applied automatically to matching
  services on future scans. Verify with `marketplace list`.
