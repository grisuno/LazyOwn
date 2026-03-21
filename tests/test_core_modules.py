"""
tests/test_core_modules.py
Integration test suite for LazyOwn core modules.
"""
import json, sys, time
from pathlib import Path
import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT / "modules"))
sys.path.insert(0, str(_ROOT / "modules" / "integrations"))

# obs_parser
def test_obs_parser_nmap():
    from obs_parser import ObsParser, FindingType
    obs = ObsParser().parse(
        "22/tcp open ssh OpenSSH 8.4p1\n80/tcp open http Apache 2.4.49\n"
        "CVE-2021-41773\nFound /admin/ Status: 200\n",
        host="10.10.11.78", tool="nmap")
    assert obs.success
    types = {f.type for f in obs.findings}
    assert FindingType.SERVICE_VERSION in types
    assert FindingType.CVE in types
    assert FindingType.PATH in types

def test_obs_parser_empty():
    from obs_parser import ObsParser
    obs = ObsParser().parse("", host="10.0.0.1")
    assert not obs.success
    assert obs.findings == []

def test_obs_parser_error():
    from obs_parser import ObsParser, FindingType
    obs = ObsParser().parse("connection refused", host="10.0.0.1")
    assert any(f.type == FindingType.ERROR for f in obs.findings)

# world_model
def test_world_model_basic():
    from world_model import WorldModel, EngagementPhase
    wm = WorldModel()
    wm.add_host("10.0.0.1")
    wm.add_service("10.0.0.1", 22, "ssh", "OpenSSH 8.4")
    assert wm.get_phase() in (EngagementPhase.RECON, EngagementPhase.SCANNING)
    assert "10.0.0.1" in wm.to_context_string()

def test_world_model_persistence(tmp_path):
    from world_model import WorldModel
    p = tmp_path / "wm.json"
    wm = WorldModel(path=str(p))
    wm.add_host("192.168.1.1")
    wm._save()
    wm2 = WorldModel(path=str(p))
    assert "192.168.1.1" in wm2.snapshot()["hosts"]

def test_world_model_from_findings():
    from world_model import WorldModel
    from obs_parser import ObsParser
    wm = WorldModel()
    obs = ObsParser().parse("22/tcp open ssh\n", host="10.1.1.1")
    wm.update_from_findings(obs.findings)
    assert "10.1.1.1" in wm.snapshot()["hosts"]

# playbook_engine
def test_playbook_engine_derive_save_load(tmp_path):
    from playbook_engine import PlaybookEngine
    engine = PlaybookEngine()
    pb = engine.derive("10.0.0.1", phase="scanning", platform="linux")
    assert pb.target == "10.0.0.1"
    saved = engine.save(pb, str(tmp_path / "pb.yaml"))
    loaded = engine.load(saved)
    assert loaded.target == pb.target

def test_playbook_engine_execute():
    from playbook_engine import PlaybookEngine, Playbook, PlaybookStep
    engine = PlaybookEngine()
    pb = Playbook(apt_name="t", description="t", target="127.0.0.1", phase="scanning",
                  steps=[PlaybookStep(atomic_id="T1046-1", technique_id="T1046",
                                     tactic="discovery", name="echo test",
                                     command="echo 22/tcp open ssh")])
    result = engine.execute(pb, executor=lambda cmd, tgt="": f"output: {cmd}")
    assert result.total_steps == 1
    assert "T1046" in engine.result_summary(result)

# cve_matcher
def test_cve_matcher():
    from cve_matcher import CVEMatcher
    m = CVEMatcher()
    assert m.cache_dir.exists()
    assert m.rate_delay > 0

