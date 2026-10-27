# vulnbot.py
import json
import logging
import os

from flask import Response, stream_with_context

try:
    from agent_runner import AgentRunner
    from ai_model import AIModel
    from llm_factory import BACKEND_GROQ, BACKEND_OLLAMA, get_llm_backend
    from llm_orchestrator import complete_with_fallback, is_error_reply
except ImportError:
    from modules.agent_runner import AgentRunner
    from modules.ai_model import AIModel
    from modules.llm_factory import BACKEND_GROQ, BACKEND_OLLAMA, get_llm_backend
    from modules.llm_orchestrator import complete_with_fallback, is_error_reply

try:
    from .logging_config import configure, get_logger
except ImportError:
    from logging_config import configure, get_logger

logger = get_logger(__name__)

_PROVIDER_ALIAS = {
    "groq": BACKEND_GROQ,
    "deepseek": BACKEND_OLLAMA,
    "ollama": BACKEND_OLLAMA,
}

BANNER = """
[*] Starting: LazyOwn GPT One Liner CLI Assistant [;,;]
"""


class VulnBotCLI:
    def __init__(
        self, provider: str = "groq", mode: str = "console", debug: bool = False, script_path: str = "lazyown.py"
    ):
        self.provider = provider
        self.mode = mode
        self.debug = debug
        self.script_dir = os.getcwd()
        self.knowledge_base_file = f"{self.script_dir}/knowledge_base_vuln.json"

        level = logging.DEBUG if debug else logging.INFO
        configure(level=level, console=True, file=False)

        self.model = self._load_model()

        self._setup_agent(script_path)

    def _load_model(self) -> AIModel:
        """Instantiate the LLM backend mapped to ``self.provider``.

        Returns:
            A configured :class:`AIModel` instance, or ``None`` when the
            resolved backend cannot be constructed (missing, placeholder
            or exhausted key); the orchestrator chain then answers.
        """
        backend = _PROVIDER_ALIAS.get(self.provider, self.provider)
        try:
            return get_llm_backend(backend=backend)
        except Exception as exc:
            logger.warning(f"Primary backend '{self.provider}' unavailable ({exc}); using the orchestrator chain.")
            return None

    def _complete_with_fallback(self, prompt: str):
        """Answer a prompt through the primary model or the orchestrator chain.

        Args:
            prompt: Fully rendered prompt text.

        Returns:
            The primary answer, or the notice-prefixed chain answer; the
            legacy error string when the chain is exhausted too.
        """
        text = ""
        if self.model is not None:
            try:
                text = str(self.model.generate(prompt) or "")
            except Exception as exc:
                text = f"Error from primary backend: {exc}"
        if is_error_reply(text):
            result = complete_with_fallback(prompt, max_tokens=4096)
            if result.ok:
                return result.display_text
            return text if text else result.text
        return text

    def _stream_with_fallback(self, prompt: str):
        """Stream a prompt with chain failover on primary failure.

        Args:
            prompt: Fully rendered prompt text.

        Yields:
            Text chunks from the primary stream or the chain answer.
        """
        collected: list[str] = []
        failed = False
        if self.model is not None:
            try:
                for chunk in self.model.stream_generate(prompt):
                    text = str(chunk or "")
                    if is_error_reply(text):
                        failed = True
                        break
                    collected.append(text)
            except Exception:
                failed = True
        if failed or (self.model is None and not collected):
            result = complete_with_fallback(prompt, max_tokens=4096)
            if result.ok:
                yield result.display_text
            elif collected:
                yield "".join(collected)
            else:
                yield result.text
        else:
            yield "".join(collected)

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
            with open(path, "r", encoding="utf-8") as f:
                return f.read()

        def edit_file(path: str, content: str, old_text: str = None) -> str:
            """Crea o edita un archivo"""
            if old_text and os.path.exists(path):
                current = read_file(path)
                content = current.replace(old_text, content)

            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
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
                if isinstance(attr, type) and "cmd" in attr.__module__:
                    try:
                        instance = attr()
                    except (TypeError, ValueError):
                        continue
                    for method_name in dir(instance):
                        if method_name.startswith("do_") and method_name != "do_exit":
                            method = getattr(instance, method_name)
                            self.agent.register_tool_from_instance(method)
                    logger.info(f"Tools from {script_path} loaded")
                    break
        except Exception as e:
            logger.warning(f"Could not load external tools: {e}")

    def _stream_agent_response(self, prompt: str) -> Response:
        """Versión streaming para web (simplificada)"""

        def generate():
            # En modo web, usamos generación directa sin herramientas
            yield from self.model.stream_generate(prompt)

        return Response(stream_with_context(generate()), mimetype="text/plain")

    def load_knowledge_base(self) -> list | dict:
        """Load the knowledge base in any known shape.

        Returns:
            The canonical list of ``{"prompt", "response"}`` records, the
            legacy dict mapping, or an empty list on any read error.
        """
        try:
            with open(self.knowledge_base_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return []
        if isinstance(data, (list, dict)):
            return data
        return []

    def save_knowledge_base(self, kb: list | dict) -> None:
        with open(self.knowledge_base_file, "w", encoding="utf-8") as f:
            json.dump(kb, f, indent=4)

    def get_relevant_knowledge(self, prompt: str) -> str:
        """Return knowledge responses whose text shares keywords with the prompt.

        Args:
            prompt: Query used to select relevant records.

        Returns:
            Newline-joined matching responses; empty when nothing matches.
        """
        kb = self.load_knowledge_base()
        lowered = prompt.lower()
        keywords = [word for word in lowered.split() if len(word) > 2]
        matches: list[str] = []
        if isinstance(kb, dict):
            candidates = ({"prompt": key, "response": value} for key, value in kb.items())
        else:
            candidates = (entry for entry in kb if isinstance(entry, dict))
        for entry in candidates:
            text = f"{entry.get('prompt', '')} {entry.get('response', '')}".lower()
            if keywords and any(word in text for word in keywords):
                matches.append(str(entry.get("response", "")))
        return "\n".join(matches)

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
            with open("event_config.json", "r") as f:
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
            return self._complete_with_fallback(prompt)

    def stream_response(self, prompt: str) -> Response:
        def generate():
            yield from self._stream_with_fallback(prompt)

        return Response(stream_with_context(generate()), mimetype="text/plain")

    def add_to_knowledge_base(self, prompt: str, response: str):
        """Append a prompt/response record in the canonical list format.

        Args:
            prompt: Operator prompt that produced the response.
            response: Model response to remember.
        """
        kb = self.load_knowledge_base()
        if isinstance(kb, dict):
            records = [{"prompt": key, "response": value} for key, value in kb.items()]
        elif isinstance(kb, list):
            records = [entry for entry in kb if isinstance(entry, dict)]
        else:
            records = []
        records.append({"prompt": prompt, "response": response})
        self.save_knowledge_base(records)
        logging.info("Respuesta guardada en base de conocimiento.")
