# API (page 9 of 20)
Previous: [API_p8.md](API_p8.md)

## modules/ai_model.py
Depends on: `core/logging.py`
Imported by: `contrib/legacy/lazyllmchat.py`, `modules/agent_runner.py`, `modules/llm_factory.py`, `modules/vuln_agent.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`
- `AIModel.generate` (method) `modules/ai_model.py:52` `def generate(self, prompt)` -- Return a non-streaming completion for ``prompt``.
- `AIModel.stream_generate` (method) `modules/ai_model.py:56` `def stream_generate(self, prompt)` -- Yield streaming completion chunks for ``prompt``.
- `AIModel.complete` (method) `modules/ai_model.py:59` `def complete(self, system, user, max_tokens, temperature)` -- Return a completion conforming to ``core.protocols.LLMBackend``.
- `_LazyImporter.groq` (method) `modules/ai_model.py:101` `def groq(cls)`
- `_LazyImporter.openai` (method) `modules/ai_model.py:109` `def openai(cls)`
- `_LazyImporter.anthropic` (method) `modules/ai_model.py:117` `def anthropic(cls)`
- `GroqModel.__init__` (method) `modules/ai_model.py:133` `def __init__(self, api_key, model)`
- `GroqModel.generate` (method) `modules/ai_model.py:137` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `GroqModel.stream_generate` (method) `modules/ai_model.py:155` `def stream_generate(self, prompt)` -- Yield streamed completion chunks for ``prompt``.
- `GroqModel.complete` (method) `modules/ai_model.py:177` `def complete(self, system, user, max_tokens, temperature)` -- Return a chat completion using native role separation.
- `OllamaModel.__init__` (method) `modules/ai_model.py:213` `def __init__(self, model, host)`
- `OllamaModel.generate` (method) `modules/ai_model.py:221` `def generate(self, prompt)` -- Return a single completion for ``prompt``.
- `OllamaModel.stream_generate` (method) `modules/ai_model.py:241` `def stream_generate(self, prompt)` -- Yield streamed completion chunks for ``prompt``.
- `OpenAIModel.__init__` (method) `modules/ai_model.py:278` `def __init__(self, api_key, model)`
- `OpenAIModel.generate` (method) `modules/ai_model.py:282` `def generate(self, prompt)`
- `OpenAIModel.stream_generate` (method) `modules/ai_model.py:293` `def stream_generate(self, prompt)`
- `OpenAIModel.complete` (method) `modules/ai_model.py:308` `def complete(self, system, user, max_tokens, temperature)`
- `AnthropicModel.__init__` (method) `modules/ai_model.py:337` `def __init__(self, api_key, model)`
- `AnthropicModel.generate` (method) `modules/ai_model.py:341` `def generate(self, prompt)`
- `AnthropicModel.stream_generate` (method) `modules/ai_model.py:353` `def stream_generate(self, prompt)`
- `AnthropicModel.complete` (method) `modules/ai_model.py:367` `def complete(self, system, user, max_tokens, temperature)`
- `DeepSeekModel.__init__` (method) `modules/ai_model.py:394` `def __init__(self, api_key, model)`
- `DeepSeekModel.generate` (method) `modules/ai_model.py:401` `def generate(self, prompt)`
- `DeepSeekModel.stream_generate` (method) `modules/ai_model.py:412` `def stream_generate(self, prompt)`
- `DeepSeekModel.complete` (method) `modules/ai_model.py:427` `def complete(self, system, user, max_tokens, temperature)`

