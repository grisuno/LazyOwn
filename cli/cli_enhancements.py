"""CLI enhancement primitives for the LazyOwn interactive shell.

This module exposes SOLID, framework-agnostic building blocks used by the
``cli/commands/audit.py`` CommandSet to extend the LazyOwn shell with:

- Fuzzy command discovery (item 4).
- Payload-aware tab completion (item 5).
- Dynamic alias resolution at execution time (item 6).
- Hot-reload of declarative addons / Lua plugins (item 7).
- Live tail of long-running commands' partial output (item 8).
- Transcript indexing + grep across recent command outputs (item 10).
- Interactive forms for commands with many parameters (item 11).

Design notes
------------
- Each primitive depends on small ``typing.Protocol`` interfaces so unit
  tests can substitute fakes without spinning up a cmd2 shell.
- Filesystem and runtime side effects live in concrete adaptors only;
  the algorithmic core is pure.
- No imports from ``lazyown.py`` are allowed: the shell composes these
  primitives, not the other way around (Dependency Inversion).
"""

from __future__ import annotations

import json
import re
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Callable, Iterable, Protocol, Sequence

# ── Protocols (Interface Segregation) ────────────────────────────────────────


class PayloadProvider(Protocol):
    """Read-only view onto ``payload.json`` style configuration."""

    def get(self, key: str, default: Any = None) -> Any: ...
    def keys(self) -> Iterable[str]: ...


class CommandLister(Protocol):
    """Source of command metadata for indexing / fuzzy matching."""

    def commands(self) -> list[CommandInfo]: ...


class TerminalIO(Protocol):
    """Minimal duck-typed prompt/print pair so tests can fake it."""

    def prompt(self, message: str, default: str = "") -> str: ...
    def emit(self, line: str) -> None: ...


@dataclass(frozen=True)
class CommandInfo:
    """Lightweight description of a shell command."""

    name: str
    summary: str = ""
    phase: str = ""
    category: str = ""
    aliases: tuple[str, ...] = ()


# ── Fuzzy command index (item 4) ─────────────────────────────────────────────


@dataclass(frozen=True)
class FuzzyMatch:
    """A scored fuzzy match against a CommandInfo."""

    info: CommandInfo
    score: float
    matched_field: str


class FuzzyCommandIndex:
    """Search a command catalogue with token-aware fuzzy matching.

    Scoring favours exact and prefix matches over substring and
    similarity-only hits, then falls back to ``difflib.SequenceMatcher``
    so the index degrades gracefully when ``rapidfuzz`` is missing.
    """

    def __init__(self, source: CommandLister) -> None:
        self._source = source

    def search(self, query: str, limit: int = 25) -> list[FuzzyMatch]:
        """Return the top ``limit`` matches ordered by descending score."""
        q = (query or "").strip().lower()
        commands = self._source.commands()
        if not q:
            return [FuzzyMatch(info=c, score=1.0, matched_field="name") for c in commands[:limit]]
        scored: list[FuzzyMatch] = []
        for c in commands:
            best_score, best_field = self._score(c, q)
            if best_score > 0:
                scored.append(FuzzyMatch(c, best_score, best_field))
        scored.sort(key=lambda m: (-m.score, m.info.name))
        return scored[:limit]

    @staticmethod
    def _score(info: CommandInfo, q: str) -> tuple[float, str]:
        haystacks = (
            ("name", info.name.lower()),
            *(("alias", a.lower()) for a in info.aliases),
            ("summary", info.summary.lower()),
        )
        best = (0.0, "")
        for field_name, value in haystacks:
            if not value:
                continue
            if value == q:
                score = 1.0
            elif value.startswith(q):
                score = 0.9
            elif q in value:
                score = 0.7
            else:
                score = SequenceMatcher(None, value, q).ratio() * 0.6
                if score < 0.45:
                    score = 0.0
            if score > best[0]:
                best = (score, field_name)
        return best


# ── Payload-aware completion (item 5) ────────────────────────────────────────


@dataclass(frozen=True)
class CompletionResult:
    """A single tab-completion suggestion."""

    text: str
    description: str = ""


