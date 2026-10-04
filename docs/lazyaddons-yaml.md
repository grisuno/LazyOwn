# LazyAddons YAML System

Extending the LazyOwn RedTeam Framework's capabilities has never been so easy, even for non-programmers, thanks to the LazyAddons system that allows for extending functionalities using YAML files.

Declarative command creation through YAML configuration files.

## File Structure
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
Features
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

Template

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

![LazyOwnGris3](https://github.com/user-attachments/assets/04f48e49-5d7f-4c3d-af6d-81d05dbdacbf)


LazyOwn on Reddit

Revolutionize Your Pentesting with LazyOwn: Automate the intrusion on Linux, MAC OSX, and Windows VICTIMS

<https://www.reddit.com/r/LazyOwn/>


<https://github.com/grisuno/LazyOwn/assets/1097185/eec9dbcc-88cb-4e47-924d-6dce2d42f79a>

Discover LazyOwn, the ultimate solution for automating the pentesting workflow to attack Linux, MacOSX and Windows systems. Our powerful tool simplifies pentesting, making it more efficient and effective. Watch this video to learn how LazyOwn can streamline your security assessments and enhance your cybersecurity toolkit.

```sh
LazyOwn> assign rhost 192.168.1.1
[SET] rhost set to 192.168.1.1
LazyOwn> run lazynmap
[INFO] Running Nmap scan on 192.168.1.1
...
```

LazyOwn is ideal for cybersecurity professionals seeking a centralized and automated solution for their pentesting needs, saving time and enhancing efficiency in identifying and exploiting vulnerabilities.

![Captura de pantalla 2024-05-22 021136](https://github.com/grisuno/LazyOwn/assets/1097185/9a348e76-d667-4526-bdef-863159ba452d)