## modules/amsi.c
- `LoadNtFunctions` (function) `modules/amsi.c:38` `void LoadNtFunctions()` -- Función para cargar las funciones dinámicamente
- `AMS1patch_OpenSession_jne` (function) `modules/amsi.c:66` `void AMS1patch_OpenSession_jne(HANDLE hproc)` -- Técnica de Saad, también conocido como @D1rkMtr (https://twitter.com/D1rkMtr/)...
- `AMS1patch_OpenSession_ret` (function) `modules/amsi.c:116` `void AMS1patch_OpenSession_ret(HANDLE hproc)`
- `AMS1patch_ScanBuffer_ret` (function) `modules/amsi.c:166` `void AMS1patch_ScanBuffer_ret(HANDLE hproc)`
- `AMS1patch_RastaMouse` (function) `modules/amsi.c:215` `void AMS1patch_RastaMouse(HANDLE hproc)`
- `AMS1patch_E_ACCESSDENIED` (function) `modules/amsi.c:274` `void AMS1patch_E_ACCESSDENIED(HANDLE hproc)`
- `AMS1patch_E_HANDLE` (function) `modules/amsi.c:326` `void AMS1patch_E_HANDLE(HANDLE hproc)`
- `AMS1patch_E_OUTOFMEMORY` (function) `modules/amsi.c:378` `void AMS1patch_E_OUTOFMEMORY(HANDLE hproc)`
- `main` (function) `modules/amsi.c:428` `int main(int argc, char** argv)`

## modules/amt_auth_bypass.py
- `start` (function) `modules/amt_auth_bypass.py:4` `def start()`
- `BlankAuthResponse.request` (method) `modules/amt_auth_bypass.py:11` `def request(self, flow)`

## modules/apt_playbooks.py
Depends on: `core/console.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `cli/recommendation_signals.py`, `modules/operation.py`
- `AptPlaybook.from_dict` (method) `modules/apt_playbooks.py:74` `def from_dict(cls, data)`
- `AptPlaybook.to_summary` (method) `modules/apt_playbooks.py:99` `def to_summary(self)`
- `AptPlaybookEngine.__init__` (method) `modules/apt_playbooks.py:114` `def __init__(self, playbook_dir)`
- `AptPlaybookEngine.list_playbooks` (method) `modules/apt_playbooks.py:131` `def list_playbooks(self)`
- `AptPlaybookEngine.get` (method) `modules/apt_playbooks.py:134` `def get(self, name)`
- `AptPlaybookEngine.validate` (method) `modules/apt_playbooks.py:138` `def validate(self, pb, atomic_path)` -- Validate that all referenced atomic tests exist locally.
- `AptPlaybookEngine.generate_attack_plan` (method) `modules/apt_playbooks.py:189` `def generate_attack_plan(self, pb, output_path)` -- Generate a legacy ``attack_plan.yaml`` from an enriched APT playbook.
- `AptPlaybookEngine.report_json` (method) `modules/apt_playbooks.py:204` `def report_json(self, pb, output_path)` -- Write a structured JSON report of the playbook for the operator.

## modules/atomic_enricher.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `tests/test_core_modules.py`
- `enrich` (function) `modules/atomic_enricher.py:173` `def enrich(force)` -- Build enriched parquet.
- `load_enriched` (function) `modules/atomic_enricher.py:215` `def load_enriched()` -- Load enriched parquet, building it first if it doesn't exist.
- `query_atomic` (function) `modules/atomic_enricher.py:232` `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` -- Structured query over the enriched Atomic Red Team technique catalogue.

## modules/auto_pivot.py
Imported by: `modules/autonomous_exploit_engine.py`, `skills/lazyown_mcp.py`
- `AutoPivotEngine.__init__` (method) `modules/auto_pivot.py:73` `def __init__(self, config)`
- `AutoPivotEngine.set_config` (method) `modules/auto_pivot.py:82` `def set_config(self, config)`
- `AutoPivotEngine.add_pivot_node` (method) `modules/auto_pivot.py:90` `def add_pivot_node(self, ip, access_type, credential_id, hostname)`
- `AutoPivotEngine.remove_pivot_node` (method) `modules/auto_pivot.py:120` `def remove_pivot_node(self, ip)`
- `AutoPivotEngine.discover_subnets` (method) `modules/auto_pivot.py:128` `def discover_subnets(self, node_ip, command_output)`
- `AutoPivotEngine.build_chain` (method) `modules/auto_pivot.py:146` `def build_chain(self, target_ip, via_nodes, subnet)`
- `AutoPivotEngine.generate_proxychains_config` (method) `modules/auto_pivot.py:177` `def generate_proxychains_config(self, chain_id)`
- `AutoPivotEngine.generate_sshuttle_command` (method) `modules/auto_pivot.py:203` `def generate_sshuttle_command(self, node_ip, subnet)`
- `AutoPivotEngine.generate_chisel_command` (method) `modules/auto_pivot.py:206` `def generate_chisel_command(self, target_ip, local_port)`
- `AutoPivotEngine.generate_ssh_socks_command` (method) `modules/auto_pivot.py:212` `def generate_ssh_socks_command(self, node_ip, local_port)`
- `AutoPivotEngine.health_check` (method) `modules/auto_pivot.py:216` `def health_check(self, node_ip)`
- `AutoPivotEngine.health_check_all` (method) `modules/auto_pivot.py:237` `def health_check_all(self)`
- `AutoPivotEngine.get_active_routes` (method) `modules/auto_pivot.py:243` `def get_active_routes(self)`
- `AutoPivotEngine.get_reachable_hosts` (method) `modules/auto_pivot.py:259` `def get_reachable_hosts(self, node_ip)`
- `AutoPivotEngine.set_reachable_hosts` (method) `modules/auto_pivot.py:267` `def set_reachable_hosts(self, node_ip, hosts)`
- `AutoPivotEngine.set_route_priority` (method) `modules/auto_pivot.py:272` `def set_route_priority(self, node_ip, priority)`
- `AutoPivotEngine.suggest_next_pivot` (method) `modules/auto_pivot.py:352` `def suggest_next_pivot(self)`

## modules/auto_purple.py
Depends on: `core/config.py`, `core/logging.py`, `core/process.py`, `modules/detection_oracle.py`
Imported by: `cli/commands/purple_team.py`
- `PurpleResult.to_csv_row` (method) `modules/auto_purple.py:146` `def to_csv_row(self)` -- Serialize to a flat dict suitable for CSV writer.
- `PurpleResult.to_dict` (method) `modules/auto_purple.py:160` `def to_dict(self)`
- `IPurpleLoop.execute_and_measure` (method) `modules/auto_purple.py:185` `def execute_and_measure(self, command, args, category)`
- `IPurpleLoop.measure_only` (method) `modules/auto_purple.py:193` `def measure_only(self, command, args, category)`
- `IPurpleLoop.engagement_score` (method) `modules/auto_purple.py:201` `def engagement_score(self)`
- `IPurpleLoop.export_dataset` (method) `modules/auto_purple.py:204` `def export_dataset(self)`
- `IPurpleLoop.export_report` (method) `modules/auto_purple.py:207` `def export_report(self)`
- `IPurpleEvaluator.last_results` (method) `modules/auto_purple.py:214` `def last_results(self, n)`
- `IPurpleEvaluator.category_accuracy` (method) `modules/auto_purple.py:217` `def category_accuracy(self, category)`
- `PurpleTeamLoop.__init__` (method) `modules/auto_purple.py:414` `def __init__(self, bt_path, detection_delay, methods, auto_feedback, session_id)`
- `PurpleTeamLoop.execute_and_measure` (method) `modules/auto_purple.py:443` `def execute_and_measure(self, command, args, category)` -- Execute a red action and measure if LazyOwnBT detects it.
- `PurpleTeamLoop.measure_only` (method) `modules/auto_purple.py:493` `def measure_only(self, command, args, category)` -- Measure without executing — test if BT would detect the command.
- `PurpleTeamLoop.engagement_score` (method) `modules/auto_purple.py:529` `def engagement_score(self)` -- Aggregate detection score from all results in this session.
- `PurpleTeamLoop.export_dataset` (method) `modules/auto_purple.py:567` `def export_dataset(self)` -- Return the path to the CSV dataset file.
- `PurpleTeamLoop.export_report` (method) `modules/auto_purple.py:571` `def export_report(self)` -- Generate a full engagement report.
- `PurpleTeamLoop.last_results` (method) `modules/auto_purple.py:596` `def last_results(self, n)`
- `PurpleTeamLoop.category_accuracy` (method) `modules/auto_purple.py:599` `def category_accuracy(self, category)`
- `PurpleTeamLoop.get_loop` (method) `modules/auto_purple.py:772` `def get_loop(bt_path, detection_delay, methods, auto_feedback)` -- Return (or create) the module-level PurpleTeamLoop singleton.
- `PurpleTeamLoop.load_config_from_payload` (method) `modules/auto_purple.py:790` `def load_config_from_payload(params)` -- Extract purple_team config from payload.json params dict.

## modules/autonomous_exploit_engine.py
Depends on: `core/safe_exec.py`, `modules/auto_pivot.py`, `modules/db.py`
Imported by: `cli/commands/pwn.py`, `cli/commands/session_ops.py`, `modules/ai_exploit_chain.py`, `skills/lazyown_mcp.py`, `tests/test_phase1_data_gaps.py`
- `AutonomousExploitEngine.__init__` (method) `modules/autonomous_exploit_engine.py:113` `def __init__(self)`
- `AutonomousExploitEngine.get_instance` (method) `modules/autonomous_exploit_engine.py:133` `def get_instance(cls)`
- `AutonomousExploitEngine.hunt` (method) `modules/autonomous_exploit_engine.py:144` `def hunt(self, target, max_exploits)` -- Execute a full autonomous exploitation chain against a target.
- `AutonomousExploitEngine.retry_with_credentials` (method) `modules/autonomous_exploit_engine.py:181` `def retry_with_credentials(self, target, credentials)` -- Re-execute exploit chain using captured credentials.
- `AutonomousExploitEngine.profile` (method) `modules/autonomous_exploit_engine.py:325` `def profile(self, target)` -- Build a TargetProfile from existing recon data.
- `AutonomousExploitEngine.rank_exploits` (method) `modules/autonomous_exploit_engine.py:386` `def rank_exploits(self, profile)` -- Rank exploit candidates by confidence for a given profile.
- `AutonomousExploitEngine.execute_candidate` (method) `modules/autonomous_exploit_engine.py:409` `def execute_candidate(self, candidate, profile)` -- Execute a single exploit candidate and return the result.
- `AutonomousExploitEngine.scan_vulnerabilities` (method) `modules/autonomous_exploit_engine.py:1645` `def scan_vulnerabilities(self, profile)` -- Scan for vulnerabilities using NSE output and heuristic version matching.
- `AutonomousExploitEngine.chain_privesc` (method) `modules/autonomous_exploit_engine.py:1960` `def chain_privesc(self, profile, session_id)` -- Run privilege escalation checks and attempt escalation techniques.
- `AutonomousExploitEngine.trigger_pivot` (method) `modules/autonomous_exploit_engine.py:2390` `def trigger_pivot(self, profile, session_id)` -- Discover internal interfaces and trigger auto-pivoting through a compromised host.
- `AutonomousExploitEngine.enable_stealth` (method) `modules/autonomous_exploit_engine.py:2516` `def enable_stealth(self, stealth_level)` -- Configure the engine's stealth level for evasion.
- `AutonomousExploitEngine.full_auto_pwn` (method) `modules/autonomous_exploit_engine.py:2580` `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth)` -- Execute the full autonomous exploit chain against a target.

## modules/aws_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `AWSAttackEngine.__init__` (method) `modules/aws_attacks.py:91` `def __init__(self, config)`
- `AWSAttackEngine.enumerate_iam_permissions` (method) `modules/aws_attacks.py:95` `def enumerate_iam_permissions(self)` -- Enumerate IAM permissions for the current user/role.
- `AWSAttackEngine.lambda_backdoor` (method) `modules/aws_attacks.py:127` `def lambda_backdoor(self, function_name)` -- Plan a Lambda backdoor for privilege escalation.
- `AWSAttackEngine.sts_role_chain` (method) `modules/aws_attacks.py:155` `def sts_role_chain(self, target_role_arn)` -- Enumerate and exploit STS AssumeRole privilege escalation chains.
- `AWSAttackEngine.ec2_user_data_exfil` (method) `modules/aws_attacks.py:181` `def ec2_user_data_exfil(self)` -- Extract sensitive data from EC2 instance user data and metadata.
- `AWSAttackEngine.s3_enumeration` (method) `modules/aws_attacks.py:206` `def s3_enumeration(self)` -- Enumerate S3 buckets and their permissions.
- `AWSAttackEngine.cloudformation_drift` (method) `modules/aws_attacks.py:242` `def cloudformation_drift(self)` -- Exploit CloudFormation for privilege escalation.
- `AWSAttackEngine.ec2_ssm_session_abuse` (method) `modules/aws_attacks.py:274` `def ec2_ssm_session_abuse(self)` -- Abuse SSM to gain shell access to EC2 instances.
- `AWSAttackEngine.summary` (method) `modules/aws_attacks.py:293` `def summary(self)`

## modules/backdoor/backdoor.c
Depends on: `modules/backdoor/keylogger.h`
- `bootRun` (function) `modules/backdoor/backdoor.c:18` `int bootRun()`
- `str_cut` (function) `modules/backdoor/backdoor.c:49` `char *
str_cut(char str[], int slice_from, int slice_to)`
- `Shell` (function) `modules/backdoor/backdoor.c:84` `void Shell()`
- `WinMain` (function) `modules/backdoor/backdoor.c:125` `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)`

## modules/backdoor/keylogger.h
Imported by: `modules/backdoor/backdoor.c`
- `logg` (function) `modules/backdoor/keylogger.h:1` `DWORD WINAPI logg(LPVOID lpParam)`

## modules/backdoor/server.c
Imported by: `cli/commands/dns_exfil.py`, `cli/commands/phishing_wizard.py`, `contrib/legacy/lazygalazy.py`, `contrib/legacy/lazyhttpreverseshell.py`, `lazyc2.py`, `modules/lazyown_bprfuzzer.py`, `skills/hermes-lazyown/mcp_server.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_opencode.py`, `utils.py`
- `main` (function) `modules/backdoor/server.c:10` `int main()`

## modules/beacon_config_builder.py
Depends on: `core/config.py`, `core/logging.py`, `modules/c2_profile_engine.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`
Imported by: `cli/commands/bof_registry.py`, `tests/test_beacon_config_builder.py`
- `BeaconConfig.to_gen_beacon_args` (method) `modules/beacon_config_builder.py:117` `def to_gen_beacon_args(self)` -- Produce CLI arguments for gen_beacon.sh.
- `BeaconConfig.to_go_implant_vars` (method) `modules/beacon_config_builder.py:137` `def to_go_implant_vars(self)` -- Produce template variables for the Go implant builder.
- `BeaconConfig.to_config_json` (method) `modules/beacon_config_builder.py:160` `def to_config_json(self)` -- Produce the config.json that beacons fetch on startup.
- `BeaconConfig.to_dict` (method) `modules/beacon_config_builder.py:185` `def to_dict(self)` -- Full serialization of beacon config.
- `BeaconConfigBuilder.__init__` (method) `modules/beacon_config_builder.py:245` `def __init__(self, payload)`
- `BeaconConfigBuilder.build` (method) `modules/beacon_config_builder.py:248` `def build(self, name)` -- Build a complete BeaconConfig.
- `BeaconConfigBuilder.from_payload` (method) `modules/beacon_config_builder.py:403` `def from_payload(cls, payload)` -- Build a BeaconConfigBuilder from a payload dictionary.
- `BeaconConfigBuilder.from_payload_file` (method) `modules/beacon_config_builder.py:408` `def from_payload_file(cls, path)` -- Build a BeaconConfigBuilder by loading payload.json from disk.
- `BeaconConfigBuilder.generate_bof_execution_command` (method) `modules/beacon_config_builder.py:416` `def generate_bof_execution_command(bof_name, c2_url, client_id, args, bofs_dir)` -- Generate a ``bof:<url>`` command that the C beacon executes.

## modules/beacon_history.py
Depends on: `core/logging.py`
Imported by: `lazyc2.py`, `lazyc2/blueprints/api_v1.py`, `tests/test_api_v1.py`, `tests/test_beacon_history.py`, `tests/test_security_lazyc2.py`
- `BeaconHistoryConfig.sessions_dir` (method) `modules/beacon_history.py:39` `def sessions_dir(self)` -- Return the resolved sessions directory under the base dir.
- `BeaconHistoryConfig.records_path` (method) `modules/beacon_history.py:43` `def records_path(self, client_id)` -- Resolve the history file path for a sanitised beacon client id.
- `BeaconHistoryConfig.sanitize_client_id` (method) `modules/beacon_history.py:70` `def sanitize_client_id(client_id)` -- Sanitise a beacon id to only URL/file-safe characters.
- `BeaconHistoryConfig.append_record` (method) `modules/beacon_history.py:82` `def append_record(record, config)` -- Append one beacon result record to the persistent JSONL history.
- `BeaconHistoryConfig.read_records` (method) `modules/beacon_history.py:116` `def read_records(client_id, config)` -- Read the ordered JSONL history for a beacon client id (oldest first).
- `BeaconHistoryConfig.records_path` (method) `modules/beacon_history.py:145` `def records_path(client_id, config)` -- Resolve the history file path for a beacon client id.

## modules/bin2img.py
- `binario_a_imagen` (function) `modules/bin2img.py:7` `def binario_a_imagen(binario, imagen_input, imagen_output, block_size)`
- `main` (function) `modules/bin2img.py:54` `def main()`

## modules/bitm_engine.py
Imported by: `cli/commands/bitm.py`
- `BitMState.bitm_start` (method) `modules/bitm_engine.py:257` `def bitm_start(target_ip, gateway_ip, interface, lhost, lport, method, payloads)` -- Start a Browser-in-the-Middle attack.
- `BitMState.bitm_stop` (method) `modules/bitm_engine.py:481` `def bitm_stop()` -- Stop a running BitM attack and clean up iptables.
- `BitMState.bitm_status` (method) `modules/bitm_engine.py:539` `def bitm_status()` -- Return the current BitM attack status.
- `BitMState.bitm_inject` (method) `modules/bitm_engine.py:572` `def bitm_inject(payload_name)` -- Inject an additional JS payload into an active BitM session.
- `BitMState.bitm_harvest_stats` (method) `modules/bitm_engine.py:607` `def bitm_harvest_stats()` -- Return statistics on harvested credentials from the active/past campaign.
- `BitMState.bitm_cleanup` (method) `modules/bitm_engine.py:642` `def bitm_cleanup()` -- Force-kill all BitM processes and remove the state file.
- `BitMState.main` (method) `modules/bitm_engine.py:661` `def main()` -- CLI entry point — display BitM status from command line.

## modules/bof_registry.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/bof_registry.py`, `tests/test_bof_registry.py`
- `BofEntry.to_dict` (method) `modules/bof_registry.py:118` `def to_dict(self)` -- Serialize to dictionary.
- `BofEntry.from_dict` (method) `modules/bof_registry.py:137` `def from_dict(cls, raw)` -- Build from a dictionary.
- `BofCatalog.register` (method) `modules/bof_registry.py:167` `def register(self, entry)` -- Register a BOF entry in the catalog.
- `BofCatalog.register_many` (method) `modules/bof_registry.py:172` `def register_many(self, entries)` -- Register multiple BOF entries at once.
- `BofCatalog.get` (method) `modules/bof_registry.py:177` `def get(self, name)` -- Retrieve a BOF entry by name.
- `BofCatalog.search` (method) `modules/bof_registry.py:188` `def search(self, query)` -- Search catalog by keyword across name, description, and technique.
- `BofCatalog.list_by_category` (method) `modules/bof_registry.py:221` `def list_by_category(self, category)` -- Return all BOFs in a specific category.
- `BofCatalog.list_by_platform` (method) `modules/bof_registry.py:225` `def list_by_platform(self, platform)` -- Return all BOFs for a specific platform.
- `BofCatalog.list_all` (method) `modules/bof_registry.py:229` `def list_all(self)` -- Return all catalog entries sorted by name.
- `BofCatalog.to_dict` (method) `modules/bof_registry.py:233` `def to_dict(self)` -- Serialize the entire catalog to a dictionary.
- `BofCatalog.from_dict` (method) `modules/bof_registry.py:241` `def from_dict(cls, raw)` -- Build a catalog from a dictionary.
- `BofCatalog.load` (method) `modules/bof_registry.py:249` `def load(cls, path)` -- Load a catalog from a JSON file.
- `BofCatalog.save` (method) `modules/bof_registry.py:257` `def save(self, path)` -- Save the catalog to a JSON file.
- `BofValidator.compute_sha256` (method) `modules/bof_registry.py:515` `def compute_sha256(filepath)` -- Compute the SHA-256 hash of a file.
- `BofValidator.verify_entry` (method) `modules/bof_registry.py:524` `def verify_entry(entry, filepath)` -- Verify the SHA-256 of a downloaded BOF source matches the catalog.
- `BofValidator.validate_args` (method) `modules/bof_registry.py:540` `def validate_args(entry, args)` -- Validate that all required arguments are supplied.
- `BofRegistry.__init__` (method) `modules/bof_registry.py:559` `def __init__(self, sessions_dir)`
- `BofRegistry.install_dir` (method) `modules/bof_registry.py:565` `def install_dir(self)` -- Return the BOF installation directory.
- `BofRegistry.is_installed` (method) `modules/bof_registry.py:585` `def is_installed(self, name)` -- Return True if a BOF is installed.
- `BofRegistry.install` (method) `modules/bof_registry.py:590` `def install(self, entry)` -- Register a BOF as installed with current timestamp.
- `BofRegistry.uninstall` (method) `modules/bof_registry.py:611` `def uninstall(self, name, remove_files)` -- Unregister a BOF from the manifest and optionally remove its files.
- `BofRegistry.list_installed` (method) `modules/bof_registry.py:628` `def list_installed(self)` -- Return a list of all installed BOFs with metadata.
- `BofRegistry.get_install_info` (method) `modules/bof_registry.py:633` `def get_install_info(self, name)` -- Return installation metadata for a BOF, or None if not installed.
- `BofMarketplace.__init__` (method) `modules/bof_registry.py:651` `def __init__(self, sessions_dir, catalog)`
- `BofMarketplace.catalog` (method) `modules/bof_registry.py:662` `def catalog(self)` -- Return the catalog.
- `BofMarketplace.registry` (method) `modules/bof_registry.py:667` `def registry(self)` -- Return the registry.
- `BofMarketplace.search` (method) `modules/bof_registry.py:671` `def search(self, query)` -- Search the catalog and return enriched results with install status.
- `BofMarketplace.info` (method) `modules/bof_registry.py:690` `def info(self, name)` -- Get detailed information about a BOF by name.
- `BofMarketplace.install` (method) `modules/bof_registry.py:707` `def install(self, name)` -- Install a BOF from the catalog by name.
- `BofMarketplace.uninstall` (method) `modules/bof_registry.py:736` `def uninstall(self, name)` -- Uninstall a BOF by name.
- `BofMarketplace.list_installed` (method) `modules/bof_registry.py:749` `def list_installed(self)` -- List all installed BOFs with catalog enrichment.
- `BofMarketplace.list_missing_dependencies` (method) `modules/bof_registry.py:761` `def list_missing_dependencies(self, name)` -- Return a list of dependencies for a BOF that are not installed.
- `BofMarketplace.bulk_install` (method) `modules/bof_registry.py:769` `def bulk_install(self, names)` -- Install multiple BOFs at once.

