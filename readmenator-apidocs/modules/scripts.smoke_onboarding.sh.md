# `scripts/smoke_onboarding.sh`

> Source: [scripts/smoke_onboarding.sh:1](../../scripts/smoke_onboarding.sh#L1) | language `sh` | coverage 50.0% | [API index](../index.md)

Smoke test for the 5-minute onboarding path.

## Contents

- **Functions:** [`check`](#check)

## Functions

<a id="check"></a>

### `check`

`function` | [scripts/smoke_onboarding.sh:8](../../scripts/smoke_onboarding.sh#L8)

```bash
check() { if eval "$2"; then echo "[+] $1"; else echo "[!] $1"; fail=1; fi; }
```

---
