"""LLM adapter facade — single import point for all LLM backends used by lazyc2.

Consolidates the scattered LLM module imports into one adapter and preserves
every original function signature for backward compatibility with the C2
dashboard. The Groq ``process_prompt_*`` family is implemented here directly on
the canonical prompt/knowledge contract (:mod:`modules.llm_prompts`) and no
longer depends on the retired ``modules.legacy.lazygptcli*`` scripts.

The three streaming local helpers (``process_prompt_local``,
``process_prompt_localreport`` and ``process_prompt_local_yaml``) are retained
as re-exports from their Ollama-specific legacy modules until those endpoints
migrate onto the factory-backed streaming path.

Usage::

    from modules.llm_adapter import (
        Groq, safe_groq_client,
        process_prompt, process_prompt_script, process_prompt_adversary,
        process_prompt_general, process_prompt_task, process_prompt_vuln,
        process_prompt_redop, process_prompt_search,
    )
"""

from __future__ import annotations

import logging
from typing import Any

from modules.legacy.lazydeepseekcli import process_prompt_local, process_prompt_localreport
from modules.legacy.lazyphishingai import process_prompt_local_yaml
from modules.llm_prompts import (
    DEFAULT_SYSTEM_PROMPT,
    TEMPLATE_KB_DOMAINS,
    TEMPLATE_MODELS,
    LlmPromptConfig,
    resolve_model,
    truncate_message,
)

DEFAULT_MAX_TOKENS = 4096

try:
    from groq import Groq
except ImportError:  # pragma: no cover - optional dependency
    Groq = None  # type: ignore[assignment,misc]


def safe_groq_client(api_key: str | None) -> Any | None:
    """Create a Groq client, returning None when no key is provided.

    Args:
        api_key: Groq API key or None.

    Returns:
        Groq client instance or None.
    """
    if not api_key or Groq is None:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception:
        return None


def _configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level)


def _read_prompt_file(prompt: str) -> str | None:
    try:
        with open(prompt, encoding="utf-8") as handle:
            return handle.read()
    except (FileNotFoundError, OSError):
        return None


def _read_error(prompt: str) -> str:
    return f"Error reading file: {prompt}"


