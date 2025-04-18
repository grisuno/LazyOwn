import os
import json
import time
import logging
import requests
import argparse
from rich.console import Console
from rich.markdown import Markdown

# Configuración de logging
logging.basicConfig(filename='code_analyzer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEEPSEEK_API_URL = "http://localhost:11434/api/generate"
DEEPSEEK_MODEL = "deepseek-r1:1.5b"

console = Console()

# Lista de extensiones de archivos a monitorear
SOURCE_FILE_EXTENSIONS = [".py", ".c", ".go", ".rs"]

class CodeAnalyzer:
    """
    Analiza el código fuente en un directorio y sus subdirectorios.
    """
    def __init__(self, mode='console'):
        self.mode = mode
        self.processed_files = set()  # Rastrear archivos procesados para evitar duplicados

    def analyze_directory(self, directory):
        """
        Analiza recursivamente todos los archivos de código fuente en el directorio especificado.
        """
        for root, _, files in os.walk(directory):
            for file_name in files:
                if any(file_name.endswith(ext) for ext in SOURCE_FILE_EXTENSIONS):
                    file_path = os.path.join(root, file_name)
                    if file_path not in self.processed_files:
                        self.processed_files.add(file_path)
                        self.analyze_code_file(file_path)

    def analyze_code_file(self, file_path):
        """
        Analiza el contenido del archivo de código fuente.
        """
        try:
            with open(file_path, 'r') as file:
                code_content = file.read()
                logging.info(f"Analyzing code in {file_path}")
                if self.mode == 'console':
                    console.print(f"Analyzing code in {file_path}")
                analyze_with_deepseek(code_content, file_path, self.mode)
        except Exception as e:
            logging.error(f"Error reading code file {file_path}: {e}")
            if self.mode == 'console':
                console.print(f"Error reading code file {file_path}")

def analyze_with_deepseek(code_content, file_path, mode='console'):
    """
    Envía el contenido del código a DeepSeek para su análisis.
    Devuelve la respuesta del modelo en fragmentos.
    """
    try:
        console.print("Sending code content to DeepSeek for analysis...")
        response = requests.post(
            DEEPSEEK_API_URL,
            json={
                "model": DEEPSEEK_MODEL,
                "prompt": f"""
                Analyze the following code and suggest improvements for each function.
                Respond with a JSON containing:
                - 'function_name': the name of the function.
                - 'original_function': the original code of the function.
                - 'improved_function': the improved code of the function.
                - 'explanation': a brief explanation of the improvements.

                Code:
                {code_content}
                """,
                "stream": True
            },
            timeout=60,
            stream=True
        )

        if response.status_code == 200:
            full_response = ""
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    try:
                        json_chunk = json.loads(chunk.decode('utf-8'))
                        chunk_response = json_chunk.get("response", "")
                        full_response += chunk_response
                        if mode == 'console':
                            console.print(chunk_response, end="")
                    except json.JSONDecodeError as e:
                        logging.error(f"Error decoding JSON: {e}")

            if mode == 'console':
                rich_markdown = Markdown(full_response)
                os.system('clear')
                console.print(rich_markdown)
            logging.info(f"DeepSeek Analysis Results:\n{full_response}")

            # Guardar los resultados en archivos JSON
            save_results_to_json(full_response, file_path)
        else:
            logging.error(f"Error communicating with DeepSeek API: {response.status_code}")
            console.print("Error communicating with DeepSeek API")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in request to DeepSeek: {e}")
        console.print("Error in request to DeepSeek")

def save_results_to_json(results, file_path):
    """
    Guarda los resultados del análisis en archivos JSON.
    """
    try:
        results_data = json.loads(results)
        os.makedirs("results", exist_ok=True)
        os.makedirs("code_snippets", exist_ok=True)

        for result in results_data:
            function_name = result.get("function_name")
            original_function = result.get("original_function")
            improved_function = result.get("improved_function")
            explanation = result.get("explanation")

            # Guardar el código original y mejorado en archivos de texto
            original_file_path = f"code_snippets/{os.path.basename(file_path)}_{function_name}_original.txt"
            improved_file_path = f"code_snippets/{os.path.basename(file_path)}_{function_name}_improved.txt"

            with open(original_file_path, 'w') as original_file:
                original_file.write(original_function)

            with open(improved_file_path, 'w') as improved_file:
                improved_file.write(improved_function)

            json_data = {
                "id": str(time.time()),
                "file": os.path.basename(file_path),
                "name": function_name,
                "original_function": original_file_path,
                "new_function": improved_file_path,
                "approval": False,
                "score": None,
                "created": time.strftime("%Y-%m-%d %H:%M:%S"),
                "modified": time.strftime("%Y-%m-%d %H:%M:%S"),
                "explanation": explanation
            }

            json_file_path = f"results/{os.path.basename(file_path)}_{function_name}.json"
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
            logging.info(f"Results saved to {json_file_path}")
    except Exception as e:
        logging.error(f"Error saving results to JSON: {e}")

def start_analysis(code_dir='/path/to/code', mode='console'):
    """
    Inicia el análisis del directorio de código especificado.
    """
    console.print(f"Starting code analysis in {code_dir}...")
    analyzer = CodeAnalyzer(mode)
    analyzer.analyze_directory(code_dir)

def parse_args():
    parser = argparse.ArgumentParser(description='Code Analyzer Bot')
    parser.add_argument('--mode', type=str, choices=['console', 'web'], default='console', help='Output mode: console or web')
    parser.add_argument('--code-dir', type=str, default='/path/to/code', help='Directory to analyze for code files')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    start_analysis(code_dir=args.code_dir, mode=args.mode)
