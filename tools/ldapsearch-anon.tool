{
  "toolname": "ldapsearch_anon",
  "command": "ldapsearch -x -b \"\" -s base -H ldap://{ip}:389 > {outputdir}/ldap_anon.txt",
  "trigger": [
    "ldap"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: ldapsearch_anon \u2014 triggers on ['ldap']"
}