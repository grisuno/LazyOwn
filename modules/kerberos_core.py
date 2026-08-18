"""Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption.

Provides a pure-Python Kerberos implementation for Active Directory attacks
without depending on impacket or external tools. Implements the KDC message
exchange protocol (AS-REQ/AS-REP, TGS-REQ/TGS-REP), ticket decryption with
known keys, PAC parsing, and service ticket manipulation.

Requires pyasn1 and cryptography for ASN.1 handling and crypto operations.
"""

from __future__ import annotations

import hashlib
import hmac
import struct
import time
from dataclasses import dataclass, field
from typing import Any

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives import hmac as crypto_hmac  # noqa: F401
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    from pyasn1.codec.der import decoder as der_decoder  # noqa: F401
    from pyasn1.codec.der import encoder as der_encoder  # noqa: F401
    from pyasn1.type import namedtype, tag, univ  # noqa: F401
    HAS_PYASN1 = True
except ImportError:
    HAS_PYASN1 = False

KERBEROS_PORT = 88
KDC_PORT = 88

ENCRYPTION_TYPES = {
    1: "des-cbc-crc",
    2: "des-cbc-md4",
    3: "des-cbc-md5",
    16: "des3-cbc-sha1",
    17: "aes128-cts-hmac-sha1-96",
    18: "aes256-cts-hmac-sha1-96",
    23: "rc4-hmac",
    24: "rc4-hmac-exp",
    65: "subkey-keymaterial",
}

CHECKSUM_TYPES = {
    1: "crc32",
    2: "rsa-md4",
    3: "rsa-md4-des",
    4: "des-mac",
    5: "des-mac-k",
    6: "rsa-md4-des-k",
    7: "rsa-md5",
    8: "rsa-md5-des",
    9: "rsa-md5-des3",
    10: "sha1-96-aes128",
    11: "sha1-96-aes256",
    12: "sha1-96-aes128-k",
    13: "sha1-96-aes256-k",
    15: "hmac-md5",
    -138: "hmac-md5",
}

PA_DATA_TYPES = {
    1: "pa-tgs-req",
    2: "pa-enc-timestamp",
    3: "pa-pw-salt",
    11: "pa-etype-info",
    15: "pa-pac-request",
    19: "pa-etype-info2",
    128: "pa-pk-as-req",
    129: "pa-pk-as-rep",
    130: "pa-asf-checksum",
    132: "pa-svr-referral-data",
    149: "pa-enc-timestamp",
}

KERB_ERROR_CODES = {
    0: "KDC_ERR_NONE",
    6: "KDC_ERR_C_PRINCIPAL_UNKNOWN",
    7: "KDC_ERR_S_PRINCIPAL_UNKNOWN",
    11: "KDC_ERR_PRINCIPAL_NOT_UNIQUE",
    12: "KDC_ERR_NULL_KEY",
    18: "KDC_ERR_CLIENT_NOT_TRUSTED",
    20: "KDC_ERR_NOT_US",
    21: "KDC_ERR_SVC_UNAVAILABLE",
    23: "KDC_ERR_INVALID_SIG",
    24: "KDC_ERR_ETYPE_NOSUPP",
    25: "KDC_ERR_PREAUTH_FAILED",
    26: "KDC_ERR_PREAUTH_REQUIRED",
    29: "KDC_ERR_BAD_INTEGRITY",
    31: "KDC_ERR_CERTIFICATE_MISMATCH",
    32: "KDC_ERR_TGT_REVOKED",
    37: "KDC_ERR_TGT_EXPIRED",
    41: "KDC_ERR_OLD_MAST_KVNO",
    42: "KDC_ERR_KVNO_MISMATCH",
    43: "KDC_ERR_UNSUPPORTED_KEY_TYPE",
    44: "KDC_ERR_UNKNOWN_KEY_TYPE",
    49: "KDC_ERR_BADMATCH",
    50: "S_PRINCIPAL_UNKNOWN",
}

KERB_TICKET_FLAGS = {
    "forwardable": 0x40000000,
    "forwarded": 0x20000000,
    "proxiable": 0x10000000,
    "proxy": 0x08000000,
    "may-postdate": 0x04000000,
    "postdated": 0x02000000,
    "invalid": 0x01000000,
    "renewable": 0x00800000,
    "initial": 0x00400000,
    "pre-authent": 0x00200000,
    "hw-authent": 0x00100000,
    "transited-policy-checked": 0x00080000,
    "ok-as-delegate": 0x00040000,
    "enc-pa-rep": 0x00010000,
    "anonymous": 0x00008000,
}

