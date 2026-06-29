"""LLM budget cap and per call token counter.

The framework exposes several LLM backed entry points. The framework
never enforced a daily cost cap. The module below is the
single source of truth for the LLM budget contract. The module is
imported by :mod:`modules.llm_factory` so every backend the factory
returns is wrapped with the guard.

The contract is the wrapper refuses the call when the daily budget is
exhausted or the per call token cap is exceeded. The contract never
raises a non budget related exception. The contract persists the
ledger to ``sessions/llm_budget.json`` so a process restart does not
reset the counter inside the same calendar day.

Pricing follows the OpenAI style model where the operator declares a
price per million input tokens and a price per million output
tokens. The default price table covers Groq and Ollama. The Ollama
prices are zero because the operator runs the model on the local
host. The operator may override every price through ``payload.json``.

The module imports nothing from the LazyOwn project beyond
:mod:`core.config` and :mod:`core.dependencies` so a fresh checkout
can use the module without activating the framework.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Protocol

DEFAULT_DAILY_BUDGET_USD = 1.0
DEFAULT_PER_CALL_TOKEN_CAP = 8000
DEFAULT_RESET_AT_UTC = "00:00"
DEFAULT_LEDGER_FILENAME = "llm_budget.json"
TOKEN_BUDGET_FIELDS = (
    "llm_daily_budget_usd",
    "llm_per_call_token_cap",
    "llm_budget_enabled",
    "llm_reset_at_utc",
    "llm_model_prices",
)
SESSIONS_DIR_ENV = "LAZYOWN_SESSIONS_DIR"
GROQ_PRICE_INPUT_USD_PER_M = 0.59
GROQ_PRICE_OUTPUT_USD_PER_M = 0.79
OLLAMA_PRICE_INPUT_USD_PER_M = 0.0
OLLAMA_PRICE_OUTPUT_USD_PER_M = 0.0


class BudgetExceeded(RuntimeError):
    """Raised when a call would breach the daily budget or the token cap."""


class LLMBackendLike(Protocol):
    """Structural type the wrapper requires from the wrapped backend."""

    def generate(self, prompt: str) -> Any: ...

    def stream_generate(self, prompt: str) -> Any: ...

    def complete(self, system: str, user: str, max_tokens: int, temperature: float) -> str: ...


@dataclass(frozen=True)
class ModelPrice:
    """Price for a single model expressed in United States dollars per million tokens.

    Attributes:
        input: Cost per million input tokens.
        output: Cost per million output tokens.
    """

    input: float
    output: float

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> ModelPrice:
        """Build a ModelPrice from a JSON friendly mapping.

        Args:
            data: Mapping that carries the ``input`` and ``output`` keys.
        Returns:
            The ModelPrice the guard consumes.
        Raises:
            ValueError: when the mapping is missing the required keys.
        """
        try:
            return cls(
                input=float(data["input"]),
                output=float(data["output"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"model price mapping must carry numeric 'input' and 'output' keys, got {data!r}"
            ) from error


@dataclass(frozen=True)
class BudgetConfig:
    """Runtime configuration for the LLM budget guard.

    Attributes:
        daily_budget_usd: Maximum amount the operator allows the
            framework to spend on a single calendar day.
        per_call_token_cap: Maximum number of input tokens a single
            call may consume. The cap is a safety net that prevents a
            runaway prompt from consuming the whole budget in one shot.
        reset_at_utc: Time of day, in HH:MM format and UTC, when the
            ledger rolls over and the day counter restarts.
        model_prices: Per model price table. The keys are model
            identifiers. The values are :class:`ModelPrice` instances
            expressed in United States dollars per million tokens.
        enabled: When False the guard passes the call through without
            recording a charge. The default is True so the operator
            who configures a budget is protected by default.
        ledger_path: Absolute path of the JSON file the ledger writes.
    """

    daily_budget_usd: float
    per_call_token_cap: int
    reset_at_utc: str
    model_prices: dict[str, ModelPrice] = field(default_factory=dict)
    enabled: bool = True
    ledger_path: Path = field(default_factory=lambda: Path("/dev/null"))


@dataclass(frozen=True)
class LedgerEntry:
    """Single charge the ledger records.

    Attributes:
        model: Model identifier the wrapper recorded.
        input_tokens: Number of input tokens the wrapper counted.
        output_tokens: Number of output tokens the wrapper recorded.
        cost_usd: Dollar cost the wrapper charged for the call.
        timestamp: ISO 8601 timestamp the wrapper wrote the entry.
    """

    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    timestamp: str


def _today_utc(now: datetime | None = None) -> str:
    """Return the current calendar day in UTC as an ISO date.

    Args:
        now: Optional override for the current time. Tests pass an
            explicit value to drive the roll over logic.
    Returns:
        The calendar day as a YYYY-MM-DD string.
    """
    moment = now or datetime.now(timezone.utc)
    return moment.date().isoformat()


def _now_iso(now: datetime | None = None) -> str:
    """Return the current time as an ISO 8601 UTC string.

    Args:
        now: Optional override for the current time.
    Returns:
        The timestamp in ISO 8601 format with explicit UTC offset.
    """
    moment = now or datetime.now(timezone.utc)
    return moment.isoformat()


@dataclass
class BudgetLedger:
    """In memory ledger that persists the daily spend to disk.

    Attributes:
        path: Absolute path of the JSON file the ledger reads on
            construction and writes after every charge.
        today: Calendar day the ledger considers the current day.
            Tests override the value to drive the day roll over.
    """

    path: Path
    today: str = field(default_factory=_today_utc)

    def _empty_state(self) -> dict[str, Any]:
        """Return the empty state the ledger starts from when no file exists."""
        return {"day": self.today, "entries": []}

    def _load(self) -> dict[str, Any]:
        """Load the ledger state from disk.

        Returns:
            The parsed state dictionary. Empty state when the file
            does not exist or is malformed.
        """
        if not self.path.exists():
            return self._empty_state()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return self._empty_state()
        if not isinstance(data, dict):
            return self._empty_state()
        if data.get("day") != self.today:
            return self._empty_state()
        entries = data.get("entries")
        if not isinstance(entries, list):
            return self._empty_state()
        return {"day": self.today, "entries": entries}

    def _save(self, state: dict[str, Any]) -> None:
        """Persist the ledger state to disk atomically.

        Args:
            state: State dictionary the ledger serialises to JSON.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def _state(self) -> dict[str, Any]:
        """Return the in memory state, reloading from disk when empty."""
        if not hasattr(self, "_cached_state"):
            object.__setattr__(self, "_cached_state", self._load())
        return self._cached_state  # type: ignore[attr-defined]

    def record(self, entry: LedgerEntry) -> None:
        """Append a charge to the ledger and persist the new state.

        Args:
            entry: Charge the guard computed.
        """
        state = self._state()
        state["day"] = self.today
        state["entries"].append(
            {
                "model": entry.model,
                "input_tokens": entry.input_tokens,
                "output_tokens": entry.output_tokens,
                "cost_usd": entry.cost_usd,
                "timestamp": entry.timestamp,
            }
        )
        self._save(state)

    def spent_today(self) -> float:
        """Return the dollar amount the ledger charged for the current day."""
        state = self._state()
        return float(sum(float(item.get("cost_usd", 0.0)) for item in state["entries"]))

    def calls_today(self) -> int:
        """Return the number of calls the ledger recorded for the current day."""
        state = self._state()
        return len(state["entries"])

    def reset(self) -> None:
        """Clear the ledger for the current day and persist the empty state."""
        empty = self._empty_state()
        object.__setattr__(self, "_cached_state", empty)
        self._save(empty)


