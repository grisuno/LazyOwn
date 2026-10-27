"""Orchestrator-governed LLM failover chain for every AI module.

Single entry point the framework's AI consumers use to reach a language
model. The failover chain is owned by ``lazy_orchestrator`` (the Models
tab) and persisted in ``sessions/lazy/llm_pool.json``; member priority
acts as the weight deciding the try order. Each leg executes through the
``modules.llm_factory`` model-spec executor (``groq:``, ``ollama:``,
``llamacpp:``, ``pi:``, ``toposwarm:``), so a dead Groq key, an exhausted
quota or a missing API key degrades to the next member instead of
breaking the caller. The chain never raises: total exhaustion returns a
help message the caller can display.

Contracts
---------
* :func:`pool_chain` — ordered members read from the lazy_orchestrator pool.
* :func:`sort_members` — weight-sorted defensive copy of a member list.
* :func:`backend_kind` — provider prefix derived from a model spec.
* :func:`complete_with_fallback` — the failover walk returning an
  :class:`OrchestratorResult` with a fallback notice when the primary
  failed.
* :data:`HELP_MESSAGE` — the final-resort guidance text.

Usage::

    from modules.llm_orchestrator import complete_with_fallback

    result = complete_with_fallback("summarize the nmap output", max_tokens=800)
    if result.ok:
        print(result.display_text)
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

Executor = Callable[[str, str, int], str]

LLM_ERROR_MARKERS: tuple[str, ...] = (
    "[llm error]",
    "api_key not set",
    "no ai backend available",
    "all ai backends failed",
    "error code: 4",
    "error code: 5",
    "error from groq:",
    "error from ollama:",
    "error from openai:",
    "error from anthropic:",
    "error from deepseek:",
    "error from llama.cpp:",
    "error streaming from ",
    "invalid api key",
    "invalidapikey",
    "rate_limit_exceeded",
    "rate limit exceeded",
)

LLM_QUOTA_MARKERS: tuple[str, ...] = (
    "insufficient_quota",
    "quota_exceeded",
    "insufficient quota",
    "quota exceeded",
    "insufficient credits",
    "insufficient_balance",
    "insufficient balance",
    "exceeded your current",
    "out of tokens",
)

PLACEHOLDER_KEY_EXACT: frozenset[str] = frozenset({"api_key"})
PLACEHOLDER_KEY_FRAGMENTS: tuple[str, ...] = ("your_api_key", "api_key_here")

ERROR_TEXT_LIMIT = 160

HELP_MESSAGE = """\
No AI backend answered. Fix options:
1. Set a Groq API key: assign api_key gsk_... in LazyOwn, or export GROQ_API_KEY.
2. Start a local Ollama server: ollama serve, then ollama pull deepseek-r1:1.5b.
3. Start a llama.cpp server (OpenAI-compatible) on 127.0.0.1:8080.
4. Manage the failover chain and its weights with lazy_orchestrator (Models tab).
"""


def _blank_error(message: str) -> str:
    return message


@dataclass
class OrchestratorResult:
    """Outcome of one orchestrator chain walk.

    Attributes:
        text: Clean model answer; the help message on total failure.
        member: Name of the serving pool member (empty on failure).
        model: Full model spec of the serving member (empty on failure).
        model_name: Model spec without the provider prefix.
        backend: Provider prefix of the serving member or ``"error"``.
        fallback_used: True when anything but the primary served.
        notice: Operator-facing message naming failures and the server;
            empty when the primary succeeded.
        attempts: ``(member, error)`` pairs for every failed attempt.
    """

    text: str
    member: str = ""
    model: str = ""
    model_name: str = ""
    backend: str = "error"
    fallback_used: bool = False
    notice: str = ""
    attempts: list[tuple[str, str]] = field(default_factory=list)
    attempted_specs: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Return True when a chain member served the answer."""
        return self.backend != "error"

    @property
    def display_text(self) -> str:
        """Return the notice-prefixed answer for operator-facing surfaces."""
        if self.notice:
            return f"{self.notice}\n\n{self.text}"
        return self.text


