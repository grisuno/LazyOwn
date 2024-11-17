# Parámetros
param (
    [string]$BasePath,
    [int]$MaxThreads = 3,
    [int]$MaxDepth = [int]::MaxValue,
    [string]$OutputFile = $null
)

# Variables
$ExcludedDirectories = @{}
$TotalDirectories = 0
$Counter = 0
$Stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$LogWriter = if ($OutputFile) { [System.IO.StreamWriter]::new($OutputFile) } else { $null }

# Función para imprimir ayuda
function PrintHelp {
    Write-Host "Usage: Script.ps1 -BasePath <Path> [-MaxThreads <N>] [-MaxDepth <N>] [-OutputFile <FilePath>]"
    Write-Host "Options:"
    Write-Host "  -MaxThreads N       Set the maximum number of threads (default 3)"
    Write-Host "  -MaxDepth N         Set the maximum directory depth to scan (default is all)"
    Write-Host "  -OutputFile Path    Specify a file to log exclusions and errors"
}

# Función para loggear mensajes
function LogMessage {
    param (
        [string]$Message,
        [bool]$IsError = $false
    )
    if ($LogWriter -and ($IsError -or $Message.Contains("[+] Folder"))) {
        $LogWriter.WriteLine($Message)
        $LogWriter.Flush()
    }
    Write-Host $Message
}

# Función para escanear directorio
function ScanDirectory {
    param (
        [string]$CurrentPath
    )
    try {
        $Counter++
        if ($Counter % 500 -eq 0) {
            Write-Host "Processed $Counter directories. Time elapsed: $($Stopwatch.Elapsed.TotalSeconds) seconds."
        }

        $Command = "C:\Program Files\Windows Defender\MpCmdRun.exe"
        $Arguments = "-Scan -ScanType 3 -File `"$CurrentPath\|*`""

        $ProcessResult = & $Command $Arguments
        if ($ProcessResult -match "was skipped") {
            LogMessage "[+] Folder $CurrentPath is excluded"
            $ExcludedDirectories[$CurrentPath] = $true
        }
    } catch {
        LogMessage ("An error occurred while scanning directory $CurrentPath" + ": " + $_.Exception.Message) -IsError $true
    }
}

# Función para verificar exclusión de un directorio
function IsDirectoryExcluded {
    param (
        [string]$Directory
    )
    $CurrentDirectory = $Directory
    while ($CurrentDirectory) {
        if ($ExcludedDirectories.ContainsKey($CurrentDirectory)) {
            return $true
        }
        $CurrentDirectory = [System.IO.Path]::GetDirectoryName($CurrentDirectory)
    }
    return $false
}

# Función para obtener carpetas excluidas por niveles
function GetExcludedFoldersByTier {
    param (
        [string]$BasePath,
        [int]$CurrentDepth = 0
    )

    if ($CurrentDepth -gt $MaxDepth) { return }

    try {
        $CurrentTierDirectories = Get-ChildItem -Directory -Path $BasePath | ForEach-Object { $_.FullName }
    } catch {
        LogMessage ("Error retrieving top-level directories from $BasePath" + ": " + $_.Exception.Message) -IsError $true
        return
    }

    $DirectoriesQueue = [System.Collections.Generic.Queue[System.Collections.ArrayList]]::new()
    $DirectoriesQueue.Enqueue([System.Collections.ArrayList]$CurrentTierDirectories)

    while ($DirectoriesQueue.Count -gt 0 -and $CurrentDepth -le $MaxDepth) {
        $CurrentTier = $DirectoriesQueue.Dequeue()
        $FilteredDirectories = $CurrentTier | Where-Object { -not (IsDirectoryExcluded $_) }
        $TotalDirectories += $FilteredDirectories.Count

        # Procesar directorios en paralelo
        $Jobs = @()
        foreach ($Dir in $FilteredDirectories) {
            $Jobs += Start-Job -ScriptBlock { param($d) ScanDirectory -CurrentPath $d } -ArgumentList $Dir
            if ($Jobs.Count -ge $MaxThreads) {
                $Jobs | ForEach-Object { $_ | Wait-Job | Remove-Job }
                $Jobs.Clear()
            }
        }
        $Jobs | ForEach-Object { $_ | Wait-Job | Remove-Job }

        $NextTierDirectories = @()
        foreach ($Dir in $FilteredDirectories) {
            try {
                $SubDirs = Get-ChildItem -Directory -Path $Dir | ForEach-Object { $_.FullName }
                $NextTierDirectories += $SubDirs
            } catch [UnauthorizedAccessException] {
                LogMessage "Access denied to $Dir. Skipping this directory and its subdirectories." -IsError $true
            } catch {
                LogMessage ("Error retrieving subdirectories from $Dir" + ": " + $_.Exception.Message) -IsError $true
            }
        }

        if ($NextTierDirectories.Count -gt 0) {
            $DirectoriesQueue.Enqueue([System.Collections.ArrayList]$NextTierDirectories)
        }

        $CurrentDepth++
    }

    $Stopwatch.Stop()
    Write-Host "Scan completed up to depth $MaxDepth. Total time: $($Stopwatch.Elapsed.TotalSeconds) seconds."
}

if (!$BasePath) {
    PrintHelp
    return
}

GetExcludedFoldersByTier -BasePath $BasePath

if ($LogWriter) {
    $LogWriter.Close()
}