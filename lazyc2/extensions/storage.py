"""JSON-file storage helpers for the C2 web interface.

Provides load/save helpers for tasks, CVEs, notes, events,
notifications, banners, and dynamic routes. All files live under
``sessions/`` and are managed with atomic write patterns.
"""

from __future__ import annotations

import json
import logging
import os
import stat

SESSION_DIR = "sessions"


def configure(sessions_dir: str = "sessions") -> None:
    """Set the session directory path.

    Args:
        sessions_dir: Path to the session storage directory.
    """
    global SESSION_DIR  # noqa: PLW0603
    SESSION_DIR = sessions_dir


# ── Tasks ──────────────────────────────────────────────────────────────────


def load_tasks() -> list[dict]:
    """Load tasks from ``sessions/tasks.json``.

    Returns:
        A list of task dicts.
    """
    path = os.path.join(SESSION_DIR, "tasks.json")
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    with open(path) as f:
        return json.load(f)


def save_tasks(tasks: list[dict]) -> None:
    """Persist tasks to ``sessions/tasks.json``.

    Args:
        tasks: List of task dicts.
    """
    path = os.path.join(SESSION_DIR, "tasks.json")
    with open(path, "w") as f:
        json.dump(tasks, f, indent=4)


# ── CVEs ───────────────────────────────────────────────────────────────────


def load_cves() -> list[dict]:
    """Load CVEs from ``sessions/cves.json``.

    Returns:
        A list of CVE dicts.
    """
    path = os.path.join(SESSION_DIR, "cves.json")
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    with open(path) as f:
        return json.load(f)


def save_cves(cves: list[dict]) -> None:
    """Persist CVEs to ``sessions/cves.json``.

    Args:
        cves: List of CVE dicts.
    """
    path = os.path.join(SESSION_DIR, "cves.json")
    with open(path, "w") as f:
        json.dump(cves, f, indent=4)


# ── Notes ──────────────────────────────────────────────────────────────────


def load_note() -> dict:
    """Load the operator note from ``sessions/notes.txt``.

    Returns:
        A dict with a single ``content`` key.
    """
    path = os.path.join(SESSION_DIR, "notes.txt")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(json.dumps({"content": ""}))
    with open(path) as f:
        raw = f.read().strip()
    if not raw:
        return {"content": ""}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"content": ""}


def save_note(content: str) -> None:
    """Persist the operator note to ``sessions/notes.txt``.

    Args:
        content: Note body string.
    """
    path = os.path.join(SESSION_DIR, "notes.txt")
    with open(path, "w") as f:
        f.write(json.dumps({"content": content}))


# ── Events ─────────────────────────────────────────────────────────────────


def load_event_config() -> dict:
    """Load event configuration from ``event_config.json``.

    Returns:
        A dict with an ``events`` list, or an empty config.
    """
    try:
        with open("event_config.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"events": []}


# ── Notifications ──────────────────────────────────────────────────────────


def load_notifications() -> list[dict]:
    """Load notifications from ``sessions/notifications.json``.

    Returns:
        A list of notification dicts.
    """
    path = os.path.join(SESSION_DIR, "notifications.json")
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    with open(path) as f:
        return json.load(f)


# ── Banners ────────────────────────────────────────────────────────────────


def load_banners() -> dict | None:
    """Load banners from ``sessions/banners.json``.

    Returns:
        A banner config dict, or ``None`` when the file is absent.
    """
    path = os.path.join(SESSION_DIR, "banners.json")
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return None


# ── Routes (dynamic template routes) ───────────────────────────────────────


def load_routes() -> dict:
    """Load dynamic routes from ``sessions/routes_to_templates.json``.

    Returns:
        A dict mapping route paths to template names.
    """
    path = os.path.join(SESSION_DIR, "routes_to_templates.json")
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("Failed to load routes: %s", e)
        return {}


def save_routes(routes: dict) -> None:
    """Persist dynamic routes with atomic write and safe permissions.

    Args:
        routes: Dict mapping route paths to template names.
    """
    path = os.path.join(SESSION_DIR, "routes_to_templates.json")
    tmp = path + ".tmp"
    try:
        os.makedirs(SESSION_DIR, exist_ok=True)
        with open(tmp, "w") as f:
            json.dump(routes, f, indent=2)
        os.rename(tmp, path)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except Exception as e:
        logging.error("Failed to save routes: %s", e)
