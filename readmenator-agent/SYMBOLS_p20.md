# Symbols (page 20 of 44)
Previous: [SYMBOLS_p19.md](SYMBOLS_p19.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `HIDDEN_FILE6` | macro | `modules/rootkit/mrhyde3.c:40` | `#define HIDDEN_FILE6` |
| `HIDDEN_FILE7` | macro | `modules/rootkit/mrhyde3.c:41` | `#define HIDDEN_FILE7` |
| `HIDDEN_FILE8` | macro | `modules/rootkit/mrhyde3.c:42` | `#define HIDDEN_FILE8` |
| `HIDDEN_FILE9` | macro | `modules/rootkit/mrhyde3.c:43` | `#define HIDDEN_FILE9` |
| `HIDE_DIR` | macro | `modules/rootkit/mrhyde3.c:45` | `#define HIDE_DIR` |
| `HIDE_USER` | macro | `modules/rootkit/mrhyde3.c:46` | `#define HIDE_USER` |
| `IO_URING_BUFFER_SIZE` | macro | `modules/rootkit/mrhyde3.c:51` | `#define IO_URING_BUFFER_SIZE` |
| `IO_URING_QUEUE_DEPTH` | macro | `modules/rootkit/mrhyde3.c:50` | `#define IO_URING_QUEUE_DEPTH` |
| `MAX_HIDE_PIDS` | macro | `modules/rootkit/mrhyde3.c:47` | `#define MAX_HIDE_PIDS` |
| `PATHMRHYDE` | macro | `modules/rootkit/mrhyde3.c:44` | `#define PATHMRHYDE` |
| `PID_FILE_PATH` | macro | `modules/rootkit/mrhyde3.c:48` | `#define PID_FILE_PATH` |
| `_GNU_SOURCE` | macro | `modules/rootkit/mrhyde3.c:7` | `#define _GNU_SOURCE` |
| `__io_uring_enter` | function | `modules/rootkit/mrhyde3.c:76` | `static inline int __io_uring_enter(int fd, unsigned int to_submit, unsigned int min_complete,    ...` |
| `__io_uring_register` | function | `modules/rootkit/mrhyde3.c:80` | `static inline int __io_uring_register(int fd, unsigned int opcode, const void *arg, unsigned int ...` |
| `__io_uring_setup` | function | `modules/rootkit/mrhyde3.c:73` | `static inline int __io_uring_setup(unsigned int entries, struct io_uring_params *p)` |
| `fopen` | function | `modules/rootkit/mrhyde3.c:407` | `FILE *fopen(const char *pathname, const char *mode)` |
| `fstat` | function | `modules/rootkit/mrhyde3.c:535` | `int fstat(int fd, struct stat *statbuf)` |
| `get_username_from_pid` | function | `modules/rootkit/mrhyde3.c:297` | `char* get_username_from_pid(pid_t pid)` |
| `getdents` | function | `modules/rootkit/mrhyde3.c:569` | `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `getdents64` | function | `modules/rootkit/mrhyde3.c:605` | `ssize_t getdents64(int fd, void *dirp, size_t count)` |
| `init_root_ring` | function | `modules/rootkit/mrhyde3.c:176` | `static int init_root_ring(void)` |
| `io_uring` | struct | `modules/rootkit/mrhyde3.c:65` | `` |
| `io_uring_cq` | struct | `modules/rootkit/mrhyde3.c:61` | `` |
| `io_uring_sq` | struct | `modules/rootkit/mrhyde3.c:57` | `` |
| `kill` | function | `modules/rootkit/mrhyde3.c:373` | `int kill(pid_t pid, int sig)` |
| `linux_dirent64` | struct | `modules/rootkit/mrhyde3.c:560` | `` |
| `load_hidden_files` | function | `modules/rootkit/mrhyde3.c:282` | `void load_hidden_files(void)` |
| `load_hidden_pids` | function | `modules/rootkit/mrhyde3.c:268` | `void load_hidden_pids(void)` |
| `lstat` | function | `modules/rootkit/mrhyde3.c:511` | `int lstat(const char *pathname, struct stat *statbuf)` |
| `open` | function | `modules/rootkit/mrhyde3.c:430` | `int open(const char *pathname, int flags, ...)` |
| `openat` | function | `modules/rootkit/mrhyde3.c:458` | `int openat(int dirfd, const char *pathname, int flags, ...)` |
| `original_dirent` | type_alias | `modules/rootkit/mrhyde3.c:312` | `typedef struct dirent original_dirent;` |
| `readdir` | function | `modules/rootkit/mrhyde3.c:336` | `struct dirent* readdir(DIR* dirp)` |
| `remove` | function | `modules/rootkit/mrhyde3.c:383` | `int remove(const char *pathname)` |
| `should_hide_file` | function | `modules/rootkit/mrhyde3.c:329` | `int should_hide_file(const char* filename)` |
| `should_hide_pid` | function | `modules/rootkit/mrhyde3.c:320` | `int should_hide_pid(const char* pid)` |
| `stat` | function | `modules/rootkit/mrhyde3.c:487` | `int stat(const char *pathname, struct stat *statbuf)` |
| `traditional_read_file` | function | `modules/rootkit/mrhyde3.c:253` | `static char *traditional_read_file(const char *path)` |
| `unlink` | function | `modules/rootkit/mrhyde3.c:367` | `int unlink(const char *pathname)` |
| `unlinkat` | function | `modules/rootkit/mrhyde3.c:389` | `int unlinkat(int dirfd, const char *pathname, int flags)` |
| `uring_cqe_seen` | function | `modules/rootkit/mrhyde3.c:163` | `static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe)` |
| `uring_get_sqe` | function | `modules/rootkit/mrhyde3.c:130` | `static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring)` |
| `uring_queue_init` | function | `modules/rootkit/mrhyde3.c:85` | `static int uring_queue_init(unsigned int entries, struct io_uring *ring)` |
| `uring_read_whole_file` | function | `modules/rootkit/mrhyde3.c:197` | `static char *uring_read_whole_file(const char *path)` |
| `uring_submit` | function | `modules/rootkit/mrhyde3.c:141` | `static int uring_submit(struct io_uring *ring)` |
| `uring_wait_cqe_timeout` | function | `modules/rootkit/mrhyde3.c:149` | `static int uring_wait_cqe_timeout(struct io_uring *ring, struct io_uring_cqe **cqe_ptr, int timeo...` |
| `_start` | function | `modules/rootkit/rootkit.asm:4` | `` |
| `HIDDEN_FILE_NAME` | macro | `modules/rootkit/rootkit.c:27` | `#define HIDDEN_FILE_NAME` |
| `HIDDEN_PROCESS_NAME` | macro | `modules/rootkit/rootkit.c:26` | `#define HIDDEN_PROCESS_NAME` |
| `LISTENER_IP` | macro | `modules/rootkit/rootkit.c:28` | `#define LISTENER_IP` |
| `LISTENER_PORT` | macro | `modules/rootkit/rootkit.c:29` | `#define LISTENER_PORT` |
| `SPECIAL_STRING` | macro | `modules/rootkit/rootkit.c:31` | `#define SPECIAL_STRING` |
| `SPECIAL_STRING_PORT` | macro | `modules/rootkit/rootkit.c:34` | `#define SPECIAL_STRING_PORT` |
| `disable_module_signature_verification` | function | `modules/rootkit/rootkit.c:181` | `static void disable_module_signature_verification(void)` |
| `hook_syscalls` | function | `modules/rootkit/rootkit.c:195` | `static int __init hook_syscalls(void)` |
| `hooked_getdents` | function | `modules/rootkit/rootkit.c:75` | `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `hooked_getdents64` | function | `modules/rootkit/rootkit.c:101` | `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `hooked_read` | function | `modules/rootkit/rootkit.c:127` | `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `regs_override_return` | function | `modules/rootkit/rootkit.c:43` | `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` |
| `unhook_syscalls` | function | `modules/rootkit/rootkit.c:208` | `static void __exit unhook_syscalls(void)` |
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
| `apply` | function | `modules/sinks/c2_surfaces.py:11` | `def apply(event)` |
| `apply` | function | `modules/sinks/campaign_db.py:9` | `def apply(event)` |
| `apply` | function | `modules/sinks/event_bus.py:9` | `def apply(event)` |
| `apply` | function | `modules/sinks/intel_graph.py:13` | `def apply(event)` |
| `apply` | function | `modules/sinks/killchain.py:11` | `def apply(event)` |
| `apply` | function | `modules/sinks/objectives.py:16` | `def apply(event)` |
| `apply` | function | `modules/sinks/routing.py:9` | `def apply(event)` |
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
| `__init__` | method | `modules/state_manager.py:107` | `def __init__(self, db_path, sessions_dir, world_model_path, facts_path)` |
| `_cred_list_for_host` | method | `modules/state_manager.py:192` | `def _cred_list_for_host(self, host_id)` |
| `_ensure_workspace` | method | `modules/state_manager.py:151` | `def _ensure_workspace(self)` |
| `_find_host` | method | `modules/state_manager.py:184` | `def _find_host(self, address)` |
| `_load_json` | function | `modules/state_manager.py:43` | `def _load_json(path)` |
| `_publish` | method | `modules/state_manager.py:169` | `def _publish(self, category, event_type, payload)` |
| `_save_json` | function | `modules/state_manager.py:53` | `def _save_json(path, data)` |
| `_sync_world_model_cache` | method | `modules/state_manager.py:556` | `def _sync_world_model_cache(self)` |
| `_vuln_list_for_host` | method | `modules/state_manager.py:197` | `def _vuln_list_for_host(self, host_id)` |
| `add_credential` | method | `modules/state_manager.py:328` | `def add_credential(self, host_address, username, password, realm, cred_type, origin)` |
| `add_host` | method | `modules/state_manager.py:213` | `def add_host(self, address, mac, hostname, os, state)` |
| `add_loot` | method | `modules/state_manager.py:411` | `def add_loot(self, name, loot_type, path, notes, host_address)` |
| `add_note` | method | `modules/state_manager.py:450` | `def add_note(self, data, note_type, host_address)` |
| `add_service` | method | `modules/state_manager.py:287` | `def add_service(self, host_address, port, protocol, name, product, version, state)` |
| `add_vulnerability` | method | `modules/state_manager.py:373` | `def add_vulnerability(self, host_address, name, severity, description, refs)` |
| `advance_host` | method | `modules/state_manager.py:249` | `def advance_host(self, address, new_state)` |
| `close` | method | `modules/state_manager.py:202` | `def close(self)` |
| `db` | method | `modules/state_manager.py:137` | `def db(self)` |
| `delete_host` | method | `modules/state_manager.py:275` | `def delete_host(self, address)` |
| `export_csv` | method | `modules/state_manager.py:757` | `def export_csv(self, table)` |
| `export_summary` | method | `modules/state_manager.py:761` | `def export_summary(self)` |
| `get_host` | method | `modules/state_manager.py:236` | `def get_host(self, address)` |
| `get_state_manager` | function | `modules/state_manager.py:776` | `def get_state_manager()` |
| `get_world_model_cache` | method | `modules/state_manager.py:606` | `def get_world_model_cache(self)` |
| `import_nmap_from_facts` | method | `modules/state_manager.py:495` | `def import_nmap_from_facts(self, facts)` |
| `import_nmap_xml` | method | `modules/state_manager.py:479` | `def import_nmap_xml(self, xml_path)` |
| `instance` | method | `modules/state_manager.py:129` | `def instance(cls)` |
| `list_credentials` | method | `modules/state_manager.py:362` | `def list_credentials(self, host_address)` |
| `list_hosts` | method | `modules/state_manager.py:245` | `def list_hosts(self)` |
| `list_loot` | method | `modules/state_manager.py:444` | `def list_loot(self)` |
| `list_notes` | method | `modules/state_manager.py:473` | `def list_notes(self)` |
| `list_services` | method | `modules/state_manager.py:319` | `def list_services(self, host_address)` |
| `list_vulnerabilities` | method | `modules/state_manager.py:398` | `def list_vulnerabilities(self, host_address, severity)` |
| `load_world_model` | method | `modules/state_manager.py:612` | `def load_world_model(self)` |
| `session_snapshot` | method | `modules/state_manager.py:653` | `def session_snapshot(self)` |
| `set_payload` | method | `modules/state_manager.py:165` | `def set_payload(self, payload)` |
| `status` | method | `modules/state_manager.py:550` | `def status(self)` |
| `workspace_id` | method | `modules/state_manager.py:146` | `def workspace_id(self)` |
| `decode` | function | `modules/stego_video.py:93` | `def decode(stego_video, output_zip)` |
| `default_output` | function | `modules/stego_video.py:113` | `def default_output(zip_path)` |
| `encode` | function | `modules/stego_video.py:75` | `def encode(zip_path, output_video)` |
| `generate_carrier` | function | `modules/stego_video.py:61` | `def generate_carrier(output)` |
| `is_video` | function | `modules/stego_video.py:40` | `def is_video(path)` |
| `is_zip` | function | `modules/stego_video.py:36` | `def is_zip(path)` |
| `load_payload_file` | function | `modules/stego_video.py:26` | `def load_payload_file()` |
| `main` | function | `modules/stego_video.py:118` | `def main(argv)` |
| `prompt_path` | function | `modules/stego_video.py:44` | `def prompt_path(message)` |
| `resolve_path` | function | `modules/stego_video.py:52` | `def resolve_path(arg_path, payload_file, validator, kind)` |
| `get_controlling_tty` | function | `modules/sudo_tiocsti.py:52` | `def get_controlling_tty()` |
| `get_sudo_pids_on_tty` | function | `modules/sudo_tiocsti.py:102` | `def get_sudo_pids_on_tty(tty_path)` |
| `inject_byte` | function | `modules/sudo_tiocsti.py:64` | `def inject_byte(fd, byte_char)` |
| `inject_payload` | function | `modules/sudo_tiocsti.py:79` | `def inject_payload(fd, payload, char_delay)` |
| `main` | function | `modules/sudo_tiocsti.py:198` | `def main()` |
| `mode_cache` | function | `modules/sudo_tiocsti.py:185` | `def mode_cache(fd)` |
| `mode_poll` | function | `modules/sudo_tiocsti.py:149` | `def mode_poll(fd, tty_path)` |
| `mode_prefill` | function | `modules/sudo_tiocsti.py:175` | `def mode_prefill(fd)` |
| `sudo_cache_valid` | function | `modules/sudo_tiocsti.py:139` | `def sudo_cache_valid()` |
| `discovery_targets` | function | `modules/surface_ops.py:31` | `def discovery_targets(sessions_dir)` |
| `is_ipv4` | function | `modules/surface_ops.py:18` | `def is_ipv4(value)` |
| `parse_confirm` | function | `modules/surface_ops.py:26` | `def parse_confirm(answer)` |
| `write_world_model_hosts` | function | `modules/surface_ops.py:50` | `def write_world_model_hosts(document, sessions)` |
| `decrypt_cookie` | function | `modules/tel.py:46` | `def decrypt_cookie(encrypted, key, iv)` |
| `get_machine_id` | function | `modules/tel.py:10` | `def get_machine_id()` |
| `get_version` | function | `modules/tel.py:24` | `def get_version()` |
| `main` | function | `modules/tel.py:53` | `def main()` |
| `to_hex` | function | `modules/tel.py:41` | `def to_hex(byte_list)` |
| `to_numbers` | function | `modules/tel.py:36` | `def to_numbers(hex_str)` |
| `ThreatModelBuilder` | class | `modules/threat_model.py:267` | `class ThreatModelBuilder` |
| `_add` | function | `modules/threat_model.py:448` | `def _add(ioc)` |
| `_build_assets` | method | `modules/threat_model.py:318` | `def _build_assets(self, rows)` |
| `_build_detection_rules` | method | `modules/threat_model.py:475` | `def _build_detection_rules(self, ttps)` |
| `_build_iocs` | method | `modules/threat_model.py:444` | `def _build_iocs(self, rows)` |
| `_build_purple_team` | method | `modules/threat_model.py:505` | `def _build_purple_team(self, ttps, detection_rules)` |
| `_build_summary` | method | `modules/threat_model.py:560` | `def _build_summary(self, rows, assets, ttps)` |
| `_build_ttps` | method | `modules/threat_model.py:404` | `def _build_ttps(self, rows)` |
| `_compromise_indicators` | method | `modules/threat_model.py:388` | `def _compromise_indicators(self, commands)` |
| `_extract_iocs` | function | `modules/threat_model.py:245` | `def _extract_iocs(text, first_seen)` |
| `_load_csv` | method | `modules/threat_model.py:305` | `def _load_csv(self)` |
| `_risk_score` | method | `modules/threat_model.py:352` | `def _risk_score(self, commands, ports)` |
| `_save` | method | `modules/threat_model.py:578` | `def _save(self, model)` |
| `build` | method | `modules/threat_model.py:270` | `def build(self)` |
| `get_builder` | function | `modules/threat_model.py:592` | `def get_builder()` |
| `load` | method | `modules/threat_model.py:293` | `def load(self)` |
| `_call_ai` | function | `modules/timeline_narrator.py:97` | `def _call_ai(api_key, events_text, target)` |
| `_format_events_for_prompt` | function | `modules/timeline_narrator.py:77` | `def _format_events_for_prompt(events)` |
| `_load_events` | function | `modules/timeline_narrator.py:57` | `def _load_events(n)` |
| `_write_timeline` | function | `modules/timeline_narrator.py:115` | `def _write_timeline(narrative, event_count, target)` |
| `load_timeline` | function | `modules/timeline_narrator.py:165` | `def load_timeline()` |
| `narrate` | function | `modules/timeline_narrator.py:130` | `def narrate(api_key, force)` |
| `FileTimestamps` | class | `modules/timestomper.py:51` | `class FileTimestamps` |
| `TimestompConfig` | class | `modules/timestomper.py:24` | `class TimestompConfig` |
| `Timestomper` | class | `modules/timestomper.py:69` | `class Timestomper` |
| `__init__` | method | `modules/timestomper.py:106` | `def __init__(self, config)` |
| `_pick_reference` | method | `modules/timestomper.py:269` | `def _pick_reference(self, path, platform)` |
| `generate_random_timestamps` | method | `modules/timestomper.py:280` | `def generate_random_timestamps(self, reference_ts, window_days)` |
| `linux_timestomp_commands` | method | `modules/timestomper.py:200` | `def linux_timestomp_commands(self)` |
| `macos_timestomp_commands` | method | `modules/timestomper.py:241` | `def macos_timestomp_commands(self)` |
| `summary` | method | `modules/timestomper.py:326` | `def summary(self)` |
| `verify_timestamps` | method | `modules/timestomper.py:300` | `def verify_timestamps(self, target_paths)` |
| `windows_timestomp_c` | method | `modules/timestomper.py:152` | `def windows_timestomp_c(self)` |
| `windows_timestomp_powershell` | method | `modules/timestomper.py:110` | `def windows_timestomp_powershell(self)` |
| `FakeEngine` | class | `modules/tools/loop_smoke.py:31` | `class FakeEngine` |
| `FakeShell` | class | `modules/tools/loop_smoke.py:22` | `class FakeShell` |
| `__init__` | method | `modules/tools/loop_smoke.py:36` | `def __init__(self)` |
| `bind_shell` | method | `modules/tools/loop_smoke.py:44` | `def bind_shell(self, shell)` |
| `create_task` | method | `modules/tools/loop_smoke.py:52` | `def create_task(self, goal, description)` |
| `main` | function | `modules/tools/loop_smoke.py:114` | `def main()` |
| `onecmd_plus_hooks` | method | `modules/tools/loop_smoke.py:25` | `def onecmd_plus_hooks(self, command)` |
| `orchestrate` | method | `modules/tools/loop_smoke.py:56` | `def orchestrate(self)` |
| `run` | function | `modules/tools/loop_smoke.py:77` | `def run()` |
| `set_concurrency` | method | `modules/tools/loop_smoke.py:48` | `def set_concurrency(self, value)` |
| `_drive` | function | `modules/tools/monitor_smoke.py:40` | `def _drive()` |
| `main` | function | `modules/tools/monitor_smoke.py:59` | `def main()` |
| `run` | function | `modules/tools/monitor_smoke.py:20` | `def run()` |
| `ToolSeed` | class | `modules/toolset.py:27` | `class ToolSeed` |
| `builtin_seeds` | function | `modules/toolset.py:35` | `def builtin_seeds()` |
| `extract_tool` | function | `modules/toolset.py:105` | `def extract_tool(command)` |
| `resolve` | function | `modules/toolset.py:72` | `def resolve(agent, tool_key)` |
| `validate_shell` | function | `modules/toolset.py:128` | `def validate_shell(role, command)` |
| `OnlineFeedbackLoop` | class | `modules/toposwarm_bridge.py:273` | `class OnlineFeedbackLoop` |
| `RoutedCall` | class | `modules/toposwarm_bridge.py:71` | `class RoutedCall` |
| `TopoSwarmBridge` | class | `modules/toposwarm_bridge.py:424` | `class TopoSwarmBridge` |
| `__init__` | method | `modules/toposwarm_bridge.py:296` | `def __init__(self, maxsize)` |
| `__init__` | method | `modules/toposwarm_bridge.py:432` | `def __init__(self)` |
| `_hook` | function | `modules/toposwarm_bridge.py:508` | `def _hook(m, i, o)` |
| `_keyword_route` | function | `modules/toposwarm_bridge.py:202` | `def _keyword_route(prompt)` |
| `_load_toposwarm_modules` | function | `modules/toposwarm_bridge.py:241` | `def _load_toposwarm_modules()` |
| `_neural_route` | method | `modules/toposwarm_bridge.py:493` | `def _neural_route(self, prompt)` |
| `_try_load` | method | `modules/toposwarm_bridge.py:452` | `def _try_load(self)` |
| `available` | method | `modules/toposwarm_bridge.py:444` | `def available(self)` |
| `execute_via_orchestrator` | method | `modules/toposwarm_bridge.py:613` | `def execute_via_orchestrator(self, prompt, no_model)` |
| `feedback` | method | `modules/toposwarm_bridge.py:318` | `def feedback(self, result_id, good, comment, routing_head)` |
| `feedback` | method | `modules/toposwarm_bridge.py:562` | `def feedback(self, result_id, good, comment)` |
| `get_bridge` | function | `modules/toposwarm_bridge.py:645` | `def get_bridge()` |
| `lazyown_command` | method | `modules/toposwarm_bridge.py:81` | `def lazyown_command(self)` |
| `load_feedback_for_training` | method | `modules/toposwarm_bridge.py:389` | `def load_feedback_for_training(self)` |
| `model_loaded` | method | `modules/toposwarm_bridge.py:449` | `def model_loaded(self)` |
| `pending_count` | method | `modules/toposwarm_bridge.py:379` | `def pending_count(self)` |
| `register` | method | `modules/toposwarm_bridge.py:303` | `def register(self, result, hidden)` |
| `route` | method | `modules/toposwarm_bridge.py:586` | `def route(self, prompt)` |
| `stats` | method | `modules/toposwarm_bridge.py:382` | `def stats(self)` |
| `TrafficMorpher` | class | `modules/traffic_morpher.py:18` | `class TrafficMorpher` |
| `__init__` | method | `modules/traffic_morpher.py:77` | `def __init__(self)` |
| `generate_beacon_profile` | method | `modules/traffic_morpher.py:270` | `def generate_beacon_profile(self, name, protocol, jitter_pct, user_agent)` |
| `generate_cloudflare_worker_proxy_config` | method | `modules/traffic_morpher.py:205` | `def generate_cloudflare_worker_proxy_config(self, c2_host, c2_port, auth_token)` |
| `generate_dns_tunnel_payload` | method | `modules/traffic_morpher.py:138` | `def generate_dns_tunnel_payload(self, data, domain)` |
| `generate_icmp_exfil_payload` | method | `modules/traffic_morpher.py:164` | `def generate_icmp_exfil_payload(self, data, chunk_size)` |
| `generate_jitter` | method | `modules/traffic_morpher.py:125` | `def generate_jitter(self, base_delay, jitter_pct)` |
| `generate_traffic_padding` | method | `modules/traffic_morpher.py:108` | `def generate_traffic_padding(self, min_bytes, max_bytes)` |
| `generate_websocket_masking` | method | `modules/traffic_morpher.py:190` | `def generate_websocket_masking(self, data)` |
| `get_cdn_fronting_hosts` | method | `modules/traffic_morpher.py:91` | `def get_cdn_fronting_hosts(self, provider, count)` |
| `get_random_http_headers` | method | `modules/traffic_morpher.py:81` | `def get_random_http_headers(self)` |
| `Exchange` | class | `modules/traffic_recorder.py:80` | `class Exchange` |
| `RecorderConfig` | class | `modules/traffic_recorder.py:24` | `class RecorderConfig` |
| `TrafficRecorder` | class | `modules/traffic_recorder.py:91` | `class TrafficRecorder` |
| `__init__` | method | `modules/traffic_recorder.py:94` | `def __init__(self, base_dir)` |
| `_connect` | method | `modules/traffic_recorder.py:132` | `def _connect(self)` |
| `_fts_query` | method | `modules/traffic_recorder.py:375` | `def _fts_query(query)` |
| `_index_fts` | method | `modules/traffic_recorder.py:323` | `def _index_fts(self, exchange_id, req, resp)` |
| `_migrate_fts` | method | `modules/traffic_recorder.py:115` | `def _migrate_fts(self, conn)` |
| `_scan_bodies` | method | `modules/traffic_recorder.py:422` | `def _scan_bodies(self, needle, limit)` |
| `backfill_fts` | method | `modules/traffic_recorder.py:343` | `def backfill_fts(self, batch)` |
| `count` | method | `modules/traffic_recorder.py:317` | `def count(self)` |
| `export_archive` | method | `modules/traffic_recorder.py:451` | `def export_archive(self, path, limit, task)` |
| `gc` | method | `modules/traffic_recorder.py:587` | `def gc(self, older_than_sec)` |
| `get_body` | method | `modules/traffic_recorder.py:275` | `def get_body(self, exchange_id)` |
| `import_archive` | method | `modules/traffic_recorder.py:493` | `def import_archive(self, path)` |
| `import_inbox` | method | `modules/traffic_recorder.py:554` | `def import_inbox(self, inbox_dir)` |
| `latest_rowid` | method | `modules/traffic_recorder.py:247` | `def latest_rowid(self)` |
| `query` | method | `modules/traffic_recorder.py:253` | `def query(self, host, status, limit, offset, task)` |
| `read_body` | method | `modules/traffic_recorder.py:284` | `def read_body(self, exchange_id, part, offset, length)` |
| `record` | method | `modules/traffic_recorder.py:138` | `def record(self, method, url, status, req_body, resp_body, content_type, req_headers, resp_headers, host, port...` |
| `search_body` | method | `modules/traffic_recorder.py:382` | `def search_body(self, query, limit)` |
| `since` | method | `modules/traffic_recorder.py:230` | `def since(self, rowid, limit)` |
| `url_template` | function | `modules/traffic_recorder.py:69` | `def url_template(url)` |
| `TriggerPolicyConfig` | class | `modules/trigger_policy.py:31` | `class TriggerPolicyConfig` |
| `_coerce_every_sec` | function | `modules/trigger_policy.py:79` | `def _coerce_every_sec(value)` |
| `export_store` | function | `modules/trigger_policy.py:171` | `def export_store(task_id)` |
| `read_policy` | function | `modules/trigger_policy.py:120` | `def read_policy(path)` |
| `remove_seed` | function | `modules/trigger_policy.py:185` | `def remove_seed(kind, arg, task_id)` |
| `seed_store` | function | `modules/trigger_policy.py:146` | `def seed_store(policy, store, task_id)` |
| `seeds` | function | `modules/trigger_policy.py:87` | `def seeds(raw)` |
| `validate_triggers` | function | `modules/trigger_policy.py:40` | `def validate_triggers(raw)` |
| `TTPCoverage` | class | `modules/ttp_coverage.py:65` | `class TTPCoverage` |
| `TTPRow` | class | `modules/ttp_coverage.py:55` | `class TTPRow` |
| `__init__` | method | `modules/ttp_coverage.py:68` | `def __init__(self)` |
| `_blocking_facts` | method | `modules/ttp_coverage.py:168` | `def _blocking_facts(self, tactic)` |
| `_load_state` | method | `modules/ttp_coverage.py:248` | `def _load_state(self)` |
| `_save_state` | method | `modules/ttp_coverage.py:241` | `def _save_state(self)` |
| `add` | method | `modules/ttp_coverage.py:125` | `def add(self, technique_id, name, tactic, status, operation_id)` |
| `compute_ready` | method | `modules/ttp_coverage.py:149` | `def compute_ready(self, available_facts)` |
| `get_coverage` | function | `modules/ttp_coverage.py:260` | `def get_coverage()` |
| `matrix` | method | `modules/ttp_coverage.py:190` | `def matrix(self)` |
| `rebuild_from_operations` | method | `modules/ttp_coverage.py:76` | `def rebuild_from_operations(self)` |
| `status_by_id` | method | `modules/ttp_coverage.py:231` | `def status_by_id(self, technique_id)` |
| `to_dict` | method | `modules/ttp_coverage.py:234` | `def to_dict(self)` |
| `_as_list` | function | `modules/ttpscope_bridge.py:460` | `def _as_list(value)` |
| `_cache_dataset_path` | function | `modules/ttpscope_bridge.py:146` | `def _cache_dataset_path()` |
| `_fallback_matrix_bundle` | function | `modules/ttpscope_bridge.py:384` | `def _fallback_matrix_bundle(platform)` |
| `_fallback_matrix_parquet` | function | `modules/ttpscope_bridge.py:453` | `def _fallback_matrix_parquet(platform)` |
| `_fallback_note` | function | `modules/ttpscope_bridge.py:422` | `def _fallback_note(object_id, text)` |
| `_fallback_notes` | function | `modules/ttpscope_bridge.py:442` | `def _fallback_notes(object_id)` |
| `_fallback_search_bundle` | function | `modules/ttpscope_bridge.py:235` | `def _fallback_search_bundle(query, limit)` |
| `_fallback_search_parquet` | function | `modules/ttpscope_bridge.py:282` | `def _fallback_search_parquet(query, limit)` |
| `_fallback_show_bundle` | function | `modules/ttpscope_bridge.py:303` | `def _fallback_show_bundle(object_id)` |
| `_fallback_show_parquet` | function | `modules/ttpscope_bridge.py:350` | `def _fallback_show_parquet(object_id)` |
| `_fallback_sync` | function | `modules/ttpscope_bridge.py:153` | `def _fallback_sync()` |
| `_load_atomic_parquet` | function | `modules/ttpscope_bridge.py:273` | `def _load_atomic_parquet()` |
| `_load_parquet` | function | `modules/ttpscope_bridge.py:259` | `def _load_parquet(name)` |
| `_load_stix_bundle` | function | `modules/ttpscope_bridge.py:193` | `def _load_stix_bundle()` |
| `_notes_dir` | function | `modules/ttpscope_bridge.py:415` | `def _notes_dir()` |
| `_run_ttpscope` | function | `modules/ttpscope_bridge.py:129` | `def _run_ttpscope(args)` |
| `_slug` | function | `modules/ttpscope_bridge.py:123` | `def _slug(text)` |

Next: [SYMBOLS_p21.md](SYMBOLS_p21.md)
