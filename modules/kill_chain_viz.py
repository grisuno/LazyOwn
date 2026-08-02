"""SVG / HTML kill-chain visualizer — generates standalone HTML with embedded SVG.

Reads ``modules.killchain.KillChain`` as the single source of truth.
"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import Any

from modules.killchain import KillChain as _KC

_LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(Path(__file__).resolve().parent.parent)))
SESSIONS_DIR = _LAZYOWN_DIR / "sessions"


def _load_phases(sessions: Path) -> list[dict[str, Any]]:
    """Return a list of phase dicts suitable for SVG/HTML rendering."""
    wm_path = sessions / "world_model.json"
    try:
        progress = _KC.get_progress(world_model_path=wm_path)
    except Exception:
        progress = _KC.get_progress(world_model_path=wm_path)
    return [
        {"id": p.key, "label": p.label, "color": p.color, "status": p.status}
        for p in progress
    ]


def _read_target() -> str:
    try:
        return json.loads((_LAZYOWN_DIR / "payload.json").read_text(encoding="utf-8"))["rhost"]
    except Exception:
        return "unknown"


def _build_svg(phases: list[dict[str, Any]]) -> str:
    num = len(phases)
    total_w = max(900, num * 100 + 40)
    bw = (total_w - 40) / num - 8
    rects = []
    texts = []
    for i, ph in enumerate(phases):
        x = 20 + i * ((total_w - 40) / num)
        y = 30
        opacity = 1.0 if ph["status"] in ("active", "done") else 0.3
        stroke = "#3fb950" if ph["status"] == "done" else ("#58a6ff" if ph["status"] == "active" else "#30363d")
        fill_opacity = 0.15 if ph["status"] == "active" else (0.25 if ph["status"] == "done" else 0.05)
        glow = ' filter="url(#glow)"' if ph["status"] == "active" else ""
        sw = 2.5 if ph["status"] == "active" else 1
        rects.append(f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="60" rx="4" fill="{ph["color"]}" fill-opacity="{fill_opacity}" stroke="{stroke}" stroke-width="{sw}"{glow}/>')
        txt_color = ph["color"] if ph["status"] in ("active", "done") else "#484f58"
        texts.append(f'<text x="{x + bw/2:.0f}" y="{y + 22}" text-anchor="middle" fill="{txt_color}" font-family="sans-serif" font-size="11" font-weight="bold" opacity="{opacity}">{ph["label"]}</text>')
        status_text = "DONE" if ph["status"] == "done" else ("ACTIVE" if ph["status"] == "active" else "PENDING")
        texts.append(f'<text x="{x + bw/2:.0f}" y="{y + 44}" text-anchor="middle" fill="{"#c9d1d9" if ph["status"] in ("active", "done") else "#484f58"}" font-family="sans-serif" font-size="9" opacity="{opacity}">{status_text}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} 120" width="{total_w}" height="120">
<defs><filter id="glow"><feGaussianBlur stdDeviation="3"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0d1117"/><stop offset="100%" stop-color="#161b22"/></linearGradient></defs>
<rect width="100%" height="100%" fill="url(#bg)" rx="8"/>
{"".join(rects)}
{"".join(texts)}
<text x="{total_w-20}" y="110" text-anchor="end" fill="#484f58" font-family="monospace" font-size="9">LazyOwn Kill-Chain</text>
</svg>"""


def generate_html(target: str = "", sessions: Path | None = None) -> str:
    sessions = sessions or SESSIONS_DIR
    phases = _load_phases(sessions)
    svg = _build_svg(phases)
    target = target or _read_target()
    now = datetime.datetime.now(datetime.UTC).isoformat()

    phase_cards = []
    for ph in phases:
        cls = "active" if ph["status"] == "active" else ("complete" if ph["status"] == "done" else "")
        phase_cards.append(f'<div class="phase-card {cls}"><div class="phase-label" style="color:{ph["color"]}">{ph["label"]}</div><div class="phase-status">{ph["status"].upper()}</div></div>')

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LazyOwn Kill-Chain — {target}</title><style>
:root{{--bg:#0d1117;--fg:#c9d1d9;--accent:#58a6ff;--border:#30363d;--card:#161b22}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:var(--bg);color:var(--fg);font-family:system-ui,sans-serif;padding:2rem}}
h1{{color:var(--accent);margin-bottom:1rem}}.svg-container{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem}}.legend{{display:flex;gap:1.5rem;margin:1rem 0;font-size:.85rem}}.legend-dot{{width:12px;height:12px;border-radius:3px;display:inline-block;margin-right:.5rem}}
.phase-detail{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.5rem;margin-top:1rem}}.phase-card{{background:var(--card);border:1px solid var(--border);border-radius:4px;padding:.8rem}}.phase-card.active{{border-color:var(--accent)}}.phase-card.complete{{border-color:#3fb950}}.phase-label{{font-weight:bold}}.phase-status{{font-size:.8rem;margin-top:.3rem}}
</style></head><body>
<h1>LazyOwn Kill-Chain: {target}</h1>
<p style="color:#484f58;margin-bottom:1rem">Generated: {now}</p>
<div class="svg-container">{svg}</div>
<div class="legend">
<div><span class="legend-dot" style="background:#3fb950"></span>Complete</div>
<div><span class="legend-dot" style="background:#58a6ff"></span>Active</div>
<div><span class="legend-dot" style="background:#30363d"></span>Pending</div>
</div>
<div class="phase-detail">{"".join(phase_cards)}</div>
<p style="color:#484f58;margin-top:2rem;font-size:.8rem">LazyOwn RedTeam Framework</p>
</body></html>"""


def generate_svg(target: str = "", sessions: Path | None = None) -> str:
    return _build_svg(_load_phases(sessions or SESSIONS_DIR))


__all__ = ["generate_html", "generate_svg"]
