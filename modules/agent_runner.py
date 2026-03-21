#!/usr/bin/env python3
"""
LazyOwn AI Agent - Ultimate Edition
Mejoras: Anti-Hang (Timeout), Gestión de Memoria, Validación de Argumentos y Anti-Loop.
"""

import json
import ast
import os
import sys
import logging
import argparse
import importlib.util
import threading
import queue
import inspect
from typing import Dict, List, Any, Optional, Callable
from time import sleep
from dataclasses import dataclass
from flask import Response, stream_with_context

# ===== IMPORTS DE TUS MODELOS =====
# Asegúrate de que ai_model.py esté en el mismo directorio o en el PYTHONPATH
try:
    from ai_model import AIModel, GroqModel, OllamaModel
except ImportError:
    print("❌ Error: No se encontró 'ai_model.py'. Asegúrate de tener tus conectores de modelos.")
    sys.exit(1)

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║  LazyOwn AI Agent - Ultimate Edition                     ║
║  • Anti-Loop & Memory Management                         ║
║  • Threaded Execution with Timeout                       ║
║  • Argument Validation                                   ║
╚═══════════════════════════════════════════════════════════╝
"""

# ===== CONFIGURACIÓN GLOBAL =====
MAX_OUTPUT_LENGTH = 3000   # Caracteres máximos por respuesta de herramienta
COMMAND_TIMEOUT = 60       # Segundos máximos para ejecutar un comando
MAX_HISTORY_MSGS = 15      # Ventana de memoria (mensajes)

def configure_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

# ===== AGENT TOOL ROBUSTO =====
class AgentTool:
    """Herramienta ejecutable con validación y truncado"""
    
    def __init__(self, name: str, description: str, func: Callable, 
                 parameters: Dict[str, Any], required: List[str] = None):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = {
            "type": "object",
            "properties": parameters,
            "required": required or list(parameters.keys())
        }
    
    def to_api_format(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
    
    def execute(self, **kwargs) -> str:
        """Ejecuta con validación de argumentos y formato claro"""
        # 1. Validación de Argumentos
        try:
            sig = inspect.signature(self.func)
            # Solo validamos si la función acepta kwargs específicos
            # (Las funciones wrapper suelen aceptar **kwargs genéricos, pero esto ayuda si es directo)
            bound = sig.bind_partial(**kwargs)
            bound.apply_defaults()
        except TypeError as e:
            msg = f"❌ Error de parámetros invocando {self.name}: {str(e)}"
            logging.error(msg)
            return msg

        # 2. Ejecución
        try:
            result = self.func(**kwargs)
            result_str = str(result)
            
            # 3. Truncado de Salida (Gestión de Contexto)
            if len(result_str) > MAX_OUTPUT_LENGTH:
                cut_len = len(result_str) - MAX_OUTPUT_LENGTH
                result_str = result_str[:MAX_OUTPUT_LENGTH] + \
                             f"\n\n[... SALIDA TRUNCADA: Se omitieron {cut_len} caracteres para ahorrar memoria ...]"

            output = f"""✅ COMANDO EJECUTADO: {self.name}
RESULTADO:
{result_str}

