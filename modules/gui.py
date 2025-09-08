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
        self.client_id = client_id
        self.command_history = []  # Lista de comandos históricos
        self.history_index = -1    # Índice actual en el historial (-1 = escribiendo un nuevo comando)
        self.load_command_history() # Cargar historial desde el archivo .log

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

        # Bind Up/Down arrow keys for command history
        self.entry.bind('<Up>', self.navigate_history_up)
        self.entry.bind('<Down>', self.navigate_history_down)

        # Configurar tags para colores
        self.output.tag_config("command", foreground=COLORS['accent_blue'])
        self.output.tag_config("response", foreground=COLORS['text_success'])
        self.output.tag_config("error", foreground=COLORS['text_error'])
        self.output.tag_config("warning", foreground=COLORS['text_warning'])

    def load_command_history(self):
        """Carga el historial de comandos desde el archivo .log del cliente"""
        if not self.client_id:
            return

        log_file_path = os.path.join(LOG_DIR, f"{self.client_id}.log")
        if not os.path.exists(log_file_path):
            return

        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Saltar la cabecera
                for row in reader:
                    if len(row) > 9:  # Asegurarse de que la columna 'command' existe (índice 9)
                        command = row[9].strip()
                        if command and command.lower() not in ['none', 'null', '']:
                            # Evitar duplicados consecutivos
                            if not self.command_history or self.command_history[-1] != command:
                                self.command_history.append(command)
        except Exception as e:
            print(f"Error loading command history for {self.client_id}: {e}")

    def send_command(self, client_id):
        cmd = self.entry.get().strip()
        if not cmd: 
            return

        # Agregar el comando al historial si no es un duplicado del último
        if not self.command_history or self.command_history[-1] != cmd:
            self.command_history.append(cmd)
        self.history_index = len(self.command_history)  # Resetear índice al final

        try:
            # Mostrar comando en la consola
            self.add_text(f"> {cmd}", "command")

            # Enviar comando al servidor
            if client_id != "GLOBAL":
                requests.post(f"{API_BASE}/issue_command", 
                            data={"client_id": client_id, "command": cmd}, verify=False)

            # Limpiar el campo de entrada
            self.entry.delete(0, tk.END)

        except Exception as e:
            self.add_text(f"[ERROR] {str(e)}", "error")

    def navigate_history_up(self, event):
        """Navegar hacia arriba en el historial de comandos"""
        if not self.command_history:
            return "break"  # Evitar que la tecla haga algo más

        if self.history_index <= 0:
            self.history_index = 0
            return "break"

        self.history_index -= 1
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.command_history[self.history_index])
        return "break"  # Prevenir el comportamiento por defecto de la tecla

    def navigate_history_down(self, event):
        """Navegar hacia abajo en el historial de comandos"""
        if not self.command_history:
            return "break"

        if self.history_index >= len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.entry.delete(0, tk.END)  # Limpiar para escribir un nuevo comando
            return "break"

        self.history_index += 1
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.command_history[self.history_index])
        return "break"

    def add_text(self, text, tag=None):
        self.output.insert(tk.END, f"{text}\n", tag)
        self.output.see(tk.END)

