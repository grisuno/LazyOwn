"""LazyPoophish: phishing fallback delivery for the LazyOwn autonomous loop.

When the loop finishes without a foothold (no access token beyond ``none``
in the fact store), this module stages a client-subject delivery as the
next move: it launches a campaign through
:class:`modules.phishing_orchestrator.PhishingOrchestrator`, optionally
rewrites the lure link through :mod:`modules.lazyshortener`, and records
the handoff plus URLs into ``sessions/phishing_fallback_<campaign>.json``.
Sending real email only happens when SMTP credentials already live in
``payload.json``; otherwise the campaign stays offline (preview emails
only), so the fallback is safe by default.

>>> from modules import lazypoophish
>>> lazypoophish.MODES
('credential_harvest', 'payload_delivery', 'callback_beacon')
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path("sessions")
FALLBACK_ARTIFACT_PREFIX = "phishing_fallback_"
FALLBACK_ACCESS_VALUES = ("none", "")
DEFAULT_TEMPLATE = "microsoft_365_login"
DEFAULT_SHORTENER_PROVIDER = "isgd"

MODES = ("credential_harvest", "payload_delivery", "callback_beacon")


def fresh_access_token(target: str) -> str:
    """Return the current access level token for a target.

    Args:
        target: Engaged host address (empty disables resolution).

    Returns:
        Access string such as ``none``, ``shell``, ``root``; ``none``
        when facts are unavailable or the host is unknown.
    """
    try:
        from modules.chain_tokens import build_tokens

        return str(build_tokens(target, {}).get("access", "") or "none")
    except Exception:
        return "none"


def fallback_ready(target: str) -> bool:
    """Return True when the target still lacks a foothold.

    Args:
        target: Engaged host address.

    Returns:
        True when the fact-store access level is absent or ``none``;
        False once any sessionAccessType exists.
    """
    try:
        from modules.chain_tokens import build_tokens

        access = str(build_tokens(target, {}).get("access", "") or "")
    except Exception:
        access = ""
    return access in FALLBACK_ACCESS_VALUES


def run_fallback(
    target: str,
    params: dict[str, Any] | None = None,
    template: str = DEFAULT_TEMPLATE,
    mode: str = MODES[0],
    targets_file: str = "",
    provider: str = DEFAULT_SHORTENER_PROVIDER,
    shorten: bool = True,
) -> dict[str, Any]:
    """Stage the phishing-fallback handoff for one failed loop run.

    Launches the campaign (offline previews unless SMTP exists in
    ``payload.json``), rewrites the lure link through the keyless
    shortener and writes the handoff artefact.

    Args:
        target: Engaged host (informational in the artefact).
        params: Payload mapping forwarded to the campaign.
        template: Phishing template name.
        mode: One of :data:`MODES`.
        targets_file: Optional targets CSV for explicit recipient scope.
        provider: Shortener provider key.
        shorten: When False the raw campaign URL stays in the lure.

    Returns:
        Summary mapping with ``campaign_id``, ``ok``, ``short_url``,
        ``artifact`` and ``error``; never raises.
    """
    if mode not in MODES:
        return {"ok": False, "campaign_id": "", "short_url": "", "artifact": "", "error": f"invalid mode: {mode}"}
    try:
        from modules.phishing_orchestrator import PhishingOrchestrator

        orchestrator = PhishingOrchestrator.get_instance()
        domain = str((params or {}).get("domain") or (params or {}).get("rhost") or target or "example.com")
        campaign_id = orchestrator.launch(domain, template=template, mode=mode, targets_file=targets_file)
        if not campaign_id or len(campaign_id) < 6:
            return {
                "ok": False,
                "campaign_id": campaign_id,
                "short_url": "",
                "artifact": "",
                "error": "campaign launch failed",
            }
    except Exception as exc:
        return {"ok": False, "campaign_id": "", "short_url": "", "artifact": "", "error": f"campaign failed: {exc}"}

    campaign_dir = SESSIONS_DIR / f"phishing_{campaign_id}"
    campaign_file = campaign_dir / "campaign.json"
    try:
        campaign_data = json.loads(campaign_file.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "ok": False,
            "campaign_id": campaign_id,
            "short_url": "",
            "artifact": "",
            "error": f"campaign file unreadable: {exc}",
        }

    phishing_url = str(campaign_data.get("phishing_url", "") or "")
    short_url = ""
    if shorten and phishing_url:
        from modules.lazyshortener import shorten as shorten_url

        short_result = shorten_url(phishing_url, provider=provider)
        short_url = str(short_result.get("short_url", "") or "")
        if short_result.get("error"):
            campaign_data["shortener_error"] = str(short_result["error"])
        if short_url:
            campaign_data["phishing_short_url"] = short_url
            try:
                campaign_file.write_text(json.dumps(campaign_data, indent=2), encoding="utf-8")
            except Exception:
                pass

    artifact: Path = SESSIONS_DIR / f"{FALLBACK_ARTIFACT_PREFIX}{campaign_id}.json"
    handoff = {
        "kind": "lazyown_phishing_fallback",
        "created_at": time.time(),
        "target": target,
        "campaign_id": campaign_id,
        "template": template,
        "mode": mode,
        "target_domain": campaign_data.get("target_domain", ""),
        "phishing_url": phishing_url,
        "phishing_short_url": short_url,
        "shortener_provider": provider if short_url else "",
        "campaign_dir": str(campaign_dir),
    }
    try:
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        artifact.write_text(json.dumps(handoff, indent=2), encoding="utf-8")
    except Exception as exc:
        return {
            "ok": False,
            "campaign_id": campaign_id,
            "short_url": short_url,
            "artifact": artifact,
            "error": f"artefact write failed: {exc}",
        }
    return {"ok": True, "campaign_id": campaign_id, "short_url": short_url, "artifact": artifact, "error": ""}


if __name__ == "__main__":
    import sys

    print(run_fallback(sys.argv[1] if len(sys.argv) > 1 else "", shorten="--no-shorten" not in sys.argv))
