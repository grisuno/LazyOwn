"""LLM adapter — single import point for all LLM backends used by lazyc2.

Consolidates the 11 scattered LLM module imports into one adapter.
Every function preserves its original signature and behavior — zero
runtime change, purely an import-path refactor.

Usage::

    from modules.llm_adapter import (
        Groq, safe_groq_client,
        process_prompt, process_prompt_script, process_prompt_adversary,
        process_prompt_general, process_prompt_task, process_prompt_vuln,
        process_prompt_redop, process_prompt_search,
        process_prompt_local, process_prompt_localreport, process_prompt_local_yaml,
    )
"""

from __future__ import annotations

from modules.legacy.lazydeepseekcli import process_prompt_local, process_prompt_localreport
from modules.legacy.lazygptcli_unified import (
    Groq,
    process_prompt,
    process_prompt_adversary,
    process_prompt_general,
    process_prompt_redop,
    process_prompt_script,
    process_prompt_search,
    process_prompt_task,
    process_prompt_vuln,
)
from modules.legacy.lazyphishingai import process_prompt_local_yaml


def safe_groq_client(api_key: str | None) -> Groq | None:
    """Create a Groq client, returning None when no key is provided.

    Args:
        api_key: Groq API key or None.

    Returns:
        Groq client instance or None.
    """
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception:
        return None


__all__ = [
    "Groq",
    "safe_groq_client",
    "process_prompt",
    "process_prompt_script",
    "process_prompt_adversary",
    "process_prompt_general",
    "process_prompt_task",
    "process_prompt_vuln",
    "process_prompt_redop",
    "process_prompt_search",
    "process_prompt_local",
    "process_prompt_localreport",
    "process_prompt_local_yaml",
]
