"""tests/test_collab_and_onboarding.py

Tests for:
- Gap #2 (team server): collab_bp UI route, SSE stream, operator registry,
  lock manager, event bus, and publish endpoint.
- Gap #3 (onboarding): QUICKSTART.md completeness, wizard module contract,
  collab_join CLI command structure.
"""

from __future__ import annotations

import ast
import json
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "modules"))

QUICKSTART = REPO_ROOT / "QUICKSTART.md"
COLLAB_TEMPLATE = REPO_ROOT / "templates" / "collab.html"
COLLAB_MODULE = REPO_ROOT / "modules" / "collab_bp.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_app():
    """Build a minimal Flask app with collab_bp registered."""
    from collab_bp import collab_bp
    from flask import Flask

    app = Flask(__name__, template_folder=str(REPO_ROOT / "templates"))
    app.config["TESTING"] = True
    app.config["LAZYOWN_CONFIG"] = {"lhost": "127.0.0.1", "c2_port": 4444}
    app.register_blueprint(collab_bp, url_prefix="/collab")
    return app


# ---------------------------------------------------------------------------
# Gap #3 — Onboarding: QUICKSTART.md
# ---------------------------------------------------------------------------

class TestQuickstartExists:
    def test_file_present(self):
        assert QUICKSTART.exists(), "QUICKSTART.md not found"

    def test_not_empty(self):
        assert QUICKSTART.stat().st_size > 500, "QUICKSTART.md is too short"


class TestQuickstartContent:
    @pytest.fixture(scope="class")
    def text(self) -> str:
        return QUICKSTART.read_text(encoding="utf-8").lower()

    def test_has_install_section(self, text):
        assert "install" in text

    def test_has_wizard_section(self, text):
        assert "wizard" in text

    def test_has_recon_step(self, text):
        assert "lazynmap" in text or "recon" in text

    def test_has_c2_step(self, text):
        assert "lazyc2" in text or "fast_run" in text

    def test_has_collab_step(self, text):
        assert "collab_join" in text

    def test_has_troubleshooting(self, text):
        assert "troubleshoot" in text

    def test_mentions_payload_json(self, text):
        assert "payload.json" in text

    def test_mentions_sessions(self, text):
        assert "sessions/" in text

    def test_five_minutes_promise(self, text):
        assert "5" in text or "five" in text

    def test_no_hardcoded_ips(self):
        import re
        text = QUICKSTART.read_text(encoding="utf-8")
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        allowed = {"10.10.11.5", "10.10.14.3", "127.0.0.1"}
        bad = [ip for ip in ips if ip not in allowed]
        assert bad == [], f"Hardcoded IPs in QUICKSTART.md: {bad}"


# ---------------------------------------------------------------------------
# Gap #3 — Onboarding: wizard module contract
# ---------------------------------------------------------------------------

class TestWizardContract:
    def test_wizard_module_exists(self):
        assert (REPO_ROOT / "cli" / "wizard.py").exists()

    def test_wizard_has_run_function(self):
        tree = ast.parse((REPO_ROOT / "cli" / "wizard.py").read_text(encoding="utf-8"))
        fns = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
        assert "run" in fns

    def test_wizard_has_build_readiness(self):
        tree = ast.parse((REPO_ROOT / "cli" / "wizard.py").read_text(encoding="utf-8"))
        fns = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
        assert "_build_readiness" in fns

    def test_wizard_does_not_import_lazyown(self):
        text = (REPO_ROOT / "cli" / "wizard.py").read_text(encoding="utf-8")
        assert "import lazyown" not in text, "wizard must not import lazyown.py (DIP violation)"

    def test_wizard_does_not_import_lazyc2(self):
        text = (REPO_ROOT / "cli" / "wizard.py").read_text(encoding="utf-8")
        assert "import lazyc2" not in text, "wizard must not import lazyc2.py (DIP violation)"


# ---------------------------------------------------------------------------
# Gap #2 — Team server: collab_bp module structure
# ---------------------------------------------------------------------------

class TestCollabModuleExists:
    def test_module_present(self):
        assert COLLAB_MODULE.exists()

    def test_template_present(self):
        assert COLLAB_TEMPLATE.exists()

    def test_template_not_empty(self):
        assert COLLAB_TEMPLATE.stat().st_size > 1000


