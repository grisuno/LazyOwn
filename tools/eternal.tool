{
  "toolname": "etarnalblue",
  "command": "nmap -p {port} --script smb-vuln-ms17-010 {ip} -oN {outputdir}/{toolname}.txt",
  "trigger": [
    "microsoft-ds"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: etarnalblue \u2014 triggers on ['microsoft-ds']"
}