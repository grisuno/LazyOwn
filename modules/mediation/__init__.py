"""Mediation layer for LazyOwn cross-module coordination.

Colleagues never import each other directly: they depend on the
``contracts`` abstractions here and each specialised mediator owns
exactly one coordination concern. The hub routes requests by domain
key so callers stay ignorant of concrete peers.
"""

from __future__ import annotations

from modules.mediation.chain_mediator import ChainMediator
from modules.mediation.contracts import (
    MediationDomains,
    MediationHubContract,
    MediatorContract,
    resolve,
)
from modules.mediation.feedback_mediator import FeedbackMediator
from modules.mediation.hub import MediationHub, default_hub, get_hub
from modules.mediation.intel_mediator import IntelMediator
from modules.mediation.telemetry_mediator import TelemetryMediator

__all__ = [
    "ChainMediator",
    "FeedbackMediator",
    "IntelMediator",
    "MediationDomains",
    "MediationHub",
    "MediationHubContract",
    "MediatorContract",
    "TelemetryMediator",
    "default_hub",
    "get_hub",
    "resolve",
]
