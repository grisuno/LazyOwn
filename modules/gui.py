import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import requests
import os
import csv
import time
import threading
import json
import queue
import re
from datetime import datetime
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === CONFIGURACIÓN ===
API_BASE = "https://127.0.0.1:4444"
USERNAME = "LazyOwn"
PASSWORD = "LazyOwn"
SESSIONS_DIR = "/home/grisun0/LazyOwn/sessions"
LOG_DIR = SESSIONS_DIR

# === VARIABLES GLOBALES ===
polling = False
root = None
canvas = None
nodes = {}
current_beacon = None
console_notebook = None
beacon_tabs = {}
event_queue = queue.Queue()
event_handler = None
observer = None
events_text = None
processes_tree = None
status_label = None
connection_status = False

# === COLORES Y TEMA ===
COLORS = {
    'bg_primary': '#1a1a1a',
    'bg_secondary': '#2d2d2d', 
    'bg_tertiary': '#3d3d3d',
    'accent_green': '#00ff41',
    'accent_blue': '#0078d4',
    'accent_red': '#ff4444',
    'accent_yellow': '#ffaa00',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'text_success': '#00ff41',
    'text_error': '#ff4444',
    'text_warning': '#ffaa00',
    'border': '#404040'
}

# === ESTILOS MEJORADOS ===
def setup_modern_theme():
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configuraciones base
    style.configure("Modern.TFrame", 
                   background=COLORS['bg_primary'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure("Card.TFrame",
                   background=COLORS['bg_secondary'],
                   relief='solid',
                   borderwidth=1)
    
    style.configure("Modern.TButton",
                   background=COLORS['bg_tertiary'],
                   foreground=COLORS['text_primary'],
                   font=('Segoe UI', 9),
                   borderwidth=1,
                   focuscolor='none',
                   relief='flat')
    
    style.map("Modern.TButton",
              background=[('active', COLORS['accent_blue']),
                         ('pressed', COLORS['bg_tertiary'])])
    
    # Botón de acción primaria
    style.configure("Primary.TButton",
                   background=COLORS['accent_blue'],
                   foreground=COLORS['text_primary'],
                   font=('Segoe UI', 9, 'bold'))
    
    # Botón de peligro
    style.configure("Danger.TButton",
                   background=COLORS['accent_red'],
                   foreground=COLORS['text_primary'])
    
    # Botón de éxito
    style.configure("Success.TButton",
                   background=COLORS['accent_green'],
                   foreground=COLORS['bg_primary'])
    
    # Labels
    style.configure("Modern.TLabel",
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   font=('Segoe UI', 9))
    
    style.configure("Title.TLabel",
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   font=('Segoe UI', 12, 'bold'))
    
    style.configure("Status.TLabel",
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_secondary'],
                   font=('Segoe UI', 8))
    
    # Entry
    style.configure("Modern.TEntry",
                   fieldbackground=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'],
                   insertcolor=COLORS['accent_green'],
                   borderwidth=1,
                   relief='solid')
    
    # Notebook
    style.configure("Modern.TNotebook",
                   background=COLORS['bg_primary'],
                   tabmargins=[0, 0, 0, 0])
    
    style.configure("Modern.TNotebook.Tab",
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_secondary'],
                   padding=[15, 8],
                   font=('Segoe UI', 9))
    
    style.map("Modern.TNotebook.Tab",
              background=[('selected', COLORS['bg_primary']),
                         ('active', COLORS['bg_tertiary'])],
              foreground=[('selected', COLORS['text_primary']),
                         ('active', COLORS['text_primary'])])
    
    # Treeview
    style.configure("Modern.Treeview",
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'],
                   fieldbackground=COLORS['bg_secondary'],
                   borderwidth=0,
                   font=('Consolas', 9))
    
    style.configure("Modern.Treeview.Heading",
                   background=COLORS['bg_tertiary'],
                   foreground=COLORS['text_primary'],
                   font=('Segoe UI', 9, 'bold'))


# === WIDGETS PERSONALIZADOS ===
class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Modern.TFrame")
        self.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)
        
        self.status_label = ttk.Label(self, text="Desconectado", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.connection_indicator = tk.Canvas(self, width=12, height=12, bg=COLORS['bg_primary'], highlightthickness=0)
        self.connection_indicator.pack(side=tk.LEFT, padx=(0, 10))
        self.connection_indicator.create_oval(2, 2, 10, 10, fill=COLORS['accent_red'], outline=COLORS['accent_red'])
        
        self.time_label = ttk.Label(self, text="", style="Status.TLabel")
        self.time_label.pack(side=tk.RIGHT, padx=5)
        self.update_time()
    
    def update_status(self, text, connected=False):
        self.status_label.config(text=text)
        color = COLORS['accent_green'] if connected else COLORS['accent_red']
        self.connection_indicator.delete("all")
        self.connection_indicator.create_oval(2, 2, 10, 10, fill=color, outline=color)
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)

class ModernTreeview(ttk.Frame):
    def __init__(self, parent, columns, data_loader=None):
        super().__init__(parent, style="Card.TFrame")
        
        # Header
        header_frame = ttk.Frame(self, style="Modern.TFrame")
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.title_label = ttk.Label(header_frame, text="Datos", style="Title.TLabel")
        self.title_label.pack(side=tk.LEFT)
        
        self.refresh_btn = ttk.Button(header_frame, text="⟳ Actualizar", 
                                     style="Modern.TButton",
                                     command=self.refresh_data)
        self.refresh_btn.pack(side=tk.RIGHT)
        
        # Treeview con scrollbar
        tree_frame = ttk.Frame(self, style="Modern.TFrame")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                                style="Modern.Treeview", height=8)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col.title(), anchor=tk.W)
            self.tree.column(col, width=100, anchor=tk.W)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars y tree
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.data_loader = data_loader
        if data_loader:
            self.refresh_data()
    
    def refresh_data(self):
        if self.data_loader:
            # Limpiar datos existentes
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Cargar nuevos datos
            data = self.data_loader()
            for item in data:
                values = [item.get(col, "") for col in self.tree["columns"]]
                self.tree.insert("", tk.END, values=values)
    
    def set_title(self, title):
        self.title_label.config(text=title)

