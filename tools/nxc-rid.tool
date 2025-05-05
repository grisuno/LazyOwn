{
    "toolname": "nxc_rid",
    "command": "nxc smb {ip} -u {username} -p '{password}' --rid-brute > {outputdir}/nxc_rid.txt",
    "trigger": ["microsoft-ds"],
    "active": true
}