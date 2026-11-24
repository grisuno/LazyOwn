"""ShadowParser contracts: crypt hashes and root access from shadow dumps."""

from __future__ import annotations

from pathlib import Path

from skills.lazyown_facts import Config, FactStore, ShadowParser

_SHADOW_CONTENT = (
    "uid=0(root) gid=0(root) groups=0(root)\n"
    "hostname: dockerlab\n"
    "root:$6$saltstring$hashhashhashhash:19000:0:99999:7:::\n"
    "daemon:*:19000:0:99999:7:::\n"
    "svc:$y$9$pepper$morehash:19010:0:99999:7:::\n"
    "ops:$2b$12$roundsalt$hashvaluehere:19010:0:99999:7:::\n"
)


def test_can_parse_by_content_and_filename():
    """Given shadow material, When matched, Then content or filename fires."""
    parser = ShadowParser()
    assert parser.can_parse("10.0.0.55_docker_escape.txt", _SHADOW_CONTENT) is True
    assert parser.can_parse("shadow_dump.txt", "root:x:0:0:root:/root:/bin/bash") is True
    assert parser.can_parse("plain.txt", "uid=0(root) gid=0(root)") is False


def test_parse_extracts_crypt_credentials():
    """Given crypt lines, When parsed, Then each user yields a typed hash fact."""
    creds, shares, access, _vulns, _paths = ShadowParser().parse_extended("10.0.0.55", _SHADOW_CONTENT, "spool.txt")
    by_user = {cred.username: cred for cred in creds}
    assert set(by_user) == {"root", "svc", "ops"}
    assert by_user["root"].hash_type == "SHA-512-crypt"
    assert by_user["root"].hash_value.startswith("$6$saltstring$")
    assert by_user["svc"].hash_type == "yescrypt"
    assert by_user["ops"].hash_type == "bcrypt"
    assert shares == []


def test_locked_accounts_are_skipped():
    """Given a locked account, When parsed, Then no credential fact exists."""
    creds, _shares, _access, _vulns, _paths = ShadowParser().parse_extended(
        "10.0.0.55", "daemon:*:19000:0:99999:7:::\n", "spool.txt"
    )
    assert creds == []


def test_unknown_prefix_is_skipped():
    """Given an unmodelled crypt prefix, When parsed, Then no credential fact exists."""
    content = "root:$99$salt$hash:19000:0:99999:7:::\n"
    parser = ShadowParser()
    assert parser.can_parse("plain.txt", content) is True
    creds, _shares, access, _vulns, _paths = parser.parse_extended("10.0.0.55", content, "spool.txt")
    assert creds == []
    assert access[0].level == "root"


def test_access_root_fact_when_shadow_present():
    """Given any shadow-like line, When parsed, Then root access is recorded."""
    _creds, _shares, access, _vulns, _paths = ShadowParser().parse_extended("10.0.0.55", _SHADOW_CONTENT, "spool.txt")
    assert len(access) == 1
    assert access[0].level == "root"
    assert access[0].method == "shadow-read"


def test_locked_only_dump_gets_access_fact(tmp_path: Path):
    """Given a shadow dump with locked accounts only, When ingested, Then root access records."""
    content = "uid=0(root) gid=0(root)\nroot:*::0:::::\nbin:!::0:::::\n"
    creds, _shares, access, _vulns, _paths = ShadowParser().parse_extended("10.0.0.55", content, "escape.txt")
    assert creds == []
    assert access and access[0].level == "root" and access[0].method == "shadow-read"


def test_factstore_ingest_text_end_to_end(tmp_path: Path):
    """Given a spooled escape output, When ingested, Then facts land per host."""
    spool = tmp_path / "10.0.0.55_docker_escape.txt"
    spool.write_text(_SHADOW_CONTENT, encoding="utf-8")
    cfg = Config(
        base_dir=tmp_path,
        sessions_dir=tmp_path,
        facts_file=tmp_path / "policy_facts.json",
        xml_glob="",
        txt_glob="*.txt",
        log_level="CRITICAL",
    )
    store = FactStore(cfg)
    ingested = store.ingest_text(spool, host_hint="10.0.0.55")
    assert ingested == 4
    host = store._data["10.0.0.55"]
    assert {(cred.username, cred.hash_type) for cred in host.credentials} == {
        ("root", "SHA-512-crypt"),
        ("svc", "yescrypt"),
        ("ops", "bcrypt"),
    }
    assert host.access[0].level == "root"
    assert str(spool) in host.raw_files
