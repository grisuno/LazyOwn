"""Tests for the graphical sudo askpass helpers."""

from __future__ import annotations

import pytest

import modules.askpass as askpass


def test_find_native_askpass_without_display_is_empty(monkeypatch):
    monkeypatch.delenv("DISPLAY", raising=False)
    monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)
    monkeypatch.delenv("LAZYOWN_ASKPASS", raising=False)
    assert askpass.graphical_askpass_path() == ""


def test_find_native_askpass_uses_installed_helper(monkeypatch, tmp_path):
    monkeypatch.setenv("DISPLAY", ":0")
    helper = tmp_path / "ksshaskpass"
    helper.write_text("#!/bin/sh\n")
    helper.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path))
    assert askpass.find_native_askpass() == str(helper)


def test_create_zenity_askpass_writes_helper(monkeypatch, tmp_path):
    monkeypatch.setenv("DISPLAY", ":0")
    monkeypatch.setenv("PATH", str(tmp_path))
    zenity = tmp_path / "zenity"
    zenity.write_text("#!/bin/sh\n")
    zenity.chmod(0o755)
    path = askpass.create_zenity_askpass()
    assert path.endswith("askpass.sh")
    text = open(path).read()
    assert "zenity" in text and "--hide-text" in text


def test_sudo_graphical_requested_defaults_on(monkeypatch):
    monkeypatch.delenv("LAZYOWN_AUTONOMOUS", raising=False)
    monkeypatch.delenv("LAZYOWN_SUDO_GRAPHICAL", raising=False)
    assert askpass.sudo_graphical_requested({}) is True
    assert askpass.sudo_graphical_requested({"sudo_graphical": False}) is False


def test_sudo_graphical_requested_off_in_autonomous_loop(monkeypatch):
    monkeypatch.setenv("LAZYOWN_AUTONOMOUS", "1")
    assert askpass.sudo_graphical_requested({}) is False
