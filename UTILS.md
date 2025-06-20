# UTILS.md Documentation  by readmeneitor.py

## check_go_tool_installed
No description available.

## parse_ip_mac
Extracts IP and MAC addresses from a formatted input string using a regular expression.

The input string is expected to be in the format: 'IP: (192.168.1.222) MAC: ec:c3:02:b0:4c:96'.
The function uses a regular expression to match and extract the IP address and MAC address from the input.

Args:
    input_string (str): The formatted string containing the IP and MAC addresses.

Returns:
    tuple: A tuple containing the extracted IP address and MAC address. If the format is incorrect, returns (None, None).

## create_arp_packet
Constructs an ARP packet with the given source and destination IP and MAC addresses.

The function creates both Ethernet and ARP headers, combining them into a complete ARP packet.

Args:
    src_mac (str): Source MAC address in the format 'xx:xx:xx:xx:xx:xx'.
    src_ip (str): Source IP address in dotted decimal format (e.g., '192.168.1.1').
    dst_ip (str): Destination IP address in dotted decimal format (e.g., '192.168.1.2').
    dst_mac (str): Destination MAC address in the format 'xx:xx:xx:xx:xx:xx'.

Returns:
    bytes: The constructed ARP packet containing the Ethernet and ARP headers.

## send_packet
Sends a raw ARP packet over the specified network interface.

The function creates a raw socket, binds it to the specified network interface, and sends the given packet.

Args:
    packet (bytes): The ARP packet to be sent.
    iface (str): The name of the network interface to use for sending the packet (e.g., 'eth0').

Raises:
    OSError: If an error occurs while creating the socket or sending the packet.

## load_version
Load the version number from the 'version.json' file.

This function attempts to open the 'version.json' file and load its contents. 
If the file is found, it retrieves the version number from the JSON data. 
If the version key does not exist, it returns a default version 'release/v0.0.14'. 
If the file is not found, it also returns the default version.

Returns:
- str: The version number from the file or the default version if the file is not found or the version key is missing.

## print_error
Prints an error message to the console.

This function takes an error message as input and prints it to the console
with a specific format to indicate that it is an error.

:param error: The error message to be printed.
:type error: str
:return: None

## print_msg
Prints a message to the console.

This function takes a message as input and prints it to the console
with a specific format to indicate that it is an informational message.

:param msg: The message to be printed.
:type msg: str
:return: None

## print_warn
Prints a warning message to the console.

This function takes a warning message as input and prints it to the console
with a specific format to indicate that it is a warning.

:param warn: The warning message to be printed.
:type warn: str
:return: None

## signal_handler
Handles signals such as Control + C and shows a message on how to exit.

This function is used to handle signals like Control + C (SIGINT) and prints
a warning message instructing the user on how to exit the program using the
commands 'exit', 'q', or 'qa'.

:param sig: The signal number.
:type sig: int
:param frame: The current stack frame.
:type frame: frame
:return: None

## check_rhost
Checks if the remote host (rhost) is defined and shows an error message if it is not.

This function verifies if the `rhost` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param rhost: The remote host to be checked.
:type rhost: str
:return: True if rhost is defined, False otherwise.
:rtype: bool

## check_lhost
Checks if the local host (lhost) is defined and shows an error message if it is not.

This function verifies if the `lhost` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param lhost: The local host to be checked.
:type lhost: str
:return: True if lhost is defined, False otherwise.
:rtype: bool

## check_lport
Checks if the local port (lport) is defined and shows an error message if it is not.

This function verifies if the `lport` parameter is set. If it is not defined,
an error message is printed, providing an example and directing the user to
additional help.

:param lport: The local port to be checked.
:type lport: int or str
:return: True if lport is defined, False otherwise.
:rtype: bool

## is_binary_present
Internal function to verify if a binary is present on the operating system.

This function checks if a specified binary is available in the system's PATH
by using the `which` command. It returns True if the binary is found and False
otherwise.

:param binary_name: The name of the binary to be checked.
:type binary_name: str
:return: True if the binary is present, False otherwise.
:rtype: bool

## handle_multiple_rhosts
Internal function to handle multiple remote hosts (rhost) for operations.

