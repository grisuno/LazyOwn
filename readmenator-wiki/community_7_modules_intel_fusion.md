# modules: intel_fusion

*Community 7 | 66 files | cohesion 0.45*

## Definition

This community groups 66 file(s) rooted at `tests` with dominant language py (cohesion 0.45). Central symbols: `CustomPayload`, `DynamicShellcodePayload`, `ExploitSighting`, `FeedEntry`, `FindingRecord`, `IngestBeaconReconSpec`, `MatchStore`, `MinimalPayload`. Core file: `modules/intel_fusion.py` (35 symbols). Documented purpose: Attack-surface operations: confirmed discovery scans, estorides fusion.  ``scandiscovery`` lists every IP found in the sessions discovery files and only launche.

## Files

### `tests` (24 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_asset_gate.py` | py | testing | 16 | yes |
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_beacon_recon_sink.py` | py | testing | 18 | yes |
| `tests/test_c2_surfaces.py` | py | testing | 12 | yes |

### `modules` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/attack_surface3d.py` | py | utility | 11 | yes |
| `modules/beacon_recon.py` | py | utility | 6 | yes |
| `modules/c2_surfaces.py` | py | utility | 11 | yes |
| `modules/estorides_fusion.py` | py | utility | 11 | yes |

### `modules/sinks` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/__init__.py` | py | utility | 0 | yes |
| `modules/sinks/attack_graph.py` | py | utility | 1 | yes |
| `modules/sinks/beacon_dispatch.py` | py | utility | 3 | yes |
| `modules/sinks/c2_surfaces.py` | py | utility | 1 | yes |

