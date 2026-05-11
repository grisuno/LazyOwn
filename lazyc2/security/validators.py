"""Input validators for the LazyOwn C2 web layer.

All validation functions are pure, stateless, and operate only on
primitive types. They return ``(bool, str)`` tuples to enable
detailed error messages without raising exceptions.
"""

from pathlib import Path

from lazyc2.security.constants import (
    AES_KEY_SIZE_BYTES,
    MAX_REQUEST_DATA_LENGTH,
    MAX_ROUTE_PATH_LENGTH,
    MAX_TEMPLATE_NAME_LENGTH,
    MAX_UPLOAD_SIZE_BYTES,
    MINIMUM_PASSWORD_LENGTH,
    ROUTE_PATH_PATTERN,
    TEMPLATE_NAME_PATTERN,
    YAML_FILENAME_PATTERN,
)


def validate_route_path(route_path: str) -> tuple[bool, str]:
    """Validate a dynamic route path segment.

    Args:
        route_path: The route path to validate.

    Returns:
        A tuple of (is_valid, error_message).
    """
    if not route_path:
        return False, "Route path is empty"
    if len(route_path) > MAX_ROUTE_PATH_LENGTH:
        return False, f"Route path exceeds {MAX_ROUTE_PATH_LENGTH} characters"
    if route_path.startswith('.') or route_path.startswith('/'):
        return False, "Route path must not start with '.' or '/'"
    if '..' in route_path:
        return False, "Route path contains path traversal sequence"
    if not ROUTE_PATH_PATTERN.match(route_path):
        return False, "Route path contains invalid characters"
    return True, ""


def validate_template_name(template_name: str) -> tuple[bool, str]:
    """Validate a Jinja2 template filename.

    Args:
        template_name: The template name to validate.

    Returns:
        A tuple of (is_valid, error_message).
    """
    if not template_name:
        return False, "Template name is empty"
    if len(template_name) > MAX_TEMPLATE_NAME_LENGTH:
        return False, f"Template name exceeds {MAX_TEMPLATE_NAME_LENGTH} characters"
    if not template_name.endswith('.html'):
        return False, "Template name must end with '.html'"
    if '..' in template_name or '/' in template_name or '\\' in template_name:
        return False, "Template name contains path separators"
    if not TEMPLATE_NAME_PATTERN.match(template_name):
        return False, "Template name contains invalid characters"
    return True, ""


def validate_yaml_filename(filename: str) -> tuple[bool, str]:
    """Validate a YAML filename for safe loading.

    Args:
        filename: The filename to validate.

    Returns:
        A tuple of (is_valid, error_message).
    """
    if not filename:
        return False, "Filename is empty"
    if '..' in filename or '/' in filename or '\\' in filename:
        return False, "Filename contains path separators"
    if not YAML_FILENAME_PATTERN.match(filename):
        return False, "Filename must end with '.yaml' or '.yml'"
    return True, ""


def validate_request_data(data: str) -> tuple[bool, str]:
    """Validate request data length to prevent buffer abuse.

    Args:
        data: The data string to validate.

    Returns:
        A tuple of (is_valid, error_message).
    """
    if not isinstance(data, str):
        return False, "Data must be a string"
    if len(data) > MAX_REQUEST_DATA_LENGTH:
        return False, f"Data exceeds {MAX_REQUEST_DATA_LENGTH} characters"
    return True, ""


def validate_aes_key(key: bytes) -> tuple[bool, str]:
    """Validate AES key length.

    Args:
        key: The AES key bytes to validate.

    Returns:
        A tuple of (is_valid, error_message).
    """
    if not isinstance(key, bytes):
        return False, "Key must be bytes"
    if len(key) != AES_KEY_SIZE_BYTES:
        return False, f"Key must be exactly {AES_KEY_SIZE_BYTES} bytes, got {len(key)}"
    return True, ""


def validate_password_length(password: str) -> tuple[bool, str]:
    """Validate password meets minimum length requirement.

    Args:
        password: The password to validate.

    Returns:
        A tuple of (is_valid, error_message).
    """
    if not isinstance(password, str):
        return False, "Password must be a string"
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return False, f"Password must be at least {MINIMUM_PASSWORD_LENGTH} characters"
    return True, ""


def validate_upload_size(content_length: int | None) -> tuple[bool, str]:
    """Validate upload size against maximum allowed.

    Args:
        content_length: The content length header value.

    Returns:
        A tuple of (is_valid, error_message).
    """
    if content_length is None:
        return True, ""
    if content_length > MAX_UPLOAD_SIZE_BYTES:
        return False, f"Upload exceeds {MAX_UPLOAD_SIZE_BYTES} bytes"
    return True, ""


def validate_file_path_within_base(file_path: Path, base_dir: Path) -> tuple[bool, str]:
    """Validate that a resolved file path is within a base directory.

    Uses Path.resolve() to canonicalize paths and Path.relative_to()
    to detect traversal. This is safer than string-based checks.

    Args:
        file_path: The path to validate (may contain traversal).
        base_dir: The allowed base directory.

    Returns:
        A tuple of (is_valid, error_message).
    """
    try:
        resolved_path = file_path.resolve()
        resolved_base = base_dir.resolve()
        resolved_path.relative_to(resolved_base)
        return True, ""
    except (ValueError, RuntimeError):
        return False, "File path is outside allowed directory"
    except OSError:
        return False, "Invalid file path"
