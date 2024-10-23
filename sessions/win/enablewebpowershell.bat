@echo off
setlocal

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Please run this script as an Administrator!
    exit /b 1
)

dism /online /enable-feature /featurename:WindowsPowerShellWebAccess /all

dism /online /enable-feature /featurename:IIS-WebServerRole /all

powershell -Command "& {Install-PswaWebApplication -UseTestCertificate}"

powershell -Command "& {Add-PswaAuthorizationRule -UserName * -ComputerName * -ConfigurationName *}"

echo PowerShell Web Access has been enabled and configured.
echo Warning: This configuration allows all users to access all computers. Please adjust the authorization rules for your specific security requirements.