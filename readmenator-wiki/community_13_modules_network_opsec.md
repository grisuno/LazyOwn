# modules: network_opsec

*Community 13 | 6 files | cohesion 0.71*

## Definition

This community groups 6 file(s) rooted at `modules` with dominant language py (cohesion 0.71). Central symbols: `FileTimestamps`, `ForensicCleaner`, `ForensicCleanerConfig`, `LogTamper`, `LogTamperConfig`, `MemoryCleaner`, `MemoryCleanerConfig`, `NetworkOpsecConfig`. Core file: `modules/network_opsec.py` (12 symbols). Documented purpose: OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory, network.  Provides: opsec_score             — Real-time OPSEC risk assess.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/opsec_cleanup.py` | py | utility | 9 | yes |
| `modules/forensic_cleaner.py` | py | utility | 8 | yes |
| `modules/log_tamper.py` | py | utility | 9 | yes |
| `modules/memory_cleaner.py` | py | utility | 7 | yes |
| `modules/network_opsec.py` | py | utility | 12 | yes |
| `modules/timestomper.py` | py | utility | 12 | yes |

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
- `ForensicCleanerConfig` (class, `modules/forensic_cleaner.py:23`) `class ForensicCleanerConfig` - Configuration for forensic artifact cleaning.
- `ForensicCleaner` (class, `modules/forensic_cleaner.py:57`) `class ForensicCleaner` - Generate artifact removal commands for Windows, Linux, and macOS.
- `__init__` (method, `modules/forensic_cleaner.py:67`) `def __init__(self, config)`
- `windows_cleanup` (method, `modules/forensic_cleaner.py:70`) `def windows_cleanup(self)` - Generate Windows forensic artifact cleanup commands.
- `linux_cleanup` (method, `modules/forensic_cleaner.py:165`) `def linux_cleanup(self)` - Generate Linux forensic artifact cleanup commands.
- `macos_cleanup` (method, `modules/forensic_cleaner.py:193`) `def macos_cleanup(self)` - Generate macOS forensic artifact cleanup commands.
- `windows_prefetch_parse` (method, `modules/forensic_cleaner.py:221`) `def windows_prefetch_parse(self, prefetch_path)` - Parse Prefetch files to identify what the attacker should clean.
- `amcache_parse` (method, `modules/forensic_cleaner.py:259`) `def amcache_parse(self)` - Parse Amcache registry entries for evidence of execution.
- `LogTamperConfig` (class, `modules/log_tamper.py:71`) `class LogTamperConfig` - Configuration for log tampering operations.
- `LogTamper` (class, `modules/log_tamper.py:95`) `class LogTamper` - Cross-platform log tampering with verification.
- `__init__` (method, `modules/log_tamper.py:105`) `def __init__(self, config)`
- `windows_clear_commands` (method, `modules/log_tamper.py:108`) `def windows_clear_commands(self)` - Generate Windows Event Log clearing commands.
- `linux_clear_commands` (method, `modules/log_tamper.py:176`) `def linux_clear_commands(self)` - Generate Linux log clearing commands.
- `macos_clear_commands` (method, `modules/log_tamper.py:243`) `def macos_clear_commands(self)` - Generate macOS log clearing commands.
- `generate_all` (method, `modules/log_tamper.py:295`) `def generate_all(self)` - Generate log tampering commands for all platforms.
- `auditd_disable_commands` (method, `modules/log_tamper.py:307`) `def auditd_disable_commands(self)` - Commands to temporarily disable or reconfigure auditd on Linux.
- `sysmon_disable_commands` (method, `modules/log_tamper.py:341`) `def sysmon_disable_commands(self)` - Commands to disable or degrade Sysmon on Windows.
- `MemoryCleanerConfig` (class, `modules/memory_cleaner.py:22`) `class MemoryCleanerConfig` - Configuration for memory artifact cleanup operations.
- `MemoryCleaner` (class, `modules/memory_cleaner.py:50`) `class MemoryCleaner` - Generate memory artifact cleanup commands for post-operation stealth.
- `__init__` (method, `modules/memory_cleaner.py:61`) `def __init__(self, config)`
- `windows_memory_cleanup` (method, `modules/memory_cleaner.py:64`) `def windows_memory_cleanup(self)` - Generate Windows memory artifact cleanup commands.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 7
- Cross-boundary resolved imports (EXTRACTED): 2

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: network_opsec changed?
- Should modules: network_opsec be split, given cohesion 0.71?

## Sources

- `cli/commands/opsec_cleanup.py`
- `modules/forensic_cleaner.py`
- `modules/log_tamper.py`
- `modules/memory_cleaner.py`
- `modules/network_opsec.py`
- `modules/timestomper.py`
