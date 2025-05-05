{
    "toolname": "crackmapexec_ldap",
    "command": "crackmapexec ldap {ip} -u {username} -p '{password}' > {outputdir}/cme_ldap.txt",
    "trigger": ["ldap", "ldaps"],
    "active": true
}