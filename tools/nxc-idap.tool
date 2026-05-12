{
  "toolname": "nxc_idap_tool",
  "command": "nxc idap {ip} -u {username} -p '{password}' > {outputdir}/nxc_idap.txt",
  "trigger": [
    "ldap",
    "ldaps"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: nxc_idap_tool \u2014 triggers on ['ldap', 'ldaps']"
}