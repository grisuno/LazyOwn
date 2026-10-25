# `scripts/lazy_hermes_ask.sh`

> Source: [scripts/lazy_hermes_ask.sh:1](../../scripts/lazy_hermes_ask.sh#L1) | language `sh` | coverage 100.0% | [API index](../index.md)

lazy_hermes_ask.sh — detached Hermes task runner for LazyOwn.

Usage: lazy_hermes_ask.sh [--in DIR] [--resume SESSION] <task words...> Joins all args as one query and runs: hermes chat --oneshot -Q -q <query> against the local Qwen server (provider/flags match lazy_llamacpp).
