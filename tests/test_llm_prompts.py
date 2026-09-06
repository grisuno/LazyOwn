"""Contract tests for :mod:`modules.llm_prompts`.

Verifies the canonical prompt-template and knowledge-base extraction: pure
template rendering, context loading, KB CRUD/relevance, truncation and the
stable template registry. No network or vendor SDK is exercised.
"""

from __future__ import annotations

import json

import pytest

from modules.llm_prompts import (
    KB_FILE_NAMES,
    TEMPLATES,
    KnowledgeStore,
    LlmPromptConfig,
    truncate_message,
)


def _write_json(path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle)


def _config(tmp_path):
    return LlmPromptConfig(
        project_root=str(tmp_path),
        kb_dir=str(tmp_path / "kb"),
        payload_path=str(tmp_path / "payload.json"),
        event_config_path=str(tmp_path / "event_config.json"),
        sessions_dir=str(tmp_path / "sessions"),
    )


class TestTruncateMessage:
    def test_short_message_returned_unchanged(self):
        assert truncate_message("abc") == "abc"

    def test_long_message_truncated_with_ellipsis(self):
        result = truncate_message("x" * 18000, max_chars=100)
        assert len(result) == 100 + 3
        assert result.endswith("...")

    def test_boundary_length_kept(self):
        text = "a" * 100
        assert truncate_message(text, max_chars=100) == text


class TestKnowledgeStore:
    def test_load_missing_file_returns_empty(self, tmp_path):
        store = KnowledgeStore(str(tmp_path / "nope.json"))
        assert store.load() == []

    def test_load_malformed_file_returns_empty(self, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("not json")
        assert KnowledgeStore(str(path)).load() == []

    def test_add_and_load_roundtrip(self, tmp_path):
        path = tmp_path / "kb.json"
        store = KnowledgeStore(str(path))
        store.add("ping scan", "nmap -sV host")
        assert store.load() == [{"prompt": "ping scan", "response": "nmap -sV host"}]

    def test_relevant_filters_on_keyword(self, tmp_path):
        store = KnowledgeStore(str(tmp_path / "kb.json"))
        store.add("scan ports", "nmap")
        store.add("harvest creds", "secretsdump")
        assert store.relevant("scan") == ["nmap"]
        assert store.relevant("nothing here") == []

    def test_relevant_limits_results(self, tmp_path):
        store = KnowledgeStore(str(tmp_path / "kb.json"))
        for idx in range(12):
            store.add(f"topic {idx}", f"answer {idx}")
        assert len(store.relevant("topic", limit=3)) == 3


class TestConfig:
    def test_from_defaults_points_under_module_parent(self, tmp_path, monkeypatch):
        monkeypatch.setattr("modules.llm_prompts.default_project_root", lambda: str(tmp_path))
        config = LlmPromptConfig.from_defaults()
        assert config.kb_dir == str(tmp_path / "modules")
        assert config.payload_path == str(tmp_path / "payload.json")

    def test_knowledge_base_path_resolves_names(self, tmp_path):
        config = _config(tmp_path)
        assert config.knowledge_base_path("vuln") == str(tmp_path / "kb" / "knowledge_base_vuln.json")

    def test_payload_context_defaults_to_empty(self, tmp_path):
        config = _config(tmp_path)
        ctx = config.load_payload_context()
        assert ctx["rhost"] == ""
        assert set(ctx) == {
            "start_user",
            "start_pass",
            "rhost",
            "lhost",
            "domain",
            "subdomain",
            "wordlist",
            "usrwordlist",
        }

    def test_payload_context_reads_values(self, tmp_path):
        config = _config(tmp_path)
        _write_json(tmp_path / "payload.json", {"rhost": "10.0.0.5", "domain": "corp.local"})
        ctx = config.load_payload_context()
        assert ctx["rhost"] == "10.0.0.5"
        assert ctx["domain"] == "corp.local"

    def test_event_tool_output_empty_when_no_match(self, tmp_path):
        config = _config(tmp_path)
        _write_json(tmp_path / "event_config.json", {"events": [{"name": "a", "tool_output": "x"}]})
        assert config.load_event_tool_output("b") == ""

    def test_event_tool_output_reads_file(self, tmp_path):
        config = _config(tmp_path)
        tool = tmp_path / "tool.txt"
        tool.write_text("open port 445")
        _write_json(tmp_path / "event_config.json", {"events": [{"name": "scan", "tool_output": str(tool)}]})
        assert config.load_event_tool_output("scan") == "open port 445"


class TestTemplates:
    @pytest.mark.parametrize("name", sorted(TEMPLATES))
    def test_render_includes_operator_prompt(self, tmp_path, name):
        config = _config(tmp_path)
        rendered = config.render(name, "MAGIC_QUERY", kb_lines=["kb line"])
        assert "MAGIC_QUERY" in rendered

    @pytest.mark.parametrize("name", sorted(TEMPLATES))
    def test_render_embeds_knowledge_tail(self, tmp_path, name):
        config = _config(tmp_path)
        lines = [f"line-{idx}" for idx in range(10)]
        rendered = config.render(name, "q", kb_lines=lines)
        assert "line-9" in rendered
        assert "line-0" not in rendered

    def test_general_embeds_payload_rhost(self, tmp_path):
        config = _config(tmp_path)
        _write_json(tmp_path / "payload.json", {"rhost": "192.168.1.1"})
        rendered = config.render("general", "q", kb_lines=[])
        assert "192.168.1.1" in rendered

    def test_vuln_embeds_payload_rhost(self, tmp_path):
        config = _config(tmp_path)
        _write_json(tmp_path / "payload.json", {"rhost": "10.1.1.1"})
        rendered = config.render("vuln", "q", kb_lines=[])
        assert "10.1.1.1" in rendered


class TestRegistryIntegrity:
    def test_kb_domains_are_valid_file_names(self):
        from modules.llm_prompts import TEMPLATE_KB_DOMAINS

        assert set(TEMPLATE_KB_DOMAINS).issubset(set(TEMPLATES))
        assert set(TEMPLATE_KB_DOMAINS.values()).issubset(set(KB_FILE_NAMES))

    def test_all_templates_have_registered_kb_domain(self):
        from modules.llm_prompts import TEMPLATE_KB_DOMAINS

        assert set(TEMPLATES) == set(TEMPLATE_KB_DOMAINS)
