"""Socket.IO terminal glue for the C2 web terminal.

Registers the ``/listener``, ``/pty`` and ``/terminal`` namespaces and
the ``/terminal`` page. Every handler mirrors the original monolith
behaviour: authentication + MFA gate, PTY fork/read-forward loop,
reverse-shell socket bridge and command execution through the shared
shell proxies.
"""

from __future__ import annotations

import fcntl
import os
import pty
import select
import struct
import subprocess
import termios

from flask import render_template, request
from flask_login import current_user, login_required
from flask_socketio import disconnect, emit

_JOIN_BUF = 1024 * 20


def set_winsize(fd: int, row: int, col: int, xpix: int = 0, ypix: int = 0) -> None:
    """Resize a pseudo-terminal.

    Args:
        fd: PTY file descriptor.
        row: Terminal rows.
        col: Terminal columns.
        xpix: Unused pixel width.
        ypix: Unused pixel height.
    """
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def register_terminal_glue(
    socketio,
    *,
    app,
    config,
    logger,
    shell,
    execute_command,
    reverse_socket,
    require_mfa_socket,
) -> None:
    """Register every terminal namespace handler on the Socket.IO server.

    Args:
        socketio: The SocketIO server instance.
        app: The Flask application owning the PTY state config keys.
        config: Active LazyConfig instance.
        logger: Lazyc2 debug logger.
        shell: Shared shell proxy exposing ``one_cmd``.
        execute_command: Beacon command executor used by ``/terminal``.
        reverse_socket: Zero-arg provider of the reverse-shell socket
            (may be None between listener restarts).
        require_mfa_socket: MFA decorator for socket handlers.
    """

    def _debug(message: str) -> None:
        if config.enable_c2_debug:
            logger.info(message)

    @socketio.on("connect", namespace="/listener")
    @login_required
    @require_mfa_socket
    def listener_connect():
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        _debug("Client connected to /listener")
        emit("output", "Welcome to LazyOwn RedTeam Framework: CRIMEN 👋\r\n$ ")

    @socketio.on("disconnect", namespace="/listener")
    @login_required
    def listener_disconnect():
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        _debug("Client disconnected from /listener")

    def read_and_forward_pty_output():
        """Read the PTY continuously and forward output over the WebSocket."""
        while True:
            socketio.sleep(0.01)
            if app.config["fd"]:
                try:
                    (data_ready, _, _) = select.select([app.config["fd"]], [], [], 0)
                    if data_ready:
                        output = os.read(app.config["fd"], _JOIN_BUF)
                        if output:
                            socketio.emit(
                                "pty-output",
                                {"output": output.decode(errors="replace")},
                                namespace="/pty",
                            )
                except Exception:
                    logger.error("Error leyendo salida:")

    @socketio.on("pty-input", namespace="/pty")
    @login_required
    @require_mfa_socket
    def pty_input(data):
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        if app.config["fd"]:
            try:
                os.write(app.config["fd"], data["input"].encode())
            except Exception:
                logger.error("Error escribiendo entrada:")

    @socketio.on("resize", namespace="/pty")
    @login_required
    @require_mfa_socket
    def resize(data):
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        if app.config["fd"]:
            _debug(f"Redimensionando terminal a {data['rows']}x{data['cols']}")
            set_winsize(app.config["fd"], data["rows"], data["cols"])

    @socketio.on("connect", namespace="/pty")
    @login_required
    @require_mfa_socket
    def pty_connect():
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        _debug("Nuevo cliente conectado")

        if app.config["child_pid"]:
            return

        try:
            (child_pid, fd) = pty.fork()

            if child_pid == 0:
                subprocess.run(["python3", "lazyown.py"], check=True)
            else:
                set_winsize(fd, 25, 120)
                app.config["fd"] = fd
                app.config["child_pid"] = child_pid

                socketio.start_background_task(read_and_forward_pty_output)
                _debug(f"Proceso hijo iniciado con PID {child_pid}")

        except Exception:
            logger.error("Error iniciando shell:")

    @socketio.on("input")
    @login_required
    @require_mfa_socket
    def handle_input(data):
        if not current_user.is_authenticated:
            print("[!] Error Unauthorized.", request.remote_addr)
            return {"error": "Unauthorized"}, 401

        command = data.get("value")
        if not command:
            return
        _debug(f"[CMD] Received: {command}")

        command_out = shell.one_cmd(command)

        shell.stdout.getvalue()
        shell.stdout.truncate(0)
        shell.stdout.seek(0)

        emit("output", command_out + "$ ")

    @socketio.on("command", namespace="/listener")
    @login_required
    @require_mfa_socket
    def listener_command(msg):
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        _debug("Received command: " + msg)
        try:
            reverse_socket().sendall((msg + "\n").encode())
        except Exception:
            emit("response", {"output": "audio"}, namespace="/listener")

    @app.route("/terminal")
    @login_required
    def terminal():
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        return render_template("terminal.html")

    @socketio.on("connect", namespace="/terminal")
    @login_required
    @require_mfa_socket
    def terminal_connect():
        if not current_user.is_authenticated:
            disconnect()
            return False
        _debug("Cliente conectado a /terminal")

    @socketio.on("disconnect", namespace="/terminal")
    @login_required
    def terminal_disconnect():
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        _debug("Cliente desconectado de /terminal")

    @socketio.on("input", namespace="/terminal")
    @login_required
    @require_mfa_socket
    def terminal_input(data):
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        command = data.get("command")
        client_id = data.get("client_id")
        if command and client_id:
            output = execute_command(command)
            socketio.emit("output", {"client_id": client_id, "output": output}, namespace="/terminal")

    @socketio.on("command", namespace="/terminal")
    @login_required
    @require_mfa_socket
    def terminal_command(data):
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        cmd = data.get("cmd")
        if not cmd:
            return
        _debug(f"Ejecutando comando: {cmd}")
        output = execute_command(cmd)
        emit("response", {"output": output})

    @socketio.on("resize", namespace="/terminal")
    @login_required
    @require_mfa_socket
    def terminal_resize(data):
        if not current_user.is_authenticated:
            print(f"[!] Error. {request.remote_addr}")
            return False
        if app.config["fd"]:
            set_winsize(app.config["fd"], data["rows"], data["cols"])
