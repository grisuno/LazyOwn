{
  "toolname": "smbclient_list",
  "command": "smbclient -L \\\\\\\\{ip}\\\\ -N > {outputdir}/smb_shares.txt",
  "trigger": [
    "microsoft-ds"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: smbclient_list \u2014 triggers on ['microsoft-ds']"
}