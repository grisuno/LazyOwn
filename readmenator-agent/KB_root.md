# Subsystem: root (page 1 of 3)
Pages: [KB_root.md](KB_root.md), [KB_root_p2.md](KB_root_p2.md), [KB_root_p3.md](KB_root_p3.md)

## DEPLOY.sh
- Doc: update_section_html: Función para actualizar una sección específica
- Layer: utility
- Language: sh
- Symbols:
  - `increment_version` (function, line 19)
  - `update_section_html` (function, line 99)
  - `get_commit_type` (function, line 203)

## __init__.py
- Layer: utility
- Language: py

## banner.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `image_to_bash` (function, line 26) `def image_to_bash(image_path, image_res)`
  - `list_png_files` (function, line 50) `def list_png_files()`
  - `main` (function, line 60) `def main()`
- Depends on: `utils.py`

## bootstrap.sh
- Doc: LazyOwn bootstrap installer (one-liner entry point).
- Layer: infrastructure
- Language: sh
- Symbols:
  - `usage` (function, line 70)
  - `log` (function, line 74)
  - `fail` (function, line 92)
  - `spin_run` (function, line 97)
  - `can_prompt` (function, line 239)
  - `ask` (function, line 250)
  - `update_checkout` (function, line 259)
  - `backup_payload` (function, line 268)
  - `clone_fresh` (function, line 280)
  - `clean_checkout` (function, line 286)
  - `confirm_clean` (function, line 293)
  - `ask_new_dir` (function, line 303)
  - `ask_existing_checkout_action` (function, line 315)
  - `ask_existing_path_action` (function, line 336)
  - `resolve_target_dir` (function, line 355)
  - `ask_launch_mode` (function, line 432)

## discord_c2.py
- Layer: utility
- Language: py
- Symbols:
  - `SecureSessionManager` (class, line 27) `class SecureSessionManager`
  - `Config` (class, line 86) `class Config`
  - `load_payload` (function, line 96) `def load_payload()`
  - `on_ready` (function, line 103) `def on_ready()`
  - `start` (function, line 108) `def start(ctx)`
  - `exce_cmd` (function, line 130) `def exce_cmd(ctx)`
  - `add_cli` (function, line 206) `def add_cli(ctx, new_client_id)`
  - `handle_file` (function, line 216) `def handle_file(ctx)`
  - `download_c2` (function, line 245) `def download_c2(ctx, client_id, file_name)`
  - `send_connected_clients` (function, line 256) `def send_connected_clients(ctx)`
  - `clients` (function, line 273) `def clients(ctx)`
  - `addcli` (function, line 278) `def addcli(ctx, new_client_id)`
  - `c2` (function, line 283) `def c2(ctx)`
  - `__init__` (method, line 28) `def __init__(self)`
  - `register_failed_attempt` (method, line 33) `def register_failed_attempt(self, user_id)`
  - `check_lockout` (method, line 40) `def check_lockout(self, user_id)`
  - `check_rate_limit` (method, line 49) `def check_rate_limit(self, user_id)`
  - `create_session` (method, line 62) `def create_session(self, user_id, client_id)`
  - `validate_session` (method, line 70) `def validate_session(self, user_id)`
  - `__init__` (method, line 87) `def __init__(self, config_dict)`
  - `__getitem__` (method, line 92) `def __getitem__(self, key)`
- Depends on: `core/parsers.py`, `lazyown.py`, `modules/llm_adapter.py`

## fast_run_as_r00t.sh
- Doc: — LazyOwn full-stack orchestrator  Speed-run launcher: brings up every core service in a tmux...
- Layer: utility
- Language: sh
- Symbols:
  - `_jq` (function, line 31)
  - `log` (function, line 59)
  - `spin` (function, line 60)
  - `err_box` (function, line 61)
  - `ensure_gum` (function, line 67)
  - `check_deps` (function, line 78)
  - `check_sudo` (function, line 87)
  - `parse_args` (function, line 96)
  - `t_send` (function, line 114)
  - `t_lazyown` (function, line 121)
  - `t_priv_user` (function, line 134)
  - `start_chown_watcher` (function, line 145)
  - `kill_stale_c2` (function, line 166)

## gen_cert.sh
- Doc: Verifica si se pasó una IP
- Layer: utility
- Language: sh

## install.sh
- Doc: LazyOwn installer.
- Layer: utility
- Language: sh
- Symbols:
  - `usage` (function, line 49)
  - `log` (function, line 88)
  - `spin_run` (function, line 98)
  - `ensure_gum` (function, line 128)
  - `install_system_packages` (function, line 139)
  - `install_external_tools` (function, line 150)
  - `install_python_environment` (function, line 165)
  - `install_ollama` (function, line 206)
  - `install_external_storage` (function, line 218)
  - `install_lazyownbt` (function, line 231)
  - `download_file` (function, line 251)
  - `install_encoder_module` (function, line 263)
  - `generate_certificates` (function, line 274)
  - `seed_payload_config` (function, line 281)
  - `verify_installation` (function, line 294)
  - `main` (function, line 310)

