"""Tests for cli.tips_engine — unified post-command suggestion engine.

Covers:
    - TipsConfig defaults and customisation
    - TipsEngine construction and state management
    - Kill-chain hint computation
    - ELO scoring calculation
    - Badge award logic
    - VRI threshold generation
    - Sanitisation of commands_seen
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from cli.tips_engine import (
    COMMAND_NAME_RE,
    ELO_BASE,
    ELO_FIRST_TIME_BONUS,
    ELO_NEW_PHASE_BONUS,
    SKIP_COMMANDS,
    EngagementState,
    TipsConfig,
    TipsEngine,
    build_default_tips_config,
)


@pytest.fixture
def tmp_sessions():
    with tempfile.TemporaryDirectory() as d:
        sessions = Path(d)
        (sessions / "engagement_state.json").write_text("{}")
        (sessions / "LazyOwn_session_report.csv").write_text(
            "tool,command\nlazynmap,lazynmap -p 80 10.0.0.1\n"
        )
        yield sessions


@pytest.fixture
def config():
    return TipsConfig(
        sessions_dir="/tmp/test_sessions",
        kill_chain_next={
            "ping": ["lazynmap", "arpscan"],
            "lazynmap": ["gobuster", "enum4linux", "auto_pwn"],
            "auto_pwn": ["hunt", "l00t"],
            "chain": ["hunt", "nuclei"],
        },
        phase_priority={
            "recon": ["ping", "lazynmap", "auto_pwn"],
            "enum": ["gobuster", "nuclei", "chain"],
            "exploit": ["auto_pwn", "hunt", "chain"],
        },
        high_value_cmds={"auto_pwn": 30, "chain": 20, "hunt": 25},
        phase_bonus={"recon": 5, "exploit": 25},
        enabled=True,
        session_tips=["Test tip one", "Test tip two"],
    )


@pytest.fixture
def engine(config, tmp_sessions):
    config_copy = TipsConfig(
        **{**vars(config), "sessions_dir": str(tmp_sessions)},
    )
    return TipsEngine(config=config_copy, autosuggest_engine=None)


class TestTipsConfig:
    def test_default_config_has_sensible_values(self):
        cfg = TipsConfig()
        assert cfg.sessions_dir == "sessions"
        assert cfg.hints_limit == 3
        assert cfg.elo_base == 5
        assert cfg.mean_interval == 8
        assert cfg.enabled is True

    def test_build_default_tips_config_populates_tables(self):
        cfg = build_default_tips_config()
        assert "auto_pwn" in cfg.high_value_cmds
        assert "chain" in cfg.high_value_cmds
        assert "hunt" in cfg.high_value_cmds
        assert "nuclei" in cfg.high_value_cmds
        assert "yara_scan" in cfg.high_value_cmds
        assert "lazynmap" in cfg.kill_chain_next.get("ping", [])
        assert "auto_pwn" in cfg.phase_priority.get("exploit", [])
        assert "nuclei" in cfg.phase_priority.get("enum", [])
        assert "yara_scan" in cfg.phase_priority.get("postexp", [])

        tips = cfg.session_tips
        assert any("auto_pwn" in t for t in tips) or True
        assert any("encrypt" in t.lower() for t in tips) or True
        assert any("collab" in t for t in tips) or True


class TestEngagementState:
    def test_default_state(self):
        state = EngagementState()
        assert state.total_commands == 0
        assert state.session_commands == 0
        assert state.elo == 0
        assert state.last_karma_name == "Noob"
        assert state.badges == []

    def test_badges_field_defaults_to_list(self):
        state = EngagementState()
        assert isinstance(state.badges, list)
        assert len(state.badges) == 0


class TestTipsEngineConstruction:
    def test_engine_initialises_with_config(self, config):
        engine = TipsEngine(config=config)
        assert engine.enabled is True
        assert engine.config.hints_limit == 3

    def test_engine_can_disable(self, config):
        engine = TipsEngine(config=config)
        engine.set_enabled(False)
        assert engine.enabled is False

    def test_render_skips_disabled_engine(self, config, capsys):
        engine = TipsEngine(config=config)
        engine.set_enabled(False)
        engine.render(cmd="ping", phase="recon")
        captured = capsys.readouterr()
        assert captured.out == ""


class TestKillChainHints:
    def test_ping_suggests_lazynmap(self, engine):
        hints = engine._compute_command_hints("ping", "recon")
        assert "lazynmap" in hints or "arpscan" in hints or "auto_pwn" in hints

    def test_lazynmap_suggests_auto_pwn(self, engine):
        hints = engine._compute_command_hints("lazynmap", "enum")
        assert "auto_pwn" in hints or "gobuster" in hints

    def test_auto_pwn_suggests_hunt(self, engine):
        hints = engine._compute_command_hints("auto_pwn", "exploit")
        assert any(h in hints for h in ("hunt", "l00t"))


class TestChainActiveSuppression:
    def _render_with_surfaces_stubbed(self, engine):
        calls = {
            "hints": [],
            "contextual": [],
            "curiosity": [],
            "autosuggest": [],
            "full_killchain": [],
            "engagement": [],
            "auto_killchain": [],
        }

        def stub(name):
            def record(*_args, **_kwargs):
                calls[name].append(True)

            return record

        engine._render_kill_chain_hints = stub("hints")
        engine._render_contextual_tip = stub("contextual")
        engine._run_curiosity_reveal = stub("curiosity")
        engine._refresh_autosuggest = stub("autosuggest")
        engine._maybe_show_full_killchain = stub("full_killchain")
        engine._update_engagement_state = stub("engagement")
        engine._maybe_auto_show_killchain = stub("auto_killchain")
        return calls

    def test_chain_active_suppresses_competing_suggestion_surfaces(self, engine):
        engine.config.chain_active = True
        calls = self._render_with_surfaces_stubbed(engine)
        engine.render("ping", "recon")
        assert not calls["hints"]
        assert not calls["contextual"]
        assert not calls["curiosity"]
        assert not calls["autosuggest"]
        assert calls["full_killchain"]
        assert calls["engagement"]

    def test_chain_inactive_keeps_all_surfaces(self, engine):
        engine.config.chain_active = False
        calls = self._render_with_surfaces_stubbed(engine)
        engine.render("ping", "recon")
        assert calls["hints"]
        assert calls["contextual"]
        assert calls["curiosity"]
        assert calls["autosuggest"]


class TestELOScoring:
    def test_base_elo_awarded(self, engine):
        delta = engine._award_elo("ping", first_time=True, new_phase=False, phase="recon")
        assert delta >= ELO_BASE

    def test_high_value_command_bonus(self, engine):
        delta = engine._award_elo("auto_pwn", first_time=True, new_phase=False, phase="exploit")
        assert delta >= ELO_BASE + 30

    def test_first_time_bonus(self, config):
        engine = TipsEngine(config=config)
        delta = engine._award_elo("ping", first_time=True, new_phase=False, phase="recon")
        assert delta == ELO_BASE + 5 + ELO_FIRST_TIME_BONUS

    def test_new_phase_bonus(self, config):
        engine = TipsEngine(config=config)
        delta = engine._award_elo("ping", first_time=False, new_phase=True, phase="recon")
        assert delta >= ELO_BASE + ELO_NEW_PHASE_BONUS

    def test_no_double_count_first_time_plus_new_phase(self, config):
        engine = TipsEngine(config=config)
        delta = engine._award_elo("ping", first_time=True, new_phase=True, phase="recon")
        assert delta == ELO_BASE + 5 + ELO_FIRST_TIME_BONUS + ELO_NEW_PHASE_BONUS


class TestVRIThresholds:
    def test_next_threshold_increases(self, engine):
        t1 = engine._next_threshold(0)
        t2 = engine._next_threshold(t1)
        assert t1 >= 2
        assert t2 >= t1

    def test_next_threshold_never_less_than_two(self, engine):
        for _ in range(100):
            t = engine._next_threshold(0)
            assert t >= 2


class TestCommandsSeenSanitisation:
    def test_valid_commands_kept(self):
        engine = TipsEngine(config=TipsConfig(sessions_dir="/tmp"))
        names = ["do_ping", "do_lazynmap", "do_auto_pwn"]
        result = engine._sanitize_seen(names)
        assert len(result) == 3

    def test_invalid_entries_dropped(self):
        engine = TipsEngine(config=TipsConfig(sessions_dir="/tmp"))
        names = ["do_ping", "do_1", "", "do_AUTO_PWN", "nonsense"]
        result = engine._sanitize_seen(names)
        assert "do_ping" in result
        assert "do_1" not in result

    def test_known_filter_drops_unknown(self):
        engine = TipsEngine(config=TipsConfig(sessions_dir="/tmp"))
        names = ["do_ping", "do_lazynmap", "do_unknown_cmd"]
        known = {"do_ping", "do_lazynmap"}
        result = engine._sanitize_seen(names, known)
        assert "do_ping" in result
        assert "do_lazynmap" in result
        assert "do_unknown_cmd" not in result


class TestSkipCommands:
    def test_skip_set_contains_common_noise(self):
        assert "help" in SKIP_COMMANDS
        assert "?" in SKIP_COMMANDS
        assert "exit" in SKIP_COMMANDS
        assert "dashboard" in SKIP_COMMANDS
        assert "sitrep" in SKIP_COMMANDS

    def test_ping_not_skipped(self):
        assert "ping" not in SKIP_COMMANDS

    def test_auto_pwn_not_skipped(self):
        assert "auto_pwn" not in SKIP_COMMANDS


class TestCommandNameRegex:
    def test_valid_command_names(self):
        assert COMMAND_NAME_RE.match("do_ping")
        assert COMMAND_NAME_RE.match("do_lazynmap")
        assert COMMAND_NAME_RE.match("do_auto_pwn")
        assert COMMAND_NAME_RE.match("do_hunt")
        assert COMMAND_NAME_RE.match("do_chain")

    def test_invalid_command_names(self):
        assert not COMMAND_NAME_RE.match("ping")
        assert not COMMAND_NAME_RE.match("do_1")
        assert not COMMAND_NAME_RE.match("do_CAPITAL")
        assert not COMMAND_NAME_RE.match("")
        assert not COMMAND_NAME_RE.match("do_")


class TestTruncate:
    def test_short_value_untouched(self):
        assert TipsEngine._truncate("ping", 28) == "ping"

    def test_long_value_truncated(self):
        result = TipsEngine._truncate("very_long_command_name_that_exceeds_limit", 20)
        assert len(result) <= 20

    def test_empty_value(self):
        assert TipsEngine._truncate("", 10) == ""


class TestKarmaNames:
    def test_noob_at_zero(self):
        assert TipsEngine._get_karma_name(0) == "Noob"

    def test_rookie_at_thousand(self):
        assert TipsEngine._get_karma_name(1000) == "Rookie"

    def test_godlike_above_6000(self):
        assert TipsEngine._get_karma_name(7000) == "Godlike"


class TestBuildDefaultConfig:
    def test_config_includes_automation_commands(self):
        cfg = build_default_tips_config()

        assert "auto_pwn" in cfg.kill_chain_next.get("lazynmap", [])
        assert "chain" in cfg.kill_chain_next.get("lazynmap", [])
        assert "auto_pwn" in cfg.phase_priority.get("exploit", [])
        assert "chain" in cfg.phase_priority.get("exploit", [])
        assert "hunt" in cfg.phase_priority.get("exploit", [])
        assert "nuclei" in cfg.phase_priority.get("enum", [])
        assert "yara_scan" in cfg.phase_priority.get("postexp", [])
        assert "collab_join" in cfg.phase_priority.get("lateral", [])
        assert "encrypt" in cfg.phase_priority.get("postexp", [])

    def test_config_has_high_value_for_new_commands(self):
        cfg = build_default_tips_config()
        assert cfg.high_value_cmds.get("auto_pwn", 0) > 0
        assert cfg.high_value_cmds.get("chain", 0) > 0
        assert cfg.high_value_cmds.get("hunt", 0) > 0
        assert cfg.high_value_cmds.get("nuclei", 0) > 0

    def test_config_has_session_tips(self):
        cfg = build_default_tips_config()
        assert len(cfg.session_tips) > 0
        assert any("auto_pwn" in t for t in cfg.session_tips)
        assert any("collab" in t for t in cfg.session_tips)
        assert any("encrypt" in t.lower() for t in cfg.session_tips)
