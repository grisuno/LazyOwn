{
    "toolname": "gobuster_http",
    "command": "gobuster dir -u http://{ip}:{port} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o {outputdir}/gobuster_{port}.txt",
    "trigger": ["http", "http-proxy", "https-alt", "https"],
    "active": true
}