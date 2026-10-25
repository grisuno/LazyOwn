# `scripts/pi_qwen_setup.sh`

> Source: [scripts/pi_qwen_setup.sh:1](../../scripts/pi_qwen_setup.sh#L1) | language `sh` | coverage 100.0% | [API index](../index.md)

pi_qwen_setup.sh - idempotent bootstrap for the pi_qwen lazyaddon.

Ensures the pi CLI is installed and registers the local llama.cpp Qwen endpoint as the "local-qwen" provider in Pi models.json, preserving any existing providers. Safe to run on every invocation.  Usage: pi_qwen_setup.sh [base_url] [model_id]  Base URL defaults to the LazyOwn llama.cpp server. Model ID defaults to the alias that server exposes (local-model).
