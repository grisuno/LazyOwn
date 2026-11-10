"""Repository-level BOF.yaml consistency for the lazyaddon beacon clients.

Every ``bofs/*.yaml`` must be a valid delivery contract naming a real
lazyaddon client; the referenced ``client_artifact`` must exist under the
client checkout when the file is present locally, and every Linux BOF
referenced by the metasploitable gym chain must stage end to end.
"""

from __future__ import annotations

from pathlib import Path

from modules.bof_admin import BOFS_DIR, scan_bofs
from modules.bof_delivery import BofDeliveryConfig, stage_bof
from modules.bof_registry import _build_default_catalog, client_addon_install_path, find_client_artifact


def test_every_yaml_is_a_valid_contract():
    rows = scan_bofs(BOFS_DIR)
    assert rows, "bofs/ entry configs missing"
    broken = [(row.file, row.error) for row in rows if not row.valid]
    assert broken == []


def test_names_unique_and_match_file():
    catalog = _build_default_catalog()
    names = list(catalog.entries)
    assert len(names) == len(set(names))
    from modules.bof_admin import load_bof

    for path in BOFS_DIR.glob("*.yaml"):
        data = load_bof(path)
        if data.get("enabled", True) and data.get("name"):
            assert data["name"] == path.stem


def test_clients_are_real_lazyaddons():
    for client in ("beacon", "blacksandbeacon"):
        assert (Path("lazyaddons") / f"{client}.yaml").is_file()
        assert client_addon_install_path(client) is not None


def test_local_artifacts_resolve_through_the_lazyaddons():
    catalog = _build_default_catalog()
    resolved = 0
    for entry in catalog.entries.values():
        artifact = find_client_artifact(entry)
        if artifact:
            resolved += 1
            assert Path(artifact).is_file()
    assert resolved >= 6, f"expected compiled artifacts for at least 6 BOFs, got {resolved}"


def test_linux_bofs_stage_for_gym():
    cfg = BofDeliveryConfig()
    for name in ("whoami_linux", "is_sudo", "suid_enum", "userenum", "cat"):
        staged = stage_bof(name, cfg)
        assert staged is not None, f"{name} failed to stage"
        assert Path(staged).is_file()
        Path(staged).unlink(missing_ok=True)


def test_gym_chain_bofs_are_catalogued():
    """The metasploitable gym chain defaults must exist in the catalog."""

    from modules.chain_registry import get as get_chain

    chain = get_chain("gym_metasploitable_ms2_beacon_bofs")
    bofs_list = [n for n in str(chain.defaults.get("bofs_run", "")).split(",") if n]
    assert bofs_list
    catalog = _build_default_catalog()
    for name in bofs_list + [str(chain.defaults.get("client", ""))]:
        if name in ("blacksandbeacon",):
            continue
        assert name in catalog.entries
