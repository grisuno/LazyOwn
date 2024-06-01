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

[?] Uso: python script.py --prompt "<tu prompt>" [--debug]

[?] Opciones:
  --prompt    "El prompt para la tarea de programación (requerido)."
  --debug, -d "Habilita el modo debug para mostrar mensajes de depuración."

[?] Asegúrate de configurar tu API key antes de ejecutar el script:
  export GROQ_API_KEY=<tu_api_key>
[->] visit: https://console.groq.com/docs/quickstart not sponsored link
"""

KNOWLEDGE_BASE_FILE = "knowledge_base.json"

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
    return parser.parse_args()

def create_complex_prompt(base_prompt: str, history: str, error_message: str = None) -> str:
    error_context = f"El siguiente error ocurrió durante la ejecución: {error_message}" if error_message else "No errors detected in the last iteration."
    return f"""
Create a coherent command or script in a single line to achieve the goal specified by the user in the argument args.prompt. Use pipes (|) only for passing stdout to stdin between commands when necessary, and use logical operators (&&) to chain commands that need to be executed sequentially. Ensure the command handles directory navigation correctly and includes proper content redirection for file creation. Respond only with the requested command and nothing else. Do not provide explanations, just the exact command to copy and paste. {base_prompt}

Previous messages:
{history}

{error_context}
"""

def execute_command(command: str) -> subprocess.CompletedProcess:
    return subprocess.run(command, shell=True, capture_output=True, text=True)

def load_knowledge_base() -> dict:
    if os.path.exists(KNOWLEDGE_BASE_FILE):
        with open(KNOWLEDGE_BASE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_knowledge_base(knowledge_base: dict) -> None:
    with open(KNOWLEDGE_BASE_FILE, "w") as f:
        json.dump(knowledge_base, f, indent=4)

def add_to_knowledge_base(prompt: str, command: str) -> None:
    knowledge_base = load_knowledge_base()
    knowledge_base[prompt] = command
    save_knowledge_base(knowledge_base)

def get_command_from_knowledge_base(prompt: str) -> str:
    knowledge_base = load_knowledge_base()
    return knowledge_base.get(prompt, "")

def main() -> None:
    print(BANNER)
    
    args = parse_args()
    configure_logging(args.debug)

    api_key = check_api_key()
    client = Groq(api_key=api_key)

    base_prompt = args.prompt
    history = []
    error_message = None

    while True:
        known_command = get_command_from_knowledge_base(base_prompt)
        if known_command:
            user_input = input(f"[?] Comando conocido encontrado: {known_command}. ¿Deseas ejecutarlo? (si/no): ").strip().lower()
            if user_input == 'si':
                message = known_command
            else:
                known_command = ""
        
        if not known_command:
            complex_prompt = create_complex_prompt(base_prompt, '\n'.join(history), error_message)
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
                add_to_knowledge_base(base_prompt, message)
                break
        else:
            base_prompt = input("[?] Por favor ingrese un nuevo prompt o información adicional: ")

        time.sleep(3)

if __name__ == "__main__":
    main()
