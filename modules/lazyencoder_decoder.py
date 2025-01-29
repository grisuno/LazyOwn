import base64

def base64_encode(data):
    return base64.urlsafe_b64encode(data.encode()).decode()

def base64_decode(data):
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding).decode()

def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                result.append(chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a')))
            elif char.isupper():
                result.append(chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

def key_substitution(text, key):
    key_length = len(key)
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            key_char = key[i % key_length]
            shift_amount = ord(key_char.lower()) - ord('a')
            if char.islower():
                result.append(chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a')))
            elif char.isupper():
                result.append(chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

def key_substitution_reverse(text, key):
    key_length = len(key)
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            key_char = key[i % key_length]
            shift_amount = ord(key_char.lower()) - ord('a')
            if char.islower():
                result.append(chr((ord(char) - ord('a') - shift_amount) % 26 + ord('a')))
            elif char.isupper():
                result.append(chr((ord(char) - ord('A') - shift_amount) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

def encode(data, shift, key):
    if isinstance(data, str):
        return encode_string(data, shift, key)
    elif isinstance(data, list):
        if all(isinstance(item, str) for item in data):
            return [encode_string(item, shift, key) for item in data]
        else:
            raise TypeError("All items in the list must be strings. Found: {}".format(data))

    else:
        pass
def encode_string(data, shift, key):
    base64_encoded = base64_encode(data)
    caesar_encoded = caesar_cipher(base64_encoded, shift)
    key_encoded = key_substitution(caesar_encoded, key)
    return key_encoded

def decode(data, shift, key):
    if isinstance(data, str):
        return decode_string(data, shift, key)
    elif isinstance(data, list):
        if all(isinstance(item, str) for item in data):
            return [decode_string(item, shift, key) for item in data]
        else:
            raise TypeError("All items in the list must be strings. Found: {}".format(data))
    else:
        raise TypeError("All items in the list must be strings. Found: {}".format(data))

def decode_string(data, shift, key):
    key_decoded = key_substitution_reverse(data, key)
    caesar_decoded = caesar_decipher(key_decoded, shift)
    try:
        base64_decoded = base64_decode(caesar_decoded)
    except Exception as e:
        print(f"Decoding error: {e}")
        print(f"Intermediate values - Caesar Decoded: {caesar_decoded}")
        raise e
    return base64_decoded
