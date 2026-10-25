# `modules/gui_askpass.sh`

> Source: [modules/gui_askpass.sh:1](../../modules/gui_askpass.sh#L1) | language `sh` | coverage 33.3% | [API index](../index.md)

gui_askpass.sh — SUDO_ASKPASS helper for LazyOwn MCP  Used by: sudo -A <script>  (set SUDO_ASKPASS to this file's path)  Tries GUI backends in order of preference.

Outputs the password to stdout (as required by SUDO_ASKPASS protocol). On cancel / error: exits non-zero so sudo aborts cleanly.  Backend priority: 1. zenity        (GTK, GNOME) 2. yad           (GTK, modern) 3. ssh-askpass   (any X11) 4. kdialog       (KDE/Qt) 5. xterm -e read (fallback — last resort X11)

## Contents

- **Functions:** [`has`](#has), [`try_zenity`](#try_zenity), [`try_yad`](#try_yad), [`try_ssh_askpass`](#try_ssh_askpass), [`try_kdialog`](#try_kdialog)

## Functions

<a id="has"></a>

### `has`

`function` | [modules/gui_askpass.sh:22](../../modules/gui_askpass.sh#L22)

```bash
has() { command -v "$1" &>/dev/null; }
```

── helpers ───────────────────────────────────────────────────────────────────

---

<a id="try_zenity"></a>

### `try_zenity`

`function` | [modules/gui_askpass.sh:24](../../modules/gui_askpass.sh#L24)

```bash
try_zenity()
```

---

<a id="try_yad"></a>

### `try_yad`

`function` | [modules/gui_askpass.sh:28](../../modules/gui_askpass.sh#L28)

```bash
try_yad()
```

---

<a id="try_ssh_askpass"></a>

### `try_ssh_askpass`

`function` | [modules/gui_askpass.sh:33](../../modules/gui_askpass.sh#L33)

```bash
try_ssh_askpass()
```

---

<a id="try_kdialog"></a>

### `try_kdialog`

`function` | [modules/gui_askpass.sh:40](../../modules/gui_askpass.sh#L40)

```bash
try_kdialog()
```

---