## modules/bot.py
- `BotConfig.find_new_repos` (method) `modules/bot.py:48` `def find_new_repos(language, days, count, order, config)` -- Search GitHub for recently created repositories.
- `BotConfig.render_repos` (method) `modules/bot.py:102` `def render_repos(repos, config)` -- Render repository summaries to text and persist them to disk.
- `BotConfig.format_output` (method) `modules/bot.py:128` `def format_output(content, config)` -- Pipe rendered content through the external formatter when available.
- `BotConfig.main` (method) `modules/bot.py:148` `def main(config)` -- Discover recent repositories and render them.

## modules/c2_builder.py
Depends on: `core/validators.py`, `modules/metrics.py`, `utils.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `tests/test_bdd_infra_range_report.py`, `tests/test_infra_disposable.py`
- `C2Builder.__init__` (method) `modules/c2_builder.py:395` `def __init__(self, params, sessions_dir, cmd_fn, onecmd_fn, toastr_fn, c2_user, c2_pass)`
- `C2Builder.run` (method) `modules/c2_builder.py:453` `def run(self, line, choice, use_tunnel)` -- Execute the full C2 build pipeline.

## modules/c2_messaging_base.py
- `SecureSessionManager.__init__` (method) `modules/c2_messaging_base.py:22` `def __init__(self, max_failed_attempts, lockout_duration, rate_limit, session_timeout)`
- `SecureSessionManager.register_failed_attempt` (method) `modules/c2_messaging_base.py:37` `def register_failed_attempt(self, user_id)` -- Record a failed authentication attempt for a user.
- `SecureSessionManager.check_lockout` (method) `modules/c2_messaging_base.py:46` `def check_lockout(self, user_id)` -- Check if a user is currently locked out due to failed attempts.
- `SecureSessionManager.check_rate_limit` (method) `modules/c2_messaging_base.py:61` `def check_rate_limit(self, user_id)` -- Check if a user has exceeded the command rate limit.
- `SecureSessionManager.create_session` (method) `modules/c2_messaging_base.py:79` `def create_session(self, user_id, client_id)` -- Create a new authenticated session for a user.
- `SecureSessionManager.validate_session` (method) `modules/c2_messaging_base.py:89` `def validate_session(self, user_id)` -- Check if a user session is still valid and refresh activity timestamp.
- `SecureSessionManager.set_client` (method) `modules/c2_messaging_base.py:106` `def set_client(self, user_id, client_id)` -- Assign a target C2 client to a user session.
- `SecureSessionManager.get_client` (method) `modules/c2_messaging_base.py:111` `def get_client(self, user_id)` -- Get the target C2 client assigned to a user session.
- `PayloadConfigAdapter.__init__` (method) `modules/c2_messaging_base.py:124` `def __init__(self, config_dict)`
- `PayloadConfigAdapter.get` (method) `modules/c2_messaging_base.py:132` `def get(self, key, default)`

## modules/c2_profile.py
Depends on: `core/logging.py`
- `C2Profile.jitter_delay` (method) `modules/c2_profile.py:101` `def jitter_delay(self)` -- Return the next sleep delay as a float in seconds.
- `C2Profile.get_uri` (method) `modules/c2_profile.py:117` `def get_uri(self, method)` -- Pick a random URI path from the appropriate HttpConfig.
- `C2Profile.build_headers` (method) `modules/c2_profile.py:128` `def build_headers(self, method)` -- Return the headers dict for the given HTTP method.
- `ProfileValidator.validate` (method) `modules/c2_profile.py:162` `def validate(self, profile)`
- `ProfileLoader.from_yaml` (method) `modules/c2_profile.py:200` `def from_yaml(path)` -- Load a C2Profile from a YAML file at *path*.
- `ProfileLoader.from_dict` (method) `modules/c2_profile.py:215` `def from_dict(d)` -- Construct a C2Profile from a plain Python dictionary.
- `ProfileLoader.to_dict` (method) `modules/c2_profile.py:254` `def to_dict(profile)` -- Convert a C2Profile to a plain Python dictionary.
- `ProfileLoader.save` (method) `modules/c2_profile.py:282` `def save(profile, path)` -- Serialise *profile* to a YAML file and return the written path.
- `ProfileRegistry.__init__` (method) `modules/c2_profile.py:457` `def __init__(self)`
- `ProfileRegistry.register` (method) `modules/c2_profile.py:464` `def register(self, name, profile)` -- Register *profile* under *name*, overwriting any previous entry.
- `ProfileRegistry.get` (method) `modules/c2_profile.py:473` `def get(self, name)` -- Return the profile registered under *name*.
- `ProfileRegistry.list_names` (method) `modules/c2_profile.py:485` `def list_names(self)` -- Return a sorted list of all registered profile names.
- `ProfileRegistry.load_from_directory` (method) `modules/c2_profile.py:493` `def load_from_directory(self, path)` -- Scan *path* for *.yaml files and register each as a profile.
- `ProfileApplier.apply_to_response` (method) `modules/c2_profile.py:529` `def apply_to_response(profile, response)` -- Patch the headers of a Flask response object to match the profile.
- `ProfileApplier.apply_to_session` (method) `modules/c2_profile.py:554` `def apply_to_session(profile, session)` -- Configure a requests.Session to mimic the profile's HTTP GET behavior.
- `ProfileApplier.get_beacon_config` (method) `modules/c2_profile.py:567` `def get_beacon_config(profile)` -- Return a JSON-serialisable dict suitable for embedding in a beacon handshake response.
- `ProfileApplier.get_registry` (method) `modules/c2_profile.py:595` `def get_registry()` -- Return the module-level singleton ProfileRegistry.
- `ProfileApplier.get_profile` (method) `modules/c2_profile.py:620` `def get_profile(name)` -- Return the named profile from the module singleton registry.
- `ProfileApplier.list_profiles` (method) `modules/c2_profile.py:625` `def list_profiles()` -- Return a sorted list of all registered profile names.

## modules/c2_profile_engine.py
Depends on: `cli/commands/enum.py`, `core/config.py`, `core/logging.py`
Imported by: `cli/commands/c2_profile.py`, `modules/beacon_config_builder.py`, `tests/test_c2_profile_engine.py`
- `TlsProfile.get_cipher_suites` (method) `modules/c2_profile_engine.py:144` `def get_cipher_suites(self)` -- Return cipher suites, resolving library alias if set.
- `TlsProfile.get_ja3_hash` (method) `modules/c2_profile_engine.py:155` `def get_ja3_hash(self)` -- Compute a JA3 fingerprint hash from the current profile.
- `TlsProfile.from_dict` (method) `modules/c2_profile_engine.py:173` `def from_dict(raw)` -- Build a TlsProfile from a configuration dictionary.
- `TlsProfile.to_dict` (method) `modules/c2_profile_engine.py:188` `def to_dict(self)` -- Serialize this profile to a plain dictionary.
- `DnsProfile.build_query_subdomain` (method) `modules/c2_profile_engine.py:231` `def build_query_subdomain(self, data, packet_id)` -- Build a DNS query subdomain from encoded data and a packet ID.
- `DnsProfile.from_dict` (method) `modules/c2_profile_engine.py:261` `def from_dict(raw)` -- Build a DnsProfile from a configuration dictionary.
- `DnsProfile.to_dict` (method) `modules/c2_profile_engine.py:274` `def to_dict(self)` -- Serialize this profile to a plain dictionary.
- `SmbProfile.from_dict` (method) `modules/c2_profile_engine.py:319` `def from_dict(raw)` -- Build an SmbProfile from a configuration dictionary.
- `SmbProfile.to_dict` (method) `modules/c2_profile_engine.py:333` `def to_dict(self)` -- Serialize this profile to a plain dictionary.
- `WebSocketProfile.from_dict` (method) `modules/c2_profile_engine.py:375` `def from_dict(raw)` -- Build a WebSocketProfile from a configuration dictionary.
- `WebSocketProfile.to_dict` (method) `modules/c2_profile_engine.py:389` `def to_dict(self)` -- Serialize this profile to a plain dictionary.
- `RotationSlot.is_available` (method) `modules/c2_profile_engine.py:429` `def is_available(self)` -- Return True if the cooldown window has elapsed.
- `RotationSlot.touch` (method) `modules/c2_profile_engine.py:436` `def touch(self)` -- Mark this slot as just used.
- `ProfileRotator.__init__` (method) `modules/c2_profile_engine.py:453` `def __init__(self, slots)`
- `ProfileRotator.current_slot` (method) `modules/c2_profile_engine.py:460` `def current_slot(self)` -- Return the currently active rotation slot.
- `ProfileRotator.transport` (method) `modules/c2_profile_engine.py:465` `def transport(self)` -- Return the transport type of the current slot.
- `ProfileRotator.rotate` (method) `modules/c2_profile_engine.py:469` `def rotate(self)` -- Advance to the next available slot and return it.
- `ProfileRotator.list_slots` (method) `modules/c2_profile_engine.py:487` `def list_slots(self)` -- Return a list of slot states for inspection.
- `ProfileValidator.validate_tls` (method) `modules/c2_profile_engine.py:511` `def validate_tls(profile)` -- Validate a TlsProfile and return error messages.
- `ProfileValidator.validate_dns` (method) `modules/c2_profile_engine.py:536` `def validate_dns(profile)` -- Validate a DnsProfile and return error messages.
- `ProfileValidator.validate_smb` (method) `modules/c2_profile_engine.py:556` `def validate_smb(profile)` -- Validate an SmbProfile and return error messages.
- `ProfileValidator.validate_websocket` (method) `modules/c2_profile_engine.py:576` `def validate_websocket(profile)` -- Validate a WebSocketProfile and return error messages.
- `ProfileValidator.validate_all` (method) `modules/c2_profile_engine.py:591` `def validate_all(self, tls, dns, smb, websocket)` -- Validate all provided profiles and return a dict of transport -> errors.
- `ProfileEngine.__init__` (method) `modules/c2_profile_engine.py:627` `def __init__(self, tls_profile, dns_profile, smb_profile, websocket_profile, rotation_slots)`
- `ProfileEngine.tls_profile` (method) `modules/c2_profile_engine.py:643` `def tls_profile(self)` -- Return the current TLS profile.
- `ProfileEngine.dns_profile` (method) `modules/c2_profile_engine.py:648` `def dns_profile(self)` -- Return the current DNS profile.
- `ProfileEngine.smb_profile` (method) `modules/c2_profile_engine.py:653` `def smb_profile(self)` -- Return the current SMB profile.
- `ProfileEngine.websocket_profile` (method) `modules/c2_profile_engine.py:658` `def websocket_profile(self)` -- Return the current WebSocket profile.
- `ProfileEngine.rotator` (method) `modules/c2_profile_engine.py:663` `def rotator(self)` -- Return the profile rotator.
- `ProfileEngine.active_transport` (method) `modules/c2_profile_engine.py:668` `def active_transport(self)` -- Return the currently active transport type.
- `ProfileEngine.rotate` (method) `modules/c2_profile_engine.py:672` `def rotate(self)` -- Advance to the next transport in the rotation queue.
- `ProfileEngine.validate` (method) `modules/c2_profile_engine.py:676` `def validate(self)` -- Validate all transport profiles and return error dict.
- `ProfileEngine.get_active_profile_dict` (method) `modules/c2_profile_engine.py:685` `def get_active_profile_dict(self)` -- Return a JSON-serializable dict of the active transport config.
- `ProfileEngine.get_all_profiles_dict` (method) `modules/c2_profile_engine.py:699` `def get_all_profiles_dict(self)` -- Return a JSON-serializable dict of all profiles.
- `ProfileEngine.from_dict` (method) `modules/c2_profile_engine.py:747` `def from_dict(cls, raw)` -- Build a ProfileEngine from a configuration dictionary.
- `ProfileEngine.from_payload` (method) `modules/c2_profile_engine.py:766` `def from_payload(cls, payload)` -- Build a ProfileEngine from a LazyOwn payload configuration dict.
- `ProfileEngine.from_config` (method) `modules/c2_profile_engine.py:771` `def from_config(cls, config)` -- Build a ProfileEngine from a LazyOwn Config object.

## modules/cal.sh
- `is_leap_year` (function) `modules/cal.sh:4` -- Función para calcular si un año es bisiesto
- `days_in_month` (function) `modules/cal.sh:14` -- Función para obtener el número de días en un mes
- `first_day_of_month` (function) `modules/cal.sh:31` -- Función para obtener el día de la semana del primer día del mes

## modules/cicd_enumerator.py
Imported by: `cli/commands/cicd.py`
- `CICDEnumerator.__init__` (method) `modules/cicd_enumerator.py:54` `def __init__(self, target_url, sessions_dir)`
- `CICDEnumerator.scan` (method) `modules/cicd_enumerator.py:60` `def scan(self)` -- Run all CI/CD scans.
- `CICDEnumerator.scan_build_log` (method) `modules/cicd_enumerator.py:297` `def scan_build_log(self, log_content, source)` -- Scan a build log for leaked secrets.
- `CICDEnumerator.generate_ci_attack_matrix` (method) `modules/cicd_enumerator.py:322` `def generate_ci_attack_matrix(self)` -- Generate a comprehensive CI/CD attack matrix.
- `CICDEnumerator.export_findings` (method) `modules/cicd_enumerator.py:387` `def export_findings(self)` -- Export CI/CD findings to a JSON file.

## modules/cli_auth.py
Depends on: `cli/engagement_hooks.py`, `modules/lazy_rbac.py`
Imported by: `cli/auto_crypto.py`, `cli/banner_config.py`, `cli/commands/cli_auth.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `cli/wizard.py`, `lazyown.py`, `modules/redteam_gym.py`, `tests/test_engagement_elo_and_methodology.py`
- `user_exists` (function) `modules/cli_auth.py:118` `def user_exists(username)` -- Check if a username already exists in users.json or RBAC store.
- `register` (function) `modules/cli_auth.py:141` `def register(username, password)` -- Register a new operator in users.json.
- `verify_password` (function) `modules/cli_auth.py:210` `def verify_password(username, password)` -- Verify a username/password against users.json using werkzeug.
- `login` (function) `modules/cli_auth.py:236` `def login(username, password, remember)` -- Authenticate a CLI operator and optionally persist a remember-me token.
- `logout` (function) `modules/cli_auth.py:289` `def logout()` -- Log out the current CLI operator and clear the remember-me token.
- `try_auto_login` (function) `modules/cli_auth.py:324` `def try_auto_login()` -- Attempt auto-login using the remember-me token from payload.json.
- `whoami` (function) `modules/cli_auth.py:362` `def whoami()` -- Return the currently logged-in CLI operator's identity.
- `get_current_operator` (function) `modules/cli_auth.py:392` `def get_current_operator()` -- Return the current operator username, or None if not logged in.
- `sync_elo_from_session` (function) `modules/cli_auth.py:404` `def sync_elo_from_session(elo)` -- Update the CLI session ELO from engagement state.
- `needs_login` (function) `modules/cli_auth.py:483` `def needs_login()` -- Check if the current session has a logged-in operator.

