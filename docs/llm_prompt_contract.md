# LLM Prompt/Knowledge-Layer Contract

Single-source contract for the LLM provider selection, prompt-template and
knowledge-base layer. Cross-cutting reference in `CLAUDE.md` §16a.1.
DoD gate listed at the end.

## Goal

One provider-agnostic source of truth for every AI assistant: `payload.json`
keys (`llm_backend`, per-provider `llm_model_*`, per-provider API key slots,
`ollama_host`) resolved exclusively through `modules.llm_factory`. No Groq
lock-in — Groq degradation no longer affects operators on other providers.

## Files

| File | Role |
|------|------|
| `modules/llm_factory.py` | Canonical factory + backend metadata (`default_model_for`, `model_config_key`, `api_key_config_key`, `backend_requires_api_key`). Only module that knows backend defaults, model slots and key slots. |
| `modules/llm_prompts.py` | Canonical prompt templates + KB CRUD/relevance + payload/event/report context + `DEFAULT_SYSTEM_PROMPT`. Pure module: no vendor SDK, no network, no direct `os.environ` reads. |
| `modules/llm_adapter.py` | Groq `process_prompt_*` facade (legacy parity for the C2 dashboard) plus `ask_general`: the provider-agnostic entry every bot uses (factory backend + canonical general template + KB persistence). MUST NOT import `modules.legacy.lazygptcli*`. |
| `core/payload_schema.py` | Typed specs for `llm_backend` (enum-validated), `llm_model_*`, `openai_api_key`, `anthropic_api_key`, `deepseek_api_key`, `ollama_host`. Makes every key `assign`-able and validated. |
| `cli/wizard.py` | Step 6 asks provider (menu from factory, never hardcoded), model (factory default per backend) and key (per-backend slot; skipped for keyless Ollama). Readiness summary is provider-aware and masks secrets. |
| `cli/commands/ai.py` | `ask` answers through the configured `llm_backend`; `groq` pins the explicit Groq backend with the canonical oneliner template. Both in-process — the dead subprocess spawn of the legacy script is gone. |
| `slack_c2_bot.py`, `telegram_c2.py`, `discord_c2.py` | Consume `llm_adapter.ask_general` only. No vendor SDK import, no direct legacy import. |
| `tests/test_llm_prompts.py` | Pure contract tests: truncation, KB store, config context loading, template rendering, registry integrity. |
| `tests/test_llm_adapter_parity.py` | Facade parity + `ask_general` provider-agnostic behaviour. |
| `tests/test_llm_legacy_isolation.py` | AST watchdog: core source must not import `modules.legacy.lazygptcli*`. |
| `tests/test_llm_contract.py` | Frozen canonical-stack contract + factory metadata contract. |
| `tests/test_payload_schema.py` | `TestLlmBackendSchema`: enum validation, assign integration, factory-synced defaults, sensitive key slots. |
| `tests/test_wizard_llm.py` | Provider parsing, secret masking, scripted `_ask_llm` flows, readiness rows. |
| `tests/test_ai_commands_llm.py` | `ask`/`groq` behaviour: context injection, explicit backend pin, error paths. |
| `tests/test_security_hardening_v2.py` | Contract 1 evolved: no subprocess/shell/env-key-passing in `ai.py`; canonical backend entry points required. |

## Canonical stack

```
payload.json (llm_backend, llm_model_*, *_api_key, ollama_host)
        -> llm_factory (selection + metadata + budget wrapper)
        -> ai_model (AIModel.generate / .complete per backend)
llm_prompts (prompt templates + KB + context + DEFAULT_SYSTEM_PROMPT)
llm_adapter.ask_general -> llm_factory + llm_prompts   <-- bots use this
llm_adapter.process_prompt_* (Groq parity)             <-- lazyc2 uses this
cli/wizard Step 6 writes the payload keys from factory metadata
```

Rules frozen by `tests/test_llm_contract.py`:
- `modules.llm_factory` is canonical (public factory + metadata API, 6 canonical backends).
- `modules.unified_llm_client` must not exist.
- `modules.llm_adapter`, `modules.llm_client`, `modules.ai_model`,
  `modules.ai_fallback` survive as support modules.

## Behavioural invariants preserved by the facade

- `client is None` returns `"Error: Groq API key not configured"`.
- Missing prompt file on `task`/`vuln`/`redop` returns
  `"Error reading file: <path>"`.
- A raw completion failure returns the SDK error string (not raised).
- Only non-`Error` results are persisted to the knowledge base (the
  `ask_general` guard also covers `"Error from <backend>:"` strings).
- `vuln` augments content with the named event's `tool_output` and the session
  `plan.txt` history before prompting.
- Default token cap is 4096.
- `ask_general` with no usable backend returns an actionable error naming
  `llm_backend`, provider keys, and Ollama.

## Config centralization

No hardcoded paths. `LlmPromptConfig.from_defaults()` derives the project root
from the module location and resolves: KB dir (env `LAZYOWN_KB_DIR` optional),
`payload.json`, `event_config.json`, `sessions/`. Default Groq model and Ollama
endpoint/model constants come from `modules.llm_factory`.

## DoD gate

```
env/bin/python -m pytest tests/test_llm_prompts.py \
  tests/test_llm_adapter_parity.py \
  tests/test_llm_legacy_isolation.py \
  tests/test_llm_contract.py \
  tests/test_payload_schema.py \
  tests/test_wizard_llm.py \
  tests/test_ai_commands_llm.py \
  tests/test_security_hardening_v2.py
```

Mutation checks (each must be killed by a test): truncate the trailing
ellipsis in `truncate_message`; remove the KB-persistence error guard in the
adapter `_process`/`ask_general`; remap `default_model_for("auto")` to the
Ollama default; shift the wizard provider menu index by one; repoint
`do_groq` at another backend; drop its completion error handler.

## Remaining legacy debt (out of core, deferred)

1. Streaming local endpoints `process_prompt_local`, `process_prompt_localreport`
   (`modules.legacy.lazydeepseekcli`) and `process_prompt_local_yaml`
   (`modules.legacy.lazyphishingai`) are still re-exported by `llm_adapter.py`
   for the Ollama web-chat path.
2. `lazyc2.py` still drives the Groq `process_prompt_*` facade with raw SDK
   clients; migrate its call sites to `ask_general` (or a factory-backed
   transport) next.
3. `modules.legacy.lazygptcli.py` and `modules.legacy.lazyllmchat.py` are dead
   code (no importers). `modules.legacy.lazygptcli_unified.py` is now
   referenced only by its own docstring — delete all three once (1) and (2)
   land.

## Pre-existing issues observed (not introduced here)

- `slack_c2_bot.py` references `config` before assignment at module level
  (pre-existing `NameError` on import at HEAD).
- `tests/test_claudemd_size.py` fails at HEAD: `CLAUDE.md` exceeds its 40 KB
  budget independently of this change.
