# `install.sh`

> Source: [install.sh:1](../../install.sh#L1) | language `sh` | coverage 5.9% | [API index](../index.md)

LazyOwn installer.

Provisions system packages (Debian/Kali via apt), a Python virtualenv with the pinned dependency lock, external storage and encoder modules, and self-signed TLS certs. The default install is intentionally light; heavy extras are opt-in via flags.  Dependencies are declared once in pyproject.toml and pinned in requirements.txt / requirements-ml.txt. This script never duplicates the list.  Usage: bash install.sh [--profile light|full] [--with-ml] [--with-ollama] [--with-tools] [--no-ml] [--no-ollama] [--help]  --profile <name>  Install profile: full (default, everything in requirements.txt) or light (shell + C2 + recon core from requirements-light.txt, without the analytics/AI stack). Overridable per shell with LAZYOWN_PROFILE=light. --with-ml       Also install the heavy, platform-specific ML stack (torch/CUDA, sklearn ~2 GB). Skipped by default. --with-ollama   Also install the local Ollama runtime. Skipped by default. --with-tools    Also apt-install the common external pentest tools (gobuster, ffuf, enum4linux, seclists, responder, ...). --no-ml         Accepted for backwards compatibility (ML is off by default). --no-ollama     Accepted for backwards compatibility (Ollama is off by default). --help          Show this help and exit.

## Contents

- **Functions:** [`usage`](#usage), [`log`](#log), [`spin_run`](#spin_run), [`ensure_gum`](#ensure_gum), [`install_system_packages`](#install_system_packages), [`install_external_tools`](#install_external_tools), [`install_python_environment`](#install_python_environment), [`install_ollama`](#install_ollama), [`install_external_storage`](#install_external_storage), [`install_lazyownbt`](#install_lazyownbt), [`download_file`](#download_file), [`install_encoder_module`](#install_encoder_module), [`generate_certificates`](#generate_certificates), [`seed_payload_config`](#seed_payload_config), [`verify_installation`](#verify_installation), [`main`](#main)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_install_sh__install_external_tools(["install_external_tools"])
    n_cli_exploration_py__ExplorationEngine_tools["exploration.ExplorationEngine.tools"]
    n_install_sh__install_external_tools -.-> n_cli_exploration_py__ExplorationEngine_tools
```

## Functions

<a id="usage"></a>

### `usage`

`function` | [install.sh:49](../../install.sh#L49)

```bash
usage()
```

---

<a id="log"></a>

### `log`

`function` | [install.sh:88](../../install.sh#L88)

```bash
log()
```

---

<a id="spin_run"></a>

### `spin_run`

`function` | [install.sh:98](../../install.sh#L98)

```bash
spin_run()
```

---

<a id="ensure_gum"></a>

### `ensure_gum`

`function` | [install.sh:128](../../install.sh#L128)

```bash
ensure_gum()
```

---

<a id="install_system_packages"></a>

### `install_system_packages`

`function` | [install.sh:139](../../install.sh#L139)

```bash
install_system_packages()
```

---

<a id="install_external_tools"></a>

### `install_external_tools`

`function` | [install.sh:150](../../install.sh#L150)

```bash
install_external_tools()
```

*Calls:* [`ExplorationEngine.tools`](cli.exploration.py.md#explorationengine-tools)

---

<a id="install_python_environment"></a>

### `install_python_environment`

`function` | [install.sh:165](../../install.sh#L165)

```bash
install_python_environment()
```

---

<a id="install_ollama"></a>

### `install_ollama`

`function` | [install.sh:206](../../install.sh#L206)

```bash
install_ollama()
```

---

<a id="install_external_storage"></a>

### `install_external_storage`

`function` | [install.sh:218](../../install.sh#L218)

```bash
install_external_storage()
```

---

<a id="install_lazyownbt"></a>

### `install_lazyownbt`

`function` | [install.sh:231](../../install.sh#L231)

```bash
install_lazyownbt()
```

---

<a id="download_file"></a>

### `download_file`

`function` | [install.sh:251](../../install.sh#L251)

```bash
download_file()
```

---

<a id="install_encoder_module"></a>

### `install_encoder_module`

`function` | [install.sh:263](../../install.sh#L263)

```bash
install_encoder_module()
```

---

<a id="generate_certificates"></a>

### `generate_certificates`

`function` | [install.sh:274](../../install.sh#L274)

```bash
generate_certificates()
```

---

<a id="seed_payload_config"></a>

### `seed_payload_config`

`function` | [install.sh:281](../../install.sh#L281)

```bash
seed_payload_config()
```

---

<a id="verify_installation"></a>

### `verify_installation`

`function` | [install.sh:294](../../install.sh#L294)

```bash
verify_installation()
```

---

<a id="main"></a>

### `main`

`function` | [install.sh:310](../../install.sh#L310)

```bash
main()
```

---
