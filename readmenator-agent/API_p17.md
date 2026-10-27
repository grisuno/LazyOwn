# API (page 17 of 24)
Previous: [API_p16.md](API_p16.md)

## modules/retry_session.py
Depends on: `modules/chain_state.py`
Imported by: `cli/retry_support.py`, `tests/test_codeql_alert_fixes.py`, `tests/test_retry_session.py`
- `is_active` (function) `modules/retry_session.py:56` `def is_active()` -- Return True when an elevated retry session is currently armed.
- `secret_enabled_path` (function) `modules/retry_session.py:61` `def secret_enabled_path()` -- Return the askpass helper path advertised via ``SUDO_ASKPASS``.
- `sudo_gate_open` (function) `modules/retry_session.py:79` `def sudo_gate_open()` -- Return True when armed and the on-disk askpass pair is sound.
- `set_sudo_secret` (function) `modules/retry_session.py:94` `def set_sudo_secret(secret)` -- Arm the elevated retry session with one secret.
- `clear_sudo_secret` (function) `modules/retry_session.py:125` `def clear_sudo_secret()` -- Disarm the elevated retry session and wipe the secret from disk.
- `apply_sudo_askpass` (function) `modules/retry_session.py:137` `def apply_sudo_askpass(command)` -- Rewrite bare ``sudo`` tokens to ``sudo -A`` for one command.
- `newest_failed_checkpoint` (function) `modules/retry_session.py:180` `def newest_failed_checkpoint(chain, run_id)` -- Return the freshest unfinished checkpoint of one chain.
- `resolve_sudo_consent` (function) `modules/retry_session.py:204` `def resolve_sudo_consent(confirmer, want_sudo)` -- Gate the elevated mode behind an explicit, warned confirmation.

## modules/reverse-shell.c
- `reverse_shell_init` (function) `modules/reverse-shell.c:12` `static int __init reverse_shell_init(void)` -- call_usermodehelper function is used to create user mode processes from kernel space
- `reverse_shell_exit` (function) `modules/reverse-shell.c:16` `static void __exit reverse_shell_exit(void)`

## modules/revshell.c
- `xlAutoOpen` (function) `modules/revshell.c:5` `void __cdecl xlAutoOpen()`
- `DllMain` (function) `modules/revshell.c:10` `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)`

## modules/rich_tui.py
Depends on: `core/console.py`, `modules/dashboard_engine.py`
Imported by: `cli/commands/pwn.py`
- `RichDashboard.__init__` (method) `modules/rich_tui.py:74` `def __init__(self, dashboard_engine, refresh_interval, live)` -- Initialize the Rich dashboard.
- `RichDashboard.run` (method) `modules/rich_tui.py:96` `def run(self)` -- Run the dashboard.
- `RichDashboard.stop` (method) `modules/rich_tui.py:132` `def stop(self)` -- Gracefully shut down the dashboard and restore terminal state.

## modules/rl_trainer.py
Depends on: `core/logging.py`
Imported by: `modules/lesson_ingestor.py`, `modules/loop_ai_bridge.py`, `skills/autonomous_daemon.py`, `skills/swan_agent.py`, `tests/test_moe_rl_swan.py`
- `IStateEncoder.encode` (method) `modules/rl_trainer.py:105` `def encode(self, task_type, engagement_phase, recent_reward_ema)` -- Return a string key representing the current state.
- `BucketedStateEncoder.encode` (method) `modules/rl_trainer.py:131` `def encode(self, task_type, engagement_phase, recent_reward_ema)`
- `QValueStore.__init__` (method) `modules/rl_trainer.py:156` `def __init__(self, path, optimistic_init)`
- `QValueStore.get` (method) `modules/rl_trainer.py:168` `def get(self, state, action)`
- `QValueStore.set` (method) `modules/rl_trainer.py:172` `def set(self, state, action, value)`
- `QValueStore.max_q` (method) `modules/rl_trainer.py:176` `def max_q(self, state, candidates)` -- Return max Q(state, a) over the given candidate actions.
- `QValueStore.argmax` (method) `modules/rl_trainer.py:182` `def argmax(self, state, candidates)` -- Return the action with highest Q(state, a).
- `QValueStore.save` (method) `modules/rl_trainer.py:188` `def save(self)`
- `EpsilonTracker.__init__` (method) `modules/rl_trainer.py:218` `def __init__(self, start, minimum, decay, path)`
- `EpsilonTracker.epsilon` (method) `modules/rl_trainer.py:233` `def epsilon(self)`
- `EpsilonTracker.step` (method) `modules/rl_trainer.py:236` `def step(self)` -- Apply one decay step and persist.
- `RLTrainer.__init__` (method) `modules/rl_trainer.py:284` `def __init__(self, config, state_encoder, q_store, epsilon_tracker)`
- `RLTrainer.encode_state` (method) `modules/rl_trainer.py:304` `def encode_state(self, task_type, engagement_phase, recent_reward_ema)` -- Convert environment observations into a discrete state key.
- `RLTrainer.select_action` (method) `modules/rl_trainer.py:313` `def select_action(self, state, candidates, force_exploit)` -- Epsilon-greedy expert selection.
- `RLTrainer.update` (method) `modules/rl_trainer.py:347` `def update(self, state, action, reward, next_state, candidates, detection_prob)` -- Apply one Q-learning update.
- `RLTrainer.best_expert_for_state` (method) `modules/rl_trainer.py:389` `def best_expert_for_state(self, state, candidates)` -- Return the highest Q-value expert for the given state (greedy).
- `RLTrainer.q_values_for_state` (method) `modules/rl_trainer.py:393` `def q_values_for_state(self, state, candidates)` -- Return {expert_id: q_value} for diagnostics.
- `RLTrainer.save` (method) `modules/rl_trainer.py:397` `def save(self)` -- Persist Q-table to disk.
- `RLTrainer.epsilon` (method) `modules/rl_trainer.py:402` `def epsilon(self)`
- `get_trainer` (function) `modules/rl_trainer.py:425` `def get_trainer(config)` -- Return (or create) the module-level singleton RLTrainer.

