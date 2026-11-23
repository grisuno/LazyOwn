"""Contract tests for the C2 channel plugins.

Covers the registry (dedup, gating, fail-soft construction), the
transport base (rate limit, error swallowing) and one adapter's request
shape with an injected fake transport.
"""

from __future__ import annotations

import pytest

from core.protocols import C2Channel, C2Message


class TestRegistry:
    def test_defaults_registered(self) -> None:
        from modules.c2_channels import registry

        assert registry.available_channels() == ("discord", "slack", "telegram")

    def test_duplicate_registration_rejected(self) -> None:
        from modules.c2_channels import registry

        def factory(config):
            return None

        with pytest.raises(ValueError):
            registry.register_channel("telegram", factory)

    def test_enabled_channels_gate_on_payload_keys(self) -> None:
        from modules.c2_channels import registry

        assert registry.enabled_channels({"enable_telegram_c2": True, "enable_slack_c2": True}) == [
            "slack",
            "telegram",
        ]
        assert registry.enabled_channels({}) == []

    def test_create_channel_unknown_returns_none(self) -> None:
        from modules.c2_channels import registry

        assert registry.create_channel("carrier-pigeon", {}) is None

    def test_create_enabled_returns_configured_instances(self) -> None:
        from modules.c2_channels import registry

        config = {"enable_telegram_c2": True, "telegram_token": "t", "telegram_chat_id": "c"}
        channels = registry.create_enabled(config)
        assert len(channels) == 1
        channel = channels[0]
        assert isinstance(channel, C2Channel)
        assert channel.name == "telegram"
        assert channel.configured is True

    def test_disabled_channels_not_created(self) -> None:
        from modules.c2_channels import registry

        assert registry.create_enabled({}) == []


class TestTransportBase:
    def _channel(self, **overrides):
        from tests._c2_channel_fakes import FakeOkTransport

        return FakeOkTransport({"telegram_token": "tok", "telegram_chat_id": "chat"}, **overrides)

    def test_poll_rate_limited(self) -> None:
        from tests._c2_channel_fakes import advance

        channel = self._channel()
        first = channel.poll()
        advance(channel)
        second = channel.poll()
        assert first == second == []
        channel.transport.inject_message("u1", "whoami")
        advance(channel, force=True)
        messages = channel.poll()
        assert len(messages) == 1
        assert isinstance(messages[0], C2Message)

    def test_send_success(self) -> None:
        from tests._c2_channel_fakes import advance

        channel = self._channel()
        assert channel.send("hello") is True
        assert channel.transport.sent == ["hello"]
        assert channel.poll() == []
        advance(channel, force=True)
        assert channel.poll() == []

    def test_send_fail_soft_on_transport_error(self) -> None:
        from tests._c2_channel_fakes import FakeExplodingTransport

        channel = FakeExplodingTransport({"telegram_token": "t", "telegram_chat_id": "c"})
        assert channel.send("boom") is False
        assert channel.poll() == []

    def test_unconfigured_channel_fails_soft(self) -> None:
        from tests._c2_channel_fakes import FakeOkTransport

        channel = FakeOkTransport({})
        assert channel.configured is False
        assert channel.send("x") is False
        assert channel.poll() == []

    def test_blank_send_rejected(self) -> None:
        from tests._c2_channel_fakes import FakeOkTransport

        channel = FakeOkTransport({"telegram_token": "t", "telegram_chat_id": "c"})
        assert channel.send("   ") is False


class TestProtocolConformance:
    def test_channel_satisfies_protocol(self) -> None:
        from tests._c2_channel_fakes import FakeOkTransport

        assert isinstance(FakeOkTransport({"telegram_token": "t", "telegram_chat_id": "c"}), C2Channel)


class TestTelegramRequests:
    def test_send_and_poll_urls(self) -> None:
        from tests._c2_channel_fakes import FakeOkTransport, advance

        channel = FakeOkTransport({"telegram_token": "tok", "telegram_chat_id": "42"})
        channel.send("hi")
        assert channel.transport.calls["send_url"].endswith("/bottok/sendMessage")
        advance(channel, force=True)
        channel.transport.inject_message("77", "issue_command_to_c2 id")
        advance(channel, force=True)
        messages = channel.poll()
        assert messages[0].text == "issue_command_to_c2 id"
        assert channel.transport.calls["poll_url"].endswith("/bottok/getUpdates")
        assert channel.transport.poll_params["offset"] == 1
        advance(channel, force=True)
        messages = channel.poll()
        assert channel.transport.poll_params["offset"] == 2
        assert messages == []
