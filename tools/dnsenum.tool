{
  "toolname": "dns_enum_tool",
  "command": "dnsenum --dnsserver {ip} --enum {domain} {dnswordlist} > {outputdir}/dnsenum.txt",
  "trigger": [
    "domain"
  ],
  "active": true,
  "category": "01. Reconnaissance",
  "description": "Pwntomate tool: dns_enum_tool \u2014 triggers on ['domain']"
}