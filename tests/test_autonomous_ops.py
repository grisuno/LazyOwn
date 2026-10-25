"""BDD scoped tests for integrated autonomous operations C04-C10.

Given the planner frontier, graph mirror, db-backed findings, pool,
notifier, side questions and updater, when I exercise their verbs
against the existing campaign flows, then the criteria hold.
"""

from __future__ import annotations


def test_c04_dedup_anchor_coverage():
    """BDD: assets deduplicate and anchors resolve both ways."""
    from modules.asset_graph import AssetGraph
    graph = AssetGraph()
    first = graph.upsert_asset("subdomain", "app.target.local")
    second = graph.upsert_asset("subdomain", "app.target.local")
    assert first.key == second.key
    intent = graph.add_node("t1", "intent", "probe login")
    graph.anchor(intent.node_id, first.key)
    assert graph.assets_for_node(intent.node_id)[0].key == first.key
    assert graph.nodes_for_asset(first.key)[0].node_id == intent.node_id
    coverage = graph.coverage("t1")
    assert coverage["total"] == 1 and coverage["tested"] == 1


def test_c04_mirror_to_campaign_db(tmp_path):
    """BDD: graph assets land in the campaign database and world model."""
    from modules.asset_graph import AssetGraph
    from modules.db import LazyOwnDB
    from modules.world_model import WorldModel
    db = LazyOwnDB(str(tmp_path / "campaign.db"))
    workspace = db.default_workspace()
    world = WorldModel(path=tmp_path / "world_model.json")
    graph = AssetGraph()
    graph.upsert_asset("ip", "10.9.0.7")
    counts = graph.mirror_to_campaign(db, world, workspace)
    assert counts["hosts"] == 1
    assert db.host_find(workspace, "10.9.0.7")
    assert "10.9.0.7" in world.get_hosts_summary()
    db.close()


def test_c05_frontier_emits_once_then_empty():
    """BDD: planner frontier emits untried intents, then nothing new."""
    from modules.planner import Frontier, Planner
    frontier = Frontier(Planner())
    first = frontier.refill("127.0.0.1", max_intents=2)
    assert len(first) >= 1
    for _ in range(20):
        while frontier.pop() is not None:
            pass
        if frontier.refill("127.0.0.1", max_intents=2) == []:
            break
    assert len(frontier) == 0
    assert frontier.refill("127.0.0.1", max_intents=2) == []


def test_c05_todo_blocks_lateral_until_creds():
    """BDD: lateral tactics wait for the credential chain step."""
    from modules.planner import Frontier, Planner
    frontier = Frontier(Planner())
    frontier.todos.todo_add("creds")
    frontier.todos.todo_add("lateral", requires=["creds"])
    assert frontier.todos.blocks("lateral-movement") is True
    assert frontier.todos.todo_done("lateral") is False
    assert frontier.todos.todo_done("creds") is True
    assert frontier.todos.blocks("lateral-movement") is False


def test_c06_finding_lifecycle_on_campaign_db(tmp_path):
    """BDD: findings live in db vulns with status markers and retests."""
    from modules import finding_lifecycle as lifecycle
    from modules.db import LazyOwnDB
    db = LazyOwnDB(str(tmp_path / "campaign.db"))
    workspace = db.default_workspace()
    finding = lifecycle.record(db, workspace, "10.9.0.7", "SQLi", "high",
                               "injection in login", poc="POC")
    assert finding.status == "pending"
    retest = lifecycle.request_retest(db, finding.finding_id,
                                      sessions_dir=tmp_path / "sessions")
    assert lifecycle.request_retest(
        db, finding.finding_id,
        sessions_dir=tmp_path / "sessions").retest_id == retest.retest_id
    lifecycle.resolve_retest(db, retest.retest_id, "reproducible",
                             sessions_dir=tmp_path / "sessions")
    assert lifecycle.findings_for(db, workspace)[0].status == "pending"
    second = lifecycle.request_retest(db, finding.finding_id,
                                      sessions_dir=tmp_path / "sessions")
    lifecycle.resolve_retest(db, second.retest_id, "fixed", evidence="patched",
                             sessions_dir=tmp_path / "sessions")
    assert lifecycle.findings_for(db, workspace)[0].status == "fixed"
    report = lifecycle.render_markdown(db, workspace, title="demo")
    assert "SQLi" in report and "high" in report
    assert lifecycle.set_status(db, finding.finding_id, "confirmed") is True
    db.close()


def test_c07_pool_failover_and_exhaustion():
    """BDD: dead head falls through, exhausted chain raises."""
    from modules.llm_pool import HealthRegistry, LLMPool, PoolExhausted, PoolMember
    def boom(_prompt):
        raise RuntimeError("no credit")
    pool = LLMPool([
        PoolMember("a", "primary", "m1", rank=10, complete=boom),
        PoolMember("b", "backup", "m2", rank=1, complete=lambda p: f"ok:{p}"),
    ], health=HealthRegistry())
    assert pool.complete("hi") == "ok:hi"
    dead = LLMPool([PoolMember("a", "only", "m1", rank=1, complete=boom)])
    try:
        dead.complete("hi")
        assert False, "expected PoolExhausted"
    except PoolExhausted:
        assert True


