# `scripts/lazy_llamacpp_serve.sh`

> Source: [scripts/lazy_llamacpp_serve.sh:1](../../scripts/lazy_llamacpp_serve.sh#L1) | language `sh` | coverage 50.0% | [API index](../index.md)

lazy_llamacpp_serve.sh — idempotent llama.cpp server manager for LazyOwn.

Usage: lazy_llamacpp_serve.sh           # ensure server up, print endpoint + status lazy_llamacpp_serve.sh status    # health check only (exit 0/1) lazy_llamacpp_serve.sh stop      # stop the server started from this repo  Env overrides: LLAMACPP_HOST (default 127.0.0.1), LLAMACPP_PORT (8080), LLAMACPP_MODEL (gguf path), LLAMACPP_NGL (auto: 26 with NVIDIA GPU else 0), LLAMACPP_THREADS (default 8), LLAMACPP_CTX (default 65536).  Non-interactive: safe for addon execute_command and fast_run panes.

## Contents

- **Functions:** [`healthy`](#healthy)

## Functions

<a id="healthy"></a>

### `healthy`

`function` | [scripts/lazy_llamacpp_serve.sh:33](../../scripts/lazy_llamacpp_serve.sh#L33)

```bash
healthy()
```

---
