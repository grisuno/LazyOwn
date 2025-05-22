{
	"toolname": "showmount_tool",
	"command": "showmount -e {domain} | tee {outputdir}/{toolname}.txt",
	"trigger": ["nfs_acl", "nfs"],
	"active": true
}
