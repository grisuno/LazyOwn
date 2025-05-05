{
    "toolname": "smbclient",
    "command": "smbclient -L //{ip} -N > {outputdir}/smbclient.txt",
    "trigger": ["microsoft-ds", "netbios-ssn"],
    "active": true
}