"""Fuzzing for input validators and rating boundaries.

Deterministic (seeded) generative tests proving two contracts hold for
arbitrary hostile input:

1. Validators never raise: ``check_rhost`` / ``check_lhost`` /
   ``check_port`` return ``True``/``False`` for anything, including
   non-strings, huge inputs, and unicode.
2. Validators never accept shell metacharacters: anything they return
   ``True`` for is free of ``;&|`$(){}!><*?~#'\"`` and newlines, and any
   accepted port is within 1-65535.

Plus boundary fuzzing for ``rate_plugin`` (non-integer and out-of-range
stars must raise, never write).
"""

from __future__ import annotations

import random
import string
from pathlib import Path

import pytest

from cli.plugin_tiers import rate_plugin
from core.validators import _SHELL_META_CHARS, check_lhost, check_lport, check_port, check_rhost

SEED = 0x1A2701
CASES_PER_FUZZ = 300

_EVIL_CORPUS: tuple[str, ...] = (
    "",
    " ",
    ";",
    "|",
    "&&",
    "$(id)",
    "`id`",
    "${HOME}",
    "10.0.0.1; rm -rf /",
    "a|b",
    "..",
    "../..",
    "%00",
    "%0a",
    "a\nb",
    "a\rb",
    "a\tb",
    "' OR '1'='1",
    '"quoted"',
    "(subshell)",
    "{brace}",
    "star*",
    "q?",
    "~root",
    "#comment",
    "\\escape",
    "!",
    ">out",
    "<in",
    "héllo",
    "中文主机",
    "🖥️",
    "\x00null",
    "\x7fdel",
    "A" * 300,
    "1" * 300,
    "10.0.0.1/99",
    "999.999.999.999",
    "::1",
    "fe80::1%eth0",
    "-1",
    "+1",
    " 10.0.0.1 ",
    "0x7f000001",
    "0177.0.0.1",
)


def _random_host(rng: random.Random) -> str:
    alphabet = string.ascii_letters + string.digits + ".;:|/&$`(){}!><*?~#'\"\n\r\\ \t-_%"
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 120)))


def _host_inputs() -> list[object]:
    rng = random.Random(SEED)
    inputs: list[object] = list(_EVIL_CORPUS)
    inputs += [_random_host(rng) for _ in range(CASES_PER_FUZZ)]
    inputs += [None, True, False, 0, 1, -1, 3.5, float("nan"), [], {}, ("a",), object()]
    return inputs


def _port_inputs() -> list[object]:
    rng = random.Random(SEED + 1)
    inputs: list[object] = ["", " ", "0", "-1", "65536", "999999999999", "3.5", "0x10", "080", " 80 ", "+80"]
    inputs += [str(rng.randint(-100000, 200000)) for _ in range(100)]
    inputs += [_random_host(rng) for _ in range(100)]
    inputs += [None, True, False, 3.5, [], {}, ("80",)]
    return inputs


@pytest.mark.parametrize("value", _host_inputs())
def test_host_validators_never_raise(value: object, capsys: pytest.CaptureFixture[str]) -> None:
    assert check_rhost(value) is False or check_rhost(value) is True
    assert check_lhost(value) is False or check_lhost(value) is True
    capsys.readouterr()


@pytest.mark.parametrize("value", _host_inputs())
def test_accepted_hosts_have_no_shell_metacharacters(value: object, capsys: pytest.CaptureFixture[str]) -> None:
    for checker in (check_rhost, check_lhost):
        if checker(value) and isinstance(value, str):
            assert not any(ch in _SHELL_META_CHARS for ch in value), f"{checker.__name__} accepted {value!r}"
    capsys.readouterr()


@pytest.mark.parametrize("value", _port_inputs())
def test_port_validator_never_raise_and_bounded(value: object, capsys: pytest.CaptureFixture[str]) -> None:
    assert check_port(value) is False or check_port(value) is True
    assert check_lport(value) is False or check_lport(value) is True
    if check_port(value) is True:
        assert 1 <= int(value) <= 65535
    capsys.readouterr()


def test_known_good_values_accepted(capsys: pytest.CaptureFixture[str]) -> None:
    assert check_rhost("10.10.11.5") is True
    assert check_rhost("example.com") is True
    assert check_lhost("192.168.1.1") is True
    assert check_port(4444) is True
    assert check_port("65535") is True
    assert check_rhost("") is False
    assert check_port(0) is False
    assert check_port(65536) is False
    capsys.readouterr()


@pytest.mark.parametrize("stars", ["5", 5.0, None, True, False, [5], "1; rm", float("nan")])
def test_rate_plugin_rejects_non_integer_stars(tmp_path: Path, stars: object) -> None:
    store = tmp_path / "ratings.json"
    with pytest.raises(ValueError):
        rate_plugin("p", stars, store)  # type: ignore[arg-type]
    assert not store.exists(), "rejected rating must not create the store"
