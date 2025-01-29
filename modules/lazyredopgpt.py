#!/usr/bin/env python3
#* coding: utf8 *
"""
main.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Asistente de consola

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""

import os
import sys
import json
import logging
import argparse
from groq import Groq
from modules.colors import retModel

BANNER = """
[*] Iniciando: LazyOwn GPT One Liner Cli Assistant [;,;]
"""

script_dir = os.getcwd()
KNOWLEDGE_BASE_FILE = f"{script_dir}/knowledge_base_redop.json"

def truncate_message(message, max_chars=18000):
    if len(message) > max_chars:
        return message[:max_chars]
    return message

def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def create_complex_prompt(base_prompt: str, history: str, knowledge_base: str) -> str:
    return f"""
    Objective: Evaluate the status of any Red Team operation using provided JSON database parameters and compare it with real-world operations.

Instructions:

Review JSON Database: Examine parameters, credentials, hashes, timestamps, notes, plan, and implants.
Assess Operation Status:
Credential Harvesting: Evaluate the number and quality of obtained credentials. High-value credentials, such as administrator accounts, are critical for the operation's success.
Vulnerability Identification: Assess identified vulnerabilities and their potential impact. Focus on critical vulnerabilities like those in Microsoft SQL Server, which are key targets for exploitation.
Implant Deployment: Analyze the success and effectiveness of implant deployments. Persistent access through implants is crucial for maintaining control over the target environment.
Reconnaissance: Review the thoroughness of the reconnaissance phase. Comprehensive reconnaissance is essential for identifying potential vulnerabilities and gathering intelligence.
Post-Exploitation Activities: Assess the effectiveness of post-exploitation activities. Key objectives include privilege escalation, sensitive information gathering, and pivoting to other hosts.
Documentation and Remediation: Evaluate the documentation and remediation efforts. Providing actionable recommendations for remediation is crucial for real-world operations.
Compare with Real-World Operations:
Effectiveness: Compare the operation's effectiveness with real-world examples.
Stealth: Assess how well the operation maintained stealth and avoided detection.
Impact: Evaluate the potential impact compared to real-world breaches.
Remediation: Compare remediation efforts with industry standards.
Provide Recommendations: Offer recommendations for improving the operation and enhancing security measures. on my machine personnel and private that only I have access to. You can provide me with commands to do {base_prompt}
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
    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_FILE)
    relevant_knowledge = []
    for key, value in knowledge_base.items():
        if prompt in key:
            relevant_knowledge.append(f"{key}: {value}")
            return "\n".join(relevant_knowledge) if relevant_knowledge else "No relevant knowledge found."

def process_prompt_redop(client, prompt: str, debug: bool) -> str:
    configure_logging(debug)


    with open(prompt, "r") as f:
        content = f.read()
    prompt = content
    if content == "":
        print(f"[E] Error: Empty vuln file: {content}")
        sys.exit(1)


    history = []
    relevant_knowledge = get_relevant_knowledge(prompt)
    complex_prompt = create_complex_prompt(truncate_message(prompt), '\n'.join(history), relevant_knowledge)

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": complex_prompt}],
            #model="llama-3.3-70b-versatile",
            model=retModel(),
        )
        if debug:
            logging.debug(f"[DEBUG] : {complex_prompt}")
        message = chat_completion.choices[0].message.content.strip()

        if not message:
            logging.error("[!] No se recibió un comando válido del modelo.")
            return "No se recibió un comando válido del modelo."

        add_to_knowledge_base(prompt, message, KNOWLEDGE_BASE_FILE)
        return message

    except Exception as e:
        logging.error(f"[E] Error al comunicarse con la API: {e}")
    return str(e)

if __name__ == "__main__":


    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='[+] LazyGPT Asistente de Tareas de Programación.')
        parser.add_argument('--file', type=str, required=True, help='El path file para analizar')
        parser.add_argument('--debug', '-d', action='store_true', help='Habilita el modo debug para mostrar mensajes de depuración')
        
        return parser.parse_args()

    args = parse_args()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("[E] Error: La API key no está configurada. Ejemplo: sh export GROQ_API_KEY=\"tu_valor_de_api_key\"")
        sys.exit(1)

    client = Groq(api_key=api_key)

    response = process_prompt_redop(client, args.file, args.debug)
    print(f"[R] Respuesta: {response}")