This function is a decorator that allows an operation to be performed across
multiple remote hosts specified in `self.params["rhost"]`. It converts a single
remote host into a list if necessary, and then iterates over each host,
performing the given function with each host. After the operation, it restores
the original remote host value.

:param func: The function to be decorated and executed for each remote host.
:type func: function
:return: The decorated function.
:rtype: function

## check_sudo
Checks if the script is running with superuser (sudo) privileges, and if not,
restarts the script with sudo privileges.

This function verifies if the script is being executed with root privileges
by checking the effective user ID. If the script is not running as root,
it prints a warning message and restarts the script using sudo.

:return: None

## activate_virtualenv
Activates a virtual environment and starts an interactive shell.

This function activates a virtual environment located at `venv_path` and then
launches an interactive bash shell with the virtual environment activated.

:param venv_path: The path to the virtual environment directory.
:type venv_path: str
:return: None

## parse_proc_net_file
Internal function to parse a /proc/net file and extract network ports.

This function reads a file specified by `file_path`, processes each line to
extract local addresses and ports, and converts them from hexadecimal to decimal.
The IP addresses are converted from hexadecimal format to standard dot-decimal
notation. The function returns a list of tuples, each containing an IP address
and a port number.

:param file_path: The path to the /proc/net file to be parsed.
:type file_path: str
:return: A list of tuples, each containing an IP address and a port number.
:rtype: list of tuple

## get_open_ports
Internal function to get open TCP and UDP ports on the operating system.

This function uses the `parse_proc_net_file` function to extract open TCP and UDP
ports from the corresponding /proc/net files. It returns two lists: one for TCP
ports and one for UDP ports.

:return: A tuple containing two lists: the first list with open TCP ports and
        the second list with open UDP ports.
:rtype: tuple of (list of tuple, list of tuple)

## find_credentials
Searches for potential credentials in files within the specified directory.

This function uses a regular expression to find possible credentials such as
passwords, secrets, API keys, and tokens in files within the given directory.
It iterates through all files in the directory and prints any matches found.

:param directory: The directory to search for files containing credentials.
:type directory: str
:return: None

## rotate_char
Internal function to rotate characters for ROT cipher.

This function takes a character and a shift value, and rotates the character
by the specified shift amount. It only affects alphabetical characters, leaving
non-alphabetical characters unchanged.

:param c: The character to be rotated.
:type c: str
:param shift: The number of positions to shift the character.
:type shift: int
:return: The rotated character.
:rtype: str

## get_network_info
Retrieves network interface information with their associated IP addresses.

This function executes a shell command to gather network interface details, 
parses the output to extract interface names and their corresponding IP addresses, 
and returns this information in a dictionary format. The dictionary keys are
interface names, and the values are IP addresses.

:return: A dictionary where the keys are network interface names and the values
         are their associated IP addresses.
:rtype: dict

## get_git_info
No description available.

## get_venv_info
No description available.

## getprompt
Generate a command prompt string with network information, user status, and icons.

## copy2clip
Copia el texto proporcionado al portapapeles usando xclip.

Args:
    text (str): El texto que se desea copiar al portapapeles.

Example:
    copy2clip("Hello, World!")

## clean_output
Elimina secuencias de escape de color y otros caracteres no imprimibles.

## teclado_usuario
Procesa un archivo para extraer y mostrar caracteres desde secuencias de escritura específicas.

Args:
    filename (str): El nombre del archivo a leer.

Raises:
    FileNotFoundError: Si el archivo no se encuentra.
    Exception: Para otros errores que puedan ocurrir.

## salida_strace
Lee un archivo, extrae texto desde secuencias de escritura y muestra el contenido reconstruido.

Args:
    filename (str): El nombre del archivo a leer.

Raises:
    FileNotFoundError: Si el archivo no se encuentra.
    Exception: Para otros errores que puedan ocurrir.

## exploitalert
Process and display results from ExploitAlert.

This function checks if the provided content contains any results. 
If results are present, it prints the title and link for each exploit found, 
and appends the results to a predata list. If no results are found, 
it prints an error message.

Parameters:
- content (list): A list of dictionaries containing exploit information.

Returns:
None
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## packetstormsecurity
Process and display results from PacketStorm Security.

This function extracts exploit data from the provided content using regex. 
If any results are found, it prints the title and link for each exploit, 
and appends the results to a predata list. If no results are found, 
it prints an error message.

