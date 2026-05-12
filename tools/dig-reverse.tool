{
  "toolname": "dig_reverse",
  "command": "dig -x {ip} @localhost +noall +answer > {outputdir}/dig_reverse.txt",
  "trigger": [
    "domain"
  ],
  "active": true,
  "category": "01. Reconnaissance",
  "description": "Pwntomate tool: dig_reverse \u2014 triggers on ['domain']"
}