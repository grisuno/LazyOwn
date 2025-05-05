{
    "toolname": "dnsrecon_axfr",
    "command": "dnsrecon -d {domain} -t axfr -n {ip} > {outputdir}/dnsrecon_axfr.txt",
    "trigger": ["domain"],
    "active": true
}