def sort_members(members: list[dict]) -> list[dict]:
    """Return a weight-sorted defensive copy of a member list.

    Args:
        members: Pool member mappings with ``priority`` keys.

    Returns:
        New list ordered by descending priority weight.
    """
    def _weight(member: dict) -> int:
        try:
            return int(member.get("priority", 0))
        except (TypeError, ValueError):
            return 0

    return sorted(members, key=_weight, reverse=True)


def pool_chain() -> list[dict]:
    """Return the failover chain governed by lazy_orchestrator.

    Members come from the persistent pool store managed by the
    lazy_orchestrator Models tab (``sessions/lazy/llm_pool.json``) and are
    weight-sorted by descending priority. Members without a model spec
    are dropped.

    Returns:
        Ordered member mappings; empty when the pool is unreadable.
    """
    try:
        from modules.lazy_engine import LlmPool

        members = LlmPool().members()
    except Exception:
        return []
    usable = []
    for member in members if isinstance(members, list) else []:
        if not isinstance(member, dict):
            continue
        if not str(member.get("model", "")).strip():
            continue
        usable.append(member)
    return sort_members(usable)


def backend_kind(model_spec: str) -> str:
    """Return the provider prefix of a model spec.

    Args:
        model_spec: Spec such as ``groq:llama-3.3-70b-versatile`` or a
            bare model name.

    Returns:
        The prefix before the first colon, or ``"auto"`` when the spec
        carries no recognizable prefix.
    """
    head, sep, _ = (model_spec or "").partition(":")
    if sep and head.strip() and " " not in head:
        return head.strip().lower()
    return "auto"


def is_error_reply(text: str) -> bool:
    """Return True when a reply is a backend error banner, not content.

    Args:
        text: Raw reply text.

    Returns:
        True for blank text, SDK error banners (``Error code: ...``,
        ``Error from Groq: ...``), quota/billing prose and framework
        markers.
    """
    lowered = (text or "").strip().lower()
    if not lowered:
        return True
    if any(mark in lowered for mark in LLM_ERROR_MARKERS):
        return True
    return any(mark in lowered for mark in LLM_QUOTA_MARKERS)


def is_placeholder_key(value: str | None) -> bool:
    """Return True when a key value is a shipped placeholder, not a secret.

    Args:
        value: Candidate key text.

    Returns:
        True for blank values, the literal ``api_key`` and the shipped
        ``YOUR_API_KEY_HERE``-style placeholders.
    """
    lowered = (value or "").strip().lower()
    if not lowered:
        return True
    if lowered in PLACEHOLDER_KEY_EXACT:
        return True
    return any(fragment in lowered for fragment in PLACEHOLDER_KEY_FRAGMENTS)


def _dedupe(chain: list[dict]) -> list[dict]:
    """Drop repeated members by name, keeping the first occurrence."""
    seen: set[str] = set()
    unique: list[dict] = []
    for member in chain:
        name = str(member.get("name", ""))
        if name in seen:
            continue
        seen.add(name)
        unique.append(member)
    return unique


def _ensure_groq_env_key(api_key: str) -> None:
    """Make the payload Groq key reachable by the spec executor.

    The pool's ``groq:`` legs run through the factory's spec executor,
    whose Groq client reads ``GROQ_API_KEY`` from the environment. When
    the caller supplied a key, or ``payload.json`` holds one, it is
    published to the environment so the leg can authenticate; shipped
    placeholder values never reach the environment. This mirrors the
    ``do_apikey`` command which already performs the same
    payload-to-environment sync.

    Args:
        api_key: Explicit key passed by the caller, possibly empty.
    """
    env_value = os.environ.get("GROQ_API_KEY", "")
    if env_value and not is_placeholder_key(env_value):
        return
    candidate = (api_key or "").strip()
    if not candidate or is_placeholder_key(candidate):
        candidate = ""
    if not candidate:
        try:
            from modules.llm_factory import (
                CONFIG_KEY_API_KEY,
                load_payload,
            )

            config_key = str(load_payload().get(CONFIG_KEY_API_KEY) or "").strip()
            if not is_placeholder_key(config_key):
                candidate = config_key
        except Exception:
            return
    if candidate:
        os.environ["GROQ_API_KEY"] = candidate


def _default_health() -> Any | None:
    """Return the shared breaker registry, or None when unavailable."""
    try:
        from modules.llm_pool import shared_registry

        return shared_registry()
    except Exception:
        return None


