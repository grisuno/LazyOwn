"""Compliance blueprint — evidence chain and SIEM export surfaces.

Extracted from the ``lazyc2`` monolith: the compliance dashboard, the
report generator (markdown + PDF artifacts under ``sessions/``), the
evidence add/verify endpoints and the SIEM bulk exports (Elastic
NDJSON, CEF). Every route requires an operator session plus the RBAC
permission, and decoy mode is resolved through the canonical
:func:`lazyc2.extensions.decoy.decoy_response` contract.
"""

from __future__ import annotations

import dataclasses
import os
from datetime import datetime
from pathlib import Path

from flask import Blueprint, flash, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required

from lazyc2.extensions.decoy import decoy_response
from modules.lazy_rbac import Permission, require_permission

compliance_bp = Blueprint("compliance", __name__)


def _decoy_or_none():
    return decoy_response()


@compliance_bp.route("/compliance", methods=["GET"])
@login_required
@require_permission(Permission.AUDIT_VIEW.value)
def compliance_dashboard():
    response = _decoy_or_none()
    if response:
        return response
    try:
        from modules.compliance import ComplianceEngine, ComplianceFinding  # noqa: F401

        engine = ComplianceEngine("sessions")
        report = engine.generate_compliance_report(include_evidence_chain=True)
        return render_template(
            "compliance.html",
            report=report,
            current_user=current_user,
        )
    except ImportError:
        flash("Compliance module not available.", "error")
        return redirect(url_for("report"))


@compliance_bp.route("/compliance/report", methods=["GET"])
@login_required
@require_permission(Permission.REPORT_GENERATE.value)
def compliance_report():
    response = _decoy_or_none()
    if response:
        return response
    try:
        from modules.compliance import ComplianceEngine, ComplianceFinding, export_pdf  # noqa: F401

        engine = ComplianceEngine("sessions")
        report = engine.generate_compliance_report(
            include_evidence_chain=True,
            include_siem_formats=True,
        )
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        md_path = f"sessions/compliance_report_{ts}.md"
        md_content = engine._format_compliance_report_md(report)
        Path(md_path).write_text(md_content, encoding="utf-8")

        pdf_path = engine.export_pdf(report, f"sessions/compliance_report_{ts}.pdf")
        flash(f"Compliance report generated: {md_path}" + (f", {pdf_path}" if pdf_path else ""), "success")
    except ImportError:
        flash("Compliance module not available.", "error")
    except Exception as e:
        from flask import current_app

        current_app.logger.warning("compliance report failed: %s", type(e).__name__)
        flash("Error generating compliance report.", "error")
    return redirect(url_for("compliance_dashboard"))


@compliance_bp.route("/compliance/evidence/add", methods=["POST"])
@login_required
@require_permission(Permission.CMD_RUN.value)
def compliance_add_evidence():
    try:
        from modules.compliance import ComplianceEngine

        engine = ComplianceEngine("sessions")
        filepath = request.form.get("filepath", "").strip()
        operator = current_user.username
        description = request.form.get("description", "").strip()
        if not filepath:
            return jsonify({"error": "File not found"}), 400
        from core.hardening import realpath_contained

        try:
            safe_path = realpath_contained(filepath, "sessions")
        except (PermissionError, ValueError):
            return jsonify({"error": "Invalid path"}), 400
        if not os.path.exists(safe_path):
            return jsonify({"error": "File not found"}), 400
        entry = engine.add_evidence(safe_path, operator, description)
        return jsonify(
            {
                "status": "added",
                "sha256": entry.sha256,
                "filename": entry.filename,
            }
        )
    except ImportError:
        return jsonify({"error": "Compliance module not available"}), 500
    except Exception:
        from flask import current_app

        current_app.logger.error("Evidence add failed", exc_info=True)
        return jsonify({"error": "Internal error"}), 500


@compliance_bp.route("/compliance/evidence/verify", methods=["GET"])
@login_required
@require_permission(Permission.AUDIT_VIEW.value)
def compliance_verify_evidence():
    try:
        from modules.compliance import ComplianceEngine

        engine = ComplianceEngine("sessions")
        valid, issues = engine.verify_evidence_chain()
        return jsonify({"valid": valid, "issues": issues})
    except ImportError:
        return jsonify({"error": "Compliance module not available"}), 500


@compliance_bp.route("/compliance/export/<format>", methods=["GET"])
@login_required
@require_permission(Permission.REPORT_GENERATE.value)
def compliance_export(format):
    try:
        from modules.compliance import (  # noqa: F401
            ComplianceEngine,
            ComplianceFinding,
            export_to_cef,
            export_to_elastic_ndjson,
        )

        engine = ComplianceEngine("sessions")
        findings = engine._load_findings()
        finding_dicts = [dataclasses.asdict(f) for f in findings]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "elastic":
            path = f"sessions/siem_export_bulk_{ts}.ndjson"
            export_to_elastic_ndjson(finding_dicts, path)
            return send_file(path, as_attachment=True, download_name=f"lazyown_findings_{ts}.ndjson")
        elif format == "cef":
            path = f"sessions/siem_export_cef_{ts}.log"
            export_to_cef(finding_dicts, path)
            return send_file(path, as_attachment=True, download_name=f"lazyown_findings_{ts}.cef")
        else:
            return jsonify({"error": f"Unknown format: {format}. Use 'elastic' or 'cef'"}), 400
    except ImportError:
        return jsonify({"error": "Compliance module not available"}), 500
