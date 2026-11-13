# API (page 11 of 28)
Previous: [API_p10.md](API_p10.md)

## modules/bof_registry.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `modules/bof_admin.py`
Imported by: `cli/commands/bof_registry.py`, `modules/bof_delivery.py`, `tests/test_bof_registry.py`, `tests/test_bof_repo_contract.py`
- `BofEntry.to_dict` (method) `modules/bof_registry.py:130` `def to_dict(self)` -- Serialize to dictionary.
- `BofEntry.from_dict` (method) `modules/bof_registry.py:151` `def from_dict(cls, raw)` -- Build from a dictionary.
- `BofCatalog.register` (method) `modules/bof_registry.py:183` `def register(self, entry)` -- Register a BOF entry in the catalog.
- `BofCatalog.register_many` (method) `modules/bof_registry.py:188` `def register_many(self, entries)` -- Register multiple BOF entries at once.
- `BofCatalog.get` (method) `modules/bof_registry.py:193` `def get(self, name)` -- Retrieve a BOF entry by name.
- `BofCatalog.search` (method) `modules/bof_registry.py:204` `def search(self, query)` -- Search catalog by keyword across name, description, and technique.
- `BofCatalog.list_by_category` (method) `modules/bof_registry.py:237` `def list_by_category(self, category)` -- Return all BOFs in a specific category.
- `BofCatalog.list_by_platform` (method) `modules/bof_registry.py:241` `def list_by_platform(self, platform)` -- Return all BOFs for a specific platform.
- `BofCatalog.list_all` (method) `modules/bof_registry.py:245` `def list_all(self)` -- Return all catalog entries sorted by name.
- `BofCatalog.to_dict` (method) `modules/bof_registry.py:249` `def to_dict(self)` -- Serialize the entire catalog to a dictionary.
- `BofCatalog.from_dict` (method) `modules/bof_registry.py:257` `def from_dict(cls, raw)` -- Build a catalog from a dictionary.
- `BofCatalog.load` (method) `modules/bof_registry.py:265` `def load(cls, path)` -- Load a catalog from a JSON file.
- `BofCatalog.save` (method) `modules/bof_registry.py:273` `def save(self, path)` -- Save the catalog to a JSON file.
- `BofYamlStore.__init__` (method) `modules/bof_registry.py:290` `def __init__(self, directory)` -- Bind the store to a directory.
- `BofYamlStore.directory` (method) `modules/bof_registry.py:299` `def directory(self)` -- Return the directory bound to this store.
- `BofYamlStore.load_entries` (method) `modules/bof_registry.py:303` `def load_entries(self)` -- Parse every YAML file into :class:`BofEntry` objects.
- `BofYamlStore.load_catalog` (method) `modules/bof_registry.py:342` `def load_catalog(self)` -- Build a :class:`BofCatalog` from the YAML configuration files.
- `find_client_artifact` (function) `modules/bof_registry.py:362` `def find_client_artifact(entry)` -- Resolve the compiled object file of a BOF across all known source trees.
- `client_addon_install_path` (function) `modules/bof_registry.py:415` `def client_addon_install_path(client, addons_dir)` -- Read the ``tool.install_path`` of one beacon client lazyaddon.
- `stage_entry_bof` (function) `modules/bof_registry.py:441` `def stage_entry_bof(entry, sessions_dir)` -- Stage a compiled BOF object for beacon delivery.
- `BofValidator.compute_sha256` (method) `modules/bof_registry.py:483` `def compute_sha256(filepath)` -- Compute the SHA-256 hash of a file.
- `BofValidator.verify_entry` (method) `modules/bof_registry.py:492` `def verify_entry(entry, filepath)` -- Verify the SHA-256 of a downloaded BOF source matches the catalog.
- `BofValidator.validate_args` (method) `modules/bof_registry.py:508` `def validate_args(entry, args)` -- Validate that all required arguments are supplied.
- `BofRegistry.__init__` (method) `modules/bof_registry.py:527` `def __init__(self, sessions_dir)`
- `BofRegistry.install_dir` (method) `modules/bof_registry.py:533` `def install_dir(self)` -- Return the BOF installation directory.
- `BofRegistry.is_installed` (method) `modules/bof_registry.py:553` `def is_installed(self, name)` -- Return True if a BOF is installed.
- `BofRegistry.install` (method) `modules/bof_registry.py:558` `def install(self, entry)` -- Register a BOF as installed with current timestamp.
- `BofRegistry.uninstall` (method) `modules/bof_registry.py:579` `def uninstall(self, name, remove_files)` -- Unregister a BOF from the manifest and optionally remove its files.
- `BofRegistry.list_installed` (method) `modules/bof_registry.py:596` `def list_installed(self)` -- Return a list of all installed BOFs with metadata.
- `BofRegistry.get_install_info` (method) `modules/bof_registry.py:601` `def get_install_info(self, name)` -- Return installation metadata for a BOF, or None if not installed.
- `BofMarketplace.__init__` (method) `modules/bof_registry.py:619` `def __init__(self, sessions_dir, catalog)`
- `BofMarketplace.catalog` (method) `modules/bof_registry.py:630` `def catalog(self)` -- Return the catalog.
- `BofMarketplace.registry` (method) `modules/bof_registry.py:635` `def registry(self)` -- Return the registry.
- `BofMarketplace.search` (method) `modules/bof_registry.py:639` `def search(self, query)` -- Search the catalog and return enriched results with install status.
- `BofMarketplace.info` (method) `modules/bof_registry.py:658` `def info(self, name)` -- Get detailed information about a BOF by name.
- `BofMarketplace.install` (method) `modules/bof_registry.py:675` `def install(self, name)` -- Install a BOF from the catalog by name.
- `BofMarketplace.uninstall` (method) `modules/bof_registry.py:704` `def uninstall(self, name)` -- Uninstall a BOF by name.
- `BofMarketplace.list_installed` (method) `modules/bof_registry.py:717` `def list_installed(self)` -- List all installed BOFs with catalog enrichment.
- `BofMarketplace.list_missing_dependencies` (method) `modules/bof_registry.py:729` `def list_missing_dependencies(self, name)` -- Return a list of dependencies for a BOF that are not installed.
- `BofMarketplace.bulk_install` (method) `modules/bof_registry.py:737` `def bulk_install(self, names)` -- Install multiple BOFs at once.