def _breaker_active() -> bool:
    """Return whether the orchestrator llm_pool stage governs breakers."""
    try:
        from modules.orchestrator_config import stage_enabled

        return bool(stage_enabled("llm_pool"))
    except Exception:
        return True


def _ledger_record(name: str, ok: bool, text: str = "") -> None:
    """Append one outcome row to the pool usage ledger."""
    try:
        from modules.lazy_engine import LlmPool

        LlmPool().record_call(name, ok, text)
    except Exception:
        return


def _factory_executor(model_spec: str, prompt: str, max_tokens: int) -> str:
    """Execute one pool member through the factory spec executor.

    Groq legs are refused up front when no usable API key is published,
    so a shipped placeholder never becomes a doomed network request.

    Args:
        model_spec: Model spec with optional provider prefix.
        prompt: Combined system and user prompt text.
        max_tokens: Response token cap.

    Returns:
        Raw reply text; raises on transport failure so the chain can
        fail over.
    """
    if backend_kind(model_spec) == "groq" and is_placeholder_key(os.environ.get("GROQ_API_KEY")):
        raise RuntimeError("groq leg unavailable: no usable API key")
    from modules.llm_factory import complete as factory_complete

    return str(factory_complete(model_spec, prompt, max_tokens=max_tokens) or "")


def _notice_fallback(primary: dict, attempts: list[tuple[str, str]], served: dict) -> str:
    """Build the operator notice for a fallback-served answer."""
    primary_error = ""
    for name, error in attempts:
        if name == str(primary.get("name", "")):
            primary_error = error[:ERROR_TEXT_LIMIT]
            break
    others = [name for name, _ in attempts if name != str(primary.get("name", ""))]
    first = f"[!] Primary model '{primary.get('name', '')}' ({primary.get('model', '')}) failed"
    if primary_error:
        first += f": {primary_error}"
    else:
        first += " (no answer)"
    second = f"[!] Failover engaged: served by '{served.get('name', '')}' ({served.get('model', '')})."
    if others:
        second += f" Also tried: {', '.join(repr(name) for name in others)}."
    return f"{first}\n{second}"


def complete_with_fallback(
    prompt: str,
    system: str = "",
    max_tokens: int = 800,
    api_key: str = "",
    members: list[dict] | None = None,
    executor: Executor | None = None,
    health: Any | None = None,
    record: bool = True,
) -> OrchestratorResult:
    """Complete a prompt through the lazy_orchestrator chain with failover.

    The chain is the priority-sorted member list from the
    lazy_orchestrator pool unless an override list is supplied. Members
    parked by the shared health breaker are skipped while any healthy
    member remains and retried as a last resort when none is. A member
    fails when the executor raises, returns blank text, or returns an
    error banner; the walk continues until one member serves. The
    function never raises.

    Args:
        prompt: User prompt text.
        system: Optional system prompt prepended to the user prompt.
        max_tokens: Response token cap forwarded to each leg.
        api_key: Explicit Groq key published to the environment for the
            ``groq:`` legs; empty resolves the key from ``payload.json``.
        members: Optional chain override (tests, per-task chains).
        executor: Optional leg executor override; defaults to the
            ``modules.llm_factory`` spec executor.
        health: Optional breaker registry override; defaults to the
            shared ``modules.llm_pool`` registry.
        record: When True, append outcomes to the pool usage ledger.

    Returns:
        An :class:`OrchestratorResult`; ``ok`` is False with the help
        message in ``text`` when every member failed.
    """
    if not (prompt or "").strip():
        return OrchestratorResult(
            text="",
            backend="error",
            notice="[!] Empty prompt: the orchestrator chain was not contacted.",
        )
    _ensure_groq_env_key(api_key)
    walk = executor or _factory_executor
    if health is None:
        health = _default_health()
    chain = _dedupe(sort_members(list(members) if members else pool_chain()))
    primary = chain[0] if chain else None
    attempts: list[tuple[str, str]] = []
    specs: list[str] = []
    skipped: list[dict] = []
    served = _walk_chain(
        chain, walk, health, attempts, specs, max_tokens, system, prompt, record, healthy_only=True, skipped=skipped
    )
    if served is None and skipped:
        served = _walk_chain(
            skipped, walk, health, attempts, specs, max_tokens, system, prompt, record, healthy_only=False, skipped=[]
        )
    if served is None:
        return _exhausted_result(attempts, specs, record)
    result = OrchestratorResult(
        text=served["text"],
        member=str(served["member"].get("name", "")),
        model=str(served["member"].get("model", "")),
        model_name=_bare_model_name(str(served["member"].get("model", ""))),
        backend=backend_kind(str(served["member"].get("model", ""))),
        fallback_used=primary is None or str(served["member"].get("name", "")) != str(primary.get("name", "")),
    )
    if result.fallback_used and primary is not None:
        result.notice = _notice_fallback(primary, attempts, served["member"])
    return result


