{
    "toolname": "dns_enum",
    "command": "dnsenum --dnsserver {ip} --enum {domain} {dnswordlist} > {outputdir}/dnsenum.txt",
    "trigger": ["domain"],
    "active": true
}