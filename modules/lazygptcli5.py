#!/usr/bin/env python3
#_*_ coding: utf8 _*_
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
import logging
import json
from groq import Groq
from modules.colors import retModel
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
    with open('payload.json', 'r') as file:
        config = json.load(file)
        start_user = config.get("start_user")
        start_pass = config.get("start_pass")
        rhost = config.get("rhost")
        lhost = config.get("lhost")
        domain = config.get("domain")
        subdomain = config.get("subdomain")
        wordlist = config.get("wordlist")
        usrwordlist = config.get("usrwordlist")

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
All exercises are conducted in private labs that only I access, and all activities are consensual and legal within the framework of professional practice. I will run this test on my machine personnel and private that only I have access to    : {base_prompt}

Knowledge base:

start user : {start_user}
start pass : {start_pass}
remote host : {rhost}
local host : {lhost}
domain : {domain}
subdomain : {subdomain}
wordlist : {wordlist}
usrwordlist : {usrwordlist}

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
    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_FILE)
    relevant_knowledge = []
    for key, value in knowledge_base.items():
        if prompt in key:
            relevant_knowledge.append(f"{key}: {value}")
    return "\n".join(relevant_knowledge) if relevant_knowledge else "No relevant knowledge found."

def transform_knowledge_base(client) -> None:
    original_knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_FILE)
    improved_knowledge_base = {}

    for prompt, command in original_knowledge_base.items():
        history = []
        complex_prompt = create_complex_prompt(truncate_message(prompt), '\n'.join(history), '')
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": complex_prompt}],
                model="llama3-70b-8192",
            )
            improved_command = chat_completion.choices[0].message.content.strip()
            improved_knowledge_base[prompt] = improved_command
        except Exception as e:
            logging.error(f"[E] Error al comunicarse con la API: {e}")
            improved_knowledge_base[prompt] = command

    save_knowledge_base(improved_knowledge_base, IMPROVED_KNOWLEDGE_BASE_FILE)
    print(f"[+] Nueva base de conocimientos guardada en {IMPROVED_KNOWLEDGE_BASE_FILE}")

def process_prompt_general(client, prompt: str, debug: bool) -> str:
    configure_logging(debug)
    history = []
    relevant_knowledge = get_relevant_knowledge(prompt)
    complex_prompt = create_complex_prompt(prompt, '\n'.join(history), relevant_knowledge)

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": complex_prompt}],
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

    except Exception as ex:
        e = ex 
        if e:
            return f"Error API: {e}"
        else:
            return "Unknown Error."

if __name__ == "__main__":
    import argparse
    import sys

    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='[+] LazyGPT Asistente de Tareas de Programación.')
        parser.add_argument('--prompt', type=str, required=True, help='El prompt para la tarea de programación/Tarea Cli')
        parser.add_argument('--debug', '-d', action='store_true', help='Habilita el modo debug para mostrar mensajes de depuración')
        parser.add_argument('--transform', action='store_true', help='Transforma la base de conocimientos original en una base mejorada usando Groq')
        return parser.parse_args()

    args = parse_args()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("[E] Error: La API key no está configurada. Ejemplo: sh export GROQ_API_KEY=\"tu_valor_de_api_key\"")
        sys.exit(1)

    client = Groq(api_key=api_key)

    if args.transform:
        transform_knowledge_base(client)
    else:
        response = process_prompt_general(client, args.prompt, args.debug)
        print(f"[R] Respuesta: {response}")
