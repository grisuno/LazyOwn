#!/usr/bin/env python3
"""
lazyaddon_creator.py
====================
Genera automáticamente un addon YAML de LazyOwn a partir de una URL de GitHub.

Uso:
    cd lazyaddons
    python3 ../modules/lazyaddon_creator.py https://github.com/user/repo

Requiere:
    - requests (pip install requests)
    - PyYAML
    - GROQ_API_KEY u Ollama corriendo (para el módulo llm_client)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import textwrap
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import yaml

# ── Ajustar sys.path para importar llm_client desde modules/ ───────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.llm_client import LLMClient  # noqa: E402

# ── Configuración ──────────────────────────────────────────────────────────────
GITHUB_API = "https://api.github.com/repos"
LAZYADDONS_DIR = PROJECT_ROOT / "lazyaddons"
DEFAULT_TIMEOUT = 30


# ── GitHub scraping helpers ────────────────────────────────────────────────────

def parse_github_url(url: str) -> tuple[str, str]:
    """Extrae (owner, repo) de una URL de GitHub."""
    parsed = urllib.parse.urlparse(url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError(f"URL inválida: {url}")
    return parts[0], parts[1]


def github_api_get(owner: str, repo: str, endpoint: str = "") -> dict:
    """GET a la API pública de GitHub (sin auth, rate-limit 60/hr)."""
    url = f"{GITHUB_API}/{owner}/{repo}"
    if endpoint:
        url = f"{url}/{endpoint}"
    resp = requests.get(url, timeout=DEFAULT_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fetch_repo_metadata(owner: str, repo: str) -> dict:
    """Devuelve metadata básica del repo."""
    return github_api_get(owner, repo)


def fetch_readme(owner: str, repo: str) -> str:
    """Descarga y decodifica el README."""
    try:
        data = github_api_get(owner, repo, "readme")
        content = data.get("content", "")
        if content:
            return base64.b64decode(content).decode("utf-8", errors="ignore")
    except Exception as exc:
        print(f"[!] No se pudo obtener README: {exc}")
    return ""


def fetch_root_files(owner: str, repo: str) -> List[str]:
    """Lista nombres de archivos en el directorio raíz."""
    try:
        data = github_api_get(owner, repo, "contents")
        if isinstance(data, list):
            return [item["name"] for item in data if item.get("type") == "file"]
    except Exception as exc:
        print(f"[!] No se pudo listar root files: {exc}")
    return []


# ── Prompt engineering ─────────────────────────────────────────────────────────

def build_llm_prompt(meta: dict, readme: str, root_files: List[str]) -> str:
    """Construye el prompt para el LLM."""
    name = meta.get("name", "unknown")
    owner = meta.get("owner", {}).get("login", "unknown")
    description = meta.get("description", "")
    language = meta.get("language", "")
    topics = ", ".join(meta.get("topics", []))
    readme_snippet = readme[:4000]
    root_files_str = ", ".join(root_files) if root_files else "N/A"

    prompt = textwrap.dedent(f"""\
        You are a penetration testing tool integration expert.
        Given the following GitHub repository metadata, infer how to install and run
        this tool inside the LazyOwn red team framework.

        Repository metadata:
        - Name: {name}
        - Owner: {owner}
        - Description: {description}
        - Primary language: {language}
        - Topics: {topics}
        - Root files: {root_files_str}
        - README excerpt (first 4000 chars):
        {readme_snippet}

        LazyOwn addons are YAML files that declaratively register a GitHub tool as a
        shell command. Each addon has:
        - name: short CLI command (lowercase, no spaces)
        - description: what the tool does (concise, red-team focused)
        - author: repo owner or author name
        - version: "1.0"
        - tool block: name, repo_url, install_path, install_command, execute_command
        - params: list of arguments like {{rhost}}, {{lhost}}, {{url}}, {{domain}}
        - Optional C2 fields for post-exploitation:
            upload_file, remote_command, download_file, lazycommand

        Rules:
        1. If the tool is a post-exploitation payload (shellcode loader, implant, DLL
           injector, EDR evasion, etc.), populate the C2 fields.
        2. install_command can be empty string "" if no build is needed.
        3. execute_command must use the PRIMARY/common usage of the tool.
        4. Use standard pentest placeholders: {{rhost}}, {{lhost}}, {{lport}}, {{url}},
           {{domain}}, {{user}}, {{pass}}, {{wordlist}}, {{target}}.
        5. install_path should be "external/.exploit/<repo_name>".
        6. Return ONLY a valid JSON object, no markdown, no explanation, no backticks.

        JSON schema:
        {{
          "name": "shortname",
          "description": "...",
          "author": "...",
          "version": "1.0",
          "install_command": "...",
          "execute_command": "...",
          "params": [
            {{"name": "rhost", "type": "string", "required": true, "description": "..."}}
          ],
          "c2_upload_file": "",
          "c2_remote_command": "",
          "c2_download_file": "",
          "c2_lazycommand": ""
        }}
    """)
    return prompt


def extract_json_from_response(text: str) -> Optional[dict]:
    """Extrae el primer bloque JSON de una respuesta de LLM."""
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    return None


# ── Heurísticas locales (fallback si no hay LLM) ───────────────────────────────

def heuristic_install_command(root_files: List[str], language: str) -> str:
    """Infiere un install_command básico a partir de los archivos raíz."""
    if "Makefile" in root_files or "makefile" in root_files:
        return "make"
    if "go.mod" in root_files or (language == "Go" and any(f.endswith(".go") for f in root_files)):
        return "go build ."
    if "setup.py" in root_files or "pyproject.toml" in root_files:
        return "pip install ."
    if "requirements.txt" in root_files:
        return "pip install -r requirements.txt"
    if "Cargo.toml" in root_files:
        return "cargo build --release"
    if "package.json" in root_files:
        return "npm install"
    if "CMakeLists.txt" in root_files:
        return "mkdir build && cd build && cmake .. && make"
    return ""


def heuristic_execute_command(name: str, root_files: List[str], language: str) -> str:
    """Infiere un execute_command básico."""
    # Buscar binario con el nombre del repo
    if name in root_files:
        return f"./{name}"
    # Python
    if language == "Python":
        candidates = [f for f in root_files if f.endswith(".py") and not f.startswith("test_")]
        if candidates:
            return f"python3 {candidates[0]}"
    # Go
    if language == "Go":
        return f"./{name}"
    # Node
    if language == "JavaScript":
        if "index.js" in root_files:
            return "node index.js"
        candidates = [f for f in root_files if f.endswith(".js")]
        if candidates:
            return f"node {candidates[0]}"
    # Ruby
    if language == "Ruby":
        candidates = [f for f in root_files if f.endswith(".rb")]
        if candidates:
            return f"ruby {candidates[0]}"
    # Shell
    if any(f.endswith(".sh") for f in root_files):
        candidates = [f for f in root_files if f.endswith(".sh")]
        if candidates:
            return f"bash {candidates[0]}"
    # Fallback genérico
    return f"./{name}"


def heuristic_params(name: str, readme: str, root_files: List[str]) -> List[dict]:
    """Infiere parámetros comunes basándose en el nombre y README."""
    params = []
    readme_lower = readme.lower()

    # Detección simple de placeholders mencionados
    if "target" in readme_lower or "-t " in readme_lower:
        params.append({"name": "target", "type": "string", "required": True, "description": "Target host or IP"})
    elif "rhost" in readme_lower or "-r " in readme_lower:
        params.append({"name": "rhost", "type": "string", "required": True, "description": "Remote target IP"})

    if "url" in readme_lower or "-u " in readme_lower or "http" in readme_lower:
        params.append({"name": "url", "type": "string", "required": True, "description": "Target URL"})

    if "domain" in readme_lower or "-d " in readme_lower:
        params.append({"name": "domain", "type": "string", "required": True, "description": "Target domain"})

    if "lhost" in readme_lower:
        params.append({"name": "lhost", "type": "string", "required": False, "description": "Local listener IP"})
    if "lport" in readme_lower:
        params.append({"name": "lport", "type": "string", "required": False, "description": "Local listener port"})

    if "wordlist" in readme_lower or "-w " in readme_lower:
        params.append({"name": "wordlist", "type": "string", "required": False, "description": "Path to wordlist"})

    if not params:
        params.append({"name": "target", "type": "string", "required": True, "description": "Target to attack"})

    return params


def fallback_yaml_data(meta: dict, readme: str, root_files: List[str]) -> dict:
    """Genera datos de addon usando solo heurísticas locales (sin LLM)."""
    name = meta.get("name", "unknown")
    owner = meta.get("owner", {}).get("login", "unknown")
    description = meta.get("description", "")
    language = meta.get("language", "")

    return {
        "name": name,
        "description": description or f"Auto-generated addon for {name}",
        "author": owner,
        "version": "1.0",
        "install_command": heuristic_install_command(root_files, language),
        "execute_command": heuristic_execute_command(name, root_files, language),
        "params": heuristic_params(name, readme, root_files),
        "c2_upload_file": "",
        "c2_remote_command": "",
        "c2_download_file": "",
        "c2_lazycommand": ""
    }


# ── YAML generation ────────────────────────────────────────────────────────────

def build_yaml(data: dict, repo_url: str) -> dict:
    """Construye la estructura de dict que representa el addon YAML."""
    name = data.get("name", "unnamed").lower().replace(" ", "_").replace("-", "_")
    if not name:
        name = "unnamed"

    tool_block: Dict[str, Any] = {
        "name": data.get("name", name),
        "repo_url": repo_url,
        "install_path": f"external/.exploit/{name}",
    }

    install_cmd = data.get("install_command", "")
    if install_cmd and install_cmd.strip():
        tool_block["install_command"] = install_cmd.strip()

    tool_block["execute_command"] = data.get("execute_command", "").strip()

    # C2 features
    for field in ("upload_file", "remote_command", "download_file", "lazycommand"):
        key = f"c2_{field}"
        if key in data and data[key] and str(data[key]).strip():
            tool_block[field] = str(data[key]).strip()

    addon = {
        "name": name,
        "description": data.get("description", "No description provided."),
        "author": data.get("author", "Unknown"),
        "version": data.get("version", "1.0"),
        "enabled": True,
        "params": data.get("params", []),
        "tool": tool_block,
    }
    return addon


def save_yaml(addon: dict, output_dir: Path) -> Path:
    """Guarda el dict como archivo YAML en output_dir."""
    filename = f"{addon['name']}.yaml"
    filepath = output_dir / filename

    # Evitar sobrescribir sin confirmar
    if filepath.exists():
        print(f"[!] Ya existe {filepath}")
        override = input("    ¿Sobrescribir? [y/N]: ").strip().lower()
        if override != "y":
            print("[*] Cancelado.")
            sys.exit(0)

    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(addon, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return filepath


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera un LazyAddon YAML desde una URL de GitHub usando IA."
    )
    parser.add_argument("url", help="URL del repositorio GitHub")
    parser.add_argument(
        "--provider",
        default="auto",
        choices=["groq", "ollama", "auto"],
        help="Proveedor de LLM (default: auto)",
    )
    parser.add_argument(
        "--model", default=None, help="Modelo específico del proveedor"
    )
    parser.add_argument(
        "--output",
        default=str(LAZYADDONS_DIR),
        help=f"Directorio de salida (default: {LAZYADDONS_DIR})",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("GROQ_API_KEY", ""),
        help="Groq API key (default: GROQ_API_KEY env var)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Imprime el YAML por pantalla sin escribirlo",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Usa una respuesta mock del LLM para testing (sin llamar a la API)",
    )
    args = parser.parse_args()

    # 1. Parsear URL
    try:
        owner, repo = parse_github_url(args.url)
    except ValueError as exc:
        print(f"[E] {exc}")
        sys.exit(1)

    print(f"[*] Analizando {owner}/{repo} ...")

    # 2. Obtener metadata
    try:
        meta = fetch_repo_metadata(owner, repo)
    except requests.HTTPError as exc:
        print(f"[E] Error al contactar GitHub API: {exc}")
        sys.exit(1)

    readme = fetch_readme(owner, repo)
    root_files = fetch_root_files(owner, repo)

    print(f"    README: {len(readme)} chars")
    print(f"    Root files: {len(root_files)} found")

    # 3. Consultar LLM
    prompt = build_llm_prompt(meta, readme, root_files)
    print(f"[*] Consultando LLM (provider={args.provider}) ...")

    if args.mock:
        print("[*] MODO MOCK: usando heurísticas locales (sin LLM)")
        parsed = fallback_yaml_data(meta, readme, root_files)
    else:
        client = LLMClient(api_key=args.api_key)
        response = client.ask(
            prompt,
            provider=args.provider,
            model=args.model,
            system="You are a cybersecurity tool integration assistant. Return ONLY valid JSON.",
            temperature=0.3,
        )

        if response.startswith("[LLM error]"):
            print(f"[!] Falló la consulta al LLM: {response}")
            print("[*] Usando heurísticas locales como fallback ...")
            parsed = fallback_yaml_data(meta, readme, root_files)
        else:
            # 4. Extraer JSON
            parsed = extract_json_from_response(response)
            if not parsed:
                print("[!] No se pudo extraer JSON válido de la respuesta del LLM.")
                print("--- Respuesta raw ---")
                print(response)
                print("[*] Usando heurísticas locales como fallback ...")
                parsed = fallback_yaml_data(meta, readme, root_files)

    print(f"[*] JSON recibido del LLM:")
    print(json.dumps(parsed, indent=2, ensure_ascii=False))

    # 5. Construir YAML
    repo_url = meta.get("html_url", args.url)
    addon = build_yaml(parsed, repo_url)

    # 6. Guardar o mostrar
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print("\n--- YAML generado ---")
        print(yaml.dump(addon, default_flow_style=False, sort_keys=False, allow_unicode=True))
    else:
        filepath = save_yaml(addon, output_dir)
        print(f"\n[✓] Addon creado: {filepath}")


if __name__ == "__main__":
    main()
