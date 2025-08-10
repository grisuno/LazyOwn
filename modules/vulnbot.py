# vulnbot.py
import os
import json
import logging
from typing import Dict, Generator
from flask import Response, stream_with_context
from ai_model import AIModel, GroqModel, OllamaModel

BANNER = """
[*] Iniciando: LazyOwn GPT One Liner Cli Assistant [;,;]
"""

class VulnBotCLI:
    def __init__(self, provider: str = "groq", mode: str = "console", debug: bool = False):
        self.provider = provider
        self.mode = mode
        self.debug = debug
        self.model = self._load_model()
        self.script_dir = os.getcwd()
        self.knowledge_base_file = f"{self.script_dir}/knowledge_base_vuln.json"
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