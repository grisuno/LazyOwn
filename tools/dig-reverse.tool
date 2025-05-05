{
    "toolname": "dig_reverse",
    "command": "dig -x {ip} @localhost +noall +answer > {outputdir}/dig_reverse.txt",
    "trigger": ["domain"],
    "active": true
}