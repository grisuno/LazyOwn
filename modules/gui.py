import csv
import json
import logging
import os
import queue
import re
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext, ttk

import requests
from PIL import Image, ImageTk
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

_LAZYOWN_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_payload_config():
    payload_path = os.path.join(_LAZYOWN_BASE, "payload.json")
    try:
        with open(payload_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


_PAYLOAD = _load_payload_config()

API_BASE = os.environ.get(
    "LAZYOWN_C2_URL",
    f"https://{_PAYLOAD.get('lhost', '127.0.0.1')}:{_PAYLOAD.get('c2_port', 4444)}",
)
USERNAME = os.environ.get("LAZYOWN_C2_USER", _PAYLOAD.get("c2_user", "lazyown"))
PASSWORD = os.environ.get("LAZYOWN_C2_PASS", _PAYLOAD.get("c2_pass", "lazyown"))
SESSIONS_DIR = os.path.join(_LAZYOWN_BASE, "sessions")
LOG_DIR = SESSIONS_DIR

# === GLOBAL VARIABLES ===
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
# === NEW VARIABLES FOR TABLE VIEW ===
global_view_mode = "card"  # 'card' o 'table'
toggle_view_btn = None
implants_frame = None
main_container = None
# === COLORS AND THEME ===
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

# === ENHANCED STYLES ===
def setup_modern_theme():
    style = ttk.Style()
    style.theme_use("clam")

    # Base configurations
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


# === CUSTOM WIDGETS ===
class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Modern.TFrame")
        self.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

        self.status_label = ttk.Label(self, text="Disconnected", style="Status.TLabel")
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

        self.title_label = ttk.Label(header_frame, text="Data", style="Title.TLabel")
        self.title_label.pack(side=tk.LEFT)

        self.refresh_btn = ttk.Button(header_frame, text="⟳ Refresh",
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
            for item in self.tree.get_children():
                self.tree.delete(item)
            data = self.data_loader()
            for item in data:
                if isinstance(item, dict):
                    values = [item.get(col, "") for col in self.tree["columns"]]
                elif isinstance(item, str):
                    values = [item] + [""] * (len(self.tree["columns"]) - 1)
                else:
                    values = [str(item)] + [""] * (len(self.tree["columns"]) - 1)
                self.tree.insert("", tk.END, values=values)

    def set_title(self, title):
        self.title_label.config(text=title)

class ModernConsole(ttk.Frame):
    def __init__(self, parent, client_id=None):
        super().__init__(parent, style="Modern.TFrame")
        self.client_id = client_id
        self.command_history = []  # Command history list
        self.history_index = -1    # Current history index (-1 = typing a new command)
        self.load_command_history() # Load history from .log file

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

        # Input frame with improved design
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
        self.send_btn = ttk.Button(input_frame, text="Send",
                                  style="Primary.TButton",
                                  command=lambda: self.send_command(client_id))
        self.send_btn.pack(side=tk.RIGHT)

        # Bind Enter key
        self.entry.bind('<Return>', lambda e: self.send_command(client_id))

        # Bind Up/Down arrow keys for command history
        self.entry.bind('<Up>', self.navigate_history_up)
        self.entry.bind('<Down>', self.navigate_history_down)

        # Configure tags for colors
        self.output.tag_config("command", foreground=COLORS['accent_blue'])
        self.output.tag_config("response", foreground=COLORS['text_success'])
        self.output.tag_config("error", foreground=COLORS['text_error'])
        self.output.tag_config("warning", foreground=COLORS['text_warning'])

    def load_command_history(self):
        """Loads the command history from the client's .log file."""
        if not self.client_id:
            return

        log_file_path = os.path.join(LOG_DIR, f"{self.client_id}.log")
        if not os.path.exists(log_file_path):
            return

        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                for row in reader:
                    if len(row) > 9:  # Ensure the 'command' column exists (index 9)
                        command = row[9].strip()
                        if command and command.lower() not in ['none', 'null', '']:
                            # Avoid consecutive duplicates
                            if not self.command_history or self.command_history[-1] != command:
                                self.command_history.append(command)
        except Exception as e:
            print(f"Error loading command history for {self.client_id}: {e}")

    def send_command(self, client_id):
        cmd = self.entry.get().strip()
        if not cmd:
            return

        # Add command to history if not a duplicate of the last
        if not self.command_history or self.command_history[-1] != cmd:
            self.command_history.append(cmd)
        self.history_index = len(self.command_history)  # Reset index to end

        try:
            # Show command in the console
            self.add_text(f"> {cmd}", "command")

            # Send command to server
            if client_id != "GLOBAL":
                requests.post(f"{API_BASE}/issue_command",
                            data={"client_id": client_id, "command": cmd}, verify=False)

            # Clear the input field
            self.entry.delete(0, tk.END)

        except Exception as e:
            self.add_text(f"[ERROR] {str(e)}", "error")

    def navigate_history_up(self, event):
        """Navigate up in the command history."""
        if not self.command_history:
            return "break"  # Prevent the key from doing anything else

        if self.history_index <= 0:
            self.history_index = 0
            return "break"

        self.history_index -= 1
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.command_history[self.history_index])
        return "break"  # Prevent default key behavior

    def navigate_history_down(self, event):
        """Navigate down in the command history."""
        if not self.command_history:
            return "break"

        if self.history_index >= len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.entry.delete(0, tk.END)  # Clear for new command
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
        self.card_content = ttk.Frame(self, style="Modern.TFrame")
        self.card_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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

        # --- Detailed Information (NEW) ---
        info_frame = ttk.Frame(content_frame, style="Modern.TFrame")
        info_frame.pack(fill=tk.X, pady=(5, 10))

        # Hostname
        hostname = self.latest_info.get('hostname', 'N/A')
        ttk.Label(info_frame, text=f"💻 Host: {hostname}",
                 style="Status.TLabel", foreground=COLORS['text_secondary']).pack(anchor=tk.W)

        # IP and User on the same line
        ip_user_frame = ttk.Frame(info_frame, style="Modern.TFrame")
        ip_user_frame.pack(fill=tk.X)
        ip = self.latest_info.get('ips', 'N/A')
        user = self.latest_info.get('user', 'N/A')
        ttk.Label(ip_user_frame, text=f"🌐 IP: {ip}",
                 style="Status.TLabel", foreground=COLORS['text_secondary']).pack(side=tk.LEFT)
        ttk.Label(ip_user_frame, text=f"👤 User: {user}",
                 style="Status.TLabel", foreground=COLORS['text_secondary']).pack(side=tk.LEFT, padx=(10, 0))

        # PID and Working Directory
        pid = self.latest_info.get('pid', 'N/A')
        pwd = self.latest_info.get('result_pwd', 'N/A')
        ttk.Label(info_frame, text=f"🆔 PID: {pid}",
                 style="Status.TLabel", foreground=COLORS['text_secondary']).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"📁 PWD: {pwd}",
                 style="Status.TLabel", foreground=COLORS['accent_green']).pack(anchor=tk.W)

        # --- Last Activity ---
        last_activity = self.latest_info.get('last_activity', 'Unknown')
        ttk.Label(info_frame, text=f"⏱️ Last activity: {last_activity}",
                 style="Status.TLabel", foreground=COLORS['text_warning']).pack(anchor=tk.W)
        # --- Implant Information (from JSON) ---
        implant_id = self.latest_info.get('implant_id', 'N/A')
        created = self.latest_info.get('created', 'N/A')
        ttk.Label(info_frame, text=f"🆔 ID Implant: {implant_id}",
                style="Status.TLabel", foreground=COLORS['text_secondary']).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"📅 Created: {created}",
         style="Status.TLabel", foreground=COLORS['text_secondary']).pack(anchor=tk.W)
        # --- Action buttons ---
        button_frame = ttk.Frame(content_frame, style="Modern.TFrame")
        button_frame.pack(fill=tk.X)
        ttk.Button(button_frame, text="Console", style="Primary.TButton",
                  command=self.open_console).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Files", style="Modern.TButton",
                  command=self.open_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Processes", style="Modern.TButton",
                  command=self.open_processes).pack(side=tk.LEFT)
        self.view_mode = "card"  # initially in card mode
        self.toggle_btn = ttk.Button(button_frame, text="📋 Table",
                                    style="Modern.TButton",
                                    command=self.toggle_view)
        print(f"[DEBUG] Toggle view: {self.view_mode} -> {'table' if self.view_mode == 'card' else 'card'}")
        self.toggle_btn.pack(side=tk.RIGHT)
        # Click on the entire card
        self.bind("<Button-1>", self.on_card_click)
        content_frame.bind("<Button-1>", self.on_card_click)
        for child in content_frame.winfo_children():
            child.bind("<Button-1>", self.on_card_click)

    def load_latest_client_info(self):
        """Loads the latest client info from its .log file AND its JSON config file."""
        self.latest_info = {}  # Reset

        # --- First, load info from .log (as before) ---
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

        # --- SECOND, load info from JSON config file ---
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
                        'malleable_route': config_data.get('malleable_route', 'N/A')
                    })
            except Exception as e:
                print(f"Error loading config from JSON for {self.client_id}: {e}")

    def update_status_indicator(self):
        """Updates the status indicator based on last activity."""
        # Simple logic: if file was modified in the last 60 seconds, it is active
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

            # Debug: check the path
            print(f"Attempting to load: {image_path}")
            print(f"File exists: {os.path.exists(image_path)}")

            # Check if the file exists
            if os.path.exists(image_path):
                # Load and resize image
                img = Image.open(image_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                print(f"Image loaded successfully: {image_path}")
                return ImageTk.PhotoImage(img)
            else:
                print(f"File not found: {image_path}")
                return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def toggle_view(self):
        if self.view_mode == "card":
            self.show_table_view()
            self.view_mode = "table"
            self.toggle_btn.config(text="🖼️ Card")
        else:
            self.show_card_view()
            self.view_mode = "card"
            self.toggle_btn.config(text="📋 Table")

    def show_table_view(self):
        # 1. Hide card
        self.card_content.pack_forget()

        # 2. Create table only once
        if not hasattr(self, 'table_frame'):
            self.table_frame = ttk.Frame(self, style="Card.TFrame")
            self.tree = ttk.Treeview(
                self.table_frame,
                columns=("Host", "IP", "User", "Url", "Rhost", "Created"),
                show="headings",
                height=1
            )
            self.tree.heading("Host", text="Host")
            self.tree.heading("IP", text="IP")
            self.tree.heading("User", text="User")
            self.tree.heading("Url", text="Url")
            self.tree.heading("Rhost", text="Rhost")
            self.tree.heading("Created", text="Created")
            # Visible colors
            style = ttk.Style()
            style.configure("Table.Treeview",
                            background=COLORS['bg_secondary'],
                            foreground=COLORS['text_primary'],
                            fieldbackground=COLORS['bg_secondary'])
            self.tree.config(style="Table.Treeview")

            self.tree.pack(fill=tk.X, padx=10, pady=10)

        # 3. Clear and insert row
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.insert("", tk.END, values=(
            self.latest_info.get('hostname', 'N/A'),
            self.latest_info.get('ips', 'N/A'),
            self.latest_info.get('user', 'N/A'),
            self.latest_info.get('url_binary', 'N/A'),
            self.latest_info.get('rhost', 'N/A'),
            self.latest_info.get('created', 'N/A')
        ))

        # 4. Show frame!
        self.table_frame.pack(fill=tk.X)
        self.table_frame.update()  # <- force render

    def show_card_view(self):
        if hasattr(self, 'table_frame'):
            self.table_frame.pack_forget()
        self.card_content.pack(fill=tk.BOTH, expand=True)

# === IMPROVED API FUNCTIONS ===
def login():
    global connection_status, status_bar
    try:
        resp = requests.post(f"{API_BASE}/login",
                           data={"username": USERNAME, "password": PASSWORD},
                           verify=False, timeout=5)
        if resp.status_code == 200:
            connection_status = True
            status_bar.update_status("Connected to C2", True)
            show_notification("✓ Connected to C2 successfully", "success")
            refresh_clients()
            start_polling()
        else:
            connection_status = False
            status_bar.update_status("Login failed", False)
            show_notification("✗ Login error", "error")
    except Exception as e:
        connection_status = False
        status_bar.update_status(f"Connection error: {str(e)}", False)
        show_notification(f"✗ Could not connect: {str(e)}", "error")

def show_notification(message, type="info"):
    """Show system notification."""
    colors = {
        "success": COLORS['text_success'],
        "error": COLORS['text_error'],
        "warning": COLORS['text_warning'],
        "info": COLORS['text_primary']
    }

    if events_text:
        timestamp = datetime.now().strftime("%H:%M:%S")
        events_text.insert(tk.END, f"[{timestamp}] {message}\n")
        events_text.tag_add(type, "end-2c linestart", "end-1c")
        events_text.tag_config(type, foreground=colors.get(type, COLORS['text_primary']))
        events_text.see(tk.END)

def refresh_clients():
    # Clear only the content
    for widget in implants_frame.winfo_children():
        widget.destroy()

    try:
        resp = requests.get(f"{API_BASE}/get_connected_clients", verify=False, timeout=5)
        data = resp.json()
        clients = data.get("connected_clients", [])

        for client in clients:
            card = ImplantCard(implants_frame, client, select_client)
            card.pack(fill=tk.X, padx=5, pady=5)

        show_notification(f"✓ {len(clients)} active implants", "success")

    except Exception as e:
        show_notification(f"✗ Error refreshing clients: {str(e)}", "error")

def select_client(client_id):
    global current_beacon
    current_beacon = client_id

    # Create or select beacon tab
    if client_id not in beacon_tabs:
        create_beacon_tab(client_id)

    console_notebook.select(beacon_tabs[client_id])
    show_notification(f"→ Beacon selected: {client_id}", "info")

def create_beacon_tab(client_id):
    """Creates a new tab for a beacon, with Console and Intel sub-tabs."""
    frame = ttk.Frame(console_notebook, style="Modern.TFrame")
    console_notebook.add(frame, text=f"🔗 {client_id}")

    # Create an inner notebook for this specific beacon
    beacon_inner_notebook = ttk.Notebook(frame, style="Modern.TNotebook")
    beacon_inner_notebook.pack(fill=tk.BOTH, expand=True)

    # Tab 1: Console
    console_frame = ttk.Frame(beacon_inner_notebook, style="Modern.TFrame")
    console = ModernConsole(console_frame, client_id)
    console.pack(fill=tk.BOTH, expand=True)
    beacon_inner_notebook.add(console_frame, text="💬 Console")

    # Tab 2: Intel (NEW!)
    intel_frame = ttk.Frame(beacon_inner_notebook, style="Modern.TFrame")
    create_intel_tab(intel_frame, client_id)
    beacon_inner_notebook.add(intel_frame, text="🔍 Intel")

    # Save references
    beacon_tabs[client_id] = frame
    frame.console = console  # Keep reference to the console
    frame.intel_frame = intel_frame  # Reference to the intel tab (optional)

    return frame

def load_implant_config(client_id):
    """Loads the implant configuration from the JSON file."""
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
    """Creates the Intelligence/Recon tab for a specific beacon."""
    # Main frame with scroll
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

    # Load log data
    intel_data = load_intel_data(client_id)

    # Section: Discovered Hosts
    if intel_data.get('discovered_ips'):
        create_section_header(scrollable_frame, "🌐 Discovered Hosts")
        for ip in intel_data['discovered_ips']:
            ttk.Label(scrollable_frame, text=f"• {ip}", style="Modern.TLabel").pack(anchor=tk.W, padx=20, pady=2)

    # Section: Port Scan
    if intel_data.get('portscan_results'):
        create_section_header(scrollable_frame, "🚪 Open Ports")
        for host, ports in intel_data['portscan_results'].items():
            ttk.Label(scrollable_frame, text=f"{host}:", style="Title.TLabel", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=20, pady=(5, 0))
            for port, status in ports.items():
                color = COLORS['text_success'] if status == 'open' else COLORS['text_error']
                ttk.Label(scrollable_frame, text=f"  • {port}: {status}", foreground=color, style="Modern.TLabel").pack(anchor=tk.W, padx=40)

    # Section: Useful Software
    if intel_data.get('useful_software'):
        create_section_header(scrollable_frame, "🛠️ Detected Software")
        for sw in intel_data['useful_software']:
            ttk.Label(scrollable_frame, text=f"• {sw}", style="Modern.TLabel").pack(anchor=tk.W, padx=20, pady=2)

    # Section: Network Configuration
    if intel_data.get('netconfig'):
        create_section_header(scrollable_frame, "📡 Network Configuration")
        net_text = scrolledtext.ScrolledText(scrollable_frame, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], font=('Consolas', 9), height=10, wrap=tk.NONE)
        net_text.insert(tk.END, intel_data['netconfig'])
        net_text.config(state=tk.DISABLED)
        net_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
    # Section: Implant Configuration (from JSON)
    config_data = load_implant_config(client_id)  # <-- NEW FUNCTION DEFINED BELOW
    if config_data:
        create_section_header(scrollable_frame, "⚙️ Implant Configuration")
        details_frame = ttk.Frame(scrollable_frame, style="Modern.TFrame")
        details_frame.pack(fill=tk.X, padx=20, pady=5)

        # Create a 2-column grid for key-value pairs
        row = 0
        col = 0
        max_cols = 2  # Number of columns
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

        # Make the columns expand
        for i in range(max_cols * 2):
            details_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
