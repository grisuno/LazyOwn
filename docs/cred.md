# Cred Phase Guide

Credential Access — harvest, crack, spray or forge credentials to enable lateral movement and further access.

All commands below abstract their arguments through ``payload.json``. Set ``rhost``, ``lhost``, ``domain``, ``wordlist`` and credentials once; the framework substitutes them automatically. Never pass raw IP addresses or credentials as positional arguments.

## Commands

| Command | Description | Source |
|---------|-------------|--------|

| `do_addusers` | Opens or creates the users.txt file in the sessions directory for editing using nano. | `lazyown.py` |
| `do_adsso_spray` | Performs a password spray attack on Azure Active Directory Seamless Single Sign-On (SSO) using a specified list of users. | `lazyown.py` |
| `do_cewl` | This function constructs and executes a command for the 'cewl' tool. | `lazyown.py` |
| `do_crack_cisco_7_password` | Crack a Cisco Type 7 password hash and display the plaintext. | `lazyown.py` |
| `do_createcredentials` | Creates a `credentials.txt` file in the `sessions` directory with the specified username and password. | `lazyown.py` |
| `do_createhash` | Creates a `hash.txt` file in the `sessions` directory with the specified hash value and analyzes it using `Name-the-hash`. | `lazyown.py` |
| `do_createmail` | Generate email permutations based on a full name and domain, then save them to a file. | `lazyown.py` |
| `do_createusers_and_hashs` | Command createusers_and_hashs: Extracts usernames and hashes from a dump file. | `lazyown.py` |
| `do_cred` | Display the credentials stored in the `credentials.txt` file and copy the password to the clipboard. | `lazyown.py` |
| `do_creds_py` | Searches for default credentials associated with a specific product or vendor, using the Default Credentials Cheat Sheet. | `lazyown.py` |
| `do_crunch` | Generate a custom dictionary using the `crunch` tool. | `lazyown.py` |
| `do_cubespraying` | Command cubespraying: Automates the installation and usage of CubeSpraying for performing credential spraying attacks. | `lazyown.py` |
| `do_dacledit` | Execute the dacledit.py command for a specific user or all users listed in the users.txt file. | `lazyown.py` |
| `do_generatedic` | Generates a wordlist based on a target name and a list of characters, with various combinations. | `lazyown.py` |
| `do_hashcat` | Runs Hashcat with specified attack mode and hash type using a wordlist. | `lazyown.py` |
| `do_hydra` | Uses Hydra to perform a brute force attack on a specified HTTP service with a user and password list. | `lazyown.py` |
| `do_john2hash` | Runs John the Ripper with a specified wordlist and options. | `lazyown.py` |
| `do_john2keepas` | List all .kdbx files in the 'sessions' directory, let the user select one, and run the | `lazyown.py` |
| `do_john2zip` | List all .zip files in the 'sessions' directory, let the user select one, and run the command | `lazyown.py` |
| `do_keepass` | Open a .kdbx file and print the titles and contents of all entries. The password can be provided through | `lazyown.py` |
| `do_medusa` | Uses medusa to perform a brute force attack on a specified ssh service with a user and password list. | `lazyown.py` |
| `do_passtightvnc` | Decrypts TightVNC passwords using Metasploit. | `lazyown.py` |
| `do_passwordspray` | Perform password spraying using crackmapexec with the provided parameters. | `lazyown.py` |
| `do_refill_password` | Generate a list of possible passwords by filling each asterisk in the input with user-specified characters. | `lazyown.py` |
| `do_rocky` | Reduces a wordlist based on the specified password length. | `lazyown.py` |
| `do_searchhash` | Helps to find hash types in Hashcat by searching through its help output. | `lazyown.py` |
| `do_smalldic` | Handles the creation of temporary files for users and passwords based on a small dictionary. | `lazyown.py` |
| `do_spraykatz` | Executes the Spraykatz tool to retrieve credentials on Windows machines and large Active Directory environments. | `lazyown.py` |
| `do_sshkey` | Generates an SSH key pair with RSA 4096-bit encryption. If no name is provided, it uses 'lazyown' by default. | `lazyown.py` |
| `do_transform` | Transforms the input string based on user-defined casing style. | `lazyown.py` |
| `do_username_anarchy` | Generate usernames using the username-anarchy tool based on user input. | `lazyown.py` |

## Next Phase

After completing the Cred phase, proceed to:
**Lateral Movement** (`docs/lateral.md`)

---
*Generated from ``cli/command_index.json``. Keep this guide in sync by running ``python3 scripts/build_command_index.py`` after adding new commands.*

