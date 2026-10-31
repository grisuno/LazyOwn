"""Exposure command-set discovery: the five lazy intel surfaces register."""

from __future__ import annotations

from cli.registry import iter_command_sets


class TestExposureSetDiscovery:
    def test_five_new_sets_discovered(self):
        story = "sentinel, autofire, timeline, intelops and lazyintel must ride the auto-registry"
        names = {command_set.__name__ for command_set in iter_command_sets()}
        expected = {
            "SentinelCommandSet",
            "AutoFireCommandSet",
            "TimelineCommandSet",
            "IntelOpsCommandSet",
            "LazyIntelCommandSet",
        }
        assert expected <= names, story
