"""tests/test_exploration_and_addons.py

Coverage for the new exploration engine and addon schema fields:

- ``cli/exploration.py`` — nmap XML parsing, addon/tool catalogues,
  trigger matching, coverage computation, OS resolution.
- ``cli/exploration_view.py`` — Rich renderer smoke tests.
- ``lazyaddons/*.yaml`` — every shipped addon declares the new ``os``
  and ``trigger`` keys with values inside the allowed sets.

The suite touches no network and writes only to ``tmp_path`` fixtures.
"""

from __future__ import annotations

import io
import json
import textwrap
from pathlib import Path

import pytest
import yaml
from rich.console import Console

from cli.exploration import (
    ALLOWED_OS_VALUES,
    ANY_OS,
    AddonCatalog,
    AddonEntry,
    DiscoveredService,
    ExplorationEngine,
    NmapXmlReader,
    ToolCatalog,
    TriggerMatcher,
    normalise_os,
    normalise_trigger,
    resolve_current_os,
)
from cli.exploration_view import render_exploration

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDONS_DIR = REPO_ROOT / "lazyaddons"


SAMPLE_NMAP_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nmaprun>
<nmaprun>
  <host>
    <address addr="10.10.10.5" addrtype="ipv4"/>
    <ports>
      <port protocol="tcp" portid="445">
        <state state="open"/>
        <service name="microsoft-ds" product="Samba" version="4.15"/>
      </port>
      <port protocol="tcp" portid="22">
        <state state="closed"/>
        <service name="ssh"/>
      </port>
      <port protocol="tcp" portid="80">
        <state state="open"/>
        <service name="http"/>
      </port>
    </ports>
  </host>
</nmaprun>
"""


@pytest.fixture
def fake_sessions(tmp_path: Path) -> Path:
    """Create a sessions/ directory with one valid nmap XML."""

    sessions = tmp_path / "sessions"
    sessions.mkdir()
    (sessions / "scan_10.10.10.5.nmap.xml").write_text(SAMPLE_NMAP_XML)
    (sessions / "LazyOwn_session_report.csv").write_text(
        "ts,tool,command\n1,evilginx2,evilginx2\n2,lazynmap,lazynmap\n"
    )
    return tmp_path


@pytest.fixture
def fake_addons(tmp_path: Path) -> Path:
    """Create a lazyaddons/ directory with two addons exercising both fields."""

    addons = tmp_path / "lazyaddons"
    addons.mkdir()
    (addons / "evilginx2.yaml").write_text(
        textwrap.dedent(
            """\
            name: evilginx2
            description: phishing
            enabled: true
            os: any
            trigger: [http, https]
            tool:
              name: evilginx2
              repo_url: https://example.invalid/evilginx2.git
              install_path: external/.exploit/evilginx2
              execute_command: ./evilginx2
            category: 08. Lateral Movement
            """
        )
    )
    (addons / "winexploit.yaml").write_text(
        textwrap.dedent(
            """\
            name: winexploit
            description: example
            enabled: true
            os: windows
            trigger: [microsoft-ds]
            tool:
              name: winexploit
              repo_url: https://example.invalid/winexploit.git
              install_path: external/.exploit/winexploit
              execute_command: ./winexploit
            category: 03. Exploitation
            """
        )
    )
    return tmp_path


@pytest.fixture
def fake_tools(tmp_path: Path) -> Path:
    """Create a tools/ directory with one trigger-matching ``.tool``."""

    tools = tmp_path / "tools"
    tools.mkdir()
    (tools / "smbenum.tool").write_text(
        json.dumps(
            {
                "toolname": "smbenum",
                "command": "smbclient -L //{ip}",
                "trigger": ["microsoft-ds"],
                "active": True,
                "category": "02. Scanning",
                "description": "smb listing",
                "os": "windows",
            }
        )
    )
    return tmp_path


class TestNormalisers:
    """Pure helpers used by both the loader and the catalogue."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("Linux", "linux"),
            ("WINDOWS", "windows"),
            ("any", "any"),
            ("bogus", "any"),
            (None, "any"),
            ("", "any"),
            (42, "any"),
        ],
    )
    def test_normalise_os(self, value, expected):
        assert normalise_os(value, default=ANY_OS) == expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("smb", ("smb",)),
            (["SMB", "microsoft-ds", ""], ("smb", "microsoft-ds")),
            ((" ftp ", "ftps"), ("ftp", "ftps")),
            (None, ()),
            ("", ()),
            (42, ()),
            ([42, "ldap"], ("ldap",)),
        ],
    )
    def test_normalise_trigger(self, value, expected):
        assert normalise_trigger(value) == expected


