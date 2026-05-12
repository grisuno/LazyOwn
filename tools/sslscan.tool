{
  "toolname": "sslscan_tool",
  "command": "sslscan --xml=- {ip}:{port} > {outputdir}/{toolname}.xml",
  "trigger": [
    "https"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: sslscan_tool \u2014 triggers on ['https']"
}