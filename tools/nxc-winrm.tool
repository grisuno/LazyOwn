{
    "toolname": "nxc_winrm",
    "command": "nxc winrm {ip} -u {username} -p '{password}' --timeout 5 > {outputdir}/nxc_winrm.txt",
    "trigger": ["winrm"],
    "active": true
}