[FIN DEL RESULTADO]"""
            
            logging.debug(f"✅ {self.name} ejecutado correctamente")
            return output
            
        except Exception as e:
            error_msg = f"❌ ERROR DE EJECUCIÓN en {self.name}: {str(e)}"
            logging.error(error_msg)
            return error_msg


# ===== EXTRACTOR AST (Sin cambios mayores) =====
@dataclass
class CommandMetadata:
    name: str
    docstring: str
    params: List[str]
    has_args: bool

class ASTToolExtractor:
    """Extractor inteligente usando AST"""
    
    @staticmethod
    def extract_commands_from_file(file_path: str, prefix: str = "do_") -> List[CommandMetadata]:
        if not os.path.exists(file_path):
            logging.warning(f"⚠️ Archivo no encontrado: {file_path}")
            return []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError as e:
            logging.error(f"❌ Error de sintaxis en script objetivo: {e}")
            return []
        
        commands = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith(prefix):
                cmd_name = node.name[len(prefix):]
                docstring = ast.get_docstring(node) or f"Ejecuta comando {cmd_name}"
                
                params = []
                has_args = False
                for arg in node.args.args:
                    if arg.arg not in ('self', 'cls'):
                        params.append(arg.arg)
                        if arg.arg in ('line', 'args', 'statement'):
                            has_args = True
                
                commands.append(CommandMetadata(
                    name=cmd_name,
                    docstring=docstring.strip()[:500],
                    params=params,
                    has_args=has_args
                ))
        
        logging.info(f"✅ Extraídos {len(commands)} comandos del shell.")
        return commands


# ===== AGENT RUNNER =====
class AgentRunner:
    """Motor del agente con Límite de Uso por Herramienta (Anti-Spam)"""
    
    def __init__(self, model: Any, system_prompt: str = None, max_iterations: int = 10):
        self.model = model
        self.max_iterations = max_iterations
        self.tools: Dict[str, AgentTool] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.last_tool_calls = []
        
        # --- NUEVO: Control de uso por tipo de herramienta ---
        self.tool_usage_count: Dict[str, int] = {} 
        self.executed_commands = set()
        
        self.system_prompt = system_prompt or "Eres un asistente útil."
        self._reset_history()
    
    def _reset_history(self):
        self.conversation_history = [{
            "role": "system", 
            "content": self.system_prompt
        }]

    def _manage_memory(self):
        """Mantiene la ventana de contexto limpia"""
        MAX_HISTORY = 12
        if len(self.conversation_history) > MAX_HISTORY:
            logging.info("🧹 Recortando memoria...")
            # Mantener System Prompt + Últimos mensajes
            self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-(MAX_HISTORY-1):]

    def register_tool(self, tool: AgentTool):
        self.tools[tool.name] = tool

    def register_tool_from_instance(self, func: Callable):
        """Wrap a plain function as an AgentTool using its signature and docstring."""
        sig = inspect.signature(func)
        parameters = {}
        required = []
        for pname, param in sig.parameters.items():
            parameters[pname] = {"type": "string", "description": f"Parameter {pname}"}
            if param.default is inspect.Parameter.empty:
                required.append(pname)
        tool = AgentTool(
            name=func.__name__,
            description=(func.__doc__ or func.__name__).strip(),
            func=func,
            parameters=parameters,
            required=required,
        )
        self.register_tool(tool)
    
    def register_tools_from_metadata(self, commands: List[CommandMetadata], executor: Callable[[str], str]):
        # (Esta parte se mantiene igual que en tu código anterior)
        for cmd in commands:
            def make_executor(cmd_name):
                def wrapper(command: str = "", **kwargs) -> str:
                    full_cmd = f"{cmd_name} {command}".strip()
                    return executor(full_cmd)
                return wrapper
            
            if cmd.has_args or not cmd.params:
                parameters = {"command": {"type": "string", "description": f"Args para {cmd.name}"}}
                required = ["command"]
            else:
                parameters = {p: {"type": "string", "description": f"Param {p}"} for p in cmd.params}
                required = cmd.params
            
            tool = AgentTool(
                name=f"cmd_{cmd.name}",
                description=cmd.docstring,
                func=make_executor(cmd.name),
                parameters=parameters,
                required=required
            )
            self.register_tool(tool)
    
    def get_tools_for_api(self) -> Optional[List[Dict[str, Any]]]:
        if not self.tools: return None
        return [tool.to_api_format() for tool in self.tools.values()]
    
    def run(self, user_input: str) -> str:
        # Reiniciar contadores en cada nueva instrucción principal
        self.conversation_history.append({"role": "user", "content": user_input})
        
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            self._manage_memory()
            logging.info(f"🔄 PASO {iteration}/{self.max_iterations}")
            
            response = self._call_model()
            tool_calls = getattr(response.choices[0].message, 'tool_calls', None)
            
            if not tool_calls:
                return response.choices[0].message.content
            
            # Procesar herramientas
            for tool_call in tool_calls:
                # Inyectar el resultado de vuelta al historial
                self._process_tool_call(tool_call)

        return f"⏱️ Límite de pasos alcanzado ({self.max_iterations}). Revisa lo encontrado."
    
    def _call_model(self):
        # Inyectar recordatorio anti-loop dinámicamente si ya se ejecutaron comandos
        current_context = list(self.conversation_history)
        
        # Si ya hemos ejecutado nmap, añadir recordatorio fuerte
        if self.tool_usage_count.get('cmd_nmap', 0) > 0:
            current_context.append({
                "role": "system",
                "content": "SISTEMA: Ya has escaneado. NO uses nmap de nuevo. Analiza los puertos abiertos y usa otra herramienta específica (ej: curl, gobuster, smbclient) o da tu reporte final."
            })

        try:
            return self.model.client.chat.completions.create(
                model=self.model.model,
                messages=current_context,
                tools=self.get_tools_for_api(),
                tool_choice="auto",
                temperature=0.1
            )
        except Exception as e:
            logging.error(f"Error API: {e}")
            raise
    
    def _process_tool_call(self, tool_call):
        tool_name = tool_call.function.name
        
        # --- LÓGICA ANTI-LOOP MEJORADA ---
        # 1. Incrementar contador global de esa herramienta
        usage = self.tool_usage_count.get(tool_name, 0) + 1
        self.tool_usage_count[tool_name] = usage
        
        # 2. Verificar límite duro (Máximo 2 veces por herramienta, Nmap máximo 1)
        limit = 1 if "nmap" in tool_name else 2
        
        if usage > limit:
            logging.warning(f"⛔ BLOQUEANDO {tool_name} (Uso excesivo: {usage})")
            result = f"""⛔ SISTEMA: PROHIBIDO EJECUTAR {tool_name} DE NUEVO.