class ModernConsole(ttk.Frame):
    def __init__(self, parent, client_id=None):
        super().__init__(parent, style="Modern.TFrame")
        
        # Output area con mejor formato
        self.output = scrolledtext.ScrolledText(
            self, 
            bg=COLORS['bg_primary'],
            fg=COLORS['text_success'],
            font=('JetBrains Mono', 10),
            wrap=tk.WORD,
            insertbackground=COLORS['accent_green'],
            selectbackground=COLORS['bg_tertiary'],
            relief='flat',
            borderwidth=0
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 0))
        
        # Input frame con mejor diseño
        input_frame = ttk.Frame(self, style="Modern.TFrame")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Prompt label
        prompt_label = ttk.Label(input_frame, text=f"[{client_id or 'GLOBAL'}]>", 
                                style="Modern.TLabel", foreground=COLORS['accent_green'])
        prompt_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Entry
        self.entry = ttk.Entry(input_frame, font=('JetBrains Mono', 10), style="Modern.TEntry")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Send button
        self.send_btn = ttk.Button(input_frame, text="Enviar", 
                                  style="Primary.TButton",
                                  command=lambda: self.send_command(client_id))
        self.send_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.entry.bind('<Return>', lambda e: self.send_command(client_id))
        
        self.client_id = client_id
        
        # Configurar tags para colores
        self.output.tag_config("command", foreground=COLORS['accent_blue'])
        self.output.tag_config("response", foreground=COLORS['text_success'])
        self.output.tag_config("error", foreground=COLORS['text_error'])
        self.output.tag_config("warning", foreground=COLORS['text_warning'])
    
    def send_command(self, client_id):
        cmd = self.entry.get().strip()
        if not cmd: 
            return
        
        try:
            # Mostrar comando
            self.add_text(f"> {cmd}", "command")
            
            if client_id != "GLOBAL":
                requests.post(f"{API_BASE}/issue_command", 
                            data={"client_id": client_id, "command": cmd}, verify=False)
            
            self.entry.delete(0, tk.END)
            
        except Exception as e:
            self.add_text(f"[ERROR] {str(e)}", "error")
    
    def add_text(self, text, tag=None):
        self.output.insert(tk.END, f"{text}\n", tag)
        self.output.see(tk.END)