## modules/rootkit/mr.c
- `get_ld_preload` (function) `modules/rootkit/mr.c:84` `char *get_ld_preload()`
- `set_ld_preload` (function) `modules/rootkit/mr.c:87` `void set_ld_preload(const char *ld_preload)`
- `ensure_ld_preload` (function) `modules/rootkit/mr.c:100` `void ensure_ld_preload()`
- `ensure_pid_file_exists` (function) `modules/rootkit/mr.c:117` `void ensure_pid_file_exists()`
- `check_elevate` (function) `modules/rootkit/mr.c:136` `int check_elevate()`
- `write_file` (function) `modules/rootkit/mr.c:145` `void write_file(const char *path, const char *content, mode_t mode)`
- `crontab` (function) `modules/rootkit/mr.c:156` `void crontab(const char *path)`
- `generate_random_string` (function) `modules/rootkit/mr.c:168` `char *generate_random_string()`
- `xdg` (function) `modules/rootkit/mr.c:178` `void xdg(const char *path, int admin)`
- `kde_plasma` (function) `modules/rootkit/mr.c:200` `void kde_plasma(const char *path)`
- `copy_binary` (function) `modules/rootkit/mr.c:215` `void copy_binary(const char *source, const char *destination)`
- `persist` (function) `modules/rootkit/mr.c:234` `void persist(const char *path)`
- `ensure_key_file_exists` (function) `modules/rootkit/mr.c:253` `void ensure_key_file_exists()`
- `ensure_hide_file_exists` (function) `modules/rootkit/mr.c:271` `void ensure_hide_file_exists()`
- `infect_command` (function) `modules/rootkit/mr.c:289` `void infect_command()`
- `load_rootkit` (function) `modules/rootkit/mr.c:303` `void load_rootkit()`
- `unload_rootkit` (function) `modules/rootkit/mr.c:314` `void unload_rootkit()`
- `handle_client` (function) `modules/rootkit/mr.c:321` `void *handle_client(void *client_socket)`
- `mon_shell` (function) `modules/rootkit/mr.c:521` `void *mon_shell(void *data)`
- `signal_handler` (function) `modules/rootkit/mr.c:609` `void signal_handler(int signum)`
- `reboot_system` (function) `modules/rootkit/mr.c:615` `void reboot_system()`
- `main` (function) `modules/rootkit/mr.c:639` `int main()`

## modules/rootkit/mrhyde.c
- `load_hidden_pids` (function) `modules/rootkit/mrhyde.c:77` `void load_hidden_pids()`
- `load_hidden_files` (function) `modules/rootkit/mrhyde.c:97` `void load_hidden_files()`
- `unlink` (function) `modules/rootkit/mrhyde.c:117` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde.c:129` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde.c:149` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde.c:161` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde.c:182` `char* get_username_from_pid(pid_t pid)`
- `should_hide_pid` (function) `modules/rootkit/mrhyde.c:201` `int should_hide_pid(const char* pid)`
- `should_hide_file` (function) `modules/rootkit/mrhyde.c:216` `int should_hide_file(const char* filename)`
- `readdir` (function) `modules/rootkit/mrhyde.c:226` `struct dirent* readdir(DIR* dirp)`
- `fopen` (function) `modules/rootkit/mrhyde.c:287` `FILE *fopen(const char *pathname, const char *mode)`
- `my_open` (function) `modules/rootkit/mrhyde.c:331` `int my_open(const char *pathname, int flags, mode_t mode)`
- `my_openat` (function) `modules/rootkit/mrhyde.c:375` `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)`
- `stat` (function) `modules/rootkit/mrhyde.c:419` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde.c:463` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde.c:507` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde.c:561` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde.c:622` `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `main` (function) `modules/rootkit/mrhyde.c:682` `int main()`

## modules/rootkit/mrhyde2.c
- `load_hidden_pids` (function) `modules/rootkit/mrhyde2.c:67` `void load_hidden_pids()`
- `unlink` (function) `modules/rootkit/mrhyde2.c:87` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde2.c:99` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde2.c:119` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde2.c:131` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde2.c:152` `char* get_username_from_pid(pid_t pid)`
- `should_hide_pid` (function) `modules/rootkit/mrhyde2.c:171` `int should_hide_pid(const char* pid)`
- `readdir` (function) `modules/rootkit/mrhyde2.c:186` `struct dirent* readdir(DIR* dirp)`
- `fopen` (function) `modules/rootkit/mrhyde2.c:242` `FILE *fopen(const char *pathname, const char *mode)`
- `my_open` (function) `modules/rootkit/mrhyde2.c:279` `int my_open(const char *pathname, int flags, mode_t mode)`
- `my_openat` (function) `modules/rootkit/mrhyde2.c:316` `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)`
- `stat` (function) `modules/rootkit/mrhyde2.c:353` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde2.c:390` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde2.c:427` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde2.c:474` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde2.c:531` `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `main` (function) `modules/rootkit/mrhyde2.c:587` `int main()`

