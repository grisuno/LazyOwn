# API (page 10 of 23)
Previous: [API_p9.md](API_p9.md)

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

## modules/c2_agent.py
Depends on: `core/logging.py`, `lazyc2/security/services.py`, `modules/atomic_exploit_bridge.py`
Imported by: `cli/commands/c2_session.py`
- `client_id_for` (function) `modules/c2_agent.py:85` `def client_id_for(target)` -- Derive a stable, file-safe client id from a target IP.
- `validate_client_id` (function) `modules/c2_agent.py:91` `def validate_client_id(raw)` -- Validate a client id (alphanumerics, dash, underscore).
- `build_agent` (function) `modules/c2_agent.py:354` `def build_agent(c2_url, client_id, aes_hex, route, sleep)` -- Render the agent script for a target (pure function, no I/O).
- `read_aes_hex` (function) `modules/c2_agent.py:441` `def read_aes_hex()` -- Read the live C2 AES key hex (snapshotted, never generated).
- `deploy` (function) `modules/c2_agent.py:446` `def deploy(target, c2_base, route, lhost, sleep)` -- Deliver + launch the agent on *target* via a working shell primitive.
- `read_records` (function) `modules/c2_agent.py:517` `def read_records(client_id, limit)` -- Read the latest beacon records for a client (newest last).
- `wait_record` (function) `modules/c2_agent.py:534` `def wait_record(client_id, command, since, timeout)` -- Wait for a fresh record matching *command* (polls the JSONL log).
- `C2Server.__init__` (method) `modules/c2_agent.py:551` `def __init__(self, port, user, password)`
- `C2Server.status` (method) `modules/c2_agent.py:568` `def status(self)` -- Report server liveness and listener reachability.
- `C2Server.start` (method) `modules/c2_agent.py:600` `def start(self)` -- Start lazyc2 headless (no-op when already running).
- `C2Server.stop` (method) `modules/c2_agent.py:631` `def stop(self)` -- Stop the headless server (SIGTERM, best-effort).
- `C2Server.ensure_http_listener` (method) `modules/c2_agent.py:654` `def ensure_http_listener(self, http_port, auth)` -- Add + start a plaintext lab listener via the C2 API (py2 agents lack TLS).

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
- `get_registry` (function) `modules/c2_profile.py:595` `def get_registry()` -- Return the module-level singleton ProfileRegistry.
- `get_profile` (function) `modules/c2_profile.py:620` `def get_profile(name)` -- Return the named profile from the module singleton registry.
- `list_profiles` (function) `modules/c2_profile.py:625` `def list_profiles()` -- Return a sorted list of all registered profile names.

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

## modules/c2_surfaces.py
Depends on: `core/logging.py`, `skills/lazyown_mcp_helpers.py`
Imported by: `cli/commands/c2_session.py`, `lazyc2.py`, `modules/atomic_exploit_bridge.py`, `modules/sinks/c2_surfaces.py`, `tests/test_c2_surfaces.py`
- `publish_banner` (function) `modules/c2_surfaces.py:73` `def publish_banner(hostname, port, protocol, service, extra, sessions_dir)` -- Append a service banner to sessions/banners.json (deduplicated).
- `publish_cve` (function) `modules/c2_surfaces.py:115` `def publish_cve(title, description, operator, risk, sessions_dir)` -- Append a CVE finding to sessions/cves.json (deduplicated by title).
- `append_note` (function) `modules/c2_surfaces.py:155` `def append_note(line, sessions_dir)` -- Append one timestamped line to sessions/notes.txt (never overwrites).
- `register_loot_event` (function) `modules/c2_surfaces.py:184` `def register_loot_event(name, path_glob, description, event_config)` -- Register an event_config.json rule watching an artefact glob.
- `refresh_session_report` (function) `modules/c2_surfaces.py:229` `def refresh_session_report(timeout)` -- Regenerate sessions/sessionLazyOwn.json via modules/session_state.py.
- `severity_to_risk` (function) `modules/c2_surfaces.py:251` `def severity_to_risk(severity)` -- Map exploit severity words to /cves risk levels.
- `group_tasks_for_display` (function) `modules/c2_surfaces.py:261` `def group_tasks_for_display(tasks)` -- Group tasks for the /tasks page: unique hits with counts + noise tally.