## modules/cloud_enum.py
Imported by: `cli/commands/cloud.py`
- `CloudEnumerator.__init__` (method) `modules/cloud_enum.py:34` `def __init__(self, provider, session, timeout)`
- `CloudEnumerator.detect_provider` (method) `modules/cloud_enum.py:47` `def detect_provider(self)` -- Auto-detect which cloud provider the host is running on.
- `CloudEnumerator.enumerate_metadata` (method) `modules/cloud_enum.py:75` `def enumerate_metadata(self)` -- Enumerate cloud instance metadata (IMDS).
- `CloudEnumerator.enumerate_storage` (method) `modules/cloud_enum.py:251` `def enumerate_storage(self, target_bucket)` -- Enumerate cloud storage buckets and objects.
- `CloudEnumerator.enumerate_iam` (method) `modules/cloud_enum.py:372` `def enumerate_iam(self)` -- Enumerate IAM roles, users, and policies.
- `CloudEnumerator.full_enumeration` (method) `modules/cloud_enum.py:576` `def full_enumeration(self)` -- Run full cloud enumeration: metadata + storage + IAM.

## modules/collab_bp.py
Depends on: `core/logging.py`, `modules/lazy_rbac.py`
Imported by: `cli/commands/collaboration.py`, `lazyc2.py`, `modules/engagement_hooks.py`, `modules/event_bus.py`, `skills/lazyown_mcp.py`, `tests/test_collab_and_onboarding.py`, `tests/test_core_modules.py`
- `login_required` (method) `modules/collab_bp.py:80` `def login_required(f)` -- No-op decorator when Flask-Login is unavailable.
- `decorated` (method) `modules/collab_bp.py:84` `def decorated()`
- `decorated` (method) `modules/collab_bp.py:124` `def decorated()`
- `decorator` (method) `modules/collab_bp.py:139` `def decorator(f)`
- `decorated` (method) `modules/collab_bp.py:141` `def decorated()`
- `ColabEvent.to_sse` (method) `modules/collab_bp.py:170` `def to_sse(self)`
- `EventBus.__init__` (method) `modules/collab_bp.py:198` `def __init__(self)`
- `EventBus.subscribe` (method) `modules/collab_bp.py:203` `def subscribe(self, subscriber_id)`
- `EventBus.unsubscribe` (method) `modules/collab_bp.py:215` `def unsubscribe(self, subscriber_id)`
- `EventBus.publish` (method) `modules/collab_bp.py:219` `def publish(self, event)`
- `EventBus.recent` (method) `modules/collab_bp.py:234` `def recent(self, n)`
- `EventBus.reset` (method) `modules/collab_bp.py:238` `def reset(self)`
- `LockManager.__init__` (method) `modules/collab_bp.py:263` `def __init__(self)`
- `LockManager.acquire` (method) `modules/collab_bp.py:267` `def acquire(self, target, operator, ttl_secs)`
- `LockManager.release` (method) `modules/collab_bp.py:279` `def release(self, target, operator)`
- `LockManager.status` (method) `modules/collab_bp.py:287` `def status(self, target)`
- `LockManager.all_locks` (method) `modules/collab_bp.py:292` `def all_locks(self)`
- `LockManager.reset` (method) `modules/collab_bp.py:304` `def reset(self)`
- `OperatorRegistry.__init__` (method) `modules/collab_bp.py:319` `def __init__(self)`
- `OperatorRegistry.join` (method) `modules/collab_bp.py:323` `def join(self, name)`
- `OperatorRegistry.heartbeat` (method) `modules/collab_bp.py:334` `def heartbeat(self, name)`
- `OperatorRegistry.leave` (method) `modules/collab_bp.py:340` `def leave(self, name)`
- `OperatorRegistry.active_operators` (method) `modules/collab_bp.py:345` `def active_operators(self)`
- `OperatorRegistry.reset` (method) `modules/collab_bp.py:356` `def reset(self)`
- `OperatorRegistry.get_event_bus` (method) `modules/collab_bp.py:370` `def get_event_bus()`
- `OperatorRegistry.get_lock_manager` (method) `modules/collab_bp.py:374` `def get_lock_manager()`
- `OperatorRegistry.get_operator_registry` (method) `modules/collab_bp.py:378` `def get_operator_registry()`
- `OperatorRegistry.publish_event` (method) `modules/collab_bp.py:382` `def publish_event(type, payload, operator)` -- Module-level convenience for other modules to broadcast events.
- `OperatorRegistry.collab_ui` (method) `modules/collab_bp.py:396` `def collab_ui()`
- `OperatorRegistry.stream` (method) `modules/collab_bp.py:411` `def stream()`
- `OperatorRegistry.generate` (method) `modules/collab_bp.py:424` `def generate()`
- `OperatorRegistry.operators` (method) `modules/collab_bp.py:458` `def operators()`
- `OperatorRegistry.publish` (method) `modules/collab_bp.py:470` `def publish()`
- `OperatorRegistry.lock` (method) `modules/collab_bp.py:483` `def lock()`
- `OperatorRegistry.unlock` (method) `modules/collab_bp.py:504` `def unlock()`
- `OperatorRegistry.locks` (method) `modules/collab_bp.py:522` `def locks()`
- `OperatorRegistry.history` (method) `modules/collab_bp.py:537` `def history()`

