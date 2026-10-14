# modules: estorides_importer

*Community 6 | 50 files | cohesion 0.46*

## Definition

This community groups 50 file(s) rooted at `tests` with dominant language py (cohesion 0.46). Central symbols: `AESdecrypt`, `AESencrypt`, `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`, `AddonYamlRenderer`. Core file: `tests/test_addon_creator.py` (86 symbols). Documented purpose: Estorides integration commands — bidirectional feedback loop with passive OSINT.  Commands: estorides_seed     Feed LazyOwn hosts into Estorides for passive dis.

## Files

### `tests` (17 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_api_authz.py` | py | testing | 48 | yes |
| `tests/test_api_v1.py` | py | testing | 13 | yes |

### `modules` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_history.py` | py | utility | 7 | yes |
| `modules/db.py` | py | utility | 37 | yes |
| `modules/estorides_importer.py` | py | utility | 47 | yes |

### `lazyc2/blueprints` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `core` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |
| `core/credential_vault.py` | py | utility | 8 | yes |

### `cli/commands` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/estorides.py` | py | utility | 9 | yes |
| `cli/commands/opsec_cleanup.py` | py | utility | 9 | yes |

### `lazyc2/extensions` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `lazyc2` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 38 | yes |
| `lazyc2/app_factory.py` | py | presentation | 9 | yes |

### `modules/integrations` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/nuclei_bridge.py` | py | utility | 29 | yes |
| `modules/integrations/nuclei_parser.py` | py | utility | 17 | yes |

### `lazyc2/security` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/csrf.py` | py | utility | 11 | yes |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

*... and 30 more files in this community.*


## Key Symbols

