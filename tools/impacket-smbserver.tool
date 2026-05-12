{
  "toolname": "smbserver_tool",
  "command": "sudo impacket-smbserver kali $(pwd) > {outputdir}/smbserver.log &",
  "trigger": [
    "microsoft-ds"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: smbserver_tool \u2014 triggers on ['microsoft-ds']"
}