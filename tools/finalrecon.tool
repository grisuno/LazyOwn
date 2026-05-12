{
  "toolname": "finalrecon_tool",
  "command": "finalrecon --url=http{s}://{ip}:{port} --full -o txt -cd {outputdir}/{toolname}/ ",
  "trigger": [
    "http",
    "https",
    "http-mgmt",
    "http-alt"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: finalrecon_tool \u2014 triggers on ['http', 'https', 'http-mgmt', 'http-alt']"
}