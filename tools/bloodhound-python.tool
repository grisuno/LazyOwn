{
  "toolname": "bloodhound-python",
  "command": "bloodhound-python -u {username} -p '{password}' -d {domain} -ns {ip} --zip -c All > {outputdir}/bloodhound_py.txt",
  "trigger": [
    "ldap",
    "kerberos-sec"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: bloodhound-python \u2014 triggers on ['ldap', 'kerberos-sec']"
}