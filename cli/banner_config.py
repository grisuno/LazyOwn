"""Configurable Neon Box banner for the LazyOwn interactive shell.

The module exposes a single, self-contained banner subsystem with three
extension axes the operator can tune through a curses wizard or directly
inside ``payload.json``:

1. **Segments** — which pieces of information appear in the prompt
   (``user_host``, ``iface``, ``rhost``, ``domain``, ``cwd``, ``git`` …).
2. **Colors** — a per-segment named ANSI color picked from
   :class:`ColorRegistry`.
3. **Glyphs** — the box-drawing characters, segment markers, arrows and
   prompt characters drawn between values, picked from
   :class:`GlyphRegistry`.

The wizard mirrors Powerlevel10k's flow: three tabs (Segments / Colors /
Glyphs) navigable with ``Tab`` / ``Shift+Tab``, arrow keys plus ``Space``
or ``←/→`` to toggle/cycle, a live preview anchored beneath the body, and
``Enter`` to commit. ``payload.json`` carries the result under the
``banner`` block so it survives shell restarts.

Design (SOLID):

- ``BannerConfig`` centralises every magic constant (keys, key codes,
  palette pair ids, layout, payload field names, cache TTLs).
- ``ColorRegistry`` and ``GlyphRegistry`` are Open/Closed extension
  points: adding a new color name or glyph slot only requires extending
  the preset map.
- ``SegmentSpec`` describes a segment; ``SegmentRenderer`` is the only
  thing that knows how to format a value (Single Responsibility).
- ``SegmentRegistry`` holds the canonical segment set; ``BannerSettings``
  references segments only by id and round-trips through the payload.
- ``BannerRenderer`` orchestrates settings + registries into a final
  ANSI string and never touches curses (Dependency Inversion).
- ``BannerConfigurator`` is the only piece bound to curses; tests can
  drive any renderer behaviour without a TTY.
- ``configure_banner_interactive`` / ``render_prompt`` / ``banner_summary``
  are the public entry points used by ``lazyown.py`` and ``utils.py``.
"""

from __future__ import annotations

import curses
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class BannerConfig:
    """Centralised constants for the banner renderer and configurator."""

    payload_key: str = "banner"
    payload_filename: str = "payload.json"
    version_filename: str = "version.json"

    middle_segment_gap: str = "   "
    fallback_user: str = "user"
    fallback_iface_ip_token: str = "tun"
    fallback_label_lhost: str = "LHOST"
    fallback_label_rhost: str = "RHOST"
    fallback_label_iface: str = "tun0"
    fallback_label_git: str = "git"
    fallback_label_env: str = "env"
    fallback_label_kernel: str = "kernel"
    fallback_label_version: str = "lazyown"
    fallback_label_public_ip: str = "PUB"
    fallback_label_battery: str = "PWR"

    time_format: str = "%H:%M:%S"
    public_ip_cache_seconds: float = 60.0
    public_ip_timeout_seconds: float = 1.5
    public_ip_endpoint: str = "https://api.ipify.org"
    kernel_cache_seconds: float = 600.0
    version_cache_seconds: float = 600.0

    wizard_title: str = "LazyOwn Banner Configurator"
    wizard_subtitle: str = "Powerlevel10k-style segment / color / glyph picker"
    wizard_preview_label: str = "Preview:"
    wizard_footer_segments: str = (
        "[↑/↓] move  [space] toggle  [a/n] all/none  [d] defaults  "
        "[tab] next tab  [enter] save  [esc] cancel"
    )
    wizard_footer_colors: str = (
        "[↑/↓] move  [space/→] next color  [←] prev color  [d] default  "
        "[tab] next tab  [enter] save  [esc] cancel"
    )
    wizard_footer_glyphs: str = (
        "[↑/↓] move  [space/→] next glyph  [←] prev glyph  [d] default  "
        "[tab] next tab  [enter] save  [esc] cancel"
    )
    wizard_padding_x: int = 2
    wizard_min_width: int = 88
    wizard_max_width: int = 132
    wizard_color_swatch_width: int = 12
    wizard_glyph_choices_width: int = 28
    wizard_segment_label_width: int = 16

    color_pair_border: int = 1
    color_pair_title: int = 2
    color_pair_help: int = 3
    color_pair_row: int = 4
    color_pair_selected: int = 5
    color_pair_enabled: int = 6
    color_pair_disabled: int = 7
    color_pair_preview: int = 8
    color_pair_tab_active: int = 9
    color_pair_tab_inactive: int = 10

    color_border_fg: int = curses.COLOR_CYAN
    color_title_fg: int = curses.COLOR_GREEN
    color_help_fg: int = curses.COLOR_YELLOW
    color_row_fg: int = curses.COLOR_WHITE
    color_selected_bg: int = curses.COLOR_BLUE
    color_selected_fg: int = curses.COLOR_WHITE
    color_enabled_fg: int = curses.COLOR_GREEN
    color_disabled_fg: int = curses.COLOR_MAGENTA
    color_preview_fg: int = curses.COLOR_CYAN
    color_tab_active_fg: int = curses.COLOR_BLACK
    color_tab_active_bg: int = curses.COLOR_GREEN
    color_tab_inactive_fg: int = curses.COLOR_WHITE

    key_tab: int = 9
    key_btab: int = 353
    key_enter: int = 10
    key_carriage_return: int = 13
    key_escape: int = 27
    key_ctrl_c: int = 3
    key_space: int = ord(" ")
    key_d_lower: int = ord("d")
    key_a_lower: int = ord("a")
    key_n_lower: int = ord("n")