class TokenEstimator:
    """Token counter the guard consumes.

    The estimator wraps ``tiktoken`` when the dependency is available.
    When ``tiktoken`` is missing the estimator falls back to a
    whitespace tokeniser that still produces a deterministic count.
    The fallback exists so the guard never crashes the operator who
    runs the framework on a host without ``tiktoken`` installed.
    """

    def __init__(self, encoding_name: str = "cl100k_base") -> None:
        self._encoding_name = encoding_name
        self._encoding = self._load_encoding(encoding_name)

    @staticmethod
    def _load_encoding(encoding_name: str) -> Any:
        """Load the tiktoken encoding or return a fallback callable."""
        try:
            import tiktoken  # type: ignore[import-not-found]

            return tiktoken.get_encoding(encoding_name)
        except Exception:
            return None

    def count(self, text: str) -> int:
        """Return the number of tokens the input text contains.

        Args:
            text: Prompt or completion the guard measures.
        Returns:
            Non negative integer count. Zero for the empty string.
        """
        if not text:
            return 0
        if self._encoding is None:
            return len(text.split())
        try:
            return len(self._encoding.encode(text))
        except Exception:
            return len(text.split())


class BudgetGuard:
    """Proxy that enforces the budget around a wrapped backend.

    Attributes:
        config: Active runtime configuration.
        estimator: Token estimator the guard uses.
        ledger: Persistent ledger the guard updates.
    """

    def __init__(
        self,
        config: BudgetConfig,
        estimator: TokenEstimator,
        ledger: BudgetLedger | None = None,
    ) -> None:
        self.config = config
        self.estimator = estimator
        self.ledger = ledger or BudgetLedger(path=config.ledger_path)

    def price_for(self, model: str) -> ModelPrice:
        """Return the price the guard applies to a model identifier.

        Args:
            model: Model identifier the caller asked for.
        Returns:
            The configured price when the operator declared one. The
            zero price for Ollama when the model is unknown so the
            local model never charges the budget.
        """
        if model in self.config.model_prices:
            return self.config.model_prices[model]
        return ModelPrice(input=OLLAMA_PRICE_INPUT_USD_PER_M, output=OLLAMA_PRICE_OUTPUT_USD_PER_M)

    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Return the dollar cost the guard would charge for a call.

        Args:
            model: Model identifier the caller asked for.
            input_tokens: Input token count the estimator reported.
            output_tokens: Output token count the caller declared.
        Returns:
            Dollar cost expressed in United States dollars.
        """
        price = self.price_for(model)
        return float(input_tokens) * price.input / 1_000_000.0 + float(output_tokens) * price.output / 1_000_000.0

    def estimate_and_check(
        self,
        prompt: str,
        model: str,
        output_tokens: int = 0,
    ) -> LedgerEntry:
        """Check the budget and record a charge when the call fits.

        Args:
            prompt: Prompt the caller will forward to the backend.
            model: Model identifier the caller will use.
            output_tokens: Output token count the caller declares in
                advance. The guard uses the value to estimate the cost
                when the caller knows the answer length. The guard
                falls back to zero when the caller cannot predict it.
        Returns:
            The LedgerEntry the guard recorded. The caller never has
            to inspect the entry. The entry exists so tests can pin
            the cost the guard charged.
        Raises:
            BudgetExceeded: when the per call token cap is exceeded,
                the daily budget is exhausted, or the budget is
                disabled and the cap is zero.
        """
        if not self.config.enabled:
            return LedgerEntry(
                model=model,
                input_tokens=self.estimator.count(prompt),
                output_tokens=output_tokens,
                cost_usd=0.0,
                timestamp=_now_iso(),
            )
        input_tokens = self.estimator.count(prompt)
        if self.config.per_call_token_cap and input_tokens > self.config.per_call_token_cap:
            raise BudgetExceeded(f"per call token cap exceeded: {input_tokens} > {self.config.per_call_token_cap}")
        cost = self.estimate_cost(model=model, input_tokens=input_tokens, output_tokens=output_tokens)
        spent = self.ledger.spent_today()
        if spent + cost > self.config.daily_budget_usd:
            raise BudgetExceeded(
                f"daily LLM budget exhausted: spent {spent:.6f} + cost {cost:.6f} > limit {self.config.daily_budget_usd:.6f}"
            )
        entry = LedgerEntry(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            timestamp=_now_iso(),
        )
        self.ledger.record(entry)
        return entry


class BudgetedBackend:
    """Transparent proxy the factory returns in place of the raw backend.

    Attributes:
        inner: Concrete backend the proxy delegates to.
        guard: Guard that enforces the budget.
        model: Model identifier the proxy records on every call.
    """

    def __init__(self, inner: Any, guard: BudgetGuard, model: str) -> None:
        self.inner = inner
        self.guard = guard
        self.model = model

    def generate(self, prompt: str) -> str:
        """Forward a non streaming call and record a charge."""
        self.guard.estimate_and_check(prompt=prompt, model=self.model)
        result = self.inner.generate(prompt)
        if isinstance(result, str):
            return result
        return "".join(chunk for chunk in result if isinstance(chunk, str))

    def stream_generate(self, prompt: str) -> Any:
        """Forward a streaming call. The charge is recorded up front."""
        self.guard.estimate_and_check(prompt=prompt, model=self.model)
        return self.inner.stream_generate(prompt)

    def complete(self, system: str, user: str, max_tokens: int, temperature: float) -> str:
        """Forward a role aware call. The prompt includes the system block."""
        prompt = f"[SYSTEM]\n{system}\n\n[USER]\n{user}"
        self.guard.estimate_and_check(prompt=prompt, model=self.model, output_tokens=max_tokens)
        return self.inner.complete(system=system, user=user, max_tokens=max_tokens, temperature=temperature)


def default_model_prices() -> dict[str, ModelPrice]:
    """Return the default price table the guard ships with.

    Returns:
        A dictionary keyed by model identifier. The values are
        :class:`ModelPrice` instances.
    """
    return {
        "llama-3.3-70b-versatile": ModelPrice(
            input=GROQ_PRICE_INPUT_USD_PER_M,
            output=GROQ_PRICE_OUTPUT_USD_PER_M,
        ),
        "deepseek-r1:1.5b": ModelPrice(
            input=OLLAMA_PRICE_INPUT_USD_PER_M,
            output=OLLAMA_PRICE_OUTPUT_USD_PER_M,
        ),
    }


def default_sessions_dir() -> Path:
    """Return the directory the ledger writes to by default.

    Returns:
        Absolute path. The directory is the LazyOwn ``sessions``
        directory under the current working directory. The operator
        may override the value through the ``LAZYOWN_SESSIONS_DIR``
        environment variable.
    """
    override = os.environ.get(SESSIONS_DIR_ENV)
    if override:
        return Path(override).expanduser().resolve()
    return Path.cwd() / "sessions"


def _coerce_bool(value: Any, default: bool) -> bool:
    """Coerce a payload value into a boolean.

    Args:
        value: Raw value from the payload mapping.
        default: Value to return when the raw value is not a boolean.
    Returns:
        The coerced boolean.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "on"}:
            return True
        if lowered in {"false", "0", "no", "off"}:
            return False
    return default


