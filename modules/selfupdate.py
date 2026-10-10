"""Verified self-update with staged swap and rollback.

Ports the LAZY selfupdate contract. Releases verify by SHA-256,
pass a smoke check, stage beside the live binary, activate by rename,
and roll back when the new binary fails repeatedly.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class UpdateConfig:
    """Centralized constants for update behavior."""

    failure_threshold: int = 3
    smoke_args: tuple = ("-h",)
    smoke_timeout_sec: float = 30.0


CONFIG = UpdateConfig()


@dataclass
class ReleaseArtifact:
    """Candidate binary with integrity metadata."""

    data: bytes
    sha256: str
    version: str = ""


def sha256_hex(data: bytes) -> str:
    """Return the hex SHA-256 digest for bytes."""
    return hashlib.sha256(bytes(data or b"")).hexdigest()


class Updater:
    """Staged updater keeping the previous binary for rollback."""

    def __init__(self, live_path: str | Path,
                 config: UpdateConfig = CONFIG) -> None:
        """Bind the updater to one live binary path."""
        self._live = Path(live_path)
        self._config = config
        self._failures = 0

    @property
    def live_path(self) -> Path:
        """Return the managed live binary path."""
        return self._live

    def verify(self, artifact: ReleaseArtifact) -> bool:
        """Check artifact integrity against its declared hash."""
        return sha256_hex(artifact.data) == str(artifact.sha256 or "").lower()

    def smoke(self, candidate: Path) -> bool:
        """Run the candidate smoke command without shell."""
        try:
            completed = subprocess.run(
                [str(candidate), *self._config.smoke_args],
                capture_output=True, timeout=self._config.smoke_timeout_sec,
                check=False)
            return completed.returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False

    def stage(self, artifact: ReleaseArtifact, staging_dir: str | Path) -> Path:
        """Write a verified artifact to staging and return its path."""
        if not self.verify(artifact):
            raise ValueError("Artifact checksum mismatch.")
        target = Path(staging_dir) / f"{self._live.name}.new"
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=str(target.parent), prefix="stage-")
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(artifact.data)
            os.replace(tmp_name, target)
        finally:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
        target.chmod(0o755)
        return target

    def activate(self, staged: Path) -> Path:
        """Smoke then swap staged binary into live position."""
        if not self.smoke(staged):
            Path(staged).unlink(missing_ok=True)
            raise RuntimeError("Staged binary failed smoke test.")
        backup = self._live.with_name(f"{self._live.name}.old")
        if self._live.exists():
            shutil.copy2(self._live, backup)
        os.replace(staged, self._live)
        self._failures = 0
        return self._live

    def note_failure(self) -> bool:
        """Record a boot failure and roll back past the threshold."""
        self._failures += 1
        if self._failures < self._config.failure_threshold:
            return False
        return self.rollback()

    def rollback(self) -> bool:
        """Restore the previous binary when present."""
        backup = self._live.with_name(f"{self._live.name}.old")
        if not backup.exists():
            return False
        failed = self._live.with_name(f"{self._live.name}.failed")
        try:
            if self._live.exists():
                os.replace(self._live, failed)
            os.replace(backup, self._live)
            self._failures = 0
            return True
        except OSError:
            return False
