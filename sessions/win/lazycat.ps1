param(
    [switch]$listen,
    [string]$execute,
    [string]$target = "0.0.0.0",
    [int]$port,
    [switch]$command,
    [string]$upload_destination
)

function run_command {
    param($cmd)
    try {
        Invoke-Expression $cmd
    } catch {
        $_.Exception.Message
    }
}

function client_handler {
    param($client)

    if ($upload_destination) {
        $buffer = New-Object System.IO.MemoryStream
        $client.GetStream().CopyTo($buffer)
        [IO.File]::WriteAllBytes($upload_destination, $buffer.ToArray())
        $client.Client.Send([System.Text.Encoding]::ASCII.GetBytes("Archivo guardado en $upload_destination`r`n"))
    }

    if ($execute) {
        $output = run_command $execute
        $client.Client.Send([System.Text.Encoding]::ASCII.GetBytes($output))
    }

    if ($command) {
        while ($true) {
            $client.Client.Send([System.Text.Encoding]::ASCII.GetBytes("[LazyOwn]# "))
            $cmd_buffer = New-Object System.IO.MemoryStream
            $client.GetStream().CopyTo($cmd_buffer)
            $cmd = [System.Text.Encoding]::ASCII.GetString($cmd_buffer.ToArray())
            $response = run_command $cmd
            $client.Client.Send([System.Text.Encoding]::ASCII.GetBytes($response))
        }
    }
}

function server_loop {
    $listener = [System.Net.Sockets.TcpListener]::new($target, $port)
    $listener.Start()
    Write-Host ("Listening on {0}:{1}..." -f $target, $port)
    
    while ($true) {
        $client = $listener.AcceptTcpClient()
        Start-Job -ScriptBlock { param($c) client_handler -client $c } -ArgumentList $client
    }
}



function client_sender {
    param($buffer)
    $client = New-Object System.Net.Sockets.TcpClient($target, $port)
    $client.Client.Send([System.Text.Encoding]::ASCII.GetBytes($buffer))
    while ($client.Connected) {
        $data = New-Object System.IO.MemoryStream
        $client.GetStream().CopyTo($data)
        $response = [System.Text.Encoding]::ASCII.GetString($data.ToArray())
        Write-Host $response
        $buffer = Read-Host
        $client.Client.Send([System.Text.Encoding]::ASCII.GetBytes("$buffer`n"))
    }
}

if ($listen) {
    server_loop
} elseif ($target -and $port) {
    $buffer = [Console]::In.ReadToEnd()
    client_sender $buffer
} else {
    Write-Host "Usage: lazycat.ps1 -t target_host -p port -l -c -u upload_destination -e execute_command"
}
