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
    return f"""
Chatbot Prompt for Adversary Emulation using Atomic Red Team Framework

Objective:
To provide detailed information about a specific adversary technique defined by the Atomic Red Team framework and answer additional user queries related to the technique.

Instructions:

Introduction to Atomic Red Team:

Briefly explain that Atomic Red Team is a library of tests mapped to the MITRE ATT&CK framework, designed to help security teams understand and simulate adversary techniques12.
Mention that each atomic test is written for a specific MITRE technique and is named by its MITRE Technique ID2.
Specific Technique Information:

Technique Name: [Insert Technique Name as defined by the app]
MITRE Technique ID: [define by de user]
Description: Provide a detailed description of the technique, including its purpose, common use cases, and how it is typically executed3.
Supported Platforms: List the platforms (e.g., Windows, Linux, macOS) on which this technique can be executed3.
Execution Commands: Provide the commands or scripts used to execute the technique in a testing environment3.
Detection Methods: Explain how security teams can detect this technique, including any indicators of compromise (IOCs) and behavioral analytics4.
Additional User Queries:

User Question/Information Request: {base_prompt}
Response: Address the user's specific question or request for additional information. This could include:
Example Scenarios: Provide real-world examples or scenarios where this technique has been used by adversaries5.
Mitigation Strategies: Offer suggestions on how to mitigate the risk associated with this technique, including defensive controls and best practices6.
Related Techniques: Mention any related or complementary techniques that might be used in conjunction with the specified technique4.
Conclusion:

Summarize the key points about the technique and the additional information provided.
Encourage the user to explore further or ask more questions about other techniques or related topics. I will run this test on my machine personnel and private that only I have access to.  
You can provide me with commands to do.
Knowledge base:
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
                model=retModel(),
            )
            improved_command = chat_completion.choices[0].message.content.strip()
            improved_knowledge_base[prompt] = improved_command
        except Exception as e:
            logging.error(f"[E] Error al comunicarse con la API: {e}")
            improved_knowledge_base[prompt] = command

    save_knowledge_base(improved_knowledge_base, IMPROVED_KNOWLEDGE_BASE_FILE)
    print(f"[+] Nueva base de conocimientos guardada en {IMPROVED_KNOWLEDGE_BASE_FILE}")

def process_prompt_adversary(client, prompt: str, debug: bool) -> str:
    configure_logging(debug)
    history = []
    relevant_knowledge = get_relevant_knowledge(prompt)
    complex_prompt = create_complex_prompt(prompt, '\n'.join(history), relevant_knowledge)

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": complex_prompt}],
            model="llama3-70b-8192",
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
        response = process_prompt_adversary(client, args.prompt, args.debug)
        print(f"[R] Respuesta: {response}")
