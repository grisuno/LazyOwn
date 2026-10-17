# modules: opsec_scorer

*Community 11 | 12 files | cohesion 0.46*

## Definition

This community groups 12 file(s) rooted at `modules` with dominant language py (cohesion 0.46). Central symbols: `CrackResult`, `FileTimestamps`, `ForensicCleaner`, `ForensicCleanerConfig`, `GateAction`, `GatedOpsecScore`, `HashCracker`, `HashIdentifier`. Core file: `modules/opsec_scorer.py` (36 symbols). Documented purpose: OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory, network.  Provides: opsec_score             — Real-time OPSEC risk assess.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/opsec_cleanup.py` | py | utility | 9 | yes |
| `cli/commands/security.py` | py | utility | 8 | yes |
| `modules/forensic_cleaner.py` | py | utility | 8 | yes |
| `modules/hash_cracker.py` | py | utility | 17 | yes |
| `modules/log_tamper.py` | py | utility | 9 | yes |
| `modules/memory_cleaner.py` | py | utility | 7 | yes |
| `modules/network_opsec.py` | py | utility | 12 | yes |
| `modules/opsec_scorer.py` | py | utility | 36 | yes |
| `modules/timestomper.py` | py | utility | 12 | yes |
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
- `ForensicCleanerConfig` (class, `modules/forensic_cleaner.py:23`) `class ForensicCleanerConfig` - Configuration for forensic artifact cleaning.
- `ForensicCleaner` (class, `modules/forensic_cleaner.py:57`) `class ForensicCleaner` - Generate artifact removal commands for Windows, Linux, and macOS.
- `__init__` (method, `modules/forensic_cleaner.py:67`) `def __init__(self, config)`
- `windows_cleanup` (method, `modules/forensic_cleaner.py:70`) `def windows_cleanup(self)` - Generate Windows forensic artifact cleanup commands.
- `linux_cleanup` (method, `modules/forensic_cleaner.py:165`) `def linux_cleanup(self)` - Generate Linux forensic artifact cleanup commands.
- `macos_cleanup` (method, `modules/forensic_cleaner.py:193`) `def macos_cleanup(self)` - Generate macOS forensic artifact cleanup commands.
- `windows_prefetch_parse` (method, `modules/forensic_cleaner.py:221`) `def windows_prefetch_parse(self, prefetch_path)` - Parse Prefetch files to identify what the attacker should clean.
- `amcache_parse` (method, `modules/forensic_cleaner.py:259`) `def amcache_parse(self)` - Parse Amcache registry entries for evidence of execution.
- `CrackResult` (class, `modules/hash_cracker.py:127`) `class CrackResult`
- `HashIdentifier` (class, `modules/hash_cracker.py:140`) `class HashIdentifier`
- `HashCracker` (class, `modules/hash_cracker.py:151`) `class HashCracker` - Pipeline for identifying and cracking password hashes.
- `__init__` (method, `modules/hash_cracker.py:164`) `def __init__(self, wordlist, rules, use_hashcat, timeout)`
- `_resolve_wordlist` (method, `modules/hash_cracker.py:178`) `def _resolve_wordlist(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 16
- Cross-boundary resolved imports (EXTRACTED): 20

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: opsec_scorer changed?
- Should modules: opsec_scorer be split, given cohesion 0.46?

## Sources

- `cli/commands/opsec_cleanup.py`
- `cli/commands/security.py`
- `modules/forensic_cleaner.py`
- `modules/hash_cracker.py`
- `modules/log_tamper.py`
- `modules/memory_cleaner.py`
- `modules/network_opsec.py`
- `modules/opsec_scorer.py`
- `modules/timestomper.py`
- `tests/test_hash_cracker.py`
- `tests/test_opsec_scorer.py`
- `tests/test_opsec_scorer_consolidated.py`
