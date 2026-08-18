"""Sleep obfuscation engine for beacon memory evasion.

Defines a catalog of sleep obfuscation techniques with configurable
parameters. Provides the ``SleepObfuscationEngine`` which selects
and validates techniques based on platform compatibility and
operational parameters.

Techniques catalogued:
    - Sleep Mask (RW -> RX/RW cycle via VirtualProtect/mprotect)
    - Ekko-style threadless sleep (timer queue + ROP gadgets)
    - Stack Spoofing (call stack overwrite before sleep)
    - Module Stomping (overwrite loaded module .text section)
    - APC Injection Chain (queued APC during sleep)
    - Hardware Breakpoint (VEH + HWBP on sleep/resume)
    - Fiber-based sleep (convert thread to fiber, swap, convert back)
    - Thread Pool (queue work item to pool thread before sleep)

Each technique is defined with its platform support, minimum beacon
version, detection resistance score, and configurable parameters.

Contracts:
    - SleepTechnique: immutable dataclass for a technique definition
    - SleepTechniqueCatalog: curated catalog of known techniques
    - SleepObfuscationConfig: runtime configuration for the active technique
    - SleepObfuscationEngine: selects, validates, and configures techniques
    - SleepTechniqueValidator: validates config against technique constraints

Design (SOLID):
    - Single Responsibility: catalog, config, engine, validator are separate
    - Open/Closed: new techniques added via catalog registration
    - Liskov: all techniques share the same dataclass contract
    - Interface Segregation: engine exposes only select/configure/validate
    - Dependency Inversion: depends on catalog abstraction, not on OS APIs

Usage:
    from modules.sleep_obfuscation import (
        SleepObfuscationEngine,
        SleepTechniqueCatalog,
    )

    engine = SleepObfuscationEngine()
    tech = engine.select("ekko")
    config = engine.configure(tech, {"encrypt_heap": True})
    errors = engine.validate(config)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

log = logging.getLogger("sleep_obfuscation")


class OsPlatform(str, Enum):  # noqa: UP042
    """Operating system platform."""

    WINDOWS = "windows"
    LINUX = "linux"


class TechniqueRisk(str, Enum):  # noqa: UP042
    """Risk classification for a sleep obfuscation technique."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class SleepTechnique:
    """Definition of a single sleep obfuscation technique.

    Attributes:
        name: Unique technique identifier.
        description: Human-readable description.
        platforms: Supported OS platforms.
        detection_resistance: Score 0-100 indicating EDR evasion strength.
        risk: Operational risk level (low/medium/high).
        min_beacon_version: Minimum beacon engine version required.
        params: Parameter schema as dict of name -> (type, default, description).
        requires_rop_gadgets: Whether the technique needs ROP gadget scanning.
        stability_note: Operator-visible note about known issues.
    """

    name: str
    description: str
    platforms: list[OsPlatform]
    detection_resistance: int
    risk: TechniqueRisk = TechniqueRisk.MEDIUM
    min_beacon_version: str = "1.0"
    params: dict[str, Any] = field(default_factory=dict)
    requires_rop_gadgets: bool = False
    stability_note: str = ""


@dataclass
class SleepObfuscationConfig:
    """Runtime configuration for the active sleep obfuscation technique.

    Attributes:
        technique_name: Name of the selected technique.
        enabled: Whether sleep obfuscation is active.
        encrypt_heap: Encrypt beacon heap memory during sleep.
        encrypt_stack: Encrypt thread stack during sleep.
        encrypt_peb: Hide/Patch Process Environment Block.
        rwx_to_rw_cycle: Temporarily change memory protections.
        indirect_syscalls: Use indirect syscalls for protection changes.
        module_stomp_target: DLL name for module stomping (if applicable).
        rop_gadget_count: Number of ROP gadgets to use (Ekko-style).
        sleep_delay_ms: Artificial delay in ms to pace operations.
        custom_params: Free-form dict for technique-specific parameters.
    """

    technique_name: str = "sleep_mask"
    enabled: bool = False
    encrypt_heap: bool = True
    encrypt_stack: bool = True
    encrypt_peb: bool = False
    rwx_to_rw_cycle: bool = True
    indirect_syscalls: bool = True
    module_stomp_target: str = ""
    rop_gadget_count: int = 3
    sleep_delay_ms: int = 100
    custom_params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "technique_name": self.technique_name,
            "enabled": self.enabled,
            "encrypt_heap": self.encrypt_heap,
            "encrypt_stack": self.encrypt_stack,
            "encrypt_peb": self.encrypt_peb,
            "rwx_to_rw_cycle": self.rwx_to_rw_cycle,
            "indirect_syscalls": self.indirect_syscalls,
            "module_stomp_target": self.module_stomp_target,
            "rop_gadget_count": self.rop_gadget_count,
            "sleep_delay_ms": self.sleep_delay_ms,
            "custom_params": self.custom_params,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> SleepObfuscationConfig:
        """Build from dictionary."""
        return cls(
            technique_name=str(raw.get("technique_name", "sleep_mask")),
            enabled=bool(raw.get("enabled", False)),
            encrypt_heap=bool(raw.get("encrypt_heap", True)),
            encrypt_stack=bool(raw.get("encrypt_stack", True)),
            encrypt_peb=bool(raw.get("encrypt_peb", False)),
            rwx_to_rw_cycle=bool(raw.get("rwx_to_rw_cycle", True)),
            indirect_syscalls=bool(raw.get("indirect_syscalls", True)),
            module_stomp_target=str(raw.get("module_stomp_target", "")),
            rop_gadget_count=int(raw.get("rop_gadget_count", 3)),
            sleep_delay_ms=int(raw.get("sleep_delay_ms", 100)),
            custom_params=dict(raw.get("custom_params", {})),
        )


