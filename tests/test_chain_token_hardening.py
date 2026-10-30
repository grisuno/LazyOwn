"""Shell-metacharacter containment contract for chain tokens.

Every scenario states Given, When, Then. Static chain values are
validated at parse time, runtime token values are shell-quoted at the
execution boundary, and an explicit ``raw_vars`` allowlist honours
operator intent.
"""

from __future__ import annotations

import shlex

from modules.chain_registry import Chain, ChainStep, validate_chain
from modules.chain_runner import ChainRunner


def _chain(steps: list[ChainStep], **kwargs) -> Chain:
    """Build a demo chain for a runner scenario."""
    return Chain(name="demo", defaults={"target": "127.0.0.1"}, steps=steps, **kwargs)


def test_static_defaults_with_metachars_fail_validation():
    """Given a default holding shell metachars, When validating, Then the file is rejected."""
    errors = validate_chain(
        {
            "name": "demo",
            "steps": [{"run": "probe {payload}"}],
            "defaults": {"payload": "safe; rm -rf /"},
        },
        filename="demo",
    )
    assert any("defaults.payload" in row and "metacharacters" in row for row in errors)


def test_raw_vars_declares_operator_intent():
    """Given a metachar default listed in raw_vars, When validating, Then the file passes."""
    errors = validate_chain(
        {
            "name": "demo",
            "steps": [{"run": "show {payload}"}],
            "defaults": {"payload": "a&b"},
            "raw_vars": ["payload"],
        },
        filename="demo",
    )
    assert errors == []


def test_runner_shellquotes_token_values_with_metachars():
    """Given a command-line var holding metachars, When a raw step renders, Then the value is quoted."""

    def executor(command: str) -> str:
        return "ok"

    chain = _chain([ChainStep(id="probe", run="probe {token}")])
    runner = ChainRunner(chain, tokens={"target": "10.0.0.9", "token": "a; touch /tmp/pwned"}, executor=executor)
    rendered = runner._render_command("probe {token} {target}", dict(runner.tokens), set())
    assert rendered == f"probe {shlex.quote('a; touch /tmp/pwned')} 10.0.0.9"


def test_runner_raw_vars_option_outs_quoting():
    """Given a var listed in raw_vars, When a raw step renders, Then the value stays verbatim."""

    def executor(command: str) -> str:
        return "ok"

    chain = _chain([ChainStep(id="show", run="show {token}")], raw_vars=("token",))
    runner = ChainRunner(chain, tokens={"token": "a&b"}, executor=executor)
    rendered = runner._render_command("show {token}", dict(runner.tokens), set())
    assert rendered == "show a&b"


def test_runner_verb_templates_keep_verbatim_values():
    """Given a verb command with metachar vars, When rendering, Then the verb stays raw."""
    from modules.chain_runner import ChainRunner as CR

    class Shell:
        aliases: dict = {}

        def do_lazynmap(self, line: str) -> None:
            return None

    chain = _chain([ChainStep(id="scan", run="lazynmap {token}")])
    runner = CR(chain, tokens={"target": "10.0.0.9", "token": "a&b"}, shell=Shell())
    rendered = runner._render_command("lazynmap {token}", dict(runner.tokens), set())
    assert rendered == "lazynmap a&b"


def test_captured_values_remain_quoted_in_raw_steps():
    """Given a capture, When the next raw step renders, Then captured output stays quoted."""

    def executor(command: str) -> str:
        if command.startswith("probe"):
            return "v; evil"
        return "ok"

    chain = _chain(
        [
            ChainStep(id="probe", run="probe {target}", capture="got"),
            ChainStep(id="use", run="use {got}"),
        ]
    )
    runner = ChainRunner(chain, tokens={"target": "10.0.0.9"}, executor=executor, retry_backoff=0)
    result = runner.run()
    assert result.ok is True
    use_step = next(step for step in result.steps if step.id == "use")
    assert "v evil" not in use_step.run


def test_yaml_chain_with_ampersand_defaults_validates_with_raw_vars():
    """Given the entra-id chain YAML with an ampersand default, When validating, Then it passes."""
    import yaml

    data = yaml.safe_load(
        (chain_file("apt_entra_id_connect___federation_attacks")).read_text(encoding="utf-8")
    )
    assert validate_chain(data, filename=data["name"], chains_dir="chains") == []


def chain_file(stem: str):
    """Return the path of one repository chain file."""
    from pathlib import Path

    return Path("chains") / f"{stem}.yaml"