class PayloadAwareCompleter:
    """Suggest values from ``payload.json`` for context-sensitive arguments.

    The completer is intentionally simple — it inspects the command name and
    the partial token under the cursor and returns suggestions drawn from:

    - ``rhost`` and ``targets[*].ip`` for ``set rhost``, ``set domain`` etc.
    - Wordlist files on disk for ``gobuster``, ``ffuf``, ``hashcat``.
    - Available addons and Lua plugins for ``run`` / ``reload``.
    - Stored credentials for ``evil``, ``cme``, ``secretsdump``.

    The shell's existing ``complete_*`` per-command hooks remain authoritative
    where they exist; this helper is invoked from ``completedefault`` to fill
    the gap for the ~280 commands that don't define their own.
    """

    _WORDLIST_KEYS = ("dirwordlist", "usrwordlist", "dnswordlist", "iiswordlist", "wordlist")
    _FILESYSTEM_HINTS = ("/usr/share/wordlists", "/usr/share/seclists")

    def __init__(
        self,
        payload: PayloadProvider,
        addon_lister: Callable[[], Sequence[str]] | None = None,
        plugin_lister: Callable[[], Sequence[str]] | None = None,
        credential_lister: Callable[[], Sequence[str]] | None = None,
    ) -> None:
        self._payload = payload
        self._addons = addon_lister or (lambda: [])
        self._plugins = plugin_lister or (lambda: [])
        self._creds = credential_lister or (lambda: [])

    def complete(self, command: str, partial: str) -> list[CompletionResult]:
        """Return suggestions for ``partial`` given the leading ``command``."""
        cmd = (command or "").lower().strip()
        partial = partial or ""

        suggestions: list[CompletionResult] = []
        if cmd in {"set", "assign"}:
            suggestions.extend(self._suggest_payload_keys(partial))
        elif cmd in {"target", "use"}:
            suggestions.extend(self._suggest_targets(partial))
        elif cmd in {"gobuster", "ffuf", "feroxbuster", "subwfuzz"}:
            suggestions.extend(self._suggest_wordlist_keys(partial))
        elif cmd in {"run", "reload", "addon"}:
            suggestions.extend(self._suggest_addons(partial))
        elif cmd in {"plugin", "lua"}:
            suggestions.extend(self._suggest_plugins(partial))
        elif cmd in {"evil", "evil-winrm", "cme", "crackmapexec", "secretsdump"}:
            suggestions.extend(self._suggest_credentials(partial))
        return [s for s in suggestions if s.text.startswith(partial)]

    def _suggest_payload_keys(self, partial: str) -> list[CompletionResult]:
        return [
            CompletionResult(k, f"payload.json key (current={self._payload.get(k)})")
            for k in sorted(self._payload.keys())
        ]

    def _suggest_targets(self, partial: str) -> list[CompletionResult]:
        targets = self._payload.get("targets", []) or []
        ips: list[CompletionResult] = []
        rhost = self._payload.get("rhost")
        if isinstance(rhost, str) and rhost:
            ips.append(CompletionResult(rhost, "payload.rhost"))
        for t in targets:
            if isinstance(t, dict) and t.get("ip"):
                ips.append(CompletionResult(t["ip"], t.get("notes", "")[:60]))
        return ips

    def _suggest_wordlist_keys(self, partial: str) -> list[CompletionResult]:
        out = []
        for k in self._WORDLIST_KEYS:
            v = self._payload.get(k)
            if v:
                out.append(CompletionResult(k, str(v)))
        return out

    def _suggest_addons(self, partial: str) -> list[CompletionResult]:
        return [CompletionResult(name, "addon") for name in self._addons()]

    def _suggest_plugins(self, partial: str) -> list[CompletionResult]:
        return [CompletionResult(name, "plugin") for name in self._plugins()]

    def _suggest_credentials(self, partial: str) -> list[CompletionResult]:
        return [CompletionResult(c, "captured credential") for c in self._creds()]


# ── Dynamic alias resolution (item 6) ────────────────────────────────────────


class AliasResolver(ABC):
    """Resolves alias templates into executable command strings."""

    @abstractmethod
    def expand(self, alias_name: str, raw_template: str, payload: PayloadProvider) -> str:
        """Return the alias rendered against the current payload."""