class ImplantCard(ttk.Frame):
    def __init__(self, parent, client_id, on_select=None):
        super().__init__(parent, style="Card.TFrame")
        self.client_id = client_id
        self.on_select = on_select
        
        # Main content
        content_frame = ttk.Frame(self, style="Modern.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Icon y nombre
        header_frame = ttk.Frame(content_frame, style="Modern.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        os_image = self.load_os_image(client_id)

        if os_image:
            print("Usando imagen")
            icon_label = ttk.Label(header_frame, image=os_image)
            icon_label.image = os_image  # Mantener referencia
        else:
            print("Usando emoji fallback")
            # Fallback a emoji si no hay imagen
            os_icon = "🖥️" if "windows" in client_id.lower() else "🐧" if "linux" in client_id.lower() else "🍎"
            icon_label = ttk.Label(header_frame, text=os_icon, font=('Segoe UI', 16))

        icon_label.pack(side=tk.LEFT, padx=(0, 10))

        
        name_label = ttk.Label(header_frame, text=client_id, 
                              style="Title.TLabel", font=('Segoe UI', 10, 'bold'))
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status indicator
        self.status_canvas = tk.Canvas(header_frame, width=12, height=12, 
                                      bg=COLORS['bg_secondary'], highlightthickness=0)
        self.status_canvas.pack(side=tk.RIGHT)
        self.status_canvas.create_oval(2, 2, 10, 10, fill=COLORS['accent_green'], outline=COLORS['accent_green'])
        
        # Info adicional
        info_frame = ttk.Frame(content_frame, style="Modern.TFrame")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text="Estado: Activo", 
                 style="Status.TLabel", foreground=COLORS['text_success']).pack(anchor=tk.W)
        
        ttk.Label(info_frame, text=f"Última actividad: {datetime.now().strftime('%H:%M:%S')}", 
                 style="Status.TLabel").pack(anchor=tk.W)
        
        # Botones de acción
        button_frame = ttk.Frame(content_frame, style="Modern.TFrame")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Consola", style="Primary.TButton",
                  command=self.open_console).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Archivos", style="Modern.TButton",
                  command=self.open_files).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Procesos", style="Modern.TButton",
                  command=self.open_processes).pack(side=tk.LEFT)
        
        # Click en toda la card
        self.bind("<Button-1>", self.on_card_click)
        content_frame.bind("<Button-1>", self.on_card_click)
        for child in content_frame.winfo_children():
            child.bind("<Button-1>", self.on_card_click)
    
    def on_card_click(self, event):
        if self.on_select:
            self.on_select(self.client_id)
    
    def open_console(self):
        if self.on_select:
            self.on_select(self.client_id)
    
    def open_files(self):
        # Implementar explorador de archivos
        pass
    
    def open_processes(self):
        # Implementar lista de procesos
        pass

    def load_os_image(self, client_id):  # IMPORTANTE: debe tener 'self' como método de clase
        """Cargar imagen del sistema operativo basado en el client_id"""
        try:
            # Determinar el tipo de OS
            if "windows" in client_id.lower() or "win" in client_id.lower():
                image_path = "windows.png"
            elif "linux" in client_id.lower():
                image_path = "linux.png"
            elif "mac" in client_id.lower() or "darwin" in client_id.lower():
                image_path = "mac.png"
            else:
                image_path = "client.png"
            
            # Debug: verificar la ruta
            print(f"Intentando cargar: {image_path}")
            print(f"Archivo existe: {os.path.exists(image_path)}")
            
            # Verificar si el archivo existe
            if os.path.exists(image_path):
                # Cargar y redimensionar imagen
                img = Image.open(image_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                print(f"Imagen cargada exitosamente: {image_path}")
                return ImageTk.PhotoImage(img)
            else:
                print(f"Archivo no encontrado: {image_path}")
                return None
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            return None
# === FUNCIONES DE API MEJORADAS ===
def login():
    global connection_status, status_bar
    try:
        resp = requests.post(f"{API_BASE}/login", 
                           data={"username": USERNAME, "password": PASSWORD}, 
                           verify=False, timeout=5)
        if resp.status_code == 200:
            connection_status = True
            status_bar.update_status("Conectado al C2", True)
            show_notification("✓ Conectado al C2 exitosamente", "success")
            refresh_clients()
            start_polling()
        else:
            connection_status = False
            status_bar.update_status("Login fallido", False)
            show_notification("✗ Error en login", "error")
    except Exception as e:
        connection_status = False
        status_bar.update_status(f"Error de conexión: {str(e)}", False)
        show_notification(f"✗ No se pudo conectar: {str(e)}", "error")

def show_notification(message, type="info"):
    """Mostrar notificación en el sistema"""
    colors = {
        "success": COLORS['text_success'],
        "error": COLORS['text_error'],
        "warning": COLORS['text_warning'],
        "info": COLORS['text_primary']
    }
    
    if events_text:
        timestamp = datetime.now().strftime("%H:%M:%S")
        events_text.insert(tk.END, f"[{timestamp}] {message}\n")
        events_text.tag_add(type, f"end-2c linestart", "end-1c")
        events_text.tag_config(type, foreground=colors.get(type, COLORS['text_primary']))
        events_text.see(tk.END)

def refresh_clients():
    global implants_container
    try:
        resp = requests.get(f"{API_BASE}/get_connected_clients", verify=False, timeout=5)
        data = resp.json()
        clients = data.get("connected_clients", [])
        
        # Limpiar contenedor de implants
        for widget in implants_container.winfo_children():
            widget.destroy()
        
        # Crear cards para cada cliente
        for i, client in enumerate(clients):
            card = ImplantCard(implants_container, client, select_client)
            card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
        
        # Configurar columnas
        implants_container.columnconfigure(0, weight=1)
        implants_container.columnconfigure(1, weight=1)
        
        show_notification(f"✓ {len(clients)} implantes activos", "success")
        
    except Exception as e:
        show_notification(f"✗ Error actualizando clientes: {str(e)}", "error")

def select_client(client_id):
    global current_beacon
    current_beacon = client_id
    
    # Crear o seleccionar pestaña del beacon
    if client_id not in beacon_tabs:
        create_beacon_tab(client_id)
    
    console_notebook.select(beacon_tabs[client_id])
    show_notification(f"→ Beacon seleccionado: {client_id}", "info")

def create_beacon_tab(client_id):
    frame = ttk.Frame(console_notebook, style="Modern.TFrame")
    console_notebook.add(frame, text=f"🔗 {client_id}")
    beacon_tabs[client_id] = frame
    
    console = ModernConsole(frame, client_id)
    console.pack(fill=tk.BOTH, expand=True)
    
    # Guardar referencia a la consola
    frame.console = console

# === HANDLERS DE ARCHIVOS ===
class LogHandler(FileSystemEventHandler):
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.last_positions = {}

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".log"):
            return
        
        filename = os.path.basename(event.src_path)
        if filename.startswith("LazyOwn_session"):
            return

        client_id = filename.replace('.log', '')
        self.process_log_file(client_id)

    def process_log_file(self, client_id):
        log_path = os.path.join(self.log_dir, f"{client_id}.log")
        if not os.path.exists(log_path):
            return

        last_pos = self.last_positions.get(client_id, 0)

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                f.seek(last_pos)
                
                reader = csv.reader(f)
                for row in reader:
                    if len(row) > 10:
                        output = row[10].strip()
                        command = row[0].strip()
                        
                        if not output or output.lower() in ['none', 'null', ''] or output == command:
                            continue

                        event_queue.put({
                            'type': 'command_output',
                            'client_id': client_id,
                            'output': output
                        })

                self.last_positions[client_id] = f.tell()

        except Exception as e:
            event_queue.put({
                'type': 'error',
                'message': f"Error procesando {log_path}: {e}"
            })