## modules/colors.py
Imported by: `contrib/legacy/lazygptcli.py`, `contrib/legacy/lazygptcli_unified.py`, `contrib/legacy/lazyproxy.py`, `contrib/legacy/lazyseo.py`, `lazyc2.py`, `modules/llm_prompts.py`, `static/js/xterm.js`
- `retModel` (function) `modules/colors.py:40` `def retModel()` -- gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768...
- `delete_lines` (function) `modules/colors.py:68` `def delete_lines(content, to_delete)`
- `no_html` (function) `modules/colors.py:74` `def no_html(content)`

## modules/command_executor.py
Depends on: `core/logging.py`, `modules/event_bus.py`
- `CommandExecutor.__init__` (method) `modules/command_executor.py:59` `def __init__(self)`
- `CommandExecutor.instance` (method) `modules/command_executor.py:63` `def instance(cls)`
- `CommandExecutor.add_hook` (method) `modules/command_executor.py:68` `def add_hook(self, hook)` -- Register a post-execution hook (e.g., for StateManager or metrics).
- `CommandExecutor.run` (method) `modules/command_executor.py:72` `def run(self, command, timeout, stream)` -- Execute a shell command and return the result.
- `CommandExecutor.run_with_tee` (method) `modules/command_executor.py:172` `def run_with_tee(self, command, output_path, timeout)` -- Execute a command and tee output to a file.
- `CommandExecutor.get_executor` (method) `modules/command_executor.py:264` `def get_executor()`

