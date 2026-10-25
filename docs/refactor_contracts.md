# LLM + OPSEC consolidation contracts

Consolidation refactors that collapsed dead and duplicated code into a single
source of truth per concern, without losing public API or behavior. Each row
lists the contract, its module, and its test/mutation gate.

## LLM — single factory entry point

`modules/llm_factory.py` is the **only** backend factory in the framework.
Every LLM consumer must call `get_llm_backend` / `try_get_llm_backend` /
`get_llm_backend_raw` — never instantiate a backend class directly.

| Contract | Module | Tests |
|----------|--------|-------|
| Canonical backend factory | `modules/llm_factory.py` | `test_llm_contract.py`, `test_llm_budget.py` |
| HTTP `ask/classify/summarize` client | `modules/llm_client.py` | `test_llm_contract.py` |
| Fallback chain (`AIResult`, `call`) | `modules/ai_fallback.py` | `test_llm_contract.py` |
| Backend model types | `modules/ai_model.py` | `test_llm_contract.py` |
| Legacy import adapter (C2) | `modules/llm_adapter.py` | `test_llm_contract.py` |

`modules/unified_llm_client.py` was dead code (no importers) and has been
removed. Mutation gate: `tests/run_mutation_llm.py` (6 mutants, all killed).
The guard test asserts the dead module no longer imports, so a parallel entry
point is never reintroduced.

## OPSEC — single scorer module

`modules/opsec_scorer.py` is the single contract for every OPSEC evaluation.
It hosts two complementary scorers that share one risk-mapping primitive:

| Contract | Module | Tests |
|----------|--------|-------|
| Advisory noise scorer (`OpsecScorer` -> `OpsecScore`) | `modules/opsec_scorer.py` | `test_opsec_scorer.py` |
| Gated scorer (`OpsecScorerV2` -> `GatedOpsecScore`) | `modules/opsec_scorer.py` | `test_opsec_scorer_consolidated.py` |
| Shared risk mapping (`_risk_bucket`/`_risk_label`/`_risk_level`) | `modules/opsec_scorer.py` | `test_opsec_scorer_consolidated.py` |

`modules/opsec_scorer_v2.py` was merged into `opsec_scorer.py`. The two
command tables (`COMMAND_NOISE` for advisory scoring, `COMMAND_RISK_PROFILES`
for gating) remain intentionally separate threat models. Import V2 symbols
from `modules.opsec_scorer`:

```python
from modules.opsec_scorer import OpsecContext, OpsecScorerV2
```

The noise-to-risk thresholds are defined exactly once in `_risk_bucket`.
Mutation gate: `tests/run_mutation_opsec.py` (6 mutants, all killed).

## API key resolution

`self.params["api_key"]` in `lazyown.py` was hardcoded to `None`, so every
startup-time gate (`recon`, the `lazynmap` post-scan chain, the AI bootstrap)
ignored a key that the wizard had persisted to `payload.json`. It now binds the
config-derived `api_key` class attribute.

Addons emit `{{key}}` placeholders (documented in `modules/yaml_generator.py`)
but `replace_command_placeholders` only handled `{key}`. It now handles both
brace styles while preserving unknown keys verbatim.

Test gate: `tests/test_api_key_resolution.py`.