## key.py
- Layer: utility
- Language: py
- Symbols:
  - `main` (function, line 10) `def main()`
- Depends on: `core/console.py`, `core/prompt.py`

## lazy_sentinel4.py
- Doc: RAGManager: Manages RAG functionality with CAG caching for document processing and querying.
- Layer: utility
- Language: py
- Symbols:
  - `sanitize_content` (function, line 45) `def sanitize_content(text)`
  - `RAGManager` (class, line 56) `class RAGManager`
  - `Database` (class, line 212) `class Database`
  - `Alert` (class, line 269) `class Alert`
  - `LazySentinelHandler` (class, line 300) `class LazySentinelHandler(FileSystemEventHandler)`
  - `LazySentinel` (class, line 338) `class LazySentinel`
  - `App` (class, line 542) `class App(Cmd)`
  - `__init__` (method, line 59) `def __init__(self, model_name, cache_size)`
  - `initialize_cache_table` (method, line 71) `def initialize_cache_table(self)`
  - `get_cache_key` (method, line 83) `def get_cache_key(self, content)`
  - `load_existing_vectorstore` (method, line 86) `def load_existing_vectorstore(self)`
  - `ollama_llm` (method, line 99) `def ollama_llm(self, question, context)`
  - `process_file_to_rag` (method, line 113) `def process_file_to_rag(self, file_path)`
  - `query_rag` (method, line 153) `def query_rag(self, question)`
  - `invalidate_cache` (method, line 175) `def invalidate_cache(self, file_path)`
  - `get_knowledge_base_stats` (method, line 189) `def get_knowledge_base_stats(self)`
  - `__init__` (method, line 213) `def __init__(self, db_path)`
  - `initialize` (method, line 217) `def initialize(self)`
  - `execute` (method, line 241) `def execute(self, query, params)`
  - `insert` (method, line 253) `def insert(self, query, params)`
  - `__init__` (method, line 272) `def __init__(self, alert_type, details, severity)`
  - `to_dict` (method, line 278) `def to_dict(self)`
  - `save_to_db` (method, line 286) `def save_to_db(self, db)`
  - `__init__` (method, line 301) `def __init__(self, lazysentinel)`
  - `is_text_file` (method, line 304) `def is_text_file(self, file_path)`
  - `on_created` (method, line 314) `def on_created(self, event)`
  - `on_modified` (method, line 326) `def on_modified(self, event)`
  - `__init__` (method, line 339) `def __init__(self, app, popup_queue, watch_dir, excluded_files, min_file_size)`
  - `chunk_text` (method, line 359) `def chunk_text(self, text, chunk_size)`
  - `select_relevant_chunk` (method, line 362) `def select_relevant_chunk(self, file_content, chunks)`
  - `parse_deepseek_response` (method, line 376) `def parse_deepseek_response(self, response_text)`
  - `show_popup` (method, line 402) `def show_popup(self, file_name, relevant_info, commands, details)`
  - `process_file` (method, line 420) `def process_file(self, file_path)`
  - `stop` (method, line 536) `def stop(self)`
  - `__init__` (method, line 543) `def __init__(self)`
  - `display_toastr` (method, line 557) `def display_toastr(self, file_name, relevant_info, commands, details, severity, duration)`
  - `postcmd` (method, line 567) `def postcmd(self, stop, line)`
  - `do_quit` (method, line 591) `def do_quit(self, arg)`
  - `do_debug` (method, line 595) `def do_debug(self, arg)`
  - `do_rag_query` (method, line 604) `def do_rag_query(self, arg)`
  - `do_rag_add` (method, line 612) `def do_rag_add(self, arg)`
  - `do_rag_status` (method, line 627) `def do_rag_status(self, arg)`
  - `do_rag_toggle` (method, line 634) `def do_rag_toggle(self, arg)`
  - `do_rag_bulk_add` (method, line 639) `def do_rag_bulk_add(self, arg)`
  - `do_rag_search` (method, line 658) `def do_rag_search(self, arg)`
  - `complete_rag_add` (method, line 679) `def complete_rag_add(self, text, line, begidx, endidx)`
  - `complete_rag_bulk_add` (method, line 686) `def complete_rag_bulk_add(self, text, line, begidx, endidx)`
- Depends on: `cli/toast_bus.py`, `core/console.py`, `core/logging.py`, `modules/logging_config.py`


Next: [KB_root_p2.md](KB_root_p2.md)
