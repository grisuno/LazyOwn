{
  "toolname": "nikto_host",
  "command": "nikto -h {ip} -p {port}{ssl_flag} > {outputdir}/nikto.txt",
  "trigger": [
    "http",
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: nikto_host \u2014 triggers on ['http', 'https']"
}