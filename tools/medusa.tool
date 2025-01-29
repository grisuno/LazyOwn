{
    "toolname": "medusa",
    "command": "medusa -h {ip} -U sessions/users.txt -P /usr/share/wordlists/rockyou.txt -e ns -M ssh -n {port} -r 11 -t 4 > {outputdir}/{toolname}.txt",
    "trigger": [],
    "active": false
}