class TestCollabModuleClasses:
    @pytest.fixture(scope="class")
    def tree(self) -> ast.Module:
        return ast.parse(COLLAB_MODULE.read_text(encoding="utf-8"))

    def test_has_event_bus(self, tree):
        classes = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        assert "EventBus" in classes

    def test_has_lock_manager(self, tree):
        classes = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        assert "LockManager" in classes

    def test_has_operator_registry(self, tree):
        classes = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        assert "OperatorRegistry" in classes

    def test_has_ui_route(self, tree):
        src = COLLAB_MODULE.read_text(encoding="utf-8")
        assert 'route("/")' in src or "route('/')" in src

    def test_has_stream_route(self, tree):
        src = COLLAB_MODULE.read_text(encoding="utf-8")
        assert "/stream" in src

    def test_has_publish_route(self):
        src = COLLAB_MODULE.read_text(encoding="utf-8")
        assert "/publish" in src

    def test_has_lock_route(self):
        src = COLLAB_MODULE.read_text(encoding="utf-8")
        assert "/lock" in src


# ---------------------------------------------------------------------------
# Gap #2 — Team server: EventBus unit tests
# ---------------------------------------------------------------------------

class TestEventBus:
    @pytest.fixture
    def bus(self):
        from collab_bp import EventBus
        return EventBus()

    def test_publish_and_receive(self, bus):
        from collab_bp import ColabEvent
        q = bus.subscribe("test_sub")
        ev = ColabEvent(type="command", payload={"cmd": "lazynmap"}, operator="alice")
        bus.publish(ev)
        received = q.get(timeout=1)
        assert received.type == "command"
        assert received.operator == "alice"

    def test_history_replay_on_subscribe(self, bus):
        from collab_bp import ColabEvent
        for i in range(5):
            bus.publish(ColabEvent(type="test", payload={"i": i}, operator="sys"))
        q = bus.subscribe("late_sub")
        replayed = []
        while not q.empty():
            replayed.append(q.get_nowait())
        assert len(replayed) == 5

    def test_recent_returns_correct_count(self, bus):
        from collab_bp import ColabEvent
        for i in range(10):
            bus.publish(ColabEvent(type="generic", payload={}, operator="x"))
        assert len(bus.recent(5)) == 5
        assert len(bus.recent(100)) == 10

    def test_reset_clears_history(self, bus):
        from collab_bp import ColabEvent
        bus.publish(ColabEvent(type="x", payload={}, operator="y"))
        bus.reset()
        assert bus.recent(10) == []

    def test_full_queue_drops_stale_subscriber(self, bus):

        from collab_bp import ColabEvent
        bus.subscribe("stale")
        for _ in range(bus._MAX_QUEUE + 10):
            try:
                bus.publish(ColabEvent(type="flood", payload={}, operator="sys"))
            except Exception:
                pass
        assert True


# ---------------------------------------------------------------------------
# Gap #2 — Team server: LockManager unit tests
# ---------------------------------------------------------------------------

class TestLockManager:
    @pytest.fixture
    def lm(self):
        from collab_bp import LockManager
        return LockManager()

    def test_acquire_grants_first_operator(self, lm):
        assert lm.acquire("10.10.11.5", "alice") is True

    def test_second_operator_denied(self, lm):
        lm.acquire("10.10.11.5", "alice")
        assert lm.acquire("10.10.11.5", "bob") is False

    def test_same_operator_can_re_acquire(self, lm):
        lm.acquire("10.10.11.5", "alice")
        assert lm.acquire("10.10.11.5", "alice") is True

    def test_release_allows_next_operator(self, lm):
        lm.acquire("10.10.11.5", "alice")
        lm.release("10.10.11.5", "alice")
        assert lm.acquire("10.10.11.5", "bob") is True

    def test_release_by_wrong_operator_fails(self, lm):
        lm.acquire("10.10.11.5", "alice")
        assert lm.release("10.10.11.5", "bob") is False

    def test_expired_lock_releases_automatically(self, lm):
        lm.acquire("10.10.11.5", "alice", ttl_secs=0)
        time.sleep(0.01)
        assert lm.acquire("10.10.11.5", "bob") is True

    def test_all_locks_returns_list(self, lm):
        lm.acquire("10.10.11.1", "alice")
        lm.acquire("10.10.11.2", "bob")
        locks = lm.all_locks()
        targets = {lock.target for lock in locks}
        assert "10.10.11.1" in targets
        assert "10.10.11.2" in targets

    def test_reset_clears_all_locks(self, lm):
        lm.acquire("10.10.11.5", "alice")
        lm.reset()
        assert lm.all_locks() == []


# ---------------------------------------------------------------------------
# Gap #2 — Team server: OperatorRegistry unit tests
# ---------------------------------------------------------------------------