def process_queue():
    while not event_queue.empty():
        event = event_queue.get_nowait()
        
        if event['type'] == 'command_output':
            # Mostrar en Event Log
            show_notification(f"[{event['client_id']}] << {event['output']}", "info")
            
            # Mostrar en pestaña del beacon
            if event['client_id'] in beacon_tabs:
                console = beacon_tabs[event['client_id']].console
                console.add_text(f"<< {event['output']}", "response")
        
        elif event['type'] == 'error':
            show_notification(f"[ERROR] {event['message']}", "error")
    
    root.after(100, process_queue)

def start_polling():
    global polling, event_handler, observer
    polling = True
    event_handler = LogHandler(LOG_DIR)
    observer = Observer()
    observer.schedule(event_handler, path=LOG_DIR, recursive=False)
    observer.start()
    threading.Thread(target=auto_refresh_clients, daemon=True).start()

def stop_polling():
    global polling, observer
    polling = False
    if observer:
        observer.stop()
        observer.join()

def auto_refresh_clients():
    while polling:
        time.sleep(10)  # Refresh cada 10 segundos
        if root.winfo_exists():
            root.after(0, refresh_clients)
        else:
            break

# === FUNCIONES DE CARGA DE DATOS ===
def load_implants_data():
    implants = []
    try:
        for file in os.listdir(SESSIONS_DIR):
            if file.startswith("implant_config_") and file.endswith(".json"):
                with open(os.path.join(SESSIONS_DIR, file), 'r') as f:
                    data = json.load(f)
                    implants.append(data)
    except Exception as e:
        show_notification(f"Error cargando implantes: {e}", "error")
    return implants

def load_banners_data():
    try:
        with open(os.path.join(SESSIONS_DIR, "banners.json"), 'r') as f:
            return json.load(f)
    except Exception as e:
        show_notification(f"Error cargando banners: {e}", "error")
        return []

def load_access_log():
    entries = []
    log_path = os.path.join(SESSIONS_DIR, "access.log")
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                for line in f:
                    match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (.+)", line)
                    if match:
                        entries.append({
                            'timestamp': match.group(1),
                            'level': match.group(2),
                            'message': match.group(3)
                        })
    except Exception as e:
        show_notification(f"Error cargando access log: {e}", "error")
    return entries

def upload_file():
    file_path = filedialog.askopenfilename()
    if not file_path or not current_beacon:
        show_notification("Selecciona un archivo y un beacon", "warning")
        return
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'client_id': current_beacon}
            resp = requests.post(f"{API_BASE}/upload", files=files, data=data, verify=False)
            
            if resp.status_code == 200:
                show_notification(f"✓ Archivo {os.path.basename(file_path)} subido a {current_beacon}", "success")
            else:
                show_notification(f"✗ Error subiendo archivo: {resp.status_code}", "error")
                
    except Exception as e:
        show_notification(f"✗ Error subiendo archivo: {str(e)}", "error")

