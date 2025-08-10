# main.py
import argparse
import sys
from vulnbot import VulnBotCLI
BANNER = "Vuln Bot LazyOwn RedTeam Technology"
def parse_args():
    parser = argparse.ArgumentParser(description='VulnBot: Asistente de Pentesting con Groq o DeepSeek')
    parser.add_argument('--file', type=str, required=True, help='Ruta del archivo con datos (ej. nmap.txt)')
    parser.add_argument('--provider', type=str, choices=['groq', 'deepseek'], default='groq', help='Modelo a usar')
    parser.add_argument('--mode', type=str, choices=['console', 'web'], default='console', help='Salida: consola o web (SSE)')
    parser.add_argument('--event', type=str, help='Evento opcional desde event_config.json')
    parser.add_argument('--debug', '-d', action='store_true', help='Modo depuración')
    return parser.parse_args()

def main():
    print(BANNER)
    args = parse_args()

    bot = VulnBotCLI(provider=args.provider, mode=args.mode, debug=args.debug)

    try:
        response = bot.process_with_context(args.file, event=args.event)
        if args.mode == "console":
            print(f"[R] Respuesta:\n{response}")
            # Guardar en base de conocimiento si es consola
            bot.add_to_knowledge_base(args.file, response)
        else:
            # En modo web, `response` ya es un `Response` de Flask
            return response
    except Exception as e:
        print(f"[E] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
