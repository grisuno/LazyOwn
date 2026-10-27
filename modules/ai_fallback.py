"""
LazyOwn AI Fallback Chain
=========================
Unified LLM caller with automatic fallback:

  1. Orchestrator chain (lazy_orchestrator pool, weight-sorted legs
     executed through modules.llm_factory — groq, ollama, llamacpp,
     pi, toposwarm)
       ↓ when every chain member fails
  2. Direct Groq call with the caller-supplied key (only when the chain
     never attempted a groq leg)
       ↓ on quota / rate-limit error
  3. Ollama (local, requires ollama running + a chat model)
       ↓ if Ollama unreachable or no suitable model
  4. TopoSwarm local brain
       ↓
  5. Helpful error message with actionable steps

Used by recommender.py and timeline_narrator.py so fallback
logic lives in exactly one place.

Public API
----------
call(prompt, system, api_key, max_tokens, temperature) -> AIResult

AIResult fields:
  .text     str   — the response text (or error/help message)
  .backend  str   — "groq" | "ollama" | "toposwarm" | "error"
  .model    str   — model name used
  .error    str   — original error if fallback occurred (else "")
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import requests

# -- Constants (imported from single source of truth) --
from modules.llm_factory import (  # noqa: F401  (contract: ai_fallback reads factory defaults)
    DEFAULT_GROQ_MODEL as _GROQ_MODEL,
)
from modules.llm_factory import (
    DEFAULT_OLLAMA_HOST as _OLLAMA_HOST,
)
from modules.llm_factory import (  # noqa: E402
    groq_model_chain as _groq_model_chain,
)
from modules.llm_factory import (  # noqa: E402
    is_model_missing_error as _is_model_missing_error,
)
from modules.llm_orchestrator import (  # noqa: E402
    OrchestratorResult as _OrchestratorResult,
)
from modules.llm_orchestrator import (  # noqa: E402
    complete_with_fallback,
)

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
[!] No AI backend available.

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
    text: str
    backend: str  # "groq" | "ollama" | "error"
    model: str = ""
    error: str = ""  # original error that triggered fallback


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
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"num_predict": max_tokens, "temperature": temperature},
    }
    r = requests.post(f"{_OLLAMA_HOST}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    obj = r.json()

    msg = obj.get("message", {})
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

    last_error: Exception | None = None
    for model in _groq_model_chain():
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].message.content.strip()
        except Exception as exc:
            last_error = exc
            if not _is_model_missing_error(exc):
                raise
    if last_error is not None:
        raise last_error
    raise RuntimeError("no Groq model candidates available")


# ── Public API ────────────────────────────────────────────────────────────────


def _toposwarm_call(prompt: str, system: str) -> AIResult | None:
    """
    Try TopoSwarm local brain as a last-resort fallback.
    Returns an AIResult if TopoSwarm is available, else None.
    """
    try:
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent))
        from toposwarm_bridge import get_bridge

        bridge = get_bridge()
        if not bridge.available:
            return None
        # Use the orchestrator subprocess for full routing + execution
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        text = bridge.execute_via_orchestrator(full_prompt, no_model=not bridge.model_loaded)
        return AIResult(
            text=f"[TopoSwarm local brain]\n\n{text}",
            backend="toposwarm",
            model="toposwarm-2M" + ("-neural" if bridge.model_loaded else "-keyword"),
            error="",
        )
    except Exception:
        return None


def _chain_groq_attempted(result: _OrchestratorResult) -> bool:
    """Return True when the orchestrator chain already ran a groq leg.

    Args:
        result: Outcome of the orchestrator chain walk.

    Returns:
        True when any executed attempt carried a ``groq:`` model spec,
        meaning a direct Groq retry would duplicate the same request.
    """
    return any(spec.startswith("groq:") for spec in result.attempted_specs)


def call(
    prompt: str,
    system: str = "",
    api_key: str = "",
    max_tokens: int = 1024,
    temperature: float = 0.3,
) -> AIResult:
    """
    Call the orchestrator chain first, then Groq (explicit key only),
    Ollama, TopoSwarm, and finally return the help message.
    Returns an AIResult with .text, .backend, .model, .error.
    """
    orch = complete_with_fallback(prompt, system=system, api_key=api_key, max_tokens=max_tokens)
    if orch.ok:
        return AIResult(
            text=orch.display_text,
            backend=orch.backend,
            model=orch.model_name,
            error=orch.attempts[0][1] if orch.attempts else "",
        )
    groq_error = next((error for name, error in orch.attempts if "groq" in name.lower()), orch.attempts[0][1] if orch.attempts else "")
    if api_key and not _chain_groq_attempted(orch):
        try:
            text = _groq_call(api_key, system, prompt, max_tokens, temperature)
            warning = _fallback_warning(orch)
            return AIResult(text=warning + text, backend="groq", model=_groq_model_chain()[0], error=groq_error or _summarize_attempts(orch))
        except Exception as exc:
            groq_error = str(exc)
            if not _is_quota_error(exc):
                pass
    if _ollama_available():
        model = _best_ollama_model()
        if model:
            try:
                text = _ollama_call(model, system, prompt, max_tokens, temperature)
                warning = _fallback_warning(orch)
                return AIResult(
                    text=warning + text,
                    backend="ollama",
                    model=model,
                    error=groq_error,
                )
            except Exception as exc:
                ollama_error = str(exc)
                ts_result = _toposwarm_call(prompt, system)
                if ts_result:
                    ts_result.error = _summarize_attempts(orch) + f" ollama:{ollama_error}"
                    return ts_result
                return _total_failure_result(orch, ollama_error)
        else:
            installed_hint = ""
            try:
                r = requests.get(f"{_OLLAMA_HOST}/api/tags", timeout=3)
                installed = [m["name"] for m in r.json().get("models", [])]
                if installed:
                    installed_hint = (
                        f"\n  Installed models (not suitable for chat): {installed}\n  Run: ollama pull llama3.2:3b"
                    )
            except Exception:
                pass
            return AIResult(
                text="Ollama is running but has no compatible chat model." + installed_hint + "\n\n" + _HELP_MESSAGE,
                backend="error",
                model="",
                error=groq_error,
            )
    return _total_failure_result(orch, "ollama: not running")


def _fallback_warning(orch: _OrchestratorResult) -> str:
    """Return the notice text describing which members failed first."""
    return orch.notice + "\n\n" if orch.notice else ""


def _summarize_attempts(orch: _OrchestratorResult) -> str:
    """Join the chain attempt errors into one compact string."""
    return "; ".join(f"{name}: {error}" for name, error in orch.attempts)[:300]


def _total_failure_result(orch: _OrchestratorResult, local_error: str) -> AIResult:
    """Build the final error AIResult after every leg failed."""
    chain_errors = _summarize_attempts(orch)
    text = (
        f"All AI backends failed (orchestrator chain, Groq, Ollama, TopoSwarm).\n\n"
        f"Chain errors:   {chain_errors or '(chain empty)'}\n"
        f"Local error:    {local_error}\n\n" + _HELP_MESSAGE
    )
    return AIResult(
        text=text,
        backend="error",
        model="",
        error=chain_errors or local_error,
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
        prompt="Reply with exactly: FALLBACK_TEST_OK",
        system="You are a test assistant.",
        api_key=key,
        max_tokens=20,
    )
    print(f"backend : {result.backend}")
    print(f"model   : {result.model}")
    print(f"error   : {result.error or '(none)'}")
    print(f"text    : {result.text}")