Ya has usado esta herramienta {usage-1} veces.
Debes AVANZAR. Usa una herramienta diferente o finaliza el análisis.
Si ya tienes la info, responde al usuario."""
        else:
            # Ejecución normal
            try:
                args = json.loads(tool_call.function.arguments)
            except:
                args = {}
            
            # Verificar duplicado exacto
            cmd_key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
            if cmd_key in self.executed_commands:
                result = "⚠️ ERROR: Ya ejecutaste este comando EXACTO. No lo repitas."
            else:
                self.executed_commands.add(cmd_key)
                if tool_name in self.tools:
                    logging.info(f"🔨 Ejecutando {tool_name} (Intento {usage})")
                    result = self.tools[tool_name].execute(**args)
                else:
                    result = "❌ Herramienta no encontrada."

        # Guardar en historial
        self.conversation_history.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [tool_call]
        })
        self.conversation_history.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": result
        })

# ===== SHELL WRAPPER CON TIMEOUT =====
class LazyOwnShellWrapper:
    """Wrapper que ejecuta comandos en hilos seguros"""
    
    def __init__(self, script_path: str):
        self.script_path = os.path.abspath(script_path)
        self.script_dir = os.path.dirname(self.script_path)
        self.shell = None
        self.commands: List[CommandMetadata] = []
        self._load_shell()
    
    def _load_shell(self):
        self.commands = ASTToolExtractor.extract_commands_from_file(self.script_path)
        
        try:
            sys.path.insert(0, self.script_dir)
            spec = importlib.util.spec_from_file_location("lazyown", self.script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Buscar la clase shell dinámicamente
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                # Buscamos una clase que tenga métodos do_*
                if isinstance(attr, type) and any(m.startswith('do_') for m in dir(attr)):
                    self.shell = attr()
                    logging.info(f"✅ Shell cargado exitosamente: {attr_name}")
                    break
        except Exception as e:
            logging.error(f"❌ Error cargando módulo del shell: {e}")
        finally:
            if self.script_dir in sys.path:
                sys.path.remove(self.script_dir)
    
    def execute_command(self, command: str) -> str:
        """Ejecuta comando con timeout usando threading"""
        if not self.shell:
            return "❌ Shell no disponible"
        
        result_queue = queue.Queue()
        
        def target():
            # Capturar stdout dentro del hilo
            import io
            capture = io.StringIO()
            original_stdout = sys.stdout
            try:
                sys.stdout = capture
                if hasattr(self.shell, 'onecmd_plus_hooks'):
                    self.shell.onecmd_plus_hooks(command)
                elif hasattr(self.shell, 'onecmd'):
                    self.shell.onecmd(command)
                else:
                    print("Error: Shell no tiene método onecmd")
                
                result_queue.put(capture.getvalue())
            except Exception as e:
                result_queue.put(f"❌ Error en ejecución: {str(e)}")
            finally:
                sys.stdout = original_stdout

        # Lanzar hilo
        t = threading.Thread(target=target)
        t.start()
        
        # Esperar con timeout
        t.join(timeout=COMMAND_TIMEOUT)
        
        if t.is_alive():
            logging.error(f"⏱️ TIMEOUT en comando: {command}")
            return f"⏱️ TIMEOUT: El comando '{command}' excedió los {COMMAND_TIMEOUT} segundos. Posiblemente está esperando input o se colgó."
        
        try:
            return result_queue.get_nowait() or "✓ Comando ejecutado (sin salida visual)"
        except queue.Empty:
            return "⚠️ Error desconocido: No se obtuvo respuesta del hilo."

    def get_commands_summary(self) -> str:
        # Resumen simplificado para el Prompt
        names = [c.name for c in self.commands]
        return ", ".join(names[:50]) + ("..." if len(names) > 50 else "")


# ===== VULNBOT CLI =====
class VulnBotCLI:
    
    def __init__(self, provider: str, mode: str, debug: bool, script_path: str):
        self.provider = provider
        self.script_dir = os.getcwd()
        self.knowledge_base_file = "knowledge_base.json"
        
        configure_logging(debug)
        
        self.model = self._load_model()
        self.shell_wrapper = LazyOwnShellWrapper(script_path)
        self.agent = None
        self._setup_agent()
    
    def _load_model(self) -> AIModel:
        if self.provider == "groq":
            key = os.environ.get("GROQ_API_KEY")
            if not key: raise ValueError("Falta GROQ_API_KEY")
            return GroqModel(api_key=key)
        elif self.provider == "deepseek":
            return OllamaModel(model="deepseek-r1:1.5b")
        else:
            raise ValueError("Proveedor desconocido")
    
    def _setup_agent(self):
        total_cmds = len(self.shell_wrapper.commands)
        summary = self.shell_wrapper.get_commands_summary()
        
        # Prompt mejorado con lógica ReAct (Pensar antes de actuar)
        system_prompt = f"""Eres LazyOwn, un Pentester AI experto y autónomo.

