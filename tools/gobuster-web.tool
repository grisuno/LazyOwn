{
  "toolname": "gobuster_web",
  "command": "gobuster dir -u https://{domain} -w {dirworlist} -k -q -o {outputdir}/gobuster_web.txt",
  "trigger": [
    "http",
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: gobuster_web \u2014 triggers on ['http', 'https']"
}