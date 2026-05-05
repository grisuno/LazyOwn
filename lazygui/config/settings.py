"""Persisted user settings.

Settings live in a JSON file under :attr:`AppPaths.config_dir`. The class
exposes typed accessors on top of the JSON document so the rest of the code
never deals with raw dictionaries or string keys directly.

Anything stored here is user-tunable. Defaults always come from
:class:`AppConstants`; this class is the only legitimate location for runtime
mutation of those defaults.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Mapping

from lazygui.config.constants import AppConstants
from lazygui.config.paths import AppPaths

_logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AppSettings:
    """Read/write wrapper around the persisted settings JSON document."""

    constants: AppConstants
    paths: AppPaths
    _document: dict[str, Any]

    @classmethod
    def load(cls, constants: AppConstants, paths: AppPaths) -> "AppSettings":
        """Load settings from disk, returning empty defaults if absent."""
        document: dict[str, Any] = {}
        target = paths.settings_file
        if target.is_file():
            try:
                document = json.loads(target.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                _logger.warning("Failed to read settings file %s: %s", target, exc)
                document = {}
        return cls(constants=constants, paths=paths, _document=document)

    def save(self) -> None:
        """Persist the current document to disk atomically."""
        self.paths.ensure_config_dir()
        target = self.paths.settings_file
        tmp = target.with_suffix(target.suffix + ".tmp")
        tmp.write_text(json.dumps(self._document, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(target)

    def get(self, key: str, default: Any = None) -> Any:
        """Generic accessor for a slash-separated settings key."""
        return self._document.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Assign ``value`` to ``key`` without persisting; call :meth:`save`."""
        self._document[key] = value

    @property
    def theme_id(self) -> str:
        """Currently selected theme identifier."""
        return str(self.get(self.constants.ids.theme_setting_key, self.constants.theme.default_palette_id))

    @theme_id.setter
    def theme_id(self, value: str) -> None:
        self.set(self.constants.ids.theme_setting_key, value)

    @property
    def last_backend_id(self) -> str:
        """Backend identifier last used in the connect dialog."""
        return str(self.get(self.constants.ids.last_backend_setting_key, self.constants.backend.local_id))

    @last_backend_id.setter
    def last_backend_id(self, value: str) -> None:
        if value not in self.constants.backend.available_ids:
            raise ValueError(f"Unknown backend id: {value!r}")
        self.set(self.constants.ids.last_backend_setting_key, value)

    @property
    def last_teamserver_url(self) -> str:
        """Last URL typed in the teamserver connection form."""
        default = (
            f"{self.constants.network.default_teamserver_scheme}://"
            f"{self.constants.network.default_teamserver_host}:"
            f"{self.constants.network.default_teamserver_port}"
        )
        return str(self.get(self.constants.ids.last_teamserver_url_setting_key, default))

    @last_teamserver_url.setter
    def last_teamserver_url(self, value: str) -> None:
        self.set(self.constants.ids.last_teamserver_url_setting_key, value)

    @property
    def last_operator_name(self) -> str:
        """Operator handle the user typed last."""
        return str(self.get(self.constants.ids.last_operator_name_setting_key, self.constants.network.default_teamserver_username))

    @last_operator_name.setter
    def last_operator_name(self, value: str) -> None:
        self.set(self.constants.ids.last_operator_name_setting_key, value)

    def snapshot(self) -> Mapping[str, Any]:
        """Return a defensive read-only copy of the underlying document."""
        return dict(self._document)
