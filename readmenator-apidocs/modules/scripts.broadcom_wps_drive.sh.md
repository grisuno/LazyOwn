# `scripts/broadcom_wps_drive.sh`

> Source: [scripts/broadcom_wps_drive.sh:1](../../scripts/broadcom_wps_drive.sh#L1) | language `sh` | coverage 3.8% | [API index](../index.md)

broadcom_wps_drive.sh - operator-side driver for the Broadcom 802.11 SDK detection toolkit.

The upstream project ships two detectors: a live fingerprinter that tells Broadcom's vulnerable wps_monitor apart from a patched hostapd, and YARA rules for extracted firmware. The live path needs a monitor-mode adapter, root privileges and scapy, and it leaves the adapter in monitor mode. This driver owns that operational overhead:  doctor       report the toolchain, the adapter and the configured SSID monitor      put the adapter in monitor mode unmonitor    restore the adapter to managed mode fingerprint  run the live detector and archive the verdict yara         run the upstream rules against an extracted firmware tree status       report the current state without touching the radio  Usage: broadcom_wps_drive.sh doctor broadcom_wps_drive.sh monitor broadcom_wps_drive.sh unmonitor broadcom_wps_drive.sh fingerprint broadcom_wps_drive.sh yara <firmware-dir> broadcom_wps_drive.sh status  Flags (after the action): --ssid <ssid>        access point to fingerprint --interface <iface>  wireless adapter to use --target <dir>       firmware tree for the YARA pass --keep-monitor       leave the adapter in monitor mode after the run --debug-assoc        log 802.11 auth status codes (passed to the tool)

## Contents

- **Functions:** [`log`](#log), [`warn`](#warn), [`die`](#die), [`usage`](#usage), [`payload_value`](#payload_value), [`parse_flags`](#parse_flags), [`detect_interface`](#detect_interface), [`is_wireless`](#is_wireless), [`apply_interface`](#apply_interface), [`resolve_interface`](#resolve_interface), [`is_root`](#is_root), [`have_sudo`](#have_sudo), [`elevate`](#elevate), [`interface_mode`](#interface_mode), [`interface_up`](#interface_up), [`python_bin`](#python_bin), [`has_scapy`](#has_scapy), [`do_monitor`](#do_monitor), [`do_unmonitor`](#do_unmonitor), [`ensure_monitor_mode`](#ensure_monitor_mode), [`run_fingerprint`](#run_fingerprint), [`run_yara`](#run_yara), [`do_status`](#do_status), [`do_doctor`](#do_doctor), [`main`](#main)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_scripts_broadcom_wps_drive_sh__do_doctor(["do_doctor"])
    n_cli_command_chain_py__PrerequisiteRegistry_prerequisites["command_chain.PrerequisiteRegistry.prerequisites"]
    n_scripts_broadcom_wps_drive_sh__do_doctor -.-> n_cli_command_chain_py__PrerequisiteRegistry_prerequisites
```

## Functions

<a id="log"></a>

### `log`

`function` | [scripts/broadcom_wps_drive.sh:53](../../scripts/broadcom_wps_drive.sh#L53)

```bash
log() { printf '%s\n' "$*"; }
```

---

<a id="warn"></a>

### `warn`

`function` | [scripts/broadcom_wps_drive.sh:54](../../scripts/broadcom_wps_drive.sh#L54)

```bash
warn() { printf '[!] %s\n' "$*" >&2; }
```

---

<a id="die"></a>

### `die`

`function` | [scripts/broadcom_wps_drive.sh:55](../../scripts/broadcom_wps_drive.sh#L55)

```bash
die() { warn "$*"; exit 1; }
```

---

<a id="usage"></a>

### `usage`

`function` | [scripts/broadcom_wps_drive.sh:57](../../scripts/broadcom_wps_drive.sh#L57)

```bash
usage()
```

---

<a id="payload_value"></a>

### `payload_value`

`function` | [scripts/broadcom_wps_drive.sh:61](../../scripts/broadcom_wps_drive.sh#L61)

```bash
payload_value()
```

---

<a id="parse_flags"></a>

### `parse_flags`

`function` | [scripts/broadcom_wps_drive.sh:81](../../scripts/broadcom_wps_drive.sh#L81)

```bash
parse_flags()
```

---

<a id="detect_interface"></a>

### `detect_interface`

`function` | [scripts/broadcom_wps_drive.sh:151](../../scripts/broadcom_wps_drive.sh#L151)

```bash
detect_interface()
```

---

<a id="is_wireless"></a>

### `is_wireless`

`function` | [scripts/broadcom_wps_drive.sh:162](../../scripts/broadcom_wps_drive.sh#L162)

```bash
is_wireless()
```

---

<a id="apply_interface"></a>

### `apply_interface`

`function` | [scripts/broadcom_wps_drive.sh:166](../../scripts/broadcom_wps_drive.sh#L166)

```bash
apply_interface()
```

---

<a id="resolve_interface"></a>

### `resolve_interface`

`function` | [scripts/broadcom_wps_drive.sh:170](../../scripts/broadcom_wps_drive.sh#L170)

```bash
resolve_interface()
```

---

<a id="is_root"></a>

### `is_root`

`function` | [scripts/broadcom_wps_drive.sh:190](../../scripts/broadcom_wps_drive.sh#L190)

```bash
is_root()
```

---

<a id="have_sudo"></a>

### `have_sudo`

`function` | [scripts/broadcom_wps_drive.sh:194](../../scripts/broadcom_wps_drive.sh#L194)

```bash
have_sudo()
```

---

<a id="elevate"></a>

### `elevate`

`function` | [scripts/broadcom_wps_drive.sh:200](../../scripts/broadcom_wps_drive.sh#L200)

```bash
elevate()
```

---

<a id="interface_mode"></a>

### `interface_mode`

`function` | [scripts/broadcom_wps_drive.sh:210](../../scripts/broadcom_wps_drive.sh#L210)

```bash
interface_mode()
```

---

<a id="interface_up"></a>

### `interface_up`

`function` | [scripts/broadcom_wps_drive.sh:216](../../scripts/broadcom_wps_drive.sh#L216)

```bash
interface_up()
```

---

<a id="python_bin"></a>

### `python_bin`

`function` | [scripts/broadcom_wps_drive.sh:227](../../scripts/broadcom_wps_drive.sh#L227)

```bash
python_bin()
```

---

<a id="has_scapy"></a>

### `has_scapy`

`function` | [scripts/broadcom_wps_drive.sh:231](../../scripts/broadcom_wps_drive.sh#L231)

```bash
has_scapy()
```

---

<a id="do_monitor"></a>

### `do_monitor`

`function` | [scripts/broadcom_wps_drive.sh:235](../../scripts/broadcom_wps_drive.sh#L235)

```bash
do_monitor()
```

---

<a id="do_unmonitor"></a>

### `do_unmonitor`

`function` | [scripts/broadcom_wps_drive.sh:247](../../scripts/broadcom_wps_drive.sh#L247)

```bash
do_unmonitor()
```

---

<a id="ensure_monitor_mode"></a>

### `ensure_monitor_mode`

`function` | [scripts/broadcom_wps_drive.sh:259](../../scripts/broadcom_wps_drive.sh#L259)

```bash
ensure_monitor_mode()
```

---

<a id="run_fingerprint"></a>

### `run_fingerprint`

`function` | [scripts/broadcom_wps_drive.sh:268](../../scripts/broadcom_wps_drive.sh#L268)

```bash
run_fingerprint()
```

---

<a id="run_yara"></a>

### `run_yara`

`function` | [scripts/broadcom_wps_drive.sh:308](../../scripts/broadcom_wps_drive.sh#L308)

```bash
run_yara()
```

---

<a id="do_status"></a>

### `do_status`

`function` | [scripts/broadcom_wps_drive.sh:325](../../scripts/broadcom_wps_drive.sh#L325)

```bash
do_status()
```

---

<a id="do_doctor"></a>

### `do_doctor`

`function` | [scripts/broadcom_wps_drive.sh:348](../../scripts/broadcom_wps_drive.sh#L348)

```bash
do_doctor()
```

*Calls:* [`PrerequisiteRegistry.prerequisites`](cli.command_chain.py.md#prerequisiteregistry-prerequisites)

---

<a id="main"></a>

### `main`

`function` | [scripts/broadcom_wps_drive.sh:404](../../scripts/broadcom_wps_drive.sh#L404)

```bash
main()
```

---