# === INTERFAZ PRINCIPAL MEJORADA ===
def create_modern_ui():
    global root, console_notebook, events_text, status_bar, implants_container, beacon_tabs

    root = tk.Tk()
    root.title("LazyOwn C2 - Modern Interface")
    root.geometry("1600x1000")
    root.configure(bg=COLORS['bg_primary'])
    root.minsize(1200, 800)

    # Configurar tema moderno
    setup_modern_theme()

    # === BARRA DE ESTADO ===
    status_bar = StatusBar(root)

    # === CONTENEDOR PRINCIPAL ===
    main_container = ttk.Frame(root, style="Modern.TFrame")
    main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

    # === PANEL SUPERIOR - IMPLANTES ===
    implants_frame = ttk.LabelFrame(main_container, text=" 🎯 Implantes Activos ", 
                                   style="Modern.TFrame")
    implants_frame.pack(fill=tk.X, pady=(0, 10))

    # Scrollable frame para implantes
    canvas_frame = ttk.Frame(implants_frame, style="Modern.TFrame")
    canvas_frame.pack(fill=tk.X, padx=10, pady=10)

    implants_canvas = tk.Canvas(canvas_frame, bg=COLORS['bg_primary'], 
                               highlightthickness=0, height=200)
    implants_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", 
                                      command=implants_canvas.xview)
    implants_canvas.configure(xscrollcommand=implants_scrollbar.set)

    implants_container = ttk.Frame(implants_canvas, style="Modern.TFrame")
    implants_canvas.create_window((0, 0), window=implants_container, anchor="nw")

    implants_canvas.pack(fill=tk.BOTH, expand=True)
    implants_scrollbar.pack(fill=tk.X, pady=(5, 0))

    def configure_scroll_region(event):
        implants_canvas.configure(scrollregion=implants_canvas.bbox("all"))

    implants_container.bind("<Configure>", configure_scroll_region)

    # === PANEL PRINCIPAL - NOTEBOOK ===
    main_notebook = ttk.Notebook(main_container, style="Modern.TNotebook")
    main_notebook.pack(fill=tk.BOTH, expand=True)

    # --- Pestaña: Consolas ---
    console_frame = ttk.Frame(main_notebook, style="Modern.TFrame")
    main_notebook.add(console_frame, text="💻 Consolas")

    console_notebook = ttk.Notebook(console_frame, style="Modern.TNotebook")
    console_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Event Log como primera pestaña
    event_frame = ttk.Frame(console_notebook, style="Modern.TFrame")
    console_notebook.add(event_frame, text="📋 Event Log")
    
    events_console = ModernConsole(event_frame, "GLOBAL")
    events_console.pack(fill=tk.BOTH, expand=True)
    events_text = events_console.output

    # --- Pestaña: Datos ---
    data_frame = ttk.Frame(main_notebook, style="Modern.TFrame")
    main_notebook.add(data_frame, text="📊 Datos")

    data_notebook = ttk.Notebook(data_frame, style="Modern.TNotebook")
    data_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Subpestaña: Banners
    banner_tree = ModernTreeview(data_notebook, 
                                ("hostname", "port", "protocol", "service", "extra"),
                                load_banners_data)
    banner_tree.set_title("🌐 Banner Grabbing")
    data_notebook.add(banner_tree, text="Banners")

    # Subpestaña: Implantes
    implant_tree = ModernTreeview(data_notebook,
                                 ("name", "os", "rhost", "sleep", "created"),
                                 load_implants_data)
    implant_tree.set_title("🔧 Configuración de Implantes")
    data_notebook.add(implant_tree, text="Implantes")

    # Subpestaña: Access Log
    access_tree = ModernTreeview(data_notebook,
                                ("timestamp", "level", "message"),
                                load_access_log)
    access_tree.set_title("📝 Registro de Accesos")
    data_notebook.add(access_tree, text="Access Log")

    # --- Pestaña: Herramientas ---
    tools_frame = ttk.Frame(main_notebook, style="Modern.TFrame")
    main_notebook.add(tools_frame, text="🛠️ Herramientas")

    tools_container = ttk.Frame(tools_frame, style="Modern.TFrame")
    tools_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Grid de herramientas
    create_tools_grid(tools_container)

    # === MENÚ MEJORADO ===
    create_modern_menu()

    # === ATAJOS DE TECLADO ===
    setup_keyboard_shortcuts()

    # === INICIALIZACIÓN ===
    beacon_tabs = {}
    
    # Mostrar mensaje de bienvenida
    show_notification("🚀 LazyOwn C2 iniciado - Presiona Ctrl+L para conectar", "info")
    
    # Intentar conexión automática
    root.after(1000, login)
    
    # Iniciar procesamiento de eventos
    root.after(100, process_queue)
    
    # Configurar cierre
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    return root

