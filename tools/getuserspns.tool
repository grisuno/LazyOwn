{
  "toolname": "GetUserSPNs.py",
  "command": "GetUserSPNs.py {domain}/{username}:{password} -dc-ip {ip} -request > {outputdir}/getNPUsers.txt",
  "trigger": [
    "kerberos-sec"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: GetUserSPNs.py \u2014 triggers on ['kerberos-sec']"
}