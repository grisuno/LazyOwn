# orphans

*Community 29 | 286 files | cohesion 0.20*

## Definition

This community groups 286 file(s) rooted at `tests` with dominant language py (cohesion 0.20). Central symbols: `AMS1patch_E_ACCESSDENIED`, `AMS1patch_E_HANDLE`, `AMS1patch_E_OUTOFMEMORY`, `AMS1patch_OpenSession_jne`, `AMS1patch_OpenSession_ret`, `AMS1patch_RastaMouse`, `AMS1patch_ScanBuffer_ret`, `ATTACKERS_IP`. Core file: `skills/mcp_generated_tools.py` (645 symbols). Documented purpose: Build and drive LazyOwn inside its Docker sandbox (Debian container).  LazyOwn is a Linux-targeted cmd2 shell; it does not run natively on a non-Linux host (Lin.

## Files

### `tests` (78 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/__init__.py` | py | testing | 0 | no |

### `modules` (68 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/49803.py` | py | utility | 3 | yes |

### `plugins` (26 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `plugins/generate_c_reverse_shell.lua` | lua | infrastructure | 2 | no |

### `scripts` (22 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/__init__.py` | py | utility | 0 | yes |

### `contrib/legacy` (19 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/__init__.py` | py | utility | 0 | yes |

### `.` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `DEPLOY.sh` | sh | utility | 3 | no |

### `modules/loop` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/loop/control_plane.py` | py | - | 1 | yes |

### `modules/rootkit` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/mr.c` | c | utility | 33 | no |

### `modules/win_rootkit` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/win_rootkit/backup.c` | c | utility | 17 | no |

### `sdk/lazymode` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `sdk/lazymode/__init__.py` | py | - | 0 | yes |

### `skills` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_generated_tools.py` | py | utility | 645 | yes |

### `tools` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/contract_check.py` | py | utility | 2 | yes |

### `lazyown-docker` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/entrypoint.sh` | sh | utility | 0 | yes |

### `sdk` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `sdk/__init__.py` | py | - | 0 | yes |

### `skills/mcp_tools` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/lazymode_exec.py` | py | - | 1 | yes |

### `static/js` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/purify-3.0.9.min.js` | js | utility | 2 | yes |

### `modules/cgi-bin` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/cgi-bin/lazywebshell.py` | py | utility | 0 | no |

### `skills/claude_md_orchestrator/tests` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/claude_md_orchestrator/tests/conftest.py` | py | testing | 0 | yes |

### `tests/contract` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/contract/__init__.py` | py | testing | 0 | no |

### `.claude/skills/run-lazyown` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `.claude/skills/run-lazyown/driver.sh` | sh | infrastructure | 0 | yes |

*... and 266 more files in this community.*


## Key Symbols

- `s` (function, `2026-11-18_112624/jquery-1.11.3.min.js:2`) - /*! jQuery v1.11.3 \| (c) 2005, 2015 jQuery Foundation, Inc. \| jquery.org/license
- `c` (function, `2026-11-18_112624/jquery-1.11.3.min.js:4`)
- `d` (function, `2026-11-18_112624/jquery-1.11.3.min.js:5`)
- `increment_version` (function, `DEPLOY.sh:19`)
- `update_section_html` (function, `DEPLOY.sh:99`) - Función para actualizar una sección específica
- `get_commit_type` (function, `DEPLOY.sh:203`) - Función para obtener el tipo de cambio basado en el mensaje del commit
- `usage` (function, `bootstrap.sh:70`)
- `log` (function, `bootstrap.sh:74`)
- `fail` (function, `bootstrap.sh:92`)
- `spin_run` (function, `bootstrap.sh:97`)
- `can_prompt` (function, `bootstrap.sh:239`)
- `ask` (function, `bootstrap.sh:250`)
- `update_checkout` (function, `bootstrap.sh:259`)
- `backup_payload` (function, `bootstrap.sh:268`)
- `clone_fresh` (function, `bootstrap.sh:280`)
- `clean_checkout` (function, `bootstrap.sh:286`)
- `confirm_clean` (function, `bootstrap.sh:293`)
- `ask_new_dir` (function, `bootstrap.sh:303`)
- `ask_existing_checkout_action` (function, `bootstrap.sh:315`)
- `ask_existing_path_action` (function, `bootstrap.sh:336`)
- `resolve_target_dir` (function, `bootstrap.sh:355`)
- `ask_launch_mode` (function, `bootstrap.sh:432`)
- `loadConfig` (function, `browser_sync_extension/popup.js:4`)
- `renderResult` (function, `browser_sync_extension/popup.js:13`)
- `LazymodeCommandSet` (class, `cli/commands/lazymode.py:20`) `class LazymodeCommandSet(LazyOwnCommandSet)` - List and run lazymode exploit playbooks.
- `do_lazymode_pb` (method, `cli/commands/lazymode.py:27`) `def do_lazymode_pb(self, line)` - List or run lazymode exploit playbooks.
- `genHeader` (function, `contrib/legacy/lazy_http_bof.py:6`) `def genHeader(raw)`
- `exploit` (function, `contrib/legacy/lazy_http_bof.py:29`) `def exploit(target, port, payload)`
- `check_sudo` (function, `contrib/legacy/lazy_packet_image_sniffer.py:23`) `def check_sudo()`
- `list_interfaces` (function, `contrib/legacy/lazy_packet_image_sniffer.py:31`) `def list_interfaces()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 30
- Cross-boundary resolved imports (EXTRACTED): 119

## Connections

- [EXTRACTED] depends_on community 29 <-> 10 (strength 0.9): Extracted import edge crosses communities: 2026-11-18_112624/jquery-1.11.3.min.js imports lazyown-docker/init.sh.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 88 file(s) lack file-level docs (e.g. `DEPLOY.sh`)? What purpose do they serve?
- What would break if the most connected file in orphans changed?
- Should orphans be split, given cohesion 0.20?

## Sources

- `.claude/skills/run-lazyown/driver.sh`
- `2026-11-18_112624/jquery-1.11.3.min.js`
- `DEPLOY.sh`
- `__init__.py`
- `bootstrap.sh`
- `browser_sync_extension/popup.js`
- `cli/commands/lazymode.py`
- `contrib/legacy/__init__.py`
- `contrib/legacy/lazy_http_bof.py`
- `contrib/legacy/lazy_packet_image_sniffer.py`
- `contrib/legacy/lazyarpspoofing.py`
- `contrib/legacy/lazycam.py`
- `contrib/legacy/lazydisassebler.py`
- `contrib/legacy/lazyftpsniff.py`
- `contrib/legacy/lazylfi2rce.py`
- `contrib/legacy/lazymariadb_rce_cve_2016-662.py`
- `contrib/legacy/lazymidm.py`
- `contrib/legacy/lazymitmap.py`
- `contrib/legacy/lazynetbios.py`
- `contrib/legacy/lazyntlrelayx.py`
- *... and 266 more*
