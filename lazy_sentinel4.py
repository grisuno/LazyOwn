import os
import time
import cmd2
import logging
import json
import requests
import sqlite3
import datetime
import re
import queue
import tempfile
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from cachetools import LRUCache
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# RAG imports
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
try:
    import ollama
    import chromadb
    import cachetools
    import rich
except ImportError as e:
    print(f"Error: Missing required library: {e}")
    print("Please install with: pip install langchain langchain-community chromadb ollama cachetools rich")
    exit(1)

# Logging configuration
logging.basicConfig(filename='lazysentinel.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEEPSEEK_API_URL = "http://localhost:11434/api/generate"
DEEPSEEK_MODEL = "deepseek-r1:1.5b"
KNOWLEDGE_BASE_DIR = "./persistent_chroma_db"

def sanitize_content(text: str) -> str:
    """Sanitize text to ensure it's safe for Markdown rendering."""
    # Preserve Markdown-compatible characters but remove problematic ones
    text = text.replace('\r', '')  # Remove carriage returns
    text = re.sub(r'```.*?```', lambda m: m.group(0), text, flags=re.DOTALL)  # Preserve code blocks
    text = re.sub(r'`.*?`', lambda m: m.group(0), text)  # Preserve inline code
    text = re.sub(r'(\[.*?\]\(.*?\))', lambda m: m.group(0), text)  # Preserve links
    # Remove invalid control characters and excessive whitespace
    text = re.sub(r'[^\x20-\x7E\n\t#*+-_`[]()|]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class RAGManager:
    """Manages RAG functionality with CAG caching for document processing and querying."""
    
    def __init__(self, model_name: str = DEEPSEEK_MODEL, cache_size: int = 1000):
        self.model_name = model_name
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.persist_dir = KNOWLEDGE_BASE_DIR
        self.vectorstore = None
        self.retriever = None
        # Initialize caches
        self.embedding_cache = LRUCache(maxsize=cache_size)  # Cache document embeddings
        self.query_cache = LRUCache(maxsize=cache_size)      # Cache query results
        self.db = Database("lazysentinel.db")                # For persistent cache
        self.load_existing_vectorstore()
        self.initialize_cache_table()
    
    def initialize_cache_table(self):
        """Initialize SQLite table for persistent cache."""
        query = """
            CREATE TABLE IF NOT EXISTS rag_cache (
                cache_key TEXT PRIMARY KEY,
                cache_type TEXT NOT NULL,
                value TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
        """
        self.db.execute(query)
        logging.info("Initialized RAG cache table")
    
    def get_cache_key(self, content: str) -> str:
        """Generate a cache key from content using SHA-256."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def load_existing_vectorstore(self):
        """Load existing vectorstore if available."""
        try:
            if os.path.exists(self.persist_dir):
                self.vectorstore = Chroma(persist_directory=self.persist_dir, embedding_function=self.embeddings)
                self.retriever = self.vectorstore.as_retriever()
                logging.info("Loaded existing RAG knowledge base")
            else:
                logging.info("No existing RAG knowledge base found")
        except Exception as e:
            logging.error(f"Error loading vectorstore: {e}")
            self.vectorstore = None
            self.retriever = None
    
    def ollama_llm(self, question: str, context: str) -> str:
        """Query LLM with context using Ollama."""
        formatted_prompt = f"Question: {question}\n\nContext: {context}"
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": formatted_prompt}],
            )
            response_content = response["message"]["content"]
            final_answer = re.sub(r"<think>.*?</think>", "", response_content, flags=re.DOTALL).strip()
            return final_answer
        except Exception as e:
            logging.error(f"Error querying Ollama: {e}")
            return f"Error querying LLM: {str(e)}"
    
    def process_file_to_rag(self, file_path: Path) -> bool:
        """Process a file, add it to the RAG knowledge base, and cache embeddings."""
        try:
            file_extension = file_path.suffix.lower()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=100
            )
            
            # Handle different file types
            if file_extension == '.pdf':
                loader = PyMuPDFLoader(str(file_path))
            elif file_extension in ['.txt', '.md', '.log', '', '.yaml', '.csv', '.json', '.nmap']:
                loader = TextLoader(str(file_path))
            else:
                logging.warning(f"Unsupported file type for RAG: {file_extension}")
                return False
            
            # Load and split documents
            data = loader.load()
            chunks = text_splitter.split_documents(data)
            
            # Cache embeddings for each chunk
            for chunk in chunks:
                chunk_content = chunk.page_content
                cache_key = self.get_cache_key(chunk_content)
                if cache_key not in self.embedding_cache:
                    embedding = self.embeddings.embed_documents([chunk_content])[0]
                    self.embedding_cache[cache_key] = embedding
                    # Persist to SQLite
                    query = """
                        INSERT OR REPLACE INTO rag_cache (cache_key, cache_type, value, timestamp)
                        VALUES (?, ?, ?, ?)
                    """
                    self.db.execute(query, (
                        cache_key,
                        "embedding",
                        json.dumps(embedding),
                        datetime.datetime.now().isoformat()
                    ))
            
            # Add to vectorstore
            if self.vectorstore is None:
                self.vectorstore = Chroma.from_documents(
                    documents=chunks, 
                    embedding=self.embeddings, 
                    persist_directory=self.persist_dir
                )
                self.retriever = self.vectorstore.as_retriever()
            else:
                self.vectorstore.add_documents(documents=chunks)
                self.vectorstore.persist()
            
            logging.info(f"Added {file_path} to RAG knowledge base with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logging.error(f"Error processing file for RAG: {e}")
            return False
    
    def query_rag(self, question: str) -> str:
        """Query the RAG system with caching."""
        if self.retriever is None:
            return "No knowledge base available. Please process some files first."
        
        # Check query cache
        query_key = self.get_cache_key(question)
        if query_key in self.query_cache:
            logging.info(f"Query cache hit for: {question}")
            return self.query_cache[query_key]
        
        try:
            # Retrieve relevant documents
            retrieved_docs = self.retriever.invoke(question)
            
            # Combine documents into context
            context = "\n\n".join(doc.page_content for doc in retrieved_docs)
            
            # Query LLM with context
            response = self.ollama_llm(question, context)
            
            # Cache the response
            self.query_cache[query_key] = response
            query = """
                INSERT OR REPLACE INTO rag_cache (cache_key, cache_type, value, timestamp)
                VALUES (?, ?, ?, ?)
            """
            self.db.execute(query, (
                query_key,
                "query",
                response,
                datetime.datetime.now().isoformat()
            ))
            
            return response
            
        except Exception as e:
            logging.error(f"Error querying RAG: {e}")
            return f"Error querying knowledge base: {str(e)}"
    
    def invalidate_cache(self, file_path: Path):
        """Invalidate cache entries for a specific file."""
        try:
            with file_path.open('r', encoding='utf-8') as f:
                content = f.read()
            chunks = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=100
            ).split_text(content)
            
            for chunk in chunks:
                cache_key = self.get_cache_key(chunk)
                if cache_key in self.embedding_cache:
                    del self.embedding_cache[cache_key]
                self.db.execute("DELETE FROM rag_cache WHERE cache_key = ?", (cache_key,))
            
            logging.info(f"Invalidated cache for {file_path}")
        except Exception as e:
            logging.error(f"Error invalidating cache for {file_path}: {e}")
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get statistics about the knowledge base and cache."""
        if self.vectorstore is None:
            return {
                "status": "No knowledge base",
                "document_count": 0,
                "embedding_cache_size": len(self.embedding_cache),
                "query_cache_size": len(self.query_cache)
            }
        
        try:
            collection = self.vectorstore._collection
            count = collection.count() if hasattr(collection, 'count') else 0
            
            return {
                "status": "Active",
                "document_count": count,
                "persist_dir": self.persist_dir,
                "embedding_cache_size": len(self.embedding_cache),
                "query_cache_size": len(self.query_cache)
            }
        except Exception as e:
            logging.error(f"Error getting knowledge base stats: {e}")
            return {"status": "Error", "error": str(e)}

class Database:
    """Clase para manejar la base de datos SQLite."""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.initialize()

    def initialize(self) -> None:
        """Inicializa la base de datos y crea las tablas si no existen."""
        try:
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY,
                        type TEXT NOT NULL,
                        details TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        timestamp DATETIME NOT NULL
                    )
                ''')
                conn.commit()
            logging.info(f"Base de datos inicializada correctamente en {self.db_path}")
        except sqlite3.Error as e:
            logging.error(f"Error al inicializar la base de datos: {e}")
        except OSError as e:
            logging.error(f"Error de OS al crear directorio para la base de datos {self.db_path}: {e}")

    def execute(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """Ejecuta una consulta SQL y devuelve los resultados."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error en consulta SQL: {e}, Query: {query}, Params: {params}")
            return []

    def insert(self, query: str, params: Tuple = ()) -> Optional[int]:
        """Inserta datos en la base de datos y devuelve el ID del último registro."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error al insertar datos: {e}, Query: {query}, Params: {params}")
            try:
                conn.rollback()
            except:
                pass
            return None

class Alert:
    """Clase para representar y manejar alertas."""
    SEVERITY_LEVELS = ["info", "low", "medium", "high", "critical"]
    
    def __init__(self, alert_type: str, details: Dict, severity: str = "medium"):
        self.alert_type = alert_type
        self.details = details
        self.severity = severity if severity in self.SEVERITY_LEVELS else "medium"
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "type": self.alert_type,
            "details": self.details,
            "severity": self.severity,
            "timestamp": self.timestamp
        }

    def save_to_db(self, db: Database) -> Optional[int]:
        """Guarda la alerta en la base de datos."""
        details_json = json.dumps(self.details)
        query = """
            INSERT INTO alerts (type, details, severity, timestamp)
            VALUES (?, ?, ?, ?)
        """
        alert_id = db.insert(query, (self.alert_type, details_json, self.severity, self.timestamp))
        if alert_id:
            logging.info(f"Alerta '{self.alert_type}' (Severidad: {self.severity}) guardada en DB con ID: {alert_id}")
        else:
            logging.error(f"No se pudo guardar la alerta '{self.alert_type}' en la DB.")
        return alert_id

class LazySentinelHandler(FileSystemEventHandler):
    def __init__(self, lazysentinel):
        self.lazysentinel = lazysentinel

    def is_text_file(self, file_path: Path) -> bool:
        """Check if a file is a text file by extension or content."""
        text_extensions = ['.txt', '.md', '.log', '.py', '.c', '.asm', '.go', '.pdf', '']
        if file_path.suffix.lower() in text_extensions:
            return True
        try:
            with file_path.open('rb') as f:
                return b'\x00' not in f.read(1024)
        except:
            return False

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = Path(event.src_path)
        if file_path.name in self.lazysentinel.excluded_files:
            logging.info(f"Excluded file created: {file_path}")
            return
        if self.is_text_file(file_path):
            logging.info(f"File created: {file_path}, scheduling processing")
            time.sleep(1)
            self.lazysentinel.process_file(file_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        file_path = Path(event.src_path)
        if file_path.name in self.lazysentinel.excluded_files:
            logging.info(f"Excluded file modified: {file_path}")
            return
        if self.is_text_file(file_path):
            logging.info(f"File modified: {file_path}, scheduling processing")
            self.lazysentinel.process_file(file_path)

class LazySentinel:
    def __init__(self, app, popup_queue, watch_dir="sessions", excluded_files=None, min_file_size=10):
        self.app = app
        self.popup_queue = popup_queue
        self.watch_dir = Path(watch_dir)
        self.excluded_files = excluded_files or ['COMMANDS.md']
        self.min_file_size = min_file_size
        self.observer = Observer()
        self.handler = LazySentinelHandler(self)
        self.commands_md = Path("COMMANDS.md")
        self.model = DEEPSEEK_MODEL
        self.max_tokens = 64000
        self.chunk_size = 40000
        self.processed_files = {}
        self.db = Database("lazysentinel.db")
        self.rag_manager = RAGManager(self.model)
        self.auto_rag_enabled = True
        
        self.watch_dir.mkdir(exist_ok=True)
        self.observer.schedule(self.handler, str(self.watch_dir), recursive=False)
        self.observer.start()

    def chunk_text(self, text, chunk_size):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def select_relevant_chunk(self, file_content, chunks):
        if not chunks:
            return ""
        file_words = set(re.findall(r'\w+', file_content.lower()))
        best_chunk = chunks[0]
        max_overlap = 0
        for chunk in chunks:
            chunk_words = set(re.findall(r'\w+', chunk.lower()))
            overlap = len(file_words & chunk_words)
            if overlap > max_overlap:
                max_overlap = overlap
                best_chunk = chunk
        return best_chunk

    def parse_deepseek_response(self, response_text: str) -> Dict:
        """Parse DeepSeek's plain text response into a JSON-like dictionary."""
        result = {
            "relevant_info": "No info extracted.",
            "commands": [],
            "details": "No additional details."
        }
        if not response_text.strip():
            logging.warning("Empty DeepSeek response")
            return result

        relevant_info_match = re.search(r'(?:Relevant Information|Summary|Info):?\s*(.*?)(?=\n(?:Suggested Commands|Commands|Details|$))', response_text, re.DOTALL | re.IGNORECASE)
        commands_match = re.search(r'(?:Suggested Commands|Commands):?\s*(.*?)(?=\n(?:Details|$))', response_text, re.DOTALL | re.IGNORECASE)
        details_match = re.search(r'(?:Details|Additional Context):?\s*(.*)', response_text, re.DOTALL | re.IGNORECASE)

        if relevant_info_match:
            result["relevant_info"] = relevant_info_match.group(1).strip()
        elif response_text.strip():
            result["relevant_info"] = response_text.strip()

        if commands_match:
            commands_text = commands_match.group(1).strip()
            if commands_text.lower() != "none":
                result["commands"] = [cmd.strip() for cmd in commands_text.replace('\n', ',').split(',') if cmd.strip()]
        
        if details_match:
            result["details"] = details_match.group(1).strip()

        return result

    def show_popup(self, file_name: str, relevant_info: str, commands: List[str], details: str):
        """Queue a Rich-based popup to be displayed in the main thread."""
        try:
            # Sanitize content to prevent invalid characters or code snippets
            file_name = sanitize_content(file_name)
            relevant_info = sanitize_content(relevant_info)
            commands_str = sanitize_content(", ".join(commands) or "None")
            details = sanitize_content(details)
            
            self.popup_queue.put((file_name, relevant_info, commands_str, details, time.time()))
            logging.info(f"Queued popup for {file_name} at {time.time()}")
        except Exception as e:
            logging.error(f"Error queuing popup: {e}")
            content = (
                f"File: {file_name}\n"
                f"Relevant Information:\n{relevant_info}\n"
                f"Suggested Commands:\n{', '.join(commands) or 'None'}\n"
                f"Details:\n{details}\n"
                f"Press any key to continue..."
            )
            self.app.poutput(content)
            self.app.read_input("")

    def process_file(self, file_path):
        logging.info(f"Attempting to process file: {file_path}")
        try:
            mtime = file_path.stat().st_mtime
            current_time = time.time()
            file_info = self.processed_files.get(str(file_path), {'mtime': 0, 'last_processed': 0})
            if file_info['mtime'] >= mtime and current_time - file_info['last_processed'] < 2:
                logging.info(f"File {file_path} recently processed, skipping")
                return
            self.processed_files[str(file_path)] = {'mtime': mtime, 'last_processed': current_time}
            
            # Invalidate cache for modified file
            self.rag_manager.invalidate_cache(file_path)
        except FileNotFoundError:
            logging.warning(f"File {file_path} not found, possibly deleted")
            return

        for _ in range(5):
            try:
                if file_path.stat().st_size >= self.min_file_size:
                    break
            except FileNotFoundError:
                logging.warning(f"File {file_path} not found, possibly deleted")
                return
            time.sleep(1)
        else:
            logging.info(f"File {file_path} too small or inaccessible, skipping.")
            return

        try:
            with file_path.open('r', encoding='utf-8') as f:
                content = f.read()
            logging.info(f"Processing file: {file_path}, size: {file_path.stat().st_size} bytes")

            if self.auto_rag_enabled:
                self.rag_manager.process_file_to_rag(file_path)

            knowledge_base = ""
            if self.commands_md.exists():
                with self.commands_md.open('r', encoding='utf-8') as f:
                    commands_content = f.read()
                chunks = self.chunk_text(commands_content, self.chunk_size)
                knowledge_base = self.select_relevant_chunk(content, chunks)

            prompt = (
                f"""
                You are a helpful assistant. Analyze the provided file content and extract relevant information like passwords or usernames.
                Use the COMMANDS.md knowledge base to suggest relevant cmd2 commands.
                Respond with plain text in this format:
                Relevant Information: A brief summary of the file's key information.
                Suggested Commands: A comma-separated list of cmd2 commands or "none".
                Details: Additional context or observations.

                File content:
                {content[:10000]}

                COMMANDS.md knowledge base (partial):
                {knowledge_base}
                """
            )

            if len(prompt) > self.max_tokens * 4:
                prompt = prompt[:self.max_tokens * 4 - 100] + "..."
                logging.warning(f"Prompt truncated for {file_path} to fit token limit.")

            response = requests.post(
                DEEPSEEK_API_URL,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=600
            )

            if response.status_code == 200:
                try:
                    json_response = response.json()
                    logging.info(f"Full DeepSeek API response for {file_path}: {json_response}")
                    full_response = json_response.get("response", "")
                    
                    final_answer = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()
                    if not final_answer:
                        logging.warning(f"Empty DeepSeek response for {file_path}")
                        full_response = "No response from DeepSeek."

                    result = self.parse_deepseek_response(final_answer)
                    relevant_info = result.get('relevant_info', 'No info extracted.')
                    commands = result.get('commands', [])
                    details = result.get('details', 'No additional details.')

                    self.show_popup(file_path.name, relevant_info, commands, details)
                    logging.info(f"Processed {file_path}: {result}")

                    alert = Alert(
                        alert_type="file_processed",
                        details={
                            "file_path": str(file_path),
                            "relevant_info": relevant_info,
                            "commands": commands,
                            "details": details
                        },
                        severity="info"
                    )
                    alert.save_to_db(self.db)

                except (KeyError, ValueError) as e:
                    logging.error(f"Error processing DeepSeek response for {file_path}: {e}, Raw response: {json_response}")
                    relevant_info = "Failed to process DeepSeek response."
                    commands = []
                    details = f"Error: {str(e)}. Raw response: {json_response.get('response', 'No response')}"
                    self.show_popup(file_path.name, relevant_info, commands, details)
                    alert = Alert(
                        alert_type="processing_error",
                        details={
                            "file_path": str(file_path),
                            "error": str(e),
                            "raw_response": str(json_response)
                        },
                        severity="medium"
                    )
                    alert.save_to_db(self.db)
            else:
                logging.error(f"DeepSeek API error for {file_path}: {response.status_code}, Response: {response.text}")
                self.app.poutput(f"Error: DeepSeek API returned {response.status_code}")
                alert = Alert(
                    alert_type="api_error",
                    details={
                        "file_path": str(file_path),
                        "status_code": response.status_code,
                        "response_text": response.text
                    },
                    severity="high"
                )
                alert.save_to_db(self.db)

        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            self.app.poutput(f"Error processing {file_path}: {str(e)}")
            alert = Alert(
                alert_type="general_error",
                details={
                    "file_path": str(file_path),
                    "error": str(e)
                },
                severity="medium"
            )
            alert.save_to_db(self.db)

    def stop(self):
        self.observer.stop()
        self.observer.join()
        logging.info("LazySentinel stopped.")

class App(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "LazySentinel> "
        self.popup_queue = queue.Queue()
        self.last_popup_time = {}
        self.console = Console()  # Initialize Rich Console
        self.sentinel = LazySentinel(
            app=self,
            popup_queue=self.popup_queue,
            watch_dir="sessions",
            excluded_files=['COMMANDS.md', '.gitignore'],
            min_file_size=10
        )

    def postcmd(self, stop, line):
        """Check the popup queue after each command and display with Rich Markdown."""
        while not self.popup_queue.empty():
            try:
                file_name, relevant_info, commands, details, queue_time = self.popup_queue.get_nowait()
                last_time = self.last_popup_time.get(file_name, 0)
                if time.time() - last_time < 2:
                    logging.info(f"Skipped duplicate popup for {file_name} at {time.time()}")
                    continue
                self.last_popup_time[file_name] = time.time()
                
                # Create a Markdown-formatted string
                content = f"""# LazySentinel Alert

**File:** {file_name}

## Relevant Information
{relevant_info}

## Suggested Commands
{commands}

## Details
{details}

*Press any key to continue...*
"""
                # Render the content as Markdown
                markdown_content = Markdown(content)
                
                # Create a panel with the Markdown content
                panel = Panel(markdown_content, title="LazySentinel Alert", border_style="red", padding=(1, 2))
                
                # Clear the console and display the panel
                self.console.clear()
                self.console.print(panel)
                
                # Wait for user input to continue
                self.console.input("")
                logging.info(f"Displayed popup for {file_name} at {time.time()}")
                
                # Clear the console after input
                self.console.clear()
                
            except Exception as e:
                logging.error(f"Error displaying popup: {e}")
                content = (
                    f"File: {file_name}\n"
                    f"Relevant Information:\n{relevant_info}\n"
                    f"Suggested Commands:\n{commands}\n"
                    f"Details:\n{details}\n"
                    f"Press any key to continue..."
                )
                self.poutput(content)
                self.read_input("")
        return stop

    def do_quit(self, arg):
        """Quit the application."""
        self.sentinel.stop()
        return True

    def do_debug(self, arg):
        """Display debug information about LazySentinel state."""
        self.poutput(f"Monitoring directory: {self.sentinel.watch_dir}")
        self.poutput(f"Processed files: {list(self.sentinel.processed_files.keys())}")
        alerts = self.sentinel.db.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 5")
        for alert in alerts:
            self.poutput(f"Alert: {alert['type']}, Severity: {alert['severity']}, Details: {json.loads(alert['details'])}")

    def do_rag_query(self, arg):
        """Query the RAG knowledge base with a question."""
        if not arg.strip():
            self.poutput("Usage: rag_query <your question>")
            return
        
        self.poutput("Querying RAG knowledge base...")
        response = self.sentinel.rag_manager.query_rag(arg)
        self.poutput(f"\nRAG Response:\n{response}\n")

    def do_rag_add(self, arg):
        """Add a specific file to the RAG knowledge base."""
        if not arg.strip():
            self.poutput("Usage: rag_add <file_path>")
            return
        
        file_path = Path(arg.strip())
        if not file_path.exists():
            self.poutput(f"File not found: {file_path}")
            return
        
        self.poutput(f"Adding {file_path} to RAG knowledge base...")
        success = self.sentinel.rag_manager.process_file_to_rag(file_path)
        if success:
            self.poutput(f"Successfully added {file_path} to knowledge base")
        else:
            self.poutput(f"Failed to add {file_path} to knowledge base")

    def do_rag_status(self, arg):
        """Display RAG knowledge base status and statistics."""
        stats = self.sentinel.rag_manager.get_knowledge_base_stats()
        self.poutput("RAG Knowledge Base Status:")
        for key, value in stats.items():
            self.poutput(f"  {key}: {value}")
        
        self.poutput(f"\nAuto-RAG enabled: {self.sentinel.auto_rag_enabled}")

    def do_rag_toggle(self, arg):
        """Toggle automatic addition of monitored files to RAG knowledge base."""
        self.sentinel.auto_rag_enabled = not self.sentinel.auto_rag_enabled
        status = "enabled" if self.sentinel.auto_rag_enabled else "disabled"
        self.poutput(f"Auto-RAG is now {status}")

    def do_rag_bulk_add(self, arg):
        """Add all files in the monitored directory to RAG knowledge base."""
        if not arg.strip():
            directory = self.sentinel.watch_dir
        else:
            directory = Path(arg.strip())
        
        if not directory.exists() or not directory.is_dir():
            self.poutput(f"Directory not found: {directory}")
            return
        
        self.poutput(f"Adding all files from {directory} to RAG knowledge base...")
        
        added_count = 0
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.name not in self.sentinel.excluded_files:
                success = self.sentinel.rag_manager.process_file_to_rag(file_path)
                if success:
                    added_count += 1
                    self.poutput(f"  Added: {file_path.name}")
        
        self.poutput(f"Successfully added {added_count} files to knowledge base")

    def do_rag_search(self, arg):
        """Search for similar content in the RAG knowledge base."""
        if not arg.strip():
            self.poutput("Usage: rag_search <search terms>")
            return
        
        if self.sentinel.rag_manager.retriever is None:
            self.poutput("No knowledge base available. Add some files first.")
            return
        
        try:
            docs = self.sentinel.rag_manager.retriever.invoke(arg)
            
            if not docs:
                self.poutput("No similar documents found.")
                return
            
            self.poutput(f"Found {len(docs)} similar documents:")
            for i, doc in enumerate(docs[:5], 1):
                self.poutput(f"\n{i}. Content preview:")
                self.poutput(f"   {doc.page_content[:200]}...")
                if hasattr(doc, 'metadata') and doc.metadata:
                    self.poutput(f"   Source: {doc.metadata.get('source', 'Unknown')}")
                    
        except Exception as e:
            self.poutput(f"Error searching knowledge base: {e}")

    def complete_rag_add(self, text, line, begidx, endidx):
        """Tab completion for rag_add command."""
        files = []
        for path in [Path("."), self.sentinel.watch_dir]:
            if path.exists():
                files.extend([str(f) for f in path.iterdir() if f.is_file()])
        return [f for f in files if f.startswith(text)]

    def complete_rag_bulk_add(self, text, line, begidx, endidx):
        """Tab completion for rag_bulk_add command."""
        dirs = []
        for path in Path(".").iterdir():
            if path.is_dir():
                dirs.append(str(path))
        return [d for d in dirs if d.startswith(text)]

if __name__ == '__main__':

    
    app = App()
    app.poutput("LazySentinel with RAG and CAG capabilities initialized.")
    app.poutput("New RAG commands available:")
    app.poutput("  - rag_query <question>     : Ask questions about your knowledge base")
    app.poutput("  - rag_add <file>          : Add a specific file to knowledge base")
    app.poutput("  - rag_bulk_add [dir]      : Add all files from directory")
    app.poutput("  - rag_status              : Show knowledge base statistics")
    app.poutput("  - rag_toggle              : Toggle auto-RAG for monitored files")
    app.poutput("  - rag_search <terms>      : Search for similar content")
    app.poutput("  - debug                   : Show debug information")
    app.poutput("  - quit                    : Exit application")
    app.poutput()
    app.cmdloop()