def create_section_header(parent, title):
    """Creates a section header for the Intel tab."""
    frame = ttk.Frame(parent, style="Modern.TFrame")
    frame.pack(fill=tk.X, pady=(15, 5))
    ttk.Label(frame, text=title, style="Title.TLabel", font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
    ttk.Separator(frame, orient='horizontal').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

def load_intel_data(client_id):
    """Extracts and parses intelligence data from the client's .log file."""
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
            next(reader, None)  # Skip header

            for row in reader:
                if len(row) < 11:
                    continue

                command = row[9].strip().lower()
                output = row[10].strip()

                # Parse discovered_ips (from row[6])
                if len(row) > 6 and row[6]:
                    ips = [ip.strip() for ip in row[6].split(',')]
                    data['discovered_ips'].update(ips)

                # Parse result_portscan (from row[7])
                if len(row) > 7 and row[7]:
                    # Suponiendo formato "port:status" o "ip:port:status"
                    entries = row[7].split(',')
                    for entry in entries:
                        if ':' in entry:
                            parts = entry.split(':')
                            if len(parts) >= 2:
                                # Assign to current host (row[4]) or 'localhost'
                                host = row[4] if len(row) > 4 and row[4] else 'localhost'
                                port = parts[0]
                                status = parts[1] if len(parts) > 1 else 'unknown'
                                if host not in data['portscan_results']:
                                    data['portscan_results'][host] = {}
                                data['portscan_results'][host][port] = status

                # Detect useful software from 'softenum' command
                if command == 'softenum:' and 'Useful software:' in output:
                    software_list = output.split('Useful software: ')[-1]
                    sw_items = [sw.strip() for sw in software_list.split(',')]
                    data['useful_software'].update(sw_items)

                # Save the last network configuration
                if command == 'netconfig:':
                    data['netconfig'] = output

    except Exception as e:
        print(f"Error loading intel data for {client_id}: {e}")

    # Convert sets to sorted lists for the UI
    data['discovered_ips'] = sorted(list(data['discovered_ips']))
    data['useful_software'] = sorted(list(data['useful_software']))

    return data

def is_client_active(client_id):
    log_path = os.path.join(LOG_DIR, f"{client_id}.log")
    if not os.path.exists(log_path):
        return False
    return (time.time() - os.path.getmtime(log_path)) < 60

def load_latest_client_info_dict(client_id):
    info = {}
    log_path = os.path.join(LOG_DIR, f"{client_id}.log")
    json_path = os.path.join(LOG_DIR, f"implant_config_{client_id}.json")

    if os.path.exists(log_path):
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                last_line = f.readlines()[-1].strip()
                reader = csv.reader([last_line])
                row = next(reader)
                if len(row) >= 9:
                    info.update({
                        'hostname': row[3],
                        'ips': row[4],
                        'user': row[5],
                        'pid': row[2],
                        'result_pwd': row[8],
                    })
        except (FileNotFoundError, IndexError, StopIteration, csv.Error) as exc:
            logging.warning("Failed to parse log file %s: %s", log_path, exc)
            pass

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                info.update({
                    'url_binary': data.get('url_binary', 'N/A'),
                    'created': data.get('created', 'N/A'),
                })
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
            logging.warning("Failed to parse JSON file %s: %s", json_path, exc)
            pass

    return info

def refresh_table_view(tree):
    for item in tree.get_children():
        tree.delete(item)

    try:
        resp = requests.get(f"{API_BASE}/get_connected_clients", verify=False, timeout=5)
        data = resp.json()
        clients = data.get("connected_clients", [])

        for client_id in clients:
            info = load_latest_client_info_dict(client_id)
            status = "🟢 Active" if is_client_active(client_id) else "🟡 Inactive"
            tree.insert("", tk.END, values=(
                info.get('hostname', 'N/A'),
                info.get('ips', 'N/A'),
                info.get('user', 'N/A'),
                info.get('pid', 'N/A'),
                info.get('url_binary', 'N/A'),
                info.get('created', 'N/A'),
                status
            ))
    except Exception as e:
        show_notification(f"Error refreshing table: {str(e)}", "error")

def create_table_view_frame(parent):
    # Create fresh frame EVERY time
    frame = ttk.Frame(parent, style="Card.TFrame")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("Hostname", "IP", "User", "PID", "URL", "Created", "Status")
    tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor=tk.W)

    style = ttk.Style()
    style.configure("Table.Treeview",
                    background=COLORS['bg_secondary'],
                    foreground=COLORS['text_primary'],
                    fieldbackground=COLORS['bg_secondary'],
                    rowheight=25)

    tree.config(style="Table.Treeview")
    tree.pack(fill=tk.BOTH, expand=True)

    refresh_table_view(tree)

    def on_table_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            client_id = item['values'][0]  # hostname = client_id
            select_client(client_id)

    tree.bind("<<TreeviewSelect>>", on_table_select)


