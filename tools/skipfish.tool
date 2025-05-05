{
    "toolname": "skipfish_tool",
    "command": "skipfish -o {outputdir} -S /usr/share/skipfish/dictionaries/complete.wl http{s}://{ip}:{port}",
    "trigger": ["http", "https", "http-mgmt", "http-alt"],
    "active": false
}
