# Report Phase Guide

Reporting — generate Situation Reports (SITREPs), timelines and campaign documentation for stakeholders.

All commands below abstract their arguments through ``payload.json``. Set ``rhost``, ``lhost``, ``domain``, ``wordlist`` and credentials once; the framework substitutes them automatically. Never pass raw IP addresses or credentials as positional arguments.

## Commands

| Command | Description | Source |
|---------|-------------|--------|

| `do_apropos` | Search for commands matching the given parameter in the cmd interface and optionally extend the search using the system's `apropos` command. | `lazyown.py` |
| `do_banners` | Extract and display banners from XML files in the 'sessions' directory. | `lazyown.py` |
| `do_c2asm` | Display C and ASM code side by side in a curses-based interface. | `lazyown.py` |
| `do_camphish` | Executes the camphish tool for Grab cam shots from target's phone front camera or PC webcam just sending a link. | `lazyown.py` |
| `do_create_session_json` | Generates or updates a JSON file to be used as a database. | `lazyown.py` |
| `do_createjsonmachine` | Create a new JSON payload file based on the template provided in payload.json. | `lazyown.py` |
| `do_createjsonmachine_batch` | Create multiple JSON payload files based on a CSV input file from HackerOne. | `lazyown.py` |
| `do_createtargets` | Generates hosts.txt, urls.txt, domains.txt, and targets.txt from multiple JSON payload files. | `lazyown.py` |
| `do_download_malwarebazar` | Download a malware sample from MalwareBazaar using its SHA256 hash. | `lazyown.py` |
| `do_extract_ports` | Extracts open ports and IP address information from a specified file. | `lazyown.py` |
| `do_eyewitness` | Executes EyeWitness to capture screenshots from a list of URLs. | `lazyown.py` |
| `do_eyewitness_py` | Automates EyeWitness installation and execution without requiring user input. | `lazyown.py` |
| `do_get_avaible_actions` | Get list de supported acctions. | `lazyown.py` |
| `do_gowitness` | Command gowitness: Installs and runs Gowitness for screenshotting web services or network CIDR blocks. | `lazyown.py` |
| `do_gpt` | Run the internal module to create Oneliners with Groq AI located at `modules/lazygptcli.py` with the specified parameters. | `lazyown.py` |
| `do_img2vid` | Generates an MP4 video from PNG images found in the sessions/captured_images directory. | `lazyown.py` |
| `do_malwarebazar` | Fetches and displays malware information from the MalwareBazaar API based on the given tag. | `lazyown.py` |
| `do_morse` | Interactive Morse Code Converter. | `lazyown.py` |
| `do_name_the_hash` | Identify hash type using nth after retrieving it with get_hash(). | `lazyown.py` |
| `do_nmapscripthelp` | Provides help to find and display information about Nmap scripts. | `lazyown.py` |
| `do_process_scans` | Processes CSV files with scan results and vulnerability data to generate a Shodan-like JSON database. | `lazyown.py` |
| `do_pth_net` | Executes the Pass-the-Hash (PTH) Net tool to change the password of an Active Directory account. | `lazyown.py` |
| `do_pup` | Processes HTML content from a specified URL using the pup utility and a default CSS selector. | `lazyown.py` |
| `do_vulns` | Search the NVD for CVEs matching a service banner and persist findings. | `lazyown.py` |

## Next Phase

After completing the Report phase, proceed to:
**Command and Control** (`docs/c2.md`) for ongoing campaign monitoring

---
*Generated from ``cli/command_index.json``. Keep this guide in sync by running ``python3 scripts/build_command_index.py`` after adding new commands.*

