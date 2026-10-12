# `scripts/validate_agent_contract.sh`

> Source: [scripts/validate_agent_contract.sh:1](../../scripts/validate_agent_contract.sh#L1) | language `sh` | coverage 50.0% | [API index](../index.md)

validate_agent_contract.sh  CI validation of the AGENTS.md branching model and coding standards.

Called by .github/workflows/agent-contract.yml on every push/PR to dev.  Checks: 1. Branch name matches allowed patterns (dev, main, pp, feature/*, hotfix/*). 2. No commits from dev directly target main (PRs only). 3. No secrets or credentials committed (baseline check). 4. No Spanish strings in code files (enforce English-only rule). 5. No hardcoded IPs/paths/creds outside payload.json.

## Contents

- **Functions:** [`pass`](#pass), [`fail`](#fail), [`check`](#check), [`check_no_hardcoded_passwords`](#check_no_hardcoded_passwords), [`check_no_hardcoded_wordlists`](#check_no_hardcoded_wordlists)

## Functions

<a id="pass"></a>

### `pass`

`function` | [scripts/validate_agent_contract.sh:23](../../scripts/validate_agent_contract.sh#L23)

```bash
pass()
```

---

<a id="fail"></a>

### `fail`

`function` | [scripts/validate_agent_contract.sh:27](../../scripts/validate_agent_contract.sh#L27)

```bash
fail()
```

---

<a id="check"></a>

### `check`

`function` | [scripts/validate_agent_contract.sh:32](../../scripts/validate_agent_contract.sh#L32)

```bash
check()
```

---

<a id="check_no_hardcoded_passwords"></a>

### `check_no_hardcoded_passwords`

`function` | [scripts/validate_agent_contract.sh:59](../../scripts/validate_agent_contract.sh#L59)

```bash
check_no_hardcoded_passwords()
```

--- No hardcoded credentials outside payload.json ---
Pentest help-text, doc placeholders (<...>), template vars ({{ ... }}),
shell arg plumbing ($1/$2/${...}), key-name constants and test fixtures
are not committed secrets. Implemented as a function to avoid eval
quoting pitfalls with nested quote classes.

---

<a id="check_no_hardcoded_wordlists"></a>

### `check_no_hardcoded_wordlists`

`function` | [scripts/validate_agent_contract.sh:74](../../scripts/validate_agent_contract.sh#L74)

```bash
check_no_hardcoded_wordlists()
```

--- No hardcoded wordlist paths outside payload.json ---
Help-text examples, docstrings and filesystem hints are allowed; only real
default assignments outside payload.json are violations.

---