def toggle_global_view():
    global global_view_mode

    # Clear ALL content of implants_frame (without destroying the frame)
    for widget in implants_frame.winfo_children():
        widget.destroy()

    if global_view_mode == "card":
        # -> Switch to table view
        create_table_view_frame(implants_frame)  # Create fresh table
        if toggle_view_btn and toggle_view_btn.winfo_exists():
            toggle_view_btn.config(text="🖼️ Card View")
        global_view_mode = "table"

    else:
        # -> Switch to card view
        refresh_clients()  # Recreates cards
        if toggle_view_btn and toggle_view_btn.winfo_exists():
            toggle_view_btn.config(text="📋 Table View")
        global_view_mode = "card"

def create_section_header(parent, title):
    """Creates a section header for the Intel tab."""
    frame = ttk.Frame(parent, style="Modern.TFrame")
    frame.pack(fill=tk.X, pady=(15, 5))
    ttk.Label(frame, text=title, style="Title.TLabel", font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
    ttk.Separator(frame, orient='horizontal').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

def load_intel_data(client_id):
    """Extracts and parses intelligence data from the client's .log file."""
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
            next(reader, None)  # Skip header

            for row in reader:
                if len(row) < 11:
                    continue

                command = row[9].strip().lower()
                output = row[10].strip()

                # Parse discovered_ips (from row[6])
                if len(row) > 6 and row[6]:
                    ips = [ip.strip() for ip in row[6].split(',')]
                    data['discovered_ips'].update(ips)

                # Parse result_portscan (from row[7])
                if len(row) > 7 and row[7]:
                    # Assuming format "ip:port:status" or "port:status"
                    entries = row[7].split(',')
                    for entry in entries:
                        if ':' in entry:
                            parts = entry.split(':')
                            if len(parts) >= 2:
                                port = parts[0]
                                status = parts[1]
                                # Assign to current host (row[4]) or 'localhost'
                                host = row[4] if len(row) > 4 else 'localhost'
                                if host not in data['portscan_results']:
                                    data['portscan_results'][host] = {}
                                data['portscan_results'][host][port] = status

                # Detect useful software from 'softenum' command
                if command == 'softenum:' and 'Useful software:' in output:
                    software_list = output.split('Useful software: ')[-1]
                    sw_items = [sw.strip() for sw in software_list.split(',')]
                    data['useful_software'].update(sw_items)

                # Save the last network configuration
                if command == 'netconfig:':
                    data['netconfig'] = output

    except Exception as e:
        print(f"Error loading intel data for {client_id}: {e}")

    # Convert sets to sorted lists for the UI
    data['discovered_ips'] = sorted(list(data['discovered_ips']))
    data['useful_software'] = sorted(list(data['useful_software']))

    return data

# === FILE HANDLERS ===
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
                        row[9].strip() if len(row) > 9 else "N/A"
                        # ... (condition to avoid empty outputs)
                        event_queue.put({
                            'type': 'command_output',
                            'client_id': client_id,
                            'command': row[9].strip() if len(row) > 9 else "N/A",  # <-- ADD THIS LINE
                            'output': output
                        })

                self.last_positions[client_id] = f.tell()

        except Exception as e:
            event_queue.put({
                'type': 'error',
                'message': f"Error processing {log_path}: {e}"
            })

def process_queue():
    while not event_queue.empty():
        event = event_queue.get_nowait()

        if event['type'] == 'command_output':
            # Show in Event Log
            show_notification(f"[{event['client_id']}] << {event['command']} -> {event['output']}", "info")

            # Show in beacon tab
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
        time.sleep(60)  # Refresh every 60 seconds
        if root.winfo_exists():
            root.after(0, refresh_clients)
        else:
            break

# === DATA LOADING FUNCTIONS ===
def load_implants_data():
    implants = []
    try:
        for file in os.listdir(SESSIONS_DIR):
            if file.startswith("implant_config_") and file.endswith(".json"):
                with open(os.path.join(SESSIONS_DIR, file), 'r') as f:
                    data = json.load(f)
                    implants.append(data)
    except Exception as e:
        show_notification(f"Error loading implants: {e}", "error")
    return implants

def load_banners_data():
    try:
        with open(os.path.join(SESSIONS_DIR, "banners.json"), 'r') as f:
            return json.load(f)
    except Exception as e:
        show_notification(f"Error loading banners: {e}", "error")
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
        show_notification(f"Error loading access log: {e}", "error")
    return entries

def upload_file():
    file_path = filedialog.askopenfilename()
    if not file_path or not current_beacon:
        show_notification("Select a file and a beacon", "warning")
        return

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'client_id': current_beacon}
            resp = requests.post(f"{API_BASE}/upload", files=files, data=data, verify=False)

            if resp.status_code == 200:
                show_notification(f"✓ File {os.path.basename(file_path)} uploaded to {current_beacon}", "success")
            else:
                show_notification(f"✗ Error uploading file: {resp.status_code}", "error")

    except Exception as e:
        show_notification(f"✗ Error uploading file: {str(e)}", "error")

