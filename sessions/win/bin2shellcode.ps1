$binaryShellcode = [System.IO.File]::ReadAllBytes("/home/grisun0/LazyOwn/sessions/sessions/shellcode.bin")
$shellcode = $binaryShellcode -join ','
Write-Output "[Byte[]]`$shellcode = $shellcode"