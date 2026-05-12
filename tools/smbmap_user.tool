{
  "toolname": "smb_map",
  "command": "smbmap -H {ip} -u {username} -p '{password}' -R > {outputdir}/smbmap.txt",
  "trigger": [
    "microsoft-ds"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: smb_map \u2014 triggers on ['microsoft-ds']"
}