class ImplantCard(ttk.Frame):
    def __init__(self, parent, client_id, on_select=None):
        super().__init__(parent, style="Card.TFrame")
        self.client_id = client_id
        self.on_select = on_select
        self.latest_info = {}  # Almacenar la última info conocida

        # Cargar la última información del log
        self.load_latest_client_info()

        # Main content
        content_frame = ttk.Frame(self, style="Modern.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- Header con icono y nombre ---
        header_frame = ttk.Frame(content_frame, style="Modern.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        os_image = self.load_os_image(client_id)
        if os_image:
            icon_label = ttk.Label(header_frame, image=os_image)
            icon_label.image = os_image
        else:
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
        self.update_status_indicator()

        # --- Información Detallada (NUEVO) ---
        info_frame = ttk.Frame(content_frame, style="Modern.TFrame")
        info_frame.pack(fill=tk.X, pady=(5, 10))

        # Hostname
        hostname = self.latest_info.get('hostname', 'N/A')
        ttk.Label(info_frame, text=f"💻 Host: {hostname}", 
                 style="Status.TLabel", foreground=COLORS['text_secondary']).pack(anchor=tk.W)

        # IP y Usuario en la misma línea
        ip_user_frame = ttk.Frame(info_frame, style="Modern.TFrame")
        ip_user_frame.pack(fill=tk.X)
        ip = self.latest_info.get('ips', 'N/A')
        user = self.latest_info.get('user', 'N/A')
        ttk.Label(ip_user_frame, text=f"🌐 IP: {ip}", 
                 style="Status.TLabel", foreground=COLORS['text_secondary']).pack(side=tk.LEFT)
        ttk.Label(ip_user_frame, text=f"👤 User: {user}", 
                 style="Status.TLabel", foreground=COLORS['text_secondary']).pack(side=tk.LEFT, padx=(10, 0))

        # PID y Directorio de Trabajo
        pid = self.latest_info.get('pid', 'N/A')
        pwd = self.latest_info.get('result_pwd', 'N/A')
        ttk.Label(info_frame, text=f"🆔 PID: {pid}", 
                 style="Status.TLabel", foreground=COLORS['text_secondary']).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"📁 PWD: {pwd}", 
                 style="Status.TLabel", foreground=COLORS['accent_green']).pack(anchor=tk.W)

        # --- Última Actividad ---
        last_activity = self.latest_info.get('last_activity', 'Desconocido')
        ttk.Label(info_frame, text=f"⏱️ Última actividad: {last_activity}", 
                 style="Status.TLabel", foreground=COLORS['text_warning']).pack(anchor=tk.W)
        # --- Información del Implant (desde JSON) ---
        implant_id = self.latest_info.get('implant_id', 'N/A')
        created = self.latest_info.get('created', 'N/A')
        ttk.Label(info_frame, text=f"🆔 ID Implant: {implant_id}", 
                style="Status.TLabel", foreground=COLORS['text_secondary']).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"📅 Creado: {created}", 
         style="Status.TLabel", foreground=COLORS['text_secondary']).pack(anchor=tk.W)
        # --- Botones de acción ---
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

    def load_latest_client_info(self):
        """Carga la información más reciente del cliente desde su archivo .log Y su archivo .json de configuración."""
        self.latest_info = {}  # Reiniciar

        # --- Primero, cargar info del .log (como antes) ---
        log_file_path = os.path.join(LOG_DIR, f"{self.client_id}.log")
        if os.path.exists(log_file_path):
            try:
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        last_line = lines[-1].strip()
                        if last_line:
                            reader = csv.reader([last_line])
                            row = next(reader)
                            if len(row) >= 9:
                                self.latest_info.update({
                                    'os': row[1] if len(row) > 1 else 'N/A',
                                    'pid': row[2] if len(row) > 2 else 'N/A',
                                    'hostname': row[3] if len(row) > 3 else 'N/A',
                                    'ips': row[4] if len(row) > 4 else 'N/A',
                                    'user': row[5] if len(row) > 5 else 'N/A',
                                    'discovered_ips': row[6] if len(row) > 6 else '',
                                    'result_portscan': row[7] if len(row) > 7 else '',
                                    'result_pwd': row[8] if len(row) > 8 else 'N/A',
                                    'last_activity': datetime.fromtimestamp(os.path.getmtime(log_file_path)).strftime('%H:%M:%S')
                                })
            except Exception as e:
                print(f"Error loading latest info from .log for {self.client_id}: {e}")

        # --- SEGUNDO, cargar info del archivo JSON de configuración ---
        config_file_path = os.path.join(LOG_DIR, f"implant_config_{self.client_id}.json")
        if os.path.exists(config_file_path):
            try:
                with open(config_file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    # Combinar con la info del log, priorizando el JSON si hay conflicto
                    self.latest_info.update({
                        'implant_id': config_data.get('id', 'N/A'),
                        'binary_path': config_data.get('binary', 'N/A'),
                        'url_binary': config_data.get('url_binary', 'N/A'),
                        'rhost': config_data.get('rhost', 'N/A'),
                        'user_agent': config_data.get('user_agent', 'N/A'),
                        'created': config_data.get('created', 'N/A'),
                        'sleep': config_data.get('sleep', 'N/A'),
                        'maleable_route': config_data.get('maleable_route', 'N/A')
                    })
            except Exception as e:
                print(f"Error loading config from JSON for {self.client_id}: {e}")

    def update_status_indicator(self):
        """Actualiza el indicador de estado basado en la última actividad"""
        # Lógica simple: si el archivo se modificó en los últimos 60 segundos, está activo
        log_file_path = os.path.join(LOG_DIR, f"{self.client_id}.log")
        if os.path.exists(log_file_path):
            last_modified = os.path.getmtime(log_file_path)
            is_active = (time.time() - last_modified) < 60
            color = COLORS['accent_green'] if is_active else COLORS['accent_yellow']
        else:
            color = COLORS['accent_red']

        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 10, 10, fill=color, outline=color)

    
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
        current_clients = set(data.get("connected_clients", []))  # Clientes reportados por el servidor
        existing_clients = set(beacon_tabs.keys())  # Clientes ya presentes en la GUI

        # --- NUEVA LÓGICA: Determinar beacons "recién conectados" ---
        # Definimos un umbral de tiempo (ej. 30 segundos)
        RECENT_THRESHOLD_SECONDS = 30
        current_time = time.time()
        truly_new_beacons = set()

        for client_id in current_clients:
            log_file_path = os.path.join(LOG_DIR, f"{client_id}.log")
            if os.path.exists(log_file_path):
                # Obtener el tiempo de la última modificación del archivo .log
                last_modified_time = os.path.getmtime(log_file_path)
                # Si el archivo se modificó hace menos del umbral, es un beacon "recién activo"
                if (current_time - last_modified_time) <= RECENT_THRESHOLD_SECONDS:
                    # Solo lo consideramos "nuevo" si no estaba ya en la GUI
                    if client_id not in existing_clients:
                        truly_new_beacons.add(client_id)
            else:
                # Si el archivo de log no existe, lo tratamos como nuevo (primera conexión)
                if client_id not in existing_clients:
                    truly_new_beacons.add(client_id)

        # Limpiar contenedor de implants
        for widget in implants_container.winfo_children():
            widget.destroy()

        # Crear cards para cada cliente
        for i, client in enumerate(current_clients):
            card = ImplantCard(implants_container, client, select_client)
            card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")

        # Configurar columnas
        implants_container.columnconfigure(0, weight=1)
        implants_container.columnconfigure(1, weight=1)

        # Mostrar notificación de éxito general
        show_notification(f"✓ {len(current_clients)} implantes activos", "success")

        # Mostrar notificación SOLO para beacons verdaderamente nuevos/recién activos
        for beacon in truly_new_beacons:
            show_notification(f"✨ ¡Nuevo beacon conectado: {beacon}!", "success")

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
    """Crea una nueva pestaña para un beacon, con subpestañas de Consola e Intel."""
    frame = ttk.Frame(console_notebook, style="Modern.TFrame")
    console_notebook.add(frame, text=f"🔗 {client_id}")

    # Crear un notebook interno para este beacon específico
    beacon_inner_notebook = ttk.Notebook(frame, style="Modern.TNotebook")
    beacon_inner_notebook.pack(fill=tk.BOTH, expand=True)

    # Pestaña 1: Consola
    console_frame = ttk.Frame(beacon_inner_notebook, style="Modern.TFrame")
    console = ModernConsole(console_frame, client_id)
    console.pack(fill=tk.BOTH, expand=True)
    beacon_inner_notebook.add(console_frame, text="💬 Consola")

    # Pestaña 2: Intel (¡NUEVO!)
    intel_frame = ttk.Frame(beacon_inner_notebook, style="Modern.TFrame")
    create_intel_tab(intel_frame, client_id)
    beacon_inner_notebook.add(intel_frame, text="🔍 Intel")

    # Guardar referencias
    beacon_tabs[client_id] = frame
    frame.console = console  # Mantener referencia a la consola
    frame.intel_frame = intel_frame  # Referencia a la pestaña de intel (opcional)

    return frame

