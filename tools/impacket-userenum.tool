{
  "toolname": "userEnum_tool",
  "command": "nxc smb {ip} -u '' -p '' --users > {outputdir}/nxc_users.txt",
  "trigger": [
    "microsoft-ds"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: userEnum_tool \u2014 triggers on ['microsoft-ds']"
}