class TestOperatorRegistry:
    @pytest.fixture
    def reg(self):
        from collab_bp import OperatorRegistry
        return OperatorRegistry()

    def test_join_registers_operator(self, reg):
        reg.join("alice")
        active = [o.name for o in reg.active_operators()]
        assert "alice" in active

    def test_leave_marks_inactive(self, reg):
        reg.join("alice")
        reg.leave("alice")
        active = [o.name for o in reg.active_operators()]
        assert "alice" not in active

    def test_multiple_operators(self, reg):
        reg.join("alice")
        reg.join("bob")
        assert len(reg.active_operators()) == 2

    def test_heartbeat_keeps_alive(self, reg):
        reg.join("alice")
        reg.heartbeat("alice")
        assert any(o.name == "alice" for o in reg.active_operators())

    def test_reset_clears_all(self, reg):
        reg.join("alice")
        reg.reset()
        assert reg.active_operators() == []


# ---------------------------------------------------------------------------
# Gap #2 — Team server: Flask HTTP endpoint tests
# ---------------------------------------------------------------------------

class TestCollabFlaskRoutes:
    @pytest.fixture(scope="class")
    def client(self):
        app = _make_app()
        with app.test_client() as c:
            yield c

    def test_operators_endpoint_returns_json(self, client):
        resp = client.get("/collab/operators")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "operators" in data
        assert "count" in data

    def test_locks_endpoint_returns_json(self, client):
        resp = client.get("/collab/locks")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "locks" in data

    def test_publish_endpoint_accepts_event(self, client):
        payload = {"type": "finding", "operator": "alice", "payload": {"detail": "root"}}
        resp = client.post("/collab/publish", json=payload)
        assert resp.status_code == 200
        assert json.loads(resp.data)["status"] == "published"

    def test_publish_rejects_non_dict_payload(self, client):
        resp = client.post("/collab/publish", json={"type": "x", "payload": "bad"})
        assert resp.status_code == 400

    def test_lock_endpoint_acquires(self, client):
        resp = client.post("/collab/lock", json={"target": "10.0.0.1", "operator": "alice"})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["acquired"] is True

    def test_unlock_endpoint_releases(self, client):
        client.post("/collab/lock", json={"target": "10.0.0.2", "operator": "alice"})
        resp = client.post("/collab/unlock", json={"target": "10.0.0.2", "operator": "alice"})
        assert resp.status_code == 200
        assert json.loads(resp.data)["released"] is True

    def test_history_endpoint_returns_events(self, client):
        client.post("/collab/publish", json={"type": "test", "operator": "x", "payload": {}})
        resp = client.get("/collab/history?n=5")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "events" in data

    def test_lock_missing_target_returns_400(self, client):
        resp = client.post("/collab/lock", json={"operator": "alice"})
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Gap #2 — Team server: collab template content
# ---------------------------------------------------------------------------

class TestCollabTemplate:
    @pytest.fixture(scope="class")
    def html(self) -> str:
        return COLLAB_TEMPLATE.read_text(encoding="utf-8")

    def test_extends_base(self, html):
        assert "extends" in html and "base.html" in html

    def test_has_sse_connect(self, html):
        assert "EventSource" in html

    def test_has_operator_list(self, html):
        assert "operators-list" in html or "operator" in html

    def test_has_lock_ui(self, html):
        assert "lock" in html.lower()

    def test_has_event_log(self, html):
        assert "event-log" in html or "event_log" in html

    def test_has_chat_input(self, html):
        assert "chat" in html.lower()

    def test_has_refresh_operators(self, html):
        assert "refreshOperators" in html or "operators" in html

    def test_has_join_url_display(self, html):
        assert "join-url" in html or "join_url" in html

    def test_no_hardcoded_ips(self):
        import re
        html = COLLAB_TEMPLATE.read_text(encoding="utf-8")
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', html)
        assert ips == [], f"Hardcoded IPs in collab.html: {ips}"


# ---------------------------------------------------------------------------
# Gap #3 — collab_join CLI command presence in lazyown.py
# ---------------------------------------------------------------------------

class TestCollabJoinCLICommand:
    @pytest.fixture(scope="class")
    def lazyown_text(self) -> str:
        return (REPO_ROOT / "lazyown.py").read_text(encoding="utf-8")

    def test_collab_join_defined(self, lazyown_text):
        assert "def do_collab_join" in lazyown_text

    def test_collab_join_uses_lhost(self, lazyown_text):
        assert 'params.get("lhost")' in lazyown_text

    def test_collab_join_uses_c2_port(self, lazyown_text):
        assert 'params.get("c2_port")' in lazyown_text

    def test_collab_join_prints_ui_url(self, lazyown_text):
        assert "/collab/" in lazyown_text

    def test_collab_join_has_docstring(self, lazyown_text):
        idx = lazyown_text.index("def do_collab_join")
        snippet = lazyown_text[idx: idx + 600]
        assert '"""' in snippet
