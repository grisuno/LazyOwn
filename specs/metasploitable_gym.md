# Metasploitable 2 Gym Specification

I define the lab matrix contract. The index names every vector and the
validator proves the exploit and chain still exist.

## Index

File: `playbooks/gym_metasploitable.yaml`

- `name`, `version`, `target`, `description`.
- `vulnerabilities`: list of entries with `id`, `name`, `cve`, `mitre`,
  `port`, `service`, `severity`, `confidence`, `exploit`, `chain`.

The shipped index covers 45 vectors: service exploits, web application
flaws (SQLi, blind SQLi, reflected/stored XSS, CSRF, LFI, file upload,
brute force, command injection), Mutillidae, phpMyAdmin, PHP-CGI,
WebDAV, TRACE, SMTP relay, MySQL file read, NFS, VNC, X11, Tomcat,
Java RMI, distcc, UnrealIRCd, ingreslock, SSH, Telnet and FTP.
Existing `vsftpd_backdoor` and `samba_usermap` are referenced, not
reimplemented.

## Chains

Every entry has `chains/gym_metasploitable_<id>.yaml` extending
`gym_metasploitable_chain` and pinning `exploit`, `vuln` and `port`.

The base chain:

1. `assign target <target>`
2. `lazynmap <target>` skipped when the scan XML exists
3. `python3 modules/atomic_exploit_bridge.py run --id <exploit> ... --feed`
4. `lazy_sync`
5. `create_session_json`
6. `atomic_shell --interactive <target>`

## Validation

`modules/metasploitable_gym.py` accepts `list`, `validate`, `info` and
`chain`. It rejects missing index fields, duplicate ids, unknown
exploits, unknown chains and chain defaults that do not match the index.

## Lab

`lab start metasploitable` prints the container IP and the
`assign rhost` line, and starts Apache when the image booted without it.
Use the container IP for native ports; use `127.0.0.1` only with the
host-mapped ports.

## Acceptance

- `gym_ms2 validate` returns `OK`.
- Every chain resolves without unresolved tokens.
- Every exploit loads under the bridge schema.
- The final step is the interactive shell.
- Tests: `tests/test_metasploitable_gym.py`,
  `tests/test_apt_chain_integration.py`,
  `tests/test_lab_target_visibility.py`.
