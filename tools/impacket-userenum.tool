{
    "toolname": "userEnum_tool",
    "command": "nxc smb {ip} -u '' -p '' --users > {outputdir}/nxc_users.txt",
    "trigger": ["microsoft-ds"],
    "active": true
}