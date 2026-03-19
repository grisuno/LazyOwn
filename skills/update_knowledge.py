#!/usr/bin/env python3
"""
LazyOwn Knowledge Refresh
==========================
Refreshes the session_knowledge.parquet from the current CSV and optionally
trains the sklearn classifier.

Usage:
    python3 skills/update_knowledge.py [--train] [--min-rows N]

Suitable for cron / post-op automation:
    0 * * * * python3 /opt/LazyOwn/skills/update_knowledge.py --train 2>&1
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[knowledge] %(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("update_knowledge")

SKILLS_DIR = Path(__file__).parent
BASE_DIR   = SKILLS_DIR.parent

if str(SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(SKILLS_DIR))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LazyOwn Knowledge Refresh")
    parser.add_argument("--train",    action="store_true",
                        help="Train RandomForest classifier after sync")
    parser.add_argument("--min-rows", type=int, default=50,
                        help="Minimum annotated rows to attempt training (default 50)")
    parser.add_argument("--quiet",    action="store_true",
                        help="Suppress informational output")
    args = parser.parse_args(argv)

    if args.quiet:
        logging.disable(logging.WARNING)

    try:
        from lazyown_parquet_db import ParquetDB, _PANDAS_OK
    except ImportError as exc:
        log.error(f"Cannot import ParquetDB: {exc}. Install: pip install pandas pyarrow")
        return 1

    if not _PANDAS_OK:
        log.error("pandas/pyarrow not available. Install: pip install pandas pyarrow")
        return 1

    db = ParquetDB()

    # ── Sync CSV → parquet ────────────────────────────────────────────────────
    log.info("Syncing session CSV → parquet …")
    try:
        n_new = db.sync()
        log.info(f"Sync complete: {n_new} new rows ingested.")
    except Exception as exc:
        log.error(f"Sync failed: {exc}")
        return 1

    # ── Stats ─────────────────────────────────────────────────────────────────
    try:
        stats = db.stats()
        log.info(f"Stats:\n{stats}")
    except Exception as exc:
        log.warning(f"Stats error: {exc}")

    # ── Optional classifier training ──────────────────────────────────────────
    if args.train:
        log.info(f"Training classifier (min_rows={args.min_rows}) …")
        try:
            result = db.train_classifier(min_rows=args.min_rows)
            if "error" in result:
                log.warning(f"Classifier not trained: {result['error']}")
            else:
                acc   = result.get("accuracy", 0)
                n_tr  = result.get("n_train", 0)
                n_te  = result.get("n_test", 0)
                path  = result.get("model_path", "")
                log.info(f"Classifier ready: accuracy={acc:.2%} train={n_tr} test={n_te}")
                log.info(f"Model saved: {path}")
                fi = result.get("feature_importance", {})
                if fi:
                    log.info("Feature importance: " +
                             " | ".join(f"{k}={v:.3f}" for k, v in fi.items()))
        except Exception as exc:
            log.error(f"Training failed: {exc}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