def _complete(client: Any, full_prompt: str, model: str | None) -> str:
    if client is None:
        return "Error: Groq client not initialized"
    try:
        response = client.chat.completions.create(
            model=resolve_model(model),
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=DEFAULT_MAX_TOKENS,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return str(exc)


def _process(
    client: Any,
    prompt: str,
    debug: bool,
    template: str,
    config: LlmPromptConfig,
) -> str:
    if client is None:
        return "Error: Groq API key not configured"
    if debug:
        _configure_logging(True)
    store = config.knowledge_store(TEMPLATE_KB_DOMAINS[template])
    relevant = store.relevant(prompt)
    full_prompt = truncate_message(
        config.render(template, prompt, kb_lines=relevant)
    )
    result = _complete(client, full_prompt, TEMPLATE_MODELS.get(template))
    if not result.startswith("Error:"):
        store.add(prompt, result)
    return result


_CONFIG = LlmPromptConfig.from_defaults()


def process_prompt(client: Any, prompt: str, debug: bool = False) -> str:
    """Generate a single-line shell command from a user prompt.

    Args:
        client: Groq-style chat completion client.
        prompt: Operator goal text.
        debug: Enable debug logging.

    Returns:
        Generated single-line command.
    """
    return _process(client, prompt, debug, "oneliner", _CONFIG)


def process_prompt_script(client: Any, prompt: str, debug: bool = False) -> str:
    """Generate a full script from a user prompt.

    Args:
        client: Groq-style chat completion client.
        prompt: Script requirements text.
        debug: Enable debug logging.

    Returns:
        Generated script text.
    """
    return _process(client, prompt, debug, "script", _CONFIG)


def process_prompt_adversary(client: Any, prompt: str, debug: bool = False) -> str:
    """Answer questions about MITRE ATT&CK techniques and Atomic Red Team.

    Args:
        client: Groq-style chat completion client.
        prompt: Adversary technique query.
        debug: Enable debug logging.

    Returns:
        Technique analysis text.
    """
    return _process(client, prompt, debug, "adversary", _CONFIG)


def process_prompt_general(client: Any, prompt: str, debug: bool = False) -> str:
    """Answer as a general red-team assistant with payload.json context.

    Args:
        client: Groq-style chat completion client.
        prompt: Operator question.
        debug: Enable debug logging.

    Returns:
        Assistance text.
    """
    return _process(client, prompt, debug, "general", _CONFIG)


def process_prompt_search(client: Any, prompt: str, debug: bool = False) -> str:
    """Perform research and threat-intelligence analysis.

    Args:
        client: Groq-style chat completion client.
        prompt: Research topic.
        debug: Enable debug logging.

    Returns:
        Analysis text.
    """
    return _process(client, prompt, debug, "search", _CONFIG)


def process_prompt_task(client: Any, prompt: str, debug: bool = False) -> str:
    """Analyze a task-assessment JSON file for completion status.

    Args:
        client: Groq-style chat completion client.
        prompt: Path to the task JSON file.
        debug: Enable debug logging.

    Returns:
        Task analysis, or an error message when the file cannot be read.
    """
    content = _read_prompt_file(prompt)
    if content is None:
        return _read_error(prompt)
    return _process(client, content, debug, "task", _CONFIG)


def process_prompt_vuln(
    client: Any,
    prompt: str,
    debug: bool = False,
    event: str = "",
) -> str:
    """Analyze Nmap output for vulnerabilities and propose an action plan.

    Args:
        client: Groq-style chat completion client.
        prompt: Path to the Nmap output file.
        debug: Enable debug logging.
        event: Optional event name whose tool output is appended.

    Returns:
        Vulnerability assessment, or an error message when the file cannot be
        read.
    """
    content = _read_prompt_file(prompt)
    if content is None:
        return _read_error(prompt)
    if event:
        tool_output = _CONFIG.load_event_tool_output(event)
        if tool_output:
            content += "\n\n--- Tool Output ---\n" + tool_output
    plan_history = _CONFIG.load_plan_history()
    if plan_history:
        content += "\n\n--- Plan History ---\n" + plan_history
    return _process(client, content, debug, "vuln", _CONFIG)


def process_prompt_redop(client: Any, prompt: str, debug: bool = False) -> str:
    """Evaluate a red-team operation status from a JSON database file.

    Args:
        client: Groq-style chat completion client.
        prompt: Path to the operation JSON file.
        debug: Enable debug logging.

    Returns:
        Operation evaluation, or an error message when the file cannot be read.
    """
    content = _read_prompt_file(prompt)
    if content is None:
        return _read_error(prompt)
    return _process(client, content, debug, "redop", _CONFIG)


def ask_general(prompt: str, debug: bool = False) -> str:
    """Answer through the configured LLM backend, regardless of provider.

    Resolves the backend from ``payload.json`` via
    :func:`modules.llm_factory.try_get_llm_backend`, renders the canonical
    general-assistant template with knowledge-base context, and persists
    successful answers. This is the single provider-agnostic entry point
    every bot (Slack, Telegram, Discord) uses.

    Args:
        prompt: Operator question or tool output to analyze.
        debug: Enable debug logging.

    Returns:
        Assistance text, or an error message when no backend is available.
    """
    from modules.llm_factory import try_get_llm_backend

    if debug:
        _configure_logging(True)
    store = _CONFIG.knowledge_store(TEMPLATE_KB_DOMAINS["general"])
    full_prompt = truncate_message(
        _CONFIG.render("general", prompt, kb_lines=store.relevant(prompt))
    )
    backend = try_get_llm_backend()
    if backend is None:
        return (
            "Error: no LLM backend available. Set llm_backend and the "
            "matching provider key, or start Ollama for local inference."
        )
    try:
        result = backend.complete(DEFAULT_SYSTEM_PROMPT, full_prompt)
    except Exception as exc:
        return f"Error: {exc}"
    if not isinstance(result, str):
        return "Error: backend returned an unusable response."
    if result.startswith("Error"):
        return result
    store.add(prompt, result)
    return result


__all__ = [
    "Groq",
    "ask_general",
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
