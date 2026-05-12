{
  "toolname": "crackmapexec_smb",
  "command": "crackmapexec smb {ip} -u sessions/users.txt -p '{password}' --shares > {outputdir}/cme_smb.txt",
  "trigger": [
    "microsoft-ds",
    "netbios-ssn"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: crackmapexec_smb \u2014 triggers on ['microsoft-ds', 'netbios-ssn']"
}