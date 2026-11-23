"""Detection rule synthesizer — offensive action to defensive rule.

Given an offensive action (command, MITRE technique, category), generates
the matching Sigma log-detection rule and, when file artifacts are known,
a YARA rule for the dropped payload. Rules are deterministic (stable
UUIDs) so the blue team can pin them in their SIEM and track them across
engagements.

>>> from modules.detection_synthesizer import ActionFingerprint, synthesize_sigma
>>> rule = synthesize_sigma(ActionFingerprint(name="mimikatz", command="mimikatz sekurlsa::logonpasswords", technique_id="T1003.001", category="credential"))
>>> "detection:" in rule
True
"""

from __future__ import annotations

import datetime
import hashlib
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RULES_DIRNAME = "sessions"
RULES_SUBDIR = "purple_rules"
KIT_SIGMA_DIR = Path("detection_kit") / "sigma"

DEFAULT_AUTHOR = "LazyOwn RedTeam Framework"
DEFAULT_STATUS = "experimental"

MIN_TOKEN_LEN = 4
MAX_SELECTION_TOKENS = 6
UUID_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

CATEGORY_TACTIC: dict[str, tuple[str, ...]] = {
    "recon": ("attack.reconnaissance",),
    "enum": ("attack.discovery",),
    "exploit": ("attack.initial_access", "attack.execution"),
    "credential": ("attack.credential_access",),
    "lateral": ("attack.lateral_movement",),
    "privesc": ("attack.privilege_escalation",),
    "payload": ("attack.execution",),
    "brute_force": ("attack.credential_access",),
    "intrusion": ("attack.command_and_control",),
    "exfil": ("attack.exfiltration",),
    "persistence": ("attack.persistence",),
    "defense_evasion": ("attack.defense_evasion",),
    "other": ("attack.execution",),
}

DEFAULT_TACTIC = CATEGORY_TACTIC["other"]


@dataclass
class ActionFingerprint:
    """One offensive action with the metadata defenders can pivot on."""

    name: str
    command: str
    technique_id: str = ""
    category: str = "other"
    target_host: str = ""
    artifacts: list[str] = field(default_factory=list)
    platform: str = "windows"

    def as_dict(self) -> dict[str, Any]:
        """Return the JSON-serialisable fingerprint."""
        return {
            "name": self.name,
            "command": self.command,
            "technique_id": self.technique_id,
            "category": self.category,
            "target_host": self.target_host,
            "artifacts": list(self.artifacts),
            "platform": self.platform,
        }


def stable_rule_id(fingerprint: ActionFingerprint, kind: str) -> str:
    """Derive a deterministic UUIDv5 for a rule.

    Args:
        fingerprint: The offensive action.
        kind: Rule family, ``sigma`` or ``yara``.

    Returns:
        UUID string derived from name + command + kind.
    """
    seed = f"{fingerprint.name}|{fingerprint.command}|{kind}"
    return str(uuid.uuid5(UUID_NAMESPACE, seed))


def _sig_tokens(command: str) -> list[str]:
    """Pick the distinctive fragments of a command line.

    Args:
        command: Raw command line.

    Returns:
        Up to :data:`MAX_SELECTION_TOKENS` fragments worth matching on.
    """
    tokens: list[str] = []
    for raw in command.split():
        token = raw.strip()
        if not token or token.startswith("-"):
            continue
        if len(token) < MIN_TOKEN_LEN:
            continue
        tokens.append(token)
        if len(tokens) >= MAX_SELECTION_TOKENS:
            break
    if not tokens and command.strip():
        tokens = [command.strip()]
    return tokens


def _tactic_tags(category: str, technique_id: str) -> list[str]:
    """Map a kill-chain category to Sigma ``attack.*`` tags.

    Args:
        category: Kill-chain category label.
        technique_id: Optional MITRE ATT&CK technique id.

    Returns:
        List of tags including the technique tag when valid.
    """
    tags = list(CATEGORY_TACTIC.get(category, DEFAULT_TACTIC))
    if technique_id.upper().startswith("T") and technique_id[1:].replace(".", "").isdigit():
        tags.append(f"attack.{technique_id.lower()}")
    return tags


