"""Compatibility shim for legacy ``python setup.py`` invocations.

All project metadata and dependencies are declared in ``pyproject.toml`` under
``[project]`` and are the single source of truth. Modern setuptools reads them
from there, so this file intentionally carries no duplicated package list; it
exists only so tooling that still shells out to ``setup.py`` keeps working.
"""

from setuptools import setup

setup()
