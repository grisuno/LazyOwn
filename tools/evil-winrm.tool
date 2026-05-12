{
  "toolname": "evil_winrm_tool",
  "command": "evil-winrm -i {ip} -u {username} -p '{password}' > {outputdir}/evil_winrm.txt",
  "trigger": [
    "winrm"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: evil_winrm_tool \u2014 triggers on ['winrm']"
}