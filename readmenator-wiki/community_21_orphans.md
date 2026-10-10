# orphans

*Community 21 | 208 files | cohesion 0.00*

## Definition

This community groups 208 file(s) rooted at `modules` with dominant language py (cohesion 0.00). Central symbols: `AMS1patch_E_ACCESSDENIED`, `AMS1patch_E_HANDLE`, `AMS1patch_E_OUTOFMEMORY`, `AMS1patch_OpenSession_jne`, `AMS1patch_OpenSession_ret`, `AMS1patch_RastaMouse`, `AMS1patch_ScanBuffer_ret`, `ATTACKERS_IP`. Core file: `skills/mcp_generated_tools.py` (645 symbols). Documented purpose: Build and drive LazyOwn inside its Docker sandbox (Debian container).  LazyOwn is a Linux-targeted cmd2 shell; it does not run natively on a non-Linux host (Lin.

## Files

### `modules` (61 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/49803.py` | py | utility | 3 | yes |

### `tests` (34 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/__init__.py` | py | testing | 0 | no |

### `plugins` (26 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `plugins/generate_c_reverse_shell.lua` | lua | infrastructure | 2 | no |

### `contrib/legacy` (22 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/__init__.py` | py | utility | 0 | yes |

### `scripts` (16 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/__init__.py` | py | utility | 0 | yes |

### `.` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `DEPLOY.sh` | sh | utility | 3 | no |

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

### `.claude/skills/run-lazyown` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `.claude/skills/run-lazyown/driver.sh` | sh | infrastructure | 0 | yes |

### `deploy/range/ad-mini` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `deploy/range/ad-mini/traffic-gen.py` | py | utility | 2 | yes |

### `external` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `external/install_external.sh` | sh | utility | 2 | yes |

### `modules/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/legacy/__init__.py` | py | utility | 0 | yes |

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

*... and 188 more files in this community.*


## Key Symbols

- `increment_version` (function, `DEPLOY.sh:19`)
- `update_section_html` (function, `DEPLOY.sh:86`) - Función para actualizar una sección específica
- `get_commit_type` (function, `DEPLOY.sh:190`) - Función para obtener el tipo de cambio basado en el mensaje del commit
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
- `genHeader` (function, `contrib/legacy/lazy_http_bof.py:6`) `def genHeader(raw)`
- `exploit` (function, `contrib/legacy/lazy_http_bof.py:29`) `def exploit(target, port, payload)`
- `check_sudo` (function, `contrib/legacy/lazy_packet_image_sniffer.py:23`) `def check_sudo()`
- `list_interfaces` (function, `contrib/legacy/lazy_packet_image_sniffer.py:31`) `def list_interfaces()`
- `choose_interface` (function, `contrib/legacy/lazy_packet_image_sniffer.py:49`) `def choose_interface(interfaces)`
- `get_subnet_from_interface` (function, `contrib/legacy/lazy_packet_image_sniffer.py:61`) `def get_subnet_from_interface(interface)`
- `get_ip_addresses` (function, `contrib/legacy/lazy_packet_image_sniffer.py:65`) `def get_ip_addresses(interface)`
- `handle_packet` (function, `contrib/legacy/lazy_packet_image_sniffer.py:111`) `def handle_packet(packet)`
- `save_image` (function, `contrib/legacy/lazy_packet_image_sniffer.py:161`) `def save_image(src_ip, end_idx)`
- `run` (function, `contrib/legacy/lazy_packet_image_sniffer.py:187`) `def run()`
- `daemonize` (function, `contrib/legacy/lazy_packet_image_sniffer.py:192`) `def daemonize()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 0
- Cross-boundary resolved imports (EXTRACTED): 16

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazy_http_bof.py:30` `exploit` `sock`: Result of allocator stored in `sock` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyarpspoofing.py:42` `get_local_ip` `s`: Result of allocator stored in `s` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazybotcli.py:59` `main` `conn`: Result of allocator stored in `conn` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazybotnet.py:79` `send_to_botnet` `conn`: Result of allocator stored in `conn` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazybotnet.py:188` `start_server` `server`: Result of allocator stored in `server` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazylfi2rce.py:86` `main` `wordlist`: Result of allocator stored in `wordlist` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/bin2img.py:17` `binario_a_imagen` `img`: Result of allocator stored in `img` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/detailed_search.py:91` `obtener_informacion` `csv_file`: Result of allocator stored in `csv_file` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:218` `spray_keyring_list_overwrite_purpose` `id_buffer`: Result of allocator stored in `id_buffer` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:274` `awake_partial_keys` `keylen`: `keylen` assigned at line 274 but never read afterwards.
- [dataflow UNCHECKED_ALLOC] `modules/exp.c:313` `unshare_setup` `temp`: Result of allocator stored in `temp` is never checked against NULL.
- [dataflow DEAD_STORE] `modules/exp.c:340` `set_stable_table_and_set` `set_id`: `set_id` assigned at line 340 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:344` `set_stable_table_and_set` `exprid`: `exprid` assigned at line 344 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:371` `set_stable_table_and_set` `seq`: `seq` assigned at line 371 but never read afterwards.
- [dataflow DEAD_STORE] `modules/exp.c:356` `set_stable_table_and_set` `table_seq`: `table_seq` assigned at line 356 but never read afterwards.

## Open Questions

- Why do 88 file(s) lack file-level docs (e.g. `DEPLOY.sh`)? What purpose do they serve?
- What would break if the most connected file in orphans changed?
- Should orphans be split, given cohesion 0.00?

## Sources

- `.claude/skills/run-lazyown/driver.sh`
- `DEPLOY.sh`
- `__init__.py`
- `bootstrap.sh`
- `contrib/legacy/__init__.py`
- `contrib/legacy/lazy_http_bof.py`
- `contrib/legacy/lazy_packet_image_sniffer.py`
- `contrib/legacy/lazyarpspoofing.py`
- `contrib/legacy/lazybotcli.py`
- `contrib/legacy/lazybotnet.py`
- `contrib/legacy/lazycam.py`
- `contrib/legacy/lazydisassebler.py`
- `contrib/legacy/lazyftpsniff.py`
- `contrib/legacy/lazykeygen.py`
- `contrib/legacy/lazylfi2rce.py`
- `contrib/legacy/lazymariadb_rce_cve_2016-662.py`
- `contrib/legacy/lazymidm.py`
- `contrib/legacy/lazymitmap.py`
- `contrib/legacy/lazynetbios.py`
- `contrib/legacy/lazyntlrelayx.py`
- *... and 188 more*