class DynamicAliasResolver(AliasResolver):
    """Resolve placeholders at execution time, not at shell load.

    The previous loader pre-substituted ``{rhost}`` etc. against the payload
    snapshot taken at startup. That meant editing ``payload.json`` at runtime
    (e.g. via ``set rhost X``) only affected commands invoked through cmd2's
    onecmd_plus_hooks pathway. This resolver always renders against the
    payload provided by the caller, so a ``set rhost`` immediately propagates
    to every alias the operator types next.
    """

    _PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def expand(self, alias_name: str, raw_template: str, payload: PayloadProvider) -> str:
        def _sub(m: re.Match[str]) -> str:
            key = m.group(1)
            value = payload.get(key)
            return "" if value is None else str(value)

        try:
            return self._PLACEHOLDER_RE.sub(_sub, raw_template)
        except Exception:
            return raw_template


# ── Hot reload (item 7) ──────────────────────────────────────────────────────


class HotReloader(ABC):
    """Notify subscribers when a watched directory changes."""

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...


class AddonHotReloader(HotReloader):
    """Polling watcher over ``lazyaddons/`` and ``plugins/``.

    A polling loop is intentionally chosen over watchdog inotify so this
    works on remote shells, in containers, and over NFS — environments where
    inotify is unreliable. Pass a fast tick (e.g. 2.0s) when used interactively.
    """

    def __init__(
        self,
        directories: Sequence[Path | str],
        on_change: Callable[[Path], None],
        tick_seconds: float = 2.0,
    ) -> None:
        self._dirs = [Path(d) for d in directories]
        self._on_change = on_change
        self._tick = max(0.25, tick_seconds)
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._snapshot: dict[Path, float] = {}

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._snapshot = self._scan()
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop,
            name="lazyown-hotreload",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    def poll_once(self) -> list[Path]:
        """Run a single scan, fire callbacks for changed paths, return them."""
        current = self._scan()
        changed: list[Path] = []
        for p, mtime in current.items():
            if self._snapshot.get(p) != mtime:
                changed.append(p)
        for p in self._snapshot.keys() - current.keys():
            changed.append(p)
        self._snapshot = current
        for p in changed:
            try:
                self._on_change(p)
            except Exception:
                continue
        return changed

    def _loop(self) -> None:
        while not self._stop.is_set():
            self.poll_once()
            self._stop.wait(self._tick)

    def _scan(self) -> dict[Path, float]:
        snap: dict[Path, float] = {}
        for d in self._dirs:
            if not d.exists():
                continue
            for fp in d.rglob("*"):
                if not fp.is_file():
                    continue
                if fp.suffix.lower() not in (".yaml", ".yml", ".lua"):
                    continue
                try:
                    snap[fp] = fp.stat().st_mtime
                except OSError:
                    continue
        return snap


# ── Live status tail (item 8) ────────────────────────────────────────────────


@dataclass(frozen=True)
class StatusUpdate:
    """One progress observation parsed from a partial scan output."""

    ports_seen: int = 0
    open_ports: tuple[int, ...] = ()
    last_line: str = ""
    completed_pct: float | None = None


class LiveStatusTail:
    """Parse a partial nmap / pwntomate file and emit a structured update.

    The parser is best-effort and forgiving: anything it doesn't recognise
    becomes ``last_line`` so the operator still sees something live.
    """

    _OPEN_RE = re.compile(r"^\s*(\d{1,5})/tcp\s+open\b", re.MULTILINE)
    _PCT_RE = re.compile(r"about\s+([\d.]+)%\s+done", re.IGNORECASE)
    _STATS_RE = re.compile(r"Stats:.*?(\d+)\s+open", re.IGNORECASE)

    def parse(self, content: str) -> StatusUpdate:
        if not content:
            return StatusUpdate()
        ports = sorted({int(m.group(1)) for m in self._OPEN_RE.finditer(content)})
        pct: float | None = None
        for m in self._PCT_RE.finditer(content):
            try:
                pct = float(m.group(1))
            except ValueError:
                continue
        last_line = ""
        for line in reversed(content.splitlines()):
            stripped = line.strip()
            if stripped:
                last_line = stripped
                break
        ports_seen = len(ports)
        if not ports_seen:
            stats = self._STATS_RE.search(content)
            if stats:
                try:
                    ports_seen = int(stats.group(1))
                except ValueError:
                    pass
        return StatusUpdate(
            ports_seen=ports_seen,
            open_ports=tuple(ports),
            last_line=last_line[:240],
            completed_pct=pct,
        )


# ── Transcript grep (item 10) ────────────────────────────────────────────────


@dataclass
class TranscriptEntry:
    """A captured command + output pair."""

    timestamp: float
    command: str
    output: str
    artefacts: tuple[str, ...] = ()


