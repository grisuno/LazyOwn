{
    "toolname": "nxc_pass_policy",
    "command": "nxc smb {ip} -u {username} -p '{password}' --pass-pol > {outputdir}/nxc_passpol.txt",
    "trigger": ["microsoft-ds"],
    "active": true
}