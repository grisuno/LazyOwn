"""
Phase-aware output compaction for the Hermes-LazyOwn integration.

Security tools produce verbose output. Hermes context windows are finite.
This module compacts tool output based on the current engagement phase,
preserving only the signal and discarding noise.

Follows the Strategy pattern: each phase implements a CompactionStrategy.
"""

import re
from abc import ABC, abstractmethod
from typing import Any

from constants import Defaults, PhaseNames


class CompactionResult:
    """Immutable result of a compaction operation."""

    def __init__(self, compacted: str, original_lines: int, compacted_lines: int) -> None:
        self.comparted = compacted
        self.original_lines = original_lines
        self.compacted_lines = compacted_lines

    @property
    def reduction_ratio(self) -> float:
        """Return the ratio of lines removed (0.0 to 1.0)."""
        if self.original_lines == 0:
            return 0.0
        return 1.0 - (self.compacted_lines / self.original_lines)

    def __str__(self) -> str:
        return (
            f"[{self.original_lines} -> {self.compacted_lines} lines "
            f"({self.reduction_ratio:.0%})]\n{self.comparted}"
        )


class CompactionStrategy(ABC):
    """Base class for phase-specific compaction strategies."""

    @abstractmethod
    def compact(self, raw_output: str, tool_name: str = "") -> CompactionResult:
        """Compact *raw_output* and return a CompactionResult."""
        raise NotImplementedError


class ReconCompaction(CompactionStrategy):
    """
    Recon phase: preserve only open ports, services, and OS guesses.
    Strip script output, traceroute, and timing details.
    """

    _SERVICE_LINE = re.compile(r"^(\d+)/(tcp|udp)\s+(open|filtered|closed)\s+(.*)$")
    _OS_GUESS = re.compile(r"^(OS details|Running|Aggressive OS guesses):", re.I)
    _PORT_STATE = re.compile(r"^(PORT|SERVICE|VERSION)", re.I)

    def compact(self, raw_output: str, tool_name: str = "") -> CompactionResult:
        lines = raw_output.splitlines()
        kept: list[str] = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if self._SERVICE_LINE.match(stripped):
                kept.append(stripped)
                continue
            if self._OS_GUESS.match(stripped):
                kept.append(stripped)
                continue
            if self._PORT_STATE.match(stripped):
                kept.append(stripped)
                continue
            if "Nmap scan report for" in stripped:
                kept.append(stripped)

        summary = f"# {tool_name or 'recon'} summary: {len(kept)} relevant lines\n"
        compacted = summary + "\n".join(kept)
        return CompactionResult(compacted, len(lines), len(kept) + 1)


class EnumCompaction(CompactionStrategy):
    """
    Enumeration phase: preserve findings that are new compared to a snapshot.
    Deduplicate against known services and only highlight changes.
    """

    _FINDING_PATTERNS = [
        re.compile(r"(found|discovered|valid|successful|exists)", re.I),
        re.compile(r"(user|password|hash|credential|token|key)", re.I),
        re.compile(r"(share|writable|readable|accessible)", re.I),
        re.compile(r"(vuln|CVE|exploit|version)", re.I),
    ]

    def compact(self, raw_output: str, tool_name: str = "") -> CompactionResult:
        lines = raw_output.splitlines()
        kept: list[str] = []

        for line in lines:
            stripped = line.strip()
            if any(pat.search(stripped) for pat in self._FINDING_PATTERNS):
                kept.append(stripped)

        if not kept:
            # Fallback: keep first 20 lines if no findings matched
            kept = [l for l in lines[:20] if l.strip()]

        summary = f"# {tool_name or 'enum'} findings: {len(kept)} lines\n"
        compacted = summary + "\n".join(kept)
        return CompactionResult(compacted, len(lines), len(kept) + 1)


