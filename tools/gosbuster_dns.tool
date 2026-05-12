{
  "toolname": "gobuster_dns",
  "command": "gobuster dns -r http{s}://{ip}:{port} -d {domain} -w {dirworlist} -t 200 | tee {outputdir}/gobuster_web.txt",
  "trigger": [
    "http",
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: gobuster_dns \u2014 triggers on ['http', 'https']"
}