class TestNmapXmlReader:
    """Discovered-service extraction from sessions/scan_*.nmap.xml."""

    def test_reads_only_open_ports(self, fake_sessions, monkeypatch):
        monkeypatch.chdir(fake_sessions)
        reader = NmapXmlReader()
        services = reader.discover()
        ports = sorted(s.port for s in services)
        assert ports == [80, 445]

    def test_target_filter_excludes_other_hosts(self, fake_sessions, monkeypatch):
        monkeypatch.chdir(fake_sessions)
        reader = NmapXmlReader()
        assert reader.discover("nope") == []

    def test_records_product_version(self, fake_sessions, monkeypatch):
        monkeypatch.chdir(fake_sessions)
        services = NmapXmlReader().discover()
        smb = [s for s in services if s.port == 445][0]
        assert smb.product == "Samba"
        assert smb.version == "4.15"
        assert smb.label == "microsoft-ds:445/tcp"


class TestCatalogues:
    """Addon and tool YAML/JSON loaders."""

    def test_addon_catalog_loads_os_and_trigger(self, fake_addons, monkeypatch):
        monkeypatch.chdir(fake_addons)
        entries = AddonCatalog().load()
        names = {e.name for e in entries}
        assert names == {"evilginx2", "winexploit"}
        ev = next(e for e in entries if e.name == "evilginx2")
        assert ev.addon_os == "any"
        assert ev.trigger == ("http", "https")
        assert ev.enabled is True

    def test_tool_catalog_loads_os_default(self, fake_tools, monkeypatch):
        monkeypatch.chdir(fake_tools)
        entries = ToolCatalog().load()
        assert len(entries) == 1
        tool = entries[0]
        assert tool.name == "smbenum"
        assert tool.tool_os == "windows"
        assert tool.trigger == ("microsoft-ds",)


class TestTriggerMatcher:
    """Service/OS overlap checks."""

    def test_os_compat_any_passes(self):
        matcher = TriggerMatcher(current_os="linux")
        addon = _addon("a", "any", ["http"])
        svc = _svc("http", 80)
        assert matcher.addons_for_service(svc, [addon]) == [addon]

    def test_os_mismatch_filters_out(self):
        matcher = TriggerMatcher(current_os="linux")
        addon = _addon("a", "windows", ["http"])
        svc = _svc("http", 80)
        assert matcher.addons_for_service(svc, [addon]) == []

    def test_wildcard_matches_any_service(self):
        matcher = TriggerMatcher(current_os="any")
        addon = _addon("a", "any", ["all"])
        svc = _svc("oddservice", 99)
        assert matcher.addons_for_service(svc, [addon]) == [addon]

    def test_disabled_addon_skipped(self):
        matcher = TriggerMatcher(current_os="any")
        addon = _addon("a", "any", ["http"], enabled=False)
        svc = _svc("http", 80)
        assert matcher.addons_for_service(svc, [addon]) == []


