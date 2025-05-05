{
    "toolname": "ldap_domain_dump",
    "command": "ldapdomaindump -u {domain}\\{username} -p '{password}' -o {outputdir} ldap://{ip} > {outputdir}/ldapdomaindump.txt",
    "trigger": ["ldap"],
    "active": true
}