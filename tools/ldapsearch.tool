{
	"toolname": "ldapsearch",
	"command": "ldapsearch -x -H ldap://{ip} -b 'dc={nameserver},dc={ext}' -s sub | tee {outputdir}/{toolname}.txt",
	"trigger": ["ldap"],
	"active": true
}
