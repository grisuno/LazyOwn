"""Operations blueprint — tasks, CVEs, notes, and event management.

CRUD endpoints for the C2 operator's daily workflow.
Registered under no prefix in :func:`lazyc2.app_factory.create_app`.
"""

from __future__ import annotations

import markdown
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from lazyc2.extensions.decoy import decoy_response
from lazyc2.extensions.storage import (
    load_cves,
    load_event_config,
    load_note,
    load_tasks,
    save_cves,
    save_note,
    save_tasks,
)

operations_bp = Blueprint("operations", __name__)

_TASK_VALID_STATUSES = ["New", "Refined", "Started", "Review", "Qa", "Done", "Blocked"]
_CVE_VALID_RISKS = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]


@operations_bp.route("/task/<int:task_id>")
def task_detail(task_id: int):
    """View a single task by ID."""
    decoy = decoy_response()
    if decoy:
        return decoy
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        flash("Task not found!", "danger")
        return redirect(url_for("index"))
    desc = markdown.markdown(task["description"])
    return render_template("task.html", task=task, task_description=desc)


@operations_bp.route("/gettasks")
def get_tasks():
    """Return all tasks as JSON."""
    decoy = decoy_response()
    if decoy:
        return decoy
    return jsonify(load_tasks())


@operations_bp.route("/tasks")
def tasks():
    """Render the tasks list page."""
    decoy = decoy_response()
    if decoy:
        return decoy
    return render_template("tasks.html", tasks=load_tasks())


@operations_bp.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id: int):
    """Edit an existing task."""
    decoy = decoy_response()
    if decoy:
        return decoy
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        flash("Task not found!", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        status = request.form.get("status", "")
        if status not in _TASK_VALID_STATUSES:
            return "Invalid status selected!", 400
        task["title"] = request.form.get("title", "")
        task["description"] = request.form.get("description", "")
        task["operator"] = request.form.get("operator", "")
        task["status"] = status
        save_tasks(tasks)
        flash("Task updated successfully!", "success")
        return redirect(url_for("operations.task_detail", task_id=task_id))
    desc = markdown.markdown(task["description"])
    return render_template("edit_task.html", task=task, task_description=desc)


@operations_bp.route("/cves", methods=["GET", "POST"])
def cves():
    """List all CVEs or create a new one."""
    decoy = decoy_response()
    cve_list = load_cves()
    if decoy:
        return decoy
    if request.method == "POST":
        risk = request.form.get("risk", "")
        if risk not in _CVE_VALID_RISKS:
            return "Invalid Risk selected!", 400
        new_cve = {
            "id": len(cve_list),
            "title": request.form.get("title", ""),
            "description": request.form.get("description", ""),
            "operator": request.form.get("operator", ""),
            "risk": risk,
        }
        cve_list.append(new_cve)
        save_cves(cve_list)
        flash("Task created successfully!", "success")
        return redirect(url_for("index"))
    return render_template("cves.html", cves=cve_list)


@operations_bp.route("/cve/<int:cve_id>")
def cve_detail(cve_id: int):
    """View a single CVE by ID."""
    decoy = decoy_response()
    if decoy:
        return decoy
    cve_list = load_cves()
    cve = next((t for t in cve_list if t["id"] == cve_id), None)
    if not cve:
        flash("CVE not found!", "danger")
        return redirect(url_for("index"))
    desc = markdown.markdown(cve["description"])
    return render_template("cve.html", cve=cve, cve_description=desc)


@operations_bp.route("/cve/<int:cve_id>/edit", methods=["GET", "POST"])
def edit_cve(cve_id: int):
    """Edit an existing CVE entry."""
    decoy = decoy_response()
    if decoy:
        return decoy
    cve_list = load_cves()
    cve = next((t for t in cve_list if t["id"] == cve_id), None)
    if not cve:
        flash("Task not found!", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        status = request.form.get("status", "")
        if status not in _TASK_VALID_STATUSES:
            return "Invalid status selected!", 400
        cve["title"] = request.form.get("title", "")
        cve["description"] = request.form.get("description", "")
        cve["operator"] = request.form.get("operator", "")
        cve["status"] = status
        save_cves(cve_list)
        flash("Task updated successfully!", "success")
        return redirect(url_for("operations.cve_detail", cve_id=cve_id))
    desc = markdown.markdown(cve["description"])
    return render_template("edit_cve.html", cve=cve, cve_description=desc)


@operations_bp.route("/notes", methods=["GET", "POST"])
def edit_notes():
    """View or edit the operator notes."""
    decoy = decoy_response()
    if decoy:
        return decoy
    if request.method == "POST":
        content = str(request.form.get("content", ""))
        save_note(content)
        flash("Notes updated successfully!", "success")
        return redirect(url_for("operations.view_note"))
    notes = load_note()
    return render_template("edit_note.html", note=notes)


@operations_bp.route("/getnotes")
def get_notes():
    """Return notes as JSON."""
    decoy = decoy_response()
    if decoy:
        return decoy
    return jsonify(load_note())


@operations_bp.route("/view_note")
def view_note():
    """Render the notes view page."""
    decoy = decoy_response()
    if decoy:
        return decoy
    content = load_note()
    return render_template("view_note.html", content=content)


@operations_bp.route("/event_config")
def event_config():
    """Return event configuration as JSON."""
    return jsonify(load_event_config())


@operations_bp.route("/event_config_view", methods=["GET", "POST"])
def event_config_view():
    """View or update event configuration."""
    decoy = decoy_response()
    if decoy:
        return decoy
    config = load_event_config()
    if request.method == "POST":
        event_name = request.form.get("event_name", "")
        description = request.form.get("description", "")
        config.setdefault("events", []).append({"name": event_name, "description": description})
        import json as _json

        with open("event_config.json", "w") as f:
            _json.dump(config, f, indent=4)
        flash("Event added successfully!", "success")
        return redirect(url_for("operations.event_config_view"))
    return render_template("event_config.html", config=config)


@operations_bp.route("/events")
def events():
    """Render the events page."""
    decoy = decoy_response()
    if decoy:
        return decoy
    config = load_event_config()
    return render_template("events.html", config=config)
