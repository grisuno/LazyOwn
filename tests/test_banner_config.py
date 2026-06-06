"""Tests for cli/banner_config.py — registry, settings, renderer, wizard.

The curses-driven configurator is exercised through a deterministic fake
:class:`BannerConfigurator` substitute so we do not need a TTY. Renderer
behaviour is verified by stripping ANSI from the output and asserting the
three-line Neon Box structure plus the on/off behaviour of each segment.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.banner_config import (  # noqa: E402
    BannerConfig,
    BannerRenderer,
    BannerSettings,
    ColorPalette,
    ColorRegistry,
    ContextResolver,
    GlyphRegistry,
    SegmentRegistry,
    banner_summary,
    build_default_registry,
    render_prompt,
    strip_ansi,
)


@pytest.fixture
def registry() -> SegmentRegistry:
    return build_default_registry()


@pytest.fixture
def color_registry() -> ColorRegistry:
    return ColorRegistry()


@pytest.fixture
def glyph_registry() -> GlyphRegistry:
    return GlyphRegistry()


@pytest.fixture
def neutral_palette() -> ColorPalette:
    blank = ""
    return ColorPalette(
        reset=blank, primary=blank, secondary=blank, accent=blank,
        info=blank, danger=blank, success=blank,
    )


# --- registry ------------------------------------------------------------


def test_registry_lists_every_canonical_segment(registry):
    ids = {s.spec.id for s in registry.all()}
    expected = {
        "user_host", "iface", "lhost", "rhost", "domain", "public_ip",
        "cwd", "git", "venv", "time", "kernel", "version", "battery_load",
    }
    assert expected.issubset(ids)


def test_registry_group_partition(registry):
    top_ids = {s.spec.id for s in registry.by_group("top")}
    middle_ids = {s.spec.id for s in registry.by_group("middle")}
    assert top_ids & middle_ids == set()
    assert "user_host" in top_ids
    assert "cwd" in middle_ids


def test_registry_lookup_returns_none_for_unknown(registry):
    assert registry.get("not_a_segment") is None


# --- settings ------------------------------------------------------------


def test_settings_defaults_match_registry_defaults(registry):
    defaults = BannerSettings.defaults(registry)
    expected_enabled = {s.spec.id for s in registry.all() if s.spec.default_enabled}
    expected_colors = {s.spec.id: s.spec.default_color for s in registry.all()}
    expected_glyphs = {slot: GlyphRegistry().default(slot) for slot in GlyphRegistry().slots()}
    assert defaults.enabled == expected_enabled
    assert defaults.colors == expected_colors
    assert defaults.glyphs == expected_glyphs


def test_settings_round_trip_through_payload_block(registry):
    settings = BannerSettings(enabled={"user_host", "rhost", "cwd"})
    block = settings.to_payload_block()
    rebuilt = BannerSettings.from_payload(registry, {"banner": block}, "banner")
    assert rebuilt.enabled == settings.enabled


def test_settings_from_payload_falls_back_to_defaults_when_missing(registry):
    settings = BannerSettings.from_payload(registry, None, "banner")
    assert settings.enabled == BannerSettings.defaults(registry).enabled


def test_settings_from_payload_ignores_unknown_ids(registry):
    payload = {"banner": {"enabled": ["user_host", "totally_made_up"]}}
    settings = BannerSettings.from_payload(registry, payload, "banner")
    assert settings.enabled == {"user_host"}


def test_settings_toggle_adds_then_removes():
    settings = BannerSettings(enabled={"cwd"})
    settings.toggle("rhost")
    assert "rhost" in settings.enabled
    settings.toggle("rhost")
    assert "rhost" not in settings.enabled


def test_settings_enable_all_then_disable_all(registry):
    settings = BannerSettings()
    settings.enable_all(registry)
    assert len(settings.enabled) == len(registry.all())
    settings.disable_all()
    assert settings.enabled == set()


# --- renderer ------------------------------------------------------------


def _make_ctx(palette: ColorPalette, **overrides):
    base = dict(
        user="root", hostname="kali",
        iface_name="tun0", iface_ip="10.10.14.5",
        lhost="10.10.14.5", rhost="10.10.11.5",
        domain="target.htb", cwd="/home/op/work",
        git_dirty=False, git_branch="main",
        venv_name="env", now_str="22:14:33",
        kernel="6.19.14", version="release/0.2.107",
        public_ip="203.0.113.7", battery_or_load="0.42",
        palette=palette,
    )
    base.update(overrides)
    from cli.banner_config import RenderContext
    return RenderContext(**base)


def test_renderer_emits_three_lines_with_box_corners(registry, neutral_palette):
    settings = BannerSettings.defaults(registry)
    ctx = _make_ctx(neutral_palette)
    rendered = BannerRenderer(BannerConfig(), registry).render(settings, ctx)
    lines = rendered.splitlines()
    assert len(lines) == 3
    assert lines[0].startswith("╔")
    assert lines[1].startswith("║")
    assert lines[2].startswith("╚")


def test_renderer_omits_disabled_segments(registry, neutral_palette):
    settings = BannerSettings(enabled={"user_host", "cwd"})
    ctx = _make_ctx(neutral_palette)
    plain = strip_ansi(BannerRenderer(BannerConfig(), registry).render(settings, ctx))
    assert "root@kali" in plain
    assert "/home/op/work" in plain
    assert "RHOST" not in plain
    assert "target.htb" not in plain
    assert "git" not in plain


def test_renderer_includes_kernel_and_version_when_enabled(registry, neutral_palette):
    settings = BannerSettings(enabled={"user_host", "kernel", "version"})
    ctx = _make_ctx(neutral_palette)
    plain = strip_ansi(BannerRenderer(BannerConfig(), registry).render(settings, ctx))
    assert "6.19.14" in plain
    assert "release/0.2.107" in plain


def test_renderer_drops_empty_value_segments(registry, neutral_palette):
    settings = BannerSettings(enabled=set(BannerSettings.defaults(registry).enabled) | {"public_ip", "kernel"})
    ctx = _make_ctx(neutral_palette, public_ip="", kernel="")
    plain = strip_ansi(BannerRenderer(BannerConfig(), registry).render(settings, ctx))
    assert "PUB" not in plain
    assert "kernel" not in plain


def test_renderer_marks_dirty_git_with_dirty_glyph(registry, neutral_palette):
    settings = BannerSettings(enabled={"git"})
    ctx_dirty = _make_ctx(neutral_palette, git_dirty=True, git_branch="feature/x")
    ctx_clean = _make_ctx(neutral_palette, git_dirty=False, git_branch="main")
    renderer = BannerRenderer(BannerConfig(), registry)
    dirty = strip_ansi(renderer.render(settings, ctx_dirty))
    clean = strip_ansi(renderer.render(settings, ctx_clean))
    assert "✗" in dirty and "✔" not in dirty
    assert "✔" in clean and "✗" not in clean


# --- render_prompt public entry point ------------------------------------


def test_render_prompt_uses_payload_banner_block():
    payload = {
        "rhost": "10.10.11.5",
        "domain": "target.htb",
        "banner": {"enabled": ["user_host", "rhost"]},
    }
    plain = strip_ansi(render_prompt(payload))
    assert "RHOST" in plain
    assert "target.htb" not in plain


def test_render_prompt_with_no_payload_uses_defaults():
    plain = strip_ansi(render_prompt(None))
    assert plain.count("\n") == 2
    assert plain.startswith("╔")


# --- summary -------------------------------------------------------------


def test_banner_summary_lists_enabled_ids_sorted():
    settings = BannerSettings(enabled={"cwd", "rhost", "user_host"})
    summary = banner_summary(settings)
    assert summary == "cwd, rhost, user_host"


def test_banner_summary_handles_empty():
    assert banner_summary(BannerSettings(enabled=set())) == "<none>"


# --- ContextResolver -----------------------------------------------------


def test_context_resolver_uses_payload_rhost_and_lhost(neutral_palette):
    cfg = BannerConfig()
    resolver = ContextResolver(cfg, neutral_palette)
    ContextResolver._public_ip_cache = (0.0, "")
    ContextResolver._kernel_cache = (0.0, "")
    ContextResolver._version_cache = (0.0, "")
    with mock.patch("cli.banner_config._read_network_info", return_value={"tun0": "10.10.14.5"}):
        ctx = resolver.resolve({"rhost": "10.10.11.5", "lhost": "10.10.14.5"})
    assert ctx.rhost == "10.10.11.5"
    assert ctx.lhost == "10.10.14.5"
    assert ctx.iface_name == "tun0"
    assert ctx.iface_ip == "10.10.14.5"


def test_context_resolver_public_ip_caches_within_ttl(neutral_palette):
    cfg = BannerConfig()
    resolver = ContextResolver(cfg, neutral_palette)
    ContextResolver._public_ip_cache = (0.0, "")
    fake_calls = {"n": 0}

    class _FakeResp:
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            return False
        def read(self):
            fake_calls["n"] += 1
            return b"198.51.100.4"

    with mock.patch("cli.banner_config.urllib.request.urlopen", return_value=_FakeResp()):
        first = resolver._public_ip({})
        second = resolver._public_ip({})
    assert first == "198.51.100.4"
    assert second == "198.51.100.4"
    assert fake_calls["n"] == 1


# --- configurator wizard (curses) ----------------------------------------


def test_configurator_returns_none_in_non_tty_environment(monkeypatch, registry, neutral_palette, color_registry, glyph_registry):
    from cli.banner_config import BannerConfigurator
    cfg = BannerConfig()
    ctx = _make_ctx(neutral_palette)
    renderer = BannerRenderer(cfg, registry, color_registry, glyph_registry)
    initial = BannerSettings.defaults(registry, color_registry, glyph_registry)
    wizard = BannerConfigurator(cfg, registry, color_registry, glyph_registry, renderer, ctx, initial)
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    assert wizard.run() is None


# --- ColorRegistry -------------------------------------------------------


def test_color_registry_exposes_named_palette(color_registry):
    names = color_registry.names()
    assert "default" in names
    assert "bright_green" in names
    assert "bright_red" in names


def test_color_registry_cycle_wraps_around(color_registry):
    names = color_registry.names()
    last = color_registry.cycle(names[-1], 1)
    assert last == names[0]
    first_back = color_registry.cycle(names[0], -1)
    assert first_back == names[-1]


def test_color_registry_resolve_unknown_falls_back(color_registry):
    fallback = color_registry.resolve("not_a_color")
    default = color_registry.resolve("default")
    assert fallback == default


# --- GlyphRegistry -------------------------------------------------------


def test_glyph_registry_exposes_canonical_slots(glyph_registry):
    slots = glyph_registry.slots()
    for slot in ("top_left", "bottom_left", "horizontal", "vertical", "bullet_primary", "arrow"):
        assert slot in slots


def test_glyph_registry_cycle_returns_known_choice(glyph_registry):
    choices = glyph_registry.choices("top_left")
    cycled = glyph_registry.cycle("top_left", choices[0], 1)
    assert cycled == choices[1]
    assert glyph_registry.cycle("top_left", choices[-1], 1) == choices[0]


def test_glyph_registry_cycle_preserves_unknown_value(glyph_registry):
    assert glyph_registry.cycle("not_a_slot", "X", 1) == "X"


# --- BannerSettings: color and glyph round-trip --------------------------


def test_settings_round_trip_carries_colors_and_glyphs(registry, color_registry, glyph_registry):
    settings = BannerSettings(
        enabled={"user_host", "rhost"},
        colors={"user_host": "bright_magenta", "rhost": "bright_red"},
        glyphs={"top_left": "┌", "bottom_left": "└", "arrow": "→"},
    )
    block = settings.to_payload_block()
    rebuilt = BannerSettings.from_payload(registry, {"banner": block}, "banner", color_registry, glyph_registry)
    assert rebuilt.enabled == settings.enabled
    assert rebuilt.colors["user_host"] == "bright_magenta"
    assert rebuilt.colors["rhost"] == "bright_red"
    assert rebuilt.glyphs["top_left"] == "┌"
    assert rebuilt.glyphs["arrow"] == "→"


def test_settings_from_payload_ignores_unknown_color_names(registry, color_registry, glyph_registry):
    payload = {"banner": {"enabled": ["user_host"], "colors": {"user_host": "neon_clown"}}}
    settings = BannerSettings.from_payload(registry, payload, "banner", color_registry, glyph_registry)
    assert settings.colors["user_host"] == registry.get("user_host").spec.default_color


def test_settings_from_payload_ignores_unknown_glyph_chars(registry, color_registry, glyph_registry):
    payload = {"banner": {"enabled": ["user_host"], "glyphs": {"top_left": "X"}}}
    settings = BannerSettings.from_payload(registry, payload, "banner", color_registry, glyph_registry)
    assert settings.glyphs["top_left"] == glyph_registry.default("top_left")


def test_settings_cycle_color_uses_registry_order(registry, color_registry):
    settings = BannerSettings.defaults(registry)
    initial = settings.colors["user_host"]
    settings.cycle_color("user_host", color_registry, 1)
    assert settings.colors["user_host"] == color_registry.cycle(initial, 1)


def test_settings_cycle_glyph_uses_registry_order(registry, color_registry, glyph_registry):
    settings = BannerSettings.defaults(registry, color_registry, glyph_registry)
    initial = settings.glyphs["arrow"]
    settings.cycle_glyph("arrow", glyph_registry, 1)
    assert settings.glyphs["arrow"] == glyph_registry.cycle("arrow", initial, 1)


def test_settings_reset_color_and_glyph_for_specific_id(registry, color_registry, glyph_registry):
    settings = BannerSettings.defaults(registry, color_registry, glyph_registry)
    settings.colors["user_host"] = "bright_red"
    settings.glyphs["arrow"] = "→"
    settings.reset_color_for("user_host", registry)
    settings.reset_glyph_for("arrow", glyph_registry)
    assert settings.colors["user_host"] == registry.get("user_host").spec.default_color
    assert settings.glyphs["arrow"] == glyph_registry.default("arrow")


# --- BannerRenderer honours per-segment color and glyph slots ------------


def test_renderer_emits_chosen_color_for_each_segment(registry, color_registry, glyph_registry, neutral_palette):
    palette = ColorPalette(
        reset="<R>", primary="<P>", secondary="<S>", accent="<A>",
        info="<I>", danger="<D>", success="<G>",
    )
    settings = BannerSettings(
        enabled={"user_host"},
        colors={"user_host": "bright_red"},
        glyphs={slot: glyph_registry.default(slot) for slot in glyph_registry.slots()},
    )
    ctx = _make_ctx(palette)
    rendered = BannerRenderer(BannerConfig(), registry, color_registry, glyph_registry).render(settings, ctx)
    assert color_registry.resolve("bright_red") in rendered


def test_renderer_uses_glyph_overrides_in_box(registry, color_registry, glyph_registry, neutral_palette):
    settings = BannerSettings(
        enabled={"user_host"},
        colors={s.spec.id: s.spec.default_color for s in registry.all()},
        glyphs={slot: glyph_registry.default(slot) for slot in glyph_registry.slots()},
    )
    settings.glyphs["top_left"] = "┌"
    settings.glyphs["bottom_left"] = "└"
    settings.glyphs["arrow"] = "→"
    settings.glyphs["bullet_primary"] = "❯"
    ctx = _make_ctx(neutral_palette)
    rendered = BannerRenderer(BannerConfig(), registry, color_registry, glyph_registry).render(settings, ctx)
    plain = strip_ansi(rendered)
    assert plain.startswith("┌")
    assert "└" in plain
    assert "→" in plain
    assert "❯" in plain
    assert "╔" not in plain


def test_render_prompt_honours_payload_colors_and_glyphs():
    payload = {
        "rhost": "10.10.11.5",
        "banner": {
            "enabled": ["user_host", "rhost"],
            "colors": {"user_host": "bright_magenta"},
            "glyphs": {"top_left": "┌", "horizontal": "─", "bottom_left": "└"},
        },
    }
    plain = strip_ansi(render_prompt(payload))
    assert plain.startswith("┌")
    assert "└" in plain
    raw = render_prompt(payload)
    assert ColorRegistry().resolve("bright_magenta") in raw
