# Symbols (page 22 of 50)
Previous: [SYMBOLS_p21.md](SYMBOLS_p21.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `sanitize_value` | method | `modules/security_sanitizers.py:139` | `def sanitize_value(self, value)` |
| `AdversarySelector` | class | `modules/selection/adversary.py:118` | `class AdversarySelector` |
| `__init__` | method | `modules/selection/adversary.py:123` | `def __init__(self, adversaries_dir, confirm)` |
| `_goal_tokens` | function | `modules/selection/adversary.py:75` | `def _goal_tokens(goal)` |
| `load_profiles` | function | `modules/selection/adversary.py:26` | `def load_profiles(adversaries_dir)` |
| `propose` | method | `modules/selection/adversary.py:136` | `def propose(self, ctx)` |
| `resolve_profile` | function | `modules/selection/adversary.py:80` | `def resolve_profile(goal, adversaries_dir)` |
| `AtomicSelector` | class | `modules/selection/atomic.py:20` | `class AtomicSelector` |
| `propose` | method | `modules/selection/atomic.py:25` | `def propose(self, ctx)` |
| `ActionDecision` | class | `modules/selection/base.py:44` | `class ActionDecision` |
| `SelectionContext` | class | `modules/selection/base.py:20` | `class SelectionContext` |
| `Selector` | class | `modules/selection/base.py:63` | `class Selector(Protocol)` |
| `propose` | method | `modules/selection/base.py:73` | `def propose(self, ctx)` |
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
| `PlaybookSelector` | class | `modules/selection/playbook.py:74` | `class PlaybookSelector` |
| `__init__` | method | `modules/selection/playbook.py:79` | `def __init__(self, playbook_dir)` |
| `_goal_tokens` | function | `modules/selection/playbook.py:26` | `def _goal_tokens(goal)` |
| `_matches` | function | `modules/selection/playbook.py:53` | `def _matches(tokens, words)` |
| `_summaries_with_binding` | method | `modules/selection/playbook.py:88` | `def _summaries_with_binding(self)` |
| `_summary_words` | function | `modules/selection/playbook.py:38` | `def _summary_words(summary)` |
| `propose` | method | `modules/selection/playbook.py:128` | `def propose(self, ctx)` |
| `PoCSelector` | class | `modules/selection/poc.py:20` | `class PoCSelector` |
| `propose` | method | `modules/selection/poc.py:25` | `def propose(self, ctx)` |
| `all_selectors` | function | `modules/selection/registry.py:31` | `def all_selectors()` |
| `default_selectors` | function | `modules/selection/registry.py:61` | `def default_selectors()` |
| `propose_next` | function | `modules/selection/registry.py:76` | `def propose_next(ctx, selectors)` |
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
| `_detect_phase` | function | `modules/session_state.py:50` | `def _detect_phase(event_types)` |
| `_extract_creds_from_events` | function | `modules/session_state.py:118` | `def _extract_creds_from_events(events)` |
| `_extract_hosts` | function | `modules/session_state.py:133` | `def _extract_hosts(rows, payload)` |
| `_read_events` | function | `modules/session_state.py:93` | `def _read_events(n)` |
| `_read_last_commands` | function | `modules/session_state.py:75` | `def _read_last_commands(n)` |
| `_summarise_commands` | function | `modules/session_state.py:175` | `def _summarise_commands(rows)` |
| `build_state` | function | `modules/session_state.py:189` | `def build_state()` |
| `load` | function | `modules/session_state.py:251` | `def load()` |
| `refresh` | function | `modules/session_state.py:240` | `def refresh()` |
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
| `apply` | function | `modules/sinks/campaign_db.py:9` | `def apply(event)` |
| `apply` | function | `modules/sinks/chain_feed.py:22` | `def apply(event)` |
| `apply` | function | `modules/sinks/event_bus.py:9` | `def apply(event)` |
| `apply` | function | `modules/sinks/findings.py:42` | `def apply(event)` |
| `handoff` | function | `modules/sinks/findings.py:88` | `def handoff(engagement_id, status, rounds)` |
| `ingest_discarded` | function | `modules/sinks/findings.py:107` | `def ingest_discarded(engagement_id, entries)` |
| `ledger_for` | function | `modules/sinks/findings.py:72` | `def ledger_for(engagement_id)` |
| `limits_for` | function | `modules/sinks/findings.py:22` | `def limits_for()` |
| `apply` | function | `modules/sinks/intel_graph.py:13` | `def apply(event)` |
| `apply` | function | `modules/sinks/killchain.py:11` | `def apply(event)` |
| `_db_mirror` | function | `modules/sinks/lazy_intel.py:88` | `def _db_mirror(host, row)` |
| `_world_mirror` | function | `modules/sinks/lazy_intel.py:58` | `def _world_mirror(host, row, temperature, severity)` |
| `apply` | function | `modules/sinks/lazy_intel.py:28` | `def apply(event)` |
| `apply` | function | `modules/sinks/objectives.py:16` | `def apply(event)` |
| `apply` | function | `modules/sinks/routing.py:9` | `def apply(event)` |
| `_current_host` | function | `modules/sinks/world_diff.py:58` | `def _current_host(root, host)` |
| `_store_host` | function | `modules/sinks/world_diff.py:65` | `def _store_host(root, host, snapshot)` |
| `_stored_host` | function | `modules/sinks/world_diff.py:52` | `def _stored_host(root, host)` |
| `apply` | function | `modules/sinks/world_diff.py:14` | `def apply(event)` |
| `apply` | function | `modules/sinks/world_model.py:12` | `def apply(event)` |
| `OsPlatform` | class | `modules/sleep_obfuscation.py:57` | `class OsPlatform(str, Enum)` |
| `SleepObfuscationConfig` | class | `modules/sleep_obfuscation.py:100` | `class SleepObfuscationConfig` |
| `SleepObfuscationEngine` | class | `modules/sleep_obfuscation.py:394` | `class SleepObfuscationEngine` |
| `SleepTechnique` | class | `modules/sleep_obfuscation.py:73` | `class SleepTechnique` |
| `SleepTechniqueCatalog` | class | `modules/sleep_obfuscation.py:163` | `class SleepTechniqueCatalog` |
| `SleepTechniqueValidator` | class | `modules/sleep_obfuscation.py:365` | `class SleepTechniqueValidator` |
| `TechniqueRisk` | class | `modules/sleep_obfuscation.py:64` | `class TechniqueRisk(str, Enum)` |
| `__init__` | method | `modules/sleep_obfuscation.py:170` | `def __init__(self)` |
| `__init__` | method | `modules/sleep_obfuscation.py:407` | `def __init__(self, catalog)` |
| `_build_default_catalog` | function | `modules/sleep_obfuscation.py:201` | `def _build_default_catalog()` |
| `catalog` | method | `modules/sleep_obfuscation.py:416` | `def catalog(self)` |
| `config` | method | `modules/sleep_obfuscation.py:421` | `def config(self)` |
| `configure` | method | `modules/sleep_obfuscation.py:449` | `def configure(self, technique, overrides)` |
| `detection_resistance` | method | `modules/sleep_obfuscation.py:426` | `def detection_resistance(self)` |
| `from_dict` | method | `modules/sleep_obfuscation.py:146` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/sleep_obfuscation.py:522` | `def from_dict(cls, raw)` |
| `get` | method | `modules/sleep_obfuscation.py:177` | `def get(self, name)` |
| `list_all` | method | `modules/sleep_obfuscation.py:184` | `def list_all(self)` |
| `list_by_platform` | method | `modules/sleep_obfuscation.py:192` | `def list_by_platform(self, platform)` |
| `list_names` | method | `modules/sleep_obfuscation.py:196` | `def list_names(self)` |
| `recommend` | method | `modules/sleep_obfuscation.py:500` | `def recommend(self, platform)` |
| `register` | method | `modules/sleep_obfuscation.py:173` | `def register(self, technique)` |
| `select` | method | `modules/sleep_obfuscation.py:442` | `def select(self, technique_name)` |
| `to_dict` | method | `modules/sleep_obfuscation.py:129` | `def to_dict(self)` |
| `to_dict` | method | `modules/sleep_obfuscation.py:513` | `def to_dict(self)` |
| `validate` | method | `modules/sleep_obfuscation.py:369` | `def validate(config, technique)` |
| `validate` | method | `modules/sleep_obfuscation.py:484` | `def validate(self, config)` |
| `validate_config` | method | `modules/sleep_obfuscation.py:386` | `def validate_config(config)` |
| `SocksAddressType` | class | `modules/socks_proxy.py:82` | `class SocksAddressType(IntEnum)` |
| `SocksAuthMethod` | class | `modules/socks_proxy.py:65` | `class SocksAuthMethod(IntEnum)` |
| `SocksCommand` | class | `modules/socks_proxy.py:74` | `class SocksCommand(IntEnum)` |
| `SocksProxyConfig` | class | `modules/socks_proxy.py:166` | `class SocksProxyConfig` |
| `SocksProxyEngine` | class | `modules/socks_proxy.py:368` | `class SocksProxyEngine` |
| `SocksReply` | class | `modules/socks_proxy.py:90` | `class SocksReply(IntEnum)` |
| `SocksSession` | class | `modules/socks_proxy.py:120` | `class SocksSession` |
| `SocksValidator` | class | `modules/socks_proxy.py:244` | `class SocksValidator` |
| `__init__` | method | `modules/socks_proxy.py:381` | `def __init__(self, config)` |
| `_check_access_control` | method | `modules/socks_proxy.py:340` | `def _check_access_control(host, port, config)` |
| `_find_oldest_session` | method | `modules/socks_proxy.py:515` | `def _find_oldest_session(self)` |
| `add_bytes` | method | `modules/socks_proxy.py:486` | `def add_bytes(self, session_id, sent, received)` |
| `build_spec` | method | `modules/socks_proxy.py:413` | `def build_spec(self)` |
| `cleanup_expired` | method | `modules/socks_proxy.py:497` | `def cleanup_expired(self)` |
| `config` | method | `modules/socks_proxy.py:387` | `def config(self)` |
| `create_session` | method | `modules/socks_proxy.py:436` | `def create_session(self, session_id, target_host, target_port, beacon_client_id)` |
| `elapsed_seconds` | method | `modules/socks_proxy.py:144` | `def elapsed_seconds(self)` |
| `from_dict` | method | `modules/socks_proxy.py:218` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/socks_proxy.py:522` | `def from_dict(cls, raw)` |
| `from_payload` | method | `modules/socks_proxy.py:528` | `def from_payload(cls, payload)` |
| `get_session` | method | `modules/socks_proxy.py:482` | `def get_session(self, session_id)` |
| `list_sessions` | method | `modules/socks_proxy.py:511` | `def list_sessions(self)` |
| `message` | method | `modules/socks_proxy.py:103` | `def message(self)` |
| `remove_session` | method | `modules/socks_proxy.py:475` | `def remove_session(self, session_id)` |
| `session_count` | method | `modules/socks_proxy.py:397` | `def session_count(self)` |
| `sessions` | method | `modules/socks_proxy.py:392` | `def sessions(self)` |
| `to_dict` | method | `modules/socks_proxy.py:150` | `def to_dict(self)` |
| `to_dict` | method | `modules/socks_proxy.py:199` | `def to_dict(self)` |
| `validate` | method | `modules/socks_proxy.py:401` | `def validate(self, config)` |
| `validate_config` | method | `modules/socks_proxy.py:253` | `def validate_config(config)` |
| `validate_request` | method | `modules/socks_proxy.py:300` | `def validate_request(command, address_type, host, port, config)` |
| `StageDeliveryConfig` | class | `modules/staged_delivery.py:25` | `class StageDeliveryConfig` |
| `StagedDeliveryFactory` | class | `modules/staged_delivery.py:51` | `class StagedDeliveryFactory` |
| `__init__` | method | `modules/staged_delivery.py:83` | `def __init__(self, config, output_dir)` |
| `_build_primary_volume_descriptor` | method | `modules/staged_delivery.py:336` | `def _build_primary_volume_descriptor(self, files)` |
| `_gmail_phish` | method | `modules/staged_delivery.py:504` | `def _gmail_phish(self)` |
| `_obfuscate_powershell` | method | `modules/staged_delivery.py:88` | `def _obfuscate_powershell(self, code)` |
| `_obfuscate_vbscript` | method | `modules/staged_delivery.py:95` | `def _obfuscate_vbscript(self, code)` |
| `_office365_phish` | method | `modules/staged_delivery.py:476` | `def _office365_phish(self)` |
| `_outlook_phish` | method | `modules/staged_delivery.py:532` | `def _outlook_phish(self)` |
| `_payload_command` | method | `modules/staged_delivery.py:102` | `def _payload_command(self)` |
| `generate_all` | method | `modules/staged_delivery.py:420` | `def generate_all(self)` |
| `generate_hta` | method | `modules/staged_delivery.py:134` | `def generate_hta(self)` |
| `generate_iso` | method | `modules/staged_delivery.py:301` | `def generate_iso(self, inner_files)` |
| `generate_lnk` | method | `modules/staged_delivery.py:237` | `def generate_lnk(self)` |
| `generate_phishing_page` | method | `modules/staged_delivery.py:460` | `def generate_phishing_page(self, template)` |
| `generate_vba_macro` | method | `modules/staged_delivery.py:171` | `def generate_vba_macro(self)` |
| `generate_vhd` | method | `modules/staged_delivery.py:370` | `def generate_vhd(self, inner_files)` |
| `generate_xlm_macro` | method | `modules/staged_delivery.py:219` | `def generate_xlm_macro(self)` |
| `HostSummary` | class | `modules/state_manager.py:65` | `class HostSummary` |
| `SessionSnapshot` | class | `modules/state_manager.py:76` | `class SessionSnapshot` |
| `StateManager` | class | `modules/state_manager.py:92` | `class StateManager` |

Next: [SYMBOLS_p23.md](SYMBOLS_p23.md)