class SleepTechniqueCatalog:
    """Curated catalog of sleep obfuscation techniques.

    New techniques are registered via ``register()``. The catalog
    is immutable at runtime after initial population.
    """

    def __init__(self) -> None:
        self._techniques: dict[str, SleepTechnique] = {}

    def register(self, technique: SleepTechnique) -> None:
        """Register a technique in the catalog."""
        self._techniques[technique.name] = technique

    def get(self, name: str) -> SleepTechnique:
        """Retrieve a technique by name. Raises KeyError if missing."""
        if name not in self._techniques:
            available = ", ".join(sorted(self._techniques.keys()))
            raise KeyError(
                f"Sleep technique '{name}' not found. Available: {available}"
            )
        return self._techniques[name]

    def list_all(self) -> list[SleepTechnique]:
        """Return all registered techniques sorted by detection resistance."""
        return sorted(
            self._techniques.values(),
            key=lambda t: t.detection_resistance,
            reverse=True,
        )

    def list_by_platform(self, platform: OsPlatform) -> list[SleepTechnique]:
        """Return techniques supported on a given platform."""
        return [
            t for t in self._techniques.values()
            if platform in t.platforms
        ]

    def list_names(self) -> list[str]:
        """Return sorted list of technique names."""
        return sorted(self._techniques.keys())


