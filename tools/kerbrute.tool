{
  "toolname": "kerbrute_tool_user",
  "command": "kerbrute userenum --dc {ip} -d {domain} -t 20  /usr/share/wordlists/SecLists-master/Usernames/xato-net-10-million-usernames.txt | tee {outputdir}/{toolname}.txt",
  "trigger": [
    "kerberos-sec"
  ],
  "active": true,
  "category": "07. Credential Access",
  "description": "Pwntomate tool: kerbrute_tool_user \u2014 triggers on ['kerberos-sec']"
}