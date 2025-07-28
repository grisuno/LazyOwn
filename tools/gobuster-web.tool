{
    "toolname": "gobuster_web",
    "command": "gobuster dir -u https://{domain} -w {dirworlist} -k -q -o {outputdir}/gobuster_web.txt",
    "trigger": ["http", "https"],
    "active": true
}
