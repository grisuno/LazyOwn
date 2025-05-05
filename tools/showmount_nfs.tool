{
    "toolname": "showmount_nfs",
    "command": "showmount -e {ip} > {outputdir}/nfs_exports.txt",
    "trigger": ["nfs"],
    "active": true
}