def load_implant_config(client_id):
    """Carga la configuración del implant desde el archivo JSON."""
    config_file_path = os.path.join(LOG_DIR, f"implant_config_{client_id}.json")
    if not os.path.exists(config_file_path):
        return None

    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading implant config for {client_id}: {e}")
        return None
        
def create_intel_tab(parent, client_id):
    """Crea la pestaña de Inteligencia/Recon para un beacon específico."""
    # Frame principal con scroll
    canvas = tk.Canvas(parent, bg=COLORS['bg_primary'], highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="Modern.TFrame")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Cargar datos del log
    intel_data = load_intel_data(client_id)

    # Sección: Hosts Descubiertos
    if intel_data.get('discovered_ips'):
        create_section_header(scrollable_frame, "🌐 Hosts Descubiertos")
        for ip in intel_data['discovered_ips']:
            ttk.Label(scrollable_frame, text=f"• {ip}", style="Modern.TLabel").pack(anchor=tk.W, padx=20, pady=2)

    # Sección: Escaneo de Puertos
    if intel_data.get('portscan_results'):
        create_section_header(scrollable_frame, "🚪 Puertos Abiertos")
        for host, ports in intel_data['portscan_results'].items():
            ttk.Label(scrollable_frame, text=f"{host}:", style="Title.TLabel", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=20, pady=(5, 0))
            for port, status in ports.items():
                color = COLORS['text_success'] if status == 'open' else COLORS['text_error']
                ttk.Label(scrollable_frame, text=f"  • {port}: {status}", foreground=color, style="Modern.TLabel").pack(anchor=tk.W, padx=40)

    # Sección: Software Útil
    if intel_data.get('useful_software'):
        create_section_header(scrollable_frame, "🛠️ Software Detectado")
        for sw in intel_data['useful_software']:
            ttk.Label(scrollable_frame, text=f"• {sw}", style="Modern.TLabel").pack(anchor=tk.W, padx=20, pady=2)

    # Sección: Configuración de Red
    if intel_data.get('netconfig'):
        create_section_header(scrollable_frame, "📡 Configuración de Red")
        net_text = scrolledtext.ScrolledText(scrollable_frame, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], font=('Consolas', 9), height=10, wrap=tk.NONE)
        net_text.insert(tk.END, intel_data['netconfig'])
        net_text.config(state=tk.DISABLED)
        net_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
    # Sección: Configuración del Implant (desde JSON)
    config_data = load_implant_config(client_id)  # <-- NUEVA FUNCIÓN QUE DEFINIREMOS
    if config_data:
        create_section_header(scrollable_frame, "⚙️ Configuración del Implant")
        details_frame = ttk.Frame(scrollable_frame, style="Modern.TFrame")
        details_frame.pack(fill=tk.X, padx=20, pady=5)

        # Crear una grilla de 2 columnas para los pares clave-valor
        row = 0
        col = 0
        max_cols = 2  # Número de columnas
        for key, value in config_data.items():
            if key in ['binary', 'url_binary', 'user_agent', 'payload']:  # Campos largos
                ttk.Label(details_frame, text=f"{key}:", style="Modern.TLabel", font=('Segoe UI', 9, 'bold')).grid(row=row, column=col, sticky=tk.W, padx=(0, 5), pady=2)
                col += 1
                text_widget = tk.Text(details_frame, height=2, width=40, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], font=('Consolas', 9), wrap=tk.WORD)
                text_widget.insert(tk.END, str(value))
                text_widget.config(state=tk.DISABLED, relief='flat', borderwidth=0)
                text_widget.grid(row=row, column=col, sticky=tk.EW, padx=(0, 10), pady=2)
                row += 1
                col = 0
            else:
                ttk.Label(details_frame, text=f"{key}:", style="Modern.TLabel", font=('Segoe UI', 9, 'bold')).grid(row=row, column=col, sticky=tk.W, padx=(0, 5), pady=2)
                ttk.Label(details_frame, text=str(value), style="Modern.TLabel").grid(row=row, column=col+1, sticky=tk.W, padx=(0, 10), pady=2)
                col += 2
                if col >= max_cols * 2:
                    col = 0
                    row += 1

        # Hacer que las columnares se expandan
        for i in range(max_cols * 2):
            details_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
