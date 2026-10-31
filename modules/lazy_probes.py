"""Read-only validation command registry for LazyOwn.

Every check kind owns its command text, its quoting and a structured
``expect`` contract that says how the output decides the question. A model
may pick a kind and parameters; the registry below validates them against
allowlists and renders the concrete command, so a person can read the
``command``/``explain`` pair and a chain step or a beacon session can run
the same command with the same ``expect``. Nothing here mutates a target.

Public surface is one function, :func:`render_check`, plus
:func:`render_checks` for a batch. Unknown kinds and out-of-allowlist
parameters fail loudly in ``errors``, never silently.
"""

from __future__ import annotations

import re
import shlex
from dataclasses import dataclass, field
from urllib.parse import quote as _url_quote

CHECK_VERSION_BANNER = "version_banner"
CHECK_HTTP_PROBE = "http_probe"
CHECK_NUCLEI_TEMPLATE = "nuclei_template"
CHECK_NSE_SCRIPT = "nse_script"
CHECK_PACKAGE_VERSION = "package_version"
CHECK_SERVICE_STATE = "service_state"

CHECK_KINDS = frozenset({
    CHECK_VERSION_BANNER,
    CHECK_HTTP_PROBE,
    CHECK_NUCLEI_TEMPLATE,
    CHECK_NSE_SCRIPT,
    CHECK_PACKAGE_VERSION,
    CHECK_SERVICE_STATE,
})

HTTP_METHODS = frozenset({"GET", "HEAD", "POST", "OPTIONS"})
ECOSYSTEMS = frozenset({"dpkg", "rpm", "apk", "pip", "npm", "gem", "any"})
SERVICE_STATES = frozenset({"running", "stopped", "enabled", "disabled"})
MAX_PORT = 65535
TARGET_PORT = "<TARGET>"
_PATH_RE = re.compile(r"^/[!-~]*$")


@dataclass
class RenderedCheck:
    """One ready-to-run read-only validation command.

    Attributes:
        kind: Check kind the command was rendered from.
        tool: Tool the command drives (nmap, curl, nuclei, ...).
        command: Read-only command line with ``<TARGET>`` (and a port)
            placeholder for the operator to substitute.
        expect: Structured accept result contract.
        explain: One-line explanation of the decision rule.
        read_only: Always True, by contract.
        errors: Empty for a valid check, else the rejection reasons.
    """

    kind: str
    tool: str = ""
    command: str = ""
    expect: dict = field(default_factory=dict)
    explain: str = ""
    read_only: bool = True
    errors: list[str] = field(default_factory=list)


def range_text(ranges: list[dict]) -> str:
    """Render affected ranges as a human phrase.

    Args:
        ranges: Range dicts with ``introduced``/``fixed``/``last_affected``.

    Returns:
        A readable sentence fragment describing the bounds.
    """
    parts: list[str] = []
    for rng in ranges or []:
        low = str(rng.get("introduced") or "")
        fixed = str(rng.get("fixed") or "")
        last = str(rng.get("last_affected") or "")
        if low and fixed:
            parts.append(f"{low} up to but not including {fixed}")
        elif fixed:
            parts.append(f"every version before {fixed}")
        elif low and last:
            parts.append(f"{low} through {last}")
        elif low:
            parts.append(f"{low} and later")
        elif last:
            parts.append(f"every version through {last}")
    return "; ".join(parts) or "the affected range"


def _need_port(params: dict) -> list[str]:
    """Validate a positive integer port parameter."""
    try:
        port = int(params.get("port") or 0)
    except (TypeError, ValueError):
        return ["port must be an integer"]
    if not 1 <= port <= MAX_PORT:
        return [f"port must be between 1 and {MAX_PORT}"]
    return []


