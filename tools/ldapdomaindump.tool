{
  "toolname": "ldap_domain_dump_tool",
  "command": "ldapdomaindump -u {domain}\\{username} -p '{password}' -o {outputdir} ldap://{ip} > {outputdir}/ldapdomaindump.txt",
  "trigger": [
    "ldap"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: ldap_domain_dump_tool \u2014 triggers on ['ldap']"
}