## modules/compliance.py
Depends on: `core/logging.py`
Imported by: `lazyc2.py`
- `EvidenceChain.__init__` (method) `modules/compliance.py:357` `def __init__(self, sessions_dir)`
- `EvidenceChain.add_file` (method) `modules/compliance.py:383` `def add_file(self, filepath, operator, description)`
- `EvidenceChain.verify` (method) `modules/compliance.py:410` `def verify(self)`
- `EvidenceChain.get_chain_digest` (method) `modules/compliance.py:429` `def get_chain_digest(self)`
- `EvidenceChain.to_report` (method) `modules/compliance.py:432` `def to_report(self)`
- `EvidenceChain.export_pdf` (method) `modules/compliance.py:449` `def export_pdf(report_md, output_path, title, classification)` -- Export a Markdown report to PDF using fpdf2.
- `EvidenceChain.export_to_elastic_ndjson` (method) `modules/compliance.py:533` `def export_to_elastic_ndjson(findings, output_path, index_prefix)` -- Export findings as Elasticsearch NDJSON bulk format.
- `EvidenceChain.export_to_cef` (method) `modules/compliance.py:572` `def export_to_cef(findings, output_path, vendor, product, version)` -- Export findings in CEF (Common Event Format) for ArcSight/QRadar/Splunk.
- `ComplianceEngine.__init__` (method) `modules/compliance.py:635` `def __init__(self, sessions_dir)`
- `ComplianceEngine.map_findings_to_compliance` (method) `modules/compliance.py:639` `def map_findings_to_compliance(self, findings, frameworks)` -- Map findings to compliance framework controls.
- `ComplianceEngine.generate_compliance_report` (method) `modules/compliance.py:710` `def generate_compliance_report(self, findings, include_evidence_chain, include_siem_formats)` -- Generate a full compliance report with evidence chain and optional SIEM export.
- `ComplianceEngine.export_pdf` (method) `modules/compliance.py:831` `def export_pdf(self, report, output_path)`
- `ComplianceEngine.add_evidence` (method) `modules/compliance.py:901` `def add_evidence(self, filepath, operator, description)`
- `ComplianceEngine.verify_evidence_chain` (method) `modules/compliance.py:904` `def verify_evidence_chain(self)`

