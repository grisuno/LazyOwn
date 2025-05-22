{
    "toolname": "nxc_idap_tool",
    "command": "nxc idap {ip} -u {username} -p '{password}' > {outputdir}/nxc_idap.txt",
    "trigger": ["ldap", "ldaps"],
    "active": true
}