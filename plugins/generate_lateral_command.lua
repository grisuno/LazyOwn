-- The main plugin function for generating lateral movement commands
-- Expects ONE string argument containing all key=value pairs
-- Attempts to use app.params as default source for target, user, password, domain, rport
function generate_lateral_command(arg_string)
    -- --- DEBUG START ---
   print("[DEBUG] generate_lateral_command function called.")
   print("[DEBUG] Received raw arg_string: '" .. tostring(arg_string) .. "' (Type: " .. type(arg_string) .. ")")
   -- --- DEBUG END ---

   local args = {}
   arg_string = arg_string or ""

   -- --- ADVANCED PARSING LOGIC (Split by whitespace, respecting quotes) ---
   local words = {}
   local current_word = ""
   local in_single_quotes = false
   local in_double_quotes = false

   -- Iterate through the string character by character
   for i = 1, #arg_string do
       local char = arg_string:sub(i, i)

       if char == '"' and not in_single_quotes then
           in_double_quotes = not in_double_quotes
            -- Optionally include the quote in the word, or handle during key/value parse
           current_word = current_word .. char
       elseif char == "'" and not in_double_quotes then
           in_single_quotes = not in_single_quotes
            -- Optionally include the quote in the word
           current_word = current_word .. char
       elseif char:match("%s") and not in_single_quotes and not in_double_quotes then
           -- Whitespace outside of quotes signifies end of a word
           if #current_word > 0 then
               table.insert(words, current_word)
           end
           current_word = "" -- Start a new word
       else
           -- Any other character, just append to the current word
           current_word = current_word .. char
       end
   end
   -- Add the last word after the loop ends
   if #current_word > 0 then
       table.insert(words, current_word)
   end
   -- --- END ADVANCED PARSING LOGIC ---


   -- --- DEBUG START ---
   print("[DEBUG] Split arg_string into " .. #words .. " words using advanced logic.")
   for i, word in ipairs(words) do
       print("[DEBUG]   Word " .. i .. ": '" .. word .. "'")
   end
   -- --- END DEBUG ---


   -- Step 2: Process each word looking for key=value (Same as before, but now words are correctly split)
   for _, word in ipairs(words) do
       local eq_pos = string.find(word, "=", 1, true) -- Find the first '='

       if eq_pos then
           local key = word:sub(1, eq_pos - 1)
           local raw_value = word:sub(eq_pos + 1)

           key = key:gsub("^%s*", ""):gsub("%s*$", "") -- Trim key

           local value = raw_value
           -- Check if value is wrapped in quotes (single or double) AFTER splitting
           -- If the advanced splitter kept the quotes, remove them here.
           if value:match('^".*"$') then -- Double quotes
                value = value:sub(2, #value - 1)
                -- Basic handling for escaped double quotes inside value \" -> " (if splitter included them)
                -- If the splitter *didn't* include them, this might need adjustment.
                -- Let's assume splitter included quotes, and handle unescaping here.
                value = value:gsub('\\"', '"')
           elseif value:match("^'.*'$") then -- Single quotes
                value = value:sub(2, #value - 1)
                 value = value:gsub("\\'", "'")
           end

           if key ~= "" then
               args[key] = value
               -- --- DEBUG START ---
               print("[DEBUG]   Parsed key-value pair (split): '" .. key .. "' = '" .. value .. "'")
               -- --- DEBUG END ---
           else
                -- --- DEBUG START ---
               print("[DEBUG]   Word contained '=', but key was empty after trim: '" .. word .. "' (ignored)")
               -- --- DEBUG END ---
           end

       else
            -- --- DEBUG START ---
           print("[DEBUG]   Word did not contain '=': '" .. word .. "' (ignored)")
           -- --- DEBUG END ---
       end
   end
   -- --- END PARSING LOGIC ---


   -- --- Check for app.params availability ---
   -- Attempt to get params table if app exists and has params field
   local params = app and app.params -- Safe access

   -- --- Get values, using app.params as fallback ---
   -- Mandatory args (must be in args OR taken from params if available)
   local method = string.lower(args.method or "")
   -- Use args.target first, then fallback to params.rhost
   local target = args.target or (params and params.rhost)
   local command = args.command -- Command must always be provided via args (now handles quotes)

   -- Optional args (use args, then fallback to params if available)
   local user = args.user or (params and params.start_user)
   local password = args.password or (params and params.start_pass)
   local domain = args.domain or (params and params.domain)
   local tool_path = args.tool_path
   local protocol = string.lower(args.protocol or "")
   -- New args for nc
   local port = args.port or (params and params.rport) -- Use args.port, fallback to app.params.rport
   local check_only = string.lower(args.check or "") -- For nc method, like check=port

   local generated_command = nil

   -- --- Simplified Help Message ---
   local help_msg = [[
Uso: generate_lateral_command method=<metodo> command=<"comando"> [target=<objetivo>] [user=<usuario>] [password=<clave>] [domain=<dominio>] [...]
Uso (nc): generate_lateral_command method=nc [target=<objetivo>] [port=<puerto>] [check=<port>]

Metodos: psexec, smbexec, wmi, winrm, ssh, nc

Optional arguments in [] can use defaults from app.params if not specified:
 target (defaults to app.params.rhost)
 user (defaults to app.params.start_user)
 password (defaults to app.params.start_pass)
 domain (defaults to app.params.domain)
 port (for nc method, defaults to app.params.rport)

Examples (using app.params defaults):
 generate_lateral_command method=psexec command="whoami"
 generate_lateral_command method=smbexec command="ipconfig" user=svc-user
 generate_lateral_command method=ssh command="id" target=192.168.1.5
 generate_lateral_command method=wmi command="hostname"
 generate_lateral_command method=winrm command="whoami /priv" protocol=https
 generate_lateral_command method=nc check=port
 generate_lateral_command method=nc target=10.10.11.5 port=80
 generate_lateral_command method=nc target=10.10.11.5 port=443
 generate_lateral_command method=psexec target=192.168.1.10 command="echo \"Hello World\" & whoami" user=admin password=Password123! -- Cmd with spaces/special chars
]]


   -- --- Argument Validation ---
   -- Check mandatory args after fallback logic
   if method == "" then return "Error: Argumento 'method' faltante.\n" .. help_msg end
   local valid_methods = { psexec = true, smbexec = true, wmi = true, winrm = true, ssh = true, nc = true }
   if not valid_methods[method] then
       return "Error: Metodo '" .. method .. "' no soportado.\n" .. help_msg
   end

   -- Check mandatory args based on method type
   if method ~= "nc" then -- For psexec, smbexec, wmi, winrm, ssh
       if not target or target == "" then return "Error: Argumento 'target' faltante. Especifique 'target' o asegúrese de que app.params.rhost esté definido en app.params.\n" .. help_msg end
       if not command or command == "" then return "Error: Argumento 'command' faltante.\n" .. help_msg end
   else -- For nc
       if not target or target == "" then return "Error: Argumento 'target' faltante para el método 'nc'. Especifique 'target' o asegúrese de que app.params.rhost esté definido.\n" .. help_msg end
       if not port or (type(port) ~= 'string' and type(port) ~= 'number') or tonumber(port) == nil then return "Error: Argumento 'port' faltante o inválido para el método 'nc'. Especifique 'port' o asegúrese de que app.params.rport esté definido.\n" .. help_msg end
       if command then return "Error: El método 'nc' no usa el argumento 'command'.\n" .. help_msg end
       -- Check if user, password, or domain were provided *as command-line args*
       if args.user or args.password or args.domain then return "Error: El método 'nc' no usa argumentos de credenciales (user, password, domain).\n" .. help_msg end
   end


   -- --- Command Generation based on Method ---
   print("[DEBUG] Generating command for method '" .. method .. "'...") -- Debug
   print("[DEBUG]   Target: '" .. tostring(target) .. "'") -- Debug
   if method ~= "nc" then print("[DEBUG]   Command: '" .. tostring(command) .. "'") end -- Debug command only if used
   print("[DEBUG]   User: '" .. tostring(user) .. "'") -- Debug user after fallback
   print("[DEBUG]   Domain: '" .. tostring(domain) .. "'") -- Debug domain after fallback
   print("[DEBUG]   Protocol: '" .. tostring(protocol) .. "'") -- Debug
   print("[DEBUG]   Tool Path: '" .. tostring(tool_path) .. "'") -- Debug
   if method == "nc" then print("[DEBUG]   Port: '" .. tostring(port) .. "'") end -- Debug port only if used
   if method == "nc" then print("[DEBUG]   Check Only: '" .. check_only .. "'") end -- Debug check_only if used


   local tool_cmd = tool_path or method

   local creds_part = ""
   -- Escape command only if needed (not for nc)
   local escaped_command = (method ~= "nc" and command) and command:gsub('"', '\\"') or nil


   if method == "psexec" then
        if user and user ~= "" then
            creds_part = "-u " .. user .. " -p " .. (password or "")
            if domain and domain ~= "" then creds_part = creds_part .. " -d " .. domain end
        end
        generated_command = string.format('%s \\\\%s %s "%s"',
                                         tool_cmd, target, creds_part, escaped_command)

   elseif method == "smbexec" or method == "wmi" or method == "winrm" then
        -- Impacket style: tool.py [domain/]user[:pass]@target [-proto proto] command
        local target_with_creds = target
        if user and user ~= "" then
            local domain_user = user
            if domain and domain ~= "" then domain_user = domain .. "/" .. user end
            target_with_creds = domain_user .. (password and (":" .. password) or "") .. "@" .. target
        end
        local protocol_part_gen = "" -- Use a different var name to avoid confusion with function arg 'protocol'
        if protocol and protocol ~= "" then
             if method == "smbexec" then protocol_part_gen = "-proto " .. protocol end
             if method == "winrm" then protocol_part_gen = (protocol == "https" and "-H" or "-P") .. " " .. protocol end -- Example for winrm, check tool docs
        end
        generated_command = string.format('%s %s %s "%s"',
                                         tool_cmd, target_with_creds, protocol_part_gen, escaped_command)
        -- Adjust default tool_cmd for wmi/winrm if not provided
        if not tool_path then
             if method == "wmi" then tool_cmd = "wmiexec.py" end
             if method == "winrm" then tool_cmd = "winexec.py" end -- Default to impacket winexec for winrm
        end
        -- Update generated_command string with potentially changed tool_cmd (if tool_path was nil)
        if type(generated_command) == 'string' then
           generated_command = generated_command:gsub("^[^%s]+", tool_cmd, 1) -- Replace only the first word (the tool name)
        end


   elseif method == "ssh" then
        local target_with_creds = target
        if user and user ~= "" then target_with_creds = user .. "@" .. target end
        generated_command = string.format('%s %s "%s"',
                                         tool_cmd, target_with_creds, escaped_command)
        if password and password ~= "" then
            -- Build a multi-line string instead of using table.insert on a string
            local hint_line = "REM ** Consider using sshpass or key-based auth for password.**"
            local sshpass_example = "Example with sshpass: sshpass -p '" .. password .. "' " .. generated_command
            generated_command = generated_command .. "\n" .. hint_line .. "\n" .. sshpass_example
        end

   elseif method == "nc" then
      -- Netcat commands: nc target port or nc -zv target port
      if check_only == "port" then
          generated_command = string.format('nc -zv %s %s', target, port)
      else
          generated_command = string.format('nc %s %s', target, port)
      end
      -- Default tool_cmd for nc
      if not tool_path then tool_cmd = "nc" end
       if type(generated_command) == 'string' then
          generated_command = generated_command:gsub("^[^%s]+", tool_cmd, 1) -- Replace only the first word (the tool name)
       end
   end


   -- --- Return Generated Command ---
   if generated_command then
       return generated_command
   else
       return "Error: No se pudo generar el comando. Verifique los argumentos y el método."
   end
end

-- Register the command with cmd2 via Lupa
register_command("generate_lateral_command", generate_lateral_command)