# === ENHANCED MAIN INTERFACE ===
def create_modern_ui():
    global root, console_notebook, events_text, status_bar, implants_container, beacon_tabs
    global implants_frame, toggle_view_btn, main_container  # <- ADDED


    root = tk.Tk()
    root.title("LazyOwn C2 - Modern Interface")
    root.geometry("1600x1000")
    root.configure(bg=COLORS['bg_primary'])
    root.minsize(1200, 800)

    # Configure modern theme
    setup_modern_theme()

    # === STATUS BAR ===
    status_bar = StatusBar(root)

    # === MAIN CONTAINER WITH VERTICAL SCROLL ===
    main_canvas = tk.Canvas(root, bg=COLORS['bg_primary'], highlightthickness=0)
    main_scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    main_container = ttk.Frame(main_canvas, style="Modern.TFrame")

    main_container.bind(
        "<Configure>",
        lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    )

    def configure_canvas_width(event):
        main_canvas.itemconfig(canvas_window, width=event.width)

    canvas_window = main_canvas.create_window((0, 0), window=main_container, anchor="nw")
    main_canvas.bind("<Configure>", configure_canvas_width)
    main_canvas.configure(yscrollcommand=main_scrollbar.set)

    main_canvas.pack(side="left", fill="both", expand=True)
    main_scrollbar.pack(side="right", fill="y")
    # Scroll with mouse
    main_canvas.bind_all("<MouseWheel>", lambda e: main_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    # === TOP HEADER (title + button) ===
    header_frame = ttk.Frame(main_container, style="Modern.TFrame")
    header_frame.pack(fill=tk.X, pady=(0, 5))

    title_label = ttk.Label(header_frame, text="🎯 Active Implants", style="Title.TLabel")
    title_label.pack(side=tk.LEFT)

    toggle_view_btn = ttk.Button(header_frame, text="📋 Table View",
                            style="Modern.TButton",
                            command=toggle_global_view)
    toggle_view_btn.pack(side=tk.RIGHT, padx=(0, 10))
    # Fixed container for implants (always on top)
    implants_frame = ttk.Frame(main_container, style="Card.TFrame")
    implants_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=(0, 10))

    # Fixed container for console (always at bottom)
    console_frame = ttk.Frame(main_container, style="Modern.TFrame")
    console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    # Global view toggle button
    toggle_view_btn = ttk.Button(implants_frame, text="📋 Table View",
                                style="Modern.TButton",
                                command=toggle_global_view)
    toggle_view_btn.pack(side=tk.RIGHT, padx=(0, 10))
    # Scrollable frame for implants
    canvas_frame = ttk.Frame(implants_frame, style="Modern.TFrame")
    canvas_frame.pack(fill=tk.X, padx=10, pady=10)

    implants_canvas = tk.Canvas(canvas_frame, bg=COLORS['bg_primary'],
                               highlightthickness=0, height=300)
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

    # === MAIN PANEL - NOTEBOOK ===
    main_notebook = ttk.Notebook(main_container, style="Modern.TNotebook")
    main_notebook.pack(fill=tk.BOTH, expand=True)

    # --- Tab: Consoles ---
    console_frame = ttk.Frame(main_notebook, style="Modern.TFrame")
    main_notebook.add(console_frame, text="💻 Consoles")

    console_notebook = ttk.Notebook(console_frame, style="Modern.TNotebook")
    console_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Event Log as first tab
    event_frame = ttk.Frame(console_notebook, style="Modern.TFrame")
    console_notebook.add(event_frame, text="📋 Event Log")

    events_console = ModernConsole(event_frame, "GLOBAL")
    events_console.pack(fill=tk.BOTH, expand=True)
    events_text = events_console.output

    # --- Tab: Data ---
    data_frame = ttk.Frame(main_notebook, style="Modern.TFrame")
    main_notebook.add(data_frame, text="📊 Data")

    data_notebook = ttk.Notebook(data_frame, style="Modern.TNotebook")
    data_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Sub-tab: Banners
    banner_tree = ModernTreeview(data_notebook,
                                ("hostname", "port", "protocol", "service", "extra"),
                                load_banners_data)
    banner_tree.set_title("🌐 Banner Grabbing")
    data_notebook.add(banner_tree, text="Banners")

    # Sub-tab: Implants
    implant_tree = ModernTreeview(data_notebook,
                                 ("name", "os", "rhost", "sleep", "created"),
                                 load_implants_data)
    implant_tree.set_title("🔧 Implant Configuration")
    data_notebook.add(implant_tree, text="Implants")

    # Sub-tab: Access Log
    access_tree = ModernTreeview(data_notebook,
                                ("timestamp", "level", "message"),
                                load_access_log)
    access_tree.set_title("📝 Access Log")
    data_notebook.add(access_tree, text="Access Log")

    # --- Tab: Tools ---
    tools_frame = ttk.Frame(main_notebook, style="Modern.TFrame")
    main_notebook.add(tools_frame, text="🛠️ Tools")

    tools_container = ttk.Frame(tools_frame, style="Modern.TFrame")
    tools_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Tools grid
    create_tools_grid(tools_container)

    # === ENHANCED MENU ===
    create_modern_menu()

    # === KEYBOARD SHORTCUTS ===
    setup_keyboard_shortcuts()

    # === INITIALIZATION ===
    beacon_tabs = {}

    # Show welcome message
    show_notification("🚀 LazyOwn C2 started - Press Ctrl+L to connect", "info")

    # Attempt auto-connection
    root.after(1000, login)

    # Start event processing
    root.after(100, process_queue)

    # Configure close
    root.protocol("WM_DELETE_WINDOW", on_closing)

    return root