## modules/rootkit/mrhyde3.c
- `uring_queue_init` (function) `modules/rootkit/mrhyde3.c:89` `static int uring_queue_init(unsigned int entries, struct io_uring *ring)` -- /* Syscalls static inline int __io_uring_setup(unsigned int entries, struct io_uring_params *p) { return...
- `uring_get_sqe` (function) `modules/rootkit/mrhyde3.c:134` `static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring)` -- ring->cq.head = (unsigned *)((char *)cq_ring + params.cq_off.head); ring->cq.tail = (unsigned *)((char *)cq_ring +...
- `uring_submit` (function) `modules/rootkit/mrhyde3.c:145` `static int uring_submit(struct io_uring *ring)` -- } /* Obtener SQE static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring) { unsigned head = *ring->sq.head...
- `uring_wait_cqe_timeout` (function) `modules/rootkit/mrhyde3.c:153` `static int uring_wait_cqe_timeout(struct io_uring *ring, struct io_uring_cqe **cqe_ptr, int timeo...` -- struct io_uring_sqe *sqe = &ring->sq.sqes[tail & *ring->sq.ring_mask]; memset(sqe, 0, sizeof(*sqe)); return sqe; }...
- `uring_cqe_seen` (function) `modules/rootkit/mrhyde3.c:167` `static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe)`
- `init_root_ring` (function) `modules/rootkit/mrhyde3.c:180` `static int init_root_ring(void)` -- static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe) { (*ring->cq.head)++; } /* Estado global...
- `uring_read_whole_file` (function) `modules/rootkit/mrhyde3.c:201` `static char *uring_read_whole_file(const char *path)` -- } ring_ok = 1; /* Registrar buffer (opcional) struct iovec iov; iov.iov_base = malloc(IO_URING_BUFFER_SIZE)...
- `traditional_read_file` (function) `modules/rootkit/mrhyde3.c:257` `static char *traditional_read_file(const char *path)` -- if (bytes_read <= 0) break; buf = realloc(buf, total_read + bytes_read + 1); if (!buf) { close(fd)...
- `load_hidden_pids` (function) `modules/rootkit/mrhyde3.c:272` `void load_hidden_pids(void)` -- FILE *f = fopen(path, "rb"); if (!f) return NULL; fseek(f, 0, SEEK_END); long size = ftell(f); fseek(f, 0...
- `load_hidden_files` (function) `modules/rootkit/mrhyde3.c:286` `void load_hidden_files(void)`
- `get_username_from_pid` (function) `modules/rootkit/mrhyde3.c:301` `char* get_username_from_pid(pid_t pid)` -- char *data = uring_read_whole_file(FILE_HIDE_PATH); if (!data) data = traditional_read_file(FILE_HIDE_PATH); if...
- `should_hide_pid` (function) `modules/rootkit/mrhyde3.c:324` `int should_hide_pid(const char* pid)`
- `should_hide_file` (function) `modules/rootkit/mrhyde3.c:333` `int should_hide_file(const char* filename)`
- `readdir` (function) `modules/rootkit/mrhyde3.c:340` `struct dirent* readdir(DIR* dirp)`
- `unlink` (function) `modules/rootkit/mrhyde3.c:371` `int unlink(const char *pathname)`
- `kill` (function) `modules/rootkit/mrhyde3.c:377` `int kill(pid_t pid, int sig)`
- `remove` (function) `modules/rootkit/mrhyde3.c:387` `int remove(const char *pathname)`
- `unlinkat` (function) `modules/rootkit/mrhyde3.c:393` `int unlinkat(int dirfd, const char *pathname, int flags)`
- `fopen` (function) `modules/rootkit/mrhyde3.c:411` `FILE *fopen(const char *pathname, const char *mode)`
- `open` (function) `modules/rootkit/mrhyde3.c:434` `int open(const char *pathname, int flags, ...)`
- `openat` (function) `modules/rootkit/mrhyde3.c:462` `int openat(int dirfd, const char *pathname, int flags, ...)`
- `stat` (function) `modules/rootkit/mrhyde3.c:491` `int stat(const char *pathname, struct stat *statbuf)`
- `lstat` (function) `modules/rootkit/mrhyde3.c:515` `int lstat(const char *pathname, struct stat *statbuf)`
- `fstat` (function) `modules/rootkit/mrhyde3.c:539` `int fstat(int fd, struct stat *statbuf)`
- `getdents` (function) `modules/rootkit/mrhyde3.c:573` `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)`
- `getdents64` (function) `modules/rootkit/mrhyde3.c:609` `ssize_t getdents64(int fd, void *dirp, size_t count)`

## modules/rootkit/rootkit.c
Depends on: `core/crypto.py`, `lazyown-docker/init.sh`
- `regs_override_return` (function) `modules/rootkit/rootkit.c:54` `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` -- Define regs_override_return function
- `hooked_getdents` (function) `modules/rootkit/rootkit.c:86` `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked getdents function
- `hooked_getdents64` (function) `modules/rootkit/rootkit.c:112` `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked getdents64 function
- `hooked_read` (function) `modules/rootkit/rootkit.c:138` `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` -- Hooked read function to create a backdoor
- `disable_module_signature_verification` (function) `modules/rootkit/rootkit.c:192` `static void disable_module_signature_verification(void)` -- Function to disable module signature verification
- `hook_syscalls` (function) `modules/rootkit/rootkit.c:206` `static int __init hook_syscalls(void)` -- Function to hook system calls
- `unhook_syscalls` (function) `modules/rootkit/rootkit.c:219` `static void __exit unhook_syscalls(void)` -- Function to unhook system calls

## modules/saas_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `SaaSEnumerationTools.microsoft365_commands` (method) `modules/saas_attacks.py:75` `def microsoft365_commands()`
- `SaaSEnumerationTools.google_workspace_commands` (method) `modules/saas_attacks.py:100` `def google_workspace_commands()`
- `SaaSEnumerationTools.salesforce_commands` (method) `modules/saas_attacks.py:118` `def salesforce_commands()`
- `SaaSEnumerationTools.servicenow_commands` (method) `modules/saas_attacks.py:135` `def servicenow_commands()`
- `SaaSAttackEngine.__init__` (method) `modules/saas_attacks.py:163` `def __init__(self, config)`
- `SaaSAttackEngine.enumerate_all` (method) `modules/saas_attacks.py:166` `def enumerate_all(self)` -- Generate enumeration commands for all supported SaaS platforms.
- `SaaSAttackEngine.m365_ews_mail_search` (method) `modules/saas_attacks.py:179` `def m365_ews_mail_search(self, search_term)` -- Search mailboxes via Exchange Web Services (EWS).
- `SaaSAttackEngine.google_workspace_domain_wide_delegation` (method) `modules/saas_attacks.py:228` `def google_workspace_domain_wide_delegation(self)` -- Abuse Google Workspace Domain-Wide Delegation (DWD).
- `SaaSAttackEngine.salesforce_report_mining` (method) `modules/saas_attacks.py:257` `def salesforce_report_mining(self)` -- Mine Salesforce reports and dashboards for sensitive data.
- `SaaSAttackEngine.slack_data_mining` (method) `modules/saas_attacks.py:286` `def slack_data_mining(self)` -- Mine Slack Enterprise for sensitive conversations and files.
- `SaaSAttackEngine.detect_external_sharing` (method) `modules/saas_attacks.py:327` `def detect_external_sharing(self)` -- Detect external sharing configurations across SaaS platforms.
- `SaaSAttackEngine.summary` (method) `modules/saas_attacks.py:352` `def summary(self)`

## modules/security_sanitizers.py
Imported by: `lazyc2.py`, `lazyc2/blueprints/phishing.py`, `modules/lazyown_bprfuzzer.py`, `pwntomate.py`, `tests/test_security_sanitizers.py`
- `SecurityConfig.from_payload` (method) `modules/security_sanitizers.py:68` `def from_payload(cls, payload)` -- Build a configuration object from a ``payload.json`` mapping.
- `HeaderValueSanitizer.__init__` (method) `modules/security_sanitizers.py:115` `def __init__(self, config)` -- Bind the sanitizer to a configuration instance.
- `HeaderValueSanitizer.is_valid_name` (method) `modules/security_sanitizers.py:129` `def is_valid_name(self, name)` -- Return True iff ``name`` is a syntactically valid header token.
- `HeaderValueSanitizer.sanitize_value` (method) `modules/security_sanitizers.py:139` `def sanitize_value(self, value)` -- Return a header value that cannot smuggle a response split.
- `SessionPathResolver.__init__` (method) `modules/security_sanitizers.py:174` `def __init__(self, base_dir, config)` -- Bind the resolver to an absolute, real base directory.
- `SessionPathResolver.base_dir` (method) `modules/security_sanitizers.py:192` `def base_dir(self)` -- The resolved, absolute base directory.
- `SessionPathResolver.resolve` (method) `modules/security_sanitizers.py:196` `def resolve(self, untrusted_name)` -- Return ``(absolute, relative)`` for a safe filename.
- `SessionPathResolver.file_exists` (method) `modules/security_sanitizers.py:238` `def file_exists(self, untrusted_name)` -- Return True iff ``untrusted_name`` resolves to an existing file.
- `BindAddressResolver.__init__` (method) `modules/security_sanitizers.py:269` `def __init__(self, config, preferred_addresses)` -- Build a resolver with a prioritised list of candidate addresses.
- `BindAddressResolver.resolve` (method) `modules/security_sanitizers.py:298` `def resolve(self)` -- Return the address sockets should bind to.
- `CommandRedactor.__init__` (method) `modules/security_sanitizers.py:333` `def __init__(self, config)` -- Bind the redactor to a configuration instance.
- `CommandRedactor.render` (method) `modules/security_sanitizers.py:359` `def render(self, template, substitutions, username, password)` -- Return ``(executable, display)`` for a templated command.
- `OutputSanitizer.__init__` (method) `modules/security_sanitizers.py:418` `def __init__(self, config)` -- Bind the sanitizer to a configuration instance.
- `OutputSanitizer.sanitize` (method) `modules/security_sanitizers.py:429` `def sanitize(self, value)` -- Return ``value`` projected into a JSON-serialisable form.
- `build_default_config` (function) `modules/security_sanitizers.py:477` `def build_default_config(payload)` -- Return a :class:`SecurityConfig` populated from ``payload``.

## modules/selector_manager.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_auto_loop_memory.py`
- `select` (function) `modules/selector_manager.py:42` `def select(proposals, is_blocked)` -- Pick the first valid proposal; None when everything is filtered.

## modules/selfupdate.py
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`, `tests/test_autonomous_ops.py`, `tests/test_lazy_loop.py`
- `Updater.__init__` (method) `modules/selfupdate.py:47` `def __init__(self, live_path)` -- Bind the updater to the binary that may be replaced.
- `Updater.verify` (method) `modules/selfupdate.py:52` `def verify(self, artifact)` -- Return True when the payload matches its recorded digest.
- `Updater.stage` (method) `modules/selfupdate.py:57` `def stage(self, artifact, directory)` -- Write a verified payload into ``directory``.
- `Updater.rollback` (method) `modules/selfupdate.py:77` `def rollback(self)` -- Restore the ``<name>.old`` snapshot over the live binary.
- `current_branch` (function) `modules/selfupdate.py:96` `def current_branch(runner)` -- Return the checked-out branch name (empty on failure).
- `dirty` (function) `modules/selfupdate.py:102` `def dirty(runner)` -- Return True when the working tree has uncommitted changes.
- `check` (function) `modules/selfupdate.py:108` `def check(branch, runner)` -- Fetch the branch and report ahead/behind counts.
- `apply` (function) `modules/selfupdate.py:140` `def apply(branch, confirm, runner)` -- Fast-forward the tree to origin/<branch> when safe.

## modules/session_cleanup.py
Imported by: `lazyown.py`, `tests/test_infra_disposable.py`
- `find_cloudflared_pids` (function) `modules/session_cleanup.py:28` `def find_cloudflared_pids(ps_output)` -- Extract PIDs of ``cloudflared tunnel`` processes from ps output.
- `stop_cloudflared_processes` (function) `modules/session_cleanup.py:94` `def stop_cloudflared_processes()` -- Terminate stray ``cloudflared tunnel`` host processes.
- `cleanup_ephemeral_infra` (function) `modules/session_cleanup.py:120` `def cleanup_ephemeral_infra()` -- Stop all disposable infrastructure owned by this checkout.

## modules/session_rag.py
Depends on: `core/logging.py`
Imported by: `cli/commands/mcp_bridge.py`, `modules/reactive_engine.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`
- `_KeywordFallback.__init__` (method) `modules/session_rag.py:111` `def __init__(self)`
- `_KeywordFallback.load` (method) `modules/session_rag.py:115` `def load(self, path)` -- Load index from disk (no-op if file absent or corrupt).
- `_KeywordFallback.save` (method) `modules/session_rag.py:126` `def save(self, path)` -- Atomically persist index to disk.
- `_KeywordFallback.add` (method) `modules/session_rag.py:136` `def add(self, doc_id, text, meta)`
- `_KeywordFallback.query` (method) `modules/session_rag.py:146` `def query(self, query_text, n)`
- `_KeywordFallback.count` (method) `modules/session_rag.py:156` `def count(self)`
- `_KeywordFallback.reset` (method) `modules/session_rag.py:159` `def reset(self)`
- `_RagState.load` (method) `modules/session_rag.py:172` `def load(cls)`
- `_RagState.save` (method) `modules/session_rag.py:181` `def save(self)`
- `SessionRAG.__init__` (method) `modules/session_rag.py:191` `def __init__(self)`
- `SessionRAG.index_new` (method) `modules/session_rag.py:301` `def index_new(self)` -- Incrementally index only new or changed files.
- `SessionRAG.index_parquet_sources` (method) `modules/session_rag.py:322` `def index_parquet_sources(self, force)` -- Index knowledge-base parquets (techniques_enriched, binarios, lolbas_index) into the RAG store.
- `SessionRAG.index_all` (method) `modules/session_rag.py:411` `def index_all(self)` -- Full re-index from scratch.
- `SessionRAG.query` (method) `modules/session_rag.py:439` `def query(self, query_text, n, collection)` -- Return top-n relevant chunks as dicts with keys: text, source, chunk, score.
- `SessionRAG.context_for_step` (method) `modules/session_rag.py:489` `def context_for_step(self, phase, target, cmd, n)` -- Return a compact RAG context string suitable for injection into an LLM prompt.
- `SessionRAG.stats` (method) `modules/session_rag.py:509` `def stats(self)`
- `get_rag` (function) `modules/session_rag.py:535` `def get_rag()`

## modules/session_reader.py
Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `ImplantRecord.is_privileged` (method) `modules/session_reader.py:55` `def is_privileged(self)`
- `ImplantRecord.platform` (method) `modules/session_reader.py:60` `def platform(self)`
- `ImplantRecord.ip_list` (method) `modules/session_reader.py:69` `def ip_list(self)`
- `SessionSummary.active_client_ids` (method) `modules/session_reader.py:94` `def active_client_ids(self)`
- `SessionSummary.privileged_sessions` (method) `modules/session_reader.py:101` `def privileged_sessions(self)`
- `SessionSummary.unprivileged_sessions` (method) `modules/session_reader.py:108` `def unprivileged_sessions(self)`
- `SessionSummary.latest_for` (method) `modules/session_reader.py:114` `def latest_for(self, client_id)`
- `SessionSummary.task_by_status` (method) `modules/session_reader.py:118` `def task_by_status(self, status)`
- `AbstractReader.read` (method) `modules/session_reader.py:129` `def read(self, sessions_dir)`
- `ImplantCSVReader.read` (method) `modules/session_reader.py:157` `def read(self, sessions_dir)`
- `CommandOutputReader.read` (method) `modules/session_reader.py:199` `def read(self, sessions_dir)`
- `DiscoveredHostReader.read` (method) `modules/session_reader.py:217` `def read(self, sessions_dir)`
- `TaskReader.read` (method) `modules/session_reader.py:235` `def read(self, sessions_dir)`
- `TaskWriter.__init__` (method) `modules/session_reader.py:260` `def __init__(self, sessions_dir)`
- `TaskWriter.append` (method) `modules/session_reader.py:263` `def append(self, title, description, operator, status)`
- `TaskWriter.update_status` (method) `modules/session_reader.py:288` `def update_status(self, task_id, status)`
- `SessionAggregator.__init__` (method) `modules/session_reader.py:319` `def __init__(self, implant_reader, output_reader, host_reader, task_reader)`
- `SessionAggregator.aggregate` (method) `modules/session_reader.py:331` `def aggregate(self, sessions_dir)`
- `get_aggregator` (function) `modules/session_reader.py:347` `def get_aggregator()`

## modules/session_state.py
Imported by: `modules/recommender.py`, `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`
- `build_state` (function) `modules/session_state.py:189` `def build_state()` -- Assemble and return the current session state dict.
- `refresh` (function) `modules/session_state.py:240` `def refresh()` -- Build state and persist to sessions/session_state.json.
- `load` (function) `modules/session_state.py:251` `def load()` -- Return the last written state, or build it fresh if stale/missing.

## modules/sidequestion.py
Imported by: `cli/commands/ai.py`, `tests/test_autonomous_ops.py`
- `SideQuestionService.__init__` (method) `modules/sidequestion.py:55` `def __init__(self, answer_fn, config)` -- Initialize registries with an optional answer function.
- `SideQuestionService.capture` (method) `modules/sidequestion.py:66` `def capture(self, task_id, text)` -- Freeze main-loop context into an immutable snapshot.
- `SideQuestionService.ask` (method) `modules/sidequestion.py:75` `def ask(self, snapshot_id, question)` -- Answer from a snapshot without touching main state.
- `SideQuestionService.cancel` (method) `modules/sidequestion.py:104` `def cancel(self, request_id)` -- Mark a pending request cancelled.
- `SideQuestionService.history` (method) `modules/sidequestion.py:113` `def history(self, limit, before)` -- Page request history newest first.

## modules/sinks/attack_graph.py
Depends on: `modules/attack_surface3d.py`, `modules/outcome_bus.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/attack_graph.py:13` `def apply(event)` -- Rebuild the attack graph and its exposure summary.

## modules/sinks/beacon_dispatch.py
Depends on: `core/config.py`, `core/hardening.py`, `modules/outcome_bus.py`, `modules/payload_factory.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/beacon_dispatch.py:46` `def apply(event)` -- Stage the catch-back command for one foothold outcome.

## modules/sinks/c2_surfaces.py
Depends on: `modules/c2_surfaces.py`, `modules/outcome_bus.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/c2_surfaces.py:11` `def apply(event)` -- Write the operator-visible surfaces for one outcome.

## modules/sinks/campaign_db.py
Depends on: `modules/db.py`, `modules/outcome_bus.py`
- `apply` (function) `modules/sinks/campaign_db.py:9` `def apply(event)` -- Mirror one outcome into the campaign database.

## modules/sinks/event_bus.py
Depends on: `modules/event_bus.py`, `modules/outcome_bus.py`
- `apply` (function) `modules/sinks/event_bus.py:9` `def apply(event)` -- Publish one event to the unified bus.

## modules/sinks/intel_graph.py
Depends on: `modules/intel_fusion.py`, `modules/outcome_bus.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/intel_graph.py:13` `def apply(event)` -- Rebuild the intel graph and its summary.

## modules/sinks/killchain.py
Depends on: `modules/killchain.py`, `modules/outcome_bus.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/killchain.py:11` `def apply(event)` -- Advance the kill-chain phase only when the outcome proves progress.

## modules/sinks/objectives.py
Depends on: `modules/outcome_bus.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/objectives.py:16` `def apply(event)` -- Append one actionable objective when the outcome warrants it.

## modules/sinks/routing.py
Depends on: `modules/lazy_intel.py`, `modules/outcome_bus.py`
Imported by: `skills/lazyown_mcp.py`
- `apply` (function) `modules/sinks/routing.py:9` `def apply(event)` -- Record one routing outcome for cross-task priors.

## modules/sinks/world_diff.py
Depends on: `modules/lazy_world_diff.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/world_diff.py:14` `def apply(event)` -- Diff one host's world snapshot and record the changes.

## modules/sinks/world_model.py
Depends on: `modules/obs_parser.py`, `modules/outcome_bus.py`, `modules/world_model.py`
- `apply` (function) `modules/sinks/world_model.py:12` `def apply(event)` -- Write one outcome into the world model.

## modules/sleep_obfuscation.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/sleep_obfuscation.py`, `modules/beacon_config_builder.py`, `tests/test_sleep_obfuscation.py`
- `SleepObfuscationConfig.to_dict` (method) `modules/sleep_obfuscation.py:129` `def to_dict(self)` -- Serialize to dictionary.
- `SleepObfuscationConfig.from_dict` (method) `modules/sleep_obfuscation.py:146` `def from_dict(cls, raw)` -- Build from dictionary.
- `SleepTechniqueCatalog.__init__` (method) `modules/sleep_obfuscation.py:170` `def __init__(self)`
- `SleepTechniqueCatalog.register` (method) `modules/sleep_obfuscation.py:173` `def register(self, technique)` -- Register a technique in the catalog.
- `SleepTechniqueCatalog.get` (method) `modules/sleep_obfuscation.py:177` `def get(self, name)` -- Retrieve a technique by name.
- `SleepTechniqueCatalog.list_all` (method) `modules/sleep_obfuscation.py:184` `def list_all(self)` -- Return all registered techniques sorted by detection resistance.
- `SleepTechniqueCatalog.list_by_platform` (method) `modules/sleep_obfuscation.py:192` `def list_by_platform(self, platform)` -- Return techniques supported on a given platform.
- `SleepTechniqueCatalog.list_names` (method) `modules/sleep_obfuscation.py:196` `def list_names(self)` -- Return sorted list of technique names.
- `SleepTechniqueValidator.validate` (method) `modules/sleep_obfuscation.py:369` `def validate(config, technique)` -- Validate config against a technique definition.
- `SleepTechniqueValidator.validate_config` (method) `modules/sleep_obfuscation.py:386` `def validate_config(config)` -- Validate the config itself for internal consistency.
- `SleepObfuscationEngine.__init__` (method) `modules/sleep_obfuscation.py:407` `def __init__(self, catalog)`
- `SleepObfuscationEngine.catalog` (method) `modules/sleep_obfuscation.py:416` `def catalog(self)` -- Return the technique catalog.
- `SleepObfuscationEngine.config` (method) `modules/sleep_obfuscation.py:421` `def config(self)` -- Return the active runtime configuration.
- `SleepObfuscationEngine.detection_resistance` (method) `modules/sleep_obfuscation.py:426` `def detection_resistance(self)` -- Return the detection resistance score of the active technique.
- `SleepObfuscationEngine.select` (method) `modules/sleep_obfuscation.py:442` `def select(self, technique_name)` -- Select a technique from the catalog.
- `SleepObfuscationEngine.configure` (method) `modules/sleep_obfuscation.py:449` `def configure(self, technique, overrides)` -- Build a validated SleepObfuscationConfig for a technique.
- `SleepObfuscationEngine.validate` (method) `modules/sleep_obfuscation.py:484` `def validate(self, config)` -- Validate configuration against the active technique.
- `SleepObfuscationEngine.recommend` (method) `modules/sleep_obfuscation.py:500` `def recommend(self, platform)` -- Recommend techniques for a platform sorted by detection resistance.
- `SleepObfuscationEngine.to_dict` (method) `modules/sleep_obfuscation.py:513` `def to_dict(self)` -- Serialize the entire engine state to a dictionary.
- `SleepObfuscationEngine.from_dict` (method) `modules/sleep_obfuscation.py:522` `def from_dict(cls, raw)` -- Build an engine from a serialized state dictionary.

## modules/socks_proxy.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/socks_proxy.py`, `modules/beacon_config_builder.py`, `tests/test_socks_proxy.py`
- `SocksReply.message` (method) `modules/socks_proxy.py:103` `def message(self)` -- Return a human-readable message for this reply code.
- `SocksSession.elapsed_seconds` (method) `modules/socks_proxy.py:144` `def elapsed_seconds(self)` -- Return seconds since session creation.
- `SocksSession.to_dict` (method) `modules/socks_proxy.py:150` `def to_dict(self)` -- Serialize session to dictionary.
- `SocksProxyConfig.to_dict` (method) `modules/socks_proxy.py:199` `def to_dict(self)` -- Serialize config to dictionary.
- `SocksProxyConfig.from_dict` (method) `modules/socks_proxy.py:218` `def from_dict(cls, raw)` -- Build config from dictionary.
- `SocksValidator.validate_config` (method) `modules/socks_proxy.py:253` `def validate_config(config)` -- Validate a SocksProxyConfig and return error messages.
- `SocksValidator.validate_request` (method) `modules/socks_proxy.py:300` `def validate_request(command, address_type, host, port, config)` -- Validate a SOCKS5 request against the proxy configuration.
- `SocksProxyEngine.__init__` (method) `modules/socks_proxy.py:381` `def __init__(self, config)`
- `SocksProxyEngine.config` (method) `modules/socks_proxy.py:387` `def config(self)` -- Return the current proxy configuration.
- `SocksProxyEngine.sessions` (method) `modules/socks_proxy.py:392` `def sessions(self)` -- Return active proxied sessions.
- `SocksProxyEngine.session_count` (method) `modules/socks_proxy.py:397` `def session_count(self)` -- Return the number of active sessions.
- `SocksProxyEngine.validate` (method) `modules/socks_proxy.py:401` `def validate(self, config)` -- Validate the configuration.
- `SocksProxyEngine.build_spec` (method) `modules/socks_proxy.py:413` `def build_spec(self)` -- Build a JSON-serializable proxy specification for beacon delivery.
- `SocksProxyEngine.create_session` (method) `modules/socks_proxy.py:436` `def create_session(self, session_id, target_host, target_port, beacon_client_id)` -- Create and track a new proxied session.
- `SocksProxyEngine.remove_session` (method) `modules/socks_proxy.py:475` `def remove_session(self, session_id)` -- Remove a session by ID.
- `SocksProxyEngine.get_session` (method) `modules/socks_proxy.py:482` `def get_session(self, session_id)` -- Return a session by ID, or None.
- `SocksProxyEngine.add_bytes` (method) `modules/socks_proxy.py:486` `def add_bytes(self, session_id, sent, received)` -- Update byte counters for a session.
- `SocksProxyEngine.cleanup_expired` (method) `modules/socks_proxy.py:497` `def cleanup_expired(self)` -- Remove sessions that have exceeded the timeout.
- `SocksProxyEngine.list_sessions` (method) `modules/socks_proxy.py:511` `def list_sessions(self)` -- Return a list of all active sessions as dictionaries.
- `SocksProxyEngine.from_dict` (method) `modules/socks_proxy.py:522` `def from_dict(cls, raw)` -- Build a SocksProxyEngine from a configuration dictionary.
- `SocksProxyEngine.from_payload` (method) `modules/socks_proxy.py:528` `def from_payload(cls, payload)` -- Build a SocksProxyEngine from a LazyOwn payload configuration.

## modules/staged_delivery.py
Imported by: `cli/commands/payload_arsenal.py`
- `StagedDeliveryFactory.__init__` (method) `modules/staged_delivery.py:83` `def __init__(self, config, output_dir)`
- `StagedDeliveryFactory.generate_hta` (method) `modules/staged_delivery.py:134` `def generate_hta(self)` -- Generate an HTA (HTML Application) dropper.
- `StagedDeliveryFactory.generate_vba_macro` (method) `modules/staged_delivery.py:171` `def generate_vba_macro(self)` -- Generate a VBA macro for Office documents (Word/Excel).
- `StagedDeliveryFactory.generate_xlm_macro` (method) `modules/staged_delivery.py:219` `def generate_xlm_macro(self)` -- Generate an Excel 4.0 (XLM) macro for legacy macro execution.
- `StagedDeliveryFactory.generate_lnk` (method) `modules/staged_delivery.py:237` `def generate_lnk(self)` -- Generate a Windows .lnk shortcut file with embedded command execution.
- `StagedDeliveryFactory.generate_iso` (method) `modules/staged_delivery.py:301` `def generate_iso(self, inner_files)` -- Generate an ISO 9660 image with an embedded payload autorun.
- `StagedDeliveryFactory.generate_vhd` (method) `modules/staged_delivery.py:370` `def generate_vhd(self, inner_files)` -- Generate a VHD (Virtual Hard Disk) image with embedded payloads.
- `StagedDeliveryFactory.generate_all` (method) `modules/staged_delivery.py:420` `def generate_all(self)` -- Generate all delivery formats for the current configuration.
- `StagedDeliveryFactory.generate_phishing_page` (method) `modules/staged_delivery.py:460` `def generate_phishing_page(self, template)` -- Generate a credential harvesting HTML page.

## modules/state_manager.py
Depends on: `core/logging.py`, `modules/db.py`, `modules/event_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/automation.py`, `lazyc2.py`, `lazyc2/blueprints/beacon.py`, `lazyown.py`, `modules/conditional_hooks.py`, `modules/event_consumers.py`, `modules/unified_bridge.py`, `tests/test_single_source_of_truth.py`
- `StateManager.__init__` (method) `modules/state_manager.py:107` `def __init__(self, db_path, sessions_dir, world_model_path, facts_path)`
- `StateManager.instance` (method) `modules/state_manager.py:129` `def instance(cls)`
- `StateManager.db` (method) `modules/state_manager.py:137` `def db(self)`
- `StateManager.workspace_id` (method) `modules/state_manager.py:146` `def workspace_id(self)`
- `StateManager.set_payload` (method) `modules/state_manager.py:165` `def set_payload(self, payload)`
- `StateManager.close` (method) `modules/state_manager.py:202` `def close(self)`
- `StateManager.add_host` (method) `modules/state_manager.py:213` `def add_host(self, address, mac, hostname, os, state)`
- `StateManager.get_host` (method) `modules/state_manager.py:236` `def get_host(self, address)`
- `StateManager.list_hosts` (method) `modules/state_manager.py:245` `def list_hosts(self)`
- `StateManager.advance_host` (method) `modules/state_manager.py:249` `def advance_host(self, address, new_state)`
- `StateManager.delete_host` (method) `modules/state_manager.py:275` `def delete_host(self, address)`
- `StateManager.add_service` (method) `modules/state_manager.py:287` `def add_service(self, host_address, port, protocol, name, product, version, state)`
- `StateManager.list_services` (method) `modules/state_manager.py:319` `def list_services(self, host_address)`
- `StateManager.add_credential` (method) `modules/state_manager.py:328` `def add_credential(self, host_address, username, password, realm, cred_type, origin)`
- `StateManager.list_credentials` (method) `modules/state_manager.py:362` `def list_credentials(self, host_address)`
- `StateManager.add_vulnerability` (method) `modules/state_manager.py:373` `def add_vulnerability(self, host_address, name, severity, description, refs)`
- `StateManager.list_vulnerabilities` (method) `modules/state_manager.py:398` `def list_vulnerabilities(self, host_address, severity)`
- `StateManager.add_loot` (method) `modules/state_manager.py:411` `def add_loot(self, name, loot_type, path, notes, host_address)`
- `StateManager.list_loot` (method) `modules/state_manager.py:444` `def list_loot(self)`
- `StateManager.add_note` (method) `modules/state_manager.py:450` `def add_note(self, data, note_type, host_address)`
- `StateManager.list_notes` (method) `modules/state_manager.py:473` `def list_notes(self)`
- `StateManager.import_nmap_xml` (method) `modules/state_manager.py:479` `def import_nmap_xml(self, xml_path)`
- `StateManager.import_nmap_from_facts` (method) `modules/state_manager.py:495` `def import_nmap_from_facts(self, facts)` -- Import hosts and services from a FactStore-style facts dict into DB.
- `StateManager.status` (method) `modules/state_manager.py:550` `def status(self)`
- `StateManager.get_world_model_cache` (method) `modules/state_manager.py:666` `def get_world_model_cache(self)`
- `StateManager.load_world_model` (method) `modules/state_manager.py:672` `def load_world_model(self)` -- Return a WorldModel instance populated from DB state.
- `StateManager.session_snapshot` (method) `modules/state_manager.py:713` `def session_snapshot(self)`
- `StateManager.export_csv` (method) `modules/state_manager.py:817` `def export_csv(self, table)`
- `StateManager.export_summary` (method) `modules/state_manager.py:821` `def export_summary(self)`
- `get_state_manager` (function) `modules/state_manager.py:836` `def get_state_manager()`

## modules/stego_video.py
- `load_payload_file` (function) `modules/stego_video.py:26` `def load_payload_file()` -- Return the ``file`` value from payload.json, or None.
- `is_zip` (function) `modules/stego_video.py:36` `def is_zip(path)`
- `is_video` (function) `modules/stego_video.py:40` `def is_video(path)`
- `prompt_path` (function) `modules/stego_video.py:44` `def prompt_path(message)`
- `resolve_path` (function) `modules/stego_video.py:52` `def resolve_path(arg_path, payload_file, validator, kind)` -- Resolve the target path using argument -> payload.json -> interactive prompt.
- `generate_carrier` (function) `modules/stego_video.py:61` `def generate_carrier(output)` -- Generate a silent carrier video with ffmpeg.
- `encode` (function) `modules/stego_video.py:75` `def encode(zip_path, output_video)` -- Hide zip_path inside output_video.
- `decode` (function) `modules/stego_video.py:93` `def decode(stego_video, output_zip)` -- Extract the hidden zip from stego_video into output_zip.
- `default_output` (function) `modules/stego_video.py:113` `def default_output(zip_path)`
- `main` (function) `modules/stego_video.py:118` `def main(argv)`

## modules/sudo_tiocsti.py
Depends on: `core/logging.py`
- `get_controlling_tty` (function) `modules/sudo_tiocsti.py:52` `def get_controlling_tty()` -- Return (file_descriptor, tty_path) for the controlling terminal.
- `inject_byte` (function) `modules/sudo_tiocsti.py:64` `def inject_byte(fd, byte_char)` -- Inject a single byte via TIOCSTI; return success status.
- `inject_payload` (function) `modules/sudo_tiocsti.py:79` `def inject_payload(fd, payload, char_delay)` -- Inject a multi‑character payload.
- `get_sudo_pids_on_tty` (function) `modules/sudo_tiocsti.py:102` `def get_sudo_pids_on_tty(tty_path)` -- Return a list of PIDs that are running 'sudo' and have the same controlling terminal as the given tty_path.
- `sudo_cache_valid` (function) `modules/sudo_tiocsti.py:139` `def sudo_cache_valid()` -- Return True if sudo credentials are cached (i.e., sudo -n succeeds).
- `mode_poll` (function) `modules/sudo_tiocsti.py:149` `def mode_poll(fd, tty_path)` -- Poll for sudo processes; inject payload when sudo exits.
- `mode_prefill` (function) `modules/sudo_tiocsti.py:175` `def mode_prefill(fd)` -- Inject payload repeatedly, regardless of sudo state.
- `mode_cache` (function) `modules/sudo_tiocsti.py:185` `def mode_cache(fd)` -- Check sudo cache; if valid, inject sudo -i once.
- `main` (function) `modules/sudo_tiocsti.py:198` `def main()`

## modules/surface_ops.py
Depends on: `modules/world_model.py`
Imported by: `cli/commands/surface.py`, `tests/test_estorides_fusion.py`
- `is_ipv4` (function) `modules/surface_ops.py:18` `def is_ipv4(value)` -- Return True for dotted-quad IPv4 literals with 0-255 octets.
- `parse_confirm` (function) `modules/surface_ops.py:26` `def parse_confirm(answer)` -- Return True for an affirmative scan confirmation answer.
- `discovery_targets` (function) `modules/surface_ops.py:31` `def discovery_targets(sessions_dir)` -- List every discovery IP across the sessions discovery files.
- `write_world_model_hosts` (function) `modules/surface_ops.py:50` `def write_world_model_hosts(document, sessions)` -- Append unknown estorides host IPs to world_model.json hosts.

## modules/threat_model.py
Depends on: `core/logging.py`
Imported by: `cli/commands/mcp_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `ThreatModelBuilder.build` (method) `modules/threat_model.py:270` `def build(self)`
- `ThreatModelBuilder.load` (method) `modules/threat_model.py:293` `def load(self)`
- `get_builder` (function) `modules/threat_model.py:592` `def get_builder()`

## modules/timeline_narrator.py
Depends on: `modules/ai_fallback.py`
Imported by: `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`
- `narrate` (function) `modules/timeline_narrator.py:130` `def narrate(api_key, force)` -- Generate and return the timeline narrative.
- `load_timeline` (function) `modules/timeline_narrator.py:165` `def load_timeline()` -- Return the last written timeline.md or empty string.

## modules/timestomper.py
Imported by: `cli/commands/opsec_cleanup.py`
- `Timestomper.__init__` (method) `modules/timestomper.py:106` `def __init__(self, config)`
- `Timestomper.windows_timestomp_powershell` (method) `modules/timestomper.py:110` `def windows_timestomp_powershell(self)` -- Generate PowerShell commands for Windows file timestomping.
- `Timestomper.windows_timestomp_c` (method) `modules/timestomper.py:152` `def windows_timestomp_c(self)` -- Generate C code for Windows timestomping via SetFileTime API.
- `Timestomper.linux_timestomp_commands` (method) `modules/timestomper.py:200` `def linux_timestomp_commands(self)` -- Generate Linux commands for file timestomping.
- `Timestomper.macos_timestomp_commands` (method) `modules/timestomper.py:241` `def macos_timestomp_commands(self)` -- Generate macOS commands for file timestomping.
- `Timestomper.generate_random_timestamps` (method) `modules/timestomper.py:280` `def generate_random_timestamps(self, reference_ts, window_days)` -- Generate randomized timestamps within a window around the reference.
- `Timestomper.verify_timestamps` (method) `modules/timestomper.py:300` `def verify_timestamps(self, target_paths)` -- Verify timestamps on target files after modification.
- `Timestomper.summary` (method) `modules/timestomper.py:326` `def summary(self)` -- Return a summary of available timestomping capabilities.

## modules/tools/loop_smoke.py
Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`
- `FakeShell.onecmd_plus_hooks` (method) `modules/tools/loop_smoke.py:25` `def onecmd_plus_hooks(self, command)` -- Emit recognizable output for every routed verb.
- `FakeEngine.__init__` (method) `modules/tools/loop_smoke.py:36` `def __init__(self)` -- Bind a sandboxed task store and runtime tracker.
- `FakeEngine.bind_shell` (method) `modules/tools/loop_smoke.py:44` `def bind_shell(self, shell)` -- Record the bound shell (runner contract).
- `FakeEngine.set_concurrency` (method) `modules/tools/loop_smoke.py:48` `def set_concurrency(self, value)` -- Accept the concurrency knob without scheduling anything.
- `FakeEngine.create_task` (method) `modules/tools/loop_smoke.py:52` `def create_task(self, goal, description)` -- Create the task record and return its id.
- `FakeEngine.orchestrate` (method) `modules/tools/loop_smoke.py:56` `def orchestrate(self)` -- Run the injected executor once and report a done summary.
- `run` (function) `modules/tools/loop_smoke.py:77` `def run()` -- Run the smoke and return ``{"ok": bool, "checks": {...}, "result": {...}}``.
- `main` (function) `modules/tools/loop_smoke.py:114` `def main()` -- CLI entry point: print the checks and exit 0/1.

## modules/tools/monitor_smoke.py
Depends on: `cli/lazy_monitor.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`
- `run` (function) `modules/tools/monitor_smoke.py:20` `def run()` -- Run the monitor smoke and return ``{"ok": bool, "checks": {...}}``.
- `main` (function) `modules/tools/monitor_smoke.py:59` `def main()` -- CLI entry point: print the checks and exit 0/1.

## modules/toolset.py
Imported by: `skills/autonomous_daemon.py`
- `builtin_seeds` (function) `modules/toolset.py:35` `def builtin_seeds()` -- Return the default graph-tool catalog (handlers stay in code).
- `resolve` (function) `modules/toolset.py:72` `def resolve(agent, tool_key)` -- Return the seed when bound to agent, else None (LAZY ToolResolve).
- `extract_tool` (function) `modules/toolset.py:105` `def extract_tool(command)` -- Split tool name with shlex; flag shell metacharacters.
- `validate_shell` (function) `modules/toolset.py:128` `def validate_shell(role, command)` -- Check a shell command against the role allowlist.


Next: [API_p18.md](API_p18.md)
