# Subsystem: legacy (page 2 of 2)
Previous: [KB_legacy.md](KB_legacy.md)

## contrib/legacy/lazyreversentlmv2.py
- Layer: utility
- Language: py
- Symbols:
  - `parse_hash_file` (function, line 11) `def parse_hash_file(file_path)`
  - `reverse_shell` (function, line 58) `def reverse_shell(target_ip, username, domain, lmhash, nthash, callback_ip, callback_port)`
- Depends on: `modules/lazyencoder_decoder.py`

## contrib/legacy/lazysearch.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `highlight_term` (function, line 29) `def highlight_term(text, term)`
  - `search_in_parquet` (function, line 32) `def search_in_parquet(term, parquet_files)`
  - `main` (function, line 44) `def main()`

## contrib/legacy/lazysearch_bot.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `signal_handler` (function, line 59) `def signal_handler(sig, frame)`
  - `show_help` (function, line 65) `def show_help(message)`
  - `check_api_key` (function, line 69) `def check_api_key()`
  - `configure_logging` (function, line 75) `def configure_logging(debug)`
  - `parse_args` (function, line 79) `def parse_args()`
  - `create_complex_prompt` (function, line 86) `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
  - `execute_command` (function, line 109) `def execute_command(command)`
  - `load_knowledge_base` (function, line 112) `def load_knowledge_base(file_path)`
  - `save_knowledge_base` (function, line 118) `def save_knowledge_base(knowledge_base, file_path)`
  - `add_to_knowledge_base` (function, line 122) `def add_to_knowledge_base(prompt, command, file_path)`
  - `get_relevant_knowledge` (function, line 127) `def get_relevant_knowledge(prompt)`
  - `transform_knowledge_base` (function, line 135) `def transform_knowledge_base(client)`
  - `main` (function, line 158) `def main()`
- Depends on: `core/logging.py`

## contrib/legacy/lazyseo.py
- Layer: utility
- Language: py
- Symbols:
  - `Config` (class, line 14) `class Config`
  - `load_payload` (method, line 23) `def load_payload()`
  - `make_request` (method, line 28) `def make_request(url, retries, timeout)`
  - `results` (method, line 49) `def results(file)`
  - `crawl` (method, line 57) `def crawl(url)`
  - `ffuf` (method, line 66) `def ffuf()`
  - `analyze_seo` (method, line 76) `def analyze_seo(url)`
  - `__init__` (method, line 15) `def __init__(self, config_dict)`
  - `__getitem__` (method, line 20) `def __getitem__(self, key)`
- Depends on: `modules/colors.py`

## contrib/legacy/lazysmbrelay.py
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 15) `def check_sudo()`
  - `start_smb_server` (function, line 27) `def start_smb_server()`
  - `start_smb_relay` (function, line 35) `def start_smb_relay(target, command)`
  - `CustomSMBRelayServer` (class, line 41) `class CustomSMBRelayServer(SMBRelayServer)`
  - `__init__` (method, line 42) `def __init__(self)`
  - `handleData` (method, line 46) `def handleData(self)`
  - `execute_remote_command` (method, line 50) `def execute_remote_command(self)`
- Depends on: `core/logging.py`, `utils.py`

## contrib/legacy/lazysniff.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `check_sudo` (function, line 41) `def check_sudo()`
  - `signal_handler` (function, line 50) `def signal_handler(sig, frame)`
  - `setup_curses` (function, line 57) `def setup_curses()`
  - `restore_curses` (function, line 66) `def restore_curses(stdscr)`
  - `show_banner` (function, line 73) `def show_banner(stdscr, banner)`
  - `process_packet` (function, line 80) `def process_packet(packet, packets, win_top, win_bottom)`
  - `analyze_packet` (function, line 90) `def analyze_packet(packet)`
  - `capture_packets` (function, line 112) `def capture_packets(interface, count, filter, pcap_file, packets, win_top, win_bottom)`
  - `main_curses` (function, line 118) `def main_curses(stdscr, packets, interface, count, filter, pcap_file)`
  - `parse_arguments` (function, line 188) `def parse_arguments()`
  - `main` (function, line 197) `def main()`

## contrib/legacy/lazysqli.py
- Doc: AUTHOR: jahman EDITED BY grisun0
- Layer: utility
- Language: py
- Symbols:
  - `send_payload` (function, line 13) `def send_payload(payload, url, s, sql_time)`
  - `sqli_dichotomie` (function, line 30) `def sqli_dichotomie(payload_brute, offset, url, s, sql_time)`
  - `sqli_thread` (function, line 51) `def sqli_thread(url, db, table, col, sql_time, threads)`
  - `main` (function, line 89) `def main(args)`

## contrib/legacy/lazyssh.py
- Layer: utility
- Language: py
- Symbols:
  - `execute` (function, line 13) `def execute(hostname, port, command)`
- Depends on: `core/logging.py`

## contrib/legacy/lazyvsftp.py
- Layer: utility
- Language: py
- Symbols:
  - `connect` (function, line 7) `def connect(host, port)`
  - `exploit` (function, line 16) `def exploit(host, port)`
  - `handle_backdoor` (function, line 61) `def handle_backdoor(s)`
- Depends on: `cli/commands/pwn.py`

## contrib/legacy/lazywerkzeug.py
- Layer: utility
- Language: py

## contrib/legacy/sql.py
- Layer: utility
- Language: py
- Symbols:
  - `def_handler` (function, line 8) `def def_handler(sig, frame)`
  - `getUnicode` (function, line 15) `def getUnicode(sqli)`
  - `makeRequest` (function, line 22) `def makeRequest(sqli_modified)`
- Depends on: `cli/commands/pwn.py`

