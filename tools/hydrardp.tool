{
  "toolname": "hydrardp_tool",
  "command": "hydra -L sessions/users.txt -P /usr/share/wordlists/rockyou.txt rdp://{ip}:{port} > {outputdir}/{toolname}.txt",
  "trigger": [
    "rdp"
  ],
  "active": true,
  "category": "08. Lateral Movement",
  "description": "Pwntomate tool: hydrardp_tool \u2014 triggers on ['rdp']"
}