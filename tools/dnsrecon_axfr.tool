{
  "toolname": "dnsrecon_axfr",
  "command": "dnsrecon -d {domain} -t axfr -n {ip} > {outputdir}/dnsrecon_axfr.txt",
  "trigger": [
    "domain"
  ],
  "active": true,
  "category": "01. Reconnaissance",
  "description": "Pwntomate tool: dnsrecon_axfr \u2014 triggers on ['domain']"
}