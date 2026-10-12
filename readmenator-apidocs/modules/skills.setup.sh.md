# `skills/setup.sh`

> Source: [skills/setup.sh:1](../../skills/setup.sh#L1) | language `sh` | coverage 33.3% | [API index](../index.md)

============================================================================= LazyOwn MCP — One-time system setup Configures sudoers NOPASSWD and Linux capabilities so LazyOwn tools can run without interactive password prompts (required for MCP / non-TTY contexts).

Usage:  bash skills/setup.sh  Safe to re-run — all operations are idempotent. Supported: Debian/Ubuntu/Kali, Arch, Fedora/RHEL, macOS (capabilities skipped) =============================================================================

## Contents

- **Functions:** [`info`](#info), [`warn`](#warn), [`die`](#die), [`paths_for_sudo`](#paths_for_sudo), [`add_nopasswd`](#add_nopasswd)

## Functions

<a id="info"></a>

### `info`

`function` | [skills/setup.sh:15](../../skills/setup.sh#L15)

```bash
info() { echo -e "${GREEN}[+]${RESET} $*"; }
```

---

<a id="warn"></a>

### `warn`

`function` | [skills/setup.sh:16](../../skills/setup.sh#L16)

```bash
warn() { echo -e "${YELLOW}[!]${RESET} $*"; }
```

---

<a id="die"></a>

### `die`

`function` | [skills/setup.sh:17](../../skills/setup.sh#L17)

```bash
die() { echo -e "${RED}[-]${RESET} $*" >&2; exit 1; }
```

---

<a id="paths_for_sudo"></a>

### `paths_for_sudo`

`function` | [skills/setup.sh:61](../../skills/setup.sh#L61)

```bash
paths_for_sudo()
```

Collect paths that exist on this system

---

<a id="add_nopasswd"></a>

### `add_nopasswd`

`function` | [skills/setup.sh:92](../../skills/setup.sh#L92)

```bash
add_nopasswd()
```

---
