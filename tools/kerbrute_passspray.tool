{
    "toolname": "kerbrute_tool",
    "command": "kerbrute passwordspray -d {domain} --dc {ip} {usrwordlist} '{password}' > {outputdir}/kerbrute.txt",
    "trigger": ["kerberos-sec"],
    "active": true
}