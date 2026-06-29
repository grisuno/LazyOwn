"""DoD validators for every artifact the orchestrator produces.

The validators are the single source of truth for the Definition of
Done. Every agent calls them before it writes a result to disk. The
reviewer agent cross checks the same set so the cycle halts on a real
violation rather than on an opinion.
"""

from __future__ import annotations

import ast
import re
import tokenize
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable, Optional

from .models import Finding, Severity, Spec


SPANISH_HINTS = (
    "captura",
    "capturar",
    "capturando",
    "capturado",
    "todos los derechos",
    "implementacion",
    "implementación",
    "generacion",
    "generación",
    "archivo",
    "carpeta",
    "ejecucion",
    "ejecución",
    "operador",
    "informacion",
    "información",
    "configuracion",
    "configuración",
    "mensaje",
    "despliegue",
    "desarrollo",
    "produccion",
    "producción",
    "crear",
    "creado",
    "eliminar",
    "eliminado",
    "actualizar",
    "actualizado",
    "mostrar",
    "obtener",
)

FORBIDDEN_MARKERS = ("TODO", "FIXME", "XXX", "HACK")
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F600-\U0001F64F"
    "\U0001F900-\U0001F9FF"
    "]+",
    flags=re.UNICODE,
)
HARDCODED_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
HARDCODED_ABS_PATH = re.compile(r"(/home/[A-Za-z0-9._-]+|/root/[^\s\"']+)")
MAGIC_NUMBER_PATTERN = re.compile(r"(?<![\w.])\b(\d{2,})\b")


@dataclass
class CheckResult:
    """Outcome of running one validator over a piece of content.

    Attributes:
        findings: Findings the validator raised. Empty list means the
            artifact is compliant.
    """

    findings: list[Finding]

    @property
    def passed(self) -> bool:
        """Return True when the result has no findings."""
        return not self.findings

    def blocks(self) -> list[Finding]:
        """Return the blocker findings only."""
        return [f for f in self.findings if f.severity is Severity.BLOCK]