class ColorRegistry:
    """Named ANSI colors operators can assign to any segment.

    Names are stable identifiers; the underlying escape codes are an
    implementation detail. Cycling through names produces a deterministic
    ordering so the wizard never surprises the operator.
    """

    _PRESETS: dict[str, str] = {
        "default": "\033[97m",
        "white": "\033[37m",
        "bright_white": "\033[97m",
        "cyan": "\033[36m",
        "bright_cyan": "\033[96m",
        "green": "\033[32m",
        "bright_green": "\033[92m",
        "yellow": "\033[33m",
        "bright_yellow": "\033[93m",
        "magenta": "\033[35m",
        "bright_magenta": "\033[95m",
        "red": "\033[31m",
        "bright_red": "\033[91m",
        "blue": "\033[34m",
        "bright_blue": "\033[94m",
    }
    _DEFAULT_NAME: str = "default"

    def names(self) -> list[str]:
        return list(self._PRESETS.keys())

    def has(self, name: str) -> bool:
        return name in self._PRESETS

    def resolve(self, name: str) -> str:
        return self._PRESETS.get(name, self._PRESETS[self._DEFAULT_NAME])

    def cycle(self, current: str, direction: int = 1) -> str:
        names = self.names()
        try:
            idx = names.index(current)
        except ValueError:
            idx = -1 if direction > 0 else 0
        return names[(idx + direction) % len(names)]

    def default_name(self) -> str:
        return self._DEFAULT_NAME


class GlyphRegistry:
    """Glyph slots used by the Neon Box renderer with cyclable choices."""

    _SLOTS: dict[str, list[str]] = {
        "top_left": ["╔", "┌", "┏", "╓", "▛", "╭"],
        "bottom_left": ["╚", "└", "┗", "╙", "▙", "╰"],
        "vertical": ["║", "│", "┃", "▎", "█", "┆"],
        "horizontal": ["═", "─", "━", "▬", "■"],
        "segment_open": ["═[", "─[", "━[", "═{", "═(", " ["],
        "segment_close": ["]", "}", ")"],
        "segment_filler": ["══", "──", "━━", "▬▬", "  "],
        "bottom_filler": ["═════", "─────", "━━━━━", "▬▬▬▬▬", "     "],
        "bullet_primary": ["▸", "▶", "❯", "➤", "►", "•", "★", "✦"],
        "bullet_secondary": ["◆", "◇", "◉", "◎", "✦", "❖", "♦", "▪"],
        "middle_pointer": ["▸", "▶", "❯", "➤", "►", "•"],
        "middle_bullet": ["◆", "◇", "◉", "◎", "✦", "•"],
        "arrow": ["➜", "➤", "❱", "➔", "❯", "→", ">"],
        "prompt_char_user": ["$", "❯", ">", "→", "λ"],
        "prompt_char_root": ["#", "⚡", "λ", "!", "❯"],
    }

    def slots(self) -> list[str]:
        return list(self._SLOTS.keys())

    def choices(self, slot: str) -> list[str]:
        return list(self._SLOTS.get(slot, []))

    def has(self, slot: str) -> bool:
        return slot in self._SLOTS

    def default(self, slot: str) -> str:
        choices = self.choices(slot)
        return choices[0] if choices else ""

    def cycle(self, slot: str, current: str, direction: int = 1) -> str:
        choices = self.choices(slot)
        if not choices:
            return current
        try:
            idx = choices.index(current)
        except ValueError:
            idx = -1 if direction > 0 else 0
        return choices[(idx + direction) % len(choices)]


@dataclass(frozen=True)
class SegmentSpec:
    """Metadata describing a prompt segment available for toggling."""

    id: str
    label: str
    description: str
    group: str
    default_enabled: bool = True
    order: int = 0
    default_color: str = "default"


@dataclass(frozen=True)
class ColorPalette:
    """ANSI escape codes for the box chrome itself.

    The chrome (corners, fillers, brackets, accents) keeps a coherent
    look; only the per-segment *value* color is operator-tunable through
    :class:`ColorRegistry`.
    """

    reset: str
    primary: str
    secondary: str
    accent: str
    info: str
    danger: str
    success: str


@dataclass(frozen=True)
class RenderContext:
    """Pre-resolved data delivered to every :class:`SegmentRenderer`."""

    user: str
    hostname: str
    iface_name: str
    iface_ip: str
    lhost: str
    rhost: str
    domain: str
    cwd: str
    git_dirty: bool
    git_branch: str
    venv_name: str
    now_str: str
    kernel: str
    version: str
    public_ip: str
    battery_or_load: str
    palette: ColorPalette


def _bracketed(label: str, value: str, bullet: str, value_color: str, ctx: RenderContext, glyphs: dict[str, str]) -> str:
    """Render one bracketed top-row segment with the chosen value color."""
    palette = ctx.palette
    label_part = f"{label} " if label else ""
    return (
        f"{palette.primary}{glyphs['segment_open']}{palette.reset} "
        f"{palette.accent}{bullet}{palette.reset} "
        f"{palette.info}{label_part}{value_color}{value}{palette.reset} "
        f"{palette.primary}{glyphs['segment_close']}{palette.reset}"
    )


def _middle(label: str, value: str, value_color: str, ctx: RenderContext, glyphs: dict[str, str]) -> str:
    """Render one middle-row segment with the chosen value color."""
    palette = ctx.palette
    label_part = f"{label}:" if label else ""
    return f"{palette.accent}{glyphs['middle_bullet']}{palette.reset} {value_color}{label_part}{value}{palette.reset}"


class SegmentRenderer(ABC):
    """Contract for a single prompt segment."""

    @property
    @abstractmethod
    def spec(self) -> SegmentSpec: ...

    @abstractmethod
    def render(self, ctx: RenderContext, cfg: BannerConfig, color: str, glyphs: dict[str, str]) -> str: ...


class UserHostSegment(SegmentRenderer):
    spec = SegmentSpec(id="user_host", label="user@host", description="Operator user and hostname", group="top", default_enabled=True, order=0, default_color="bright_green")

    def render(self, ctx, cfg, color, glyphs):
        return _bracketed("", f"{ctx.user}@{ctx.hostname}", glyphs["bullet_primary"], color, ctx, glyphs)


class IfaceSegment(SegmentRenderer):
    spec = SegmentSpec(id="iface", label="iface", description="Local network interface IP (tun0, wlan0, ...)", group="top", default_enabled=True, order=10, default_color="bright_green")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.iface_ip:
            return ""
        return _bracketed(ctx.iface_name or cfg.fallback_label_iface, ctx.iface_ip, glyphs["bullet_secondary"], color, ctx, glyphs)


