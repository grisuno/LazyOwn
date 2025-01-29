{
    "toolname": "hydrassh",
    "command": "hydra -L sessions/users.txt -P /usr/share/wordlists/rockyou.txt ssh://{ip}:{port} > {outputdir}/{toolname}.txt",
    "trigger": [],
    "active": false
}