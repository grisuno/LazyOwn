{
    "toolname": "nxc_null_session",
    "command": "nxc smb {ip} -u '' -p '' --shares > {outputdir}/nxc_null.txt",
    "trigger": ["microsoft-ds"],
    "active": true
}