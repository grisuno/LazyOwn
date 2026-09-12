#!/usr/bin/env python3
"""Smoke check for the public surfaces documented in CORE.md.

I run this before a release and after a refactor that touches the consumer
API. It imports every public name, calls a small safe subset, and exits
non-zero on the first missing name. It never mutates the campaign state: the
database runs in a temporary directory and the kill-chain read is read-only.
"""

from __future__ import annotations

import importlib
import os
import sys
import tempfile
from dataclasses import dataclass, field


@dataclass
class SmokeConfig:
    """Configuration for the smoke check.

    Attributes:
        surfaces: Mapping of module name to the public attributes it must
            expose.
    """

    surfaces: dict[str, tuple[str, ...]] = field(
        default_factory=lambda: {
            "utils": ("Config", "load_payload"),
            "core.config": ("load_payload", "save_payload", "Config", "resolve_aes_key"),
            "core.protocols": ("Selector", "LLMBackend", "MemoryStore", "BridgeCatalog", "OutcomeEvaluator"),
            "modules.llm_factory": (
                "get_llm_backend",
                "get_llm_backend_raw",
                "try_get_llm_backend",
                "LLMBackendUnavailableError",
                "LLMBackendNotSupportedError",
                "SUPPORTED_BACKENDS",
            ),
            "modules.db": ("LazyOwnDB", "get_db"),
            "modules.module_registry": (
                "ModuleRegistry",
                "ModuleInfo",
                "format_module_table",
                "format_module_detail",
            ),
            "modules.payload_factory": ("PayloadFactory", "PayloadTemplate", "format_payload_table"),
            "modules.killchain": ("KillChain", "KillChainConfig"),
            "modules.world_model": ("WorldModel", "HostState", "read_state_dict", "write_state_dict"),
            "core.hardening": (
                "safe_path_join",
                "validate_host",
                "validate_network_cidr",
                "validate_port_spec",
                "defused_xml_parse",
            ),
            "core.safe_exec": ("safe_run_argv", "validate_url"),
            "core.payload_schema": ("validate_payload", "validate_value", "coerce_value", "SCHEMA"),
        }
    )


def check_surfaces(config: SmokeConfig) -> list[str]:
    """Return the dotted names that are missing from the imported modules.

    Args:
        config: Active smoke configuration.
    Returns:
        A list of missing ``module.attribute`` names. Empty means all present.
    """
    missing: list[str] = []
    for module_name, attributes in config.surfaces.items():
        module = importlib.import_module(module_name)
        for attribute in attributes:
            if not hasattr(module, attribute):
                missing.append(f"{module_name}.{attribute}")
    return missing


def check_calls() -> list[str]:
    """Exercise a small safe subset of the public API.

    Returns:
        A list of failures. Empty means every call succeeded.
    """
    from core.hardening import safe_path_join, validate_port_spec
    from core.payload_schema import coerce_value
    from modules.db import get_db
    from modules.killchain import KillChain
    from modules.payload_factory import PayloadFactory

    failures: list[str] = []
    raw = PayloadFactory().generate("cmd/unix/reverse_shell", lhost="10.10.14.20", lport=4444)
    if not isinstance(raw, bytes) or not raw:
        failures.append("payload_factory.generate returned no bytes")

    if coerce_value("rport", "5555") != 5555:
        failures.append("payload_schema.coerce_value did not cast the port")
    if not validate_port_spec("80,443,1-1024"):
        failures.append("hardening.validate_port_spec rejected a valid spec")
    if not safe_path_join("/tmp", "notes.txt").endswith("notes.txt"):
        failures.append("hardening.safe_path_join lost the file name")
    if not KillChain.snapshot():
        failures.append("killchain.snapshot returned an empty payload")

    with tempfile.TemporaryDirectory() as directory:
        database = get_db(os.path.join(directory, "smoke.sqlite"))
        workspace = database.workspace_create("smoke")
        host_id = database.host_add(workspace, "10.10.11.5", hostname="target")
        database.service_add(host_id, port=22, name="ssh", version="OpenSSH 8.2")
        if not database.status(workspace):
            failures.append("db.status returned nothing")
        database.close()
    return failures


def main() -> int:
    """Run the smoke check and return the process exit code."""
    failures = check_surfaces(SmokeConfig()) + check_calls()
    if failures:
        for failure in failures:
            print(f"[core-smoke] {failure}")
        return 1
    print("core smoke check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