Parameters:
- content (str): The HTML content from PacketStorm Security.

Returns:
None
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## nvddb
Process and display results from the National Vulnerability Database.

This function checks if there are any vulnerabilities in the provided content. 
If vulnerabilities are present, it prints the ID, description, and link 
for each CVE found, and appends the results to a predata list. 
If no results are found, it prints an error message.

Parameters:
- content (dict): A dictionary containing vulnerability data.

Returns:
None
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## find_ss
Find CVEs in the National Vulnerability Database based on a keyword.

This function takes a keyword, formats it for the API request, 
and sends a GET request to the NVD API. If the request is successful, 
it returns the JSON response containing CVE data; otherwise, 
it returns False.

Parameters:
- keyword (str): The keyword to search for in CVEs.

Returns:
- dict or bool: The JSON response containing CVE data or False on failure.
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## find_ea
Find exploits in ExploitAlert based on a keyword.

This function takes a keyword, formats it for the API request, 
and sends a GET request to the ExploitAlert API. If the request is successful, 
it returns the JSON response containing exploit data; otherwise, 
it returns False.

Parameters:
- keyword (str): The keyword to search for exploits.

Returns:
- dict or bool: The JSON response containing exploit data or False on failure.
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## find_ps
Find exploits in PacketStorm Security based on a keyword.

This function takes a keyword, formats it for the search request, 
and sends a GET request to the PacketStorm Security website. 
If the request is successful, it returns the HTML response; otherwise, 
it returns False.

Parameters:
- keyword (str): The keyword to search for exploits.

Returns:
- str or bool: The HTML response containing exploit data or False on failure.
Thanks to Sicat 🐈
An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. https://github.com/justakazh/sicat/

## xor_encrypt_decrypt
Encrypts or decrypts data using XOR encryption with the provided key.

Parameters:
data (bytes or bytearray): The input data to be encrypted or decrypted.
key (str): The encryption key as a string.

Returns:
bytearray: The result of the XOR operation, which can be either the encrypted or decrypted data.

Example:
encrypted_data = xor_encrypt_decrypt(b"Hello, World!", "key")
decrypted_data = xor_encrypt_decrypt(encrypted_data, "key")
print(decrypted_data.decode("utf-8"))  # Outputs: Hello, World!

Additional Notes:
- XOR encryption is symmetric, meaning that the same function is used for both encryption and decryption.
- The key is repeated cyclically to match the length of the data if necessary.
- This method is commonly used for simple encryption tasks, but it is not secure for protecting sensitive information.

## run
Executes a shell command using the subprocess module, capturing its output.

Parameters:
command (str): The command to execute.

Returns:
str: The output of the command if successful, or an error message if an exception occurs.

Exceptions:
- FileNotFoundError: Raised if the command is not found.
- subprocess.CalledProcessError: Raised if the command exits with a non-zero status.
- subprocess.TimeoutExpired: Raised if the command times out.
- Exception: Catches any other unexpected exceptions.

Example:
output = run("ls -la")
print(output)

Additional Notes:
The function attempts to execute the provided command, capturing its output.
It also handles common exceptions that may occur during command execution.

## is_exist
Check if a file exists.

This function checks whether a given file exists on the filesystem. If the file 
does not exist, it prints an error message and returns False. Otherwise, it returns True.

Arguments:
file (str): The path to the file that needs to be checked.

Returns:
bool: Returns True if the file exists, False otherwise.

Example:
>>> is_exist('/path/to/file.txt')
True
>>> is_exist('/non/existent/file.txt')
False

Notes:
This function uses os.path.isfile to determine the existence of the file. 
Ensure that the provided path is correct and accessible.

## get_domain
Extracts the domain from a given URL.

Parameters:
url (str): The full URL from which to extract the domain.

Returns:
str: The extracted domain from the URL, or None if it cannot be extracted.

## generate_certificates
Generates a certificate authority (CA), client certificate, and client key.

Returns:
    str: Paths to the generated CA certificate, client certificate, and client key.

## generate_emails
Generate email permutations based on the provided full name and domain.

This function takes a full name and domain as input, splits the full name into
components, and creates a list of potential email addresses.

