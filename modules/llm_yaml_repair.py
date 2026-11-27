"""LLM response to playbook pipeline.

Extracted from ``utils``: query Ollama, pre-process and repair the YAML
a model emits, fall back to manual extraction or a synthetic playbook,
and persist/reload the result. Pure pipeline — no shell state.
"""

from __future__ import annotations

import json
import os
import random
import re

import requests
import yaml

from core.console import print_error
from core.paths import sanitize_filename


def query_ollama(prompt, model="deepseek-r1:1.5b"):
    """Sends query to Ollama and returns model response."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate", json={"model": model, "prompt": prompt, "stream": False}, timeout=600
        )
        if response.status_code == 200:
            return response.json()["response"]
        print_error(f"[!] API error: {response.status_code}")
        return None
    except Exception as e:
        print_error(f"[!] Ollama error: {str(e)}")
        return None


def preprocess_llm_response(response):
    """
    Pre-process LLM response to handle common issues before YAML parsing
    """
    import re

    # Remove any markdown code block markers
    response = re.sub(r"```yaml\s*", "", response)
    response = re.sub(r"```\s*", "", response)

    # Remove any thinking or explanatory text
    if "<think>" in response:
        think_end = response.find("</think>")
        if think_end > 0:
            response = response[think_end + 8 :].strip()

    # Remove any leading text before apt_name
    apt_name_pos = response.find("apt_name:")
    if apt_name_pos > 0:
        response = response[apt_name_pos:].strip()

    # Remove any trailing text after the YAML content
    last_yaml_line = -1
    lines = response.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and ":" in stripped:
            last_yaml_line = i

    if last_yaml_line >= 0 and last_yaml_line < len(lines) - 1:
        response = "\n".join(lines[: last_yaml_line + 1])

    return response


def manual_yaml_extraction(content):
    """
    Fallback method to manually extract YAML data from malformed content
    """
    import re

    result = {}
    lines = content.split("\n")

    # Extract apt_name
    apt_name_match = re.search(r"apt_name:\s*(.+)", content)
    if apt_name_match:
        result["apt_name"] = apt_name_match.group(1).strip()

    # Extract description
    desc_match = re.search(r"description:\s*(.+)", content)
    if desc_match:
        result["description"] = desc_match.group(1).strip()

    # Extract steps - this is more complex
    steps = []
    current_step = None
    in_mitre_info = False

    for line in lines:
        stripped = line.strip()

        # Start of a new step
        if stripped.startswith("- atomic_id:") or (
            stripped == "-" and lines.index(line) < len(lines) - 1 and "atomic_id:" in lines[lines.index(line) + 1]
        ):
            if current_step:
                steps.append(current_step)
            current_step = {}
            in_mitre_info = False
            continue

        # Parse step properties
        if current_step is not None:
            # Handle mitre_info subsection
            if "mitre_info:" in stripped:
                in_mitre_info = True
                current_step["mitre_info"] = {}
                continue

            # Parse regular key-value pairs
            if ":" in stripped:
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""

                if in_mitre_info:
                    current_step["mitre_info"][key] = value
                else:
                    current_step[key] = value

    # Add the last step if exists
    if current_step:
        steps.append(current_step)

    if steps:
        result["steps"] = steps

    return result if "apt_name" in result and "steps" in result else None


def create_synthetic_yaml(nmap_services):
    """
    Create a basic synthetic YAML playbook when all else fails
    """

    # Sample MITRE techniques relevant to common services
    techniques = {
        "ssh": {"id": "T1021.004", "name": "Remote Services: SSH"},
        "http": {"id": "T1190", "name": "Exploit Public-Facing Application"},
        "ftp": {"id": "T1021.001", "name": "Remote Services: FTP"},
        "smb": {"id": "T1021.002", "name": "Remote Services: SMB"},
        "mysql": {"id": "T1190", "name": "Exploit Database Service"},
        "rdp": {"id": "T1021.001", "name": "Remote Services: RDP"},
        "dns": {"id": "T1590.002", "name": "Information Gathering: DNS"},
    }

    # Generic commands for different services
    commands = {
        "ssh": "hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://{ip} -t 4",
        "http": "nikto -host {ip}:{port}",
        "ftp": "hydra -l anonymous -p '' {ip} ftp",
        "smb": "enum4linux -a {ip}",
        "mysql": "nmap -sV --script=mysql-enum {ip} -p {port}",
        "rdp": "xfreerdp /u:administrator /p:password /v:{ip}",
        "dns": "dig axfr @{ip}",
    }

    # Create playbook structure
    playbook = {
        "apt_name": "SyntheticAttackChain",
        "description": "Automatically generated playbook based on discovered services",
        "steps": [],
    }

    # Generate steps based on discovered services
    step_id = 1
    for service_name, instances in nmap_services.items():
        service_key = service_name.lower()

        # Match service to known technique or use generic
        if service_key in techniques:
            technique = techniques[service_key]
        else:
            # Pick a random technique if service not in our mapping
            technique = random.choice(list(techniques.values()))

        # Create a command using the first instance
        if instances:
            instance = instances[0]
            ip = instance.get("ip", "target_ip")
            port = instance.get("port", "target_port")

            # Get command template or use nmap fallback
            command_template = commands.get(service_key, "nmap -sV -p {port} {ip}")
            command = command_template.format(ip=ip, port=port)

            # Create step
            step = {
                "atomic_id": f"S{step_id:03d}",
                "name": f"Attack {service_name.upper()}",
                "description": f"Attempt to exploit {service_name} service",
                "command": command,
                "service": service_name,
                "mitre_info": {"mitre_id": technique["id"], "mitre_name": technique["name"]},
            }

            playbook["steps"].append(step)
            step_id += 1

    return playbook


def parse_yaml_response(content):
    """
    Improved function to extract and parse YAML content from LLM response
    with better error handling and recovery attempts
    """

    try:
        # First, try to extract YAML between ```yaml and ``` markers
        yaml_pattern = r"```(?:yaml)?\s*([\s\S]*?)```"
        matches = re.findall(yaml_pattern, content)

        if matches:
            yaml_content = matches[0].strip()
        else:
            # If no code blocks found, try to extract the whole text as YAML
            yaml_content = content.strip()

        # Try to fix common YAML formatting issues
        yaml_content = fix_common_yaml_issues(yaml_content)

        # Attempt to parse the YAML
        return yaml.safe_load(yaml_content)
    except Exception as e:
        print_error(f"[!] YAML parse error: {str(e)}")
        print_error(f"[!] Failed content: {yaml_content[:150]}...")

        # Try one more recovery attempt with a more aggressive fix
        try:
            fixed_yaml = aggressive_yaml_fix(yaml_content)
            return yaml.safe_load(fixed_yaml)
        except Exception as e2:
            print_error(f"[!] Recovery attempt failed: {str(e2)}")
            return None


def fix_common_yaml_issues(yaml_content):
    """Fixes common YAML formatting issues"""
    import re

    # Fix 1: Fix indentation issues in lists under properties
    fixed_content = []
    current_indent = 0
    expected_indent = None

    for line in yaml_content.split("\n"):
        stripped = line.lstrip()

        # Skip empty lines
        if not stripped:
            fixed_content.append(line)
            continue

        # Calculate current line indentation
        indent = len(line) - len(stripped)

        # Fix common issue with mixed spaces and improper indentation
        if stripped.startswith("- ") and expected_indent is not None and indent != expected_indent:
            # Adjust indentation for list items
            fixed_line = " " * expected_indent + stripped
            fixed_content.append(fixed_line)
        else:
            fixed_content.append(line)

        # Set expected indentation for next items if this is a property
        if ":" in stripped and not stripped.startswith("- "):
            current_indent = indent
            expected_indent = indent + 2  # Common YAML convention for nested items

    # Fix 2: Fix invalid mapping values (the specific error you encountered)
    result = "\n".join(fixed_content)
    result = re.sub(r"(\w+):\s+(\w+):\s+", r"\1:\n  \2: ", result)

    return result


def aggressive_yaml_fix(yaml_content):
    """More aggressive YAML fixing for recovery attempts"""
    import re

    # Fix multi-line values without proper block scalar indicators
    lines = yaml_content.split("\n")
    fixed_lines = []
    in_block = False

    for line in lines:
        stripped = line.lstrip()

        # Handle mapping errors - common cause of "mapping values not allowed here"
        if re.search(r":\s+\w+:\s+", line):
            parts = re.split(r":\s+", line, maxsplit=1)
            if len(parts) > 1:
                fixed_lines.append(f"{parts[0]}:")
                fixed_lines.append(f"  {parts[1]}")
                continue

        fixed_lines.append(line)

    # Try to identify and fix specific line with error
    content = "\n".join(fixed_lines)

    # Last resort: Replace any potential inline mapping errors
    content = re.sub(r"(\w+):\s+(\w+):\s+", r"\1:\n  \2: ", content)

    return content


_PLAYBOOK_NAME_MAX_LENGTH = 128
_PLAYBOOK_COMMAND_KEYS = ("command", "cmd", "commands", "run")


def validate_playbook_shape(playbook_data) -> None:
    """Validate the minimal shape an executable playbook must have.

    An LLM can return prose wrapped as YAML or an object where a string
    belongs; executing that means feeding non-command text to the shell.
    Args:
        playbook_data: Candidate document.

    Raises:
        ValueError: When the document is not a mapping, the name exceeds
            the length cap, or an executable phase field is not a string.
    """
    import re as _re

    if not isinstance(playbook_data, dict):
        raise ValueError("playbook document must be a mapping")
    name = str(playbook_data.get("apt_name", ""))
    if len(name) > _PLAYBOOK_NAME_MAX_LENGTH:
        raise ValueError("playbook name exceeds maximum length")
    phases = playbook_data.get("phases", [])
    if not isinstance(phases, list):
        raise ValueError("playbook phases must be a list")
    for phase in phases:
        if not isinstance(phase, dict):
            raise ValueError("playbook phases must be mappings")
        for key in _PLAYBOOK_COMMAND_KEYS:
            if key in phase and not isinstance(phase[key], str):
                raise ValueError(f"playbook phase field {key!r} must be a string")
    name = str(playbook_data.get("apt_name", ""))
    if name and not _re.fullmatch(r"[A-Za-z0-9_\- .]+", name):
        raise ValueError("playbook name contains forbidden characters")


def save_playbook(playbook_data, playbook_name):
    """Guarda el playbook generado en disco (fail-closed sobre la forma).

    The name is sanitized to a single path segment (traversal attempts
    collapse into underscores) and the document must pass
    :func:`validate_playbook_shape` before it touches disk.

    Args:
        playbook_data: Candidate document from the LLM.
        playbook_name: Desired short name (without extension).

    Returns:
        The relative path of the persisted playbook.

    Raises:
        ValueError: When the document shape is not executable or the
            name is empty after sanitization.
    """
    safe_name = sanitize_filename(str(playbook_name or ""))
    if not safe_name:
        raise ValueError("playbook name is empty after sanitization")
    validate_playbook_shape(playbook_data)
    playbook_dir = "playbooks"
    os.makedirs(playbook_dir, exist_ok=True)
    playbook_path = os.path.join(playbook_dir, f"{safe_name}.yaml")

    with open(playbook_path, "w") as f:
        yaml.dump(playbook_data, f, default_flow_style=False)

    return playbook_path


def load_knowledge_base(knowledge_file="my_techniques.json"):
    """Carga la base de conocimientos personalizada."""
    if os.path.exists(knowledge_file):
        with open(knowledge_file, "r") as f:
            return json.load(f)
    return []


__all__ = [
    "query_ollama",
    "preprocess_llm_response",
    "manual_yaml_extraction",
    "create_synthetic_yaml",
    "parse_yaml_response",
    "fix_common_yaml_issues",
    "aggressive_yaml_fix",
    "save_playbook",
    "load_knowledge_base",
]
