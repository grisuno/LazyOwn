"""Tests for modules/resource_script.py — ScriptContext and ResourceScriptEngine."""

from __future__ import annotations

import pytest

from modules.resource_script import ResourceScriptEngine, ScriptContext, ScriptError


class TestResourceScript:
    """Test suite for ScriptContext and ResourceScriptEngine."""

    @staticmethod
    def _execute(script: str, **params) -> list[str]:
        """Execute an inline script string, returning captured output."""
        output: list[str] = []
        ctx = ScriptContext(
            shell_params=params,
            on_print=output.append,
            on_command=lambda cmd: output.append(f"[cmd] {cmd}"),
        )
        ResourceScriptEngine(ctx).execute_string(script)
        return output

    def test_set_and_get(self):
        """Set a variable, verify _resolve returns it."""
        ctx = ScriptContext()
        ctx.vars["var"] = "hello"
        assert ctx._resolve("$var") == "hello"

    def test_setg_and_get(self):
        """Set a global, verify it persists via _resolve."""
        ctx = ScriptContext()
        ctx.globals["var"] = "global_val"
        assert ctx._resolve("$var") == "global_val"

    def test_unset_removes_var(self):
        """Set then unset a var, verify it is gone."""
        ctx = ScriptContext()
        ctx.vars["x"] = "hello"
        ctx.vars.pop("x", None)
        resolved = ctx._resolve("$x")
        assert resolved != "hello"
        assert "${x}" in resolved

    def test_var_substitution(self):
        """Both ${var} and $var resolve identically."""
        ctx = ScriptContext()
        ctx.vars["x"] = "42"
        assert ctx._resolve("${x}") == "42"
        assert ctx._resolve("$x") == "42"

    def test_builtin_timestamp(self):
        """$timestamp is not empty."""
        ctx = ScriptContext()
        val = ctx._resolve("$timestamp")
        assert val
        assert "${timestamp}" not in val

    def test_resolve_unresolved(self):
        """$nonexistent stays as ${nonexistent}."""
        ctx = ScriptContext()
        result = ctx._resolve("$nonexistent")
        assert result == "${nonexistent}"

    def test_eval_condition_equals(self):
        """'hello == hello' is True, 'x == y' is False."""
        ctx = ScriptContext()
        assert ctx.eval_condition("hello == hello")
        assert not ctx.eval_condition("x == y")

    def test_eval_condition_not_equals(self):
        """'x != y' is True."""
        ctx = ScriptContext()
        assert ctx.eval_condition("x != y")

    def test_eval_condition_regex(self):
        """'hello =~ ell' is True, 'hello !~ xyz' is True."""
        ctx = ScriptContext()
        assert ctx.eval_condition("hello =~ ell")
        assert ctx.eval_condition("hello !~ xyz")

    def test_eval_condition_numeric(self):
        """Numeric comparisons evaluate correctly."""
        ctx = ScriptContext()
        assert ctx.eval_condition("3 > 2")
        assert not ctx.eval_condition("1 >= 2")
        assert ctx.eval_condition("2 < 3")
        assert ctx.eval_condition("2 <= 2")

    def test_eval_condition_contains(self):
        """'hello contains ll' is True, 'abc contains x' is False."""
        ctx = ScriptContext()
        assert ctx.eval_condition("hello contains ll")
        assert not ctx.eval_condition("abc contains x")

    def test_eval_condition_defined(self):
        """'defined $x' is False then True after setting x."""
        ctx = ScriptContext()
        assert not ctx.eval_condition("defined $x")
        ctx.vars["x"] = "something"
        assert ctx.eval_condition("defined $x")

    def test_eval_condition_fallback_falsy(self):
        """Falsy values: false, 0, no, off, empty string are all False."""
        ctx = ScriptContext()
        for v in ("false", "0", "no", "off", ""):
            assert not ctx.eval_condition(v), f"'{v}' should be falsy"

    def test_eval_condition_fallback_truthy(self):
        """Truthy values: hello, 1, yes are all True."""
        ctx = ScriptContext()
        for v in ("hello", "1", "yes"):
            assert ctx.eval_condition(v), f"'{v}' should be truthy"

    def test_dry_run_mode(self):
        """dry_run=True captures [dry-run] prefix in print callback."""
        output: list[str] = []
        ctx = ScriptContext(on_print=output.append)
        ctx.dry_run = True
        ctx.run_command("echo hello")
        assert len(output) == 1
        assert "[dry-run]" in output[0]

    def test_skip_depth(self):
        """_skip() follows _if_stack and _skip_depth."""
        ctx = ScriptContext()
        assert not ctx._skip()

        ctx._if_stack.append(True)
        assert not ctx._skip()

        ctx._if_stack[-1] = False
        assert ctx._skip()

        ctx._if_stack.pop()
        ctx._skip_depth = 1
        assert ctx._skip()

        ctx._skip_depth = 0
        assert not ctx._skip()

    def test_if_else_endif_true(self):
        """if true / echo yes / else / echo no / endif prints 'yes'."""
        output = self._execute("""\
if true
echo yes
else
echo no
endif""")
        assert output == ["yes"]

    def test_if_else_endif_false(self):
        """if false variant prints 'no'."""
        output = self._execute("""\
if false
echo yes
else
echo no
endif""")
        assert output == ["no"]

    def test_set_and_echo(self):
        """set x hello / echo $x prints 'hello'."""
        output = self._execute("""\
set x hello
echo $x""")
        assert output == ["hello"]

    def test_for_loop(self):
        """for item in a b c / echo $item / endfor prints a, b, c."""
        output = self._execute("""\
for item in a b c
echo $item
endfor""")
        assert output == ["a", "b", "c"]

    def test_for_loop_empty(self):
        """for with nothing after 'in' is not parsed as a for loop, runs as raw command."""
        output = self._execute("""\
for item in
echo never
endfor""")
        assert any("for item in" in o for o in output)
        assert "never" in output

    def test_while_loop(self):
        """Basic while loop runs once then exits."""
        output = self._execute("""\
set i 0
while $i contains 0
echo $i
set i 1
endwhile""")
        assert output == ["0"]

    def test_break(self):
        """break exits the for loop early."""
        output = self._execute("""\
for item in a b c
if $item == b
break
endif
echo $item
endfor""")
        assert output == ["a"]

    def test_continue(self):
        """continue skips the current for iteration."""
        output = self._execute("""\
for item in a b c
if $item == b
continue
endif
echo $item
endfor""")
        assert output == ["a", "c"]

    def test_comment(self):
        """Lines starting with # are ignored."""
        output = self._execute("""\
# this is a comment
set x hello
# another comment
echo $x""")
        assert output == ["hello"]

    def test_macro_and_call(self):
        """Macro body runs once during main pass (unresolved), then call resolves args."""
        output = self._execute("""\
macro greet name
echo hello $name
endmacro
call greet world""")
        assert "hello ${name}" in output
        assert "hello world" in output

    def test_spool(self, tmp_path):
        """spool writes echoed output to file."""
        spool_path = tmp_path / "spool.txt"
        script = f"""\
spool {spool_path}
echo hello
echo world
spool off"""
        output = self._execute(script)
        content = spool_path.read_text()
        assert "hello" in content
        assert "world" in content
        assert "hello" in output
        assert "world" in output

    def test_undefined_macro_raises(self):
        """call nonexistent raises ScriptError."""
        with pytest.raises(ScriptError):
            self._execute("call nonexistent")

    def test_unset_variable(self):
        """Set then unset, echo resolves to ${x} placeholder."""
        output = self._execute("""\
set x hello
echo $x
unset x
echo $x""")
        assert output == ["hello", "${x}"]

    def test_nested_if(self):
        """Nested if/endif blocks work correctly."""
        output = self._execute("""\
set x outer
if true
echo outer
set y inner
if true
echo inner
else
echo never_inner
endif
echo after_inner
else
echo never_outer
endif
echo done""")
        assert output == ["outer", "inner", "after_inner", "done"]
