# lazyc2/blueprints

*Community 8 | 26 files | cohesion 0.49*

## Definition

This community groups 26 file(s) rooted at `tests` with dominant language py (cohesion 0.49). Central symbols: `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`, `AddonYamlRenderer`, `CSRFPolicy`, `CliAuthCommandSet`. Core file: `modules/lazy_rbac.py` (86 symbols). Documented purpose: CLI authentication command set — login/logout/whoami.  Integrates with :mod:`modules.cli_auth` to authenticate CLI operators against the same ``users.json`` as .

## Files

### `tests` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_csrf_behavior.py` | py | testing | 6 | yes |
| `tests/test_csrf_policy.py` | py | testing | 24 | yes |

### `lazyc2/blueprints` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |
| `lazyc2/blueprints/auth.py` | py | presentation | 19 | yes |
| `lazyc2/blueprints/operations.py` | py | presentation | 13 | yes |

### `lazyc2` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |
| `lazyc2/addon_creator.py` | py | utility | 38 | yes |
| `lazyc2/models.py` | py | business_logic | 2 | yes |

### `lazyc2/extensions` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |
| `lazyc2/extensions/storage.py` | py | data_access | 12 | yes |
| `lazyc2/extensions/users.py` | py | infrastructure | 3 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/cli_auth.py` | py | utility | 18 | yes |
| `modules/lazy_rbac.py` | py | presentation | 86 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/cli_auth.py` | py | utility | 5 | yes |
| `cli/commands/redteam_gym.py` | py | utility | 8 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |
| `static/js/socket.io-4.3.2.min.js` | js | utility | 15 | yes |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/engagement_hooks.py` | py | utility | 32 | yes |

### `lazyc2/security` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/csrf.py` | py | utility | 11 | yes |

*... and 6 more files in this community.*


## Key Symbols

