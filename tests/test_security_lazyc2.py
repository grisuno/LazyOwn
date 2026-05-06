"""Security tests for the LazyOwn C2 web layer.

Validates path traversal resistance, input sanitization, secret management,
and content security policies using pytest.
"""

import os
import tempfile
from pathlib import Path

import pytest

from lazyc2.security import constants
from lazyc2.security.validators import (
    validate_route_path,
    validate_template_name,
    validate_yaml_filename,
    validate_request_data,
    validate_aes_key,
    validate_password_length,
    validate_upload_size,
    validate_file_path_within_base,
)
from lazyc2.security.services import (
    SecretKeyManager,
    SafeFileService,
    AESKeyManager,
    UploadSizeValidator,
)


class TestRoutePathValidator:
    """Validate route path sanitization."""

    @pytest.mark.parametrize(
        "route_path,expected_valid",
        [
            ("api/v1/users", True),
            ("hello-world", True),
            ("test_123", True),
            ("", False),
            ("../etc/passwd", False),
            ("../../config.json", False),
            ("./hidden", False),
            ("/absolute", False),
            ("api<v1>", False),
            ("api%20test", False),
            ("a" * 129, False),
            ("a" * 128, True),
        ],
    )
    def test_route_path_validation(self, route_path: str, expected_valid: bool):
        is_valid, error = validate_route_path(route_path)
        assert is_valid == expected_valid, f"Failed for {route_path}: {error}"


class TestTemplateNameValidator:
    """Validate Jinja2 template name sanitization."""

    @pytest.mark.parametrize(
        "template_name,expected_valid",
        [
            ("index.html", True),
            ("phishing/login.html", False),
            ("../etc/passwd", False),
            ("decoy.html", True),
            ("test_123.html", True),
            ("", False),
            ("file.txt", False),
            ("a" * 129, False),
            ("normal.html", True),
            ("template.html", True),
        ],
    )
    def test_template_name_validation(self, template_name: str, expected_valid: bool):
        is_valid, error = validate_template_name(template_name)
        assert is_valid == expected_valid, f"Failed for {template_name}: {error}"


class TestYamlFilenameValidator:
    """Validate YAML filename sanitization."""

    @pytest.mark.parametrize(
        "filename,expected_valid",
        [
            ("test.yaml", True),
            ("test.yml", True),
            ("../etc/passwd", False),
            ("config.json", False),
            ("", False),
            ("phishing/email.yaml", False),
            ("a" * 100 + ".yaml", True),
        ],
    )
    def test_yaml_filename_validation(self, filename: str, expected_valid: bool):
        is_valid, error = validate_yaml_filename(filename)
        assert is_valid == expected_valid, f"Failed for {filename}: {error}"


class TestRequestDataValidator:
    """Validate request data length constraints."""

    def test_short_data_is_valid(self):
        is_valid, error = validate_request_data("short data")
        assert is_valid is True
        assert error == ""

    def test_exact_max_length_is_valid(self):
        data = "x" * constants.MAX_REQUEST_DATA_LENGTH
        is_valid, error = validate_request_data(data)
        assert is_valid is True

    def test_over_max_length_is_invalid(self):
        data = "x" * (constants.MAX_REQUEST_DATA_LENGTH + 1)
        is_valid, error = validate_request_data(data)
        assert is_valid is False
        assert "exceeds" in error

    def test_non_string_is_invalid(self):
        is_valid, error = validate_request_data(12345)
        assert is_valid is False


class TestAESKeyValidator:
    """Validate AES key length enforcement."""

    def test_valid_32_byte_key(self):
        key = os.urandom(constants.AES_KEY_SIZE_BYTES)
        is_valid, error = validate_aes_key(key)
        assert is_valid is True
        assert error == ""

    def test_invalid_16_byte_key(self):
        key = os.urandom(16)
        is_valid, error = validate_aes_key(key)
        assert is_valid is False

    def test_invalid_string_key(self):
        is_valid, error = validate_aes_key("not bytes")
        assert is_valid is False

    def test_empty_key_is_invalid(self):
        is_valid, error = validate_aes_key(b"")
        assert is_valid is False


class TestPasswordLengthValidator:
    """Validate password minimum length enforcement."""

    def test_exact_minimum_length(self):
        password = "a" * constants.MINIMUM_PASSWORD_LENGTH
        is_valid, error = validate_password_length(password)
        assert is_valid is True

    def test_below_minimum_length(self):
        password = "a" * (constants.MINIMUM_PASSWORD_LENGTH - 1)
        is_valid, error = validate_password_length(password)
        assert is_valid is False

    def test_non_string_password(self):
        is_valid, error = validate_password_length(123456789012)
        assert is_valid is False


class TestUploadSizeValidator:
    """Validate upload size constraints."""

    def test_none_content_length(self):
        is_valid, error = validate_upload_size(None)
        assert is_valid is True

    def test_valid_size(self):
        is_valid, error = validate_upload_size(1024)
        assert is_valid is True

    def test_exceeds_max(self):
        is_valid, error = validate_upload_size(constants.MAX_UPLOAD_SIZE_BYTES + 1)
        assert is_valid is False

    def test_exact_max(self):
        is_valid, error = validate_upload_size(constants.MAX_UPLOAD_SIZE_BYTES)
        assert is_valid is True


