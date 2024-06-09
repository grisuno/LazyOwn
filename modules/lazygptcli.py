"""
main.py

Autor: Gris Iscomeback 
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Assistente de consola

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import os
import argparse
import logging
import signal
import sys
import time
import subprocess
import json
from groq import Groq

BANNER = """
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
[*] Iniciando: LazyOwn GPT One Liner Cli Assistent [;,;]
"""

HELP_MESSAGE = """
{message}

[?] Uso: python lazygptcli.py --prompt "<tu prompt>" [--debug]

[?] Opciones:
  --prompt    "El prompt para la tarea de programación (requerido)."
  --debug, -d "Habilita el modo debug para mostrar mensajes de depuración."
  --transform "Transforma la base de conocimientos original en una base mejorada usando Groq."

[?] Asegúrate de configurar tu API key antes de ejecutar el script:
  export GROQ_API_KEY=<tu_api_key>
[->] visit: https://console.groq.com/docs/quickstart not sponsored link
"""

KNOWLEDGE_BASE_FILE = "knowledge_base.json"
IMPROVED_KNOWLEDGE_BASE_FILE = "knowledge_base_improved.json"

def signal_handler(sig: int, frame: any) -> None:
    print(f'\n[*] Interrupción recibida, saliendo del programa.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def show_help(message: str) -> None:
    print(HELP_MESSAGE.format(message=message))
    sys.exit(1)

def check_api_key() -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        show_help("[E] Error: La API key no está configurada.")
    return api_key

def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='[+] LazyGPT Asistente de Tareas de Programación.')
    parser.add_argument('--prompt', type=str, required=True, help='El prompt para la tarea de programación/Tarea Cli')
    parser.add_argument('--debug', '-d', action='store_true', help='Habilita el modo debug para mostrar mensajes de depuración')
    parser.add_argument('--transform', action='store_true', help='Transforma la base de conocimientos original en una base mejorada usando Groq')
    return parser.parse_args()

def create_complex_prompt(base_prompt: str, history: str, knowledge_base: str, error_message: str = None) -> str:
    error_context = f"The following error occurred during execution.: {error_message}" if error_message else "No errors detected in the last iteration."
    return f"""
Create a coherent command or script in a single line to achieve the goal specified by the user in the argument args.prompt. Use pipes (|) only for passing stdout to stdin between commands when necessary, and use logical operators (&&) to chain commands that need to be executed sequentially. Ensure the command handles directory navigation correctly and includes proper content redirection for file creation. Respond only with the requested command and nothing else. Do not provide explanations, just the exact command to copy and paste. {base_prompt}

Knowledge base:
{knowledge_base}

Previous messages:
{history}

{error_context}
"""

def execute_command(command: str) -> subprocess.CompletedProcess:
    return subprocess.run(command, shell=True, capture_output=True, text=True)

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
        error_message = None
        complex_prompt = create_complex_prompt(prompt, '\n'.join(history), '', error_message)
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": complex_prompt}],
                model="llama3-8b-8192",
            )
            improved_command = chat_completion.choices[0].message.content.strip()
            improved_knowledge_base[prompt] = improved_command
            time.sleep(2)
        except Exception as e:
            logging.error(f"[E] Error al comunicarse con la API: {e}")
            improved_knowledge_base[prompt] = command

    save_knowledge_base(improved_knowledge_base, IMPROVED_KNOWLEDGE_BASE_FILE)
    print(f"[+] Nueva base de conocimientos guardada en {IMPROVED_KNOWLEDGE_BASE_FILE}")

def main() -> None:
    print(BANNER)
    
    args = parse_args()
    configure_logging(args.debug)

    api_key = check_api_key()
    client = Groq(api_key=api_key)

    if args.transform:
        transform_knowledge_base(client)
        return

    base_prompt = args.prompt
    history = []
    error_message = None

    while True:
        relevant_knowledge = get_relevant_knowledge(base_prompt)
        complex_prompt = create_complex_prompt(base_prompt, '\n'.join(history), relevant_knowledge, error_message)
        error_message = None  # Reset the error message for the next iteration

        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": complex_prompt}],
                model="llama3-8b-8192",
            )
            if args.debug:
                logging.debug(f"[DEBUG] : {complex_prompt}")
            message = chat_completion.choices[0].message.content.strip()
            print(f"[R] Respuesta de Groq:\n{message}")

            history.append(f"User: {base_prompt}")
            history.append(f"Groq: {message}")

            if not message:
                logging.error("[!] No se recibió un comando válido del modelo.")
                base_prompt = input("[?] Por favor ingrese un nuevo prompt o información adicional: ")
                continue

        except Exception as e:
            logging.error(f"[E] Error al comunicarse con la API: {e}")
            break

        user_input = input("[?] ¿Deseas ejecutar el comando? (si/no): ").strip().lower()
        if user_input == 'si':
            print(f"[$] Ejecutando el comando: > {message}")
            result = execute_command(message)
            print(f"[C] return code: {result.returncode}")
            if result.returncode != 0:
                error_message = result.stderr.strip()
                logging.error(f"[E] Error al ejecutar el comando: {error_message}")
                base_prompt = input("[*] Por favor ingrese un nuevo prompt para corregir el error: ")
            else:
                print(f"[+] El comando se ejecutó correctamente: {result.stdout}")
                add_to_knowledge_base(base_prompt, message, KNOWLEDGE_BASE_FILE)
                break
        else:
            base_prompt = input("[?] Por favor ingrese un nuevo prompt o información adicional: ")

        time.sleep(3)

if __name__ == "__main__":
    main()
