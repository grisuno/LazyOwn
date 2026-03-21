"""
modules/session_reader.py
==========================
Reads LazyOwn C2 session artefacts:
  - sessions/{client_id}.log  (implant CSV: os, pid, hostname, ips, user,
                                discovered_ips, result_portscan, result_pwd,
                                command, output)
  - sessions/logs/c2/         (per-command output text files)
  - sessions/implant_config_*.json
  - sessions/hostsdiscovery.txt
  - sessions/tasks.json       (campaign task board)

Design (SOLID)
--------------
- Single Responsibility : each Reader reads exactly one artefact type.
- Open/Closed           : new artefact types via new Reader subclass.
- Liskov                : all Reader subclasses honour the read() contract.
- Interface Segregation : SessionAggregator exposes only what callers need.
- Dependency Inversion  : SessionAggregator depends on AbstractReader.
"""
from __future__ import annotations

import csv
import glob
import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

@dataclass
class ImplantRecord:
    """One row from sessions/{client_id}.log."""
    client_id: str
    os: str
    pid: str
    hostname: str
    ips: str
    user: str
    discovered_ips: str
    result_portscan: str
    result_pwd: str
    command: str
    output: str

    @property
    def is_privileged(self) -> bool:
        u = self.user.lower()
        return "root" in u or "nt authority\\system" in u or "administrator" in u

    @property
    def platform(self) -> str:
        o = self.os.lower()
        if "windows" in o:
            return "windows"
        if "linux" in o or "unix" in o:
            return "linux"
        return "unknown"

    @property
    def ip_list(self) -> List[str]:
        return [ip.strip() for ip in self.ips.split(",") if ip.strip()]


@dataclass
class CampaignTask:
    """One task from sessions/tasks.json."""
    id: int
    title: str
    description: str
    operator: str
    status: str  # New|Refined|Started|Review|Qa|Done|Blocked


@dataclass
class SessionSummary:
    """Aggregated view of all active sessions."""
    implants: List[ImplantRecord] = field(default_factory=list)
    tasks: List[CampaignTask] = field(default_factory=list)
    discovered_hosts: List[str] = field(default_factory=list)
    command_outputs: Dict[str, str] = field(default_factory=dict)

    @property
    def active_client_ids(self) -> List[str]:
        seen: Dict[str, ImplantRecord] = {}
        for r in self.implants:
            seen[r.client_id] = r
        return list(seen.keys())

    @property
    def privileged_sessions(self) -> List[ImplantRecord]:
        seen: Dict[str, ImplantRecord] = {}
        for r in self.implants:
            seen[r.client_id] = r
        return [r for r in seen.values() if r.is_privileged]

    @property
    def unprivileged_sessions(self) -> List[ImplantRecord]:
        seen: Dict[str, ImplantRecord] = {}
        for r in self.implants:
            seen[r.client_id] = r
        return [r for r in seen.values() if not r.is_privileged]

    def latest_for(self, client_id: str) -> Optional[ImplantRecord]:
        matches = [r for r in self.implants if r.client_id == client_id]
        return matches[-1] if matches else None

    def task_by_status(self, status: str) -> List[CampaignTask]:
        return [t for t in self.tasks if t.status.lower() == status.lower()]


# ---------------------------------------------------------------------------
# Abstract reader
# ---------------------------------------------------------------------------

class AbstractReader(ABC):

    @abstractmethod
    def read(self, sessions_dir: Path) -> Any:
        ...


# ---------------------------------------------------------------------------
# Concrete readers
# ---------------------------------------------------------------------------

class ImplantCSVReader(AbstractReader):
    """
    Reads all sessions/{client_id}.log CSV files.
    Returns List[ImplantRecord] with all rows from all implants.
    """

    _FIELDS = [
        "client_id", "os", "pid", "hostname", "ips", "user",
        "discovered_ips", "result_portscan", "result_pwd", "command", "output",
    ]

    def read(self, sessions_dir: Path) -> List[ImplantRecord]:
        records: List[ImplantRecord] = []
        pattern = str(sessions_dir / "*.log")
        for log_path in sorted(glob.glob(pattern)):
            # Skip non-implant logs (access.log, searchsploit.log, etc.)
            name = Path(log_path).stem
            if any(x in name for x in ("access", "searchsploit", "scan_discovery")):
                continue
            try:
                with open(log_path, newline="", encoding="utf-8", errors="replace") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Normalise field names (strip whitespace)
                        row = {k.strip(): (v or "").strip() for k, v in row.items()}
                        if "client_id" not in row and "os" not in row:
                            continue
                        records.append(ImplantRecord(
                            client_id=row.get("client_id", name),
                            os=row.get("os", ""),
                            pid=row.get("pid", ""),
                            hostname=row.get("hostname", ""),
                            ips=row.get("ips", ""),
                            user=row.get("user", ""),
                            discovered_ips=row.get("discovered_ips", ""),
                            result_portscan=row.get("result_portscan", ""),
                            result_pwd=row.get("result_pwd", ""),
                            command=row.get("command", ""),
                            output=row.get("output", ""),
                        ))
            except (OSError, csv.Error):
                continue
        return records


