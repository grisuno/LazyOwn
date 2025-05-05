{
    "toolname": "nuclei_ad_http",
    "command": "nuclei -u http{s}://{ip}:{port} -t ../nuclei-templates/  > {outputdir}/nuclei_ad_http.txt",
    "trigger": ["http", "https", "http-rpc-epmap", "adws"],
    "active": true
}