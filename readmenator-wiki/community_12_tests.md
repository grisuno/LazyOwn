# tests

*Community 12 | 2 files | cohesion 0.50*

## Definition

This community groups 2 file(s) rooted at `tests` with dominant language py (cohesion 0.50). Central symbols: `TestRunShell`, `TestSafeRun`, `_validate_input`, `_validate_timeout`, `run_shell`, `safe_run`, `test_bad_type_raises_type_error`, `test_echo_hello_returns_completed_process_with_stdout`. Core file: `tests/test_core_executor.py` (15 symbols). Documented purpose: Centralised subprocess wrapper for the LazyOwn framework.  Provides safe, logged command execution as a replacement for bare :func:`os.system` and unguarded :fu.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/executor.py` | py | utility | 6 | yes |
| `tests/test_core_executor.py` | py | testing | 15 | yes |

## Key Symbols

- `_validate_input` (function, `core/executor.py:41`) `def _validate_input(command)` - Validate command input and return argv and loggable string.
- `_validate_timeout` (function, `core/executor.py:75`) `def _validate_timeout(timeout)` - Clamp and validate timeout seconds.
- `safe_run` (function, `core/executor.py:96`) `def safe_run(command)`
- `safe_run` (function, `core/executor.py:98`) `def safe_run(command)`
- `safe_run` (function, `core/executor.py:101`) `def safe_run(command)` - Execute a command with logging and timeout.
- `run_shell` (function, `core/executor.py:149`) `def run_shell(cmd)` - Execute a shell command and return its stdout.
- `TestSafeRun` (class, `tests/test_core_executor.py:15`) `class TestSafeRun` - Tests for :func:`core.executor.safe_run`.
- `test_echo_hello_returns_completed_process_with_stdout` (method, `tests/test_core_executor.py:18`) `def test_echo_hello_returns_completed_process_with_stdout(self)` - safe_run with a list returns a CompletedProcess and captures stdout.
- `test_false_command_returns_nonzero` (method, `tests/test_core_executor.py:27`) `def test_false_command_returns_nonzero(self)` - safe_run with the false command returns a non-zero exit code.
- `test_empty_list_raises_value_error` (method, `tests/test_core_executor.py:34`) `def test_empty_list_raises_value_error(self)` - safe_run raises ValueError when given an empty list.
- `test_empty_string_raises_value_error` (method, `tests/test_core_executor.py:41`) `def test_empty_string_raises_value_error(self)` - safe_run raises ValueError when given a whitespace-only string.
- `test_timeout_raises_timeout_expired` (method, `tests/test_core_executor.py:48`) `def test_timeout_raises_timeout_expired(self)` - safe_run raises TimeoutExpired when the command exceeds the timeout.
- `test_null_bytes_in_list_arg_raises_value_error` (method, `tests/test_core_executor.py:55`) `def test_null_bytes_in_list_arg_raises_value_error(self)` - safe_run rejects null bytes inside list arguments.
- `test_null_bytes_in_string_raises_value_error` (method, `tests/test_core_executor.py:62`) `def test_null_bytes_in_string_raises_value_error(self)` - safe_run rejects null bytes inside a command string.
- `test_bad_type_raises_type_error` (method, `tests/test_core_executor.py:69`) `def test_bad_type_raises_type_error(self)` - safe_run raises TypeError when command is neither str nor list.
- `test_timeout_below_minimum_raises_value_error` (method, `tests/test_core_executor.py:76`) `def test_timeout_below_minimum_raises_value_error(self)` - safe_run raises ValueError when timeout is below the valid range.
- `TestRunShell` (class, `tests/test_core_executor.py:84`) `class TestRunShell` - Tests for :func:`core.executor.run_shell`.
- `test_echo_hello_returns_stdout_string` (method, `tests/test_core_executor.py:87`) `def test_echo_hello_returns_stdout_string(self)` - run_shell returns stripped stdout of a successful command.
- `test_nonzero_exit_raises_called_process_error` (method, `tests/test_core_executor.py:95`) `def test_nonzero_exit_raises_called_process_error(self)` - run_shell raises CalledProcessError when the command exits non-zero.
- `test_pipes_and_redirects_work` (method, `tests/test_core_executor.py:102`) `def test_pipes_and_redirects_work(self)` - run_shell supports shell-builtins like pipes.
- `test_stdout_is_stripped_of_whitespace` (method, `tests/test_core_executor.py:109`) `def test_stdout_is_stripped_of_whitespace(self)` - run_shell strips leading and trailing whitespace from stdout.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 13
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in tests changed?
- Should tests be split, given cohesion 0.50?

## Sources

- `core/executor.py`
- `tests/test_core_executor.py`