# report_generator + CVSSv3Calculator
def test_cvss_critical():
    from report_generator import CVSSv3Calculator
    score, sev = CVSSv3Calculator().calculate("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
    assert score == 9.8
    assert sev == "Critical"

def test_cvss_medium():
    from report_generator import CVSSv3Calculator
    score, sev = CVSSv3Calculator().calculate("AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N")
    assert 3.0 <= score <= 6.9

def test_cvss_from_nvd():
    from report_generator import CVSSv3Calculator
    score, sev = CVSSv3Calculator().from_nvd_metrics(
        "NETWORK","LOW","NONE","NONE","UNCHANGED","HIGH","HIGH","HIGH")
    assert score == 9.8

def test_report_with_data(tmp_path):
    from report_generator import ReportGenerator
    sess = tmp_path / "sessions"; sess.mkdir()
    (sess / "policy_facts.json").write_text(json.dumps({"hosts": {"10.10.11.78": {
        "services": {"22": {"name": "ssh", "version": "OpenSSH 8.4"}},
        "vulnerabilities": [{"id": "CVE-2021-41773", "cvss": 9.8, "desc": "path traversal"}]
    }}}))
    (sess / "credentials.txt").write_text("admin:pass\n")
    path = ReportGenerator(sessions_dir=sess).generate(str(tmp_path / "r.md"))
    assert "10.10.11.78" in path.read_text()

def test_report_empty(tmp_path):
    from report_generator import ReportGenerator
    sess = tmp_path / "sessions"; sess.mkdir()
    path = ReportGenerator(sessions_dir=sess).generate(str(tmp_path / "r.md"))
    assert path.exists()

# memory_store
def test_memory_remember_recall(tmp_path):
    from memory_store import MemoryStore, SQLiteBackend
    ms = MemoryStore(backend=SQLiteBackend(db_path=tmp_path / "mem.db"))
    ms.remember("s1","10.0.0.1","nmap","nmap -sV 10.0.0.1","22/tcp open ssh OpenSSH 8.4",[],True)
    ms.remember("s1","10.0.0.1","gobuster","gobuster dir -u http://10.0.0.1","Found /admin 200",[],True)
    results = ms.recall("openssh ssh", top_k=5)
    assert any("10.0.0.1" in r.host for r in results)

def test_memory_by_host(tmp_path):
    from memory_store import MemoryStore, SQLiteBackend
    ms = MemoryStore(backend=SQLiteBackend(db_path=tmp_path / "mem.db"))
    ms.remember("s1","10.0.0.1","nmap","cmd","out",[],True)
    ms.remember("s1","10.0.0.2","nmap","cmd","out",[],True)
    results = ms.recall_by_host("10.0.0.1")
    assert all(r.host == "10.0.0.1" for r in results)

def test_memory_export(tmp_path):
    from memory_store import MemoryStore, SQLiteBackend
    ms = MemoryStore(backend=SQLiteBackend(db_path=tmp_path / "mem.db"))
    ms.remember("s1","10.0.0.1","nmap","nmap -sV","22/tcp open ssh",[],True)
    out = tmp_path / "ft.jsonl"
    ms.export_finetuning_dataset(out)
    assert out.exists()
    lines = [l for l in out.read_text().splitlines() if l.strip()]
    assert len(lines) >= 1
    for line in lines:
        assert "prompt" in json.loads(line) or "messages" in json.loads(line)

# llm_evaluator
def test_llm_evaluator(tmp_path):
    from llm_evaluator import LLMEvaluator, JSONLRecorder
    ev = LLMEvaluator(recorder=JSONLRecorder(path=tmp_path / "d.jsonl"))
    did = ev.record_decision("s1","thought","action","recon","expected",0.8)
    ev.record_outcome(did, "found ssh", 2, True)
    m = ev.compute_metrics()
    assert m.total_decisions == 1
    assert m.success_rate == 1.0

def test_llm_evaluator_report(tmp_path):
    from llm_evaluator import LLMEvaluator, JSONLRecorder
    ev = LLMEvaluator(recorder=JSONLRecorder(path=tmp_path / "d.jsonl"))
    d1 = ev.record_decision("s1","t1","a1","recon","e1",0.9)
    d2 = ev.record_decision("s1","t2","a2","execution","e2",0.5)
    ev.record_outcome(d1,"ok",3,True)
    ev.record_outcome(d2,"fail",0,False)
    report = ev.quality_report()
    assert len(report) > 10

def test_llm_evaluator_empty(tmp_path):
    from llm_evaluator import LLMEvaluator, JSONLRecorder
    ev = LLMEvaluator(recorder=JSONLRecorder(path=tmp_path / "d.jsonl"))
    assert ev.compute_metrics().total_decisions == 0

# searchsploit (graceful no binary)
def test_searchsploit_graceful():
    from integrations.searchsploit import SearchsploitCLI
    results = SearchsploitCLI().search_cve("CVE-9999-99999")
    assert isinstance(results, list)

def test_searchsploit_client():
    from integrations.searchsploit import get_client
    c = get_client()
    assert hasattr(c, "search_cve")
    assert hasattr(c, "enrich_findings")

# misp_export
def test_misp_export(tmp_path):
    from integrations.misp_export import MISPExporter
    sess = tmp_path / "sessions"; sess.mkdir()
    (sess / "policy_facts.json").write_text(json.dumps({"hosts": {"10.10.11.78": {
        "services": {"22": {"name": "ssh"}},
        "vulnerabilities": [{"id": "CVE-2021-41773", "cvss": 9.8, "desc": "test"}]
    }}}))
    (sess / "credentials.txt").write_text("admin:pass\n")
    ex = MISPExporter()
    event = ex.export_session(sess)
    assert len(event.attributes) >= 1
    saved = ex.save(event, str(tmp_path / "ev.json"))
    assert saved.exists()
    data = json.loads(saved.read_text())
    assert isinstance(data, dict)

# dashboard_bp
def test_dashboard_endpoints():
    from dashboard_bp import dashboard_bp
    from flask import Flask
    app = Flask(__name__); app.config["TESTING"] = True
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    c = app.test_client()
    assert c.get("/dashboard/").status_code == 200
    r = c.get("/dashboard/api/data")
    assert r.status_code == 200
    assert isinstance(json.loads(r.data), dict)

# collab_bp
def test_collab_endpoints():
    from collab_bp import collab_bp, get_lock_manager
    from flask import Flask
    app = Flask(__name__); app.config["TESTING"] = True
    app.register_blueprint(collab_bp, url_prefix="/collab")
    get_lock_manager().reset()
    c = app.test_client()
    r = c.get("/collab/operators")
    assert r.status_code == 200
    r2 = c.post("/collab/publish", json={"type":"finding","payload":{"h":"10.0.0.1"}})
    assert json.loads(r2.data)["status"] == "published"
    r3 = c.post("/collab/lock",   json={"target":"10.0.0.1","operator":"alice"})
    r4 = c.post("/collab/lock",   json={"target":"10.0.0.1","operator":"bob"})
    r5 = c.post("/collab/unlock", json={"target":"10.0.0.1","operator":"alice"})
    assert json.loads(r3.data)["acquired"] is True
    assert json.loads(r4.data)["acquired"] is False
    assert json.loads(r5.data)["released"] is True

# c2_profile
def test_c2_profile_builtins():
    from c2_profile import get_registry
    reg = get_registry()
    for name in ["default","stealth","aggressive"]:
        assert name in reg.list_names()
        p = reg.get(name)
        assert p.sleep.interval_ms > 0
        assert 0 <= p.sleep.jitter_pct <= 50

def test_c2_profile_jitter():
    from c2_profile import get_registry
    p = get_registry().get("default")
    delays = [p.jitter_delay() for _ in range(20)]
    assert all(d > 0 for d in delays)

def test_c2_profile_save_load(tmp_path):
    from c2_profile import get_registry, ProfileLoader
    p = get_registry().get("stealth")
    loader = ProfileLoader()
    saved = loader.save(p, tmp_path / "stealth.yaml")
    loaded = loader.from_yaml(saved)
    assert loaded.sleep.interval_ms == p.sleep.interval_ms

# config_store
def test_config_store(tmp_path):
    import config_store
    p = tmp_path / "payload.json"
    p.write_text(json.dumps({"rhost": "10.0.0.1", "lport": 4444}))
    old_path, old_data = config_store._payload_path, dict(config_store._data)
    config_store._payload_path = p; config_store._data = {}; config_store._last_mtime = 0.0
    try:
        assert config_store.get_config("rhost") == "10.0.0.1"
        config_store.set_config(rhost="10.99.99.99")
        assert config_store.get_config("rhost") == "10.99.99.99"
        assert json.loads(p.read_text())["rhost"] == "10.99.99.99"
    finally:
        config_store._payload_path = old_path; config_store._data = old_data; config_store._last_mtime = 0.0

# MCP registration
def test_mcp_tools_registered():
    import ast
    src = open(str(_ROOT / "skills" / "lazyown_mcp.py")).read()
    for tool in ["lazyown_memory_recall","lazyown_memory_store","lazyown_searchsploit",
                 "lazyown_misp_export","lazyown_eval_quality","lazyown_collab_publish",
                 "lazyown_c2_profile","lazyown_bridge_suggest",
                 "lazyown_session_status","lazyown_reactive_suggest",
                 "lazyown_campaign_tasks","lazyown_cron_schedule",
                 "lazyown_rag_index","lazyown_rag_query","lazyown_threat_model"]:
        assert src.count(tool) >= 2, f"{tool} not registered+handled"
    ast.parse(src)


# lazyown_bridge
def test_bridge_catalog_phases():
    from lazyown_bridge import CommandCatalog
    cat = CommandCatalog()
    phases = cat.all_phases()
    assert "recon" in phases
    assert "enum" in phases
    assert "exploit" in phases
    assert "lateral" in phases
    assert "cred" in phases


def test_bridge_by_phase():
    from lazyown_bridge import CommandCatalog
    cat = CommandCatalog()
    recon = cat.by_phase("recon")
    assert len(recon) >= 3
    # sorted by priority
    assert recon[0].priority <= recon[-1].priority


def test_bridge_service_match():
    from lazyown_bridge import CommandCatalog
    cat = CommandCatalog()
    http_entries = cat.by_service("http")
    names = [e.command for e in http_entries]
    assert "gobuster" in names or "nikto" in names or "nuclei" in names


def test_bridge_build_command():
    from lazyown_bridge import CatalogEntry
    e = CatalogEntry(
        command="gobuster",
        phase="enum",
        mitre_tactic="T1083",
        services=["http"],
        arg_template="dir -u http://{target}:{port}",
    )
    cmd = e.build_command(target="10.10.11.78", port="80")
    assert "10.10.11.78" in cmd
    assert "80" in cmd
    assert "gobuster" in cmd


def test_bridge_suggest():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    result = d.suggest(phase="recon", target="10.10.11.78")
    assert result is not None
    cmd, entry = result
    assert entry.phase == "recon"
    assert entry.command in cmd or cmd == entry.command


def test_bridge_suggest_with_services():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    result = d.suggest(phase="enum", target="10.10.11.78", services=["http:80"])
    assert result is not None
    cmd, entry = result
    assert "http" in entry.services or not entry.services


def test_bridge_suggest_excluded():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    first = d.suggest(phase="recon", target="10.10.11.78")
    assert first is not None
    first_cmd = first[1].command
    second = d.suggest(phase="recon", target="10.10.11.78", excluded={first_cmd})
    assert second is not None
    assert second[1].command != first_cmd


def test_bridge_list_all_phases():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    summary = d.catalog_summary()
    assert isinstance(summary, dict)
    for phase, cmds in summary.items():
        assert isinstance(cmds, list)
        assert len(cmds) >= 1


def test_bridge_phase_mapper():
    from lazyown_bridge import PhaseMapper
    pm = PhaseMapper()
    assert pm.to_bridge_phase("recon") == "recon"
    assert pm.to_bridge_phase("scanning") == "recon"
    assert pm.to_bridge_phase("enumeration") == "enum"
    assert pm.to_bridge_phase("exploitation") == "exploit"
    assert pm.to_bridge_phase("post_exploitation") == "postexp"
    assert pm.to_bridge_phase("lateral_movement") == "lateral"
    assert pm.to_bridge_phase("exfiltration") == "exfil"
    assert pm.to_bridge_phase("unknown") == "recon"


def test_bridge_full_catalog_count():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    assert d.catalog_count() >= 300, f"Expected 300+ commands, got {d.catalog_count()}"


def test_bridge_all_phases_populated():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    for phase in ["recon", "enum", "exploit", "postexp", "cred",
                  "lateral", "privesc", "persist", "exfil", "c2", "report"]:
        entries = d.list_phase(phase)
        assert len(entries) >= 1, f"Phase '{phase}' has no entries"


def test_bridge_suggest_sequence():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    seq = d.suggest_sequence(phase="enum", target="10.10.11.78", limit=5)
    assert len(seq) >= 1
    assert len(seq) <= 5
    for cmd, entry in seq:
        assert entry.phase == "enum"


def test_bridge_tag_selector():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    result = d.suggest(phase="enum", tag_hint="kerberos")
    assert result is not None
    _, entry = result
    assert "kerberos" in entry.tags or "ad" in entry.tags


def test_bridge_suggest_kerberos_phase():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    result = d.suggest(phase="exfil", target="10.10.11.78",
                       services=["kerberos:88", "ldap:389"],
                       has_creds=True)
    assert result is not None


def test_bridge_suggest_windows_os():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    result = d.suggest(phase="lateral", services=["winrm:5985"], has_creds=True, os_hint="windows")
    assert result is not None
    _, entry = result
    assert entry.os_target in ("windows", "any")


def test_bridge_suggest_linux_os():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    result = d.suggest(phase="postexp", os_hint="linux")
    assert result is not None
    _, entry = result
    assert entry.os_target in ("linux", "any")


def test_bridge_catalog_summary_has_all_phases():
    from lazyown_bridge import get_dispatcher
    d = get_dispatcher()
    summary = d.catalog_summary()
    for phase in ["recon", "enum", "exploit", "cred", "lateral"]:
        assert phase in summary
        assert len(summary[phase]) >= 5


# ---------------------------------------------------------------------------
# session_reader
# ---------------------------------------------------------------------------

def test_session_reader_empty(tmp_path):
    from session_reader import SessionAggregator
    agg = SessionAggregator()
    summary = agg.aggregate(tmp_path)
    assert summary.implants == []
    assert summary.tasks == []
    assert summary.discovered_hosts == []
    assert summary.command_outputs == {}


def test_session_reader_implant_csv(tmp_path):
    from session_reader import SessionAggregator, ImplantRecord
    csv_content = (
        "client_id,os,pid,hostname,ips,user,discovered_ips,"
        "result_portscan,result_pwd,command,output\n"
        "abc123,Linux,1234,webserver,10.0.0.5,root,,22/tcp open,,id,uid=0(root)\n"
    )
    (tmp_path / "abc123.log").write_text(csv_content)
    summary = SessionAggregator().aggregate(tmp_path)
    assert len(summary.implants) == 1
    rec = summary.implants[0]
    assert rec.client_id == "abc123"
    assert rec.is_privileged
    assert rec.platform == "linux"


def test_session_reader_privileged_sessions(tmp_path):
    from session_reader import SessionAggregator
    csv_root = (
        "client_id,os,pid,hostname,ips,user,discovered_ips,"
        "result_portscan,result_pwd,command,output\n"
        "c1,Linux,1,host1,10.0.0.1,root,,,, id,uid=0\n"
    )
    csv_user = (
        "client_id,os,pid,hostname,ips,user,discovered_ips,"
        "result_portscan,result_pwd,command,output\n"
        "c2,Windows,2,host2,10.0.0.2,jdoe,,,, whoami,jdoe\n"
    )
    (tmp_path / "c1.log").write_text(csv_root)
    (tmp_path / "c2.log").write_text(csv_user)
    summary = SessionAggregator().aggregate(tmp_path)
    assert len(summary.privileged_sessions) == 1
    assert summary.privileged_sessions[0].client_id == "c1"
    assert len(summary.unprivileged_sessions) == 1


def test_session_reader_tasks(tmp_path):
    from session_reader import TaskReader, TaskWriter
    writer = TaskWriter(tmp_path)
    t1 = writer.append("Recon target", "Run nmap", operator="op1")
    t2 = writer.append("Exploit SMB", "ms17-010", operator="op2", status="Started")
    tasks = TaskReader().read(tmp_path)
    assert len(tasks) == 2
    assert tasks[0].title == "Recon target"
    assert tasks[1].status == "Started"
    ok = writer.update_status(t1.id, "Done")
    assert ok
    tasks2 = TaskReader().read(tmp_path)
    assert tasks2[0].status == "Done"


def test_session_reader_discovered_hosts(tmp_path):
    from session_reader import DiscoveredHostReader
    (tmp_path / "hostsdiscovery.txt").write_text("10.0.0.1\n10.0.0.2\n10.0.0.1\n")
    hosts = DiscoveredHostReader().read(tmp_path)
    assert len(hosts) == 2  # deduped
    assert "10.0.0.1" in hosts


def test_session_reader_skips_non_implant_logs(tmp_path):
    from session_reader import ImplantCSVReader
    (tmp_path / "access.log").write_text("127.0.0.1 - GET /\n")
    (tmp_path / "searchsploit.log").write_text("ms17-010 found\n")
    records = ImplantCSVReader().read(tmp_path)
    assert records == []


# ---------------------------------------------------------------------------
# reactive_engine
# ---------------------------------------------------------------------------

def test_reactive_engine_av_detection():
    from reactive_engine import get_engine
    engine = get_engine()
    output = "Windows Defender blocked the executable: Access denied"
    decisions = engine.analyse(output=output, command="meterpreter", platform="windows")
    assert len(decisions) > 0
    # AV detection produces escalate_evasion or run_command action
    actions = [d.action for d in decisions]
    assert any(a in ("escalate_evasion", "run_command") for a in actions)
    top = decisions[0]
    assert top.priority <= 5
    assert top.mitre_tactic != ""


def test_reactive_engine_privesc_sudo():
    from reactive_engine import get_engine
    engine = get_engine()
    output = "User alice may run the following commands:\n    (ALL) NOPASSWD: ALL"
    decisions = engine.analyse(output=output, command="sudo -l", platform="linux")
    assert any(d.action == "run_command" for d in decisions)
    priv = next(d for d in decisions if d.action == "run_command")
    assert priv.command != ""


def test_reactive_engine_credential_found():
    from reactive_engine import get_engine
    engine = get_engine()
    output = "password: S3cr3t!2024\nHash: aad3b435b51404eeaad3b435b51404ee"
    decisions = engine.analyse(output=output, command="secretsdump", platform="windows")
    assert any(d.action == "record_cred" for d in decisions)


def test_reactive_engine_new_host():
    from reactive_engine import get_engine
    engine = get_engine()
    output = "Discovered host: 192.168.1.100\nHost 10.10.10.50 is up"
    decisions = engine.analyse(output=output, command="arp-scan", platform="linux")
    assert any(d.action == "add_host" for d in decisions)


def test_reactive_engine_shell_error():
    from reactive_engine import get_engine
    engine = get_engine()
    output = "Connection refused (port 445)\nError: authentication failed"
    decisions = engine.analyse(output=output, command="smbclient", platform="linux")
    assert any(d.action in ("switch_tool",) for d in decisions)


def test_reactive_engine_no_signal():
    from reactive_engine import get_engine
    engine = get_engine()
    output = "Scan complete. No findings."
    decisions = engine.analyse(output=output, command="nmap", platform="linux")
    # May be empty or only low-priority
    for d in decisions:
        assert d.priority >= 3  # no critical signals


def test_reactive_engine_priority_ordering():
    from reactive_engine import get_engine
    engine = get_engine()
    output = (
        "AMSI detected. Quarantined.\n"
        "User may run: (ALL) NOPASSWD: ALL\n"
        "password: Admin123\n"
    )
    decisions = engine.analyse(output=output, command="loader", platform="windows")
    assert len(decisions) >= 2
    priorities = [d.priority for d in decisions]
    assert priorities == sorted(priorities)  # sorted ascending by priority


# ── session_rag ───────────────────────────────────────────────────────────────
def test_session_rag_init():
    from session_rag import get_rag, SessionRAG
    rag = get_rag()
    assert isinstance(rag, SessionRAG)


def test_session_rag_stats():
    from session_rag import get_rag
    rag = get_rag()
    s = rag.stats()
    assert "backend" in s
    assert "indexed_files" in s
    assert "total_chunks" in s
    assert s["backend"] in ("chromadb", "keyword_fallback")


def test_session_rag_chunk_text():
    from session_rag import _chunk_text
    text = "A" * 1000
    chunks = _chunk_text(text, size=400, overlap=50)
    assert len(chunks) >= 2
    # Each chunk should be at most CHUNK_SIZE
    for c in chunks:
        assert len(c) <= 400


def test_session_rag_index_new():
    from session_rag import get_rag
    rag = get_rag()
    result = rag.index_new()
    assert "files" in result
    assert "chunks" in result
    assert result["files"] >= 0


def test_session_rag_query_returns_list():
    from session_rag import get_rag
    rag = get_rag()
    hits = rag.query("nmap recon", n=3)
    assert isinstance(hits, list)
    for h in hits:
        assert "text" in h
        assert "source" in h


def test_session_rag_context_for_step():
    from session_rag import get_rag
    rag = get_rag()
    ctx = rag.context_for_step(phase="recon", target="10.10.11.78", n=2)
    assert isinstance(ctx, str)
    # Either empty (no indexed docs) or contains the header
    if ctx:
        assert "[RAG context" in ctx


# ── threat_model ─────────────────────────────────────────────────────────────
def test_threat_model_builder_init():
    from threat_model import get_builder, ThreatModelBuilder
    b = get_builder()
    assert isinstance(b, ThreatModelBuilder)


def test_threat_model_build():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    assert "generated_at" in model
    assert "assets" in model
    assert "ttps" in model
    assert "ioc_registry" in model
    assert "detection_rules" in model
    assert "summary" in model


def test_threat_model_summary_fields():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    s = model["summary"]
    assert "total_events" in s
    assert "unique_targets" in s
    assert "unique_commands" in s
    assert s["total_events"] >= 0


def test_threat_model_ttps_have_required_fields():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    for ttp in model["ttps"]:
        assert "technique_id" in ttp
        assert "tactic" in ttp
        assert "severity" in ttp
        assert "occurrences" in ttp
        assert ttp["severity"] in ("low", "medium", "high", "critical")


def test_threat_model_detection_rules_structure():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    for rule in model["detection_rules"]:
        assert "rule_id" in rule
        assert rule["rule_id"].startswith("LO-")
        assert "condition" in rule
        assert "log_source" in rule
        assert "response" in rule


def test_threat_model_load_after_build():
    from threat_model import get_builder
    b = get_builder()
    b.build()
    loaded = b.load()
    assert loaded is not None
    assert "assets" in loaded


def test_threat_model_ioc_types():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    valid_types = {"ip", "domain", "hash", "credential", "url", "path"}
    for ioc in model["ioc_registry"]:
        assert ioc["type"] in valid_types


# ── session_rag persistence ────────────────────────────────────────────────
def test_session_rag_fallback_persistence(tmp_path):
    """Keyword fallback must survive a save/load cycle."""
    from session_rag import _KeywordFallback
    fb = _KeywordFallback()
    fb.add("id1", "nmap scan shows port 80 open", {"source": "test.txt", "chunk": 0})
    fb.add("id2", "found credential admin:admin123", {"source": "creds.txt", "chunk": 0})

    idx_file = tmp_path / "fallback.json"
    fb.save(idx_file)

    fb2 = _KeywordFallback()
    fb2.load(idx_file)
    assert fb2.count() == 2

    hits = fb2.query("credential admin", n=5)
    assert len(hits) >= 1
    assert "credential" in hits[0]["text"].lower()


def test_session_rag_fallback_dedup():
    """Adding the same doc_id twice must not duplicate the entry."""
    from session_rag import _KeywordFallback
    fb = _KeywordFallback()
    fb.add("same-id", "text one", {"source": "a.txt", "chunk": 0})
    fb.add("same-id", "text two", {"source": "a.txt", "chunk": 0})
    assert fb.count() == 1


def test_session_rag_fallback_ring_buffer():
    """Ring-buffer must cap at MAX_FALLBACK_DOCS and evict oldest."""
    import session_rag as _sr
    original_max = _sr.MAX_FALLBACK_DOCS
    _sr.MAX_FALLBACK_DOCS = 5
    try:
        from session_rag import _KeywordFallback
        fb = _KeywordFallback()
        for i in range(8):
            fb.add(f"id{i}", f"document {i}", {"source": "f.txt", "chunk": i})
        assert fb.count() == 5
        # Oldest entries (id0, id1, id2) should have been evicted
        ids_present = {d["id"] for d in fb._docs}
        assert "id0" not in ids_present
        assert "id7" in ids_present
    finally:
        _sr.MAX_FALLBACK_DOCS = original_max


# ── threat_model purple team ───────────────────────────────────────────────
def test_threat_model_has_purple_team():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    assert "purple_team" in model
    assert isinstance(model["purple_team"], list)


def test_threat_model_purple_team_structure():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    for p in model["purple_team"]:
        assert "technique_id" in p
        assert "gap" in p
        assert "red" in p
        assert "blue" in p
        assert "coverage" in p
        assert isinstance(p["red"], dict)
        assert "commands" in p["red"]
        assert "occurrences" in p["red"]


def test_threat_model_purple_gaps_sorted_first():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    purple = model["purple_team"]
    if len(purple) < 2:
        return  # not enough data to test ordering
    # All gap entries should appear before non-gap entries
    saw_non_gap = False
    for p in purple:
        if not p["gap"]:
            saw_non_gap = True
        if saw_non_gap and p["gap"]:
            assert False, "Gap entry appeared after a non-gap entry"


def test_threat_model_purple_coverage_field():
    from threat_model import get_builder
    b = get_builder()
    model = b.build()
    for p in model["purple_team"]:
        if p["gap"]:
            assert p["coverage"] == "none"
            assert p["blue"] is None
        else:
            assert p["coverage"] in ("partial", "full")
            assert p["blue"] is not None


# ── atomic_enricher ───────────────────────────────────────────────────────────
def test_atomic_enricher_builds():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import enrich, DST_PARQUET
    df = enrich()
    assert len(df) == 1690
    assert "platform_list" in df.columns
    assert "scope"         in df.columns
    assert "complexity"    in df.columns
    assert "has_prereqs"   in df.columns
    assert "tactic_prefix" in df.columns
    assert "keyword_tags"  in df.columns
    assert DST_PARQUET.exists()


def test_atomic_enricher_complexity_values():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import load_enriched
    df = load_enriched()
    assert set(df["complexity"].unique()).issubset({"low", "medium", "high"})


def test_atomic_enricher_scope_values():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import load_enriched
    df = load_enriched()
    assert set(df["scope"].unique()).issubset({"local", "remote", "elevated", "any"})


def test_atomic_query_keyword():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import query_atomic
    rows = query_atomic(keyword="amsi bypass", limit=5)
    assert isinstance(rows, list)
    assert len(rows) >= 1
    for r in rows:
        assert "mitre_id" in r
        assert "name" in r
        assert "complexity" in r
        assert "platform_list" in r


def test_atomic_query_mitre_prefix():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import query_atomic
    rows = query_atomic(mitre_id="T1548", limit=10)
    assert all(r["mitre_id"].startswith("T1548") for r in rows)
    assert len(rows) >= 1


def test_atomic_query_platform_filter():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import query_atomic
    rows = query_atomic(platform="linux", complexity="low", limit=10)
    for r in rows:
        assert "linux" in r["platform_list"]
    assert len(rows) >= 1


def test_atomic_query_no_prereqs():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import query_atomic
    rows = query_atomic(platform="windows", has_prereqs=False, limit=10)
    for r in rows:
        assert r["has_prereqs"] is False


def test_atomic_query_include_command():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import query_atomic
    rows = query_atomic(keyword="dump memory", include_command=True, limit=3)
    for r in rows:
        assert "command_preview" in r
        assert len(r["command_preview"]) > 0


def test_atomic_query_empty_returns_list():
    """Impossible filter combination returns empty list gracefully."""
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from atomic_enricher import query_atomic
    rows = query_atomic(keyword="xyzzy_impossible_keyword_123", limit=5)
    assert isinstance(rows, list)
    assert len(rows) == 0


def test_parquet_db_query_atomic():
    import sys; sys.path.insert(0, str(_ROOT / "skills"))
    from lazyown_parquet_db import ParquetDB
    db = ParquetDB(_ROOT)
    rows = db.query_atomic(keyword="mimikatz", platform="windows", limit=5)
    assert isinstance(rows, list)


def test_session_rag_index_parquet_sources():
    import sys; sys.path.insert(0, str(_ROOT / "modules"))
    from session_rag import get_rag
    rag = get_rag()
    result = rag.index_parquet_sources()
    assert "files" in result
    assert "chunks" in result
    # After indexing parquets, a semantic query should return hits
    hits = rag.query("privilege escalation suid linux", n=3)
    assert isinstance(hits, list)

