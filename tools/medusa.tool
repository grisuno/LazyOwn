{
  "toolname": "medusa_tool",
  "command": "medusa -h {ip} -U sessions/users.txt -P /usr/share/wordlists/rockyou.txt -e ns -M ssh -n {port} -r 11 -t 4 > {outputdir}/{toolname}.txt",
  "trigger": [],
  "active": false,
  "category": "15. Pwntomate Tools",
  "description": "Pwntomate tool: medusa_tool \u2014 triggers on []"
}