class TranscriptStore:
    """In-memory ring buffer of recent command outputs with regex grep.

    Persists to ``sessions/_cli_transcript.jsonl`` so a restart does not lose
    the history; on startup the most recent ``capacity`` entries are loaded
    back. Each entry stores: timestamp, command, output (truncated to
    ``max_output_chars``), and artefact paths the command claims to have
    produced (informational only).
    """

    def __init__(
        self,
        sessions_dir: Path | str,
        capacity: int = 200,
        max_output_chars: int = 64 * 1024,
    ) -> None:
        self._dir = Path(sessions_dir)
        self._capacity = capacity
        self._max_output = max_output_chars
        self._buffer: list[TranscriptEntry] = []
        self._lock = threading.Lock()
        self._path = self._dir / "_cli_transcript.jsonl"
        self._load()

    def append(self, command: str, output: str, artefacts: Iterable[str] = ()) -> None:
        clipped = (output or "")[: self._max_output]
        entry = TranscriptEntry(
            timestamp=time.time(),
            command=command,
            output=clipped,
            artefacts=tuple(artefacts),
        )
        with self._lock:
            self._buffer.append(entry)
            if len(self._buffer) > self._capacity:
                self._buffer = self._buffer[-self._capacity :]
        self._persist(entry)

    def grep(
        self,
        pattern: str,
        command_filter: str | None = None,
        limit: int = 50,
        case_insensitive: bool = True,
    ) -> list[dict[str, Any]]:
        """Return matching lines across all stored outputs."""
        try:
            rx = re.compile(pattern, re.IGNORECASE if case_insensitive else 0)
        except re.error as exc:
            return [{"error": f"invalid_regex: {exc}"}]
        matches: list[dict[str, Any]] = []
        with self._lock:
            entries = list(self._buffer)
        for entry in reversed(entries):
            if command_filter and command_filter not in entry.command:
                continue
            for i, line in enumerate(entry.output.splitlines(), 1):
                if rx.search(line):
                    matches.append(
                        {
                            "command": entry.command,
                            "line_no": i,
                            "line": line[:240],
                            "ts": entry.timestamp,
                        }
                    )
                    if len(matches) >= limit:
                        return matches
        return matches

    def list(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "ts": e.timestamp,
                    "command": e.command,
                    "output_chars": len(e.output),
                    "artefacts": list(e.artefacts),
                }
                for e in list(self._buffer)[-limit:][::-1]
            ]

    def _persist(self, entry: TranscriptEntry) -> None:
        try:
            self._dir.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(
                    json.dumps(
                        {
                            "ts": entry.timestamp,
                            "command": entry.command,
                            "output": entry.output,
                            "artefacts": list(entry.artefacts),
                        }
                    )
                    + "\n"
                )
        except OSError:
            pass

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            lines = self._path.read_text(encoding="utf-8").splitlines()
        except OSError:
            return
        loaded: list[TranscriptEntry] = []
        for raw in lines[-self._capacity :]:
            try:
                d = json.loads(raw)
                loaded.append(
                    TranscriptEntry(
                        timestamp=float(d.get("ts", 0)),
                        command=d.get("command", ""),
                        output=d.get("output", ""),
                        artefacts=tuple(d.get("artefacts", []) or ()),
                    )
                )
            except (json.JSONDecodeError, ValueError):
                continue
        self._buffer = loaded


# ── Interactive forms (item 11) ──────────────────────────────────────────────


@dataclass(frozen=True)
class FormField:
    """Specification for one input in an interactive form."""

    name: str
    description: str = ""
    default: Any = None
    required: bool = False
    options: tuple[str, ...] = ()


@dataclass(frozen=True)
class FormSpec:
    """A bundle of form fields plus a target command name."""

    command: str
    fields: tuple[FormField, ...]
    summary: str = ""


class _DefaultTerminalIO:
    """Std-in/out adaptor; falls back to non-interactive defaults gracefully."""

    def prompt(self, message: str, default: str = "") -> str:
        try:
            raw = input(message)
        except EOFError:
            return default
        return raw if raw != "" else default

    def emit(self, line: str) -> None:
        print(line)