def create_tools_grid(parent):
    """Create tools grid."""

    # Main tools
    tools = [
        {
            "name": "📁 Upload File",
            "desc": "Upload file to selected beacon",
            "command": upload_file,
            "style": "Primary.TButton"
        },
        {
            "name": "🔄 Refresh",
            "desc": "Refresh beacon list",
            "command": refresh_clients,
            "style": "Success.TButton"
        },
        {
            "name": "🔌 Reconnect",
            "desc": "Reconnect to C2 server",
            "command": login,
            "style": "Modern.TButton"
        },
        {
            "name": "💾 Export Logs",
            "desc": "Export session logs",
            "command": export_logs,
            "style": "Modern.TButton"
        },
        {
            "name": "🗂️ Manage Payloads",
            "desc": "Generate and manage payloads",
            "command": manage_payloads,
            "style": "Modern.TButton"
        },
        {
            "name": "📊 Statistics",
            "desc": "View C2 statistics",
            "command": show_statistics,
            "style": "Modern.TButton"
        }
    ]

    # Create cards for each tool
    for i, tool in enumerate(tools):
        card = create_tool_card(parent, tool)
        card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")

    # Configure columns
    for i in range(3):
        parent.columnconfigure(i, weight=1)

def create_tool_card(parent, tool):
    """Create tool card."""
    card = ttk.Frame(parent, style="Card.TFrame")

    content = ttk.Frame(card, style="Modern.TFrame")
    content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    # Title
    title_label = ttk.Label(content, text=tool["name"],
                           style="Title.TLabel", font=('Segoe UI', 11, 'bold'))
    title_label.pack(anchor=tk.W, pady=(0, 5))

    # Description
    desc_label = ttk.Label(content, text=tool["desc"],
                          style="Status.TLabel", wraplength=200)
    desc_label.pack(anchor=tk.W, pady=(0, 10))

    # Button
    button = ttk.Button(content, text="Execute",
                       style=tool["style"], command=tool["command"])
    button.pack(anchor=tk.W)

    return card