class LhostSegment(SegmentRenderer):
    spec = SegmentSpec(id="lhost", label="lhost", description="Explicit LHOST from payload.json", group="top", default_enabled=False, order=15, default_color="bright_cyan")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.lhost:
            return ""
        return _bracketed(cfg.fallback_label_lhost, ctx.lhost, glyphs["bullet_secondary"], color, ctx, glyphs)


class RhostSegment(SegmentRenderer):
    spec = SegmentSpec(id="rhost", label="rhost", description="Target RHOST from payload.json", group="top", default_enabled=True, order=20, default_color="bright_red")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.rhost:
            return ""
        return _bracketed(cfg.fallback_label_rhost, ctx.rhost, glyphs["bullet_secondary"], color, ctx, glyphs)


class DomainSegment(SegmentRenderer):
    spec = SegmentSpec(id="domain", label="domain", description="Target domain from payload.json", group="top", default_enabled=True, order=30, default_color="bright_yellow")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.domain:
            return ""
        return _bracketed("", ctx.domain, glyphs["bullet_secondary"], color, ctx, glyphs)


class PublicIpSegment(SegmentRenderer):
    spec = SegmentSpec(id="public_ip", label="public_ip", description="Egress public IP (cached 60s)", group="top", default_enabled=False, order=40, default_color="bright_magenta")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.public_ip:
            return ""
        return _bracketed(cfg.fallback_label_public_ip, ctx.public_ip, glyphs["bullet_secondary"], color, ctx, glyphs)


class CwdSegment(SegmentRenderer):
    spec = SegmentSpec(id="cwd", label="cwd", description="Current working directory", group="middle", default_enabled=True, order=0, default_color="bright_green")

    def render(self, ctx, cfg, color, glyphs):
        palette = ctx.palette
        return f"{palette.accent}{glyphs['middle_pointer']}{palette.reset} {color}{ctx.cwd}{palette.reset}"


class GitSegment(SegmentRenderer):
    spec = SegmentSpec(id="git", label="git", description="Git branch and dirty marker", group="middle", default_enabled=True, order=10, default_color="bright_yellow")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.git_branch:
            return ""
        marker = "✗" if ctx.git_dirty else "✔"
        marker_color = ctx.palette.danger if ctx.git_dirty else ctx.palette.success
        return (
            f"{ctx.palette.accent}{glyphs['middle_bullet']}{ctx.palette.reset} "
            f"{color}{cfg.fallback_label_git}:{marker_color}{marker} {color}{ctx.git_branch}{ctx.palette.reset}"
        )


class VenvSegment(SegmentRenderer):
    spec = SegmentSpec(id="venv", label="venv", description="Active Python virtualenv", group="middle", default_enabled=True, order=20, default_color="bright_blue")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.venv_name:
            return ""
        return _middle(cfg.fallback_label_env, ctx.venv_name, color, ctx, glyphs)


class TimeSegment(SegmentRenderer):
    spec = SegmentSpec(id="time", label="time", description="Local clock HH:MM:SS", group="middle", default_enabled=True, order=30, default_color="bright_cyan")

    def render(self, ctx, cfg, color, glyphs):
        return _middle("", ctx.now_str, color, ctx, glyphs)


class KernelSegment(SegmentRenderer):
    spec = SegmentSpec(id="kernel", label="kernel", description="uname -r kernel release", group="middle", default_enabled=False, order=40, default_color="bright_white")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.kernel:
            return ""
        return _middle(cfg.fallback_label_kernel, ctx.kernel, color, ctx, glyphs)


class VersionSegment(SegmentRenderer):
    spec = SegmentSpec(id="version", label="version", description="LazyOwn version from version.json", group="middle", default_enabled=False, order=50, default_color="bright_blue")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.version:
            return ""
        return _middle(cfg.fallback_label_version, ctx.version, color, ctx, glyphs)


class BatteryLoadSegment(SegmentRenderer):
    spec = SegmentSpec(id="battery_load", label="battery/load", description="Battery % or 1m load average", group="middle", default_enabled=False, order=60, default_color="bright_yellow")

    def render(self, ctx, cfg, color, glyphs):
        if not ctx.battery_or_load:
            return ""
        return _middle(cfg.fallback_label_battery, ctx.battery_or_load, color, ctx, glyphs)


class SegmentRegistry:
    """Open/Closed registry of available prompt segments."""

    def __init__(self) -> None:
        self._segments: dict[str, SegmentRenderer] = {}

    def register(self, segment: SegmentRenderer) -> None:
        self._segments[segment.spec.id] = segment

    def get(self, segment_id: str) -> SegmentRenderer | None:
        return self._segments.get(segment_id)

    def all(self) -> list[SegmentRenderer]:
        return sorted(
            self._segments.values(),
            key=lambda s: (
                0 if s.spec.group == "top" else 1,
                s.spec.order,
                s.spec.id,
            ),
        )

    def by_group(self, group: str) -> list[SegmentRenderer]:
        return [s for s in self.all() if s.spec.group == group]


def build_default_registry() -> SegmentRegistry:
    """Return the registry populated with the canonical segment set."""
    registry = SegmentRegistry()
    for segment in (
        UserHostSegment(),
        IfaceSegment(),
        LhostSegment(),
        RhostSegment(),
        DomainSegment(),
        PublicIpSegment(),
        CwdSegment(),
        GitSegment(),
        VenvSegment(),
        TimeSegment(),
        KernelSegment(),
        VersionSegment(),
        BatteryLoadSegment(),
    ):
        registry.register(segment)
    return registry