Parameters:
full_name (str): The full name to base the email addresses on.
domain (str): The domain to use for the generated email addresses.

Internal Variables:
names (list): A list of the name components extracted from the full name.
first_name (str): The first name component.
last_name (str): The last name component.
first_initial (str): The first initial of the first name.
last_initial (str): The first initial of the last name.

Returns:
list: A list of generated email permutations.

Note:
- At least two parts of the name are required to generate valid email addresses.

## clean_url
Verifica si el último carácter es una barra y, de ser así, la elimina

## random_string
Generates a random alphanumeric string.

## generate_http_req
Generates an HTTP request with the Shellshock payload.

## format_openssh_key
Formats a raw OpenSSH private key string to the correct OpenSSH format.

This function takes a raw OpenSSH private key string, cleans it by removing any unnecessary 
characters (such as newlines, spaces, and headers/footers), splits the key content into lines 
of 64 characters, and then reassembles the key with the standard OpenSSH header and footer. 
It ensures the key follows the correct OpenSSH format.

Parameters:
    raw_key (str): The raw OpenSSH private key string to format.

Returns:
    str: The formatted OpenSSH private key with proper headers, footers, and 64-character lines.

## format_rsa_key
Formats a raw RSA private key string to the correct PEM format.

This function takes a raw RSA private key string, cleans it by removing any unnecessary
characters (such as newlines, spaces, and headers/footers), splits the key content into lines 
of 64 characters, and then reassembles the key with the standard PEM header and footer. 
It ensures the key follows the correct RSA format.

Parameters:
    raw_key (str): The raw RSA private key string to format.

Returns:
    str: The formatted RSA private key with proper headers, footers, and 64-character lines.

## is_package_installed
Check if a Python package is installed.

:param package_name: Name of the package to check.
:returns: True if installed, False otherwise.

## extract
Extracts and processes specific hexadecimal sequences from a string based on a flag.

If the `extract_flag` is set to True, the function extracts all sequences of the form 'x[a-f0-9][a-f0-9]' 
(where 'x' is followed by two hexadecimal digits), removes the 'x' from the extracted sequences, 
and returns the processed string. If `extract_flag` is False, the function returns the original string.

Parameters:
    string (str): The input string from which hexadecimal sequences are to be extracted.
    extract_flag (bool): A flag indicating whether to perform the extraction (True) or not (False).

Returns:
    str: The processed string with the extracted hexadecimal sequences if `extract_flag` is True, 
         or the original string if `extract_flag` is False.

## clean_html
Remove HTML tags from a string.

This function uses a regular expression to strip HTML tags and return plain text.

:param html_string: A string containing HTML content.
:returns: A cleaned string with HTML tags removed.

## command
Run a command, print output in real-time, and store the output in a variable.

This method executes a given command using `subprocess.Popen`, streams both the standard 
output and standard error to the console in real-time, and stores the full output (stdout 
and stderr) in a variable. If interrupted, the process is terminated gracefully.

:param command: The command to be executed as a string.
:type command: str

:returns: The full output of the command (stdout and stderr).
:rtype: str

Example:
    To execute a command, call `run_command("ls -l")`.

## generate_random_cve_id
Generates a random CVE (Common Vulnerabilities and Exposures) ID.

This function creates a random CVE ID by selecting a random year between 2020 and 2024,
and a random code between 1000 and 9999. The CVE ID is returned in the format 'CVE-{year}-{code}'.

Returns:
    str: A randomly generated CVE ID in the format 'CVE-{year}-{code}'.

## get_credentials
Searches for credential files with the pattern 'credentials*.txt' and allows the user to select one.

The function lists all matching files and prompts the user to select one. It then reads the selected file
and returns a list of tuples with the format (username, password) for each line in the file.

Parameters:
ncred (int, optional): If provided, automatically selects the credential file with the given number.

Returns:
list of tuples: A list containing tuples with (username, password) for each credential found in the file.
                If no files are found or an invalid selection is made, an empty list is returned.

## load_payload
No description available.

## obfuscate_payload
Obfuscates a payload string by converting its characters into hexadecimal format, 
with additional comments for every third character.

For every character in the payload, the function converts it to its hexadecimal representation.
Every third character (after the first) is enclosed in a comment `/*hex_value*/`, while the rest 
are prefixed with `\x`.

