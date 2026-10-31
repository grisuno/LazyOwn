# Subsystem: commands (page 5 of 5)
Previous: [KB_commands_p4.md](KB_commands_p4.md)

## cli/commands/verb_admin.py
- Doc: Operator administration of the autonomous-loop verb catalog.
- Layer: utility
- Language: py
- Symbols:
  - `VerbAdminConfig` (class, line 23) `class VerbAdminConfig`
  - `_row_text` (function, line 35) `def _row_text(entry)`
  - `VerbCommandSet` (class, line 45) `class VerbCommandSet(LazyOwnCommandSet)`
  - `do_verb` (method, line 52) `def do_verb(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/verb_catalog.py`, `utils.py`

## cli/commands/winbox_gym.py
- Doc: WinBox lab CommandSet — VM lifecycle, guest execution and gym matrix.
- Layer: utility
- Language: py
- Symbols:
  - `WinboxCommandSet` (class, line 44) `class WinboxCommandSet(LazyOwnCommandSet)`
  - `_extract_flag` (function, line 514) `def _extract_flag(args, flag)`
  - `_extract_bool` (function, line 537) `def _extract_bool(args, flag)`
  - `do_winbox` (method, line 51) `def do_winbox(self, line)`
  - `_overview` (method, line 121) `def _overview(self)`
  - `_bootstrap` (method, line 127) `def _bootstrap(self)`
  - `_status` (method, line 151) `def _status(self)`
  - `_lifecycle` (method, line 178) `def _lifecycle(self, action, rest)`
  - `_lab_ready` (method, line 200) `def _lab_ready(self, rest)`
  - `_exec` (method, line 234) `def _exec(self, rest)`
  - `_interactive_passthrough` (method, line 268) `def _interactive_passthrough(self, action, rest)`
  - `_tools` (method, line 281) `def _tools(self, rest)`
  - `_upload` (method, line 292) `def _upload(self, rest)`
  - `_eventlogs` (method, line 302) `def _eventlogs(self, rest)`
  - `_net` (method, line 309) `def _net(self, rest)`
  - `_defense` (method, line 325) `def _defense(self, tool, rest)`
  - `_snapshot` (method, line 341) `def _snapshot(self, rest)`
  - `_resolve` (method, line 363) `def _resolve(self, rest)`
  - `_gym` (method, line 382) `def _gym(self, rest)`
  - `_gym_matrix` (method, line 418) `def _gym_matrix(self, action, rest)`
  - `_confirmed` (method, line 501) `def _confirmed(self, rest)`
  - `_lab_notify` (function, line 215) `def _lab_notify(message)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`

