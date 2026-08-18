"""Automation command set — credential reuse, conditional hooks, operator profiles.

Provides CLI commands for managing the credential reuse engine,
conditional hook rules, and multi-operator profiles.
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.categories import miscellaneous_category


class AutomationCommandSet(LazyOwnCommandSet):
    """Automation & operator workflow commands."""

    phase = "misc"
    category = "12. Automation"

    @cmd2.with_category(miscellaneous_category)
    def do_cred_reuse(self, line: str):
        """Analyze captured credentials and suggest spray targets.

        Usage: cred_reuse [limit=N]
        """
        try:
            from modules.credential_reuse import get_credential_reuse_engine
            from modules.state_manager import StateManager

            limit = 20
            if line:
                for part in line.split():
                    if part.startswith("limit="):
                        try:
                            limit = int(part.split("=")[1])
                        except ValueError:
                            pass

            engine = get_credential_reuse_engine()
            state = StateManager()
            candidates = engine.suggest_from_state_manager(state, limit=limit)

            if not candidates:
                self.print("[*] No credential reuse candidates found.")
                self.print("[*] Capture creds first (lazydump, crackmapexec, cred gather).")
                return

            self.print(engine.get_summary(candidates))

        except Exception as exc:
            self.print(f"[!] cred_reuse failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_cred_mark_failed(self, line: str):
        """Mark a credential as failed against a host.

        Usage: cred_mark_failed <user> <password> <host>
        """
        try:
            parts = line.split()
            if len(parts) < 3:
                self.print("[!] Usage: cred_mark_failed <user> <password> <host>")
                return

            from modules.credential_reuse import get_credential_reuse_engine

            engine = get_credential_reuse_engine()
            engine.mark_failed(parts[0], parts[1], parts[2])
            self.print(f"[+] Marked {parts[0]}:*** as FAILED against {parts[2]}")

        except Exception as exc:
            self.print(f"[!] cred_mark_failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_hooks_list(self, line: str):
        """List all conditional hook rules.

        Usage: hooks_list
        """
        try:
            from modules.conditional_hooks import get_hook_engine

            engine = get_hook_engine()
            rules = engine.list_rules()

            self.print(f"\nConditional Hooks ({len(rules)} rules)\n{'=' * 50}")
            for r in rules:
                status = "ON" if r.get("enabled", True) else "OFF"
                trigger = r["trigger"].get("event", "?")
                actions = len(r.get("actions", []))
                cooldown = r.get("cooldown_seconds", 0)
                self.print(f"  [{status}] {r['name']} | trigger={trigger} | actions={actions} | cooldown={cooldown}s")

        except Exception as exc:
            self.print(f"[!] hooks_list failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_hooks_enable(self, line: str):
        """Enable or disable a hook rule.

        Usage: hooks_enable <rule_name> [on|off]
        """
        try:
            parts = line.split(None, 1)
            if not parts:
                self.print("[!] Usage: hooks_enable <rule_name> [on|off]")
                return

            name = parts[0]
            enabled = True
            if len(parts) > 1 and parts[1].lower() in ("off", "false", "0", "disable"):
                enabled = False

            from modules.conditional_hooks import get_hook_engine

            engine = get_hook_engine()
            if engine.enable_rule(name, enabled):
                self.print(f"[+] Rule '{name}': {'ENABLED' if enabled else 'DISABLED'}")
            else:
                self.print(f"[!] Rule '{name}' not found")

        except Exception as exc:
            self.print(f"[!] hooks_enable failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_hooks_add(self, line: str):
        """Add a new conditional hook rule (JSON string).

        Usage: hooks_add '{"name":"my-rule","trigger":{"event":"beacon_connected"},"actions":[{"type":"run_command","command":"whoami"}]}'
        """
        try:
            import json

            rule_dict = json.loads(line)
            from modules.conditional_hooks import get_hook_engine

            engine = get_hook_engine()
            rule = engine.add_rule(rule_dict)
            self.print(f"[+] Rule '{rule.name}' added")

        except json.JSONDecodeError as exc:
            self.print(f"[!] Invalid JSON: {exc}")
        except Exception as exc:
            self.print(f"[!] hooks_add failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_hooks_remove(self, line: str):
        """Remove a hook rule by name.

        Usage: hooks_remove <rule_name>
        """
        try:
            if not line.strip():
                self.print("[!] Usage: hooks_remove <rule_name>")
                return

            from modules.conditional_hooks import get_hook_engine

            engine = get_hook_engine()
            if engine.remove_rule(line.strip()):
                self.print(f"[+] Rule '{line.strip()}' removed")
            else:
                self.print(f"[!] Rule '{line.strip()}' not found")

        except Exception as exc:
            self.print(f"[!] hooks_remove failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_hooks_fire(self, line: str):
        """Manually fire a hook event for testing.

        Usage: hooks_fire <event_name> [key=value ...]
        """
        try:
            parts = line.split()
            if not parts:
                self.print("[!] Usage: hooks_fire <event_name> [key=value ...]")
                return

            event = parts[0]
            context = {}
            for kv in parts[1:]:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    context[k] = v

            from modules.conditional_hooks import get_hook_engine

            engine = get_hook_engine()
            results = engine.fire(event, context)
            self.print(f"[+] Fired '{event}' -> {len(results)} actions triggered")
            for r in results:
                self.print(f"    {r['rule']}: {r.get('result', r.get('error', 'ok'))}")

        except Exception as exc:
            self.print(f"[!] hooks_fire failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_operators(self, line: str):
        """List all operator profiles.

        Usage: operators
        """
        try:
            from modules.operator_profiles import get_operator_profile_manager

            mgr = get_operator_profile_manager()
            profiles = mgr.list_profiles()

            if not profiles:
                self.print("[*] No operator profiles found.")
                self.print("[*] Use 'operator_create <name>' to create one.")
                return

            self.print(f"\nOperator Profiles ({len(profiles)})\n{'=' * 50}")
            for p in profiles:
                self.print(
                    f"  {p.username} | role={p.role} | lhost={p.lhost} | "
                    f"last={p.last_active[:19] if p.last_active else 'never'}"
                )

        except Exception as exc:
            self.print(f"[!] operators failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_operator_create(self, line: str):
        """Create a new operator profile.

        Usage: operator_create <username> [role=operator] [lhost=IP] [lport=PORT]
        """
        try:
            parts = line.split()
            if not parts:
                self.print("[!] Usage: operator_create <username> [role=operator] [lhost=IP] [lport=PORT]")
                return

            username = parts[0]
            kwargs = {}
            for kv in parts[1:]:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    if k in ("lport", "c2_port", "listener_port"):
                        kwargs[k] = int(v)
                    else:
                        kwargs[k] = v

            from modules.operator_profiles import get_operator_profile_manager

            mgr = get_operator_profile_manager()
            profile = mgr.create_profile(username, display_name=username, **kwargs)
            self.print(f"[+] Created operator profile: {profile.username}")
            self.print(f"    Certificate: {profile.cert_file}")
            self.print(f"    Audit log:   {profile.audit_log}")

        except ValueError as exc:
            self.print(f"[!] {exc}")
        except Exception as exc:
            self.print(f"[!] operator_create failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_operator_load(self, line: str):
        """Load effective config for an operator (team baseline + overrides).

        Usage: operator_load <username>
        """
        try:
            if not line.strip():
                self.print("[!] Usage: operator_load <username>")
                return

            from modules.operator_profiles import get_operator_profile_manager

            mgr = get_operator_profile_manager()
            config = mgr.effective_config(line.strip())

            if config.get("_operator") is None:
                self.print(f"[!] Operator '{line.strip()}' not found")
                return

            self.print(f"\nEffective config for {line.strip()}\n{'=' * 50}")
            key_fields = ["lhost", "lport", "c2_port", "c2_malleable_route", "rhost", "domain", "user_agent_lin"]
            for k in key_fields:
                self.print(f"  {k}: {config.get(k, 'N/A')}")

        except Exception as exc:
            self.print(f"[!] operator_load failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_operator_delete(self, line: str):
        """Delete an operator profile.

        Usage: operator_delete <username>
        """
        try:
            if not line.strip():
                self.print("[!] Usage: operator_delete <username>")
                return

            from modules.operator_profiles import get_operator_profile_manager

            mgr = get_operator_profile_manager()
            if mgr.delete_profile(line.strip()):
                self.print(f"[+] Deleted operator profile: {line.strip()}")
            else:
                self.print(f"[!] Operator '{line.strip()}' not found")

        except Exception as exc:
            self.print(f"[!] operator_delete failed: {exc}")

    @cmd2.with_category(miscellaneous_category)
    def do_hooks(self, line: str):
        """Conditional hooks management — list, enable, disable, add, remove rules.

        Usage: hooks [subcommand] [args]
        Subcommands: list, enable, disable, add, remove, fire
        """
        if not line:
            self.do_hooks_list("")
            return

        parts = line.split(None, 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "list":
            self.do_hooks_list(args)
        elif cmd == "enable":
            self.do_hooks_enable(args)
        elif cmd == "disable":
            self.do_hooks_enable(f"{args} off")
        elif cmd == "add":
            self.do_hooks_add(args)
        elif cmd == "remove":
            self.do_hooks_remove(args)
        elif cmd == "fire":
            self.do_hooks_fire(args)
        else:
            self.print(f"[!] Unknown hooks subcommand: {cmd}")
            self.print("[*] Available: list, enable, disable, add, remove, fire")
