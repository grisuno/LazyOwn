{
  "toolname": "smbmap_tool",
  "command": "smbmap -H {ip} -u '{username}' {password} -A '(xlsx|docx|txt|xml)' -r --no-banner | tee {outputdir}/{toolname}.txt",
  "trigger": [
    "microsoft-ds"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: smbmap_tool \u2014 triggers on ['microsoft-ds']"
}