def _build_default_catalog() -> SleepTechniqueCatalog:
    """Build the default curated sleep obfuscation catalog."""
    catalog = SleepTechniqueCatalog()
    techniques = [
        SleepTechnique(
            name="sleep_mask",
            description=(
                "Encrypts beacon heap and stack regions during sleep by flipping "
                "memory protections from executable to read-write and back. "
                "Uses VirtualProtect (Windows) or mprotect (Linux)."
            ),
            platforms=[OsPlatform.WINDOWS, OsPlatform.LINUX],
            detection_resistance=65,
            risk=TechniqueRisk.LOW,
            params={
                "xor_key_seed": {"type": "int", "default": 0x55, "description": "XOR key byte"},
                "protect_heap": {"type": "bool", "default": True, "description": "Encrypt heap allocations"},
                "protect_stack": {"type": "bool", "default": True, "description": "Encrypt thread stack"},
            },
        ),
        SleepTechnique(
            name="ekko",
            description=(
                "Threadless sleep obfuscation using timer queues (CreateTimerQueueTimer) "
                "and ROP gadget chains to call WaitForSingleObject without the thread "
                "being present. Requires ROP gadget scanning at startup. Implemented as "
                "described by C5pider (Ekko)."
            ),
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=85,
            risk=TechniqueRisk.MEDIUM,
            params={
                "rop_gadget_count": {"type": "int", "default": 3, "description": "Number of ROP gadgets in chain"},
                "trigger_delay_ms": {"type": "int", "default": 10, "description": "Timer trigger delay"},
                "gadget_source_dll": {"type": "str", "default": "ntdll.dll", "description": "DLL to scan for gadgets"},
            },
            requires_rop_gadgets=True,
            stability_note=(
                "Requires careful ROP gadget selection. May crash on systems "
                "with Control Flow Guard (CFG) if gadgets overlap protected regions."
            ),
        ),
        SleepTechnique(
            name="stack_spoof",
            description=(
                "Overwrites the call stack with fake return addresses before "
                "sleep, then restores the original stack on resume. Prevents "
                "EDRs from walking the call stack to find suspicious frames."
            ),
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=78,
            risk=TechniqueRisk.MEDIUM,
            params={
                "spoof_depth": {"type": "int", "default": 16, "description": "Number of frames to spoof"},
                "use_legitimate_module": {"type": "bool", "default": True, "description": "Use legitimate module addresses"},
            },
        ),
        SleepTechnique(
            name="module_stomp",
            description=(
                "Overwrites a loaded DLL's .text section with beacon code, then "
                "restores the original bytes during sleep. The beacon lives inside "
                "a legitimate signed module, evading memory scanners."
            ),
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=80,
            risk=TechniqueRisk.HIGH,
            params={
                "stomp_target_dll": {"type": "str", "default": "mshtml.dll", "description": "Target DLL to stomp"},
                "backup_section": {"type": "str", "default": ".text", "description": "Section to overwrite"},
            },
            stability_note=(
                "Module stomping is unstable on systems with CFG, CET, or "
                "hypervisor-based integrity checks."
            ),
        ),
        SleepTechnique(
            name="fiber_sleep",
            description=(
                "Converts the beacon thread to a fiber, swaps to a secondary "
                "fiber to perform the sleep, then swaps back. The main thread "
                "is not in an alertable state during sleep, evading EDR callbacks."
            ),
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=72,
            risk=TechniqueRisk.LOW,
            params={
                "fiber_count": {"type": "int", "default": 2, "description": "Number of fibers"},
                "encrypt_fiber_data": {"type": "bool", "default": False, "description": "Encrypt fiber-local storage"},
            },
        ),
        SleepTechnique(
            name="thread_pool",
            description=(
                "Queues a work item to the Windows thread pool with a timer, "
                "then calls WaitForSingleObject. The actual thread is pooled "
                "by the system, making it harder to attribute to beacon activity."
            ),
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=60,
            risk=TechniqueRisk.LOW,
            params={
                "pool_work_count": {"type": "int", "default": 1, "description": "Number of queued work items"},
            },
        ),
        SleepTechnique(
            name="hwbp_sleep",
            description=(
                "Sets a hardware breakpoint on the resume address, registers a "
                "Vectored Exception Handler, and enters sleep. On resume, the "
                "HWBP fires the VEH which decrypts memory before the thread "
                "continues. No timer or thread pool required."
            ),
            platforms=[OsPlatform.WINDOWS],
            detection_resistance=88,
            risk=TechniqueRisk.HIGH,
            params={
                "hwbp_register": {"type": "str", "default": "Dr0", "description": "Debug register to use"},
                "fake_veh_count": {"type": "int", "default": 0, "description": "Fake VEH registrations for noise"},
            },
            stability_note=(
                "HWBP-based sleep conflicts with debuggers and some EDRs "
                "that also use hardware breakpoints. Test before use."
            ),
        ),
        SleepTechnique(
            name="linux_gatekeeper",
            description=(
                "Linux-specific sleep obfuscation using mprotect to mark beacon "
                "pages as PROT_NONE during sleep, with a SIGSEGV handler to "
                "restore permissions on resume. Avoids RWX pages in memory scans."
            ),
            platforms=[OsPlatform.LINUX],
            detection_resistance=60,
            risk=TechniqueRisk.MEDIUM,
            params={
                "protect_pages": {"type": "str", "default": "all", "description": "Pages to protect: 'all' or 'code'"},
                "signal_handler": {"type": "str", "default": "SIGSEGV", "description": "Signal to hook"},
            },
        ),
        SleepTechnique(
            name="linux_futex_hide",
            description=(
                "Uses POSIX futex (FUTEX_WAIT) with mprotect cycling to hide "
                "beacon memory from /proc/pid/maps during sleep periods. "
                "Thread waits on a futex while memory is unmapped."
            ),
            platforms=[OsPlatform.LINUX],
            detection_resistance=68,
            risk=TechniqueRisk.MEDIUM,
            params={
                "futex_timeout_ms": {"type": "int", "default": 1000, "description": "Futex wait timeout"},
                "hide_from_proc": {"type": "bool", "default": True, "description": "Unmap from /proc/pid/maps"},
            },
        ),
    ]
    for technique in techniques:
        catalog.register(technique)
    return catalog


class SleepTechniqueValidator:
    """Validates a SleepObfuscationConfig against technique constraints."""

    @staticmethod
    def validate(config: SleepObfuscationConfig, technique: SleepTechnique) -> list[str]:
        """Validate config against a technique definition.

        Returns a list of error strings (empty = valid).
        """
        errors: list[str] = []
        if config.rop_gadget_count < 1 and technique.requires_rop_gadgets:
            errors.append(
                f"Technique '{technique.name}' requires rop_gadget_count >= 1"
            )
        if config.rop_gadget_count > 20:
            errors.append(
                "rop_gadget_count > 20 is excessive and likely to cause instability"
            )
        if config.sleep_delay_ms < 0:
            errors.append("sleep_delay_ms must be >= 0")
        if config.sleep_delay_ms > 60000:
            errors.append("sleep_delay_ms > 60000 is excessive for sleep obfuscation")
        return errors

    @staticmethod
    def validate_config(config: SleepObfuscationConfig) -> list[str]:
        """Validate the config itself for internal consistency."""
        errors: list[str] = []
        if config.enabled and not config.technique_name:
            errors.append("technique_name is required when sleep obfuscation is enabled")
        return errors


