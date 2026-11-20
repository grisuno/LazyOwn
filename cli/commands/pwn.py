"""Autonomous exploitation and LOLBAS command set.

New chingon commands: auto_pwn, rich_tui, lolbas_list, lolbas_use,
exploit_chain, stealth.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    exploitation_category,
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
PLUGINS_DIR = BASE_DIR / "plugins"

_STALE_PROBE_TIMEOUT_SEC = 2.0
_STALE_ANSWER_RATIO = 0.5
_STEALTH_LEVELS = ("low", "medium", "high", "paranoid")


def refresh_stale_profile(target: str, ports: list[int], onecmd) -> bool:
    """Verify the cached attack surface is live, rescanning when it is not.

    Docker reuses bridge IPs, so a world-model host can carry the services
    of a container that no longer holds the address. Every cached port is
    probed with a TCP connect; when fewer than half answer the profile is
    stale: a fresh scan runs and the world-model host is rebuilt from it,
    so the exploit budget is not burned on phantom ports.

    Args:
        target: Target IP the cached profile belongs to.
        ports: Cached open ports from the current profile.
        onecmd: Callable executing one shell command (``onecmd``).

    Returns:
        ``True`` when the profile was verified or refreshed, ``False``
        when no fresh scan data could be obtained.
    """
    from modules import loop_preflight
    from modules.nmap_fingerprint import find_nmap_xml, parse_nmap_xml
    from modules.world_model import get_world_model

    try:
        live = loop_preflight.probe_tcp(target, ports=ports, timeout=_STALE_PROBE_TIMEOUT_SEC)
    except Exception:
        live = []
    if live and len(live) >= max(1, int(len(ports) * _STALE_ANSWER_RATIO)):
        return True
    if live:
        print_warn(
            f"[coverage] only {len(live)}/{len(ports)} cached port(s) answer for {target} "
            "(stale world model or reused Docker IP) — rescanning."
        )
    else:
        print_warn(
            f"[coverage] cached profile lists {len(ports)} port(s) for {target} but none answer "
            "(stale world model or reused Docker IP) — rescanning."
        )
    onecmd(f"lazynmap {target}")

    xml_files = find_nmap_xml(target, sessions_dir=str(SESSIONS_DIR))
    services = parse_nmap_xml(xml_files[0]) if xml_files else []
    if not services:
        print_error(f"No fresh scan data for {target}; profile stays stale.")
        return False

    world = get_world_model()
    world.reset_host(target)
    for svc in services:
        world.add_service(target, port=svc.port, name=svc.name, version=svc.version, protocol=svc.protocol)
    print_msg(f"[coverage] profile refreshed from scan: {len(services)} open service(s) on {target}")
    return True


def _as_bool(raw) -> bool:
    """Coerce a payload value into a boolean flag.

    Args:
        raw: Payload value (bool, int or string).

    Returns:
        ``True`` for truthy boolean spellings, ``False`` otherwise.
    """
    if isinstance(raw, bool):
        return raw
    return str(raw).strip().lower() in ("true", "yes", "on", "1")


def load_fresh_payload() -> dict:
    """Load payload.json straight from disk (operator edits apply at once).

    The live shell ``params`` dict can lag behind an orchestrator save, so
    auto_pwn defaults are resolved against the file itself.

    Returns:
        The current payload mapping (empty when unreadable).
    """
    try:
        from core.config import load_payload

        return dict(load_payload() or {})
    except Exception:
        return {}


def resolve_auto_pwn_defaults(params: dict) -> dict:
    """Resolve auto_pwn run defaults from the payload configuration.

    Args:
        params: Live payload params (``payload.json`` view).

    Returns:
        Mapping with ``pivot``, ``privesc``, ``cover_all`` and ``stealth``
        defaults; ``stealth`` falls back to ``low`` on unknown values.
    """
    stealth = str(params.get("auto_pwn_stealth", "") or "low").strip().lower()
    if stealth not in _STEALTH_LEVELS:
        stealth = "low"
    return {
        "pivot": _as_bool(params.get("auto_pwn_enable_pivot", False)),
        "privesc": _as_bool(params.get("auto_pwn_enable_privesc", False)),
        "cover_all": _as_bool(params.get("auto_pwn_cover_all", False)),
        "stealth": stealth,
    }


class PwnCommandSet(LazyOwnCommandSet):
    """Autonomous exploitation, LOLBAS, and advanced attack commands."""

    phase = "exploit"
    category = "03. Exploitation"

    @cmd2.with_category(exploitation_category)
    def do_auto_pwn(self, line):
        """Run the full autonomous exploitation chain against the target.

        Usage:
            auto_pwn [target_ip] [--all] [--pivot] [--privesc] [--stealth low|medium|high|paranoid]

        Executes recon, vulnerability scanning, exploit selection,
        exploitation, optional privilege escalation and auto-pivoting.
        The optional positional target overrides payload ``rhost`` so
        deterministic callers (autonomous loop, chains) can point the
        engine at a scoped host without mutating payload.json. ``--all``
        enables coverage mode: every ranked vector is exploited and
        recorded instead of stopping at the first shell, so a gym run
        exercises all of the target's Metasploitable paths. Flags not
        passed fall back to the payload ``auto_pwn_*`` knobs
        (pivot, privesc, coverage, stealth), editable from the
        lazy_orchestrator Config tab.
        """
        args = line.strip().split()
        target_override = ""
        if args and not args[0].startswith("-"):
            target_override = args.pop(0)
        defaults = resolve_auto_pwn_defaults(load_fresh_payload())
        enable_pivot = "--pivot" in args or defaults["pivot"]
        enable_privesc = "--privesc" in args or defaults["privesc"]
        cover_all = "--all" in args or defaults["cover_all"]
        stealth = ""
        for arg in args:
            if arg.startswith("--stealth="):
                stealth = arg.split("=", 1)[1]
            elif arg == "--stealth":
                idx = args.index("--stealth") + 1
                if idx < len(args):
                    stealth = args[idx]
        if stealth.strip().lower() not in _STEALTH_LEVELS:
            stealth = defaults["stealth"]
        stealth = stealth.strip().lower()

        try:
            from modules.autonomous_exploit_engine import AutonomousExploitEngine
        except ImportError as exc:
            print_error(f"Failed to load AutonomousExploitEngine: {exc}")
            return

        target = target_override or self.params.get("rhost", "")
        if not target:
            print_error("No target set. Use: assign rhost <target_ip> or auto_pwn <target_ip>")
            return

        try:
            from modules import loop_preflight

            lab = loop_preflight.lab_state_for(target)
            if lab and not lab.get("running"):
                scenario = str(lab.get("scenario", ""))
                print_error(
                    f"lab scenario '{scenario}' is DOWN (container {lab.get('container', '')} is stopped); "
                    f"auto_pwn would report success against a dead target"
                )
                print_warn(f"recover with: lab start {scenario}")
                return
            if lab:
                print_msg(f"[*] lab target: scenario '{lab.get('scenario', '')}' is running ({lab.get('ip', '')})")
        except Exception as exc:
            print_warn(f"[!] lab preflight skipped: {exc}")

        engine = AutonomousExploitEngine()
        engine.enable_stealth(stealth)

        profile = engine.profile(target)
        if not profile.open_ports:
            # LAZY coverage parity: never re-scan what sessions/ holds.
            try:
                from modules.enrich import should_rescan as _should_rescan

                _need = _should_rescan("sessions", target)
            except Exception:
                _need = True
            if not _need:
                print_msg(f"[coverage] fresh scan artefact for {target} — reusing, no rescan.")
            else:
                print_warn(f"No open ports discovered for {target} — running lazynmap first.")
                self.onecmd(f"lazynmap {target}")
                profile = engine.profile(target)
            if not profile.open_ports:
                print_error(f"Still no open ports after scan. Target {target} may be unreachable.")
                return
        else:
            try:
                if not refresh_stale_profile(target, list(profile.open_ports), self.onecmd):
                    return
                refreshed = engine.profile(target)
                if refreshed.open_ports:
                    profile = refreshed
            except Exception as exc:
                print_warn(f"[!] stale profile check skipped: {exc}")

        print_msg(f"\n[*] Target: {target}  Pivot: {enable_pivot}  PrivEsc: {enable_privesc}  Stealth: {stealth}")

        result = engine.full_auto_pwn(
            target,
            enable_pivot=enable_pivot,
            enable_privesc=enable_privesc,
            stealth=stealth,
            cover_all=cover_all,
        )

        exploits = result.get("exploit_results", [])
        success = [e for e in exploits if e.get("success")]
        shell = [e for e in exploits if e.get("shell_obtained")]
        shell_flag = result.get("shell_obtained", False)
        if result.get("error"):
            print_error(f"engine error: {result.get('error')}")
        mode = "coverage" if cover_all else "foothold"
        print_msg(
            f"\n  [+] DONE ({mode})  exploits={len(exploits)}  success={len(success)}  shells={len(shell)}  shell={'YES' if shell_flag else 'no'}"
        )
        if not exploits and not result.get("error"):
            print_warn(
                "no vector attempted: re-run with 'auto_pwn' after a fresh scan, "
                "or enable coverage with --all"
            )
        if shell_flag and result.get("best_session_id"):
            print_msg(f"  [+] Session: {result.get('best_session_id')}", flush=True)

    @cmd2.with_category(miscellaneous_category)
    def do_rich_tui(self, line):
        """Launch the Rich-based live dashboard TUI.

        Usage:
            rich_tui [--interval 3]

        Opens a real-time htop-style terminal dashboard showing host
        topology, service status, exploit recommendations, active
        pivots and beacons. Press 'q' to quit.
        """
        try:
            from modules.rich_tui import RichDashboard
        except ImportError as exc:
            print_error(f"Failed to load RichDashboard: {exc}")
            return

        try:
            from modules.dashboard_engine import DashboardEngine
            from modules.exploit_recommender import ExploitRecommender
            from modules.world_model import WorldModel
        except ImportError as exc:
            print_error(f"Failed to load dashboard dependencies: {exc}")
            return

        interval = 3.0
        args = line.strip().split()
        if "--interval" in args:
            idx = args.index("--interval")
            if idx + 1 < len(args):
                try:
                    interval = float(args[idx + 1])
                except ValueError:
                    pass

        wm_path = SESSIONS_DIR / "world_model.json"
        wm = WorldModel(wm_path)

        try:
            from modules.exploit_recommender import ExploitRecommender
        except ImportError:
            pass
        er = ExploitRecommender(wm)
        de = DashboardEngine(wm)
        de.set_exploit_recommender(er)

        dashboard = RichDashboard(de, refresh_interval=interval)
        dashboard.run()

    @cmd2.with_category(exploitation_category)
    def do_exploit_chain(self, line):
        """AI-driven multi-step exploit chaining with fallback strategies.

        Usage:
            exploit_chain <target_ip>

        Uses heuristic reasoning to chain exploits: if one fails,
        the engine analyzes the failure and pivots to an alternative
        strategy automatically.
        """
        try:
            from modules.ai_exploit_chain import AIExploitChainer, ExploitChainContext
            from modules.autonomous_exploit_engine import AutonomousExploitEngine
        except ImportError as exc:
            print_error(f"Failed to load exploit chain modules: {exc}")
            return

        args = line.strip().split()
        target = args[0] if args else self.params.get("rhost", "")
        if not target:
            print_error("Usage: exploit_chain <target_ip>")
            return

        engine = AutonomousExploitEngine()
        profile = engine.profile(target)
        chainer = AIExploitChainer()

        ctx = ExploitChainContext(
            target=target,
            profile=profile,
            attempted=[],
            available_strategies=chainer.build_chain_plan(
                ExploitChainContext(
                    target=target,
                    profile=profile,
                    attempted=[],
                    available_strategies=[],
                    failed_strategies=[],
                    success_strategies=[],
                    current_phase="recon",
                    chain_score=0.0,
                )
            ),
            failed_strategies=[],
            success_strategies=[],
            current_phase="recon",
            chain_score=0.0,
        )

        plan = chainer.build_chain_plan(ctx)
        print_msg(f"[*] AI Exploit Chain plan for {target}:")
        for step in plan:
            print_msg(
                f"    Phase: {step.get('phase', '?')} | Strategy: {step.get('strategy', '?')} | Confidence: {step.get('confidence', 0):.0%}"
            )

        max_steps = min(len(plan), 8)
        for i, step in enumerate(plan[:max_steps]):
            strategy = step.get("strategy", "direct")
            print_msg(f"\n[*] Step {i + 1}/{max_steps}: {strategy}")

            candidate = chainer.reason(ctx)
            if candidate is None:
                print_warn("No more candidates from reasoning engine.")
                break

            result = engine.execute_candidate(candidate, profile)
            ctx.attempted.append(result)

            if result.success:
                ctx.success_strategies.append(strategy)
                ctx.current_phase = "post_exploitation"
                state = "SHELL" if result.shell_obtained else "SUCCESS"
                print_msg(f"    [{state}] {result.output[:200]}")
                if result.shell_obtained:
                    print_msg("[*] Shell obtained! Breaking chain.")
                    break
            else:
                ctx.failed_strategies.append(strategy)
                failure_reason = chainer.evaluate_failure(result)
                print_warn(f"    [FAILED] Reason: {failure_reason}")
                new_info = {"last_error": result.error or result.output[:200]}
                plan = chainer.adapt_chain(ctx, new_info)

        print_msg(f"\n[*] Chain complete. {len(ctx.success_strategies)}/{len(ctx.attempted)} successful.")

    @cmd2.with_category(miscellaneous_category)
    def do_lolbas_list(self, line):
        """List available LOLBAS (Living Off The Land) techniques from plugins.

        Usage:
            lolbas_list [amsi|etw|powershell|dotnet|all]

        Displays evasion and execution techniques that use native OS
        binaries and scripts to bypass security controls.
        """
        filter_cat = line.strip().lower() or "all"

        techniques: list[dict] = []
        if not PLUGINS_DIR.exists():
            print_error(f"Plugins directory not found: {PLUGINS_DIR}")
            return

        import yaml

        for plugin_file in sorted(PLUGINS_DIR.glob("*.yaml")):
            if (
                "bypass" not in plugin_file.stem
                and "obfuscation" not in plugin_file.stem
                and "reflection" not in plugin_file.stem
            ):
                continue
            try:
                data = yaml.safe_load(plugin_file.read_text())
            except Exception:
                continue
            cat = data.get("category", "")
            if filter_cat != "all" and filter_cat not in cat.lower() and filter_cat not in plugin_file.stem.lower():
                continue
            for tech in data.get("techniques", []):
                techniques.append(
                    {
                        "plugin": plugin_file.stem,
                        "name": tech.get("name", ""),
                        "description": tech.get("description", ""),
                        "requires_admin": tech.get("requires_admin", False),
                        "platforms": data.get("platforms", []),
                    }
                )

        if not techniques:
            print_warn(f"No LOLBAS techniques found matching '{filter_cat}'.")
            return

        print_msg(f"LOLBAS Techniques ({len(techniques)} total):\n")
        for t in techniques:
            admin_flag = " [ADMIN]" if t.get("requires_admin") else ""
            platforms = ", ".join(t.get("platforms", []))
            print_msg(f"  [{t['plugin']}] {t['name']}{admin_flag}")
            print_msg(f"    Platforms: {platforms}")
            print_msg(f"    {t['description']}")
            print_msg("")

    @cmd2.with_category(exploitation_category)
    def do_lolbas_use(self, line):
        """Execute a specific LOLBAS technique.

        Usage:
            lolbas_use <plugin>/<technique_name>

        Example: lolbas_use amsi_bypass/amsiInitFailed
        """
        args = line.strip().split()
        if not args:
            print_error("Usage: lolbas_use <plugin>/<technique_name>")
            return

        parts = args[0].split("/")
        if len(parts) != 2:
            print_error("Format: <plugin>/<technique_name>. Example: amsi_bypass/amsiInitFailed")
            return

        plugin_name, technique_name = parts
        plugin_path = PLUGINS_DIR / f"{plugin_name}.yaml"
        if not plugin_path.exists():
            print_error(f"Plugin not found: {plugin_path}")
            return

        import yaml

        try:
            data = yaml.safe_load(plugin_path.read_text())
        except Exception as exc:
            print_error(f"Failed to load plugin: {exc}")
            return

        technique = None
        for t in data.get("techniques", []):
            if t.get("name") == technique_name:
                technique = t
                break

        if technique is None:
            print_error(f"Technique '{technique_name}' not found in {plugin_name}")
            return

        command = technique.get("command", "")
        if not command:
            print_error("No command defined for this technique.")
            return

        print_msg(f"[*] Technique: {technique.get('name')}")
        print_msg(f"    Description: {technique.get('description')}")
        print_msg(f"    Requires admin: {technique.get('requires_admin', False)}")
        print_msg(f"    Command: {command}")
        print_msg("")

        if technique.get("requires_admin"):
            print_warn("This technique requires administrator privileges.")

        rhost = self.params.get("rhost", "")
        lhost = self.params.get("lhost", "")
        lport = self.params.get("lport", "")

        from core.validators import check_lport
        from utils import check_lhost as _check_lhost
        from utils import check_rhost as _check_rhost

        if "{rhost}" in command and not _check_rhost(rhost):
            return
        if "{lhost}" in command and not _check_lhost(lhost):
            return
        if "{lport}" in command and not check_lport(lport):
            return

        resolved_cmd = command.replace("{rhost}", rhost).replace("{lhost}", lhost).replace("{lport}", str(lport))

        print_msg(f"[*] Executing: {resolved_cmd[:200]}")

        from core.safe_exec import safe_run_shell

        try:
            result = safe_run_shell(
                resolved_cmd,
                allow=True,
                reason="pwn plugin technique execution, pipes allowed",
                timeout=30,
            )
            output = result.stdout or result.stderr
            print_msg(output[:2000] if output else "(no output)")
        except subprocess.TimeoutExpired:
            print_warn("Command timed out after 30 seconds.")
        except Exception as exc:
            print_error(f"Execution failed: {exc}")

    @cmd2.with_category(exploitation_category)
    def do_stealth_on(self, line):
        """Enable stealth mode for subsequent operations.

        Usage:
            stealth_on [low|medium|high|paranoid]

        Adds delays between operations, limits concurrency, and applies
        traffic shaping to avoid detection.
        """
        level = line.strip().lower() or "medium"
        if level not in ("low", "medium", "high", "paranoid"):
            print_error(f"Invalid stealth level: {level}. Use: low, medium, high, paranoid")
            return

        self.params["stealth_mode"] = level
        try:
            from modules.autonomous_exploit_engine import AutonomousExploitEngine

            engine = AutonomousExploitEngine.get_instance()
            config = engine.enable_stealth(level)
            print_msg(f"[*] Stealth mode: {level}")
            print_msg(f"    Scan flags: {config.get('nmap_flags', '')}")
            print_msg(f"    Min delay: {config.get('min_delay_s', 0)}s")
            print_msg(f"    Max delay: {config.get('max_delay_s', 0)}s")
        except Exception as exc:
            print_error(f"Failed to enable stealth: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_stealth_off(self, line):
        """Disable stealth mode."""
        self.params["stealth_mode"] = "off"
        try:
            from modules.autonomous_exploit_engine import AutonomousExploitEngine

            engine = AutonomousExploitEngine.get_instance()
            engine.enable_stealth("low")
        except Exception:
            pass
        print_msg("[*] Stealth mode disabled.")


__all__ = ["PwnCommandSet"]
