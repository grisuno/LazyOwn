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
        from modules.lazy_loop import AssetGate, _scope_covers, _target_as_asset

        try:
            gate = AssetGate(self.task_id).evaluate(target or "")
            if not gate["allowed"]:
                self.activity.emit(self.name, "block", f"asset-gate: {target} {gate['reason']}", intent_id=0)
                return False
        except Exception:
            pass
        try:
            from modules.intercept import scope_blocked as _blocked

            if _blocked(target or ""):
                self.activity.emit(
                    self.name, "block", f"scope-deny-global: {target} matches protected suffix", intent_id=0
                )
                return False
        except Exception:
            pass
        record = self.store.get(self.task_id) or {}
        scope = record.get("scope", []) or []
        if not scope:
            return self._lab_scope_default(target)
        shim = _target_as_asset(target)
        for item in scope:
            if _scope_covers(str(item.get("kind", "")), str(item.get("value", "")), shim):
                return True
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
        from modules import lazy_scope

        if not lazy_scope.LAB_DEFAULT_ENABLED:
            return True
        verdict = lazy_scope.scope_verdict(
            target,
            allowlist=lazy_scope.read_allowlist(),
            denylist=lazy_scope.read_denylist(),
        )
        if verdict.allowed:
            return True
        self.activity.emit(
            self.name,
            "block",
            f"scope-lab-default: {target} {verdict.reason}: {verdict.detail}",
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

    def _command_in_scope(self, command: str) -> bool:
        """Return True when every host a command mentions is in scope."""
        text = command or ""
        targets = set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text))
        targets.update(re.findall(r"https?://[^\s'\"]+", text))
        if not targets:
            return True
        return all(self._scope_allows_target(target) for target in targets)