## modules/cal.sh
- `is_leap_year` (function) `modules/cal.sh:4` -- Función para calcular si un año es bisiesto
- `days_in_month` (function) `modules/cal.sh:14` -- Función para obtener el número de días en un mes
- `first_day_of_month` (function) `modules/cal.sh:31` -- Función para obtener el día de la semana del primer día del mes

## modules/chain_registry.py
Depends on: `core/logging.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `cli/commands/exploit_migrated.py`, `cli/lazy_orchestrator.py`, `modules/chain_runner.py`, `modules/metasploitable_gym.py`, `skills/lazyown_mcp.py`, `tests/test_apt_chain_integration.py`, `tests/test_chain_registry.py`, `tests/test_chain_runner.py`, `tests/test_metasploitable_gym.py`
- `ChainStep.identifier` (method) `modules/chain_registry.py:67` `def identifier(self)` -- Return the declared id or a stable generated one.
- `Chain.resolve` (method) `modules/chain_registry.py:88` `def resolve(self, tokens)` -- Substitute tokens, evaluate conditions and guards.
- `evaluate_when` (function) `modules/chain_registry.py:192` `def evaluate_when(expression, variables)` -- Evaluate a safe ``when`` expression against string variables.
- `validate_chain` (function) `modules/chain_registry.py:257` `def validate_chain(data, filename, chains_dir)` -- Validate raw YAML data against the chain schema.
- `load_all` (function) `modules/chain_registry.py:334` `def load_all(chains_dir)` -- Load every valid, enabled chain file (skips the rest loudly).
- `get` (function) `modules/chain_registry.py:434` `def get(name, chains_dir)` -- Return one chain by name, or None.
- `scan_all` (function) `modules/chain_registry.py:439` `def scan_all(chains_dir)` -- List every chain file including disabled ones (for administration).
- `set_enabled` (function) `modules/chain_registry.py:498` `def set_enabled(name, enabled, chains_dir)` -- Flip a chain's ``enabled`` flag in its YAML file (round-trip).
- `generate_for_playbook` (function) `modules/chain_registry.py:521` `def generate_for_playbook(engine_key, apt_display, description, chains_dir, overwrite)` -- Write a per-APT chain file inheriting the base APT chain.

## modules/chain_runner.py
Depends on: `core/safe_exec.py`, `modules/chain_registry.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `tests/test_chain_runner.py`
- `StepOutcome.ok` (method) `modules/chain_runner.py:50` `def ok(self)` -- Return True for success and dry-run steps.
- `StepOutcome.to_dict` (method) `modules/chain_runner.py:54` `def to_dict(self)` -- Return a JSON-serializable view.
- `ChainRunResult.to_dict` (method) `modules/chain_runner.py:86` `def to_dict(self)` -- Return a JSON-serializable view.
- `render_text` (function) `modules/chain_runner.py:103` `def render_text(template, variables)` -- Substitute single-brace tokens in one pass.
- `ChainRunner.__init__` (method) `modules/chain_runner.py:114` `def __init__(self, chain, tokens, shell, executor, default_timeout, dry_run, on_step, retry_backoff)` -- Bind the chain, the execution primitive and operator switches.
- `ChainRunner.run` (method) `modules/chain_runner.py:135` `def run(self)` -- Execute the chain in order and return every step outcome.

## modules/cicd_enumerator.py
Imported by: `cli/commands/cicd.py`
- `CICDEnumerator.__init__` (method) `modules/cicd_enumerator.py:54` `def __init__(self, target_url, sessions_dir)`
- `CICDEnumerator.scan` (method) `modules/cicd_enumerator.py:60` `def scan(self)` -- Run all CI/CD scans.
- `CICDEnumerator.scan_build_log` (method) `modules/cicd_enumerator.py:297` `def scan_build_log(self, log_content, source)` -- Scan a build log for leaked secrets.
- `CICDEnumerator.generate_ci_attack_matrix` (method) `modules/cicd_enumerator.py:322` `def generate_ci_attack_matrix(self)` -- Generate a comprehensive CI/CD attack matrix.
- `CICDEnumerator.export_findings` (method) `modules/cicd_enumerator.py:387` `def export_findings(self)` -- Export CI/CD findings to a JSON file.

