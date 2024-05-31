import os
import argparse
import logging
import signal
import sys
import time
import subprocess
from groq import Groq

# Banner
print("██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗")
print("██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║")
print("██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║")
print("██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║")
print("███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║")
print("╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝")
print(f"[*] Iniciando: LazyOwn GPT One Liner Cli Assistent [;,;]")

complex_prompt = ""

def signal_handler(sig, frame):
    print(f'\n[*] Interrupción recibida, saliendo del programa.{complex_prompt}')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def show_help(message):
    help_message = f"""
{message}

[?] Uso: python script.py --prompt "<tu prompt>" [--debug]

[?] Opciones:
  --prompt    " El prompt para la tarea de programación (requerido)."
  --debug, -d  " Habilita el modo debug para mostrar mensajes de depuración."

[?] Asegúrate de configurar tu API key antes de ejecutar el script:
  export GROQ_API_KEY=<tu_api_key>
[->] visit: https://console.groq.com/docs/quickstart not sponsored link
"""
    print(help_message)
    sys.exit(1)

# Verificar la API key
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    show_help("[E] Error: La API key no está configurada.")

# Configura el cliente con tu API key
client = Groq(api_key=api_key)

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir y parsear los argumentos de línea de comandos
def parse_args():
    parser = argparse.ArgumentParser(description='[+] LazyGPT Asistente de Tareas de Programación.')
    parser.add_argument('--prompt', type=str, required=True, help='El prompt para la tarea de programación/Tarea Cli')
    parser.add_argument('--debug', '-d', action='store_true', help='Habilita el modo debug para mostrar mensajes de depuración')
    args = parser.parse_args()
    if not args.prompt:
        show_help("Error: Falta el argumento --prompt.")
    return args

# Función para crear el prompt complejo
def create_complex_prompt(base_prompt, history, error_message=None):
    error_context = f"El siguiente error ocurrió durante la ejecución: {error_message}" if error_message else "No errors detected in the last iteration."
    prompt_message = f"""
Create a coherent command or script in a single line to achieve the goal specified by the user in the argument args.prompt. Use pipes (|) only for passing stdout to stdin between commands when necessary, and use logical operators (&&) to chain commands that need to be executed sequentially. Ensure the command handles directory navigation correctly and includes proper content redirection for file creation. Respond only with the requested command and nothing else. Do not provide explanations, just the exact command to copy and paste.  {base_prompt} 

Previous messages:
{history}

{error_context}
"""
    return prompt_message

# Función principal
def main():
    # Recibir el prompt inicial del usuario
    args = parse_args()
    base_prompt = args.prompt
    history = []
    error_message = None

    while True:
        # Crear el prompt complejo
        complex_prompt = create_complex_prompt(base_prompt, '\n'.join(history), error_message)
        error_message = None  # Reset the error message for the next iteration

        # Enviar el prompt al modelo y obtener la respuesta
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": complex_prompt}],
                model="llama3-8b-8192",
            )
            if args.debug:
                print(f"[DEBUG] : {complex_prompt}")
            message = chat_completion.choices[0].message.content.strip()
            print(f"[R] Respuesta de Groq:\n{message}")

            # Agregar el prompt y la respuesta al historial
            history.append(f"User: {base_prompt}")
            history.append(f"Groq: {message}")

            # Validar el comando antes de ejecutarlo
            if not message:
                logging.error("[!] No se recibió un comando válido del modelo.")
                base_prompt = input("[?] Por favor ingrese un nuevo prompt o información adicional: ")
                continue

            # Preguntar al usuario si desea ejecutar el comando
            user_input = input("[?] ¿Deseas ejecutar el comando? (si/no): ").strip().lower()
            if user_input == 'si':
                # Ejecutar el comando en el shell y capturar cualquier error
                print(f"[$] Ejecutando el comando: > {message}")
                result = subprocess.run(message, shell=True, capture_output=True, text=True)
                print(f"[C] return code: {result.returncode}")
                if result.returncode != 0:
                    error_message = result.stderr.strip()
                    logging.error(f"[E] Error al ejecutar el comando: {error_message}")
                    base_prompt = input("[*] Por favor ingrese un nuevo prompt para corregir el error: ")
                else:
                    print(f"[+] El comando se ejecutó correctamente: {result.stdout}")
                    break
            else:
                base_prompt = input("[?] Por favor ingrese un nuevo prompt o información adicional: ")

            time.sleep(3)
        except Exception as e:
            logging.error(f"[E] Error al comunicarse con la API: {e}")
            break

if __name__ == "__main__":
    main()
