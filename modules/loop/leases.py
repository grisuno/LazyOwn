"""Claim leases with heartbeat for the lazy loop frontier.

Ports the ARTEX lease model (HeartbeatIntentClaim / SettleIntentClaim)
onto SQLite: a claim is a transactional row under ``BEGIN IMMEDIATE``,
extended by heartbeats, and provably dead claims are swept back to
pending. The in-memory JSON graph keeps being the display truth; the
lease store owns the cross-process "who owns this intent now" question
and survives crashes, which the flock-CAS alone never did.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass

from modules.loop.state_db import thread_connection

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS loop_leases (
    task_id TEXT NOT NULL,
    node_id INTEGER NOT NULL,
    worker TEXT NOT NULL DEFAULT '',
    created REAL NOT NULL,
    expires_at REAL NOT NULL,
    settled INTEGER NOT NULL DEFAULT 0,
    settled_at REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (task_id, node_id)
);
"""

DEFAULT_LEASE_TTL_SEC = 900.0
SETTLED_RETENTION_SEC = 7 * 24 * 3600.0


@dataclass
class Lease:
    """One live claim over a task intent."""

    task_id: str
    node_id: int
    worker: str
    expires_at: float


class LeaseStore:
    """Transactional claim leases keyed by (task_id, node_id).

    Args:
        db_path: Optional SQLite path override (tests); defaults to
            ``sessions/db/loop_state.db``.
    """

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path
        self._local = threading.local()
        conn = self._conn()
        conn.executescript(SCHEMA_SQL)
        conn.commit()

    def _conn(self):
        """Return the per-thread connection."""
        return thread_connection(self._db_path)

    def _now(self) -> float:
        """Return the reference clock."""
        return time.time()

    def try_claim(
        self, task_id: str, node_id: int, worker: str = "", ttl_sec: float = DEFAULT_LEASE_TTL_SEC
    ) -> Lease | None:
        """Acquire or refresh the lease for one intent, or fail when held.

        The CAS runs inside ``BEGIN IMMEDIATE``: only one concurrent
        claimer (or process) wins the row; a settled intent never
        re-claims.

        Returns:
            The new :class:`Lease` when the claim is taken, else None.
        """
        now = self._now()
        conn = self._conn()
        try:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT settled, expires_at FROM loop_leases WHERE task_id = ? AND node_id = ?",
                (task_id, int(node_id)),
            ).fetchone()
            if row is None:
                conn.execute(
                    "INSERT INTO loop_leases (task_id, node_id, worker, created, expires_at) VALUES (?, ?, ?, ?, ?)",
                    (task_id, int(node_id), str(worker or ""), now, now + float(ttl_sec)),
                )
            elif int(row["settled"]):
                conn.execute("ROLLBACK")
                return None
            elif float(row["expires_at"]) > now:
                conn.execute("ROLLBACK")
                return None
            else:
                conn.execute(
                    "UPDATE loop_leases SET worker = ?, created = ?, expires_at = ?, settled = 0, settled_at = 0 "
                    "WHERE task_id = ? AND node_id = ?",
                    (str(worker or ""), now, now + float(ttl_sec), task_id, int(node_id)),
                )
            conn.commit()
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            return None
        return Lease(task_id=task_id, node_id=int(node_id), worker=str(worker or ""), expires_at=now + float(ttl_sec))

    def heartbeat(self, task_id: str, node_id: int, ttl_sec: float = DEFAULT_LEASE_TTL_SEC) -> bool:
        """Extend one live lease; settled or expired leases do not extend."""
        conn = self._conn()
        now = self._now()
        try:
            cur = conn.execute(
                "UPDATE loop_leases SET expires_at = ? "
                "WHERE task_id = ? AND node_id = ? AND settled = 0 AND expires_at > ?",
                (now + float(ttl_sec), task_id, int(node_id), now),
            )
            conn.commit()
        except Exception:
            return False
        return cur.rowcount > 0

    def settle(self, task_id: str, node_id: int) -> bool:
        """Mark the lease settled so the intent can never be claimed again."""
        conn = self._conn()
        now = self._now()
        try:
            cur = conn.execute(
                "UPDATE loop_leases SET settled = 1, settled_at = ? WHERE task_id = ? AND node_id = ? AND settled = 0",
                (now, task_id, int(node_id)),
            )
            conn.commit()
        except Exception:
            return False
        return cur.rowcount > 0

    def release(self, task_id: str, node_id: int) -> bool:
        """Drop the lease row so the intent becomes claimable again."""
        conn = self._conn()
        try:
            cur = conn.execute(
                "DELETE FROM loop_leases WHERE task_id = ? AND node_id = ?",
                (task_id, int(node_id)),
            )
            conn.commit()
        except Exception:
            return False
        return cur.rowcount > 0

    def active(self, task_id: str, node_id: int) -> bool:
        """Return True when an unexpired, unsettled lease exists."""
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT settled, expires_at FROM loop_leases WHERE task_id = ? AND node_id = ?",
                (task_id, int(node_id)),
            ).fetchone()
        except Exception:
            return False
        if row is None:
            return False
        return not int(row["settled"]) and float(row["expires_at"]) > self._now()

    def sweep(self, now: float | None = None) -> list[tuple[str, int]]:
        """Drop expired live leases and return the freed claims.

        Returns:
            List of ``(task_id, node_id)`` whose leases expired; the
            caller resets those graph nodes back to pending.
        """
        conn = self._conn()
        reference = float(now if now is not None else self._now())
        freed: list[tuple[str, int]] = []
        try:
            conn.execute("BEGIN IMMEDIATE")
            rows = conn.execute(
                "SELECT task_id, node_id FROM loop_leases WHERE settled = 0 AND expires_at < ?",
                (reference,),
            ).fetchall()
            for row in rows:
                freed.append((str(row["task_id"]), int(row["node_id"])))
            if freed:
                conn.execute(
                    "DELETE FROM loop_leases WHERE settled = 0 AND expires_at < ?",
                    (reference,),
                )
            conn.execute(
                "DELETE FROM loop_leases WHERE settled = 1 AND settled_at > 0 AND settled_at < ?",
                (reference - SETTLED_RETENTION_SEC,),
            )
            conn.commit()
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            return []
        return freed

    def counts(self) -> dict[str, int]:
        """Return live, expired and settled lease counts (observability)."""
        conn = self._conn()
        now = self._now()
        try:
            row = conn.execute(
                "SELECT "
                "SUM(CASE WHEN settled = 0 AND expires_at > ? THEN 1 ELSE 0 END) AS live, "
                "SUM(CASE WHEN settled = 0 AND expires_at <= ? THEN 1 ELSE 0 END) AS expired, "
                "SUM(CASE WHEN settled = 1 THEN 1 ELSE 0 END) AS settled "
                "FROM loop_leases",
                (now, now),
            ).fetchone()
        except Exception:
            return {"live": 0, "expired": 0, "settled": 0}
        return {
            "live": int(row["live"] or 0),
            "expired": int(row["expired"] or 0),
            "settled": int(row["settled"] or 0),
        }