class CommandOutputReader(AbstractReader):
    """
    Reads sessions/logs/c2/command_*output*.txt files.
    Returns Dict[str, str]: {filename_stem -> content}
    """

    def read(self, sessions_dir: Path) -> Dict[str, str]:
        log_dir = sessions_dir / "logs" / "c2"
        outputs: Dict[str, str] = {}
        if not log_dir.exists():
            return outputs
        for txt in sorted(log_dir.glob("command_*output*.txt"))[-200:]:
            try:
                content = txt.read_text(encoding="utf-8", errors="replace").strip()
                if content:
                    outputs[txt.stem] = content[:2000]  # cap at 2KB per file
            except OSError:
                continue
        return outputs


class DiscoveredHostReader(AbstractReader):
    """Reads sessions/hostsdiscovery.txt."""

    def read(self, sessions_dir: Path) -> List[str]:
        path = sessions_dir / "hostsdiscovery.txt"
        if not path.exists():
            return []
        hosts: List[str] = []
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                h = line.strip()
                if h and h not in hosts:
                    hosts.append(h)
        except OSError:
            pass
        return hosts


class TaskReader(AbstractReader):
    """Reads sessions/tasks.json."""

    def read(self, sessions_dir: Path) -> List[CampaignTask]:
        path = sessions_dir / "tasks.json"
        if not path.exists():
            return []
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            tasks: List[CampaignTask] = []
            for item in raw if isinstance(raw, list) else []:
                tasks.append(CampaignTask(
                    id=int(item.get("id", 0)),
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    operator=item.get("operator", ""),
                    status=item.get("status", "New"),
                ))
            return tasks
        except (json.JSONDecodeError, OSError):
            return []


class TaskWriter:
    """Appends or updates tasks in sessions/tasks.json."""

    def __init__(self, sessions_dir: Path) -> None:
        self._path = sessions_dir / "tasks.json"

    def append(self, title: str, description: str, operator: str = "agent",
                status: str = "New") -> CampaignTask:
        tasks = TaskReader().read(self._path.parent)
        new_id = max((t.id for t in tasks), default=-1) + 1
        task = CampaignTask(id=new_id, title=title, description=description,
                            operator=operator, status=status)
        raw = [{"id": t.id, "title": t.title, "description": t.description,
                "operator": t.operator, "status": t.status} for t in tasks]
        raw.append({"id": task.id, "title": task.title,
                    "description": task.description,
                    "operator": task.operator, "status": task.status})
        try:
            tmp = str(self._path) + ".tmp"
            Path(tmp).write_text(json.dumps(raw, indent=2), encoding="utf-8")
            os.replace(tmp, str(self._path))
        except OSError:
            pass
        return task

    def update_status(self, task_id: int, status: str) -> bool:
        tasks = TaskReader().read(self._path.parent)
        raw = []
        found = False
        for t in tasks:
            d = {"id": t.id, "title": t.title, "description": t.description,
                 "operator": t.operator, "status": t.status}
            if t.id == task_id:
                d["status"] = status
                found = True
            raw.append(d)
        if found:
            try:
                tmp = str(self._path) + ".tmp"
                Path(tmp).write_text(json.dumps(raw, indent=2), encoding="utf-8")
                os.replace(tmp, str(self._path))
            except OSError:
                pass
        return found


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------

class SessionAggregator:
    """
    Combines all readers into a single SessionSummary.
    Dependency-injected readers allow substitution in tests.
    """

    def __init__(
        self,
        implant_reader: Optional[AbstractReader] = None,
        output_reader: Optional[AbstractReader] = None,
        host_reader: Optional[AbstractReader] = None,
        task_reader: Optional[AbstractReader] = None,
    ) -> None:
        self._implant_reader = implant_reader or ImplantCSVReader()
        self._output_reader = output_reader or CommandOutputReader()
        self._host_reader = host_reader or DiscoveredHostReader()
        self._task_reader = task_reader or TaskReader()

    def aggregate(self, sessions_dir: Path) -> SessionSummary:
        return SessionSummary(
            implants=self._implant_reader.read(sessions_dir),
            command_outputs=self._output_reader.read(sessions_dir),
            discovered_hosts=self._host_reader.read(sessions_dir),
            tasks=self._task_reader.read(sessions_dir),
        )


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------

_aggregator: Optional[SessionAggregator] = None


def get_aggregator() -> SessionAggregator:
    global _aggregator
    if _aggregator is None:
        _aggregator = SessionAggregator()
    return _aggregator
