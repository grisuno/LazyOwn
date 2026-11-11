# Architecture (page 8 of 11)
Previous: [ARCHITECTURE_p7.md](ARCHITECTURE_p7.md)

## Internal Dependencies (continued)
- `tests/test_vulnbot_fallback.py` -> `modules/llm_factory.py`
- `tests/test_vulnbot_fallback.py` -> `modules/llm_orchestrator.py`
- `tests/test_vulnbot_fallback.py` -> `modules/vulnbot.py`
- `tests/test_winbox_gym.py` -> `core/hardening.py`
- `tests/test_winbox_gym.py` -> `modules/__init__.py`
- `tests/test_winbox_gym.py` -> `modules/gym_registry.py`
- `tests/test_wizard_binary_check.py` -> `cli/__init__.py`
- `tests/test_wizard_llm.py` -> `cli/wizard.py`
- `tests/test_wizard_llm.py` -> `modules/llm_factory.py`
- `tests/test_world_diff_retest.py` -> `modules/lazy_engine.py`
- `tests/test_world_diff_retest.py` -> `modules/lazy_loop.py`
- `tests/test_world_diff_retest.py` -> `modules/lazy_world_diff.py`
- `tests/test_world_diff_retest.py` -> `modules/outcome_bus.py`
- `tests/test_world_diff_retest.py` -> `modules/sinks/world_diff.py`
- `tests/test_world_model_extended.py` -> `modules/world_model.py`
- `tests/test_writeback_hygiene.py` -> `modules/lazy_loop.py`
- `tests/test_writeback_hygiene.py` -> `modules/loop_guardrails.py`
- `tools/gen_demo_gifs_extra.py` -> `tools/gen_demo_gifs.py`
- `utils.py` -> `cli/banner_config.py`
- `utils.py` -> `core/config.py`
- `utils.py` -> `core/console.py`
- `utils.py` -> `core/crypto.py`
- `utils.py` -> `core/dependencies.py`
- `utils.py` -> `core/logging.py`
- `utils.py` -> `core/parsers.py`
- `utils.py` -> `core/process.py`
- `utils.py` -> `core/safe_subprocess.py`
- `utils.py` -> `core/validators.py`
- `utils.py` -> `modules/backdoor/server.c`
- `utils.py` -> `modules/lazyencoder_decoder.py`
- `utils.py` -> `skills/claude_md_orchestrator/parser.py`


Next: [ARCHITECTURE_p9.md](ARCHITECTURE_p9.md)