## modules/browser_sync.py
Depends on: `modules/__init__.py`, `modules/backdoor/server.c`
Imported by: `modules/chain_runner.py`, `modules/lazy_proxy.py`, `modules/lazyown_bprfuzzer.py`, `tests/conftest.py`
- `token` (function) `modules/browser_sync.py:112` `def token(create)` -- Return the receiver auth token, generating it on first use.
- `reset_token` (function) `modules/browser_sync.py:138` `def reset_token()` -- Regenerate the receiver token.
- `load_profile` (function) `modules/browser_sync.py:151` `def load_profile()` -- Load the last synced browser identity profile.
- `profile_stats` (function) `modules/browser_sync.py:164` `def profile_stats()` -- Summarise the synced profile.
- `cookie_matches_host` (function) `modules/browser_sync.py:183` `def cookie_matches_host(cookie, host)` -- Return True when a synced cookie applies to a request host.
- `cookie_matches_path` (function) `modules/browser_sync.py:202` `def cookie_matches_path(cookie, request_path)` -- Return True when a synced cookie applies to one request path.
- `cookie_expired` (function) `modules/browser_sync.py:226` `def cookie_expired(cookie, now)` -- Return True when a persistent cookie is already expired.
- `cookies_for_host` (function) `modules/browser_sync.py:248` `def cookies_for_host(profile, host, path, scheme)` -- Return synced cookies a browser would send for one request.
- `build_cookie_header` (function) `modules/browser_sync.py:285` `def build_cookie_header(existing, cookies)` -- Merge synced cookies into an existing Cookie header.
- `write_netscape_jar` (function) `modules/browser_sync.py:340` `def write_netscape_jar(profile, path)` -- Write the synced cookie store as a Netscape cookie jar.
- `jar_path` (function) `modules/browser_sync.py:362` `def jar_path()` -- Return the cookie jar path as a string.
- `apply_rules` (function) `modules/browser_sync.py:418` `def apply_rules(headers, body)` -- Apply Burp-style Match and Replace rules to request headers and body.
- `apply_identity_headers` (function) `modules/browser_sync.py:475` `def apply_identity_headers(host, headers, body, path, scheme)` -- Inject the synced browser identity into one proxied request.
- `SyncReceiver.__init__` (method) `modules/browser_sync.py:595` `def __init__(self, host, port)` -- Prepare state; nothing binds until :meth:`start`.
- `SyncReceiver.start` (method) `modules/browser_sync.py:610` `def start(self, host, port)` -- Bind the receiver; idempotent while already running.
- `_Handler.log_message` (method) `modules/browser_sync.py:638` `def log_message(self, fmt)` -- Silence per-request logging; the profile is the audit trail.
- `_Handler.do_GET` (method) `modules/browser_sync.py:642` `def do_GET(self)` -- Answer the health probe.
- `_Handler.do_POST` (method) `modules/browser_sync.py:654` `def do_POST(self)` -- Accept one identity sync push.
- `_Handler.stop` (method) `modules/browser_sync.py:755` `def stop(self)` -- Shut the receiver down; safe when it was never started.
- `_Handler.status` (method) `modules/browser_sync.py:771` `def status(self)` -- Report running state, address, token and profile stats.
- `get_receiver` (function) `modules/browser_sync.py:791` `def get_receiver()` -- Return the process-wide shared receiver instance.
- `start_receiver` (function) `modules/browser_sync.py:800` `def start_receiver(port, host)` -- Start the shared receiver.
- `stop_receiver` (function) `modules/browser_sync.py:813` `def stop_receiver()` -- Stop the shared receiver.
- `clear_profile` (function) `modules/browser_sync.py:822` `def clear_profile()` -- Delete the synced profile and cookie jar.
- `apply_identity_to_url` (function) `modules/browser_sync.py:839` `def apply_identity_to_url(url, headers, body)` -- Apply the synced browser identity to one URL-scoped request.
- `ensure_wiring` (function) `modules/browser_sync.py:864` `def ensure_wiring()` -- Start the receiver and route framework traffic through the recorder proxy.
- `masked_rows` (function) `modules/browser_sync.py:906` `def masked_rows(profile, domain_filter, full)` -- Render synced cookies as display rows with masked values.