@dataclass
class BannerSettings:
    """Mutable banner state: enabled segments + per-segment color + glyph slots."""

    enabled: set[str] = field(default_factory=set)
    colors: dict[str, str] = field(default_factory=dict)
    glyphs: dict[str, str] = field(default_factory=dict)

    @classmethod
    def defaults(
        cls,
        registry: SegmentRegistry,
        color_registry: ColorRegistry | None = None,
        glyph_registry: GlyphRegistry | None = None,
    ) -> "BannerSettings":
        colors_r = color_registry or ColorRegistry()
        glyphs_r = glyph_registry or GlyphRegistry()
        return cls(
            enabled={s.spec.id for s in registry.all() if s.spec.default_enabled},
            colors={s.spec.id: s.spec.default_color for s in registry.all()},
            glyphs={slot: glyphs_r.default(slot) for slot in glyphs_r.slots()},
        )

    @classmethod
    def from_payload(
        cls,
        registry: SegmentRegistry,
        payload: dict | None,
        key: str,
        color_registry: ColorRegistry | None = None,
        glyph_registry: GlyphRegistry | None = None,
    ) -> "BannerSettings":
        colors_r = color_registry or ColorRegistry()
        glyphs_r = glyph_registry or GlyphRegistry()
        defaults = cls.defaults(registry, colors_r, glyphs_r)
        block = (payload or {}).get(key)
        if not isinstance(block, dict):
            return defaults
        enabled_raw = block.get("enabled")
        if isinstance(enabled_raw, list):
            known = {s.spec.id for s in registry.all()}
            enabled = {name for name in enabled_raw if name in known}
        else:
            enabled = set(defaults.enabled)
        colors = dict(defaults.colors)
        colors_raw = block.get("colors")
        if isinstance(colors_raw, dict):
            for sid, cname in colors_raw.items():
                if sid in colors and isinstance(cname, str) and colors_r.has(cname):
                    colors[sid] = cname
        glyphs = dict(defaults.glyphs)
        glyphs_raw = block.get("glyphs")
        if isinstance(glyphs_raw, dict):
            for slot, char in glyphs_raw.items():
                if slot in glyphs and isinstance(char, str) and char in glyphs_r.choices(slot):
                    glyphs[slot] = char
        return cls(enabled=enabled, colors=colors, glyphs=glyphs)

    def is_enabled(self, segment_id: str) -> bool:
        return segment_id in self.enabled

    def toggle(self, segment_id: str) -> None:
        if segment_id in self.enabled:
            self.enabled.discard(segment_id)
        else:
            self.enabled.add(segment_id)

    def enable_all(self, registry: SegmentRegistry) -> None:
        self.enabled = {s.spec.id for s in registry.all()}

    def disable_all(self) -> None:
        self.enabled = set()

    def reset_segments(self, registry: SegmentRegistry) -> None:
        self.enabled = {s.spec.id for s in registry.all() if s.spec.default_enabled}

    def reset_colors(self, registry: SegmentRegistry) -> None:
        self.colors = {s.spec.id: s.spec.default_color for s in registry.all()}

    def reset_color_for(self, segment_id: str, registry: SegmentRegistry) -> None:
        seg = registry.get(segment_id)
        if seg is not None:
            self.colors[segment_id] = seg.spec.default_color

    def reset_glyphs(self, glyph_registry: GlyphRegistry) -> None:
        self.glyphs = {slot: glyph_registry.default(slot) for slot in glyph_registry.slots()}

    def reset_glyph_for(self, slot: str, glyph_registry: GlyphRegistry) -> None:
        if slot in self.glyphs:
            self.glyphs[slot] = glyph_registry.default(slot)

    def cycle_color(self, segment_id: str, color_registry: ColorRegistry, direction: int = 1) -> None:
        current = self.colors.get(segment_id, color_registry.default_name())
        self.colors[segment_id] = color_registry.cycle(current, direction)

    def cycle_glyph(self, slot: str, glyph_registry: GlyphRegistry, direction: int = 1) -> None:
        current = self.glyphs.get(slot, glyph_registry.default(slot))
        self.glyphs[slot] = glyph_registry.cycle(slot, current, direction)

    def to_payload_block(self) -> dict:
        return {
            "enabled": sorted(self.enabled),
            "colors": dict(self.colors),
            "glyphs": dict(self.glyphs),
        }


class ContextResolver:
    """Resolve a :class:`RenderContext` once per prompt render, with caches."""

    _public_ip_cache: tuple[float, str] = (0.0, "")
    _kernel_cache: tuple[float, str] = (0.0, "")
    _version_cache: tuple[float, str] = (0.0, "")

    def __init__(self, cfg: BannerConfig, palette: ColorPalette) -> None:
        self._cfg = cfg
        self._palette = palette

    def resolve(self, payload: dict | None, network: dict[str, str] | None = None) -> RenderContext:
        cfg = self._cfg
        payload = payload or {}
        network = network if network is not None else _read_network_info()
        user = "root" if os.geteuid() == 0 else (os.getenv("USER") or cfg.fallback_user)
        hostname = socket.gethostname()
        iface_name, iface_ip = _select_iface(network, cfg.fallback_iface_ip_token)
        return RenderContext(
            user=user,
            hostname=hostname,
            iface_name=iface_name,
            iface_ip=iface_ip,
            lhost=str(payload.get("lhost") or ""),
            rhost=str(payload.get("rhost") or ""),
            domain=str(payload.get("domain") or ""),
            cwd=os.getcwd(),
            git_dirty=_git_dirty(),
            git_branch=_git_branch(),
            venv_name=_venv_name(),
            now_str=time.strftime(cfg.time_format),
            kernel=self._kernel(),
            version=self._version(),
            public_ip=self._public_ip(payload),
            battery_or_load=_battery_or_load(),
            palette=self._palette,
        )

    def _public_ip(self, payload: dict) -> str:
        cfg = self._cfg
        block = payload.get(cfg.payload_key, {}) if isinstance(payload, dict) else {}
        if isinstance(block, dict) and block.get("enable_public_ip", True) is False:
            return ""
        cached_at, value = ContextResolver._public_ip_cache
        if time.time() - cached_at < cfg.public_ip_cache_seconds and value:
            return value
        try:
            with urllib.request.urlopen(cfg.public_ip_endpoint, timeout=cfg.public_ip_timeout_seconds) as resp:
                text = resp.read().decode("utf-8", "ignore").strip()
                if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", text) or ":" in text:
                    ContextResolver._public_ip_cache = (time.time(), text)
                    return text
        except (OSError, ValueError, TimeoutError):
            pass
        ContextResolver._public_ip_cache = (time.time(), value)
        return value

    def _kernel(self) -> str:
        cached_at, value = ContextResolver._kernel_cache
        if time.time() - cached_at < self._cfg.kernel_cache_seconds and value:
            return value
        try:
            out = subprocess.run(["uname", "-r"], capture_output=True, text=True, timeout=1.0)
            text = (out.stdout or "").strip()
        except (FileNotFoundError, subprocess.SubprocessError):
            text = ""
        ContextResolver._kernel_cache = (time.time(), text)
        return text

    def _version(self) -> str:
        cached_at, value = ContextResolver._version_cache
        if time.time() - cached_at < self._cfg.version_cache_seconds and value:
            return value
        text = ""
        try:
            path = Path(self._cfg.version_filename)
            if path.exists():
                with path.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
                if isinstance(data, dict) and isinstance(data.get("version"), str):
                    text = data["version"]
        except (OSError, json.JSONDecodeError):
            text = ""
        ContextResolver._version_cache = (time.time(), text)
        return text


