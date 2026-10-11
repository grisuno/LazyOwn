"""Single-implementation rule for extracted helpers.

SDD contract: ``utils.*`` holds the live implementations used by the
CLI/C2. The divergent copies that a past extraction left behind in
``core/parsers`` and ``core/credentials`` had zero callers and trapped
future imports into the wrong behavior, so they were removed. Only
``strip_ansi`` (imported by ``utils`` and the C2 bots) stays in
``core/parsers``. This test fails the build if the dead fork grows
back.
"""

from __future__ import annotations

import core
import core.parsers

REMOVED = [
    "aggressive_yaml_fix",
    "clean_html",
    "clean_output",
    "clean_url",
    "create_synthetic_yaml",
    "crack_password",
    "de_htmlify",
    "extract_banners",
    "find_ea",
    "find_ps",
    "find_ss",
    "fix_common_yaml_issues",
    "format_openssh_key",
    "format_rsa_key",
    "generate_emails",
    "get_credentials",
    "get_domain",
    "get_domain_from_xml",
    "get_hash",
    "get_users_dic",
    "get_xml",
    "htmlify",
    "is_exist",
    "list_binaries",
    "load_adversary",
    "load_knowledge_base",
    "load_user_aliases",
    "manual_yaml_extraction",
    "parse_nmap_csv",
    "parse_yaml_response",
    "return_creds",
    "select_binary",
    "Spray",
]


class TestDeadForkRemoved:
    def test_no_divergent_copies_in_core_parsers(self) -> None:
        for name in REMOVED:
            assert not hasattr(core.parsers, name), name

    def test_no_divergent_copies_in_core_namespace(self) -> None:
        for name in REMOVED:
            assert not hasattr(core, name), name

    def test_shared_kernel_still_available(self) -> None:
        from core.parsers import strip_ansi

        assert strip_ansi("\x1b[31mred\x1b[0m") == "red"

    def test_live_utils_implementations_intact(self) -> None:
        import utils

        for name in (
            "clean_output",
            "is_exist",
            "get_domain",
            "parse_yaml_response",
            "get_credentials",
            "return_creds",
        ):
            assert callable(getattr(utils, name)), name