## modules/bsb_compat.py
Depends on: `core/logging.py`
Imported by: `lazyc2.py`, `tests/test_bsb_fileless_compat.py`
- `derive_bsb_keys` (function) `modules/bsb_compat.py:52` `def derive_bsb_keys(master_key)` -- Derive the BSB encryption and HMAC keys from the raw C2 key.
- `decrypt_bsb_report` (function) `modules/bsb_compat.py:90` `def decrypt_bsb_report(encrypted_data, master_key, replay_window_seconds)` -- Decrypt and decode one BSB report.
- `encrypt_bsb_command` (function) `modules/bsb_compat.py:139` `def encrypt_bsb_command(data, master_key)` -- Encrypt one command for a BSB beacon in the legacy wire format.
- `derive_bsb_stage_keys` (function) `modules/bsb_compat.py:162` `def derive_bsb_stage_keys(token)` -- Derive the staging encryption and HMAC keys from a staging token.
- `encrypt_bsb_stage_blob` (function) `modules/bsb_compat.py:208` `def encrypt_bsb_stage_blob(data, token)` -- Encrypt one staging payload in the diskless-stager wire format.
- `decrypt_bsb_stage_blob` (function) `modules/bsb_compat.py:232` `def decrypt_bsb_stage_blob(encrypted_data, token)` -- Decode one staging payload exactly the way the upstream stager does.

## modules/c2_agent.py
Depends on: `core/logging.py`, `core/session_secrets.py`, `lazyc2/security/services.py`, `modules/atomic_exploit_bridge.py`
Imported by: `cli/commands/c2_session.py`
- `client_id_for` (function) `modules/c2_agent.py:94` `def client_id_for(target, privilege)` -- Derive a stable, file-safe client id from a target IP.
- `validate_client_id` (function) `modules/c2_agent.py:119` `def validate_client_id(raw)` -- Validate a client id (alphanumerics, dash, underscore).
- `build_agent` (function) `modules/c2_agent.py:398` `def build_agent(c2_url, client_id, aes_hex, rat_key, route, sleep, privilege)` -- Render the agent script for a target (pure function, no I/O).
- `read_aes_hex` (function) `modules/c2_agent.py:528` `def read_aes_hex()` -- Read the live C2 AES key hex (snapshotted, never generated).
- `deploy` (function) `modules/c2_agent.py:533` `def deploy(target, c2_base, route, lhost, sleep, privilege)` -- Deliver + launch the agent on *target* via a working shell primitive.
- `read_records` (function) `modules/c2_agent.py:680` `def read_records(client_id, limit)` -- Read the latest beacon records for a client (newest last).
- `wait_record` (function) `modules/c2_agent.py:697` `def wait_record(client_id, command, since, timeout)` -- Wait for a fresh record matching *command* (polls the JSONL log).
- `C2Server.__init__` (method) `modules/c2_agent.py:714` `def __init__(self, port, user, password)`
- `C2Server.status` (method) `modules/c2_agent.py:731` `def status(self)` -- Report server liveness and listener reachability.
- `C2Server.start` (method) `modules/c2_agent.py:763` `def start(self)` -- Start lazyc2 headless (no-op when already running).
- `C2Server.stop` (method) `modules/c2_agent.py:794` `def stop(self)` -- Stop the headless server (SIGTERM, best-effort).
- `C2Server.ensure_http_listener` (method) `modules/c2_agent.py:817` `def ensure_http_listener(self, http_port, auth)` -- Add + start a plaintext lab listener via the C2 API (py2 agents lack TLS).

