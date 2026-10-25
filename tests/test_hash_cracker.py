"""Tests for modules/hash_cracker.py"""

from __future__ import annotations

from modules.hash_cracker import (
    COMMON_WORDLISTS,
    HASH_PATTERNS,
    CrackResult,
    HashCracker,
    HashIdentifier,
)


class TestHashIdentification:
    def test_identify_ntlm(self):
        cracker = HashCracker(use_hashcat=False)
        ntlm = "aad3b435b51404eeaad3b435b51404ee"
        ident = cracker.identify(ntlm)
        assert ident is not None
        assert ident.hash_type == "ntlm"

    def test_identify_ntlm_from_secretsdump(self):
        cracker = HashCracker(use_hashcat=False)
        line = "Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::"
        ident = cracker.identify(line)
        assert ident is not None
        assert ident.hash_type == "ntlm"

    def test_identify_sha512crypt(self):
        cracker = HashCracker(use_hashcat=False)
        shadow = "$6$salt$hashedvaluehere"
        ident = cracker.identify(shadow)
        assert ident is not None
        assert ident.hash_type == "sha512crypt"

    def test_identify_unknown(self):
        cracker = HashCracker(use_hashcat=False)
        ident = cracker.identify("not_a_hash")
        assert ident is None

    def test_identify_empty(self):
        cracker = HashCracker(use_hashcat=False)
        assert cracker.identify("") is None
        assert cracker.identify("# comment") is None

    def test_identify_kerberos_tgs(self):
        cracker = HashCracker(use_hashcat=False)
        tgs = "$krb5tgs$23$*user$DOMAIN$spn/name$hashvalue"
        ident = cracker.identify(tgs)
        if ident is not None:
            assert ident.hash_type in ("kerberos_tgs",)

    def test_identify_md5(self):
        cracker = HashCracker(use_hashcat=False)
        ident = cracker.identify("5d41402abc4b2a76b9719d911017c592")
        assert ident is not None
        assert ident.hash_type in ("ntlm", "md5")

    def test_identify_sha1(self):
        cracker = HashCracker(use_hashcat=False)
        ident = cracker.identify("aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d")
        assert ident is not None
        assert ident.hash_type == "sha1"


class TestFileIdentification:
    def test_identify_file_empty(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        cracker = HashCracker(use_hashcat=False)
        grouped = cracker.identify_file(str(f))
        assert len(grouped) == 0

    def test_identify_file_with_hashes(self, tmp_path):
        f = tmp_path / "hashes.txt"
        f.write_text(
            "Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::\n"
            "$6$salt$longhash\n"
            "not_a_hash line\n"
        )
        cracker = HashCracker(use_hashcat=False)
        grouped = cracker.identify_file(str(f))
        assert len(grouped) > 0

    def test_identify_file_not_exists(self):
        cracker = HashCracker(use_hashcat=False)
        grouped = cracker.identify_file("/nonexistent/path.txt")
        assert len(grouped) == 0


class TestCrackResult:
    def test_crack_result_defaults(self):
        result = CrackResult(
            hash_value="test",
            password="",
            hash_type="ntlm",
            format="NT",
        )
        assert not result.cracked
        assert result.password == ""

    def test_crack_result_cracked(self):
        result = CrackResult(
            hash_value="test",
            password="hunter2",
            hash_type="ntlm",
            format="NT",
            cracked=True,
        )
        assert result.cracked
        assert result.password == "hunter2"


class TestHashPatterns:
    def test_all_patterns_exist(self):
        for fmt_name in ("ntlm", "sha1", "sha256", "md5crypt", "sha512crypt", "descrypt"):
            assert fmt_name in HASH_PATTERNS, f"{fmt_name} should be in HASH_PATTERNS"
            assert "pattern" in HASH_PATTERNS[fmt_name]
            assert "format" in HASH_PATTERNS[fmt_name]


class TestWordlists:
    def test_wordlist_paths_are_strings(self):
        for wl in COMMON_WORDLISTS:
            assert isinstance(wl, str)
            assert wl.endswith(".txt") or wl.endswith(".txt.gz")


class TestHashIdentifier:
    def test_hash_identifier_fields(self):
        ident = HashIdentifier(
            raw="test:hash",
            hash_type="ntlm",
            format="NT",
            hashcat_mode="1000",
            john_format="NT",
            source="SAM dump",
            username="admin",
            hostname="DC01",
        )
        assert ident.hash_type == "ntlm"
        assert ident.username == "admin"
        assert ident.hostname == "DC01"