class TestFilePathWithinBaseValidator:
    """Validate path traversal resistance using Path.resolve()."""

    def test_normal_path_is_valid(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        file_path = base / "subdir" / "file.txt"
        is_valid, error = validate_file_path_within_base(file_path, base)
        assert is_valid is True

    def test_traversal_outside_base_is_invalid(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        evil_path = tmp_path / "secret.txt"
        evil_path.write_text("secret")
        traversal_path = base / ".." / "secret.txt"
        is_valid, error = validate_file_path_within_base(traversal_path, base)
        assert is_valid is False

    def test_traversal_with_dotdot_is_invalid(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        traversal_path = base / ".." / ".." / "etc" / "passwd"
        is_valid, error = validate_file_path_within_base(traversal_path, base)
        assert is_valid is False

    def test_symlink_traversal_is_detected(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        secret_file = tmp_path / "secret.txt"
        secret_file.write_text("secret")
        symlink = base / "link"
        symlink.symlink_to(secret_file)
        is_valid, error = validate_file_path_within_base(symlink, base)
        assert is_valid is False


class TestSecretKeyManager:
    """Validate secret key generation and persistence."""

    def test_generates_new_key_on_first_run(self, tmp_path: Path):
        manager = SecretKeyManager(tmp_path)
        key = manager.get_or_create()
        assert len(key) == SecretKeyManager.KEY_SIZE_BYTES * 2
        assert all(c in "0123456789abcdef" for c in key)

    def test_reuses_existing_key(self, tmp_path: Path):
        manager = SecretKeyManager(tmp_path)
        key1 = manager.get_or_create()
        key2 = manager.get_or_create()
        assert key1 == key2

    def test_key_file_has_restrictive_permissions(self, tmp_path: Path):
        manager = SecretKeyManager(tmp_path)
        manager.get_or_create()
        key_file = tmp_path / SecretKeyManager.KEY_FILENAME
        mode = key_file.stat().st_mode
        assert mode & 0o777 == constants.FILE_PERMISSION_OWNER_RW


class TestSafeFileService:
    """Validate safe file operations with path traversal protection."""

    def test_read_bytes_within_base(self, tmp_path: Path):
        base = tmp_path / "safe"
        base.mkdir()
        target = base / "test.txt"
        target.write_text("hello")
        service = SafeFileService(base)
        data = service.read_bytes("test.txt")
        assert data == b"hello"

    def test_read_bytes_traversal_raises(self, tmp_path: Path):
        base = tmp_path / "safe"
        base.mkdir()
        outside = tmp_path / "secret.txt"
        outside.write_text("secret")
        service = SafeFileService(base)
        with pytest.raises(PermissionError):
            service.read_bytes("../secret.txt")

    def test_write_bytes_creates_file(self, tmp_path: Path):
        base = tmp_path / "safe"
        base.mkdir()
        service = SafeFileService(base)
        service.write_bytes("subdir/file.txt", b"data")
        assert (base / "subdir" / "file.txt").read_bytes() == b"data"

    def test_exists_returns_true_for_valid_path(self, tmp_path: Path):
        base = tmp_path / "safe"
        base.mkdir()
        (base / "file.txt").write_text("hello")
        service = SafeFileService(base)
        assert service.exists("file.txt") is True

    def test_exists_returns_false_for_missing(self, tmp_path: Path):
        base = tmp_path / "safe"
        base.mkdir()
        service = SafeFileService(base)
        assert service.exists("missing.txt") is False

    def test_exists_traversal_raises(self, tmp_path: Path):
        base = tmp_path / "safe"
        base.mkdir()
        service = SafeFileService(base)
        with pytest.raises(PermissionError):
            service.exists("../secret.txt")


class TestAESKeyManager:
    """Validate AES key generation and validation."""

    def test_generates_new_key(self, tmp_path: Path):
        key_file = tmp_path / "key.aes"
        manager = AESKeyManager(key_file)
        key = manager.get_or_generate()
        assert len(key) == constants.AES_KEY_SIZE_BYTES

    def test_reuses_existing_valid_key(self, tmp_path: Path):
        key_file = tmp_path / "key.aes"
        key_file.write_bytes(os.urandom(constants.AES_KEY_SIZE_BYTES))
        manager = AESKeyManager(key_file)
        key = manager.get_or_generate()
        assert key == key_file.read_bytes()

    def test_raises_on_invalid_existing_key(self, tmp_path: Path):
        key_file = tmp_path / "key.aes"
        key_file.write_bytes(b"short")
        manager = AESKeyManager(key_file)
        with pytest.raises(ValueError, match="exactly"):
            manager.get_or_generate()


class TestUploadSizeValidatorService:
    """Validate upload size service."""

    def test_valid_size_passes(self):
        validator = UploadSizeValidator(max_size_bytes=1024)
        validator.validate(512)

    def test_exact_max_passes(self):
        validator = UploadSizeValidator(max_size_bytes=1024)
        validator.validate(1024)

    def test_exceeds_max_raises(self):
        validator = UploadSizeValidator(max_size_bytes=1024)
        with pytest.raises(ValueError, match="exceeds"):
            validator.validate(1025)

    def test_none_passes(self):
        validator = UploadSizeValidator(max_size_bytes=1024)
        validator.validate(None)
