"""Headless / non-interactive runner for automated pipelines.

Provides HeadlessRunner which wraps LazyOwnShell and produces
structured JSON output suitable for CI/CD and agent-driven ops.
"""

import io
import json
import sys
import time
import yaml
from typing import Any, Dict, List, Optional

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_CONFIG = 2
EXIT_SCOPE = 3
EXIT_TIMEOUT = 4

EXIT_LABELS = {
    EXIT_OK: "OK",
    EXIT_ERROR: "ERROR",
    EXIT_CONFIG: "CONFIG_ERROR",
    EXIT_SCOPE: "SCOPE_VIOLATION",
    EXIT_TIMEOUT: "TIMEOUT",
}


def load_profile(path: str) -> Dict[str, Any]:
    """Load a YAML profile that overrides payload.json keys.

    Args:
        path: filesystem path to the YAML profile.

    Returns:
        Dictionary of config overrides.

    Raises:
        FileNotFoundError: profile not found.
        yaml.YAMLError: malformed YAML.
    """
    with open(path) as f:
        return yaml.safe_load(f)


def apply_profile(config: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    """Merge profile values into config (shallow overlay).

    Args:
        config: base configuration dictionary (e.g. shell.params).
        profile: override dictionary from profile file.

    Returns:
        Updated config (same reference).
    """
    config.update(profile)
    return config


class HeadlessRunner:
    """Non-interactive runner that executes commands and emits structured output.

    Usage:
        shell = LazyOwnShell()
        runner = HeadlessRunner(shell, json_output=True)
        runner.run_command("nmap_scan")
        sys.exit(runner.exit_code)
    """

    def __init__(
        self,
        shell,
        json_output: bool = False,
        profile_path: Optional[str] = None,
    ):
        self.shell = shell
        self.json_output = json_output
        self.exit_code = EXIT_OK
        self.results: List[Dict[str, Any]] = []

        if profile_path:
            profile = load_profile(profile_path)
            apply_profile(shell.params, profile)

    def run_command(self, cmd: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Execute a single command, capture output, return structured result.

        Args:
            cmd: command string to execute via onecmd.
            timeout: optional timeout in seconds (not yet enforced).

        Returns:
            Dict with keys: command, success, output, error, duration_ms.
        """
        start = time.time()
        exit_label = EXIT_LABELS[EXIT_OK]
        result: Dict[str, Any] = {
            "command": cmd,
            "success": False,
            "output": "",
            "error": None,
            "duration_ms": 0,
            "exit_code": EXIT_OK,
            "exit_label": exit_label,
        }
        old_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            self.shell.onecmd(cmd)
            captured = sys.stdout.getvalue()
            result["output"] = captured
            result["success"] = True
        except Exception as exc:
            result["error"] = str(exc)
            result["success"] = False
            if self.exit_code == EXIT_OK:
                self.exit_code = EXIT_ERROR
        finally:
            sys.stdout = old_stdout

        result["duration_ms"] = int((time.time() - start) * 1000)
        result["exit_code"] = self.exit_code
        result["exit_label"] = EXIT_LABELS.get(self.exit_code, "UNKNOWN")

        if self.json_output:
            json.dump(result, sys.stdout)
            sys.stdout.write("\n")
            sys.stdout.flush()

        self.results.append(result)
        return result

    def run_chain(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Execute multiple commands and emit final summary.

        Args:
            commands: list of command strings to execute sequentially.

        Returns:
            List of result dicts, one per command.
        """
        for cmd in commands:
            self.run_command(cmd)

        if self.json_output:
            summary = {
                "_meta": "headless_chain_complete",
                "total": len(commands),
                "successful": sum(1 for r in self.results if r["success"]),
                "failed": sum(1 for r in self.results if not r["success"]),
                "exit_code": self.exit_code,
                "exit_label": EXIT_LABELS.get(self.exit_code, "UNKNOWN"),
            }
            json.dump(summary, sys.stdout)
            sys.stdout.write("\n")

        return self.results