def synthesize_sigma(fingerprint: ActionFingerprint) -> str:
    """Render a Sigma rule for a process/network-detectable action.

    Args:
        fingerprint: The offensive action to detect.

    Returns:
        Sigma YAML string following the Sigma v2 field layout used by
        ``detection_kit/sigma/``.
    """
    tokens = _sig_tokens(fingerprint.command)
    process = fingerprint.command.split()[0] if fingerprint.command.split() else fingerprint.name
    tags = _tactic_tags(fingerprint.category, fingerprint.technique_id)
    title = f'"LazyOwn Red Action: {fingerprint.name}"'
    references = [
        "https://github.com/grisuno/LazyOwn",
        f"https://attack.mitre.org/techniques/{fingerprint.technique_id}/" if fingerprint.technique_id else "",
    ]
    references = [ref for ref in references if ref]
    lines = [
        "title: " + title,
        "id: " + stable_rule_id(fingerprint, "sigma"),
        "status: " + DEFAULT_STATUS,
        "description: >",
        f"  Detects the execution of {fingerprint.name!r} on the target host."
        " Generated by the LazyOwn detection synthesizer so the blue team can"
        " validate detection coverage in real time during purple-team drills.",
        "author: " + DEFAULT_AUTHOR,
        "date: " + datetime.date.today().isoformat(),
        "references:",
        *[f"  - {ref}" for ref in references],
        "tags:",
        *[f"  - {tag}" for tag in tags],
        "logsource:",
        "  category: process_creation",
        f"  product: {fingerprint.platform}",
        "detection:",
        "  selection:",
        f"    Image|endswith: '{process}'",
        f"    CommandLine|contains: '{tokens[0]}'"
        if tokens
        else f"    CommandLine|contains: '{fingerprint.command[:32]}'",
        "  condition: selection",
        "falsepositives:",
        "  - Legitimate administration using the same binary with identical arguments.",
        "level: high",
        "",
    ]
    return "\n".join(lines)


def synthesize_yara(fingerprint: ActionFingerprint) -> str:
    """Render a YARA rule for payload artifacts of an action.

    Args:
        fingerprint: The offensive action whose artifacts to fingerprint.

    Returns:
        YARA rule string; empty string when no artifacts are known.
    """
    if not fingerprint.artifacts:
        return ""
    fragments: list[str] = []
    for artifact in fingerprint.artifacts[:8]:
        name = Path(artifact).name
        if len(name) >= MIN_TOKEN_LEN and name.lower() not in fragments:
            fragments.append(name.lower())
    if not fragments:
        return ""
    rule_name = "LazyOwn_" + "".join(part.capitalize() for part in fingerprint.name.replace("-", "_").split("_"))[:32]
    if not rule_name or not rule_name.isidentifier():
        rule_name = "LazyOwn_Action_" + hashlib.sha1(fingerprint.name.encode()).hexdigest()[:8]
    lines = [
        f"rule {rule_name}",
        "{",
        "  meta:",
        f'    author = "{DEFAULT_AUTHOR}"',
        f'    description = "Payload artifacts observed for {fingerprint.name} (LazyOwn red action)"',
        f'    category = "{fingerprint.category}"',
        f'    technique = "{fingerprint.technique_id}"',
        "  strings:",
    ]
    for index, fragment in enumerate(fragments):
        lines.append(f'    $artifact{index} = "{fragment}" nocase')
    lines.extend(
        [
            "  condition:",
            f"    {len(fragments)} of them",
            "}",
            "",
        ]
    )
    return "\n".join(lines)


def save_rules(fingerprint: ActionFingerprint, install: bool = False) -> dict[str, str]:
    """Write the synthesized rules to disk.

    Args:
        fingerprint: The offensive action.
        install: When True also drop the Sigma rule into
            ``detection_kit/sigma/`` for the packaged detection kit.

    Returns:
        Mapping ``sigma``/``yara`` to the written path (empty when the
        rule was not produced).
    """
    out_dir = Path(RULES_DIRNAME) / RULES_SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}
    sigma = synthesize_sigma(fingerprint)
    sigma_path = out_dir / f"lazyown_{_slug(fingerprint.name)}_{stable_rule_id(fingerprint, 'sigma')[:8]}.yml"
    sigma_path.write_text(sigma, encoding="utf-8")
    written["sigma"] = str(sigma_path)
    yara = synthesize_yara(fingerprint)
    if yara:
        yara_path = out_dir / f"lazyown_{_slug(fingerprint.name)}.yar"
        yara_path.write_text(yara, encoding="utf-8")
        written["yara"] = str(yara_path)
    if install and sigma_path.exists():
        KIT_SIGMA_DIR.mkdir(parents=True, exist_ok=True)
        kit_path = KIT_SIGMA_DIR / sigma_path.name
        kit_path.write_text(sigma, encoding="utf-8")
        written["kit_sigma"] = str(kit_path)
    return written


def _slug(name: str) -> str:
    """Normalize a name into a filename-safe slug.

    Args:
        name: Raw name.

    Returns:
        Lowercase slug safe for filenames.
    """
    slug = "".join(char if char.isalnum() else "_" for char in name.strip().lower())
    return slug.strip("_") or "action"
