{
    "toolname": "smbserver",
    "command": "sudo impacket-smbserver kali $(pwd) > {outputdir}/smbserver.log &",
    "trigger": ["microsoft-ds"],
    "active": true
}