"""Tests for the ``core.payload_schema`` validation layer.

The schema is the contract that gives ``payload.json`` a typed,
documented shape after years of being a free-form dictionary. These
tests pin three properties:

- Every key historically present in the shipped ``payload.json`` has a
  registered :class:`FieldSpec` so the operator gets descriptions for
  every value in the wizard.
- Type validation produces structured :class:`ValidationIssue` instances
  with the right severity for required vs optional fields.
- Coercion never widens behaviour beyond the documented narrow scope
  (port strings, boolean-like strings).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from core.payload_schema import (  # noqa: E402
    SCHEMA,
    FieldKind,
    FieldSpec,
    Severity,
    ValidationIssue,
    categories,
    coerce_value,
    default_payload,
    field_for,
    format_issue,
    validate_payload,
    validate_value,
)


class TestSchemaShape:
    def test_schema_is_not_empty(self):
        assert len(SCHEMA) > 30

    def test_every_spec_has_required_fields(self):
        for key, spec in SCHEMA.items():
            assert isinstance(spec, FieldSpec)
            assert spec.name == key
            assert spec.description
            assert isinstance(spec.kind, FieldKind)
            assert spec.category

    def test_required_fields_are_documented(self):
        required = [s for s in SCHEMA.values() if s.required]
        assert {s.name for s in required} >= {"rhost", "lhost", "os_id"}

    def test_shipped_payload_keys_are_all_in_schema(self):
        payload = json.loads((REPO_ROOT / "payload.json").read_text(encoding="utf-8"))
        missing = [key for key in payload if key not in SCHEMA]
        assert missing == [], (
            f"payload.json has keys with no FieldSpec: {missing}. "
            "Add an entry to SCHEMA so the wizard can document them."
        )

    def test_categories_split_schema(self):
        grouped = categories()
        assert "network" in grouped and "c2" in grouped and "ai" in grouped
        flat = [s for specs in grouped.values() for s in specs]
        assert len(flat) == len(SCHEMA)


class TestValidateValue:
    def test_unknown_key_returns_info(self):
        issue = validate_value("totally_unknown", "foo")
        assert issue is not None
        assert issue.severity is Severity.INFO

    def test_required_missing_returns_error(self):
        issue = validate_value("rhost", "")
        assert issue is not None and issue.severity is Severity.ERROR

    def test_optional_missing_returns_none(self):
        issue = validate_value("domain", "")
        assert issue is None

    def test_valid_ip_passes(self):
        assert validate_value("rhost", "10.10.11.5") is None

    def test_invalid_ip_returns_error(self):
        issue = validate_value("rhost", "not.an.ip.address")
        assert issue is not None
        assert issue.severity is Severity.ERROR
        assert "valid IPv4" in issue.message

    def test_port_string_is_accepted(self):
        assert validate_value("c2_port", "4444") is None

    def test_port_out_of_range_is_warning(self):
        issue = validate_value("c2_port", 70000)
        assert issue is not None and issue.severity is Severity.WARNING

    def test_negative_port_warns(self):
        issue = validate_value("lport", -1)
        assert issue is not None

    def test_os_id_must_be_1_or_2(self):
        assert validate_value("os_id", "1") is None
        assert validate_value("os_id", "2") is None
        issue = validate_value("os_id", "3")
        assert issue is not None and issue.severity is Severity.ERROR

    def test_url_validates(self):
        assert validate_value("url", "http://example.com/path") is None
        bad = validate_value("url", "not a url")
        assert bad is not None

    def test_hex_validates(self):
        assert validate_value("rat_key", "deadbeef00") is None
        assert validate_value("rat_key", "not-hex") is not None

    def test_allowed_values_enforced(self):
        assert validate_value("method", "POST") is None
        issue = validate_value("method", "TRACE")
        assert issue is not None
        assert "must be one of" in issue.message

    def test_hide_code_range(self):
        assert validate_value("hide_code", 404) is None
        assert validate_value("hide_code", 99) is not None
        assert validate_value("hide_code", 600) is not None


class TestCoerceValue:
    def test_port_string_to_int(self):
        assert coerce_value("c2_port", "4444") == 4444

    def test_port_int_passthrough(self):
        assert coerce_value("c2_port", 4444) == 4444

    def test_port_non_numeric_passthrough(self):
        assert coerce_value("c2_port", "not-a-number") == "not-a-number"

    def test_bool_truthy_strings(self):
        for value in ("true", "TRUE", "yes", "on", "1"):
            assert coerce_value("enable_cloudflare", value) is True

    def test_bool_falsy_strings(self):
        for value in ("false", "no", "off", "0"):
            assert coerce_value("enable_cloudflare", value) is False

    def test_bool_passthrough(self):
        assert coerce_value("enable_cloudflare", True) is True
        assert coerce_value("enable_cloudflare", False) is False

    def test_unknown_key_passthrough(self):
        assert coerce_value("unknown_key", "raw") == "raw"

    def test_ip_string_unchanged(self):
        assert coerce_value("rhost", "10.10.10.10") == "10.10.10.10"


class TestValidatePayload:
    def test_default_payload_passes(self):
        issues = validate_payload(default_payload())
        errors = [i for i in issues if i.severity is Severity.ERROR]
        assert errors == [], f"defaults produce errors: {errors}"

    def test_missing_required_field_reports_error(self):
        payload = default_payload()
        del payload["rhost"]
        issues = validate_payload(payload)
        rhost_errors = [
            i for i in issues if i.key == "rhost" and i.severity is Severity.ERROR
        ]
        assert rhost_errors

    def test_unknown_key_in_payload_is_info(self):
        payload = default_payload()
        payload["operator_extension"] = "anything"
        issues = validate_payload(payload)
        info = [i for i in issues if i.key == "operator_extension"]
        assert info and info[0].severity is Severity.INFO

    def test_shipped_payload_has_no_errors(self):
        payload = json.loads((REPO_ROOT / "payload.json").read_text(encoding="utf-8"))
        issues = validate_payload(payload)
        errors = [i for i in issues if i.severity is Severity.ERROR]
        assert errors == [], (
            "Shipped payload.json fails schema validation: "
            + "; ".join(format_issue(i) for i in errors)
        )


class TestFieldFor:
    def test_returns_spec_for_known_key(self):
        spec = field_for("rhost")
        assert spec is not None
        assert spec.required is True

    def test_returns_none_for_unknown_key(self):
        assert field_for("does_not_exist") is None


class TestFormatIssue:
    def test_sensitive_values_redacted(self):
        issue = ValidationIssue(
            key="api_key",
            message="example",
            severity=Severity.WARNING,
            value="gsk_secret_key_value",
        )
        rendered = format_issue(issue)
        assert "gsk_secret_key_value" not in rendered
        assert "redacted" in rendered

    def test_non_sensitive_values_shown(self):
        issue = ValidationIssue(
            key="rhost",
            message="example",
            severity=Severity.ERROR,
            value="10.10.10.10",
        )
        rendered = format_issue(issue)
        assert "10.10.10.10" in rendered

    def test_long_values_truncated(self):
        issue = ValidationIssue(
            key="url",
            message="example",
            severity=Severity.WARNING,
            value="x" * 200,
        )
        rendered = format_issue(issue)
        assert "..." in rendered
        assert len(rendered) < 200


class TestAssignIntegration:
    def test_apply_assign_coerces_port_strings(self):
        from cli.assign import apply_assign

        params = {"c2_port": 4444}
        ok = apply_assign(params, "c2_port", "5555")
        assert ok is True
        assert params["c2_port"] == 5555

    def test_apply_assign_surfaces_issue_for_bad_ip(self):
        from cli.assign import apply_assign

        captured: list = []
        params = {"rhost": "10.10.10.10"}
        ok = apply_assign(
            params,
            "rhost",
            "not.an.ip",
            on_issue=captured.append,
        )
        assert ok is True
        assert captured
        assert captured[0].severity is Severity.ERROR

    def test_apply_assign_no_issue_for_valid_value(self):
        from cli.assign import apply_assign

        captured: list = []
        params = {"rhost": "10.10.10.10"}
        apply_assign(params, "rhost", "192.168.1.1", on_issue=captured.append)
        assert captured == []

    def test_apply_assign_keeps_unknown_key_behavior(self):
        from cli.assign import apply_assign

        params = {"rhost": "10.10.10.10"}
        assert apply_assign(params, "made_up_key", "x") is False
        assert "made_up_key" not in params
