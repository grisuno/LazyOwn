# plugins

Lua plugin layer for LazyOwn. Each `.lua` file registers one or more commands
with the framework via `register_command`. The Lua runtime is provided by
`lupa` (Python binding to LuaJIT). Plugins are auto-discovered at startup
alongside `lazyaddons/`.

## When to write a plugin vs an addon

Write a Lua plugin when the logic is a few lines of shell glue or string
manipulation with no external dependencies, no Git clone, and no build step.

Write a YAML addon (`lazyaddons/`) when the tool needs to be cloned from
GitHub, compiled, or has non-trivial install steps.

## Structure of a plugin file

### Lua code (`plugins/<name>.lua`)

```lua
function my_command()
    local target = app.params["rhost"]
    if not target then
        return "Error: rhost is not set."
    end
    local result = io.popen("ping -c 1 " .. target):read("*a")
    return result
end

register_command("my_command", my_command)
```

Rules:
- Validate all parameters before use. Return an error string for missing params.
- Never crash the framework. Wrap risky calls in `pcall`.
- Always return a string. The CLI prints the return value directly.
- Use `app.params["key"]` to read `payload.json` values.

### YAML metadata (`plugins/<name>.yaml`)

Every plugin needs a YAML file for auto-discovery, help text, and completion:

```yaml
name: my_command
description: One-line description shown by help.
author: Your Name
version: "1.0"
enabled: true
tags:
  - recon
  - network
params:
  - name: rhost
    description: Target IP address
    required: true
permissions:
  - needs_network
requires_root: false
dependencies: []
outputs:
  - console_output
notes: Optional additional usage notes.
```

## Available plugins

| Plugin | Description |
|--------|-------------|
| `generate_c_reverse_shell` | Generates a C source reverse shell patched with `lhost` and `lport`. |
| `generate_cleanup_commands` | Produces cleanup commands to remove engagement artefacts from a Linux target. |
| `generate_html_payload` | Generates an HTML file with an embedded payload for phishing scenarios. |
| `generate_lateral_command` | Suggests lateral movement commands based on discovered credentials and OS. |
| `generate_linux_asm_reverse_shell` | Generates an x86-64 Linux assembly reverse shell stub. |

## Running a plugin

```
(LazyOwn) > my_command
(LazyOwn) > generate_c_reverse_shell
```

List all plugins:

```
(LazyOwn) > list_plugins
```

## YAML permissions reference

| Permission | Meaning |
|------------|---------|
| `needs_file_read` | Plugin reads files from the filesystem |
| `needs_file_write` | Plugin writes files to the filesystem |
| `needs_network` | Plugin makes network connections |
| `needs_exec` | Plugin spawns subprocesses |

## Troubleshooting

**Plugin not found** — verify `register_command("name", fn)` is called at the
bottom of the Lua file and that the YAML `enabled` field is `true`.

**Lua syntax error** — run `lua plugins/name.lua` to check syntax before
loading. The lupa runtime logs load-time errors to `sessions/access.log`.

**Parameter missing** — use `assign <key> <value>` from the CLI to set the
required `payload.json` key.
