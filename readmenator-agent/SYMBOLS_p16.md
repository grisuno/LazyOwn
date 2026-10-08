# Symbols (page 16 of 35)
Previous: [SYMBOLS_p15.md](SYMBOLS_p15.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `SaaSAttackEngine` | class | `modules/saas_attacks.py:151` | `class SaaSAttackEngine` |
| `SaaSConfig` | class | `modules/saas_attacks.py:48` | `class SaaSConfig` |
| `SaaSEnumerationTools` | class | `modules/saas_attacks.py:70` | `class SaaSEnumerationTools` |
| `__init__` | method | `modules/saas_attacks.py:162` | `def __init__(self, config)` |
| `detect_external_sharing` | method | `modules/saas_attacks.py:311` | `def detect_external_sharing(self)` |
| `enumerate_all` | method | `modules/saas_attacks.py:165` | `def enumerate_all(self)` |
| `google_workspace_commands` | method | `modules/saas_attacks.py:99` | `def google_workspace_commands()` |
| `google_workspace_domain_wide_delegation` | method | `modules/saas_attacks.py:227` | `def google_workspace_domain_wide_delegation(self)` |
| `m365_ews_mail_search` | method | `modules/saas_attacks.py:178` | `def m365_ews_mail_search(self, search_term)` |
| `microsoft365_commands` | method | `modules/saas_attacks.py:74` | `def microsoft365_commands()` |
| `salesforce_commands` | method | `modules/saas_attacks.py:117` | `def salesforce_commands()` |
| `salesforce_report_mining` | method | `modules/saas_attacks.py:256` | `def salesforce_report_mining(self)` |
| `servicenow_commands` | method | `modules/saas_attacks.py:134` | `def servicenow_commands()` |
| `slack_data_mining` | method | `modules/saas_attacks.py:285` | `def slack_data_mining(self)` |
| `summary` | method | `modules/saas_attacks.py:336` | `def summary(self)` |
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
| `build_default_config` | method | `modules/security_sanitizers.py:477` | `def build_default_config(payload)` |
| `file_exists` | method | `modules/security_sanitizers.py:238` | `def file_exists(self, untrusted_name)` |
| `from_payload` | method | `modules/security_sanitizers.py:68` | `def from_payload(cls, payload)` |
| `is_valid_name` | method | `modules/security_sanitizers.py:129` | `def is_valid_name(self, name)` |
| `render` | method | `modules/security_sanitizers.py:359` | `def render(self, template, substitutions, username, password)` |
| `resolve` | method | `modules/security_sanitizers.py:196` | `def resolve(self, untrusted_name)` |
| `resolve` | method | `modules/security_sanitizers.py:298` | `def resolve(self)` |
| `sanitize` | method | `modules/security_sanitizers.py:429` | `def sanitize(self, value)` |
| `sanitize_value` | method | `modules/security_sanitizers.py:139` | `def sanitize_value(self, value)` |
| `_compose_down` | function | `modules/session_cleanup.py:66` | `def _compose_down(compose_file, label)` |
| `_run_quiet` | function | `modules/session_cleanup.py:49` | `def _run_quiet(argv, timeout)` |
| `cleanup_ephemeral_infra` | function | `modules/session_cleanup.py:122` | `def cleanup_ephemeral_infra()` |
| `find_cloudflared_pids` | function | `modules/session_cleanup.py:28` | `def find_cloudflared_pids(ps_output)` |
| `stop_cloudflared_processes` | function | `modules/session_cleanup.py:94` | `def stop_cloudflared_processes()` |
| `SessionRAG` | class | `modules/session_rag.py:181` | `class SessionRAG` |
| `_KeywordFallback` | class | `modules/session_rag.py:96` | `class _KeywordFallback` |
| `_RagState` | class | `modules/session_rag.py:161` | `class _RagState` |
| `__init__` | method | `modules/session_rag.py:104` | `def __init__(self)` |
| `__init__` | method | `modules/session_rag.py:184` | `def __init__(self)` |
| `_chunk_text` | function | `modules/session_rag.py:81` | `def _chunk_text(text, size, overlap)` |
| `_index_file` | method | `modules/session_rag.py:260` | `def _index_file(self, path, collection_key)` |
| `_init_backend` | method | `modules/session_rag.py:195` | `def _init_backend(self)` |
| `_iter_artefacts` | method | `modules/session_rag.py:243` | `def _iter_artefacts(self)` |
| `add` | method | `modules/session_rag.py:129` | `def add(self, doc_id, text, meta)` |
| `context_for_step` | method | `modules/session_rag.py:482` | `def context_for_step(self, phase, target, cmd, n)` |
| `count` | method | `modules/session_rag.py:149` | `def count(self)` |
| `get_rag` | method | `modules/session_rag.py:528` | `def get_rag()` |
| `index_all` | method | `modules/session_rag.py:406` | `def index_all(self)` |
| `index_new` | method | `modules/session_rag.py:296` | `def index_new(self)` |
| `index_parquet_sources` | method | `modules/session_rag.py:317` | `def index_parquet_sources(self, force)` |
| `load` | method | `modules/session_rag.py:108` | `def load(self, path)` |
| `load` | method | `modules/session_rag.py:165` | `def load(cls)` |
| `query` | method | `modules/session_rag.py:139` | `def query(self, query_text, n)` |
| `query` | method | `modules/session_rag.py:434` | `def query(self, query_text, n, collection)` |
| `reset` | method | `modules/session_rag.py:152` | `def reset(self)` |
| `save` | method | `modules/session_rag.py:119` | `def save(self, path)` |
| `save` | method | `modules/session_rag.py:174` | `def save(self)` |
| `stats` | method | `modules/session_rag.py:502` | `def stats(self)` |
| `AbstractReader` | class | `modules/session_reader.py:121` | `class AbstractReader(ABC)` |
| `CampaignTask` | class | `modules/session_reader.py:71` | `class CampaignTask` |
| `CommandOutputReader` | class | `modules/session_reader.py:177` | `class CommandOutputReader(AbstractReader)` |
| `DiscoveredHostReader` | class | `modules/session_reader.py:198` | `class DiscoveredHostReader(AbstractReader)` |
| `ImplantCSVReader` | class | `modules/session_reader.py:132` | `class ImplantCSVReader(AbstractReader)` |
| `ImplantRecord` | class | `modules/session_reader.py:37` | `class ImplantRecord` |
| `SessionAggregator` | class | `modules/session_reader.py:289` | `class SessionAggregator` |
| `SessionSummary` | class | `modules/session_reader.py:81` | `class SessionSummary` |
| `TaskReader` | class | `modules/session_reader.py:216` | `class TaskReader(AbstractReader)` |
| `TaskWriter` | class | `modules/session_reader.py:239` | `class TaskWriter` |
| `__init__` | method | `modules/session_reader.py:242` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/session_reader.py:295` | `def __init__(self, implant_reader, output_reader, host_reader, task_reader)` |
| `active_client_ids` | method | `modules/session_reader.py:89` | `def active_client_ids(self)` |
| `aggregate` | method | `modules/session_reader.py:307` | `def aggregate(self, sessions_dir)` |
| `append` | method | `modules/session_reader.py:245` | `def append(self, title, description, operator, status)` |
| `get_aggregator` | method | `modules/session_reader.py:323` | `def get_aggregator()` |
| `ip_list` | method | `modules/session_reader.py:66` | `def ip_list(self)` |
| `is_privileged` | method | `modules/session_reader.py:52` | `def is_privileged(self)` |
| `latest_for` | method | `modules/session_reader.py:109` | `def latest_for(self, client_id)` |
| `platform` | method | `modules/session_reader.py:57` | `def platform(self)` |
| `privileged_sessions` | method | `modules/session_reader.py:96` | `def privileged_sessions(self)` |
| `read` | method | `modules/session_reader.py:124` | `def read(self, sessions_dir)` |
| `read` | method | `modules/session_reader.py:143` | `def read(self, sessions_dir)` |
| `read` | method | `modules/session_reader.py:183` | `def read(self, sessions_dir)` |
| `read` | method | `modules/session_reader.py:201` | `def read(self, sessions_dir)` |
| `read` | method | `modules/session_reader.py:219` | `def read(self, sessions_dir)` |
| `task_by_status` | method | `modules/session_reader.py:113` | `def task_by_status(self, status)` |
| `unprivileged_sessions` | method | `modules/session_reader.py:103` | `def unprivileged_sessions(self)` |
| `update_status` | method | `modules/session_reader.py:264` | `def update_status(self, task_id, status)` |
| `_detect_phase` | function | `modules/session_state.py:49` | `def _detect_phase(event_types)` |
| `_extract_creds_from_events` | function | `modules/session_state.py:105` | `def _extract_creds_from_events(events)` |
| `_extract_hosts` | function | `modules/session_state.py:119` | `def _extract_hosts(rows, payload)` |
| `_read_events` | function | `modules/session_state.py:81` | `def _read_events(n)` |
| `_read_last_commands` | function | `modules/session_state.py:64` | `def _read_last_commands(n)` |
| `_summarise_commands` | function | `modules/session_state.py:160` | `def _summarise_commands(rows)` |
| `build_state` | function | `modules/session_state.py:173` | `def build_state()` |
| `load` | function | `modules/session_state.py:234` | `def load()` |
| `refresh` | function | `modules/session_state.py:223` | `def refresh()` |
| `OsPlatform` | class | `modules/sleep_obfuscation.py:57` | `class OsPlatform(str, Enum)` |
| `SleepObfuscationConfig` | class | `modules/sleep_obfuscation.py:100` | `class SleepObfuscationConfig` |
| `SleepObfuscationEngine` | class | `modules/sleep_obfuscation.py:400` | `class SleepObfuscationEngine` |
| `SleepTechnique` | class | `modules/sleep_obfuscation.py:73` | `class SleepTechnique` |
| `SleepTechniqueCatalog` | class | `modules/sleep_obfuscation.py:163` | `class SleepTechniqueCatalog` |
| `SleepTechniqueValidator` | class | `modules/sleep_obfuscation.py:367` | `class SleepTechniqueValidator` |
| `TechniqueRisk` | class | `modules/sleep_obfuscation.py:64` | `class TechniqueRisk(str, Enum)` |
| `__init__` | method | `modules/sleep_obfuscation.py:170` | `def __init__(self)` |
| `__init__` | method | `modules/sleep_obfuscation.py:413` | `def __init__(self, catalog)` |
| `_build_default_catalog` | method | `modules/sleep_obfuscation.py:206` | `def _build_default_catalog()` |
| `catalog` | method | `modules/sleep_obfuscation.py:422` | `def catalog(self)` |
| `config` | method | `modules/sleep_obfuscation.py:427` | `def config(self)` |
| `configure` | method | `modules/sleep_obfuscation.py:455` | `def configure(self, technique, overrides)` |
| `detection_resistance` | method | `modules/sleep_obfuscation.py:432` | `def detection_resistance(self)` |
| `from_dict` | method | `modules/sleep_obfuscation.py:146` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/sleep_obfuscation.py:528` | `def from_dict(cls, raw)` |
| `get` | method | `modules/sleep_obfuscation.py:177` | `def get(self, name)` |
| `list_all` | method | `modules/sleep_obfuscation.py:186` | `def list_all(self)` |
| `list_by_platform` | method | `modules/sleep_obfuscation.py:194` | `def list_by_platform(self, platform)` |
| `list_names` | method | `modules/sleep_obfuscation.py:201` | `def list_names(self)` |
| `recommend` | method | `modules/sleep_obfuscation.py:506` | `def recommend(self, platform)` |
| `register` | method | `modules/sleep_obfuscation.py:173` | `def register(self, technique)` |
| `select` | method | `modules/sleep_obfuscation.py:448` | `def select(self, technique_name)` |
| `to_dict` | method | `modules/sleep_obfuscation.py:129` | `def to_dict(self)` |
| `to_dict` | method | `modules/sleep_obfuscation.py:519` | `def to_dict(self)` |
| `validate` | method | `modules/sleep_obfuscation.py:371` | `def validate(config, technique)` |
| `validate` | method | `modules/sleep_obfuscation.py:490` | `def validate(self, config)` |
| `validate_config` | method | `modules/sleep_obfuscation.py:392` | `def validate_config(config)` |
| `SocksAddressType` | class | `modules/socks_proxy.py:82` | `class SocksAddressType(IntEnum)` |
| `SocksAuthMethod` | class | `modules/socks_proxy.py:65` | `class SocksAuthMethod(IntEnum)` |
| `SocksCommand` | class | `modules/socks_proxy.py:74` | `class SocksCommand(IntEnum)` |
| `SocksProxyConfig` | class | `modules/socks_proxy.py:165` | `class SocksProxyConfig` |
| `SocksProxyEngine` | class | `modules/socks_proxy.py:379` | `class SocksProxyEngine` |
| `SocksReply` | class | `modules/socks_proxy.py:90` | `class SocksReply(IntEnum)` |
| `SocksSession` | class | `modules/socks_proxy.py:120` | `class SocksSession` |
| `SocksValidator` | class | `modules/socks_proxy.py:245` | `class SocksValidator` |
| `__init__` | method | `modules/socks_proxy.py:392` | `def __init__(self, config)` |
| `_check_access_control` | method | `modules/socks_proxy.py:351` | `def _check_access_control(host, port, config)` |
| `_find_oldest_session` | method | `modules/socks_proxy.py:521` | `def _find_oldest_session(self)` |
| `add_bytes` | method | `modules/socks_proxy.py:493` | `def add_bytes(self, session_id, sent, received)` |
| `build_spec` | method | `modules/socks_proxy.py:424` | `def build_spec(self)` |
| `cleanup_expired` | method | `modules/socks_proxy.py:503` | `def cleanup_expired(self)` |
| `config` | method | `modules/socks_proxy.py:398` | `def config(self)` |
| `create_session` | method | `modules/socks_proxy.py:447` | `def create_session(self, session_id, target_host, target_port, beacon_client_id)` |
| `elapsed_seconds` | method | `modules/socks_proxy.py:144` | `def elapsed_seconds(self)` |
| `from_dict` | method | `modules/socks_proxy.py:219` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/socks_proxy.py:528` | `def from_dict(cls, raw)` |
| `from_payload` | method | `modules/socks_proxy.py:534` | `def from_payload(cls, payload)` |
| `get_session` | method | `modules/socks_proxy.py:489` | `def get_session(self, session_id)` |
| `list_sessions` | method | `modules/socks_proxy.py:517` | `def list_sessions(self)` |
| `message` | method | `modules/socks_proxy.py:103` | `def message(self)` |
| `remove_session` | method | `modules/socks_proxy.py:482` | `def remove_session(self, session_id)` |
| `session_count` | method | `modules/socks_proxy.py:408` | `def session_count(self)` |
| `sessions` | method | `modules/socks_proxy.py:403` | `def sessions(self)` |
| `to_dict` | method | `modules/socks_proxy.py:149` | `def to_dict(self)` |
| `to_dict` | method | `modules/socks_proxy.py:200` | `def to_dict(self)` |
| `validate` | method | `modules/socks_proxy.py:412` | `def validate(self, config)` |
| `validate_config` | method | `modules/socks_proxy.py:254` | `def validate_config(config)` |
| `validate_request` | method | `modules/socks_proxy.py:311` | `def validate_request(command, address_type, host, port, config)` |
| `StageDeliveryConfig` | class | `modules/staged_delivery.py:25` | `class StageDeliveryConfig` |
| `StagedDeliveryFactory` | class | `modules/staged_delivery.py:51` | `class StagedDeliveryFactory` |
| `__init__` | method | `modules/staged_delivery.py:83` | `def __init__(self, config, output_dir)` |
| `_build_primary_volume_descriptor` | method | `modules/staged_delivery.py:356` | `def _build_primary_volume_descriptor(self, files)` |
| `_gmail_phish` | method | `modules/staged_delivery.py:524` | `def _gmail_phish(self)` |
| `_obfuscate_powershell` | method | `modules/staged_delivery.py:88` | `def _obfuscate_powershell(self, code)` |
| `_obfuscate_vbscript` | method | `modules/staged_delivery.py:97` | `def _obfuscate_vbscript(self, code)` |
| `_office365_phish` | method | `modules/staged_delivery.py:496` | `def _office365_phish(self)` |
| `_outlook_phish` | method | `modules/staged_delivery.py:552` | `def _outlook_phish(self)` |
| `_payload_command` | method | `modules/staged_delivery.py:107` | `def _payload_command(self)` |
| `generate_all` | method | `modules/staged_delivery.py:440` | `def generate_all(self)` |
| `generate_hta` | method | `modules/staged_delivery.py:141` | `def generate_hta(self)` |
| `generate_iso` | method | `modules/staged_delivery.py:321` | `def generate_iso(self, inner_files)` |
| `generate_lnk` | method | `modules/staged_delivery.py:244` | `def generate_lnk(self)` |
| `generate_phishing_page` | method | `modules/staged_delivery.py:480` | `def generate_phishing_page(self, template)` |
| `generate_vba_macro` | method | `modules/staged_delivery.py:178` | `def generate_vba_macro(self)` |
| `generate_vhd` | method | `modules/staged_delivery.py:390` | `def generate_vhd(self, inner_files)` |
| `generate_xlm_macro` | method | `modules/staged_delivery.py:226` | `def generate_xlm_macro(self)` |
| `HostSummary` | class | `modules/state_manager.py:65` | `class HostSummary` |
| `SessionSnapshot` | class | `modules/state_manager.py:76` | `class SessionSnapshot` |
| `StateManager` | class | `modules/state_manager.py:92` | `class StateManager` |
| `__init__` | method | `modules/state_manager.py:107` | `def __init__(self, db_path, sessions_dir, world_model_path, facts_path)` |
| `_cred_list_for_host` | method | `modules/state_manager.py:188` | `def _cred_list_for_host(self, host_id)` |
| `_ensure_workspace` | method | `modules/state_manager.py:150` | `def _ensure_workspace(self)` |
| `_find_host` | method | `modules/state_manager.py:180` | `def _find_host(self, address)` |
| `_load_json` | function | `modules/state_manager.py:43` | `def _load_json(path)` |
| `_publish` | method | `modules/state_manager.py:168` | `def _publish(self, category, event_type, payload)` |
| `_save_json` | function | `modules/state_manager.py:53` | `def _save_json(path, data)` |
| `_sync_world_model_cache` | method | `modules/state_manager.py:481` | `def _sync_world_model_cache(self)` |
| `_vuln_list_for_host` | method | `modules/state_manager.py:193` | `def _vuln_list_for_host(self, host_id)` |
| `add_credential` | method | `modules/state_manager.py:299` | `def add_credential(self, host_address, username, password, realm, cred_type, origin)` |
| `add_host` | method | `modules/state_manager.py:209` | `def add_host(self, address, mac, hostname, os, state)` |
| `add_loot` | method | `modules/state_manager.py:363` | `def add_loot(self, name, loot_type, path, notes, host_address)` |
| `add_note` | method | `modules/state_manager.py:391` | `def add_note(self, data, note_type, host_address)` |
| `add_service` | method | `modules/state_manager.py:266` | `def add_service(self, host_address, port, protocol, name, product, version, state)` |
| `add_vulnerability` | method | `modules/state_manager.py:333` | `def add_vulnerability(self, host_address, name, severity, description, refs)` |
| `advance_host` | method | `modules/state_manager.py:238` | `def advance_host(self, address, new_state)` |
| `close` | method | `modules/state_manager.py:198` | `def close(self)` |
| `db` | method | `modules/state_manager.py:137` | `def db(self)` |
| `delete_host` | method | `modules/state_manager.py:254` | `def delete_host(self, address)` |
| `export_csv` | method | `modules/state_manager.py:648` | `def export_csv(self, table)` |
| `export_summary` | method | `modules/state_manager.py:652` | `def export_summary(self)` |
| `get_host` | method | `modules/state_manager.py:225` | `def get_host(self, address)` |
| `get_state_manager` | method | `modules/state_manager.py:667` | `def get_state_manager()` |
| `get_world_model_cache` | method | `modules/state_manager.py:524` | `def get_world_model_cache(self)` |
| `import_nmap_from_facts` | method | `modules/state_manager.py:424` | `def import_nmap_from_facts(self, facts)` |
| `import_nmap_xml` | method | `modules/state_manager.py:412` | `def import_nmap_xml(self, xml_path)` |
| `instance` | method | `modules/state_manager.py:129` | `def instance(cls)` |
| `list_credentials` | method | `modules/state_manager.py:322` | `def list_credentials(self, host_address)` |
| `list_hosts` | method | `modules/state_manager.py:234` | `def list_hosts(self)` |
| `list_loot` | method | `modules/state_manager.py:385` | `def list_loot(self)` |
| `list_notes` | method | `modules/state_manager.py:406` | `def list_notes(self)` |
| `list_services` | method | `modules/state_manager.py:290` | `def list_services(self, host_address)` |
| `list_vulnerabilities` | method | `modules/state_manager.py:352` | `def list_vulnerabilities(self, host_address, severity)` |
| `load_world_model` | method | `modules/state_manager.py:530` | `def load_world_model(self)` |
| `session_snapshot` | method | `modules/state_manager.py:565` | `def session_snapshot(self)` |
| `set_payload` | method | `modules/state_manager.py:164` | `def set_payload(self, payload)` |
| `status` | method | `modules/state_manager.py:475` | `def status(self)` |
| `workspace_id` | method | `modules/state_manager.py:145` | `def workspace_id(self)` |
| `get_controlling_tty` | function | `modules/sudo_tiocsti.py:44` | `def get_controlling_tty()` |
| `get_sudo_pids_on_tty` | function | `modules/sudo_tiocsti.py:91` | `def get_sudo_pids_on_tty(tty_path)` |
| `inject_byte` | function | `modules/sudo_tiocsti.py:55` | `def inject_byte(fd, byte_char)` |
| `inject_payload` | function | `modules/sudo_tiocsti.py:69` | `def inject_payload(fd, payload, char_delay)` |
| `main` | function | `modules/sudo_tiocsti.py:185` | `def main()` |
| `mode_cache` | function | `modules/sudo_tiocsti.py:173` | `def mode_cache(fd)` |
| `mode_poll` | function | `modules/sudo_tiocsti.py:138` | `def mode_poll(fd, tty_path)` |
| `mode_prefill` | function | `modules/sudo_tiocsti.py:163` | `def mode_prefill(fd)` |
| `sudo_cache_valid` | function | `modules/sudo_tiocsti.py:127` | `def sudo_cache_valid()` |
| `decrypt_cookie` | function | `modules/tel.py:41` | `def decrypt_cookie(encrypted, key, iv)` |
| `get_machine_id` | function | `modules/tel.py:10` | `def get_machine_id()` |
| `get_version` | function | `modules/tel.py:22` | `def get_version()` |
| `main` | function | `modules/tel.py:47` | `def main()` |
| `to_hex` | function | `modules/tel.py:37` | `def to_hex(byte_list)` |
| `to_numbers` | function | `modules/tel.py:33` | `def to_numbers(hex_str)` |
| `ThreatModelBuilder` | class | `modules/threat_model.py:267` | `class ThreatModelBuilder` |
| `_add` | method | `modules/threat_model.py:435` | `def _add(ioc)` |
| `_build_assets` | method | `modules/threat_model.py:318` | `def _build_assets(self, rows)` |
| `_build_detection_rules` | method | `modules/threat_model.py:462` | `def _build_detection_rules(self, ttps)` |
| `_build_iocs` | method | `modules/threat_model.py:431` | `def _build_iocs(self, rows)` |
| `_build_purple_team` | method | `modules/threat_model.py:490` | `def _build_purple_team(self, ttps, detection_rules)` |
| `_build_summary` | method | `modules/threat_model.py:545` | `def _build_summary(self, rows, assets, ttps)` |
| `_build_ttps` | method | `modules/threat_model.py:391` | `def _build_ttps(self, rows)` |
| `_compromise_indicators` | method | `modules/threat_model.py:375` | `def _compromise_indicators(self, commands)` |
| `_extract_iocs` | function | `modules/threat_model.py:245` | `def _extract_iocs(text, first_seen)` |
| `_load_csv` | method | `modules/threat_model.py:305` | `def _load_csv(self)` |
| `_risk_score` | method | `modules/threat_model.py:352` | `def _risk_score(self, commands, ports)` |
| `_save` | method | `modules/threat_model.py:563` | `def _save(self, model)` |
| `build` | method | `modules/threat_model.py:270` | `def build(self)` |
| `get_builder` | method | `modules/threat_model.py:577` | `def get_builder()` |
| `load` | method | `modules/threat_model.py:293` | `def load(self)` |
| `_call_ai` | function | `modules/timeline_narrator.py:94` | `def _call_ai(api_key, events_text, target)` |
| `_format_events_for_prompt` | function | `modules/timeline_narrator.py:75` | `def _format_events_for_prompt(events)` |
| `_load_events` | function | `modules/timeline_narrator.py:56` | `def _load_events(n)` |
| `_write_timeline` | function | `modules/timeline_narrator.py:115` | `def _write_timeline(narrative, event_count, target)` |
| `load_timeline` | function | `modules/timeline_narrator.py:164` | `def load_timeline()` |
| `narrate` | function | `modules/timeline_narrator.py:129` | `def narrate(api_key, force)` |
| `FileTimestamps` | class | `modules/timestomper.py:51` | `class FileTimestamps` |
| `TimestompConfig` | class | `modules/timestomper.py:24` | `class TimestompConfig` |
| `Timestomper` | class | `modules/timestomper.py:69` | `class Timestomper` |
| `__init__` | method | `modules/timestomper.py:106` | `def __init__(self, config)` |
| `_pick_reference` | method | `modules/timestomper.py:269` | `def _pick_reference(self, path, platform)` |
| `generate_random_timestamps` | method | `modules/timestomper.py:280` | `def generate_random_timestamps(self, reference_ts, window_days)` |
| `linux_timestomp_commands` | method | `modules/timestomper.py:200` | `def linux_timestomp_commands(self)` |
| `macos_timestomp_commands` | method | `modules/timestomper.py:241` | `def macos_timestomp_commands(self)` |
| `summary` | method | `modules/timestomper.py:324` | `def summary(self)` |
| `verify_timestamps` | method | `modules/timestomper.py:300` | `def verify_timestamps(self, target_paths)` |
| `windows_timestomp_c` | method | `modules/timestomper.py:152` | `def windows_timestomp_c(self)` |
| `windows_timestomp_powershell` | method | `modules/timestomper.py:110` | `def windows_timestomp_powershell(self)` |
| `extract_tools_from_source` | function | `modules/tool_extractor.py:6` | `def extract_tools_from_source(file_path, class_name, prefix)` |
| `OnlineFeedbackLoop` | class | `modules/toposwarm_bridge.py:266` | `class OnlineFeedbackLoop` |
| `RoutedCall` | class | `modules/toposwarm_bridge.py:68` | `class RoutedCall` |
| `TopoSwarmBridge` | class | `modules/toposwarm_bridge.py:413` | `class TopoSwarmBridge` |
| `__init__` | method | `modules/toposwarm_bridge.py:289` | `def __init__(self, maxsize)` |
| `__init__` | method | `modules/toposwarm_bridge.py:421` | `def __init__(self)` |
| `_hook` | method | `modules/toposwarm_bridge.py:494` | `def _hook(m, i, o)` |
| `_keyword_route` | method | `modules/toposwarm_bridge.py:198` | `def _keyword_route(prompt)` |
| `_load_toposwarm_modules` | method | `modules/toposwarm_bridge.py:234` | `def _load_toposwarm_modules()` |
| `_neural_route` | method | `modules/toposwarm_bridge.py:481` | `def _neural_route(self, prompt)` |
| `_try_load` | method | `modules/toposwarm_bridge.py:441` | `def _try_load(self)` |
| `available` | method | `modules/toposwarm_bridge.py:433` | `def available(self)` |
| `execute_via_orchestrator` | method | `modules/toposwarm_bridge.py:595` | `def execute_via_orchestrator(self, prompt, no_model)` |
| `feedback` | method | `modules/toposwarm_bridge.py:311` | `def feedback(self, result_id, good, comment, routing_head)` |
| `feedback` | method | `modules/toposwarm_bridge.py:544` | `def feedback(self, result_id, good, comment)` |
| `get_bridge` | method | `modules/toposwarm_bridge.py:626` | `def get_bridge()` |
| `lazyown_command` | method | `modules/toposwarm_bridge.py:77` | `def lazyown_command(self)` |
| `load_feedback_for_training` | method | `modules/toposwarm_bridge.py:383` | `def load_feedback_for_training(self)` |
| `model_loaded` | method | `modules/toposwarm_bridge.py:438` | `def model_loaded(self)` |
| `pending_count` | method | `modules/toposwarm_bridge.py:373` | `def pending_count(self)` |
| `register` | method | `modules/toposwarm_bridge.py:296` | `def register(self, result, hidden)` |
| `route` | method | `modules/toposwarm_bridge.py:568` | `def route(self, prompt)` |
| `stats` | method | `modules/toposwarm_bridge.py:376` | `def stats(self)` |
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
| `TTPCoverage` | class | `modules/ttp_coverage.py:65` | `class TTPCoverage` |
| `TTPRow` | class | `modules/ttp_coverage.py:55` | `class TTPRow` |
| `__init__` | method | `modules/ttp_coverage.py:68` | `def __init__(self)` |
| `_blocking_facts` | method | `modules/ttp_coverage.py:165` | `def _blocking_facts(self, tactic)` |
| `_load_state` | method | `modules/ttp_coverage.py:248` | `def _load_state(self)` |
| `_save_state` | method | `modules/ttp_coverage.py:241` | `def _save_state(self)` |
| `add` | method | `modules/ttp_coverage.py:125` | `def add(self, technique_id, name, tactic, status, operation_id)` |
| `compute_ready` | method | `modules/ttp_coverage.py:146` | `def compute_ready(self, available_facts)` |
| `get_coverage` | method | `modules/ttp_coverage.py:260` | `def get_coverage()` |
| `matrix` | method | `modules/ttp_coverage.py:187` | `def matrix(self)` |
| `rebuild_from_operations` | method | `modules/ttp_coverage.py:76` | `def rebuild_from_operations(self)` |
| `status_by_id` | method | `modules/ttp_coverage.py:231` | `def status_by_id(self, technique_id)` |
| `to_dict` | method | `modules/ttp_coverage.py:234` | `def to_dict(self)` |
| `DelegateResult` | class | `modules/unified_bridge.py:52` | `class DelegateResult` |
| `KeywordBackend` | class | `modules/unified_bridge.py:68` | `class KeywordBackend(RouteBackend)` |
| `LazyownBridgeBackend` | class | `modules/unified_bridge.py:116` | `class LazyownBridgeBackend(RouteBackend)` |
| `RouteBackend` | class | `modules/unified_bridge.py:60` | `class RouteBackend(ABC)` |
| `RouteResult` | class | `modules/unified_bridge.py:39` | `class RouteResult` |
| `TopoSwarmBackend` | class | `modules/unified_bridge.py:151` | `class TopoSwarmBackend(RouteBackend)` |
| `UnifiedBridge` | class | `modules/unified_bridge.py:182` | `class UnifiedBridge` |
| `__init__` | method | `modules/unified_bridge.py:201` | `def __init__(self)` |
| `_detect_phase` | method | `modules/unified_bridge.py:338` | `def _detect_phase(self)` |
| `_get_active_target` | method | `modules/unified_bridge.py:346` | `def _get_active_target(self)` |
| `_init_backends` | method | `modules/unified_bridge.py:206` | `def _init_backends(self)` |
| `_publish` | method | `modules/unified_bridge.py:220` | `def _publish(self, category, event_type, payload)` |
| `available` | method | `modules/unified_bridge.py:62` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:95` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:119` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:154` | `def available(self)` |
| `delegate` | method | `modules/unified_bridge.py:280` | `def delegate(self, goal, backend, timeout)` |
| `delegate_task` | method | `modules/unified_bridge.py:360` | `def delegate_task(goal, backend)` |
| `get` | method | `modules/unified_bridge.py:212` | `def get(cls)` |
| `list_backends` | method | `modules/unified_bridge.py:332` | `def list_backends(self)` |
| `route` | method | `modules/unified_bridge.py:65` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:98` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:126` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:162` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:237` | `def route(self, prompt, context)` |
| `route_prompt` | method | `modules/unified_bridge.py:355` | `def route_prompt(prompt, context)` |
| `set_publish_callback` | method | `modules/unified_bridge.py:217` | `def set_publish_callback(self, cb)` |
| `UnifiedDashboard` | class | `modules/unified_dashboard.py:36` | `class UnifiedDashboard` |
| `__init__` | method | `modules/unified_dashboard.py:43` | `def __init__(self, sessions_dir)` |
| `_collect_daemon_status` | method | `modules/unified_dashboard.py:119` | `def _collect_daemon_status(self)` |
| `_collect_dashboard` | method | `modules/unified_dashboard.py:157` | `def _collect_dashboard(self)` |
| `_collect_graph_advice` | method | `modules/unified_dashboard.py:139` | `def _collect_graph_advice(self)` |
| `_collect_hive_status` | method | `modules/unified_dashboard.py:101` | `def _collect_hive_status(self)` |
| `_collect_live_graph` | method | `modules/unified_dashboard.py:128` | `def _collect_live_graph(self)` |
| `_collect_policy_status` | method | `modules/unified_dashboard.py:110` | `def _collect_policy_status(self)` |
| `_collect_world_model` | method | `modules/unified_dashboard.py:92` | `def _collect_world_model(self)` |
| `_get_dashboard` | method | `modules/unified_dashboard.py:48` | `def _get_dashboard(self)` |
| `_get_graph` | method | `modules/unified_dashboard.py:63` | `def _get_graph(self)` |
| `build_unified_snapshot` | method | `modules/unified_dashboard.py:73` | `def build_unified_snapshot(self)` |
| `export_json` | method | `modules/unified_dashboard.py:248` | `def export_json(self)` |
| `get_unified_dashboard` | method | `modules/unified_dashboard.py:253` | `def get_unified_dashboard(sessions_dir)` |
| `render_unified` | method | `modules/unified_dashboard.py:167` | `def render_unified(self)` |
| `GatekeeperStatus` | function | `modules/venator.py:598` | `def GatekeeperStatus(output_file)` |
| `SIPStatus` | function | `modules/venator.py:584` | `def SIPStatus(output_file)` |
| `amzn_canonical_req` | function | `modules/venator.py:795` | `def amzn_canonical_req(filename_path, headers_list)` |
| `amzn_sig` | function | `modules/venator.py:785` | `def amzn_sig(secret_access_key, data, aws_region, aws_service)` |
| `checkSignature` | function | `modules/venator.py:119` | `def checkSignature(file, bundle)` |
| `datetime_handler` | function | `modules/venator.py:186` | `def datetime_handler(x)` |
| `getApps` | function | `modules/venator.py:681` | `def getApps(path, output_file, ignoreVFlag)` |
| `getBashHistory` | function | `modules/venator.py:724` | `def getBashHistory(output_file, users)` |
| `getChromeDownloads` | function | `modules/venator.py:357` | `def getChromeDownloads(chromeHistoryDbPath, output_file)` |
| `getChromeExtensions` | function | `modules/venator.py:327` | `def getChromeExtensions(path, output_file)` |
| `getConnections` | function | `modules/venator.py:557` | `def getConnections(output_file)` |
| `getCronJobs` | function | `modules/venator.py:449` | `def getCronJobs(users, output_file)` |
| `getEmond` | function | `modules/venator.py:465` | `def getEmond(output_file)` |
| `getEnv` | function | `modules/venator.py:527` | `def getEnv(output_file)` |
| `getEventTaps` | function | `modules/venator.py:704` | `def getEventTaps(output_file)` |
| `getFirefoxExtensions` | function | `modules/venator.py:398` | `def getFirefoxExtensions(path, output_file)` |
| `getHash` | function | `modules/venator.py:100` | `def getHash(file, ignoreVFlag)` |
| `getInstallHistory` | function | `modules/venator.py:432` | `def getInstallHistory(output_file)` |
| `getKext` | function | `modules/venator.py:481` | `def getKext(sipStatus, kextPath, output_file, ignoreVFlag)` |
| `getLaunchAgents` | function | `modules/venator.py:261` | `def getLaunchAgents(path, output_file, ignoreVFlag)` |
| `getLaunchDaemons` | function | `modules/venator.py:275` | `def getLaunchDaemons(path, output_file, ignoreVFlag)` |
| `getLoginItems` | function | `modules/venator.py:651` | `def getLoginItems(path, output_file, ignoreVFlag)` |
| `getPeriodicScripts` | function | `modules/venator.py:541` | `def getPeriodicScripts(output_file)` |
| `getSafariExtensions` | function | `modules/venator.py:309` | `def getSafariExtensions(path, output_file)` |
| `getShellStartupScripts` | function | `modules/venator.py:741` | `def getShellStartupScripts(users, output_file)` |
| `getSystemInfo` | function | `modules/venator.py:55` | `def getSystemInfo(output_file)` |
| `getUUID` | function | `modules/venator.py:37` | `def getUUID()` |
| `getUsers` | function | `modules/venator.py:289` | `def getUsers(output_file)` |
| `getVTResult` | function | `modules/venator.py:71` | `def getVTResult(fileHash)` |
| `hmac_sha256` | function | `modules/venator.py:781` | `def hmac_sha256(key, data)` |
| `io_key` | function | `modules/venator.py:45` | `def io_key(keyname)` |
| `parseAgentsDaemons` | function | `modules/venator.py:190` | `def parseAgentsDaemons(item, path)` |
| `parseApp` | function | `modules/venator.py:609` | `def parseApp(app, ignoreVFlag)` |
| `s3_upload` | function | `modules/venator.py:807` | `def s3_upload(data, content_type, filename_path, access_key_id, secret_access_key, s3_bucket, aws_region)` |
| `LazyOwnShellWrapper` | class | `modules/vuln_agent.py:39` | `class LazyOwnShellWrapper` |
| `VulnBotCLI` | class | `modules/vuln_agent.py:121` | `class VulnBotCLI` |
| `__init__` | method | `modules/vuln_agent.py:42` | `def __init__(self, script_path)` |
| `__init__` | method | `modules/vuln_agent.py:122` | `def __init__(self, provider, mode, debug, script_path)` |
| `_load_model` | method | `modules/vuln_agent.py:136` | `def _load_model(self)` |
| `_load_shell_with_deps` | method | `modules/vuln_agent.py:48` | `def _load_shell_with_deps(self)` |
| `_register_fallback_tools` | method | `modules/vuln_agent.py:207` | `def _register_fallback_tools(self)` |
| `_register_pentesting_tools` | method | `modules/vuln_agent.py:179` | `def _register_pentesting_tools(self)` |
| `_setup_agent` | method | `modules/vuln_agent.py:155` | `def _setup_agent(self)` |
| `_stream_response` | method | `modules/vuln_agent.py:279` | `def _stream_response(self, prompt)` |
| `add_to_knowledge_base` | method | `modules/vuln_agent.py:238` | `def add_to_knowledge_base(self, prompt, response)` |
| `configure_logging` | function | `modules/vuln_agent.py:35` | `def configure_logging(debug)` |
| `execute_command` | method | `modules/vuln_agent.py:84` | `def execute_command(self, command)` |
| `generate` | method | `modules/vuln_agent.py:280` | `def generate()` |
| `get_available_commands` | method | `modules/vuln_agent.py:110` | `def get_available_commands(self)` |
| `get_relevant_knowledge` | method | `modules/vuln_agent.py:233` | `def get_relevant_knowledge(self, prompt)` |
| `interactive_mode` | method | `modules/vuln_agent.py:297` | `def interactive_mode(bot)` |
| `load_knowledge_base` | method | `modules/vuln_agent.py:223` | `def load_knowledge_base(self)` |
| `main` | method | `modules/vuln_agent.py:318` | `def main()` |
| `parse_args` | method | `modules/vuln_agent.py:285` | `def parse_args()` |
| `process_with_context` | method | `modules/vuln_agent.py:244` | `def process_with_context(self, file_path, event)` |
| `read_file` | method | `modules/vuln_agent.py:208` | `def read_file(path)` |
| `read_file_content` | method | `modules/vuln_agent.py:213` | `def read_file_content(self, file_path)` |
| `run_cli_command` | method | `modules/vuln_agent.py:188` | `def run_cli_command(command)` |
| `save_knowledge_base` | method | `modules/vuln_agent.py:229` | `def save_knowledge_base(self, kb)` |
| `main` | function | `modules/vuln_bot_cli.py:17` | `def main()` |
| `parse_args` | function | `modules/vuln_bot_cli.py:8` | `def parse_args()` |
| `VulnBotCLI` | class | `modules/vulnbot.py:28` | `class VulnBotCLI` |
| `__init__` | method | `modules/vulnbot.py:29` | `def __init__(self, provider, mode, debug, script_path)` |
| `_load_external_tools` | method | `modules/vulnbot.py:107` | `def _load_external_tools(self, script_path)` |
| `_load_model` | method | `modules/vulnbot.py:44` | `def _load_model(self)` |
| `_register_file_tools` | method | `modules/vulnbot.py:81` | `def _register_file_tools(self)` |
| `_setup_agent` | method | `modules/vulnbot.py:59` | `def _setup_agent(self, script_path)` |
| `_stream_agent_response` | method | `modules/vulnbot.py:133` | `def _stream_agent_response(self, prompt)` |
| `add_to_knowledge_base` | method | `modules/vulnbot.py:207` | `def add_to_knowledge_base(self, prompt, response)` |
| `create_complex_prompt` | method | `modules/vulnbot.py:155` | `def create_complex_prompt(self, base_prompt, history, knowledge)` |
| `edit_file` | method | `modules/vulnbot.py:93` | `def edit_file(path, content, old_text)` |
| `generate` | method | `modules/vulnbot.py:135` | `def generate()` |
| `generate` | method | `modules/vulnbot.py:202` | `def generate()` |
| `get_relevant_knowledge` | method | `modules/vulnbot.py:150` | `def get_relevant_knowledge(self, prompt)` |
| `list_files` | method | `modules/vulnbot.py:84` | `def list_files(directory)` |
| `load_event_config` | method | `modules/vulnbot.py:177` | `def load_event_config(self)` |
| `load_knowledge_base` | method | `modules/vulnbot.py:140` | `def load_knowledge_base(self)` |
| `process_with_context` | method | `modules/vulnbot.py:185` | `def process_with_context(self, file_path, event)` |

Next: [SYMBOLS_p17.md](SYMBOLS_p17.md)
