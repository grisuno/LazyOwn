"""Regression test for the CLI approval-backend wiring.

``do_apt_chain`` routes confirm steps to the C2 pending list when
``LAZYOWN_APPROVAL_BACKEND=c2``; the import used to reach for a symbol
that ``cli.apt_chain_support`` never shipped, so the backend silently
fell back to the interactive approver and pending records were dead.
"""

from __future__ import annotations

from modules.chain_approval import build_c2_approver


class TestCliApprovalBackendWiring:
    def test_c2_approver_importable_from_support(self):
        story = "the C2 approver must be importable from cli.apt_chain_support exactly as do_apt_chain imports it"
        from cli.apt_chain_support import approval_backend as cli_backend
        from cli.apt_chain_support import build_c2_approver as cli_builder

        assert cli_builder is build_c2_approver, story
        assert callable(cli_backend), story
