{
  "toolname": "enum4linux_tool",
  "command": "enum4linux -a {ip} > {outputdir}/enum4linux.txt",
  "trigger": [
    "microsoft-ds",
    "netbios-ssn"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: enum4linux_tool \u2014 triggers on ['microsoft-ds', 'netbios-ssn']"
}