def _read_network_info() -> dict[str, str]:
    """Return ``{interface: ip}`` for every globally-scoped IPv4 link."""
    cmd = (
        "ip a show scope global | "
        "awk '/^[0-9]+:/ { sub(/:/,\"\",$2); iface=$2 } "
        "/^[[:space:]]*inet / { split($2, a, \"/\"); print iface \" \" a[1] }'"
    )
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=1.5)
    except (FileNotFoundError, subprocess.SubprocessError):
        return {}
    info: dict[str, str] = {}
    for line in (result.stdout or "").splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            info[parts[0]] = parts[1]
    return info


def _select_iface(network: dict[str, str], preferred: str) -> tuple[str, str]:
    for iface, ip in network.items():
        if preferred in iface:
            return iface, ip
    if network:
        iface = next(iter(network))
        return iface, network[iface]
    return "", ""


def _git_branch() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
            timeout=1.0,
        )
        return out.decode("utf-8", "ignore").strip()
    except (FileNotFoundError, subprocess.SubprocessError, subprocess.TimeoutExpired):
        return ""


def _git_dirty() -> bool:
    try:
        modified = subprocess.call(["git", "diff", "--quiet"], stderr=subprocess.DEVNULL, timeout=1.0)
        staged = subprocess.call(["git", "diff", "--staged", "--quiet"], stderr=subprocess.DEVNULL, timeout=1.0)
        return modified != 0 or staged != 0
    except (FileNotFoundError, subprocess.SubprocessError, subprocess.TimeoutExpired):
        return False


def _venv_name() -> str:
    if "VIRTUAL_ENV" in os.environ:
        return os.path.basename(os.environ["VIRTUAL_ENV"])
    return ""


def _battery_or_load() -> str:
    try:
        battery_dirs = sorted(Path("/sys/class/power_supply").glob("BAT*"))
    except OSError:
        battery_dirs = []
    for battery in battery_dirs:
        capacity = battery / "capacity"
        try:
            return f"{int(capacity.read_text().strip())}%"
        except (OSError, ValueError):
            continue
    try:
        with open("/proc/loadavg", "r", encoding="utf-8") as fh:
            first = fh.read().split()[0]
            return first
    except (OSError, IndexError):
        return ""


def default_palette() -> ColorPalette:
    """Box-chrome palette used around segment values."""
    return ColorPalette(
        reset="\033[0m",
        primary="\033[96m",
        secondary="\033[94m",
        accent="\033[95m",
        info="\033[97m",
        danger="\033[91m",
        success="\033[92m",
    )


_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


def strip_ansi(value: str) -> str:
    return _ANSI_RE.sub("", value)


class BannerRenderer:
    """Pure renderer of the three-line Neon Box prompt."""

    def __init__(
        self,
        config: BannerConfig,
        registry: SegmentRegistry,
        color_registry: ColorRegistry | None = None,
        glyph_registry: GlyphRegistry | None = None,
    ) -> None:
        self._cfg = config
        self._registry = registry
        self._colors = color_registry or ColorRegistry()
        self._glyph_registry = glyph_registry or GlyphRegistry()

    def render(self, settings: BannerSettings, ctx: RenderContext) -> str:
        glyphs = self._merged_glyphs(settings)
        top_pieces = self._render_group(settings, ctx, "top", glyphs)
        middle_pieces = self._render_group(settings, ctx, "middle", glyphs)
        top_line = self._build_top(top_pieces, ctx.palette, glyphs)
        middle_line = self._build_middle(middle_pieces, ctx.palette, glyphs)
        bottom_line = self._build_bottom(ctx.palette, glyphs)
        return f"{top_line}\n{middle_line}\n{bottom_line}"

    def _merged_glyphs(self, settings: BannerSettings) -> dict[str, str]:
        merged: dict[str, str] = {slot: self._glyph_registry.default(slot) for slot in self._glyph_registry.slots()}
        for slot, char in settings.glyphs.items():
            if slot in merged and isinstance(char, str) and char:
                merged[slot] = char
        return merged

    def _render_group(self, settings: BannerSettings, ctx: RenderContext, group: str, glyphs: dict[str, str]) -> list[str]:
        rendered: list[str] = []
        for segment in self._registry.by_group(group):
            if not settings.is_enabled(segment.spec.id):
                continue
            color_name = settings.colors.get(segment.spec.id, segment.spec.default_color)
            color = self._colors.resolve(color_name)
            fragment = segment.render(ctx, self._cfg, color, glyphs)
            if fragment:
                rendered.append(fragment)
        return rendered

    def _build_top(self, pieces: list[str], palette: ColorPalette, glyphs: dict[str, str]) -> str:
        head = f"{palette.primary}{glyphs['top_left']}{glyphs['horizontal']}{palette.reset}"
        if not pieces:
            return head
        join = f"{palette.primary}{glyphs['segment_filler']}{palette.reset}"
        return head + join.join(pieces)

    def _build_middle(self, pieces: list[str], palette: ColorPalette, glyphs: dict[str, str]) -> str:
        head = f"{palette.primary}{glyphs['vertical']}{palette.reset}  "
        if not pieces:
            return head
        return head + self._cfg.middle_segment_gap.join(pieces)

    def _build_bottom(self, palette: ColorPalette, glyphs: dict[str, str]) -> str:
        is_root = os.geteuid() == 0
        prompt_char = glyphs["prompt_char_root"] if is_root else glyphs["prompt_char_user"]
        char_color = palette.danger if is_root else palette.success
        return (
            f"{palette.primary}{glyphs['bottom_left']}{glyphs['bottom_filler']}{palette.reset}"
            f"{palette.accent}{glyphs['arrow']}{palette.reset} {char_color}{prompt_char}{palette.reset} "
        )


