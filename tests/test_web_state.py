"""Web-app state machine: token-aware sessions for DVWA/Mutillidae/phpMyAdmin."""

from __future__ import annotations

import sys
import urllib.parse
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import requests  # noqa: E402

from modules.autonomous_exploit_engine import ExploitCandidate  # noqa: E402
from modules.exploit_engine.outcomes import AUTH_BYPASS, SQLI, classify_outcome  # noqa: E402
from modules.web_state import run_web_vector  # noqa: E402

DVWA_LOGIN_PAGE = '<form action="login.php"><input name="user_token" value="tok1"></form>'
DVWA_HOME = "<html>Welcome to Damn Vulnerable Web Application [Logout]</html>"
DVWA_SECURITY = "<html>Security level: low [Logout]</html>"
DVWA_SQLI = "<html>First name: admin<br>Surname: admin</html>"
DVWA_LOGIN_FAIL = DVWA_LOGIN_PAGE
PMA_INDEX = '<html>phpMyAdmin <form><input name="token" value="tok2"></form></html>'
PMA_WELCOME = "<html>Welcome to phpMyAdmin<br>Database server</html>"
MUT_HOME = "<html>Mutillidae</html>"
MUT_SQLI = "<html>You have an error in your SQL syntax</html>"
MUT_CMD = "<html>uid=33(www-data) gid=33(www-data)</html>"
MUT_LFI = "<html>root:x:0:0:root:/root:/bin/bash</html>"


class FakeResponse:
    def __init__(self, text: str):
        self.text = text


class FakeSession:
    def __init__(self, server):
        self.headers = {}
        self.trust_env = True
        self.server = server
        self.cookies = {}

    def get(self, url, timeout=None, verify=False):
        return FakeResponse(self.server("get", url, {}))

    def post(self, url, data=None, timeout=None, verify=False):
        return FakeResponse(self.server("post", url, dict(data or {})))


def _fake_server(method: str, url: str, data: dict):
    path = urllib.parse.urlsplit(url).path
    if method == "get" and path == "/dvwa/login.php":
        return DVWA_LOGIN_PAGE
    if method == "post" and path == "/dvwa/login.php":
        if data.get("user_token") == "tok1" and data.get("password") in {"charley", "password", "abc123"}:
            return DVWA_HOME
        return DVWA_LOGIN_FAIL
    if method == "get" and path == "/dvwa/security.php":
        return DVWA_SECURITY
    if method == "post" and path == "/dvwa/security.php":
        return DVWA_SECURITY
    if method == "get" and path == "/dvwa/vulnerabilities/sqli/":
        return DVWA_SQLI
    if method == "get" and path == "/phpmyadmin/index.php":
        return PMA_INDEX
    if method == "post" and path == "/phpmyadmin/index.php":
        return PMA_WELCOME
    if method == "get" and path == "/mutillidae/index.php" and "page=/etc/passwd" in url:
        return MUT_LFI
    if method == "get" and "user-info.php" in url:
        return MUT_SQLI
    if method == "post" and "dns-lookup.php" in url:
        return MUT_CMD
    if method == "get" and path == "/mutillidae/index.php":
        return MUT_HOME
    return ""


@pytest.fixture()
def fake_web(monkeypatch):
    monkeypatch.setattr(requests, "Session", lambda: FakeSession(_fake_server))


def _profile():
    profile = type("P", (), {})()
    profile.ip = "10.0.0.2"
    profile.services = ()
    return profile


def _cand(strategy, port="80"):
    return ExploitCandidate(service="http", product="", version="", strategy=strategy, confidence=0.9, port=port)


def test_dvwa_sqli_flows_through_login_and_succeeds(fake_web):
    output = run_web_vector(_cand("ms2_dvwa_sqli"), _profile())
    assert "First name: admin" in output
    result = classify_outcome(output, _cand("ms2_dvwa_sqli"))
    assert result.kind == SQLI
    assert result.success is True


def test_dvwa_login_failure_returns_empty(fake_web, monkeypatch):
    def no_login(method, url, data):
        if "login" in url:
            return DVWA_LOGIN_FAIL
        return _fake_server(method, url, data)

    monkeypatch.setattr(requests, "Session", lambda: FakeSession(no_login))
    assert run_web_vector(_cand("ms2_dvwa_sqli"), _profile()) == ""


def test_phpmyadmin_default_cred_welcomes(fake_web):
    output = run_web_vector(_cand("ms2_phpmyadmin_default"), _profile())
    assert "Welcome to phpMyAdmin" in output
    assert classify_outcome(output, _cand("ms2_phpmyadmin_default")).kind == AUTH_BYPASS


def test_mutillidae_sqli_page(fake_web):
    output = run_web_vector(_cand("ms2_mutillidae_sqli"), _profile())
    assert "You have an error" in output


def test_non_web_strategy_skips(fake_web):
    assert run_web_vector(_cand("ms2_ingreslock"), _profile()) == ""


def test_brute_force_strategy_skips(fake_web):
    assert run_web_vector(_cand("ms2_dvwa_brute_force"), _profile()) == ""


def test_upload_strategy_skips(fake_web):
    assert run_web_vector(_cand("ms2_dvwa_file_upload"), _profile()) == ""


def test_rfi_strategy_skips(fake_web):
    assert run_web_vector(_cand("ms2_mutillidae_rfi"), _profile()) == ""
