{
  "toolname": "enum_smb",
  "command": "crackmapexec smb {ip} --shares > {outputdir}/smb_enum.txt",
  "trigger": [
    "microsoft-ds"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: enum_smb \u2014 triggers on ['microsoft-ds']"
}