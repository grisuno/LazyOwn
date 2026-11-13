# `cli.commands.browser_sync`

> Source: [cli/commands/browser_sync.py:1](../../cli/commands/browser_sync.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

BrowserSync shell commands: operator browser identity into the proxy.

## Contents

- **Classes:** [`BrowserSyncCommandSet`](#browsersynccommandset)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class BrowserSyncCommandSet
    BrowserSyncCommandSet : phase
    BrowserSyncCommandSet : category
    BrowserSyncCommandSet : do_browsersync()
    class LazyOwnCommandSet
    LazyOwnCommandSet <|-- BrowserSyncCommandSet
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync(["BrowserSyncCommandSet.do_browsersync"])
    n_cli_commands__base_py__extract_flag["_base.extract_flag"]
    n_core_console_py__print_error["console.print_error"]
    n_core_console_py__print_msg["console.print_msg"]
    n_core_console_py__print_succ["console.print_succ"]
    n_core_console_py__print_warn["console.print_warn"]
    n_modules_browser_sync_py__apply_identity_headers["browser_sync.apply_identity_headers"]
    n_modules_browser_sync_py__clear_profile["browser_sync.clear_profile"]
    n_modules_browser_sync_py__get_receiver["browser_sync.get_receiver"]
    n_modules_browser_sync_py__jar_path["browser_sync.jar_path"]
    n_modules_browser_sync_py__masked_rows["browser_sync.masked_rows"]
    n_modules_browser_sync_py__reset_token["browser_sync.reset_token"]
    n_modules_browser_sync_py__start_receiver["browser_sync.start_receiver"]
    n_modules_browser_sync_py__stop_receiver["browser_sync.stop_receiver"]
    n_modules_browser_sync_py__token["browser_sync.token"]
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_cli_commands__base_py__extract_flag
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_core_console_py__print_error
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_core_console_py__print_msg
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_core_console_py__print_succ
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_core_console_py__print_warn
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__apply_identity_headers
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__clear_profile
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__get_receiver
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__jar_path
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__masked_rows
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__reset_token
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__start_receiver
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__stop_receiver
    n_cli_commands_browser_sync_py__BrowserSyncCommandSet_do_browsersync -.-> n_modules_browser_sync_py__token
```

## Classes

<a id="browsersynccommandset"></a>

### `BrowserSyncCommandSet`

`class` | [cli/commands/browser_sync.py:13](../../cli/commands/browser_sync.py#L13)

```python
class BrowserSyncCommandSet(LazyOwnCommandSet)
```

Bases: [`LazyOwnCommandSet`](cli.commands._base.py.md#lazyowncommandset)

Expose the browser identity sync receiver to the operator.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`phase`](#browsersynccommandset-phase) |  | `'credential_access'` |  |
| [`category`](#browsersynccommandset-category) |  | `miscellaneous_category` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`do_browsersync`](#browsersynccommandset-do_browsersync) | method | Sync the real browser session into the recorder proxy. |

<a id="browsersynccommandset-do_browsersync"></a>

#### `BrowserSyncCommandSet.do_browsersync`

`method` | [cli/commands/browser_sync.py:20](../../cli/commands/browser_sync.py#L20)

Decorators: `@cmd2.with_category(miscellaneous_category)`

```python
def do_browsersync(self, line)
```

Sync the real browser session into the recorder proxy.

Usage:
    browsersync start [port]    start the loopback receiver
    browsersync stop            stop the receiver
    browsersync status          running state, profile stats, token
    browsersync token           print the receiver token
    browsersync reset-token     regenerate the receiver token
    browsersync show [domain] [--full]   list synced cookies (masked by default)
    browsersync jar             print the Netscape jar path and curl usage
    browsersync rules           show the Burp-style Match and Replace rules file
    browsersync test [path] [--http]   preview injected headers for the payload rhost
    browsersync clear           delete the synced profile and cookie jar

Load browser_sync_extension/ in Chrome or Brave, paste the token in
the popup and every auto_loop / apt_chain / auto_pwn request that
goes through the recorder proxy carries your real cookies.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `line` |  |  |  |

*Calls:* [`extract_flag`](cli.commands._base.py.md#extract_flag), [`print_error`](core.console.py.md#print_error), [`print_msg`](core.console.py.md#print_msg), [`print_succ`](core.console.py.md#print_succ), [`print_warn`](core.console.py.md#print_warn), [`apply_identity_headers`](modules.browser_sync.py.md#apply_identity_headers), [`clear_profile`](modules.browser_sync.py.md#clear_profile), [`get_receiver`](modules.browser_sync.py.md#get_receiver), [`jar_path`](modules.browser_sync.py.md#jar_path), [`masked_rows`](modules.browser_sync.py.md#masked_rows), [`reset_token`](modules.browser_sync.py.md#reset_token), [`start_receiver`](modules.browser_sync.py.md#start_receiver) and 2 more

---
