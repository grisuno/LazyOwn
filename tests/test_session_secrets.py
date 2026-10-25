from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from core.config import Config, load_payload
from core.session_secrets import ensure_session_secrets, rotate_session_secrets


class SessionSecretsSpec(unittest.TestCase):
    """Contract for session-scoped secret rotation."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.prev_cwd = os.getcwd()
        os.chdir(self._tmp.name)
        self.addCleanup(os.chdir, self.prev_cwd)
        Path("payload.json").write_text("{}", encoding="utf-8")
        Path("sessions").mkdir(exist_ok=True)

    def test_rotate_generates_and_persists_all_secrets(self) -> None:
        result = rotate_session_secrets()
        payload = load_payload()
        self.assertEqual(len(result["rat_key"]), 64)
        self.assertEqual(len(result["session_magic"]), 32)
        self.assertEqual(len(result["aes_hex"]), 64)
        self.assertEqual(payload["rat_key"], result["rat_key"])
        self.assertEqual(payload["session_magic"], result["session_magic"])
        key_file = Path("sessions/key.aes")
        self.assertTrue(key_file.exists())
        self.assertEqual(key_file.stat().st_size, 32)
        self.assertEqual(key_file.read_bytes().hex(), result["aes_hex"])
        self.assertEqual(key_file.stat().st_mode & 0o777, 0o600)

    def test_rotate_replaces_previous_values(self) -> None:
        first = rotate_session_secrets()
        second = rotate_session_secrets()
        self.assertNotEqual(first["rat_key"], second["rat_key"])
        self.assertNotEqual(first["session_magic"], second["session_magic"])
        self.assertNotEqual(first["aes_hex"], second["aes_hex"])

    def test_ensure_replaces_legacy_placeholders(self) -> None:
        payload = load_payload()
        payload["rat_key"] = "CHANGE_ME"
        payload["session_magic"] = None
        from core.config import save_payload

        save_payload(payload)
        result = ensure_session_secrets()
        self.assertNotEqual(result["rat_key"], "CHANGE_ME")
        self.assertTrue(all(c in "0123456789abcdef" for c in result["session_magic"]))

    def test_ensure_keeps_valid_values(self) -> None:
        first = rotate_session_secrets()
        second = ensure_session_secrets()
        self.assertEqual(first["rat_key"], second["rat_key"])
        self.assertEqual(first["session_magic"], second["session_magic"])
        self.assertEqual(first["aes_hex"], second["aes_hex"])

    def test_ensure_force_rotation(self) -> None:
        first = ensure_session_secrets()
        second = ensure_session_secrets(rotate=True)
        self.assertNotEqual(first["rat_key"], second["rat_key"])

    def test_mirror_updates_config_object(self) -> None:
        config_obj = Config(load_payload())
        result = rotate_session_secrets(config_obj)
        self.assertEqual(config_obj.rat_key, result["rat_key"])
        self.assertEqual(config_obj.session_magic, result["session_magic"])
        self.assertEqual(config_obj.aes_key, result["aes_hex"])


if __name__ == "__main__":
    unittest.main()
