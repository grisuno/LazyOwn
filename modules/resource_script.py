"""Enhanced resource script engine — variables, conditionals, loops, macros.

Extends LazyOwn's existing ``.ls`` script format with:

- ``set <var> <value>`` — set a local variable
- ``setg <var> <value>`` — set a global variable (persists in shell params)
- ``unset <var>`` — remove a variable
- ``if <condition>`` / ``else`` / ``endif`` — conditional execution
- ``while <condition>`` / ``endwhile`` — loop until condition is false
- ``for <var> in <items>`` / ``endfor`` — iterate over space-separated items
- ``macro <name> <args>`` / ``endmacro`` / ``call <name> <args>`` — reusable blocks
- ``spool <file>`` / ``spool off`` — log output to file
- ``sleep <seconds>`` — pause execution
- ``echo <message>`` — print a message
- ``comment <text>`` — inline comment (also ``#`` lines)
- Variable substitution: ``$var`` or ``${var}`` anywhere in command lines

Built-in variables: ``$rhost``, ``$lhost``, ``$lport``, ``$domain``,
``$workspace``, ``$timestamp``.

Usage:
    resource path/to/script.ls
"""

from __future__ import annotations

import os
import re
import shlex
import subprocess
import time as _time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple


_VAR_RE = re.compile(r"\$\{([^}]+)\}|\$([a-zA-Z_][a-zA-Z0-9_.]*)")
_COMMENT_RE = re.compile(r"^\s*(#|//|comment\b)", re.IGNORECASE)
_MACRO_DEF_RE = re.compile(r"^\s*macro\s+(\w+)\s*(.*)", re.IGNORECASE)
_ENDMACRO_RE = re.compile(r"^\s*endmacro\s*$", re.IGNORECASE)
_IF_RE = re.compile(r"^\s*if\s+(.+)", re.IGNORECASE)
_ELSE_RE = re.compile(r"^\s*else\s*$", re.IGNORECASE)
_ENDIF_RE = re.compile(r"^\s*endif\s*$", re.IGNORECASE)
_WHILE_RE = re.compile(r"^\s*while\s+(.+)", re.IGNORECASE)
_ENDWHILE_RE = re.compile(r"^\s*endwhile\s*$", re.IGNORECASE)
_FOR_RE = re.compile(r"^\s*for\s+(\w+)\s+in\s+(.+)", re.IGNORECASE)
_ENDFOR_RE = re.compile(r"^\s*endfor\s*$", re.IGNORECASE)
_SET_RE = re.compile(r"^\s*set(?:g)?\s+(\w+)\s+(.+)", re.IGNORECASE)
_SETG_RE = re.compile(r"^\s*setg\s+(\w+)\s+(.+)", re.IGNORECASE)
_UNSET_RE = re.compile(r"^\s*unset\s+(\w+)", re.IGNORECASE)
_SPOOL_RE = re.compile(r"^\s*spool\s+(.+|off)", re.IGNORECASE)
_ECHO_RE = re.compile(r"^\s*echo\s+(.+)", re.IGNORECASE)
_SLEEP_RE = re.compile(r"^\s*sleep\s+(\d+)", re.IGNORECASE)
_CALL_RE = re.compile(r"^\s*call\s+(\w+)\s*(.*)", re.IGNORECASE)


class ScriptError(RuntimeError):
    """Raised when a resource script encounters a fatal error."""
    ...


class ScriptContext:
    """Runtime context for a single resource script execution.

    Tracks local/global variables, macro definitions, nesting state,
    and the spool file.
    """

    def __init__(
        self,
        shell_params: Dict[str, Any] | None = None,
        on_command: Callable[[str], None] | None = None,
        on_print: Callable[[str], None] | None = None,
    ) -> None:
        self.vars: Dict[str, str] = {}
        self.globals: Dict[str, str] = {}
        self.macros: Dict[str, Tuple[List[str], List[str]]] = {}
        self.spool_file: Optional[str] = None
        self.spool_handle = None
        self._command_cb = on_command
        self._print_cb = on_print
        self._if_stack: List[bool] = []
        self._while_stack: List[Tuple[str, int]] = []
        self._for_stack: List[Tuple[str, List[str], int]] = []
        self._skip_depth: int = 0
        self._line_number: int = 0
        self._lines: List[str] = []
        self._pos: int = 0

        if shell_params:
            for k, v in shell_params.items():
                if isinstance(v, str):
                    self.globals[k] = v
                else:
                    self.globals[k] = str(v)

        self._builtins: Dict[str, str] = {
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
        }

    def _resolve(self, text: str) -> str:
        def _repl(m: re.Match) -> str:
            key = m.group(1) or m.group(2)
            val = self.vars.get(key)
            if val is None:
                val = self._builtins.get(key)
            if val is None:
                val = self.globals.get(key)
            if val is None:
                val = os.environ.get(key, f"${{{key}}}")
            return val
        return _VAR_RE.sub(_repl, text)

    def print(self, msg: str = "") -> None:
        if self._print_cb:
            self._print_cb(msg)
        elif msg:
            print(msg)
        if self.spool_handle and not self.spool_handle.closed:
            self.spool_handle.write(msg + "\n")
            self.spool_handle.flush()

    def run_command(self, cmd: str) -> None:
        resolved = self._resolve(cmd)
        if self._command_cb:
            self._command_cb(resolved)
        elif resolved.strip():
            subprocess.run(resolved, shell=True)

    def _skip(self) -> bool:
        return self._skip_depth > 0 or (self._if_stack and not self._if_stack[-1])


