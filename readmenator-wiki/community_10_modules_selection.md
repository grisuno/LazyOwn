# modules/selection

*Community 10 | 26 files | cohesion 0.59*

## Definition

This community groups 26 file(s) rooted at `modules/selection` with dominant language py (cohesion 0.59). Central symbols: `ActionDecision`, `AdversarySelector`, `AtomicSelector`, `ChainSelector`, `CredentialSpraySelector`, `EDBSelector`, `IntelSelector`, `ModuleInfo`. Core file: `modules/module_registry.py` (30 symbols). Documented purpose: Shared selector for the best vetted chain given phase, platform and services.  Both the autonomous daemon's ChainSelector and the LazyLoopEngine planner need to.

## Files

### `modules/selection` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/selection/__init__.py` | py | utility | 0 | yes |
| `modules/selection/adversary.py` | py | utility | 6 | yes |
| `modules/selection/atomic.py` | py | utility | 2 | yes |
| `modules/selection/base.py` | py | utility | 4 | yes |
| `modules/selection/chain.py` | py | utility | 3 | yes |
| `modules/selection/cred_spray.py` | py | utility | 2 | yes |
| `modules/selection/edb.py` | py | utility | 2 | no |
| `modules/selection/intel.py` | py | utility | 7 | yes |

### `tests` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_intel_selector.py` | py | testing | 16 | yes |
| `tests/test_loop_fire_pending.py` | py | testing | 14 | yes |
| `tests/test_module_registry.py` | py | testing | 29 | yes |
| `tests/test_poc_registry.py` | py | testing | 29 | yes |
| `tests/test_selection_module.py` | py | testing | 10 | yes |
| `tests/test_selection_technique.py` | py | testing | 21 | yes |
| `tests/test_selection_wiring.py` | py | testing | 13 | yes |
| `tests/test_selectors_base.py` | py | testing | 9 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/chain_match.py` | py | utility | 7 | yes |
| `modules/module_registry.py` | py | utility | 30 | yes |
| `modules/reverse-shell.c` | c | utility | 2 | no |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/select2-4.1.0.min.js` | js | utility | 3 | yes |

*... and 6 more files in this community.*


## Key Symbols

- `normalize_tags` (function, `modules/chain_match.py:49`) `def normalize_tags(tags)` - Return a chain's tags lowercased and aliased to the shared vocabulary.
- `service_tokens` (function, `modules/chain_match.py:65`) `def service_tokens(services)` - Normalise discovered service names into the chain tag vocabulary.
- `platform_ok` (function, `modules/chain_match.py:75`) `def platform_ok(platforms, os_hint)` - Return True when a chain's platforms admit the target OS hint.
- `score` (function, `modules/chain_match.py:86`) `def score(tags, phase, svc_tokens)` - Score one chain's tags for the phase and discovered services.
- `reset_cache` (function, `modules/chain_match.py:101`) `def reset_cache()` - Clear the process-wide registry scan cache (tests, long-lived loops).
- `load_rows` (function, `modules/chain_match.py:109`) `def load_rows(allow_lab, ttl)` - Return enabled, valid, non-lab chain rows, cached for the TTL.
- `best_chain` (function, `modules/chain_match.py:139`) `def best_chain(phase, os_hint, services, exclude, allow_lab, rows, ttl)` - Return the ``(name, reason)`` of the best matching chain, or None.
- `_classify` (function, `modules/module_registry.py:91`) `def _classify(category)`
- `_classify_module_source` (function, `modules/module_registry.py:162`) `def _classify_module_source(name, source)` - Classify a Python module by its name and source content.
- `_extract_docstring_summary` (function, `modules/module_registry.py:180`) `def _extract_docstring_summary(source)` - Extract the first line of a module's docstring.
- `ModuleInfo` (class, `modules/module_registry.py:194`) `class ModuleInfo` - Metadata for a single discoverable module.
- `__init__` (method, `modules/module_registry.py:216`) `def __init__(self, name, module_type, author, version, description, category, pa`
- `to_dict` (method, `modules/module_registry.py:246`) `def to_dict(self)`
- `__repr__` (method, `modules/module_registry.py:263`) `def __repr__(self)`
- `ModuleRegistry` (class, `modules/module_registry.py:267`) `class ModuleRegistry` - Scans and indexes all discoverable modules in the framework.
- `__init__` (method, `modules/module_registry.py:279`) `def __init__(self, base_dir)`
- `get_instance` (method, `modules/module_registry.py:285`) `def get_instance(cls, base_dir)` - Return the singleton registry instance.
- `scan` (method, `modules/module_registry.py:291`) `def scan(self)` - Scan all module directories and return the full list.
- `rescan` (method, `modules/module_registry.py:304`) `def rescan(self)` - Force a full rescan and return modules.
- `get` (method, `modules/module_registry.py:313`) `def get(self, name)` - Get a module by name.
- `search` (method, `modules/module_registry.py:319`) `def search(self, query, module_type, category, enabled_only, include_deprecated)` - Search indexed modules.
- `deprecated_modules` (method, `modules/module_registry.py:359`) `def deprecated_modules(self)` - Return all deprecated modules.
- `by_type` (method, `modules/module_registry.py:365`) `def by_type(self, module_type)` - Shorthand for ``search(module_type=module_type)``.
- `summary` (method, `modules/module_registry.py:369`) `def summary(self)` - Return counts by module type.
- `proposal_intents` (method, `modules/module_registry.py:378`) `def proposal_intents(self, texts, target, limit)` - Loop bridge: map corpus mentions onto runnable module intents.
- `_scan_yaml_addons` (method, `modules/module_registry.py:462`) `def _scan_yaml_addons(self)`
- `_scan_plugins` (method, `modules/module_registry.py:503`) `def _scan_plugins(self)`
- `_scan_tools` (method, `modules/module_registry.py:543`) `def _scan_tools(self)`
- `_scan_playbooks` (method, `modules/module_registry.py:577`) `def _scan_playbooks(self)`
- `_scan_python_modules` (method, `modules/module_registry.py:597`) `def _scan_python_modules(self)` - Scan ``modules/`` for Python files with discoverable entry points.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 64
- Cross-boundary resolved imports (EXTRACTED): 65

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `modules/reverse-shell.c`)? What purpose do they serve?
- What would break if the most connected file in modules/selection changed?
- Should modules/selection be split, given cohesion 0.59?

## Sources

- `modules/chain_match.py`
- `modules/module_registry.py`
- `modules/reverse-shell.c`
- `modules/selection/__init__.py`
- `modules/selection/adversary.py`
- `modules/selection/atomic.py`
- `modules/selection/base.py`
- `modules/selection/chain.py`
- `modules/selection/cred_spray.py`
- `modules/selection/edb.py`
- `modules/selection/intel.py`
- `modules/selection/module.py`
- `modules/selection/playbook.py`
- `modules/selection/poc.py`
- `modules/selection/registry.py`
- `modules/selection/technique.py`
- `static/js/select2-4.1.0.min.js`
- `tests/test_intel_selector.py`
- `tests/test_loop_fire_pending.py`
- `tests/test_module_registry.py`
- *... and 6 more*