Parameters:
    payload (str): The input string that needs to be obfuscated.

Returns:
    str: The obfuscated string where characters are replaced by their hexadecimal representations, 
         with every third character wrapped in a comment.

## read_payloads
Reads a file containing payloads and returns a list of properly formatted strings.

This function opens a specified file, reads each line, and checks if the line starts with a 
double quote. If it does not, it adds double quotes around the line. Each line is stripped 
of leading and trailing whitespace before being added to the list.

Parameters:
    file_path (str): The path to the file containing payloads.

Returns:
    list: A list of strings, each representing a payload from the file, formatted with 
          leading and trailing double quotes if necessary.

## inject_payloads
Sends HTTP requests to a list of URLs with injected payloads for testing XSS vulnerabilities.

This function reads payloads from a specified file and sends GET requests to the provided URLs,
injecting obfuscated payloads into the query parameters or form fields to test for cross-site 
scripting (XSS) vulnerabilities. It handles both URLs with existing query parameters and those 
without. If forms are found in the response, it submits them with the payloads as well.

Parameters:
    urls (list): A list of URLs to test for XSS vulnerabilities.
    payload_url (str): A placeholder string within the payloads that will be replaced with 
                       the actual URL for testing.
    request_timeout (int, optional): The timeout for each request in seconds. Defaults to 15.

Returns:
    None: This function does not return any value but prints the status of each request and 
          form submission to the console.

Raises:
    requests.RequestException: Raises an exception if any HTTP request fails, which is handled
                               by printing a warning message.

## prompt
Return the prompt in the function do_xss

## is_lower
Checks if a character is lowercase.

Parameters:
    char (str): The character to check.

Returns:
    bool: True if the character is lowercase, False otherwise.

## is_upper
Checks if a character is uppercase.

Parameters:
    char (str): The character to check.

Returns:
    bool: True if the character is uppercase, False otherwise.

## is_mixed
Determines if a string contains both lowercase and uppercase characters.

Parameters:
    s (str): The string to check.

Returns:
    bool: True if the string has mixed casing, False otherwise.

## add
Adds a delimiter between string parts if it's not the first part.

Parameters:
    str_part (str): The string part to add.
    delimiter (str): The delimiter to insert between parts.
    i (int): The index of the part.

Returns:
    str: The string part with delimiter if applicable.

## detect_delimiter
Detects the delimiter used in the input string (e.g., "-", "_", ".").

Parameters:
    foo_bar (str): The input string.

Returns:
    str: The detected delimiter.

## transform
Transforms a list of string parts based on the chosen casing style.

Parameters:
    parts (list): List of string parts.
    delimiter (str): Delimiter to use between parts.
    casing (str): Casing style ('l', 'u', 'c', 'p').

Returns:
    str: The transformed string.

## handle
Splits the input string into parts based on delimiters or mixed casing.

Parameters:
    input_str (str): The input string to split.

Returns:
    list: A list of string parts.

## get_users_dic
List all .txt files in the 'sessions/' directory and prompt the user to select one by number.

:returns: The path of the selected .txt file.

## get_hash
Searches for hash files with the pattern 'hash*.txt' and allows the user to select one.

The function lists all matching files and prompts the user to select one. It then reads the selected file
and returns the hash content as a single string, without any newline characters or extra formatting.

Returns:
str: The hash content from the selected file as a single string. If no files are found or an invalid
     selection is made, an empty string is returned.

## is_digit
Check if the given character is a digit.

Args:
    the_digit (str): The character to check.

Returns:
    bool: True if the character is a digit, False otherwise.

## crack_password
Crack a Cisco Type 7 password.

Args:
    crypttext (str): The encrypted password in Type 7 format.

Returns:
    str: The cracked plaintext password or an empty string if invalid.

## get_terminal_size
No description available.

## halp
Display the help panel for the LazyOwn RedTeam Framework.

This function prints usage instructions, options, and descriptions for 
running the LazyOwn framework. It provides users with an overview of 
command-line options that can be used when executing the `./run` command.

The output includes the current version of the framework and various 
options available for users, along with a brief description of each option.