## modules/c2_builder.py
Depends on: `core/config.py`, `core/session_secrets.py`, `core/validators.py`, `modules/beacon_config_builder.py`, `modules/metrics.py`, `utils.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `tests/test_bdd_infra_range_report.py`, `tests/test_implant_session_secrets.py`, `tests/test_infra_disposable.py`
- `C2Builder.__init__` (method) `modules/c2_builder.py:452` `def __init__(self, params, sessions_dir, cmd_fn, onecmd_fn, toastr_fn, c2_user, c2_pass)`
- `C2Builder.run` (method) `modules/c2_builder.py:510` `def run(self, line, choice, use_tunnel)` -- Execute the full C2 build pipeline.

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

## modules/campaign_blacklist.py
Imported by: `modules/selection/parquet.py`
- `campaign_blacklist` (function) `modules/campaign_blacklist.py:53` `def campaign_blacklist()` -- Return the cached blacklist, reloading when the lessons file changes.
- `blocked_commands` (function) `modules/campaign_blacklist.py:63` `def blocked_commands(category)` -- Return command heads blacklisted for a category plus the global ``any``.

## modules/chain_approval.py
Imported by: `cli/apt_chain_support.py`, `cli/commands/command_and_control_migrated.py`, `lazyc2.py`, `tests/test_chain_approval_c2.py`, `tests/test_chain_approval_cli_wiring.py`
- `command_fingerprint` (function) `modules/chain_approval.py:78` `def command_fingerprint(command)` -- Return the SHA-256 fingerprint of one command line.
- `PendingStore.__init__` (method) `modules/chain_approval.py:117` `def __init__(self, sessions_dir)` -- Bind the store to one sessions directory.
- `PendingStore.create` (method) `modules/chain_approval.py:153` `def create(self, chain, step_id, command, timeout, run_id, now_override)` -- Register one pending approval request.
- `PendingStore.get` (method) `modules/chain_approval.py:204` `def get(self, request_id)` -- Return one request record or None.
- `PendingStore.list` (method) `modules/chain_approval.py:215` `def list(self, status)` -- Return request records newest first, optionally by status.
- `PendingStore.decide` (method) `modules/chain_approval.py:229` `def decide(self, request_id, allowed, decided_by, note, expired)` -- Record one decision or expiry, audited, idempotent-fail.
- `PendingStore.expire_stale` (method) `modules/chain_approval.py:282` `def expire_stale(self, now)` -- Expire every pending request past its deadline.
- `approval_backend` (function) `modules/chain_approval.py:318` `def approval_backend()` -- Return the configured approval backend.
- `build_c2_approver` (function) `modules/chain_approval.py:328` `def build_c2_approver(printer, chain_name, run_id, timeout, poll_interval, sessions_dir, clock)` -- Return an approver that routes confirm steps to the C2 pending list.
- `approve` (function) `modules/chain_approval.py:358` `def approve(step_id, command)`

## modules/chain_distill.py
Depends on: `core/logging.py`, `modules/chain_registry.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_scope.py`, `modules/verb_manifest.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `tests/test_chain_distill.py`, `tests/test_chain_distill_custody.py`, `tests/test_chain_distill_scope.py`, `tests/test_codeql_alert_fixes.py`
- `locate_traces` (function) `modules/chain_distill.py:93` `def locate_traces(task, sessions_dir)` -- Find the exp/traffic pair of one loop task under sessions/.
- `DistillReport.kept` (method) `modules/chain_distill.py:507` `def kept(self)` -- Count decisions turned into steps.
- `DistillReport.dropped` (method) `modules/chain_distill.py:512` `def dropped(self)` -- Count decisions rejected with a reason.
- `DistillReport.to_dict` (method) `modules/chain_distill.py:516` `def to_dict(self)` -- Return a JSON-serializable report.
- `DistillReport.render` (method) `modules/chain_distill.py:543` `def render(self, verbose)` -- Return printable report lines.
- `build_chain_data` (function) `modules/chain_distill.py:574` `def build_chain_data(task, rows, graph, manifests)` -- Turn deduped traffic rows and graph context into chain YAML data.
- `note` (function) `modules/chain_distill.py:598` `def note(row, kept, reason)` -- Record one keep/drop decision for the report.
- `distill` (function) `modules/chain_distill.py:687` `def distill(task, sessions_dir, write, chains_dir)` -- Distill one loop task into a validated chain YAML.

