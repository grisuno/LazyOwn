# UTILS.md Documentation  by readmeneitor.py

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

## getprompt
Generate a command prompt string with network information and user status.

:param: None

:returns: A string representing the command prompt with network information and user status.

Manual execution:
To manually get a prompt string with network information and user status, ensure you have `get_network_info()` implemented to return a dictionary of network interfaces and their IPs. Then use the function to create a prompt string based on the current user and network info.

Example:
If the function `get_network_info()` returns:
    {
        'tun0': '10.0.0.1',
        'eth0': '192.168.1.2'
    }

And the user is root, the prompt string generated might be:
    [LazyOwn👽10.0.0.1]# 
If the user is not root, it would be:
    [LazyOwn👽10.0.0.1]$ 

If no 'tun' interface is found, the function will use the first available IP or fallback to '127.0.0.1'.

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
No description available.

## is_package_installed
Check if a Python package is installed.

:param package_name: Name of the package to check.
:returns: True if installed, False otherwise.

## extract
No description available.

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
No description available.

## get_credentials
Searches for credential files with the pattern 'credentials*.txt' and allows the user to select one.

The function lists all matching files and prompts the user to select one. It then reads the selected file
and returns a list of tuples with the format (username, password) for each line in the file.

Returns:
list of tuples: A list containing tuples with (username, password) for each credential found in the file.
                If no files are found or an invalid selection is made, an empty list is returned.

## wrapper
internal wrapper of internal function to implement multiples rhost to operate. 

