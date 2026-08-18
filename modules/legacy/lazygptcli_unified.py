"""Unified Groq LLM client for LazyOwn — merges lazygptcli2/3/4/5 + lazyagentAi + lazygpttask + lazygptvulns + lazyredopgpt.

All original ``process_prompt_*`` function signatures are preserved for
backward compatibility (used by ``llm_adapter.py`` and the C2 dashboard).

Shared utility functions (knowledge-base CRUD, truncation, logging)
are defined once and reused across all task variants.

Usage::

    from modules.legacy.lazygptcli import (
        Groq, process_prompt, process_prompt_script, process_prompt_adversary,
        process_prompt_general, process_prompt_search, process_prompt_task,
        process_prompt_vuln, process_prompt_redop,
    )
"""

from __future__ import annotations

import json
import logging
import os

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False
    Groq = None

from typing import Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

KB_FILE_ONELINER = os.path.join(SCRIPT_DIR, "..", "knowledge_base.json")
KB_FILE_SCRIPT = os.path.join(SCRIPT_DIR, "..", "knowledge_base_script.json")
KB_FILE_SEARCH = os.path.join(SCRIPT_DIR, "..", "knowledge_base_search.json")
KB_FILE_VULN = os.path.join(SCRIPT_DIR, "..", "knowledge_base_vuln.json")
KB_FILE_REDOP = os.path.join(SCRIPT_DIR, "..", "knowledge_base_redop.json")

PAYLOAD_FILE = os.path.join(SCRIPT_DIR, "..", "..", "payload.json")
EVENT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "..", "..", "event_config.json")


def _ret_model():
    try:
        from modules.colors import retModel
        return retModel()
    except Exception:
        return "llama3-70b-8192"


def truncate_message(message: str, max_chars: int = 18000) -> str:
    return message[:max_chars] + "..." if len(message) > max_chars else message


def _configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level)


def _load_knowledge_base(file_path: str) -> list[dict]:
    try:
        with open(file_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_knowledge_base(knowledge_base: list[dict], file_path: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(knowledge_base, f, indent=2)


def _add_to_knowledge_base(prompt: str, response: str, file_path: str) -> None:
    kb = _load_knowledge_base(file_path)
    kb.append({"prompt": prompt, "response": response})
    _save_knowledge_base(kb, file_path)


def _get_relevant_knowledge(prompt: str, file_path: str | None = None) -> list[str]:
    if file_path is None:
        file_path = KB_FILE_ONELINER
    kb = _load_knowledge_base(file_path)
    keywords = prompt.lower().split()
    relevant = []
    for entry in kb:
        entry_text = entry.get("prompt", "") + " " + entry.get("response", "")
        if any(kw in entry_text.lower() for kw in keywords):
            relevant.append(entry.get("response", ""))
    return relevant


def _transform_knowledge_base(client, kb_file: str, improved_file: str) -> None:
    kb = _load_knowledge_base(kb_file)
    if not kb or client is None:
        return
    improved = []
    model = _ret_model()
    for entry in kb:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"Improve: {entry.get('response', '')}"}],
                max_tokens=512,
            )
            improved_text = response.choices[0].message.content.strip()
        except Exception:
            improved_text = entry.get("response", "")
        improved.append({"prompt": entry.get("prompt", ""), "response": improved_text})
    _save_knowledge_base(improved, improved_file)


def _groq_chat(client, messages: list[dict], model: str | None = None, max_tokens: int = 4096) -> str:
    if client is None:
        return "Error: Groq client not initialized"
    try:
        response = client.chat.completions.create(
            model=model or _ret_model(),
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)


def _load_payload_kv() -> dict[str, str]:
    try:
        with open(PAYLOAD_FILE) as f:
            config = json.load(f)
    except Exception:
        config = {}
    return {
        "start_user": config.get("start_user", ""),
        "start_pass": config.get("start_pass", ""),
        "rhost": config.get("rhost", ""),
        "lhost": config.get("lhost", ""),
        "domain": config.get("domain", ""),
        "subdomain": config.get("subdomain", ""),
        "wordlist": config.get("wordlist", ""),
        "usrwordlist": config.get("usrwordlist", ""),
    }