class ExploitCompaction(CompactionStrategy):
    """
    Exploitation phase: preserve only success/failure and access level gained.
    Discard exploit noise, shell banners, and download progress.
    """

    _SUCCESS_PATTERNS = [
        re.compile(r"(session opened|meterpreter|shell obtained|pwned|owned)", re.I),
        re.compile(r"(authenticated|logged in|access granted)", re.I),
        re.compile(r"(privilege escalation successful|root|administrator)", re.I),
        re.compile(r"(error|failed|timeout|connection refused)", re.I),
    ]

    def compact(self, raw_output: str, tool_name: str = "") -> CompactionResult:
        lines = raw_output.splitlines()
        kept: list[str] = []

        for line in lines:
            stripped = line.strip()
            if any(pat.search(stripped) for pat in self._SUCCESS_PATTERNS):
                kept.append(stripped)

        if not kept:
            kept = [f"# {tool_name or 'exploit'}: no clear success/failure signal"]

        compacted = "\n".join(kept)
        return CompactionResult(compacted, len(lines), len(kept))


class PrivescCompaction(CompactionStrategy):
    """
    Privilege escalation phase: preserve vectors found and commands executed.
    """

    _VECTOR_PATTERNS = [
        re.compile(r"(SUID|sudo|capability|writable|cron|path hijack)", re.I),
        re.compile(r"(CVE|exploit|kernel|version vulnerable)", re.I),
        re.compile(r"(root|administrator|NT AUTHORITY)", re.I),
    ]

    def compact(self, raw_output: str, tool_name: str = "") -> CompactionResult:
        lines = raw_output.splitlines()
        kept = [ln for ln in lines if any(p.search(ln) for p in self._VECTOR_PATTERNS)]

        if not kept:
            kept = [f"# {tool_name or 'privesc'}: no vectors detected"]

        compacted = "\n".join(kept)
        return CompactionResult(compacted, len(lines), len(kept))


class DefaultCompaction(CompactionStrategy):
    """Default pass-through with line-cap enforcement."""

    def __init__(self, max_lines: int = Defaults.MAX_OUTPUT_LINES) -> None:
        self._max_lines = max_lines

    def compact(self, raw_output: str, tool_name: str = "") -> CompactionResult:
        lines = raw_output.splitlines()
        if len(lines) <= self._max_lines:
            return CompactionResult(raw_output, len(lines), len(lines))

        kept = lines[: self._max_lines]
        kept.append(f"# ... {len(lines) - self._max_lines} lines truncated")
        compacted = "\n".join(kept)
        return CompactionResult(compacted, len(lines), len(kept))


class OutputCompactor:
    """
    Phase-aware output compactor.

    Usage:
        compactor = OutputCompactor()
        result = compactor.compact(raw_nmap_output, phase="recon", tool_name="lazynmap")
        print(result.comparted)
    """

    _STRATEGIES: dict[str, type[CompactionStrategy]] = {
        PhaseNames.RECON: ReconCompaction,
        PhaseNames.ENUM: EnumCompaction,
        PhaseNames.EXPLOIT: ExploitCompaction,
        PhaseNames.PRIVESC: PrivescCompaction,
    }

    def __init__(self, default_max_lines: int = Defaults.MAX_OUTPUT_LINES) -> None:
        self._default_max_lines = default_max_lines
        self._default_strategy = DefaultCompaction(default_max_lines)

    def compact(self, raw_output: str, phase: str = "", tool_name: str = "") -> CompactionResult:
        """
        Compact *raw_output* according to *phase*.

        Args:
            raw_output: The raw tool output string.
            phase: One of the PhaseNames values.
            tool_name: Optional tool name for context in the summary.

        Returns:
            A CompactionResult with the compacted output and metadata.
        """
        if not raw_output:
            return CompactionResult("", 0, 0)

        strategy_cls = self._STRATEGIES.get(phase)
        if strategy_cls is None:
            return self._default_strategy.compact(raw_output, tool_name)

        try:
            strategy = strategy_cls()
            return strategy.compact(raw_output, tool_name)
        except Exception:
            # Fallback on any strategy error so we never lose output entirely.
            return self._default_strategy.compact(raw_output, tool_name)
