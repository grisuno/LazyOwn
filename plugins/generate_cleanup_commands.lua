-- The main plugin function for generating cleanup commands
-- NOW expects ONE string argument containing all key=value pairs
function generate_cleanup_commands(arg_string)
    -- --- DEBUG START ---
    print("[DEBUG] generate_cleanup_commands function called.")
    print("[DEBUG] Received raw arg_string: '" .. tostring(arg_string) .. "' (Type: " .. type(arg_string) .. ")")
    -- --- DEBUG END ---

    local args = {}
    arg_string = arg_string or "" -- Handle case with no arguments

    -- --- NEW PARSING LOGIC (Split then Parse) ---
    local words = {}
    -- Step 1: Split the string into words by whitespace
    -- Use a simple pattern to find sequences of non-whitespace characters
    for word in string.gmatch(arg_string, "[^%s]+") do
        table.insert(words, word)
    end

    -- --- DEBUG START ---
    print("[DEBUG] Split arg_string into " .. #words .. " words.")
    for i, word in ipairs(words) do
        print("[DEBUG]   Word " .. i .. ": '" .. word .. "'")
    end
    -- --- DEBUG END ---


    -- Step 2: Process each word
    for _, word in ipairs(words) do
        -- Find the first '=' in the word
        local eq_pos = string.find(word, "=", 1, true) -- Use plain find for literal =

        if eq_pos then
            -- Split into key and potential value string
            local key = word:sub(1, eq_pos - 1)
            local raw_value = word:sub(eq_pos + 1)

            -- Handle trimming key
            key = key:gsub("^%s*", ""):gsub("%s*$", "")

            -- Handle value: check for quotes or just use raw
            local value = raw_value
            -- Check if value is wrapped in quotes (single or double)
            if raw_value:match('^".*"$') or raw_value:match("^'.*'$") then
                 -- Value is quoted, remove outer quotes
                 value = raw_value:sub(2, #raw_value - 1)
                 -- NOTE: This basic parsing does NOT handle escaped quotes INSIDE the value (e.g. "va\"lue")
            end
            -- Optional: trim value if needed
            -- value = value:gsub("^%s*", ""):gsub("%s*$", "")


            -- Check if key is not empty after trim
            if key ~= "" then
                args[key] = value
                -- --- DEBUG START ---
                print("[DEBUG]   Parsed key-value pair (split): '" .. key .. "' = '" .. value .. "'")
                -- --- DEBUG END ---
            else
                 -- --- DEBUG START ---
                print("[DEBUG]   Word contained '=', but key was empty after trim: '" .. word .. "'")
                -- --- DEBUG END ---
            end

        else
            -- Word does not contain '=', ignore it as it's not a key=value pair
             -- --- DEBUG START ---
            print("[DEBUG]   Word did not contain '=': '" .. word .. "' (ignored)")
            -- --- DEBUG END ---
        end
    end
    -- --- END NEW PARSING LOGIC ---


    -- --- DEBUG START ---
    print("[DEBUG] Final parsed 'args' table content:")
    print("[DEBUG]   args.os = '" .. tostring(args.os) .. "' (Type: " .. type(args.os) .. ")")
    print("[DEBUG]   args.type = '" .. tostring(args.type) .. "' (Type: " .. type(args.type) .. ")")
    print("[DEBUG]   args.log_name = '" .. tostring(args.log_name) .. "' (Type: " .. type(args.log_name) .. ")")
    print("[DEBUG]   args.user = '" .. tostring(args.user) .. "' (Type: " .. type(args.user) .. ")")
    -- --- DEBUG END ---


    local target_os = string.lower(args.os or "")
    local cleanup_type = string.lower(args.type or "")
    local specific_log = args.log_name
    local specific_user = args.user

    local commands = {}
    local help_msg = [[
Uso: generate_cleanup_commands os=<windows|linux> type=<logs|temp|history|all> [log_name=<canal>] [user=<usuario>]

Ejemplos:
  generate_cleanup_commands os=windows type=logs
  generate_cleanup_commands os=windows type=logs log_name="Sysmon/Operational" -- Use quotes if name has spaces/special chars
  generate_cleanup_commands os=windows type=temp
  generate_cleanup_commands os=windows type=all
  generate_cleanup_commands os=linux type=logs
  generate_cleanup_commands os=linux type=logs log_name=auth.log (Linux log_name example)
  generate_cleanup_commands os=linux type=temp
  generate_cleanup_commands os=linux type=history
  generate_cleanup_commands os=linux type=history user=kali
  generate_cleanup_commands os=linux type=all
]]

    -- --- Argument Validation ---
    -- --- DEBUG START ---
    print("[DEBUG] Validating arguments...")
    print("[DEBUG]   target_os = '" .. target_os .. "'")
    print("[DEBUG]   cleanup_type = '" .. cleanup_type .. "'")
    -- --- DEBUG END ---


    if (target_os ~= "windows" and target_os ~= "linux") then
         return "Error: Argumento 'os' inválido o faltante. Debe ser 'windows' o 'linux'.\n" .. help_msg
     end
    if cleanup_type == "" then
         return "Error: Argumento 'type' faltante.\n" .. help_msg
    end


    if cleanup_type ~= "logs" and cleanup_type ~= "temp" and cleanup_type ~= "history" and cleanup_type ~= "all" then
         return "Error: Argumento 'type' inválido. Debe ser 'logs', 'temp', 'history' o 'all'.\n" .. help_msg
    end

    if target_os == "windows" and specific_user then
        return "Error: El argumento 'user' solo es aplicable para os=linux type=history.\n" .. help_msg
    end

    -- log_name can be used with Linux logs for specific files, removed the strict check here
    -- if target_os == "linux" and specific_log then
    --      return "Error: El argumento 'log_name' solo es aplicable para os=windows type=logs.\n" .. help_msg
    -- end


    -- --- Command Generation ---

    if target_os == "windows" then
        table.insert(commands, "REM --- Comandos de Limpieza para Windows (" .. cleanup_type .. ") ---")
        if cleanup_type == "logs" or cleanup_type == "all" then
            local logs_to_clear = {}
            if specific_log and specific_log ~= "" then
                -- Support comma-separated log_names here, need to parse specific_log string
                for log_name in specific_log:gmatch("([^,%s]+)") do
                    if log_name ~= "" then table.insert(logs_to_clear, log_name) end
                end
            else
                -- Default common Windows logs
                table.insert(logs_to_clear, "System")
                table.insert(logs_to_clear, "Security")
                table.insert(logs_to_clear, "Application")
                table.insert(logs_to_clear, "Setup")
                table.insert(logs_to_clear, "ForwardedEvents")
            end
             if #logs_to_clear == 0 then
                 return "Error: No se especificaron canales de log válidos con 'log_name' o la lista de canales está vacía."
             end

            table.insert(commands, "REM Limpiando Event Logs:")
            for _, log_name in ipairs(logs_to_clear) do
                 table.insert(commands, "wevtutil cl \"" .. log_name .. "\"")
            end
        end

        if cleanup_type == "temp" or cleanup_type == "all" then
             table.insert(commands, "REM Limpiando Archivos Temporales:")
             table.insert(commands, "del /Q \"%TEMP%\\*.*\"")
             table.insert(commands, "del /Q \"%TMP%\\*.*\"")
             table.insert(commands, "rmdir /S /Q \"%TEMP%\"")
             table.insert(commands, "rmdir /S /Q \"%TMP%\"")
        end

        if cleanup_type == "history" or cleanup_type == "all" then
             table.insert(commands, "REM Limpiando Historial de PowerShell (requiere PowerShell):")
             table.insert(commands, "powershell -Command \"(Get-History).Clear()\"")
             table.insert(commands, "del /Q \"%userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt\" 2>NUL")
             table.insert(commands, "REM La historia de CMD es no persistente.")
        end


    elseif target_os == "linux" then
        table.insert(commands, "REM --- Comandos de Limpieza para Linux (" .. cleanup_type .. ") ---")
        table.insert(commands, "REM **Advertencia: La limpieza de logs/temp/history en Linux a menudo requiere privilegios (ej: sudo).**")
         if cleanup_type == "logs" or cleanup_type == "all" then
             local logs_to_clear = {
                "/var/log/syslog",
                "/var/log/auth.log",
                "/var/log/kern.log",
                "/var/log/boot.log",
                "/var/log/daemon.log",
                "/var/log/messages", -- Common on RHEL/CentOS
                "/var/log/secure",  -- Common on RHEL/CentOS
                "/var/log/wtmp",    -- Login records
                "/var/log/btmp",    -- Failed login records
                "/var/log/lastlog", -- last login records
             }
             if specific_log and specific_log ~= "" then
                 -- Allow specifying specific Linux logs too, similar to Windows
                  local specific_linux_logs = {}
                   for log_path in specific_log:gmatch("([^,%s]+)") do
                     if log_path ~= "" then table.insert(specific_linux_logs, log_path) end
                  end
                  if #specific_linux_logs > 0 then
                      logs_to_clear = specific_linux_logs -- Override defaults if specific logs given
                  end
             end


              table.insert(commands, "REM Limpiando Logs Comunes (requiere permisos):")
             for _, log_path in ipairs(logs_to_clear) do
                 table.insert(commands, "sudo truncate -s 0 \"" .. log_path .. "\" 2>/dev/null")
             end
         end

         if cleanup_type == "temp" or cleanup_type == "all" then
             table.insert(commands, "REM Limpiando Directorios Temporales (requiere permisos):")
             table.insert(commands, "sudo rm -rf /tmp/*")
             table.insert(commands, "sudo rm -rf /var/tmp/*")
         end

         if cleanup_type == "history" or cleanup_type == "all" then
             table.insert(commands, "REM Limpiando Historial de Shells (requiere permisos):")
             table.insert(commands, "history -c && history -w") -- For current session (bash/zsh)
             table.insert(commands, "sudo rm -f /root/.bash_history /root/.zsh_history /root/.history 2>/dev/null")

             if specific_user and specific_user ~= "" then
                 table.insert(commands, "REM Limpiando historial para usuario específico: " .. specific_user)
                 table.insert(commands, "sudo rm -f /home/" .. specific_user .. "/.bash_history /home/" .. specific_user .. "/.zsh_history /home/" .. specific_user .. "/.history 2>/dev/null")
             end
         end
    end


    if #commands == 0 then
        return "No se pudieron generar comandos para la combinación OS/Type/Opciones especificada."
    end


    -- --- Return Generated Commands ---
    return table.concat(commands, "\n")
end

-- Register the command with cmd2 via Lupa
register_command("generate_cleanup_commands", generate_cleanup_commands)