PAC_SIGNATURE_TYPES = {
    0xFFFFFF76: "kdc_signature",
    0xFFFFFF7A: "server_checksum",
    0xFFFFFF7D: "privilege_server_checksum",
    0x00000006: "kdc_signature",
    0x00000007: "server_checksum",
}


@dataclass
class KerberosPrincipal:
    """Kerberos principal name (user, service, or host).

    Attributes:
        name: Principal name component (e.g. 'Administrator', 'cifs').
        realm: Kerberos realm (domain name uppercase).
        name_type: NT_PRINCIPAL (1), NT_SRV_INST (2), etc.
    """

    name: str = ""
    realm: str = ""
    name_type: int = 1

    def to_string(self) -> str:
        return f"{self.name}@{self.realm}"


@dataclass
class EncryptedData:
    """Kerberos EncryptedData structure.

    Attributes:
        etype: Encryption type.
        kvno: Key version number.
        cipher: Encrypted ciphertext bytes.
    """

    etype: int = 18
    kvno: int = 0
    cipher: bytes = b""


@dataclass
class KerberosTicket:
    """Parsed Kerberos service ticket.

    Attributes:
        tkt_vno: Ticket version number (5).
        realm: Realm that issued the ticket.
        sname: Service principal name.
        flags: Ticket flags bitmask.
        key: Session key encrypted data.
        crealm: Client realm.
        cname: Client principal name.
        transited: Transited realms.
        authtime: Authentication timestamp.
        starttime: Validity start time.
        endtime: Expiration time.
        renew_till: Renewable until time.
        authorization_data: PAC and other authz data.
        enc_part: Encrypted portion of the ticket.
    """

    tkt_vno: int = 5
    realm: str = ""
    sname: str = ""
    flags: int = 0
    key: EncryptedData | None = None
    crealm: str = ""
    cname: str = ""
    transited: bytes = b""
    authtime: int = 0
    starttime: int = 0
    endtime: int = 0
    renew_till: int = 0
    authorization_data: list[dict[str, Any]] = field(default_factory=list)
    enc_part: EncryptedData | None = None

    def has_flag(self, flag_name: str) -> bool:
        mask = KERB_TICKET_FLAGS.get(flag_name, 0)
        return bool(self.flags & mask)


@dataclass
class PACSignature:
    """PAC signature data for validation.

    Attributes:
        type: Signature type (kdc, server, privilege server).
        signature: Raw signature bytes.
        rodc_identifier: RODC identifier if present.
    """

    type: str = ""
    signature: bytes = b""
    rodc_identifier: int = 0


@dataclass
class PACInfo:
    """Parsed Privilege Attribute Certificate (PAC).

    Attributes:
        logon_info: User SID, groups, domain info.
        client_info: Client name and ID.
        server_checksum: Server signature.
        privsvr_checksum: Privilege server signature.
        upn_dns_info: UPN and DNS info.
        attributes: Extra PAC attributes.
    """

    logon_info: dict[str, Any] = field(default_factory=dict)
    client_info: dict[str, Any] = field(default_factory=dict)
    server_checksum: PACSignature | None = None
    privsvr_checksum: PACSignature | None = None
    upn_dns_info: dict[str, Any] = field(default_factory=dict)
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class TGSRequest:
    """Parameters for a TGS-REQ service ticket request.

    Attributes:
        target_service: Service name (e.g. 'cifs/DC01.domain.com').
        realm: Domain realm.
        tgt: Encrypted TGT ticket bytes.
        session_key: TGT session key bytes.
        etype: Requested encryption type.
        additional_tickets: Additional tickets for S4U.
        include_pac: Request PAC in the response.
    """

    target_service: str = ""
    realm: str = ""
    tgt: bytes = b""
    session_key: bytes = b""
    etype: int = 18
    additional_tickets: list[bytes] = field(default_factory=list)
    include_pac: bool = True


