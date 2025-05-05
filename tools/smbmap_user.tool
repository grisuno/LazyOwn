{
    "toolname": "smb_map",
    "command": "smbmap -H {ip} -u {username} -p '{password}' -R > {outputdir}/smbmap.txt",
    "trigger": ["microsoft-ds"],
    "active": true
}