#!/usr/bin/env python3
"""
LazyOwn Unified LLM Client
============================
Single interface for all LLM providers used in LazyOwn:
  - Groq (cloud, fast inference)
  - Ollama (local models)
  - DeepSeek via Ollama
  - Fallback chain: Groq → Ollama → static message

Usage:
    from modules.llm_client import LLMClient

    client = LLMClient()
    response = client.ask("Explain this nmap output: ...", provider="groq")
    response = client.ask("Suggest next steps", provider="ollama", model="qwen3.5:0.8b")
    response = client.ask("Classify this output", provider="auto")   # tries groq then ollama
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Optional

log = logging.getLogger("llm_client")

# ── Defaults (overridable via env or constructor) ──────────────────────────────

GROQ_API_URL     = "https://api.groq.com/openai/v1/chat/completions"
GROQ_DEFAULT_MODEL   = "llama3-8b-8192"
GROQ_FAST_MODEL      = "llama-3.1-8b-instant"

OLLAMA_HOST      = os.environ.get("OLLAMA_HOST", "127.0.0.1")
OLLAMA_PORT      = int(os.environ.get("OLLAMA_PORT", "11434"))
OLLAMA_DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:0.8b")
OLLAMA_LARGE_MODEL   = os.environ.get("OLLAMA_LARGE_MODEL", "llama3.2")

DEFAULT_TIMEOUT  = int(os.environ.get("LLM_TIMEOUT", "90"))
DEFAULT_MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", "1024"))


class LLMClient:
    """
    Unified LLM client with automatic fallback.

    Parameters
    ----------
    api_key : str, optional
        Groq API key. Falls back to GROQ_API_KEY env var.
    groq_model : str, optional
        Default Groq model name.
    ollama_model : str, optional
        Default Ollama model name.
    timeout : int, optional
        HTTP request timeout in seconds.
    max_tokens : int, optional
        Max tokens in response.
    """

    def __init__(
        self,
        api_key: str = "",
        groq_model: str = GROQ_DEFAULT_MODEL,
        ollama_model: str = OLLAMA_DEFAULT_MODEL,
        timeout: int = DEFAULT_TIMEOUT,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> None:
        self.api_key     = api_key or os.environ.get("GROQ_API_KEY", "")
        self.groq_model  = groq_model
        self.ollama_model = ollama_model
        self.timeout     = timeout
        self.max_tokens  = max_tokens

    # ── Public API ─────────────────────────────────────────────────────────────

    def ask(
        self,
        prompt: str,
        *,
        provider: str = "auto",
        model: Optional[str] = None,
        system: str = "You are a helpful penetration testing assistant.",
        temperature: float = 0.7,
    ) -> str:
        """
        Send a prompt and return the text response.

        Parameters
        ----------
        prompt : str
            The user prompt.
        provider : str
            One of: "groq", "ollama", "auto".
            "auto" tries groq first, falls back to ollama, then returns static msg.
        model : str, optional
            Override the default model for the selected provider.
        system : str, optional
            System prompt / persona.
        temperature : float, optional
            Sampling temperature (0.0–2.0).

        Returns
        -------
        str
            The model's response text, or an error message prefixed with "[LLM error]".
        """
        if provider == "groq":
            return self._ask_groq(prompt, model or self.groq_model, system, temperature)
        if provider == "ollama":
            return self._ask_ollama(prompt, model or self.ollama_model)
        if provider == "auto":
            if self.api_key:
                result = self._ask_groq(prompt, model or self.groq_model, system, temperature)
                if not result.startswith("[LLM error]"):
                    return result
            result = self._ask_ollama(prompt, model or self.ollama_model)
            if not result.startswith("[LLM error]"):
                return result
            return "[LLM error] No LLM provider available. Set GROQ_API_KEY or start Ollama."
        return f"[LLM error] Unknown provider: {provider}. Use 'groq', 'ollama', or 'auto'."

    def classify(
        self,
        output: str,
        *,
        question: str = "Did this command succeed? Answer only: success, failure, or partial.",
        provider: str = "auto",
        model: Optional[str] = None,
    ) -> str:
        """
        Short classification prompt. Returns a single word: success / failure / partial.
        Uses the faster/cheaper model by default.
        """
        prompt = f"{question}\n\nOUTPUT:\n{output[:2000]}"
        raw = self.ask(
            prompt,
            provider=provider,
            model=model or (GROQ_FAST_MODEL if provider in ("groq", "auto") else OLLAMA_DEFAULT_MODEL),
            system="You are a command output classifier. Reply with one word only.",
            temperature=0.0,
        )
        raw_lower = raw.strip().lower()
        if "success" in raw_lower:
            return "success"
        if "partial" in raw_lower:
            return "partial"
        if "failure" in raw_lower or "fail" in raw_lower:
            return "failure"
        return raw.strip()[:50]

    def summarize(
        self,
        text: str,
        *,
        max_chars: int = 6000,
        provider: str = "auto",
        model: Optional[str] = None,
    ) -> str:
        """
        Summarize a block of text (e.g. nmap output, tool output).
        """
        prompt = (
            f"Summarize the following penetration testing output in 3-5 bullet points. "
            f"Focus on security-relevant findings (open ports, credentials, vulnerabilities):\n\n"
            f"{text[:max_chars]}"
        )
        return self.ask(prompt, provider=provider, model=model)

    # ── Internal: Groq ─────────────────────────────────────────────────────────

    def _ask_groq(
        self,
        prompt: str,
        model: str,
        system: str,
        temperature: float,
    ) -> str:
        if not self.api_key:
            return "[LLM error] GROQ_API_KEY not set."
        body = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            "max_tokens":  self.max_tokens,
            "temperature": temperature,
        }).encode()
        req = urllib.request.Request(
            GROQ_API_URL,
            data=body,
            headers={
                "Content-Type":  "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read())
                return data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as exc:
            log.warning(f"Groq HTTP {exc.code}: {exc.read()[:200]}")
            return f"[LLM error] Groq HTTP {exc.code}"
        except Exception as exc:
            log.warning(f"Groq request failed: {exc}")
            return f"[LLM error] Groq: {exc}"

    # ── Internal: Ollama ───────────────────────────────────────────────────────

    def _ask_ollama(self, prompt: str, model: str) -> str:
        url  = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
        body = json.dumps({
            "model":  model,
            "prompt": prompt,
            "stream": False,
        }).encode()
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read())
                return data.get("response", "").strip()
        except Exception as exc:
            log.warning(f"Ollama request failed: {exc}")
            return f"[LLM error] Ollama: {exc}"


# ── Module-level singleton (lazy init) ────────────────────────────────────────

_default_client: Optional[LLMClient] = None


def get_client(api_key: str = "") -> LLMClient:
    """Return (or create) the module-level singleton LLMClient."""
    global _default_client
    if _default_client is None or (api_key and _default_client.api_key != api_key):
        _default_client = LLMClient(api_key=api_key)
    return _default_client


def ask(
    prompt: str,
    *,
    provider: str = "auto",
    model: Optional[str] = None,
    api_key: str = "",
    system: str = "You are a helpful penetration testing assistant.",
) -> str:
    """Module-level convenience wrapper."""
    return get_client(api_key).ask(prompt, provider=provider, model=model, system=system)


def classify(output: str, *, provider: str = "auto", api_key: str = "") -> str:
    """Module-level convenience wrapper."""
    return get_client(api_key).classify(output, provider=provider)


def summarize(text: str, *, provider: str = "auto", api_key: str = "") -> str:
    """Module-level convenience wrapper."""
    return get_client(api_key).summarize(text, provider=provider)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse, sys

    p = argparse.ArgumentParser(description="LazyOwn LLM Client CLI")
    p.add_argument("prompt", nargs="?", default="", help="Prompt text (or pipe via stdin)")
    p.add_argument("--provider", default="auto", choices=["groq", "ollama", "auto"])
    p.add_argument("--model",    default=None)
    p.add_argument("--classify", action="store_true", help="Run as classifier")
    p.add_argument("--system",   default="You are a helpful penetration testing assistant.")
    args = p.parse_args()

    prompt_text = args.prompt or sys.stdin.read()
    if not prompt_text.strip():
        p.print_help()
        sys.exit(1)

    client = LLMClient(api_key=os.environ.get("GROQ_API_KEY", ""))
    if args.classify:
        print(client.classify(prompt_text, provider=args.provider, model=args.model))
    else:
        print(client.ask(prompt_text, provider=args.provider, model=args.model, system=args.system))
