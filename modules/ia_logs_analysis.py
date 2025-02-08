#!/usr/bin/env python3

"""
log_monitor_bot.py

Author: Your Name
Email: youremail@example.com
Creation Date: 10/06/2024
License: GPL v3

Description: Real-time log monitoring bot for Linux systems.
             Monitors logs in /var/log (e.g., SSH, Apache2, Nginx) and uses DeepSeek to detect suspicious activity.
"""

import time
import json
import logging
import os
import requests
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.markdown import Markdown

# Logging configuration
logging.basicConfig(filename='log_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEEPSEEK_API_URL = "http://localhost:11434/api/generate"
DEEPSEEK_MODEL = "deepseek-r1:1.5b"

console = Console()

# List of known text-based log files to monitor
TEXT_LOG_FILES = [
    "auth.log",          # SSH and authentication logs
    "syslog",            # General system logs
    "kern.log",          # Kernel logs
    "nginx/access.log",  # Nginx access logs
    "nginx/error.log",   # Nginx error logs
    "apache2/access.log",# Apache access logs
    "apache2/error.log", # Apache error logs
    "dpkg.log",          # Package manager logs
    "boot.log",          # Boot logs
]

class LogFileHandler(FileSystemEventHandler):
    """
    Handles file system events for log files.
    """
    def __init__(self, mode='console'):
        super().__init__()
        self.mode = mode
        self.processed_files = set()  # Track processed files to avoid duplicates

    def on_modified(self, event):
        """
        Triggered when a log file is modified.
        """
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            if file_name in TEXT_LOG_FILES or any(file_name.endswith(log) for log in TEXT_LOG_FILES):
                if event.src_path not in self.processed_files:
                    self.processed_files.add(event.src_path)
                    self.analyze_log_file(event.src_path)

    def analyze_log_file(self, file_path):
        """
        Analyzes the content of the modified log file.
        """
        try:
            with open(file_path, 'r') as file:
                new_lines = file.readlines()
                if new_lines:
                    log_content = "".join(new_lines)
                    logging.info(f"New log entries detected in {file_path}:\n{log_content}")
                    if self.mode == 'console':
                        console.print(f"New log entries detected in {file_path}:\n{log_content}")
                    analyze_with_deepseek(log_content, self.mode)
        except Exception as e:
            logging.error(f"Error reading log file {file_path}: {e}")
            if self.mode == 'console':
                console.print(f"Error reading log file {file_path}")

def analyze_with_deepseek(log_content, mode='console'):
    """
    Sends log content to DeepSeek for advanced analysis.
    Returns the model's response in chunks.
    """
    try:
        console.print("Sending log content to DeepSeek for analysis...")
        response = requests.post(
            DEEPSEEK_API_URL,
            json={
                "model": DEEPSEEK_MODEL,
                "prompt": f"""
                Analyze the following log entries and determine if there is suspicious activity.
                Respond with a JSON containing:
                - 'suspicious': true/false (if the activity is suspicious).
                - 'reason': a brief explanation of why it is suspicious (if applicable).
                - 'details': additional relevant information.

                Log entries:
                {log_content}
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
        else:
            logging.error(f"Error communicating with DeepSeek API: {response.status_code}")
            console.print("Error communicating with DeepSeek API")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in request to DeepSeek: {e}")
        console.print("Error in request to DeepSeek")

def start_monitoring(log_dir='/var/log', mode='console'):
    """
    Starts monitoring the specified log directory.
    """
    console.print(f"Starting log monitoring in {log_dir}...")
    event_handler = LogFileHandler(mode)
    observer = Observer()
    observer.schedule(event_handler, path=log_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Log monitoring stopped by the user.")
        if mode == 'console':
            console.print("Log monitoring stopped by the user.")
    observer.join()

def parse_args():
    parser = argparse.ArgumentParser(description='Log Monitor Bot')
    parser.add_argument('--mode', type=str, choices=['console', 'web'], default='console', help='Output mode: console or web')
    parser.add_argument('--log-dir', type=str, default='/var/log', help='Directory to monitor for logs')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    start_monitoring(log_dir=args.log_dir, mode=args.mode)