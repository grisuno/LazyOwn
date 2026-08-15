"""LazyAddon creator contract for the LazyOwn C2 web interface.

Single source of truth for authoring ``lazyaddons/*.yaml`` files from the
``/addons/create`` form shipped with ``lazyc2.py``. The contract covers
the full lifecycle: form parsing, validation, YAML rendering, and safe
persistence, so the CLI loader in ``lazyown.py`` can register the
resulting file as a first-class shell command.

Contracts:
    - AddonCreatorConfig: centralised constants and schema options
    - ParamSpec: immutable value object for one addon parameter
    - AddonDraft: mutable form state collected by the web layer
    - ValidationIssue: one field-specific validation finding
    - AddonValidationError: raised when a draft is not persistable
    - AddonValidator: pure validation returning field-specific issues
    - AddonYamlRenderer: renders an AddonDraft as canonical addon YAML
    - AddonStore: path-safe, atomic persistence inside the addons directory
    - parse_addon_form: adapts Flask form data into an AddonDraft

Design (SOLID):
    - Single Responsibility: validation, rendering, and persistence are
      separate collaborators, each with one reason to change
    - Open/Closed: new categories, OS values, or triggers extend the
      config constants without touching behaviour
    - Liskov: parse_addon_form accepts any Mapping, Flask MultiDict
      included, and every collaborator is independently replaceable
    - Interface Segregation: the Flask blueprint consumes only the small
      public surface below, never internal state
    - Dependency Inversion: the web layer depends on this contract,
      never the other way around

Security invariants:
    - Addon names pass a strict whitelist regex, so path traversal
      through the generated filename is impossible by construction
    - AddonStore re-checks realpath containment against the addons
      directory as defence in depth before any read, write, or delete
    - Every write is atomic (temp file plus os.replace) so an aborted
      request can never leave a half-written addon behind
    - Command placeholder tokens are validated against declared params
      and known payload.json keys so a typo cannot ship silently

Usage:
    from lazyc2.addon_creator import (
        AddonStore,
        AddonValidator,
        AddonYamlRenderer,
        parse_addon_form,
    )

    draft = parse_addon_form(request.form)
    issues = AddonValidator(draft).validate()
    yaml_text = AddonYamlRenderer().render(draft)
    path = AddonStore().save(draft.name, yaml_text)
"""

from __future__ import annotations

import os
import re
import stat
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


