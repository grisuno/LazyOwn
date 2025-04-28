-- Helper function to convert a hex string (e.g., "414243") to a byte string ("ABC")
local function hex_to_bytes(hex_string)
    if type(hex_string) ~= 'string' then return nil end
    hex_string = hex_string:gsub("^%s*", ""):gsub("%s*$", "") -- Trim whitespace
    hex_string = hex_string:gsub("[^0-9a-fA-F]", "") -- Remove non-hex characters after trimming
    if #hex_string % 2 ~= 0 then
        return nil -- Invalid: odd number of hex characters
    end
    local bytes = ""
    for i = 1, #hex_string, 2 do
        local byte_hex = hex_string:sub(i, i + 1)
        local byte_value = tonumber(byte_hex, 16)
        if byte_value == nil then return nil end -- Should not happen with current gsub, but safety
        bytes = bytes .. string.char(byte_value)
    end
    return bytes
end

-- Helper function to convert a string with \xNN escapes (e.g., "\\x48\\x31\\xc0") to a byte string
-- Note: The input string here contains literal '\' and 'x', not interpreted escapes.
local function esc_hex_to_bytes(esc_hex_string)
    if type(esc_hex_string) ~= 'string' then return nil end

    local bytes = ""
    local i = 1
    while i <= #esc_hex_string do
        -- Look for "\x" pattern
        if esc_hex_string:sub(i, i + 1) == "\\x" then
            -- Check if there are two more characters for hex digits
            if i + 3 <= #esc_hex_string then
                local hex_pair = esc_hex_string:sub(i + 2, i + 3)
                -- Check if the next two characters are hex digits
                if hex_pair:match("^[0-9a-fA-F][0-9a-fA-F]$") then
                    local byte_value = tonumber(hex_pair, 16)
                    bytes = bytes .. string.char(byte_value)
                    i = i + 4 -- Skip the "\xNN" sequence
                else
                    -- Not a valid hex pair after \x, maybe report error or skip?
                    -- For now, skip the '\x' and continue, maybe indicate warning later
                    -- print("Warning: Invalid hex pair after \\x at index " .. i .. ": " .. hex_pair)
                    bytes = bytes .. esc_hex_string:sub(i, i+1) -- Include the literal "\x"
                    i = i + 2
                end
            else
                -- "\x" at end of string, not followed by two hex chars
                -- print("Warning: Incomplete \\x escape at end of string")
                bytes = bytes .. esc_hex_string:sub(i, #esc_hex_string) -- Include remaining part
                i = #esc_hex_string + 1 -- Exit loop
            end
        else
            -- Not "\x", just append the character
            bytes = bytes .. esc_hex_string:sub(i, i)
            i = i + 1
        end
    end

     -- Optional: Check if the resulting string seems like it was intended to be only bytes
     -- If it contains non-byte characters, it might indicate mixed input or parsing issue.
     -- For this use case (shellcode), the result should ideally only contain byte values <= 255.

    return bytes
end

-- Helper function to convert a comma-separated hex string (e.g., "00,0A,FF") to a table of byte values
local function hex_list_to_byte_values(hex_list_string)
    if type(hex_list_string) ~= 'string' then return {} end
    local byte_values = {}
    -- Split by comma or whitespace and match hex parts
    for hex_byte in hex_list_string:gmatch("[%s]*,[%s]*|[%s]*([0-9a-fA-F]+)") do
        local byte_value = tonumber(hex_byte, 16)
        if byte_value ~= nil then
            table.insert(byte_values, byte_value)
        end
    end
    return byte_values
end


-- The main plugin function
-- Receives arguments as separate strings via varargs (...)
function validate_shellcode(...)
    local args = {}
    -- Manually parse varargs looking for key=value pairs
    for i = 1, select('#', ...) do
        local arg_str = select(i, ...)
        local key, value = arg_str:match("^([^=]+)=(.*)$")
        if key then
            key = key:gsub("^%s*", ""):gsub("%s*$", "") -- Trim key
            value = value:gsub("^%s*", ""):gsub("%s*$", "") -- Trim value
            args[key] = value
        end
    end

    local shellcode_data = nil
    local source_desc = "input"

    -- --- Input Handling (Ahora con 3 opciones) ---
    if args.file then
        local filename = args.file
        local file = io.open(filename, "rb") -- Open in binary read mode
        if file then
            shellcode_data = file:read("*a") -- Read entire file as a string of bytes
            file:close()
            source_desc = "file '" .. filename .. "'"
        else
            return "Error: No se pudo abrir el archivo: " .. filename
        end
    elseif args.hex_string then
        -- Input is a pure hex string, convert it to bytes
        shellcode_data = hex_to_bytes(args.hex_string)
        if not shellcode_data then
             return "Error: Cadena hexadecimal pura inválida o de longitud impar."
        end
        source_desc = "pure hex string input"
    elseif args.esc_hex_string then
         -- Input is a string with \xNN escapes, parse it to bytes
         shellcode_data = esc_hex_to_bytes(args.esc_hex_string)
         if not shellcode_data then
              return "Error: La cadena con escapes \\xNN no pudo ser parseada correctamente."
         end
         source_desc = "escaped hex string input"
    else
        -- If none of the recognized key=value args were provided
        return "Uso: validate_shellcode file=<ruta_archivo> | hex_string=<cadena_hex> | esc_hex_string=<cadena_con_escapes>" ..
               "\nEjemplo (archivo): validate_shellcode file=shellcode.bin" ..
               "\nEjemplo (hex puro): validate_shellcode hex_string=4831C04831FF..." ..
               "\nEjemplo (\\x escapes): validate_shellcode esc_hex_string=\"\\x48\\x31\\xc0\\x48\\x31\\xff...\"" ..
               "\nEjemplo (bad bytes): validate_shellcode file=shellcode.bin bad_bytes=00,0a,0d,ff" ..
               "\nEjemplo (max len): validate_shellcode file=shellcode.bin max_len=1024"
    end

    if not shellcode_data or #shellcode_data == 0 then
        return "Error: No se cargaron datos de shellcode del " .. source_desc .. "."
    end

    -- --- Configuration ---
    local max_len = tonumber(args.max_len) or 512 -- Default max length
    local bad_byte_values = hex_list_to_byte_values(args.bad_bytes)
    -- Add null byte (0x00) to bad bytes list automatically if it wasn't explicitly provided
    local check_for_null = true
    if args.bad_bytes then -- If bad_bytes was specified
        check_for_null = false -- Assume user specified exactly what they want
        -- But if they specified it and *included* 00, we still check it
        for _, val in ipairs(bad_byte_values) do
            if val == 0 then
                check_for_null = true -- Yes, they want null check
                break
            end
        end
    end
    if check_for_null then
        -- Ensure 0 is in the list of values to check against
        local found_zero = false
        for _, val in ipairs(bad_byte_values) do
            if val == 0 then found_zero = true; break end
        end
        if not found_zero then table.insert(bad_byte_values, 0) end
    end


    -- --- Validation Checks ---
    local results = {}
    local data_len = #shellcode_data

    -- Length Check
    table.insert(results, "--- Resultados de Validación ---")
    table.insert(results, "Longitud del Shellcode: " .. data_len .. " bytes")
    if data_len > max_len then
        table.insert(results, "[!] Advertencia: La longitud (" .. data_len .. " bytes) excede la longitud máxima recomendada (" .. max_len .. " bytes).")
    else
        table.insert(results, "[+] Longitud dentro del límite (" .. max_len .. " bytes).")
    end

    -- Bad Bytes Check
    local found_bad_bytes_map = {} -- Use a map to store unique hex representations found
    local bad_byte_occurrences = {} -- Store occurrences with index for display

    if #bad_byte_values > 0 then
        -- Sort bad byte values for consistent checking/reporting order (optional but nice)
        table.sort(bad_byte_values)

        for i = 1, data_len do
            local byte_value = string.byte(shellcode_data, i)
            for _, bad_val in ipairs(bad_byte_values) do
                 if byte_value == bad_val then
                    local hex_rep = string.format("%02X", byte_value)
                    table.insert(bad_byte_occurrences, {hex = hex_rep, index = i - 1}) -- 0-based index
                    found_bad_bytes_map[hex_rep] = true -- Mark this hex value as found

                    -- Optimization: Once a byte matches *any* bad_val, move to the next byte in shellcode_data
                    goto next_byte
                end
            end
            ::next_byte:: -- Label for goto
        end
    end

    local unique_bad_bytes_count = 0
    for hex_rep, _ in pairs(found_bad_bytes_map) do
        unique_bad_bytes_count = unique_bad_bytes_count + 1
    end

    if unique_bad_bytes_count > 0 then
        table.insert(results, "[!] ¡Bytes Malos Encontrados! (" .. unique_bad_bytes_count .. " tipos únicos, " .. #bad_byte_occurrences .. " ocurrencias totales):")
        local occurrences_list = {}
        for _, entry in ipairs(bad_byte_occurrences) do
            table.insert(occurrences_list, string.format("0x%s (idx %d)", entry.hex, entry.index))
        end
        table.insert(results, table.concat(occurrences_list, ", "))

        -- Specific check for null bytes based on the map
        if found_bad_bytes_map["00"] then
             table.insert(results, "[!] ¡Contiene Bytes Nulos (0x00)! Esto puede causar problemas.")
        else
             table.insert(results, "[+] No se encontraron bytes nulos (0x00).")
        end

    else
         table.insert(results, "[+] No se encontraron bytes malos.")
         table.insert(results, "[+] No se encontraron bytes nulos (0x00).") -- Reiterate if no bad bytes at all
    end


    -- --- Return Results ---
    return table.concat(results, "\n")
end

-- Register the command with cmd2 via Lupa
register_command("validate_shellcode", validate_shellcode)