def _coerce_price_table(value: Any) -> dict[str, ModelPrice]:
    """Coerce a payload value into the price table.

    Args:
        value: Raw value from the payload mapping. The value is a
            dictionary keyed by model identifier whose values are
            mappings with ``input`` and ``output`` keys.
    Returns:
        The price table the guard consumes. Empty when the payload
        omits the key.
    """
    if not isinstance(value, Mapping):
        return {}
    table: dict[str, ModelPrice] = {}
    for model, raw in value.items():
        if not isinstance(model, str) or not isinstance(raw, Mapping):
            continue
        try:
            table[model] = ModelPrice.from_mapping(raw)
        except ValueError:
            continue
    return table


def _coerce_positive_float(value: Any, default: float) -> float:
    """Coerce a payload value into a non negative float.

    Args:
        value: Raw value from the payload mapping.
        default: Value to return when the raw value is not a number.
    Returns:
        The coerced float. Negative values are clamped to zero.
    """
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return max(result, 0.0)


def _coerce_positive_int(value: Any, default: int) -> int:
    """Coerce a payload value into a non negative integer.

    Args:
        value: Raw value from the payload mapping.
        default: Value to return when the raw value is not an integer.
    Returns:
        The coerced integer. Negative values are clamped to zero.
    """
    try:
        result = int(value)
    except (TypeError, ValueError):
        return default
    return max(result, 0)