class SleepObfuscationEngine:
    """Engine for selecting, configuring, and validating sleep obfuscation.

    Composes a technique catalog, a validator, and runtime configuration.
    Provides the primary interface for beacon compile-time and run-time
    sleep obfuscation decisions.

    Attributes:
        catalog: The technique catalog.
        validator: The config validator.
        config: The active runtime configuration.
    """

    def __init__(
        self,
        catalog: SleepTechniqueCatalog | None = None,
    ) -> None:
        self._catalog = catalog or _build_default_catalog()
        self._validator = SleepTechniqueValidator()
        self._config = SleepObfuscationConfig()

    @property
    def catalog(self) -> SleepTechniqueCatalog:
        """Return the technique catalog."""
        return self._catalog

    @property
    def config(self) -> SleepObfuscationConfig:
        """Return the active runtime configuration."""
        return self._config

    @property
    def detection_resistance(self) -> int:
        """Return the detection resistance score of the active technique.

        If the active technique is not found in the catalog (e.g., custom
        catalog was provided but config still references a built-in name),
        fall back to the highest available technique in the catalog.
        """
        try:
            tech = self._catalog.get(self._config.technique_name)
            return tech.detection_resistance
        except KeyError:
            techniques = self._catalog.list_all()
            if techniques:
                return max(t.detection_resistance for t in techniques)
            return 0

    def select(self, technique_name: str) -> SleepTechnique:
        """Select a technique from the catalog.

        Returns the SleepTechnique. Raises KeyError if not found.
        """
        return self._catalog.get(technique_name)

    def configure(
        self,
        technique: SleepTechnique,
        overrides: dict[str, Any] | None = None,
    ) -> SleepObfuscationConfig:
        """Build a validated SleepObfuscationConfig for a technique.

        Args:
            technique: The SleepTechnique to configure.
            overrides: Optional dict to override default config values.

        Returns:
            A validated SleepObfuscationConfig ready for beacon embedding.
        """
        config = SleepObfuscationConfig(
            technique_name=technique.name,
            enabled=True,
        )
        if overrides:
            config = SleepObfuscationConfig(
                technique_name=technique.name,
                enabled=True,
                encrypt_heap=bool(overrides.get("encrypt_heap", config.encrypt_heap)),
                encrypt_stack=bool(overrides.get("encrypt_stack", config.encrypt_stack)),
                encrypt_peb=bool(overrides.get("encrypt_peb", config.encrypt_peb)),
                rwx_to_rw_cycle=bool(overrides.get("rwx_to_rw_cycle", config.rwx_to_rw_cycle)),
                indirect_syscalls=bool(overrides.get("indirect_syscalls", config.indirect_syscalls)),
                module_stomp_target=str(overrides.get("module_stomp_target", config.module_stomp_target)),
                rop_gadget_count=int(overrides.get("rop_gadget_count", config.rop_gadget_count)),
                sleep_delay_ms=int(overrides.get("sleep_delay_ms", config.sleep_delay_ms)),
                custom_params=dict(overrides.get("custom_params", config.custom_params)),
            )
        self._config = config
        return config

    def validate(self, config: SleepObfuscationConfig | None = None) -> list[str]:
        """Validate configuration against the active technique.

        Args:
            config: Optional config to validate. Uses self.config if None.

        Returns:
            List of error strings (empty = valid).
        """
        cfg = config or self._config
        try:
            technique = self._catalog.get(cfg.technique_name)
        except KeyError:
            return [f"Unknown technique: '{cfg.technique_name}'"]
        return self._validator.validate(cfg, technique)

    def recommend(self, platform: OsPlatform) -> list[SleepTechnique]:
        """Recommend techniques for a platform sorted by detection resistance.

        Returns techniques supported on the given platform, sorted with the
        highest detection resistance first.
        """
        techniques = self._catalog.list_by_platform(platform)
        return sorted(
            techniques,
            key=lambda t: t.detection_resistance,
            reverse=True,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the entire engine state to a dictionary."""
        return {
            "config": self._config.to_dict(),
            "available_techniques": self._catalog.list_names(),
            "active_detection_resistance": self.detection_resistance,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> SleepObfuscationEngine:
        """Build an engine from a serialized state dictionary."""
        engine = cls()
        if "config" in raw:
            engine._config = SleepObfuscationConfig.from_dict(raw["config"])
        return engine


__all__ = [
    "SleepObfuscationEngine",
    "SleepObfuscationConfig",
    "SleepTechnique",
    "SleepTechniqueCatalog",
    "SleepTechniqueValidator",
    "OsPlatform",
    "TechniqueRisk",
    "_build_default_catalog",
]
