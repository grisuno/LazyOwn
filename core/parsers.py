"""Parsing utilities for the LazyOwn framework.

Extracted from ``utils.py`` — YAML, XML, CSV, HTML, and text parsers
used throughout the framework.
"""

from __future__ import annotations

import csv
import json
import os
import re
from typing import Any

import yaml
from defusedxml import ElementTree as ET

from core.console import print_error, print_msg


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences and readline markers from a string.

    Handles standard escape codes (``\x1b[...m``), extended unicode
    escape initiators (``\u001b``, ``\u009b``), CSI sequences, and the
    ``\x01``/``\x02`` (SOH/STX) delimiters that ``render_prompt`` emits
    so readline can measure prompt width.

    Args:
        text: Raw terminal output.

    Returns:
        Clean text without ANSI codes or readline control markers.
    """
    ansi_regex = re.compile(r"[\u001b\u009b][\[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]")
    cleaned = ansi_regex.sub("", text)
    return cleaned.replace("\x01", "").replace("\x02", "")


def clean_output(output: str) -> str:
    """Remove ANSI escape sequences from a string.

    Args:
        output: Raw terminal output.

    Returns:
        Clean text without ANSI codes.
    """
    return strip_ansi(output)


def clean_html(html_string: str) -> str:
    """Strip HTML tags from a string.

    Args:
        html_string: HTML content.

    Returns:
        Plain text.
    """
    return re.sub(r"<.*?>", "", html_string).strip()


def clean_url(host: str) -> str:
    """Normalize a URL by stripping protocol and trailing slash.

    Args:
        host: Raw host string (e.g. ``https://example.com/``).

    Returns:
        Cleaned hostname.
    """
    host = re.sub(r"https?://", "", host)
    host = re.sub(r":443$|:80$", "", host)
    host = host.rstrip("/")
    return host


def htmlify(data: str) -> str:
    """Encode text as HTML entities.

    Args:
        data: Plain text.

    Returns:
        HTML-encoded string.
    """
    return data.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def de_htmlify(data: str) -> str:
    """Decode HTML entities back to plain text.

    Args:
        data: HTML-encoded string.

    Returns:
        Decoded text.
    """
    from html.parser import HTMLParser

    parser = HTMLParser()
    return parser.unescape(data)


def is_exist(file: str) -> bool:
    """Check if a file exists.

    Args:
        file: Path to the file.

    Returns:
        True if the file exists.
    """
    if not os.path.exists(file):
        print_error(f"File {file} not found")
        return False
    return True


def get_xml(directory: str) -> list[str]:
    """Find all XML files in a directory.

    Args:
        directory: Path to search.

    Returns:
        List of XML file paths.
    """
    xml_files = []
    for f in os.listdir(directory):
        if f.endswith(".xml"):
            xml_files.append(os.path.join(directory, f))
    return xml_files


def get_domain_from_xml(xml_file: str) -> str:
    """Extract the hostname from an Nmap XML file.

    Args:
        xml_file: Path to Nmap XML output.

    Returns:
        Hostname if found, else ``""``.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for host in root.findall("host"):
            hostnames = host.find("hostnames")
            if hostnames is not None:
                for hn in hostnames.findall("hostname"):
                    name = hn.get("name", "")
                    if name:
                        return name
    except (ET.ParseError, FileNotFoundError):
        pass
    return ""


def extract_banners(xml_file: str) -> list[dict[str, Any]]:
    """Extract service banners from an Nmap XML file.

    Args:
        xml_file: Path to Nmap XML output.

    Returns:
        List of banner dicts with keys ``port``, ``protocol``, ``service``.
    """
    banners: list[dict[str, Any]] = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for host in root.findall("host"):
            for port_elem in host.findall(".//port"):
                port = port_elem.get("portid")
                protocol = port_elem.get("protocol")
                service = port_elem.find("service")
                banners.append(
                    {
                        "port": port,
                        "protocol": protocol or "tcp",
                        "service": service.get("name", "") if service is not None else "",
                    }
                )
    except (ET.ParseError, FileNotFoundError):
        pass
    return banners


def parse_nmap_csv(csv_path: str) -> list[dict[str, Any]]:
    """Parse an Nmap CSV output file.

    Args:
        csv_path: Path to CSV file.

    Returns:
        List of row dicts.
    """
    results: list[dict[str, Any]] = []
    try:
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
    except FileNotFoundError:
        print_error(f"File not found: {csv_path}")
    return results


def manual_yaml_extraction(content: str) -> dict[str, Any]:
    """Fallback YAML parser for malformed content.

    Args:
        content: Raw text containing YAML-like data.

    Returns:
        Extracted key-value pairs.
    """
    result: dict[str, Any] = {}
    lines = content.split("\n")
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip()
            if key and value:
                result[key] = value
    return result


def fix_common_yaml_issues(yaml_content: str) -> str:
    """Fix common YAML formatting issues.

    Args:
        yaml_content: Raw YAML string.

    Returns:
        Cleaned YAML string.
    """
    fixed_lines: list[str] = []
    expected_indent: int | None = None
    for line in yaml_content.split("\n"):
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            fixed_lines.append(line)
            continue
        indent = len(line) - len(stripped)
        if expected_indent is None and ":" in stripped:
            expected_indent = indent
        if stripped.startswith("- ") and expected_indent is not None and indent > expected_indent:
            line = " " * expected_indent + stripped
        fixed_lines.append(line)
    return "\n".join(fixed_lines)


def aggressive_yaml_fix(yaml_content: str) -> str:
    """Aggressively fix YAML by normalizing indentation.

    Args:
        yaml_content: Raw YAML string.

    Returns:
        Fixed YAML string.
    """
    lines = yaml_content.split("\n")
    fixed = []
    base_indent: int | None = None
    for line in lines:
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            fixed.append(line)
            continue
        indent = len(line) - len(stripped)
        if base_indent is None and stripped and not stripped.startswith("-"):
            base_indent = indent
        if base_indent is not None and indent > base_indent and not stripped.startswith("-"):
            line = " " * (base_indent + 2) + stripped
        fixed.append(line)
    return "\n".join(fixed)


def create_synthetic_yaml(nmap_services: list[dict[str, Any]]) -> str:
    """Build a YAML string from parsed Nmap service data.

    Args:
        nmap_services: List of service dicts.

    Returns:
        YAML-formatted string.
    """
    doc: dict[str, Any] = {"services": []}
    for svc in nmap_services:
        entry = {
            "port": svc.get("port"),
            "protocol": svc.get("protocol", "tcp"),
            "state": svc.get("state", "open"),
            "service": svc.get("name", svc.get("service", "")),
        }
        if svc.get("version"):
            entry["version"] = svc["version"]
        doc["services"].append(entry)
    return yaml.dump(doc, default_flow_style=False)


def parse_yaml_response(content: str) -> dict[str, Any] | None:
    """Parse a YAML string, trying multiple strategies.

    Args:
        content: YAML string (possibly malformed).

    Returns:
        Parsed dict or None.
    """
    for fixer in (lambda c: c, fix_common_yaml_issues, aggressive_yaml_fix, manual_yaml_extraction):
        try:
            result = yaml.safe_load(fixer(content))
            if isinstance(result, dict):
                return result
        except (yaml.YAMLError, AttributeError):
            continue
    return None


def load_adversary() -> dict[str, Any]:
    """Load adversary profile from ``adversary.json``.

    Returns:
        Adversary config dict.
    """
    try:
        with open("adversary.json") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_knowledge_base(knowledge_file: str = "my_techniques.json") -> dict[str, Any]:
    """Load the knowledge base JSON file.

    Args:
        knowledge_file: Path to the JSON file.

    Returns:
        Knowledge base dict.
    """
    try:
        with open(knowledge_file) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_user_aliases() -> dict[str, Any]:
    """Load user-defined aliases from ``user_aliases.json``.

    Returns:
        Aliases dict.
    """
    path = "user_aliases.json"
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def list_binaries(directory: str = "sessions") -> list[str]:
    """List files in the sessions directory.

    Args:
        directory: Path to list.

    Returns:
        List of filenames.
    """
    try:
        return os.listdir(directory)
    except FileNotFoundError:
        return []


def select_binary(binaries: list[str]) -> str | None:
    """Interactive binary selector (fallback).

    Args:
        binaries: List of filenames.

    Returns:
        Selected filename or None.
    """
    if not binaries:
        print_msg("No binaries found.")
        return None
    for i, b in enumerate(binaries, 1):
        print_msg(f"{i}. {b}")
    try:
        choice = int(input("Select: ")) - 1
        if 0 <= choice < len(binaries):
            return binaries[choice]
    except (ValueError, IndexError):
        pass
    return None


__all__ = [
    "aggressive_yaml_fix",
    "clean_html",
    "clean_output",
    "clean_url",
    "create_synthetic_yaml",
    "de_htmlify",
    "extract_banners",
    "fix_common_yaml_issues",
    "get_domain_from_xml",
    "get_xml",
    "htmlify",
    "is_exist",
    "list_binaries",
    "load_adversary",
    "load_knowledge_base",
    "load_user_aliases",
    "manual_yaml_extraction",
    "parse_nmap_csv",
    "parse_yaml_response",
    "select_binary",
]
