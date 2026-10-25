from __future__ import annotations

import unittest
from pathlib import Path

from modules.c2_builder import _lkm_makefile_text

REPO_ROOT = Path(__file__).parent.parent
IMPLANT_DIR = REPO_ROOT / "sessions" / "implant"

IMPLANT_TEMPLATE_CONSTANTS = (
    "SLEEP_JIT_ENABLED = \"{sleep_jit_enabled}\"",
    "SLEEP_JIT_PCT_MIN = \"{sleep_jit_pct_min}\"",
    "SLEEP_JIT_PCT_MAX = \"{sleep_jit_pct_max}\"",
    "ACT_DELAY_MIN = \"{sleep_activation_delay_min}\"",
    "ACT_DELAY_MAX = \"{sleep_activation_delay_max}\"",
    "PERSIST_CRON = \"{persistence_cron_schedule}\"",
    "PERSIST_SERVICE = \"{persistence_service_name}\"",
)


class ImplantSessionSecretsSpec(unittest.TestCase):
    """Contract: lab Go implant templates bind rotating session secrets."""

    def test_implant_binds_sleep_and_persistence_placeholders(self) -> None:
        source = (IMPLANT_DIR / "implant_crypt.go").read_text(encoding="utf-8")
        for constant in IMPLANT_TEMPLATE_CONSTANTS:
            self.assertIn(constant, source)

    def test_implant_uses_obfuscated_sleep_and_jitter_bounds(self) -> None:
        source = (IMPLANT_DIR / "implant_crypt.go").read_text(encoding="utf-8")
        self.assertIn("func obfuscatedSleep(", source)
        self.assertIn("func jitteredSleep(", source)
        self.assertIn("func randomActivationDelay(", source)
        self.assertIn("obfuscatedSleep(jitteredSleep(baseSleepTime))", source)
        self.assertNotIn("calculateJitteredSleep", source)

    def test_implant_uses_utls_for_real_tls_fingerprint(self) -> None:
        source = (IMPLANT_DIR / "implant_crypt.go").read_text(encoding="utf-8")
        self.assertIn('utls "github.com/refraction-networking/utls"', source)
        self.assertIn("func initTLSProfile(", source)
        self.assertIn("func dialTLS(", source)
        self.assertIn("DialTLSContext: dialTLS", source)

    def test_listener_and_monrevlin_bind_session_magic(self) -> None:
        listener = (IMPLANT_DIR / "listener.go").read_text(encoding="utf-8")
        monrevlin = (IMPLANT_DIR / "monrevlin.go").read_text(encoding="utf-8")
        self.assertIn('especialCadena = "{session_magic}"', listener)
        self.assertIn('PASSWORD        = "{session_magic}"', monrevlin)
        self.assertNotIn("grisiscomebacksayknokknok", listener)
        self.assertNotIn("grisiscomebacksayknokknok", monrevlin)

    def test_rootkit_listener_default_is_neutral(self) -> None:
        rootkit = (REPO_ROOT / "modules" / "rootkit" / "rootkit.c").read_text(encoding="utf-8")
        self.assertIn('#define LISTENER_IP "127.0.0.1"', rootkit)

    def test_lkm_makefile_carries_deployment_values(self) -> None:
        text = _lkm_makefile_text("10.10.10.5", "4444")
        self.assertIn("LISTENER_IP ?= 10.10.10.5", text)
        self.assertIn("LISTENER_PORT ?= 4444", text)
        self.assertIn("obj-m += rootkit.o", text)
        self.assertIn("ccflags-y +=", text)

    def test_url_traffic_template_keys_match_builder_context(self) -> None:
        source = (IMPLANT_DIR / "implant_crypt.go").read_text(encoding="utf-8")
        self.assertIn('"{url_traffic_1}"', source)
        self.assertNotIn("{url_trafic_1}", source)


if __name__ == "__main__":
    unittest.main()
