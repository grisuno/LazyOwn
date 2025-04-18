#!/usr/bin/env python3

"""
log_monitor_bot_v2_monolithic.py

Author: Your Name
Email: youremail@example.com
Creation Date: 14/04/2025 
License: GPL v3

Description: Real-time log monitoring bot for Linux systems (Monolithic Test Version).
             Monitors logs, performs basic parsing, uses DeepSeek for analysis per line,
             and stores structured results locally.
"""

import time
import json
import logging
import os
import requests
import argparse
import re
import socket
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

# --- Configuration ---
LOG_FILE = 'log_monitor_bot.log'
OUTPUT_EVENTS_FILE = 'processed_events.jsonl' # File to store structured results
DEEPSEEK_API_URL = "http://localhost:11434/api/generate"
DEEPSEEK_MODEL = "deepseek-r1:1.5b" # Asegúrate que este modelo esté disponible en tu Ollama
REQUEST_TIMEOUT = 60 # Segundos
MONITOR_INTERVAL = 1.0 # Segundos entre chequeos de watchdog

# Lista de archivos de log conocidos (pueden ser rutas relativas al log_dir o absolutas)
# Se recomienda usar rutas completas si no están directamente en log_dir
TEXT_LOG_FILES_PATTERNS = [
    r"auth\.log.*",          # SSH y autenticación (incluye rotados como .1, .gz)
    r"syslog.*",            # Logs generales del sistema
    r"kern\.log.*",          # Logs del kernel
    r"nginx[/\\]access\.log.*", # Nginx access logs (usa [/\\] para compatibilidad OS)
    r"nginx[/\\]error\.log.*",  # Nginx error logs
    r"apache2[/\\]access\.log.*",# Apache access logs
    r"apache2[/\\]error\.log.*", # Apache error logs
    r"dpkg\.log.*",          # Logs del gestor de paquetes
    r"boot\.log.*",          # Logs de arranque
    # Añade más patrones aquí si es necesario
]
# --- End Configuration ---

# Logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()
HOSTNAME = socket.gethostname()

# Diccionario para mantener la última posición leída en cada archivo
file_positions = {}

def simple_parse_log_line(line, file_path):
    """
    Intenta extraer información básica de una línea de log.
    Esto es MUY básico, idealmente se usarían regex más específicos por tipo de log.
    """
    log_type = "unknown"
    base_name = os.path.basename(file_path)

    # Intenta identificar el tipo de log basado en el nombre del archivo
    if re.match(r"auth\.log.*", base_name):
        log_type = "auth"
    elif re.match(r"syslog.*", base_name):
        log_type = "syslog"
    elif re.match(r"nginx.*access\.log.*", base_name):
        log_type = "nginx_access"
    elif re.match(r"nginx.*error\.log.*", base_name):
        log_type = "nginx_error"
    elif re.match(r"apache2.*access\.log.*", base_name):
        log_type = "apache_access"
    elif re.match(r"apache2.*error\.log.*", base_name):
        log_type = "apache_error"
    # Añadir más tipos si es necesario

    # Intenta extraer timestamp (esto es muy genérico, puede fallar)
    timestamp_iso = datetime.now().isoformat() # Fallback
    match = re.match(r"^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})", line) # Formato Syslog común
    if match:
        # Necesitaría más lógica para convertir este timestamp parcial a uno completo con año
        pass # Por ahora, usamos el timestamp de procesamiento

    return {
        "timestamp_processed": timestamp_iso,
        "hostname": HOSTNAME,
        "log_source_path": file_path,
        "log_type": log_type,
        "raw_log": line.strip(),
    }

def store_event(event_data):
    """
    Almacena el evento procesado (diccionario Python) como una línea JSON
    en el archivo de salida.
    """
    try:
        with open(OUTPUT_EVENTS_FILE, 'a') as f:
            json.dump(event_data, f)
            f.write('\n')
        logging.info(f"Event stored: {event_data.get('raw_log', '')[:100]}...") # Loguea un snippet
    except Exception as e:
        logging.error(f"Error storing event to {OUTPUT_EVENTS_FILE}: {e}")
        console.print(f"[bold red]Error storing event:[/bold red] {e}")

