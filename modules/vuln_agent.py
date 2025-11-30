#!/usr/bin/env python3
import argparse
import sys
import os
import json
import logging
import importlib.util
import importlib.machinery
from flask import Response, stream_with_context
from ai_model import AIModel, GroqModel, OllamaModel
from agent_tool import AgentTool
from agent_runner import AgentRunner

BANNER = """
[LazyOwn AI Agent]
Asistente de Pentesting con Modo Agente ACTIVO
[*] Ejecuta comandos reales desde tu CLI
"""

def configure_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

class LazyOwnShellWrapper:
    """Wrapper robusto para integrar lazyown.py"""
    
    def __init__(self, script_path: str):
        self.script_path = os.path.abspath(script_path)
        self.script_dir = os.path.dirname(self.script_path)
        self.shell = None
        self._load_shell_with_deps()
    
    def _load_shell_with_deps(self):
        """Carga el módulo resolviendo dependencias correctamente"""
        try:
            # Añadir el directorio del script al sys.path temporalmente
            if self.script_dir not in sys.path:
                sys.path.insert(0, self.script_dir)
            
            # Cargar el módulo
            spec = importlib.util.spec_from_file_location("lazyown", self.script_path)
            module = importlib.util.module_from_spec(spec)
            
            # Ejecutar el módulo para resolver importaciones
            spec.loader.exec_module(module)
            
            # Buscar la clase principal (cmd.Cmd o similar)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):
                    # Verificar si tiene métodos do_ (cmd2)
                    if any(m.startswith('do_') for m in dir(attr) if m != 'do_exit'):
                        self.shell = attr()
                        logging.info(f"✅ CLI cargada exitosamente: {attr_name}")
                        break
            
            if not self.shell:
                logging.error("No se encontró clase CLI con métodos do_*")
                
        except Exception as e:
            logging.error(f"Error cargando {self.script_path}: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Remover el path temporal si lo añadimos
            if self.script_dir in sys.path:
                sys.path.remove(self.script_dir)
    
    def execute_command(self, command: str) -> str:
        """Ejecuta un comando en la CLI y retorna el output"""
        if not self.shell:
            return "Error: CLI no cargada - no se puede ejecutar comandos"
        
        try:
            # Para cmd2: usar onecmd_plus_hooks
            if hasattr(self.shell, 'onecmd_plus_hooks'):
                original_stdout = sys.stdout
                sys.stdout = captured_output = __import__('io').StringIO()
                
                try:
                    self.shell.onecmd_plus_hooks(command)
                    output = captured_output.getvalue()
                finally:
                    sys.stdout = original_stdout
                
                return output or f"Comando '{command}' ejecutado (sin output visible)"
            
            # Fallback para cmd.Cmd estándar
            elif hasattr(self.shell, 'onecmd'):
                original_stdout = sys.stdout
                sys.stdout = captured_output = __import__('io').StringIO()
                
                try:
                    self.shell.onecmd(command)
                    output = captured_output.getvalue()
                finally:
                    sys.stdout = original_stdout
                
                return output or f"Comando '{command}' ejecutado (sin output visible)"
            
            else:
                return "Error: CLI no tiene método onecmd disponible"
                
        except Exception as e:
            return f"Error ejecutando '{command}': {str(e)}\n{__import__('traceback').format_exc()}"
    
    def get_available_commands(self) -> list:
        """Retorna lista de comandos disponibles"""
        if not self.shell:
            return []
        
        commands = []
        for attr in dir(self.shell):
            if attr.startswith('do_') and attr != 'do_exit':
                commands.append(attr[3:])
        return commands

class VulnBotCLI:
    def __init__(self, provider: str = "groq", mode: str = "console", 
                 debug: bool = False, script_path: str = "lazyown.py"):
        self.provider = provider
        self.mode = mode
        self.debug = debug
        self.script_path = script_path
        self.script_dir = os.getcwd()
        self.knowledge_base_file = f"{self.script_dir}/knowledge_base_vuln.json"
        self.model = self._load_model()
        self.shell_wrapper = LazyOwnShellWrapper(script_path)
        self.agent = None
        self._setup_agent()
        configure_logging(debug)
    
    def _load_model(self) -> AIModel:
        if self.provider == "groq":
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY no está definida en las variables de entorno.")
            return GroqModel(api_key=api_key)
        elif self.provider == "deepseek":
            return OllamaModel(model="deepseek-r1:1.5b")
        else:
            raise ValueError(f"Proveedor no soportado: {self.provider}")
    
    def _setup_agent(self):
        """Configura el agente para EJECUTAR COMANDOS REALES"""
        available_cmds = self.shell_wrapper.get_available_commands()
        commands_list = ", ".join(available_cmds[:10]) + ("..." if len(available_cmds) > 10 else "")
        
        system_prompt = f"""Eres un agente AUTÓNOMO de pentesting experto llamado LazyOwn.
TU OBJETIVO: Ejecutar comandos reales de pentesting usando la CLI disponible.
NO leas archivos localmente - USA LAS HERRAMIENTAS PARA EJECUTAR COMANDOS.

COMANDOS DISPONIBLES EN TU CLI:
{commands_list}
...

REGLAS DE EJECUCIÓN:
1. Para analizar datos, EJECUTA comandos como 'run_cli_command("nmap -sV 10.10.11.78")'
2. Analiza el resultado de cada comando que ejecutas
3. NUNCA simules resultados - usa run_cli_command para ejecutar comandos reales
4. Sé AGRESIVO en el reconocimiento pero preciso
5. Ejecuta al menos 3-5 comandos de reconocimiento antes de dar conclusiones
6. Documenta cada acción ejecutada"""

        self.agent = AgentRunner(self.model, system_prompt, max_iterations=10)
        self._register_pentesting_tools()
    
    def _register_pentesting_tools(self):
        """Registra la herramienta principal para ejecutar comandos"""
        
        if not self.shell_wrapper.shell:
            logging.warning("⚠️ CLI no disponible, usando herramientas de fallback")
            self._register_fallback_tools()
            return
        
        # Herramienta principal: ejecutar cualquier comando
        def run_cli_command(command: str) -> str:
            """Ejecuta un comando directamente en la CLI de pentesting"""
            logging.info(f"  🔥 EJECUTANDO COMANDO REAL: {command}")
            return self.shell_wrapper.execute_command(command)
        
        run_tool = AgentTool(
            name="run_cli_command",
            description="Ejecuta CUALQUIER comando de pentesting reconocimiento (nmap, ping, gospider, kerbrute, etc.)",
            func=run_cli_command,
            parameters={
                "command": {
                    "type": "string", 
                    "description": "Comando completo con argumentos (ej: 'nmap -sV -p 80,443 10.10.11.78')"
                }
            },
            required=["command"]
        )
        self.agent.register_tool(run_tool)
    
    def _register_fallback_tools(self):
        def read_file(path: str) -> str:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        self.agent.register_tool_from_instance(read_file)
    
    def read_file_content(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            full_path = os.path.join(self.script_dir, file_path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
            file_path = full_path
        
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    def load_knowledge_base(self) -> dict:
        if os.path.exists(self.knowledge_base_file):
            with open(self.knowledge_base_file, "r") as f:
                return json.load(f)
        return {}
    
    def save_knowledge_base(self, kb: dict) -> None:
        with open(self.knowledge_base_file, "w") as f:
            json.dump(kb, f, indent=4)
    
    def get_relevant_knowledge(self, prompt: str) -> str:
        kb = self.load_knowledge_base()
        matches = [f"{k}: {v}" for k, v in kb.items() if prompt.lower() in k.lower()]
        return "\n".join(matches) if matches else "No hay conocimiento previo relevante."
    
    def add_to_knowledge_base(self, prompt: str, response: str):
        kb = self.load_knowledge_base()
        kb[prompt] = response
        self.save_knowledge_base(kb)
        logging.info("Respuesta guardada en base de conocimiento.")
    
    def process_with_context(self, file_path: str, event: str = None) -> str:
        content = self.read_file_content(file_path)
        knowledge = self.get_relevant_knowledge(content)
        
        prompt = f"""ARCHIVO DE ENTRADA:
        {content[:800]}...

INFORMACIÓN EXTRAÍDA:
- Tipo de archivo: {file_path.split('.')[-1].upper()}
- IPs/dominios detectados: [extraer del contenido]
- Servicios detectados: [extraer del contenido]

MISIÓN CRÍTICA:
Eres un agente de pentesting AUTÓNOMO. DEBES:
1. EJECUTAR al menos 3-5 comandos de reconocimiento usando run_cli_command()
2. Analizar los RESULTADOS REALES de cada comando
3. Identificar vectores de ataque basados en datos reales
4. Proporcionar un PLAN DE ACCIÓN concreto

EJEMPLOS DE COMANDOS A EJECUTAR:
- run_cli_command("ping 10.10.11.78")
- run_cli_command("nmap -sV -p 53,88,445 10.10.11.78")
- run_cli_command("gospider -s http://10.10.11.78")

REGLAS:
- NUNCA simules resultados
- EJECUTA comandos reales
- Analiza cada salida antes de continuar
- Prioriza reconocimiento activo sobre análisis pasivo"""

        if self.mode == "web":
            return self._stream_response(prompt)
        else:
            return self.agent.run(prompt)
    
    def _stream_response(self, prompt: str) -> Response:
        def generate():
            for token in self.model.stream_generate(prompt):
                yield token
        return Response(stream_with_context(generate()), mimetype='text/plain')


def parse_args():
    parser = argparse.ArgumentParser(description='LazyOwn AI Agent')
    parser.add_argument('--file', '-f', type=str, help='Archivo de entrada (NMAP, CSV, etc.)')
    parser.add_argument('--provider', '-p', choices=['groq', 'deepseek'], default='groq')
    parser.add_argument('--mode', '-m', choices=['console', 'web'], default='console')
    parser.add_argument('--script', '-s', type=str, default='lazyown.py', help='Script de CLI (cmd2)')
    parser.add_argument('--event', '-e', type=str, help='Evento opcional')
    parser.add_argument('--interactive', '-i', action='store_true', help='Modo chat interactivo')
    parser.add_argument('--debug', '-d', action='store_true', help='Modo depuración')
    return parser.parse_args()


def interactive_mode(bot: VulnBotCLI):
    print("\n[Modo Interactivo - Agente de Pentesting Activo]")
    print("Escribe comandos o 'salir' para terminar.\n")
    while True:
        try:
            user_input = input("[Tú] > ").strip()
            if user_input.lower() in ('salir', 'exit', 'quit'):
                print("¡Hasta luego!")
                break
            if not user_input:
                continue
            
            response = bot.agent.run(user_input)
            print(f"\n[Agente] > {response}\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Error: {e}")
            print(f"[Error] {e}")


def main():
    print(BANNER)
    args = parse_args()
    
    bot = VulnBotCLI(
        provider=args.provider,
        mode=args.mode,
        debug=args.debug,
        script_path=args.script
    )
    
    if args.interactive:
        interactive_mode(bot)
        return
    
    if not args.file:
        print("[!] Error: Necesitas especificar --file o usar --interactive")
        sys.exit(1)
    
    try:
        print(f"[*] Procesando archivo: {args.file}")
        print(f"[*] CLI: {args.script}")
        print(f"[*] Modelo: {args.provider}")
        print("[*] El agente ejecutará comandos reales de pentesting...\n")
        
        response = bot.process_with_context(args.file, event=args.event)
        
        if args.mode == "console":
            print(f"\n[RESULTADO DEL AGENTE]\n{'='*70}")
            print(response)
            print('='*70)
            bot.add_to_knowledge_base(args.file, response)
        else:
            return response
    except Exception as e:
        logging.exception("Error fatal")
        print(f"[Error] {e}")
        sys.exit(1)


# CORREGIDO: Esto debe estar FUERA de cualquier clase o función
if __name__ == "__main__":
    main()