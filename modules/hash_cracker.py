"""Hash cracking pipeline — John the Ripper and Hashcat integration.

Parses hash formats from secretsdump output, identifies hash types, and
runs the appropriate cracker. Results feed back into the LazyOwnDB
credentials table.

Design (SOLID):
- Single Responsibility: HashCracker only cracks hashes.
- Open/Closed: new hash formats added via HASH_FORMATS dict.
- Liskov: any cracker (John, Hashcat) implements CrackBackend protocol.
- Interface Segregation: identify(), crack(), and import_results().
- Dependency Inversion: depends on abstract backend, not concrete binary.

Usage:
    from modules.hash_cracker import HashCracker

    cracker = HashCracker(wordlist="/usr/share/wordlists/rockyou.txt")
    results = cracker.crack_file("sessions/hashes_10.10.11.5.txt")
    cracker.import_to_db(results, rhost="10.10.11.5")
"""

from __future__ import annotations

import hashlib
import logging
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("hash_cracker")

HASH_PATTERNS: dict[str, dict[str, Any]] = {
    "ntlm": {
        "format": "NT",
        "hashcat_mode": "1000",
        "pattern": re.compile(r"^[0-9a-fA-F]{32}$"),
        "john_format": "NT",
        "source": "SAM / NTDS dump",
    },
    "ntlmv2": {
        "format": "netntlmv2",
        "hashcat_mode": "5600",
        "pattern": re.compile(r"^\w+::[\w\\]+:[0-9a-fA-F:]+$"),
        "john_format": "netntlmv2",
        "source": "Responder / relay capture",
    },
    "kerberos_tgs": {
        "format": "krb5tgs",
        "hashcat_mode": "13100",
        "pattern": re.compile(r"^\$krb5tgs\$\d+\$\*"),
        "john_format": "krb5tgs",
        "source": "Kerberoasting",
    },
    "kerberos_asrep": {
        "format": "krb5asrep",
        "hashcat_mode": "18200",
        "pattern": re.compile(r"^\$krb5asrep\$\d+\$"),
        "john_format": "krb5asrep",
        "source": "AS-REP roasting",
    },
    "md5": {
        "format": "Raw-MD5",
        "hashcat_mode": "0",
        "pattern": re.compile(r"^[0-9a-fA-F]{32}$"),
        "john_format": "raw-md5",
        "source": "generic",
    },
    "sha1": {
        "format": "Raw-SHA1",
        "hashcat_mode": "100",
        "pattern": re.compile(r"^[0-9a-fA-F]{40}$"),
        "john_format": "raw-sha1",
        "source": "generic",
    },
    "sha256": {
        "format": "Raw-SHA256",
        "hashcat_mode": "1400",
        "pattern": re.compile(r"^[0-9a-fA-F]{64}$"),
        "john_format": "raw-sha256",
        "source": "generic",
    },
    "md5crypt": {
        "format": "md5crypt",
        "hashcat_mode": "500",
        "pattern": re.compile(r"^\$1\$[./0-9A-Za-z]+\$[./0-9A-Za-z]{22}$"),
        "john_format": "md5crypt",
        "source": "Linux /etc/shadow",
    },
    "sha512crypt": {
        "format": "sha512crypt",
        "hashcat_mode": "1800",
        "pattern": re.compile(r"^\$6\$.+\$.+$"),
        "john_format": "sha512crypt",
        "source": "Linux /etc/shadow",
    },
    "yescrypt": {
        "format": "yescrypt",
        "hashcat_mode": None,
        "pattern": re.compile(r"^\$y\$j.+\$.+$"),
        "john_format": "yescrypt",
        "source": "Linux /etc/shadow (modern)",
    },
    "descrypt": {
        "format": "descrypt",
        "hashcat_mode": "1500",
        "pattern": re.compile(r"^[./0-9A-Za-z]{13}$"),
        "john_format": "descrypt",
        "source": "Linux /etc/shadow (legacy)",
    },
    "krb5pa": {
        "format": "krb5pa-sha1",
        "hashcat_mode": "7500",
        "pattern": re.compile(r"^\$krb5pa\$\d+\$"),
        "john_format": "krb5pa",
        "source": "Kerberos pre-auth (AS-REP/GetNPUsers)",
    },
}