## modules/chain_facts.py
Depends on: `core/logging.py`, `modules/chain_runner.py`, `skills/lazyown_facts.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `modules/chain_loop.py`, `modules/gym_matrix_runner.py`, `tests/test_chain_loop.py`, `tests/test_f4_hardening.py`
- `spool_chain_outputs` (function) `modules/chain_facts.py:24` `def spool_chain_outputs(result, sessions_dir, fact_store_factory)` -- Persist one chain run's outputs and ingest them as facts.

## modules/chain_family.py
Depends on: `modules/lazy_loop.py`
Imported by: `cli/apt_chain_support.py`, `cli/commands/command_and_control_migrated.py`, `tests/test_chain_family.py`
- `family_signature` (function) `modules/chain_family.py:41` `def family_signature(facts)` -- Return a stable structural signature for a target from its facts.
- `FamilyRegistry.__init__` (method) `modules/chain_family.py:76` `def __init__(self, path)` -- Bind the registry to a JSON file.
- `FamilyRegistry.record_association` (method) `modules/chain_family.py:111` `def record_association(self, signature, chain, target)` -- Record that ``chain`` was synthesised for a target of this family.
- `FamilyRegistry.record_win` (method) `modules/chain_family.py:117` `def record_win(self, signature, chain, target)` -- Record that ``chain`` proved a target of this family.
- `FamilyRegistry.best` (method) `modules/chain_family.py:123` `def best(self, signature)` -- Return the strongest chain recorded for a family, or None.
- `FamilyRegistry.transfer_note` (method) `modules/chain_family.py:159` `def transfer_note(self, facts)` -- Return an operator note when this family has a known winning chain.
- `default_registry` (function) `modules/chain_family.py:185` `def default_registry()` -- Return a registry bound to the shared ``chain_families.json``.

## modules/chain_loop.py
Depends on: `cli/apt_chain_support.py`, `core/config.py`, `modules/auto_registry.py`, `modules/chain_facts.py`, `modules/chain_registry.py`, `modules/chain_runner.py`, `modules/chain_state.py`
Imported by: `modules/lazy_loop.py`, `tests/test_chain_loop.py`, `tests/test_playbook_chain.py`
- `chain_mode` (function) `modules/chain_loop.py:35` `def chain_mode()` -- Return the configured chain transport mode for loop runs.
- `is_chain_command` (function) `modules/chain_loop.py:53` `def is_chain_command(command)` -- True when the command line invokes the apt_chain verb.
- `parse_chain_invocation` (function) `modules/chain_loop.py:58` `def parse_chain_invocation(command)` -- Split one ``apt_chain`` command line into name, target and vars.
- `stepwise_eligible` (function) `modules/chain_loop.py:109` `def stepwise_eligible(chain, routable)` -- Decide whether one chain can run stepwise inside the worker.
- `ChainStepBlocked.__init__` (method) `modules/chain_loop.py:142` `def __init__(self, status, detail)` -- Record the guard status and reason.
- `run_chain_stepwise` (function) `modules/chain_loop.py:154` `def run_chain_stepwise(worker, intent, command, executor, budget, intercept, retry_state)` -- Run one ``apt_chain`` decision step-by-step inside the worker.
- `guarded` (function) `modules/chain_loop.py:226` `def guarded(step_command)` -- Route one chain step through the worker's guard path.
- `on_step` (function) `modules/chain_loop.py:283` `def on_step(outcome)` -- Emit one chain_step telemetry event.

## modules/chain_match.py
Depends on: `modules/chain_registry.py`
Imported by: `modules/selection/chain.py`, `tests/test_chain_match_determinism.py`, `tests/test_chain_selector.py`, `tests/test_lazy_loop.py`, `tests/test_selectors_base.py`
- `normalize_tags` (function) `modules/chain_match.py:49` `def normalize_tags(tags)` -- Return a chain's tags lowercased and aliased to the shared vocabulary.
- `service_tokens` (function) `modules/chain_match.py:65` `def service_tokens(services)` -- Normalise discovered service names into the chain tag vocabulary.
- `platform_ok` (function) `modules/chain_match.py:75` `def platform_ok(platforms, os_hint)` -- Return True when a chain's platforms admit the target OS hint.
- `score` (function) `modules/chain_match.py:86` `def score(tags, phase, svc_tokens)` -- Score one chain's tags for the phase and discovered services.
- `reset_cache` (function) `modules/chain_match.py:101` `def reset_cache()` -- Clear the process-wide registry scan cache (tests, long-lived loops).
- `load_rows` (function) `modules/chain_match.py:109` `def load_rows(allow_lab, ttl)` -- Return enabled, valid, non-lab chain rows, cached for the TTL.
- `best_chain` (function) `modules/chain_match.py:139` `def best_chain(phase, os_hint, services, exclude, allow_lab, rows, ttl)` -- Return the ``(name, reason)`` of the best matching chain, or None.

## modules/chain_registry.py
Depends on: `core/logging.py`
Imported by: `cli/apt_chain_support.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/exploit_migrated.py`, `cli/orchestrator_assets_tabs.py`, `cli/retry_support.py`, `modules/ad_gym.py`, `modules/auto_registry.py`, `modules/chain_distill.py`, `modules/chain_loop.py`, `modules/chain_match.py`, `modules/chain_runner.py`, `modules/chain_synth.py`, `modules/gym_matrix_runner.py`, `modules/gym_winbox_runner.py`, `modules/metasploitable_gym.py`, `modules/playbook_chain.py`, `modules/selection/playbook.py`, `modules/selection/technique_chain.py`, `modules/verb_manifest.py`, `modules/winbox_gym.py`, `skills/mcp_tools/apt_chain.py`, `tests/test_apt_chain_admin.py`, `tests/test_apt_chain_integration.py`, `tests/test_audit_remediation.py`, `tests/test_bof_repo_contract.py`, `tests/test_chain_distill.py`, `tests/test_chain_distill_custody.py`, `tests/test_chain_evidence.py`, `tests/test_chain_finalizer.py`, `tests/test_chain_freshness_guard.py`, `tests/test_chain_loop.py`, `tests/test_chain_parallel_fallback.py`, `tests/test_chain_registry.py`, `tests/test_chain_runner.py`, `tests/test_chain_step_streaming.py`, `tests/test_chain_token_hardening.py`, `tests/test_chain_v24_core.py`, `tests/test_f4_hardening.py`, `tests/test_lazy_adaptive_replan.py`, `tests/test_lazy_deviations.py`, `tests/test_metasploitable_gym.py`, `tests/test_playbook_chain.py`, `tests/test_retry_session.py`, `tests/test_selectors_capabilities.py`, `tests/test_verb_manifest.py`
- `skip_pending` (function) `modules/chain_registry.py:69` `def skip_pending(path, max_age, now)` -- Return the skip reason when an artefact is present and fresh.
- `ChainStep.identifier` (method) `modules/chain_registry.py:152` `def identifier(self)` -- Return the declared id or a stable generated one.
- `Chain.resolve` (method) `modules/chain_registry.py:176` `def resolve(self, tokens)` -- Substitute tokens, evaluate conditions and guards.
- `evaluate_when` (function) `modules/chain_registry.py:297` `def evaluate_when(expression, variables)` -- Evaluate a safe ``when`` expression against string variables.
- `validate_chain` (function) `modules/chain_registry.py:362` `def validate_chain(data, filename, chains_dir)` -- Validate raw YAML data against the chain schema.
- `render_text_token_braces` (function) `modules/chain_registry.py:586` `def render_text_token_braces(text)` -- Return text with every ``{name}`` token replaced by a placeholder.
- `load_all` (function) `modules/chain_registry.py:591` `def load_all(chains_dir)` -- Load every valid, enabled chain file (skips the rest loudly).
- `get` (function) `modules/chain_registry.py:749` `def get(name, chains_dir)` -- Return one chain by name, or None.
- `scan_all` (function) `modules/chain_registry.py:754` `def scan_all(chains_dir)` -- List every chain file including disabled ones (for administration).
- `set_enabled` (function) `modules/chain_registry.py:814` `def set_enabled(name, enabled, chains_dir)` -- Flip a chain's ``enabled`` flag in its YAML file (round-trip).
- `generate_for_playbook` (function) `modules/chain_registry.py:837` `def generate_for_playbook(engine_key, apt_display, description, chains_dir, overwrite)` -- Write a per-APT chain file inheriting the base APT chain.

## modules/chain_runner.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `modules/__init__.py`, `modules/browser_sync.py`, `modules/chain_registry.py`, `modules/chain_state.py`, `modules/detection_oracle.py`, `modules/hunt_verify.py`, `modules/lazy_deviations.py`, `modules/loop_guardrails.py`, `modules/outcome_bus.py`, `modules/verb_manifest.py`
Imported by: `cli/apt_chain_support.py`, `cli/commands/command_and_control_migrated.py`, `cli/retry_support.py`, `modules/chain_facts.py`, `modules/chain_loop.py`, `modules/gym_matrix_runner.py`, `tests/test_chain_distill_custody.py`, `tests/test_chain_evidence.py`, `tests/test_chain_finalizer.py`, `tests/test_chain_freshness_guard.py`, `tests/test_chain_parallel_fallback.py`, `tests/test_chain_runner.py`, `tests/test_chain_step_streaming.py`, `tests/test_chain_token_hardening.py`, `tests/test_chain_v24_core.py`, `tests/test_f4_hardening.py`, `tests/test_lazy_adaptive_replan.py`, `tests/test_lazy_deviations.py`, `tests/test_mediation.py`, `tests/test_retry_session.py`
- `StepOutcome.ok` (method) `modules/chain_runner.py:90` `def ok(self)` -- Return True for success, dry-run and skipped steps.
- `StepOutcome.to_dict` (method) `modules/chain_runner.py:94` `def to_dict(self)` -- Return a JSON-serializable view.
- `ChainRunResult.to_dict` (method) `modules/chain_runner.py:149` `def to_dict(self)` -- Return a JSON-serializable view.
- `ChainRunResult.chain_proven` (method) `modules/chain_runner.py:174` `def chain_proven(self)` -- Return whether every declared hunting dependency is observed.
- `ReplanContext.set_var` (method) `modules/chain_runner.py:197` `def set_var(self, name, value)` -- Record a variable the next steps should see.
- `ReplanContext.insert_step` (method) `modules/chain_runner.py:202` `def insert_step(self, step)` -- Record one step to execute right after the finished step.
- `ReplanContext.skip_rest` (method) `modules/chain_runner.py:207` `def skip_rest(self)` -- Record that remaining steps must not execute.
- `ReplanContext.applied_vars` (method) `modules/chain_runner.py:212` `def applied_vars(self)` -- Return recorded variable changes.
- `ReplanContext.inserted` (method) `modules/chain_runner.py:217` `def inserted(self)` -- Return recorded steps to insert.
- `ReplanContext.skip_rest_flag` (method) `modules/chain_runner.py:222` `def skip_rest_flag(self)` -- Return True when remaining steps should be skipped.
- `render_text` (function) `modules/chain_runner.py:227` `def render_text(template, variables)` -- Substitute single-brace tokens in one pass.
- `ChainRunner.__init__` (method) `modules/chain_runner.py:238` `def __init__(self, chain, tokens, shell, executor, default_timeout, dry_run, on_step, retry_backoff, total_timeout...` -- Bind the chain, the execution primitive and operator switches.
- `ChainRunner.run` (method) `modules/chain_runner.py:363` `def run(self)` -- Execute the chain in order and return every step outcome.

## modules/chain_state.py
Imported by: `cli/apt_chain_support.py`, `cli/commands/command_and_control_migrated.py`, `cli/retry_support.py`, `modules/chain_loop.py`, `modules/chain_runner.py`, `modules/retry_session.py`, `tests/test_apt_chain_admin.py`, `tests/test_chain_v24_core.py`, `tests/test_retry_session.py`
- `checkpoint_dir` (function) `modules/chain_state.py:26` `def checkpoint_dir(base_dir)` -- Return the directory that stores chain checkpoints.
- `new_run_id` (function) `modules/chain_state.py:33` `def new_run_id(chain_name)` -- Return a collision-resistant run id for one chain execution.
- `write_checkpoint` (function) `modules/chain_state.py:39` `def write_checkpoint(directory, state)` -- Persist one chain run state as JSON and return the file path.
- `load_checkpoint` (function) `modules/chain_state.py:65` `def load_checkpoint(directory, run_id)` -- Load one checkpoint by run id, or None when missing/unreadable.
- `list_checkpoints` (function) `modules/chain_state.py:80` `def list_checkpoints(directory, limit, chain)` -- Return the newest checkpoints (run_id, chain, target, state, times).

## modules/chain_synth.py
Depends on: `modules/chain_registry.py`, `skills/lazyown_facts.py`
Imported by: `cli/apt_chain_support.py`, `cli/commands/command_and_control_migrated.py`, `modules/lazy_autofire.py`, `modules/selection/technique_chain.py`, `tests/test_chain_synth.py`, `tests/test_selection_technique_chain.py`
- `synth_chain_data` (function) `modules/chain_synth.py:91` `def synth_chain_data(playbook, target, services, has_creds, os_hint, include_c2, techniques)` -- Compose the chain dict for a host; (data, notes).
- `facts_for_target` (function) `modules/chain_synth.py:243` `def facts_for_target(target)` -- Pull host facts from the FactStore for synthesis inputs.
- `synth_technique_chain_data` (function) `modules/chain_synth.py:272` `def synth_technique_chain_data(target, techniques, os_hint)` -- Compose a focused chain of ordered MITRE/atomic technique steps.
- `write_generated_chain` (function) `modules/chain_synth.py:339` `def write_generated_chain(data, chains_dir)` -- Validate and persist the generated chain file; returns (path, errors).

## modules/chain_tokens.py
Depends on: `skills/lazyown_facts.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `modules/lazypoophish.py`, `tests/test_apt_chain_admin.py`
- `token_keys` (function) `modules/chain_tokens.py:24` `def token_keys()` -- Return every engagement token name this module can produce.
- `build_tokens` (function) `modules/chain_tokens.py:29` `def build_tokens(target, params)` -- Resolve engagement tokens for one target.

## modules/cicd_enumerator.py
Imported by: `cli/commands/cicd.py`
- `CICDEnumerator.__init__` (method) `modules/cicd_enumerator.py:54` `def __init__(self, target_url, sessions_dir)`
- `CICDEnumerator.scan` (method) `modules/cicd_enumerator.py:60` `def scan(self)` -- Run all CI/CD scans.
- `CICDEnumerator.scan_build_log` (method) `modules/cicd_enumerator.py:297` `def scan_build_log(self, log_content, source)` -- Scan a build log for leaked secrets.
- `CICDEnumerator.generate_ci_attack_matrix` (method) `modules/cicd_enumerator.py:322` `def generate_ci_attack_matrix(self)` -- Generate a comprehensive CI/CD attack matrix.
- `CICDEnumerator.export_findings` (method) `modules/cicd_enumerator.py:387` `def export_findings(self)` -- Export CI/CD findings to a JSON file.

## modules/cli_auth.py
Depends on: `cli/engagement_hooks.py`, `core/config.py`, `modules/lazy_rbac.py`
Imported by: `cli/auto_crypto.py`, `cli/banner_config.py`, `cli/commands/cli_auth.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `cli/wizard.py`, `lazyown.py`, `modules/redteam_gym.py`, `modules/world_model.py`, `tests/test_cli_auth_remember.py`, `tests/test_codeql_alert_fixes.py`, `tests/test_engagement_elo_and_methodology.py`
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

## modules/closedloop.py
Depends on: `modules/defense_eval.py`
Imported by: `modules/defense_stages.py`, `tests/test_closedloop.py`
- `RuleMetrics.to_dict` (method) `modules/closedloop.py:42` `def to_dict(self)` -- Return a JSON-serializable view.
- `Comparison.to_dict` (method) `modules/closedloop.py:66` `def to_dict(self)` -- Return a JSON-serializable view.
- `compare_rules` (function) `modules/closedloop.py:90` `def compare_rules(baseline_rule, candidate_rule, target_logs, control_logs)` -- Replay baseline and candidate rules over identical datasets.
- `suggest_tuning` (function) `modules/closedloop.py:136` `def suggest_tuning(candidate, baseline)` -- Return deterministic tuning suggestions from replay evidence.

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
Imported by: `cli/commands/collaboration.py`, `lazyc2.py`, `modules/engagement_hooks.py`, `modules/event_bus.py`, `skills/mcp_tools/collab_publish.py`, `tests/test_collab_and_onboarding.py`, `tests/test_core_modules.py`
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
Depends on: `core/logging.py`, `modules/factsio.py`
Imported by: `lazyc2.py`, `tests/test_single_source_of_truth.py`
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
- `ComplianceEngine.export_pdf` (method) `modules/compliance.py:857` `def export_pdf(self, report, output_path)`
- `ComplianceEngine.add_evidence` (method) `modules/compliance.py:927` `def add_evidence(self, filepath, operator, description)`
- `ComplianceEngine.verify_evidence_chain` (method) `modules/compliance.py:930` `def verify_evidence_chain(self)`

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


Next: [API_p12.md](API_p12.md)
