"""
Central constants for the Hermes-LazyOwn integration layer.

All paths, timeouts, and thresholds are derived from environment variables
or payload.json. No hardcoded hostnames, ports, or filesystem paths.
"""

import os
from pathlib import Path


class ConfigKeys:
    """Payload.json keys referenced across the integration layer."""

    RHOST = "rhost"
    LHOST = "lhost"
    RPORT = "rport"
    LPORT = "lport"
    DOMAIN = "domain"
    C2_PORT = "c2_port"
    C2_USER = "c2_user"
    C2_PASS = "c2_pass"
    API_KEY = "api_key"
    WORDLIST = "wordlist"
    DIRWORDLIST = "dirwordlist"
    START_USER = "start_user"
    START_PASS = "start_pass"
    OS_ID = "os_id"
    PROXY_PORT = "proxy_port"
    REVERSE_SHELL_PORT = "reverse_shell_port"
    LISTENER = "listener"
    SLEEP = "sleep"


class EnvKeys:
    """Environment variables used for Hermes integration."""

    LAZYOWN_DIR = "LAZYOWN_DIR"
    HERMES_SESSION_ID = "HERMES_SESSION_ID"
    HERMES_SKILL_DIR = "HERMES_SKILL_DIR"
    LAZYOWN_C2_HOST = "LAZYOWN_C2_HOST"
    LAZYOWN_C2_PORT = "LAZYOWN_C2_PORT"


class Defaults:
    """Fallback defaults when neither payload.json nor env vars provide a value."""

    TIMEOUT_SECONDS = 30
    ASYNC_TIMEOUT_SECONDS = 1800
    MAX_OUTPUT_LINES = 2000
    MAX_OUTPUT_BYTES = 50000
    COMPACT_THRESHOLD_LINES = 100
    FRESHNESS_THRESHOLD_SECONDS = 604800
    DAEMON_POLL_INTERVAL_SECONDS = 5
    MAX_TOOL_BATCH_SIZE = 5
    CHECKPOINT_VERSION = "1"


class PhaseNames:
    """Kill-chain phase identifiers."""

    RECON = "recon"
    ENUM = "enum"
    EXPLOIT = "exploit"
    POSTEXP = "postexp"
    PERSIST = "persist"
    PRIVESC = "privesc"
    CRED = "cred"
    LATERAL = "lateral"
    EXFIL = "exfil"
    C2 = "c2"
    REPORT = "report"

    ALL = [
        RECON, ENUM, EXPLOIT, POSTEXP, PERSIST,
        PRIVESC, CRED, LATERAL, EXFIL, C2, REPORT,
    ]


class Paths:
    """LazyOwn directory layout derived at runtime."""

    @staticmethod
    def lazyown_dir() -> Path:
        """Return the LazyOwn project root directory."""
        env_dir = os.environ.get(EnvKeys.LAZYOWN_DIR)
        if env_dir:
            return Path(env_dir)
        # Fallback: parent of skills/hermes-lazyown
        return Path(__file__).parent.parent.parent

    @staticmethod
    def payload_file() -> Path:
        """Return the path to payload.json."""
        return Paths.lazyown_dir() / "payload.json"

    @staticmethod
    def sessions_dir() -> Path:
        """Return the path to the sessions directory."""
        return Paths.lazyown_dir() / "sessions"

    @staticmethod
    def scan_file(rhost: str) -> Path:
        """Return the expected nmap scan file for a target."""
        return Paths.sessions_dir() / f"scan_{rhost}.nmap"

    @staticmethod
    def vulns_file(rhost: str) -> Path:
        """Return the expected vulnerability scan file for a target."""
        return Paths.sessions_dir() / f"vulns_{rhost}.nmap"

    @staticmethod
    def world_model_file() -> Path:
        """Return the path to world_model.json."""
        return Paths.sessions_dir() / "world_model.json"

    @staticmethod
    def objectives_file() -> Path:
        """Return the path to objectives.jsonl."""
        return Paths.sessions_dir() / "objectives.jsonl"

    @staticmethod
    def tasks_file() -> Path:
        """Return the path to tasks.json."""
        return Paths.sessions_dir() / "tasks.json"

    @staticmethod
    def soul_file() -> Path:
        """Return the path to soul.md."""
        return Paths.lazyown_dir() / "soul.md"

    @staticmethod
    def claude_md_file() -> Path:
        """Return the path to CLAUDE.md."""
        return Paths.lazyown_dir() / "CLAUDE.md"