## modules/cli_auth.py
Depends on: `cli/engagement_hooks.py`, `core/config.py`, `modules/lazy_rbac.py`
Imported by: `cli/auto_crypto.py`, `cli/banner_config.py`, `cli/commands/cli_auth.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `cli/wizard.py`, `lazyown.py`, `modules/redteam_gym.py`, `tests/test_cli_auth_remember.py`, `tests/test_engagement_elo_and_methodology.py`
- `user_exists` (function) `modules/cli_auth.py:122` `def user_exists(username)` -- Check if a username already exists in users.json or RBAC store.
- `register` (function) `modules/cli_auth.py:145` `def register(username, password)` -- Register a new operator in users.json.
- `verify_password` (function) `modules/cli_auth.py:214` `def verify_password(username, password)` -- Verify a username/password against users.json using werkzeug.
- `login` (function) `modules/cli_auth.py:240` `def login(username, password, remember)` -- Authenticate a CLI operator and optionally persist a remember-me token.
- `logout` (function) `modules/cli_auth.py:293` `def logout()` -- Log out the current CLI operator and clear the remember-me token.
- `try_auto_login` (function) `modules/cli_auth.py:328` `def try_auto_login()` -- Attempt auto-login using the remember-me token from payload.json.
- `whoami` (function) `modules/cli_auth.py:366` `def whoami()` -- Return the currently logged-in CLI operator's identity.
- `get_current_operator` (function) `modules/cli_auth.py:396` `def get_current_operator()` -- Return the current operator username, or None if not logged in.
- `sync_elo_from_session` (function) `modules/cli_auth.py:408` `def sync_elo_from_session(elo)` -- Update the CLI session ELO from engagement state.
- `needs_login` (function) `modules/cli_auth.py:487` `def needs_login()` -- Check if the current session has a logged-in operator.

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
- `login_required` (function) `modules/collab_bp.py:80` `def login_required(f)` -- No-op decorator when Flask-Login is unavailable.
- `decorated` (function) `modules/collab_bp.py:84` `def decorated()`
- `decorated` (function) `modules/collab_bp.py:124` `def decorated()`
- `decorator` (function) `modules/collab_bp.py:139` `def decorator(f)`
- `decorated` (function) `modules/collab_bp.py:141` `def decorated()`
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
- `get_event_bus` (function) `modules/collab_bp.py:370` `def get_event_bus()`
- `get_lock_manager` (function) `modules/collab_bp.py:374` `def get_lock_manager()`
- `get_operator_registry` (function) `modules/collab_bp.py:378` `def get_operator_registry()`
- `publish_event` (function) `modules/collab_bp.py:382` `def publish_event(type, payload, operator)` -- Module-level convenience for other modules to broadcast events.
- `collab_ui` (function) `modules/collab_bp.py:396` `def collab_ui()`
- `stream` (function) `modules/collab_bp.py:411` `def stream()`
- `generate` (function) `modules/collab_bp.py:424` `def generate()`
- `operators` (function) `modules/collab_bp.py:458` `def operators()`
- `publish` (function) `modules/collab_bp.py:470` `def publish()`
- `lock` (function) `modules/collab_bp.py:483` `def lock()`
- `unlock` (function) `modules/collab_bp.py:504` `def unlock()`
- `locks` (function) `modules/collab_bp.py:522` `def locks()`
- `history` (function) `modules/collab_bp.py:537` `def history()`

## modules/colors.py
Imported by: `contrib/legacy/lazygptcli.py`, `contrib/legacy/lazygptcli_unified.py`, `contrib/legacy/lazyproxy.py`, `contrib/legacy/lazyseo.py`, `lazyc2.py`, `modules/llm_prompts.py`, `static/js/xterm.js`
- `retModel` (function) `modules/colors.py:40` `def retModel()` -- gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768...
- `delete_lines` (function) `modules/colors.py:68` `def delete_lines(content, to_delete)`
- `no_html` (function) `modules/colors.py:74` `def no_html(content)`

## modules/command_executor.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/auto_registry.py`, `modules/event_bus.py`
Imported by: `lazyown.py`, `modules/auto_registry.py`, `tests/test_executor_kernel.py`, `tests/test_lazy_runner.py`
- `set_thread_timeout` (function) `modules/command_executor.py:41` `def set_thread_timeout(seconds)` -- Bound the next ``run_tee`` call on this thread by wall-clock seconds.
- `clear_thread_timeout` (function) `modules/command_executor.py:46` `def clear_thread_timeout()` -- Remove this thread's ``run_tee`` deadline, if any.
- `thread_timeout` (function) `modules/command_executor.py:54` `def thread_timeout()` -- Return this thread's pending ``run_tee`` deadline, or None.
- `set_thread_stdin_devnull` (function) `modules/command_executor.py:59` `def set_thread_stdin_devnull(enabled)` -- Detach the next ``run_tee`` child from the operator terminal.
- `clear_thread_stdin_devnull` (function) `modules/command_executor.py:64` `def clear_thread_stdin_devnull()` -- Restore inherited stdin for this thread's ``run_tee`` calls.
- `thread_stdin_devnull` (function) `modules/command_executor.py:72` `def thread_stdin_devnull()` -- Return True when this thread's ``run_tee`` children drop stdin.
- `CommandExecutor.__init__` (method) `modules/command_executor.py:118` `def __init__(self)`
- `CommandExecutor.instance` (method) `modules/command_executor.py:122` `def instance(cls)`
- `CommandExecutor.add_hook` (method) `modules/command_executor.py:127` `def add_hook(self, hook)` -- Register a post-execution hook (e.g., for StateManager or metrics).
- `CommandExecutor.run` (method) `modules/command_executor.py:131` `def run(self, command, timeout, stream)` -- Execute a shell command and return the result.
- `CommandExecutor.run_passthrough` (method) `modules/command_executor.py:179` `def run_passthrough(self, command, env)` -- Run a command with stdio inherited, returning its exit code.
- `CommandExecutor.run_tee` (method) `modules/command_executor.py:194` `def run_tee(self, command)` -- Run a command teeing raw output bytes to a writer and a log file.
- `CommandExecutor.run_with_tee` (method) `modules/command_executor.py:358` `def run_with_tee(self, command, output_path, timeout)` -- Execute a command and tee output to a file.
- `get_executor` (function) `modules/command_executor.py:426` `def get_executor()`

