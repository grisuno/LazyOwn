# modules: lazy_rbac

*Community 8 | 23 files | cohesion 0.41*

## Definition

This community groups 23 file(s) rooted at `modules` with dominant language py (cohesion 0.41). Central symbols: `C2Builder`, `C2Profile`, `CliAuthCommandSet`, `Completed`, `EngagementState`, `Et`, `GymAttempt`, `LabCommandSet`. Core file: `modules/lazy_rbac.py` (86 symbols). Documented purpose: CLI authentication command set — login/logout/whoami.  Integrates with :mod:`modules.cli_auth` to authenticate CLI operators against the same ``users.json`` as .

## Files

### `modules` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/c2_builder.py` | py | infrastructure | 21 | yes |
| `modules/cli_auth.py` | py | utility | 18 | yes |
| `modules/lazy_rbac.py` | py | presentation | 86 | yes |
| `modules/metrics.py` | py | utility | 24 | yes |
| `modules/professional_report.py` | py | utility | 22 | yes |

### `tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_bdd_infra_range_report.py` | py | testing | 5 | yes |
| `tests/test_engagement_and_ping.py` | py | testing | 40 | yes |
| `tests/test_engagement_command_gate.py` | py | testing | 18 | yes |
| `tests/test_engagement_elo_and_methodology.py` | py | testing | 43 | yes |
| `tests/test_infra_disposable.py` | py | testing | 35 | yes |

### `cli/commands` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/cli_auth.py` | py | utility | 5 | yes |
| `cli/commands/lab.py` | py | utility | 21 | yes |
| `cli/commands/redteam_gym.py` | py | utility | 8 | yes |

### `lazyc2` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |
| `lazyc2/models.py` | py | business_logic | 2 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |
| `static/js/socket.io-4.3.2.min.js` | js | utility | 15 | yes |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/engagement_hooks.py` | py | utility | 32 | yes |

### `lazyc2/blueprints` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/auth.py` | py | presentation | 19 | yes |

### `lazyc2/extensions` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/users.py` | py | infrastructure | 3 | yes |

*... and 3 more files in this community.*


## Key Symbols

- `CliAuthCommandSet` (class, `cli/commands/cli_auth.py:27`) `class CliAuthCommandSet(LazyOwnCommandSet)` - CLI operator authentication — login, logout, whoami.
- `do_login` (method, `cli/commands/cli_auth.py:34`) `def do_login(self, line)` - Authenticate against users.json (same users as lazyc2.py).
- `do_register` (method, `cli/commands/cli_auth.py:117`) `def do_register(self, line)` - Register a new operator account in users.json.
- `do_logout` (method, `cli/commands/cli_auth.py:191`) `def do_logout(self, line)` - Log out the current CLI operator and clear the remember-me token.
- `do_whoami` (method, `cli/commands/cli_auth.py:224`) `def do_whoami(self, line)` - Show the currently logged-in CLI operator.
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
- `RedTeamGymCommandSet` (class, `cli/commands/redteam_gym.py:32`) `class RedTeamGymCommandSet(LazyOwnCommandSet)` - Red Team Gym — scored pentest challenges with leaderboards.
- `do_gym` (method, `cli/commands/redteam_gym.py:39`) `def do_gym(self, line)` - Red Team Gym — gamified pentest training with ELO scoring.
- `_gym_list` (method, `cli/commands/redteam_gym.py:83`) `def _gym_list(self)` - Display all available gym challenges.
- `_gym_start` (method, `cli/commands/redteam_gym.py:117`) `def _gym_start(self, args)` - Begin a gym challenge.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 142
- Cross-boundary resolved imports (EXTRACTED): 61

## Connections

- [EXTRACTED] depends_on community 3 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports cli/engagement_hooks.py.
- [EXTRACTED] depends_on community 4 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports cli/engagement_hooks.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [cycle] `cli/engagement_hooks.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py`

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `lazyc2/__init__.py`)? What purpose do they serve?
- Can the cycle `cli/engagement_hooks.py` -> `modules/cli_auth.py` be broken with an interface?
- What would break if the most connected file in modules: lazy_rbac changed?
- Should modules: lazy_rbac be split, given cohesion 0.41?

## Sources

- `cli/commands/cli_auth.py`
- `cli/commands/lab.py`
- `cli/commands/redteam_gym.py`
- `cli/engagement_hooks.py`
- `lazyc2/__init__.py`
- `lazyc2/blueprints/auth.py`
- `lazyc2/extensions/users.py`
- `lazyc2/models.py`
- `modules/c2_builder.py`
- `modules/cli_auth.py`
- `modules/lazy_rbac.py`
- `modules/metrics.py`
- `modules/professional_report.py`
- `modules/redteam_gym.py`
- `modules/session_cleanup.py`
- `static/js/socket.io-4.0.0.min.js`
- `static/js/socket.io-4.3.2.min.js`
- `tests/test_bdd_infra_range_report.py`
- `tests/test_engagement_and_ping.py`
- `tests/test_engagement_command_gate.py`
- *... and 3 more*
