#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py

Author: Gris Iscomeback
Email: grisiscomeback[at]gmail[dot]com
Creation Date: 09/06/2024
License: GPL v3

Description: Console assistant for generating dynamic YAML phishing templates using AI
"""
import re
import os
import logging
import json
import requests
import argparse
from flask import jsonify, Response, stream_with_context

BANNER = """
[*] Starting: LazyOwn GPT Phishing Template Generator [;,;]
"""

script_dir = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_FILE = f"{script_dir}/knowledge_base_script.json"

def clean_think(texto):
    return re.sub(r'<think>.*?</think>', '', texto, flags=re.DOTALL)

def clean_yaml(texto):
    texto = re.sub(r"(?:```yaml)+", "", texto)
    texto = re.sub(r"(?:```)+$", "", texto)
    texto = texto.strip()
    return texto

def truncate_message(message, max_chars=18000):
    if len(message) > max_chars:
        return message[:max_chars]
    return message

def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def create_complex_prompt(base_prompt: str, history: str, knowledge_base: str) -> str:
    try:
        with open('payload.json', 'r') as file:
            config = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error reading payload.json: {e}")
        config = {}
    
    start_user = config.get("start_user", "")
    start_pass = config.get("start_pass", "")
    rhost = config.get("rhost", "")
    lhost = config.get("lhost", "")
    domain = config.get("domain", "")
    subdomain = config.get("subdomain", "")
    wordlist = config.get("wordlist", "")
    usrwordlist = config.get("usrwordlist", "")

    return f"""
You are an AI assistant tasked with generating a YAML file for a phishing email template based on a given scenario. The YAML file must include 'subject' and 'body' fields. The 'subject' should be an enticing email subject line. The 'body' should contain a valid HTML email with placeholders {{name}}, {{beacon_url}}, and {{tracking_pixel}}. The HTML must be professional and suitable for a phishing scenario.

Based on the following prompt: [[ {base_prompt} ]]

Generate the YAML content directly, starting with 'subject:' and ending with the closing HTML tag.

Example:
subject: "Urgent: Verify Your Bank Account"
body: |
  <!DOCTYPE html>
  <html>
  <body>
    <p>Hello {{name}},</p>
    <p>We detected suspicious activity on your account. Please verify your identity by clicking the link below:</p>
    <p><a href="{{beacon_url}}">Verify Account</a></p>
    <p>Note: If the link does not work, copy and paste it into a new tab.</p>
    <p>Thank you,<br>Security Team</p>
    {{tracking_pixel}}
  </body>
  </html>

Knowledge base:
start user: {start_user}
start pass: {start_pass}
remote host: {rhost}
local host: {lhost}
domain: {domain}
subdomain: {subdomain}
wordlist: {wordlist}
usrwordlist: {usrwordlist}

{knowledge_base}

Previous messages:
{history}
"""

def load_knowledge_base(file_path: str) -> dict:
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error reading knowledge base: {e}")
    return {}

def save_knowledge_base(knowledge_base: dict, file_path: str) -> None:
    try:
        with open(file_path, "w") as f:
            json.dump(knowledge_base, f, indent=4)
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error saving knowledge base: {e}")

def add_to_knowledge_base(prompt: str, command: str, file_path: str) -> None:
    knowledge_base = load_knowledge_base(file_path)
    knowledge_base[prompt] = command
    save_knowledge_base(knowledge_base, file_path)

def get_relevant_knowledge(prompt: str) -> str:
    if not isinstance(prompt, str):
        prompt = str(prompt)
    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_FILE)
    relevant_knowledge = []
    for key, value in knowledge_base.items():
        if prompt in key:
            relevant_knowledge.append(f"{key}: {value}")
    return "\n".join(relevant_knowledge) if relevant_knowledge else "No relevant knowledge found."

def process_prompt_local_yaml(prompt: str, debug: bool, mode: str, output_file: str = None) -> Response:
    configure_logging(debug)
    if not prompt.strip():
        logging.error("Prompt cannot be empty")
        return jsonify({"error": "Prompt cannot be empty"}), 400

    history = []
    relevant_knowledge = get_relevant_knowledge(prompt)
    complex_prompt = create_complex_prompt(truncate_message(prompt), '\n'.join(history), relevant_knowledge)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": complex_prompt,
                "stream": True
            },
            stream=True,
            timeout=1000
        )

        if response.status_code == 200:
            def generate():
                full_response = ""
                buffer = ""
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        try:
                            buffer += chunk.decode('utf-8')
                            while '\n' in buffer:
                                line, buffer = buffer.split('\n', 1)
                                if line.strip():
                                    json_chunk = json.loads(line)
                                    response_text = json_chunk.get("response", "")
                                    full_response += response_text
                                    if mode == 'web':
                                        yield json.dumps(json_chunk) + '\n'
                                    else:
                                        yield response_text
                        except (UnicodeDecodeError, json.JSONDecodeError) as e:
                            logging.error(f"Error decoding chunk: {e}")
                            continue
                if output_file:
                    try:
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(clean_think(clean_yaml(full_response)))
                        logging.info(f"Phishing YAML template saved to {output_file}")
                    except (IOError, OSError) as e:
                        logging.error(f"Error writing YAML file: {e}")

            return Response(stream_with_context(generate()), mimetype='text/event-stream' if mode == 'web' else 'text/plain')
        else:
            logging.error(f"API request failed: {response.status_code}")
            return jsonify({"error": f"Request error: {response.status_code}"}), 500

    except requests.RequestException as ex:
        logging.error(f"API communication error: {ex}")
        return jsonify({"error": str(ex)}), 500

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Phishing YAML Template Generator')
    parser.add_argument('--prompt', type=str, required=True, help='Prompt describing the phishing scenario')
    parser.add_argument('--output', type=str, help='Output YAML file path')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug logging')
    parser.add_argument('--mode', type=str, choices=['web', 'console'], default='console', help='Output mode: web (JSON) or console (text)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    configure_logging(args.debug)
    print(BANNER)
    response = process_prompt_local_yaml(args.prompt, args.debug, args.mode, args.output)
    if args.mode == 'console':
        for chunk in response.response:
            print(chunk.decode('utf-8'), end='', flush=True)