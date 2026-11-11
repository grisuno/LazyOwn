# API (page 19 of 28)
Previous: [API_p18.md](API_p18.md)

## modules/redteam_gym.py
Depends on: `cli/engagement_hooks.py`, `core/config.py`, `modules/__init__.py`, `modules/atomic_exploit_bridge.py`, `modules/cli_auth.py`, `modules/gym_registry.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `cli/commands/redteam_gym.py`, `cli/lazy_orchestrator.py`, `cli/orchestrator_assets_tabs.py`, `modules/exploitgym_gym.py`, `tests/test_gym_cli.py`, `tests/test_gym_registry.py`, `tests/test_infra_disposable.py`, `tests/test_lazy_orchestrator.py`
- `reload_challenge_definitions` (function) `modules/redteam_gym.py:300` `def reload_challenge_definitions(directory)` -- Reload YAML definitions, falling back to the embedded catalogue.
- `definition_rows` (function) `modules/redteam_gym.py:394` `def definition_rows()` -- Return one row per gym YAML file, including invalid files.
- `create_gym` (function) `modules/redteam_gym.py:399` `def create_gym(gym_id)` -- Create a gym definition YAML and reload the catalogue.
- `save_gym_yaml` (function) `modules/redteam_gym.py:436` `def save_gym_yaml(gym_id, text)` -- Validate and persist raw YAML for one gym definition.
- `delete_gym` (function) `modules/redteam_gym.py:446` `def delete_gym(gym_id)` -- Delete one gym definition unless it has active runs.
- `list_challenges` (function) `modules/redteam_gym.py:454` `def list_challenges()` -- Return all defined gym challenges with metadata.
- `start_challenge` (function) `modules/redteam_gym.py:495` `def start_challenge(challenge_id, target, spin_lab, notify)` -- Begin a gym challenge and persist the run in the world model.
- `submit_challenge` (function) `modules/redteam_gym.py:648` `def submit_challenge(techniques_used, success, run_id)` -- Submit a completed challenge for scoring.
- `stop_challenges` (function) `modules/redteam_gym.py:756` `def stop_challenges(selector)` -- Stop one gym by id/name/run id, or every gym when selector is empty.
- `engagement_context` (function) `modules/redteam_gym.py:838` `def engagement_context(target)` -- Return in-scope phase, compromised hosts and live shells.
- `get_active_challenges` (function) `modules/redteam_gym.py:898` `def get_active_challenges()` -- Return every active gym run across operators.
- `show_leaderboard` (function) `modules/redteam_gym.py:1057` `def show_leaderboard(top_n)` -- Return the top N players from the leaderboard.
- `get_active_challenge` (function) `modules/redteam_gym.py:1084` `def get_active_challenge(run_id)` -- Return one active challenge, preferring the current operator.
- `record_external_attempt` (function) `modules/redteam_gym.py:1115` `def record_external_attempt(challenge_id, success, elo_bonus, techniques)` -- Record a scored attempt for a challenge not defined in the catalog.
- `main` (function) `modules/redteam_gym.py:1169` `def main()` -- CLI entry point — show gym leaderboard from command line.

## modules/reflective_dll.py
- `PEParser.__init__` (method) `modules/reflective_dll.py:151` `def __init__(self, pe_data)`
- `PEParser.parse_file_header` (method) `modules/reflective_dll.py:166` `def parse_file_header(self)` -- Extract the COFF file header.
- `PEParser.parse_sections` (method) `modules/reflective_dll.py:208` `def parse_sections(self, num_sections)` -- Parse all section headers from the PE.
- `PEParser.parse_data_directories` (method) `modules/reflective_dll.py:243` `def parse_data_directories(self, num_entries)` -- Parse the PE data directory entries.
- `PEParser.rva_to_offset` (method) `modules/reflective_dll.py:265` `def rva_to_offset(self, rva, sections)` -- Convert a relative virtual address to a file offset.
- `PEParser.parse_imports` (method) `modules/reflective_dll.py:280` `def parse_imports(self, import_dir, sections)` -- Parse the import directory to enumerate imported DLLs and functions.
- `PEParser.parse_relocations` (method) `modules/reflective_dll.py:326` `def parse_relocations(self, reloc_dir, sections)` -- Parse base relocation entries.
- `PEParser.parse_exports` (method) `modules/reflective_dll.py:374` `def parse_exports(self, export_dir, sections)` -- Parse the export directory.
- `PEParser.is_64bit` (method) `modules/reflective_dll.py:456` `def is_64bit(self)`
- `PEParser.raw_data` (method) `modules/reflective_dll.py:460` `def raw_data(self)`
- `ReflectiveLoader.__init__` (method) `modules/reflective_dll.py:492` `def __init__(self, pe_data, config)`
- `ReflectiveLoader.sha256` (method) `modules/reflective_dll.py:505` `def sha256(self)` -- SHA-256 hash of the raw PE bytes.
- `ReflectiveLoader.architecture` (method) `modules/reflective_dll.py:510` `def architecture(self)` -- CPU architecture string ('x64' or 'x86').
- `ReflectiveLoader.required_imports` (method) `modules/reflective_dll.py:515` `def required_imports(self)` -- DLL names needed for import resolution.
- `ReflectiveLoader.plan_injection` (method) `modules/reflective_dll.py:526` `def plan_injection(self)` -- Generate an injection plan based on the configured technique.
- `ReflectiveLoader.generate_c_stub` (method) `modules/reflective_dll.py:588` `def generate_c_stub(self)` -- Generate a C stub that implements reflective loading.
- `ReflectiveLoader.generate_powershell_stub` (method) `modules/reflective_dll.py:666` `def generate_powershell_stub(self)` -- Generate PowerShell reflective loader script.
- `ReflectiveLoader.summarize` (method) `modules/reflective_dll.py:685` `def summarize(self)` -- Human-readable summary of the parsed PE for operator review.

## modules/resource_script.py
Depends on: `core/safe_exec.py`
Imported by: `cli/commands/resource_scripting.py`, `tests/test_resource_script.py`, `tests/test_security_hardening_v3.py`
- `ScriptContext.__init__` (method) `modules/resource_script.py:89` `def __init__(self, shell_params, on_command, on_print)`
- `ScriptContext.print` (method) `modules/resource_script.py:138` `def print(self, msg)`
- `ScriptContext.run_command` (method) `modules/resource_script.py:147` `def run_command(self, cmd)`
- `ScriptContext.eval_condition` (method) `modules/resource_script.py:191` `def eval_condition(self, raw_condition)` -- Evaluate an ``if``/``while`` condition expression.
- `ResourceScriptEngine.__init__` (method) `modules/resource_script.py:276` `def __init__(self, context)`
- `ResourceScriptEngine.execute` (method) `modules/resource_script.py:279` `def execute(self, script_path)` -- Load and run a script file.
- `ResourceScriptEngine.execute_lines` (method) `modules/resource_script.py:293` `def execute_lines(self, lines, source)` -- Execute a list of script lines.
- `ResourceScriptEngine.execute_string` (method) `modules/resource_script.py:327` `def execute_string(self, script)` -- Execute a script string (split on newlines).

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
Depends on: `modules/selection/module.py`
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
Depends on: `core/crypto.py`, `lazyown-docker/init.sh`, `modules/selection/module.py`
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

## modules/selection/adversary.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_selectors_capabilities.py`
- `load_profiles` (function) `modules/selection/adversary.py:26` `def load_profiles(adversaries_dir)` -- Load every adversary profile dictionary shipped in the repo.
- `resolve_profile` (function) `modules/selection/adversary.py:80` `def resolve_profile(goal, adversaries_dir)` -- Resolve the adversary profile the goal names, if any.
- `AdversarySelector.__init__` (method) `modules/selection/adversary.py:123` `def __init__(self, adversaries_dir, confirm)` -- Bind the profile directory and the execution confirmation word.
- `AdversarySelector.propose` (method) `modules/selection/adversary.py:136` `def propose(self, ctx)` -- Return the emulation action when the goal names a profile.

