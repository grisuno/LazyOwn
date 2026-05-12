{
  "toolname": "ollama_enum",
  "command": "curl -s http{s}://{ip}:{port}/api/tags 2>/dev/null | python3 -m json.tool > {outputdir}/ollama_tags.txt 2>&1; curl -s http{s}://{ip}:{port}/api/ps 2>/dev/null | python3 -m json.tool >> {outputdir}/ollama_tags.txt 2>&1; curl -s http{s}://{ip}:{port}/api/version >> {outputdir}/ollama_tags.txt 2>&1",
  "trigger": [
    "http",
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: ollama_enum \u2014 triggers on ['http', 'https']"
}