from __future__ import annotations

import re


class WorkerGatingMixin:
    """Scope, operating-system and privilege gates for a loop worker.

    Groups the policy decisions a worker makes before a command reaches
    the shell: explicit and lab-default scope enforcement, OS-mismatch
    vetoes, passwordless-sudo skips and whole-command scope checks. Every
    method binds to the host ``Worker`` through ``self`` and uses the
    collaborators set in ``__init__`` (``activity``, ``store``,
    ``task_id``) plus ``_target_for`` and ``_resolved_command``.
    """

    def _scope_allows_target(self, target: str) -> bool:
        """Enforce explicit scope: targets outside scope are blocked."""
        from modules.lazy_loop import scope_allows_target

        allowed, reason = scope_allows_target(self.task_id, self.store, target)
        if allowed:
            return True
        self.activity.emit(self.name, "block", f"scope: {target} {reason}", intent_id=0)
        return False

    def _lab_scope_default(self, target: str) -> bool:
        """Default-deny public targets when no explicit scope is set.

        With no task scope the loop would otherwise touch anything; the
        lab-only fallback keeps autonomous rounds inside loopback and
        RFC1918 space, plus operator-approved allowlist entries.

        Args:
            target: Host or IP the loop wants to touch.

        Returns:
            True when the target is lab-local or explicitly allowed.
        """
        from modules.lazy_loop import scope_allows_target

        allowed, reason = scope_allows_target(self.task_id, self.store, target)
        if allowed:
            return True
        self.activity.emit(
            self.name,
            "block",
            f"scope-lab-default: {target} {reason}",
            intent_id=0,
        )
        return False

    def _os_gate(self, intent, command: str) -> tuple[bool, str]:
        """Block OS-mismatched verbs before they reach the shell.

        A Windows-only verb (a shellcode loader, an AD privesc tool)
        must never fire against an inferred Linux host and vice versa.
        Unknown host OS or ``any`` verbs never block.

        Args:
            intent: Owning intent (for target resolution).
            command: Resolved shell command line.

        Returns:
            ``(allowed, reason)``; reason is empty when allowed.
        """
        try:
            from modules import lazy_osinfer

            target = self._target_for(intent)
            host_os = lazy_osinfer.host_os_for_target(target)
            if host_os not in ("linux", "windows"):
                return True, ""
            allowed, _verb_os, reason = lazy_osinfer.verb_compatible_with_host(command, host_os)
            return allowed, reason
        except Exception:
            return True, ""

    def _learn_os(self, intent, command: str, output: str) -> None:
        """Feed ping/TTL and banner evidence into host OS memory.

        The loop's first step is a ping; its reply's TTL infers the
        target OS which is remembered on the asset graph and world
        model so every later verb choice can read it.

        Args:
            intent: Owning intent (for target resolution).
            command: Executed command line.
            output: Captured stdout/stderr.
        """
        if not output:
            return
        try:
            from modules import lazy_osinfer

            target = self._target_for(intent)
            lowered = command.lower()
            if lowered.startswith("ping") or " ttl=" in output.lower() or "ttl " in output.lower()[:200]:
                lazy_osinfer.learn_from_transcripts(target, [(command, output)])
        except Exception:
            pass

    def _sudo_guard(self, intent, command: str) -> tuple[bool, str]:
        """Skip sudo commands when passwordless sudo is unavailable.

        Returns (True, "") when the command may run; (False, refusal)
        when it must be skipped before executing, so no INFO panel,
        sudo error or post-tool failure ever reaches the operator.
        """
        try:
            from utils import needs_sudo, sudo_available

            resolved = self._resolved_command(command)
            blocked = needs_sudo(resolved) and not sudo_available()
        except Exception:
            return True, ""
        if not blocked:
            return True, ""
        try:
            self.activity.emit(
                self.name,
                "block",
                f"skipped sudo step (passwordless sudo unavailable): {command[:140]}",
                intent_id=intent.node_id,
            )
        except Exception:
            pass
        return False, "sudo-unavailable"

    def _downgrade_privileged(self, command: str, target: str = "") -> tuple[str, str]:
        """Rewrite a root/tty-only verb to its unprivileged fallback when the
        unattended loop cannot elevate.

        ``lazynmap`` and peers run a privileged primitive under sudo; with no
        tty and no passwordless sudo they degrade or hang, so the loop keeps
        re-proposing a verb it can never run. This substitutes an unprivileged
        equivalent (``nmap -sT``) once, so the scan actually runs. Fail-open:
        any error leaves the command unchanged.

        Args:
            command: Proposed command line.
            target: Resolved intent target to aim the fallback.

        Returns:
            ``(command, note)``: unchanged command and empty note when no
            downgrade applies, else the fallback command and a reason.
        """
        try:
            from modules.verb_capabilities import downgrade_for_unattended, requires_privilege
            from utils import sudo_available

            if not requires_privilege(command):
                return command, ""
            if sudo_available():
                return command, ""
            return downgrade_for_unattended(command, target)
        except Exception:
            return command, ""

    def _command_in_scope(self, command: str) -> bool:
        """Return True when every host and network a command mentions is in scope.

        IPv4 literals, URLs and CIDR sweeps are extracted independently.
        A CIDR must be covered by the task scope as a whole, so a sweep
        cannot hide behind one in-scope host inside it.
        """
        from modules.lazy_loop import scope_allows_network

        text = command or ""
        networks = set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b", text))
        targets = set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text))
        for network in networks:
            base = network.split("/", 1)[0]
            targets.discard(base)
            allowed, reason = scope_allows_network(self.task_id, self.store, network)
            if not allowed:
                self.activity.emit(
                    self.name,
                    "block",
                    f"scope-network: {network} {reason}",
                    intent_id=0,
                )
                return False
        targets.update(re.findall(r"https?://[^\s'\"]+", text))
        if not targets:
            return True
        return all(self._scope_allows_target(target) for target in targets)
