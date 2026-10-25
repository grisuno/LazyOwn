{
  "toolname": "nuclei_templates_cve",
  "command": "nuclei -u http{s}://{ip}:{port} -t external/.exploit/nuclei-templates/http/cves/ -severity critical,high -silent -o {outputdir}/nuclei_templates_cve.txt",
  "trigger": [
    "http",
    "https"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: nuclei_templates_cve \u2014 triggers on ['http', 'https']"
}
