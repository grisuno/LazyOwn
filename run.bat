@echo off
setlocal

:: Ruta al entorno virtual
set VENV_PATH=env

:: Ruta al script de Python
set PYTHON_SCRIPT=lazyown

:: Verificar si el script de activación existe
if exist %VENV_PATH%\Scripts\activate.bat (
    :: Activar el entorno virtual
    call %VENV_PATH%\Scripts\activate.bat
) else (
    echo Alerta: El entorno virtual no se pudo encontrar o activar. Ejecutando sin activar el entorno virtual.
)

:: Verificar si hay argumentos
if "%~1"=="" (
    python %PYTHON_SCRIPT%
) else (
    python %PYTHON_SCRIPT% %*
)

endlocal
