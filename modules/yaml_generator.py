# yaml_generator.py
import json
import os
import re
import sys
from typing import Dict, Optional
from ai_model import AIModel, GroqModel, OllamaModel


class YAMLPromptGenerator:
    def __init__(self, provider: str = "groq", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.payload_file = "../payload.json"
        self.payload_data = self.load_payload()
        self.model = self._load_model()

    def load_payload(self) -> Dict:
        """Carga las variables desde payload.json"""
        if not os.path.exists(self.payload_file):
            raise FileNotFoundError(f"No se encontró {self.payload_file} en la raíz del proyecto.")
        with open(self.payload_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_model(self) -> AIModel:
        if self.provider == "groq":
            if not self.api_key:
                raise ValueError("GROQ_API_KEY no está definida ni en argumento ni en variables de entorno.")
            return GroqModel(api_key=self.api_key)
        elif self.provider == "deepseek":
            return OllamaModel(model="deepseek-r1:1.5b")
        else:
            raise ValueError(f"Proveedor no soportado: {self.provider}")

    def generate_prompt(self, user_request: str) -> str:
        """Genera el prompt para la IA en inglés"""
        available_params = list(self.payload_data.keys())

        return f"""
You are a YAML configuration generator for the LazyAddons system in LazyOwn RedTeam Framework.
Create a complete, valid YAML addon configuration based on the user's request.
Use only the following available parameters (from payload.json). Do NOT hardcode values. Use mustache-style {{}} placeholders.

Available parameters:
{', '.join(available_params)}

Rules:
- Output ONLY a single YAML block wrapped in ```yaml ... ```
- Use `enabled: true`
- Use `install_type: git` if repo is GitHub
- For `execute_command`, use {{var}} syntax for dynamic values
- If the tool needs to be installed, include `install_command`
- Always include `repo_url`, `install_path`, and `execute_command`
- For post-exploitation tools, you can include `upload_file`, `remote_command`, `download_file`
- Use realistic paths: `external/.exploit/toolname`, `sessions/output.txt`, etc.

User request:
{user_request}

Output format:
```yaml
name: "shortname"
description: "Brief description"
author: "LazyOwn RedTeam"
version: "1.0"
enabled: true
params:
  - name: "param1"
    type: string
    required: true
    description: "Description of param1"
tool:
  name: "Full Tool Name"
  repo_url: "https://github.com/user/repo.git"
  install_path: "external/.exploit/toolname"
  install_command: "make && make install"
  execute_command: "python run.py --target {{url}} --output sessions/out.txt"
  ```
  """

    def extract_yaml_from_markdown(self, text: str) -> str:
        """Extrae el primer bloque YAML entre ```yaml y ```"""
        pattern = r"```yaml\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            raise ValueError("No se encontró un bloque YAML válido en la respuesta de la IA.")

    def create_yaml_addon(self, user_request: str, output_dir: str = "lazyaddons") -> str:
        """Genera el YAML y lo guarda en disco"""
        full_prompt = self.generate_prompt(user_request)
        print("[*] Enviando solicitud a la IA...")
        response = self.model.generate(full_prompt)

        try:
            yaml_content = self.extract_yaml_from_markdown(response)
        except ValueError as e:
            print(f"[E] Error al extraer YAML: {e}")
            print("[R] Respuesta completa de la IA:")
            print(response)
            sys.exit(1)

        # Generar nombre seguro
        name_line = yaml_content.split("\n")[0]
        if name_line.startswith("name:"):
            name = name_line.split(":", 1)[1].strip().strip('"').strip("'")
        else:
            name = "generated_tool"

        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"{name}.yaml")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(yaml_content + "\n")

        print(f"[+] YAML generado y guardado en: {filename}")
        return filename

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generador de YAMLs para LazyAddons usando IA")
    parser.add_argument("--request", type=str, help="Descripción de la herramienta a generar (ej: 'Herramienta para explotar Log4j')")
    parser.add_argument("--provider", choices=["groq", "deepseek"], default="groq", help="Modelo a usar")
    parser.add_argument("--api-key", type=str, help="API Key (opcional, si no está en env)")
    parser.add_argument("--output", type=str, default="../lazyaddons", help="Directorio de salida")

    args = parser.parse_args()

    generator = YAMLPromptGenerator(provider=args.provider, api_key=args.api_key)
    generator.create_yaml_addon(user_request=args.request, output_dir=args.output)

if __name__ == "__main__":
    main()
