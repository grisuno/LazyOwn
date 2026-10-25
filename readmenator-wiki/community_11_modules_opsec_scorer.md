# modules: opsec_scorer

*Community 11 | 14 files | cohesion 0.43*

## Definition

This community groups 14 file(s) rooted at `modules` with dominant language py (cohesion 0.43). Central symbols: `CrackResult`, `FileTimestamps`, `ForensicCleaner`, `ForensicCleanerConfig`, `GateAction`, `GatedOpsecScore`, `HashCracker`, `HashIdentifier`. Core file: `modules/opsec_scorer.py` (36 symbols). Documented purpose: OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory, network.  Provides: opsec_score             — Real-time OPSEC risk assess.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/opsec_cleanup.py` | py | utility | 9 | yes |
| `cli/commands/security.py` | py | utility | 8 | yes |
| `core/credential_vault.py` | py | utility | 8 | yes |
| `modules/forensic_cleaner.py` | py | utility | 8 | yes |
| `modules/hash_cracker.py` | py | utility | 17 | yes |
| `modules/log_tamper.py` | py | utility | 9 | yes |
| `modules/memory_cleaner.py` | py | utility | 7 | yes |
| `modules/network_opsec.py` | py | utility | 12 | yes |
| `modules/opsec_scorer.py` | py | utility | 36 | yes |
| `modules/timestomper.py` | py | utility | 12 | yes |
| `tests/test_credential_vault.py` | py | testing | 16 | yes |
| `tests/test_hash_cracker.py` | py | testing | 22 | yes |
| `tests/test_opsec_scorer.py` | py | testing | 13 | yes |
| `tests/test_opsec_scorer_consolidated.py` | py | testing | 22 | yes |

## Key Symbols

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
- `check_dangerous_defaults` (function, `core/credential_vault.py:63`) `def check_dangerous_defaults(payload)` - Scan payload for unchanged default credential values.
- `_get_aes_key` (function, `core/credential_vault.py:79`) `def _get_aes_key(payload)` - Resolve the AES key from payload, disk, or generate fresh.
- `seal_value` (function, `core/credential_vault.py:93`) `def seal_value(plaintext, key)` - Encrypt a single credential value.
- `unseal_value` (function, `core/credential_vault.py:112`) `def unseal_value(sealed, key)` - Decrypt a sealed credential value.
- `seal_payload` (function, `core/credential_vault.py:141`) `def seal_payload(payload, key)` - Return a copy of ``payload`` with all sensitive values encrypted.
- `unseal_payload` (function, `core/credential_vault.py:164`) `def unseal_payload(payload, key)` - Return a copy of ``payload`` with all sealed values decrypted.
- `rotate_aes_key` (function, `core/credential_vault.py:186`) `def rotate_aes_key(payload, current_key)` - Generate a new AES key, re-encrypt all sealed values under it.
- `generate_secure_defaults` (function, `core/credential_vault.py:215`) `def generate_secure_defaults()` - Generate cryptographically random default values for sensitive keys.
- `ForensicCleanerConfig` (class, `modules/forensic_cleaner.py:23`) `class ForensicCleanerConfig` - Configuration for forensic artifact cleaning.
- `ForensicCleaner` (class, `modules/forensic_cleaner.py:57`) `class ForensicCleaner` - Generate artifact removal commands for Windows, Linux, and macOS.
- `__init__` (method, `modules/forensic_cleaner.py:67`) `def __init__(self, config)`
- `windows_cleanup` (method, `modules/forensic_cleaner.py:70`) `def windows_cleanup(self)` - Generate Windows forensic artifact cleanup commands.
- `linux_cleanup` (method, `modules/forensic_cleaner.py:165`) `def linux_cleanup(self)` - Generate Linux forensic artifact cleanup commands.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 20
- Cross-boundary resolved imports (EXTRACTED): 22

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` be broken with an interface?
- What would break if the most connected file in modules: opsec_scorer changed?
- Should modules: opsec_scorer be split, given cohesion 0.43?

## Sources

- `cli/commands/opsec_cleanup.py`
- `cli/commands/security.py`
- `core/credential_vault.py`
- `modules/forensic_cleaner.py`
- `modules/hash_cracker.py`
- `modules/log_tamper.py`
- `modules/memory_cleaner.py`
- `modules/network_opsec.py`
- `modules/opsec_scorer.py`
- `modules/timestomper.py`
- `tests/test_credential_vault.py`
- `tests/test_hash_cracker.py`
- `tests/test_opsec_scorer.py`
- `tests/test_opsec_scorer_consolidated.py`
