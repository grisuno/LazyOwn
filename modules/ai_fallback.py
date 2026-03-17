"""
LazyOwn AI Fallback Chain
==========================
Unified LLM caller with automatic fallback:

  1. Groq (cloud, fast, requires api_key)
       ↓ on quota / rate-limit error
  2. Ollama (local, requires ollama running + a chat model)
       ↓ if Ollama unreachable or no suitable model
  3. Helpful error message with actionable steps

Used by recommender.py and timeline_narrator.py so fallback
logic lives in exactly one place.

Public API
----------
call(prompt, system, api_key, max_tokens, temperature) -> AIResult

AIResult fields:
  .text     str   — the response text (or error/help message)
  .backend  str   — "groq" | "ollama" | "error"
  .model    str   — model name used
  .error    str   — original error if fallback occurred (else "")
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import requests

# ── Constants ──────────────────────────────────────────────────────────────────

_GROQ_MODEL   = "llama-3.3-70b-versatile"
_OLLAMA_HOST  = "http://localhost:11434"

# Models we prefer for chat (ordered by quality)
_PREFERRED_CHAT = ["llama3.2", "llama3", "mistral", "gemma", "phi3", "qwen2.5"]

# Models that are reasoning-only and can't do simple JSON/prose tasks well
_REASONING_ONLY = {"qwen3", "qwen3.5", "deepseek-r1"}

# Groq error strings that indicate quota exhaustion (not transient errors)
_QUOTA_ERRORS = (
    "rate_limit_exceeded",
    "quota_exceeded",
    "insufficient_quota",
    "tokens per",
    "requests per",
    "exceeded your",
    "429",
)

_HELP_MESSAGE = """\
⚠️  No AI backend available.

── Option 1: Add a Groq API key (free tier, 14,400 req/day) ──
  1. Create a free account at https://console.groq.com
  2. Generate an API key
  3. Add it to payload.json:  "api_key": "gsk_..."
  Or set the environment variable: export GROQ_API_KEY=gsk_...

── Option 2: Run a local model with Ollama ──
  Install Ollama:
    curl -fsSL https://ollama.com/install.sh | sh

  Pull a fast chat model (pick one):
    ollama pull llama3.2:3b    # recommended — fast & capable
    ollama pull mistral        # excellent for pentesting tasks
    ollama pull gemma:2b       # lightweight

  Start the server:
    ollama serve &

  Then retry your request.
