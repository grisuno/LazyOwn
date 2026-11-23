# modules.c2_channels

Operator chat platforms (telegram/discord/slack) as C2 transports.

## Contract

- Transport-only: `send(text) -> bool` and `poll() -> list[C2Message]`
  (`core.protocols.C2Channel`). Command execution lives with the
  injected executor strategy, never inside a channel.
- Credentials come from `payload.json`; a channel without them reports
  `configured=False` and fails soft (no raises on the poll loop).
- Gating: `enable_<name>_c2` payload keys (`enable_telegram_c2`,
  `enable_discord_c2`, `enable_slack_c2`).
- Poll cursors (telegram update offset, discord message id, slack ts)
  stay in memory per channel instance.

## Files

| File | Purpose |
|------|---------|
| `base.py` | `HttpC2Channel` wire I/O, poll rate limit, fail-soft contract. |
| `telegram.py` | Bot API `sendMessage` / `getUpdates`. |
| `discord.py` | Webhook or bot REST send; `channels/<id>/messages` polling. |
| `slack.py` | `chat.postMessage`; `conversations.history` polling. |
| `registry.py` | Factory registry, `enabled_channels`, `create_enabled`. |

## Payload keys

| Key | Purpose |
|-----|---------|
| `enable_telegram_c2` / `telegram_token` / `telegram_chat_id` | Telegram channel. |
| `enable_discord_c2` / `discord_token` / `discord_channel_id` / `discord_webhook` | Discord channel. |
| `enable_slack_c2` / `slack_bot_token` / `slack_channel_id` | Slack channel. |

The standalone bots (`telegram_c2.py`, `discord_c2.py`,
`slack_c2_bot.py`) predate this package and own their own session
managers; they remain the interactive reference implementations.