- `_yellow` (function, `cli/commands/estorides.py:43`) `def _yellow(text)`
- `_green` (function, `cli/commands/estorides.py:47`) `def _green(text)`
- `EstoridesCommandSet` (class, `cli/commands/estorides.py:51`) `class EstoridesCommandSet(LazyOwnCommandSet)` - Bidirectional Estorides <-> LazyOwn integration commands.
- `_check_estorides` (method, `cli/commands/estorides.py:57`) `def _check_estorides(self)` - Check that estorides is cloned and available.
- `do_estorides_seed` (method, `cli/commands/estorides.py:73`) `def do_estorides_seed(self, line)` - Feed LazyOwn hosts/domains into Estorides for passive OSINT discovery.
- `do_estorides_import` (method, `cli/commands/estorides.py:189`) `def do_estorides_import(self, line)` - Import Estorides-discovered entities into LazyOwn database and scope.
- `_preview_entities` (method, `cli/commands/estorides.py:319`) `def _preview_entities(self, entities)` - Show a preview of entities grouped by type.
- `do_estorides_loop` (method, `cli/commands/estorides.py:337`) `def do_estorides_loop(self, line)` - Run the bidirectional Estorides <-> LazyOwn feedback loop.
- `do_estorides_surface` (method, `cli/commands/estorides.py:441`) `def do_estorides_surface(self, line)` - Show the combined active + passive attack surface.
- `OpsecCleanupCommandSet` (class, `cli/commands/opsec_cleanup.py:19`) `class OpsecCleanupCommandSet(LazyOwnCommandSet)` - OPSEC scoring, log tampering, forensic cleaning, timestomping, memory/network OPSEC.
- `do_opsec_score` (method, `cli/commands/opsec_cleanup.py:25`) `def do_opsec_score(self, line)` - Real-time OPSEC risk assessment with contextual action gating (v2).
- `do_log_tamper` (method, `cli/commands/opsec_cleanup.py:97`) `def do_log_tamper(self, line)` - Cross-platform log clearing commands.
- `do_forensic_clean` (method, `cli/commands/opsec_cleanup.py:162`) `def do_forensic_clean(self, line)` - Clean forensic artifacts — Prefetch, Shimcache, Amcache, Jump Lists, etc.
- `do_timestomp` (method, `cli/commands/opsec_cleanup.py:219`) `def do_timestomp(self, line)` - Manipulate file MACB timestamps to evade forensic timeline analysis.
- `do_memory_clean` (method, `cli/commands/opsec_cleanup.py:288`) `def do_memory_clean(self, line)` - Clean memory artifacts — Kerberos tickets, clipboard, env vars, credentials.
- `do_network_opsec` (method, `cli/commands/opsec_cleanup.py:342`) `def do_network_opsec(self, line)` - Network OPSEC — proxy chains, DoH, canary detection, traffic analysis.
- `do_auditd_disable` (method, `cli/commands/opsec_cleanup.py:445`) `def do_auditd_disable(self, line)` - Generate commands to disable Linux auditd.
- `do_sysmon_disable` (method, `cli/commands/opsec_cleanup.py:468`) `def do_sysmon_disable(self, line)` - Generate commands to disable Windows Sysmon.
- `SecurityCommandSet` (class, `cli/commands/security.py:20`) `class SecurityCommandSet(LazyOwnCommandSet)` - OPSEC scoring, credential vault, and hash cracking commands.
- `do_opsec` (method, `cli/commands/security.py:26`) `def do_opsec(self, line)` - Score OPSEC risk for a LazyOwn command before execution.
- `do_seal_credentials` (method, `cli/commands/security.py:106`) `def do_seal_credentials(self, _line)` - Encrypt all sensitive values in payload.json using AES-256-GCM.
- `do_rotate_aes` (method, `cli/commands/security.py:127`) `def do_rotate_aes(self, _line)` - Generate a new AES key and re-encrypt all sealed credentials.
- `do_unseal_credentials` (method, `cli/commands/security.py:150`) `def do_unseal_credentials(self, _line)` - Decrypt sealed credential values in payload.json for inspection.
- `do_crack_hashes` (method, `cli/commands/security.py:170`) `def do_crack_hashes(self, line)` - Crack password hashes from a file using John the Ripper or Hashcat.
- `complete_opsec` (method, `cli/commands/security.py:267`) `def complete_opsec(self, text, line, begidx, endidx)`
- `complete_crack_hashes` (method, `cli/commands/security.py:276`) `def complete_crack_hashes(self, text, line, begidx, endidx)`
- `ApiAuthzConfig` (class, `core/api_authz.py:54`) `class ApiAuthzConfig` - Configuration contract for the API authorization module.
- `ApiKey` (class, `core/api_authz.py:75`) `class ApiKey` - Immutable record of a hashed API key bound to a tenant.
- `to_dict` (method, `core/api_authz.py:94`) `def to_dict(self)`
- `from_dict` (method, `core/api_authz.py:107`) `def from_dict(cls, data)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 98
- Cross-boundary resolved imports (EXTRACTED): 105

## Connections

- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/crypto.py.
- [EXTRACTED] depends_on community 0 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/campaign.py imports modules/db.py.
- [EXTRACTED] depends_on community 11 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.

## Risks

- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)

## Open Questions

- What would break if the most connected file in modules: estorides_importer changed?
- Should modules: estorides_importer be split, given cohesion 0.46?

## Sources

- `cli/commands/estorides.py`
- `cli/commands/opsec_cleanup.py`
- `cli/commands/security.py`
- `core/api_authz.py`
- `core/credential_vault.py`
- `core/crypto.py`
- `core/protocols.py`
- `lazyc2/addon_creator.py`
- `lazyc2/app_factory.py`
- `lazyc2/blueprints/__init__.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/api.py`
- `lazyc2/blueprints/api_v1.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/session_auth.py`
- `lazyc2/extensions/__init__.py`
- `lazyc2/extensions/decoy.py`
- `lazyc2/extensions/storage.py`
- `lazyc2/security/csrf.py`
- `modules/beacon_history.py`
- *... and 30 more*