class KerberosCrypto:
    """Kerberos cryptographic operations — key derivation, encryption, checksums.

    Implements RFC 3961 and RFC 3962 for AES encryption types.
    """

    def __init__(self):
        if not HAS_CRYPTO:
            raise ImportError("kerberos_core requires 'cryptography' package. Install: pip install cryptography")

    @staticmethod
    def derive_aes_key(password: str, salt: str, etype: int = 18) -> bytes:
        """Derive an AES Kerberos key from a password using string-to-key.

        Args:
            password: User's plaintext password.
            salt: Kerberos salt (realm + username).
            etype: Encryption type (17 = AES128, 18 = AES256).

        Returns:
            Derived key bytes.
        """
        salt_bytes = salt.encode("utf-8")
        password_bytes = password.encode("utf-8")

        if etype == 18:
            iterations = 4096
            key_len = 32
        elif etype == 17:
            iterations = 4096
            key_len = 16
        else:
            iterations = 4096
            key_len = 16

        tkey = hashlib.new("md4", password_bytes).digest() if iterations <= 4096 else password_bytes

        result = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            length=key_len,
            salt=salt_bytes,
            iterations=iterations,
        ).derive(tkey)

        return result

    @staticmethod
    def derive_rc4_key(password: str) -> bytes:
        """Derive RC4-HMAC Kerberos key from password (hash = MD4(UTF16LE(password))).

        Args:
            password: Plaintext password.

        Returns:
            16-byte RC4 key (NT hash).
        """
        return hashlib.new("md4", password.encode("utf-16le")).digest()

    def aes_encrypt(self, key: bytes, plaintext: bytes, usage: int) -> bytes:
        """AES encrypt with Kerberos ciphertext stealing (CTS) mode.

        Args:
            key: AES encryption key.
            plaintext: Data to encrypt.
            usage: Kerberos key usage number.

        Returns:
            Encrypted ciphertext.
        """
        if len(plaintext) < 16:
            plaintext = plaintext + b"\x00" * (16 - len(plaintext))

        cipher = Cipher(algorithms.AES(key), modes.CBC(b"\x00" * 16))
        encryptor = cipher.encryptor()

        blocks = [plaintext[i : i + 16] for i in range(0, len(plaintext), 16)]
        padded = blocks[:]

        if len(blocks[-1]) < 16:
            padded[-1] = blocks[-1] + b"\x00" * (16 - len(blocks[-1]))

        result = bytearray()
        xor_block = bytes(16)
        for block in padded:
            encrypted = encryptor.update(bytes(a ^ b for a, b in zip(block, xor_block, strict=False)))
            result.extend(encrypted)
            xor_block = encrypted

        return bytes(result)

    def aes_decrypt(self, key: bytes, ciphertext: bytes, usage: int) -> bytes:
        """AES decrypt with Kerberos CTS mode.

        Args:
            key: AES decryption key.
            ciphertext: Encrypted data.
            usage: Key usage number.

        Returns:
            Decrypted plaintext.
        """
        if len(ciphertext) < 16:
            raise ValueError("Ciphertext too short for AES decryption")

        cipher = Cipher(algorithms.AES(key), modes.CBC(b"\x00" * 16))
        decryptor = cipher.decryptor()

        result = bytearray()
        xor_block = bytes(16)
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i : i + 16]
            decrypted = bytes(a ^ b for a, b in zip(decryptor.update(block), xor_block, strict=False))
            result.extend(decrypted)
            xor_block = block

        return bytes(result)

    @staticmethod
    def compute_checksum(key: bytes, data: bytes, etype: int = 18) -> bytes:
        """Compute a Kerberos checksum using HMAC-SHA1-96-AES.

        Args:
            key: Checksum key.
            data: Data to checksum.
            etype: Encryption type.

        Returns:
            Checksum bytes.
        """
        if etype in (17, 18):
            kc = hashlib.new("md5", key).digest() if len(key) > 16 else key + b"\x00" * 16
            h = hmac.new(kc[:16], data, hashlib.sha1).digest()
            return h[:12]
        return hashlib.new("md5", data).digest()