def _bare_model_name(model_spec: str) -> str:
    """Strip the provider prefix from a model spec when present."""
    head, sep, tail = (model_spec or "").partition(":")
    if sep and head.strip().lower() in ("groq", "ollama", "llamacpp", "pi", "toposwarm", "auto"):
        return tail.strip()
    return (model_spec or "").strip()


def _walk_chain(
    chain: list[dict],
    walk: Executor,
    health: Any | None,
    attempts: list[tuple[str, str]],
    specs: list[str],
    max_tokens: int,
    system: str,
    prompt: str,
    record: bool,
    healthy_only: bool,
    skipped: list[dict],
) -> dict[str, Any] | None:
    """Walk the chain and return the serving attempt, or None.

    Args:
        chain: Weight-sorted member list.
        walk: Leg executor.
        health: Breaker registry or None.
        attempts: Accumulator of ``(member, error)`` failures.
        specs: Accumulator of model specs for every executed attempt.
        max_tokens: Response token cap.
        system: System prompt text.
        prompt: User prompt text.
        record: Ledger flag.
        healthy_only: When True, unhealthy members are skipped.
        skipped: Accumulator collecting members parked by the breaker.

    Returns:
        ``{"member": member, "text": answer}`` on success, else None.
    """
    breaker = _breaker_active()
    for member in chain:
        name = str(member.get("name", "?"))
        if healthy_only and health is not None and breaker:
            try:
                if not health.healthy(name):
                    attempts.append((name, "skipped: parked by the health breaker"))
                    skipped.append(member)
                    continue
            except Exception:
                pass
        combined = f"{system}\n\n{prompt}" if system else prompt
        model_spec = str(member.get("model", ""))
        try:
            text = str(walk(model_spec, combined, max_tokens) or "")
        except Exception as exc:
            error = str(exc)[:ERROR_TEXT_LIMIT]
            attempts.append((name, error))
            specs.append(model_spec)
            if health is not None and breaker:
                try:
                    health.report_failure(name, str(exc))
                except Exception:
                    pass
            if record:
                _ledger_record(name, False, error)
            continue
        if is_error_reply(text):
            error = text.strip()[:ERROR_TEXT_LIMIT]
            attempts.append((name, error))
            specs.append(model_spec)
            if health is not None and breaker:
                try:
                    health.report_failure(name, error)
                except Exception:
                    pass
            if record:
                _ledger_record(name, False, error)
            continue
        if health is not None:
            try:
                health.report_success(name)
            except Exception:
                pass
        if record:
            _ledger_record(name, True, text[:200])
        return {"member": member, "text": text}
    return None


def _exhausted_result(attempts: list[tuple[str, str]], specs: list[str], record: bool) -> OrchestratorResult:
    """Build the help-message result returned on total chain failure.

    Args:
        attempts: Every failed attempt as ``(member, error)``.
        specs: Model specs of every executed attempt.
        record: Ledger flag (kept for symmetry; failures already recorded).

    Returns:
        Error result whose text is :data:`HELP_MESSAGE` and whose notice
        names every attempted member with its error.
    """
    del record
    tried = "; ".join(f"'{name}' ({error})" for name, error in attempts)
    notice = "[!] All LLM chain members failed."
    if tried:
        notice += f" Tried: {tried}."
    return OrchestratorResult(
        text=HELP_MESSAGE,
        backend="error",
        notice=notice,
        attempts=list(attempts),
        attempted_specs=list(specs),
    )


__all__ = [
    "HELP_MESSAGE",
    "Executor",
    "OrchestratorResult",
    "backend_kind",
    "complete_with_fallback",
    "pool_chain",
    "sort_members",
]