## modules/compliance.py
Depends on: `core/logging.py`
Imported by: `lazyc2.py`
- `EvidenceChain.__init__` (method) `modules/compliance.py:357` `def __init__(self, sessions_dir)`
- `EvidenceChain.add_file` (method) `modules/compliance.py:383` `def add_file(self, filepath, operator, description)`
- `EvidenceChain.verify` (method) `modules/compliance.py:410` `def verify(self)`
- `EvidenceChain.get_chain_digest` (method) `modules/compliance.py:429` `def get_chain_digest(self)`
- `EvidenceChain.to_report` (method) `modules/compliance.py:432` `def to_report(self)`
- `export_pdf` (function) `modules/compliance.py:449` `def export_pdf(report_md, output_path, title, classification)` -- Export a Markdown report to PDF using fpdf2.
- `export_to_elastic_ndjson` (function) `modules/compliance.py:533` `def export_to_elastic_ndjson(findings, output_path, index_prefix)` -- Export findings as Elasticsearch NDJSON bulk format.
- `export_to_cef` (function) `modules/compliance.py:572` `def export_to_cef(findings, output_path, vendor, product, version)` -- Export findings in CEF (Common Event Format) for ArcSight/QRadar/Splunk.
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
- `get_hook_engine` (function) `modules/conditional_hooks.py:586` `def get_hook_engine()` -- Return the singleton :class:`HookEngine`.

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
- `get_credential_reuse_engine` (function) `modules/credential_reuse.py:358` `def get_credential_reuse_engine()` -- Return the singleton :class:`CredentialReuseEngine`.

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