def analyze_with_deepseek(log_entry_data):
    """
    Sends a single log entry to DeepSeek for analysis.
    Returns the analysis result as a Python dictionary or None if error.
    """
    raw_log = log_entry_data.get("raw_log", "No raw log provided")
    prompt = f"""
    Analyze the following single log entry and determine if it indicates suspicious activity related to system security.
    Respond ONLY with a valid JSON object containing:
    - "suspicious": boolean (true if suspicious, false otherwise).
    - "reason": string (a brief explanation ONLY if suspicious, otherwise empty string or null).
    - "severity": string (e.g., "low", "medium", "high", "critical" ONLY if suspicious, otherwise null).
    - "confidence": float (from 0.0 to 1.0, your confidence in the suspicious assessment, otherwise null).

    Log entry:
    ```{raw_log}```

    JSON Response:
    """

    console.print(f"[cyan]Analyzing log entry:[/cyan] {raw_log[:150]}...") # Muestra inicio de análisis
    logging.info(f"Sending to DeepSeek: {raw_log}")

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            json={
                "model": DEEPSEEK_MODEL,
                "prompt": prompt,
                "stream": False, # No necesitamos stream para una respuesta JSON completa
                "format": "json" # Pedimos explícitamente JSON si el modelo/API lo soporta
            },
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status() # Lanza excepción para errores HTTP 4xx/5xx

        response_text = response.text
        logging.debug(f"Raw DeepSeek response: {response_text}")

        # Ollama a veces envuelve la respuesta en una estructura, intentamos extraer el JSON
        try:
            # Intento 1: Asumir que la respuesta directa es el JSON esperado
            analysis_result = json.loads(response_text)
            if 'response' in analysis_result and isinstance(analysis_result['response'], str):
                 # Intento 2: Ollama a veces devuelve el JSON como un string dentro de 'response'
                try:
                   analysis_result = json.loads(analysis_result['response'])
                except json.JSONDecodeError:
                   logging.error(f"Failed to decode JSON string within 'response': {analysis_result['response']}")
                   console.print(f"[bold red]Error:[/bold red] DeepSeek response format unexpected (JSON string decode).")
                   return None

        except json.JSONDecodeError:
             # Intento 3: Fallback por si devuelve texto plano que *contiene* un JSON
             match = re.search(r'\{.*\}', response_text, re.DOTALL)
             if match:
                 try:
                     analysis_result = json.loads(match.group(0))
                 except json.JSONDecodeError as e:
                     logging.error(f"Failed to decode JSON extracted from text: {match.group(0)} - Error: {e}")
                     console.print(f"[bold red]Error:[/bold red] Could not decode JSON from DeepSeek response.")
                     return None
             else:
                logging.error(f"No valid JSON found in DeepSeek response: {response_text}")
                console.print(f"[bold red]Error:[/bold red] DeepSeek response was not valid JSON.")
                return None


        # Validación básica del JSON esperado
        if not all(k in analysis_result for k in ["suspicious", "reason", "severity", "confidence"]):
             logging.warning(f"DeepSeek JSON response missing expected keys: {analysis_result}")
             # Podrías intentar rellenar con valores por defecto o devolver None
             return None # O manejarlo como prefieras

        logging.info(f"DeepSeek analysis successful for: {raw_log[:100]}...")
        return analysis_result

    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with DeepSeek API: {e}")
        console.print(f"[bold red]Error connecting to DeepSeek API:[/bold red] {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding DeepSeek JSON response: {e} - Response text: {response.text if 'response' in locals() else 'N/A'}")
        console.print(f"[bold red]Error decoding DeepSeek JSON:[/bold red] {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error during DeepSeek analysis: {e}")
        console.print(f"[bold red]Unexpected error during analysis:[/bold red] {e}")
        return None


