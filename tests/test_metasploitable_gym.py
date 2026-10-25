"""Metasploitable 2 gym BDD contract: one exploit, one chain, one index entry.

Every scenario states Given, When, Then. The matrix must stay complete:
a vulnerability without a valid exploit or chain is a broken lab path.
"""

from __future__ import annotations

import yaml

from modules.atomic_exploit_bridge import load_all as load_exploits
from modules.chain_registry import get as get_chain
from modules.metasploitable_gym import (
    chain_for,
    exploit_for,
    get,
    summary,
    validate_matrix,
    vulnerabilities,
)


def test_index_covers_the_ms2_vectors():
    """Given the shipped index, When listed, Then every vector has both artefacts."""
    entries = vulnerabilities()
    assert len(entries) >= 20
    assert len({entry["id"] for entry in entries}) == len(entries)
    matrix_errors = validate_matrix()
    assert matrix_errors == []
    assert summary()["target"] == "Metasploitable 2"
    ids = {entry["id"] for entry in entries}
    assert {
        "ms2_dvwa_sqli",
        "ms2_dvwa_sqli_blind",
        "ms2_dvwa_xss_reflected",
        "ms2_dvwa_xss_stored",
        "ms2_dvwa_xss_dom",
        "ms2_dvwa_csrf",
        "ms2_dvwa_lfi",
        "ms2_dvwa_file_upload",
        "ms2_dvwa_brute_force",
        "ms2_mutillidae_xss",
        "ms2_mutillidae_lfi",
        "ms2_mutillidae_command_injection",
        "ms2_php_cgi_arg_injection",
        "ms2_webdav_put",
    } <= ids


def test_every_exploit_and_chain_is_loadable():
    """Given the matrix, When each entry resolves, Then the catalogue and chain registry agree."""
    exploits = load_exploits()
    for entry in vulnerabilities():
        assert entry["exploit"] in exploits
        assert exploit_for(entry["id"]) is not None
        chain = chain_for(entry["id"])
        assert chain is not None
        assert chain.defaults["exploit"] == entry["exploit"]
        assert chain.defaults["vuln"] == entry["id"]
        assert chain.extends == "gym_metasploitable_chain"


def test_gym_base_ends_with_interactive_shell():
    """Given the gym base chain, When resolved, Then it opens the shell after reporting."""
    base = get_chain("gym_metasploitable_chain")
    assert base is not None
    assert base.steps[-1].run == "atomic_shell --interactive {target}"
    for entry in vulnerabilities():
        chain = get_chain(entry["chain"])
        assert chain is not None
        assert chain.steps[-1].run == "atomic_shell --interactive {target}"


def test_every_chain_resolves_without_unresolved_tokens():
    """Given a target, When each chain resolves, Then no step hides an unresolved token."""
    tokens = {"target": "192.0.2.55", "lhost": "127.0.0.1", "lport": "4444"}
    for entry in vulnerabilities():
        chain = get_chain(entry["chain"])
        assert chain is not None
        resolved = chain.resolve(tokens)
        assert resolved
        for step in resolved:
            if step["skipped"]:
                assert "unresolved token" not in step["reason"], (entry["id"], step["run"], step["reason"])
            else:
                assert entry["exploit"] in step["run"] or not step["run"].startswith("python3 modules")


def test_unknown_vulnerability_returns_none():
    """Given an unknown id, When looked up, Then every accessor returns None."""
    assert get("ghost") is None
    assert chain_for("ghost") is None
    assert exploit_for("ghost") is None


def test_invalid_matrix_is_reported(tmp_path):
    """Given a broken index, When validated, Then every missing artefact is named."""
    from modules.metasploitable_gym import validate_matrix as validate

    index = {
        "name": "gym_metasploitable",
        "version": 1,
        "vulnerabilities": [
            {"id": "Bad Id", "name": "x"},
            {"id": "demo", "name": "Demo", "mitre": "T1190", "port": "1", "service": "http", "severity": "high",
             "exploit": "missing_exploit", "chain": "missing_chain"},
        ],
    }
    path = tmp_path / "gym.yaml"
    path.write_text(yaml.safe_dump(index), encoding="utf-8")
    errors = validate(path)
    assert any("invalid vulnerability id" in error for error in errors)
    assert any("missing mitre" in error for error in errors)
    assert any("exploit 'missing_exploit' not loaded" in error for error in errors)
    assert any("chain 'missing_chain' not loaded" in error for error in errors)