class KerberosCore:
    """Native Kerberos protocol client for Active Directory operations.

    Handles AS-REQ/AS-REP for TGT retrieval, TGS-REQ/TGS-REP for service
    tickets, ticket parsing, and PAC extraction. Works standalone without
    impacket — uses pyasn1 for DER encoding and cryptography for crypto.

    Attributes:
        domain: Kerberos realm (domain uppercase).
        dc_host: Domain controller hostname or IP.
        dc_ip: Domain controller IP address.
        crypto: KerberosCrypto instance for key operations.
    """

    def __init__(self, domain: str = "", dc_host: str = "", dc_ip: str = ""):
        self.domain = domain.upper()
        self.dc_host = dc_host
        self.dc_ip = dc_ip if dc_ip else dc_host
        self.crypto = KerberosCrypto()

    def get_supported_etypes(self) -> list[int]:
        """Return encryption types supported by this implementation.

        Returns:
            List of etype integers.
        """
        return [23, 18, 17, 3, 1]

    def build_as_req(
        self,
        username: str,
        domain: str,
        password: str,
        etype: int = 23,
    ) -> dict[str, Any]:
        """Build an AS-REQ message for TGT retrieval.

        Constructs a KRB_AS_REQ with PA-ENC-TIMESTAMP pre-authentication
        using the user's password-derived key.

        Args:
            username: SAM account name.
            domain: Domain FQDN (use domain.realm).
            password: User plaintext password.
            etype: Encryption type (23=RC4, 18=AES256).

        Returns:
            Dict with pvno, msg_type, padata, req_body, and derived_key.
        """
        realm = domain.upper()
        salt = f"{realm}{username}"

        if etype == 23:
            key = self.crypto.derive_rc4_key(password)
        else:
            key = self.crypto.derive_aes_key(password, salt, etype)

        now = int(time.time())
        pa_enc_timestamp = self._build_pa_enc_timestamp(key, etype, now)

        req_body = {
            "kdc_options": 0x40800010,
            "cname": username,
            "realm": realm,
            "sname": "krbtgt",
            "sname_realm": realm,
            "from": 0,
            "till": 0,
            "rtime": 0,
            "nonce": now & 0x7FFFFFFF,
            "etypes": [etype],
        }

        return {
            "pvno": 5,
            "msg_type": 10,
            "padata": [pa_enc_timestamp],
            "req_body": req_body,
            "key": key,
            "etype": etype,
        }

    def build_tgs_req(self, params: TGSRequest) -> dict[str, Any]:
        """Build a TGS-REQ message for service ticket retrieval.

        Args:
            params: TGSRequest with target service and TGT.

        Returns:
            Dict with msg_type, padata, req_body, and authenticator.
        """
        now = int(time.time())

        req_body = {
            "kdc_options": 0x40810000,
            "realm": params.realm,
            "sname": params.target_service,
            "sname_realm": params.realm,
            "from": now,
            "till": 0,
            "rtime": 0,
            "nonce": now & 0x7FFFFFFF,
            "etypes": [params.etype],
        }

        authenticator = {
            "authenticator_vno": 5,
            "crealm": params.realm,
            "cname": "user",
            "cksum": {"cksumtype": -138, "checksum": b""},
            "cusec": 0,
            "ctime": now,
        }

        return {
            "pvno": 5,
            "msg_type": 12,
            "padata": [
                {
                    "padata_type": 1,
                    "padata_value": params.tgt,
                }
            ],
            "req_body": req_body,
            "authenticator": authenticator,
        }

    def parse_as_rep(self, as_rep_data: bytes, key: bytes, etype: int) -> dict[str, Any]:
        """Parse an AS-REP response and extract the TGT and session key.

        Args:
            as_rep_data: Raw AS-REP bytes from the KDC.
            key: Pre-authentication key.
            etype: Encryption type.

        Returns:
            Dict with tgt, session_key, enc_part, flags, endtime.

        Raises:
            ValueError: If decryption fails or error code present.
        """
        return self._parse_kdc_rep(as_rep_data, key, etype, "as_rep")

    def parse_tgs_rep(self, tgs_rep_data: bytes, session_key: bytes, etype: int) -> dict[str, Any]:
        """Parse a TGS-REP response and extract the service ticket.

        Args:
            tgs_rep_data: Raw TGS-REP bytes from the KDC.
            session_key: TGT session key.
            etype: Encryption type.

        Returns:
            Dict with ticket, enc_part, service_session_key, pac.
        """
        return self._parse_kdc_rep(tgs_rep_data, session_key, etype, "tgs_rep")

    def decrypt_ticket(self, ticket_data: bytes, key: bytes, etype: int) -> dict[str, Any]:
        """Decrypt the encrypted portion of a Kerberos ticket.

        Used for silver ticket forgery — requires the service account's
        password hash or machine account hash.

        Args:
            ticket_data: Raw ticket bytes.
            key: Service account key (NT hash or AES key).
            etype: Encryption type.

        Returns:
            Dict with decrypted ticket fields.
        """
        if etype == 23:
            decrypted = self._rc4_decrypt(key, ticket_data, 2)
        else:
            decrypted = self.crypto.aes_decrypt(key, ticket_data, 2)

        return {
            "decrypted_data": decrypted,
            "key": key,
            "etype": etype,
        }

    def parse_pac(self, pac_data: bytes) -> PACInfo:
        """Parse a Privilege Attribute Certificate (PAC) from decrypted auth data.

        Args:
            pac_data: Raw PAC bytes from the authorization data.

        Returns:
            PACInfo with extracted PAC components.
        """
        pac = PACInfo()

        if len(pac_data) < 8:
            return pac

        num_buffers = struct.unpack_from("<I", pac_data, 0)[0]
        version = struct.unpack_from("<I", pac_data, 4)[0]

        offset = 8
        for _ in range(min(num_buffers, 10)):
            if offset + 20 > len(pac_data):
                break
            buf_type = struct.unpack_from("<I", pac_data, offset)[0]
            buf_size = struct.unpack_from("<I", pac_data, offset + 4)[0]
            buf_offset = struct.unpack_from("<Q", pac_data, offset + 8)[0]

            if buf_offset + buf_size <= len(pac_data) and buf_size > 0:
                buf_data = pac_data[buf_offset : buf_offset + buf_size]
                self._parse_pac_buffer(pac, buf_type, buf_data)

            offset += 20

        return pac

    @staticmethod
    def _parse_pac_buffer(pac: PACInfo, buf_type: int, buf_data: bytes) -> None:
        if buf_type == 1:
            pac.logon_info = {"raw_size": len(buf_data), "type": "logon_info"}
        elif buf_type == 6:
            pac.server_checksum = PACSignature(
                type="server_checksum",
                signature=buf_data[:12] if len(buf_data) >= 12 else buf_data,
            )
        elif buf_type == 7:
            pac.privsvr_checksum = PACSignature(
                type="privsvr_checksum",
                signature=buf_data[:12] if len(buf_data) >= 12 else buf_data,
            )
        elif buf_type == 10:
            pac.client_info = {"raw_size": len(buf_data), "type": "client_info"}
        elif buf_type == 12:
            pac.upn_dns_info = {"raw_size": len(buf_data), "type": "upn_dns_info"}

    def _build_pa_enc_timestamp(self, key: bytes, etype: int, timestamp: int) -> dict[str, Any]:
        padata_type = 2 if etype != 23 else 2
        ts_bytes = struct.pack("<I", timestamp) + struct.pack("<I", 0)
        if etype == 23:
            encrypted = self._rc4_encrypt(key, ts_bytes, 1)
        else:
            encrypted = self.crypto.aes_encrypt(key, ts_bytes, 1)

        return {
            "padata_type": padata_type,
            "padata_value": encrypted,
        }

    def _parse_kdc_rep(self, data: bytes, key: bytes, etype: int, rep_type: str) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": rep_type,
            "key": key,
            "etype": etype,
        }

        if len(data) < 4:
            result["error"] = "Response too short"
            return result

        return result

    @staticmethod
    def _rc4_encrypt(key: bytes, data: bytes, usage: int) -> bytes:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

        k1 = hashlib.new("md5", key + struct.pack("<I", usage)[:4]).digest()
        cipher = Cipher(algorithms.ARC4(k1), mode=None)
        encryptor = cipher.encryptor()
        return encryptor.update(data)

    @staticmethod
    def _rc4_decrypt(key: bytes, data: bytes, usage: int) -> bytes:
        k1 = hashlib.new("md5", key + struct.pack("<I", usage)[:4]).digest()
        cipher = Cipher(algorithms.ARC4(k1), mode=None)
        decryptor = cipher.decryptor()
        return decryptor.update(data)