"""


# ── Result type ────────────────────────────────────────────────────────────────

@dataclass
class AIResult:
    text:    str
    backend: str          # "groq" | "ollama" | "error"
    model:   str = ""
    error:   str = ""     # original error that triggered fallback


# ── Ollama helpers ─────────────────────────────────────────────────────────────

def _ollama_available() -> bool:
    try:
        r = requests.get(f"{_OLLAMA_HOST}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def _best_ollama_model() -> str | None:
    """Return the best available chat model, or None if none found."""
    try:
        r = requests.get(f"{_OLLAMA_HOST}/api/tags", timeout=3)
        all_models = [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return None

    if not all_models:
        return None

    # Try preferred models first
    for pref in _PREFERRED_CHAT:
        for m in all_models:
            base = m.split(":")[0].lower()
            if base == pref or base.startswith(pref):
                return m

    # Accept any model that isn't reasoning-only
    for m in all_models:
        base = m.split(":")[0].lower()
        if not any(r in base for r in _REASONING_ONLY):
            return m

    return None


def _ollama_call(
    model: str,
    system: str,
    user: str,
    max_tokens: int,
    temperature: float,
) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    payload = {
        "model":   model,
        "messages": messages,
        "stream":  False,
        "options": {"num_predict": max_tokens, "temperature": temperature},
    }
    r = requests.post(f"{_OLLAMA_HOST}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    obj = r.json()

    msg     = obj.get("message", {})
    content = (msg.get("content") or "").strip()
    if content:
        content = re.sub(r"<think>[\s\S]*?</think>", "", content).strip()
        if content:
            return content

    # reasoning-only fallback
    thinking = (obj.get("thinking") or msg.get("thinking") or "").strip()
    if thinking:
        match = re.search(r"(?:Answer|Result|Output|Final)[:\s]+(.+?)(?:\n\n|\Z)", thinking, re.DOTALL)
        if match:
            return match.group(1).strip()
        paragraphs = [p.strip() for p in thinking.split("\n\n") if p.strip()]
        return paragraphs[-1] if paragraphs else thinking[:400]

    return "[ollama returned empty response]"


# ── Groq helper ───────────────────────────────────────────────────────────────

def _is_quota_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(q in msg for q in _QUOTA_ERRORS)


def _groq_call(
    api_key: str,
    system: str,
    user: str,
    max_tokens: int,
    temperature: float,
) -> str:
    from groq import Groq
    client = Groq(api_key=api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    resp = client.chat.completions.create(
        model=_GROQ_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()


# ── Public API ────────────────────────────────────────────────────────────────

def call(
    prompt:      str,
    system:      str  = "",
    api_key:     str  = "",
    max_tokens:  int  = 1024,
    temperature: float = 0.3,
) -> AIResult:
    """
    Call Groq → fallback to Ollama → fallback to helpful error message.
    Returns an AIResult with .text, .backend, .model, .error.
    """
    groq_error = ""

    # ── 1. Try Groq ────────────────────────────────────────────────────────
    if api_key:
        try:
            text = _groq_call(api_key, system, prompt, max_tokens, temperature)
            return AIResult(text=text, backend="groq", model=_GROQ_MODEL)
        except Exception as exc:
            groq_error = str(exc)
            if not _is_quota_error(exc):
                # Non-quota error (network, bad key, etc.) — still fall through
                # but include the actual error in the result
                pass

    # ── 2. Try Ollama ──────────────────────────────────────────────────────
    if _ollama_available():
        model = _best_ollama_model()
        if model:
            try:
                text = _ollama_call(model, system, prompt, max_tokens, temperature)
                warning = ""
                if groq_error:
                    if _is_quota_error(Exception(groq_error)):
                        warning = f"[Groq quota exceeded — using local model {model}]\n\n"
                    else:
                        warning = f"[Groq unavailable ({groq_error[:60]}…) — using local model {model}]\n\n"
                return AIResult(
                    text    = warning + text,
                    backend = "ollama",
                    model   = model,
                    error   = groq_error,
                )
            except Exception as exc:
                ollama_error = str(exc)
                # Fall through to help message
                return AIResult(
                    text = (
                        f"⚠️  Both AI backends failed.\n\n"
                        f"Groq error:  {groq_error or '(not configured)'}\n"
                        f"Ollama error: {ollama_error}\n\n"
                        + _HELP_MESSAGE
                    ),
                    backend = "error",
                    model   = "",
                    error   = ollama_error,
                )
        else:
            # Ollama running but no suitable model installed
            installed_hint = ""
            try:
                r = requests.get(f"{_OLLAMA_HOST}/api/tags", timeout=3)
                installed = [m["name"] for m in r.json().get("models", [])]
                if installed:
                    installed_hint = (
                        f"\n  Installed models (not suitable for chat): {installed}\n"
                        f"  Run: ollama pull llama3.2:3b"
                    )
            except Exception:
                pass

            return AIResult(
                text = (
                    f"⚠️  Ollama is running but has no compatible chat model.\n"
                    + installed_hint + "\n\n"
                    + _HELP_MESSAGE
                ),
                backend = "error",
                model   = "",
                error   = groq_error,
            )

    # ── 3. Nothing available ───────────────────────────────────────────────
    prefix = ""
    if groq_error:
        if _is_quota_error(Exception(groq_error)):
            prefix = f"⚠️  Groq quota exceeded: {groq_error[:120]}\n\n"
        else:
            prefix = f"⚠️  Groq error: {groq_error[:120]}\n\n"

    return AIResult(
        text    = prefix + _HELP_MESSAGE,
        backend = "error",
        model   = "",
        error   = groq_error,
    )


# ── CLI smoke-test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        try:
            key = json.loads(Path("../payload.json").read_text()).get("api_key", "")
        except Exception:
            pass

    result = call(
        prompt     = "Reply with exactly: FALLBACK_TEST_OK",
        system     = "You are a test assistant.",
        api_key    = key,
        max_tokens = 20,
    )
    print(f"backend : {result.backend}")
    print(f"model   : {result.model}")
    print(f"error   : {result.error or '(none)'}")
    print(f"text    : {result.text}")
