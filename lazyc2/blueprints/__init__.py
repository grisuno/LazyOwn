"""Flask Blueprints for lazydown C2.

Each blueprint owns a domain area of the C2 web interface.
Registered in :func:`lazyc2.app_factory.create_app`.
"""

from lazyc2.blueprints.api import api_bp
from lazyc2.blueprints.phishing import phishing_bp

__all__ = ["api_bp", "phishing_bp"]