Options include:
    - `--help`: Displays the help panel.
    - `-v`: Shows the version of the framework.
    - `-p <payloadN.json>`: Executes the framework with a specified payload 
      JSON file. This option is particularly useful for Red Teams.
    - `-c <command>`: Executes a specific command using LazyOwn, for 
      example, `ping`.
    - `--no-banner`: Runs the framework without displaying the banner.
    - `-s`: Runs the framework with root privileges.
    - `--old-banner`: Displays the old banner.

Example:
    To see the help panel, call the function as follows:
    
    >>> halp()

Note:
    - This function exits the program after displaying the help information,
      using `sys.exit(0)`.

## ensure_tmux_session
Ensure that a tmux session is active.

This function checks whether a specified tmux session is currently running.
If the session does not exist, it creates a new tmux session with the specified
name and executes the command to run the LazyOwn RedTeam Framework script.

The function uses the `tmux has-session` command to check for the existence
of the session. If the session is not found (i.e., the return code is not zero),
it will create a new tmux session in detached mode and run the command 
`./run --no-banner` within that session.

Args:
    session_name (str): The name of the tmux session to check or create.

Example:
    To ensure that a tmux session named 'lazyown_sessions' is active,
    call the function as follows:
    
    >>> ensure_tmux_session('lazyown_sessions')

Note:
    - Ensure that tmux is installed and properly configured on the system.
    - The command executed within the tmux session must be valid and
      accessible in the current environment.

## get_xml
Retrieves a list of XML files from the specified directory.

Args:
    directory (str): The directory to search for XML files.

Returns:
    list: A list of XML filenames found in the specified directory.

## get_domain_from_xml
Extrae el primer dominio o dirección IP de un archivo XML de un escaneo Nmap.

## shellcode_to_sylk
No description available.

## get_banner
No description available.

## list_binaries
List all executable binaries in the specified directory.

Parameters:
directory (str): The directory to search for binaries. Defaults to 'sessions'.

Returns:
list: A list of paths to executable binaries.

## select_binary
Prompt the user to select a binary from a list.

Parameters:
binaries (list): A list of binary paths.

Returns:
str: The path of the selected binary.

## decode
Decodes base64 data received from the server output.

Parameters:
data (str): Encoded base64 data from the server.

Returns:
str: Decoded string output, or an error message if decoding fails.

## get_command
Reads a command from standard input and initiates a thread to send the command to the target server.

## send_command
Constructs and sends an SQL payload with xp_cmdshell and certutil for command execution and exfiltration.

Parameters:
cmd (str): Command to be executed on the remote MSSQL server.

## activate_server
Activates the HTTP server and fetches the first command from the user.

Parameters:
httpd (HTTPServer): The server instance to activate.

## Spray
No description available.

## ProcessResults
No description available.

## generate_index
Generates an APT repository structure and index files for proper compatibility.

Parameters:
repo_dir (str): Path to the repository directory.

Returns:
None

## replace_variables
Replace variables in a command string with their corresponding values.

This function takes a command string and a dictionary of variables and their values.
It replaces each occurrence of a variable in the command string with its corresponding value.

Args:
    command (str): The command string containing variables to be replaced.
    variables (dict): A dictionary where the keys are the variables to be replaced
                      and the values are the corresponding values to replace them with.

Returns:
    str: The command string with all variables replaced by their corresponding values.

Example:
    command = "Hello, \$name! You have \$amount dollars."
    variables = {"\$name": "Alice", "\$amount": 100}
    result = replace_variables(command, variables)
    print(result)  # Output: "Hello, Alice! You have 100 dollars."

## create_caldera_config
Creates a Caldera configuration file with the specified content at the given file path.

Parameters:
file_path (str): The path where the configuration file will be created.

Returns:
None

## extract_banners
Extract banner information from an XML file.

This function parses an XML file and extracts banner information for each host and port.
The banner information includes the hostname, port, protocol, extra details, and service.

Args:
    xml_file (str): The path to the XML file to be parsed.

Returns:
    list: A list of dictionaries, where each dictionary contains banner information for a specific host and port.
          Each dictionary has the following keys:
            - hostname (str): The hostname of the host.
            - port (str): The port number.
            - protocol (str): The protocol used (e.g., tcp, udp).
            - banner (str): Extra information about the service.
            - service (str): The name of the service running on the port.