def test_c08_notify_filter_and_redact():
    """BDD: severity gate drops noise and secrets are masked."""
    from modules.notify import Channel, Notifier, NotifyMessage
    notifier = Notifier()
    low = NotifyMessage("finding_created", "low", "t", "body")
    channel = Channel("telegram", "ops", min_severity="high")
    assert notifier.dispatch(low, [channel]) == []
    secret = NotifyMessage("finding_created", "critical", "t sk-abcdef123456", "b")
    deliveries = notifier.dispatch(secret, [channel])
    assert deliveries and "[REDACTED]" in deliveries[0]["text"]


def test_c09_side_question_isolated():
    """BDD: side questions need snapshots and never mutate main state."""
    from modules.sidequestion import SideQuestionService
    svc = SideQuestionService(answer_fn=lambda snap, q: f"{snap}:{q}")
    snap = svc.capture("t1", "main context")
    asked = svc.ask(snap.snapshot_id, "what next?")
    assert asked.status == "done" and "what next?" in asked.answer
    assert len(svc.history()) == 1
    try:
        svc.ask("missing", "q")
        assert False, "expected KeyError"
    except KeyError:
        assert True


def test_c10_verify_rejects_bad_checksum(tmp_path):
    """BDD: bad checksum aborts without touching the live binary."""
    from modules.selfupdate import ReleaseArtifact, Updater
    live = tmp_path / "lazyown.bin"
    live.write_bytes(b"v1")
    updater = Updater(live)
    bad = ReleaseArtifact(data=b"v2", sha256="0" * 64, version="v2")
    assert updater.verify(bad) is False
    try:
        updater.stage(bad, tmp_path)
        assert False, "expected ValueError"
    except ValueError:
        assert True
    assert live.read_bytes() == b"v1"


def test_c10_rollback_restores_previous(tmp_path):
    """BDD: rollback restores the previous binary."""
    from modules.selfupdate import Updater
    live = tmp_path / "lazyown.bin"
    live.write_bytes(b"broken")
    updater = Updater(live)
    backup = live.with_name("lazyown.bin.old")
    backup.write_bytes(b"v0")
    assert updater.rollback() is True
    assert live.read_bytes() == b"v0"


def test_i2_shared_registry_survives_rebuilds():
    """BDD: breaker state is process-wide, not reset per pool build."""
    from modules.llm_pool import HealthRegistry, LLMPool, PoolMember, shared_registry
    first, second = shared_registry(), shared_registry()
    assert first is second
    first.report_failure("m", "boom")
    assert second.healthy("m") is True
    for _ in range(5):
        second.report_failure("m", "boom")
    assert first.healthy("m") is False
    first.report_success("m")
    assert second.healthy("m") is True
    assert isinstance(HealthRegistry(), HealthRegistry)


def test_i2_pool_hard_trips_on_auth_errors():
    """BDD: quota/auth errors trip immediately without waiting for count."""
    from modules.llm_pool import HealthRegistry
    health = HealthRegistry()
    health.report_failure("m", "402 quota exceeded")
    assert health.healthy("m") is False


def test_i3_classify_retest_verdicts():
    """BDD: retest output maps onto reproducible / fixed / inconclusive."""
    from modules.finding_lifecycle import classify_retest
    assert classify_retest("CVE-2024-1", "CVE-2024-1 still open on 445") == "reproducible"
    assert classify_retest("CVE-2024-1", "connection refused on 445") == "fixed"
    assert classify_retest("CVE-2024-1", "weird banner") == "inconclusive"
    assert classify_retest("CVE-2024-1", "error traceback boom") == "inconclusive"


def test_i3_retest_bumps_evidence_version(tmp_path):
    """BDD: resolving a retest bumps the optimistic evidence version."""
    from modules import finding_lifecycle as lifecycle
    from modules.db import LazyOwnDB
    db = LazyOwnDB(str(tmp_path / "campaign.db"))
    workspace = db.default_workspace()
    finding = lifecycle.record(db, workspace, "10.9.0.8", "XSS", "medium", "reflected")
    sessions = tmp_path / "sessions"
    assert lifecycle.has_running_retest(finding.finding_id, sessions) is False
    retest = lifecycle.request_retest(db, finding.finding_id, sessions_dir=sessions)
    assert lifecycle.has_running_retest(finding.finding_id, sessions) is True
    done = lifecycle.resolve_retest(db, retest.retest_id, "reproducible",
                                    evidence="still there", sessions_dir=sessions)
    assert done.conclusion == "reproducible"
    assert lifecycle.has_running_retest(finding.finding_id, sessions) is False
    rows = db.vuln_list(workspace)
    refs = next(r["refs"] for r in rows if str(r["id"]) == finding.finding_id)
    assert "evidence_version:1" in refs
    db.close()


def test_i4_shared_engine_cooldown():
    """BDD: one process-wide enrich engine; cooldown dedups targets."""
    from modules.enrich import shared_engine
    assert shared_engine() is shared_engine()
    assert shared_engine().submit("example-target-xyz") is True
    assert shared_engine().submit("example-target-xyz") is False


def test_i4_should_rescan_honours_fresh_scans(tmp_path):
    """BDD: fresh scan artefacts suppress rescans."""
    from modules.enrich import should_rescan
    assert should_rescan(tmp_path, "10.9.0.9") is True
    (tmp_path / "scan_10.9.0.9.nmap").write_text("fresh")
    assert should_rescan(tmp_path, "10.9.0.9") is False
