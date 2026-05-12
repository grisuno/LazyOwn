{
  "toolname": "nxc_ldap",
  "command": "nxc ldap {ip} -u {username} -p '{password}' --ldap-shell > {outputdir}/nxc_ldap.txt",
  "trigger": [
    "ldap"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: nxc_ldap \u2014 triggers on ['ldap']"
}