class TestEngineEndToEnd:
    """ExplorationEngine wires reader + catalogues + matcher + history."""

    def test_suggestions_and_coverage(self, fake_sessions, fake_addons, fake_tools, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        engine = ExplorationEngine(current_os="windows")
        grouped = engine.suggestions_for_target("10.10.10.5")
        smb_entry = grouped["microsoft-ds:445/tcp"]
        assert {a.name for a in smb_entry["addons"]} == {"winexploit"}
        assert {t.name for t in smb_entry["tools"]} == {"smbenum"}
        http_entry = grouped["http:80/tcp"]
        assert {a.name for a in http_entry["addons"]} == {"evilginx2"}

        report = engine.coverage("10.10.10.5")
        assert report.services_total == 2
        assert report.addons_executed == 1
        assert 0.0 < report.addon_coverage <= 1.0

    def test_unexplored_excludes_history(self, fake_sessions, fake_addons, fake_tools, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        engine = ExplorationEngine(current_os="windows")
        ux_addons = {a.name for a in engine.unexplored_addons("10.10.10.5")}
        assert "evilginx2" not in ux_addons
        assert "winexploit" in ux_addons


class TestResolveCurrentOs:
    """Mapping between payload.json fields and the MITRE platform string."""

    @pytest.mark.parametrize(
        "payload,expected",
        [
            ({"os_id": 1}, "linux"),
            ({"os_id": 2}, "windows"),
            ({"os_id": 3}, "macos"),
            ({"os_id": 9}, "any"),
            ({"platform": "Linux"}, "linux"),
            ({"platform": "windows"}, "windows"),
            ({"platform": "garbage"}, "any"),
            ({}, "any"),
            (None, "any"),
        ],
    )
    def test_resolves(self, payload, expected):
        assert resolve_current_os(payload) == expected


class TestRenderer:
    """``render_exploration`` must run without raising for any scope."""

    def test_renders_empty_scope(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        engine = ExplorationEngine(current_os="any")
        buffer = io.StringIO()
        console = Console(file=buffer, force_terminal=False, width=80)
        render_exploration(console, engine, target=None, history=set())
        text = buffer.getvalue()
        assert "Exploration scope" in text
        assert "Exploration coverage" in text

    def test_renders_populated_scope(self, fake_sessions, fake_addons, fake_tools, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        engine = ExplorationEngine(current_os="windows")
        buffer = io.StringIO()
        console = Console(file=buffer, force_terminal=False, width=140)
        render_exploration(console, engine, target="10.10.10.5", history=engine.history())
        text = buffer.getvalue()
        assert "10.10.10.5" in text
        assert "microsoft-ds:445/tcp" in text
        assert "winexploit" in text


class TestShippedAddonsRespectSchema:
    """Every YAML in lazyaddons/ must declare ``os`` + ``trigger`` validly."""

    @pytest.fixture(scope="class")
    def addon_files(self) -> list[Path]:
        return sorted(ADDONS_DIR.glob("*.yaml"))

    def test_at_least_one_addon_exists(self, addon_files):
        assert addon_files, "no lazyaddons/*.yaml files found"

    def test_all_have_os_in_allowed_values(self, addon_files):
        offenders: list[str] = []
        for path in addon_files:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            raw = data.get("os")
            if not isinstance(raw, str) or raw.strip().lower() not in ALLOWED_OS_VALUES:
                offenders.append(f"{path.name}: os={raw!r}")
        assert not offenders, "\n".join(offenders)

    def test_all_have_trigger_list(self, addon_files):
        offenders: list[str] = []
        for path in addon_files:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            raw = data.get("trigger")
            if not isinstance(raw, list):
                offenders.append(f"{path.name}: trigger={raw!r}")
                continue
            for item in raw:
                if not isinstance(item, str):
                    offenders.append(f"{path.name}: non-string trigger {item!r}")
        assert not offenders, "\n".join(offenders)


def _addon(name: str, addon_os: str, trigger: list[str], enabled: bool = True) -> AddonEntry:
    """Build an AddonEntry for unit tests."""

    return AddonEntry(
        name=name,
        description="",
        category="14. Yaml Addon.",
        addon_os=addon_os,
        trigger=tuple(trigger),
        repo_url="",
        enabled=enabled,
        source_path=f"{name}.yaml",
    )


def _svc(service: str, port: int) -> DiscoveredService:
    """Build a DiscoveredService for unit tests."""

    return DiscoveredService(
        host="10.10.10.5",
        port=port,
        proto="tcp",
        service=service,
    )
