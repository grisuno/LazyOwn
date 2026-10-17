"""Playbook YAML administration: scan, create, update, delete, validate."""

from __future__ import annotations

import yaml

from modules.playbook_admin import (
    create_playbook,
    delete_playbook,
    playbook_kind,
    playbook_path,
    preview_playbook,
    save_playbook_yaml,
    scan_playbooks,
    slugify,
    update_playbook,
    validate_playbook,
)


def _write(directory, name, data):
    path = directory / name
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def test_scan_reports_apt_and_plan_shapes(tmp_path):
    """Both on-disk shapes are summarized with the right kind and counts."""
    _write(
        tmp_path,
        "apt_demo.yaml",
        {
            "apt_name": "Demo APT",
            "description": "demo",
            "platforms": ["linux", "windows"],
            "phases": [
                {"name": "execution", "technique_id": "T1059", "atomic_tests": [{}, {}]},
                {"name": "impact", "technique_id": "T1485", "atomic_tests": [{}]},
            ],
        },
    )
    _write(
        tmp_path,
        "attack_plan.yaml",
        {"apt_name": "Plan", "description": "plan", "steps": [{"atomic_id": "T1"}, {"atomic_id": "T2"}]},
    )
    (tmp_path / "broken.yaml").write_text("apt_name: [", encoding="utf-8")

    rows = {row.file: row for row in scan_playbooks(tmp_path)}
    assert rows["apt_demo.yaml"].kind == "apt"
    assert rows["apt_demo.yaml"].steps == 3
    assert rows["apt_demo.yaml"].phases == 2
    assert rows["apt_demo.yaml"].valid is True
    assert rows["attack_plan.yaml"].kind == "plan"
    assert rows["attack_plan.yaml"].steps == 2
    assert rows["broken.yaml"].valid is False
    assert rows["broken.yaml"].error


def test_validate_rejects_mixed_and_empty(tmp_path):
    """Mixed shapes and missing names are validation errors."""
    assert validate_playbook({"phases": [], "steps": []}) == [
        "apt_name is required",
        "playbook cannot declare both phases and steps",
    ]
    assert validate_playbook([]) == ["playbook must be a mapping"]
    assert validate_playbook({"apt_name": "x", "phases": [{"technique_id": "T1"}]}) == ["phase #1 name is required"]


def test_create_update_and_delete_round_trip(tmp_path):
    """CRUD writes valid YAML confined to the directory."""
    path = create_playbook("demo", name="Demo", description="new", platforms=["linux"], directory=tmp_path)
    assert path.name == "demo.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["apt_name"] == "Demo"
    assert playbook_kind(data) == "apt"

    data["phases"] = [
        {"name": "initial_access", "technique_id": "T1566", "atomic_tests": [{"atomic_id": "T1566"}]}
    ]
    update_playbook(path, data, directory=tmp_path)
    assert scan_playbooks(tmp_path)[0].steps == 1

    raw = yaml.safe_dump({"apt_name": "Demo", "phases": []}, sort_keys=False)
    save_playbook_yaml("demo.yaml", raw, directory=tmp_path)
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["apt_name"] == "Demo"
    assert delete_playbook("demo.yaml", directory=tmp_path) is True
    assert scan_playbooks(tmp_path) == []


def test_create_refuses_overwrite_and_escape(tmp_path):
    """Existing files and path traversal are rejected."""
    create_playbook("demo", directory=tmp_path)
    try:
        create_playbook("demo", directory=tmp_path)
    except FileExistsError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected FileExistsError")
    create_playbook("demo", directory=tmp_path, overwrite=True)
    assert playbook_path("demo", tmp_path) == (tmp_path / "demo.yaml").resolve()
    try:
        playbook_path("../escape", tmp_path)
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")


def test_slug_and_preview(tmp_path):
    """Slugs are filesystem-safe and previews are bounded."""
    assert slugify("My Demo APT!") == "my_demo_apt"
    path = _write(tmp_path, "apt_demo.yaml", {"apt_name": "Demo", "phases": []})
    preview = preview_playbook(path, limit=2)
    assert "apt_name: Demo" in preview
    assert preview.count("\n") <= 3