def _load_event_config() -> dict[str, Any]:
    try:
        with open(EVENT_CONFIG_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

def _prompt_oneliner(base_prompt: str, history: list, knowledge_base: list[str]) -> str:
    kb_text = "\n".join(knowledge_base[-5:]) if knowledge_base else ""
    return (
        "Create a coherent command or script in a single line to achieve the goal "
        "specified by the user. Use tools like nmap, curl, wget, python, perl, ruby, "
        "powershell, bash, netcat, sqlmap, hydra, john, metasploit, msfvenom, "
        "crackmapexec, impacket, evil-winrm, chisel, socat, etc.\n"
        "The command must be executable in a terminal (Linux or Windows).\n"
        "Return the exact command in a single line. Do not wrap in markdown code fences.\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Respond only with the requested command and nothing else. "
        "Do not provide explanations, just the exact command to copy and paste."
    )


def _prompt_script(base_prompt: str, history: list, knowledge_base: list[str]) -> str:
    kb_text = "\n".join(knowledge_base[-5:]) if knowledge_base else ""
    return (
        "Create a script that meets the following requirements:\n"
        "- Functionality\n- Language\n- Architecture\n- Refactoring\n\n"
        "Context for red team and pentesting:\n"
        "- Ethical: Must only be used with proper authorization\n"
        "- Legal: Compliance with local laws is mandatory\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Respond only with the requested script and nothing else. "
        "Do not provide explanations, just the exact script to copy and paste."
    )


def _prompt_adversary(base_prompt: str, history: list, knowledge_base: list[str]) -> str:
    kb_text = "\n".join(knowledge_base[-5:]) if knowledge_base else ""
    return (
        "Chatbot Prompt for Adversary Emulation using Atomic Red Team Framework\n\n"
        "Objective: To provide detailed information about a specific adversary technique "
        "defined by the Atomic Red Team framework.\n\n"
        "Technique Name\nMITRE Technique ID\nDescription\nSupported Platforms\n"
        "Execution Commands\nDetection Methods\n"
        "All testing must be conducted in authorized environments. "
        "The purpose is for ethical security research.\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Respond only with the requested technical details and commands."
    )


def _prompt_general(base_prompt: str, history: list, knowledge_base: list[str]) -> str:
    kb_text = "\n".join(knowledge_base[-5:]) if knowledge_base else ""
    ctx = _load_payload_kv()
    return (
        "Analyze the following prompt and provide assistance by suggesting commands "
        "or strategies. The context is a simulated red team operation where we act as "
        "ethical hackers performing authorized penetration testing.\n\n"
        f"Knowledge base:\n"
        f"start_user: {ctx['start_user']}\nstart_pass: {ctx['start_pass']}\n"
        f"rhost: {ctx['rhost']}\nlhost: {ctx['lhost']}\n"
        f"domain: {ctx['domain']}\nsubdomain: {ctx['subdomain']}\n"
        f"wordlist: {ctx['wordlist']}\nusrwordlist: {ctx['usrwordlist']}\n"
        f"{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "All exercises are conducted in private labs with explicit authorization. "
        "Provide clear, actionable commands and strategies."
    )


def _prompt_search(base_prompt: str, history: list, knowledge_base: list[str]) -> str:
    kb_text = "\n".join(knowledge_base[-5:]) if knowledge_base else ""
    return (
        "investigating and analyzing techniques, tools, and strategies used in red teaming, "
        "pentesting, and APT. The RESEARCH should be able to provide up-to-date information, "
        "identify emerging trends, and offer practical recommendations.\n\n"
        "Analysis of Techniques and Tools\nThreat Intelligence\nVulnerability Analysis\n"
        "Trend Analysis\nCase Studies\nRecommendations\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Provide comprehensive analysis and actionable recommendations."
    )


def _prompt_vuln(base_prompt: str, history: list, knowledge_base: list[str]) -> str:
    kb_text = "\n".join(knowledge_base[-5:]) if knowledge_base else ""
    ctx = _load_payload_kv()
    return (
        "Analyze the following NMAP output generated by Nmap and use a vulnerability "
        "assessment template to identify vulnerabilities. Based on your analysis, "
        "generate a detailed action plan for penetration testing.\n\n"
        f"rhost: {ctx['rhost']}\n"
        "If EXIST VALID USERS of KERBRUTE show me in your RESPONSE.\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Provide a detailed vulnerability assessment and penetration testing action plan."
    )


def _prompt_task(base_prompt: str, history: list, knowledge_base: list[str]) -> str:
    kb_text = "\n".join(knowledge_base[-5:]) if knowledge_base else ""
    ctx = _load_payload_kv()
    return (
        "Analyze the following Task output json generated to task assessment template "
        "to identify What tasks do I have left to do according to the given JSON template? "
        "please give me a porcent of completitud, and You can provide me with commands "
        f"to perform this tasks {base_prompt} here the ip {ctx['rhost']} and domain: {ctx['domain']}\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        "Provide task completion percentage and suggested next commands."
    )


def _prompt_redop(base_prompt: str, history: list, knowledge_base: list[str]) -> str:
    kb_text = "\n".join(knowledge_base[-5:]) if knowledge_base else ""
    return (
        "Objective: Evaluate the status of any Red Team operation using provided JSON "
        "database parameters and compare it with real-world operations.\n\n"
        "Instructions:\n"
        "Review JSON Database: Examine parameters, credentials, hashes, timestamps, notes, plan, and implants.\n"
        "Assess Operation Status: Credential Harvesting, Vulnerability Identification, Implant Deployment, "
        "Reconnaissance, Post-Exploitation, Documentation.\n"
        "Compare with Real-World Operations: Effectiveness, Stealth, Impact, Remediation.\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Provide a thorough evaluation and recommendations."
    )


# ---------------------------------------------------------------------------
# Core Groq invocation
# ---------------------------------------------------------------------------

def _process_groq(
    client,
    prompt: str,
    debug: bool,
    prompt_template,
    kb_file: str,
    model: str | None = None,
) -> str:
    if client is None:
        return "Error: Groq API key not configured"
    if debug:
        _configure_logging(True)
    kb = _load_knowledge_base(kb_file)
    relevant = _get_relevant_knowledge(prompt, kb_file)
    full_prompt = truncate_message(
        prompt_template(prompt, [], relevant)
    )
    result = _groq_chat(
        client,
        [{"role": "user", "content": full_prompt}],
        model=model,
    )
    if not result.startswith("Error:"):
        _add_to_knowledge_base(prompt, result, kb_file)
    return result


# ---------------------------------------------------------------------------
# Public API — preserved function signatures
# ---------------------------------------------------------------------------

def process_prompt(client, prompt: str, debug: bool = False) -> str:
    """Generate a single-line shell command from a user prompt."""
    return _process_groq(client, prompt, debug, _prompt_oneliner, KB_FILE_ONELINER, "llama3-70b-8192")


def process_prompt_script(client, prompt: str, debug: bool = False) -> str:
    """Generate a full script from a user prompt."""
    return _process_groq(client, prompt, debug, _prompt_script, KB_FILE_SCRIPT)


def process_prompt_adversary(client, prompt: str, debug: bool = False) -> str:
    """Answer questions about MITRE ATT&CK techniques and Atomic Red Team."""
    return _process_groq(client, prompt, debug, _prompt_adversary, KB_FILE_SCRIPT, "llama3-70b-8192")


def process_prompt_general(client, prompt: str, debug: bool = False) -> str:
    """General red team assistant with payload.json context and DeepSeek fallback."""
    try:
        return _process_groq(client, prompt, debug, _prompt_general, KB_FILE_SCRIPT)
    except Exception:
        return _deepseek_fallback(prompt)


def process_prompt_search(client, prompt: str, debug: bool = False) -> str:
    """Research and threat intelligence analysis."""
    return _process_groq(client, prompt, debug, _prompt_search, KB_FILE_SEARCH)


def process_prompt_task(client, prompt: str, debug: bool = False) -> str:
    """Analyze task assessment JSON for completion status and next commands."""
    try:
        with open(prompt) as f:
            content = f.read()
    except (FileNotFoundError, OSError) as e:
        return f"Error reading file: {e}"
    return _process_groq(client, content, debug, _prompt_task, KB_FILE_VULN)


def process_prompt_vuln(client, prompt: str, debug: bool = False, event: str = "") -> str:
    """Analyze Nmap output for vulnerabilities and generate penetration test action plan."""
    try:
        with open(prompt) as f:
            content = f.read()
    except (FileNotFoundError, OSError) as e:
        return f"Error reading file: {e}"
    if event:
        try:
            ec = _load_event_config()
            for e in ec.get("events", []):
                if e.get("name") == event:
                    tool_output_path = e.get("tool_output", "")
                    if tool_output_path and os.path.exists(tool_output_path):
                        with open(tool_output_path) as tf:
                            content += "\n\n--- Tool Output ---\n" + tf.read()
                    break
        except Exception:
            pass
    history_path = os.path.join(SCRIPT_DIR, "..", "..", "sessions", "plan.txt")
    if os.path.exists(history_path):
        with open(history_path) as pf:
            content += "\n\n--- Plan History ---\n" + pf.read()
    return _process_groq(client, content, debug, _prompt_vuln, KB_FILE_VULN)


def process_prompt_redop(client, prompt: str, debug: bool = False) -> str:
    """Evaluate Red Team operation status from JSON database params."""
    try:
        with open(prompt) as f:
            content = f.read()
    except (FileNotFoundError, OSError) as e:
        return f"Error reading file: {e}"
    return _process_groq(client, content, debug, _prompt_redop, KB_FILE_REDOP)


def _deepseek_fallback(prompt: str) -> str:
    try:
        import requests
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:1.5b", "prompt": prompt, "stream": False},
            timeout=60,
        )
        return resp.json().get("response", "DeepSeek fallback failed")
    except Exception as e:
        return f"DeepSeek fallback error: {e}"


__all__ = [
    "Groq",
    "process_prompt",
    "process_prompt_script",
    "process_prompt_adversary",
    "process_prompt_general",
    "process_prompt_search",
    "process_prompt_task",
    "process_prompt_vuln",
    "process_prompt_redop",
]
