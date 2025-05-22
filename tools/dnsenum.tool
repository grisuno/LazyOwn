{
    "toolname": "dns_enum_tool",
    "command": "dnsenum --dnsserver {ip} --enum {domain} {dnswordlist} > {outputdir}/dnsenum.txt",
    "trigger": ["domain"],
    "active": true
}