class LogFileHandler(FileSystemEventHandler):
    """
    Handles file system events, reads new lines using position tracking,
    parses, analyzes, and stores them.
    """
    def __init__(self, log_dir, mode='console'):
        super().__init__()
        self.log_dir = log_dir
        self.mode = mode
        self.initialize_file_positions()

    def initialize_file_positions(self):
        """Set initial position to the end of all currently monitored files."""
        console.print("[yellow]Initializing file positions (reading to end)...[/yellow]")
        for root, _, files in os.walk(self.log_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                if self.is_monitored(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            f.seek(0, os.SEEK_END) # Ir al final del archivo
                            file_positions[file_path] = f.tell() # Guardar la posición final
                            logging.info(f"Initialized position for {file_path} at {file_positions[file_path]}")
                    except Exception as e:
                        logging.error(f"Error initializing position for {file_path}: {e}")
                        # console.print(f"[red]Error initializing {file_path}: {e}[/red]")

    def is_monitored(self, file_path):
        """Check if the file path matches any of the monitored patterns."""
        # Normaliza la ruta para comparación (opcional, pero útil)
        normalized_path = os.path.normpath(file_path)
        relative_path = os.path.relpath(normalized_path, self.log_dir)

        for pattern in TEXT_LOG_FILES_PATTERNS:
             # Intentar hacer match con la ruta relativa o el nombre base
             if re.fullmatch(pattern, relative_path) or re.fullmatch(pattern, os.path.basename(normalized_path)):
                 return True
        return False

    def process_file(self, file_path):
         """Reads new lines from a file since the last known position."""
         if not self.is_monitored(file_path):
             return # No procesar si no coincide con los patrones

         current_pos = file_positions.get(file_path, 0) # Obtener última posición o 0 si es nuevo
         try:
             # Verificar si el archivo aún existe (puede ser rotado/eliminado)
             if not os.path.exists(file_path):
                 if file_path in file_positions:
                     del file_positions[file_path]
                     logging.info(f"Monitored file {file_path} removed or rotated.")
                 return

             with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                 f.seek(current_pos) # Ir a la última posición conocida
                 new_lines = f.readlines()
                 new_pos = f.tell() # Obtener la nueva posición

             if new_pos < current_pos:
                  # El archivo probablemente fue truncado o rotado sin crear uno nuevo
                  logging.warning(f"File {file_path} possibly truncated or rotated (new_pos < current_pos). Resetting position.")
                  console.print(f"[yellow]File {file_path} possibly truncated/rotated. Reading from start.[/yellow]")
                  current_pos = 0
                  with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                      new_lines = f.readlines()
                      new_pos = f.tell()

             file_positions[file_path] = new_pos # Actualizar la posición

             if new_lines:
                 console.print(f"[green]Detected {len(new_lines)} new line(s) in {file_path}[/green]")
                 for line in new_lines:
                     if not line.strip(): # Saltar líneas vacías
                         continue

                     # 1. Parse básico
                     parsed_data = simple_parse_log_line(line, file_path)

                     # 2. Analizar con LLM
                     analysis_result = analyze_with_deepseek(parsed_data) # Pasar datos parseados

                     # 3. Combinar y almacenar
                     if analysis_result: # Solo almacenar si el análisis fue exitoso
                         event_record = {**parsed_data, "llm_analysis": analysis_result}
                         store_event(event_record)

                         # 4. Mostrar en consola (si el modo es consola)
                         if self.mode == 'console':
                             display_record(event_record)
                     else:
                         # Opcional: Almacenar incluso si el análisis falla, marcándolo
                         event_record = {**parsed_data, "llm_analysis": {"error": "Analysis failed or timed out"}}
                         store_event(event_record)
                         logging.warning(f"LLM analysis failed for log: {line.strip()}")
                         console.print(f"[yellow]LLM analysis failed for: {line.strip()[:100]}...[/yellow]")


         except FileNotFoundError:
             logging.warning(f"File not found during processing: {file_path}. Removing from tracked positions.")
             if file_path in file_positions:
                 del file_positions[file_path]
         except PermissionError:
              logging.error(f"Permission denied reading file: {file_path}.")
              console.print(f"[bold red]Permission denied reading {file_path}. Check permissions.[/bold red]")
              # Podríamos querer dejar de intentar leer este archivo
              if file_path in file_positions:
                  del file_positions[file_path] # Dejar de rastrearlo
         except Exception as e:
             logging.error(f"Error processing file {file_path}: {e}", exc_info=True)
             if self.mode == 'console':
                 console.print(f"[bold red]Error processing file {file_path}: {e}[/bold red]")


    def on_modified(self, event):
        """Triggered when a file or directory is modified."""
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_created(self, event):
        """Triggered when a file or directory is created."""
        if not event.is_directory:
             # Es un archivo nuevo, empezar a leer desde el principio (posición 0)
             # La llamada a process_file lo manejará ya que no estará en file_positions
            logging.info(f"Detected new file: {event.src_path}. Will start monitoring.")
            console.print(f"[yellow]Detected new file: {event.src_path}[/yellow]")
            self.process_file(event.src_path) # Procesarlo inmediatamente

def display_record(record):
     """Muestra un registro procesado de forma atractiva en la consola."""
     log_line = record.get('raw_log', '')
     analysis = record.get('llm_analysis', {})
     is_suspicious = analysis.get('suspicious', False)
     reason = analysis.get('reason', 'N/A')
     severity = analysis.get('severity', 'N/A')
     confidence = analysis.get('confidence', 'N/A')
     log_source = record.get('log_source_path', 'N/A')
     timestamp = record.get('timestamp_processed', 'N/A')

     color = "green"
     title = "Log Event Analysis"
     if is_suspicious:
         if severity == "high" or severity == "critical":
             color = "bold red"
             title = "[bold red]Suspicious Event Detected!"
         elif severity == "medium":
             color = "bold yellow"
             title = "[bold yellow]Suspicious Event Detected"
         else:
             color = "yellow"
             title = "[yellow]Suspicious Event Detected"


     panel_content = f"[dim]{timestamp} | Host: {record.get('hostname')} | Source: {log_source}[/dim]\n"
     panel_content += f"[bold]Raw Log:[/bold]\n{log_line}\n\n"
     panel_content += f"[bold]LLM Analysis:[/bold]\n"
     panel_content += f"  Suspicious: [bold {'red' if is_suspicious else 'green'}]{is_suspicious}[/]\n"
     if is_suspicious:
         panel_content += f"  Reason: {reason}\n"
         panel_content += f"  Severity: {severity}\n"
         panel_content += f"  Confidence: {confidence:.2f}\n"

     console.print(Panel(panel_content, title=title, border_style=color, expand=False))


def search_logs(query, file_path=OUTPUT_EVENTS_FILE):
     """
     Busca en el archivo de eventos JSONL registros que coincidan (búsqueda simple de substring).
     """
     console.print(f"\n[bold blue]Searching for '{query}' in {file_path}...[/bold blue]\n")
     found_count = 0
     try:
         with open(file_path, 'r') as f:
             for line_num, line in enumerate(f):
                 try:
                     record = json.loads(line)
                     record_str = json.dumps(record) # Convertir a string para búsqueda simple
                     if query.lower() in record_str.lower():
                         display_record(record) # Mostrar el registro completo formateado
                         found_count += 1
                 except json.JSONDecodeError:
                     console.print(f"[red]Skipping malformed JSON line {line_num + 1}[/red]")
                 except Exception as e:
                      console.print(f"[red]Error processing line {line_num + 1}: {e}[/red]")

         if found_count == 0:
             console.print(f"[yellow]No records found matching '{query}'.[/yellow]")
         else:
              console.print(f"\n[bold blue]Found {found_count} matching records.[/bold blue]")

     except FileNotFoundError:
         console.print(f"[bold red]Error:[/bold red] Event file '{file_path}' not found.")
     except Exception as e:
         console.print(f"[bold red]Error during search:[/bold red] {e}")


def start_monitoring(log_dir='/var/log', mode='console'):
    """
    Starts monitoring the specified log directory.
    """
    if not os.path.isdir(log_dir):
         console.print(f"[bold red]Error:[/bold red] Log directory '{log_dir}' not found or is not a directory.")
         return

    console.print(f"Starting log monitoring in [bold cyan]{log_dir}[/bold cyan]...")
    console.print(f"Storing processed events in [bold cyan]{OUTPUT_EVENTS_FILE}[/bold cyan]")
    console.print(f"Using LLM: [bold cyan]{DEEPSEEK_MODEL}[/bold cyan] at [bold cyan]{DEEPSEEK_API_URL}[/bold cyan]")
    console.print("Press Ctrl+C to stop.")

    event_handler = LogFileHandler(log_dir=log_dir, mode=mode)
    observer = Observer()
    # ¡Importante! Monitorizar el directorio raíz de logs
    # Watchdog detectará eventos en subdirectorios si recursive=True
    observer.schedule(event_handler, path=log_dir, recursive=True)
    observer.start()

    try:
        while True:
            # Aquí podríamos añadir chequeos periódicos si es necesario
            # Por ejemplo, verificar si los archivos monitoreados todavía existen
            # O re-escanear el directorio por si acaso watchdog pierde algo (raro)
            time.sleep(MONITOR_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Log monitoring stopped by the user.")
        console.print("\n[bold yellow]Log monitoring stopped by the user.[/bold yellow]")
    observer.join()

def parse_args():
    parser = argparse.ArgumentParser(description='Log Monitor Bot v2 (Monolithic)')
    parser.add_argument('--mode', type=str, choices=['console'], default='console', help='Output mode (currently only console)')
    parser.add_argument('--log-dir', type=str, default='/var/log', help='Directory to monitor for logs')
    parser.add_argument('--search', type=str, metavar='QUERY', help='Search the stored event log for QUERY instead of monitoring.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.search:
        search_logs(args.search)
    else:
        # Asegurarse que el directorio de logs exista antes de empezar
        if not os.path.isdir(args.log_dir):
             console.print(f"[bold red]Error:[/bold red] Log directory '{args.log_dir}' does not exist.")
        else:
            start_monitoring(log_dir=args.log_dir, mode=args.mode)