## modules/selection/atomic.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `modules/selection/technique.py`, `modules/selection/technique_chain.py`, `tests/test_selectors_capabilities.py`
- `AtomicSelector.propose` (method) `modules/selection/atomic.py:25` `def propose(self, ctx)` -- Return an atomic-emulation action when technique ids are named.

## modules/selection/base.py
Imported by: `modules/lazy_loop.py`, `modules/selection/__init__.py`, `modules/selection/adversary.py`, `modules/selection/atomic.py`, `modules/selection/chain.py`, `modules/selection/cred_spray.py`, `modules/selection/edb.py`, `modules/selection/intel.py`, `modules/selection/lazyscript.py`, `modules/selection/module.py`, `modules/selection/playbook.py`, `modules/selection/poc.py`, `modules/selection/registry.py`, `modules/selection/technique.py`, `modules/selection/technique_chain.py`, `skills/autonomous_daemon.py`, `tests/test_intel_selector.py`, `tests/test_loop_fire_pending.py`, `tests/test_poc_registry.py`, `tests/test_selection_lazyscript.py`, `tests/test_selection_module.py`, `tests/test_selection_technique.py`, `tests/test_selection_technique_chain.py`, `tests/test_selection_wiring.py`, `tests/test_selectors_base.py`, `tests/test_selectors_capabilities.py`
- `Selector.propose` (method) `modules/selection/base.py:73` `def propose(self, ctx)` -- Return the next action for this strategy, or None to abstain.

