# modules: finding_lifecycle

modules: finding_lifecycle groups 13 files (py) around _cache_path, _cache_load, _cache_save, _cached, _store. Database commands — workspace isolation, host/service/vuln management, nmap import...

```mermaid
graph LR
    cli["cli"]
    modules["modules"]
    tests["tests"]
    cli -- "calls into" --> modules
    tests -- "calls into" --> modules
```

## cli (13.1)

cli groups 2 files (py) around DatabaseCommandSet, _get_db, _active_workspace, do_db_init, do_db_workspace. Database commands — workspace isolation, host/service/vuln management, nmap import...

## modules (13.2)

modules groups 6 files (py) around _cache_path, _cache_load, _cache_save, _cached, _store. Attack-surface 3D intel module: C2-centred campaign graph.

## tests (13.3)

tests groups 5 files (py) around gate_env, test_gate_exact_and_fuzzy_match, test_gate_cidr_match, test_gate_task_allow_is_closed_whitelist, test_gate_blocks_asset_insert. Asset gate + un-nerfed outputs + IntelGraph CSP regression tests.

**Files**:

- cli/commands/database.py
- cli/commands/surface.py
- modules/attack_surface3d.py
- modules/estorides_fusion.py
- modules/finding_lifecycle.py
- modules/intel_fusion.py
- modules/osint_enrich.py
- modules/surface_ops.py
- tests/test_asset_gate.py
- tests/test_attack_surface3d.py
- tests/test_estorides_fusion.py
- tests/test_finding_lifecycle.py
- tests/test_intel_fusion.py
