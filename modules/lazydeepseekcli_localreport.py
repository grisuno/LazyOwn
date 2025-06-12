#!/usr/bin/env python3
#_*_ coding: utf8 _*_
"""
main.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Asistente de consola
"""

import os
import logging
import json
import requests
import argparse
from flask import jsonify, Response, stream_with_context

BANNER = """
[*] Iniciando: LazyOwn GPT One Liner Cli Assistant [;,;]
"""

script_dir = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_FILE = f"{script_dir}/knowledge_base_script.json"
IMPROVED_KNOWLEDGE_BASE_FILE = f"{script_dir}/knowledge_base_improved.json"

def truncate_message(message, max_chars=18000):
    if len(message) > max_chars:
        return message[:max_chars]
    return message

def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def create_complex_prompt(base_prompt: str, history: str, knowledge_base: str) -> str:
    
    with open('sessions/sessionLazyOwn.json', 'r') as file:
        config = json.load(file)

    with open('static/body_report.json', 'r') as file:
        base_report = json.load(file)    
    
    with open('sessions/tasks.json', 'r') as file:
        tasks = json.load(file)
    
    with open('users.json', 'r') as file:
        operators = json.load(file)

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
json base report: {base_report}
scope and info: {config}
tasks: {tasks}
operators: {operators}
{knowledge_base}

Previous messages:
{history}
"""

def load_knowledge_base(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_knowledge_base(knowledge_base: dict, file_path: str) -> None:
    with open(file_path, "w") as f:
        json.dump(knowledge_base, f, indent=4)

def add_to_knowledge_base(prompt: str, command: str, file_path: str) -> None:
    knowledge_base = load_knowledge_base(file_path)
    knowledge_base[prompt] = command
    save_knowledge_base(knowledge_base, file_path)

def get_relevant_knowledge(prompt: str) -> str:
    if not isinstance(prompt, str):
        prompt = str(prompt)

    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_FILE)
    relevant_knowledge = []
    for key, value in knowledge_base.items():
        if prompt in key:
            relevant_knowledge.append(f"{key}: {value}")
    return "\n".join(relevant_knowledge) if relevant_knowledge else "No relevant knowledge found."

def transform_knowledge_base() -> None:
    original_knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_FILE)
    improved_knowledge_base = {}
    for prompt, command in original_knowledge_base.items():
        history = []
        complex_prompt = create_complex_prompt(truncate_message(prompt), '\n'.join(history), '')
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "deepseek-r1:1.5b",
                    "prompt": complex_prompt,
                    "stream": True
                }, stream=True
            )
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line.decode('utf-8'))
                            print(chunk.get("response", ""), end="", flush=True)
                        except json.JSONDecodeError as e:
                            print(f"Error decodificando JSON: {e}")
                print()
            else:
                logging.error(f"[E] Error al comunicarse con la API: {response.status_code}")
                improved_knowledge_base[prompt] = command
        except Exception as e:
            logging.error(f"[E] Error al comunicarse con la API: {e}")
            improved_knowledge_base[prompt] = command

    save_knowledge_base(improved_knowledge_base, IMPROVED_KNOWLEDGE_BASE_FILE)
    print(f"[+] Nueva base de conocimientos guardada en {IMPROVED_KNOWLEDGE_BASE_FILE}")

def process_prompt_localreport(prompt: str, debug: bool, mode: str) -> Response:
    configure_logging(debug)
    history = []
    relevant_knowledge = get_relevant_knowledge(prompt)
    complex_prompt = create_complex_prompt(prompt, '\n'.join(history), relevant_knowledge)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": complex_prompt,
                "stream": True
            },
            stream=True
        )

        if response.status_code == 200:
            def generate():
                buffer = ""
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        try:
                            buffer += chunk.decode('utf-8')
                            while '\n' in buffer:
                                line, buffer = buffer.split('\n', 1)
                                if line.strip():
                                    json_chunk = json.loads(line)
                                    if mode == 'web':
                                        yield json.dumps(json_chunk) + '\n'
                                    else:
                                        yield json_chunk.get("response", "")
                        except (UnicodeDecodeError, json.JSONDecodeError) as e:
                            logging.error(f"Error decodificando chunk: {e}")
                            continue
            return Response(stream_with_context(generate()), mimetype='text/event-stream' if mode == 'web' else 'text/plain')
        else:
            return jsonify({"error": f"Error en la solicitud: {response.status_code}"}), 500

    except Exception as ex:
        return jsonify({"error": str("")}), 500


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='[+] LazyGPT Asistente de Tareas de Programación.')
    parser.add_argument('--prompt', type=str, required=True, help='El prompt para la tarea de programación/Tarea Cli')
    parser.add_argument('--debug', '-d', action='store_true', help='Habilita el modo debug para mostrar mensajes de depuración')
    parser.add_argument('--transform', action='store_true', help='Transforma la base de conocimientos original en una base mejorada usando Ollama')
    parser.add_argument('--mode', type=str, choices=['web', 'console'], default='console', help='Modo de salida: web (JSON) o console (texto plano)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.transform:
        transform_knowledge_base()
    else:
        process_prompt_localreport(args.prompt, args.debug, args.mode)