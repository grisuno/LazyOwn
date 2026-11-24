"""Token and turn budgets with wrap-up reservation for the lazy loop.

Ports the ARTEX budget idea: LLM spend is measured per task and per
intent, a wrap-up reserve is kept aside, and the engine termination
policy is configurable between ``save_tokens`` (quit cleanly when the
budget is spent) and ``try_hard`` (keep the loop running, degrade to
the deterministic layer only). Tokens are estimated from prompt and
completion characters because the providers behind :mod:`modules.llm_pool`
do not expose usage counters; the estimate is deterministic and
monotonic, which is all a budget gate needs.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from modules.loop.state_db import thread_connection

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS token_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    task_id TEXT NOT NULL,
    intent_id INTEGER NOT NULL DEFAULT 0,
    member TEXT NOT NULL DEFAULT '',
    prompt_tokens INTEGER NOT NULL,
    completion_tokens INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_token_usage_task ON token_usage(task_id);
"""

CHARS_PER_TOKEN = 4
DEFAULT_MODE = "try_hard"
MODES = ("save_tokens", "try_hard")
DEFAULT_MAX_TOKENS_PER_TASK = 2_000_000
DEFAULT_MAX_TOKENS_PER_INTENT = 150_000
DEFAULT_WRAPUP_RESERVE_PCT = 5.0
DEFAULT_WRAPUP_RESERVE_TOKENS = 20_000
SINK_LIMIT_CHARS = 200_000
USAGES = ("continue", "deterministic_only", "wrapup")


def estimate_tokens(chars: int) -> int:
    """Estimate token count from character count (deterministic heuristic)."""
    return max(1, int(chars or 0) // CHARS_PER_TOKEN)


def register_llm_sink() -> None:
    """Wire the ledger into the LLM pool usage sink (idempotent)."""
    from modules import llm_pool

    ledger = shared_ledger()

    def _sink(member: str, prompt_chars: int, completion_chars: int) -> None:
        ledger.charge_chars(member, prompt_chars, completion_chars)

    llm_pool.register_usage_sink(_sink)


_shared_ledger = None


def shared_ledger() -> TokenLedger:
    """Return the process-wide ledger bound to the default database."""
    global _shared_ledger
    if _shared_ledger is None:
        _shared_ledger = TokenLedger()
    return _shared_ledger


class TokenLedger:
    """Token usage accounting persisted in SQLite.

    Args:
        db_path: Optional SQLite path override (tests).
    """

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path
        conn = self._conn()
        conn.executescript(SCHEMA_SQL)
        conn.commit()

    def _conn(self):
        """Return the per-thread connection."""
        return thread_connection(self._db_path)

    def charge_chars(
        self, member: str, prompt_chars: int, completion_chars: int, task_id: str = "", intent_id: int = 0
    ) -> None:
        """Charge one estimated-token usage row from raw characters."""
        prompt_tokens = estimate_tokens(min(int(prompt_chars or 0), SINK_LIMIT_CHARS))
        completion_tokens = estimate_tokens(min(int(completion_chars or 0), SINK_LIMIT_CHARS))
        conn = self._conn()
        try:
            conn.execute(
                "INSERT INTO token_usage (ts, task_id, intent_id, member, prompt_tokens, completion_tokens) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (time.time(), str(task_id), int(intent_id), str(member or ""), prompt_tokens, completion_tokens),
            )
            conn.commit()
        except Exception:
            pass

    def charge(
        self, task_id: str, prompt_tokens: int, completion_tokens: int, intent_id: int = 0, member: str = ""
    ) -> None:
        """Charge one explicit token usage row."""
        conn = self._conn()
        try:
            conn.execute(
                "INSERT INTO token_usage (ts, task_id, intent_id, member, prompt_tokens, completion_tokens) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    time.time(),
                    str(task_id),
                    int(intent_id),
                    str(member or ""),
                    int(prompt_tokens),
                    int(completion_tokens),
                ),
            )
            conn.commit()
        except Exception:
            pass

    def usage(self, task_id: str, intent_id: int | None = None) -> dict[str, int]:
        """Return prompt/completion/total token sums for a task or intent."""
        conn = self._conn()
        try:
            if intent_id is None:
                row = conn.execute(
                    "SELECT COALESCE(SUM(prompt_tokens),0) AS p, COALESCE(SUM(completion_tokens),0) AS c "
                    "FROM token_usage WHERE task_id = ?",
                    (task_id,),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT COALESCE(SUM(prompt_tokens),0) AS p, COALESCE(SUM(completion_tokens),0) AS c "
                    "FROM token_usage WHERE task_id = ? AND intent_id = ?",
                    (task_id, int(intent_id)),
                ).fetchone()
        except Exception:
            return {"prompt": 0, "completion": 0, "total": 0}
        prompt = int(row["p"] or 0)
        completion = int(row["c"] or 0)
        return {"prompt": prompt, "completion": completion, "total": prompt + completion}

    def reset(self, task_id: str) -> int:
        """Delete usage rows for one task; returns removed count."""
        conn = self._conn()
        try:
            cur = conn.execute("DELETE FROM token_usage WHERE task_id = ?", (task_id,))
            conn.commit()
            return cur.rowcount
        except Exception:
            return 0

    def counts(self) -> dict[str, int]:
        """Return total rows and token sums (observability)."""
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT COUNT(*) AS n, COALESCE(SUM(prompt_tokens),0) AS p, COALESCE(SUM(completion_tokens),0) AS c "
                "FROM token_usage"
            ).fetchone()
        except Exception:
            return {"rows": 0, "prompt": 0, "completion": 0}
        return {
            "rows": int(row["n"] or 0),
            "prompt": int(row["p"] or 0),
            "completion": int(row["c"] or 0),
        }


