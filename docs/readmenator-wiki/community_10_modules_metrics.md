# modules: metrics

*Community 10 | 8 files | cohesion 0.36*

## Definition

This community groups 8 file(s) rooted at `modules` with dominant language py (cohesion 0.36). Central symbols: `C2Builder`, `C2Profile`, `Completed`, `LabCommandSet`, `MetricRecord`, `MetricsAggregator`, `MetricsRecorder`, `MetricsRegistry`. Core file: `tests/test_infra_disposable.py` (35 symbols). Documented purpose: Lab environment commands -- spin up vulnerable practice targets.  Provides on-demand CTF-style lab scenarios powered by Docker containers. Operators can practic.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/lab.py` | py | utility | 21 | yes |
| `modules/c2_builder.py` | py | infrastructure | 21 | yes |
| `modules/metrics.py` | py | utility | 24 | yes |
| `modules/professional_report.py` | py | utility | 22 | yes |
| `modules/session_cleanup.py` | py | utility | 5 | yes |
| `tests/test_bdd_infra_range_report.py` | py | testing | 5 | yes |
| `tests/test_infra_disposable.py` | py | testing | 35 | yes |
| `tests/test_metrics.py` | py | testing | 14 | yes |

## Key Symbols

- `LabCommandSet` (class, `cli/commands/lab.py:81`) `class LabCommandSet(LazyOwnCommandSet)` - Manage local CTF lab environments via Docker.
- `_docker_available` (method, `cli/commands/lab.py:87`) `def _docker_available(self)` - Check if Docker is installed and the daemon is reachable.
- `_running_containers` (method, `cli/commands/lab.py:100`) `def _running_containers(self)` - Return list of running lab container names.
- `_container_name` (method, `cli/commands/lab.py:114`) `def _container_name(self, scenario)` - Return the container name for a given scenario.
- `do_lab` (method, `cli/commands/lab.py:119`) `def do_lab(self, line)` - Manage local CTF practice labs.
- `_lab_list` (method, `cli/commands/lab.py:171`) `def _lab_list(self)` - Display available lab scenarios.
- `_lab_start` (method, `cli/commands/lab.py:185`) `def _lab_start(self, scenario)` - Spin up a lab scenario container.
- `_lab_stop` (method, `cli/commands/lab.py:234`) `def _lab_stop(self, scenario)` - Stop a running lab scenario.
- `_range_dispatch` (method, `cli/commands/lab.py:252`) `def _range_dispatch(self, args)` - Dispatch ``lab range`` subcommands.
- `_range_list` (method, `cli/commands/lab.py:284`) `def _range_list(self)` - Display available cyber range profiles.
- `_range_compose` (method, `cli/commands/lab.py:293`) `def _range_compose(self, profile)` - Resolve the compose file for a range profile.
- `_range_start` (method, `cli/commands/lab.py:312`) `def _range_start(self, profile)` - Start a cyber range profile via Docker Compose.
- `_range_container_state` (method, `cli/commands/lab.py:347`) `def _range_container_state(self, container)` - Read a container's lifecycle state.
- `_range_wait_healthy` (method, `cli/commands/lab.py:370`) `def _range_wait_healthy(self, compose, timeout)` - Wait for range containers to run and probe host-side ports.
- `_range_verify` (method, `cli/commands/lab.py:402`) `def _range_verify(self, profile)` - Prove the range is exploitable by firing a real exploit.
- `_tcp_reachable` (method, `cli/commands/lab.py:438`) `def _tcp_reachable(host, port, timeout)` - Probe one TCP port from this host.
- `_ensure_range_secret` (method, `cli/commands/lab.py:455`) `def _ensure_range_secret(self, profile_dir)` - Generate the DC admin secret file when missing.
- `_range_container_ip` (method, `cli/commands/lab.py:485`) `def _range_container_ip(self, container)` - Resolve a range container's IP on its compose network.
- `_range_stop` (method, `cli/commands/lab.py:508`) `def _range_stop(self, profile)` - Stop a cyber range profile.
- `_range_status` (method, `cli/commands/lab.py:524`) `def _range_status(self)` - Show range container status.
- `_lab_status` (method, `cli/commands/lab.py:536`) `def _lab_status(self)` - Show currently running lab containers.
- `_resolve_go_bin` (function, `modules/c2_builder.py:44`) `def _resolve_go_bin()` - Return the full path to the go binary.
- `_ensure_go` (function, `modules/c2_builder.py:59`) `def _ensure_go(cmd_fn)` - Guarantee a go binary is available, installing via apt if needed.
- `C2Profile` (class, `modules/c2_builder.py:76`) `class C2Profile` - Compilation profile for a target platform.
- `_preflight` (method, `modules/c2_builder.py:160`) `def _preflight(profile)` - Check that all required external binaries are present.
- `_render_template` (method, `modules/c2_builder.py:169`) `def _render_template(content, context)` - Render a template by replacing {key} placeholders with context values.
- `_replacer` (method, `modules/c2_builder.py:173`) `def _replacer(match)`
- `_resolve_fallback_urls` (method, `modules/c2_builder.py:180`) `def _resolve_fallback_urls(params)` - Collect disposable redirector URLs for the Go beacon fallback list.
- `_go_string_list` (method, `modules/c2_builder.py:220`) `def _go_string_list(urls)` - Format URLs as a Go string slice body.
- `_parse_go_version` (method, `modules/c2_builder.py:234`) `def _parse_go_version(text)` - Parse a ``go version`` output line into a version triple.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 24
- Cross-boundary resolved imports (EXTRACTED): 23

## Connections

- [EXTRACTED] depends_on community 1 <-> 10 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/c2_builder.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: metrics changed?
- Should modules: metrics be split, given cohesion 0.36?

## Sources

- `cli/commands/lab.py`
- `modules/c2_builder.py`
- `modules/metrics.py`
- `modules/professional_report.py`
- `modules/session_cleanup.py`
- `tests/test_bdd_infra_range_report.py`
- `tests/test_infra_disposable.py`
- `tests/test_metrics.py`