def check_errors(kind: str, params: dict) -> list[str]:
    """Validate one check request against the kind's allowlist.

    Args:
        kind: One of the :data:`CHECK_KINDS`.
        params: Check parameters.

    Returns:
        A list of rejection reasons, empty when the check is renderable.
    """
    errors: list[str] = []
    params = params if isinstance(params, dict) else {}
    if kind == CHECK_VERSION_BANNER:
        errors += _need_port(params)
        if not str(params.get("product") or "").strip():
            errors.append("product is required")
    elif kind == CHECK_HTTP_PROBE:
        method = str(params.get("method") or "GET").upper()
        if method not in HTTP_METHODS:
            errors.append(f"method must be one of {sorted(HTTP_METHODS)}")
        path = str(params.get("path") or "/")
        if not _PATH_RE.match(path):
            errors.append("path must be an absolute URL path")
        codes = params.get("codes") if isinstance(params.get("codes"), list) else [200]
        for code in codes:
            if not isinstance(code, int) or not 100 <= code <= 599:
                errors.append("codes entries must be HTTP status integers")
    elif kind == CHECK_NUCLEI_TEMPLATE:
        if not re.fullmatch(r"[A-Za-z0-9._\-]+", str(params.get("template_id") or "")):
            errors.append("template_id must match the nuclei id grammar")
    elif kind == CHECK_NSE_SCRIPT:
        if not re.fullmatch(r"[A-Za-z0-9._\-]+", str(params.get("script") or "")):
            errors.append("script must match the nse script name grammar")
    elif kind == CHECK_PACKAGE_VERSION:
        if str(params.get("ecosystem") or "") not in ECOSYSTEMS:
            errors.append(f"ecosystem must be one of {sorted(ECOSYSTEMS)}")
        if not re.fullmatch(r"[A-Za-z0-9._+\-@/]+", str(params.get("package") or "")):
            errors.append("package must match the package name grammar")
    elif kind == CHECK_SERVICE_STATE:
        if not re.fullmatch(r"[A-Za-z0-9._\-@]+", str(params.get("service") or "")):
            errors.append("service must match the unit name grammar")
        if str(params.get("state") or "") not in SERVICE_STATES:
            errors.append(f"state must be one of {sorted(SERVICE_STATES)}")
    else:
        errors.append(f"unknown check kind: {kind}")
    return errors


def render_check(kind: str, params: dict) -> RenderedCheck:
    """Render one read-only validation command.

    Args:
        kind: One of the :data:`CHECK_KINDS`.
        params: Validated check parameters; extra keys are ignored.

    Returns:
        A :class:`RenderedCheck`; when the parameters fail their
        allowlist the result carries only ``errors``.
    """
    params = params if isinstance(params, dict) else {}
    errors = check_errors(kind, params)
    if errors:
        return RenderedCheck(kind=kind, errors=errors)
    renderer = _RENDERERS.get(kind)
    if renderer is None:
        return RenderedCheck(kind=kind, errors=[f"no renderer for kind: {kind}"])
    return renderer(params)


def render_checks(checks: list[dict]) -> list[RenderedCheck]:
    """Render a batch of checks in order.

    Args:
        checks: ``{"kind": ..., "params": {...}}`` dicts.

    Returns:
        Rendered checks in the same order.
    """
    return [render_check(str(item.get("kind") or ""), dict(item.get("params") or {})) for item in checks]


def _render_version_banner(params: dict) -> RenderedCheck:
    """Render an nmap version probe for a bounded-range verdict."""
    port = int(params.get("port") or 0)
    product = str(params.get("product"))
    ranges = params.get("ranges") if isinstance(params.get("ranges"), list) else []
    command = f"nmap -Pn -sV --version-intensity 5 -p {port} {TARGET_PORT}"
    return RenderedCheck(
        kind=CHECK_VERSION_BANNER,
        tool="nmap",
        command=command,
        expect={"kind": "version_in_range", "product": product, "ranges": ranges},
        explain=(
            f"The reported {product} version is inside {range_text(ranges)}. A banner can hide a backported fix, "
            "so match here plus a probe confirmation is the honest verdict."
        ),
    )


def _render_http_probe(params: dict) -> RenderedCheck:
    """Render a read-only curl probe with a status/body verdict."""
    method = str(params.get("method") or "GET").upper()
    path = str(params.get("path") or "/")
    codes = params.get("codes") if isinstance(params.get("codes"), list) else [200]
    flags = " -sS -i -m1" + (" -I" if method == "HEAD" else "")
    method_flag = "" if method == "HEAD" else f" -X {method}"
    expected = f"status {', '.join(str(code) for code in codes)}"
    if params.get("contains"):
        expected += f" and the body contains {params['contains']!r}"
    if params.get("absent"):
        expected += f" and the body does not contain {params['absent']!r}"
    url = f"https://{TARGET_PORT}" + _url_quote(path, safe="/?&=%:@!$'()*+,;~-._")
    return RenderedCheck(
        kind=CHECK_HTTP_PROBE,
        tool="curl",
        command=f"curl{flags}{method_flag} {shlex.quote(url)}",
        expect={
            "kind": "http_status",
            "codes": codes,
            "contains": str(params.get("contains") or ""),
            "absent": str(params.get("absent") or ""),
        },
        explain=f"Vulnerable when the TLS response has {expected}. Plain http swaps the scheme.",
    )


