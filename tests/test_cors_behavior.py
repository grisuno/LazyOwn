"""BDD behavior scenarios for the CORS policy contract.

These scenarios describe the user-visible behavior of the CORS policy in
plain language, then exercise it. They are intentionally distinct from the
unit tests in :mod:`tests.test_cors_policy` so the contract has both a
fine-grained check and a coarse-grained one.
"""

from __future__ import annotations

import pytest

from lazyc2.security.cors import CorsConfigError, CorsPolicy


def test_given_wildcard_in_prod_when_resolving_then_raises() -> None:
    """Given a PROD env with a wildcard, when origins are resolved, then raise."""
    policy = CorsPolicy(env="PROD", lhost="10.0.0.1", allowed_origins="*")
    with pytest.raises(CorsConfigError):
        policy.resolve_origins()


def test_given_empty_in_dev_when_resolving_then_falls_back_to_lhost() -> None:
    """Given DEV env with empty allowlist, when resolved, then http+https://lhost are used."""
    policy = CorsPolicy(env="DEV", lhost="192.168.1.5", allowed_origins="")
    origins = policy.resolve_origins()
    assert "https://192.168.1.5" in origins
    assert "http://192.168.1.5" in origins


def test_given_unknown_origin_when_handshake_then_denied() -> None:
    """Given an origin not in the allowlist, when checked, then it is denied."""
    policy = CorsPolicy(
        env="PROD",
        lhost="10.0.0.1",
        allowed_origins="https://c2.example",
    )
    assert policy.is_allowed("https://attacker.example") is False


def test_given_matching_origin_when_handshake_then_allowed() -> None:
    """Given an origin in the allowlist, when checked, then it is allowed."""
    policy = CorsPolicy(
        env="PROD",
        lhost="10.0.0.1",
        allowed_origins="https://c2.example",
    )
    assert policy.is_allowed("https://c2.example") is True
