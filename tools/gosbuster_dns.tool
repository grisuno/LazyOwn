{
  "toolname": "gobuster_dns",
  "command": "gobuster dns -d {domain} -w {dirworlist} -t 200 -o {outputdir}/gobuster_dns.txt",
  "trigger": [
    "http",
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: gobuster_dns \u2014 triggers on ['http', 'https']"
}
