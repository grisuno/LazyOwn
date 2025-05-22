{
    "toolname": "getNPUsers_tool",
    "command": "GetNPUsers.py {domain}/{username}:{password} -dc-ip {ip} -request > {outputdir}/getNPUsers.txt",
    "trigger": ["kerberos-sec"],
    "active": true
}