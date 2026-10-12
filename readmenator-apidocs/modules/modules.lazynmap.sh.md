# `modules/lazynmap.sh`

> Source: [modules/lazynmap.sh:1](../../modules/lazynmap.sh#L1) | language `sh` | coverage 22.2% | [API index](../index.md)

Nombre del script: lazynmap.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este script contiene la lógica principal de la aplicación. lazynmap Licencia: GPL v3

## Contents

- **Functions:** [`cleanup`](#cleanup), [`ctrl_c`](#ctrl_c), [`fix_sessions_owner`](#fix_sessions_owner), [`nmaptest`](#nmaptest), [`discover_network`](#discover_network), [`extract_ports_info`](#extract_ports_info), [`run_nmap_script`](#run_nmap_script), [`print_row`](#print_row)

## Functions

<a id="cleanup"></a>

### `cleanup`

`function` | [modules/lazynmap.sh:29](../../modules/lazynmap.sh#L29)

```bash
cleanup()
```

---

<a id="ctrl_c"></a>

### `ctrl_c`

`function` | [modules/lazynmap.sh:38](../../modules/lazynmap.sh#L38)

```bash
function ctrl_c()
```

---

<a id="fix_sessions_owner"></a>

### `fix_sessions_owner`

`function` | [modules/lazynmap.sh:74](../../modules/lazynmap.sh#L74)

```bash
fix_sessions_owner()
```

Best-effort ownership fixup: scans run under sudo leave root-owned files behind, and only root can chown those.

Try passwordless sudo first, fall back to a plain call, and stay silent when neither is permitted (non-fatal: the scan artefacts themselves are already written at this point).

---

<a id="nmaptest"></a>

### `nmaptest`

`function` | [modules/lazynmap.sh:129](../../modules/lazynmap.sh#L129)

```bash
nmaptest()
```

---

<a id="discover_network"></a>

### `discover_network`

`function` | [modules/lazynmap.sh:149](../../modules/lazynmap.sh#L149)

```bash
discover_network()
```

---

<a id="extract_ports_info"></a>

### `extract_ports_info`

`function` | [modules/lazynmap.sh:818](../../modules/lazynmap.sh#L818)

```bash
extract_ports_info()
```

---

<a id="run_nmap_script"></a>

### `run_nmap_script`

`function` | [modules/lazynmap.sh:844](../../modules/lazynmap.sh#L844)

```bash
run_nmap_script()
```

---

<a id="print_row"></a>

### `print_row`

`function` | [modules/lazynmap.sh:877](../../modules/lazynmap.sh#L877)

```bash
print_row()
```

---
