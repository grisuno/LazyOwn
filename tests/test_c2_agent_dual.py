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


if __name__ == "__main__":
    unittest.main()
