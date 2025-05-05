{
    "toolname": "bloodhound-python",
    "command": "bloodhound-python -u {username} -p '{password}' -d {domain} -ns {ip} --zip -c All > {outputdir}/bloodhound_py.txt",
    "trigger": ["ldap", "kerberos-sec"],
    "active": true
}