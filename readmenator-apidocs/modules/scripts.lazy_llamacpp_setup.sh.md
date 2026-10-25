# `scripts/lazy_llamacpp_setup.sh`

> Source: [scripts/lazy_llamacpp_setup.sh:1](../../scripts/lazy_llamacpp_setup.sh#L1) | language `sh` | coverage 50.0% | [API index](../index.md)

lazy_llamacpp_setup.sh — one-time local LLM setup for LazyOwn users.

Interactively (or via flags) it: 1. builds llama.cpp from the lazy_llamacpp addon clone (CUDA when present), 2. downloads the Qwen 27B GGUF model (~8GB, asks first), 3. starts the server through lazy_llamacpp_serve.sh, 4. optionally patches opencode (~/.config/opencode/opencode.json), 5. optionally patches hermes (~/.hermes/config.yaml), 6. optionally sets payload.json local_llm so fast_run uses it.  Flags (all default to asking): --yes            accept every default without prompting --no-download    skip the model download (reuse existing models/*.gguf) --no-opencode    skip opencode config patch --no-hermes      skip hermes config patch --no-payload     skip payload.json local_llm change  The operator's existing setup is never touched without an explicit yes.

## Contents

- **Functions:** [`ask`](#ask)

## Functions

<a id="ask"></a>

### `ask`

`function` | [scripts/lazy_llamacpp_setup.sh:40](../../scripts/lazy_llamacpp_setup.sh#L40)

```bash
ask()
```

---