def create_tools_grid(parent):
    """Crear grid de herramientas"""
    
    # Herramientas principales
    tools = [
        {
            "name": "📁 Subir Archivo",
            "desc": "Subir archivo al beacon seleccionado",
            "command": upload_file,
            "style": "Primary.TButton"
        },
        {
            "name": "🔄 Actualizar",
            "desc": "Actualizar lista de beacons",
            "command": refresh_clients,
            "style": "Success.TButton"
        },
        {
            "name": "🔌 Reconectar",
            "desc": "Reconectar al servidor C2",
            "command": login,
            "style": "Modern.TButton"
        },
        {
            "name": "💾 Exportar Logs",
            "desc": "Exportar logs de sesión",
            "command": export_logs,
            "style": "Modern.TButton"
        },
        {
            "name": "🗂️ Gestionar Payloads",
            "desc": "Generar y gestionar payloads",
            "command": manage_payloads,
            "style": "Modern.TButton"
        },
        {
            "name": "📊 Estadísticas",
            "desc": "Ver estadísticas del C2",
            "command": show_statistics,
            "style": "Modern.TButton"
        }
    ]
    
    # Crear cards para cada herramienta
    for i, tool in enumerate(tools):
        card = create_tool_card(parent, tool)
        card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")
    
    # Configurar columnas
    for i in range(3):
        parent.columnconfigure(i, weight=1)

def create_tool_card(parent, tool):
    """Crear card de herramienta"""
    card = ttk.Frame(parent, style="Card.TFrame")
    
    content = ttk.Frame(card, style="Modern.TFrame")
    content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # Título
    title_label = ttk.Label(content, text=tool["name"], 
                           style="Title.TLabel", font=('Segoe UI', 11, 'bold'))
    title_label.pack(anchor=tk.W, pady=(0, 5))
    
    # Descripción
    desc_label = ttk.Label(content, text=tool["desc"], 
                          style="Status.TLabel", wraplength=200)
    desc_label.pack(anchor=tk.W, pady=(0, 10))
    
    # Botón
    button = ttk.Button(content, text="Ejecutar", 
                       style=tool["style"], command=tool["command"])
    button.pack(anchor=tk.W)
    
    return card

def create_modern_menu():
    """Crear menú moderno"""
    menubar = tk.Menu(root, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                      activebackground=COLORS['accent_blue'], activeforeground=COLORS['text_primary'])
    root.config(menu=menubar)
    
    # Menú Archivo
    file_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                        activebackground=COLORS['accent_blue'])
    menubar.add_cascade(label="📁 Archivo", menu=file_menu)
    file_menu.add_command(label="📤 Subir Archivo", command=upload_file, accelerator="Ctrl+U")
    file_menu.add_command(label="💾 Exportar Logs", command=export_logs, accelerator="Ctrl+E")
    file_menu.add_separator()
    file_menu.add_command(label="❌ Salir", command=on_closing, accelerator="Ctrl+Q")
    
    # Menú Conexión
    conn_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                        activebackground=COLORS['accent_blue'])
    menubar.add_cascade(label="🔌 Conexión", menu=conn_menu)
    conn_menu.add_command(label="🔗 Conectar", command=login, accelerator="Ctrl+L")
    conn_menu.add_command(label="🔄 Actualizar Beacons", command=refresh_clients, accelerator="F5")
    conn_menu.add_command(label="⏹️ Detener Polling", command=stop_polling)
    
    # Menú Herramientas
    tools_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                         activebackground=COLORS['accent_blue'])
    menubar.add_cascade(label="🛠️ Herramientas", menu=tools_menu)
    tools_menu.add_command(label="🗂️ Gestionar Payloads", command=manage_payloads)
    tools_menu.add_command(label="📊 Estadísticas", command=show_statistics)
    tools_menu.add_command(label="🔧 Configuración", command=show_settings)
    
    # Menú Ayuda
    help_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                        activebackground=COLORS['accent_blue'])
    menubar.add_cascade(label="❓ Ayuda", menu=help_menu)
    help_menu.add_command(label="📖 Manual de Usuario", command=show_help)
    help_menu.add_command(label="ℹ️ Acerca de", command=show_about)

def setup_keyboard_shortcuts():
    """Configurar atajos de teclado"""
    root.bind('<Control-l>', lambda e: login())
    root.bind('<Control-u>', lambda e: upload_file())
    root.bind('<Control-e>', lambda e: export_logs())
    root.bind('<Control-q>', lambda e: on_closing())
    root.bind('<F5>', lambda e: refresh_clients())
    root.bind('<Control-r>', lambda e: refresh_clients())

