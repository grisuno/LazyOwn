{
  "toolname": "wkhtmltopdf_tool",
  "command": "wkhtmltopdf {ip}:{port} {outputdir}/{toolname}.pdf",
  "trigger": [
    "http",
    "https",
    "http-mgmt",
    "http-alt"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: wkhtmltopdf_tool \u2014 triggers on ['http', 'https', 'http-mgmt', 'http-alt']"
}