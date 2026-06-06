#!/home/grisun0/LazyOwn/venv_telegram/bin/python3
"""
telegram_hermes.py
LazyOwn Telegram Bot with Hermes Gateway Integration

This bot bridges Telegram to the full LazyOwn framework via the MCP layer
and Hermes gateway for autonomous task execution. It supports:
- Direct LazyOwn shell command execution
- Autonomous agent delegation (Groq/Ollama)
- Cron-scheduled tasks
- C2 beacon interaction
- Cross-platform messaging via Hermes gateway

Usage:
    python3 telegram_hermes.py

Configuration (payload.json keys):
    telegram_token       - Telegram bot token from @BotFather
    c2_pass              - Authentication secret for /start
    enable_ia            - Enable Groq AI processing (default: false)
    api_key              - Groq API key (if enable_ia is true)
    lhost, c2_port       - C2 server coordinates
"""

import asyncio
import fcntl
import json
import os
import pty
import re
import select
import ssl
import struct
import subprocess
import sys
import termios
import time
import urllib.error
import urllib.request
from pathlib import Path

import nest_asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)

# ── Paths ─────────────────────────────────────────────────────────────────────
LAZYOWN_DIR = Path(__file__).parent.resolve()
SESSIONS_DIR = LAZYOWN_DIR / "sessions"
PAYLOAD_FILE = LAZYOWN_DIR / "payload.json"

# ── Helper: strip ANSI escape codes ───────────────────────────────────────────
def strip_ansi(s: str) -> str:
    ansi_regex = re.compile(
        r'[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]'
    )
    return ansi_regex.sub('', s)

# ── Helper: run LazyOwn shell command via PTY (from MCP _run_lazyown_command) ──
def run_lazyown_command(command: str, timeout: int = 30) -> str:
    """
    Execute one or more LazyOwn shell commands non-interactively via PTY.
    Replicates the MCP server's _run_lazyown_command logic.
    """
    cmd_input = (command.strip() + "\nexit\n").encode()

    run_script = LAZYOWN_DIR / "run"
    if run_script.is_file():
        argv = ["bash", str(run_script)]
    else:
        argv = [sys.executable, "-W", "ignore", str(LAZYOWN_DIR / "lazyown.py")]

    env = os.environ.copy()
    env["TERM"] = "xterm-256color"

    master_fd, slave_fd = pty.openpty()
    winsize = struct.pack("HHHH", 50, 220, 0, 0)
    fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsize)

    try:
        proc = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=slave_fd,
            stderr=slave_fd,
            env=env,
            cwd=str(LAZYOWN_DIR),
            start_new_session=True,
        )
        os.close(slave_fd)

        try:
            if proc.stdin is not None:
                proc.stdin.write(cmd_input)
                proc.stdin.close()
        except BrokenPipeError:
            pass

        output_chunks: list[str] = []
        deadline = time.monotonic() + timeout

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                proc.kill()
                os.close(master_fd)
                return f"[timeout] Command exceeded {timeout}s"

            r, _, _ = select.select([master_fd], [], [], min(remaining, 0.5))
            if r:
                try:
                    data = os.read(master_fd, 4096)
                    if data:
                        output_chunks.append(data.decode("utf-8", errors="replace"))
                except OSError:
                    break
            else:
                if proc.poll() is not None:
                    try:
                        while True:
                            r2, _, _ = select.select([master_fd], [], [], 0.1)
                            if not r2:
                                break
                            data = os.read(master_fd, 4096)
                            if not data:
                                break
                            output_chunks.append(data.decode("utf-8", errors="replace"))
                    except OSError:
                        pass
                    break

        os.close(master_fd)
        proc.wait()
        return "".join(output_chunks)
    except Exception as exc:
        try:
            os.close(master_fd)
        except OSError:
            pass
        return f"[error] {exc}"

