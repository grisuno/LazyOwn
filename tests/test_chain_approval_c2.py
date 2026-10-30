"""Contract tests for the chain approval gate (C2 human-in-the-loop)."""

from __future__ import annotations

import os
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

from modules.chain_approval import (
    AUDIT_FILENAME,
    DEFAULT_TIMEOUT_SEC,
    PENDING_FILENAME,
    PendingStore,
    _clamp_timeout,
    approval_backend,
    build_c2_approver,
    command_fingerprint,
)


class StoreLifecycle(unittest.TestCase):
    """PendingStore create/decide/expire contract."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_create_and_list_roundtrip(self):
        store = PendingStore(self.tmp)
        record = store.create("apt_chain", "smb_exec", "whoami", timeout=60, run_id="run1")
        rows = store.list()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "pending")
        self.assertEqual(rows[0]["chain"], "apt_chain")
        self.assertEqual(rows[0]["command"], "whoami")
        self.assertEqual(rows[0]["command_sha256"], command_fingerprint("whoami"))
        self.assertEqual(record["run_id"], "run1")

    def test_decision_records_and_dedupes(self):
        store = PendingStore(self.tmp)
        record = store.create("c", "s", "cmd")
        approved = store.decide(record["id"], True, decided_by="c2")
        self.assertEqual(approved["status"], "approved")
        self.assertEqual(approved["decided_by"], "c2")
        self.assertIsNone(store.decide(record["id"], False))

    def test_unknown_and_already_decided_failures(self):
        store = PendingStore(self.tmp)
        self.assertIsNone(store.decide("deadbeefdeadbeef", True))
        self.assertIsNone(store.get("missing"))

    def test_expire_stale_sweeps_only_past_deadline(self):
        store = PendingStore(self.tmp)
        old = store.create("c", "s1", "cmd1", timeout=1.0)
        fresh = store.create("c", "s2", "cmd2", timeout=60.0)
        self.assertEqual(store.expire_stale(now=time.time() + 5), 1)
        self.assertEqual(store.get(old["id"])["status"], "expired")
        self.assertEqual(store.get(fresh["id"])["status"], "pending")

    def test_audit_trail_written(self):
        store = PendingStore(self.tmp)
        record = store.create("c", "s", "cmd")
        store.decide(record["id"], False, decided_by="c2")
        log = (Path(self.tmp) / AUDIT_FILENAME).read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(log), 2)
        self.assertIn('"event": "requested"', log[0])
        self.assertIn('"event": "denied"', log[1])


class C2Approver(unittest.TestCase):
    """build_c2_approver poll/expiry/failure-closed contract."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_approve_after_c2_decision(self):
        approver = build_c2_approver(timeout=5.0, poll_interval=0.01, sessions_dir=self.tmp)

        def decide_later():
            time.sleep(0.05)
            store = PendingStore(self.tmp)
            rows = store.list(status="pending")
            self.assertEqual(len(rows), 1)
            store.decide(rows[0]["id"], True, decided_by="c2")

        thread = threading.Thread(target=decide_later, daemon=True)
        thread.start()
        self.assertTrue(approver("step1", "whoami"))
        thread.join(timeout=2.0)

    def test_deny_votes_false(self):
        approver = build_c2_approver(timeout=5.0, poll_interval=0.01, sessions_dir=self.tmp)

        def deny_later():
            time.sleep(0.05)
            store = PendingStore(self.tmp)
            for row in store.list(status="pending"):
                store.decide(row["id"], False, decided_by="c2")

        thread = threading.Thread(target=deny_later, daemon=True)
        thread.start()
        self.assertFalse(approver("step", "cmd"))
        thread.join(timeout=2.0)

    def test_deadline_expiry_denies(self):
        advance = [0.0]

        def fast_clock() -> float:
            advance[0] += 1.0
            return advance[0]

        approver = build_c2_approver(timeout=2.0, poll_interval=0.001, sessions_dir=self.tmp, clock=fast_clock)
        self.assertFalse(approver("step", "cmd"))
        store = PendingStore(self.tmp)
        rows = store.list(status="expired")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["step_id"], "step")

    def test_store_failure_denies(self):
        approver = build_c2_approver(timeout=5.0, poll_interval=0.0, sessions_dir=self.tmp)
        with mock.patch.object(PendingStore, "create", side_effect=OSError("disk full")):
            self.assertFalse(approver("step", "cmd"))


