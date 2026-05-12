{
  "toolname": "dig_any",
  "command": "dig any {domain} @{ip} | tee {outputdir}/{toolname}.txt",
  "trigger": [
    "domain"
  ],
  "active": true,
  "category": "01. Reconnaissance",
  "description": "Pwntomate tool: dig_any \u2014 triggers on ['domain']"
}