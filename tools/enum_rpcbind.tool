{
    "toolname": "enum_rpcbind",
    "command": "rpcinfo -p {ip} > {outputdir}/rpc_services.txt",
    "trigger": ["rpcbind"],
    "active": true
}