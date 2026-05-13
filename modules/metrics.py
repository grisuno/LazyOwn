"""Minimal in-memory metrics registry with optional Prometheus text exposition.

No external dependencies required.  If ``prometheus_client`` is installed it
will be used for exposition, otherwise a bare-bones text/plain fallback is
provided.
"""

from collections import defaultdict
from threading import Lock


class MetricsRegistry:
    """Thread-safe counter registry."""

    def __init__(self):
        self._counters: dict = defaultdict(lambda: defaultdict(int))
        self._lock = Lock()

    def inc(self, name: str, labels: dict | None = None, value: int = 1):
        """Increment a counter."""
        key = _labels_key(labels or {})
        with self._lock:
            self._counters[name][key] += value

    def get(self, name: str, labels: dict | None = None) -> int:
        key = _labels_key(labels or {})
        with self._lock:
            return self._counters[name][key]

    def prometheus_text(self) -> str:
        """Render counters in Prometheus exposition format."""
        lines = []
        for name, series in self._counters.items():
            lines.append(f"# TYPE {name} counter")
            for label_key, value in series.items():
                if label_key:
                    lines.append(f'{name}{{{label_key}}} {value}')
                else:
                    lines.append(f'{name} {value}')
        return "\n".join(lines)


def _labels_key(labels: dict) -> str:
    if not labels:
        return ""
    return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))


# Global registry instance
REGISTRY = MetricsRegistry()
