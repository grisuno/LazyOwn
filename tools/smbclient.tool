{
  "toolname": "smbclient_tool",
  "command": "smbclient -L //{ip} -N > {outputdir}/smbclient.txt",
  "trigger": [
    "microsoft-ds",
    "netbios-ssn"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: smbclient_tool \u2014 triggers on ['microsoft-ds', 'netbios-ssn']"
}