def create_modern_menu():
    """Create modern menu."""
    menubar = tk.Menu(root, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                      activebackground=COLORS['accent_blue'], activeforeground=COLORS['text_primary'])
    root.config(menu=menubar)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                        activebackground=COLORS['accent_blue'])
    menubar.add_cascade(label="📁 File", menu=file_menu)
    file_menu.add_command(label="📤 Upload File", command=upload_file, accelerator="Ctrl+U")
    file_menu.add_command(label="💾 Export Logs", command=export_logs, accelerator="Ctrl+E")
    file_menu.add_separator()
    file_menu.add_command(label="❌ Exit", command=on_closing, accelerator="Ctrl+Q")

    # Connection Menu
    conn_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                        activebackground=COLORS['accent_blue'])
    menubar.add_cascade(label="🔌 Connection", menu=conn_menu)
    conn_menu.add_command(label="🔗 Connect", command=login, accelerator="Ctrl+L")
    conn_menu.add_command(label="🔄 Refresh Beacons", command=refresh_clients, accelerator="F5")
    conn_menu.add_command(label="⏹️ Stop Polling", command=stop_polling)

    # Tools Menu
    tools_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                         activebackground=COLORS['accent_blue'])
    menubar.add_cascade(label="🛠️ Tools", menu=tools_menu)
    tools_menu.add_command(label="🗂️ Manage Payloads", command=manage_payloads)
    tools_menu.add_command(label="📊 Statistics", command=show_statistics)
    tools_menu.add_command(label="🔧 Settings", command=show_settings)

    # Help Menu
    help_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                        activebackground=COLORS['accent_blue'])
    menubar.add_cascade(label="❓ Help", menu=help_menu)
    help_menu.add_command(label="📖 User Manual", command=show_help)
    help_menu.add_command(label="ℹ️ About", command=show_about)

