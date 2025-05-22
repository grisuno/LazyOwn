{
    "toolname": "evil_winrm_tool",
    "command": "evil-winrm -i {ip} -u {username} -p '{password}' > {outputdir}/evil_winrm.txt",
    "trigger": ["winrm"],
    "active": true
}