"""LazyDorks: target-aware Google and GitHub dork generator for LazyOwn.

Pure in-memory text generation that renders the classic sensitive-information
dork grammar (backend logins, upload pages, injectable URLs, directory
listings, open redirects, SQL errors, phpinfo, exposed files, leaked cloud
keys and GitHub org secrets) around one target domain. No network, no shell.

>>> from modules import lazydorks
>>> bool(lazydorks.queries("backend_logins", "example.com")[0])
True
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

MAX_QUERIES_PER_CATEGORY = 12

CATEGORIES: tuple[str, ...] = (
    "backend_logins",
    "upload_pages",
    "injectable_urls",
    "editor_pages",
    "directory_listing",
    "open_redirects",
    "sql_errors",
    "phpinfo",
    "exposed_files",
    "leaked_keys",
    "github_org",
)

_GRAMMAR: dict[str, tuple[str, ...]] = {
    "backend_logins": (
        "site:{domain} inurl:login | inurl:admin | inurl:manage | inurl:backend",
        "site:{domain} intitle:admin | intitle:login | intitle:dashboard | intitle:{domain} admin",
        "site:{domain} intext:password | intext:admin panel | intext:control panel",
        "site:{domain} inurl:admin_login | inurl:signin | inurl:portal | inurl:cpanel",
    ),
    "upload_pages": (
        "site:{domain} inurl:upload | inurl:file | inurl:import",
        "site:{domain} inurl:attachments | inurl:media | inurl:wp-content",
    ),
    "injectable_urls": (
        "site:{domain} inurl:?id=",
        "site:{domain} inurl:?page= | inurl:?cat= | inurl:?item=",
        "site:{domain} inurl:.php?id= | inurl:.asp?id= | inurl:.jsp?id=",
    ),
    "editor_pages": (
        "site:{domain} inurl:ewebeditor | inurl:ckeditor | inurl:fckeditor",
        "site:{domain} inurl:tinymce | inurl:editor | inurl:wysiwyg",
    ),
    "directory_listing": (
        'site:{domain} intitle:"index of"',
        'site:{domain} intitle:"index of" intext:backup | intext:password | intext:sql',
        'site:{domain} intitle:"directory listing for" | inurl:."/"',
    ),
    "open_redirects": (
        "site:{domain} inurl:url= | inurl:return= | inurl:next= | inurl:redirect=",
        "site:{domain} inurl:navigate= | inurl:goto= | inurl:link= | inurl:destination=",
    ),
    "sql_errors": (
        'site:{domain} intext:"sql syntax near" | intext:"syntax error has occurred"',
        'site:{domain} intext:"incorrect syntax near" | intext:"unexpected end of sql command"',
        'site:{domain} intext:"warning: mysql_connect()" | intext:"warning: mysql_query()"',
        'site:{domain} intext:"warning: pg_connect()" | intext:"odbc drivers error"',
    ),
    "phpinfo": (
        'site:{domain} ext:php intitle:phpinfo "published by the php group"',
        "site:{domain} intitle:phpinfo | ext:php inurl:info.php",
    ),
    "exposed_files": (
        "site:{domain} filetype:xls | filetype:xlsx | filetype:doc | filetype:pdf",
        "site:{domain} filetype:sql | filetype:config | filetype:ini | filetype:env",
        "site:{domain} filetype:bak | filetype:old | filetype:zip | filetype:tar",
        "site:{domain} ext:logs | ext:log | ext:conf | ext:yml | ext:json",
        'site:{domain} intitle:"password change" | intext:prueba | intext:credentials',
        "site:{domain} filetype:conf inurl:wp-config | inurl:database.yml | inurl:settings.py",
        "site:{domain} filetype:reg inurl:hkey_local_machine | inurl:hkey_current_user",
    ),
    "leaked_keys": (
        "site:{domain} aws_access_key_id | aks sk | api_key | apikey | api key",
        "site:{domain} amzn mws | jdbc | dbpassword | dbuser | authorization bearer",
        "site:{domain} sa | inurl Dillon | secret_key | private key | secret key",
    ),
    "github_org": (
        '"{domain}" org:{org}',
        '"password" org:{org} filename:.env',
        '"aws_secret_access_key" org:{org}',
        '"api_key" OR "apikey" org:{org} filename:config',
    ),
}


def categories() -> tuple[str, ...]:
    """Return every supported dork category."""
    return CATEGORIES


def queries(category: str, domain: str, org: str = "") -> tuple[str, ...]:
    """Render the dork queries for one category against one target.

    Args:
        category: One of the names returned by :func:`categories`.
        domain: Target domain to scope with ``site:``.
        org: GitHub organisation name for the ``github_org`` category;
            falls back to ``domain`` when empty.

    Returns:
        Rendered queries capped at ``MAX_QUERIES_PER_CATEGORY``; empty when
        the domain is empty or the category is unknown.
    """
    domain = str(domain or "").strip().lower()
    org = str(org or "").strip().lower() or domain
    category = str(category or "").strip().lower()
    if not domain or category not in _GRAMMAR:
        return ()
    rendered = tuple(fixture.format(domain=domain, org=org) for fixture in _GRAMMAR[category] if fixture)
    return rendered[:MAX_QUERIES_PER_CATEGORY]


def all_queries(domain: str, org: str = "") -> dict[str, tuple[str, ...]]:
    """Render the full grammar for one target.

    Args:
        domain: Target domain to scope with ``site:``.
        org: GitHub organisation name; falls back to ``domain``.

    Returns:
        Mapping of category name to rendered queries (only populated sets).
    """
    org = str(org or "").strip().lower() or domain
    return {category: queries(category, domain, org) for category in CATEGORIES if queries(category, domain, org)}


def write_report(path: Path | str, domain: str, org: str = "") -> dict[str, Any]:
    """Persist the rendered dorks as a markdown playbook.

    Args:
        path: Destination file (created/overwritten).
        domain: Target domain.
        org: GitHub organisation; falls back to ``domain``.

    Returns:
        Mapping with ``written`` (query count), ``path`` and ``error``.
    """
    mapping = all_queries(domain, org)
    if not mapping:
        return {"written": 0, "path": "", "error": "no dorks rendered"}
    lines: list[str] = [f"# LazyDorks: {domain}", ""]
    for category, items in mapping.items():
        lines.append(f"## {category}")
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    try:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines), encoding="utf-8")
    except Exception as exc:
        return {"written": 0, "path": "", "error": str(exc)}
    return {"written": sum(len(v) for v in mapping.values()), "path": str(target), "error": ""}


if __name__ == "__main__":
    import sys

    domain_arg = sys.argv[1] if len(sys.argv) > 1 else ""
    for category_name, items in all_queries(domain_arg).items():
        print(f"== {category_name}")
        for item in items:
            print(f"  {item}")