def load_budget_config(
    payload: Mapping[str, Any],
    sessions_dir: Path | None = None,
) -> BudgetConfig:
    """Build a BudgetConfig from a payload mapping.

    Args:
        payload: Mapping derived from ``payload.json``.
        sessions_dir: Directory the ledger writes to. Defaults to the
            LazyOwn ``sessions`` directory.
    Returns:
        The BudgetConfig the guard consumes.
    """
    ledger_dir = Path(sessions_dir) if sessions_dir is not None else default_sessions_dir()
    table = _coerce_price_table(payload.get("llm_model_prices"))
    if not table:
        table = default_model_prices()
    return BudgetConfig(
        daily_budget_usd=_coerce_positive_float(
            payload.get("llm_daily_budget_usd"),
            DEFAULT_DAILY_BUDGET_USD,
        ),
        per_call_token_cap=_coerce_positive_int(
            payload.get("llm_per_call_token_cap"),
            DEFAULT_PER_CALL_TOKEN_CAP,
        ),
        reset_at_utc=str(payload.get("llm_reset_at_utc") or DEFAULT_RESET_AT_UTC),
        model_prices=table,
        enabled=_coerce_bool(payload.get("llm_budget_enabled"), True),
        ledger_path=ledger_dir / DEFAULT_LEDGER_FILENAME,
    )


