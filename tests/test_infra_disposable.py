"""TDD unit tests for the disposable infrastructure contracts.

Covers ``cli.commands.infra``, ``modules.c2_builder`` fallback helpers,
``modules.professional_report`` loot/history/summary, ``modules.redteam_gym``
range challenges, ``cli.commands.lab`` range profiles, and the
``c2_fallback_urls`` payload schema slot.
"""

from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def test_parse_tunnel_urls_dedupes() -> None:
    """Tunnel log parsing dedupes quick-tunnel URLs preserving order."""
    from cli.commands.infra import _parse_tunnel_urls

    log = (
        "2026-01-01 INF + https://aaa.trycloudflare.com\n"
        "2026-01-01 INF + https://aaa.trycloudflare.com\n"
        "2026-01-01 INF + https://bbb.trycloudflare.com\n"
    )
    assert _parse_tunnel_urls(log) == [
        "https://aaa.trycloudflare.com",
        "https://bbb.trycloudflare.com",
    ]


def test_parse_tunnel_urls_empty() -> None:
    """Logs without tunnel URLs yield an empty list."""
    from cli.commands.infra import _parse_tunnel_urls

    assert _parse_tunnel_urls("no tunnels here") == []


def test_parse_tunnel_urls_rejects_non_cloudflare() -> None:
    """Non-Cloudflare URLs never enter the redirector inventory."""
    from cli.commands.infra import _parse_tunnel_urls

    assert _parse_tunnel_urls("see https://evil.example.com for details") == []


def test_valid_providers_exact_allowlist() -> None:
    """Provider allowlist is exactly the four supported targets."""
    from cli.commands.infra import VALID_PROVIDERS

    assert set(VALID_PROVIDERS) == {"local", "docker", "digitalocean", "aws"}


def test_infra_phases_as_c2() -> None:
    """Infra commands belong to the C2 kill-chain phase."""
    from cli.commands.infra import InfraCommandSet

    assert InfraCommandSet.phase == "c2"
    assert hasattr(InfraCommandSet, "do_infra")


def test_go_string_list_formats_slice() -> None:
    """Fallback URLs render as a Go string slice body."""
    from modules.c2_builder import _go_string_list

    assert _go_string_list([]) == '""'
    assert _go_string_list(["https://a.trycloudflare.com"]) == '"https://a.trycloudflare.com"'
    rendered = _go_string_list(["https://a.trycloudflare.com", "https://b.trycloudflare.com"])
    assert rendered == '"https://a.trycloudflare.com", "https://b.trycloudflare.com"'


def test_resolve_fallback_urls_param_string() -> None:
    """Comma-separated param values split into fallback URLs."""
    from modules.c2_builder import _resolve_fallback_urls

    urls = _resolve_fallback_urls({"c2_fallback_urls": "https://a.trycloudflare.com, https://b.trycloudflare.com"})
    assert {"https://a.trycloudflare.com", "https://b.trycloudflare.com"} <= set(urls)


def test_resolve_fallback_urls_param_list() -> None:
    """List param values pass through stripped."""
    from modules.c2_builder import _resolve_fallback_urls

    urls = _resolve_fallback_urls({"c2_fallback_urls": ["https://a.trycloudflare.com", ""]})
    assert "https://a.trycloudflare.com" in urls


def test_implant_template_has_fallback_helpers() -> None:
    """Go beacon template carries multi-C2 fallback rotation."""
    template = (BASE_DIR / "sessions" / "implant" / "implant_crypt.go").read_text()
    assert "C2_FALLBACK_URLS" in template
    assert "func c2Candidates(" in template
    assert "func loadBeaconConfig(" in template
    assert "{c2_fallback_urls}" in template


def test_redirector_caddy_filters_paths() -> None:
    """Redirector Caddyfile only forwards C2 paths and 404s the rest."""
    caddyfile = (BASE_DIR / "deploy" / "redirector" / "Caddyfile").read_text()
    assert "/gmail/*" in caddyfile
    assert "respond \"Not Found\" 404" in caddyfile
    assert "host.docker.internal" in caddyfile


def test_redirector_compose_routes_to_caddy() -> None:
    """Redirector compose chains cloudflared through the Caddy filter."""
    compose = (BASE_DIR / "deploy" / "redirector" / "docker-compose.yml").read_text()
    assert "cloudflare/cloudflared" in compose
    assert "http://caddy:8080" in compose
    assert "C2_HOST" in compose


def test_c2_compose_terminates_tls() -> None:
    """Local C2 stack exposes TLS via Caddy with Let's Encrypt storage."""
    compose = (BASE_DIR / "deploy" / "c2" / "docker-compose.yml").read_text()
    assert "caddy:2-alpine" in compose
    assert "443:443" in compose


def test_terraform_firewall_restricts_c2_port() -> None:
    """Terraform firewall pins port 4444 to the redirector droplet."""
    main_tf = (BASE_DIR / "deploy" / "infra" / "providers" / "digitalocean" / "main.tf").read_text()
    assert 'port_range       = "4444"' in main_tf
    assert "redirector" in main_tf