@dataclass
class TerminationPolicy:
    """Configured termination mode and spend caps for one run."""

    mode: str = DEFAULT_MODE
    max_tokens_per_task: int = DEFAULT_MAX_TOKENS_PER_TASK
    max_tokens_per_intent: int = DEFAULT_MAX_TOKENS_PER_INTENT
    wrapup_reserve_pct: float = DEFAULT_WRAPUP_RESERVE_PCT
    wrapup_reserve_tokens: int = DEFAULT_WRAPUP_RESERVE_TOKENS

    def __post_init__(self) -> None:
        """Normalise the mode so an invalid value always falls back."""
        mode = str(self.mode or DEFAULT_MODE).strip().lower()
        self.mode = mode if mode in MODES else DEFAULT_MODE

    @classmethod
    def from_orchestrator(cls) -> TerminationPolicy:
        """Build the policy from the active orchestrator profile."""
        try:
            from modules import orchestrator_config as oc

            section = dict(oc.profile_config().get("termination") or {})
        except Exception:
            section = {}
        mode = str(section.get("mode") or DEFAULT_MODE).strip().lower()
        if mode not in MODES:
            mode = DEFAULT_MODE

        def _int(key: str, fallback: int) -> int:
            try:
                return max(0, int(section.get(key, fallback)))
            except (TypeError, ValueError):
                return fallback

        def _float(key: str, fallback: float) -> float:
            try:
                return min(50.0, max(0.0, float(section.get(key, fallback))))
            except (TypeError, ValueError):
                return fallback

        return cls(
            mode=mode,
            max_tokens_per_task=_int("max_tokens_per_task", DEFAULT_MAX_TOKENS_PER_TASK),
            max_tokens_per_intent=_int("max_tokens_per_intent", DEFAULT_MAX_TOKENS_PER_INTENT),
            wrapup_reserve_pct=_float("wrapup_reserve_pct", DEFAULT_WRAPUP_RESERVE_PCT),
            wrapup_reserve_tokens=_int("wrapup_reserve_tokens", DEFAULT_WRAPUP_RESERVE_TOKENS),
        )

    def wrapup_reserve(self, max_tokens: int) -> int:
        """Return the reserved token count that the wrap-up must keep."""
        reserved = 0
        if self.wrapup_reserve_pct > 0:
            reserved += int(max(0, max_tokens) * self.wrapup_reserve_pct / 100.0)
        if self.wrapup_reserve_tokens > 0:
            reserved = max(reserved, self.wrapup_reserve_tokens)
        return min(reserved, max(0, max_tokens))

    def guard(self, task_id: str, ledger: TokenLedger, intent_id: int = 0) -> dict:
        """Return the spend verdict and the action the loop must take.

        Returns:
            Dict with ``ok`` (bool), ``reason`` (str), ``action`` in
            :data:`USAGES`, plus ``used`` and ``limits`` snapshots.
            ``save_tokens`` fails the whole loop to a clean wrap-up;
            ``try_hard`` keeps the loop alive but blocks further LLM
            turns once the budget is spent.
        """
        usage = ledger.usage(task_id)
        used = usage["total"]
        limit = max(0, int(self.max_tokens_per_task))
        reserve = self.wrapup_reserve(limit)
        spendable = max(0, limit - reserve)
        over_intent = False
        if intent_id:
            intent_used = ledger.usage(task_id, intent_id=intent_id)["total"]
            over_intent = 0 < self.max_tokens_per_intent < intent_used
        if used >= spendable:
            if self.mode == "save_tokens":
                action = "wrapup"
            else:
                action = "deterministic_only"
            return {
                "ok": False,
                "reason": f"token budget {used}/{limit}",
                "action": action,
                "used": usage,
                "limits": {"max_tokens_per_task": limit, "wrapup_reserve": reserve},
            }
        if over_intent:
            return {
                "ok": False,
                "reason": f"intent token budget {intent_used}/{self.max_tokens_per_intent}",
                "action": "deterministic_only",
                "used": usage,
                "limits": {"max_tokens_per_intent": self.max_tokens_per_intent},
            }
        return {
            "ok": True,
            "reason": "",
            "action": "continue",
            "used": usage,
            "limits": {"max_tokens_per_task": limit, "wrapup_reserve": reserve},
        }
