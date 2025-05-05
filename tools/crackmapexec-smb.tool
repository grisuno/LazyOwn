{
    "toolname": "crackmapexec_smb",
    "command": "crackmapexec smb {ip} -u sessions/users.txt -p '{password}' --shares > {outputdir}/cme_smb.txt",
    "trigger": ["microsoft-ds", "netbios-ssn"],
    "active": true
}