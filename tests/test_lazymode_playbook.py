"""Behaviour tests for the lazymode playbook runner."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules.lazymode_playbook import (
    is_vector_playbook,
    list_vector_playbooks,
    run_playbook,
)
from modules.playbook_admin import validate_playbook

_REPO_ROOT = Path(__file__).resolve().parent.parent

_VECTOR_PB = """name: Trivial Vector
description: test
platforms: [linux]
vector: test
steps:
- kind: lazymode
  lang: python
  run: |
    result = {"seen_target": target}
"""

_APT_PB = """apt_name: NotAVector
phases:
- name: recon
  technique_id: T1046
"""


def _write(tmp_path: Path, name: str, body: str) -> Path:
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return path


def test_is_vector_playbook_true(tmp_path):
    import yaml

    data = yaml.safe_load(_VECTOR_PB)
    assert is_vector_playbook(data) is True


def test_is_vector_playbook_false():
    import yaml

    assert is_vector_playbook(yaml.safe_load(_APT_PB)) is False


def test_list_vector_playbooks_filters(tmp_path):
    _write(tmp_path, "vec.yaml", _VECTOR_PB)
    _write(tmp_path, "apt.yaml", _APT_PB)
    names = {item["file"] for item in list_vector_playbooks(tmp_path)}
    assert names == {"vec.yaml"}


def test_run_playbook_injects_target(tmp_path):
    _write(tmp_path, "vec.yaml", _VECTOR_PB)
    outcome = run_playbook("vec.yaml", target="10.0.0.9", directory=tmp_path)
    assert outcome["ok"] is True
    assert outcome["steps"][0]["result"] == {"seen_target": "10.0.0.9"}


def test_run_playbook_resolves_by_name(tmp_path):
    _write(tmp_path, "vec.yaml", _VECTOR_PB)
    outcome = run_playbook("Trivial Vector", target="10.0.0.9", directory=tmp_path)
    assert outcome["ok"] is True


def test_run_playbook_rejects_bad_target(tmp_path):
    _write(tmp_path, "vec.yaml", _VECTOR_PB)
    with pytest.raises(ValueError):
        run_playbook("vec.yaml", target="x; rm -rf /", directory=tmp_path)


def test_run_playbook_rejects_traversal(tmp_path):
    with pytest.raises(ValueError):
        run_playbook("../payload", directory=tmp_path)


def test_shipped_metasploitable_playbooks_validate():
    import yaml

    ms2 = sorted((_REPO_ROOT / "playbooks").glob("ms2_*.yaml"))
    assert len(ms2) >= 9
    for path in ms2:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert validate_playbook(data) == [], path.name
        assert is_vector_playbook(data) is True, path.name
