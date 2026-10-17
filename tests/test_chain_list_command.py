"""BDD: chain list exposes the YAML chain registry.

Given the command set, When chain list runs, Then every chain appears
with state, resolved steps and playbook; a filter narrows the result.
"""

from __future__ import annotations

from cli.commands.exploit_migrated import ExploitMigratedCommandSet


def test_chain_list_lists_registry(capsys):
    """Given the registry, When chain list runs, Then apt and gym chains are visible."""
    ExploitMigratedCommandSet().do_chain("list")
    output = capsys.readouterr().out
    assert "apt_chain" in output
    assert "gym_metasploitable_chain" in output
    assert "gym_metasploitable_ms2_dvwa_sqli" in output
    assert "chain(s)" in output


def test_chain_list_filters(capsys):
    """Given a filter, When chain list runs, Then only matching chains appear."""
    ExploitMigratedCommandSet().do_chain("list gym_metasploitable_ms2")
    output = capsys.readouterr().out
    assert "gym_metasploitable_ms2_dvwa_sqli" in output
    assert "apt_chain " not in output.split("chain(s)")[0]
    assert "chain(s)" in output
