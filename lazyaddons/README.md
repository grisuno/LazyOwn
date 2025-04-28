# LazyAddons YAML System

Declarative command creation through YAML configuration files.

## 📂 File Structure
lazyaddons/
├── addon1.yaml
├── addon2.yaml
└── example.yaml


## 🛠️ Addon Definition

### Minimal Example
```yaml
name: "shortname"  # CLI command (do_shortname)
enabled: true
description: "Tool description for help system"

tool:
  name: "Full Tool Name"
  repo_url: "https://github.com/user/repo"
  install_path: "tools/toolname"
  execute_command: "python tool.py -u {url}"
```  
Advanced Configuration
```yaml
params:
  - name: "url"
    required: true
    description: "Target URL"
    default: "http://localhost"
  
  - name: "threads"
    required: false
    default: 4
```    
✨ Features
Auto-Installation
Tools clone from Git when missing:

```bash
git clone <repo_url> <install_path>
```
Parameter Substitution
Replaces {param} in commands with values from:

- Command arguments

- Default values

- self.params

- Help Integration

help <command> displays the YAML description.

🧩 Template

```yaml
name: ""
enabled: true
description: ""

tool:
  name: ""
  repo_url: ""
  install_path: ""
  install_command: ""  # Optional
  execute_command: ""

params:
  - name: ""
    required: true/false
    default: ""
    description: ""
```
▶️ Usage
Place YAML files in lazyaddons/

Start your CLI application

Execute registered commands:

```bash
(Cmd) help your_command
(Cmd) your_command -args
```
🚨 Troubleshooting
Missing parameters: Verify required fields in YAML

Install failures: Check network/git access

Command errors: Validate execute_command syntax


Key features:
- Clean GitHub-flavored markdown
- Focused only on YAML addons
- Includes ready-to-use templates
- Documents the parameter substitution system
- Provides troubleshooting tips

Would you like me to add any specific examples or usage scenarios?