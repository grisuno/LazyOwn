"""WinBox lab CommandSet — VM lifecycle, guest execution and gym matrix.

Bridges the totekuh/winbox platform (isolated Windows vulnerability-research
lab on QEMU/libvirt) into the LazyOwn shell. Every action goes through the
allowlisted, shell-free adapter in :mod:`modules.winbox_gym`; the gym matrix
reuses the shared engine via :mod:`modules.gym_winbox_runner` so scored
captures land in the same CTF/leaderboard pipeline as Metasploitable 2.
"""

from __future__ import annotations

import json
import shlex
import subprocess

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules import winbox_gym
from utils import (
    BLUE,
    CYAN,
    GREEN,
    RED,
    RESET,
    YELLOW,
    exploitation_category,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)

_INTERACTIVE_ACTIONS = ("shell", "ssh", "vnc")
_CONFIRM_TOKENS = ("-y", "--yes", "confirm")

_INTERACTIVE_HINT = {
    "shell": "winbox shell",
    "ssh": "winbox ssh",
    "vnc": "winbox vnc",
}


class WinboxCommandSet(LazyOwnCommandSet):
    """WinBox lab control plane and scored gym matrix."""

    phase = "exploit"
    category = exploitation_category

    @cmd2.with_category(exploitation_category)
    def do_winbox(self, line):
        """Control the WinBox isolated Windows lab from the LazyOwn shell.

        Usage:
            winbox status                     # readiness, VM state, IP
            winbox up                         # FULL bootstrap: deps, ISO, VM build, up, rhost
            winbox setup                      # same bootstrap as up (one command)
            winbox up --os server2025         # bootstrap a different guest OS
            winbox down [--force]             # graceful/hard shutdown
            winbox suspend                    # save VM state to disk
            winbox exec [--timeout S] [--user U --password P] [--bg] [--log] <cmd...>
            winbox shell | ssh | vnc          # interactive passthrough
            winbox tools list | add <files...> | remove <name>
            winbox upload <path> [dst]
            winbox eventlogs [--since S] [--max N] [--log L]
            winbox net status | isolate | connect | unplug
            winbox av status | disable | enable
            winbox applocker status | enable | disable
            winbox snapshot list | create <name> | restore <name>
            winbox resolve [ip]               # bind rhost to the lab VM IP
            winbox gym list | chains | validate | info <id> | chain <id>
            winbox gym plan | run [--only a,b] [--dry-run] | report | verify <id>

        Destructive actions (av/applocker disable, eventlogs clear, net
        unplug, destroy) require an explicit confirm token (-y/--yes).
        The lab VM must stay isolated: never point WinBox at production
        infrastructure.

        Examples:
            winbox status
            winbox exec --timeout 120 whoami
            winbox gym plan --only winbox_system_exec,winbox_smb_enum
        """
        args = shlex.split(line)
        if not args:
            self._overview()
            return
        action = args[0].lower()
        rest = args[1:]
        if action != "status" and not self._bootstrap():
            return
        if action == "status":
            self._status()
        elif action in ("up", "down", "suspend"):
            self._lifecycle(action, rest)
        elif action == "setup":
            self._lab_ready(rest)
        elif action == "exec":
            self._exec(rest)
        elif action in _INTERACTIVE_ACTIONS:
            self._interactive_passthrough(action, rest)
        elif action == "tools":
            self._tools(rest)
        elif action == "upload":
            self._upload(rest)
        elif action == "eventlogs":
            self._eventlogs(rest)
        elif action == "net":
            self._net(rest)
        elif action in ("av", "applocker"):
            self._defense(action, rest)
        elif action == "snapshot":
            self._snapshot(rest)
        elif action == "resolve":
            self._resolve(rest)
        elif action == "gym":
            self._gym(rest)
        else:
            print_error(f"Unknown winbox action: {action}")

    def _overview(self) -> None:
        """Print the action overview and current readiness."""
        print_msg(f"{BLUE}WinBox — isolated Windows vulnerability-research lab{RESET}")
        self._status()
        print_msg(f"  {CYAN}Try:{RESET} winbox status | winbox up | winbox exec whoami | winbox gym list")

    def _bootstrap(self) -> bool:
        """Install the upstream repo and host prereqs when missing.

        Returns:
            True when the winbox binary is available.
        """
        if not winbox_gym.binary_path():
            print_warn("winbox not installed — cloning and pip-installing the upstream lab (one-time)...")
            result = winbox_gym.ensure_installed(self.params)
            if not result.get("success"):
                print_error(result.get("message") or "winbox install failed")
                print_msg("  Manual setup:")
                setup = winbox_gym.check_readiness(self.params).get("setup") or {}
                print_msg(f"    {setup.get('clone', '')}")
                print_msg(f"    {setup.get('install', '')}")
                return False
            if result.get("installed"):
                print_succ(f"winbox installed at {result.get('path')} (run 'winbox up' to build the VM)")
        prereqs = winbox_gym.ensure_prereqs()
        if not prereqs.get("success"):
            print_warn(prereqs.get("message") or "host prerequisites missing")
            return False
        return True

    def _status(self) -> None:
        """Show lab readiness and the live VM state."""
        status = winbox_gym.check_readiness(self.params)
        vm = status.get("vm") or {}
        print("")
        print(f"  {BLUE}WinBox Lab Readiness{RESET}")
        print(f"  {'Ready:':<16} {GREEN + 'YES' if status.get('ready') else RED + 'NO'}{RESET}")
        print(f"  {'Binary:':<16} {status.get('binary') or '-'}")
        print(f"  {'Guest OS:':<16} {status.get('guest_os') or '-'}")
        print(f"  {'Install path:':<16} {status.get('install_path') or '-'}")
        missing = status.get("missing_prereqs") or []
        print(f"  {'Prereqs:':<16} {GREEN + 'ok' if not missing else RED + 'missing ' + ', '.join(missing)}{RESET}")
        print(f"  {'VM built:':<16} {GREEN + 'yes' if status.get('vm_built') else RED + 'no (winbox setup -y)'}{RESET}")
        if vm:
            state = str(vm.get("state") or "-")
            color = GREEN if state and state not in ("off", "shut", "shutoff", "down", "unknown") else YELLOW
            print(f"  {'VM state:':<16} {color}{state or '-'}{RESET}")
            print(f"  {'VM IP:':<16} {vm.get('ip') or '-'}")
        if not status.get("ready"):
            setup = status.get("setup") or {}
            print_warn("  Setup steps:")
            print_msg(f"    {setup.get('packages', '')}")
            print_msg(f"    {setup.get('clone', '')}")
            print_msg(f"    {setup.get('install', '')}")
            print_msg(f"    {setup.get('iso', '')}")
            print_msg(f"    {setup.get('build', '')}")

    def _lifecycle(self, action: str, rest: list[str]) -> None:
        """Start, stop or suspend the lab VM.

        ``up`` is the full bootstrap: it installs the upstream repo and
        host prerequisites, downloads the ISO and builds the VM when
        missing, boots the guest and binds rhost — all idempotent.
        """
        if action == "up":
            self._lab_ready(rest)
            return
        argv = [action] + [str(arg) for arg in rest]
        result = winbox_gym.run_cli(argv, timeout=winbox_gym.CLI_TIMEOUT_SEC)
        if result.get("ok"):
            print_succ(f"winbox {action}: done")
            print_msg((result.get("output") or "").strip()[-400:])
            vm = winbox_gym.vm_status()
            if vm.get("ip"):
                print_msg(f"  {CYAN}VM IP:{RESET} {vm['ip']}")
        else:
            print_error(f"winbox {action} failed (exit {result.get('code')})")
            print_warn((result.get("output") or "").strip()[-400:])

    def _lab_ready(self, rest: list[str]) -> None:
        """Run the idempotent full bootstrap until the lab is attackable."""
        guest_os = ""
        if "--os" in rest:
            index = rest.index("--os")
            if index + 1 < len(rest):
                guest_os = rest[index + 1]
        params = dict(self.params)
        if guest_os:
            from utils import lazyown_set_config

            lazyown_set_config("winbox_os", guest_os)
            params["winbox_os"] = guest_os
        print_msg(f"{BLUE}WinBox bootstrap — binary, prereqs, ISO, VM build, up, resolve{RESET}")

        def _lab_notify(message: str) -> None:
            print(message, flush=True)

        result = winbox_gym.ensure_lab_ready(params, notify=_lab_notify)
        for stage, detail in (result.get("stages") or {}).items():
            output = str((detail or {}).get("output", "") if isinstance(detail, dict) else "").strip()
            if output:
                print_msg(f"  {CYAN}[{stage}]{RESET} {output[-300:]}")
        if result.get("success"):
            print_succ(result.get("message") or "WinBox lab ready")
            return
        message = str(result.get("message") or "")
        stage = str(result.get("stage") or "")
        if message:
            (print_warn if stage == "prereqs" else print_error)(message)
        else:
            print_error(f"WinBox bootstrap stopped at stage: {stage or 'unknown'}")
        print_warn("Fix the failing stage and re-run: winbox up (idempotent)")

    def _exec(self, rest: list[str]) -> None:
        """Run a guest command through the winbox agent."""
        argv = ["exec"]
        timeout = 120
        while rest and rest[0] in ("--timeout", "--user", "--password", "--bg", "--log"):
            flag = rest.pop(0)
            if flag == "--timeout":
                if not rest:
                    print_error("--timeout requires a value")
                    return
                timeout = int(rest.pop(0))
                argv += ["--timeout", str(timeout)]
            elif flag in ("--user", "--password"):
                if not rest:
                    print_error(f"{flag} requires a value")
                    return
                argv += [flag, rest.pop(0)]
            else:
                argv.append(flag)
        if not rest:
            print_error("Usage: winbox exec [--timeout S] <command...>")
            return
        argv += rest
        result = winbox_gym.run_cli(
            argv, timeout=min(winbox_gym.EXE_TIMEOUT_MAX, max(winbox_gym.MIN_TIMEOUT_SEC, timeout + 30))
        )
        if result.get("ok"):
            print_succ("winbox exec: done")
        else:
            print_warn(f"winbox exec exited {result.get('code')}")
        output = (result.get("output") or "").strip()
        if output:
            print_msg(output)

    def _interactive_passthrough(self, action: str, rest: list[str]) -> None:
        """Run one interactive winbox command with the inherited terminal."""
        binary = winbox_gym.binary_path()
        if not binary:
            print_error(f"'{winbox_gym.WINBOX_BIN}' is not installed. Run 'winbox status' for setup guidance.")
            return
        argv = [binary, action] + [str(arg) for arg in rest]
        print_msg(f"{CYAN}Interactive session: {' '.join(argv)}{RESET} (exit to return)")
        try:
            subprocess.run(argv, shell=False, check=False)
        except Exception as exc:
            print_error(f"{action} failed: {exc}")

    def _tools(self, rest: list[str]) -> None:
        """Manage the guest tool directory."""
        if not rest or rest[0].lower() not in ("list", "add", "remove"):
            print_error("Usage: winbox tools list | add <files...> | remove <name>")
            return
        argv = ["tools"] + rest
        result = winbox_gym.run_cli(argv, timeout=winbox_gym.CLI_TIMEOUT_SEC)
        if result.get("ok"):
            print_succ("winbox tools: done")
        print_msg((result.get("output") or "").strip())

    def _upload(self, rest: list[str]) -> None:
        """Stage one file into the guest through VirtIO-FS."""
        if not rest:
            print_error("Usage: winbox upload <path> [dst]")
            return
        result = winbox_gym.run_cli(["upload", *rest], timeout=winbox_gym.CLI_TIMEOUT_SEC)
        if result.get("ok"):
            print_succ("winbox upload: done")
        print_msg((result.get("output") or "").strip())

    def _eventlogs(self, rest: list[str]) -> None:
        """Query guest event logs."""
        result = winbox_gym.run_cli(["eventlogs", *rest], timeout=winbox_gym.CLI_TIMEOUT_SEC)
        if result.get("ok"):
            print_succ("winbox eventlogs: done")
        print_msg((result.get("output") or "").strip())

    def _net(self, rest: list[str]) -> None:
        """Control guest network containment."""
        sub = rest[0].lower() if rest else "status"
        if sub not in ("status", "isolate", "connect", "unplug"):
            print_error("Usage: winbox net status | isolate | connect | unplug")
            return
        if sub == "unplug" and not self._confirmed(rest):
            print_warn("net unplug is a full air-gap — repeat with: winbox net unplug -y")
            return
        result = winbox_gym.run_cli(
            ["net", sub] + rest[1:] if sub != "status" else ["net", "status"], timeout=winbox_gym.CLI_TIMEOUT_SEC
        )
        if result.get("ok"):
            print_succ(f"winbox net {sub}: done")
        print_msg((result.get("output") or "").strip())

    def _defense(self, tool: str, rest: list[str]) -> None:
        """Report or flip Defender/AppLocker posture."""
        sub = rest[0].lower() if rest else "status"
        if sub not in ("status", "enable", "disable"):
            print_error(f"Usage: winbox {tool} status | enable | disable")
            return
        if sub in ("enable", "disable") and not self._confirmed(rest):
            print_warn(f"{tool} {sub} changes guest posture — repeat with: winbox {tool} {sub} -y")
            return
        result = winbox_gym.run_cli(
            [tool, sub] + rest[1:] if sub != "status" else [tool, "status"], timeout=winbox_gym.CLI_TIMEOUT_SEC
        )
        if result.get("ok"):
            print_succ(f"winbox {tool} {sub}: done")
        print_msg((result.get("output") or "").strip())

    def _snapshot(self, rest: list[str]) -> None:
        """List, create or restore lab snapshots."""
        if not rest or rest[0].lower() == "list":
            result = winbox_gym.run_cli(["snapshot"], timeout=winbox_gym.CLI_TIMEOUT_SEC)
        else:
            sub = rest[0].lower()
            if sub == "create":
                if len(rest) < 2:
                    print_error("Usage: winbox snapshot create <name>")
                    return
                result = winbox_gym.run_cli(["snapshot", rest[1]], timeout=winbox_gym.UP_TIMEOUT_SEC)
            elif sub == "restore":
                if len(rest) < 2:
                    print_error("Usage: winbox snapshot restore <name>")
                    return
                result = winbox_gym.run_cli(["restore", rest[1]], timeout=winbox_gym.UP_TIMEOUT_SEC)
            else:
                result = winbox_gym.run_cli(["snapshot", *rest], timeout=winbox_gym.UP_TIMEOUT_SEC)
        if result.get("ok"):
            print_succ("winbox snapshot: done")
        print_msg((result.get("output") or "").strip())

    def _resolve(self, rest: list[str]) -> None:
        """Bind rhost to the lab VM IP."""
        if rest:
            target = rest[0].strip()
            shell = self._resolve_shell()
            if shell is not None:
                shell.onecmd(f"assign rhost {target}")
            print_succ(f"rhost bound to {target}")
            return
        ip = winbox_gym.resolve_target()
        if not ip:
            print_error("VM IP unknown. Is the VM built and running? Try: winbox up")
            return
        print_msg(f"{GREEN}VM IP:{RESET} {ip}")
        shell = self._resolve_shell()
        if shell is not None:
            shell.onecmd(f"assign rhost {ip}")
            print_succ(f"rhost bound to {ip}")

    def _gym(self, rest: list[str]) -> None:
        """WinBox gym matrix: list, validate, plan, run, report."""
        args = rest if rest else ["list"]
        action = args[0].lower()
        if action in ("list", "summary"):
            print(json.dumps(winbox_gym.summary(), indent=2))
            return
        if action == "chains":
            for entry in winbox_gym.vulnerabilities():
                print_msg(f"{entry['id']:<28} {entry['chain']:<34} exploit={entry['exploit']:<28} {entry['severity']}")
            return
        if action == "validate":
            errors = winbox_gym.validate_matrix()
            if errors:
                for error in errors:
                    print_error(error)
                return
            print_succ("WinBox gym matrix is consistent.")
            return
        if action == "info" and len(args) > 1:
            print(json.dumps(winbox_gym.get(args[1]) or {"error": "not found"}, indent=2))
            return
        if action == "chain" and len(args) > 1:
            chain = winbox_gym.chain_for(args[1])
            if chain is None:
                print_error(f"Unknown lab vector: {args[1]}")
                return
            for step in chain.resolve({"target": "TARGET", "lhost": "LHOST", "lport": "4444"}):
                status = "skip" if step["skipped"] else "run"
                print(f"[{status}] {step['run']} {step['reason']}".strip())
            return
        if action in ("plan", "run", "report", "verify"):
            self._gym_matrix(action, args[1:])
            return
        print_error(f"Unknown winbox gym action: {action}")

    def _gym_matrix(self, action: str, rest: list[str]) -> None:
        """Plan, run or report the scored WinBox matrix."""
        from modules import ctf_capture, gym_winbox_runner

        top_k = 0
        if rest and rest[0].isdigit():
            top_k = int(rest.pop(0))
        only_arg = _extract_flag(rest, "only")
        only = [name.strip() for name in (only_arg or "").split(",") if name.strip()] or None
        dry_run = _extract_bool(rest, "dry-run") or action == "plan"
        target = _extract_flag(rest, "target") or str(self.params.get("rhost") or "")
        if action == "plan":
            if not target:
                print_error("Set rhost first: winbox resolve")
                return
            try:
                plan = gym_winbox_runner.plan_matrix(target, only=only, top_k=top_k)
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"{BLUE}WinBox gym plan ({len(plan)} vector(s)){RESET}")
            for idx, item in enumerate(plan, 1):
                print_msg(
                    f"  {CYAN}[{idx}]{RESET} {item['vuln_id']:<28} {item['severity']:<8} "
                    f"{item['chain_name'] or '(no chain)':<34} {item['mitre']}"
                )
            return
        if action == "run":
            if not target:
                print_error("Set rhost first: winbox resolve")
                return
            try:
                result = gym_winbox_runner.run_matrix(
                    target,
                    shell=self._resolve_shell(),
                    dry_run=dry_run,
                    only=only,
                    top_k=top_k,
                    lhost=str(self.params.get("lhost") or ""),
                    lport=str(self.params.get("lport") or ""),
                )
            except ValueError as exc:
                print_error(str(exc))
                return
            if result.get("error"):
                print_error(f"WinBox matrix: {result['error']}")
                return
            label = "DRY-RUN" if dry_run else "MATRIX"
            print_msg(f"{label} {result['target']} stats={result['stats']}")
            for run in result["runs"]:
                status_color = GREEN if run["status"] == "ok" else RED
                print_msg(
                    f"  {status_color}{run['status']:<10}{RESET} {run['vuln_id']:<28} capture={run.get('capture', '-')}"
                )
            return
        if action == "report":
            summary = ctf_capture.summary()
            records = {
                vuln_id: record for vuln_id, record in summary["records"].items() if winbox_gym.get(vuln_id) is not None
            }
            if not records:
                print_msg(f"{YELLOW}No WinBox CTF records yet — run: winbox gym run{RESET}")
                return
            print_msg(f"{BLUE}WinBox CTF captures{RESET}")
            for vuln_id, record in records.items():
                total = len(record.get("checks") or [])
                matched = sum(1 for check in (record.get("checks") or []) if check.get("matched"))
                print_msg(
                    f"  [{record['status']:<8}] {vuln_id:<28} {record['target']:<15} "
                    f"{record['severity']:<8} {matched}/{total} checks"
                )
            return
        if action == "verify":
            if not rest:
                print_error("Usage: winbox gym verify <vuln_id>")
                return
            vuln_id = rest[0]
            path = ctf_capture.record_path(vuln_id)
            if not path.is_file():
                print_error(f"No CTF record for {vuln_id}")
                return
            print(path.read_text()[:2000])

    def _confirmed(self, rest: list[str]) -> bool:
        """Return True when the operator passed an explicit confirm token.

        Args:
            rest: Argument tokens after the action.

        Returns:
            True when any token confirms the destructive action.
        """
        lowered = {str(token).lower() for token in rest}
        return any(token in lowered for token in _CONFIRM_TOKENS)


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract ``--flag <value>`` from tokenised arguments.

    Args:
        args: Tokenised argument list (mutated to remove the pair).
        flag: Flag name without dashes.

    Returns:
        The value or None.
    """
    marker = f"--{flag}"
    try:
        index = args.index(marker)
    except ValueError:
        return None
    if index + 1 < len(args):
        value = args[index + 1]
        args.pop(index)
        args.pop(index)
        return value
    return None


def _extract_bool(args: list[str], flag: str) -> bool:
    """Extract a boolean flag from tokenised arguments.

    Args:
        args: Tokenised argument list.
        flag: Flag name without dashes.

    Returns:
        True when the flag was present.
    """
    marker = f"--{flag}"
    if marker in args:
        args.remove(marker)
        return True
    return False
