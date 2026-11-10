"""Tests for modules/bof_admin.py — BOF YAML configuration CRUD.

Covers scan (valid + invalid files), schema validation, sandboxed
create/update/delete round-trips, path confinement and atomic saves.
"""

from __future__ import annotations

import pytest

from modules.bof_admin import (
    BOF_CATEGORIES,
    BOF_CLIENTS,
    bof_path,
    create_bof,
    delete_bof,
    load_bof,
    preview_bof,
    save_bof_yaml,
    scan_bofs,
    slugify,
    update_bof,
    validate_bof,
)

VALID = {
    "name": "demo_bof",
    "description": "Demo capability",
    "author": "LazyOwn",
    "url": "https://github.com/grisuno/blacksandbeacon",
    "source_file": "bof/demo_bof/bof.c",
    "client": "blacksandbeacon",
    "platform": "linux",
    "category": "reconnaissance",
    "client_artifact": "build/bof/demo_bof.x64.o",
    "required_args": [],
    "optional_args": [],
    "mitre_technique": "T1033",
    "enabled": True,
}


@pytest.fixture
def bofs_dir(tmp_path):
    return str(tmp_path / "bofs")


class TestValidate:
    def test_valid_document(self):
        assert validate_bof(VALID) == []

    def test_non_mapping(self):
        assert validate_bof(["nope"]) == ["document must be a mapping"]

    def test_unknown_client(self):
        errors = validate_bof({**VALID, "client": "mettle"})
        assert any("unknown client" in e for e in errors)

    def test_platform_client_mismatch(self):
        errors = validate_bof({**VALID, "client": "beacon"})
        assert any("delivers windows" in e for e in errors)

    def test_bad_artifact_escapes(self):
        errors = validate_bof({**VALID, "client_artifact": "../../etc/x"})
        assert any("client_artifact" in e for e in errors)

    def test_bad_mitre(self):
        errors = validate_bof({**VALID, "mitre_technique": "X9999"})
        assert any("mitre_technique" in e for e in errors)

    def test_missing_required_field(self):
        data = {k: v for k, v in VALID.items() if k != "source_file"}
        errors = validate_bof(data)
        assert any("source_file" in e for e in errors)

    def test_bad_name_slug(self):
        errors = validate_bof({**VALID, "name": "Bad Name"})
        assert any("invalid name" in e for e in errors)

    def test_args_lists(self):
        errors = validate_bof({**VALID, "required_args": ["good", 42]})
        assert any("required_args" in e for e in errors)


class TestPathConfine:
    def test_rejects_traversal(self, tmp_path):
        with pytest.raises(ValueError):
            bof_path("../evil", tmp_path)

    def test_appends_suffix(self, tmp_path):
        target = bof_path("demo", tmp_path)
        assert target.name == "demo.yaml"
        assert target.parent == tmp_path.resolve()


class TestCrud:
    def test_create_and_load_roundtrip(self, bofs_dir):
        path = create_bof(
            "demo", name="demo", description="Demo capability", client="blacksandbeacon", directory=bofs_dir
        )
        data = load_bof(path)
        assert data["name"] == "demo"
        assert data["client"] == "blacksandbeacon"
        assert validate_bof(data) == []

    def test_create_duplicate_refused(self, bofs_dir):
        create_bof("demo", directory=bofs_dir)
        with pytest.raises(FileExistsError):
            create_bof("demo", directory=bofs_dir)

    def test_update_rewrites(self, bofs_dir):
        path = create_bof("demo", directory=bofs_dir)
        data = load_bof(path)
        data["description"] = "updated"
        update_bof(path, data, directory=bofs_dir)
        assert load_bof(path)["description"] == "updated"

    def test_delete(self, bofs_dir):
        create_bof("demo", directory=bofs_dir)
        assert delete_bof("demo.yaml", directory=bofs_dir) is True
        assert delete_bof("demo.yaml", directory=bofs_dir) is False

    def test_save_yaml_renames_from_stem(self, bofs_dir):
        create_bof("demo", directory=bofs_dir)
        saved = save_bof_yaml(
            "demo",
            """name: demo
description: replace
author: LazyOwn
url: https://github.com/grisuno/blacksandbeacon
source_file: bof/demo/bof.c
client: blacksandbeacon
platform: linux
category: reconnaissance
client_artifact: build/bof/demo.x64.o
required_args: []
optional_args: []
mitre_technique: T1033
enabled: true
""",
            directory=bofs_dir,
        )
        assert saved.name == "demo.yaml"
        assert load_bof(saved)["description"] == "replace"

    def test_save_yaml_bad_document_refused(self, bofs_dir):
        create_bof("demo", directory=bofs_dir)
        with pytest.raises(ValueError):
            save_bof_yaml("demo", "{ not yaml", directory=bofs_dir)


class TestScan:
    def test_scan_reports_invalid_file(self, bofs_dir):
        create_bof("demo", directory=bofs_dir)
        from pathlib import Path

        bad = Path(bofs_dir) / "broken.yaml"
        bad.write_text("client: not_a_client\n")
        rows = scan_bofs(bofs_dir)
        by_file = {row.file: row for row in rows}
        assert by_file["demo.yaml"].valid is True
        assert by_file["broken.yaml"].valid is False
        assert "unknown client" in by_file["broken.yaml"].error

    def test_preview_bounded(self, bofs_dir):
        path = create_bof("demo", directory=bofs_dir)
        text = preview_bof(path, limit=3)
        assert len(text.splitlines()) <= 4


class TestSlug:
    def test_slugify(self):
        assert slugify("Who Am I BOF!") == "who_am_i_bof"


def test_constants():
    assert BOF_CLIENTS == ("beacon", "blacksandbeacon")
    assert "reconnaissance" in BOF_CATEGORIES
