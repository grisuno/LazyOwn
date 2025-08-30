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
from PIL import Image, ImageTk  # pip install Pillow
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
events_text = None  # Para el Event Log
processes_tree = None  # Si quieres mostrar procesos

# === FUNCIONES DE API ===
def login():
    try:
        resp = requests.post(f"{API_BASE}/login", data={"username": USERNAME, "password": PASSWORD}, verify=False)
        if resp.status_code == 200:
            messagebox.showinfo("Login", "Conectado al C2")
            refresh_clients()
            start_polling()
        else:
            messagebox.showerror("Error", "Login fallido")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar: {e}")

def refresh_clients():
    try:
        resp = requests.get(f"{API_BASE}/get_connected_clients", verify=False)
        data = resp.json()
        client_listbox.delete(0, tk.END)
        clients = data.get("connected_clients", [])
        for client in clients:
            client_listbox.insert(tk.END, client)
        update_map(clients)
    except Exception as e:
        client_listbox.delete(0, tk.END)
        client_listbox.insert(tk.END, "Sin conexión")

def update_map(clients):
    global nodes, canvas
    canvas.delete("all")
    nodes.clear()
    x_offset = 100
    y_offset = 80
    spacing = 150
    for i, client_id in enumerate(clients):
        x = x_offset + (i % 5) * spacing
        y = y_offset + (i // 5) * spacing
        system_type = "windows" if "win" in client_id.lower() else "linux" if "linux" in client_id.lower() else "mac"
        img_path = f"{system_type}.png"
        if not os.path.exists(img_path):
            img_path = "windows.png"
        img = Image.open(img_path).resize((60, 60), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        node = canvas.create_image(x, y, image=photo, anchor="center")
        label = canvas.create_text(x, y + 70, text=client_id, font=("Consolas", 8), fill="white")
        nodes[client_id] = {"x": x, "y": y, "image": photo, "label": label, "node": node}
        canvas.tag_bind(node, "<Button-1>", lambda e, cid=client_id: select_node(cid))

def upload_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    client = client_listbox.get(tk.ACTIVE)
    if not client:
        return
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'client_id': client}
        try:
            requests.post(f"{API_BASE}/upload", files=files, data=data, verify=False)
            output_text.insert(tk.END, f"[+] Archivo {os.path.basename(file_path)} subido a {client}\n")
        except Exception as e:
            output_text.insert(tk.END, f"[!] Error subiendo archivo: {str(e)}\n")

def select_node(client_id):
    global current_beacon
    current_beacon = client_id
    refresh_console_tab()

def refresh_console_tab():
    if current_beacon and current_beacon not in beacon_tabs:
        create_beacon_tab(current_beacon)
    if current_beacon in beacon_tabs:
        console_notebook.select(beacon_tabs[current_beacon])

def create_beacon_tab(client_id):
    frame = ttk.Frame(console_notebook)
    console_notebook.add(frame, text=f"Beacon {client_id}")
    beacon_tabs[client_id] = frame
    output = scrolledtext.ScrolledText(frame, bg="#000000", fg="#00ff00", font=("Consolas", 10), wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    input_frame = ttk.Frame(frame)
    input_frame.pack(fill=tk.X, padx=5, pady=5)
    entry = ttk.Entry(input_frame, font=("Consolas", 10))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    send_btn = ttk.Button(input_frame, text="Send", command=lambda: send_command(entry, output, client_id))
    send_btn.pack(side=tk.RIGHT)
    entry.bind('<Return>', lambda e: send_command(entry, output, client_id))
    frame.output = output
    frame.entry = entry

def send_command(entry, output, client_id):
    cmd = entry.get().strip()
    if not cmd: return
    try:
        requests.post(f"{API_BASE}/issue_command", data={"client_id": client_id, "command": cmd}, verify=False)
        output.insert(tk.END, f"[{client_id}] > {cmd}\n")
        entry.delete(0, tk.END)
        output.see(tk.END)
    except Exception as e:
        output.insert(tk.END, f"[!] Error: {str(e)}\n")

class LogHandler(FileSystemEventHandler):
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.last_positions = {}  # {client_id: last_read_position}

    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".log"):
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

        # Obtener última posición leída
        last_pos = self.last_positions.get(client_id, 0)

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                # Ir a la última posición
                f.seek(last_pos)
                lines = f.readlines()

                # Actualizar última posición
                self.last_positions[client_id] = f.tell()

                # Parsear solo nuevas líneas
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("command,") or line.startswith("timestamp"):
                        continue  # Saltar encabezados
                    if ',' not in line:
                        continue
                    # Intentar parsear como CSV manualmente
                    parts = line.split(',', 1)
                    command = parts[0].strip()
                    output = parts[1].strip() if len(parts) > 1 else ""

                    # Evitar mostrar comandos como salida
                    if not output or output.lower() in ['none', 'null', ''] or output == command:
                        continue

                    # Enviar a la cola
                    event_queue.put({
                        'type': 'command_output',
                        'client_id': client_id,
                        'output': output
                    })

        except Exception as e:
            event_queue.put({'type': 'error', 'message': f"Error leyendo {log_path}: {e}"})

def process_queue():
    while not event_queue.empty():
        event = event_queue.get_nowait()
        if event['type'] == 'command_output':
            # Mostrar en Event Log
            events_text.insert(tk.END, f"[{event['client_id']}] << {event['output']}\n")
            events_text.see(tk.END)
            # Mostrar en pestaña del beacon
            if event['client_id'] in beacon_tabs:
                beacon_tabs[event['client_id']].output.insert(tk.END, f"[{event['client_id']}] << {event['output']}\n")
                beacon_tabs[event['client_id']].output.see(tk.END)
        elif event['type'] == 'error':
            events_text.insert(tk.END, f"[ERROR] {event['message']}\n")
            events_text.see(tk.END)
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
        time.sleep(5)
        if root.winfo_exists():
            root.after(0, refresh_clients)
        else:
            break

# === CARGA DE DATOS ===
def load_implants_data():
    implants = []
    for file in os.listdir(SESSIONS_DIR):
        if file.startswith("implant_config_") and file.endswith(".json"):
            try:
                with open(os.path.join(SESSIONS_DIR, file), 'r') as f:
                    data = json.load(f)
                    implants.append(data)
            except Exception as e:
                print(f"Error leyendo {file}: {e}")
    return implants

def load_banners_data():
    try:
        with open(os.path.join(SESSIONS_DIR, "banners.json"), 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error leyendo banners.json: {e}")
        return []

def load_access_log():
    entries = []
    log_path = os.path.join(SESSIONS_DIR, "access.log")
    if not os.path.exists(log_path): return []
    with open(log_path, 'r') as f:
        for line in f:
            match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (.+)", line)
            if match:
                entries.append({
                    'timestamp': match.group(1),
                    'level': match.group(2),
                    'message': match.group(3)
                })
    return entries

def load_sessions_data():
    try:
        with open(os.path.join(SESSIONS_DIR, "sessionLazyOwn.json"), 'r') as f:
            data = json.load(f)
            return data.get("implants", [])
    except Exception as e:
        print(f"Error leyendo sessionLazyOwn.json: {e}")
        return []

# === INTERFAZ ===
def create_ui():
    global root, client_listbox, canvas, console_notebook, events_text

    root = tk.Tk()
    root.title("LazyOwn C2 - Cobalt Strike Style")
    root.geometry("1400x900")
    root.configure(bg="#1e1e1e")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#1e1e1e")
    style.configure("TButton", background="#2d2d2d", foreground="white", font=("Segoe UI", 9))
    style.configure("TLabel", background="#1e1e1e", foreground="white")
    style.configure("TEntry", fieldbackground="#2d2d2d", foreground="white", insertcolor="white")
    style.configure("TNotebook", background="#1e1e1e", tabmargins=[2, 5, 2, 0])
    style.configure("TNotebook.Tab", background="#2d2d2d", foreground="white", padding=[10, 5], font=("Segoe UI", 9, "bold"))
    style.map("TNotebook.Tab", background=[('selected', '#1e1e1e'), ('active', '#3d3d3d')])

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- MAPA DE RED (arriba) ---
    map_frame = ttk.LabelFrame(main_frame, text="Mapa de Red", relief="flat")
    map_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    canvas = tk.Canvas(map_frame, bg="#000000", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # --- PANEL INFERIOR: NOTEBOOK ---
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    console_notebook = ttk.Notebook(bottom_frame)
    console_notebook.pack(fill=tk.BOTH, expand=True)

    # Pestaña: Event Log
    tab_events = ttk.Frame(console_notebook)
    console_notebook.add(tab_events, text="Event Log")
    global events_text
    events_text = scrolledtext.ScrolledText(tab_events, bg="#000000", fg="#00ff00", font=("Consolas", 10), wrap=tk.WORD)
    events_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    input_frame = ttk.Frame(tab_events)
    input_frame.pack(fill=tk.X, padx=5, pady=5)
    cmd_entry = ttk.Entry(input_frame, font=("Consolas", 10))
    cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    send_btn = ttk.Button(input_frame, text="Send", command=lambda: send_command(cmd_entry, events_text, "GLOBAL"))
    send_btn.pack(side=tk.RIGHT)
    cmd_entry.bind('<Return>', lambda e: send_command(cmd_entry, events_text, "GLOBAL"))

    # Pestaña: Data (con subpestañas)
    tab_data = ttk.Frame(console_notebook)
    console_notebook.add(tab_data, text="Data")
    data_notebook = ttk.Notebook(tab_data)
    data_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Subpestaña: Banners
    banner_frame = ttk.Frame(data_notebook)
    data_notebook.add(banner_frame, text="Banners")
    columns = ("hostname", "port", "protocol", "service", "extra")
    banner_tree = ttk.Treeview(banner_frame, columns=columns, show="headings", height=10)
    for col in columns:
        banner_tree.heading(col, text=col)
    banner_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    for banner in load_banners_data():
        banner_tree.insert("", tk.END, values=(
            banner.get("hostname", ""),
            banner.get("port", ""),
            banner.get("protocol", ""),
            banner.get("service", ""),
            banner.get("extra", "")
        ))

    # Subpestaña: Implants
    implant_frame = ttk.Frame(data_notebook)
    data_notebook.add(implant_frame, text="Implants")
    columns = ("name", "os", "rhost", "sleep", "created")
    implant_tree = ttk.Treeview(implant_frame, columns=columns, show="headings", height=10)
    for col in columns:
        implant_tree.heading(col, text=col)
    implant_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    for implant in load_implants_data():
        implant_tree.insert("", tk.END, values=(
            implant.get("name", ""),
            implant.get("os", ""),
            implant.get("rhost", ""),
            implant.get("sleep", ""),
            implant.get("created", "")
        ))

    # Subpestaña: Access Log
    log_frame = ttk.Frame(data_notebook)
    data_notebook.add(log_frame, text="Access Log")
    columns = ("timestamp", "level", "message")
    log_tree = ttk.Treeview(log_frame, columns=columns, show="headings", height=10)
    for col in columns:
        log_tree.heading(col, text=col)
    log_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    for entry in load_access_log():
        log_tree.insert("", tk.END, values=(
            entry.get("timestamp", ""),
            entry.get("level", ""),
            entry.get("message", "")
        ))

    # --- PANEL DERECHO: CLIENTES ---
    client_frame = ttk.LabelFrame(main_frame, text="Implantes", width=220)
    client_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
    client_frame.pack_propagate(False)
    client_listbox = tk.Listbox(client_frame, bg="#2d2d2d", fg="#00ff00", font=("Consolas", 10), selectmode=tk.SINGLE)
    client_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    refresh_btn = ttk.Button(client_frame, text="Refresh", command=refresh_clients)
    refresh_btn.pack(pady=5)

    # --- MENÚ ---
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Upload File", command=upload_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # === INICIAR ===
    login()
    root.after(100, process_queue)
    root.protocol("WM_DELETE_WINDOW", lambda: [stop_polling(), root.destroy()])
    root.mainloop()

if __name__ == "__main__":
    create_ui()