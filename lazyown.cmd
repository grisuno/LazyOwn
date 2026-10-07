@echo off
rem LazyOwn launcher (Windows) - interactive cmd2 shell via the Docker sandbox.
rem Usage (from the repo root, in PowerShell or cmd):
rem   .\lazyown.cmd                 interactive shell
rem   .\lazyown.cmd --no-banner     skip the banner
rem   .\lazyown.cmd --headless --json-output -c "help"   drive one command
rem Any arguments are forwarded to lazyown.py inside the container.
setlocal
docker image inspect lazyown-sandbox >nul 2>&1 || docker build -f Dockerfile.sandbox -t lazyown-sandbox .
docker run -it --rm -v "%cd%:/app" -w /app lazyown-sandbox %*
endlocal
