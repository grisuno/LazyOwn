"""Unit tests for :mod:`modules.security_sanitizers`.

Each test asserts a security invariant that the corresponding
sanitizer guarantees. The suite is designed so a regression that
re-introduces any of the CodeQL findings (#731, #745, #753, #754,
#755, #756, #757) breaks an explicit, named test instead of a
production endpoint.
"""

from __future__ import annotations

import os

import pytest

from modules.security_sanitizers import (
    BindAddressResolver,
    CommandRedactor,
    HeaderValueSanitizer,
    OutputSanitizer,
    SecurityConfig,
    SessionPathResolver,
    build_default_config,
)


@pytest.fixture()
def cfg() -> SecurityConfig:
    """Return the default :class:`SecurityConfig` used by the suite."""
    return SecurityConfig()


class TestSecurityConfig:
    """Verify configuration creation and override behaviour."""

    def test_defaults_are_conservative(self, cfg: SecurityConfig) -> None:
        """The shipped defaults must fail closed."""
        assert cfg.allow_unspecified_bind is False
        assert cfg.bind_loopback_address == "127.0.0.1"
        assert cfg.bind_unspecified_address == "0.0.0.0"
        assert cfg.max_serialization_depth >= 1
        assert cfg.max_serialization_collection >= 1

    def test_from_payload_accepts_known_keys(self) -> None:
        """Known string and int keys override the defaults."""
        payload = {
            "redacted_password_token": "<HIDDEN>",
            "max_serialization_depth": 4,
            "allow_unspecified_bind": True,
        }
        cfg = SecurityConfig.from_payload(payload)
        assert cfg.redacted_password_token == "<HIDDEN>"
        assert cfg.max_serialization_depth == 4
        assert cfg.allow_unspecified_bind is True

    def test_from_payload_drops_wrong_types(self) -> None:
        """Type-mismatched values must not overwrite the defaults."""
        payload = {
            "max_serialization_depth": "not-an-int",
            "allow_unspecified_bind": "yes",
        }
        cfg = SecurityConfig.from_payload(payload)
        default = SecurityConfig()
        assert cfg.max_serialization_depth == default.max_serialization_depth
        assert cfg.allow_unspecified_bind == default.allow_unspecified_bind

    def test_build_default_config_handles_none(self) -> None:
        """``build_default_config`` accepts ``None`` and arbitrary types."""
        assert isinstance(build_default_config(None), SecurityConfig)
        assert isinstance(build_default_config({"x": 1}), SecurityConfig)
        assert isinstance(build_default_config("not-a-mapping"), SecurityConfig)


class TestHeaderValueSanitizer:
    """HTTP response-splitting guarantees (#745, #757)."""

    def test_strips_cr_lf_nul(self, cfg: SecurityConfig) -> None:
        """CR, LF and NUL must never appear in the output."""
        sanitizer = HeaderValueSanitizer(cfg)
        for forbidden in ("\r", "\n", "\x00"):
            value = f"safe{forbidden}injected: 1"
            out = sanitizer.sanitize_value(value)
            assert forbidden not in out

    def test_rejects_control_characters(self, cfg: SecurityConfig) -> None:
        """Non-printable bytes outside the allowlist are filtered."""
        sanitizer = HeaderValueSanitizer(cfg)
        assert sanitizer.sanitize_value("bad\x01value") == cfg.filtered_header_sentinel

    def test_length_capped(self, cfg: SecurityConfig) -> None:
        """Output never exceeds ``max_header_value_length``."""
        sanitizer = HeaderValueSanitizer(cfg)
        out = sanitizer.sanitize_value("A" * (cfg.max_header_value_length * 2))
        assert len(out) == cfg.max_header_value_length

    def test_valid_name_accepts_rfc7230_tokens(self, cfg: SecurityConfig) -> None:
        """RFC 7230 ``token`` names must pass the allowlist."""
        sanitizer = HeaderValueSanitizer(cfg)
        for name in ("Content-Type", "X-Custom", "Set-Cookie"):
            assert sanitizer.is_valid_name(name)

    def test_invalid_name_rejected(self, cfg: SecurityConfig) -> None:
        """Names with whitespace or control bytes are rejected."""
        sanitizer = HeaderValueSanitizer(cfg)
        assert not sanitizer.is_valid_name("X Bad")
        assert not sanitizer.is_valid_name("X-Bad\r\n")
        assert not sanitizer.is_valid_name("")
        assert not sanitizer.is_valid_name(None)

    def test_constructor_rejects_non_config(self) -> None:
        """``HeaderValueSanitizer`` requires a :class:`SecurityConfig`."""
        with pytest.raises(TypeError):
            HeaderValueSanitizer({})  # type: ignore[arg-type]


