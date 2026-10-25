"""Global C2 server state — namespace for shared mutable objects.

Extracted from lazyc2.py to break the circular dependency between
lazyc2.py and lazyc2/blueprints/. Both can import this module safely.
"""

from typing import Any

shell: Any = None
implants: dict = None
commands: dict = None
results: dict = None
commands_history: dict = None
remote_commands_history: dict = None
connected_clients: set = None
events: list = None
counter_events: int = 0
listener_manager: Any = None
login_manager: Any = None
socketio: Any = None
MODEL: Any = None
JSON_FILE_PATH_REPORT: str = "static/body_report.json"
USER_DATA_PATH: str = "users.json"