## modules/custom_tools.py
Depends on: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/notify.py`
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `tests/test_lazy_loop.py`
- `add_tool` (function) `modules/custom_tools.py:52` `def add_tool(name, kind, target, description, method, body, timeout, trigger)` -- Register or replace one custom tool.
- `remove_tool` (function) `modules/custom_tools.py:97` `def remove_tool(name)` -- Delete a tool by name.
- `list_tools` (function) `modules/custom_tools.py:109` `def list_tools()` -- Return every registered tool.
- `get_tool` (function) `modules/custom_tools.py:114` `def get_tool(name)` -- Find one tool by name.
- `match_tools` (function) `modules/custom_tools.py:128` `def match_tools(text, limit)` -- Rank tools whose name/description/trigger keywords appear in the text.
- `run_tool` (function) `modules/custom_tools.py:151` `def run_tool(name, arg, on_output)` -- Execute one custom tool and return its transcript.

## modules/cve_matcher.py
Depends on: `core/logging.py`
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `CVEMatcher.__init__` (method) `modules/cve_matcher.py:70` `def __init__(self, api_key, cache_dir)`
- `CVEMatcher.search` (method) `modules/cve_matcher.py:82` `def search(self)` -- Search CVEs by product / version keywords.
- `CVEMatcher.search_by_cpe` (method) `modules/cve_matcher.py:89` `def search_by_cpe(self, cpe_name, max_results)` -- Search CVEs by CPE 2.3 string.
- `get_matcher` (function) `modules/cve_matcher.py:198` `def get_matcher()` -- Return (or create) the module-level singleton CVEMatcher.
- `search` (function) `modules/cve_matcher.py:206` `def search(product, version, max_results)` -- Module-level convenience wrapper.

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

## modules/dashboard_bp.py
Imported by: `lazyc2.py`, `tests/test_core_modules.py`, `tests/test_dashboard_routes.py`
- `dashboard_index` (function) `modules/dashboard_bp.py:778` `def dashboard_index()` -- Render the main SOC dashboard HTML page.
- `dashboard_api_data` (function) `modules/dashboard_bp.py:784` `def dashboard_api_data()` -- JSON snapshot of all dashboard data.
- `dashboard_loot` (function) `modules/dashboard_bp.py:902` `def dashboard_loot()` -- Render the loot browser: captured credentials, hashes and files.
- `dashboard_timeline` (function) `modules/dashboard_bp.py:1017` `def dashboard_timeline()` -- Render the campaign timeline: commands and events, newest first.

## modules/dashboard_engine.py
Imported by: `cli/commands/pwn.py`, `modules/rich_tui.py`, `modules/unified_dashboard.py`, `skills/lazyown_mcp.py`
- `DashboardEngine.__init__` (method) `modules/dashboard_engine.py:139` `def __init__(self, world_model)`
- `DashboardEngine.set_world_model` (method) `modules/dashboard_engine.py:148` `def set_world_model(self, model)`
- `DashboardEngine.set_exploit_recommender` (method) `modules/dashboard_engine.py:151` `def set_exploit_recommender(self, recommender)`
- `DashboardEngine.set_auto_pivot` (method) `modules/dashboard_engine.py:154` `def set_auto_pivot(self, pivot)`
- `DashboardEngine.set_evasion_engine` (method) `modules/dashboard_engine.py:157` `def set_evasion_engine(self, evasion)`
- `DashboardEngine.build_snapshot` (method) `modules/dashboard_engine.py:160` `def build_snapshot(self)` -- Build a complete dashboard snapshot from all data sources.
- `DashboardEngine.render_text_map` (method) `modules/dashboard_engine.py:276` `def render_text_map(self, snapshot)` -- Render a text-based network map from a dashboard snapshot.
- `DashboardEngine.render_ascii_topology` (method) `modules/dashboard_engine.py:358` `def render_ascii_topology(self, snapshot)` -- Render an ASCII-art topology tree from a snapshot.
- `DashboardEngine.export_json` (method) `modules/dashboard_engine.py:408` `def export_json(self, snapshot)` -- Export dashboard snapshot as JSON string.
- `DashboardEngine.persist_snapshot` (method) `modules/dashboard_engine.py:421` `def persist_snapshot(self, snapshot)` -- Persist dashboard snapshot to sessions/dashboard_snapshot.json.
- `DashboardEngine.format_for_cli` (method) `modules/dashboard_engine.py:438` `def format_for_cli(self, snapshot)` -- Compact single-line status for CLI prompt integration.

## modules/db.py
Depends on: `core/config.py`, `core/crypto.py`, `core/logging.py`
Imported by: `cli/commands/campaign.py`, `cli/commands/collaboration.py`, `cli/commands/database.py`, `lazyc2/blueprints/api_v1.py`, `modules/autonomous_exploit_engine.py`, `modules/estorides_importer.py`, `modules/hash_cracker.py`, `modules/integrations/nuclei_parser.py`, `modules/opsec_scorer.py`, `modules/sinks/campaign_db.py`, `modules/state_manager.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_api_v1.py`, `tests/test_autonomous_ops.py`, `tests/test_daemon_loop.py`, `tests/test_db.py`, `tests/test_mutation_verification.py`, `tests/test_security_hardening.py`
- `LazyOwnDB.__init__` (method) `modules/db.py:159` `def __init__(self, db_path)`
- `LazyOwnDB.db_path` (method) `modules/db.py:182` `def db_path(self)` -- Path to the SQLite database file.
- `LazyOwnDB.migration_status` (method) `modules/db.py:222` `def migration_status(self)` -- Return the current and latest migration versions.
- `LazyOwnDB.workspace_create` (method) `modules/db.py:292` `def workspace_create(self, name, description)` -- Create a new workspace.
- `LazyOwnDB.workspace_list` (method) `modules/db.py:307` `def workspace_list(self)` -- Return all workspaces as dicts.
- `LazyOwnDB.workspace_get` (method) `modules/db.py:313` `def workspace_get(self, name)` -- Get a workspace by name, or None.
- `LazyOwnDB.default_workspace` (method) `modules/db.py:320` `def default_workspace(self, name)` -- Return the id of the named workspace, creating it when absent.
- `LazyOwnDB.workspace_delete` (method) `modules/db.py:333` `def workspace_delete(self, name)` -- Delete a workspace and all its data.
- `LazyOwnDB.host_add` (method) `modules/db.py:357` `def host_add(self, workspace_id, address, mac, hostname, os, state)` -- Add or update a host.
- `LazyOwnDB.host_delete` (method) `modules/db.py:390` `def host_delete(self, host_id)` -- Delete a host and its related data.
- `LazyOwnDB.host_list` (method) `modules/db.py:401` `def host_list(self, workspace_id)` -- List all hosts in a workspace.
- `LazyOwnDB.host_find` (method) `modules/db.py:410` `def host_find(self, workspace_id, query)` -- Search hosts by address, hostname, or os.
- `LazyOwnDB.service_add` (method) `modules/db.py:427` `def service_add(self, host_id, port, protocol, state, name, product, version)` -- Add a service to a host.
- `LazyOwnDB.service_list` (method) `modules/db.py:447` `def service_list(self, host_id)` -- List all services on a host.
- `LazyOwnDB.vuln_add` (method) `modules/db.py:460` `def vuln_add(self, host_id, name, severity, description, refs)` -- Add a vulnerability to a host.
- `LazyOwnDB.vuln_get` (method) `modules/db.py:478` `def vuln_get(self, vuln_id)` -- Return one vuln row with its host address, or None.
- `LazyOwnDB.vuln_update` (method) `modules/db.py:490` `def vuln_update(self, vuln_id, refs, severity, description)` -- Update mutable vuln fields; returns True when a row changed.
- `LazyOwnDB.vuln_list` (method) `modules/db.py:528` `def vuln_list(self, workspace_id, severity)` -- List vulns in workspace, optionally filtered by severity.
- `LazyOwnDB.cred_add` (method) `modules/db.py:557` `def cred_add(self, host_id, username, password, realm, cred_type, origin)` -- Add a credential (password encrypted at rest).
- `LazyOwnDB.cred_list` (method) `modules/db.py:577` `def cred_list(self, workspace_id)` -- List all creds in workspace (passwords decrypted).
- `LazyOwnDB.loot_add` (method) `modules/db.py:596` `def loot_add(self, workspace_id, name, loot_type, path, notes, host_id)` -- Add a loot entry.
- `LazyOwnDB.loot_list` (method) `modules/db.py:615` `def loot_list(self, workspace_id)` -- List all loot in workspace.
- `LazyOwnDB.note_add` (method) `modules/db.py:631` `def note_add(self, workspace_id, data, note_type, host_id)` -- Add a note.
- `LazyOwnDB.note_list` (method) `modules/db.py:648` `def note_list(self, workspace_id)` -- List all notes in workspace.
- `LazyOwnDB.import_nmap_xml` (method) `modules/db.py:664` `def import_nmap_xml(self, workspace_id, xml_path)` -- Import an Nmap XML file into the database.
- `LazyOwnDB.export_csv` (method) `modules/db.py:740` `def export_csv(self, table, workspace_id)` -- Export a table to CSV string.
- `LazyOwnDB.status` (method) `modules/db.py:775` `def status(self, workspace_id)` -- Return counts for every entity type in a workspace.
- `LazyOwnDB.close` (method) `modules/db.py:804` `def close(self)` -- Close the database connection for the current thread.
- `get_db` (function) `modules/db.py:821` `def get_db(db_path)` -- Get or create a :class:`LazyOwnDB` instance.

## modules/delegation_attacks.py
Imported by: `cli/commands/active_directory.py`
- `DelegationEnumerator.__init__` (method) `modules/delegation_attacks.py:98` `def __init__(self, domain, raw_ldap_output)`
- `DelegationEnumerator.enumerate_from_uac_flags` (method) `modules/delegation_attacks.py:104` `def enumerate_from_uac_flags(self, accounts)` -- Enumerate delegation targets from parsed account data.
- `DelegationEnumerator.parse_bloodhound_output` (method) `modules/delegation_attacks.py:151` `def parse_bloodhound_output(self, bloodhound_json)` -- Parse BloodHound JSON output for delegation data.
- `DelegationEnumerator.find_unconstrained_targets` (method) `modules/delegation_attacks.py:181` `def find_unconstrained_targets(self)` -- Return all accounts with unconstrained delegation enabled.
- `DelegationEnumerator.find_constrained_targets` (method) `modules/delegation_attacks.py:189` `def find_constrained_targets(self)` -- Return all accounts with constrained delegation configured.
- `DelegationEnumerator.find_rbcd_targets` (method) `modules/delegation_attacks.py:197` `def find_rbcd_targets(self)` -- Return all accounts with RBCD configured.
- `DelegationEnumerator.find_dc_targets` (method) `modules/delegation_attacks.py:205` `def find_dc_targets(self)` -- Return domain controllers with delegation configured.
- `DelegationEnumerator.compute_attack_paths` (method) `modules/delegation_attacks.py:215` `def compute_attack_paths(self)` -- Compute delegation-based attack paths.
- `DelegationEnumerator.summary` (method) `modules/delegation_attacks.py:296` `def summary(self)` -- Return a summary of all delegation findings.

## modules/detailed_search.py
- `obtener_informacion` (function) `modules/detailed_search.py:40` `def obtener_informacion(url)`

## modules/detection_feed.py
Depends on: `core/logging.py`, `modules/detection_oracle.py`
Imported by: `modules/detection_oracle.py`, `tests/test_detection_feed.py`
- `DetectionFeed.__init__` (method) `modules/detection_feed.py:83` `def __init__(self, cache_dir, sources)`
- `DetectionFeed.update_rules` (method) `modules/detection_feed.py:92` `def update_rules(self, source)` -- Download and parse rules from the given source.
- `DetectionFeed.load_cached_rules` (method) `modules/detection_feed.py:246` `def load_cached_rules(self, source)` -- Load previously cached rules from disk.
- `DetectionFeed.adjust_from_feedback` (method) `modules/detection_feed.py:270` `def adjust_from_feedback(self, feedback_file)` -- Adjust rule probabilities based on historical detection feedback.
- `get_feed` (function) `modules/detection_feed.py:326` `def get_feed()` -- Return a module-level :class:`DetectionFeed` singleton.

## modules/detection_oracle.py
Depends on: `core/logging.py`, `modules/detection_feed.py`
Imported by: `modules/auto_purple.py`, `modules/detection_feed.py`, `modules/loop_ai_bridge.py`, `skills/autonomous_daemon.py`, `skills/lazyown_policy.py`, `skills/swan_agent.py`, `tests/test_detection_feed.py`, `tests/test_loop_ai_bridge.py`, `tests/test_moe_rl_swan.py`
- `DetectionAssessment.is_high_risk` (method) `modules/detection_oracle.py:75` `def is_high_risk(self)` -- Return True when detection probability is 70% or higher.
- `DetectionAssessment.is_critical_risk` (method) `modules/detection_oracle.py:80` `def is_critical_risk(self)` -- Return True when detection probability is 90% or higher.
- `IDetectionOracle.assess` (method) `modules/detection_oracle.py:94` `def assess(self, command, args, action_category)` -- Return a full DetectionAssessment for the given action.
- `IDetectionOracle.probability` (method) `modules/detection_oracle.py:103` `def probability(self, command, args, action_category)` -- Return only the probability score in [0.0, 1.0].
- `DetectionOracle.__init__` (method) `modules/detection_oracle.py:332` `def __init__(self, rules, feed)`
- `DetectionOracle.refresh` (method) `modules/detection_oracle.py:336` `def refresh(self)` -- Update rules from the detection feed (if available).
- `DetectionOracle.assess` (method) `modules/detection_oracle.py:371` `def assess(self, command, args, action_category)`
- `DetectionOracle.probability` (method) `modules/detection_oracle.py:392` `def probability(self, command, args, action_category)`
- `get_oracle` (function) `modules/detection_oracle.py:478` `def get_oracle()` -- Return (or create) the module-level singleton DetectionOracle.

## modules/dns_beacon.py
Depends on: `core/safe_exec.py`
Imported by: `cli/commands/dns_exfil.py`
- `DNSBeacon.__init__` (method) `modules/dns_beacon.py:38` `def __init__(self, domain, dns_server, sleep_seconds, jitter_percent, dns_type, encode_method)`
- `DNSBeacon.check_in` (method) `modules/dns_beacon.py:105` `def check_in(self)` -- Send heartbeat and check for pending commands.
- `DNSBeacon.send_result` (method) `modules/dns_beacon.py:135` `def send_result(self, command, output, exit_code)` -- Send command output via DNS TXT queries.
- `DNSBeacon.run` (method) `modules/dns_beacon.py:171` `def run(self)` -- Main beacon loop: check-in -> execute command -> send result -> sleep.
- `DNSC2Server.__init__` (method) `modules/dns_beacon.py:211` `def __init__(self, domain, log_source, interface)`
- `DNSC2Server.register_beacon` (method) `modules/dns_beacon.py:225` `def register_beacon(self, beacon_id, hostname)` -- Register a new DNS beacon.
- `DNSC2Server.list_beacons` (method) `modules/dns_beacon.py:235` `def list_beacons(self)` -- List all registered DNS beacons.
- `DNSC2Server.send_task` (method) `modules/dns_beacon.py:239` `def send_task(self, beacon_id, command)` -- Queue a command for a DNS beacon.
- `DNSC2Server.process_query_log` (method) `modules/dns_beacon.py:248` `def process_query_log(self, line)` -- Process a single DNS query log line and extract beacon data.
- `DNSC2Server.get_results` (method) `modules/dns_beacon.py:327` `def get_results(self, beacon_id)` -- Get received results for a beacon.

## modules/domain_dominance.py
Depends on: `core/hardening.py`
Imported by: `cli/commands/lateral_migrated.py`, `tests/test_security_alerts_fix.py`
- `DomainDominance.__init__` (method) `modules/domain_dominance.py:103` `def __init__(self)`
- `DomainDominance.get_instance` (method) `modules/domain_dominance.py:110` `def get_instance(cls)`
- `DomainDominance.dominate` (method) `modules/domain_dominance.py:121` `def dominate(self, domain, dc_ip, username, password, ntlm_hash)` -- Execute the full AD dominance kill-chain.
- `DomainDominance.enumerate_domain` (method) `modules/domain_dominance.py:194` `def enumerate_domain(self, domain, dc_ip)` -- Enumerate the target domain topology.
- `DomainDominance.extract_credentials` (method) `modules/domain_dominance.py:227` `def extract_credentials(self, domain_info, known_creds)` -- Extract credentials using the discovered domain topology.
- `DomainDominance.escalate` (method) `modules/domain_dominance.py:260` `def escalate(self, domain_info, stash)` -- Escalate privileges and move laterally through the domain.
- `DomainDominance.persist` (method) `modules/domain_dominance.py:314` `def persist(self, domain_info)` -- Establish persistence mechanisms across the domain.


Next: [API_p11.md](API_p11.md)