def test_report_collects_history_and_loot() -> None:
    """Report generator collects history lines and loot counters."""
    from modules.professional_report import RedTeamReportGenerator

    generator = RedTeamReportGenerator()
    history = generator.collect_command_history(max_entries=5)
    assert isinstance(history, list)
    assert len(history) <= 5
    loot = generator.collect_loot_summary()
    assert set(loot) == {"categories", "total_files", "total_bytes"}


def test_report_template_summary_mentions_remediation_windows() -> None:
    """Template executive summary states 30-day remediation priority."""
    from modules.professional_report import RedTeamReportGenerator

    generator = RedTeamReportGenerator()
    data = generator.collect_data()
    data["command_history"] = []
    data["loot_summary"] = {"categories": {}, "total_files": 0, "total_bytes": 0}
    generator.classify_findings(data)
    summary = generator.generate_executive_summary(data, with_ai=False)
    assert "30 days" in summary


def test_report_ai_failure_falls_back_to_template() -> None:
    """LLM backend failure never blocks reporting; template is returned."""
    from modules.professional_report import RedTeamReportGenerator

    generator = RedTeamReportGenerator()
    data = {"loot_summary": {}, "command_history": []}
    generator._findings = []
    summary = generator.generate_executive_summary(data, with_ai=True, ai_backend="bogus-backend-xyz")
    assert isinstance(summary, str) and len(summary) > 0


def test_gym_range_challenges_registered() -> None:
    """Range challenges exist for implant, lateral, and exfil practice."""
    from modules.redteam_gym import GYM_CHALLENGE_DEFINITIONS

    for challenge_id in ("first_implant", "lateral_ad", "vault_exfil"):
        assert challenge_id in GYM_CHALLENGE_DEFINITIONS
        assert GYM_CHALLENGE_DEFINITIONS[challenge_id]["scenario"] == "ad-mini"


def test_lab_range_profiles_registered() -> None:
    """Lab exposes the ad-mini cyber range profile with compose file."""
    from cli.commands.lab import RANGE_PROFILES

    assert "ad-mini" in RANGE_PROFILES
    compose = BASE_DIR / "deploy" / "range" / RANGE_PROFILES["ad-mini"]["compose"]
    assert compose.exists()


def test_range_compose_uses_valid_images() -> None:
    """Range compose references verified images (no fictional repositories)."""
    from cli.commands.lab import RANGE_PROFILES

    compose = (BASE_DIR / "deploy" / "range" / RANGE_PROFILES["ad-mini"]["compose"]).read_text()
    assert "instantlinux/samba-dc" in compose
    assert "ziel/" not in compose
    assert "tleemcjr/metasploitable2" in compose


def test_range_workstation_stays_alive() -> None:
    """ws01 keeps a foreground shell so boot services stay reachable."""
    from cli.commands.lab import RANGE_PROFILES

    compose = (BASE_DIR / "deploy" / "range" / RANGE_PROFILES["ad-mini"]["compose"]).read_text()
    assert "tty: true" in compose
    assert "stdin_open: true" in compose


def test_range_dc_secret_wired() -> None:
    """DC consumes the per-deployment admin secret the CLI generates."""
    from cli.commands.lab import RANGE_PROFILES

    compose = (BASE_DIR / "deploy" / "range" / RANGE_PROFILES["ad-mini"]["compose"]).read_text()
    assert "samba-admin-password" in compose
    assert "ADMIN_PASSWORD_SECRET" in compose


def test_range_secret_generator_roundtrip(tmp_path) -> None:
    """Secret helper creates a 0600 file once and reuses it after."""
    from cli.commands.lab import LabCommandSet

    first = LabCommandSet()._ensure_range_secret(tmp_path)
    second = LabCommandSet()._ensure_range_secret(tmp_path)
    assert first and first == second
    assert (tmp_path / "secrets" / "samba-admin-password.txt").exists()


def test_parse_go_version_triples() -> None:
    """Go version strings parse into comparable triples."""
    from modules.c2_builder import _parse_go_version

    assert _parse_go_version("go version go1.26.5 linux/amd64") == (1, 26, 5)
    assert _parse_go_version("garble: go1.26.2") == (1, 26, 2)
    assert _parse_go_version("go version go1.21 linux/arm64") == (1, 21, 0)
    assert _parse_go_version("not a version") is None
    assert _parse_go_version("") is None


def test_compile_commands_route_through_shell() -> None:
    """Every compile command starts with cd so the dispatcher uses bash.

    A bare ``CGO_ENABLED=0`` prefix would be argv-split and crash with
    ``FileNotFoundError: 'CGO_ENABLED=0'``.
    """
    from types import SimpleNamespace

    from modules.c2_builder import _build_compile_commands

    profile = SimpleNamespace(goos="linux", goarch="amd64", cc="gcc", cgo="1", loader="loader_linux.go")
    main, listener, monitor = _build_compile_commands(
        "sessions",
        profile,
        "garble -literals -tiny build",
        '-ldflags="-s -w"',
        "/x/sessions/linux",
        "main.go",
        "/x/sessions/linux_l.go",
        "/x/sessions/linux_l.go",
        "/x/sessions/monrevlin",
        "/x/sessions/monrevlin.go",
    )
    for cmd in (main, listener, monitor):
        assert cmd.startswith("cd sessions && ")
    assert "CGO_ENABLED=1" in main
    assert "CGO_ENABLED=0" in listener
    assert "-o /x/sessions/linux main.go loader_linux.go" in main


