# skills/claude_md_orchestrator

skills/claude_md_orchestrator groups 29 files (c, py) around main, _now_iso, Stage, Severity, Contract. Phishing Wizard command set.

```mermaid
graph LR
    cli["cli"]
    contrib["contrib"]
    modules["modules"]
    root["root"]
    skills["skills"]
    tests["tests"]
    cli -- "depends on" --> modules
    contrib -- "depends on" --> modules
    root -- "calls into" --> modules
    root -- "depends on" --> skills
    skills -- "depends on" --> modules
    tests -- "calls into" --> modules
```

## cli (9.1)

cli groups 1 files (py) around PhishingWizardCommandSet, do_phish_wizard, do_phish_serve, PhishingHandler, log_message. Phishing Wizard command set.

## contrib (9.2)

contrib groups 2 files (py) around SamsungKnoxExploitServer, do_GET, apk_bytes, launch_html, exploit_js.

## modules (9.3)

modules groups 3 files (c, py) around main, SecurityConfig, from_payload, HeaderValueSanitizer, __init__. Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de...

## root (9.4)

root groups 1 files (py) around _build_substitutions, _fix_sessions_owner, _run_tool. This software must not be used by military or secret service organisations.

## skills (9.5)

skills groups 21 files (py) around _now_iso, Stage, Severity, Contract, to_dict. Public API for the claude_md_orchestrator skill.

## tests (9.6)

tests groups 1 files (py) around cfg, TestSecurityConfig, test_defaults_are_conservative, test_from_payload_accepts_known_keys, test_from_payload_drops_wrong_types. Unit tests for :mod:`modules.security_sanitizers`.

**Files**:

- cli/commands/phishing_wizard.py
- contrib/legacy/lazygalazy.py
- contrib/legacy/lazyhttpreverseshell.py
- modules/backdoor/server.c
- modules/lazyown_bprfuzzer.py
- modules/security_sanitizers.py
- pwntomate.py
- skills/claude_md_orchestrator/__init__.py
- skills/claude_md_orchestrator/bdd_agent.py
- skills/claude_md_orchestrator/boy_scout.py
- skills/claude_md_orchestrator/cicd_agent.py
- skills/claude_md_orchestrator/config.py
- skills/claude_md_orchestrator/documentation_agent.py
- skills/claude_md_orchestrator/models.py
- skills/claude_md_orchestrator/orchestrator.py
- skills/claude_md_orchestrator/parser.py
- skills/claude_md_orchestrator/reviewer_agent.py
- skills/claude_md_orchestrator/sdd_agent.py
- skills/claude_md_orchestrator/tdd_agent.py
- skills/claude_md_orchestrator/validators.py
- skills/hermes-lazyown/claudemd_rules.py
- skills/hermes-lazyown/config_bridge.py
- skills/hermes-lazyown/constants.py
- skills/hermes-lazyown/executor.py
- skills/hermes-lazyown/hermes_sync.py
- skills/hermes-lazyown/mcp_server.py
- skills/hermes-lazyown/output_compactor.py
- skills/lazyown_mcp_opencode.py
- tests/test_security_sanitizers.py
