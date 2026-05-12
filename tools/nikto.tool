{
  "toolname": "nikto_tool",
  "command": "nikto -ask no -host {ip} -port {port} -output {outputdir}/{toolname}.html",
  "trigger": [
    "http",
    "https",
    "http-mgmt",
    "http-alt"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: nikto_tool \u2014 triggers on ['http', 'https', 'http-mgmt', 'http-alt']"
}