class TestSessionPathResolver:
    """Path-injection guarantees (#753)."""

    def test_rejects_parent_traversal(self, cfg: SecurityConfig, tmp_path) -> None:
        """``..`` segments must never resolve."""
        resolver = SessionPathResolver(str(tmp_path), cfg)
        assert resolver.resolve("../etc/passwd") is None
        assert resolver.resolve("a/../../etc/passwd") is None

    def test_rejects_absolute(self, cfg: SecurityConfig, tmp_path) -> None:
        """Absolute paths and leading separators are rejected."""
        resolver = SessionPathResolver(str(tmp_path), cfg)
        assert resolver.resolve("/etc/passwd") is None
        assert resolver.resolve("\\\\windows\\\\secret") is None

    def test_rejects_null_byte(self, cfg: SecurityConfig, tmp_path) -> None:
        """NUL bytes in filenames are refused."""
        resolver = SessionPathResolver(str(tmp_path), cfg)
        assert resolver.resolve("ok.txt\x00ignored") is None

    def test_rejects_too_many_segments(self, cfg: SecurityConfig, tmp_path) -> None:
        """Excessive segment counts are refused."""
        resolver = SessionPathResolver(str(tmp_path), cfg)
        too_many = "/".join(["a"] * (cfg.max_path_segments + 1))
        assert resolver.resolve(too_many) is None

    def test_resolves_valid_path(self, cfg: SecurityConfig, tmp_path) -> None:
        """A clean relative path resolves under the base directory."""
        sub = tmp_path / "a"
        sub.mkdir()
        (sub / "index.html").write_text("ok")
        resolver = SessionPathResolver(str(tmp_path), cfg)
        result = resolver.resolve("a/index.html")
        assert result is not None
        absolute, relative = result
        assert relative == "a/index.html"
        assert absolute.startswith(resolver.base_dir + os.sep)
        assert resolver.file_exists("a/index.html")

    def test_file_exists_false_on_invalid(self, cfg: SecurityConfig, tmp_path) -> None:
        """Validation failures surface as ``False`` rather than exceptions."""
        resolver = SessionPathResolver(str(tmp_path), cfg)
        assert resolver.file_exists("../etc/passwd") is False
        assert resolver.file_exists(None) is False

    def test_constructor_rejects_bad_base(self, cfg: SecurityConfig) -> None:
        """Empty and non-string base directories are refused."""
        with pytest.raises(ValueError):
            SessionPathResolver("", cfg)
        with pytest.raises(ValueError):
            SessionPathResolver(None, cfg)  # type: ignore[arg-type]


class TestBindAddressResolver:
    """Socket-binding guarantees (#754, #755)."""

    def test_falls_back_to_loopback(self, cfg: SecurityConfig) -> None:
        """No preferred address must yield the loopback."""
        resolver = BindAddressResolver(cfg)
        assert resolver.resolve() == cfg.bind_loopback_address

    def test_accepts_first_valid_preferred(self, cfg: SecurityConfig) -> None:
        """The first parseable IP literal wins."""
        resolver = BindAddressResolver(cfg, [None, "", "not-an-ip", "10.0.0.7"])
        assert resolver.resolve() == "10.0.0.7"

    def test_accepts_ipv6_literal(self, cfg: SecurityConfig) -> None:
        """IPv6 literals are accepted."""
        resolver = BindAddressResolver(cfg, ["::1"])
        assert resolver.resolve() == "::1"

    def test_unspecified_requires_opt_in(self, cfg: SecurityConfig) -> None:
        """The unspecified address is only returned when allowed."""
        denied = BindAddressResolver(cfg)
        assert denied.resolve() == cfg.bind_loopback_address
        permissive_cfg = SecurityConfig.from_payload({"allow_unspecified_bind": True})
        allowed = BindAddressResolver(permissive_cfg)
        assert allowed.resolve() == permissive_cfg.bind_unspecified_address

    def test_constructor_rejects_non_config(self) -> None:
        """``BindAddressResolver`` requires a :class:`SecurityConfig`."""
        with pytest.raises(TypeError):
            BindAddressResolver({}, ["10.0.0.1"])  # type: ignore[arg-type]


