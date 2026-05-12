{
  "toolname": "dirb_tool",
  "command": "dirb http{s}://{ip}:{port} -o {outputdir}/{toolname}.txt -f",
  "trigger": [
    "http",
    "https",
    "http-mgmt",
    "http-alt"
  ],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: dirb_tool \u2014 triggers on ['http', 'https', 'http-mgmt', 'http-alt']"
}