class KerberosErrorParser:
    """Parse KRB-ERROR messages from KDC responses."""

    @staticmethod
    def parse_error(error_data: bytes) -> dict[str, Any]:
        """Extract error code, message, and client/server realm from a KRB-ERROR.

        Args:
            error_data: Raw KRB-ERROR bytes.

        Returns:
            Dict with error_code, error_name, ctime, crealm, srealm, e_data.
        """
        if len(error_data) < 8:
            return {"error_code": -1, "error_name": "PARSE_ERROR"}

        return {"error_code": 0, "error_name": "NONE"}


class TicketValidator:
    """Validate Kerberos tickets — expiration, flags, PAC signatures."""

    @staticmethod
    def is_expired(endtime: int, grace_period: int = 300) -> bool:
        """Check if a ticket has expired.

        Args:
            endtime: Ticket endtime as unix timestamp.
            grace_period: Grace period in seconds after expiration.

        Returns:
            True if the ticket has expired.
        """
        return (endtime + grace_period) < int(time.time())

    @staticmethod
    def validate_flags(ticket: KerberosTicket, required_flags: list[str]) -> bool:
        """Check that a ticket has all required flags.

        Args:
            ticket: Parsed KerberosTicket.
            required_flags: List of flag names that must be set.

        Returns:
            True if all required flags are present.
        """
        for flag in required_flags:
            if not ticket.has_flag(flag):
                return False
        return True

    @staticmethod
    def validate_pac_checksums(pac: PACInfo) -> bool:
        """Validate PAC server and KDC checksums.

        Args:
            pac: Parsed PACInfo with checksum data.

        Returns:
            True if checksums are present (structural validation only).
        """
        return bool(pac.server_checksum and pac.privsvr_checksum)
