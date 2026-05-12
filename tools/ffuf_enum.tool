{
  "toolname": "ffuf_enumeration",
  "command": "ffuf -u http{s}://{ip}:{port}/FUZZ -w {dirworlist} -mc 200,302,403 -timeout 10 > {outputdir}/ffuf.txt",
  "trigger": [
    "http",
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: ffuf_enumeration \u2014 triggers on ['http', 'https']"
}