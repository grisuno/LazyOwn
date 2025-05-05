{
    "toolname": "evil_winrm",
    "command": "evil-winrm -i {ip} -u {username} -p '{password}' > {outputdir}/evil_winrm.txt",
    "trigger": ["winrm"],
    "active": true
}