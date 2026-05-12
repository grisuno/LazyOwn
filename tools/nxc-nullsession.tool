{
  "toolname": "nxc_null_session",
  "command": "nxc smb {ip} -u '' -p '' --shares > {outputdir}/nxc_null.txt",
  "trigger": [
    "microsoft-ds"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: nxc_null_session \u2014 triggers on ['microsoft-ds']"
}