"""Flask Blueprints for lazydown C2.

Each blueprint owns a domain area of the C2 web interface.
Registered in :func:`lazyc2.app_factory.create_app`.
"""

from lazyc2.blueprints.addons import addons_bp
from lazyc2.blueprints.api import api_bp
from lazyc2.blueprints.auth import auth_bp
from lazyc2.blueprints.operations import operations_bp
from lazyc2.blueprints.phishing import redirect_bp

__all__ = ["addons_bp", "api_bp", "auth_bp", "operations_bp", "redirect_bp"]
