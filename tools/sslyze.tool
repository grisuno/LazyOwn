{
  "toolname": "sslyze_tool",
  "command": "sslyze --regular --xml_out=- {ip}:{port} > {outputdir}/{toolname}.xml",
  "trigger": [
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: sslyze_tool \u2014 triggers on ['https']"
}