class _WizardTab:
    """Identifiers for the three wizard tabs."""

    SEGMENTS = "segments"
    COLORS = "colors"
    GLYPHS = "glyphs"


class BannerConfigurator:
    """Curses-driven p10k-style wizard editing segments, colors and glyphs."""

    _TAB_ORDER = (_WizardTab.SEGMENTS, _WizardTab.COLORS, _WizardTab.GLYPHS)
    _TAB_TITLES = {
        _WizardTab.SEGMENTS: "Segments",
        _WizardTab.COLORS: "Colors",
        _WizardTab.GLYPHS: "Glyphs",
    }

    def __init__(
        self,
        config: BannerConfig,
        registry: SegmentRegistry,
        color_registry: ColorRegistry,
        glyph_registry: GlyphRegistry,
        renderer: BannerRenderer,
        ctx: RenderContext,
        initial: BannerSettings,
    ) -> None:
        self._cfg = config
        self._registry = registry
        self._colors = color_registry
        self._glyphs = glyph_registry
        self._renderer = renderer
        self._ctx = ctx
        self._settings = BannerSettings(
            enabled=set(initial.enabled),
            colors=dict(initial.colors),
            glyphs=dict(initial.glyphs),
        )
        self._current_tab = _WizardTab.SEGMENTS
        self._cursor: dict[str, int] = {tab: 0 for tab in self._TAB_ORDER}

    def run(self) -> BannerSettings | None:
        if not self._tty_available():
            return None
        try:
            return curses.wrapper(self._loop)
        except curses.error:
            return None
        except KeyboardInterrupt:
            return None

    @staticmethod
    def _tty_available() -> bool:
        return (
            sys.stdin.isatty()
            and sys.stdout.isatty()
            and os.environ.get("TERM", "") not in {"", "dumb"}
        )

    def _loop(self, stdscr: "curses._CursesWindow") -> BannerSettings | None:
        curses.curs_set(0)
        stdscr.keypad(True)
        self._init_colors()
        while True:
            rows = self._rows_for(self._current_tab)
            cursor = self._cursor[self._current_tab]
            if rows:
                cursor = max(0, min(cursor, len(rows) - 1))
                self._cursor[self._current_tab] = cursor
            self._render(stdscr, rows, cursor)
            key = stdscr.getch()
            if key in (self._cfg.key_escape, self._cfg.key_ctrl_c):
                return None
            if key in (self._cfg.key_enter, self._cfg.key_carriage_return, curses.KEY_ENTER):
                return self._settings
            if key == self._cfg.key_tab:
                self._cycle_tab(1)
                continue
            if key == self._cfg.key_btab or key == curses.KEY_BTAB:
                self._cycle_tab(-1)
                continue
            if not rows:
                continue
            if key == curses.KEY_UP:
                self._cursor[self._current_tab] = (cursor - 1) % len(rows)
            elif key == curses.KEY_DOWN:
                self._cursor[self._current_tab] = (cursor + 1) % len(rows)
            elif key == curses.KEY_HOME:
                self._cursor[self._current_tab] = 0
            elif key == curses.KEY_END:
                self._cursor[self._current_tab] = len(rows) - 1
            else:
                self._dispatch_action(key, rows, cursor)

    def _cycle_tab(self, direction: int) -> None:
        idx = self._TAB_ORDER.index(self._current_tab)
        self._current_tab = self._TAB_ORDER[(idx + direction) % len(self._TAB_ORDER)]

    def _rows_for(self, tab: str) -> list:
        if tab == _WizardTab.SEGMENTS:
            return self._registry.all()
        if tab == _WizardTab.COLORS:
            return self._registry.all()
        if tab == _WizardTab.GLYPHS:
            return self._glyphs.slots()
        return []

    def _dispatch_action(self, key: int, rows: list, cursor: int) -> None:
        cfg = self._cfg
        tab = self._current_tab
        if tab == _WizardTab.SEGMENTS:
            segment = rows[cursor]
            if key == cfg.key_space:
                self._settings.toggle(segment.spec.id)
            elif key == cfg.key_a_lower:
                self._settings.enable_all(self._registry)
            elif key == cfg.key_n_lower:
                self._settings.disable_all()
            elif key == cfg.key_d_lower:
                self._settings.reset_segments(self._registry)
        elif tab == _WizardTab.COLORS:
            segment = rows[cursor]
            if key in (cfg.key_space, curses.KEY_RIGHT):
                self._settings.cycle_color(segment.spec.id, self._colors, 1)
            elif key == curses.KEY_LEFT:
                self._settings.cycle_color(segment.spec.id, self._colors, -1)
            elif key == cfg.key_d_lower:
                self._settings.reset_color_for(segment.spec.id, self._registry)
        elif tab == _WizardTab.GLYPHS:
            slot = rows[cursor]
            if key in (cfg.key_space, curses.KEY_RIGHT):
                self._settings.cycle_glyph(slot, self._glyphs, 1)
            elif key == curses.KEY_LEFT:
                self._settings.cycle_glyph(slot, self._glyphs, -1)
            elif key == cfg.key_d_lower:
                self._settings.reset_glyph_for(slot, self._glyphs)

    def _init_colors(self) -> None:
        if not curses.has_colors():
            return
        try:
            curses.start_color()
            curses.use_default_colors()
        except curses.error:
            return
        default_bg = -1
        pairs = (
            (self._cfg.color_pair_border, self._cfg.color_border_fg, default_bg),
            (self._cfg.color_pair_title, self._cfg.color_title_fg, default_bg),
            (self._cfg.color_pair_help, self._cfg.color_help_fg, default_bg),
            (self._cfg.color_pair_row, self._cfg.color_row_fg, default_bg),
            (self._cfg.color_pair_selected, self._cfg.color_selected_fg, self._cfg.color_selected_bg),
            (self._cfg.color_pair_enabled, self._cfg.color_enabled_fg, default_bg),
            (self._cfg.color_pair_disabled, self._cfg.color_disabled_fg, default_bg),
            (self._cfg.color_pair_preview, self._cfg.color_preview_fg, default_bg),
            (self._cfg.color_pair_tab_active, self._cfg.color_tab_active_fg, self._cfg.color_tab_active_bg),
            (self._cfg.color_pair_tab_inactive, self._cfg.color_tab_inactive_fg, default_bg),
        )
        for pair, fg, bg in pairs:
            try:
                curses.init_pair(pair, fg, bg)
            except curses.error:
                continue

    def _render(self, stdscr: "curses._CursesWindow", rows: list, cursor: int) -> None:
        cfg = self._cfg
        max_y, max_x = stdscr.getmaxyx()
        width = max(cfg.wizard_min_width, min(cfg.wizard_max_width, max_x))
        preview_text = strip_ansi(self._renderer.render(self._settings, self._ctx)).splitlines()
        body_rows = len(rows) if rows else 1
        height = min(max_y, body_rows + len(preview_text) + 9)
        top = 0
        left = max(0, (max_x - width) // 2)
        stdscr.erase()
        self._draw_frame(stdscr, top, left, height, width)
        self._draw_header(stdscr, top, left, width)
        self._draw_tabs(stdscr, top + 3, left, width)
        body_top = top + 5
        if self._current_tab == _WizardTab.SEGMENTS:
            self._draw_segments(stdscr, body_top, left, width, rows, cursor)
        elif self._current_tab == _WizardTab.COLORS:
            self._draw_colors(stdscr, body_top, left, width, rows, cursor)
        elif self._current_tab == _WizardTab.GLYPHS:
            self._draw_glyphs(stdscr, body_top, left, width, rows, cursor)
        preview_top = body_top + body_rows + 1
        self._draw_preview(stdscr, preview_top, left, width, preview_text)
        self._draw_footer(stdscr, top + height - 2, left, width)
        stdscr.refresh()

    def _draw_frame(self, stdscr, top: int, left: int, height: int, width: int) -> None:
        cfg = self._cfg
        attr = self._color(cfg.color_pair_border)
        horizontal = "═" * (width - 2)
        try:
            stdscr.addnstr(top, left, "╔" + horizontal + "╗", width, attr)
            for y in range(top + 1, top + height - 1):
                stdscr.addnstr(y, left, "║", 1, attr)
                stdscr.addnstr(y, left + width - 1, "║", 1, attr)
            stdscr.addnstr(top + 2, left, "╠" + horizontal + "╣", width, attr)
            stdscr.addnstr(top + height - 1, left, "╚" + horizontal + "╝", width, attr)
        except curses.error:
            pass

    def _draw_header(self, stdscr, top: int, left: int, width: int) -> None:
        cfg = self._cfg
        title_attr = self._color(cfg.color_pair_title) | curses.A_BOLD
        sub_attr = self._color(cfg.color_pair_help)
        try:
            stdscr.addnstr(top + 1, left + cfg.wizard_padding_x, cfg.wizard_title, width - cfg.wizard_padding_x * 2, title_attr)
            subtitle_x = left + width - len(cfg.wizard_subtitle) - cfg.wizard_padding_x
            stdscr.addnstr(top + 1, max(subtitle_x, left + cfg.wizard_padding_x + len(cfg.wizard_title) + 2), cfg.wizard_subtitle, width - cfg.wizard_padding_x * 2, sub_attr)
        except curses.error:
            pass

    def _draw_tabs(self, stdscr, row_y: int, left: int, width: int) -> None:
        cfg = self._cfg
        x = left + cfg.wizard_padding_x
        for tab in self._TAB_ORDER:
            title = self._TAB_TITLES[tab]
            label = f"  {title}  "
            attr = (
                self._color(cfg.color_pair_tab_active) | curses.A_BOLD
                if tab == self._current_tab
                else self._color(cfg.color_pair_tab_inactive)
            )
            try:
                stdscr.addnstr(row_y, x, label, len(label), attr)
            except curses.error:
                return
            x += len(label) + 1

    def _draw_segments(self, stdscr, top: int, left: int, width: int, rows: list, cursor: int) -> None:
        cfg = self._cfg
        for index, segment in enumerate(rows):
            row_y = top + index
            is_cursor = index == cursor
            is_enabled = self._settings.is_enabled(segment.spec.id)
            box = "[x]" if is_enabled else "[ ]"
            attr = (
                self._color(cfg.color_pair_selected)
                if is_cursor
                else (self._color(cfg.color_pair_enabled) if is_enabled else self._color(cfg.color_pair_disabled))
            )
            pointer = "▶" if is_cursor else " "
            label = segment.spec.label.ljust(cfg.wizard_segment_label_width)
            text = f" {pointer} {box} {label} {segment.spec.description}"
            self._addrow(stdscr, row_y, left, width, text, attr)

    def _draw_colors(self, stdscr, top: int, left: int, width: int, rows: list, cursor: int) -> None:
        cfg = self._cfg
        for index, segment in enumerate(rows):
            row_y = top + index
            is_cursor = index == cursor
            color_name = self._settings.colors.get(segment.spec.id, segment.spec.default_color)
            attr = self._color(cfg.color_pair_selected) if is_cursor else self._color(cfg.color_pair_row)
            pointer = "▶" if is_cursor else " "
            label = segment.spec.label.ljust(cfg.wizard_segment_label_width)
            swatch_text = color_name.ljust(cfg.wizard_color_swatch_width)
            text = f" {pointer}  {label} {swatch_text}  ({color_name})"
            self._addrow(stdscr, row_y, left, width, text, attr)

    def _draw_glyphs(self, stdscr, top: int, left: int, width: int, rows: list, cursor: int) -> None:
        cfg = self._cfg
        for index, slot in enumerate(rows):
            row_y = top + index
            is_cursor = index == cursor
            current = self._settings.glyphs.get(slot, self._glyphs.default(slot))
            choices = self._glyphs.choices(slot)
            others = " ".join(c for c in choices if c != current)[: cfg.wizard_glyph_choices_width]
            attr = self._color(cfg.color_pair_selected) if is_cursor else self._color(cfg.color_pair_row)
            pointer = "▶" if is_cursor else " "
            label = slot.ljust(cfg.wizard_segment_label_width)
            text = f" {pointer}  {label}  current: {current}    others: {others}"
            self._addrow(stdscr, row_y, left, width, text, attr)

    def _addrow(self, stdscr, row_y: int, left: int, width: int, text: str, attr: int) -> None:
        cfg = self._cfg
        usable = width - cfg.wizard_padding_x * 2
        try:
            stdscr.addnstr(row_y, left + cfg.wizard_padding_x, " " * usable, usable, attr)
            stdscr.addnstr(row_y, left + cfg.wizard_padding_x, text, usable, attr)
        except curses.error:
            pass

    def _draw_preview(self, stdscr, top: int, left: int, width: int, lines: list[str]) -> None:
        cfg = self._cfg
        label_attr = self._color(cfg.color_pair_title) | curses.A_BOLD
        preview_attr = self._color(cfg.color_pair_preview)
        usable = width - cfg.wizard_padding_x * 2
        try:
            stdscr.addnstr(top, left + cfg.wizard_padding_x, cfg.wizard_preview_label, usable, label_attr)
            for offset, line in enumerate(lines, 1):
                stdscr.addnstr(top + offset, left + cfg.wizard_padding_x, line, usable, preview_attr)
        except curses.error:
            pass

    def _draw_footer(self, stdscr, row_y: int, left: int, width: int) -> None:
        cfg = self._cfg
        attr = self._color(cfg.color_pair_help)
        usable = width - cfg.wizard_padding_x * 2
        footer = {
            _WizardTab.SEGMENTS: cfg.wizard_footer_segments,
            _WizardTab.COLORS: cfg.wizard_footer_colors,
            _WizardTab.GLYPHS: cfg.wizard_footer_glyphs,
        }[self._current_tab]
        try:
            stdscr.addnstr(row_y, left + cfg.wizard_padding_x, footer, usable, attr)
        except curses.error:
            pass

    def _color(self, pair: int) -> int:
        if not curses.has_colors():
            return curses.A_NORMAL
        try:
            return curses.color_pair(pair)
        except curses.error:
            return curses.A_NORMAL


def render_prompt(payload: dict | None, config: BannerConfig | None = None) -> str:
    """Render the Neon Box prompt from a payload dictionary.

    Reads the operator's segment, color and glyph selection from
    ``payload[banner]`` and walks the canonical registry. Segments whose
    underlying value cannot be resolved (no git, no venv, no network) drop
    silently so the prompt never shows empty brackets.
    """
    cfg = config or BannerConfig()
    registry = build_default_registry()
    colors = ColorRegistry()
    glyphs = GlyphRegistry()
    settings = BannerSettings.from_payload(registry, payload, cfg.payload_key, colors, glyphs)
    ctx = ContextResolver(cfg, default_palette()).resolve(payload)
    return BannerRenderer(cfg, registry, colors, glyphs).render(settings, ctx)


def configure_banner_interactive(
    payload: dict | None,
    config: BannerConfig | None = None,
) -> BannerSettings | None:
    """Open the multi-tab curses wizard and return updated settings on save.

    Returns ``None`` when the operator cancels or the environment cannot
    host a curses session. Callers persist the returned
    :class:`BannerSettings` through ``BannerSettings.to_payload_block``.
    """
    cfg = config or BannerConfig()
    registry = build_default_registry()
    colors = ColorRegistry()
    glyphs = GlyphRegistry()
    settings = BannerSettings.from_payload(registry, payload, cfg.payload_key, colors, glyphs)
    ctx = ContextResolver(cfg, default_palette()).resolve(payload)
    renderer = BannerRenderer(cfg, registry, colors, glyphs)
    return BannerConfigurator(cfg, registry, colors, glyphs, renderer, ctx, settings).run()


def banner_summary(settings: BannerSettings, registry: SegmentRegistry | None = None) -> str:
    """Return a single-line summary listing enabled segment ids."""
    registry = registry or build_default_registry()
    enabled = sorted(s.spec.id for s in registry.all() if settings.is_enabled(s.spec.id))
    return ", ".join(enabled) if enabled else "<none>"


__all__ = [
    "BannerConfig",
    "BannerConfigurator",
    "BannerRenderer",
    "BannerSettings",
    "BatteryLoadSegment",
    "ColorPalette",
    "ColorRegistry",
    "ContextResolver",
    "CwdSegment",
    "DomainSegment",
    "GitSegment",
    "GlyphRegistry",
    "IfaceSegment",
    "KernelSegment",
    "LhostSegment",
    "PublicIpSegment",
    "RenderContext",
    "RhostSegment",
    "SegmentRegistry",
    "SegmentRenderer",
    "SegmentSpec",
    "TimeSegment",
    "UserHostSegment",
    "VenvSegment",
    "VersionSegment",
    "banner_summary",
    "build_default_registry",
    "configure_banner_interactive",
    "default_palette",
    "render_prompt",
    "strip_ansi",
]
