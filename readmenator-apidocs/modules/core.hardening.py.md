# `core.hardening`

> Source: [core/hardening.py:1](../../core/hardening.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Centralized security hardening utilities for the LazyOwn framework.

Contract: provides safe alternatives to dangerous patterns found across
the codebase. Every function is a single-responsibility security control
that replaces ad-hoc, vulnerable patterns with a tested, auditable path.

Invariants:

1. `[`safe_subprocess_run`](#safe_subprocess_run)` never invokes a shell unless explicitly allowed
   and audited.
2. `[`safe_clipboard_copy`](#safe_clipboard_copy)` uses subprocess list-form, never os.system.
3. ``validate_sshpass_env`` sets SSHPASS env var and uses sshpass -e,
   never sshpass -p.
4. ``escape_html`` sanitizes all user-controlled data before HTML insertion.
5. `[`safe_path_join`](#safe_path_join)` prevents path traversal via os.path.realpath prefix
   check.
6. `[`require_encryption_key`](#require_encryption_key)` refuses to operate with a static fallback key.
7. `[`defused_xml_parse`](#defused_xml_parse)` wraps defusedxml for safe XML parsing.

## Contents

- **Exceptions:** [`SecurityViolation`](#securityviolation)
- **Functions:** [`reject_option_injection`](#reject_option_injection), [`escape_powershell_single_quoted`](#escape_powershell_single_quoted), [`safe_subprocess_run`](#safe_subprocess_run), [`safe_clipboard_copy`](#safe_clipboard_copy), [`build_sshpass_command`](#build_sshpass_command), [`set_sshpass_env`](#set_sshpass_env), [`escape_html_content`](#escape_html_content), [`safe_path_join`](#safe_path_join), [`validate_network_cidr`](#validate_network_cidr), [`validate_port_spec`](#validate_port_spec), [`validate_host`](#validate_host), [`require_encryption_key`](#require_encryption_key), [`defused_xml_parse`](#defused_xml_parse), [`sanitize_filename`](#sanitize_filename)
- **Constants:** [`MAX_SSH_COMMAND_LENGTH`](#max_ssh_command_length), [`MAX_CLIPBOARD_CONTENT_LENGTH`](#max_clipboard_content_length), [`SHELL_OPERATOR_CHARS`](#shell_operator_chars), [`PROGRAM_NAME_PATTERN`](#program_name_pattern)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class SecurityViolation
    <<exception>> SecurityViolation
    class PermissionError
    PermissionError <|-- SecurityViolation
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_core_hardening_py__reject_option_injection(["reject_option_injection"])
    n_core_hardening_py__SecurityViolation(["SecurityViolation"])
    n_core_hardening_py__safe_subprocess_run(["safe_subprocess_run"])
    n_core_hardening_py__safe_clipboard_copy(["safe_clipboard_copy"])
    n_core_hardening_py__build_sshpass_command(["build_sshpass_command"])
    n_core_hardening_py__set_sshpass_env(["set_sshpass_env"])
    n_core_hardening_py__safe_path_join(["safe_path_join"])
    n_core_hardening_py__require_encryption_key(["require_encryption_key"])
    n_core_hardening_py__reject_option_injection --> n_core_hardening_py__SecurityViolation
    n_core_hardening_py__safe_subprocess_run --> n_core_hardening_py__SecurityViolation
    n_core_hardening_py__safe_clipboard_copy --> n_core_hardening_py__SecurityViolation
    n_core_hardening_py__build_sshpass_command --> n_core_hardening_py__SecurityViolation
    n_core_hardening_py__set_sshpass_env --> n_core_hardening_py__SecurityViolation
    n_core_hardening_py__safe_path_join --> n_core_hardening_py__SecurityViolation
    n_core_hardening_py__require_encryption_key --> n_core_hardening_py__SecurityViolation
```

## Exceptions

<a id="securityviolation"></a>

### `SecurityViolation`

`exception` | [core/hardening.py:82](../../core/hardening.py#L82)

```python
class SecurityViolation(PermissionError)
```

Bases: [`PermissionError`](core.errors.py.md#permissionerror)

Raised when a security invariant is violated.

---

## Functions

<a id="reject_option_injection"></a>

### `reject_option_injection`

`function` | [core/hardening.py:42](../../core/hardening.py#L42)

```python
def reject_option_injection(argv: Sequence[str], *, allow_options: bool = True) -> None
```

Reject argument-injection payloads in argv.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `argv` | `Sequence[str]` |  | Program and arguments as a sequence. |
| `allow_options` | `bool` | `True` | When False, reject any argument starting with dash. |

**Raises**

- [`SecurityViolation`](#securityviolation): If an injection pattern is detected.

*Calls:* [`SecurityViolation`](#securityviolation)

---

<a id="escape_powershell_single_quoted"></a>

### `escape_powershell_single_quoted`

`function` | [core/hardening.py:61](../../core/hardening.py#L61)

```python
def escape_powershell_single_quoted(value: str) -> str
```

Escape a value for embedding in a PowerShell single-quoted string.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `str` |  | Raw value that may contain quotes or metacharacters. |

**Returns:** `str` - Value safe to embed between single quotes in PowerShell.

*Called by:* [`PersistMigratedCommandSet.do_grisun0w`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_grisun0w)

---

<a id="safe_subprocess_run"></a>

### `safe_subprocess_run`

`function` | [core/hardening.py:107](../../core/hardening.py#L107)

```python
def safe_subprocess_run(argv: Sequence[str], *, timeout: float | None = None, capture_output: bool = True, reason: str = '') -> subprocess.CompletedProcess[str]
```

Execute a command via subprocess without shell interpretation.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `argv` | `Sequence[str]` |  | Program and arguments as a sequence. Must not be empty. |
| `timeout` | `float \| None` | `None` | Optional wall-clock timeout in seconds. |
| `capture_output` | `bool` | `True` | Whether to capture stdout and stderr. |
| `reason` | `str` | `''` | Free-text justification for audit logging. |

**Returns:** `subprocess.CompletedProcess[str]` - CompletedProcess result.

**Raises**

- [`SecurityViolation`](#securityviolation): If argv is empty or contains shell metacharacters.
- `ValueError`: If argv is empty.

*Calls:* [`SecurityViolation`](#securityviolation)

*Called by:* [`CloudCommandSet.do_cloud_iam`](cli.commands.cloud.py.md#cloudcommandset-do_cloud_iam), [`WebSocketBeacon.run`](modules.websocket_beacon.py.md#websocketbeacon-run)

---

<a id="safe_clipboard_copy"></a>

### `safe_clipboard_copy`

`function` | [core/hardening.py:152](../../core/hardening.py#L152)

```python
def safe_clipboard_copy(content: str) -> bool
```

Copy content to system clipboard without shell interpretation.

Uses subprocess list-form with xclip or xsel. Never uses os.system.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `content` | `str` |  | Text to copy to clipboard. |

**Returns:** `bool` - True if copy succeeded, False otherwise.

**Raises**

- [`SecurityViolation`](#securityviolation): If content exceeds MAX_CLIPBOARD_CONTENT_LENGTH.

*Calls:* [`SecurityViolation`](#securityviolation)

*Called by:* [`NetworkHelpersCommandSet.do_rhost`](cli.commands.nethelpers.py.md#networkhelperscommandset-do_rhost), [`PersistMigratedCommandSet.do_grisun0`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_grisun0), [`PersistMigratedCommandSet.do_rdp`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_rdp)

---

<a id="build_sshpass_command"></a>

### `build_sshpass_command`

`function` | [core/hardening.py:191](../../core/hardening.py#L191)

```python
def build_sshpass_command(password: str, ssh_args: list[str], *, max_password_length: int = 256) -> list[str]
```

Build an sshpass command using SSHPASS env var (sshpass -e).

Never uses sshpass -p which exposes passwords in process listings.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `password` | `str` |  | The SSH password to use. |
| `ssh_args` | `list[str]` |  | Arguments to pass to ssh/scp after sshpass. |
| `max_password_length` | `int` | `256` | Maximum allowed password length. |

**Returns:** `list[str]` - List of command arguments suitable for subprocess.run.

**Raises**

- [`SecurityViolation`](#securityviolation): If password exceeds max_password_length or contains characters that could break the env var.

*Calls:* [`SecurityViolation`](#securityviolation)

---

<a id="set_sshpass_env"></a>

### `set_sshpass_env`

`function` | [core/hardening.py:220](../../core/hardening.py#L220)

```python
def set_sshpass_env(password: str) -> dict[str, str]
```

Create an environment dict with SSHPASS set for sshpass -e.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `password` | `str` |  | The SSH password. |

**Returns:** `dict[str, str]` - Copy of os.environ with SSHPASS set.

**Raises**

- [`SecurityViolation`](#securityviolation): If password contains null bytes.

*Calls:* [`SecurityViolation`](#securityviolation)

*Called by:* [`AntiForensicsCommandSet.do_clean_ad`](cli.commands.anti_forensics.py.md#antiforensicscommandset-do_clean_ad), [`CommandAndControlMigratedCommandSet.do_atomic_agent`](cli.commands.command_and_control_migrated.py.md#commandandcontrolmigratedcommandset-do_atomic_agent), [`ExfiltrationCommandSet.do_rsync`](cli.commands.exfiltration.py.md#exfiltrationcommandset-do_rsync), [`LateralMigratedCommandSet.do_lateral_mov_lin`](cli.commands.lateral_migrated.py.md#lateralmigratedcommandset-do_lateral_mov_lin), [`PersistMigratedCommandSet.do_ftp`](cli.commands.persist_migrated.py.md#persistmigratedcommandset-do_ftp)

---

<a id="escape_html_content"></a>

### `escape_html_content`

`function` | [core/hardening.py:239](../../core/hardening.py#L239)

```python
def escape_html_content(value: str) -> str
```

Escape HTML special characters to prevent XSS.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `str` |  | Raw string that may contain HTML. |

**Returns:** `str` - HTML-escaped string safe for insertion into HTML context.

---

<a id="safe_path_join"></a>

### `safe_path_join`

`function` | [core/hardening.py:251](../../core/hardening.py#L251)

```python
def safe_path_join(base_dir: str, user_path: str) -> str
```

Join base_dir and user_path safely, preventing path traversal.

Uses os.path.realpath to resolve symlinks and .. components, then
verifies the result starts with the allowed base directory.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_dir` | `str` |  | The allowed root directory. |
| `user_path` | `str` |  | User-controlled path component. |

**Returns:** `str` - Resolved absolute path within base_dir.

**Raises**

- [`SecurityViolation`](#securityviolation): If the resolved path escapes base_dir.
- `ValueError`: If user_path is empty or contains only separators.

*Calls:* [`SecurityViolation`](#securityviolation)

*Called by:* [`check_calls`](scripts.devtools.core_smoke.py.md#check_calls)

---

<a id="validate_network_cidr"></a>

### `validate_network_cidr`

`function` | [core/hardening.py:277](../../core/hardening.py#L277)

```python
def validate_network_cidr(cidr: str) -> bool
```

Validate a network CIDR notation string.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `cidr` | `str` |  | Network address in CIDR notation (e.g. "192.168.1.0/24"). |

**Returns:** `bool` - True if valid CIDR, False otherwise.

---

<a id="validate_port_spec"></a>

### `validate_port_spec`

`function` | [core/hardening.py:289](../../core/hardening.py#L289)

```python
def validate_port_spec(ports: str) -> bool
```

Validate a port specification string.

Supports comma-separated ports and ranges (e.g. "22,80,443-445").

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ports` | `str` |  | Port specification string. |

**Returns:** `bool` - True if valid, False otherwise.

*Called by:* [`check_calls`](scripts.devtools.core_smoke.py.md#check_calls)

---

<a id="validate_host"></a>

### `validate_host`

`function` | [core/hardening.py:305](../../core/hardening.py#L305)

```python
def validate_host(host: str) -> bool
```

Validate a hostname or IP address.

Single policy shared with the CLI gates: plain IPs, CIDR blocks
and hostnames pass, shell metacharacters fail. CIDR-only strings
are additionally accepted by the network pattern below.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `host` | `str` |  | Hostname or IP to validate. |

**Returns:** `bool` - True if valid, False otherwise.

*Called by:* [`AntiForensicsCommandSet.do_shred`](cli.commands.anti_forensics.py.md#antiforensicscommandset-do_shred), [`AntiForensicsCommandSet.do_wipe_free`](cli.commands.anti_forensics.py.md#antiforensicscommandset-do_wipe_free), [`AntiForensicsCommandSet.do_wipe_logs`](cli.commands.anti_forensics.py.md#antiforensicscommandset-do_wipe_logs), [`AntiForensicsCommandSet.do_wipe_timeline`](cli.commands.anti_forensics.py.md#antiforensicscommandset-do_wipe_timeline)

---

<a id="require_encryption_key"></a>

### `require_encryption_key`

`function` | [core/hardening.py:325](../../core/hardening.py#L325)

```python
def require_encryption_key(env_key: str = 'LAZYOWN_SECRET_KEY', secret_file: Path | None = None) -> str
```

Require a proper encryption key; never fall back to a static default.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `env_key` | `str` | `'LAZYOWN_SECRET_KEY'` | Environment variable name for the secret key. |
| `secret_file` | `Path \| None` | `None` | Optional path to a file containing the key. |

**Returns:** `str` - The encryption key string.

**Raises**

- [`SecurityViolation`](#securityviolation): If no key is configured.

*Calls:* [`SecurityViolation`](#securityviolation)

---

<a id="defused_xml_parse"></a>

### `defused_xml_parse`

`function` | [core/hardening.py:353](../../core/hardening.py#L353)

```python
def defused_xml_parse(source: str | Path) -> Any
```

Parse XML safely using defusedxml.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `source` | `str \| Path` |  | File path or string containing XML data. |

**Returns:** `Any` - Parsed XML ElementTree root element.

**Raises**

- `ImportError`: If defusedxml is not installed.
- `ValueError`: If XML parsing fails.

---

<a id="sanitize_filename"></a>

### `sanitize_filename`

`function` | [core/hardening.py:375](../../core/hardening.py#L375)

```python
def sanitize_filename(filename: str, max_length: int = 255) -> str
```

Sanitize a filename by removing dangerous characters.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `filename` | `str` |  | Raw filename from user input. |
| `max_length` | `int` | `255` | Maximum filename length. |

**Returns:** `str` - Sanitized filename with only safe characters.

---

## Constants

<a id="max_ssh_command_length"></a>

### `MAX_SSH_COMMAND_LENGTH`

`constant` | [core/hardening.py:36](../../core/hardening.py#L36)

```python
MAX_SSH_COMMAND_LENGTH = 4096
```

---

<a id="max_clipboard_content_length"></a>

### `MAX_CLIPBOARD_CONTENT_LENGTH`

`constant` | [core/hardening.py:37](../../core/hardening.py#L37)

```python
MAX_CLIPBOARD_CONTENT_LENGTH = 65536
```

---

<a id="shell_operator_chars"></a>

### `SHELL_OPERATOR_CHARS`

`constant` | [core/hardening.py:38](../../core/hardening.py#L38)

```python
SHELL_OPERATOR_CHARS = frozenset([';', '|', '&', '$', '`', '\n', '\r'])
```

---

<a id="program_name_pattern"></a>

### `PROGRAM_NAME_PATTERN`

`constant` | [core/hardening.py:39](../../core/hardening.py#L39)

```python
PROGRAM_NAME_PATTERN = re.compile('^[a-zA-Z0-9._/\\-][a-zA-Z0-9._/\\- ]*$')
```

---
