# modules: network_opsec

modules: network_opsec groups 6 files (py) around LogTamperConfig, LogTamper, __init__, windows_clear_commands, linux_clear_commands. OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory...

```mermaid
graph LR
    cli["cli"]
    modules["modules"]
    cli -- "calls into" --> modules
```

## cli (16.1)

cli groups 1 files (py) around OpsecCleanupCommandSet, do_opsec_score, do_log_tamper, do_forensic_clean, do_timestomp. OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory...

## modules (16.2)

modules groups 5 files (py) around LogTamperConfig, LogTamper, __init__, windows_clear_commands, linux_clear_commands. Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup.

**Files**:

- cli/commands/opsec_cleanup.py
- modules/forensic_cleaner.py
- modules/log_tamper.py
- modules/memory_cleaner.py
- modules/network_opsec.py
- modules/timestomper.py
