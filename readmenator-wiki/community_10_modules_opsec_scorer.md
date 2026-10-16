# modules: opsec_scorer

*Community 10 | 20 files | cohesion 0.37*

## Definition

This community groups 20 file(s) rooted at `modules` with dominant language py (cohesion 0.37). Central symbols: `AESdecrypt`, `AESencrypt`, `AutoCryptoConfig`, `AutoCryptoEngine`, `Bogus`, `BridgeCatalog`, `CrackResult`, `Dummy`. Core file: `tests/test_core.py` (47 symbols). Documented purpose: Automatic encryption of sensitive session data on app open/close.  Before this module the operator had to manually run ``lazyenc.py encrypt`` and ``lazyenc.py d.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/auto_crypto.py` | py | utility | 13 | yes |
| `cli/commands/opsec_cleanup.py` | py | utility | 9 | yes |
| `cli/commands/security.py` | py | utility | 8 | yes |
| `core/credential_vault.py` | py | utility | 8 | yes |
| `core/crypto.py` | py | utility | 7 | yes |
| `core/protocols.py` | py | utility | 12 | yes |
| `modules/forensic_cleaner.py` | py | utility | 8 | yes |
| `modules/hash_cracker.py` | py | utility | 17 | yes |
| `modules/log_tamper.py` | py | utility | 9 | yes |
| `modules/memory_cleaner.py` | py | utility | 7 | yes |
| `modules/network_opsec.py` | py | utility | 12 | yes |
| `modules/opsec_scorer.py` | py | utility | 36 | yes |
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |
| `modules/timestomper.py` | py | utility | 12 | yes |
| `tests/test_auto_crypto.py` | py | testing | 22 | yes |
| `tests/test_core.py` | py | testing | 47 | yes |
| `tests/test_credential_vault.py` | py | testing | 16 | yes |
| `tests/test_hash_cracker.py` | py | testing | 22 | yes |
| `tests/test_opsec_scorer.py` | py | testing | 13 | yes |
| `tests/test_opsec_scorer_consolidated.py` | py | testing | 22 | yes |

## Key Symbols

- `AutoCryptoConfig` (class, `cli/auto_crypto.py:48`) `class AutoCryptoConfig` - Centralised configuration for automatic session encryption.
- `AutoCryptoEngine` (class, `cli/auto_crypto.py:77`) `class AutoCryptoEngine` - Encrypt and decrypt sensitive session files with a derived key.
- `__init__` (method, `cli/auto_crypto.py:85`) `def __init__(self, config)`
- `enabled` (method, `cli/auto_crypto.py:90`) `def enabled(self)` - Whether the engine performs any I/O.
- `is_encrypted` (method, `cli/auto_crypto.py:95`) `def is_encrypted(self)` - Check whether session data appears encrypted.
- `encrypt_session` (method, `cli/auto_crypto.py:124`) `def encrypt_session(self)` - Encrypt all protected session files.
- `decrypt_session` (method, `cli/auto_crypto.py:174`) `def decrypt_session(self)` - Decrypt all protected session files.
- `has_password` (method, `cli/auto_crypto.py:239`) `def has_password(self)` - Return True when the configured provider yields a password now.
- `_get_password` (method, `cli/auto_crypto.py:251`) `def _get_password(self)`
- `_load_or_create_salt` (method, `cli/auto_crypto.py:260`) `def _load_or_create_salt(self)`
- `_derive_key` (method, `cli/auto_crypto.py:291`) `def _derive_key(password, salt)`
- `build_password_provider_from_cli_login` (function, `cli/auto_crypto.py:297`) `def build_password_provider_from_cli_login()` - Return a password provider that reads the CLI login session.
- `_provider` (function, `cli/auto_crypto.py:310`) `def _provider()`
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 33
- Cross-boundary resolved imports (EXTRACTED): 63

## Connections

- [EXTRACTED] depends_on community 10 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 10 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.

## Risks

- [dataflow UNCHECKED_ALLOC] `cli/auto_crypto.py:272` `_load_or_create_salt` `fd`: Result of allocator stored in `fd` is never checked against NULL.

## Open Questions

- What would break if the most connected file in modules: opsec_scorer changed?
- Should modules: opsec_scorer be split, given cohesion 0.37?

## Sources

- `cli/auto_crypto.py`
- `cli/commands/opsec_cleanup.py`
- `cli/commands/security.py`
- `core/credential_vault.py`
- `core/crypto.py`
- `core/protocols.py`
- `modules/forensic_cleaner.py`
- `modules/hash_cracker.py`
- `modules/log_tamper.py`
- `modules/memory_cleaner.py`
- `modules/network_opsec.py`
- `modules/opsec_scorer.py`
- `modules/rootkit/rootkit.c`
- `modules/timestomper.py`
- `tests/test_auto_crypto.py`
- `tests/test_core.py`
- `tests/test_credential_vault.py`
- `tests/test_hash_cracker.py`
- `tests/test_opsec_scorer.py`
- `tests/test_opsec_scorer_consolidated.py`
