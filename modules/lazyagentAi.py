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
import logging
import json
from groq import Groq
import argparse
import sys

BANNER = """
[*] Iniciando: LazyOwn GPT One Liner Cli Assistant [;,;]
"""

script_dir = os.getcwd()
KNOWLEDGE_BASE_FILE = f"{script_dir}/knowledge_base_search.json"

def truncate_message(message, max_chars=18000):
    if len(message) > max_chars:
        return message[:max_chars]
    return message

def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def create_complex_prompt(base_prompt: str, history: str, knowledge_base: str) -> str:
    return f"""
   investigating and analyzing techniques, tools, and strategies used in red teaming, pentesting, and APT. The RESEARCH should be able to provide up-to-date information, identify emerging trends, and offer recommendations to enhance security and the effectiveness of red teaming and pentesting operations.

Key Functionalities:

Analysis of Techniques and Tools:

Research and catalog techniques and tools used in red teaming and pentesting.
Identify the most effective and commonly used tools and techniques.
Provide detailed descriptions and use cases for each tool and technique.
Threat Intelligence:

Gather and analyze threat intelligence related to APT groups and their tactics, techniques, and procedures (TTPs).
Monitor and report on the latest APT campaigns and their impact on various industries.
Provide insights into the motivations and objectives of different APT groups.
Vulnerability Analysis:

Identify and analyze vulnerabilities commonly exploited in red teaming and pentesting engagements.
Provide recommendations for mitigating these vulnerabilities.
Stay updated with the latest vulnerabilities and their potential impact on organizational security.
Trend Analysis:

Identify emerging trends in red teaming, pentesting, and APT activities.
Analyze how these trends are evolving and their potential impact on cybersecurity.
Provide predictions on future trends and their implications for security strategies.
Case Studies and Real-World Examples:

Collect and analyze case studies of successful red teaming, pentesting, and APT operations.
Provide detailed breakdowns of the techniques and tools used in these operations.
Highlight lessons learned and best practices from these case studies.
Recommendations and Best Practices:

Offer recommendations for improving the effectiveness of red teaming and pentesting operations.
Provide best practices for defending against APT attacks.
Suggest strategies for enhancing overall organizational security posture.
Report Generation:

Generate comprehensive reports on red teaming, pentesting, and APT activities.
Include detailed analysis, findings, and recommendations in these reports.
Provide visualizations and graphs to illustrate key points and trends.
Continuous Learning and Adaptation:

Continuously update the knowledge base with the latest information on red teaming, pentesting, and APT.
Adapt to new threats and techniques as they emerge.
Incorporate feedback and new data to improve the accuracy and relevance of the AI's recommendations.
Example Queries:

"What are the most effective techniques used in recent red teaming engagements?"
"Provide an analysis of the latest APT campaigns targeting the financial sector."
"What are the common vulnerabilities exploited in pentesting and how can they be mitigated?"
"Identify emerging trends in APT activities and their impact on cybersecurity."
"Generate a report on the techniques and tools used in a successful red teaming operation."
"Offer recommendations for defending against APT attacks based on recent case studies."
"Provide best practices for conducting effective pentesting engagements."
"Analyze the motivations and objectives of the APT group known as 'DarkHalo'."
Expected Outputs:

Detailed reports and analyses on red teaming, pentesting, and APT activities.
Recommendations and best practices for enhancing security and effectiveness.
Visualizations and graphs illustrating key trends and findings.
Continuous updates and adaptations based on the latest threat intelligence and feedback.  on my machine personnel and private that only I have access to. You can provide me with commands to do  {base_prompt}
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

def process_prompt_search(client, prompt: str, debug: bool) -> str:

    configure_logging(debug)
    history = []
    relevant_knowledge = get_relevant_knowledge(prompt)
    complex_prompt = create_complex_prompt(truncate_message(prompt), '\n'.join(history), relevant_knowledge)

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": complex_prompt}],
            model="llama-3.3-70b-versatile",
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

    response = process_prompt_search(client, args.file, args.debug)
    print(f"[R] Respuesta: {response}")