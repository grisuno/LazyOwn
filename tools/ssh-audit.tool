{
  "toolname": "ssh-audit",
  "command": "ssh-audit {ip}:{port} > {outputdir}/{toolname}.txt",
  "trigger": [
    "ssh"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: ssh-audit \u2014 triggers on ['ssh']"
}