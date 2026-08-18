"""Autonomous exploitation and LOLBAS command set.

New chingon commands: auto_pwn, rich_tui, lolbas_list, lolbas_use,
exploit_chain, stealth.
"""

from __future__ import annotations

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


class PwnCommandSet(LazyOwnCommandSet):
    """Autonomous exploitation, LOLBAS, and advanced attack commands."""

    phase = "exploit"
    category = "03. Exploitation"

    @cmd2.with_category(exploitation_category)
    def do_auto_pwn(self, line):
        """Run the full autonomous exploitation chain against the target.

        Usage:
            auto_pwn [--pivot] [--privesc] [--stealth low|medium|high|paranoid]

        Executes recon, vulnerability scanning, exploit selection,
        exploitation, optional privilege escalation and auto-pivoting.
        """
        args = line.strip().split()
        enable_pivot = "--pivot" in args
        enable_privesc = "--privesc" in args
        stealth = "low"
        for arg in args:
            if arg.startswith("--stealth="):
                stealth = arg.split("=", 1)[1]
            elif arg == "--stealth":
                idx = args.index("--stealth") + 1
                if idx < len(args):
                    stealth = args[idx]

        try:
            from modules.autonomous_exploit_engine import AutonomousExploitEngine
        except ImportError as exc:
            print_error(f"Failed to load AutonomousExploitEngine: {exc}")
            return

        target = self.params.get("rhost", "")
        if not target:
            print_error("No target set. Use: assign rhost <target_ip>")
            return

        engine = AutonomousExploitEngine()
        engine.enable_stealth(stealth)

        profile = engine.profile(target)
        if not profile.open_ports:
            print_warn(f"No open ports discovered for {target} — running lazynmap first.")
            self.onecmd(f"lazynmap {target}")
            profile = engine.profile(target)
            if not profile.open_ports:
                print_error(f"Still no open ports after scan. Target {target} may be unreachable.")
                return

        print_msg(f"\n[*] Target: {target}  Pivot: {enable_pivot}  PrivEsc: {enable_privesc}  Stealth: {stealth}")

        result = engine.full_auto_pwn(
            target,
            enable_pivot=enable_pivot,
            enable_privesc=enable_privesc,
            stealth=stealth,
        )

        exploits = result.get("exploit_results", [])
        success = [e for e in exploits if e.get("success")]
        shell = [e for e in exploits if e.get("shell_obtained")]
        shell_flag = result.get("shell_obtained", False)
        print_msg(
            f"\n  [+] DONE  exploits={len(exploits)}  success={len(success)}  shells={len(shell)}  shell={'YES' if shell_flag else 'no'}"
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

        resolved_cmd = command.replace("{rhost}", rhost).replace("{lhost}", lhost).replace("{lport}", str(lport))

        print_msg(f"[*] Executing: {resolved_cmd[:200]}")

        import subprocess

        try:
            result = subprocess.run(
                resolved_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(BASE_DIR),
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
