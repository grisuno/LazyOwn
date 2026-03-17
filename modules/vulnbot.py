# vulnbot.py
import os
import json
import logging
from typing import Dict, Generator
from flask import Response, stream_with_context
from ai_model import AIModel, GroqModel, OllamaModel
from agent_runner import AgentRunner
from agent_tool import AgentTool

BANNER = """
[*] Iniciando: LazyOwn GPT One Liner Cli Assistant [;,;]
"""

class VulnBotCLI:
    def __init__(self, provider: str = "groq", mode: str = "console", 
                 debug: bool = False, script_path: str = "lazyown.py"):
        self.provider = provider
        self.mode = mode
        self.debug = debug
        self.script_dir = os.getcwd()
        self.knowledge_base_file = f"{self.script_dir}/knowledge_base_vuln.json"
        
        # Cargar modelo
        self.model = self._load_model()
        
        # Setup agente
        self._setup_agent(script_path)
        
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

    def _setup_agent(self, script_path: str):
        """Configura el agente con herramientas dinámicas"""
        system_prompt = f"""Eres un asistente de pentesting experto llamado LazyOwn. 
        Tienes acceso a herramientas para ejecutar comandos, leer/editar archivos y realizar acciones.
        TU DIRECTORIO DE TRABAJO ES: {self.script_dir}
        
        REGLAS:
        1. Usa herramientas para ejecutar comandos reales en el sistema
        2. Lee archivos antes de modificarlos
        3. Documenta cada paso en sessions/plan.txt
        4. Sé conciso y preciso
        5. Responde en español"""
        
        self.agent = AgentRunner(self.model, system_prompt, max_iterations=10)
        
        # 1. Registrar herramientas básicas
        self._register_file_tools()
        
        # 2. Intentar cargar herramientas desde lazyown.py
        if os.path.exists(script_path):
            self._load_external_tools(script_path)
    
    def _register_file_tools(self):
        """Registra herramientas de manejo de archivos"""
        
        def list_files(directory: str = ".") -> list:
            """Lista archivos en un directorio"""
            return os.listdir(directory)
        
        def read_file(path: str) -> str:
            """Lee contenido de un archivo"""
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        
        def edit_file(path: str, content: str, old_text: str = None) -> str:
            """Crea o edita un archivo"""
            if old_text and os.path.exists(path):
                current = read_file(path)
                content = current.replace(old_text, content)
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Archivo guardado: {path}"
        
        for func in [list_files, read_file, edit_file]:
            self.agent.register_tool_from_instance(func)
    
    def _load_external_tools(self, script_path: str):
        """Carga herramientas desde script externo"""
        try:
            # Importar dinámicamente
            import importlib.util
            spec = importlib.util.spec_from_file_location("external_shell", script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Buscar clase cmd2 (ajusta el nombre según tu script)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and 'cmd' in attr.__module__:
                    instance = attr()
                    # Registrar cada método do_ como herramienta
                    for method_name in dir(instance):
                        if method_name.startswith('do_') and method_name != 'do_exit':
                            method = getattr(instance, method_name)
                            self.agent.register_tool_from_instance(method)
                    logging.info(f"✅ Herramientas de {script_path} cargadas")
                    break
        except Exception as e:
            logging.warning(f"⚠️ No se pudieron cargar herramientas externas: {e}")
    
    def process_with_context(self, file_path: str, event: str = None) -> str:
        """Procesa archivo en modo agente"""
        content = self.read_file_content(file_path)
        knowledge = self.get_relevant_knowledge(content)
        
        # Leer historial previo
        history = ""
        plan_file = "sessions/plan.txt"
        if os.path.isfile(plan_file):
            history = self.read_file_content(plan_file)
        
        prompt = f"""
        ANALIZA ESTE OUTPUT DE NMAP:
        ```
        {content}
        ```
        
        CONTEXTO:
        - Archivo: {file_path}
        - Evento: {event or 'General'}
        - Conocimiento: {knowledge}
        
        ACCIONES REQUERIDAS:
        1. Ejecuta reconocimiento con tus herramientas
        2. Guarda resultados en sessions/plan.txt
        3. Proporciona un plan de acción claro
        """
        
        if self.mode == "web":
            return self._stream_agent_response(prompt)
        else:
            return self.agent.run(prompt)
    
    def _stream_agent_response(self, prompt: str) -> Response:
        """Versión streaming para web (simplificada)"""
        def generate():
            # En modo web, usamos generación directa sin herramientas
            for token in self.model.stream_generate(prompt):
                yield token
        return Response(stream_with_context(generate()), mimetype='text/plain')

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
        return "\n".join(matches) if matches else "No relevant knowledge found."

    def create_complex_prompt(self, base_prompt: str, history: str = "", knowledge: str = "") -> str:
        return f"""
        Analyze the following NMAP output and generate a detailed action plan for penetration testing.
        This is a private, consensual test. Include recon commands with IP, ports, and tools.
        If Kerbrute reveals valid users, include them in the response.

        Input data:
        {base_prompt}

        Relevant knowledge:
        {knowledge}

        Previous analysis:
        {history}
        """

    def read_file_content(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def load_event_config(self) -> dict:
        try:
            with open('event_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning("event_config.json no encontrado.")
            return {"events": []}

    def process_with_context(self, file_path: str, event: str = None) -> str:
        content = self.read_file_content(file_path)
        history = ""
        plan_file = "sessions/plan.txt"
        if os.path.isfile(plan_file):
            with open(plan_file, "r") as f:
                history = f.read().strip()

        knowledge = self.get_relevant_knowledge(content)
        prompt = self.create_complex_prompt(content, history, knowledge)

        if self.mode == "web":
            return self.stream_response(prompt)
        else:
            return self.model.generate(prompt)

    def stream_response(self, prompt: str) -> Response:
        def generate():
            for token in self.model.stream_generate(prompt):
                yield token

        return Response(stream_with_context(generate()), mimetype='text/plain')

    def add_to_knowledge_base(self, prompt: str, response: str):
        kb = self.load_knowledge_base()
        kb[prompt] = response
        self.save_knowledge_base(kb)
        logging.info("Respuesta guardada en base de conocimiento.")


def configure_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')