def test_garble_mismatch_detected() -> None:
    """Stale garble (built with older Go) is detected before compiling."""
    from unittest.mock import patch

    from modules.c2_builder import _garble_matches_toolchain

    with patch("modules.c2_builder._command_output") as fake:
        fake.side_effect = ["go version go1.26.5 linux/amd64", "garble: go1.26.2"]
        assert _garble_matches_toolchain("go", "garble") is False
    with patch("modules.c2_builder._command_output") as fake:
        fake.side_effect = ["go version go1.26.5 linux/amd64", "garble: go1.26.5"]
        assert _garble_matches_toolchain("go", "garble") is True


def test_redirector_stale_threshold() -> None:
    """Stale redirector threshold is exactly 24 hours."""
    from cli.commands.infra import STALE_AFTER_SECONDS

    assert STALE_AFTER_SECONDS == 86400


def test_format_timeline_event_summarizes_payload() -> None:
    """Timeline events render command payloads instead of raw dicts."""
    from cli.commands.report_enhanced import _format_timeline_event

    ts, etype, msg = _format_timeline_event(
        {
            "ts_iso": "2026-08-22T22:16:42",
            "category": "command",
            "event_type": "killchain",
            "payload": {"command": "lazynmap", "args": "-sV"},
            "target": "127.0.0.1",
        }
    )
    assert ts == "2026-08-22T22:16:42"
    assert etype == "killchain"
    assert msg == "lazynmap -sV"
    assert "{" not in msg


def test_mitre_matrix_keeps_unknown_tactics() -> None:
    """Techniques without a known tactic still render in the matrix."""
    from cli.commands.report_enhanced import _render_mitre_matrix_html

    html = _render_mitre_matrix_html({}, [{"technique_id": "T1003", "name": "Credential Dump", "tactic": "", "status": "tested"}])
    assert "T1003" in html
    assert "Credential Dump" in html


def test_range_backdoor_shell_published() -> None:
    """vsftpd backdoor shell port is reachable from the host."""
    from cli.commands.lab import RANGE_PROFILES

    compose = (BASE_DIR / "deploy" / "range" / RANGE_PROFILES["ad-mini"]["compose"]).read_text()
    assert "6200:6200" in compose
    assert "2121:21" in compose


def test_range_verify_confirms_root(capsys) -> None:
    """Range verifier reports root only when the shell answers uid=0."""
    from unittest.mock import MagicMock, patch

    from cli.commands.lab import LabCommandSet

    ftp = MagicMock()
    ftp.recv.return_value = b"331 Please specify the password.\r\n"
    ftp.__enter__.return_value = ftp
    shell = MagicMock()
    shell.recv.return_value = b"uid=0(root) gid=0(root)\n"
    shell.__enter__.return_value = shell

    with patch("socket.create_connection", side_effect=[ftp, shell]):
        LabCommandSet()._range_verify("ad-mini")
    assert "Root shell confirmed" in capsys.readouterr().out


def test_range_verify_unknown_profile(capsys) -> None:
    """Verifier rejects profiles without an exploit without raising."""
    from cli.commands.lab import LabCommandSet

    LabCommandSet()._range_verify("nosuch")
    assert "No verifier" in capsys.readouterr().out


def test_gym_range_next_steps() -> None:
    """Range challenges point at range commands, others stay classic."""

    from modules.redteam_gym import GYM_DIR, start_challenge

    assert start_challenge("first_implant")["next_steps"][0] == "lab range start ad-mini"
    assert start_challenge("first_blood_web")["next_steps"][0] == "lab start wordpress"
    for leftover in GYM_DIR.glob("active_*.json"):
        try:
            leftover.unlink()
        except OSError:
            pass


def test_find_cloudflared_pids() -> None:
    """ps parsing extracts tunnel PIDs and skips our own process."""
    import os

    from modules.session_cleanup import find_cloudflared_pids

    own = os.getpid()
    ps_output = (
        f"  100 /usr/bin/cloudflared tunnel --url http://x\n"
        f"  {own} /usr/bin/cloudflared tunnel --url http://y\n"
        "  200 /usr/bin/docker compose up\n"
    )
    assert find_cloudflared_pids(ps_output) == [100]
    assert find_cloudflared_pids("") == []


def test_compose_down_missing_file() -> None:
    """Teardown of a missing stack reports success without docker."""
    from modules.session_cleanup import _compose_down

    assert _compose_down(BASE_DIR / "deploy" / "nope" / "docker-compose.yml", "nope") is True


def test_payload_schema_has_fallback_slot() -> None:
    """Payload schema declares the c2_fallback_urls config slot."""
    from core.payload_schema import field_for

    spec = field_for("c2_fallback_urls")
    assert spec is not None
