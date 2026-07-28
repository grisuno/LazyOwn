import re
import time
from typing import Any, Dict, Optional


MAX_FAILED_ATTEMPTS = 3
RATE_LIMIT = 5
SESSION_TIMEOUT = 1800


from core.parsers import strip_ansi


class SecureSessionManager:
    """Unified session manager for C2 messaging bots.

    Provides login, rate limiting, lockout, and session validation
    shared across Discord, Telegram, and Slack C2 bots.

    Args:
        max_failed_attempts: Maximum failed login attempts before lockout.
        lockout_duration: Lockout duration in seconds.
        rate_limit: Maximum commands per 60-second window.
        session_timeout: Session inactivity timeout in seconds.
    """

    def __init__(
        self,
        max_failed_attempts: int = MAX_FAILED_ATTEMPTS,
        lockout_duration: int = 3600,
        rate_limit: int = RATE_LIMIT,
        session_timeout: int = SESSION_TIMEOUT,
    ):
        self.max_failed_attempts = max_failed_attempts
        self.lockout_duration = lockout_duration
        self._rate_limit = rate_limit
        self._session_timeout = session_timeout
        self.sessions: Dict[int, Dict[str, Any]] = {}
        self.failed_attempts: Dict[int, Dict[str, Any]] = {}
        self.command_timestamps: Dict[int, list] = {}

    def register_failed_attempt(self, user_id: int) -> None:
        """Record a failed authentication attempt for a user."""
        now = time.time()
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = {'count': 1, 'timestamp': now}
        else:
            self.failed_attempts[user_id]['count'] += 1
            self.failed_attempts[user_id]['timestamp'] = now

    def check_lockout(self, user_id: int) -> bool:
        """Check if a user is currently locked out due to failed attempts.

        Returns:
            bool: True if locked out, False otherwise.
        """
        attempt = self.failed_attempts.get(user_id)
        if not attempt:
            return False
        if attempt['count'] >= self.max_failed_attempts:
            if (time.time() - attempt['timestamp']) < self.lockout_duration:
                return True
            del self.failed_attempts[user_id]
        return False

    def check_rate_limit(self, user_id: int) -> bool:
        """Check if a user has exceeded the command rate limit.

        Returns:
            bool: True if allowed, False if rate-limited.
        """
        now = time.time()
        if user_id not in self.command_timestamps:
            self.command_timestamps[user_id] = []

        self.command_timestamps[user_id] = [
            t for t in self.command_timestamps[user_id] if now - t < 60
        ]

        if len(self.command_timestamps[user_id]) >= self._rate_limit:
            return False

        self.command_timestamps[user_id].append(now)
        return True

    def create_session(self, user_id: int, client_id: Optional[str] = None) -> None:
        """Create a new authenticated session for a user."""
        now = time.time()
        self.sessions[user_id] = {
            'user_id': user_id,
            'client_id': client_id,
            'session_start': now,
            'last_activity': now,
        }

    def validate_session(self, user_id: int) -> bool:
        """Check if a user session is still valid and refresh activity timestamp.

        Returns:
            bool: True if session is valid, False otherwise.
        """
        session = self.sessions.get(user_id)
        if not session:
            return False

        if (time.time() - session['last_activity']) > self._session_timeout:
            del self.sessions[user_id]
            return False

        session['last_activity'] = time.time()
        return True

    def set_client(self, user_id: int, client_id: str) -> None:
        """Assign a target C2 client to a user session."""
        if user_id in self.sessions:
            self.sessions[user_id]['client_id'] = client_id

    def get_client(self, user_id: int) -> Optional[str]:
        """Get the target C2 client assigned to a user session."""
        session = self.sessions.get(user_id)
        return session.get('client_id') if session else None


class PayloadConfigAdapter:
    """Adapter that wraps payload.json dict with attribute access.

    Args:
        config_dict: The loaded payload.json dictionary.
    """

    def __init__(self, config_dict: Dict[str, Any]):
        self._config = config_dict
        for key, value in config_dict.items():
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)
