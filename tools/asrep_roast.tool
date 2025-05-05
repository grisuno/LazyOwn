{
    "toolname": "asrep_roast",
    "command": "GetNPUsers.py {domain}/ -no-pass -dc-ip {ip} -request > {outputdir}/asreproast_hashes.txt",
    "trigger": ["ldap", "kerberos-sec"],
    "active": true
}