def _render_nuclei_template(params: dict) -> RenderedCheck:
    """Render a single-template nuclei run with a present/absent verdict."""
    template = str(params.get("template_id"))
    return RenderedCheck(
        kind=CHECK_NUCLEI_TEMPLATE,
        tool="nuclei",
        command=f"nuclei -duc -id {shlex.quote(template)} -u {TARGET_PORT}",
        expect={"kind": "template_match", "template_id": template},
        explain=(
            "Vulnerable when the template reports a match; no match means "
            "the check did not fire, not that the host is safe."
        ),
    )


def _render_nse_script(params: dict) -> RenderedCheck:
    """Render an nmap NSE probe with a contains verdict."""
    script = str(params.get("script"))
    extra = f" and the output contains {params['contains']!r}" if params.get("contains") else ""
    command = f"nmap -Pn -sV --script {shlex.quote(script)} -p {int(params.get('port') or 0)} {TARGET_PORT}"
    return RenderedCheck(
        kind=CHECK_NSE_SCRIPT,
        tool="nmap",
        command=command,
        expect={"kind": "output_contains", "script": script, "contains": str(params.get("contains") or "")},
        explain=f"Read the {script} output{extra}.",
    )


def _render_package_version(params: dict) -> RenderedCheck:
    """Render the installed-version query for one package ecosystem."""
    package = shlex.quote(str(params.get("package")))
    ecosystem = str(params.get("ecosystem"))
    queries = {
        "any": ("dpkg", "dpkg-query -W -f='${Version}\\n' " + package),
        "dpkg": ("dpkg", "dpkg-query -W -f='${Version}\\n' " + package),
        "rpm": ("rpm", "rpm -q --qf '%{VERSION}-%{RELEASE}\\n' " + package),
        "apk": ("apk", "apk info -v " + package),
        "pip": ("pip", "python3 -m pip show " + package),
        "npm": ("npm", "npm ls -g --depth=0 " + package),
        "gem": ("gem", "gem list -e " + package),
    }
    tool, command = queries.get(ecosystem, queries["any"])
    bound = str(params.get("affected_below") or params.get("fixed_version") or "")
    return RenderedCheck(
        kind=CHECK_PACKAGE_VERSION,
        tool=tool,
        command=command,
        expect={"kind": "version_lt", "bound": bound, "package": str(params.get("package"))},
        explain=(
            f"Read the installed version line; affected when it is below {bound or 'the fixed version'}. "
            "A vendor backport may hide the fix without raising the upstream version."
        ),
    )


def _render_service_state(params: dict) -> RenderedCheck:
    """Render a read-only service state check for linux and windows."""
    service = shlex.quote(str(params.get("service")))
    state = str(params.get("state") or "")
    wanted = {"running": ("is-active", "active"), "stopped": ("is-active", "inactive"),
              "enabled": ("is-enabled", "enabled"), "disabled": ("is-enabled", "disabled")}[state]
    rendered = RenderedCheck(
        kind=CHECK_SERVICE_STATE,
        tool="systemctl",
        command=f"systemctl {wanted[0]} {service}",
        expect={"kind": "output_equals", "value": wanted[1]},
        explain=f"Prints {wanted[1]} when the unit is {state}.",
    )
    return rendered


_RENDERERS = {
    CHECK_VERSION_BANNER: _render_version_banner,
    CHECK_HTTP_PROBE: _render_http_probe,
    CHECK_NUCLEI_TEMPLATE: _render_nuclei_template,
    CHECK_NSE_SCRIPT: _render_nse_script,
    CHECK_PACKAGE_VERSION: _render_package_version,
    CHECK_SERVICE_STATE: _render_service_state,
}


__all__ = [
    "CHECK_HTTP_PROBE",
    "CHECK_KINDS",
    "CHECK_NSE_SCRIPT",
    "CHECK_NUCLEI_TEMPLATE",
    "CHECK_PACKAGE_VERSION",
    "CHECK_SERVICE_STATE",
    "CHECK_VERSION_BANNER",
    "TARGET_PORT",
    "RenderedCheck",
    "check_errors",
    "range_text",
    "render_check",
    "render_checks",
]
