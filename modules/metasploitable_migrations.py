"""Idempotent migrations for the Metasploitable 2 gym container.

The stock ``tleemcjr/metasploitable2`` image boots only a subset of the
services the gym matrix expects, and several exercises need small lab
adjustments (open X display, anonymous FTP, a deliberately vulnerable CGI
script, a PHP URL-include fixture and a populated mutillidae database).
Each migration below is idempotent: it first checks whether the fix is
already in place and only applies the change when it is not, so running
the migrations on every gym start is safe and cheap.

Execution goes through ``docker exec`` in argv form (no shell on the
operator side). Every step reports its own status; a failing step never
blocks the rest.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.safe_exec import safe_run_argv

DEFAULT_CONTAINER = "lazyown-lab-metasploitable"
DEFAULT_DOCKER_SUBNET = "172.17.0."
XVNC_LOG = "/root/.lz_xvnc.log"
DISTCCD_LOG = "/tmp/.lz_distccd.log"
CGI_STATUS = "/usr/lib/cgi-bin/status"
RFI_PAYLOAD = "/var/www/ms2_rfi.txt"
DVWA_DOM_PAGE = "/var/www/dvwa/vulnerabilities/xss_d/index.php"
PHP_INI_CGI = "/etc/php5/cgi/php.ini"
PHP_INI_APACHE = "/etc/php5/apache2/php.ini"
MUTILLIDAE_SETUP_URL = "http://127.0.0.1/mutillidae/set-up-database.php"
MUTILLIDAE_DB = "metasploit"
MUTILLIDAE_SOURCE_DB = "owasp10"
XVNC_COMMAND = (
    "Xtightvnc :0 -desktop X -ac -auth /root/.Xauthority -geometry 1024x768 "
    "-depth 24 -rfbwait 120000 -rfbauth /root/.vnc/passwd -rfbport 5900 "
    "-fp /usr/share/X11/fonts/misc,/usr/share/fonts/X11/misc/ -co /etc/X11/rgb"
)

DVWA_DOM_PHP = """<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<!DOCTYPE html>
<html>
<head><title>DVWA DOM XSS (lab build)</title></head>
<body>
<div id="helper" style="display:none"></div>
<h1>DOM XSS</h1>
<select id="default" onchange="Quiz(this,'English')">
<script>
if (document.location.search.indexOf("default=") != -1) {
 document.write("<option value='" + decodeURIComponent(document.location.search.substring(document.location.search.indexOf("default=")+8)) + "'>");
 document.write("</option>");
}
document.write("<option value='English'>English</option>");
</script>
</select>
</body>
</html>
"""


@dataclass(frozen=True)
class Migration:
    """One idempotent gym fix: a check script and an apply script.

    Attributes:
        id: Stable migration identifier used in reports.
        description: Human-readable summary.
        check: Shell script run inside the container; exit 0 means the
            migration is already applied.
        apply: Shell script run inside the container when the check
            fails (or when there is no check).
        payload: Optional stdin content handed to the apply script
            (used by file-writing migrations with ``cat > path``).
    """

    id: str
    description: str
    check: str = ""
    apply: str = ""
    payload: str = ""


def _docker_exec(
    container: str,
    script: str,
    payload: str = "",
    timeout: float = 120,
) -> tuple[int, str]:
    """Run one shell script inside a container via argv-form docker exec.

    Args:
        container: Container name.
        script: Shell script text executed with ``sh -c``.
        payload: Optional stdin content.
        timeout: Wall-clock timeout in seconds.

    Returns:
        Tuple of (return code, combined stdout+stderr).
    """
    argv = ["docker", "exec", "-i", container, "sh", "-c", script]
    try:
        completed = safe_run_argv(
            argv,
            timeout=timeout,
            input_data=payload or None,
        )
    except Exception as exc:
        return 125, str(exc)[:300]
    output = ((completed.stdout or "") + (completed.stderr or "")).strip()
    return completed.returncode, output


def _core_services_apply() -> str:
    """Return the idempotent service-start script for the gym core."""
    return "\n".join(
        [
            "for s in apache2 xinetd proftpd postfix mysql portmap; do "
            "/etc/init.d/$s start >/dev/null 2>&1 || true; done",
            "/etc/init.d/samba start >/dev/null 2>&1 || true",
            "/etc/init.d/postgresql-8.3 start >/dev/null 2>&1 || true",
            "/etc/init.d/tomcat5.5 start >/dev/null 2>&1 || true",
            "pgrep -x distccd >/dev/null 2>&1 || "
            f"distccd --daemon --allow 0.0.0.0/0 >{DISTCCD_LOG} 2>&1 || true",
        ]
    )


def build_migrations(subnet: str = DEFAULT_DOCKER_SUBNET) -> tuple[Migration, ...]:
    """Return the ordered migration list with the docker subnet applied.

    Args:
        subnet: IPv4 prefix of the lab docker network (hosts.allow
            entries use it as the trusted client list).

    Returns:
        Ordered tuple of :class:`Migration` steps.
    """
    hosts_allow = "\n".join(
        [
            'for svc in in.telnetd in.rlogind in.rshd in.rexecd; do',
            ' grep -q "^$svc" /etc/hosts.allow || printf "%s: {subnet}\\n" "$svc" >> /etc/hosts.allow',
            "done",
            "for i in 0 1 2 3 4 5; do grep -q \"pts/$i\" /etc/securetty || echo \"pts/$i\" >> /etc/securetty; done",
        ]
    ).replace("{subnet}", subnet)
    return (
        Migration(
            id="core-services",
            description="Start the gym core daemons (apache2, xinetd, proftpd, postfix, mysql, portmap, samba, postgresql, tomcat, distccd)",
            apply=_core_services_apply(),
        ),
        Migration(
            id="rservices-access",
            description="Allow telnet/rlogin/rsh/exec from the docker subnet and trust pts devices",
            check="grep -q '^in.telnetd' /etc/hosts.allow && grep -q '^pts/5' /etc/securetty",
            apply=hosts_allow,
        ),
        Migration(
            id="proftpd-anonymous",
            description="Enable anonymous FTP access in proftpd",
            check="grep -q '<Anonymous' /etc/proftpd/proftpd.conf",
            apply="\n".join(
                [
                    "grep -q '<Anonymous' /etc/proftpd/proftpd.conf || cat >> /etc/proftpd/proftpd.conf <<'LZEOF'",
                    "<Anonymous ~ftp>",
                    "  User ftp",
                    "  Group nogroup",
                    "  UserAlias anonymous ftp",
                    "  RequireValidShell off",
                    "</Anonymous>",
                    "LZEOF",
                    "/etc/init.d/proftpd restart >/dev/null 2>&1 || true",
                ]
            ),
        ),
        Migration(
            id="xvnc-open",
            description="Restart Xtightvnc with an open display (-ac) and a valid font path",
            check='ps aux | grep "[X]tightvnc" | grep -q " -ac "',
            apply="\n".join(
                [
                    "pkill -f Xtightvnc 2>/dev/null || true",
                    "sleep 1",
                    f"(nohup {XVNC_COMMAND} >{XVNC_LOG} 2>&1 &)",
                    "sleep 2",
                ]
            ),
        ),
        Migration(
            id="shellshock-cgi",
            description="Install a deliberately vulnerable bash CGI script",
            check=f"test -x {CGI_STATUS}",
            apply=f'printf "#!/bin/bash\\necho \\"Content-Type: text/plain\\"\\necho \\"\\"\\necho \\"status: OK\\"\\n" > {CGI_STATUS} && chmod 755 {CGI_STATUS}',
        ),
        Migration(
            id="mutillidae-rfi-payload",
            description="Install the mutillidae remote-include payload file",
            check=f"test -f {RFI_PAYLOAD}",
            apply=f'printf "<?php echo \\"RFI_SHELL_MARKER;\\"; echo shell_exec(\\"id\\"); ?>\\n" > {RFI_PAYLOAD}',
        ),
        Migration(
            id="php-allow-url-include",
            description="Enable allow_url_include in php.ini for cgi and apache2",
            check=f"grep -q '^allow_url_include = On' {PHP_INI_CGI} && grep -q '^allow_url_include = On' {PHP_INI_APACHE}",
            apply="\n".join(
                [
                    f'sed -i "s/^allow_url_include = Off/allow_url_include = On/" {PHP_INI_CGI} {PHP_INI_APACHE}',
                    "/etc/init.d/apache2 restart >/dev/null 2>&1 || true",
                ]
            ),
        ),
        Migration(
            id="mutillidae-database",
            description="Populate the mutillidae database and mirror owasp10 into metasploit",
            check=f'mysql -u root -N -e "SHOW TABLES FROM {MUTILLIDAE_DB}" 2>/dev/null | grep -q "^blogs_table$"',
            apply="\n".join(
                [
                    f"curl -s {MUTILLIDAE_SETUP_URL} >/dev/null 2>&1 || true",
                    f"mysqldump -u root {MUTILLIDAE_SOURCE_DB} 2>/dev/null | mysql -u root {MUTILLIDAE_DB} || true",
                ]
            ),
        ),
        Migration(
            id="dvwa-dom-page",
            description="Install the canonical DVWA DOM XSS page (missing from this DVWA build)",
            check=f"test -f {DVWA_DOM_PAGE}",
            apply=f"mkdir -p $(dirname {DVWA_DOM_PAGE}) && cat > {DVWA_DOM_PAGE}",
            payload=DVWA_DOM_PHP,
        ),
    )


def apply_migrations(
    container: str = DEFAULT_CONTAINER,
    subnet: str = DEFAULT_DOCKER_SUBNET,
) -> dict[str, dict[str, Any]]:
    """Run every migration on the gym container, skipping applied ones.

    Args:
        container: Gym container name.
        subnet: Docker subnet prefix handed to the hosts.allow entries.

    Returns:
        Mapping of migration id to ``{"applied": bool, "skipped": bool,
        "detail": str}``; ``applied`` reports the apply script's exit
        status, ``skipped`` marks already-satisfied migrations.
    """
    report: dict[str, dict[str, Any]] = {}
    for migration in build_migrations(subnet):
        if migration.check:
            code, detail = _docker_exec(container, migration.check)
            if code == 0:
                report[migration.id] = {"applied": False, "skipped": True, "detail": "already applied"}
                continue
        code, detail = _docker_exec(container, migration.apply, migration.payload)
        report[migration.id] = {"applied": code == 0, "skipped": False, "detail": detail[:200]}
    return report


__all__ = [
    "Migration",
    "DEFAULT_CONTAINER",
    "DEFAULT_DOCKER_SUBNET",
    "apply_migrations",
    "build_migrations",
]
