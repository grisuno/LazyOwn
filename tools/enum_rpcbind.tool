{
  "toolname": "enum_rpcbind",
  "command": "rpcinfo -p {ip} > {outputdir}/rpc_services.txt",
  "trigger": [
    "rpcbind"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: enum_rpcbind \u2014 triggers on ['rpcbind']"
}