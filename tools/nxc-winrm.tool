{
  "toolname": "nxc_winrm",
  "command": "nxc winrm {ip} -u {username} -p '{password}' --timeout 5 > {outputdir}/nxc_winrm.txt",
  "trigger": [
    "winrm"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: nxc_winrm \u2014 triggers on ['winrm']"
}