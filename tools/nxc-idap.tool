{
    "toolname": "nxc_idap",
    "command": "nxc idap {ip} -u {username} -p '{password}' > {outputdir}/nxc_idap.txt",
    "trigger": ["ldap", "ldaps"],
    "active": true
}