- `CliAuthCommandSet` (class, `cli/commands/cli_auth.py:27`) `class CliAuthCommandSet(LazyOwnCommandSet)` - CLI operator authentication — login, logout, whoami.
- `do_login` (method, `cli/commands/cli_auth.py:34`) `def do_login(self, line)` - Authenticate against users.json (same users as lazyc2.py).
- `do_register` (method, `cli/commands/cli_auth.py:117`) `def do_register(self, line)` - Register a new operator account in users.json.
- `do_logout` (method, `cli/commands/cli_auth.py:191`) `def do_logout(self, line)` - Log out the current CLI operator and clear the remember-me token.
- `do_whoami` (method, `cli/commands/cli_auth.py:224`) `def do_whoami(self, line)` - Show the currently logged-in CLI operator.
- `RedTeamGymCommandSet` (class, `cli/commands/redteam_gym.py:32`) `class RedTeamGymCommandSet(LazyOwnCommandSet)` - Red Team Gym — scored pentest challenges with leaderboards.
- `do_gym` (method, `cli/commands/redteam_gym.py:39`) `def do_gym(self, line)` - Red Team Gym — gamified pentest training with ELO scoring.
- `_gym_list` (method, `cli/commands/redteam_gym.py:83`) `def _gym_list(self)` - Display all available gym challenges.
- `_gym_start` (method, `cli/commands/redteam_gym.py:117`) `def _gym_start(self, args)` - Begin a gym challenge.
- `_gym_submit` (method, `cli/commands/redteam_gym.py:154`) `def _gym_submit(self, args)` - Submit a completed challenge for scoring.
- `_gym_status` (method, `cli/commands/redteam_gym.py:198`) `def _gym_status(self)` - Show the currently active challenge.
- `_gym_leaderboard` (method, `cli/commands/redteam_gym.py:223`) `def _gym_leaderboard(self, args)` - Show the gym leaderboard.
- `_gym_hint` (method, `cli/commands/redteam_gym.py:257`) `def _gym_hint(self)` - Get the next hint for the active challenge.
- `EngagementState` (class, `cli/engagement_hooks.py:242`) `class EngagementState` - Persisted cross-session engagement metrics.
- `_load_state` (method, `cli/engagement_hooks.py:260`) `def _load_state()`
- `_save_state` (method, `cli/engagement_hooks.py:280`) `def _save_state(state)`
- `_load_index` (method, `cli/engagement_hooks.py:290`) `def _load_index()`
- `_normalize_command` (method, `cli/engagement_hooks.py:301`) `def _normalize_command(cmd)` - Return ``cmd`` with a single leading ``do_`` prefix.
- `_is_recordable_command` (method, `cli/engagement_hooks.py:306`) `def _is_recordable_command(cmd)` - Return ``True`` when ``cmd`` is a syntactically valid command name.
- `_sanitize_seen` (method, `cli/engagement_hooks.py:332`) `def _sanitize_seen(names, known)` - Drop malformed entries left by the pre-gate telemetry bug.
- `heal_commands_seen` (method, `cli/engagement_hooks.py:365`) `def heal_commands_seen(known)` - Purge non-command entries from persisted ``commands_seen`` in place.
- `_next_threshold` (method, `cli/engagement_hooks.py:394`) `def _next_threshold(current)` - Draw the next reward trigger from a geometric distribution.
- `_phase_for_cmd` (method, `cli/engagement_hooks.py:400`) `def _phase_for_cmd(cmd, index)`
- `_commands_in_phase` (method, `cli/engagement_hooks.py:409`) `def _commands_in_phase(phase, index)`
- `_summary_for_cmd` (method, `cli/engagement_hooks.py:414`) `def _summary_for_cmd(cmd, index)`
- `_run_curiosity` (method, `cli/engagement_hooks.py:431`) `def _run_curiosity(cmd, state, index)` - Surface one undiscovered command from the same phase as ``cmd``.
- `_render_streak` (method, `cli/engagement_hooks.py:459`) `def _render_streak(ctx)` - Render the streak reward; always succeeds (always renders).
- `_render_exploration` (method, `cli/engagement_hooks.py:488`) `def _render_exploration(ctx)` - Render arsenal exploration progress bar.
- `_render_phase_badge` (method, `cli/engagement_hooks.py:506`) `def _render_phase_badge(ctx)` - Render the current kill-chain phase badge; skips when phase unknown.
- `_render_hidden_feature` (method, `cli/engagement_hooks.py:522`) `def _render_hidden_feature(ctx)` - Reveal one hidden CLI feature the operator hasn't seen recently.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 129
- Cross-boundary resolved imports (EXTRACTED): 47

## Connections

- [EXTRACTED] depends_on community 2 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 0 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports cli/engagement_hooks.py.
- [EXTRACTED] depends_on community 4 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/help_ui.py imports cli/engagement_hooks.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [cycle] `cli/engagement_hooks.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py`
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_security_hardening_v5.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `lazyc2/__init__.py`)? What purpose do they serve?
- Can the cycle `cli/engagement_hooks.py` -> `modules/cli_auth.py` be broken with an interface?
- What would break if the most connected file in lazyc2/blueprints changed?
- Should lazyc2/blueprints be split, given cohesion 0.49?

## Sources

- `cli/commands/cli_auth.py`
- `cli/commands/redteam_gym.py`
- `cli/engagement_hooks.py`
- `lazyc2/__init__.py`
- `lazyc2/addon_creator.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/auth.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/session_auth.py`
- `lazyc2/extensions/decoy.py`
- `lazyc2/extensions/storage.py`
- `lazyc2/extensions/users.py`
- `lazyc2/models.py`
- `lazyc2/security/csrf.py`
- `modules/cli_auth.py`
- `modules/lazy_rbac.py`
- `modules/redteam_gym.py`
- `static/js/socket.io-4.0.0.min.js`
- `static/js/socket.io-4.3.2.min.js`
- `tests/test_addon_creator.py`
- *... and 6 more*
