{
  "toolname": "showmount_tool",
  "command": "showmount -e {domain} | tee {outputdir}/{toolname}.txt",
  "trigger": [
    "nfs_acl",
    "nfs"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: showmount_tool \u2014 triggers on ['nfs_acl', 'nfs']"
}