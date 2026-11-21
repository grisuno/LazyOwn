"""Crack consumer contracts: FactStore crypt hashes -> stores for lateral spray."""

from __future__ import annotations

from pathlib import Path

from modules.crack_consumer import consume, export_facts, render_summary
from modules.hash_cracker import CrackResult, HashCracker
from skills.lazyown_facts import Config, CredentialFact, FactStore


def _store(tmp_path: Path, host: str = "10.0.0.55") -> FactStore:
    cfg = Config(
        base_dir=tmp_path,
        sessions_dir=tmp_path,
        facts_file=tmp_path / "policy_facts.json",
        xml_glob="",
        txt_glob="*.txt",
        log_level="CRITICAL",
    )
    return FactStore(cfg)


def _add_creds(store: FactStore, host: str) -> None:
    facts = store._host(host)
    facts.credentials.append(
        CredentialFact(host=host, username="root", password="", source_file="spool.txt",
                       hash_value="$6$saltstring$hashhashhashhash", hash_type="SHA-512-crypt")
    )
    facts.credentials.append(
        CredentialFact(host=host, username="svc", password="", source_file="spool.txt",
                       hash_value="$y$9$pepper$morehash", hash_type="yescrypt")
    )
    facts.credentials.append(
        CredentialFact(host=host, username="ntlm-user", password="", source_file="spool.txt",
                       hash_value="0123456789abcdef0123456789abcdef", hash_type="MD4/NTLM")
    )


def _fake_cracker(monkeypatch, results: list[CrackResult]):
    from modules.world_model import get_world_model

    class FakeCracker:
        def __init__(self, wordlist=None) -> None:
            self.wordlist = wordlist

        def crack_file(self, path, wordlist=None):
            return list(results)

        def import_to_db(self, cracked, rhost=""):
            return len(cracked)

        def import_to_world_model(self, cracked, host=""):
            world = get_world_model()
            count = 0
            for result in cracked:
                username = result.hash_value.split(":")[0] if ":" in result.hash_value else ""
                world.add_credential(f"{username}:{result.password}", host="", service="local")
                count += 1
            return count

    return FakeCracker()


def test_export_writes_only_crypt_facts(tmp_path: Path):
    """Given mixed hash facts, When exported, Then only crypt rows land in the file."""
    store = _store(tmp_path)
    _add_creds(store, "10.0.0.55")
    path = tmp_path / "hashes_10.0.0.55.txt"
    count = export_facts("10.0.0.55", path, store=store)
    assert count == 2
    text = path.read_text()
    assert "root:$6$saltstring$hashhashhashhash" in text
    assert "svc:$y$9$pepper$morehash" in text
    assert "0123456789abcdef0123456789abcdef" not in text


def test_export_empty_produces_nothing(tmp_path: Path):
    """Given a host without facts, When exported, Then zero rows are written."""
    store = _store(tmp_path)
    path = tmp_path / "hashes_nobody.txt"
    assert export_facts("10.9.9.9", path, store=store) == 0
    assert not path.exists()


def test_identify_accepts_all_crypt_prefixes():
    """Given crypt lines, When identified, Then every glibc prefix resolves."""
    assert HashCracker().identify("root:$1$ab$" + "d" * 22 + ":19000:0:99999:7:::").hash_type == "md5crypt"
    assert HashCracker().identify("root:$5$salt$hashhashhashhash:19000:0:99999:7:::").hash_type == "sha256crypt"
    assert HashCracker().identify("root:$6$salt$hashhashhashhash:19000:0:99999:7:::").hash_type == "sha512crypt"
    assert HashCracker().identify("ops:$2b$12$" + "a" * 53 + ":19010:0:99999:7:::").hash_type == "bcrypt"
    assert HashCracker().identify("svc:$y$9$pepper$morehash:19010:0:99999:7:::").hash_type == "yescrypt"
    assert HashCracker().identify("g:$gy$j9T$salt$hashhashhash:19010:0:99999:7:::").hash_type == "gost_yescrypt"
    assert HashCracker().identify("s:$7$C6..$salt$hashhashhash:19010:0:99999:7:::").hash_type == "scrypt"


def test_consume_cracks_and_feeds_world_model(tmp_path: Path, monkeypatch):
    """Given a cracked result, When consumed, Then the world model holds user:pass."""
    store = _store(tmp_path)
    _add_creds(store, "10.0.0.55")
    fake = _fake_cracker(
        monkeypatch,
        [CrackResult(hash_value="root:$6$saltstring$hashhashhashhash",
                     password="Password1!", hash_type="sha512crypt",
                     format="sha512crypt", cracked=True, cracker="john")],
    )
    summary = consume("10.0.0.55", cracker=fake, store=store, sessions_dir=tmp_path)
    assert summary["identified"] == 2
    assert summary["cracked"] == 1
    assert summary["db_imported"] == 1
    assert summary["world_model"] == 1
    assert summary["users"] == ["root"]
    from modules.world_model import get_world_model

    world = get_world_model()
    values = [cred.value for cred in world.list_credentials()] if hasattr(world, "list_credentials") else None
    if values is None:
        values = [c.value for c in world._creds]
    assert "root:Password1!" in values


def test_consume_without_hashes_is_noop(tmp_path: Path):
    """Given no crypt facts, When consumed, Then summary is empty and no file remains."""
    store = _store(tmp_path)
    summary = consume("10.9.9.9", cracker=object(), store=store, sessions_dir=tmp_path)
    assert summary["identified"] == 0
    assert not (tmp_path / "hashes_10.9.9.9.txt").exists()


def test_consume_survives_broken_backend(tmp_path: Path):
    """Given a broken cracker, When consumed, Then the summary fails open."""
    store = _store(tmp_path)
    _add_creds(store, "10.0.0.55")

    class Boom:
        def crack_file(self, *args, **kwargs):
            raise RuntimeError("boom")

    summary = consume("10.0.0.55", cracker=Boom(), store=store, sessions_dir=tmp_path)
    assert summary["identified"] == 2
    assert summary["cracked"] == 0


def test_render_summary_masks_passwords():
    """Given a summary, When rendered, Then no password material appears."""
    lines = render_summary(
        {
            "file": "sessions/hashes_10.0.0.55.txt",
            "identified": 2,
            "cracked": 1,
            "db_imported": 1,
            "world_model": 1,
            "users": ["root"],
        }
    )
    assert any("cracked: 1/2" in line for line in lines)
    assert any("root" in line for line in lines)
    assert not any("Password1!" in line for line in lines)


def test_lateral_planner_sprays_world_model_cred(tmp_path: Path):
    """Given an unbound world-model cred, When planned, Then crackmapexec sprays it."""
    from modules.loop.lateral_planner import plan_lateral

    hosts = {
        "10.0.0.55": {"ip": "10.0.0.55", "services": {"445": {"port": 445, "name": "smb"}}},
    }
    proposals = plan_lateral(hosts, [{"value": "root:Password1!", "host": "", "service": ""}])
    assert proposals
    assert proposals[0].command.startswith("crackmapexec smb 10.0.0.55 -u root -p ")
