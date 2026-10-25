# `scripts/mutate.sh`

> Source: [scripts/mutate.sh:1](../../scripts/mutate.sh#L1) | language `sh` | coverage 25.0% | [API index](../index.md)

Mutation gate for LazyOwn.

The gate runs the curated mutation runners under tests/. Each runner mutates one production module and asserts the matching test suite kills the mutant. A surviving mutant means the suite does not cover the behaviour, and the gate fails so the gap is closed before the change lands.  Modes: scripts/mutate.sh                    scoped to source files changed vs HEAD scripts/mutate.sh --all              every curated runner scripts/mutate.sh --list             print the available runners scripts/mutate.sh FILE [FILE ...]    runners that reference the given files  Environment: PYTHON             interpreter for the runners (default: env/bin/python3) MUTATION_TIMEOUT   per runner timeout in seconds (default: 1800)

## Contents

- **Functions:** [`runners`](#runners), [`changed_sources`](#changed_sources), [`usage`](#usage)

## Functions

<a id="runners"></a>

### `runners`

`function` | [scripts/mutate.sh:29](../../scripts/mutate.sh#L29)

```bash
runners()
```

---

<a id="changed_sources"></a>

### `changed_sources`

`function` | [scripts/mutate.sh:33](../../scripts/mutate.sh#L33)

```bash
changed_sources()
```

---

<a id="usage"></a>

### `usage`

`function` | [scripts/mutate.sh:40](../../scripts/mutate.sh#L40)

```bash
usage()
```

---