def find_block_comments(source: str) -> list[tuple[int, int]]:
    """Return the start and end line of every block comment in source.

    Args:
        source: Python source code.
    Returns:
        A list of tuples. Each tuple carries the start line and the
        end line of a block comment.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    comments: list[tuple[int, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            value = node.value.value
            if isinstance(value, str) and value.startswith("#") and not value.startswith("#!"):
                comments.append((node.lineno, node.end_lineno or node.lineno))
    return comments


def find_inline_comments(source: str) -> list[int]:
    """Return the line numbers of every inline comment in source.

    Inline comments are tokens that start with the COMMENT token type.
    The helper walks the token stream and ignores shebang lines.
    """
    lines: list[int] = []
    readline = StringIO(source).readline
    try:
        for tok in tokenize.generate_tokens(readline):
            if tok.type == tokenize.COMMENT and not tok.string.startswith("#!"):
                lines.append(tok.start[0])
    except (tokenize.TokenError, IndentationError):
        return lines
    return lines


def check_no_comments(source: str, path: str) -> list[Finding]:
    """Return a finding for every comment in the source code.

    Args:
        source: Python source code.
        path: Path the source belongs to. Used in the finding.
    Returns:
        Findings. Empty list when the source has no comments.
    """
    findings: list[Finding] = []
    for line in find_inline_comments(source):
        findings.append(
            Finding(
                severity=Severity.BLOCK,
                rule="dod.no_comments",
                message=f"inline comment on line {line}",
                path=path,
            )
        )
    for start, end in find_block_comments(source):
        findings.append(
            Finding(
                severity=Severity.BLOCK,
                rule="dod.no_comments",
                message=f"block comment from line {start} to {end}",
                path=path,
            )
        )
    return findings


def check_no_emoji(content: str, path: str) -> list[Finding]:
    """Return a finding for every emoji the content carries.

    Args:
        content: Text to inspect.
        path: Path the content belongs to. Used in the finding.
    Returns:
        Findings. Empty list when the content has no emoji.
    """
    findings: list[Finding] = []
    for match in EMOJI_PATTERN.finditer(content):
        findings.append(
            Finding(
                severity=Severity.BLOCK,
                rule="dod.no_emoji",
                message=f"emoji at offset {match.start()}: {match.group(0)!r}",
                path=path,
            )
        )
    return findings


def check_no_forbidden_markers(content: str, path: str) -> list[Finding]:
    """Return a finding for every TODO, FIXME, XXX, or HACK marker."""
    findings: list[Finding] = []
    for marker in FORBIDDEN_MARKERS:
        pattern = re.compile(rf"\b{marker}\b")
        for match in pattern.finditer(content):
            findings.append(
                Finding(
                    severity=Severity.BLOCK,
                    rule=f"dod.no_{marker.lower()}",
                    message=f"{marker} marker at offset {match.start()}",
                    path=path,
                )
            )
    return findings


def check_english_only(source: str, path: str) -> list[Finding]:
    """Return a finding for every Spanish hint the source carries.

    The validator is conservative. It scans identifiers, docstrings,
    and string literals. False positives are possible. The reviewer
    treats every hit as a warning and the operator can mark it as a
    non blocker through the strict flag.
    """
    findings: list[Finding] = []
    lowered = source.lower()
    for hint in SPANISH_HINTS:
        pattern = re.compile(rf"\b{re.escape(hint)}\b", re.IGNORECASE)
        for match in pattern.finditer(lowered):
            findings.append(
                Finding(
                    severity=Severity.WARN,
                    rule="dod.english_only",
                    message=f"Spanish hint '{hint}' at offset {match.start()}",
                    path=path,
                )
            )
    return findings


def check_docstrings(source: str, path: str) -> list[Finding]:
    """Return a finding for every public function or class without a docstring.

    The validator parses the source with ast and walks the tree. A
    public name is a name that does not start with an underscore. A
    missing docstring is a blocker.
    """
    findings: list[Finding] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return findings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_") and not isinstance(node, ast.ClassDef):
                continue
            doc = ast.get_docstring(node)
            if not doc or not doc.strip():
                findings.append(
                    Finding(
                        severity=Severity.BLOCK,
                        rule="dod.docstrings",
                        message=f"{type(node).__name__} '{node.name}' has no docstring",
                        path=path,
                    )
                )
                continue
            if "Args:" not in doc and "Returns:" not in doc and "Raises:" not in doc:
                findings.append(
                    Finding(
                        severity=Severity.WARN,
                        rule="dod.docstring_sections",
                        message=(
                            f"{type(node).__name__} '{node.name}' docstring "
                            "should include Args, Returns, or Raises"
                        ),
                        path=path,
                    )
                )
    return findings


def check_no_hardcoded_paths_or_ips(source: str, path: str) -> list[Finding]:
    """Return a finding for every absolute path or IP literal.

    Args:
        source: Python source code.
        path: Path the source belongs to.
    Returns:
        Findings. Empty list when the source has no hardcoded literal.
    """
    findings: list[Finding] = []
    for match in HARDCODED_IPV4.finditer(source):
        literal = match.group(0)
        if literal.startswith("127.") or literal.startswith("0.0.0.0"):
            continue
        findings.append(
            Finding(
                severity=Severity.WARN,
                rule="dod.no_hardcoded_ip",
                message=f"hardcoded IP {literal} at offset {match.start()}",
                path=path,
            )
        )
    for match in HARDCODED_ABS_PATH.finditer(source):
        findings.append(
            Finding(
                severity=Severity.BLOCK,
                rule="dod.no_hardcoded_path",
                message=f"absolute path {match.group(0)!r} at offset {match.start()}",
                path=path,
            )
        )
    return findings


def check_magic_numbers(source: str, path: str, allow: Optional[Iterable[int]] = None) -> list[Finding]:
    """Return a finding for every numeric literal that is not in the allow list.

    Args:
        source: Python source code.
        path: Path the source belongs to.
        allow: Iterable of literals that are explicitly allowed.
    Returns:
        Findings. Empty list when the source has no magic number.
    """
    findings: list[Finding] = []
    allow_set = {str(value) for value in (allow or [])}
    try:
        tokens = list(tokenize.generate_tokens(StringIO(source).readline))
    except (tokenize.TokenError, IndentationError):
        return findings
    for token in tokens:
        if token.type == tokenize.NUMBER:
            literal = token.string
            stripped = literal.rstrip("lLfFdDjJ")
            if stripped in allow_set or stripped in {"0", "1", "2"}:
                continue
            if not re.fullmatch(r"\d{2,}", stripped):
                continue
            findings.append(
                Finding(
                    severity=Severity.WARN,
                    rule="dod.no_magic_number",
                    message=f"magic number {literal!r} at line {token.start[0]}",
                    path=path,
                )
            )
    return findings


def check_source(source: str, path: str, allow_numbers: Optional[Iterable[int]] = None) -> list[Finding]:
    """Run every source level DoD check and return the findings."""
    findings: list[Finding] = []
    findings.extend(check_no_comments(source, path))
    findings.extend(check_no_emoji(source, path))
    findings.extend(check_no_forbidden_markers(source, path))
    findings.extend(check_english_only(source, path))
    findings.extend(check_docstrings(source, path))
    findings.extend(check_no_hardcoded_paths_or_ips(source, path))
    findings.extend(check_magic_numbers(source, path, allow=allow_numbers))
    return findings


def check_markdown(content: str, path: str) -> list[Finding]:
    """Run every markdown level DoD check and return the findings."""
    findings: list[Finding] = []
    findings.extend(check_no_emoji(content, path))
    findings.extend(check_no_forbidden_markers(content, path))
    findings.extend(check_english_only(content, path))
    return findings


def check_spec(spec: Spec, min_sad_paths: int) -> list[Finding]:
    """Run the spec level DoD check and return the findings."""
    findings: list[Finding] = []
    findings.extend(check_no_emoji(spec.goal + " " + spec.trigger, "spec"))
    findings.extend(check_no_forbidden_markers(spec.goal + " " + spec.trigger, "spec"))
    for violation in spec.validate(min_sad_paths):
        findings.append(
            Finding(
                severity=Severity.BLOCK,
                rule="dod.spec_integrity",
                message=violation,
                path="spec",
            )
        )
    return findings
