{
    "toolname": "smb_ghost",
    "command": "python3 /usr/share/exploitdb/scripts/smbghost_scanner.py {ip} > {outputdir}/smbghost.txt",
    "trigger": ["microsoft-ds"],
    "active": true
}