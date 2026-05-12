{
  "toolname": "rpcclient_tool",
  "command": "rpcclient -U '' -N {ip} > {outputdir}/rpcclient_nullsession.txt",
  "trigger": [
    "msrpc"
  ],
  "active": true,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: rpcclient_tool \u2014 triggers on ['msrpc']"
}