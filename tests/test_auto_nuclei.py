"""Tests for the deterministic auto_nuclei sweep."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import modules.auto_nuclei as auto_nuclei
from modules.auto_nuclei import AutoNucleiEngine, NucleiContext


def _write_template(root: Path, relative: str, body: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def _template(root: Path, name: str, *, template_id: str, severity: str, tags: str) -> None:
    _write_template(
        root,
        f"http/{name}.yaml",
        f"""id: {template_id}
info:
  name: {name}
  severity: {severity}
  tags: {tags}
http:
  - method: GET
    path:
      - "{{{{BaseURL}}}}/"
""",
    )


def _engine(tmp_path: Path, runner=None) -> AutoNucleiEngine:
    templates = tmp_path / "templates"
    templates.mkdir()
    _template(templates, "apache-path-traversal", template_id="CVE-2021-41773", severity="critical", tags="cve,apache")
    _template(templates, "nginx-confusion", template_id="CVE-2022-0001", severity="high", tags="cve,nginx")
    _template(templates, "dos-flood", template_id="dos-flood", severity="critical", tags="dos,apache")
    _template(templates, "generic-cve", template_id="CVE-2099-9999", severity="high", tags="cve")
    return AutoNucleiEngine(
        template_dir=templates,
        sessions_dir=tmp_path / "sessions",
        binary="nuclei-test",
        runner=runner,
    )


def test_select_templates_ranks_context_matches_and_skips_dos(tmp_path: Path) -> None:
    engine = _engine(tmp_path)
    context = NucleiContext(
        host="10.0.0.5",
        services=({"port": 80, "name": "http", "product": "apache httpd", "version": "2.4.49"},),
        cves=("CVE-2021-41773",),
        web_targets=("http://10.0.0.5",),
    )
    selected = engine.select_templates(context)
    assert [item.template.id for item in selected] == ["CVE-2021-41773"]
    assert selected[0].score >= 100
    assert "cve:CVE-2021-41773" in selected[0].reasons


def test_allow_generic_admits_unmatched_cve_templates(tmp_path: Path) -> None:
    engine = _engine(tmp_path)
    context = NucleiContext(host="10.0.0.5", services=(), cves=(), web_targets=("http://10.0.0.5",))
    assert engine.select_templates(context) == []
    selected = engine.select_templates(context, allow_generic=True)
    assert {item.template.id for item in selected} == {"CVE-2021-41773", "CVE-2022-0001", "CVE-2099-9999"}
    assert all("dos" not in item.template.tags for item in selected)


def test_run_parses_jsonl_and_publishes_findings(tmp_path: Path, monkeypatch) -> None:
    captured: list[dict] = []

    def fake_record_event(**kwargs):
        captured.append(kwargs)

    monkeypatch.setattr(auto_nuclei, "record_event", fake_record_event)
    payload = {
        "template-id": "CVE-2021-41773",
        "info": {
            "name": "Apache path traversal",
            "severity": "critical",
            "tags": ["cve", "apache"],
            "classification": {"cve-id": ["CVE-2021-41773"]},
        },
        "matched-at": "http://10.0.0.5/",
        "host": "10.0.0.5",
        "matcher-name": "word",
    }

    def fake_runner(command, timeout):
        return subprocess.CompletedProcess(command, 0, stdout=json.dumps(payload) + "\n", stderr="")

    engine = _engine(tmp_path, runner=fake_runner)
    engine.build_context = lambda target: NucleiContext(
        host=target,
        services=({"port": 80, "name": "http", "product": "apache", "version": "2.4.49"},),
        cves=("CVE-2021-41773",),
        web_targets=("http://10.0.0.5",),
    )
    result = engine.run("10.0.0.5")
    assert result.error == ""
    assert len(result.findings) == 1
    assert result.findings[0]["cve"] == "CVE-2021-41773"
    assert result.findings[0]["severity"] == "critical"
    assert "-jsonl" in result.command
    assert "-no-interactsh" in result.command
    assert captured and captured[0]["kind"] == "finding"
    assert captured[0]["severity"] == "critical"
    assert Path(result.artifact).is_file()
    raw = tmp_path / "sessions" / "nuclei_auto_10.0.0.5_output.txt"
    assert raw.is_file()
    assert "CVE-2021-41773" in raw.read_text(encoding="utf-8")


def test_run_fails_closed_without_templates(tmp_path: Path) -> None:
    engine = AutoNucleiEngine(
        template_dir=tmp_path / "missing",
        sessions_dir=tmp_path / "sessions",
        binary="nuclei-test",
        runner=lambda command, timeout: subprocess.CompletedProcess(command, 0, stdout="", stderr=""),
    )
    result = engine.run("10.0.0.5")
    assert "download_nuclei_templates" in result.error


def test_run_fails_closed_without_binary(tmp_path: Path) -> None:
    templates = tmp_path / "templates"
    templates.mkdir()
    _template(templates, "apache", template_id="CVE-2021-41773", severity="critical", tags="cve,apache")
    engine = AutoNucleiEngine(
        template_dir=templates,
        sessions_dir=tmp_path / "sessions",
        binary=str(tmp_path / "missing-nuclei"),
    )
    result = engine.run("10.0.0.5")
    assert "nuclei binary not found" in result.error


def test_dry_run_builds_command_without_executing(tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def fake_runner(command, timeout):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    engine = _engine(tmp_path, runner=fake_runner)
    engine.build_context = lambda target: NucleiContext(
        host=target,
        services=({"port": 80, "name": "http", "product": "apache", "version": "2.4.49"},),
        cves=("CVE-2021-41773",),
        web_targets=("http://10.0.0.5",),
    )
    result = engine.run("10.0.0.5", dry_run=True)
    assert result.error == ""
    assert result.command
    assert calls == []
    assert result.findings == []


def test_build_context_merges_world_model_and_ss_cve(tmp_path: Path) -> None:
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    state = {
        "hosts": {
            "10.0.0.5": {
                "services": {
                    "8080": {"port": 8080, "name": "http-proxy", "product": "nginx", "version": "1.18"},
                    "22": {"port": 22, "name": "ssh", "product": "OpenSSH", "version": "8.2"},
                }
            }
        }
    }
    (sessions / "world_model.json").write_text(json.dumps(state), encoding="utf-8")
    (sessions / "ss_cve_context_10.0.0.5.json").write_text(
        json.dumps(
            {
                "services": [
                    {"port": 8080, "name": "http", "product": "nginx", "version": "1.18", "cves": [{"cve": "cve-2021-23017"}]}
                ]
            }
        ),
        encoding="utf-8",
    )
    engine = AutoNucleiEngine(template_dir=tmp_path / "templates", sessions_dir=sessions, binary="nuclei-test", runner=lambda c, t: None)
    context = engine.build_context("10.0.0.5")
    assert [service["port"] for service in context.services] == [22, 8080]
    assert context.cves == ("CVE-2021-23017",)
    assert "http://10.0.0.5:8080" in context.web_targets