## modules/conditional_hooks.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/credential_reuse.py`, `modules/state_manager.py`
Imported by: `cli/commands/automation.py`, `lazyc2.py`, `lazyc2/blueprints/beacon.py`, `tests/test_conditional_hooks_extended.py`
- `HookRule.can_fire` (method) `modules/conditional_hooks.py:56` `def can_fire(self, now)`
- `HookRule.mark_fired` (method) `modules/conditional_hooks.py:65` `def mark_fired(self)`
- `HookRule.to_dict` (method) `modules/conditional_hooks.py:69` `def to_dict(self)`
- `HookEngine.__init__` (method) `modules/conditional_hooks.py:270` `def __init__(self)`
- `HookEngine.register_action_handler` (method) `modules/conditional_hooks.py:277` `def register_action_handler(self, action_type, handler)` -- Register a handler for a custom action type.
- `HookEngine.set_placeholders` (method) `modules/conditional_hooks.py:286` `def set_placeholders(self, placeholders)` -- Set placeholder values for command templating (rhost, lhost, etc.).
- `HookEngine.load_rules` (method) `modules/conditional_hooks.py:290` `def load_rules(self, path)` -- Load rules from JSON file, or create it with defaults.
- `HookEngine.save_rules` (method) `modules/conditional_hooks.py:322` `def save_rules(self, path)` -- Persist current rules to JSON.
- `HookEngine.add_rule` (method) `modules/conditional_hooks.py:330` `def add_rule(self, rule_dict)` -- Add a rule at runtime.
- `HookEngine.remove_rule` (method) `modules/conditional_hooks.py:345` `def remove_rule(self, name)` -- Remove a rule by name.
- `HookEngine.enable_rule` (method) `modules/conditional_hooks.py:359` `def enable_rule(self, name, enabled)` -- Enable or disable a rule by name.
- `HookEngine.fire` (method) `modules/conditional_hooks.py:516` `def fire(self, event, context)` -- Fire an event, evaluating all matching rules.
- `HookEngine.list_rules` (method) `modules/conditional_hooks.py:571` `def list_rules(self)` -- Return all rules as dictionaries.
- `HookEngine.get_rule` (method) `modules/conditional_hooks.py:575` `def get_rule(self, name)` -- Return a single rule by name, or None.
- `HookEngine.get_hook_engine` (method) `modules/conditional_hooks.py:586` `def get_hook_engine()` -- Return the singleton :class:`HookEngine`.

