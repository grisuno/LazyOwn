{
    "toolname": "nikto_host",
    "command": "nikto -h {ip} -p {port} -ssl {s} > {outputdir}/nikto.txt",
    "trigger": ["http", "https"],
    "active": true
}