Example:
    banners = extract_banners('path/to/file.xml')

## generate_xor_key
Generate key XOR long specifyed

:param length: Lenght of XOR key
:return: Key XOR in hex.

## scrape_news
Realiza una solicitud a la página de noticias de Hacker News y extrae los títulos, enlaces y puntuaciones de las noticias.

Returns:
    tuple: Tres listas conteniendo los títulos, enlaces y puntuaciones de las noticias respectivamente.

## display_news
Crea un DataFrame de pandas y lo imprime, mostrando los títulos, enlaces y puntuaciones de las noticias.

Args:
    titles (list): Lista de títulos de las noticias.
    links (list): Lista de enlaces de las noticias.
    scores (list): Lista de puntuaciones de las noticias.

## htmlify
Wrap C2 comms in html and html2 code to make requests look more legitimate

## de_htmlify
Cleant wrap C2 comms of html and html2 code to get the command from request

## is_port_in_use
No description available.

## return_creds
No description available.

## query_arin_ip
Queries ARIN whois API for organization information of an IP address.

Args:
    ip: The IP address to query.

Returns:
    A dictionary containing IP information or None on failure.

## get_org
Extracts organization name from ARIN whois response data.

Args:
    data: The JSON data from the ARIN whois API response.

Returns:
    The organization name or "null" if not found.

## load_payload
No description available.

## load_adversary
No description available.

## replace_placeholders
Replace placeholders in a template string with values from a dictionary.

Parameters:
    template (str): The template string containing placeholders.
    replacements (dict): A dictionary where keys are placeholders and values are replacements.

Returns:
    str: The template string with placeholders replaced.

## replace_command_placeholders
Replace placeholders in a command string with values from a params dictionary,
handling spaces within placeholders.

The function looks for placeholders in curly braces (e.g., {url} or { url }) within
the command string and replaces them with corresponding values from the params dictionary,
ignoring any spaces inside the curly braces.

Args:
    command (str): The command string containing placeholders.
    params (dict): A dictionary containing key-value pairs for replacement.

Returns:
    str: The command string with placeholders replaced by their corresponding values.

## parse_nmap_csv
No description available.

## query_ollama
Envía consulta a Ollama y retorna respuesta del modelo

## preprocess_llm_response
Pre-process LLM response to handle common issues before YAML parsing

## manual_yaml_extraction
Fallback method to manually extract YAML data from malformed content

## create_synthetic_yaml
Create a basic synthetic YAML playbook when all else fails

## parse_yaml_response
Improved function to extract and parse YAML content from LLM response
with better error handling and recovery attempts

## fix_common_yaml_issues
Fixes common YAML formatting issues

## aggressive_yaml_fix
More aggressive YAML fixing for recovery attempts

## save_playbook
Guarda el playbook generado en disco

## load_knowledge_base
Carga la base de conocimientos personalizada.

## anti_debug
No description available.

## wrapper
internal wrapper of internal function to implement multiples rhost to operate. 

## send_request
No description available.

## handle_forms
No description available.

## replace_match
No description available.

## log_request
No description available.

## log_message
No description available.

## GET
No description available.

## __init__
No description available.

## open_file
Open and parse the IP-to-ASN file.

## open_reader
Parse the reader stream, handling both regular and gzipped files.

## _parse_file
Parse the TSV data and load it into memory.

## as_of_ip
Return the ASN associated with the given IP address.

## _rec_index_has_ip
Check if the given index contains the IP.

## as_name
Get the AS name by ASN.

## as_country
Get the country by ASN.

## __init__
No description available.

## __getitem__
No description available.

## __init__
Inicializa el escáner con las cabeceras HTTP predefinidas.

## search_cves
Busca CVEs basados en un servicio específico.

Args:
    service (str): El servicio para buscar vulnerabilidades relacionadas.

Returns:
    list: Lista de diccionarios con información sobre cada CVE o mensaje de error.

## search_cve_details
Añade detalles adicionales a la información del CVE.

Args:
    cve_info (dict): Información básica del CVE incluyendo id y descripción.

## pretty_print
Imprime una tabla bonita con detalles de CVEs.

Args:
    cves_details (list): Lista de CVEs con toda la información recopilada.

## __init__
No description available.

## __getitem__
No description available.

