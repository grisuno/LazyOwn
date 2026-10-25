# Symbols (page 27 of 45)
Previous: [SYMBOLS_p26.md](SYMBOLS_p26.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_post_execution_update` | method | `skills/swan_agent.py:827` | `def _post_execution_update(self, expert_id, task_type, reward, detection_prob, state_key, next_state, candidate_ids...` |
| `_store_to_hive` | method | `skills/swan_agent.py:860` | `def _store_to_hive(self, result, reward, detection_prob)` |
| `_tools_for_task` | method | `skills/swan_agent.py:417` | `def _tools_for_task(task_type)` |
| `aggregate` | method | `skills/swan_agent.py:209` | `def aggregate(self, task_type, goal, votes)` |
| `aggregate` | method | `skills/swan_agent.py:264` | `def aggregate(self, task_type, goal, votes)` |
| `ensemble_run` | method | `skills/swan_agent.py:236` | `def ensemble_run(self, task_type, goal, n_experts, engagement_phase, timeout)` |
| `ensemble_run` | method | `skills/swan_agent.py:680` | `def ensemble_run(self, task_type, goal, n_experts, engagement_phase, timeout)` |
| `evaluate` | method | `skills/swan_agent.py:479` | `def evaluate(self, result, task_type)` |
| `execute` | method | `skills/swan_agent.py:351` | `def execute(self, expert_id, backend, model, goal, task_type, timeout, api_key)` |
| `get_swan` | function | `skills/swan_agent.py:1039` | `def get_swan(api_key)` |
| `is_success` | method | `skills/swan_agent.py:167` | `def is_success(self)` |
| `mcp_swan_ensemble` | function | `skills/swan_agent.py:968` | `def mcp_swan_ensemble(task_type, goal, n_experts, phase)` |
| `mcp_swan_route` | function | `skills/swan_agent.py:1003` | `def mcp_swan_route(task_type, goal)` |
| `mcp_swan_run` | function | `skills/swan_agent.py:945` | `def mcp_swan_run(task_type, goal, phase)` |
| `mcp_swan_status` | function | `skills/swan_agent.py:996` | `def mcp_swan_status()` |
| `run` | method | `skills/swan_agent.py:226` | `def run(self, task_type, goal, engagement_phase, timeout)` |
| `run` | method | `skills/swan_agent.py:592` | `def run(self, task_type, goal, engagement_phase, timeout)` |
| `status` | method | `skills/swan_agent.py:763` | `def status(self)` |
| `CapturingSelector` | class | `skills/tests/test_autonomous_daemon.py:343` | `class CapturingSelector(ICommandSelector)` |
| `TestCascadeStrategy` | class | `skills/tests/test_autonomous_daemon.py:296` | `class TestCascadeStrategy` |
| `TestCommandRunnerChain` | class | `skills/tests/test_autonomous_daemon.py:134` | `class TestCommandRunnerChain` |
| `TestEmitEvent` | class | `skills/tests/test_autonomous_daemon.py:486` | `class TestEmitEvent` |
| `TestFallbackSelector` | class | `skills/tests/test_autonomous_daemon.py:205` | `class TestFallbackSelector` |
| `TestInjectToTasksJson` | class | `skills/tests/test_autonomous_daemon.py:360` | `class TestInjectToTasksJson` |
| `TestMCPAutonomousInject` | class | `skills/tests/test_autonomous_daemon.py:537` | `class TestMCPAutonomousInject` |
| `TestMCPAutonomousStatus` | class | `skills/tests/test_autonomous_daemon.py:610` | `class TestMCPAutonomousStatus` |
| `TestMCPCommandRunner` | class | `skills/tests/test_autonomous_daemon.py:88` | `class TestMCPCommandRunner` |
| `TestObjectiveLoopUnit` | class | `skills/tests/test_autonomous_daemon.py:666` | `class TestObjectiveLoopUnit` |
| `TestPTYCommandRunner` | class | `skills/tests/test_autonomous_daemon.py:59` | `class TestPTYCommandRunner` |
| `TestParquetSelector` | class | `skills/tests/test_autonomous_daemon.py:248` | `class TestParquetSelector` |
| `TestUpdateTaskStatus` | class | `skills/tests/test_autonomous_daemon.py:437` | `class TestUpdateTaskStatus` |
| `_R` | class | `skills/tests/test_autonomous_daemon.py:140` | `class _R(ICommandRunner)` |
| `_S` | class | `skills/tests/test_autonomous_daemon.py:303` | `class _S(ICommandSelector)` |
| `_failing_run_async` | function | `skills/tests/test_autonomous_daemon.py:784` | `def _failing_run_async(objective_id, objective_text, target)` |
| `_fake_run_async` | function | `skills/tests/test_autonomous_daemon.py:721` | `def _fake_run_async(objective_id, objective_text, target)` |
| `_make_mock_objective` | method | `skills/tests/test_autonomous_daemon.py:683` | `def _make_mock_objective(self)` |
| `_make_mock_store` | method | `skills/tests/test_autonomous_daemon.py:550` | `def _make_mock_store(self)` |
| `_make_runner` | method | `skills/tests/test_autonomous_daemon.py:137` | `def _make_runner(self, name, result, raises)` |
| `_make_selector` | method | `skills/tests/test_autonomous_daemon.py:299` | `def _make_selector(self, returns)` |
| `_next_pending` | function | `skills/tests/test_autonomous_daemon.py:706` | `def _next_pending()` |
| `_next_pending` | function | `skills/tests/test_autonomous_daemon.py:772` | `def _next_pending()` |
| `_patch_paths` | function | `skills/tests/test_autonomous_daemon.py:32` | `def _patch_paths(tmp_path)` |
| `_run_loop` | function | `skills/tests/test_autonomous_daemon.py:745` | `def _run_loop()` |
| `_run_loop` | function | `skills/tests/test_autonomous_daemon.py:807` | `def _run_loop()` |
| `_run_loop` | function | `skills/tests/test_autonomous_daemon.py:831` | `def _run_loop()` |
| `_stop_patchers` | function | `skills/tests/test_autonomous_daemon.py:49` | `def _stop_patchers(patchers)` |
| `_write_tasks` | method | `skills/tests/test_autonomous_daemon.py:450` | `def _write_tasks(self, tasks)` |
| `name` | method | `skills/tests/test_autonomous_daemon.py:142` | `def name(self)` |
| `run` | method | `skills/tests/test_autonomous_daemon.py:145` | `def run(self, command, timeout)` |
| `select` | method | `skills/tests/test_autonomous_daemon.py:304` | `def select(self, target, phase, context)` |
| `select` | method | `skills/tests/test_autonomous_daemon.py:344` | `def select(self, target, phase, context)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:363` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:440` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:489` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:540` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:613` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_autonomous_daemon.py:673` | `def setup_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:369` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:446` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:495` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:546` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:619` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_autonomous_daemon.py:679` | `def teardown_method(self)` |
| `test_always_returns_decision` | method | `skills/tests/test_autonomous_daemon.py:208` | `def test_always_returns_decision(self)` |
| `test_appends_new_task` | method | `skills/tests/test_autonomous_daemon.py:382` | `def test_appends_new_task(self)` |
| `test_block_called_on_execution_failure` | method | `skills/tests/test_autonomous_daemon.py:760` | `def test_block_called_on_execution_failure(self)` |
| `test_complete_called_after_successful_execution` | method | `skills/tests/test_autonomous_daemon.py:692` | `def test_complete_called_after_successful_execution(self)` |
| `test_contains_expected_fields` | method | `skills/tests/test_autonomous_daemon.py:631` | `def test_contains_expected_fields(self)` |
| `test_correct_schema` | method | `skills/tests/test_autonomous_daemon.py:394` | `def test_correct_schema(self)` |
| `test_creates_file_if_missing` | method | `skills/tests/test_autonomous_daemon.py:373` | `def test_creates_file_if_missing(self)` |
| `test_delegates_to_mcp_when_available` | method | `skills/tests/test_autonomous_daemon.py:114` | `def test_delegates_to_mcp_when_available(self)` |
| `test_event_has_required_fields` | method | `skills/tests/test_autonomous_daemon.py:511` | `def test_event_has_required_fields(self)` |
| `test_falls_back_to_second_on_exception` | method | `skills/tests/test_autonomous_daemon.py:162` | `def test_falls_back_to_second_on_exception(self)` |
| `test_handles_existing_invalid_json` | method | `skills/tests/test_autonomous_daemon.py:421` | `def test_handles_existing_invalid_json(self)` |
| `test_ignores_missing_title` | method | `skills/tests/test_autonomous_daemon.py:465` | `def test_ignores_missing_title(self)` |
| `test_implements_icommand_runner` | method | `skills/tests/test_autonomous_daemon.py:76` | `def test_implements_icommand_runner(self)` |
| `test_injects_to_objective_store_and_tasks_json` | method | `skills/tests/test_autonomous_daemon.py:562` | `def test_injects_to_objective_store_and_tasks_json(self)` |
| `test_instantiation` | method | `skills/tests/test_autonomous_daemon.py:62` | `def test_instantiation(self)` |
| `test_instantiation` | method | `skills/tests/test_autonomous_daemon.py:91` | `def test_instantiation(self)` |
| `test_loop_disabled_when_objective_store_missing` | method | `skills/tests/test_autonomous_daemon.py:821` | `def test_loop_disabled_when_objective_store_missing(self)` |
| `test_merges_status_file_when_present` | method | `skills/tests/test_autonomous_daemon.py:650` | `def test_merges_status_file_when_present(self)` |
| `test_multiple_emits_append_lines` | method | `skills/tests/test_autonomous_daemon.py:521` | `def test_multiple_emits_append_lines(self)` |
| `test_name_property` | method | `skills/tests/test_autonomous_daemon.py:69` | `def test_name_property(self)` |
| `test_name_property` | method | `skills/tests/test_autonomous_daemon.py:98` | `def test_name_property(self)` |
| `test_name_reflects_all_runners` | method | `skills/tests/test_autonomous_daemon.py:182` | `def test_name_reflects_all_runners(self)` |
| `test_passes_context_to_selectors` | method | `skills/tests/test_autonomous_daemon.py:337` | `def test_passes_context_to_selectors(self)` |
| `test_raises_when_all_fail` | method | `skills/tests/test_autonomous_daemon.py:172` | `def test_raises_when_all_fail(self)` |
| `test_raises_when_import_fails` | method | `skills/tests/test_autonomous_daemon.py:105` | `def test_raises_when_import_fails(self)` |
| `test_requires_at_least_one_runner` | method | `skills/tests/test_autonomous_daemon.py:192` | `def test_requires_at_least_one_runner(self)` |
| `test_respects_fail_counts` | method | `skills/tests/test_autonomous_daemon.py:275` | `def test_respects_fail_counts(self)` |
| `test_returns_assigned_id` | method | `skills/tests/test_autonomous_daemon.py:412` | `def test_returns_assigned_id(self)` |
| `test_returns_candidate_when_pdb_has_history` | method | `skills/tests/test_autonomous_daemon.py:259` | `def test_returns_candidate_when_pdb_has_history(self)` |
| `test_returns_command_decision_type` | method | `skills/tests/test_autonomous_daemon.py:216` | `def test_returns_command_decision_type(self)` |
| `test_returns_error_string_when_store_unavailable` | method | `skills/tests/test_autonomous_daemon.py:596` | `def test_returns_error_string_when_store_unavailable(self)` |
| `test_returns_false_when_file_missing` | method | `skills/tests/test_autonomous_daemon.py:473` | `def test_returns_false_when_file_missing(self)` |
| `test_returns_first_non_none_result` | method | `skills/tests/test_autonomous_daemon.py:309` | `def test_returns_first_non_none_result(self)` |
| `test_returns_json_with_both_ids` | method | `skills/tests/test_autonomous_daemon.py:581` | `def test_returns_json_with_both_ids(self)` |
| `test_returns_none_when_pdb_unavailable` | method | `skills/tests/test_autonomous_daemon.py:251` | `def test_returns_none_when_pdb_unavailable(self)` |
| `test_returns_valid_json` | method | `skills/tests/test_autonomous_daemon.py:623` | `def test_returns_valid_json(self)` |
| `test_running_is_false_when_no_daemon` | method | `skills/tests/test_autonomous_daemon.py:641` | `def test_running_is_false_when_no_daemon(self)` |
| `test_source_is_fallback` | method | `skills/tests/test_autonomous_daemon.py:225` | `def test_source_is_fallback(self)` |
| `test_unknown_phase_returns_decision` | method | `skills/tests/test_autonomous_daemon.py:233` | `def test_unknown_phase_returns_decision(self)` |
| `test_updates_existing_task` | method | `skills/tests/test_autonomous_daemon.py:455` | `def test_updates_existing_task(self)` |
| `test_uses_fallback_when_all_none` | method | `skills/tests/test_autonomous_daemon.py:325` | `def test_uses_fallback_when_all_none(self)` |
| `test_uses_first_runner_when_successful` | method | `skills/tests/test_autonomous_daemon.py:152` | `def test_uses_first_runner_when_successful(self)` |
| `test_writes_valid_json_line` | method | `skills/tests/test_autonomous_daemon.py:499` | `def test_writes_valid_json_line(self)` |
| `TestCrackMapExecParser` | class | `skills/tests/test_facts.py:61` | `class TestCrackMapExecParser` |
| `TestEnum4linuxParser` | class | `skills/tests/test_facts.py:81` | `class TestEnum4linuxParser` |
| `TestFactStore` | class | `skills/tests/test_facts.py:300` | `class TestFactStore` |
| `TestGobusterParser` | class | `skills/tests/test_facts.py:149` | `class TestGobusterParser` |
| `TestKerbruteParser` | class | `skills/tests/test_facts.py:119` | `class TestKerbruteParser` |
| `TestNiktoParser` | class | `skills/tests/test_facts.py:176` | `class TestNiktoParser` |
| `TestNmapXmlParser` | class | `skills/tests/test_facts.py:246` | `class TestNmapXmlParser` |
| `TestNucleiParser` | class | `skills/tests/test_facts.py:196` | `class TestNucleiParser` |
| `TestRpcclientParser` | class | `skills/tests/test_facts.py:138` | `class TestRpcclientParser` |
| `TestSecretsdumpParser` | class | `skills/tests/test_facts.py:105` | `class TestSecretsdumpParser` |
| `TestSslscanParser` | class | `skills/tests/test_facts.py:218` | `class TestSslscanParser` |
| `_make_config` | function | `skills/tests/test_facts.py:42` | `def _make_config(tmp_path)` |
| `test_context_for_command` | method | `skills/tests/test_facts.py:322` | `def test_context_for_command(self, tmp_path)` |
| `test_context_for_unknown_host` | method | `skills/tests/test_facts.py:356` | `def test_context_for_unknown_host(self, tmp_path)` |
| `test_crackmapexec_parser` | method | `skills/tests/test_facts.py:62` | `def test_crackmapexec_parser(self)` |
| `test_crackmapexec_pwned` | method | `skills/tests/test_facts.py:73` | `def test_crackmapexec_pwned(self)` |
| `test_dedup_creds` | method | `skills/tests/test_facts.py:429` | `def test_dedup_creds(self, tmp_path)` |
| `test_enum4linux_access_when_results` | method | `skills/tests/test_facts.py:97` | `def test_enum4linux_access_when_results(self)` |
| `test_enum4linux_parser` | method | `skills/tests/test_facts.py:82` | `def test_enum4linux_parser(self)` |
| `test_factstore_dedup` | method | `skills/tests/test_facts.py:301` | `def test_factstore_dedup(self, tmp_path)` |
| `test_factstore_save_and_reload` | method | `skills/tests/test_facts.py:363` | `def test_factstore_save_and_reload(self, tmp_path)` |
| `test_gobuster_multiple_paths` | method | `skills/tests/test_facts.py:162` | `def test_gobuster_multiple_paths(self)` |
| `test_gobuster_parser_parse_extended` | method | `skills/tests/test_facts.py:150` | `def test_gobuster_parser_parse_extended(self)` |
| `test_ingest_text_crackmapexec` | method | `skills/tests/test_facts.py:416` | `def test_ingest_text_crackmapexec(self, tmp_path)` |
| `test_ingest_xml` | method | `skills/tests/test_facts.py:390` | `def test_ingest_xml(self, tmp_path)` |
| `test_kerbrute_multiple_users` | method | `skills/tests/test_facts.py:129` | `def test_kerbrute_multiple_users(self)` |
| `test_kerbrute_parser` | method | `skills/tests/test_facts.py:120` | `def test_kerbrute_parser(self)` |
| `test_nikto_cve_line` | method | `skills/tests/test_facts.py:189` | `def test_nikto_cve_line(self)` |
| `test_nikto_parser_parse_extended` | method | `skills/tests/test_facts.py:177` | `def test_nikto_parser_parse_extended(self)` |
| `test_nmap_xml_parse` | method | `skills/tests/test_facts.py:270` | `def test_nmap_xml_parse(self, tmp_path)` |
| `test_nmap_xml_parse_invalid` | method | `skills/tests/test_facts.py:286` | `def test_nmap_xml_parse_invalid(self, tmp_path)` |
| `test_nuclei_multiple_severities` | method | `skills/tests/test_facts.py:209` | `def test_nuclei_multiple_severities(self)` |
| `test_nuclei_parser_parse_extended` | method | `skills/tests/test_facts.py:197` | `def test_nuclei_parser_parse_extended(self)` |
| `test_rpcclient_parser` | method | `skills/tests/test_facts.py:139` | `def test_rpcclient_parser(self)` |
| `test_secretsdump_parser` | method | `skills/tests/test_facts.py:106` | `def test_secretsdump_parser(self)` |
| `test_sslscan_dedup` | method | `skills/tests/test_facts.py:231` | `def test_sslscan_dedup(self)` |
| `test_sslscan_parser_parse_extended` | method | `skills/tests/test_facts.py:219` | `def test_sslscan_parser_parse_extended(self)` |
| `check` | function | `skills/tests/test_harness_e2e.py:33` | `def check(label, cond, hint)` |
| `main` | function | `skills/tests/test_harness_e2e.py:391` | `def main()` |
| `test_auto_compact` | function | `skills/tests/test_harness_e2e.py:263` | `def test_auto_compact(tmp)` |
| `test_claudemd` | function | `skills/tests/test_harness_e2e.py:228` | `def test_claudemd(tmp)` |
| `test_compaction` | function | `skills/tests/test_harness_e2e.py:98` | `def test_compaction()` |
| `test_hooks` | function | `skills/tests/test_harness_e2e.py:182` | `def test_hooks(tmp)` |
| `test_integration` | function | `skills/tests/test_harness_e2e.py:332` | `def test_integration(tmp)` |
| `test_metrics` | function | `skills/tests/test_harness_e2e.py:300` | `def test_metrics(tmp)` |
| `test_permissions` | function | `skills/tests/test_harness_e2e.py:47` | `def test_permissions(tmp)` |
| `test_transcript` | function | `skills/tests/test_harness_e2e.py:143` | `def test_transcript(tmp)` |
| `TestDronePool` | class | `skills/tests/test_hive_mind.py:346` | `class TestDronePool` |
| `TestDronePoolWithPersistence` | class | `skills/tests/test_hive_mind.py:770` | `class TestDronePoolWithPersistence` |
| `TestDroneStateStore` | class | `skills/tests/test_hive_mind.py:673` | `class TestDroneStateStore` |
| `TestEpisodicStore` | class | `skills/tests/test_hive_mind.py:72` | `class TestEpisodicStore` |
| `TestHiveBus` | class | `skills/tests/test_hive_mind.py:293` | `class TestHiveBus` |
| `TestHiveMemory` | class | `skills/tests/test_hive_mind.py:226` | `class TestHiveMemory` |
| `TestHiveMind` | class | `skills/tests/test_hive_mind.py:509` | `class TestHiveMind` |
| `TestMCPHandlers` | class | `skills/tests/test_hive_mind.py:575` | `class TestMCPHandlers` |
| `TestQueenBrain` | class | `skills/tests/test_hive_mind.py:428` | `class TestQueenBrain` |
| `TestSemanticStore` | class | `skills/tests/test_hive_mind.py:152` | `class TestSemanticStore` |
| `_build_hive_and_patch` | method | `skills/tests/test_hive_mind.py:588` | `def _build_hive_and_patch(self)` |
| `_instant_run` | function | `skills/tests/test_hive_mind.py:405` | `def _instant_run(self_inner)` |
| `_make_episodic` | function | `skills/tests/test_hive_mind.py:32` | `def _make_episodic(tmp_path)` |
| `_make_hive` | method | `skills/tests/test_hive_mind.py:519` | `def _make_hive(self)` |
| `_make_hive_memory` | function | `skills/tests/test_hive_mind.py:49` | `def _make_hive_memory(tmp_path)` |
| `_make_pool` | method | `skills/tests/test_hive_mind.py:356` | `def _make_pool(self)` |
| `_make_pool_with_store` | method | `skills/tests/test_hive_mind.py:780` | `def _make_pool_with_store(self)` |
| `_make_queen` | method | `skills/tests/test_hive_mind.py:438` | `def _make_queen(self)` |
| `_make_semantic` | function | `skills/tests/test_hive_mind.py:39` | `def _make_semantic(tmp_path, episodic)` |
| `_make_state` | method | `skills/tests/test_hive_mind.py:688` | `def _make_state(self, status)` |
| `_make_store` | method | `skills/tests/test_hive_mind.py:683` | `def _make_store(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:75` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:155` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:229` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:296` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:349` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:431` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:512` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:578` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:676` | `def setup_method(self)` |
| `setup_method` | method | `skills/tests/test_hive_mind.py:773` | `def setup_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:79` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:159` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:233` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:353` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:435` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:516` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:584` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:680` | `def teardown_method(self)` |
| `teardown_method` | method | `skills/tests/test_hive_mind.py:777` | `def teardown_method(self)` |
| `test_active_count_decrements_when_done` | method | `skills/tests/test_hive_mind.py:401` | `def test_active_count_decrements_when_done(self)` |
| `test_broadcast_received_by_everyone` | method | `skills/tests/test_hive_mind.py:312` | `def test_broadcast_received_by_everyone(self)` |
| `test_count_returns_zero_when_unavailable` | method | `skills/tests/test_hive_mind.py:212` | `def test_count_returns_zero_when_unavailable(self)` |
| `test_delete_older_than_removes_stale` | method | `skills/tests/test_hive_mind.py:750` | `def test_delete_older_than_removes_stale(self)` |
| `test_dispatch_returns_drone_ids` | method | `skills/tests/test_hive_mind.py:480` | `def test_dispatch_returns_drone_ids(self)` |
| `test_drone_result_unknown_id` | method | `skills/tests/test_hive_mind.py:557` | `def test_drone_result_unknown_id(self)` |
| `test_fallback_to_episodic_when_chroma_unavailable` | method | `skills/tests/test_hive_mind.py:179` | `def test_fallback_to_episodic_when_chroma_unavailable(self)` |
| `test_forget_by_topic` | method | `skills/tests/test_hive_mind.py:132` | `def test_forget_by_topic(self)` |
| `test_forget_delegates_to_episodic` | method | `skills/tests/test_hive_mind.py:277` | `def test_forget_delegates_to_episodic(self)` |
| `test_forget_old_events` | method | `skills/tests/test_hive_mind.py:121` | `def test_forget_old_events(self)` |
| `test_forget_returns_int` | method | `skills/tests/test_hive_mind.py:563` | `def test_forget_returns_int(self)` |
| `test_get_state_returns_drone_state` | method | `skills/tests/test_hive_mind.py:374` | `def test_get_state_returns_drone_state(self)` |
| `test_get_state_unknown_id_returns_none` | method | `skills/tests/test_hive_mind.py:386` | `def test_get_state_unknown_id_returns_none(self)` |
| `test_instantiation` | method | `skills/tests/test_hive_mind.py:162` | `def test_instantiation(self)` |
| `test_list_all_includes_history` | method | `skills/tests/test_hive_mind.py:844` | `def test_list_all_includes_history(self)` |
| `test_list_all_includes_spawned_drone` | method | `skills/tests/test_hive_mind.py:392` | `def test_list_all_includes_spawned_drone(self)` |
| `test_load_all_empty_db` | method | `skills/tests/test_hive_mind.py:759` | `def test_load_all_empty_db(self)` |
| `test_load_interrupted_returns_only_interrupted` | method | `skills/tests/test_hive_mind.py:737` | `def test_load_interrupted_returns_only_interrupted(self)` |
| `test_mark_interrupted_targets_queued_and_running` | method | `skills/tests/test_hive_mind.py:722` | `def test_mark_interrupted_targets_queued_and_running(self)` |
| `test_mcp_hive_collect_no_ids` | method | `skills/tests/test_hive_mind.py:660` | `def test_mcp_hive_collect_no_ids(self)` |
| `test_mcp_hive_forget_returns_pruned_count` | method | `skills/tests/test_hive_mind.py:636` | `def test_mcp_hive_forget_returns_pruned_count(self)` |
| `test_mcp_hive_plan_returns_parseable_string` | method | `skills/tests/test_hive_mind.py:610` | `def test_mcp_hive_plan_returns_parseable_string(self)` |
| `test_mcp_hive_recall_no_results` | method | `skills/tests/test_hive_mind.py:629` | `def test_mcp_hive_recall_no_results(self)` |
| `test_mcp_hive_recover_no_interrupted` | method | `skills/tests/test_hive_mind.py:862` | `def test_mcp_hive_recover_no_interrupted(self)` |
| `test_mcp_hive_result_unknown_drone` | method | `skills/tests/test_hive_mind.py:652` | `def test_mcp_hive_result_unknown_drone(self)` |
| `test_mcp_hive_spawn_single` | method | `skills/tests/test_hive_mind.py:643` | `def test_mcp_hive_spawn_single(self)` |
| `test_mcp_hive_status_contains_fields` | method | `skills/tests/test_hive_mind.py:619` | `def test_mcp_hive_status_contains_fields(self)` |
| `test_pending_count_after_publish` | method | `skills/tests/test_hive_mind.py:321` | `def test_pending_count_after_publish(self)` |
| `test_plan_ad_goal` | method | `skills/tests/test_hive_mind.py:461` | `def test_plan_ad_goal(self)` |
| `test_plan_enum_returns_multiple_tasks` | method | `skills/tests/test_hive_mind.py:446` | `def test_plan_enum_returns_multiple_tasks(self)` |
| `test_plan_exploit_goal` | method | `skills/tests/test_hive_mind.py:454` | `def test_plan_exploit_goal(self)` |
| `test_plan_generic_goal` | method | `skills/tests/test_hive_mind.py:468` | `def test_plan_generic_goal(self)` |
| `test_plan_n_drones_pads_to_requested` | method | `skills/tests/test_hive_mind.py:474` | `def test_plan_n_drones_pads_to_requested(self)` |
| `test_publish_and_receive` | method | `skills/tests/test_hive_mind.py:301` | `def test_publish_and_receive(self)` |
| `test_recall_deduplication` | method | `skills/tests/test_hive_mind.py:244` | `def test_recall_deduplication(self)` |
| `test_recall_from_memory_after_store` | method | `skills/tests/test_hive_mind.py:542` | `def test_recall_from_memory_after_store(self)` |
| `test_recall_fts_multiple_hits` | method | `skills/tests/test_hive_mind.py:104` | `def test_recall_fts_multiple_hits(self)` |
| `test_recall_keyword_found` | method | `skills/tests/test_hive_mind.py:89` | `def test_recall_keyword_found(self)` |
| `test_recall_keyword_not_found` | method | `skills/tests/test_hive_mind.py:97` | `def test_recall_keyword_not_found(self)` |
| `test_recall_with_mock_chroma` | method | `skills/tests/test_hive_mind.py:192` | `def test_recall_with_mock_chroma(self)` |
| `test_receive_drains_direct_mailbox` | method | `skills/tests/test_hive_mind.py:329` | `def test_receive_drains_direct_mailbox(self)` |
| `test_recover_from_store_marks_interrupted` | method | `skills/tests/test_hive_mind.py:798` | `def test_recover_from_store_marks_interrupted(self)` |
| `test_requeue_interrupted_respawns_drones` | method | `skills/tests/test_hive_mind.py:825` | `def test_requeue_interrupted_respawns_drones(self)` |
| `test_spawn_persists_initial_state` | method | `skills/tests/test_hive_mind.py:789` | `def test_spawn_persists_initial_state(self)` |
| `test_spawn_returns_drone_id` | method | `skills/tests/test_hive_mind.py:365` | `def test_spawn_returns_drone_id(self)` |
| `test_spawn_single_drone` | method | `skills/tests/test_hive_mind.py:534` | `def test_spawn_single_drone(self)` |
| `test_stats_contains_expected_keys` | method | `skills/tests/test_hive_mind.py:269` | `def test_stats_contains_expected_keys(self)` |
| `test_stats_counts_rows` | method | `skills/tests/test_hive_mind.py:112` | `def test_stats_counts_rows(self)` |
| `test_status_contains_expected_fields` | method | `skills/tests/test_hive_mind.py:549` | `def test_status_contains_expected_fields(self)` |
| `test_store_and_recall` | method | `skills/tests/test_hive_mind.py:236` | `def test_store_and_recall(self)` |
| `test_store_returns_id` | method | `skills/tests/test_hive_mind.py:169` | `def test_store_returns_id(self)` |
| `test_store_returns_nonempty_id` | method | `skills/tests/test_hive_mind.py:82` | `def test_store_returns_nonempty_id(self)` |
| `test_synthesize_structure` | method | `skills/tests/test_hive_mind.py:489` | `def test_synthesize_structure(self)` |
| `test_upsert_and_load_all` | method | `skills/tests/test_hive_mind.py:700` | `def test_upsert_and_load_all(self)` |
| `test_upsert_updates_existing` | method | `skills/tests/test_hive_mind.py:709` | `def test_upsert_updates_existing(self)` |
| `check` | function | `skills/tests/test_mcp_smoke.py:23` | `def check(label, cond, hint)` |
| `main` | function | `skills/tests/test_mcp_smoke.py:96` | `def main()` |
| `test_list_tools_returns_tools` | function | `skills/tests/test_mcp_smoke.py:61` | `def test_list_tools_returns_tools(mcp)` |
| `test_mcp_module_imports` | function | `skills/tests/test_mcp_smoke.py:34` | `def test_mcp_module_imports()` |
| `test_mcp_wellknown_symbols` | function | `skills/tests/test_mcp_smoke.py:47` | `def test_mcp_wellknown_symbols(mcp)` |
| `TestObjectiveStore` | class | `skills/tests/test_objectives.py:51` | `class TestObjectiveStore` |
| `TestSoulUpdater` | class | `skills/tests/test_objectives.py:204` | `class TestSoulUpdater` |
| `_soul_updater` | function | `skills/tests/test_objectives.py:36` | `def _soul_updater(tmp_path)` |
| `_store` | function | `skills/tests/test_objectives.py:31` | `def _store(tmp_path)` |
| `test_block` | method | `skills/tests/test_objectives.py:129` | `def test_block(self, tmp_path)` |
| `test_cleanup_critical_never_expires` | method | `skills/tests/test_objectives.py:182` | `def test_cleanup_critical_never_expires(self, tmp_path)` |
| `test_cleanup_medium_72h_ttl` | method | `skills/tests/test_objectives.py:166` | `def test_cleanup_medium_72h_ttl(self, tmp_path)` |
| `test_complete` | method | `skills/tests/test_objectives.py:119` | `def test_complete(self, tmp_path)` |
| `test_dedup` | method | `skills/tests/test_objectives.py:62` | `def test_dedup(self, tmp_path)` |
| `test_inject_basic` | method | `skills/tests/test_objectives.py:52` | `def test_inject_basic(self, tmp_path)` |
| `test_inject_invalid_priority_defaults_medium` | method | `skills/tests/test_objectives.py:140` | `def test_inject_invalid_priority_defaults_medium(self, tmp_path)` |
| `test_list_pending_empty` | method | `skills/tests/test_objectives.py:146` | `def test_list_pending_empty(self, tmp_path)` |
| `test_next_pending_fifo_same_priority` | method | `skills/tests/test_objectives.py:109` | `def test_next_pending_fifo_same_priority(self, tmp_path)` |
| `test_next_pending_none_when_empty` | method | `skills/tests/test_objectives.py:151` | `def test_next_pending_none_when_empty(self, tmp_path)` |
| `test_next_pending_priority` | method | `skills/tests/test_objectives.py:99` | `def test_next_pending_priority(self, tmp_path)` |
| `test_objectives_persist_on_disk` | method | `skills/tests/test_objectives.py:156` | `def test_objectives_persist_on_disk(self, tmp_path)` |
| `test_soul_updater_appends_new_section` | method | `skills/tests/test_objectives.py:293` | `def test_soul_updater_appends_new_section(self, tmp_path)` |
| `test_soul_updater_credentials_hash` | method | `skills/tests/test_objectives.py:231` | `def test_soul_updater_credentials_hash(self, tmp_path)` |
| `test_soul_updater_credentials_username_only` | method | `skills/tests/test_objectives.py:241` | `def test_soul_updater_credentials_username_only(self, tmp_path)` |
| `test_soul_updater_empty_creds_noop` | method | `skills/tests/test_objectives.py:285` | `def test_soul_updater_empty_creds_noop(self, tmp_path)` |
| `test_soul_updater_patch_line` | method | `skills/tests/test_objectives.py:205` | `def test_soul_updater_patch_line(self, tmp_path)` |
| `test_soul_updater_patch_replaces_existing` | method | `skills/tests/test_objectives.py:274` | `def test_soul_updater_patch_replaces_existing(self, tmp_path)` |
| `test_soul_updater_section` | method | `skills/tests/test_objectives.py:223` | `def test_soul_updater_section(self, tmp_path)` |
| `test_soul_updater_section_access` | method | `skills/tests/test_objectives.py:257` | `def test_soul_updater_section_access(self, tmp_path)` |
| `test_soul_updater_section_os` | method | `skills/tests/test_objectives.py:249` | `def test_soul_updater_section_os(self, tmp_path)` |
| `test_soul_updater_target_line` | method | `skills/tests/test_objectives.py:216` | `def test_soul_updater_target_line(self, tmp_path)` |
| `test_soul_updater_vulnerabilities` | method | `skills/tests/test_objectives.py:265` | `def test_soul_updater_vulnerabilities(self, tmp_path)` |
| `test_ttl_expiry` | method | `skills/tests/test_objectives.py:74` | `def test_ttl_expiry(self, tmp_path)` |
| `TestParquetDBAnnotate` | class | `skills/tests/test_parquet_db.py:177` | `class TestParquetDBAnnotate` |
| `TestParquetDBQueryKnowledge` | class | `skills/tests/test_parquet_db.py:351` | `class TestParquetDBQueryKnowledge` |
| `TestParquetDBQuerySession` | class | `skills/tests/test_parquet_db.py:276` | `class TestParquetDBQuerySession` |
| `TestParquetDBSync` | class | `skills/tests/test_parquet_db.py:91` | `class TestParquetDBSync` |
| `TestStableId` | class | `skills/tests/test_parquet_db.py:401` | `class TestStableId` |
| `_make_db` | function | `skills/tests/test_parquet_db.py:67` | `def _make_db(tmp_path)` |
| `_setup_two_phases` | method | `skills/tests/test_parquet_db.py:277` | `def _setup_two_phases(self, tmp_path)` |
| `_setup_with_one_row` | method | `skills/tests/test_parquet_db.py:178` | `def _setup_with_one_row(self, tmp_path)` |
| `_write_csv` | function | `skills/tests/test_parquet_db.py:56` | `def _write_csv(path, rows)` |
| `test_annotate` | method | `skills/tests/test_parquet_db.py:198` | `def test_annotate(self, tmp_path)` |
| `test_annotate_category` | method | `skills/tests/test_parquet_db.py:208` | `def test_annotate_category(self, tmp_path)` |
| `test_annotate_missing_id` | method | `skills/tests/test_parquet_db.py:217` | `def test_annotate_missing_id(self, tmp_path)` |
| `test_annotate_rich_explicit_finding_type` | method | `skills/tests/test_parquet_db.py:265` | `def test_annotate_rich_explicit_finding_type(self, tmp_path)` |
| `test_annotate_rich_finding_type_credential` | method | `skills/tests/test_parquet_db.py:223` | `def test_annotate_rich_finding_type_credential(self, tmp_path)` |
| `test_annotate_rich_finding_type_hash` | method | `skills/tests/test_parquet_db.py:243` | `def test_annotate_rich_finding_type_hash(self, tmp_path)` |
| `test_annotate_rich_finding_type_vulnerability` | method | `skills/tests/test_parquet_db.py:233` | `def test_annotate_rich_finding_type_vulnerability(self, tmp_path)` |
| `test_annotate_rich_output_snippet_truncated` | method | `skills/tests/test_parquet_db.py:256` | `def test_annotate_rich_output_snippet_truncated(self, tmp_path)` |
| `test_query_knowledge_keyword_binarios` | method | `skills/tests/test_parquet_db.py:390` | `def test_query_knowledge_keyword_binarios(self, tmp_path)` |
| `test_query_knowledge_no_match` | method | `skills/tests/test_parquet_db.py:370` | `def test_query_knowledge_no_match(self, tmp_path)` |
| `test_query_knowledge_session_parquet` | method | `skills/tests/test_parquet_db.py:352` | `def test_query_knowledge_session_parquet(self, tmp_path)` |
| `test_query_session_empty` | method | `skills/tests/test_parquet_db.py:328` | `def test_query_session_empty(self, tmp_path)` |
| `test_query_session_filter` | method | `skills/tests/test_parquet_db.py:306` | `def test_query_session_filter(self, tmp_path)` |
| `test_query_session_no_filter` | method | `skills/tests/test_parquet_db.py:322` | `def test_query_session_no_filter(self, tmp_path)` |
| `test_query_session_scanning_filter` | method | `skills/tests/test_parquet_db.py:314` | `def test_query_session_scanning_filter(self, tmp_path)` |
| `test_query_session_target_filter` | method | `skills/tests/test_parquet_db.py:334` | `def test_query_session_target_filter(self, tmp_path)` |
| `test_schema_cols` | method | `skills/tests/test_parquet_db.py:155` | `def test_schema_cols(self, tmp_path)` |
| `test_stable_id_deterministic` | method | `skills/tests/test_parquet_db.py:402` | `def test_stable_id_deterministic(self)` |
| `test_stable_id_different_inputs` | method | `skills/tests/test_parquet_db.py:408` | `def test_stable_id_different_inputs(self)` |
| `test_stable_id_length` | method | `skills/tests/test_parquet_db.py:414` | `def test_stable_id_length(self)` |
| `test_sync_from_csv` | method | `skills/tests/test_parquet_db.py:92` | `def test_sync_from_csv(self, tmp_path)` |
| `test_sync_idempotent` | method | `skills/tests/test_parquet_db.py:140` | `def test_sync_idempotent(self, tmp_path)` |
| `test_sync_missing_csv` | method | `skills/tests/test_parquet_db.py:170` | `def test_sync_missing_csv(self, tmp_path)` |
| `test_sync_skips_empty_command` | method | `skills/tests/test_parquet_db.py:121` | `def test_sync_skips_empty_command(self, tmp_path)` |
| `AutonomousAgent` | class | `skills/toposwarm_autonomous.py:309` | `class AutonomousAgent` |
| `PentestState` | class | `skills/toposwarm_autonomous.py:127` | `class PentestState` |
| `__init__` | method | `skills/toposwarm_autonomous.py:310` | `def __init__(self, state, no_model, verbose, effort, max_phases, json_out)` |
| `_enum_goals` | function | `skills/toposwarm_autonomous.py:286` | `def _enum_goals(state)` |
| `_execute_goal` | method | `skills/toposwarm_autonomous.py:347` | `def _execute_goal(self, goal, phase_name)` |
| `_load_payload` | function | `skills/toposwarm_autonomous.py:479` | `def _load_payload()` |
| `_parse_output` | function | `skills/toposwarm_autonomous.py:181` | `def _parse_output(output, state, phase_name)` |
| `_phase_goals` | function | `skills/toposwarm_autonomous.py:233` | `def _phase_goals(phase_idx, state, effort)` |
| `_run_phase` | method | `skills/toposwarm_autonomous.py:386` | `def _run_phase(self, phase_idx)` |
| `_save_state` | method | `skills/toposwarm_autonomous.py:418` | `def _save_state(self)` |
| `add_finding` | method | `skills/toposwarm_autonomous.py:145` | `def add_finding(self, phase_name, text)` |
| `main` | function | `skills/toposwarm_autonomous.py:489` | `def main(argv)` |
| `run` | method | `skills/toposwarm_autonomous.py:432` | `def run(self, start_phase)` |
| `summary` | method | `skills/toposwarm_autonomous.py:149` | `def summary(self)` |
| `to_dict` | method | `skills/toposwarm_autonomous.py:160` | `def to_dict(self)` |
| `BackendRegistry` | class | `skills/unified_orchestrator.py:300` | `class BackendRegistry` |
| `DaemonBackend` | class | `skills/unified_orchestrator.py:408` | `class DaemonBackend` |
| `EventBus` | class | `skills/unified_orchestrator.py:224` | `class EventBus` |
| `GoalValidator` | class | `skills/unified_orchestrator.py:806` | `class GoalValidator` |
| `HiveBackend` | class | `skills/unified_orchestrator.py:605` | `class HiveBackend` |
| `IOrchestratorBackend` | class | `skills/unified_orchestrator.py:210` | `class IOrchestratorBackend(Protocol)` |
| `OrchestratorConfig` | class | `skills/unified_orchestrator.py:51` | `class OrchestratorConfig` |
| `OrchestratorGoal` | class | `skills/unified_orchestrator.py:143` | `class OrchestratorGoal` |
| `OrchestratorResult` | class | `skills/unified_orchestrator.py:174` | `class OrchestratorResult` |
| `RouterPolicy` | class | `skills/unified_orchestrator.py:340` | `class RouterPolicy` |
| `SwanBackend` | class | `skills/unified_orchestrator.py:706` | `class SwanBackend` |
| `UnifiedOrchestrator` | class | `skills/unified_orchestrator.py:871` | `class UnifiedOrchestrator` |
| `__init__` | method | `skills/unified_orchestrator.py:233` | `def __init__(self, config, root)` |
| `__init__` | method | `skills/unified_orchestrator.py:303` | `def __init__(self, backends)` |
| `__init__` | method | `skills/unified_orchestrator.py:347` | `def __init__(self, config, registry)` |
| `__init__` | method | `skills/unified_orchestrator.py:413` | `def __init__(self, config, factory, payload)` |
| `__init__` | method | `skills/unified_orchestrator.py:610` | `def __init__(self, config, factory)` |
| `__init__` | method | `skills/unified_orchestrator.py:711` | `def __init__(self, config, factory)` |
| `__init__` | method | `skills/unified_orchestrator.py:814` | `def __init__(self, config)` |
| `__init__` | method | `skills/unified_orchestrator.py:874` | `def __init__(self, config, registry, router, validator, bus)` |
| `_artefacts` | method | `skills/unified_orchestrator.py:585` | `def _artefacts(raw)` |
| `_artefacts` | method | `skills/unified_orchestrator.py:795` | `def _artefacts(swan_result)` |
| `_build` | method | `skills/unified_orchestrator.py:513` | `def _build(self, goal, target)` |
| `_build` | method | `skills/unified_orchestrator.py:677` | `def _build(self)` |
| `_build` | method | `skills/unified_orchestrator.py:772` | `def _build(self, api_key)` |
| `_emit` | method | `skills/unified_orchestrator.py:948` | `def _emit(self, result, mode, goal)` |
| `_import_class` | method | `skills/unified_orchestrator.py:535` | `def _import_class()` |
| `_import_factory` | method | `skills/unified_orchestrator.py:687` | `def _import_factory()` |
| `_import_factory` | method | `skills/unified_orchestrator.py:779` | `def _import_factory()` |
| `_keyword_score` | method | `skills/unified_orchestrator.py:404` | `def _keyword_score(text, keywords)` |
| `_make_result` | function | `skills/unified_orchestrator.py:968` | `def _make_result(request_id, backend, status, summary, artefacts, events, duration, raw)` |
| `_new_request_id` | function | `skills/unified_orchestrator.py:963` | `def _new_request_id()` |
| `_score` | method | `skills/unified_orchestrator.py:367` | `def _score(self, goal, backend)` |
| `_summarise` | method | `skills/unified_orchestrator.py:541` | `def _summarise(raw, target)` |
| `_summarise` | method | `skills/unified_orchestrator.py:698` | `def _summarise(tasks, synthesis)` |
| `_summarise` | method | `skills/unified_orchestrator.py:785` | `def _summarise(swan_result)` |
| `_target_from_metadata` | method | `skills/unified_orchestrator.py:502` | `def _target_from_metadata(self, goal)` |
| `available` | method | `skills/unified_orchestrator.py:215` | `def available(self)` |
| `available` | method | `skills/unified_orchestrator.py:335` | `def available(self)` |
| `available` | method | `skills/unified_orchestrator.py:435` | `def available(self)` |
| `available` | method | `skills/unified_orchestrator.py:619` | `def available(self)` |
| `available` | method | `skills/unified_orchestrator.py:720` | `def available(self)` |
| `backends` | method | `skills/unified_orchestrator.py:890` | `def backends(self)` |
| `build_default_orchestrator` | function | `skills/unified_orchestrator.py:995` | `def build_default_orchestrator(payload, sessions_dir)` |
| `choose` | method | `skills/unified_orchestrator.py:352` | `def choose(self, goal)` |
| `effective_target` | method | `skills/unified_orchestrator.py:489` | `def effective_target(self, goal)` |
| `emit` | method | `skills/unified_orchestrator.py:256` | `def emit(self, event)` |
| `execute` | method | `skills/unified_orchestrator.py:894` | `def execute(self, goal, mode, phase, task_type, target, drones, timeout, api_key, metadata)` |
| `from_payload` | method | `skills/unified_orchestrator.py:111` | `def from_payload(cls, payload)` |
| `get` | method | `skills/unified_orchestrator.py:331` | `def get(self, name)` |
| `names` | method | `skills/unified_orchestrator.py:327` | `def names(self)` |
| `path` | method | `skills/unified_orchestrator.py:252` | `def path(self)` |
| `run` | method | `skills/unified_orchestrator.py:219` | `def run(self, goal)` |
| `run` | method | `skills/unified_orchestrator.py:445` | `def run(self, goal)` |
| `run` | method | `skills/unified_orchestrator.py:629` | `def run(self, goal)` |
| `run` | method | `skills/unified_orchestrator.py:730` | `def run(self, goal)` |
| `to_dict` | method | `skills/unified_orchestrator.py:197` | `def to_dict(self)` |
| `validate` | method | `skills/unified_orchestrator.py:818` | `def validate(self, goal, mode, phase, task_type, target, drones, timeout, api_key, metadata)` |
| `with_defaults` | method | `skills/unified_orchestrator.py:156` | `def with_defaults(self, config)` |
| `main` | function | `skills/update_knowledge.py:40` | `def main(argv)` |
| `SecureSessionManager` | class | `slack_c2_bot.py:28` | `class SecureSessionManager` |
| `__init__` | method | `slack_c2_bot.py:29` | `def __init__(self)` |
| `capture_shell_output` | function | `slack_c2_bot.py:95` | `def capture_shell_output(cmd)` |
| `check_lockout` | method | `slack_c2_bot.py:42` | `def check_lockout(self, user_id)` |
| `check_rate_limit` | method | `slack_c2_bot.py:52` | `def check_rate_limit(self, user_id)` |
| `cmd_addcli` | function | `slack_c2_bot.py:177` | `def cmd_addcli(ack, respond, command)` |
| `cmd_clients` | function | `slack_c2_bot.py:195` | `def cmd_clients(ack, respond, command)` |
| `cmd_download` | function | `slack_c2_bot.py:209` | `def cmd_download(ack, respond, command)` |
| `create_session` | method | `slack_c2_bot.py:63` | `def create_session(self, user_id)` |
| `get_client` | method | `slack_c2_bot.py:85` | `def get_client(self, user_id)` |
| `handle_file` | function | `slack_c2_bot.py:240` | `def handle_file(event, say, logger)` |
| `handle_message` | function | `slack_c2_bot.py:113` | `def handle_message(event, say, logger)` |
| `mentioned` | function | `slack_c2_bot.py:252` | `def mentioned(ack, say, event)` |
| `register_failed_attempt` | method | `slack_c2_bot.py:34` | `def register_failed_attempt(self, user_id)` |
| `set_client` | method | `slack_c2_bot.py:81` | `def set_client(self, user_id, client_id)` |
| `validate_session` | method | `slack_c2_bot.py:71` | `def validate_session(self, user_id)` |
| `As` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Be` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Cs` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Do` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ds` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ef` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `Fp` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `Fs` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Gd` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `Ge` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Gs` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `He` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Hh` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `I` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `In` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ir` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Is` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Jh` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Jo` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Jp` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `Js` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ke` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Kp` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `Lo` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ls` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Md` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `Mi` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Mn` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ne` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Oe` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `On` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Pi` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ps` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Qp` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `Sn` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Te` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Us` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ve` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Vh` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Vr` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `We` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Wo` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Wr` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ws` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Xe` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Xo` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Xp` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `Yi` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Ys` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Zi` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Zn` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `Zp` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `_r` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `_s` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `a` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `ao` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `as` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `as` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `b` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `bi` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `bp` | class | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `c` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `c` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `cf` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `co` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `coefficient` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `cr` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `di` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `differentBody` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `e` | function | `static/js/3d-force-graph-1.73.4.min.js:5` | `` |
| `er` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `es` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `extends` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `extends` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `extends` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `extends` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |
| `extends` | class | `static/js/3d-force-graph-1.73.4.min.js:2` | `` |

Next: [SYMBOLS_p28.md](SYMBOLS_p28.md)