def create_section_header(parent, title):
    """Crea un encabezado de sección para la pestaña de Intel."""
    frame = ttk.Frame(parent, style="Modern.TFrame")
    frame.pack(fill=tk.X, pady=(15, 5))
    ttk.Label(frame, text=title, style="Title.TLabel", font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
    ttk.Separator(frame, orient='horizontal').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

def load_intel_data(client_id):
    """Extrae y parsea datos de inteligencia del archivo .log del cliente."""
    data = {
        'discovered_ips': set(),
        'portscan_results': {},
        'useful_software': set(),
        'netconfig': ''
    }

    log_file_path = os.path.join(LOG_DIR, f"{client_id}.log")
    if not os.path.exists(log_file_path):
        return data

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Saltar cabecera

            for row in reader:
                if len(row) < 11:
                    continue

                command = row[9].strip().lower()
                output = row[10].strip()

                # Parsear discovered_ips (del campo row[6])
                if len(row) > 6 and row[6]:
                    ips = [ip.strip() for ip in row[6].split(',')]
                    data['discovered_ips'].update(ips)

                # Parsear result_portscan (del campo row[7])
                if len(row) > 7 and row[7]:
                    # Suponiendo formato "port:status" o "ip:port:status"
                    entries = row[7].split(',')
                    for entry in entries:
                        if ':' in entry:
                            parts = entry.split(':')
                            if len(parts) >= 2:
                                # Asignar al host actual (row[4]) o a 'localhost'
                                host = row[4] if len(row) > 4 and row[4] else 'localhost'
                                port = parts[0]
                                status = parts[1] if len(parts) > 1 else 'unknown'
                                if host not in data['portscan_results']:
                                    data['portscan_results'][host] = {}
                                data['portscan_results'][host][port] = status

                # Detectar software útil desde el comando 'softenum'
                if command == 'softenum:' and 'Useful software:' in output:
                    software_list = output.split('Useful software: ')[-1]
                    sw_items = [sw.strip() for sw in software_list.split(',')]
                    data['useful_software'].update(sw_items)

                # Guardar la última configuración de red
                if command == 'netconfig:':
                    data['netconfig'] = output

    except Exception as e:
        print(f"Error loading intel data for {client_id}: {e}")

    # Convertir sets a listas ordenadas para la UI
    data['discovered_ips'] = sorted(list(data['discovered_ips']))
    data['useful_software'] = sorted(list(data['useful_software']))

    return data

def create_section_header(parent, title):
    """Crea un encabezado de sección para la pestaña de Intel."""
    frame = ttk.Frame(parent, style="Modern.TFrame")
    frame.pack(fill=tk.X, pady=(15, 5))
    ttk.Label(frame, text=title, style="Title.TLabel", font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
    ttk.Separator(frame, orient='horizontal').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

def load_intel_data(client_id):
    """Extrae y parsea datos de inteligencia del archivo .log del cliente."""
    data = {
        'discovered_ips': set(),
        'portscan_results': {},
        'useful_software': set(),
        'netconfig': ''
    }

    log_file_path = os.path.join(LOG_DIR, f"{client_id}.log")
    if not os.path.exists(log_file_path):
        return data

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Saltar cabecera

            for row in reader:
                if len(row) < 11:
                    continue

                command = row[9].strip().lower()
                output = row[10].strip()

                # Parsear discovered_ips (del campo row[6])
                if len(row) > 6 and row[6]:
                    ips = [ip.strip() for ip in row[6].split(',')]
                    data['discovered_ips'].update(ips)

                # Parsear result_portscan (del campo row[7])
                if len(row) > 7 and row[7]:
                    # Suponiendo formato "ip:port:status" o "port:status"
                    entries = row[7].split(',')
                    for entry in entries:
                        if ':' in entry:
                            parts = entry.split(':')
                            if len(parts) >= 2:
                                port = parts[0]
                                status = parts[1]
                                # Asignar al host actual (row[4]) o a 'localhost'
                                host = row[4] if len(row) > 4 else 'localhost'
                                if host not in data['portscan_results']:
                                    data['portscan_results'][host] = {}
                                data['portscan_results'][host][port] = status

                # Detectar software útil desde el comando 'softenum'
                if command == 'softenum:' and 'Useful software:' in output:
                    software_list = output.split('Useful software: ')[-1]
                    sw_items = [sw.strip() for sw in software_list.split(',')]
                    data['useful_software'].update(sw_items)

                # Guardar la última configuración de red
                if command == 'netconfig:':
                    data['netconfig'] = output

    except Exception as e:
        print(f"Error loading intel data for {client_id}: {e}")

    # Convertir sets a listas ordenadas para la UI
    data['discovered_ips'] = sorted(list(data['discovered_ips']))
    data['useful_software'] = sorted(list(data['useful_software']))

    return data

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
                        command = row[9].strip() if len(row) > 9 else "N/A"
                        # ... (condición para evitar outputs vacíos)
                        event_queue.put({
                            'type': 'command_output',
                            'client_id': client_id,
                            'command': row[9].strip() if len(row) > 9 else "N/A",  # <-- AÑADIR ESTA LÍNEA
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
            show_notification(f"[{event['client_id']}] << {event['command']} -> {event['output']}", "info")
            
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
                               highlightthickness=0, height=250)
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
    tools_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
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
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    title_label = ttk.Label(main_frame, text="📊 Estadísticas del Sistema", style="Title.TLabel")
    title_label.pack(pady=(0, 20))
    
    # Estadísticas básicas
    stats_frame = ttk.Frame(main_frame, style="Card.TFrame")
    stats_frame.pack(fill=tk.BOTH, expand=True)
    
    content_frame = ttk.Frame(stats_frame, style="Modern.TFrame")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
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
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    title_label = ttk.Label(main_frame, text="🔧 Configuración", style="Title.TLabel")
    title_label.pack(pady=(0, 20))
    
    # Configuraciones
    config_frame = ttk.Frame(main_frame, style="Card.TFrame")
    config_frame.pack(fill=tk.BOTH, expand=True)
    
    content_frame = ttk.Frame(config_frame, style="Modern.TFrame")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
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
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
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