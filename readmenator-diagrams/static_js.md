# static/js

static/js groups 43 files (c, js, py, sh) around FieldKind, Severity, FieldSpec, ValidationIssue, _validate_string. ``assign`` business logic.

```mermaid
graph LR
    cli["cli"]
    contrib["contrib"]
    core["core"]
    lazyc2["lazyc2"]
    lazyown_docker["lazyown-docker"]
    modules["modules"]
    root["root"]
    static["static"]
    tests["tests"]
    cli -- "calls into" --> core
    cli -- "calls into" --> static
    contrib -- "depends on" --> core
    lazyc2 -- "calls into" --> core
    modules -- "depends on" --> core
    modules -- "depends on" --> lazyown_docker
    root -- "depends on" --> core
    static -- "depends on" --> cli
    static -- "depends on" --> core
    static -- "depends on" --> lazyc2
    static -- "depends on" --> lazyown_docker
    static -- "depends on" --> modules
    tests -- "calls into" --> cli
    tests -- "calls into" --> core
    tests -- "calls into" --> lazyc2
```

## cli (7.1)

cli groups 7 files (py) around apply_assign, format_payload, style, active_tokens, paint. ``assign`` business logic.

## contrib (7.2)

contrib groups 1 files (py) around generate_key_iv, main.

## core (7.3)

core groups 6 files (py) around FieldKind, Severity, FieldSpec, ValidationIssue, _validate_string. Symmetric primitives used by the framework.

## lazyc2 (7.4)

lazyc2 groups 2 files (py) around AddonCreatorConfig, live_placeholders, ParamSpec, to_dict, AddonDraft. LazyAddon creator contract for the LazyOwn C2 web interface.

## lazyown-docker (7.5)

lazyown-docker groups 1 files (sh).

## modules (7.6)

modules groups 3 files (c, py) around _GNU_SOURCE, MQUEUE_NUM, INBOUND, OUTBOUND, DESC_MAX. gcc exp.c -o exp -l mnl -l nftnl -w

## root (7.7)

root groups 1 files (py) around main.

## static (7.8)

static groups 14 files (js) around As, Be, Cs, Do, Ds. Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph...

## tests (7.9)

tests groups 8 files (py) around crypto_module, tmp_sessions, TestAutoCryptoConfig, test_default_config, test_custom_config. Tests for cli.auto_crypto — automatic session data encryption.

**Files**:

- cli/assign.py
- cli/auto_crypto.py
- cli/commands/params_ops.py
- cli/commands/session_ops.py
- cli/session_resumer.py
- cli/show.py
- cli/style.py
- contrib/legacy/lazybinenc.py
- core/crypto.py
- core/param_registry.py
- core/payload_schema.py
- core/process.py
- core/prompt.py
- core/protocols.py
- key.py
- lazyc2/addon_creator.py
- lazyc2/state.py
- lazyown-docker/init.sh
- modules/exp.c
- modules/rootkit/rootkit.c
- modules/search.py
- static/js/3d-force-graph-1.73.4.min.js
- static/js/bootstrap-4.5.2.min.js
- static/js/bootstrap-5.3.0.bundle.min.js
- static/js/chart.min.js
- static/js/force-graph-1.43.5.min.js
- static/js/html2pdf.bundle.min.js
- static/js/jquery-3.5.1.slim.min.js
- static/js/particles.js
- static/js/popper-2.5.4.min.js
- static/js/quill-2.0.3.js
- static/js/showdown-2.1.0.min.js
- static/js/tippy-6.js
- static/js/vis-network-9.1.2.min.js
- static/js/vis-network.min.js
- tests/test_auto_crypto.py
- tests/test_cli_assign.py
- tests/test_core.py
- tests/test_core_config.py
- tests/test_param_registry.py
- tests/test_payload_schema.py
- tests/test_php2shell_addon.py
- tests/test_placeholder_coverage.py