## modules/selection/chain.py
Depends on: `modules/chain_match.py`, `modules/selection/base.py`
Imported by: `modules/exp.c`, `modules/selection/__init__.py`, `modules/selection/registry.py`, `skills/autonomous_daemon.py`, `tests/test_selectors_base.py`
- `ChainSelector.__init__` (method) `modules/selection/chain.py:18` `def __init__(self, allow_lab)` -- Bind the lab-inclusion policy for the matcher.
- `ChainSelector.propose` (method) `modules/selection/chain.py:27` `def propose(self, ctx)` -- Return a chain action for the context, or None when nothing fits.

## modules/selection/cred_spray.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `skills/autonomous_daemon.py`, `tests/test_selectors_capabilities.py`
- `CredentialSpraySelector.propose` (method) `modules/selection/cred_spray.py:37` `def propose(self, ctx)` -- Return a spray verb for the first matching open service, or None.

## modules/selection/edb.py
Depends on: `modules/__init__.py`, `modules/selection/base.py`
Imported by: `modules/selection/registry.py`
- `EDBSelector.propose` (method) `modules/selection/edb.py:11` `def propose(self, ctx)`

## modules/selection/intel.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/registry.py`, `tests/test_intel_selector.py`, `tests/test_loop_fire_pending.py`
- `intel_report_path` (function) `modules/selection/intel.py:32` `def intel_report_path(target)` -- Return the saved exposure report path for one target.
- `load_report` (function) `modules/selection/intel.py:44` `def load_report(target)` -- Read the saved exposure report of one target.
- `pending_fires` (function) `modules/selection/intel.py:60` `def pending_fires(target)` -- Fire-tier bounded matches of a target not covered by a chain yet.
- `IntelSelector.propose` (method) `modules/selection/intel.py:117` `def propose(self, ctx)` -- Return the next intelligence action, or None when none applies.

## modules/selection/lazyscript.py
Depends on: `modules/selection/base.py`
Imported by: `modules/selection/registry.py`, `tests/test_selection_lazyscript.py`
- `LazyscriptSelector.__init__` (method) `modules/selection/lazyscript.py:41` `def __init__(self, scripts_dir)` -- Bind the lazyscripts directory (overridable for tests).
- `LazyscriptSelector.propose` (method) `modules/selection/lazyscript.py:56` `def propose(self, ctx)` -- Return a lazyscript action for the context, or None when none fit.

## modules/selection/module.py
Depends on: `modules/module_registry.py`, `modules/selection/base.py`
Imported by: `modules/reverse-shell.c`, `modules/rootkit/rootkit.c`, `modules/selection/registry.py`, `static/js/select2-4.1.0.min.js`, `tests/test_selection_module.py`
- `ModuleSelector.propose` (method) `modules/selection/module.py:21` `def propose(self, ctx)` -- Return the first unproposed registry intent, or None.

## modules/selection/playbook.py
Depends on: `modules/apt_playbooks.py`, `modules/chain_registry.py`, `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_selectors_capabilities.py`
- `PlaybookSelector.__init__` (method) `modules/selection/playbook.py:79` `def __init__(self, playbook_dir)` -- Bind the playbook directory for summary loading.
- `PlaybookSelector.propose` (method) `modules/selection/playbook.py:128` `def propose(self, ctx)` -- Return an actor-emulation action when the goal names one, else None.

## modules/selection/poc.py
Depends on: `modules/__init__.py`, `modules/selection/base.py`
Imported by: `modules/selection/__init__.py`, `modules/selection/registry.py`, `tests/test_poc_registry.py`
- `PoCSelector.propose` (method) `modules/selection/poc.py:25` `def propose(self, ctx)` -- Return a PoC action for the context, or None when nothing fits.

## modules/selection/registry.py
Depends on: `modules/__init__.py`, `modules/selection/adversary.py`, `modules/selection/atomic.py`, `modules/selection/base.py`, `modules/selection/chain.py`, `modules/selection/cred_spray.py`, `modules/selection/edb.py`, `modules/selection/intel.py`, `modules/selection/lazyscript.py`, `modules/selection/module.py`, `modules/selection/playbook.py`, `modules/selection/poc.py`, `modules/selection/technique.py`, `modules/selection/technique_chain.py`
Imported by: `modules/lazy_loop.py`, `modules/selection/__init__.py`, `skills/autonomous_daemon.py`, `tests/test_selection_wiring.py`, `tests/test_selectors_base.py`, `tests/test_selectors_capabilities.py`
- `all_selectors` (function) `modules/selection/registry.py:31` `def all_selectors()` -- Return every shared selector in priority order, before admin filtering.
- `default_selectors` (function) `modules/selection/registry.py:61` `def default_selectors()` -- Return the cascade after applying the orchestrator's enable toggles.
- `propose_next` (function) `modules/selection/registry.py:76` `def propose_next(ctx, selectors)` -- Return the best concrete decision from the cascade, or None.

