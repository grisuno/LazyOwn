"""Security constants and validation patterns for the LazyOwn C2 web layer.

All regex patterns, length limits, and allowlists are defined here
to ensure single-source-of-truth and eliminate magic numbers.
"""

import re

ROUTE_PATH_PATTERN = re.compile(r'^[a-zA-Z0-9/_-]+$')
TEMPLATE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+\.html$')
YAML_FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+\.(yaml|yml)$')

MAX_ROUTE_PATH_LENGTH = 128
MAX_TEMPLATE_NAME_LENGTH = 128
MAX_REQUEST_DATA_LENGTH = 2000
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024
AES_KEY_SIZE_BYTES = 32
MINIMUM_PASSWORD_LENGTH = 12

ALLOWED_HTML_TAGS = (
    'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'code', 'pre', 'a', 'h1',
    'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'hr', 'table', 'thead',
    'tbody', 'tr', 'td', 'th'
)
ALLOWED_HTML_ATTRIBUTES = {
    'a': ['href', 'title'],
    '*': ['class']
}

SESSIONS_DIR_NAME = 'sessions'
TEMPLATES_DIR_NAME = 'templates'
UPLOADS_DIR_NAME = 'uploads'
TEMP_UPLOADS_DIR_NAME = 'temp_uploads'

FILE_PERMISSION_OWNER_RW = 0o600
DIR_PERMISSION_OWNER_RWX = 0o700

MAX_YAML_FILE_SIZE_BYTES = 10 * 1024 * 1024
