"""Beacon domain contracts for the LazyOwn C2 server.

The package owns the on-disk state shared by the C2 routes, the CLI and the
loop: command queue, result history and malleable recon markers. Import the
public surface from here so route modules never reach into private helpers.
"""

from lazyc2.beacons.store import BeaconPathError, BeaconStore
from lazyc2.beacons.service import BeaconRuntime

__all__ = ["BeaconPathError", "BeaconRuntime", "BeaconStore"]
