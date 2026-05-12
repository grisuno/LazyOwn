{
  "toolname": "kerbrute_tool",
  "command": "kerbrute passwordspray -d {domain} --dc {ip} {usrwordlist} '{password}' > {outputdir}/kerbrute.txt",
  "trigger": [
    "kerberos-sec"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: kerbrute_tool \u2014 triggers on ['kerberos-sec']"
}