class AddonCreatorConfig:
    """Centralised constants and schema options for the addon creator.

    Every whitelist, pattern, length limit, and default value lives here
    so the contract stays data-driven and nothing is hardcoded in the
    collaborators below.
    """

    addons_dir: str = "lazyaddons"
    file_suffix: str = ".yaml"
    tmp_suffix: str = ".tmp"
    file_mode: int = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    yaml_width: int = 88

    name_pattern: re.Pattern[str] = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
    filename_pattern: re.Pattern[str] = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,127}$")
    version_pattern: re.Pattern[str] = re.compile(r"^\d+(\.\d+){0,3}$")
    param_name_pattern: re.Pattern[str] = re.compile(r"^[a-z][a-z0-9_]{0,47}$")
    trigger_pattern: re.Pattern[str] = re.compile(r"^[a-z0-9][a-z0-9\-]{0,63}$")
    category_pattern: re.Pattern[str] = re.compile(r"^\d{2}\. [A-Za-z0-9 /&()+\-]{3,60}$")
    env_pattern: re.Pattern[str] = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:\s?.*$")
    rel_path_pattern: re.Pattern[str] = re.compile(r"^[A-Za-z0-9._\-]+(/[A-Za-z0-9._\-]+)*$")
    placeholder_pattern: re.Pattern[str] = re.compile(r"\{([^{}]+)\}")
    double_brace_pattern: re.Pattern[str] = re.compile(r"\{\{[^{}]*\}\}")

    description_max_length: int = 500
    author_max_length: int = 80
    param_description_max_length: int = 200
    default_value_max_length: int = 200
    max_params: int = 20
    max_triggers: int = 40

    param_types: tuple[str, ...] = ("string", "integer", "boolean")

    os_options: tuple[str, ...] = (
        "any",
        "linux",
        "windows",
        "macos",
        "network",
        "containers",
        "saas",
        "iaas",
    )

    category_options: tuple[str, ...] = (
        "01. Reconnaissance",
        "02. Scanning & Enumeration",
        "03. Exploitation",
        "04. Evasion & Bypass",
        "04. Post-Exploitation",
        "06. Privilege Escalation",
        "07. Credential Access",
        "08. Lateral Movement",
        "09. Data Exfiltration",
        "10. Command & Control",
        "11. Reporting",
        "12. Credential Access & Bypass",
        "12. Miscellaneous",
        "16. Artificial Intelligence",
        "17. Cloud Attacks",
        "18. Container & Kubernetes",
        "20. CI/CD Pipeline Attacks",
    )

    module_type_options: tuple[str, ...] = ("scanner", "exploit", "payload", "auxiliary")
    install_type_options: tuple[str, ...] = ("git",)

    trigger_options: tuple[str, ...] = (
        "ftp",
        "ftps",
        "ssh",
        "telnet",
        "http",
        "https",
        "http-proxy",
        "smtp",
        "pop3",
        "imap",
        "dns",
        "dhcp",
        "ntp",
        "snmp",
        "ldap",
        "rpc",
        "nfs",
        "smb",
        "microsoft-ds",
        "netbios-ssn",
        "msrpc",
        "rdp",
        "mysql",
        "mssql",
        "postgresql",
        "oracle",
        "mongodb",
        "redis",
        "memcached",
        "elasticsearch",
        "rabbitmq",
        "mqtt",
        "kubernetes",
        "sip",
        "sccp",
        "irc",
        "xmpp",
        "rtsp",
        "kafka",
        "zookeeper",
        "cassandra",
        "activemq",
        "amqp",
        "stomp",
        "coap",
        "modbus",
        "bacnet",
        "afp",
    )

    payload_placeholders: frozenset[str] = frozenset(
        {
            "aes_key",
            "backdoor_linux_home",
            "backdoor_password",
            "backdoor_username",
            "backdoor_win_home",
            "backdoor_win_service_path",
            "baseoutputdir",
            "binary_name",
            "c2_malleable_route",
            "c2_pass",
            "c2_port",
            "c2_user",
            "cloud_provider",
            "cloud_region",
            "data",
            "data_file",
            "device",
            "dirwordlist",
            "dnswordlist",
            "domain",
            "email_from",
            "email_password",
            "email_to",
            "email_username",
            "enable_c2_implant_debug",
            "enable_cloudflare",
            "enable_operator_presence",
            "enable_toasts",
            "endip",
            "exploitdb",
            "ext",
            "field",
            "file",
            "headers",
            "headers_file",
            "hide_code",
            "ip",
            "json_data",
            "json_data_file",
            "lhost",
            "listener",
            "lport",
            "method",
            "mode",
            "nameserver",
            "os_id",
            "outputdir",
            "params",
            "params_file",
            "pass",
            "password",
            "path",
            "port",
            "prompt",
            "proxy_port",
            "rat_key",
            "region",
            "report_output_path",
            "reverse_shell_port",
            "rhost",
            "rport",
            "s",
            "scan_type",
            "scope",
            "scope_enforcement",
            "sleep",
            "sleep_start",
            "smtp_port",
            "smtp_server",
            "spoof_ip",
            "start_pass",
            "start_user",
            "startip",
            "subdomain",
            "target",
            "toast_max_per_tick",
            "toolname",
            "tui_theme",
            "url",
            "url_traffic_1",
            "url_traffic_2",
            "url_traffic_3",
            "user",
            "user_agent_1",
            "user_agent_2",
            "user_agent_3",
            "user_agent_lin",
            "user_agent_win",
            "username",
            "usrwordlist",
            "wordlist",
        }
    )

    default_author: str = "LazyOwn"
    default_version: str = "1.0"
    default_os: str = "any"
    default_install_type: str = "git"


