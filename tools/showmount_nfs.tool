{
  "toolname": "showmount_nfs",
  "command": "showmount -e {ip} > {outputdir}/nfs_exports.txt",
  "trigger": [
    "nfs"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: showmount_nfs \u2014 triggers on ['nfs']"
}