class ResourceScriptEngine:
    """Parses and executes enhanced resource scripts.

    Args:
        context: A :class:`ScriptContext` providing variable scope and
            command execution callbacks.
    """

    def __init__(self, context: ScriptContext) -> None:
        self.ctx = context

    def execute(self, script_path: str) -> None:
        """Load and run a script file.

        Args:
            script_path: Path to the ``.ls`` or resource script file.

        Raises:
            ScriptError: On parse/execution errors.
            FileNotFoundError: When the script does not exist.
        """
        with open(script_path) as f:
            lines = f.readlines()
        self.execute_lines(lines, source=script_path)

    def execute_lines(
        self, lines: List[str], source: str = "<inline>"
    ) -> None:
        """Execute a list of script lines.

        Args:
            lines: Script lines (may include trailing newlines).
            source: Source name for error messages.

        Raises:
            ScriptError: On parse/execution errors.
        """
        self.ctx._lines = lines
        self.ctx._pos = 0

        # First pass: extract macro definitions
        self._extract_macros(lines)

        # Second pass: execute
        self.ctx._pos = 0
        while self.ctx._pos < len(lines):
            self.ctx._line_number = self.ctx._pos + 1
            raw = lines[self.ctx._pos]
            self.ctx._pos += 1
            try:
                self._execute_line(raw)
            except ScriptError:
                raise
            except Exception as e:
                raise ScriptError(
                    f"{source}:{self.ctx._line_number}: {e}"
                ) from e

        # Close spool if still open
        if self.ctx.spool_handle and not self.ctx.spool_handle.closed:
            self.ctx.spool_handle.close()
            self.ctx.spool_handle = None

    def execute_string(self, script: str) -> None:
        """Execute a script string (split on newlines)."""
        self.execute_lines(script.splitlines(), source="<string>")

    def _extract_macros(self, lines: List[str]) -> None:
        i = 0
        while i < len(lines):
            m = _MACRO_DEF_RE.match(lines[i])
            if m:
                name = m.group(1)
                args_raw = m.group(2).strip()
                args = shlex.split(args_raw) if args_raw else []
                body: List[str] = []
                i += 1
                while i < len(lines) and not _ENDMACRO_RE.match(lines[i]):
                    body.append(lines[i])
                    i += 1
                self.ctx.macros[name] = (args, body)
            i += 1

    def _execute_line(self, raw: str) -> None:
        text = raw.strip()
        if not text:
            return

        # Comment
        if _COMMENT_RE.match(text):
            return

        # setg <var> <value>
        m = _SETG_RE.match(text)
        if m:
            if not self.ctx._skip():
                self.ctx.globals[m.group(1)] = self.ctx._resolve(m.group(2).strip())
            return

        # set <var> <value>
        m = _SET_RE.match(text)
        if m:
            if not self.ctx._skip():
                self.ctx.vars[m.group(1)] = self.ctx._resolve(m.group(2).strip())
            return

        # unset <var>
        m = _UNSET_RE.match(text)
        if m:
            if not self.ctx._skip():
                self.ctx.vars.pop(m.group(1), None)
                self.ctx.globals.pop(m.group(1), None)
            return

        # if <condition>
        m = _IF_RE.match(text)
        if m:
            cond = self.ctx._resolve(m.group(1).strip()).lower()
            truthy = cond in ("true", "1", "yes", "on", "") or (
                not cond.startswith("false") and cond != "0" and cond != "no" and cond != "off"
            )
            self.ctx._if_stack.append(truthy)
            return

        # else
        if _ELSE_RE.match(text):
            if self.ctx._if_stack:
                self.ctx._if_stack[-1] = not self.ctx._if_stack[-1]
            return

        # endif
        if _ENDIF_RE.match(text):
            if self.ctx._if_stack:
                self.ctx._if_stack.pop()
            return

        # while <condition>
        m = _WHILE_RE.match(text)
        if m:
            if not self.ctx._skip():
                self.ctx._while_stack.append((m.group(1).strip(), self.ctx._pos))
            return

        # endwhile
        if _ENDWHILE_RE.match(text):
            if self.ctx._while_stack and not self.ctx._skip():
                cond_text, start_pos = self.ctx._while_stack[-1]
                resolved_cond = self.ctx._resolve(cond_text).lower()
                still_true = resolved_cond in ("true", "1", "yes", "on", "") and resolved_cond not in ("false", "0", "no", "off")
                if still_true:
                    self.ctx._pos = start_pos
                else:
                    self.ctx._while_stack.pop()
            elif self.ctx._while_stack:
                self.ctx._while_stack.pop()
            return

        # for <var> in <items>
        m = _FOR_RE.match(text)
        if m:
            if not self.ctx._skip():
                var = m.group(1)
                items_raw = self.ctx._resolve(m.group(2).strip())
                items = shlex.split(items_raw) if items_raw else []
                self.ctx._for_stack.append((var, items, self.ctx._pos))
                if items:
                    self.ctx.vars[var] = items[0]
            return

        # endfor
        if _ENDFOR_RE.match(text):
            if self.ctx._for_stack and not self.ctx._skip():
                var, items, start_pos = self.ctx._for_stack[-1]
                current_val = self.ctx.vars.get(var, "")
                try:
                    idx = items.index(current_val) + 1
                except ValueError:
                    idx = len(items)
                if idx < len(items):
                    self.ctx.vars[var] = items[idx]
                    self.ctx._pos = start_pos
                else:
                    self.ctx._for_stack.pop()
                    self.ctx.vars.pop(var, None)
            elif self.ctx._for_stack:
                self.ctx._for_stack.pop()
            return

        # macro / endmacro (handled in extract pass, skip here)
        if _MACRO_DEF_RE.match(text) or _ENDMACRO_RE.match(text):
            return

        # call <name> <args>
        m = _CALL_RE.match(text)
        if m:
            if not self.ctx._skip():
                name = m.group(1)
                args_raw = m.group(2).strip()
                call_args = shlex.split(self.ctx._resolve(args_raw)) if args_raw else []
                self._call_macro(name, call_args)
            return

        # spool <file> / spool off
        m = _SPOOL_RE.match(text)
        if m:
            if not self.ctx._skip():
                target = m.group(1).strip().lower()
                if target == "off":
                    if self.ctx.spool_handle and not self.ctx.spool_handle.closed:
                        self.ctx.spool_handle.close()
                    self.ctx.spool_handle = None
                    self.ctx.spool_file = None
                else:
                    resolved = self.ctx._resolve(m.group(1).strip())
                    os.makedirs(os.path.dirname(resolved) or ".", exist_ok=True)
                    self.ctx.spool_file = resolved
                    self.ctx.spool_handle = open(resolved, "a")
            return

        # echo <message>
        m = _ECHO_RE.match(text)
        if m:
            if not self.ctx._skip():
                msg = self.ctx._resolve(m.group(1).strip())
                self.ctx.print(msg)
            return

        # sleep <seconds>
        m = _SLEEP_RE.match(text)
        if m:
            if not self.ctx._skip():
                _time.sleep(int(m.group(1)))
            return

        # Regular command
        if not self.ctx._skip():
            self.ctx.run_command(text)

    def _call_macro(self, name: str, args: List[str]) -> None:
        entry = self.ctx.macros.get(name)
        if entry is None:
            raise ScriptError(f"undefined macro: {name}")
        param_names, body = entry
        saved_vars = dict(self.ctx.vars)
        for pname, pval in zip(param_names, args):
            self.ctx.vars[pname] = pval
        try:
            saved_pos = self.ctx._pos
            self.ctx._pos = 0
            inner_lines = body[:]
            i = 0
            while i < len(inner_lines):
                self.ctx._line_number = -1  # macro line
                self._execute_line(inner_lines[i])
                i += 1
            self.ctx._pos = saved_pos
        finally:
            self.ctx.vars.clear()
            self.ctx.vars.update(saved_vars)


__all__ = ["ResourceScriptEngine", "ScriptContext", "ScriptError"]