def read_budget_status(
    payload: Mapping[str, Any],
    sessions_dir: Path | None = None,
) -> dict[str, Any]:
    """Return a structured snapshot of the current budget.

    Args:
        payload: Mapping derived from ``payload.json``.
        sessions_dir: Directory the ledger writes to.
    Returns:
        Dictionary the CLI command and the MCP tool surface to the
        operator. Keys are stable across releases.
    """
    config = load_budget_config(payload=payload, sessions_dir=sessions_dir)
    ledger = BudgetLedger(path=config.ledger_path)
    spent = ledger.spent_today()
    limit = config.daily_budget_usd
    return {
        "enabled": config.enabled,
        "limit_usd": limit,
        "spent_usd": spent,
        "remaining_usd": max(limit - spent, 0.0),
        "calls_today": ledger.calls_today(),
        "per_call_token_cap": config.per_call_token_cap,
        "model_prices": {
            model: {"input": price.input, "output": price.output} for model, price in config.model_prices.items()
        },
        "ledger_path": str(config.ledger_path),
    }


def format_budget_status(config: BudgetConfig, ledger: BudgetLedger) -> str:
    """Render the budget status as a human readable block.

    Args:
        config: Active runtime configuration.
        ledger: Ledger the operator wants to inspect.
    Returns:
        Multi line text the CLI command prints. The block is plain
        text so the operator can pipe it to ``grep`` or ``awk``.
    """
    spent = ledger.spent_today()
    remaining = max(config.daily_budget_usd - spent, 0.0)
    lines = [
        "LLM budget status",
        f"enabled         : {config.enabled}",
        f"daily limit USD : {config.daily_budget_usd:.6f}",
        f"spent USD       : {spent:.6f}",
        f"remaining USD   : {remaining:.6f}",
        f"calls today     : {ledger.calls_today()}",
        f"per call cap    : {config.per_call_token_cap}",
        f"reset at UTC    : {config.reset_at_utc}",
        f"ledger path     : {config.ledger_path}",
    ]
    return "\n".join(lines)


def _has_required_methods(backend: Any) -> bool:
    """Return True when the backend exposes the three call surface methods.

    Args:
        backend: Object the factory returns.
    Returns:
        True when the object exposes ``generate``, ``stream_generate``,
        and ``complete``. False otherwise.
    """
    for method_name in ("generate", "stream_generate", "complete"):
        if not callable(getattr(backend, method_name, None)):
            return False
    return True


def wrap_backend_with_budget(
    backend: Any,
    config: BudgetConfig,
    estimator: TokenEstimator,
    model: str,
    ledger: BudgetLedger | None = None,
) -> BudgetedBackend:
    """Wrap a concrete backend with a budgeted proxy.

    Args:
        backend: Concrete backend the factory returns.
        config: Active runtime configuration.
        estimator: Token estimator the proxy uses.
        model: Model identifier the proxy records on every call.
        ledger: Optional ledger. The factory passes ``None`` and lets
            the guard build the default ledger.
    Returns:
        The proxy the caller forwards every request through.
    Raises:
        TypeError: when the backend does not expose the three call
            surface methods the proxy delegates to.
    """
    if not _has_required_methods(backend):
        raise TypeError(
            "wrap_backend_with_budget requires a backend that exposes generate, stream_generate, and complete"
        )
    guard = BudgetGuard(config=config, estimator=estimator, ledger=ledger)
    return BudgetedBackend(inner=backend, guard=guard, model=model)


__all__ = [
    "DEFAULT_DAILY_BUDGET_USD",
    "DEFAULT_PER_CALL_TOKEN_CAP",
    "DEFAULT_RESET_AT_UTC",
    "DEFAULT_LEDGER_FILENAME",
    "GROQ_PRICE_INPUT_USD_PER_M",
    "GROQ_PRICE_OUTPUT_USD_PER_M",
    "OLLAMA_PRICE_INPUT_USD_PER_M",
    "OLLAMA_PRICE_OUTPUT_USD_PER_M",
    "SESSIONS_DIR_ENV",
    "TOKEN_BUDGET_FIELDS",
    "BudgetConfig",
    "BudgetExceeded",
    "BudgetGuard",
    "BudgetLedger",
    "BudgetedBackend",
    "LedgerEntry",
    "LLMBackendLike",
    "ModelPrice",
    "TokenEstimator",
    "default_model_prices",
    "default_sessions_dir",
    "format_budget_status",
    "load_budget_config",
    "read_budget_status",
    "wrap_backend_with_budget",
]
