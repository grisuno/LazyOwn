{
    "toolname": "ldapsearch_anon",
    "command": "ldapsearch -x -b \"\" -s base -H ldap://{ip}:389 > {outputdir}/ldap_anon.txt",
    "trigger": ["ldap"],
    "active": true
}