def setup_keyboard_shortcuts():
    """Configure keyboard shortcuts."""
    root.bind('<Control-l>', lambda e: login())
    root.bind('<Control-u>', lambda e: upload_file())
    root.bind('<Control-e>', lambda e: export_logs())
    root.bind('<Control-q>', lambda e: on_closing())
    root.bind('<F5>', lambda e: refresh_clients())
    root.bind('<Control-r>', lambda e: refresh_clients())

# === TOOL FUNCTIONS ===
def export_logs():
    """Export logs to file."""
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
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")

                # Export event log content
                if events_text:
                    f.write("EVENT LOG:\n")
                    f.write("-"*20 + "\n")
                    f.write(events_text.get(1.0, tk.END))
                    f.write("\n" + "="*50 + "\n\n")

                # Export logs from each beacon
                for client_id, tab_frame in beacon_tabs.items():
                    if hasattr(tab_frame, 'console'):
                        f.write(f"BEACON {client_id}:\n")
                        f.write("-"*20 + "\n")
                        f.write(tab_frame.console.output.get(1.0, tk.END))
                        f.write("\n" + "="*50 + "\n\n")

            show_notification(f"✓ Logs exported to {filename}", "success")
    except Exception as e:
        show_notification(f"✗ Error exporting logs: {str(e)}", "error")

def manage_payloads():
    """Payload management window."""
    payload_window = tk.Toplevel(root)
    payload_window.title("🗂️ Payload Management")
    payload_window.geometry("800x600")
    payload_window.configure(bg=COLORS['bg_primary'])

    # Apply theme
    payload_window.transient(root)
    payload_window.grab_set()

    # Content
    main_frame = ttk.Frame(payload_window, style="Modern.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    title_label = ttk.Label(main_frame, text="🗂️ Payload Management", style="Title.TLabel")
    title_label.pack(pady=(0, 20))

    # Notebook for different payload types
    payload_notebook = ttk.Notebook(main_frame, style="Modern.TNotebook")
    payload_notebook.pack(fill=tk.BOTH, expand=True)

    # Windows tab
    windows_frame = ttk.Frame(payload_notebook, style="Modern.TFrame")
    payload_notebook.add(windows_frame, text="🖥️ Windows")

    # Linux tab
    linux_frame = ttk.Frame(payload_notebook, style="Modern.TFrame")
    payload_notebook.add(linux_frame, text="🐧 Linux")

    # Action buttons
    button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
    button_frame.pack(fill=tk.X, pady=(20, 0))

    ttk.Button(button_frame, text="Generate Payload",
              style="Primary.TButton").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Close",
              style="Modern.TButton",
              command=payload_window.destroy).pack(side=tk.RIGHT)

