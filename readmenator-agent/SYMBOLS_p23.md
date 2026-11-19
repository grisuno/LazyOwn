# Symbols (page 23 of 54)
Previous: [SYMBOLS_p22.md](SYMBOLS_p22.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_jump_past` | method | `modules/resource_script.py:251` | `def _jump_past(self, open_res, close_re)` |
| `_lookup` | method | `modules/resource_script.py:168` | `def _lookup(self, name)` |
| `_repl` | function | `modules/resource_script.py:125` | `def _repl(m)` |
| `_resolve` | method | `modules/resource_script.py:124` | `def _resolve(self, text)` |
| `_resolve_operand` | method | `modules/resource_script.py:183` | `def _resolve_operand(self, operand)` |
| `_skip` | method | `modules/resource_script.py:165` | `def _skip(self)` |
| `eval_condition` | method | `modules/resource_script.py:191` | `def eval_condition(self, raw_condition)` |
| `execute` | method | `modules/resource_script.py:279` | `def execute(self, script_path)` |
| `execute_lines` | method | `modules/resource_script.py:293` | `def execute_lines(self, lines, source)` |
| `execute_string` | method | `modules/resource_script.py:327` | `def execute_string(self, script)` |
| `print` | method | `modules/resource_script.py:138` | `def print(self, msg)` |
| `run_command` | method | `modules/resource_script.py:147` | `def run_command(self, cmd)` |
| `_rewrite_segment` | function | `modules/retry_session.py:162` | `def _rewrite_segment(segment)` |
| `_verify_askpass_layout` | function | `modules/retry_session.py:67` | `def _verify_askpass_layout(helper, secret_file)` |
| `apply_sudo_askpass` | function | `modules/retry_session.py:137` | `def apply_sudo_askpass(command)` |
| `clear_sudo_secret` | function | `modules/retry_session.py:125` | `def clear_sudo_secret()` |
| `is_active` | function | `modules/retry_session.py:56` | `def is_active()` |
| `newest_failed_checkpoint` | function | `modules/retry_session.py:180` | `def newest_failed_checkpoint(chain, run_id)` |
| `resolve_sudo_consent` | function | `modules/retry_session.py:204` | `def resolve_sudo_consent(confirmer, want_sudo)` |
| `secret_enabled_path` | function | `modules/retry_session.py:61` | `def secret_enabled_path()` |
| `set_sudo_secret` | function | `modules/retry_session.py:94` | `def set_sudo_secret(secret)` |
| `sudo_gate_open` | function | `modules/retry_session.py:79` | `def sudo_gate_open()` |
| `reverse_shell_exit` | function | `modules/reverse-shell.c:16` | `static void __exit reverse_shell_exit(void)` |
| `reverse_shell_init` | function | `modules/reverse-shell.c:12` | `static int __init reverse_shell_init(void)` |
| `DllMain` | function | `modules/revshell.c:10` | `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)` |
| `xlAutoOpen` | function | `modules/revshell.c:5` | `void __cdecl xlAutoOpen()` |
| `RichDashboard` | class | `modules/rich_tui.py:66` | `class RichDashboard` |
| `__init__` | method | `modules/rich_tui.py:74` | `def __init__(self, dashboard_engine, refresh_interval, live)` |
| `_keyboard_listener` | method | `modules/rich_tui.py:146` | `def _keyboard_listener(self)` |
| `_render` | method | `modules/rich_tui.py:137` | `def _render(self)` |
| `_render_beacons` | method | `modules/rich_tui.py:372` | `def _render_beacons(self, snapshot)` |
| `_render_header` | method | `modules/rich_tui.py:193` | `def _render_header(self, snapshot)` |
| `_render_layout` | method | `modules/rich_tui.py:168` | `def _render_layout(self, snapshot)` |
| `_render_pivots` | method | `modules/rich_tui.py:337` | `def _render_pivots(self, snapshot)` |
| `_render_pivots_beacons` | method | `modules/rich_tui.py:321` | `def _render_pivots_beacons(self, snapshot)` |
| `_render_recommendations` | method | `modules/rich_tui.py:261` | `def _render_recommendations(self, snapshot)` |
| `_render_shortcuts` | method | `modules/rich_tui.py:413` | `def _render_shortcuts(self)` |
| `_render_topology` | method | `modules/rich_tui.py:221` | `def _render_topology(self, snapshot)` |
| `run` | method | `modules/rich_tui.py:96` | `def run(self)` |
| `stop` | method | `modules/rich_tui.py:132` | `def stop(self)` |
| `BucketedStateEncoder` | class | `modules/rl_trainer.py:114` | `class BucketedStateEncoder(IStateEncoder)` |
| `EpsilonTracker` | class | `modules/rl_trainer.py:215` | `class EpsilonTracker` |
| `IStateEncoder` | class | `modules/rl_trainer.py:101` | `class IStateEncoder(ABC)` |
| `QValueStore` | class | `modules/rl_trainer.py:150` | `class QValueStore` |
| `RLConfig` | class | `modules/rl_trainer.py:84` | `class RLConfig` |
| `RLTrainer` | class | `modules/rl_trainer.py:267` | `class RLTrainer` |
| `__init__` | method | `modules/rl_trainer.py:156` | `def __init__(self, path, optimistic_init)` |
| `__init__` | method | `modules/rl_trainer.py:218` | `def __init__(self, start, minimum, decay, path)` |
| `__init__` | method | `modules/rl_trainer.py:284` | `def __init__(self, config, state_encoder, q_store, epsilon_tracker)` |
| `_load` | method | `modules/rl_trainer.py:200` | `def _load(self)` |
| `_load` | method | `modules/rl_trainer.py:250` | `def _load(self)` |
| `_penalize` | method | `modules/rl_trainer.py:407` | `def _penalize(self, reward, detection_prob)` |
| `_persist` | method | `modules/rl_trainer.py:192` | `def _persist(self)` |
| `_save` | method | `modules/rl_trainer.py:241` | `def _save(self)` |
| `argmax` | method | `modules/rl_trainer.py:182` | `def argmax(self, state, candidates)` |
| `best_expert_for_state` | method | `modules/rl_trainer.py:389` | `def best_expert_for_state(self, state, candidates)` |
| `encode` | method | `modules/rl_trainer.py:105` | `def encode(self, task_type, engagement_phase, recent_reward_ema)` |
| `encode` | method | `modules/rl_trainer.py:131` | `def encode(self, task_type, engagement_phase, recent_reward_ema)` |
| `encode_state` | method | `modules/rl_trainer.py:304` | `def encode_state(self, task_type, engagement_phase, recent_reward_ema)` |
| `epsilon` | method | `modules/rl_trainer.py:233` | `def epsilon(self)` |
| `epsilon` | method | `modules/rl_trainer.py:402` | `def epsilon(self)` |
| `get` | method | `modules/rl_trainer.py:168` | `def get(self, state, action)` |
| `get_trainer` | function | `modules/rl_trainer.py:425` | `def get_trainer(config)` |
| `max_q` | method | `modules/rl_trainer.py:176` | `def max_q(self, state, candidates)` |
| `q_values_for_state` | method | `modules/rl_trainer.py:393` | `def q_values_for_state(self, state, candidates)` |
| `save` | method | `modules/rl_trainer.py:188` | `def save(self)` |
| `save` | method | `modules/rl_trainer.py:397` | `def save(self)` |
| `select_action` | method | `modules/rl_trainer.py:313` | `def select_action(self, state, candidates, force_exploit)` |
| `set` | method | `modules/rl_trainer.py:172` | `def set(self, state, action, value)` |
| `step` | method | `modules/rl_trainer.py:236` | `def step(self)` |
| `update` | method | `modules/rl_trainer.py:347` | `def update(self, state, action, reward, next_state, candidates, detection_prob)` |
| `BUFFER_SIZE` | macro | `modules/rootkit/mr.c:32` | `#define BUFFER_SIZE` |
| `Command` | struct | `modules/rootkit/mr.c:43` | `` |
| `DESIRED_LD_PRELOAD` | macro | `modules/rootkit/mr.c:34` | `#define DESIRED_LD_PRELOAD` |
| `HIDE_FILE` | macro | `modules/rootkit/mr.c:36` | `#define HIDE_FILE` |
| `KEY_FILE` | macro | `modules/rootkit/mr.c:37` | `#define KEY_FILE` |
| `MAX_COMMANDS` | macro | `modules/rootkit/mr.c:33` | `#define MAX_COMMANDS` |
| `PASSWORD` | macro | `modules/rootkit/mr.c:39` | `#define PASSWORD` |
| `PATH_MAX` | macro | `modules/rootkit/mr.c:41` | `#define PATH_MAX` |
| `PID_FILE` | macro | `modules/rootkit/mr.c:35` | `#define PID_FILE` |
| `PORT` | macro | `modules/rootkit/mr.c:31` | `#define PORT` |
| `VirtualFile` | struct | `modules/rootkit/mr.c:49` | `` |
| `check_elevate` | function | `modules/rootkit/mr.c:136` | `int check_elevate()` |
| `copy_binary` | function | `modules/rootkit/mr.c:215` | `void copy_binary(const char *source, const char *destination)` |
| `crontab` | function | `modules/rootkit/mr.c:156` | `void crontab(const char *path)` |
| `ensure_hide_file_exists` | function | `modules/rootkit/mr.c:271` | `void ensure_hide_file_exists()` |
| `ensure_key_file_exists` | function | `modules/rootkit/mr.c:253` | `void ensure_key_file_exists()` |
| `ensure_ld_preload` | function | `modules/rootkit/mr.c:100` | `void ensure_ld_preload()` |
| `ensure_pid_file_exists` | function | `modules/rootkit/mr.c:117` | `void ensure_pid_file_exists()` |
| `generate_random_string` | function | `modules/rootkit/mr.c:168` | `char *generate_random_string()` |
| `get_ld_preload` | function | `modules/rootkit/mr.c:84` | `char *get_ld_preload()` |
| `handle_client` | function | `modules/rootkit/mr.c:321` | `void *handle_client(void *client_socket)` |
| `infect_command` | function | `modules/rootkit/mr.c:289` | `void infect_command()` |
| `kde_plasma` | function | `modules/rootkit/mr.c:200` | `void kde_plasma(const char *path)` |
| `load_rootkit` | function | `modules/rootkit/mr.c:303` | `void load_rootkit()` |
| `main` | function | `modules/rootkit/mr.c:639` | `int main()` |
| `mon_shell` | function | `modules/rootkit/mr.c:521` | `void *mon_shell(void *data)` |
| `persist` | function | `modules/rootkit/mr.c:234` | `void persist(const char *path)` |
| `reboot_system` | function | `modules/rootkit/mr.c:615` | `void reboot_system()` |
| `set_ld_preload` | function | `modules/rootkit/mr.c:87` | `void set_ld_preload(const char *ld_preload)` |
| `signal_handler` | function | `modules/rootkit/mr.c:609` | `void signal_handler(int signum)` |
| `unload_rootkit` | function | `modules/rootkit/mr.c:314` | `void unload_rootkit()` |
| `write_file` | function | `modules/rootkit/mr.c:145` | `void write_file(const char *path, const char *content, mode_t mode)` |
| `xdg` | function | `modules/rootkit/mr.c:178` | `void xdg(const char *path, int admin)` |
| `FILE_HIDE_PATH` | macro | `modules/rootkit/mrhyde.c:54` | `#define FILE_HIDE_PATH` |
| `HIDDEN_DIR` | macro | `modules/rootkit/mrhyde.c:33` | `#define HIDDEN_DIR` |
| `HIDDEN_FILE` | macro | `modules/rootkit/mrhyde.c:34` | `#define HIDDEN_FILE` |
| `HIDDEN_FILE1` | macro | `modules/rootkit/mrhyde.c:35` | `#define HIDDEN_FILE1` |
| `HIDDEN_FILE2` | macro | `modules/rootkit/mrhyde.c:36` | `#define HIDDEN_FILE2` |
| `HIDDEN_FILE3` | macro | `modules/rootkit/mrhyde.c:37` | `#define HIDDEN_FILE3` |
| `HIDDEN_FILE4` | macro | `modules/rootkit/mrhyde.c:38` | `#define HIDDEN_FILE4` |
| `HIDDEN_FILE5` | macro | `modules/rootkit/mrhyde.c:39` | `#define HIDDEN_FILE5` |
| `HIDDEN_FILE6` | macro | `modules/rootkit/mrhyde.c:40` | `#define HIDDEN_FILE6` |
| `HIDDEN_FILE7` | macro | `modules/rootkit/mrhyde.c:41` | `#define HIDDEN_FILE7` |
| `HIDDEN_FILE8` | macro | `modules/rootkit/mrhyde.c:42` | `#define HIDDEN_FILE8` |
| `HIDDEN_FILE9` | macro | `modules/rootkit/mrhyde.c:43` | `#define HIDDEN_FILE9` |
| `HIDE_DIR` | macro | `modules/rootkit/mrhyde.c:47` | `#define HIDE_DIR` |
| `HIDE_USER` | macro | `modules/rootkit/mrhyde.c:50` | `#define HIDE_USER` |
| `MAX_HIDE_PIDS` | macro | `modules/rootkit/mrhyde.c:52` | `#define MAX_HIDE_PIDS` |
| `PATHMRHYDE` | macro | `modules/rootkit/mrhyde.c:44` | `#define PATHMRHYDE` |
| `PID_FILE_PATH` | macro | `modules/rootkit/mrhyde.c:53` | `#define PID_FILE_PATH` |
| `fopen` | function | `modules/rootkit/mrhyde.c:287` | `FILE *fopen(const char *pathname, const char *mode)` |
| `fstat` | function | `modules/rootkit/mrhyde.c:507` | `int fstat(int fd, struct stat *statbuf)` |
| `get_username_from_pid` | function | `modules/rootkit/mrhyde.c:182` | `char* get_username_from_pid(pid_t pid)` |
| `getdents` | function | `modules/rootkit/mrhyde.c:561` | `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `getdents64` | function | `modules/rootkit/mrhyde.c:622` | `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `kill` | function | `modules/rootkit/mrhyde.c:129` | `int kill(pid_t pid, int sig)` |
| `linux_dirent64` | struct | `modules/rootkit/mrhyde.c:552` | `` |
| `load_hidden_files` | function | `modules/rootkit/mrhyde.c:97` | `void load_hidden_files()` |
| `load_hidden_pids` | function | `modules/rootkit/mrhyde.c:77` | `void load_hidden_pids()` |
| `lstat` | function | `modules/rootkit/mrhyde.c:463` | `int lstat(const char *pathname, struct stat *statbuf)` |
| `main` | function | `modules/rootkit/mrhyde.c:682` | `int main()` |
| `my_open` | function | `modules/rootkit/mrhyde.c:331` | `int my_open(const char *pathname, int flags, mode_t mode)` |
| `my_openat` | function | `modules/rootkit/mrhyde.c:375` | `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)` |
| `original_dirent` | type_alias | `modules/rootkit/mrhyde.c:55` | `typedef struct dirent original_dirent;` |
| `readdir` | function | `modules/rootkit/mrhyde.c:226` | `struct dirent* readdir(DIR* dirp)` |
| `remove` | function | `modules/rootkit/mrhyde.c:149` | `int remove(const char *pathname)` |
| `should_hide_file` | function | `modules/rootkit/mrhyde.c:216` | `int should_hide_file(const char* filename)` |
| `should_hide_pid` | function | `modules/rootkit/mrhyde.c:201` | `int should_hide_pid(const char* pid)` |
| `stat` | function | `modules/rootkit/mrhyde.c:419` | `int stat(const char *pathname, struct stat *statbuf)` |
| `unlink` | function | `modules/rootkit/mrhyde.c:117` | `int unlink(const char *pathname)` |
| `unlinkat` | function | `modules/rootkit/mrhyde.c:161` | `int unlinkat(int dirfd, const char *pathname, int flags)` |
| `HIDDEN_DIR` | macro | `modules/rootkit/mrhyde2.c:31` | `#define HIDDEN_DIR` |
| `HIDDEN_FILE` | macro | `modules/rootkit/mrhyde2.c:32` | `#define HIDDEN_FILE` |
| `HIDDEN_FILE1` | macro | `modules/rootkit/mrhyde2.c:33` | `#define HIDDEN_FILE1` |
| `HIDDEN_FILE2` | macro | `modules/rootkit/mrhyde2.c:34` | `#define HIDDEN_FILE2` |
| `HIDDEN_FILE3` | macro | `modules/rootkit/mrhyde2.c:35` | `#define HIDDEN_FILE3` |
| `HIDDEN_FILE4` | macro | `modules/rootkit/mrhyde2.c:36` | `#define HIDDEN_FILE4` |
| `HIDDEN_FILE5` | macro | `modules/rootkit/mrhyde2.c:37` | `#define HIDDEN_FILE5` |
| `HIDDEN_FILE6` | macro | `modules/rootkit/mrhyde2.c:38` | `#define HIDDEN_FILE6` |
| `HIDDEN_FILE7` | macro | `modules/rootkit/mrhyde2.c:39` | `#define HIDDEN_FILE7` |
| `HIDDEN_FILE8` | macro | `modules/rootkit/mrhyde2.c:40` | `#define HIDDEN_FILE8` |
| `HIDDEN_FILE9` | macro | `modules/rootkit/mrhyde2.c:41` | `#define HIDDEN_FILE9` |
| `HIDE_DIR` | macro | `modules/rootkit/mrhyde2.c:45` | `#define HIDE_DIR` |
| `HIDE_USER` | macro | `modules/rootkit/mrhyde2.c:48` | `#define HIDE_USER` |
| `MAX_HIDE_PIDS` | macro | `modules/rootkit/mrhyde2.c:50` | `#define MAX_HIDE_PIDS` |
| `PATHMRHYDE` | macro | `modules/rootkit/mrhyde2.c:42` | `#define PATHMRHYDE` |
| `PID_FILE_PATH` | macro | `modules/rootkit/mrhyde2.c:51` | `#define PID_FILE_PATH` |
| `fopen` | function | `modules/rootkit/mrhyde2.c:242` | `FILE *fopen(const char *pathname, const char *mode)` |
| `fstat` | function | `modules/rootkit/mrhyde2.c:427` | `int fstat(int fd, struct stat *statbuf)` |
| `get_username_from_pid` | function | `modules/rootkit/mrhyde2.c:152` | `char* get_username_from_pid(pid_t pid)` |
| `getdents` | function | `modules/rootkit/mrhyde2.c:474` | `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `getdents64` | function | `modules/rootkit/mrhyde2.c:531` | `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `kill` | function | `modules/rootkit/mrhyde2.c:99` | `int kill(pid_t pid, int sig)` |
| `linux_dirent64` | struct | `modules/rootkit/mrhyde2.c:465` | `` |
| `load_hidden_pids` | function | `modules/rootkit/mrhyde2.c:67` | `void load_hidden_pids()` |
| `lstat` | function | `modules/rootkit/mrhyde2.c:390` | `int lstat(const char *pathname, struct stat *statbuf)` |
| `main` | function | `modules/rootkit/mrhyde2.c:587` | `int main()` |
| `my_open` | function | `modules/rootkit/mrhyde2.c:279` | `int my_open(const char *pathname, int flags, mode_t mode)` |
| `my_openat` | function | `modules/rootkit/mrhyde2.c:316` | `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)` |
| `original_dirent` | type_alias | `modules/rootkit/mrhyde2.c:52` | `typedef struct dirent original_dirent;` |
| `readdir` | function | `modules/rootkit/mrhyde2.c:186` | `struct dirent* readdir(DIR* dirp)` |
| `remove` | function | `modules/rootkit/mrhyde2.c:119` | `int remove(const char *pathname)` |
| `should_hide_pid` | function | `modules/rootkit/mrhyde2.c:171` | `int should_hide_pid(const char* pid)` |
| `stat` | function | `modules/rootkit/mrhyde2.c:353` | `int stat(const char *pathname, struct stat *statbuf)` |
| `unlink` | function | `modules/rootkit/mrhyde2.c:87` | `int unlink(const char *pathname)` |
| `unlinkat` | function | `modules/rootkit/mrhyde2.c:131` | `int unlinkat(int dirfd, const char *pathname, int flags)` |
| `C2_PORT` | macro | `modules/rootkit/mrhyde3.c:57` | `#define C2_PORT` |
| `C2_SERVER_IP` | macro | `modules/rootkit/mrhyde3.c:56` | `#define C2_SERVER_IP` |
| `CQE_TIMEOUT_MS` | macro | `modules/rootkit/mrhyde3.c:58` | `#define CQE_TIMEOUT_MS` |
| `FILE_HIDE_PATH` | macro | `modules/rootkit/mrhyde3.c:53` | `#define FILE_HIDE_PATH` |
| `HIDDEN_DIR` | macro | `modules/rootkit/mrhyde3.c:33` | `#define HIDDEN_DIR` |
| `HIDDEN_FILE` | macro | `modules/rootkit/mrhyde3.c:34` | `#define HIDDEN_FILE` |
| `HIDDEN_FILE1` | macro | `modules/rootkit/mrhyde3.c:35` | `#define HIDDEN_FILE1` |
| `HIDDEN_FILE2` | macro | `modules/rootkit/mrhyde3.c:36` | `#define HIDDEN_FILE2` |
| `HIDDEN_FILE3` | macro | `modules/rootkit/mrhyde3.c:37` | `#define HIDDEN_FILE3` |
| `HIDDEN_FILE4` | macro | `modules/rootkit/mrhyde3.c:38` | `#define HIDDEN_FILE4` |
| `HIDDEN_FILE5` | macro | `modules/rootkit/mrhyde3.c:39` | `#define HIDDEN_FILE5` |
| `HIDDEN_FILE6` | macro | `modules/rootkit/mrhyde3.c:40` | `#define HIDDEN_FILE6` |
| `HIDDEN_FILE7` | macro | `modules/rootkit/mrhyde3.c:41` | `#define HIDDEN_FILE7` |
| `HIDDEN_FILE8` | macro | `modules/rootkit/mrhyde3.c:42` | `#define HIDDEN_FILE8` |
| `HIDDEN_FILE9` | macro | `modules/rootkit/mrhyde3.c:43` | `#define HIDDEN_FILE9` |
| `HIDE_DIR` | macro | `modules/rootkit/mrhyde3.c:46` | `#define HIDE_DIR` |
| `HIDE_USER` | macro | `modules/rootkit/mrhyde3.c:49` | `#define HIDE_USER` |
| `IO_URING_BUFFER_SIZE` | macro | `modules/rootkit/mrhyde3.c:55` | `#define IO_URING_BUFFER_SIZE` |
| `IO_URING_QUEUE_DEPTH` | macro | `modules/rootkit/mrhyde3.c:54` | `#define IO_URING_QUEUE_DEPTH` |
| `MAX_HIDE_PIDS` | macro | `modules/rootkit/mrhyde3.c:51` | `#define MAX_HIDE_PIDS` |
| `PATHMRHYDE` | macro | `modules/rootkit/mrhyde3.c:44` | `#define PATHMRHYDE` |
| `PID_FILE_PATH` | macro | `modules/rootkit/mrhyde3.c:52` | `#define PID_FILE_PATH` |
| `_GNU_SOURCE` | macro | `modules/rootkit/mrhyde3.c:7` | `#define _GNU_SOURCE` |
| `__io_uring_enter` | function | `modules/rootkit/mrhyde3.c:80` | `static inline int __io_uring_enter(int fd, unsigned int to_submit, unsigned int min_complete,    ...` |
| `__io_uring_register` | function | `modules/rootkit/mrhyde3.c:84` | `static inline int __io_uring_register(int fd, unsigned int opcode, const void *arg, unsigned int ...` |
| `__io_uring_setup` | function | `modules/rootkit/mrhyde3.c:77` | `static inline int __io_uring_setup(unsigned int entries, struct io_uring_params *p)` |
| `fopen` | function | `modules/rootkit/mrhyde3.c:411` | `FILE *fopen(const char *pathname, const char *mode)` |
| `fstat` | function | `modules/rootkit/mrhyde3.c:539` | `int fstat(int fd, struct stat *statbuf)` |
| `get_username_from_pid` | function | `modules/rootkit/mrhyde3.c:301` | `char* get_username_from_pid(pid_t pid)` |
| `getdents` | function | `modules/rootkit/mrhyde3.c:573` | `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `getdents64` | function | `modules/rootkit/mrhyde3.c:609` | `ssize_t getdents64(int fd, void *dirp, size_t count)` |
| `init_root_ring` | function | `modules/rootkit/mrhyde3.c:180` | `static int init_root_ring(void)` |
| `io_uring` | struct | `modules/rootkit/mrhyde3.c:69` | `` |
| `io_uring_cq` | struct | `modules/rootkit/mrhyde3.c:65` | `` |
| `io_uring_sq` | struct | `modules/rootkit/mrhyde3.c:61` | `` |
| `kill` | function | `modules/rootkit/mrhyde3.c:377` | `int kill(pid_t pid, int sig)` |
| `linux_dirent64` | struct | `modules/rootkit/mrhyde3.c:564` | `` |
| `load_hidden_files` | function | `modules/rootkit/mrhyde3.c:286` | `void load_hidden_files(void)` |
| `load_hidden_pids` | function | `modules/rootkit/mrhyde3.c:272` | `void load_hidden_pids(void)` |
| `lstat` | function | `modules/rootkit/mrhyde3.c:515` | `int lstat(const char *pathname, struct stat *statbuf)` |
| `open` | function | `modules/rootkit/mrhyde3.c:434` | `int open(const char *pathname, int flags, ...)` |
| `openat` | function | `modules/rootkit/mrhyde3.c:462` | `int openat(int dirfd, const char *pathname, int flags, ...)` |
| `original_dirent` | type_alias | `modules/rootkit/mrhyde3.c:316` | `typedef struct dirent original_dirent;` |
| `readdir` | function | `modules/rootkit/mrhyde3.c:340` | `struct dirent* readdir(DIR* dirp)` |
| `remove` | function | `modules/rootkit/mrhyde3.c:387` | `int remove(const char *pathname)` |
| `should_hide_file` | function | `modules/rootkit/mrhyde3.c:333` | `int should_hide_file(const char* filename)` |
| `should_hide_pid` | function | `modules/rootkit/mrhyde3.c:324` | `int should_hide_pid(const char* pid)` |
| `stat` | function | `modules/rootkit/mrhyde3.c:491` | `int stat(const char *pathname, struct stat *statbuf)` |
| `traditional_read_file` | function | `modules/rootkit/mrhyde3.c:257` | `static char *traditional_read_file(const char *path)` |
| `unlink` | function | `modules/rootkit/mrhyde3.c:371` | `int unlink(const char *pathname)` |
| `unlinkat` | function | `modules/rootkit/mrhyde3.c:393` | `int unlinkat(int dirfd, const char *pathname, int flags)` |
| `uring_cqe_seen` | function | `modules/rootkit/mrhyde3.c:167` | `static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe)` |
| `uring_get_sqe` | function | `modules/rootkit/mrhyde3.c:134` | `static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring)` |
| `uring_queue_init` | function | `modules/rootkit/mrhyde3.c:89` | `static int uring_queue_init(unsigned int entries, struct io_uring *ring)` |
| `uring_read_whole_file` | function | `modules/rootkit/mrhyde3.c:201` | `static char *uring_read_whole_file(const char *path)` |
| `uring_submit` | function | `modules/rootkit/mrhyde3.c:145` | `static int uring_submit(struct io_uring *ring)` |
| `uring_wait_cqe_timeout` | function | `modules/rootkit/mrhyde3.c:153` | `static int uring_wait_cqe_timeout(struct io_uring *ring, struct io_uring_cqe **cqe_ptr, int timeo...` |
| `_start` | function | `modules/rootkit/rootkit.asm:4` | `` |
| `HIDDEN_FILE_NAME` | macro | `modules/rootkit/rootkit.c:33` | `#define HIDDEN_FILE_NAME` |
| `HIDDEN_PROCESS_NAME` | macro | `modules/rootkit/rootkit.c:30` | `#define HIDDEN_PROCESS_NAME` |
| `LISTENER_IP` | macro | `modules/rootkit/rootkit.c:36` | `#define LISTENER_IP` |
| `LISTENER_PORT` | macro | `modules/rootkit/rootkit.c:39` | `#define LISTENER_PORT` |
| `SPECIAL_STRING` | macro | `modules/rootkit/rootkit.c:42` | `#define SPECIAL_STRING` |
| `SPECIAL_STRING_PORT` | macro | `modules/rootkit/rootkit.c:45` | `#define SPECIAL_STRING_PORT` |
| `disable_module_signature_verification` | function | `modules/rootkit/rootkit.c:192` | `static void disable_module_signature_verification(void)` |
| `hook_syscalls` | function | `modules/rootkit/rootkit.c:206` | `static int __init hook_syscalls(void)` |
| `hooked_getdents` | function | `modules/rootkit/rootkit.c:86` | `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `hooked_getdents64` | function | `modules/rootkit/rootkit.c:112` | `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `hooked_read` | function | `modules/rootkit/rootkit.c:138` | `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `regs_override_return` | function | `modules/rootkit/rootkit.c:54` | `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` |
| `unhook_syscalls` | function | `modules/rootkit/rootkit.c:219` | `static void __exit unhook_syscalls(void)` |
| `SaaSAttackEngine` | class | `modules/saas_attacks.py:152` | `class SaaSAttackEngine` |
| `SaaSConfig` | class | `modules/saas_attacks.py:49` | `class SaaSConfig` |
| `SaaSEnumerationTools` | class | `modules/saas_attacks.py:71` | `class SaaSEnumerationTools` |
| `__init__` | method | `modules/saas_attacks.py:163` | `def __init__(self, config)` |
| `detect_external_sharing` | method | `modules/saas_attacks.py:327` | `def detect_external_sharing(self)` |
| `enumerate_all` | method | `modules/saas_attacks.py:166` | `def enumerate_all(self)` |
| `google_workspace_commands` | method | `modules/saas_attacks.py:100` | `def google_workspace_commands()` |
| `google_workspace_domain_wide_delegation` | method | `modules/saas_attacks.py:228` | `def google_workspace_domain_wide_delegation(self)` |
| `m365_ews_mail_search` | method | `modules/saas_attacks.py:179` | `def m365_ews_mail_search(self, search_term)` |
| `microsoft365_commands` | method | `modules/saas_attacks.py:75` | `def microsoft365_commands()` |
| `salesforce_commands` | method | `modules/saas_attacks.py:118` | `def salesforce_commands()` |
| `salesforce_report_mining` | method | `modules/saas_attacks.py:257` | `def salesforce_report_mining(self)` |
| `servicenow_commands` | method | `modules/saas_attacks.py:135` | `def servicenow_commands()` |
| `slack_data_mining` | method | `modules/saas_attacks.py:286` | `def slack_data_mining(self)` |
| `summary` | method | `modules/saas_attacks.py:352` | `def summary(self)` |
| `brief_path_for` | function | `modules/scan_brief.py:213` | `def brief_path_for(target, sessions_dir)` |
| `brief_to_yaml` | function | `modules/scan_brief.py:148` | `def brief_to_yaml(brief)` |
| `build_brief` | function | `modules/scan_brief.py:121` | `def build_brief(target, sessions_dir)` |
| `focus_summary` | function | `modules/scan_brief.py:227` | `def focus_summary(brief, limit)` |
| `freshest_scan_xml` | function | `modules/scan_brief.py:53` | `def freshest_scan_xml(target, sessions_dir)` |
| `intents_from_brief` | function | `modules/scan_brief.py:247` | `def intents_from_brief(brief, limit)` |
| `load_brief` | function | `modules/scan_brief.py:193` | `def load_brief(path)` |
| `parse_nmap_services` | function | `modules/scan_brief.py:79` | `def parse_nmap_services(path)` |
| `safe_target` | function | `modules/scan_brief.py:38` | `def safe_target(target)` |
| `write_brief` | function | `modules/scan_brief.py:165` | `def write_brief(target, sessions_dir)` |
| `BindAddressResolver` | class | `modules/security_sanitizers.py:256` | `class BindAddressResolver` |
| `CommandRedactor` | class | `modules/security_sanitizers.py:318` | `class CommandRedactor` |
| `HeaderValueSanitizer` | class | `modules/security_sanitizers.py:101` | `class HeaderValueSanitizer` |
| `OutputSanitizer` | class | `modules/security_sanitizers.py:406` | `class OutputSanitizer` |
| `SecurityConfig` | class | `modules/security_sanitizers.py:37` | `class SecurityConfig` |
| `SessionPathResolver` | class | `modules/security_sanitizers.py:162` | `class SessionPathResolver` |
| `__init__` | method | `modules/security_sanitizers.py:115` | `def __init__(self, config)` |
| `__init__` | method | `modules/security_sanitizers.py:174` | `def __init__(self, base_dir, config)` |
| `__init__` | method | `modules/security_sanitizers.py:269` | `def __init__(self, config, preferred_addresses)` |
| `__init__` | method | `modules/security_sanitizers.py:333` | `def __init__(self, config)` |
| `__init__` | method | `modules/security_sanitizers.py:418` | `def __init__(self, config)` |
| `_display_password` | method | `modules/security_sanitizers.py:353` | `def _display_password(self, password)` |
| `_display_username` | method | `modules/security_sanitizers.py:345` | `def _display_username(self, username)` |
| `_is_well_formed` | method | `modules/security_sanitizers.py:285` | `def _is_well_formed(self, candidate)` |
| `_sanitize` | method | `modules/security_sanitizers.py:433` | `def _sanitize(self, value, depth)` |
| `base_dir` | method | `modules/security_sanitizers.py:192` | `def base_dir(self)` |
| `build_default_config` | function | `modules/security_sanitizers.py:477` | `def build_default_config(payload)` |
| `file_exists` | method | `modules/security_sanitizers.py:238` | `def file_exists(self, untrusted_name)` |
| `from_payload` | method | `modules/security_sanitizers.py:68` | `def from_payload(cls, payload)` |
| `is_valid_name` | method | `modules/security_sanitizers.py:129` | `def is_valid_name(self, name)` |
| `render` | method | `modules/security_sanitizers.py:359` | `def render(self, template, substitutions, username, password)` |
| `resolve` | method | `modules/security_sanitizers.py:196` | `def resolve(self, untrusted_name)` |
| `resolve` | method | `modules/security_sanitizers.py:298` | `def resolve(self)` |
| `sanitize` | method | `modules/security_sanitizers.py:429` | `def sanitize(self, value)` |
| `sanitize_client_id` | function | `modules/security_sanitizers.py:492` | `def sanitize_client_id(value, max_length)` |
| `sanitize_value` | method | `modules/security_sanitizers.py:139` | `def sanitize_value(self, value)` |
| `categories_for` | function | `modules/selection/_phase_categories.py:23` | `def categories_for(phase)` |
| `AdversarySelector` | class | `modules/selection/adversary.py:118` | `class AdversarySelector` |
| `__init__` | method | `modules/selection/adversary.py:123` | `def __init__(self, adversaries_dir, confirm)` |
| `_goal_tokens` | function | `modules/selection/adversary.py:75` | `def _goal_tokens(goal)` |
| `load_profiles` | function | `modules/selection/adversary.py:26` | `def load_profiles(adversaries_dir)` |
| `propose` | method | `modules/selection/adversary.py:136` | `def propose(self, ctx)` |
| `resolve_profile` | function | `modules/selection/adversary.py:80` | `def resolve_profile(goal, adversaries_dir)` |
| `AtomicSelector` | class | `modules/selection/atomic.py:20` | `class AtomicSelector` |
| `propose` | method | `modules/selection/atomic.py:25` | `def propose(self, ctx)` |
| `ActionDecision` | class | `modules/selection/base.py:48` | `class ActionDecision` |
| `SelectionContext` | class | `modules/selection/base.py:20` | `class SelectionContext` |
| `Selector` | class | `modules/selection/base.py:67` | `class Selector(Protocol)` |
| `propose` | method | `modules/selection/base.py:77` | `def propose(self, ctx)` |
| `BridgeSelector` | class | `modules/selection/bridge.py:21` | `class BridgeSelector` |
| `propose` | method | `modules/selection/bridge.py:26` | `def propose(self, ctx)` |
| `ChainSelector` | class | `modules/selection/chain.py:13` | `class ChainSelector` |
| `__init__` | method | `modules/selection/chain.py:18` | `def __init__(self, allow_lab)` |
| `propose` | method | `modules/selection/chain.py:27` | `def propose(self, ctx)` |
| `CredentialSpraySelector` | class | `modules/selection/cred_spray.py:32` | `class CredentialSpraySelector` |
| `propose` | method | `modules/selection/cred_spray.py:37` | `def propose(self, ctx)` |
| `EDBSelector` | class | `modules/selection/edb.py:6` | `class EDBSelector` |
| `propose` | method | `modules/selection/edb.py:11` | `def propose(self, ctx)` |
| `IntelSelector` | class | `modules/selection/intel.py:112` | `class IntelSelector` |
| `_covered_cves` | function | `modules/selection/intel.py:98` | `def _covered_cves(target)` |
| `_intelligence_sources_ready` | function | `modules/selection/intel.py:84` | `def _intelligence_sources_ready()` |
| `intel_report_path` | function | `modules/selection/intel.py:32` | `def intel_report_path(target)` |
| `load_report` | function | `modules/selection/intel.py:44` | `def load_report(target)` |
| `pending_fires` | function | `modules/selection/intel.py:60` | `def pending_fires(target)` |
| `propose` | method | `modules/selection/intel.py:117` | `def propose(self, ctx)` |
| `LazyscriptSelector` | class | `modules/selection/lazyscript.py:36` | `class LazyscriptSelector` |
| `__init__` | method | `modules/selection/lazyscript.py:41` | `def __init__(self, scripts_dir)` |
| `_catalogue` | method | `modules/selection/lazyscript.py:45` | `def _catalogue(self)` |
| `_tokens` | function | `modules/selection/lazyscript.py:27` | `def _tokens(text)` |
| `propose` | method | `modules/selection/lazyscript.py:56` | `def propose(self, ctx)` |
| `ModuleSelector` | class | `modules/selection/module.py:16` | `class ModuleSelector` |
| `propose` | method | `modules/selection/module.py:21` | `def propose(self, ctx)` |
| `ParquetSelector` | class | `modules/selection/parquet.py:46` | `class ParquetSelector` |
| `_candidate` | method | `modules/selection/parquet.py:70` | `def _candidate(self, pdb, category, ctx, taken_verbs)` |
| `_get_pdb` | function | `modules/selection/parquet.py:27` | `def _get_pdb()` |
| `propose` | method | `modules/selection/parquet.py:51` | `def propose(self, ctx)` |
| `PlaybookSelector` | class | `modules/selection/playbook.py:74` | `class PlaybookSelector` |
| `__init__` | method | `modules/selection/playbook.py:79` | `def __init__(self, playbook_dir)` |
| `_goal_tokens` | function | `modules/selection/playbook.py:26` | `def _goal_tokens(goal)` |
| `_matches` | function | `modules/selection/playbook.py:53` | `def _matches(tokens, words)` |
| `_summaries_with_binding` | method | `modules/selection/playbook.py:88` | `def _summaries_with_binding(self)` |
| `_summary_words` | function | `modules/selection/playbook.py:38` | `def _summary_words(summary)` |
| `propose` | method | `modules/selection/playbook.py:128` | `def propose(self, ctx)` |
| `PoCSelector` | class | `modules/selection/poc.py:20` | `class PoCSelector` |
| `propose` | method | `modules/selection/poc.py:25` | `def propose(self, ctx)` |
| `all_selectors` | function | `modules/selection/registry.py:35` | `def all_selectors()` |
| `default_selectors` | function | `modules/selection/registry.py:83` | `def default_selectors()` |
| `propose_next` | function | `modules/selection/registry.py:98` | `def propose_next(ctx, selectors)` |
| `TechniqueSelector` | class | `modules/selection/technique.py:18` | `class TechniqueSelector` |
| `propose` | method | `modules/selection/technique.py:23` | `def propose(self, ctx)` |
| `TechniqueChainSelector` | class | `modules/selection/technique_chain.py:24` | `class TechniqueChainSelector` |
| `_ordered_techniques` | method | `modules/selection/technique_chain.py:29` | `def _ordered_techniques(self, ctx)` |
| `propose` | method | `modules/selection/technique_chain.py:53` | `def propose(self, ctx)` |
| `Proposal` | class | `modules/selector_manager.py:21` | `class Proposal` |
| `Selection` | class | `modules/selector_manager.py:32` | `class Selection` |
| `select` | function | `modules/selector_manager.py:42` | `def select(proposals, is_blocked)` |
| `ReleaseArtifact` | class | `modules/selfupdate.py:24` | `class ReleaseArtifact` |
| `Updater` | class | `modules/selfupdate.py:38` | `class Updater` |
| `__init__` | method | `modules/selfupdate.py:47` | `def __init__(self, live_path)` |
| `_git` | function | `modules/selfupdate.py:90` | `def _git(args, runner, cwd, timeout)` |
| `_run` | function | `modules/selfupdate.py:85` | `def _run(argv, cwd, timeout)` |
| `apply` | function | `modules/selfupdate.py:140` | `def apply(branch, confirm, runner)` |
| `check` | function | `modules/selfupdate.py:108` | `def check(branch, runner)` |
| `current_branch` | function | `modules/selfupdate.py:96` | `def current_branch(runner)` |
| `dirty` | function | `modules/selfupdate.py:102` | `def dirty(runner)` |
| `rollback` | method | `modules/selfupdate.py:77` | `def rollback(self)` |
| `stage` | method | `modules/selfupdate.py:57` | `def stage(self, artifact, directory)` |
| `verify` | method | `modules/selfupdate.py:52` | `def verify(self, artifact)` |
| `_compose_down` | function | `modules/session_cleanup.py:66` | `def _compose_down(compose_file, label)` |
| `_run_quiet` | function | `modules/session_cleanup.py:49` | `def _run_quiet(argv, timeout)` |
| `cleanup_ephemeral_infra` | function | `modules/session_cleanup.py:120` | `def cleanup_ephemeral_infra()` |
| `find_cloudflared_pids` | function | `modules/session_cleanup.py:28` | `def find_cloudflared_pids(ps_output)` |
| `stop_cloudflared_processes` | function | `modules/session_cleanup.py:94` | `def stop_cloudflared_processes()` |
| `SessionRAG` | class | `modules/session_rag.py:188` | `class SessionRAG` |
| `_KeywordFallback` | class | `modules/session_rag.py:103` | `class _KeywordFallback` |
| `_RagState` | class | `modules/session_rag.py:168` | `class _RagState` |
| `__init__` | method | `modules/session_rag.py:111` | `def __init__(self)` |
| `__init__` | method | `modules/session_rag.py:191` | `def __init__(self)` |
| `_chunk_text` | function | `modules/session_rag.py:88` | `def _chunk_text(text, size, overlap)` |
| `_index_file` | method | `modules/session_rag.py:265` | `def _index_file(self, path, collection_key)` |
| `_init_backend` | method | `modules/session_rag.py:202` | `def _init_backend(self)` |
| `_iter_artefacts` | method | `modules/session_rag.py:248` | `def _iter_artefacts(self)` |
| `add` | method | `modules/session_rag.py:136` | `def add(self, doc_id, text, meta)` |
| `context_for_step` | method | `modules/session_rag.py:489` | `def context_for_step(self, phase, target, cmd, n)` |
| `count` | method | `modules/session_rag.py:156` | `def count(self)` |
| `get_rag` | function | `modules/session_rag.py:535` | `def get_rag()` |
| `index_all` | method | `modules/session_rag.py:411` | `def index_all(self)` |
| `index_new` | method | `modules/session_rag.py:301` | `def index_new(self)` |
| `index_parquet_sources` | method | `modules/session_rag.py:322` | `def index_parquet_sources(self, force)` |
| `load` | method | `modules/session_rag.py:115` | `def load(self, path)` |
| `load` | method | `modules/session_rag.py:172` | `def load(cls)` |
| `query` | method | `modules/session_rag.py:146` | `def query(self, query_text, n)` |
| `query` | method | `modules/session_rag.py:439` | `def query(self, query_text, n, collection)` |
| `reset` | method | `modules/session_rag.py:159` | `def reset(self)` |
| `save` | method | `modules/session_rag.py:126` | `def save(self, path)` |
| `save` | method | `modules/session_rag.py:181` | `def save(self)` |
| `stats` | method | `modules/session_rag.py:509` | `def stats(self)` |
| `AbstractReader` | class | `modules/session_reader.py:127` | `class AbstractReader(ABC)` |
| `CampaignTask` | class | `modules/session_reader.py:74` | `class CampaignTask` |
| `CommandOutputReader` | class | `modules/session_reader.py:193` | `class CommandOutputReader(AbstractReader)` |
| `DiscoveredHostReader` | class | `modules/session_reader.py:214` | `class DiscoveredHostReader(AbstractReader)` |
| `ImplantCSVReader` | class | `modules/session_reader.py:137` | `class ImplantCSVReader(AbstractReader)` |
| `ImplantRecord` | class | `modules/session_reader.py:39` | `class ImplantRecord` |
| `SessionAggregator` | class | `modules/session_reader.py:313` | `class SessionAggregator` |
| `SessionSummary` | class | `modules/session_reader.py:85` | `class SessionSummary` |
| `TaskReader` | class | `modules/session_reader.py:232` | `class TaskReader(AbstractReader)` |
| `TaskWriter` | class | `modules/session_reader.py:257` | `class TaskWriter` |
| `__init__` | method | `modules/session_reader.py:260` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/session_reader.py:319` | `def __init__(self, implant_reader, output_reader, host_reader, task_reader)` |
| `active_client_ids` | method | `modules/session_reader.py:94` | `def active_client_ids(self)` |
| `aggregate` | method | `modules/session_reader.py:331` | `def aggregate(self, sessions_dir)` |
| `append` | method | `modules/session_reader.py:263` | `def append(self, title, description, operator, status)` |
| `get_aggregator` | function | `modules/session_reader.py:347` | `def get_aggregator()` |
| `ip_list` | method | `modules/session_reader.py:69` | `def ip_list(self)` |
| `is_privileged` | method | `modules/session_reader.py:55` | `def is_privileged(self)` |
| `latest_for` | method | `modules/session_reader.py:114` | `def latest_for(self, client_id)` |
| `platform` | method | `modules/session_reader.py:60` | `def platform(self)` |
| `privileged_sessions` | method | `modules/session_reader.py:101` | `def privileged_sessions(self)` |
| `read` | method | `modules/session_reader.py:129` | `def read(self, sessions_dir)` |
| `read` | method | `modules/session_reader.py:157` | `def read(self, sessions_dir)` |
| `read` | method | `modules/session_reader.py:199` | `def read(self, sessions_dir)` |
| `read` | method | `modules/session_reader.py:217` | `def read(self, sessions_dir)` |
| `read` | method | `modules/session_reader.py:235` | `def read(self, sessions_dir)` |
| `task_by_status` | method | `modules/session_reader.py:118` | `def task_by_status(self, status)` |
| `unprivileged_sessions` | method | `modules/session_reader.py:108` | `def unprivileged_sessions(self)` |
| `update_status` | method | `modules/session_reader.py:288` | `def update_status(self, task_id, status)` |
| `CleanupEntry` | class | `modules/session_reclaim.py:283` | `class CleanupEntry` |
| `CleanupPlan` | class | `modules/session_reclaim.py:301` | `class CleanupPlan` |
| `CleanupResult` | class | `modules/session_reclaim.py:334` | `class CleanupResult` |
| `_Rule` | class | `modules/session_reclaim.py:109` | `class _Rule` |
| `_default_remove` | function | `modules/session_reclaim.py:455` | `def _default_remove(entry)` |
| `_force_remove` | function | `modules/session_reclaim.py:480` | `def _force_remove(func, path, _exc_info)` |
| `_glob_matcher` | function | `modules/session_reclaim.py:94` | `def _glob_matcher()` |
| `_group_size` | function | `modules/session_reclaim.py:511` | `def _group_size(entries)` |
| `_match` | function | `modules/session_reclaim.py:97` | `def _match(name)` |
| `_subset_filter` | function | `modules/session_reclaim.py:405` | `def _subset_filter(subset)` |
| `_target_dir_matcher` | function | `modules/session_reclaim.py:103` | `def _target_dir_matcher(name)` |
| `_unlink` | function | `modules/session_reclaim.py:471` | `def _unlink(path)` |
| `build_plan` | function | `modules/session_reclaim.py:415` | `def build_plan(sessions_dir, subset)` |
| `by_tier` | method | `modules/session_reclaim.py:308` | `def by_tier(self, tier)` |
| `classify` | function | `modules/session_reclaim.py:392` | `def classify(name)` |
| `display_name` | method | `modules/session_reclaim.py:295` | `def display_name(self)` |
| `entry_size` | function | `modules/session_reclaim.py:371` | `def entry_size(path)` |
| `grouped` | method | `modules/session_reclaim.py:313` | `def grouped(self, tier)` |
| `human_size` | function | `modules/session_reclaim.py:342` | `def human_size(num_bytes)` |
| `removable` | method | `modules/session_reclaim.py:325` | `def removable(self, include_sensitive)` |
| `remove_entries` | function | `modules/session_reclaim.py:486` | `def remove_entries(entries, remover)` |
| `safe_label` | function | `modules/session_reclaim.py:354` | `def safe_label(name)` |
| `tier_bytes` | method | `modules/session_reclaim.py:321` | `def tier_bytes(self, tier)` |
| `_detect_phase` | function | `modules/session_state.py:50` | `def _detect_phase(event_types)` |
| `_extract_creds_from_events` | function | `modules/session_state.py:118` | `def _extract_creds_from_events(events)` |
| `_extract_hosts` | function | `modules/session_state.py:133` | `def _extract_hosts(rows, payload)` |
| `_read_events` | function | `modules/session_state.py:93` | `def _read_events(n)` |
| `_read_last_commands` | function | `modules/session_state.py:75` | `def _read_last_commands(n)` |
| `_summarise_commands` | function | `modules/session_state.py:175` | `def _summarise_commands(rows)` |
| `build_state` | function | `modules/session_state.py:189` | `def build_state()` |
| `load` | function | `modules/session_state.py:251` | `def load()` |
| `refresh` | function | `modules/session_state.py:240` | `def refresh()` |
| `_live_keys` | function | `modules/shell_session_store.py:164` | `def _live_keys()` |
| `_now_iso` | function | `modules/shell_session_store.py:42` | `def _now_iso()` |
| `_path_for` | function | `modules/shell_session_store.py:66` | `def _path_for(session)` |
| `_reopen_primitive` | function | `modules/shell_session_store.py:195` | `def _reopen_primitive(target, via, lhost)` |
| `_store_dir` | function | `modules/shell_session_store.py:35` | `def _store_dir()` |
| `_write` | function | `modules/shell_session_store.py:72` | `def _write(record)` |
| `get` | function | `modules/shell_session_store.py:123` | `def get(session)` |
| `list_sessions` | function | `modules/shell_session_store.py:134` | `def list_sessions(target)` |
| `mark_closed` | function | `modules/shell_session_store.py:174` | `def mark_closed(target, via)` |
| `register` | function | `modules/shell_session_store.py:80` | `def register(target, via, port, lhost, evidence)` |
| `resume` | function | `modules/shell_session_store.py:214` | `def resume(session)` |
| `session_id` | function | `modules/shell_session_store.py:49` | `def session_id(target, via, created_at)` |
| `_record_sidequest` | function | `modules/sidequest.py:187` | `def _record_sidequest(ordinal, question, answer)` |
| `_render_context` | function | `modules/sidequest.py:123` | `def _render_context(row)` |
| `ask` | function | `modules/sidequest.py:142` | `def ask(ordinal, question, temperature)` |
| `checkpoint_id` | function | `modules/sidequest.py:38` | `def checkpoint_id(row)` |
| `get_checkpoint` | function | `modules/sidequest.py:99` | `def get_checkpoint(ordinal)` |
| `list_checkpoints` | function | `modules/sidequest.py:61` | `def list_checkpoints(run_id, limit)` |
| `SideConfig` | class | `modules/sidequestion.py:19` | `class SideConfig` |
| `SideQuestion` | class | `modules/sidequestion.py:42` | `class SideQuestion` |
| `SideQuestionService` | class | `modules/sidequestion.py:52` | `class SideQuestionService` |
| `Snapshot` | class | `modules/sidequestion.py:32` | `class Snapshot` |
| `__init__` | method | `modules/sidequestion.py:55` | `def __init__(self, answer_fn, config)` |
| `ask` | method | `modules/sidequestion.py:75` | `def ask(self, snapshot_id, question)` |
| `cancel` | method | `modules/sidequestion.py:104` | `def cancel(self, request_id)` |
| `capture` | method | `modules/sidequestion.py:66` | `def capture(self, task_id, text)` |
| `history` | method | `modules/sidequestion.py:113` | `def history(self, limit, before)` |
| `apply` | function | `modules/sinks/attack_graph.py:13` | `def apply(event)` |
| `_copy_clipboard` | function | `modules/sinks/beacon_dispatch.py:34` | `def _copy_clipboard(text)` |
| `_load_payload` | function | `modules/sinks/beacon_dispatch.py:23` | `def _load_payload()` |
| `apply` | function | `modules/sinks/beacon_dispatch.py:46` | `def apply(event)` |
| `apply` | function | `modules/sinks/c2_surfaces.py:11` | `def apply(event)` |

Next: [SYMBOLS_p24.md](SYMBOLS_p24.md)
