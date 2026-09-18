# orphans

*Community 23 | 201 files | cohesion 0.00*

## Definition

This community groups 201 file(s) rooted at `modules` with dominant language py (cohesion 0.00). Central symbols: `AMS1patch_E_ACCESSDENIED`, `AMS1patch_E_HANDLE`, `AMS1patch_E_OUTOFMEMORY`, `AMS1patch_OpenSession_jne`, `AMS1patch_OpenSession_ret`, `AMS1patch_RastaMouse`, `AMS1patch_ScanBuffer_ret`, `ATTACKERS_IP`. Core file: `skills/mcp_generated_tools.py` (645 symbols). Documented purpose: Nombre del script: download_resources.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 31/07/2024 Descripción: E.

## Files

### `modules` (62 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/49803.py` | py | utility | 3 | yes |

### `tests` (32 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/__init__.py` | py | testing | 0 | no |

### `plugins` (26 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `plugins/generate_c_reverse_shell.lua` | lua | infrastructure | 2 | no |

### `modules/legacy` (22 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/legacy/__init__.py` | py | utility | 0 | yes |

### `scripts` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/__init__.py` | py | utility | 0 | yes |

### `.` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `DEPLOY.sh` | sh | utility | 4 | no |

### `modules/rootkit` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/mr.c` | c | utility | 33 | no |

### `modules/win_rootkit` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/win_rootkit/backup.c` | c | utility | 17 | no |

### `skills` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_generated_tools.py` | py | utility | 645 | yes |

### `static/js` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/purify-3.0.9.min.js` | js | utility | 2 | yes |

### `lazyown-docker` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/entrypoint.sh` | sh | utility | 0 | yes |

### `modules/cgi-bin` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/cgi-bin/lazywebshell.py` | py | utility | 0 | no |

### `skills/claude_md_orchestrator/tests` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/claude_md_orchestrator/tests/conftest.py` | py | testing | 0 | yes |

### `external` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `external/install_external.sh` | sh | utility | 2 | yes |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |

### `modules/scripts` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/scripts/clean_history.sh.sh` | sh | utility | 0 | no |

### `skills/hermes-lazyown` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/__init__.py` | py | utility | 0 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/__init__.py` | py | testing | 0 | no |

### `source` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `source/conf.py` | py | utility | 0 | yes |

### `tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/extract_cluster.py` | py | utility | 4 | yes |

*... and 181 more files in this community.*


## Key Symbols

- `increment_version` (function, `DEPLOY.sh:19`)
- `update_section_md` (function, `DEPLOY.sh:68`) - Función para actualizar una sección específica
- `update_section_html` (function, `DEPLOY.sh:98`) - Función para actualizar una sección específica
- `get_commit_type` (function, `DEPLOY.sh:202`) - Función para obtener el tipo de cambio basado en el mensaje del commit
- `ctrl_c` (function, `external/install_external.sh:13`)
- `download` (function, `external/install_external.sh:18`)
- `_jq` (function, `fast_run_as_r00t.sh:31`) - ── Read payload.json ─────────────────────────────────────────────────────────
- `log` (function, `fast_run_as_r00t.sh:55`) - ── Pretty-print helpers ──────────────────────────────────────────────────────
- `spin` (function, `fast_run_as_r00t.sh:56`)
- `err_box` (function, `fast_run_as_r00t.sh:57`)
- `ensure_gum` (function, `fast_run_as_r00t.sh:63`) - ── Ensure gum is installed ───────────────────────────────────────────────────
- `check_deps` (function, `fast_run_as_r00t.sh:74`) - ── Dependency check ──────────────────────────────────────────────────────────
- `check_sudo` (function, `fast_run_as_r00t.sh:83`) - ── Re-exec as root if needed ─────────────────────────────────────────────────
- `parse_args` (function, `fast_run_as_r00t.sh:92`) - ── CLI argument parsing ──────────────────────────────────────────────────────
- `t_send` (function, `fast_run_as_r00t.sh:110`) - Send one or more commands to the active tmux pane
- `t_lazyown` (function, `fast_run_as_r00t.sh:117`) - Open a new pane (split v or h), start LazyOwn shell with optional run flags, then send any follow-up
- `t_priv_user` (function, `fast_run_as_r00t.sh:130`) - Open a new pane running a command as unprivileged user 1000 (with venv). Usage: t_priv_user <v\|h> <c
- `start_chown_watcher` (function, `fast_run_as_r00t.sh:141`) - ── Background chown watcher ────────────────────────────────────────────────── Re-chowns the project
- `usage` (function, `install.sh:35`)
- `log` (function, `install.sh:58`)
- `ensure_gum` (function, `install.sh:68`)
- `install_system_packages` (function, `install.sh:79`)
- `install_external_tools` (function, `install.sh:90`)
- `install_python_environment` (function, `install.sh:105`)
- `install_ollama` (function, `install.sh:141`)
- `install_external_storage` (function, `install.sh:153`)
- `install_lazyownbt` (function, `install.sh:166`)
- `download_file` (function, `install.sh:186`)
- `install_encoder_module` (function, `install.sh:198`)
- `generate_certificates` (function, `install.sh:209`)

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 0
- Cross-boundary resolved imports (EXTRACTED): 16

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [dataflow UNCHECKED_ALLOC] `modules/bin2img.py:17` `binario_a_imagen` `img`: Result of allocator stored in `img` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/detailed_search.py:86` `obtener_informacion` `csv_file`: Result of allocator stored in `csv_file` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:371` `set_stable_table_and_set` `seq`: `seq` assigned at line 371 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:356` `set_stable_table_and_set` `table_seq`: `table_seq` assigned at line 356 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:406` `set_trigger_set_and_overwrite` `exprid`: `exprid` assigned at line 406 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:423` `set_trigger_set_and_overwrite` `seq`: `seq` assigned at line 423 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:453` `spray_mqueue` `unresolved`: `unresolved` assigned at line 453 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:455` `spray_mqueue` `priority`: `priority` assigned at line 455 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:465` `gather_mqueue` `priority`: `priority` assigned at line 465 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:487` `gather_mqueue_nosave` `priority`: `priority` assigned at line 487 but never read afterwards.

## Open Questions

- Why do 88 file(s) lack file-level docs (e.g. `DEPLOY.sh`)? What purpose do they serve?
- What would break if the most connected file in orphans changed?
- Should orphans be split, given cohesion 0.00?

## Sources

- `DEPLOY.sh`
- `__init__.py`
- `external/install_external.sh`
- `fast_run_as_r00t.sh`
- `gen_cert.sh`
- `install.sh`
- `lazyc2/__init__.py`
- `lazyown-docker/entrypoint.sh`
- `lazyown-docker/hostdiscover.sh`
- `lazyown-docker/mkdocker.sh`
- `modules/49803.py`
- `modules/CVE-2018-15133.php`
- `modules/CVE-2023-28432.py`
- `modules/LazyOwnExplorer.py`
- `modules/__init__.py`
- `modules/amsi.c`
- `modules/amt_auth_bypass.py`
- `modules/bin2img.py`
- `modules/bot.py`
- `modules/c2_messaging_base.py`
- *... and 181 more*
