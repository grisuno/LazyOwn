# Ruta al entorno virtual
$VENV_PATH = "env"

# Ruta al script de Python
$PYTHON_SCRIPT = "lazyown"

# Verificar si el script de activación existe
if (Test-Path "$VENV_PATH\Scripts\Activate.ps1") {
    # Activar el entorno virtual
    & "$VENV_PATH\Scripts\Activate.ps1"
} else {
    Write-Host "Alerta: El entorno virtual no se pudo encontrar o activar. Ejecutando sin activar el entorno virtual."
}

# Verificar si hay argumentos
if ($args.Count -eq 0) {
    python $PYTHON_SCRIPT
} else {
    python $PYTHON_SCRIPT $args
}
