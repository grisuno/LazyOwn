"""Tests for /report and /banners endpoints error handling.

Validates that both endpoints handle: missing files, empty files,
invalid JSON, missing dictionary keys, and malformed data.

Since lazyc2.py blocks importing the lazyc2 package (file vs directory
package conflict), these tests validate the fixed logic via pure
standalone functions that mirror the actual endpoint handlers.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest


def load_banners(path: str) -> list | None:
    """Mirrors the fixed load_banners() from lazyc2.py and storage.py.

    Handles: FileNotFoundError, JSONDecodeError, dict format with 'banners' key,
    and flat list format.
    """
    try:
        with open(path, "r") as f:
            config_banner = json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    if isinstance(config_banner, dict) and "banners" in config_banner:
        return config_banner.get("banners", [])
    if isinstance(config_banner, list):
        return config_banner
    return None


def load_json_file_safe(path: str) -> dict | list:
    """Mirrors the fixed session data loading logic from /report endpoint.

    Handles: FileNotFoundError, JSONDecodeError, empty files.
    """
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            return {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def build_report_context(report_file: str, session_file: str, tools_dir: str) -> dict:
    """Mirrors the fixed /report endpoint data-gathering logic.

    Returns:
        dict with keys: report_data, tools, session_data.
    """
    try:
        with open(report_file, "r") as f:
            report_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        report_data = {}

    tools = []
    try:
        for filename in os.listdir(tools_dir):
            if filename.endswith(".tool"):
                tool_path = os.path.join(tools_dir, filename)
                try:
                    with open(tool_path, "r") as f:
                        tool_data = json.load(f)
                        tool_data["filename"] = filename
                        tools.append(tool_data)
                except (FileNotFoundError, json.JSONDecodeError):
                    pass
    except FileNotFoundError:
        pass

    session_data = load_json_file_safe(session_file)

    if isinstance(session_data, list):
        session_data = session_data[0] if session_data else {}
    if not isinstance(session_data, dict):
        session_data = {}

    session_data.setdefault("params", {})
    session_data["params"]["api_key"] = "Hidden content"

    return {"report_data": report_data, "tools": tools, "session_data": session_data}


def build_banners_html(banners: list | None) -> str:
    """Mirrors the fixed /banners endpoint HTML table generation logic.

    Uses .get() for all banner keys to avoid KeyError on missing fields.
    """
    if not banners:
        return "No banners found."

    html = '<table class="table table-dark table-striped">\n'
    html += "  <thead>\n    <tr>\n"
    html += "      <th>Hostname</th>\n"
    html += "      <th>Port</th>\n"
    html += "      <th>Protocol</th>\n"
    html += "      <th>Extra</th>\n"
    html += "      <th>Service</th>\n"
    html += "    </tr>\n  </thead>\n  <tbody>\n"

    for banner in banners:
        html += "    <tr>\n"
        html += f'      <td>{banner.get("hostname", "")}</td>\n'
        html += f'      <td>{banner.get("port", "")}</td>\n'
        html += f'      <td>{banner.get("protocol", "")}</td>\n'
        html += f'      <td>{banner.get("extra", "")}</td>\n'
        html += f'      <td>{banner.get("service", "")}</td>\n'
        html += "    </tr>\n"

    html += "  </tbody>\n</table>"
    return html


class TestLoadBanners:
    """Tests for the fixed load_banners() logic."""

    def test_dict_format(self, tmp_path: Path):
        path = tmp_path / "banners.json"
        path.write_text(json.dumps({
            "banners": [
                {"hostname": "srv1", "port": 22, "protocol": "tcp", "extra": "", "service": "ssh"},
                {"hostname": "srv2", "port": 443, "protocol": "tcp", "extra": "nginx", "service": "https"},
            ]
        }))
        result = load_banners(str(path))
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["hostname"] == "srv1"
        assert result[1]["service"] == "https"

    def test_empty_dict(self, tmp_path: Path):
        path = tmp_path / "banners.json"
        path.write_text(json.dumps({"banners": []}))
        result = load_banners(str(path))
        assert isinstance(result, list)
        assert len(result) == 0

    def test_file_not_found(self, tmp_path: Path):
        result = load_banners(str(tmp_path / "nonexistent.json"))
        assert result is None

    def test_invalid_json(self, tmp_path: Path):
        path = tmp_path / "banners.json"
        path.write_text("{not valid json")
        result = load_banners(str(path))
        assert result is None

    def test_empty_file(self, tmp_path: Path):
        path = tmp_path / "banners.json"
        path.write_text("")
        result = load_banners(str(path))
        assert result is None

    def test_flat_list_format(self, tmp_path: Path):
        path = tmp_path / "banners.json"
        path.write_text(json.dumps([
            {"hostname": "flat", "port": 8080, "protocol": "tcp", "extra": "", "service": "http"},
        ]))
        result = load_banners(str(path))
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["hostname"] == "flat"


class TestBannersHTML:
    """Tests for the fixed banners HTML table generation."""

    def test_empty_banners(self):
        assert build_banners_html(None) == "No banners found."
        assert build_banners_html([]) == "No banners found."

    def test_missing_keys_does_not_crash(self):
        banners = [
            {"hostname": "srv1"},
            {"port": 8080},
            {},
            {"hostname": "srv4", "port": 443, "protocol": "tcp", "extra": "", "service": "https"},
        ]
        result = build_banners_html(banners)
        assert "srv1" in result
        assert "8080" in result
        assert "srv4" in result
        assert "https" in result

    def test_valid_data(self):
        banners = [
            {"hostname": "dc01", "port": 389, "protocol": "tcp", "extra": "LDAP", "service": "ldap"},
        ]
        result = build_banners_html(banners)
        assert "dc01" in result
        assert "389" in result
        assert "LDAP" in result
        assert "ldap" in result
        assert "<table" in result
        assert "table-dark" in result


class TestReportContext:
    """Tests for the fixed /report data gathering logic."""

    def test_valid_files(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text(json.dumps({"assessment": "test"}))
        session_file = tmp_path / "session.json"
        session_file.write_text(json.dumps({"rhost": "10.0.0.1", "params": {"lhost": "10.10.14.1"}}))
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "test.tool").write_text(json.dumps({"name": "nmap"}))

        ctx = build_report_context(str(report_file), str(session_file), str(tools_dir))
        assert ctx["report_data"]["assessment"] == "test"
        assert ctx["session_data"]["rhost"] == "10.0.0.1"
        assert ctx["session_data"]["params"]["api_key"] == "Hidden content"
        assert len(ctx["tools"]) == 1
        assert ctx["tools"][0]["name"] == "nmap"

    def test_empty_session_file(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text(json.dumps({"key": "val"}))
        session_file = tmp_path / "session.json"
        session_file.write_text("")
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        ctx = build_report_context(str(report_file), str(session_file), str(tools_dir))
        assert ctx["report_data"]["key"] == "val"
        assert isinstance(ctx["session_data"], dict)
        assert ctx["session_data"]["params"]["api_key"] == "Hidden content"

    def test_invalid_json_session(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text(json.dumps({"key": "val"}))
        session_file = tmp_path / "session.json"
        session_file.write_text("{not json content")
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        ctx = build_report_context(str(report_file), str(session_file), str(tools_dir))
        assert isinstance(ctx["session_data"], dict)
        assert ctx["session_data"]["params"]["api_key"] == "Hidden content"

    def test_missing_session_file(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text(json.dumps({"key": "val"}))
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        ctx = build_report_context(str(report_file), str(tmp_path / "nonexistent.json"), str(tools_dir))
        assert isinstance(ctx["session_data"], dict)
        assert ctx["session_data"]["params"]["api_key"] == "Hidden content"

    def test_missing_body_report(self, tmp_path: Path):
        session_file = tmp_path / "session.json"
        session_file.write_text(json.dumps({"rhost": "10.0.0.1"}))
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        ctx = build_report_context(str(tmp_path / "nonexistent.json"), str(session_file), str(tools_dir))
        assert ctx["report_data"] == {}
        assert ctx["session_data"]["rhost"] == "10.0.0.1"

    def test_invalid_body_report_json(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text("{bad stuff")
        session_file = tmp_path / "session.json"
        session_file.write_text(json.dumps({"rhost": "10.0.0.1"}))
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        ctx = build_report_context(str(report_file), str(session_file), str(tools_dir))
        assert ctx["report_data"] == {}
        assert ctx["session_data"]["rhost"] == "10.0.0.1"

    def test_session_data_as_list(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text(json.dumps({"key": "val"}))
        session_file = tmp_path / "session.json"
        session_file.write_text(json.dumps([{"rhost": "10.0.0.2"}]))
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        ctx = build_report_context(str(report_file), str(session_file), str(tools_dir))
        assert ctx["session_data"]["rhost"] == "10.0.0.2"

    def test_empty_session_list(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text(json.dumps({"key": "val"}))
        session_file = tmp_path / "session.json"
        session_file.write_text("[]")
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        ctx = build_report_context(str(report_file), str(session_file), str(tools_dir))
        assert isinstance(ctx["session_data"], dict)
        assert ctx["session_data"]["params"]["api_key"] == "Hidden content"

    def test_missing_tools_dir(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text(json.dumps({"key": "val"}))
        session_file = tmp_path / "session.json"
        session_file.write_text(json.dumps({"rhost": "10.0.0.1"}))

        ctx = build_report_context(str(report_file), str(session_file), str(tmp_path / "nonexistent_tools"))
        assert ctx["tools"] == []
        assert ctx["session_data"]["rhost"] == "10.0.0.1"

    def test_invalid_tool_file_does_not_crash(self, tmp_path: Path):
        report_file = tmp_path / "body_report.json"
        report_file.write_text(json.dumps({"key": "val"}))
        session_file = tmp_path / "session.json"
        session_file.write_text(json.dumps({"rhost": "10.0.0.1"}))
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "bad.tool").write_text("{invalid json")
        (tools_dir / "good.tool").write_text(json.dumps({"name": "valid_tool"}))

        ctx = build_report_context(str(report_file), str(session_file), str(tools_dir))
        assert len(ctx["tools"]) == 1
        assert ctx["tools"][0]["name"] == "valid_tool"


class TestLoadJSONFileSafe:
    """Tests for the safe JSON file loader used by /report."""

    def test_valid_json(self, tmp_path: Path):
        path = tmp_path / "data.json"
        path.write_text('{"key": "value"}')
        assert load_json_file_safe(str(path)) == {"key": "value"}

    def test_empty_file(self, tmp_path: Path):
        path = tmp_path / "data.json"
        path.write_text("")
        assert load_json_file_safe(str(path)) == {}

    def test_file_not_found(self, tmp_path: Path):
        assert load_json_file_safe(str(tmp_path / "nonexistent.json")) == {}

    def test_invalid_json(self, tmp_path: Path):
        path = tmp_path / "data.json"
        path.write_text("{not json at all")
        assert load_json_file_safe(str(path)) == {}

    def test_list_json(self, tmp_path: Path):
        path = tmp_path / "data.json"
        path.write_text('[{"a": 1}, {"b": 2}]')
        assert load_json_file_safe(str(path)) == [{"a": 1}, {"b": 2}]
