"""Purple Sync — real-time offensive telemetry to a local SIEM.

Streams every LazyOwn action (commands executed, targets, exit status) to
an Elastic, Splunk HEC or generic webhook endpoint so the blue team can
validate detection rules against live red activity. Events are appended
to a local write-ahead spool first (``sessions/purple_sync/spool.jsonl``)
and only leave the host when the feature is explicitly enabled, so an
unconfigured install never phones home.

>>> from modules import purple_sync
>>> purple_sync.configure(siem_type="elastic", endpoint="https://127.0.0.1:9200", token="...")
>>> purple_sync.emit_command("nmap -sV 10.0.0.5")
>>> purple_sync.flush()
"""

from __future__ import annotations

import json
import re
import threading
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
SPOOL_DIR = SESSIONS_DIR / "purple_sync"
SPOOL_PATH = SPOOL_DIR / "spool.jsonl"
AUDIT_PATH = SPOOL_DIR / "sent.jsonl"

DEFAULT_BATCH_SIZE = 50
DEFAULT_TIMEOUT_SEC = 5.0
SPOOL_MAX_ROWS = 5000
SPOOL_TRIM_CHUNK = 500
REDACTED = "[REDACTED]"
MIN_PORT = 1
MAX_PORT = 65535

SIEM_ELASTIC = "elastic"
SIEM_SPLUNK = "splunk"
SIEM_WEBHOOK = "webhook"
SIEM_TYPES = (SIEM_ELASTIC, SIEM_SPLUNK, SIEM_WEBHOOK)

from core.config import load_payload  # noqa: E402

_SENDER: Callable[[str, str, str, float], tuple[int, str]] | None = None
_LOCK = threading.Lock()


@dataclass
class PurpleSyncConfig:
    """Connection and behaviour settings for one SIEM endpoint."""

    enabled: bool = False
    siem_type: str = SIEM_ELASTIC
    endpoint: str = ""
    token: str = ""
    index: str = "lazyown-purple"
    source_type: str = "lazyown:purple"
    batch_size: int = DEFAULT_BATCH_SIZE
    timeout_sec: float = DEFAULT_TIMEOUT_SEC
    verify_tls: bool = False
    redact: bool = True

    def as_dict(self) -> dict[str, Any]:
        """Return the payload.json-serialisable configuration."""
        return {
            "enabled": self.enabled,
            "siem_type": self.siem_type,
            "endpoint": self.endpoint,
            "token": self.token,
            "index": self.index,
            "source_type": self.source_type,
            "batch_size": self.batch_size,
            "timeout_sec": self.timeout_sec,
            "verify_tls": self.verify_tls,
            "redact": self.redact,
        }


def load_config() -> PurpleSyncConfig:
    """Build the configuration from ``payload.json`` (``purple_sync`` key).

    Returns:
        A fully populated :class:`PurpleSyncConfig`; unknown siem types
        fall back to ``elastic``.
    """
    from core.config import load_payload

    section = {}
    try:
        section = dict((load_payload() or {}).get("purple_sync") or {})
    except Exception:
        section = {}
    config = PurpleSyncConfig()
    for key, value in section.items():
        if hasattr(config, key):
            setattr(config, key, value)
    if config.siem_type not in SIEM_TYPES:
        config.siem_type = SIEM_ELASTIC
    return config


def save_config(config: PurpleSyncConfig) -> dict[str, Any]:
    """Persist the configuration under the ``purple_sync`` payload key.

    Args:
        config: Configuration to store.

    Returns:
        The stored mapping.
    """
    from utils import lazyown_set_config

    data = config.as_dict()
    lazyown_set_config("purple_sync", data)
    return data


def redact_secret(text: str) -> str:
    """Mask password-shaped fragments inside a command line.

    Args:
        text: Raw command or argument string.

    Returns:
        Text with ``password=...``, ``pass:...``, ``-p <secret>`` and
        long token-looking fragments replaced by ``[REDACTED]``.
    """
    out = re.sub(
        r"(?i)\b(pass(?:word)?|secret|token|apikey|api_key)\s*[=:\s]\s*(\S+)",
        r"\1 " + REDACTED,
        text,
    )

    def _password_flag(match: re.Match) -> str:
        value = match.group(3)
        if re.fullmatch(r"[0-9,:\-]+", value):
            return match.group(0)
        return f"{match.group(1)}{match.group(2)} {REDACTED}"

    out = re.sub(
        r"(?i)(^|\s)(-p|--password)\s+(\S+)",
        _password_flag,
        out,
    )
    out = re.sub(r"\b[A-Za-z0-9_\-]{32,}\b", REDACTED, out)
    return out