@dataclass(frozen=True)
class ParamSpec:
    """One addon parameter declared under the ``params`` key.

    Attributes:
        name: Placeholder token, must match ``param_name_pattern``.
        type: One of ``param_types``.
        required: Whether the CLI refuses to run without a value.
        description: Short help text shown to the operator.
        default: Optional fallback value applied when payload.json
            does not define the parameter.
    """

    name: str
    type: str = "string"
    required: bool = False
    description: str = ""
    default: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Return the param as a schema-ordered mapping."""
        payload: dict[str, object] = {
            "name": self.name,
            "type": self.type,
            "required": self.required,
        }
        if self.default is not None and str(self.default) != "":
            payload["default"] = self.default
        if self.description:
            payload["description"] = self.description
        return payload


@dataclass
class AddonDraft:
    """Complete addon form state collected from the web layer."""

    name: str = ""
    description: str = ""
    author: str = ""
    version: str = ""
    enabled: bool = True
    os: str = "any"
    triggers: list[str] = field(default_factory=list)
    category: str = ""
    module_type: str = ""
    install_type: str = ""
    params: list[ParamSpec] = field(default_factory=list)
    tool_name: str = ""
    repo_url: str = ""
    install_path: str = ""
    install_command: str = ""
    execute_command: str = ""
    upload_file: str = ""
    remote_command: str = ""
    download_file: str = ""
    lazycommand: str = ""
    env: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ValidationIssue:
    """One field-specific validation finding for the form."""

    field: str
    message: str


class AddonValidationError(ValueError):
    """Raised when an AddonDraft cannot be persisted.

    Attributes:
        issues: The collected ValidationIssue instances.
    """

    def __init__(self, issues: list[ValidationIssue]) -> None:
        self.issues = issues
        summary = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
        super().__init__(f"Addon validation failed: {summary}")


class AddonValidator:
    """Pure validation of an AddonDraft against the schema contract.

    The validator performs no I/O; name collision checks belong to the
    web layer because they require store state.
    """

    def __init__(
        self,
        draft: AddonDraft,
        config: AddonCreatorConfig | None = None,
    ) -> None:
        """Store the draft and configuration used by every check.

        Args:
            draft: The form state to validate.
            config: Optional configuration override for tests.
        """
        self.draft = draft
        self.config = config or AddonCreatorConfig()

    def validate(self) -> list[ValidationIssue]:
        """Run every rule and return the collected issues.

        Returns:
            A list of ValidationIssue instances, empty when the draft
            is valid.
        """
        issues: list[ValidationIssue] = []
        issues.extend(self._check_identity())
        issues.extend(self._check_targeting())
        issues.extend(self._check_tool())
        issues.extend(self._check_params())
        return issues

    def is_valid(self) -> bool:
        """Return True when the draft passes every rule."""
        return not self.validate()

    def _check_identity(self) -> list[ValidationIssue]:
        """Validate name, description, author, and version fields."""
        issues: list[ValidationIssue] = []
        name = self.draft.name.strip()
        if not name:
            issues.append(ValidationIssue("name", "Name is required."))
        elif not self.config.name_pattern.fullmatch(name):
            issues.append(
                ValidationIssue(
                    "name",
                    "Name must be lowercase, start with a letter, and contain "
                    "only letters, digits, and underscores (max 64 characters).",
                )
            )
        description = self.draft.description.strip()
        if not description:
            issues.append(ValidationIssue("description", "Description is required."))
        elif len(description) > self.config.description_max_length:
            issues.append(
                ValidationIssue(
                    "description",
                    f"Description exceeds {self.config.description_max_length} characters.",
                )
            )
        author = self.draft.author.strip()
        if author and len(author) > self.config.author_max_length:
            issues.append(
                ValidationIssue(
                    "author",
                    f"Author exceeds {self.config.author_max_length} characters.",
                )
            )
        version = self.draft.version.strip()
        if not version:
            issues.append(ValidationIssue("version", "Version is required."))
        elif not self.config.version_pattern.fullmatch(version):
            issues.append(
                ValidationIssue(
                    "version",
                    "Version must look like 1.0, 1.0.0, or 2.1.0-beta style is not allowed; use digits and dots only.",
                )
            )
        return issues

    def _check_targeting(self) -> list[ValidationIssue]:
        """Validate os, category, module/install type, and triggers."""
        issues: list[ValidationIssue] = []
        if self.draft.os not in self.config.os_options:
            issues.append(
                ValidationIssue(
                    "os",
                    f"OS must be one of: {', '.join(self.config.os_options)}.",
                )
            )
        category = self.draft.category.strip()
        if not category:
            issues.append(ValidationIssue("category", "Category is required."))
        elif not self.config.category_pattern.fullmatch(category):
            issues.append(
                ValidationIssue(
                    "category",
                    "Category must look like '03. Exploitation'.",
                )
            )
        if self.draft.module_type and self.draft.module_type not in self.config.module_type_options:
            issues.append(
                ValidationIssue(
                    "module_type",
                    f"Module type must be one of: {', '.join(self.config.module_type_options)}.",
                )
            )
        if self.draft.install_type and self.draft.install_type not in self.config.install_type_options:
            issues.append(
                ValidationIssue(
                    "install_type",
                    f"Install type must be one of: {', '.join(self.config.install_type_options)}.",
                )
            )
        triggers = self.draft.triggers
        if len(triggers) > self.config.max_triggers:
            issues.append(ValidationIssue("trigger", f"At most {self.config.max_triggers} triggers allowed."))
        for trigger in triggers:
            if not self.config.trigger_pattern.fullmatch(trigger):
                issues.append(
                    ValidationIssue(
                        "trigger",
                        f"Trigger '{trigger}' must be a lowercase service name using letters, digits, and hyphens.",
                    )
                )
        return issues

    def _check_tool(self) -> list[ValidationIssue]:
        """Validate the tool block: URLs, paths, and command placeholders."""
        issues: list[ValidationIssue] = []
        repo_url = self.draft.repo_url.strip()
        if repo_url and not self._is_valid_repo_url(repo_url):
            issues.append(
                ValidationIssue(
                    "repo_url",
                    "Repository URL must be an absolute http(s) URL, for example https://github.com/user/repo.",
                )
            )
        install_path = self.draft.install_path.strip()
        if install_path:
            if not self.config.rel_path_pattern.fullmatch(install_path):
                issues.append(
                    ValidationIssue(
                        "install_path",
                        "Install path must be a relative path without spaces, backslashes, or '..' segments.",
                    )
                )
            if ".." in install_path.split("/"):
                issues.append(ValidationIssue("install_path", "Install path must not contain '..'."))
            if not repo_url:
                issues.append(
                    ValidationIssue(
                        "repo_url",
                        "Repository URL is required when an install path is set, "
                        "because the CLI clones the repository.",
                    )
                )
        execute_command = self.draft.execute_command.strip()
        if not execute_command:
            issues.append(ValidationIssue("execute_command", "Execute command is required."))
        else:
            issues.extend(self._check_placeholders(execute_command, "execute_command"))
        install_command = self.draft.install_command.strip()
        if install_command:
            issues.extend(self._check_placeholders(install_command, "install_command"))
        remote_command = self.draft.remote_command.strip()
        if remote_command:
            issues.extend(self._check_placeholders(remote_command, "remote_command"))
        for entry in self.draft.env:
            if not self.config.env_pattern.fullmatch(entry):
                issues.append(
                    ValidationIssue(
                        "env",
                        f"Environment entry '{entry}' must use the 'KEY: value' format.",
                    )
                )
        return issues

    def _check_params(self) -> list[ValidationIssue]:
        """Validate the declared parameter rows."""
        issues: list[ValidationIssue] = []
        params = self.draft.params
        if len(params) > self.config.max_params:
            issues.append(ValidationIssue("params", f"At most {self.config.max_params} parameters allowed."))
        seen: set[str] = set()
        for param in params:
            name = param.name.strip()
            if not name:
                issues.append(ValidationIssue("params", "Every parameter needs a name."))
                continue
            if not self.config.param_name_pattern.fullmatch(name):
                issues.append(
                    ValidationIssue(
                        "params",
                        f"Parameter '{name}' must be lowercase, start with a letter, "
                        "and contain only letters, digits, and underscores.",
                    )
                )
            if name in seen:
                issues.append(ValidationIssue("params", f"Duplicate parameter '{name}'."))
            seen.add(name)
            if param.type not in self.config.param_types:
                issues.append(
                    ValidationIssue(
                        "params",
                        f"Parameter '{name}' has unknown type '{param.type}'.",
                    )
                )
            if not param.description.strip():
                issues.append(
                    ValidationIssue(
                        "params",
                        f"Parameter '{name}' needs a short description so operators know what to provide.",
                    )
                )
            elif len(param.description.strip()) > self.config.param_description_max_length:
                issues.append(
                    ValidationIssue(
                        "params",
                        f"Parameter '{name}' description exceeds "
                        f"{self.config.param_description_max_length} characters.",
                    )
                )
            if param.default is not None:
                default_text = str(param.default)
                if len(default_text) > self.config.default_value_max_length:
                    issues.append(
                        ValidationIssue(
                            "params",
                            f"Parameter '{name}' default exceeds {self.config.default_value_max_length} characters.",
                        )
                    )
                if param.type == "integer":
                    try:
                        int(default_text)
                    except ValueError:
                        issues.append(
                            ValidationIssue(
                                "params",
                                f"Parameter '{name}' default must be an integer.",
                            )
                        )
                if param.type == "boolean" and default_text.strip().lower() not in ("true", "false"):
                    issues.append(
                        ValidationIssue(
                            "params",
                            f"Parameter '{name}' default must be 'true' or 'false'.",
                        )
                    )
        return issues

    def _check_placeholders(self, text: str, field: str) -> list[ValidationIssue]:
        """Validate every {token} inside a command template.

        Double-brace tokens are rejected explicitly because the CLI
        replacement engine only honours single braces; nested forms
        otherwise survive extraction as valid-looking tokens.

        Args:
            text: The command template to scan.
            field: The form field name used in the issue output.

        Returns:
            Issues for unknown or malformed placeholder tokens.
        """
        issues: list[ValidationIssue] = []
        for double_match in self.config.double_brace_pattern.findall(text):
            issues.append(
                ValidationIssue(
                    field,
                    f"Placeholder '{double_match}' uses double braces; use single "
                    "braces such as {param_name} instead.",
                )
            )
        param_names = {param.name for param in self.draft.params}
        for raw_token in self.config.placeholder_pattern.findall(text):
            token = raw_token.strip()
            if not token or "{" in token or "}" in token:
                continue
            if token in param_names or token in self.config.payload_placeholders:
                continue
            issues.append(
                ValidationIssue(
                    field,
                    f"Placeholder '{{{token}}}' is not a declared parameter nor a "
                    "known payload.json key. Declare it under Parameters first.",
                )
            )
        return issues

    @staticmethod
    def _is_valid_repo_url(value: str) -> bool:
        """Return True when value is an absolute http(s) URL with a host."""
        try:
            parsed = urlparse(value)
        except ValueError:
            return False
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)


class AddonYamlRenderer:
    """Render an AddonDraft as canonical LazyAddon YAML."""

    def __init__(self, config: AddonCreatorConfig | None = None) -> None:
        """Store the configuration used for defaults.

        Args:
            config: Optional configuration override for tests.
        """
        self.config = config or AddonCreatorConfig()

    def render(self, draft: AddonDraft) -> str:
        """Return the YAML document for the draft.

        Args:
            draft: The validated form state.

        Returns:
            A YAML string ready to be written to ``lazyaddons/<name>.yaml``.
        """
        document = self.to_document(draft)
        return yaml.safe_dump(
            document,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            width=self.config.yaml_width,
        )

    def to_document(self, draft: AddonDraft) -> dict[str, object]:
        """Build the schema-ordered document mapping for the draft.

        Args:
            draft: The validated form state.

        Returns:
            A plain mapping accepted by ``yaml.safe_dump`` and by the
            CLI loader in ``lazyown.register_yaml_plugin``.
        """
        document: dict[str, object] = {
            "name": draft.name.strip(),
            "description": draft.description.strip(),
            "author": draft.author.strip() or self.config.default_author,
            "version": draft.version.strip() or self.config.default_version,
            "enabled": bool(draft.enabled),
            "os": draft.os or self.config.default_os,
        }
        if draft.triggers:
            document["trigger"] = list(draft.triggers)
        if draft.params:
            document["params"] = [param.to_dict() for param in draft.params]
        document["tool"] = self._render_tool(draft)
        document["category"] = draft.category.strip()
        if draft.module_type:
            document["module_type"] = draft.module_type
        if draft.install_type:
            document["install_type"] = draft.install_type
        return document

    def _render_tool(self, draft: AddonDraft) -> dict[str, object]:
        """Build the tool block, dropping empty optional fields."""
        tool: dict[str, object] = {
            "name": draft.tool_name.strip() or draft.name.strip(),
        }
        if draft.repo_url.strip():
            tool["repo_url"] = draft.repo_url.strip()
        if draft.install_path.strip():
            tool["install_path"] = draft.install_path.strip()
        if draft.install_command.strip():
            tool["install_command"] = draft.install_command.strip()
        if draft.execute_command.strip():
            tool["execute_command"] = draft.execute_command.strip()
        if draft.upload_file.strip():
            tool["upload_file"] = draft.upload_file.strip()
        if draft.remote_command.strip():
            tool["remote_command"] = draft.remote_command.strip()
        if draft.download_file.strip():
            tool["download_file"] = draft.download_file.strip()
        if draft.lazycommand.strip():
            tool["lazycommand"] = draft.lazycommand.strip()
        if draft.env:
            tool["env"] = list(draft.env)
        return tool


class AddonStore:
    """Path-safe, atomic persistence for addon files.

    Every operation resolves the target path against the addons
    directory and re-checks realpath containment before touching the
    filesystem. Writes go through a temp file plus ``os.replace`` so a
    crashed request can never leave a partial document behind.
    """

    def __init__(
        self,
        config: AddonCreatorConfig | None = None,
        base_dir: str | None = None,
    ) -> None:
        """Configure the store.

        Args:
            config: Optional configuration override for tests.
            base_dir: Optional absolute or relative addons directory.
                Defaults to ``lazyaddons`` below the current directory.
        """
        self.config = config or AddonCreatorConfig()
        self._base_dir = Path(base_dir or self.config.addons_dir)

    def resolve_path(self, name: str) -> Path:
        """Return the safe absolute path for a newly created addon name.

        Args:
            name: The addon name (without extension).

        Returns:
            The resolved file path inside the addons directory.

        Raises:
            AddonValidationError: When the name is not whitelisted or
                the resolved path escapes the addons directory.
        """
        return self._resolve_target(name, self.config.name_pattern)

    def resolve_existing_path(self, name: str) -> Path:
        """Return the safe absolute path for an existing addon file.

        Pre-existing addons predate the creation whitelist and may use
        uppercase letters, dots, or hyphens (for example
        ``AdaptixC2.yaml`` or ``copy-fail-CVE-2026-31431.yaml``).
        Lookups therefore validate against the looser filename pattern
        while keeping the same traversal and containment guarantees.

        Args:
            name: The addon file stem (without extension).

        Returns:
            The resolved file path inside the addons directory.

        Raises:
            AddonValidationError: When the name contains path
                separators, traversal sequences, or escapes the addons
                directory.
        """
        return self._resolve_target(name, self.config.filename_pattern)

    def _resolve_target(self, name: str, pattern: re.Pattern[str]) -> Path:
        """Build and guard a target path for a validated name.

        Args:
            name: The addon file stem (without extension).
            pattern: The pattern the name must satisfy.

        Returns:
            The resolved, containment-checked file path.

        Raises:
            AddonValidationError: When the name fails the pattern or
                the resolved path escapes the addons directory.
        """
        if not pattern.fullmatch(name):
            raise AddonValidationError([ValidationIssue("name", f"Invalid addon name '{name}'.")])
        base = self._base_dir.resolve()
        target = (base / f"{name}{self.config.file_suffix}").resolve()
        if not target.is_relative_to(base):
            raise AddonValidationError([ValidationIssue("name", "Addon path escapes the addons directory.")])
        return target

    def exists(self, name: str) -> bool:
        """Return True when an addon file already exists for the name.

        Args:
            name: The addon name to probe.
        """
        try:
            return self.resolve_path(name).is_file()
        except AddonValidationError:
            return False

    def save(self, name: str, yaml_text: str) -> Path:
        """Persist the YAML document atomically.

        The temp file is created with the store file mode from the first
        byte, so no reader can ever observe a permissive partial document.
        The write is flushed and fsynced before ``os.replace`` promotes it
        into place, and any failure removes the temp file.

        Args:
            name: The addon name (without extension).
            yaml_text: The rendered YAML document.

        Returns:
            The written file path.

        Raises:
            AddonValidationError: When the name is unsafe.
            OSError: When the write fails.
        """
        target = self.resolve_path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        self._atomic_write(target, yaml_text)
        return target

    def _atomic_write(self, target: Path, text: str) -> None:
        """Write ``text`` to ``target`` through a securely created temp file.

        Args:
            target: The final file path inside the addons directory.
            text: The content to persist.

        Raises:
            OSError: When the temp file cannot be created, written, or
                promoted.
        """
        fd, tmp_name = tempfile.mkstemp(
            dir=str(target.parent),
            prefix=f".{target.name}.",
            suffix=self.config.tmp_suffix,
        )
        try:
            os.fchmod(fd, self.config.file_mode)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, target)
        except OSError:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise

    def load(self, name: str) -> dict[str, Any]:
        """Return the parsed addon document for a name.

        Args:
            name: The addon name (without extension).

        Returns:
            The parsed YAML mapping.

        Raises:
            AddonValidationError: When the name is unsafe.
            FileNotFoundError: When the addon does not exist.
            yaml.YAMLError: When the file is not valid YAML.
            ValueError: When the document is not a mapping.
        """
        target = self.resolve_existing_path(name)
        if not target.is_file():
            raise FileNotFoundError(f"Addon '{name}' does not exist.")
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Addon '{name}' is not a mapping document.")
        return data

    def delete(self, name: str) -> bool:
        """Delete the addon file for a name.

        Args:
            name: The addon name (without extension).

        Returns:
            True when the file was removed, False when it did not exist.
        """
        target = self.resolve_existing_path(name)
        try:
            target.unlink()
        except (FileNotFoundError, IsADirectoryError):
            return False
        return True

    def list_all(self) -> list[dict[str, Any]]:
        """Return summary dicts for every parseable addon.

        Returns:
            A list sorted by display name with keys ``name``
            (declared YAML name), ``filename`` (file stem used by the
            view and delete routes), ``description``, ``category``,
            ``author``, ``os``, and ``enabled``. Broken files are
            skipped so the dashboard keeps working.
        """
        base = self._base_dir.resolve()
        if not base.is_dir():
            return []
        summaries: list[dict[str, Any]] = []
        for path in sorted(base.glob(f"*{self.config.file_suffix}")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (yaml.YAMLError, OSError):
                continue
            if not isinstance(data, dict):
                continue
            summaries.append(
                {
                    "name": str(data.get("name") or path.stem),
                    "filename": path.stem,
                    "description": str(data.get("description") or "").strip(),
                    "category": str(data.get("category") or "").strip(),
                    "author": str(data.get("author") or "").strip(),
                    "os": str(data.get("os") or self.config.default_os),
                    "enabled": bool(data.get("enabled", False)),
                }
            )
        return sorted(summaries, key=lambda item: item["name"])


def _multi_values(form: Mapping[str, Any], key: str) -> list[str]:
    """Collect every value for a repeated form key.

    Args:
        form: A Mapping that may expose ``getlist`` (Flask MultiDict).
        key: The field name.

    Returns:
        String values; empty list when absent.
    """
    getter = getattr(form, "getlist", None)
    if getter is not None:
        return [str(value) for value in getter(key)]
    value = form.get(key)
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return [str(value)]


def _first_value(form: Mapping[str, Any], key: str) -> str:
    """Return the first value for a form key or an empty string.

    Args:
        form: The form mapping.
        key: The field name.
    """
    values = _multi_values(form, key)
    return values[0] if values else ""


def parse_addon_form(form: Mapping[str, Any]) -> AddonDraft:
    """Adapt raw form data into an AddonDraft.

    Args:
        form: A mapping shaped like ``request.form``. Param rows use
            indexed keys ``params-<i>-name``, ``params-<i>-type``,
            ``params-<i>-required``, ``params-<i>-default``, and
            ``params-<i>-description``.

    Returns:
        The populated draft, ready for validation.
    """
    triggers = [trigger.strip() for trigger in _multi_values(form, "trigger") if trigger.strip()]
    env_lines = [line.strip() for line in _first_value(form, "env").splitlines() if line.strip()]
    return AddonDraft(
        name=_first_value(form, "name").strip(),
        description=_first_value(form, "description").strip(),
        author=_first_value(form, "author").strip(),
        version=_first_value(form, "version").strip(),
        enabled=_first_value(form, "enabled").strip().lower() in ("true", "1", "on", "yes"),
        os=_first_value(form, "os").strip().lower() or "any",
        triggers=triggers,
        category=_first_value(form, "category").strip(),
        module_type=_first_value(form, "module_type").strip(),
        install_type=_first_value(form, "install_type").strip(),
        params=_parse_param_rows(form),
        tool_name=_first_value(form, "tool_name").strip(),
        repo_url=_first_value(form, "repo_url").strip(),
        install_path=_first_value(form, "install_path").strip(),
        install_command=_first_value(form, "install_command").strip(),
        execute_command=_first_value(form, "execute_command").strip(),
        upload_file=_first_value(form, "upload_file").strip(),
        remote_command=_first_value(form, "remote_command").strip(),
        download_file=_first_value(form, "download_file").strip(),
        lazycommand=_first_value(form, "lazycommand").strip(),
        env=env_lines,
    )


def _parse_param_rows(form: Mapping[str, Any]) -> list[ParamSpec]:
    """Parse indexed param rows from the form mapping.

    Args:
        form: The form mapping carrying ``params-<i>-*`` keys.

    Returns:
        ParamSpec instances in index order, skipping rows whose index
        names are absent.
    """
    rows: list[ParamSpec] = []
    index = 0
    while f"params-{index}-name" in form:
        default_value = _first_value(form, f"params-{index}-default").strip()
        rows.append(
            ParamSpec(
                name=_first_value(form, f"params-{index}-name").strip(),
                type=_first_value(form, f"params-{index}-type").strip() or "string",
                required=_first_value(form, f"params-{index}-required").strip().lower() in ("true", "1", "on", "yes"),
                description=_first_value(form, f"params-{index}-description").strip(),
                default=default_value or None,
            )
        )
        index += 1
    return rows


__all__ = [
    "AddonCreatorConfig",
    "AddonDraft",
    "AddonStore",
    "AddonValidationError",
    "AddonValidator",
    "AddonYamlRenderer",
    "ParamSpec",
    "ValidationIssue",
    "parse_addon_form",
]
