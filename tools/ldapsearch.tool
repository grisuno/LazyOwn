{
  "toolname": "ldapsearch_tool",
  "command": "ldapsearch -x -H ldap://{ip} -b 'dc={nameserver},dc={ext}' -s sub | tee {outputdir}/{toolname}.txt",
  "trigger": [
    "ldap"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: ldapsearch_tool \u2014 triggers on ['ldap']"
}