# ── Helper: C2 API request ──────────────────────────────────────────────────────
def c2_request(path: str, method: str = "GET", body: dict | None = None) -> dict:
    host = config.get("lhost", "127.0.0.1")
    port = int(config.get("c2_port", 4444))
    user = config.get("c2_user", "LazyOwn")
    passwd = config.get("c2_pass", "LazyOwn")
    url = f"https://{host}:{port}{path}"

    import base64
    token = base64.b64encode(f"{user}:{passwd}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        try:
            return json.loads(exc.read().decode("utf-8", errors="replace"))
        except Exception:
            return {"error": f"HTTP {exc.code}"}
    except Exception as exc:
        return {"_error": str(exc)}

# ── Helper: load/save payload ───────────────────────────────────────────────────
def load_payload() -> dict:
    try:
        with open(PAYLOAD_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

# ── Secure Session Manager ─────────────────────────────────────────────────────
class SecureSessionManager:
    def __init__(self):
        self.sessions = {}
        self.failed_attempts = {}
        self.command_timestamps = {}

    def register_failed_attempt(self, user_id: int):
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = {"count": 1, "timestamp": time.time()}
        else:
            self.failed_attempts[user_id]["count"] += 1
            self.failed_attempts[user_id]["timestamp"] = time.time()

    def check_lockout(self, user_id: int) -> bool:
        attempt = self.failed_attempts.get(user_id)
        if attempt and attempt["count"] >= MAX_FAILED_ATTEMPTS:
            if (time.time() - attempt["timestamp"]) < 3600:
                return True
            else:
                del self.failed_attempts[user_id]
        return False

    def check_rate_limit(self, user_id: int) -> bool:
        now = time.time()
        if user_id not in self.command_timestamps:
            self.command_timestamps[user_id] = []

        self.command_timestamps[user_id] = [
            t for t in self.command_timestamps[user_id] if now - t < 60
        ]

        if len(self.command_timestamps[user_id]) >= RATE_LIMIT:
            return False

        self.command_timestamps[user_id].append(now)
        return True

    def create_session(self, user_id: int, client_id: str | None = None):
        self.sessions[user_id] = {
            "user_id": user_id,
            "client_id": client_id,
            "session_start": time.time(),
            "last_activity": time.time(),
        }

    def validate_session(self, user_id: int) -> bool:
        session = self.sessions.get(user_id)
        if not session:
            return False

        if (time.time() - session["last_activity"]) > SESSION_TIMEOUT:
            del self.sessions[user_id]
            return False

        session["last_activity"] = time.time()
        return True

    def get_client_id(self, user_id: int) -> str | None:
        session = self.sessions.get(user_id)
        return session["client_id"] if session else None

    def set_client_id(self, user_id: int, client_id: str):
        if user_id in self.sessions:
            self.sessions[user_id]["client_id"] = client_id


session_manager = SecureSessionManager()

# ── Telegram Handlers ─────────────────────────────────────────────────────────

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if session_manager.check_lockout(user_id):
        await update.message.reply_text(
            "[SECURITY] Account locked due to brute-force attempts. Wait 1 hour."
        )
        return

    if not context.args:
        await update.message.reply_text("Usage: /start <secret>")
        return

    if context.args[0] == c2_pass:
        session_manager.create_session(user_id, client_id=None)
        await update.message.reply_text(
            "h1! 1 4m 4 b0t to APT/RedTeaming with Hermes Gateway.\n"
            "I can execute LazyOwn commands, run autonomous agents, and bridge messages.\n"
            "Use /help to see available commands."
        )
    else:
        session_manager.register_failed_attempt(user_id)
        await update.message.reply_text("Usage: /start <secret>")


async def help_cmd(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    help_text = (
        "LazyOwn Hermes Bot Commands:\n"
        "---\n"
        "/cmd <command>       - Execute a LazyOwn shell command\n"
        "/sitrep             - Full campaign situation report\n"
        "/config [key] [val] - View or set payload.json config\n"
        "/addcli <id>        - Set active C2 client_id\n"
        "/clients            - List online C2 implants\n"
        "/c2 <command>       - Send command to C2 beacon\n"
        "/agent <goal>       - Run autonomous Groq agent (async)\n"
        "/delegate <goal>    - Delegate task to Hermes subagent\n"
        "/cron <sched> <cmd> - Schedule LazyOwn command via cron\n"
        "/status             - Show daemon and campaign status\n"
        "/download <file>    - Download file from sessions/\n"
        "/upload (document)  - Upload file to C2 beacon\n"
        "/stop               - Stop any running autonomous daemon\n"
        "---\n"
        "Any text message not starting with / is treated as a direct LazyOwn command."
    )
    await update.message.reply_text(help_text)


async def execute_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not session_manager.check_rate_limit(user_id):
        await update.message.reply_text("Rate limit exceeded. Max 5 commands/minute.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /cmd <lazyown_command>")
        return

    command = " ".join(context.args)
    await update.message.reply_text(f"Executing: {command}")

    try:
        output = await asyncio.get_event_loop().run_in_executor(
            None, lambda: run_lazyown_command(command, timeout=60)
        )
        output = strip_ansi(output)

        # Truncate if too long for Telegram (4096 limit)
        if len(output) > 4000:
            output = output[:3990] + "\n... [truncated]"

        await update.message.reply_text(f"Output:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def sitrep(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not session_manager.check_rate_limit(user_id):
        await update.message.reply_text("Rate limit exceeded.")
        return

    await update.message.reply_text("Generating SITREP...")

    try:
        # Run campaign_sitrep equivalent commands
        output = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: run_lazyown_command("session_state", timeout=30),
        )
        output = strip_ansi(output)

        # Also try to get world model
        world_model = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: run_lazyown_command("world_model", timeout=30),
        )
        world_model = strip_ansi(world_model)

        combined = f"SESSION STATE:\n{output}\n\nWORLD MODEL:\n{world_model}"
        if len(combined) > 4000:
            combined = combined[:3990] + "\n... [truncated]"

        await update.message.reply_text(combined)
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def config_cmd(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not context.args:
        cfg = load_payload()
        # Mask sensitive keys
        safe = {k: v for k, v in cfg.items() if k not in ("api_key", "c2_pass", "telegram_token")}
        await update.message.reply_text(f"Current config:\n```\n{json.dumps(safe, indent=2)}\n```", parse_mode="Markdown")
        return

    if len(context.args) < 2:
        key = context.args[0]
        cfg = load_payload()
        value = cfg.get(key, "<not set>")
        await update.message.reply_text(f"{key} = {value}")
        return

    key = context.args[0]
    value = " ".join(context.args[1:])

    # Auto-convert types
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    else:
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass

    cfg = load_payload()
    cfg[key] = value
    try:
        with open(PAYLOAD_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
        await update.message.reply_text(f"Set {key} = {value!r}")
    except Exception as exc:
        await update.message.reply_text(f"Error saving config: {exc}")


async def add_cli(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not context.args:
        await update.message.reply_text("Usage: /addcli <client_id>")
        return

    client_id = context.args[0]
    session_manager.set_client_id(user_id, client_id)
    await update.message.reply_text(f"Client ID set to '{client_id}'")


async def list_clients(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not session_manager.check_rate_limit(user_id):
        await update.message.reply_text("Rate limit exceeded.")
        return

    try:
        result = c2_request("/get_connected_clients")
        if "_error" in result or "error" in result:
            await update.message.reply_text(f"C2 Error: {result}")
            return

        clients = result.get("connected_clients", [])
        if not clients:
            await update.message.reply_text("No implants online.")
            return

        msg = "Online Implants:\n" + "\n".join(f"  {c}" for c in clients)
        await update.message.reply_text(msg)
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def c2_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not session_manager.check_rate_limit(user_id):
        await update.message.reply_text("Rate limit exceeded.")
        return

    client_id = session_manager.get_client_id(user_id)
    if not client_id:
        await update.message.reply_text("No client ID set. Use /addcli <client_id> first.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /c2 <command_to_send>")
        return

    command = " ".join(context.args)

    try:
        result = c2_request("/api/command", method="POST", body={
            "client_id": client_id,
            "command": command,
        })
        if "_error" in result or "error" in result:
            await update.message.reply_text(f"C2 Error: {result}")
            return

        output = result.get("output", result.get("result", "<no output>"))
        await update.message.reply_text(f"C2 Response:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def run_agent(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /agent <goal>\n"
            "Example: /agent Enumerate SMB shares on rhost"
        )
        return

    goal = " ".join(context.args)
    await update.message.reply_text(f"Spawning autonomous agent with goal:\n{goal}\nThis may take a few minutes...")

    try:
        # Use the run_agent command from LazyOwn shell
        output = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: run_lazyown_command(f"run_agent {goal}", timeout=300),
        )
        output = strip_ansi(output)

        if len(output) > 4000:
            output = output[:3990] + "\n... [truncated]"

        await update.message.reply_text(f"Agent Result:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def delegate_task_cmd(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /delegate <goal>\n"
            "Delegates to a Hermes subagent for parallel processing."
        )
        return

    goal = " ".join(context.args)
    await update.message.reply_text(f"Delegating to Hermes subagent:\n{goal}\nThis runs in parallel...")

    try:
        # Use delegate_task via execute_code or direct shell
        output = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: run_lazyown_command(f"delegate_task {goal}", timeout=180),
        )
        output = strip_ansi(output)

        if len(output) > 4000:
            output = output[:3990] + "\n... [truncated]"

        await update.message.reply_text(f"Delegate Result:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def cron_schedule_cmd(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /cron <schedule> <command>\n"
            "Examples:\n"
            "  /cron 30m lazynmap\n"
            "  /cron '0 9 * * *' host_discover\n"
            "  /cron every 2h beacon_check"
        )
        return

    schedule = context.args[0]
    command = " ".join(context.args[1:])

    try:
        output = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: run_lazyown_command(
                f'cron_schedule add "{schedule}" "{command}"',
                timeout=30,
            ),
        )
        output = strip_ansi(output)
        await update.message.reply_text(f"Cron Result:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def status_cmd(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not session_manager.check_rate_limit(user_id):
        await update.message.reply_text("Rate limit exceeded.")
        return

    try:
        output = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: run_lazyown_command("autonomous_status", timeout=30),
        )
        output = strip_ansi(output)

        # Also check daemon
        daemon_output = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: run_lazyown_command("daemon_status", timeout=15),
        )
        daemon_output = strip_ansi(daemon_output)

        combined = f"AUTONOMOUS STATUS:\n{output}\n\nDAEMON STATUS:\n{daemon_output}"
        if len(combined) > 4000:
            combined = combined[:3990] + "\n... [truncated]"

        await update.message.reply_text(combined)
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def stop_daemon_cmd(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    try:
        output = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: run_lazyown_command("autonomous_stop", timeout=30),
        )
        output = strip_ansi(output)
        await update.message.reply_text(f"Stop Result:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


async def download_file_cmd(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not context.args:
        await update.message.reply_text("Usage: /download <filename_or_path>")
        return

    file_path = " ".join(context.args)
    full_path = LAZYOWN_DIR / "sessions" / file_path

    if not full_path.exists():
        # Try as absolute path under sessions/
        alt_path = Path(file_path)
        if alt_path.exists():
            full_path = alt_path
        else:
            await update.message.reply_text(f"File not found: {file_path}")
            return

    try:
        await update.message.reply_document(document=open(full_path, "rb"))
    except Exception as exc:
        await update.message.reply_text(f"Error sending file: {exc}")


async def handle_file_upload(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    client_id = session_manager.get_client_id(user_id)
    document = update.message.document
    file = await document.get_file()
    file_name = document.file_name

    temp_dir = LAZYOWN_DIR / "sessions" / "temp_telegram"
    temp_dir.mkdir(parents=True, exist_ok=True)
    file_path = temp_dir / f"{file.file_id}_{file_name}"

    await file.download_to_drive(str(file_path))

    if client_id:
        try:
            result = c2_request("/api/upload", method="POST", body={
                "client_id": client_id,
                "file_path": str(file_path),
            })
            output = result.get("output", result.get("result", "<no response>"))
            await update.message.reply_text(f"Uploaded to implant {client_id}:\n{output}")
        except Exception as exc:
            await update.message.reply_text(f"Upload error: {exc}")
    else:
        await update.message.reply_text(
            f"File saved locally: {file_path}\n"
            "No C2 client set. Use /addcli <client_id> to upload to implant."
        )


async def text_command(update: Update, context: CallbackContext) -> None:
    """Handle any text message as a direct LazyOwn command."""
    user_id = update.message.from_user.id

    if not session_manager.validate_session(user_id):
        await update.message.reply_text("Invalid session. Use /start <secret>")
        return

    if not session_manager.check_rate_limit(user_id):
        await update.message.reply_text("Rate limit exceeded. Max 5 commands/minute.")
        return

    command = update.message.text.strip()
    if command.startswith("/"):
        return  # Ignore unknown commands

    # Check for C2 prefix
    if command.startswith("c2 "):
        client_id = session_manager.get_client_id(user_id)
        if not client_id:
            await update.message.reply_text("No client ID set. Use /addcli <client_id> first.")
            return

        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            await update.message.reply_text("Usage: c2 <command>")
            return

        c2_cmd = parts[1]
        try:
            result = c2_request("/api/command", method="POST", body={
                "client_id": client_id,
                "command": c2_cmd,
            })
            output = result.get("output", result.get("result", "<no output>"))
            await update.message.reply_text(f"C2 Response:\n```\n{output}\n```", parse_mode="Markdown")
        except Exception as exc:
            await update.message.reply_text(f"Error: {exc}")
        return

    # Direct LazyOwn command
    await update.message.reply_text(f"Executing: {command}")

    try:
        output = await asyncio.get_event_loop().run_in_executor(
            None, lambda: run_lazyown_command(command, timeout=60)
        )
        output = strip_ansi(output)

        if len(output) > 4000:
            output = output[:3990] + "\n... [truncated]"

        await update.message.reply_text(f"Output:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as exc:
        await update.message.reply_text(f"Error: {exc}")


# ── Main ────────────────────────────────────────────────────────────────────────
async def main() -> None:
    application = Application.builder().token(telegram_token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("cmd", execute_command))
    application.add_handler(CommandHandler("sitrep", sitrep))
    application.add_handler(CommandHandler("config", config_cmd))
    application.add_handler(CommandHandler("addcli", add_cli))
    application.add_handler(CommandHandler("clients", list_clients))
    application.add_handler(CommandHandler("c2", c2_command))
    application.add_handler(CommandHandler("agent", run_agent))
    application.add_handler(CommandHandler("delegate", delegate_task_cmd))
    application.add_handler(CommandHandler("cron", cron_schedule_cmd))
    application.add_handler(CommandHandler("status", status_cmd))
    application.add_handler(CommandHandler("stop", stop_daemon_cmd))
    application.add_handler(CommandHandler("download", download_file_cmd))

    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file_upload))

    await application.run_polling()


# ── Bootstrap ───────────────────────────────────────────────────────────────────
nest_asyncio.apply()
config = load_payload()
telegram_token = config.get("telegram_token", "")
c2_pass = config.get("c2_pass", "LazyOwn")
enable_ia = config.get("enable_ia", False)

SESSION_TIMEOUT = 1800
MAX_FAILED_ATTEMPTS = 3
RATE_LIMIT = 5

if __name__ == "__main__":
    if not telegram_token:
        print("[ERROR] telegram_token not set in payload.json")
        print("Get a token from @BotFather and set it with:")
        print("  python3 -c \"import json; p=json.load(open('payload.json')); p['telegram_token']='YOUR_TOKEN'; json.dump(p,open('payload.json','w'),indent=2)\"")
        sys.exit(1)

    print("[INFO] LazyOwn Hermes Bot starting...")
    print(f"[INFO] C2 auth secret: {c2_pass[:2]}***")
    print(f"[INFO] IA enabled: {enable_ia}")
    print(f"[INFO] Sessions dir: {SESSIONS_DIR}")

    asyncio.run(main())
