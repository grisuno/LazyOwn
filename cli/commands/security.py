"""OPSEC and security commands — risk scoring, credential sealing, rotation.

Integrates modules/opsec_scorer.py, core/credential_vault.py, and
modules/hash_cracker.py into the CLI.

Provides commands:
    opsec <command>        — Score OPSEC risk for a command
    seal_credentials       — Encrypt sensitive payload values at rest
    rotate_aes             — Generate new AES key and re-encrypt
    crack_hashes <file>    — Crack hashes from secretsdump output
"""

from __future__ import annotations

import os
from pathlib import Path

from cli.commands._base import LazyOwnCommandSet


class SecurityCommandSet(LazyOwnCommandSet):
    """OPSEC scoring, credential vault, and hash cracking commands."""

    def do_opsec(self, line: str) -> None:
        """Score OPSEC risk for a LazyOwn command before execution.

Usage: opsec <command>

Examples:
    opsec secretsdump
    opsec psexec
    opsec lazynmap
"""
        if not line.strip():
            self._cmd.perror("Usage: opsec <command>")
            return

        command = line.strip().split()[0]
        try:
            from rich.table import Table
            from rich.console import Console

            from core.config import load_payload
            from modules.opsec_scorer import OpsecScorer

            console = Console()
            payload = load_payload()
            scorer = OpsecScorer(payload)
            rhost = self.params.get("rhost", "")
            score = scorer.score(command, rhost=rhost)

            risk_colors = {
                "low": "green",
                "medium": "yellow",
                "high": "orange1",
                "critical": "red",
            }
            risk_color = risk_colors.get(score.risk_level, "white")

            table = Table(title=f"OPSEC Score: {command}")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")

            table.add_row("Noise Score", f"{score.noise_score}/10")
            table.add_row("Risk Level", f"[{risk_color}]{score.risk_level.upper()}[/{risk_color}]")
            table.add_row("Detection Risk", score.detection_risk)
            table.add_row("Confidence", f"{score.confidence:.0%}")
            table.add_row("Detectable By", ", ".join(score.detectable_by) if score.detectable_by else "none")

            console.print(table)

            if score.mitigation:
                console.print(f"\n[bold yellow]Mitigations:[/bold yellow]")
                for m in score.mitigation[:5]:
                    console.print(f"  - {m}")

            console.print(f"\n[bold]{score.recommendation}[/bold]\n")

        except ImportError:
            from cli.style import print_warn
            try:
                from core.config import load_payload
                from modules.opsec_scorer import OpsecScorer

                payload = load_payload()
                scorer = OpsecScorer(payload)
                rhost = self.params.get("rhost", "")
                score = scorer.score(command, rhost=rhost)

                print(f"\n  OPSEC Score for '{command}':")
                print(f"    Noise:     {score.noise_score}/10")
                print(f"    Risk:      {score.risk_level.upper()}")
                print(f"    Detection: {score.detection_risk}")
                print(f"    Confidence: {score.confidence:.0%}")
                if score.detectable_by:
                    print(f"    Detectable: {', '.join(score.detectable_by)}")
                if score.mitigation:
                    print(f"    Mitigations:")
                    for m in score.mitigation[:5]:
                        print(f"      - {m}")
                print(f"    {score.recommendation}\n")
            except Exception as exc:
                from cli.style import print_error
                print_error(f"OPSEC scoring failed: {exc}")

    def do_seal_credentials(self, _line: str) -> None:
        """Encrypt all sensitive values in payload.json using AES-256-GCM.

Usage: seal_credentials

After sealing, payload.json will contain encrypted values for passwords,
API keys, and other secrets. They are transparently decrypted at runtime.
"""
        try:
            from core.config import load_payload, save_payload
            from core.credential_vault import seal_payload

            payload = load_payload()
            sealed = seal_payload(payload)
            save_payload(sealed)
            self._cmd.poutput("Credentials sealed successfully.")
            self._cmd.poutput("  payload.json now contains encrypted credential values.")
            self._cmd.poutput("  Restart the shell to pick up changes.")
        except Exception as exc:
            self._cmd.perror(f"Failed to seal credentials: {exc}")

    def do_rotate_aes(self, _line: str) -> None:
        """Generate a new AES key and re-encrypt all sealed credentials.

Usage: rotate_aes

Use this when you need to rotate the encryption key for operational security.
All existing sealed values are decrypted with the old key and re-encrypted
with a fresh key.
"""
        try:
            from core.config import load_payload, save_payload
            from core.credential_vault import rotate_aes_key

            payload = load_payload()
            new_payload, new_key = rotate_aes_key(payload)
            save_payload(new_payload)
            self._cmd.poutput("AES key rotated successfully.")
            self._cmd.poutput(f"  New key saved to sessions/key.aes")
            self._cmd.poutput(f"  Credentials re-encrypted under fresh key.")
            self._cmd.poutput("  Restart the shell to pick up changes.")
        except Exception as exc:
            self._cmd.perror(f"Failed to rotate AES key: {exc}")

    def do_unseal_credentials(self, _line: str) -> None:
        """Decrypt sealed credential values in payload.json for inspection.

Usage: unseal_credentials

Warning: this writes plaintext credentials back to payload.json.
Use seal_credentials to re-encrypt them.
"""
        try:
            from core.config import load_payload, save_payload
            from core.credential_vault import unseal_payload

            payload = load_payload()
            unsealed = unseal_payload(payload)
            save_payload(unsealed)
            self._cmd.poutput("Credentials decrypted — values are now plaintext in payload.json.")
            self._cmd.poutput("  Run 'seal_credentials' to encrypt them again.")
        except Exception as exc:
            self._cmd.perror(f"Failed to unseal credentials: {exc}")

    def do_crack_hashes(self, line: str) -> None:
        """Crack password hashes from a file using John the Ripper or Hashcat.

Usage: crack_hashes <filepath> [--wordlist <path>]

Parses hashes from the file (e.g., secretsdump output), identifies hash types,
and runs John or Hashcat. Cracked passwords are imported into the DB.

Examples:
    crack_hashes sessions/hashes_10.10.11.5.txt
    crack_hashes sessions/ntds.dit --wordlist /usr/share/wordlists/rockyou.txt
"""
        args = line.strip().split()
        if not args:
            self._cmd.perror("Usage: crack_hashes <filepath> [--wordlist <path>]")
            return

        filepath = args[0]
        if not Path(filepath).exists():
            self._cmd.perror(f"File not found: {filepath}")
            return

        wordlist = None
        if "--wordlist" in args:
            idx = args.index("--wordlist")
            if idx + 1 < len(args):
                wordlist = args[idx + 1]

        try:
            from rich.table import Table
            from rich.console import Console

            from modules.hash_cracker import HashCracker

            console = Console()
            cracker = HashCracker(wordlist=wordlist)

            grouped = cracker.identify_file(filepath)
            if not grouped:
                self._cmd.poutput("No recognizable hashes found in file.")
                return

            table = Table(title=f"Hash Analysis: {filepath}")
            table.add_column("Hash Type", style="cyan")
            table.add_column("Count", style="white")
            table.add_column("Format", style="yellow")

            for htype, idents in grouped.items():
                table.add_row(htype, str(len(idents)), idents[0].format)

            console.print(table)

            rhost = self.params.get("rhost", "")
            results = cracker.crack_file(filepath, wordlist=wordlist)
            cracked = [r for r in results if r.cracked]

            if cracked:
                console.print(f"\n[green]Cracked {len(cracked)}/{len(results)} hashes:[/green]")
                for r in cracked[:20]:
                    console.print(f"  {r.hash_type:12s} {r.password}")
                if len(cracked) > 20:
                    console.print(f"  ... and {len(cracked) - 20} more")

                if rhost:
                    imported = cracker.import_to_db(cracked, rhost=rhost)
                    console.print(f"\n[green]Imported {imported} credentials into DB.[/green]")
            else:
                self._cmd.poutput(f"No hashes cracked out of {len(results)} total.")
                self._cmd.poutput("Try a larger wordlist with --wordlist <path>.")

        except ImportError:
            from modules.hash_cracker import HashCracker

            cracker = HashCracker(wordlist=wordlist)
            grouped = cracker.identify_file(filepath)
            if not grouped:
                self._cmd.poutput("No recognizable hashes found in file.")
                return

            print(f"\n  Hash types detected in {filepath}:")
            for htype, idents in grouped.items():
                print(f"    {htype}: {len(idents)} ({idents[0].format})")

            rhost = self.params.get("rhost", "")
            results = cracker.crack_file(filepath, wordlist=wordlist)
            cracked = [r for r in results if r.cracked]

            if cracked:
                print(f"\n  Cracked {len(cracked)}/{len(results)}:")
                for r in cracked[:20]:
                    print(f"    {r.hash_type:12s} {r.password}")
                if rhost:
                    imported = cracker.import_to_db(cracked, rhost=rhost)
                    print(f"\n  Imported {imported} credentials into DB.")
            else:
                print(f"  No hashes cracked out of {len(results)} total.")

    def complete_opsec(self, text: str, line: str, begidx: int, endidx: int) -> list[str]:
        words = line[:begidx].split()
        if len(words) <= 2:
            from modules.opsec_scorer import COMMAND_NOISE
            candidates = list(COMMAND_NOISE.keys())
            return [c for c in candidates if c.lower().startswith(text.lower())]
        return []

    def complete_crack_hashes(self, text: str, line: str, begidx: int, endidx: int) -> list[str]:
        import glob
        sessions_path = Path("sessions")
        candidates = list(sessions_path.glob("hash*")) + list(sessions_path.glob("*hash*"))
        return [str(p) for p in candidates if p.name.startswith(text)]
