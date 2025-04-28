## 📕 LazyOwn RedTeam Framework - Plugin Development Guide
Welcome to the LazyOwn RedTeam Framework!
This guide will teach you how to create your own plugins and how to document them properly using the YAML template.

# 📦 What is a Plugin?
In LazyOwn, a plugin is simply a Lua function that adds new functionality to the framework.
Plugins are registered into the command system and can be called via the LazyOwn CLI.

Each plugin usually does something specific like:

- Generating a payload

- Harvesting Kerberos tickets

- Validating shellcode

- Visualizing networks

etc.

# 🛠 How to Create a New Plugin
Follow these simple steps:

1. Write the Lua Function
Define a Lua function that implements the functionality you want.

Always follow this structure:

- Validate parameters if needed

- Handle errors gracefully

- Return a string as output (success, results, or error messages)

Example structure:

```lua

function my_plugin()
    -- Step 1: Read input parameters
    local param = app.params["rhost"]

    if not param then
        return "Error: Missing parameter 'rhost'."
    end

    -- Step 2: Main logic
    -- (your code here)

    -- Step 3: Return a clear message
    return "Plugin executed successfully with param: " .. param
end
```
2. Register the Plugin
At the end of your plugin file, register the command with LazyOwn:

```lua

register_command("my_plugin", my_plugin)
```
The first argument is the name you will use to call it inside the framework.

📄 How to Create the YAML Metadata
Every plugin needs a small YAML file to describe it.
This YAML is used by LazyOwn to automatically load, list, and document plugins.

Here is the standard template:

```yaml

name: your_plugin_name
description: >
  A short description of what your plugin does.
author: "Your Name"
version: "1.0"
enabled: true
tags:
  - category1
  - category2
params:
  - name: param1
    description: Description of the first parameter
    required: true
  - name: param2
    description: Optional second parameter
    required: false
permissions:
  - needs_file_read    # If your plugin reads files
  - needs_file_write   # If your plugin writes files
requires_root: false     # true if your plugin needs root privileges
dependencies: []
outputs:
  - file_output        # file_output, console_output, etc.
notes: >
  Any extra notes or tips for the users.
  ```
✅ Important:

If your plugin reads files, use needs_file_read under permissions.

If it writes files, add needs_file_write.

If it needs root permissions (like network sniffing), set requires_root: true.

📋 Quick Checklist Before Finalizing

- Task	Done?
- Lua function is written	✅
- register_command is called	✅
- YAML metadata file is created	✅
- Proper error handling included	✅
- Clear output messages	✅

# 🚀 Example: Creating a Simple Ping Plugin

Lua code (plugins/ping.lua)

```lua

function ping_host()
    local target = app.params["target"]
    if not target then
        return "Error: 'target' parameter missing."
    end

    local cmd = "ping -c 1 " .. target
    local result = io.popen(cmd):read("*a")
    
    return result
end

register_command("ping_host", ping_host)
```
YAML metadata (plugins/ping.yaml)

```yaml

name: ping_host
description: >
  Pings a target host and returns the response.
author: "LazyOwn RedTeam"
version: "1.0"
enabled: true
tags:
  - network
  - recon
params:
  - name: target
    description: Target IP or hostname to ping
    required: true
permissions:
  - needs_file_read
requires_root: false
dependencies: []
outputs:
  - console_output
notes: >
  Useful for quick network reachability checks.
🎯 Final Notes
Always keep your Lua code simple and modular.

```
Think RedTeam: Validate inputs, and avoid crashing the framework if something unexpected happens.

Tag your plugins well: It helps with autocompletion and search inside the framework.

Use YAML carefully: YAML parsing is strict, indentation matters!

🧠 Example Plugins in LazyOwn

Plugin	Purpose
- generate_reverse_shell	Create a Python reverse shell payload
- kerberos_harvest	Dump Kerberos SPNs and tickets
- validate_shellcode	Check shellcode for bad bytes and size
- visualize_network	Generate an interactive network graph from IPs