def _default_sender(url: str, headers: str, body: str, timeout: float) -> tuple[int, str]:
    """Perform the HTTP POST used when no sender is injected.

    Local SIEM deployments usually run with self-signed certificates, so
    TLS verification defaults to disabled and the resulting urllib3
    warning is silenced for this call only.

    Args:
        url: Fully qualified SIEM endpoint.
        headers: JSON encoded ``{header: value}`` mapping.
        body: Serialized request payload.
        timeout: Per-request timeout in seconds.

    Returns:
        ``(status_code, body_text)`` from the remote endpoint.
    """
    import warnings

    import requests
    import urllib3

    parsed = json.loads(headers)
    verify = parsed.pop("verify", False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(
            url,
            data=body.encode("utf-8"),
            headers=parsed,
            timeout=timeout,
            verify=verify,
        )
    return response.status_code, response.text[:2048]


class PurpleSync:
    """Spool and forward LazyOwn offensive events to a local SIEM."""

    def __init__(
        self,
        config: PurpleSyncConfig | None = None,
        sender: Callable[[str, str, str, float], tuple[int, str]] | None = None,
        spool_path: Path | None = None,
        audit_path: Path | None = None,
        payload_reader: Callable[[], dict[str, Any]] | None = None,
    ) -> None:
        """Initialize the sync engine.

        Args:
            config: Connection settings; defaults to :func:`load_config`.
            sender: Injected transport ``(url, headers_json, body, timeout)
                -> (status, text)``; defaults to :func:`_default_sender`.
            spool_path: Write-ahead file; defaults to ``sessions/`` layout.
            audit_path: File recording successfully forwarded events.
            payload_reader: Config source override used by tests.
        """
        self._config = config if config is not None else PurpleSyncConfig()
        self._sender = sender
        self._spool_path = spool_path or SPOOL_PATH
        self._audit_path = audit_path or AUDIT_PATH
        self._payload_reader = payload_reader
        self._context: dict[str, Any] = {}

    @property
    def config(self) -> PurpleSyncConfig:
        """Current configuration object."""
        return self._config

    def configure(self, config: PurpleSyncConfig) -> None:
        """Replace the active configuration.

        Args:
            config: New settings.
        """
        self._config = config

    def set_context(self, **fields: Any) -> None:
        """Attach engagement context (rhost, phase, task) to future events.

        Args:
            fields: Context keys forwarded into every event.
        """
        for key, value in fields.items():
            if value:
                self._context[key] = value

    def _resolve(self, key: str, default: Any = "") -> Any:
        """Resolve ``key`` from live payload.json, falling back to config.

        Args:
            key: Configuration key.
            default: Value when neither source defines it.

        Returns:
            The resolved value.
        """
        try:
            if self._payload_reader is not None:
                section = dict((self._payload_reader() or {}).get("purple_sync") or {})
                if key in section:
                    return section[key]
            else:
                section = dict((load_payload() or {}).get("purple_sync") or {})
                if key in section:
                    return section[key]
        except Exception:
            pass
        return getattr(self._config, key, default)

    def _endpoint(self) -> str:
        """Resolve the SIEM endpoint URL.

        Returns:
            Endpoint string; may be empty when unconfigured.
        """
        endpoint = str(self._resolve("endpoint", ""))
        if self._config.endpoint and self._config.endpoint != endpoint:
            endpoint = self._config.endpoint
        return endpoint

    def build_event(self, command: str, exit_code: int | None = None, category: str = "") -> dict[str, Any]:
        """Build one normalized ECS-flavoured event.

        Args:
            command: Executed command line.
            exit_code: Process exit status when known.
            category: Kill-chain category when known.

        Returns:
            JSON-serialisable event dictionary.
        """
        try:
            payload = load_payload() or {}
        except Exception:
            payload = {}
        rhost = payload.get("rhost") or self._context.get("rhost") or ""
        lhost = payload.get("lhost") or self._context.get("lhost") or ""
        phase = payload.get("phase") or self._context.get("phase") or ""
        event: dict[str, Any] = {
            "@timestamp": datetime.now(UTC).isoformat(),
            "event": {
                "action": "lazyown_command",
                "dataset": "lazyown.purple",
                "module": "lazyown",
                "kind": "event",
                "outcome": "success" if exit_code in (0, None) else "failure",
            },
            "observer": {"product": "LazyOwn", "type": "redteam-framework"},
            "host": {"ip": str(rhost)},
            "lazyown": {
                "operator_host": str(lhost),
                "command": redact_secret(str(command)) if self._resolve("redact", True) else str(command),
                "target": str(rhost),
                "phase": str(phase),
                "category": str(category),
                "exit_code": exit_code,
            },
        }
        technique = self._context.get("technique_id")
        if technique:
            event["lazyown"]["technique_id"] = technique
        return event

    def _append_row(self, path: Path, row: dict[str, Any]) -> None:
        """Append one JSON row to a jsonl file, creating parents.

        Args:
            path: Target file.
            row: Serializable row.
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
        except OSError:
            pass

    def _read_spool(self) -> list[dict[str, Any]]:
        """Read pending events from the spool file.

        Returns:
            List of event dictionaries; corrupt rows are skipped.
        """
        if not self._spool_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        try:
            for line in self._spool_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
        except OSError:
            return []
        return rows

    def _write_spool(self, rows: list[dict[str, Any]]) -> None:
        """Atomically rewrite the spool file with the supplied rows.

        Args:
            rows: Events that remain pending.
        """
        if len(rows) > SPOOL_MAX_ROWS:
            rows = rows[-SPOOL_MAX_ROWS:]
        try:
            self._spool_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._spool_path.with_suffix(".tmp")
            with tmp.open("w", encoding="utf-8") as handle:
                for row in rows:
                    handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
            tmp.replace(self._spool_path)
        except OSError:
            pass

    def emit(self, event: dict[str, Any]) -> bool:
        """Queue one event: spool locally, then forward when enabled.

        Args:
            event: Serializable event dictionary.

        Returns:
            True when the event was forwarded (or dropped intentionally),
            False when it stayed in the local spool.
        """
        self._append_row(self._spool_path, event)
        if not bool(self._resolve("enabled", False)):
            return False
        return self._send_batch()

    def emit_command(self, command: str, exit_code: int | None = None, category: str = "") -> bool:
        """Capture one executed command as a SIEM event.

        Args:
            command: Command line that ran.
            exit_code: Exit status when known.
            category: Kill-chain category when known.

        Returns:
            True when forwarded to the SIEM.
        """
        return self.emit(self.build_event(command, exit_code=exit_code, category=category))

    def _elastic_envelope(self, events: list[dict[str, Any]]) -> tuple[str, str, str]:
        """Build the Elastic ``_bulk`` request.

        Args:
            events: Events to forward.

        Returns:
            ``(url, headers_json, body)`` triple.
        """
        endpoint = self._endpoint().rstrip("/")
        index = str(self._resolve("index", "lazyown-purple"))
        lines = [json.dumps({"index": {"_index": index}}, ensure_ascii=False)]
        lines.extend(json.dumps(event, ensure_ascii=False, default=str) for event in events)
        headers = {"Content-Type": "application/x-ndjson", "verify": self._config.verify_tls}
        token = str(self._resolve("token", ""))
        if token:
            headers["Authorization"] = f"Basic {token}"
        return f"{endpoint}/_bulk", json.dumps(headers), "\n".join(lines) + "\n"

    def _splunk_envelope(self, events: list[dict[str, Any]]) -> tuple[str, str, str]:
        """Build the Splunk HEC request.

        Args:
            events: Events to forward.

        Returns:
            ``(url, headers_json, body)`` triple.
        """
        endpoint = self._endpoint().rstrip("/")
        source_type = str(self._resolve("source_type", "lazyown:purple"))
        token = str(self._resolve("token", ""))
        rows = []
        for event in events:
            rows.append(json.dumps({"event": event, "sourcetype": source_type}, ensure_ascii=False, default=str))
        headers = {"Content-Type": "application/json", "verify": self._config.verify_tls}
        if token:
            headers["Authorization"] = f"Splunk {token}"
        return f"{endpoint}/services/collector/event", json.dumps(headers), "\n".join(rows)

    def _webhook_envelope(self, events: list[dict[str, Any]]) -> tuple[str, str, str]:
        """Build the generic webhook request.

        Args:
            events: Events to forward.

        Returns:
            ``(url, headers_json, body)`` triple.
        """
        headers = {"Content-Type": "application/json", "verify": self._config.verify_tls}
        token = str(self._resolve("token", ""))
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return self._endpoint(), json.dumps(headers), json.dumps({"events": events}, ensure_ascii=False, default=str)

    def _envelope(self, events: list[dict[str, Any]]) -> tuple[str, str, str] | None:
        """Select the adapter envelope for the configured SIEM type.

        Args:
            events: Events to forward.

        Returns:
            Adapter triple or None for an unknown type.
        """
        siem_type = str(self._resolve("siem_type", SIEM_ELASTIC))
        if siem_type == SIEM_ELASTIC:
            return self._elastic_envelope(events)
        if siem_type == SIEM_SPLUNK:
            return self._splunk_envelope(events)
        if siem_type == SIEM_WEBHOOK:
            return self._webhook_envelope(events)
        return None

    def _sender_call(self, url: str, headers: str, body: str) -> tuple[int, str]:
        """Invoke the configured transport.

        Args:
            url: Endpoint URL.
            headers: JSON encoded headers.
            body: Request payload.

        Returns:
            ``(status, text)``; ``(0, error)`` on transport failure.
        """
        timeout = float(self._resolve("timeout_sec", DEFAULT_TIMEOUT_SEC) or DEFAULT_TIMEOUT_SEC)
        sender = self._sender or _SENDER or _default_sender
        try:
            return sender(url, headers, body, timeout)
        except Exception as exc:
            return 0, str(exc)

    def _send_batch(self, batch_size: int | None = None) -> bool:
        """Forward up to ``batch_size`` spooled events.

        Args:
            batch_size: Override for the configured batch size.

        Returns:
            True when at least one batch was accepted (2xx) or the spool
            was empty; False when the SIEM rejected or the batch failed.
        """
        rows = self._read_spool()
        if not rows:
            return True
        limit = int(batch_size or self._resolve("batch_size", DEFAULT_BATCH_SIZE) or DEFAULT_BATCH_SIZE)
        batch = rows[:limit]
        envelope = self._envelope(batch)
        if envelope is None:
            return False
        url, headers, body = envelope
        status, text = self._sender_call(url, headers, body)
        if 200 <= status < 300:
            self._write_spool(rows[len(batch) :])
            for row in batch:
                self._append_row(self._audit_path, row)
            return True
        return False

    def flush(self, batch_size: int | None = None) -> int:
        """Drain the spool to the SIEM.

        Args:
            batch_size: Override for the configured batch size.

        Returns:
            Number of events successfully forwarded.
        """
        if not bool(self._resolve("enabled", False)):
            return 0
        sent = 0
        while True:
            pending = len(self._read_spool())
            if pending == 0:
                break
            if not self._send_batch(batch_size):
                break
            remaining = len(self._read_spool())
            sent += pending - remaining
            if remaining >= pending:
                break
        return sent

    def status(self) -> dict[str, Any]:
        """Report the current sync state.

        Returns:
            Mapping with ``enabled``, ``siem_type``, ``endpoint_set``,
            ``pending`` and ``sent`` counters.
        """
        return {
            "enabled": bool(self._resolve("enabled", False)),
            "siem_type": str(self._resolve("siem_type", SIEM_ELASTIC)),
            "endpoint_set": bool(self._endpoint()),
            "pending": len(self._read_spool()),
            "sent": _count_rows(self._audit_path),
        }

    def test_event(self) -> dict[str, Any]:
        """Emit one synthetic connectivity event.

        Returns:
            The emitted event dictionary.
        """
        event = self.build_event("purple_sync test-event", exit_code=0, category="other")
        event["event"]["action"] = "lazyown_purple_sync_test"
        self.emit(event)
        return event


def _count_rows(path: Path) -> int:
    """Count rows in a jsonl file without loading it fully.

    Args:
        path: File to inspect.

    Returns:
        Number of non-empty lines; 0 when missing.
    """
    if not path.exists():
        return 0
    try:
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    except OSError:
        return 0


_SYNC: PurpleSync | None = None


def get_sync() -> PurpleSync:
    """Return the process-wide sync engine.

    Returns:
        The shared :class:`PurpleSync` instance.
    """
    global _SYNC
    if _SYNC is None:
        _SYNC = PurpleSync(load_config())
    return _SYNC


def reset_sync() -> None:
    """Drop the shared engine (tests)."""
    global _SYNC
    _SYNC = None


def configure(
    siem_type: str = SIEM_ELASTIC, endpoint: str = "", token: str = "", index: str = "lazyown-purple", **overrides: Any
) -> dict[str, Any]:
    """Configure and persist the shared sync engine.

    Args:
        siem_type: One of ``elastic``, ``splunk``, ``webhook``.
        endpoint: SIEM URL.
        token: Auth token (Splunk HEC value, Elastic basic auth, bearer).
        index: Elastic index name.
        overrides: Extra config keys (``batch_size``, ``timeout_sec``, ...).

    Returns:
        The persisted configuration mapping.
    """
    config = load_config()
    config.siem_type = siem_type
    config.endpoint = endpoint
    config.token = token
    config.index = index
    for key, value in overrides.items():
        if hasattr(config, key):
            setattr(config, key, value)
    data = save_config(config)
    get_sync().configure(config)
    return data


def emit_command(command: str, exit_code: int | None = None, category: str = "") -> bool:
    """Capture one command through the shared engine.

    Args:
        command: Command line that ran.
        exit_code: Exit status when known.
        category: Kill-chain category when known.

    Returns:
        True when the event reached the SIEM.
    """
    sync = get_sync()
    sync.set_context(**_context_from_payload())
    return sync.emit_command(command, exit_code=exit_code, category=category)


def _context_from_payload() -> dict[str, Any]:
    """Derive engagement context keys from payload.json.

    Returns:
        Mapping with ``rhost``, ``lhost`` and ``phase`` when set.
    """
    from core.config import load_payload

    try:
        payload = load_payload() or {}
    except Exception:
        return {}
    context: dict[str, Any] = {}
    for key in ("rhost", "lhost", "phase", "technique_id"):
        if payload.get(key):
            context[key] = payload.get(key)
    return context


def hook_command(command: str, exit_code: int | None = None) -> None:
    """Run-command hook: capture executed commands, never raises.

    Args:
        command: Command line that ran.
        exit_code: Exit status when known.
    """
    try:
        emit_command(command, exit_code=exit_code)
    except Exception:
        pass


def status() -> dict[str, Any]:
    """Report the shared engine status.

    Returns:
        Status mapping from :meth:`PurpleSync.status`.
    """
    return get_sync().status()


def flush(batch_size: int | None = None) -> int:
    """Drain the shared spool.

    Args:
        batch_size: Optional per-batch override.

    Returns:
        Number of forwarded events.
    """
    return get_sync().flush(batch_size)


def test_event() -> dict[str, Any]:
    """Emit one synthetic event through the shared engine.

    Returns:
        The emitted event.
    """
    return get_sync().test_event()


def backfill(paths: list[str], batch_size: int | None = None) -> int:
    """Forward historical audit logs through the shared engine.

    Args:
        paths: JSONL files whose rows carry events to forward.
        batch_size: Optional per-batch override.

    Returns:
        Number of forwarded events.
    """
    sync = get_sync()
    total = 0
    for raw_path in paths:
        path = Path(raw_path).expanduser()
        if not path.exists():
            continue
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                sync.emit(row)
                total += 1
        except OSError:
            continue
    total += sync.flush(batch_size)
    return total