def show_statistics():
    """Show statistics window."""
    stats_window = tk.Toplevel(root)
    stats_window.title("📊 C2 Statistics")
    stats_window.geometry("600x400")
    stats_window.configure(bg=COLORS['bg_primary'])

    stats_window.transient(root)
    stats_window.grab_set()

    main_frame = ttk.Frame(stats_window, style="Modern.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    title_label = ttk.Label(main_frame, text="📊 System Statistics", style="Title.TLabel")
    title_label.pack(pady=(0, 20))

    # Basic statistics
    stats_frame = ttk.Frame(main_frame, style="Card.TFrame")
    stats_frame.pack(fill=tk.BOTH, expand=True)

    content_frame = ttk.Frame(stats_frame, style="Modern.TFrame")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Calculate statistics
    total_beacons = len(beacon_tabs)
    uptime = "Calculating..."

    stats_text = f"""
    🎯 Active Beacons: {total_beacons}
    ⏱️ Uptime: {uptime}
    🔌 Connection Status: {'Connected' if connection_status else 'Disconnected'}
    📁 Logs Directory: {LOG_DIR}
    🌐 C2 Server: {API_BASE}
    """

    stats_label = ttk.Label(content_frame, text=stats_text, style="Modern.TLabel")
    stats_label.pack(anchor=tk.W)

    ttk.Button(main_frame, text="Close",
              style="Modern.TButton",
              command=stats_window.destroy).pack(pady=(20, 0))

def show_settings():
    """Show settings window."""
    settings_window = tk.Toplevel(root)
    settings_window.title("🔧 Settings")
    settings_window.geometry("500x400")
    settings_window.configure(bg=COLORS['bg_primary'])

    settings_window.transient(root)
    settings_window.grab_set()

    main_frame = ttk.Frame(settings_window, style="Modern.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    title_label = ttk.Label(main_frame, text="🔧 Settings", style="Title.TLabel")
    title_label.pack(pady=(0, 20))

    # Settings
    config_frame = ttk.Frame(main_frame, style="Card.TFrame")
    config_frame.pack(fill=tk.BOTH, expand=True)

    content_frame = ttk.Frame(config_frame, style="Modern.TFrame")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # C2 Server
    ttk.Label(content_frame, text="C2 Server:", style="Modern.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
    server_entry = ttk.Entry(content_frame, style="Modern.TEntry", width=30)
    server_entry.insert(0, API_BASE)
    server_entry.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=5)

    # Username
    ttk.Label(content_frame, text="Username:", style="Modern.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
    user_entry = ttk.Entry(content_frame, style="Modern.TEntry", width=30)
    user_entry.insert(0, USERNAME)
    user_entry.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=5)

    # Sessions directory
    ttk.Label(content_frame, text="Sessions Dir:", style="Modern.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
    sessions_entry = ttk.Entry(content_frame, style="Modern.TEntry", width=30)
    sessions_entry.insert(0, SESSIONS_DIR)
    sessions_entry.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0), pady=5)

    content_frame.columnconfigure(1, weight=1)

    # Buttons
    button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
    button_frame.pack(fill=tk.X, pady=(20, 0))

    ttk.Button(button_frame, text="Save",
              style="Primary.TButton").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Cancel",
              style="Modern.TButton",
              command=settings_window.destroy).pack(side=tk.RIGHT)

def show_help():
    """Show help."""
    help_window = tk.Toplevel(root)
    help_window.title("📖 User Manual")
    help_window.geometry("700x500")
    help_window.configure(bg=COLORS['bg_primary'])

    help_window.transient(root)
    help_window.grab_set()

    main_frame = ttk.Frame(help_window, style="Modern.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    title_label = ttk.Label(main_frame, text="📖 User Manual", style="Title.TLabel")
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
LAZYOWN C2 BLACK BASALT - USER MANUAL

KEYBOARD SHORTCUTS:
- Ctrl+L: Connect to C2 server
- Ctrl+U: Upload file
- Ctrl+E: Export logs
- Ctrl+Q: Exit
- F5: Refresh beacons

MAIN FEATURES:

1. BEACON MANAGEMENT
   - Beacons appear as cards at the top
   - Click a beacon to open its console
   - Green indicator shows active beacons

2. CONSOLES
   - Each beacon has its own console tab
   - Use the Event Log to see all activity
   - Commands are shown in blue, responses in green

3. DATA
   - Banners tab: Information about detected services
   - Implants tab: Implant configuration
   - Access Log tab: System access log

4. TOOLS
   - Upload File: Transfer files to beacons
   - Manage Payloads: Generate new payloads
   - Statistics: View system information

COLORS:
- Green: Success/Active
- Red: Error/Inactive
- Blue: Commands/Actions
- Yellow: Warnings
    """

    help_text.insert(1.0, help_content)
    help_text.config(state=tk.DISABLED)

    ttk.Button(main_frame, text="Close",
              style="Modern.TButton",
              command=help_window.destroy).pack(pady=(20, 0))

def show_about():
    """Show program information."""
    messagebox.showinfo(
        "About LazyOwn C2 Black Basalt GUI",
        "LazyOwn C2 - Black Basalt Modern Interface\n\n"
        "Version: 2.0\n"
        "Developed by: LazyOwn Team\n\n"
        "A modern interface for the LazyOwn RedTeam Framework\n"
        "LazyOwn Command & Control BLACK BASALT (c).\n\n"
        "(c) 2025 LazyOwn RedTeam Framework Project"
    )

def on_closing():
    """Handle application close."""
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        stop_polling()
        root.destroy()

# === FUNCIÓN PRINCIPAL ===
def main():
    """Función principal"""
    global root

    # Verificar dependencias
    try:
        from PIL import Image, ImageTk
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError as e:
        messagebox.showerror("Error", f"Dependencia faltante: {e}")
        return

    # Crear y ejecutar interfaz
    root = create_modern_ui()
    root.mainloop()

if __name__ == "__main__":
    main()
