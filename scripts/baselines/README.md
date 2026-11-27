# Bandit baselines

`bandit_baseline.json` is the **ratchet baseline** for first-party code
(`cli/`, `core/`, `modules/`, `skills/`, `utils.py`, `lazyown.py`,
`lazyc2.py`). The security workflow runs bandit with
`-b scripts/baselines/bandit_baseline.json`: any finding that is NOT in
the baseline fails the build. Findings already in the baseline do not,
so the set can only shrink or stay equal — never grow.

## Triage state (generated 2026-11-27)

No HIGH-severity findings exist in first-party code. The 182 baselined
findings are MEDIUM, dominated by families expected in a red-team
framework that shells out and scrapes feeds:

- **B310** (`urllib_urlopen` over user-controlled URLs, 39): the whole
  point of the tool — feed scrapers and web probes. Shrinks per-module
  as callers migrate to `requests` + `core` hardening helpers.
- **B108** (hardcoded `/tmp`, 49): sandbox/test paths; burns down as
  call sites adopt `tempfile` + `core.paths`.
- **B104** (hardcoded bind `0.0.0.0`, 45): listeners intentionally bind
  all interfaces; the operator chooses `lhost` via `payload.json`.
- **B314** (`xml.etree` parse, 10): remaining call sites of the shared
  defusedxml parser (`modules/nmap_fingerprint.py`); each one is a
  migration candidate.
- **B103/B303/B601/B113/B604/B608** (long tail): triaged individually;
  do not add to this file by hand.

B404/B603/B607 (subprocess import/invocation) are below the `-ll`
medium-only threshold by design: the framework shells out to security
tools everywhere and flagging them would be pure noise.

## Updating

Shrink the baseline when you fix findings:

    bandit -c pyproject.toml -r cli core modules skills utils.py lazyown.py lazyc2.py \
      -ll -f json -o scripts/baselines/bandit_baseline.json

then strip anything already fixed (the gate fails only on NEW findings,
so the committed file may stay larger than reality — remove the stale
entries when you touch them). Never add findings to make CI pass.