OBJETIVO: Analizar vulnerabilidades y explotarlas de forma ética.

HERRAMIENTAS ({total_cmds} disponibles):
{summary}

REGLAS DE ORO:
1. PENSAMIENTO (Thought): Antes de actuar, explica brevemente POR QUÉ eliges esa herramienta.
2. PRECISIÓN: Si un comando falla, lee el error y corrige los argumentos.
3. ANTI-LOOP: Jamás repitas el mismo comando con los mismos argumentos si ya obtuviste resultado.
4. ECONOMÍA: Usa máximo 5 pasos. Si tienes la info, termina con un resumen.
5. SINTAXIS: Para ejecutar usa las funciones provistas (ej: cmd_nmap).

Si el resultado es muy largo, céntrate en los puertos abiertos o vulnerabilidades críticas.
"""
        self.agent = AgentRunner(self.model, system_prompt, max_iterations=8)
        
        if self.shell_wrapper.commands:
            self.agent.register_tools_from_metadata(
                self.shell_wrapper.commands,
                self.shell_wrapper.execute_command
            )
        else:
            logging.warning("⚠️ No se detectaron comandos en el archivo provisto.")

    def process_request(self, user_input: str) -> str:
        return self.agent.run(user_input)


# ===== MODO INTERACTIVO =====
def interactive_mode(bot: VulnBotCLI):
    print("\n[💻 Modo Interactivo LazyOwn]")
    print("Escribe tu objetivo (ej: 'Escanea 10.10.10.5 y busca SMB')")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        try:
            u_input = input("LazyOwn > ").strip()
            if u_input.lower() in ('salir', 'exit'): break
            if not u_input: continue
            
            response = bot.process_request(u_input)
            print(f"\n🤖 AGENTE:\n{response}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Error ciclo principal: {e}")

# ===== MAIN =====
def parse_args():
    parser = argparse.ArgumentParser(description='LazyOwn AI Agent - Ultimate')
    parser.add_argument('--script', '-s', type=str, default='lazyown.py', help='Script Python con clase CMD')
    parser.add_argument('--provider', '-p', default='groq', choices=['groq', 'deepseek'])
    parser.add_argument('--debug', '-d', action='store_true')
    # Opcional: Modo archivo directo
    parser.add_argument('--instruction', '-i', type=str, help='Instrucción directa (no interactivo)')
    return parser.parse_args()

def main():
    print(BANNER)
    args = parse_args()
    
    if not os.path.exists(args.script):
        print(f"❌ Error: No existe el archivo {args.script}")
        sys.exit(1)
        
    try:
        bot = VulnBotCLI(args.provider, "console", args.debug, args.script)
        
        if args.instruction:
            print(f"[*] Ejecutando instrucción: {args.instruction}")
            res = bot.process_request(args.instruction)
            print("\nRESULTADO FINAL:\n", res)
        else:
            interactive_mode(bot)
            
    except Exception as e:
        logging.critical(f"Error Fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()