class InteractiveForm:
    """Walk the operator through a form, returning a populated dict.

    Validates required fields and accepts ``options`` constraints. Falls back
    to defaults silently when the IO layer is non-interactive (CI, scripts).
    """

    def __init__(self, io: TerminalIO | None = None) -> None:
        self._io = io or _DefaultTerminalIO()

    def render(self, spec: FormSpec, defaults: dict[str, Any] | None = None) -> dict[str, Any]:
        merged: dict[str, Any] = {}
        defaults = defaults or {}
        self._io.emit(f"Form for: {spec.command}")
        if spec.summary:
            self._io.emit(f"  {spec.summary}")
        for field_spec in spec.fields:
            current_default = defaults.get(field_spec.name, field_spec.default)
            label = self._field_label(field_spec, current_default)
            value = self._io.prompt(label, "" if current_default is None else str(current_default))
            value = value.strip() if isinstance(value, str) else value
            if value == "" and field_spec.required and not current_default:
                self._io.emit(f"  [!] {field_spec.name} is required.")
                value = self._io.prompt(label, "")
            if field_spec.options and value not in field_spec.options:
                self._io.emit(f"  [!] {value!r} not in allowed options {list(field_spec.options)}; using default.")
                value = "" if current_default is None else str(current_default)
            merged[field_spec.name] = value if value != "" else current_default
        return merged

    @staticmethod
    def _field_label(field_spec: FormField, default: Any) -> str:
        bits = [field_spec.name]
        if field_spec.required:
            bits.append("(required)")
        if field_spec.description:
            bits.append(f"- {field_spec.description}")
        if default not in (None, ""):
            bits.append(f"[{default}]")
        if field_spec.options:
            bits.append(f"<{'|'.join(field_spec.options)}>")
        return " ".join(bits) + ": "


# ── Adaptors (Concrete glue, easy to swap in tests) ──────────────────────────


class DictPayloadProvider:
    """Wrap any plain ``dict`` so it satisfies :class:`PayloadProvider`."""

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self._data = data or {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def keys(self) -> Iterable[str]:
        return list(self._data.keys())

    def update(self, data: dict[str, Any]) -> None:
        self._data.update(data)


class StaticCommandLister:
    """Source for FuzzyCommandIndex backed by a fixed list of CommandInfo."""

    def __init__(self, commands: Sequence[CommandInfo]) -> None:
        self._commands = list(commands)

    def commands(self) -> list[CommandInfo]:
        return list(self._commands)


def commands_from_cmd2_shell(shell: Any) -> list[CommandInfo]:
    """Best-effort extraction of CommandInfo entries from a live cmd2 shell.

    Uses ``shell.get_all_commands()`` when available; otherwise falls back
    to scanning ``do_*`` attributes. Aliases are pulled from ``shell.aliases``.
    """
    seen: dict[str, CommandInfo] = {}
    aliases_for: dict[str, list[str]] = {}
    aliases = getattr(shell, "aliases", {}) or {}
    for alias_name, target in aliases.items():
        if isinstance(target, str):
            target_cmd = target.split(None, 1)[0]
            aliases_for.setdefault(target_cmd, []).append(alias_name)

    if hasattr(shell, "get_all_commands"):
        for name in shell.get_all_commands():
            seen[name] = CommandInfo(
                name=name,
                summary=_extract_doc(shell, name),
                aliases=tuple(aliases_for.get(name, [])),
            )
    for attr in dir(shell):
        if not attr.startswith("do_"):
            continue
        name = attr[3:]
        if name in seen:
            continue
        seen[name] = CommandInfo(
            name=name,
            summary=_extract_doc(shell, name),
            aliases=tuple(aliases_for.get(name, [])),
        )
    return sorted(seen.values(), key=lambda c: c.name)


def _extract_doc(shell: Any, name: str) -> str:
    fn = getattr(shell, f"do_{name}", None)
    if fn is None:
        return ""
    doc = (fn.__doc__ or "").strip()
    return doc.splitlines()[0] if doc else ""


__all__ = [
    "AddonHotReloader",
    "AliasResolver",
    "CommandInfo",
    "CommandLister",
    "CompletionResult",
    "DictPayloadProvider",
    "DynamicAliasResolver",
    "FormField",
    "FormSpec",
    "FuzzyCommandIndex",
    "FuzzyMatch",
    "HotReloader",
    "InteractiveForm",
    "LiveStatusTail",
    "PayloadAwareCompleter",
    "PayloadProvider",
    "StaticCommandLister",
    "StatusUpdate",
    "TerminalIO",
    "TranscriptEntry",
    "TranscriptStore",
    "commands_from_cmd2_shell",
]
