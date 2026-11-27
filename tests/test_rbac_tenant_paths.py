"""SDD regression tests for tenant-id path containment in lazy_rbac.

Pins the fixed behavior for CodeQL #1057: tenant identifiers reaching
path expressions (payload files, sessions directories) must pass a
strict allowlist before any path is built or created.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def test_validate_tenant_id_allows_slugs():
    from modules.lazy_rbac import _validate_tenant_id

    assert _validate_tenant_id("acme_corp") == "acme_corp"
    assert _validate_tenant_id("default") == "default"
    assert _validate_tenant_id("t" + "0" * 63) == "t" + "0" * 63


def test_validate_tenant_id_rejects_bad_ids():
    from modules.lazy_rbac import _validate_tenant_id

    for bad in (
        "../evil",
        "..",
        "",
        "a/b",
        "a b",
        "A_upper",
        "id;rm",
        "id$(id)",
        "id\n",
        "x" * 65,
        "café",
    ):
        with pytest.raises(ValueError):
            _validate_tenant_id(bad)


def test_tenant_sessions_dir_containment(monkeypatch, tmp_path):
    from modules.lazy_rbac import _tenant_sessions_dir

    monkeypatch.chdir(tmp_path)
    assert _tenant_sessions_dir("acme") == os.path.join("sessions", "acme")
    for bad in ("../evil", "a/b", "", "id$(id)", "x" * 65):
        with pytest.raises(ValueError):
            _tenant_sessions_dir(bad)
    assert not (tmp_path / "evil").exists()


def test_create_tenant_slugifies_and_containment(monkeypatch, tmp_path):
    from modules.lazy_rbac import TenantManager

    monkeypatch.chdir(tmp_path)
    manager = TenantManager(
        payloads_dir=str(tmp_path / "payloads"),
        config_path=str(tmp_path / "config.json"),
        default_payload=str(tmp_path / "payload.json"),
    )
    tc = manager.create_tenant("Evil/../Name <script>")
    assert tc.tenant_id == "evil_name_script"
    assert (tmp_path / "sessions" / "evil_name_script").is_dir()
    assert not (tmp_path / "evil").exists()


def test_slugify_caps_length():
    from modules.lazy_rbac import TENANT_ID_MAX_CHARS, _slugify

    slug = _slugify("A" * (TENANT_ID_MAX_CHARS + 10) + "!!!tail")
    assert len(slug) <= TENANT_ID_MAX_CHARS
    assert not slug.endswith("_")