## modules/config_store.py
Depends on: `core/config.py`, `core/logging.py`
Imported by: `tests/test_core_modules.py`
- `init` (function) `modules/config_store.py:36` `def init(path, watch)` -- Initialise the config store (idempotent).
- `get_config` (function) `modules/config_store.py:53` `def get_config(key, default)` -- Return a config value (or the full dict when *key* is empty).
- `set_config` (function) `modules/config_store.py:66` `def set_config()` -- Update one or more keys and persist to disk atomically.
- `set_config_dict` (function) `modules/config_store.py:80` `def set_config_dict(updates)` -- Bulk-update from a dict and persist to disk.
- `reload_config` (function) `modules/config_store.py:90` `def reload_config()` -- Force reload from disk (discards in-memory changes).
- `stop_watcher` (function) `modules/config_store.py:96` `def stop_watcher()` -- Stop the file-watcher background thread (if running).

## modules/credential_reuse.py
Depends on: `core/logging.py`
Imported by: `cli/commands/automation.py`, `lazyc2.py`, `lazyc2/blueprints/beacon.py`, `modules/conditional_hooks.py`
- `ReuseCandidate.to_dict` (method) `modules/credential_reuse.py:43` `def to_dict(self)`
- `CredentialReuseEngine.__init__` (method) `modules/credential_reuse.py:80` `def __init__(self)`
- `CredentialReuseEngine.mark_failed` (method) `modules/credential_reuse.py:107` `def mark_failed(self, username, password, host)` -- Record that a credential did NOT work against a host.
- `CredentialReuseEngine.mark_confirmed` (method) `modules/credential_reuse.py:112` `def mark_confirmed(self, username, password, host)` -- Record that a credential worked against a host.
- `CredentialReuseEngine.rank` (method) `modules/credential_reuse.py:226` `def rank(self, hosts, creds, host_services, limit)` -- Score all (cred, host) pairs and return top candidates.
- `CredentialReuseEngine.suggest_from_state_manager` (method) `modules/credential_reuse.py:278` `def suggest_from_state_manager(self, state_manager, limit)` -- Convenience: rank creds using hosts and creds from StateManager.
- `CredentialReuseEngine.suggest_from_world_model` (method) `modules/credential_reuse.py:308` `def suggest_from_world_model(self, world_model, limit)` -- Convenience: rank creds using hosts and creds from WorldModel.
- `CredentialReuseEngine.get_summary` (method) `modules/credential_reuse.py:338` `def get_summary(self, candidates)` -- Format candidates as a human-readable summary string.
- `CredentialReuseEngine.get_credential_reuse_engine` (method) `modules/credential_reuse.py:358` `def get_credential_reuse_engine()` -- Return the singleton :class:`CredentialReuseEngine`.

## modules/cross_cloud.py
Imported by: `cli/commands/cloud_attacks.py`
- `CrossCloudAttackEngine.__init__` (method) `modules/cross_cloud.py:64` `def __init__(self, config)`
- `CrossCloudAttackEngine.azure_saml_to_aws` (method) `modules/cross_cloud.py:67` `def azure_saml_to_aws(self)` -- Abuse Azure AD SAML federation to gain AWS access.
- `CrossCloudAttackEngine.gcp_oidc_to_azure` (method) `modules/cross_cloud.py:104` `def gcp_oidc_to_azure(self)` -- Abuse GCP OIDC federation to gain Azure access.
- `CrossCloudAttackEngine.aws_oidc_to_gcp` (method) `modules/cross_cloud.py:133` `def aws_oidc_to_gcp(self)` -- Abuse AWS OIDC federation to gain GCP access.
- `CrossCloudAttackEngine.multi_cloud_imds_harvesting` (method) `modules/cross_cloud.py:167` `def multi_cloud_imds_harvesting(self)` -- Harvest metadata from all cloud providers simultaneously.
- `CrossCloudAttackEngine.entra_id_to_gcp_workforce_federation` (method) `modules/cross_cloud.py:204` `def entra_id_to_gcp_workforce_federation(self)` -- Exploit Entra ID to GCP workforce identity federation.
- `CrossCloudAttackEngine.detect_cross_cloud_federation` (method) `modules/cross_cloud.py:234` `def detect_cross_cloud_federation(self)` -- Detect cross-cloud federation configurations for attack surface mapping.
- `CrossCloudAttackEngine.summary` (method) `modules/cross_cloud.py:258` `def summary(self)`

## modules/cve_matcher.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `CVEMatcher.__init__` (method) `modules/cve_matcher.py:70` `def __init__(self, api_key, cache_dir)`
- `CVEMatcher.search` (method) `modules/cve_matcher.py:82` `def search(self)` -- Search CVEs by product / version keywords.
- `CVEMatcher.search_by_cpe` (method) `modules/cve_matcher.py:89` `def search_by_cpe(self, cpe_name, max_results)` -- Search CVEs by CPE 2.3 string.
- `CVEMatcher.get_matcher` (method) `modules/cve_matcher.py:198` `def get_matcher()` -- Return (or create) the module-level singleton CVEMatcher.
- `CVEMatcher.search` (method) `modules/cve_matcher.py:206` `def search(product, version, max_results)` -- Module-level convenience wrapper.

## modules/dacl_abuse.py
Imported by: `cli/commands/active_directory.py`
- `DACLAbuseEngine.__init__` (method) `modules/dacl_abuse.py:136` `def __init__(self, domain, domain_sid, acl_data)`
- `DACLAbuseEngine.parse_bloodhound_acls` (method) `modules/dacl_abuse.py:143` `def parse_bloodhound_acls(self, edges)` -- Parse BloodHound edge data to extract exploitable ACLs.
- `DACLAbuseEngine.parse_raw_aces` (method) `modules/dacl_abuse.py:182` `def parse_raw_aces(self, raw_nthashes)` -- Parse raw ACE data from ntSecurityDescriptor parsing.
- `DACLAbuseEngine.compute_attack_chains` (method) `modules/dacl_abuse.py:224` `def compute_attack_chains(self)` -- Generate exploitation plans for all discovered ACL targets.
- `DACLAbuseEngine.adminsdholder_abuse_plan` (method) `modules/dacl_abuse.py:291` `def adminsdholder_abuse_plan(self, target_sid)` -- Generate an AdminSDHolder abuse plan.
- `DACLAbuseEngine.dcsync_rights_assignment_plan` (method) `modules/dacl_abuse.py:318` `def dcsync_rights_assignment_plan(self, target_sid, domain_dn)` -- Generate a DCSync rights assignment plan.
- `DACLAbuseEngine.owner_takeover_plan` (method) `modules/dacl_abuse.py:348` `def owner_takeover_plan(self, target_dn, attacker_sid)` -- Generate an ownership takeover plan.
- `DACLAbuseEngine.summary` (method) `modules/dacl_abuse.py:418` `def summary(self)` -- Return a summary of all DACL/SACL abuse findings.


Next: [API_p10.md](API_p10.md)