class TestCommandRedactor:
    """Credential-leak guarantees (#756)."""

    def test_display_omits_real_credentials(self, cfg: SecurityConfig) -> None:
        """Real credentials must never appear in the display string."""
        redactor = CommandRedactor(cfg)
        executable, display = redactor.render(
            "hydra -L {ip} -p {password} -u {username}",
            {"ip": "10.0.0.1"},
            "alice",
            " -p 's3cret!' ",
        )
        assert "alice" not in display
        assert "s3cret" not in display
        assert "alice" in executable
        assert "s3cret" in executable

    def test_placeholder_username_is_visible(self, cfg: SecurityConfig) -> None:
        """The placeholder marker is intentionally shown so operators
        can tell when no credentials were available."""
        redactor = CommandRedactor(cfg)
        _, display = redactor.render(
            "tool -u {username}",
            {},
            cfg.placeholder_username_marker,
            "",
        )
        assert cfg.placeholder_username_marker in display

    def test_executable_renders_substitutions(self, cfg: SecurityConfig) -> None:
        """Non-credential placeholders resolve correctly in both forms."""
        redactor = CommandRedactor(cfg)
        executable, display = redactor.render(
            "tool {ip}:{port}/{name}",
            {"ip": "10.0.0.5", "port": 22, "name": "svc"},
            "",
            "",
        )
        assert executable == "tool 10.0.0.5:22/svc"
        assert display == "tool 10.0.0.5:22/svc"

    def test_rejects_non_string_template(self, cfg: SecurityConfig) -> None:
        """``render`` must enforce string types on inputs."""
        redactor = CommandRedactor(cfg)
        with pytest.raises(TypeError):
            redactor.render(None, {}, "u", "p")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            redactor.render("tpl", "not-a-mapping", "u", "p")  # type: ignore[arg-type]


class TestOutputSanitizer:
    """Information-exposure guarantees (#731)."""

    def test_exception_is_replaced(self, cfg: SecurityConfig) -> None:
        """Exception instances yield the opaque placeholder."""
        sanitizer = OutputSanitizer(cfg)
        result = sanitizer.sanitize(ValueError("/etc/passwd"))
        assert result == cfg.exception_placeholder
        assert "passwd" not in str(result)

    def test_exception_nested_in_collection(self, cfg: SecurityConfig) -> None:
        """Exceptions inside lists and dicts are stripped recursively."""
        sanitizer = OutputSanitizer(cfg)
        out = sanitizer.sanitize({"err": [RuntimeError("secret")]})
        assert out == {"err": [cfg.exception_placeholder]}

    def test_recursion_is_bounded(self, cfg: SecurityConfig) -> None:
        """Deeply nested structures yield the non-serialisable sentinel."""
        sanitizer = OutputSanitizer(cfg)
        value: object = {"k": 0}
        for _ in range(cfg.max_serialization_depth + 5):
            value = {"k": value}
        result = sanitizer.sanitize(value)
        text = repr(result)
        assert cfg.non_serializable_placeholder in text

    def test_breadth_is_bounded(self, cfg: SecurityConfig) -> None:
        """Collections are truncated to the configured cap."""
        sanitizer = OutputSanitizer(cfg)
        big_list = list(range(cfg.max_serialization_collection + 50))
        out = sanitizer.sanitize(big_list)
        assert isinstance(out, list)
        assert len(out) == cfg.max_serialization_collection

    def test_passes_through_scalars(self, cfg: SecurityConfig) -> None:
        """Primitive types are returned unchanged."""
        sanitizer = OutputSanitizer(cfg)
        assert sanitizer.sanitize(None) is None
        assert sanitizer.sanitize(True) is True
        assert sanitizer.sanitize(42) == 42
        assert sanitizer.sanitize(3.14) == 3.14
        assert sanitizer.sanitize("ok") == "ok"

    def test_decodes_bytes(self, cfg: SecurityConfig) -> None:
        """Bytes are decoded with replacement for invalid sequences."""
        sanitizer = OutputSanitizer(cfg)
        assert sanitizer.sanitize(b"hello") == "hello"
        assert isinstance(sanitizer.sanitize(b"\xff\xfe"), str)

    def test_unknown_objects_become_sentinel(self, cfg: SecurityConfig) -> None:
        """Arbitrary objects are not stringified - they become the sentinel."""

        class Custom:
            def __str__(self) -> str:
                return "/internal/secret"

        sanitizer = OutputSanitizer(cfg)
        assert sanitizer.sanitize(Custom()) == cfg.non_serializable_placeholder


class TestIntegrationFromPayloadFile:
    """End-to-end check that the module reads ``payload.json`` cleanly."""

    def test_real_payload_file_builds_config(self) -> None:
        """The bundled ``payload.json`` must produce a valid configuration."""
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "payload.json",
        )
        if not os.path.exists(path):
            pytest.skip("payload.json is not present in this environment")
        import json

        with open(path, "r") as fh:
            data = json.load(fh)
        cfg = build_default_config(data)
        assert isinstance(cfg, SecurityConfig)
        resolver = BindAddressResolver(cfg, [data.get("c2_bind_address"), data.get("lhost")])
        bound = resolver.resolve()
        assert bound and isinstance(bound, str)


def test_module_exports_are_complete() -> None:
    """``__all__`` must list every public class and helper."""
    from modules import security_sanitizers as mod

    for name in (
        "SecurityConfig",
        "HeaderValueSanitizer",
        "SessionPathResolver",
        "BindAddressResolver",
        "CommandRedactor",
        "OutputSanitizer",
        "build_default_config",
    ):
        assert name in mod.__all__
        assert hasattr(mod, name)