## modules/selection/technique.py
Depends on: `modules/playbook_engine.py`, `modules/selection/atomic.py`, `modules/selection/base.py`
Imported by: `modules/selection/registry.py`, `tests/test_selection_technique.py`
- `TechniqueSelector.propose` (method) `modules/selection/technique.py:23` `def propose(self, ctx)` -- Return a technique emulation action, or None when not applicable.

## modules/selection/technique_chain.py
Depends on: `modules/chain_registry.py`, `modules/chain_synth.py`, `modules/playbook_engine.py`, `modules/selection/atomic.py`, `modules/selection/base.py`
Imported by: `modules/selection/registry.py`, `tests/test_selection_technique_chain.py`
- `TechniqueChainSelector.propose` (method) `modules/selection/technique_chain.py:53` `def propose(self, ctx)` -- Return a technique-chain action, or None when fewer than two fit.

## modules/selector_manager.py
Imported by: `tests/test_auto_loop_memory.py`
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
Imported by: `cli/commands/mcp_bridge.py`, `modules/reactive_engine.py`, `skills/lazyown_groq_agents.py`, `skills/mcp_tools/rag_index.py`, `skills/mcp_tools/rag_query.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`
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
Imported by: `skills/lazyown_groq_agents.py`, `skills/mcp_tools/campaign_tasks.py`, `skills/mcp_tools/session_status.py`, `tests/test_core_modules.py`
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
Imported by: `modules/recommender.py`
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

## modules/sinks/chain_feed.py
Depends on: `modules/lazy_loop.py`, `modules/outcome_bus.py`
Imported by: `tests/test_lazy_loop.py`, `tests/test_sink_chain_feed.py`
- `apply` (function) `modules/sinks/chain_feed.py:22` `def apply(event)` -- Append one chain-step trace record and steer unhandled failures.

## modules/sinks/event_bus.py
Depends on: `modules/event_bus.py`, `modules/outcome_bus.py`
- `apply` (function) `modules/sinks/event_bus.py:9` `def apply(event)` -- Publish one event to the unified bus.

## modules/sinks/findings.py
Depends on: `core/logging.py`, `modules/__init__.py`, `modules/orchestrator_config.py`, `modules/outcome_bus.py`
Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`
- `limits_for` (function) `modules/sinks/findings.py:22` `def limits_for()` -- Return the ledger limits resolved from operator configuration.
- `apply` (function) `modules/sinks/findings.py:42` `def apply(event)` -- Append one ledger row for a finding-class outcome.
- `ledger_for` (function) `modules/sinks/findings.py:72` `def ledger_for(engagement_id)` -- Return one ledger bound to the sessions findings directory.
- `handoff` (function) `modules/sinks/findings.py:88` `def handoff(engagement_id, status, rounds)` -- Build the operator handoff from the durable ledger.
- `ingest_discarded` (function) `modules/sinks/findings.py:107` `def ingest_discarded(engagement_id, entries)` -- Record discarded vector rows for one engagement.

## modules/sinks/intel_graph.py
Depends on: `modules/intel_fusion.py`, `modules/outcome_bus.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/intel_graph.py:13` `def apply(event)` -- Rebuild the intel graph and its summary.

## modules/sinks/killchain.py
Depends on: `modules/killchain.py`, `modules/outcome_bus.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/killchain.py:11` `def apply(event)` -- Advance the kill-chain phase only when the outcome proves progress.

## modules/sinks/lazy_intel.py
Depends on: `modules/db.py`, `modules/lazy_heat.py`, `modules/outcome_bus.py`, `modules/world_model.py`
- `apply` (function) `modules/sinks/lazy_intel.py:28` `def apply(event)` -- Mirror one lazy_intel event into the world model and the database.

## modules/sinks/objectives.py
Depends on: `modules/outcome_bus.py`
Imported by: `tests/test_outcome_bus.py`
- `apply` (function) `modules/sinks/objectives.py:16` `def apply(event)` -- Append one actionable objective when the outcome warrants it.

## modules/sinks/routing.py
Depends on: `modules/lazy_intel.py`, `modules/lazy_ledger.py`, `modules/outcome_bus.py`
Imported by: `skills/lazyown_mcp.py`
- `apply` (function) `modules/sinks/routing.py:9` `def apply(event)` -- Record one routing outcome for cross-task priors.

## modules/sinks/world_diff.py
Depends on: `modules/lazy_world_diff.py`, `modules/outcome_bus.py`, `modules/world_model.py`
Imported by: `tests/test_outcome_bus.py`, `tests/test_world_diff_retest.py`
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


Next: [API_p20.md](API_p20.md)