# === FUNCIONES DE HERRAMIENTAS ===
def export_logs():
    """Exportar logs a archivo"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialvalue=f"lazyown_logs_{timestamp}.txt"
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== LAZYOWN C2 LOGS ===\n")
                f.write(f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                # Exportar contenido del event log
                if events_text:
                    f.write("EVENT LOG:\n")
                    f.write("-"*20 + "\n")
                    f.write(events_text.get(1.0, tk.END))
                    f.write("\n" + "="*50 + "\n\n")
                
                # Exportar logs de cada beacon
                for client_id, tab_frame in beacon_tabs.items():
                    if hasattr(tab_frame, 'console'):
                        f.write(f"BEACON {client_id}:\n")
                        f.write("-"*20 + "\n")
                        f.write(tab_frame.console.output.get(1.0, tk.END))
                        f.write("\n" + "="*50 + "\n\n")
            
            show_notification(f"✓ Logs exportados a {filename}", "success")
    except Exception as e:
        show_notification(f"✗ Error exportando logs: {str(e)}", "error")

def manage_payloads():
    """Ventana de gestión de payloads"""
    payload_window = tk.Toplevel(root)
    payload_window.title("🗂️ Gestión de Payloads")
    payload_window.geometry("800x600")
    payload_window.configure(bg=COLORS['bg_primary'])
    
    # Aplicar tema
    payload_window.transient(root)
    payload_window.grab_set()
    
    # Contenido
    main_frame = ttk.Frame(payload_window, style="Modern.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    title_label = ttk.Label(main_frame, text="🗂️ Gestión de Payloads", style="Title.TLabel")
    title_label.pack(pady=(0, 20))
    
    # Notebook para diferentes tipos de payloads
    payload_notebook = ttk.Notebook(main_frame, style="Modern.TNotebook")
    payload_notebook.pack(fill=tk.BOTH, expand=True)
    
    # Pestaña Windows
    windows_frame = ttk.Frame(payload_notebook, style="Modern.TFrame")
    payload_notebook.add(windows_frame, text="🖥️ Windows")
    
    # Pestaña Linux
    linux_frame = ttk.Frame(payload_notebook, style="Modern.TFrame")
    payload_notebook.add(linux_frame, text="🐧 Linux")
    
    # Botones de acción
    button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
    button_frame.pack(fill=tk.X, pady=(20, 0))
    
    ttk.Button(button_frame, text="Generar Payload", 
              style="Primary.TButton").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Cerrar", 
              style="Modern.TButton", 
              command=payload_window.destroy).pack(side=tk.RIGHT)

def show_statistics():
    """Mostrar ventana de estadísticas"""
    stats_window = tk.Toplevel(root)
    stats_window.title("📊 Estadísticas del C2")
    stats_window.geometry("600x400")
    stats_window.configure(bg=COLORS['bg_primary'])
    
    stats_window.transient(root)
    stats_window.grab_set()
    
    main_frame = ttk.Frame(stats_window, style="Modern.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    title_label = ttk.Label(main_frame, text="📊 Estadísticas del Sistema", style="Title.TLabel")
    title_label.pack(pady=(0, 20))
    
    # Estadísticas básicas
    stats_frame = ttk.Frame(main_frame, style="Card.TFrame")
    stats_frame.pack(fill=tk.BOTH, expand=True)
    
    content_frame = ttk.Frame(stats_frame, style="Modern.TFrame")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Calcular estadísticas
    total_beacons = len(beacon_tabs)
    uptime = "Calculando..."
    
    stats_text = f"""
    🎯 Beacons Activos: {total_beacons}
    ⏱️ Tiempo Activo: {uptime}
    🔌 Estado Conexión: {'Conectado' if connection_status else 'Desconectado'}
    📁 Directorio Logs: {LOG_DIR}
    🌐 Servidor C2: {API_BASE}
    """
    
    stats_label = ttk.Label(content_frame, text=stats_text, style="Modern.TLabel")
    stats_label.pack(anchor=tk.W)
    
    ttk.Button(main_frame, text="Cerrar", 
              style="Modern.TButton", 
              command=stats_window.destroy).pack(pady=(20, 0))

def show_settings():
    """Mostrar ventana de configuración"""
    settings_window = tk.Toplevel(root)
    settings_window.title("🔧 Configuración")
    settings_window.geometry("500x400")
    settings_window.configure(bg=COLORS['bg_primary'])
    
    settings_window.transient(root)
    settings_window.grab_set()
    
    main_frame = ttk.Frame(settings_window, style="Modern.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    title_label = ttk.Label(main_frame, text="🔧 Configuración", style="Title.TLabel")
    title_label.pack(pady=(0, 20))
    
    # Configuraciones
    config_frame = ttk.Frame(main_frame, style="Card.TFrame")
    config_frame.pack(fill=tk.BOTH, expand=True)
    
    content_frame = ttk.Frame(config_frame, style="Modern.TFrame")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Servidor C2
    ttk.Label(content_frame, text="Servidor C2:", style="Modern.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
    server_entry = ttk.Entry(content_frame, style="Modern.TEntry", width=30)
    server_entry.insert(0, API_BASE)
    server_entry.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
    
    # Usuario
    ttk.Label(content_frame, text="Usuario:", style="Modern.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
    user_entry = ttk.Entry(content_frame, style="Modern.TEntry", width=30)
    user_entry.insert(0, USERNAME)
    user_entry.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
    
    # Directorio de sesiones
    ttk.Label(content_frame, text="Dir. Sesiones:", style="Modern.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
    sessions_entry = ttk.Entry(content_frame, style="Modern.TEntry", width=30)
    sessions_entry.insert(0, SESSIONS_DIR)
    sessions_entry.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
    
    content_frame.columnconfigure(1, weight=1)
    
    # Botones
    button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
    button_frame.pack(fill=tk.X, pady=(20, 0))
    
    ttk.Button(button_frame, text="Guardar", 
              style="Primary.TButton").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Cancelar", 
              style="Modern.TButton", 
              command=settings_window.destroy).pack(side=tk.RIGHT)

def show_help():
    """Mostrar ayuda"""
    help_window = tk.Toplevel(root)
    help_window.title("📖 Manual de Usuario")
    help_window.geometry("700x500")
    help_window.configure(bg=COLORS['bg_primary'])
    
    help_window.transient(root)
    help_window.grab_set()
    
    main_frame = ttk.Frame(help_window, style="Modern.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    title_label = ttk.Label(main_frame, text="📖 Manual de Usuario", style="Title.TLabel")
    title_label.pack(pady=(0, 20))
    
    help_text = scrolledtext.ScrolledText(
        main_frame,
        bg=COLORS['bg_secondary'],
        fg=COLORS['text_primary'],
        font=('Segoe UI', 10),
        wrap=tk.WORD
    )
    help_text.pack(fill=tk.BOTH, expand=True)
    
    help_content = """
