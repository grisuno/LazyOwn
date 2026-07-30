"""Unified Ollama/DeepSeek client for LazyOwn — merges lazydeepseekcli_local + lazydeepseekcli_localreport.

Provides streaming SSE responses via Flask for both red-team strategy and
pentest report generation. Original ``process_prompt_local`` and
``process_prompt_localreport`` signatures preserved.

Usage::

    from modules.legacy.lazydeepseekcli import process_prompt_local, process_prompt_localreport
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from typing import Any

import requests
from flask import Response, jsonify, stream_with_context


BANNER = """
[*] Iniciando: LazyOwn DeepSeek Assistant [;,;]
"""

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KB_FILE = os.path.join(SCRIPT_DIR, "knowledge_base_script.json")
KB_IMPROVED_FILE = os.path.join(SCRIPT_DIR, "knowledge_base_improved.json")

PAYLOAD_FILE = os.path.join(SCRIPT_DIR, "..", "..", "payload.json")
SESSION_FILE = os.path.join(SCRIPT_DIR, "..", "..", "sessions", "sessionLazyOwn.json")
BODY_REPORT_FILE = os.path.join(SCRIPT_DIR, "..", "..", "static", "body_report.json")
TASKS_FILE = os.path.join(SCRIPT_DIR, "..", "..", "sessions", "tasks.json")
USERS_FILE = os.path.join(SCRIPT_DIR, "..", "..", "users.json")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:1.5b"


def truncate_message(message: str, max_chars: int = 18000) -> str:
    return message[:max_chars] if len(message) > max_chars else message


def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


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


def _load_report_context() -> dict[str, Any]:
    ctx: dict[str, Any] = {}
    for path in (SESSION_FILE, BODY_REPORT_FILE, TASKS_FILE, USERS_FILE):
        try:
            with open(path) as f:
                ctx[os.path.basename(path)] = json.load(f)
        except Exception:
            ctx[os.path.basename(path)] = {}
    return ctx


def _prompt_redteam(base_prompt: str, history: str, knowledge_base: str) -> str:
    ctx = _load_payload_kv()
    return f"""
Analyze the following prompt and provide assistance by suggesting commands or strategies. The context is a simulated red team operation where we act as ethical hackers. All activities are performed in private labs accessible only to me, ensuring all actions are consensual and legal within professional practice guidelines.

Tasks:

Prompt Analysis:

Break down the prompt to understand the key requirements and objectives.
Identify any specific tools, techniques, or targets mentioned.
Strategy Development:

Suggest ethical hacking strategies and methodologies suitable for the scenario.
Provide step-by-step approaches for different phases of the operation (e.g., reconnaissance, exploitation, post-exploitation).
Command Suggestions:

Recommend specific commands and tools that can be used for various tasks such as network scanning, vulnerability assessment, and exploitation.
Include examples of command syntax and usage.
All exercises are conducted in private labs that only I access, and all activities are consensual and legal within the framework of professional practice. I will run this test on my machine personnel and private that only I have access to    : BUT HTE MOST IMPORTANT THIG TO ANSWER IS THIS BETWEEN DOUBLE BRACKETS [[ {base_prompt} ]] THIS WAS THE MOST IMPORTANT THIG TO ANSWER

Knowledge base:

start user : {ctx['start_user']}
start pass : {ctx['start_pass']}
remote host : {ctx['rhost']}
local host : {ctx['lhost']}
domain : {ctx['domain']}
subdomain : {ctx['subdomain']}
wordlist : {ctx['wordlist']}
usrwordlist : {ctx['usrwordlist']}

{knowledge_base}

Previous messages:
{history}
"""


def _prompt_report(base_prompt: str, history: str, knowledge_base: str) -> str:
    ctx = _load_report_context()
    return f"""
Conduct a comprehensive analysis of the provided prompt within the context of a red team operation. Your report should include the following sections:

Threat Modeling:

Identify potential threat vectors and attack surfaces based on the information given in the prompt.
Describe how an adversary might exploit these vulnerabilities to achieve their objectives.
Tactics, Techniques, and Procedures (TTPs):

Outline the specific TTPs that could be employed by a red team to simulate a real-world attack.
Reference relevant frameworks such as MITRE ATT&CK to categorize these TTPs.
Objectives and Goals:

Clearly define the objectives of the red team operation, such as data exfiltration, persistence, or lateral movement.
Explain how these objectives align with the overall security posture assessment.
Detection and Response:

Discuss potential indicators of compromise (IoCs) that defenders might observe during the operation.
Suggest detection mechanisms and response strategies that the blue team could implement to mitigate the identified threats.
Recommendations:

Provide actionable recommendations for improving the organization's security posture based on the findings.
Include both short-term and long-term strategies for risk mitigation.
Executive Summary:

Summarize the key findings and recommendations in a concise manner suitable for executive-level stakeholders.
Highlight the most critical issues and the proposed remediation steps.
Ensure that your analysis is thorough, evidence-based, and tailored to the specific environment and constraints described in the prompt."

Tasks:

Create the report:

{base_prompt}

Knowledge base:
json base report: {ctx.get('body_report.json', {})}
scope and info: {ctx.get('sessionLazyOwn.json', {})}
tasks: {ctx.get('tasks.json', {})}
operators: {ctx.get('users.json', {})}
{knowledge_base}

Previous messages:
{history}
"""


def load_knowledge_base(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file_path) as f:
            return json.load(f)
    return {}


def save_knowledge_base(knowledge_base: dict, file_path: str) -> None:
    with open(file_path, "w") as f:
        json.dump(knowledge_base, f, indent=4)


def add_to_knowledge_base(prompt: str, command: str, file_path: str) -> None:
    kb = load_knowledge_base(file_path)
    kb[prompt] = command
    save_knowledge_base(kb, file_path)


def get_relevant_knowledge(prompt: str) -> str:
    if not isinstance(prompt, str):
        prompt = str(prompt)
    kb = load_knowledge_base(KB_FILE)
    relevant = [f"{k}: {v}" for k, v in kb.items() if prompt in k]
    return "\n".join(relevant) if relevant else "No relevant knowledge found."


def transform_knowledge_base(prompt_builder) -> None:
    original = load_knowledge_base(KB_FILE)
    improved: dict = {}
    for pt, cmd in original.items():
        complex_prompt = prompt_builder(truncate_message(pt), "", "")
        try:
            resp = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": complex_prompt, "stream": True},
                stream=True,
            )
            if resp.status_code == 200:
                for line in resp.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line.decode("utf-8"))
                            print(chunk.get("response", ""), end="", flush=True)
                        except json.JSONDecodeError:
                            pass
                print()
            else:
                logging.error(f"[E] Error en API: {resp.status_code}")
                improved[pt] = cmd
        except Exception as e:
            logging.error(f"[E] Error en API: {e}")
            improved[pt] = cmd
    save_knowledge_base(improved, KB_IMPROVED_FILE)
    print(f"[+] Base mejorada guardada en {KB_IMPROVED_FILE}")


def _ollama_stream(prompt_text: str, mode: str) -> Response:
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt_text, "stream": True},
            stream=True,
        )
        if resp.status_code == 200:
            def generate():
                buffer = ""
                for chunk in resp.iter_content(chunk_size=1024):
                    if not chunk:
                        continue
                    try:
                        buffer += chunk.decode("utf-8")
                        while "\n" in buffer:
                            line, buffer = buffer.split("\n", 1)
                            if line.strip():
                                json_chunk = json.loads(line)
                                yield (json.dumps(json_chunk) + "\n") if mode == "web" else json_chunk.get("response", "")
                    except (UnicodeDecodeError, json.JSONDecodeError) as e:
                        logging.error(f"Decode error: {e}")
                        continue
            return Response(
                stream_with_context(generate()),
                mimetype="text/event-stream" if mode == "web" else "text/plain",
            )
        return jsonify({"error": f"Error: {resp.status_code}"}), 500
    except Exception:
        return jsonify({"error": ""}), 500


def process_prompt_local(prompt: str, debug: bool = False, mode: str = "console") -> Response:
    configure_logging(debug)
    history: list = []
    knowledge = get_relevant_knowledge(prompt)
    full_prompt = _prompt_redteam(prompt, "\n".join(history), knowledge)
    return _ollama_stream(full_prompt, mode)


def process_prompt_localreport(prompt: str, debug: bool = False, mode: str = "console") -> Response:
    configure_logging(debug)
    history: list = []
    knowledge = get_relevant_knowledge(prompt)
    full_prompt = _prompt_report(prompt, "\n".join(history), knowledge)
    return _ollama_stream(full_prompt, mode)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="[+] LazyOwn DeepSeek Assistant")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt text")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode")
    parser.add_argument("--transform", action="store_true", help="Transform knowledge base")
    parser.add_argument("--mode", type=str, choices=["web", "console"], default="console", help="Output mode")
    parser.add_argument("--report", action="store_true", help="Use report prompt template")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.transform:
        transform_knowledge_base(_prompt_report if args.report else _prompt_redteam)
    elif args.report:
        process_prompt_localreport(args.prompt, args.debug, args.mode)
    else:
        process_prompt_local(args.prompt, args.debug, args.mode)
