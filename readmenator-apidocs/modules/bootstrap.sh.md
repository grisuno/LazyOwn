# `bootstrap.sh`

> Source: [bootstrap.sh:1](../../bootstrap.sh#L1) | language `sh` | coverage 5.9% | [API index](../index.md)

LazyOwn bootstrap installer (one-liner entry point).

Clones the repository into a target directory (default: $HOME/LazyOwn), runs install.sh, then asks whether to launch a normal session (./run) or the full stack as root (fast_run_as_r00t.sh).  One-liner (download first, then run — immune to pipe stalls and CDN cache): curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh -o /tmp/bootstrap.sh \ && bash /tmp/bootstrap.sh  Pipe alternative (same result, single command): curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh | bash  With options (append after the script path, or use bash -s through the pipe): bash /tmp/bootstrap.sh -- --with-tools --dir ~/pentest/LazyOwn curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh | bash -s -- --with-tools --dir ~/pentest/LazyOwn  asks what to do: update in place (git pull + reinstall), clean install (delete everything and clone fresh), install into a different directory, or abort. Set --existing to skip the question in scripts.  Options: --dir <path>     Install directory (default: $HOME/LazyOwn, or $LAZYOWN_DIR). --branch <name>  Git branch to clone (default: main, or $LAZYOWN_BRANCH). --with-ml        Also install the heavy ML stack (forwarded to install.sh). --with-ollama    Also install the Ollama runtime (forwarded to install.sh). --with-tools     Also apt-install common external pentest tools.

## Contents

- **Functions:** [`usage`](#usage), [`log`](#log), [`fail`](#fail), [`spin_run`](#spin_run), [`can_prompt`](#can_prompt), [`ask`](#ask), [`update_checkout`](#update_checkout), [`backup_payload`](#backup_payload), [`clone_fresh`](#clone_fresh), [`clean_checkout`](#clean_checkout), [`confirm_clean`](#confirm_clean), [`ask_new_dir`](#ask_new_dir), [`ask_existing_checkout_action`](#ask_existing_checkout_action), [`ask_existing_path_action`](#ask_existing_path_action), [`resolve_target_dir`](#resolve_target_dir), [`ask_launch_mode`](#ask_launch_mode)

## Functions

<a id="usage"></a>

### `usage`

`function` | [bootstrap.sh:70](../../bootstrap.sh#L70)

```bash
usage()
```

---

<a id="log"></a>

### `log`

`function` | [bootstrap.sh:74](../../bootstrap.sh#L74)

```bash
log()
```

---

<a id="fail"></a>

### `fail`

`function` | [bootstrap.sh:92](../../bootstrap.sh#L92)

```bash
fail()
```

---

<a id="spin_run"></a>

### `spin_run`

`function` | [bootstrap.sh:97](../../bootstrap.sh#L97)

```bash
spin_run()
```

---

<a id="can_prompt"></a>

### `can_prompt`

`function` | [bootstrap.sh:239](../../bootstrap.sh#L239)

```bash
can_prompt()
```

---

<a id="ask"></a>

### `ask`

`function` | [bootstrap.sh:250](../../bootstrap.sh#L250)

```bash
ask()
```

---

<a id="update_checkout"></a>

### `update_checkout`

`function` | [bootstrap.sh:259](../../bootstrap.sh#L259)

```bash
update_checkout()
```

---

<a id="backup_payload"></a>

### `backup_payload`

`function` | [bootstrap.sh:268](../../bootstrap.sh#L268)

```bash
backup_payload()
```

---

<a id="clone_fresh"></a>

### `clone_fresh`

`function` | [bootstrap.sh:280](../../bootstrap.sh#L280)

```bash
clone_fresh()
```

---

<a id="clean_checkout"></a>

### `clean_checkout`

`function` | [bootstrap.sh:286](../../bootstrap.sh#L286)

```bash
clean_checkout()
```

---

<a id="confirm_clean"></a>

### `confirm_clean`

`function` | [bootstrap.sh:293](../../bootstrap.sh#L293)

```bash
confirm_clean()
```

---

<a id="ask_new_dir"></a>

### `ask_new_dir`

`function` | [bootstrap.sh:303](../../bootstrap.sh#L303)

```bash
ask_new_dir()
```

---

<a id="ask_existing_checkout_action"></a>

### `ask_existing_checkout_action`

`function` | [bootstrap.sh:315](../../bootstrap.sh#L315)

```bash
ask_existing_checkout_action()
```

---

<a id="ask_existing_path_action"></a>

### `ask_existing_path_action`

`function` | [bootstrap.sh:336](../../bootstrap.sh#L336)

```bash
ask_existing_path_action()
```

---

<a id="resolve_target_dir"></a>

### `resolve_target_dir`

`function` | [bootstrap.sh:355](../../bootstrap.sh#L355)

```bash
resolve_target_dir()
```

---

<a id="ask_launch_mode"></a>

### `ask_launch_mode`

`function` | [bootstrap.sh:432](../../bootstrap.sh#L432)

```bash
ask_launch_mode()
```

---