LAZYOWN C2 BLACK BASALT - MANUAL DE USUARIO

ATAJOS DE TECLADO:
• Ctrl+L: Conectar al servidor C2
• Ctrl+U: Subir archivo
• Ctrl+E: Exportar logs
• Ctrl+Q: Salir
• F5: Actualizar beacons

FUNCIONES PRINCIPALES:

1. GESTIÓN DE BEACONS
   - Los beacons aparecen como cards en la parte superior
   - Haz clic en un beacon para abrir su consola
   - El indicador verde muestra beacons activos

2. CONSOLAS
   - Cada beacon tiene su propia pestaña de consola
   - Usa el Event Log para ver toda la actividad
   - Los comandos se muestran en azul, las respuestas en verde

3. DATOS
   - Pestaña Banners: Información de servicios detectados
   - Pestaña Implantes: Configuración de implantes
   - Pestaña Access Log: Registro de accesos al sistema

4. HERRAMIENTAS
   - Subir Archivo: Transfiere archivos a beacons
   - Gestionar Payloads: Genera nuevos payloads
   - Estadísticas: Ver información del sistema

COLORES:
• Verde: Éxito/Activo
• Rojo: Error/Inactivo  
• Azul: Comandos/Acciones
• Amarillo: Advertencias
    """
    
    help_text.insert(1.0, help_content)
    help_text.config(state=tk.DISABLED)
    
    ttk.Button(main_frame, text="Cerrar", 
              style="Modern.TButton", 
              command=help_window.destroy).pack(pady=(20, 0))

def show_about():
    """Mostrar información del programa"""
    messagebox.showinfo(
        "Acerca de LazyOwn C2 Black Basalt GUI",
        "LazyOwn C2 - Black Basalt Modern Interface\n\n"
        "Versión: 2.0\n"
        "Desarrollado por: LazyOwn Team\n\n"
        "Una interfaz moderna para el LazyOwn RedTeam Framework\n"
        "LazyOwn Command & Control BLACK BASALT ©.\n\n"
        "© 2025 LazyOwn RedTeam Framework Project"
    )

def on_closing():
    """Manejar cierre de aplicación"""
    if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
        stop_polling()
        root.destroy()

# === FUNCIÓN PRINCIPAL ===
def main():
    """Función principal"""
    global root
    
    # Verificar dependencias
    try:
        from PIL import Image, ImageTk
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError as e:
        messagebox.showerror("Error", f"Dependencia faltante: {e}")
        return
    
    # Crear y ejecutar interfaz
    root = create_modern_ui()
    root.mainloop()

if __name__ == "__main__":
    main()