### `skills/mcp_tools` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/lazy_intel.py` | py | utility | 1 | yes |
| `skills/mcp_tools/lazy_status.py` | py | utility | 1 | yes |
| `skills/mcp_tools/lazy_sync.py` | py | utility | 1 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/surface_graph.py` | py | utility | 33 | yes |
| `cli/surface_tui.py` | py | utility | 19 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/surface.py` | py | utility | 3 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/core_smoke.py` | py | utility | 4 | yes |

*... and 46 more files in this community.*


## Key Symbols

- `SurfaceCommandSet` (class, `cli/commands/surface.py:36`) `class SurfaceCommandSet(LazyOwnCommandSet)` - Discovery scans and OSINT fusion for the attack surface.
- `do_scandiscovery` (method, `cli/commands/surface.py:43`) `def do_scandiscovery(self, line)` - Scan every discovery IP with operator confirmation.
- `do_estorides_intel` (method, `cli/commands/surface.py:86`) `def do_estorides_intel(self, line)` - Fuse estorides OSINT entities into the campaign intel graphs.
- `_slug_host` (function, `cli/surface_graph.py:75`) `def _slug_host(ip)` - Return the canonical ``host-<dotted-ip>`` id used by the web graph.
- `_slug_port` (function, `cli/surface_graph.py:80`) `def _slug_port(host_id, port, protocol)` - Return a stable port-node id rooted at ``host_id``.
- `SurfaceNode` (class, `cli/surface_graph.py:87`) `class SurfaceNode` - A node in the network surface graph.
- `to_dict` (method, `cli/surface_graph.py:102`) `def to_dict(self)` - Return a JSON-serialisable view of the node.
- `SurfaceEdge` (class, `cli/surface_graph.py:113`) `class SurfaceEdge` - A directed edge between two surface nodes.
- `to_dict` (method, `cli/surface_graph.py:120`) `def to_dict(self)` - Return a JSON-serialisable view of the edge.
- `SurfaceGraph` (class, `cli/surface_graph.py:126`) `class SurfaceGraph` - Aggregate snapshot of nodes + edges discovered on disk.
- `to_dict` (method, `cli/surface_graph.py:135`) `def to_dict(self)` - Return a JSON-serialisable view (mirrors the web UI payload).
- `stats` (method, `cli/surface_graph.py:146`) `def stats(self)` - Return per-kind node counts plus edge count.
- `children_of` (method, `cli/surface_graph.py:153`) `def children_of(self, node_id)` - Return nodes that ``node_id`` points to via an outgoing edge.
- `get` (method, `cli/surface_graph.py:165`) `def get(self, node_id)` - Return the node with ``node_id`` or ``None``.
- `SurfaceGraphConfig` (class, `cli/surface_graph.py:174`) `class SurfaceGraphConfig` - Configuration for :class:`SurfaceGraphBuilder`.
- `SurfaceGraphBuilder` (class, `cli/surface_graph.py:196`) `class SurfaceGraphBuilder` - Compose a :class:`SurfaceGraph` from on-disk session artefacts.
- `__init__` (method, `cli/surface_graph.py:199`) `def __init__(self, config)`
- `build` (method, `cli/surface_graph.py:202`) `def build(self)` - Read every session artefact and return the assembled graph.
- `_kind_order` (method, `cli/surface_graph.py:331`) `def _kind_order(kind)`
- `_build_c2_node` (method, `cli/surface_graph.py:341`) `def _build_c2_node(self, local_ips, payload)`
- `_discover_local_ips` (method, `cli/surface_graph.py:359`) `def _discover_local_ips(self)`
- `_fallback_local_ips` (method, `cli/surface_graph.py:380`) `def _fallback_local_ips()`
- `_load_payload` (method, `cli/surface_graph.py:386`) `def _load_payload(self)`
- `_read_os_hint` (method, `cli/surface_graph.py:399`) `def _read_os_hint(self)`
- `_read_hostsdiscovery` (method, `cli/surface_graph.py:414`) `def _read_hostsdiscovery(self, local_ips)` - Collect discovery IPs from every hosts discovery file.
- `_read_scan_discovery` (method, `cli/surface_graph.py:436`) `def _read_scan_discovery(self, local_ips)` - Collect port records from every scan CSV plus nmap normal output.
- `_read_scan_csv` (method, `cli/surface_graph.py:442`) `def _read_scan_csv(self, local_ips)`
- `_read_scan_nmap` (method, `cli/surface_graph.py:467`) `def _read_scan_nmap(self, local_ips)` - Parse nmap normal output (``-oN``) for hosts and open ports.
- `_read_implants` (method, `cli/surface_graph.py:525`) `def _read_implants(self)`
- `_read_last_implant_row` (method, `cli/surface_graph.py:542`) `def _read_last_implant_row(self, path)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 125
- Cross-boundary resolved imports (EXTRACTED): 164

## Connections

- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/c2_session.py imports modules/c2_surfaces.py.

## Risks

- [cycle] `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_ledger.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_intel.py`
- [layer strict] `tests/test_c2_surfaces.py` (testing) -> `contrib/legacy/lazydeepseekcli.py` (presentation)

## Open Questions

- Can the cycle `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_ledger.py` be broken with an interface?
- What would break if the most connected file in modules: intel_fusion changed?
- Should modules: intel_fusion be split, given cohesion 0.45?

## Sources

- `cli/commands/surface.py`
- `cli/surface_graph.py`
- `cli/surface_tui.py`
- `contrib/legacy/lazydeepseekcli.py`
- `modules/attack_surface3d.py`
- `modules/beacon_recon.py`
- `modules/c2_surfaces.py`
- `modules/estorides_fusion.py`
- `modules/finding_lifecycle.py`
- `modules/intel_fusion.py`
- `modules/lazy_bridge.py`
- `modules/lazy_checks.py`
- `modules/lazy_cve_feed.py`
- `modules/lazy_exposure.py`
- `modules/lazy_feedmatch.py`
- `modules/lazy_heat.py`
- `modules/lazy_hostscore.py`
- `modules/lazy_inventory.py`
- `modules/lazy_ledger.py`
- `modules/lazy_match_policy.py`
- *... and 46 more*
