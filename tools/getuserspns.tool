{
    "toolname": "GetUserSPNs.py",
    "command": "GetUserSPNs.py {domain}/{username}:{password} -dc-ip {ip} -request > {outputdir}/getNPUsers.txt",
    "trigger": ["kerberos-sec"],
    "active": true
}