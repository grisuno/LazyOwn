# Symbols (page 21 of 48)
Previous: [SYMBOLS_p20.md](SYMBOLS_p20.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `match` | method | `modules/reactive_engine.py:349` | `def match(self, output, context)` |
| `suggest` | method | `modules/reactive_engine.py:504` | `def suggest(self, signals, platform)` |
| `suggest` | method | `modules/reactive_engine.py:565` | `def suggest(self, signals, platform, parquet)` |
| `suggest` | method | `modules/reactive_engine.py:734` | `def suggest(self, output, command, platform, context)` |
| `technique_commands_for` | method | `modules/reactive_engine.py:448` | `def technique_commands_for(self, platform, keyword)` |
| `top_decision` | method | `modules/reactive_engine.py:958` | `def top_decision(self, output, command, platform, context)` |
| `_build_user_prompt` | function | `modules/recommender.py:55` | `def _build_user_prompt(state)` |
| `_call_ai` | function | `modules/recommender.py:97` | `def _call_ai(api_key, user_prompt)` |
| `recommend` | function | `modules/recommender.py:143` | `def recommend(state, api_key)` |
| `recommend_and_save` | function | `modules/recommender.py:163` | `def recommend_and_save(api_key)` |
| `GymAttempt` | class | `modules/redteam_gym.py:319` | `class GymAttempt` |
| `_award_gym_elo` | function | `modules/redteam_gym.py:1014` | `def _award_gym_elo(username, elo_bonus)` |
| `_calc_speed_score` | function | `modules/redteam_gym.py:911` | `def _calc_speed_score(elapsed_seconds, max_bonus)` |
| `_calc_stealth_score` | function | `modules/redteam_gym.py:932` | `def _calc_stealth_score(techniques, max_bonus)` |
| `_calc_technique_score` | function | `modules/redteam_gym.py:948` | `def _calc_technique_score(techniques, chal, max_bonus)` |
| `_ensure_gym_dir` | function | `modules/redteam_gym.py:335` | `def _ensure_gym_dir()` |
| `_get_rank` | function | `modules/redteam_gym.py:1040` | `def _get_rank(username)` |
| `_get_username` | function | `modules/redteam_gym.py:367` | `def _get_username()` |
| `_load_leaderboard` | function | `modules/redteam_gym.py:340` | `def _load_leaderboard()` |
| `_resolve_active_run` | function | `modules/redteam_gym.py:477` | `def _resolve_active_run(selector, operator)` |
| `_same_engagement` | function | `modules/redteam_gym.py:811` | `def _same_engagement(ip, target)` |
| `_save_leaderboard` | function | `modules/redteam_gym.py:356` | `def _save_leaderboard(board)` |
| `_spin_scenario` | function | `modules/redteam_gym.py:603` | `def _spin_scenario(scenario, notify)` |
| `_teardown_stopped_scenarios` | function | `modules/redteam_gym.py:777` | `def _teardown_stopped_scenarios(stopped)` |
| `_update_leaderboard` | function | `modules/redteam_gym.py:970` | `def _update_leaderboard(attempt)` |
| `create_gym` | function | `modules/redteam_gym.py:399` | `def create_gym(gym_id)` |
| `definition_rows` | function | `modules/redteam_gym.py:394` | `def definition_rows()` |
| `delete_gym` | function | `modules/redteam_gym.py:446` | `def delete_gym(gym_id)` |
| `engagement_context` | function | `modules/redteam_gym.py:838` | `def engagement_context(target)` |
| `get_active_challenge` | function | `modules/redteam_gym.py:1084` | `def get_active_challenge(run_id)` |
| `get_active_challenges` | function | `modules/redteam_gym.py:898` | `def get_active_challenges()` |
| `list_challenges` | function | `modules/redteam_gym.py:454` | `def list_challenges()` |
| `main` | function | `modules/redteam_gym.py:1169` | `def main()` |
| `record_external_attempt` | function | `modules/redteam_gym.py:1115` | `def record_external_attempt(challenge_id, success, elo_bonus, techniques)` |
| `reload_challenge_definitions` | function | `modules/redteam_gym.py:300` | `def reload_challenge_definitions(directory)` |
| `save_gym_yaml` | function | `modules/redteam_gym.py:436` | `def save_gym_yaml(gym_id, text)` |
| `show_leaderboard` | function | `modules/redteam_gym.py:1057` | `def show_leaderboard(top_n)` |
| `start_challenge` | function | `modules/redteam_gym.py:495` | `def start_challenge(challenge_id, target, spin_lab, notify)` |
| `stop_challenges` | function | `modules/redteam_gym.py:756` | `def stop_challenges(selector)` |
| `submit_challenge` | function | `modules/redteam_gym.py:648` | `def submit_challenge(techniques_used, success, run_id)` |
| `DataDirectory` | class | `modules/reflective_dll.py:70` | `class DataDirectory` |
| `ImportDescriptor` | class | `modules/reflective_dll.py:104` | `class ImportDescriptor` |
| `PEHeader` | class | `modules/reflective_dll.py:37` | `class PEHeader` |
| `PEParser` | class | `modules/reflective_dll.py:142` | `class PEParser` |
| `ReflectiveLoader` | class | `modules/reflective_dll.py:464` | `class ReflectiveLoader` |
| `ReflectiveLoaderConfig` | class | `modules/reflective_dll.py:121` | `class ReflectiveLoaderConfig` |
| `SectionHeader` | class | `modules/reflective_dll.py:83` | `class SectionHeader` |
| `__init__` | method | `modules/reflective_dll.py:151` | `def __init__(self, pe_data)` |
| `__init__` | method | `modules/reflective_dll.py:492` | `def __init__(self, pe_data, config)` |
| `_parse_thunk_names` | method | `modules/reflective_dll.py:426` | `def _parse_thunk_names(self, thunk_rva, sections)` |
| `_read_asciiz_at_rva` | method | `modules/reflective_dll.py:417` | `def _read_asciiz_at_rva(self, rva, sections)` |
| `architecture` | method | `modules/reflective_dll.py:510` | `def architecture(self)` |
| `generate_c_stub` | method | `modules/reflective_dll.py:588` | `def generate_c_stub(self)` |
| `generate_powershell_stub` | method | `modules/reflective_dll.py:666` | `def generate_powershell_stub(self)` |
| `is_64bit` | method | `modules/reflective_dll.py:456` | `def is_64bit(self)` |
| `parse_data_directories` | method | `modules/reflective_dll.py:243` | `def parse_data_directories(self, num_entries)` |
| `parse_exports` | method | `modules/reflective_dll.py:374` | `def parse_exports(self, export_dir, sections)` |
| `parse_file_header` | method | `modules/reflective_dll.py:166` | `def parse_file_header(self)` |
| `parse_imports` | method | `modules/reflective_dll.py:280` | `def parse_imports(self, import_dir, sections)` |
| `parse_relocations` | method | `modules/reflective_dll.py:326` | `def parse_relocations(self, reloc_dir, sections)` |
| `parse_sections` | method | `modules/reflective_dll.py:208` | `def parse_sections(self, num_sections)` |
| `plan_injection` | method | `modules/reflective_dll.py:526` | `def plan_injection(self)` |
| `raw_data` | method | `modules/reflective_dll.py:460` | `def raw_data(self)` |
| `required_imports` | method | `modules/reflective_dll.py:515` | `def required_imports(self)` |
| `rva_to_offset` | method | `modules/reflective_dll.py:265` | `def rva_to_offset(self, rva, sections)` |
| `sha256` | method | `modules/reflective_dll.py:505` | `def sha256(self)` |
| `summarize` | method | `modules/reflective_dll.py:685` | `def summarize(self)` |
| `ResourceScriptEngine` | class | `modules/resource_script.py:268` | `class ResourceScriptEngine` |
| `ScriptContext` | class | `modules/resource_script.py:82` | `class ScriptContext` |
| `ScriptError` | class | `modules/resource_script.py:76` | `class ScriptError(RuntimeError)` |
| `__init__` | method | `modules/resource_script.py:89` | `def __init__(self, shell_params, on_command, on_print)` |
| `__init__` | method | `modules/resource_script.py:276` | `def __init__(self, context)` |
| `_call_macro` | method | `modules/resource_script.py:537` | `def _call_macro(self, name, args)` |
| `_compare` | method | `modules/resource_script.py:220` | `def _compare(left, op, right)` |
| `_execute_line` | method | `modules/resource_script.py:347` | `def _execute_line(self, raw)` |
| `_extract_macros` | method | `modules/resource_script.py:331` | `def _extract_macros(self, lines)` |
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

Next: [SYMBOLS_p22.md](SYMBOLS_p22.md)