COMMON_WORDLISTS: list[str] = [
    "/usr/share/wordlists/rockyou.txt",
    "/usr/share/wordlists/rockyou.txt.gz",
    "/usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt",
    "/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt",
    "/usr/share/wordlists/fasttrack.txt",
]


@dataclass
class CrackResult:
    hash_value: str
    password: str
    hash_type: str
    format: str
    cracked: bool = False
    source: str = ""
    cracker: str = ""
    speed_guesses_per_sec: int = 0
    duration_seconds: float = 0.0


@dataclass
class HashIdentifier:
    raw: str
    hash_type: str
    format: str
    hashcat_mode: str | None = None
    john_format: str = ""
    source: str = ""
    username: str = ""
    hostname: str = ""


class HashCracker:
    """Pipeline for identifying and cracking password hashes.

    Supports John the Ripper and Hashcat backends. Automatically selects
    the best available cracker per hash format.

    Attributes:
        wordlist: Path to wordlist file for dictionary attacks.
        rules: John rules to apply (default: ``--rules=best64``).
        use_hashcat: Prefer Hashcat over John when available.
        timeout: Max cracking time in seconds per format group.
    """

    def __init__(
        self,
        wordlist: str | None = None,
        rules: str = "best64",
        use_hashcat: bool = True,
        timeout: int = 1800,
    ) -> None:
        self._wordlist = wordlist
        self._rules = rules
        self._use_hashcat = use_hashcat
        self._timeout = timeout
        self._john_bin = shutil.which("john")
        self._hashcat_bin = shutil.which("hashcat")

    def _resolve_wordlist(self) -> str | None:
        if self._wordlist and Path(self._wordlist).exists():
            return self._wordlist
        for wl in COMMON_WORDLISTS:
            if Path(wl).exists():
                return wl
        return None

    def identify(self, line: str) -> HashIdentifier | None:
        """Identify the hash type of a single line.

        Args:
            line: A hash string (with or without username prefix).

        Returns:
            HashIdentifier if recognized, None otherwise.
        """
        line = line.strip()
        if not line or line.startswith("#"):
            return None

        username = ""
        hostname = ""
        if ":" in line:
            parts = line.split(":")
            if len(parts) >= 2:
                username = parts[0]
            if len(parts) >= 3:
                hostname = parts[1]

            if ":::" in line and len(parts) >= 4:
                for fmt_name in ("ntlm",):
                    fmt = HASH_PATTERNS[fmt_name]
                    nt_hash = parts[3].strip()
                    if fmt["pattern"].match(nt_hash):
                        return HashIdentifier(
                            raw=line,
                            hash_type=fmt_name,
                            format=fmt["format"],
                            hashcat_mode=fmt["hashcat_mode"],
                            john_format=fmt["john_format"],
                            source=fmt["source"],
                            username=username,
                            hostname=hostname,
                        )

            candidates = [parts[-1]] if parts[-1] else [p for p in parts[1:] if p]
        else:
            candidates = [line]

        for fmt_name in ("ntlmv2",):
            fmt = HASH_PATTERNS[fmt_name]
            if fmt["pattern"].search(line):
                return HashIdentifier(
                    raw=line,
                    hash_type=fmt_name,
                    format=fmt["format"],
                    hashcat_mode=fmt["hashcat_mode"],
                    john_format=fmt["john_format"],
                    source=fmt["source"],
                    username=username,
                    hostname=hostname,
                )

        for candidate in candidates:
            candidate = candidate.strip()
            if not candidate:
                continue
            for fmt_name, fmt in HASH_PATTERNS.items():
                if fmt["pattern"].match(candidate):
                    return HashIdentifier(
                        raw=line,
                        hash_type=fmt_name,
                        format=fmt["format"],
                        hashcat_mode=fmt["hashcat_mode"],
                        john_format=fmt["john_format"],
                        source=fmt["source"],
                        username=username,
                        hostname=hostname,
                    )
            for fmt_name, fmt in HASH_PATTERNS.items():
                if fmt["pattern"].search(line):
                    return HashIdentifier(
                        raw=line,
                        hash_type=fmt_name,
                        format=fmt["format"],
                        hashcat_mode=fmt["hashcat_mode"],
                        john_format=fmt["john_format"],
                        source=fmt["source"],
                        username=username,
                        hostname=hostname,
                    )

        return None

    def identify_file(self, filepath: str | Path) -> dict[str, list[HashIdentifier]]:
        """Parse a hash file and group hashes by type.

        Args:
            filepath: Path to file containing hashes (e.g. secretsdump output).

        Returns:
            Dict mapping hash_type -> list of HashIdentifier.
        """
        path = Path(filepath)
        if not path.exists():
            log.warning("Hash file not found: %s", filepath)
            return {}

        grouped: dict[str, list[HashIdentifier]] = {}
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                ident = self.identify(line)
                if ident:
                    grouped.setdefault(ident.hash_type, []).append(ident)
        return grouped

    def crack_hash(
        self,
        hash_value: str,
        hash_type: str | None = None,
        wordlist: str | None = None,
    ) -> CrackResult:
        """Attempt to crack a single hash.

        Args:
            hash_value: The hash string to crack.
            hash_type: Known hash type (auto-detected if None).
            wordlist: Override wordlist path.

        Returns:
            CrackResult with cracked password if successful.
        """
        if hash_type is None:
            ident = self.identify(hash_value)
            if ident is None:
                return CrackResult(
                    hash_value=hash_value,
                    password="",
                    hash_type="unknown",
                    format="unknown",
                )
            hash_type = ident.hash_type
            fmt_info = HASH_PATTERNS.get(hash_type, {})
        else:
            fmt_info = HASH_PATTERNS.get(hash_type, {})

        wl = wordlist or self._resolve_wordlist()
        if wl is None:
            return CrackResult(
                hash_value=hash_value,
                password="",
                hash_type=hash_type or "unknown",
                format=fmt_info.get("format", "unknown"),
                cracked=False,
            )

        if self._use_hashcat and self._hashcat_bin and fmt_info.get("hashcat_mode"):
            return self._crack_hashcat(hash_value, hash_type, fmt_info, wl)

        if self._john_bin:
            return self._crack_john(hash_value, hash_type, fmt_info, wl)

        return CrackResult(
            hash_value=hash_value,
            password="",
            hash_type=hash_type,
            format=fmt_info.get("format", "unknown"),
            cracked=False,
        )

    def crack_file(
        self,
        filepath: str | Path,
        wordlist: str | None = None,
        hash_types: list[str] | None = None,
    ) -> list[CrackResult]:
        """Crack all hashes in a file.

        Args:
            filepath: Path to file containing hashes.
            wordlist: Override wordlist path.
            hash_types: Filter to only crack specific hash types.

        Returns:
            List of CrackResult with cracked passwords.
        """
        grouped = self.identify_file(filepath)
        results: list[CrackResult] = []

        for htype, idents in grouped.items():
            if hash_types and htype not in hash_types:
                continue

            wl = wordlist or self._resolve_wordlist()
            if wl is None:
                log.warning("No wordlist available for cracking %s hashes", htype)
                for ident in idents:
                    results.append(CrackResult(
                        hash_value=ident.raw,
                        password="",
                        hash_type=htype,
                        format=ident.format,
                    ))
                continue

            fmt_info = HASH_PATTERNS.get(htype, {})

            if self._use_hashcat and self._hashcat_bin and fmt_info.get("hashcat_mode"):
                results.extend(self._crack_batch_hashcat(idents, htype, fmt_info, wl))
            elif self._john_bin:
                results.extend(self._crack_batch_john(idents, htype, fmt_info, wl))
            else:
                for ident in idents:
                    results.append(CrackResult(
                        hash_value=ident.raw,
                        password="",
                        hash_type=htype,
                        format=ident.format,
                    ))

        return results

    def import_to_db(
        self,
        results: list[CrackResult],
        rhost: str = "",
        workspace_name: str = "default",
    ) -> int:
        """Import cracked results into the LazyOwnDB credentials table.

        Args:
            results: Crack results from crack_file().
            rhost: Target IP for associating credentials.
            workspace_name: DB workspace to use.

        Returns:
            Number of credentials imported.
        """
        from modules.db import LazyOwnDB
        db = LazyOwnDB()
        ws = db.workspace_get(workspace_name)
        if ws is None:
            ws_id = db.workspace_create(workspace_name)
        else:
            ws_id = ws["id"]

        host_id: int | None = None
        if rhost:
            hosts = db.host_search(address=rhost, workspace_id=ws_id)
            if hosts:
                host_id = hosts[0]["id"]

        imported = 0
        for result in results:
            if not result.cracked or not result.password:
                continue
            db.cred_add(
                host_id=host_id,
                username=result.hash_value.split(":")[0] if ":" in result.hash_value else "",
                password=result.password,
                realm=rhost,
                cred_type="password",
                origin=f"cracked_{result.cracker}",
                cracked=1,
            )
            imported += 1

        log.info("Imported %d cracked credentials into DB workspace '%s'", imported, workspace_name)
        return imported

    def _crack_hashcat(
        self,
        hash_value: str,
        hash_type: str,
        fmt_info: dict,
        wordlist: str,
    ) -> CrackResult:
        import tempfile
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".hash", delete=False)
        try:
            tmp.write(hash_value + "\n")
            tmp.close()
            cmd = [
                self._hashcat_bin,
                "-m", str(fmt_info["hashcat_mode"]),
                "-a", "0",
                tmp.name,
                wordlist,
                "--potfile-disable",
                "--quiet",
                "-O",
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=self._timeout)
            password = self._parse_hashcat_output(proc.stdout, proc.stderr, hash_value)
            return CrackResult(
                hash_value=hash_value,
                password=password,
                hash_type=hash_type,
                format=fmt_info["format"],
                cracked=bool(password),
                cracker="hashcat",
            )
        except subprocess.TimeoutExpired:
            return CrackResult(hash_value=hash_value, password="", hash_type=hash_type, format=fmt_info["format"])
        except Exception as exc:
            log.debug("hashcat error: %s", exc)
            return CrackResult(hash_value=hash_value, password="", hash_type=hash_type, format=fmt_info["format"])
        finally:
            try:
                Path(tmp.name).unlink()
            except OSError:
                pass

    def _crack_batch_hashcat(
        self,
        idents: list[HashIdentifier],
        hash_type: str,
        fmt_info: dict,
        wordlist: str,
    ) -> list[CrackResult]:
        import tempfile
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".hashes", delete=False)
        try:
            for ident in idents:
                tmp.write(ident.raw + "\n")
            tmp.close()
            cmd = [
                self._hashcat_bin,
                "-m", str(fmt_info["hashcat_mode"]),
                "-a", "0",
                tmp.name,
                wordlist,
                "--potfile-disable",
                "--quiet",
                "-O",
                "--outfile-format", "1",
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=self._timeout)
            cracked_map: dict[str, str] = {}
            for line in proc.stdout.splitlines():
                if ":" in line:
                    h, p = line.strip().rsplit(":", 1)
                    cracked_map[h.strip()] = p.strip()

            results: list[CrackResult] = []
            for ident in idents:
                pw = cracked_map.get(ident.raw.strip(), "")
                results.append(CrackResult(
                    hash_value=ident.raw,
                    password=pw,
                    hash_type=hash_type,
                    format=ident.format,
                    cracked=bool(pw),
                    cracker="hashcat",
                ))
            return results
        except subprocess.TimeoutExpired:
            return [
                CrackResult(h=ident.raw, password="", hash_type=hash_type, format=ident.format)
                for ident in idents
            ]
        except Exception as exc:
            log.debug("hashcat batch error: %s", exc)
            return [
                CrackResult(h=ident.raw, password="", hash_type=hash_type, format=ident.format)
                for ident in idents
            ]
        finally:
            try:
                Path(tmp.name).unlink()
            except OSError:
                pass

    def _crack_john(
        self,
        hash_value: str,
        hash_type: str,
        fmt_info: dict,
        wordlist: str,
    ) -> CrackResult:
        import tempfile
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".hash", delete=False)
        try:
            tmp.write(hash_value + "\n")
            tmp.close()
            cmd = [
                self._john_bin,
                f"--format={fmt_info['john_format']}",
                f"--wordlist={wordlist}",
                f"--rules={self._rules}",
                "--max-run-time", str(self._timeout),
                tmp.name,
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=self._timeout + 30)
            show_cmd = [
                self._john_bin,
                f"--format={fmt_info['john_format']}",
                "--show",
                tmp.name,
            ]
            show = subprocess.run(show_cmd, capture_output=True, text=True, timeout=30)
            password = self._parse_john_show(show.stdout, hash_value)
            return CrackResult(
                hash_value=hash_value,
                password=password,
                hash_type=hash_type,
                format=fmt_info["format"],
                cracked=bool(password),
                cracker="john",
            )
        except subprocess.TimeoutExpired:
            return CrackResult(hash_value=hash_value, password="", hash_type=hash_type, format=fmt_info["format"])
        except Exception as exc:
            log.debug("john error: %s", exc)
            return CrackResult(hash_value=hash_value, password="", hash_type=hash_type, format=fmt_info["format"])
        finally:
            try:
                Path(tmp.name).unlink()
            except OSError:
                pass

    def _crack_batch_john(
        self,
        idents: list[HashIdentifier],
        hash_type: str,
        fmt_info: dict,
        wordlist: str,
    ) -> list[CrackResult]:
        import tempfile
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".hashes", delete=False)
        try:
            for ident in idents:
                tmp.write(ident.raw + "\n")
            tmp.close()
            cmd = [
                self._john_bin,
                f"--format={fmt_info['john_format']}",
                f"--wordlist={wordlist}",
                f"--rules={self._rules}",
                "--max-run-time", str(self._timeout),
                tmp.name,
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=self._timeout + 30)
            show_cmd = [self._john_bin, f"--format={fmt_info['john_format']}", "--show", tmp.name]
            show = subprocess.run(show_cmd, capture_output=True, text=True, timeout=30)
            cracked_map: dict[str, str] = {}
            for line in show.stdout.splitlines():
                if ":" in line:
                    parts = line.strip().split(":")
                    h = parts[0] if parts else ""
                    p = parts[1] if len(parts) > 1 else ""
                    if h and p:
                        cracked_map[h] = p

            results: list[CrackResult] = []
            for ident in idents:
                pw = cracked_map.get(ident.raw.strip().split(":")[0], "")
                results.append(CrackResult(
                    hash_value=ident.raw,
                    password=pw,
                    hash_type=hash_type,
                    format=ident.format,
                    cracked=bool(pw),
                    cracker="john",
                ))
            return results
        except subprocess.TimeoutExpired:
            return [
                CrackResult(h=ident.raw, password="", hash_type=hash_type, format=ident.format)
                for ident in idents
            ]
        except Exception as exc:
            log.debug("john batch error: %s", exc)
            return [
                CrackResult(h=ident.raw, password="", hash_type=hash_type, format=ident.format)
                for ident in idents
            ]
        finally:
            try:
                Path(tmp.name).unlink()
            except OSError:
                pass

    @staticmethod
    def _parse_hashcat_output(stdout: str, stderr: str, original: str) -> str:
        for line in stdout.splitlines():
            line = line.strip()
            if line and ":" in line:
                parts = line.rsplit(":", 1)
                if len(parts) == 2:
                    return parts[1].strip()
        for line in stderr.splitlines():
            if "Cracked" in line or "Recovered" in line:
                parts = line.rsplit(":", 1)
                if len(parts) == 2:
                    return parts[1].strip()
        return ""

    @staticmethod
    def _parse_john_show(show_output: str, original: str) -> str:
        for line in show_output.splitlines():
            if line.strip() and ":" in line:
                parts = line.strip().split(":")
                if parts and parts[0].strip() == original.strip():
                    return parts[1].strip() if len(parts) > 1 else ""
        return ""


def crack_secretsdump_output(
    filepath: str | Path,
    wordlist: str | None = None,
    rhost: str = "",
) -> list[CrackResult]:
    """Convenience function: crack a secretsdump output file and import results.

    Args:
        filepath: Path to secretsdump output with hashes.
        wordlist: Override wordlist path.
        rhost: Target IP for DB import.

    Returns:
        List of CrackResult.
    """
    cracker = HashCracker(wordlist=wordlist)
    results = cracker.crack_file(filepath)
    if rhost:
        cracked = [r for r in results if r.cracked]
        if cracked:
            cracker.import_to_db(cracked, rhost=rhost)
    return results


__all__ = [
    "HashCracker",
    "HashIdentifier",
    "CrackResult",
    "HASH_PATTERNS",
    "COMMON_WORDLISTS",
    "crack_secretsdump_output",
]
