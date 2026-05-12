{
  "toolname": "nxc_rid",
  "command": "nxc smb {ip} -u {username} -p '{password}' --rid-brute > {outputdir}/nxc_rid.txt",
  "trigger": [
    "microsoft-ds"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: nxc_rid \u2014 triggers on ['microsoft-ds']"
}