class BackendSelection(unittest.TestCase):
    """approval_backend and timeout clamp contract."""

    def test_default_cli(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("LAZYOWN_APPROVAL_BACKEND", None)
            self.assertEqual(approval_backend(), "cli")

    def test_c2_selected(self):
        with mock.patch.dict(os.environ, {"LAZYOWN_APPROVAL_BACKEND": "c2"}):
            self.assertEqual(approval_backend(), "c2")

    def test_timeout_clamped(self):
        self.assertEqual(_clamp_timeout(-5), 1.0)
        self.assertEqual(_clamp_timeout(None), DEFAULT_TIMEOUT_SEC)
        self.assertEqual(_clamp_timeout(999999), 5400.0)
        self.assertEqual(_clamp_timeout("bad"), DEFAULT_TIMEOUT_SEC)


class Directive(unittest.TestCase):
    """File layout contract shared by CLI and C2."""

    def test_filenames(self):
        self.assertEqual(PENDING_FILENAME, "chain_pending.json")
        self.assertEqual(AUDIT_FILENAME, "chain_audit.jsonl")


class C2ChainApprovalEndpoints(unittest.TestCase):
    """lazyc2 REST surface for the chain approval gate."""

    SERVER: object = None

    @classmethod
    def _server(cls):
        if cls.SERVER is None:
            import importlib.util
            import sys

            root = Path(__file__).resolve().parent.parent
            spec = importlib.util.spec_from_file_location("lazyc2_server_appr_test", str(root / "lazyc2.py"))
            module = importlib.util.module_from_spec(spec)
            old_argv = sys.argv
            sys.argv = ["lazyc2"]
            try:
                spec.loader.exec_module(module)
            finally:
                sys.argv = old_argv
            cls.SERVER = module
        return cls.SERVER

    def setUp(self):
        module = self._server()
        module.config.c2_csrf_enabled = False
        module.config.c2_decoy_mode = "off"
        module.login_manager._user_callback = lambda uid: module.User(
            {"id": 1, "username": "op", "password_hash": "x"}
        )
        self.client = module.app.test_client()
        with self.client.session_transaction() as sess:
            sess["_user_id"] = "1"
            sess["_fresh"] = False

    def test_list_shape(self):
        response = self.client.get("/api/chain_approvals")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertIn("requests", body)
        self.assertIn("count", body)

    def test_list_filter_and_decide_roundtrip(self):
        store = PendingStore()
        record = store.create("apt_chain_smoke", "smb_exec", "whoami", timeout=60, run_id="r2")

        listed = self.client.get("/api/chain_approvals", query_string={"status": "pending"}).get_json()
        self.assertTrue(any(row["id"] == record["id"] for row in listed["requests"]))

        self.assertEqual(self.client.post("/api/chain_approvals/NOPE/decide", json={"decision": "approve"}).status_code, 400)
        self.assertEqual(
            self.client.post(f"/api/chain_approvals/{'0'*16}/decide", json={"decision": "approve"}).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(f"/api/chain_approvals/{record['id']}/decide", json={"decision": "explode"}).status_code,
            400,
        )

        ok = self.client.post(
            f"/api/chain_approvals/{record['id']}/decide",
            json={"decision": "approve", "note": "operator ok"},
        )
        self.assertEqual(ok.status_code, 200)
        final = ok.get_json()["request"]
        self.assertEqual(final["status"], "approved")
        self.assertEqual(final["decided_by"], "c2")

        again = self.client.post(f"/api/chain_approvals/{record['id']}/decide", json={"decision": "deny"})
        self.assertEqual(again.status_code, 404)


if __name__ == "__main__":
    unittest.main()
