# PrivCheck
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as an Administrator!"
    Exit
}

# Install Windows PowerShell Web Access feature
try {
    Install-WindowsFeature -Name WindowsPowerShellWebAccess -IncludeManagementTools
    Write-Host "Windows PowerShell Web Access feature installed successfully." -ForegroundColor Green
} catch {
    Write-Error "Failed to install Windows PowerShell Web Access feature: $_"
    Exit
}

# Install and configure IIS if not already installed
if (!(Get-WindowsFeature Web-Server).Installed) {
    Install-WindowsFeature -Name Web-Server -IncludeManagementTools
    Write-Host "IIS installed successfully." -ForegroundColor Green
}

# Configure PowerShell Web Access gateway
try {
    Install-PswaWebApplication -UseTestCertificate
    Write-Host "PowerShell Web Access gateway configured successfully." -ForegroundColor Green
} catch {
    Write-Error "Failed to configure PowerShell Web Access gateway: $_"
    Exit
}

# Add a rule to allow all users to access all computers
Add-PswaAuthorizationRule -UserName * -ComputerName * -ConfigurationName *

Write-Host "PowerShell Web Access has been enabled and configured." -ForegroundColor Green
Write-Host "Warning: This configuration allows all users to access all computers. Please adjust the authorization rules for your specific security requirements." -ForegroundColor Yellow 