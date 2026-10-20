# Metasploitable 2 Gym

I keep one exploit, one chain and one index entry for every
Metasploitable 2 vector I emulate. The index is
`playbooks/gym_metasploitable.yaml`; the loader is
`modules/metasploitable_gym.py`; the runtime artefacts are the normal
`exploits/*.yaml` and `chains/*.yaml` files.

## Matrix

The shipped index covers 45 vectors:

- FTP: vsftpd 2.3.4 backdoor, ProFTPD anonymous.
- SSH, Telnet, SMTP, DNS, rlogin.
- SMB: Samba username map script.
- Web and OWASP: phpMyAdmin, DVWA SQLi/blind SQLi, reflected/stored/DOM
  XSS, CSRF, LFI, file upload, brute force, command injection,
  Mutillidae XSS/LFI/RFI/command injection/CSRF, PHP-CGI argument
  injection, TWiki XSS, Axis2, WebDAV PUT, Apache TRACE, Shellshock,
  Tomcat Manager.
- Remote services: Java RMI, ingreslock, UnrealIRCd, distcc.
- Data and desktop: NFS exports, MySQL root, PostgreSQL default,
  VNC, X11.

Every entry names its `exploit` id and `chain` name. The validator
refuses a matrix where either file is missing or the chain defaults do
not match.

## Commands

```bash
gym_ms2 list
gym_ms2 chains
gym_ms2 validate
chain list gym
gym_ms2 info ms2_distcc_exec
gym_ms2 chain ms2_distcc_exec
apt_chain gym_metasploitable_ms2_distcc_exec 172.17.0.2
apt_chain gym_metasploitable_ms2_distcc_exec 172.17.0.2 --dry-run
```

The per-vulnerability chain inherits `gym_metasploitable_chain`:

1. bind the target (`assign target`);
2. scan once (`lazynmap`, skipped when the XML exists);
3. run the selected YAML exploit with `--feed`;
4. mirror the loop graphs (`lazy_sync`);
5. refresh the session report (`create_session_json`);
6. open the interactive shell (`atomic_shell --interactive`).

Every exploit outcome goes through `atomic_exploit_bridge.record_outcome`
and the outcome bus, so the world model, kill-chain, intel graph, attack
graph, C2 banners/CVEs/notes, objectives and report stay current.

## Lab

```bash
lab start metasploitable
# prints the container IP and the assign command, starts Apache
# and applies the gym migrations automatically
assign rhost <container-ip>
gym start metasploitable_full_chain
apt_chain gym_metasploitable_ms2_tomcat_manager <container-ip>
```

The Docker lab maps the container ports; the classic VM flow lives in
`scripts/lazy_msf_lab.sh`. Both are lab-only and in-scope targets only.

### Gym migrations

The stock `tleemcjr/metasploitable2` image boots only a subset of the
services the matrix needs. `modules/metasploitable_migrations.py` ships
an ordered, idempotent migration list that is applied automatically on
every `lab start metasploitable` (both on first create and when the
container is already running). Each step checks whether the fix is
already present and only runs the change when it is not.

| Migration | What it fixes |
|-----------|---------------|
| `core-services` | Starts apache2, xinetd, proftpd, postfix, mysql, portmap, samba, postgresql, tomcat and distccd (all idempotent starts) |
| `rservices-access` | Trusts telnet/rlogin/rsh/exec from the docker subnet in `/etc/hosts.allow` and adds `pts/0-5` to `/etc/securetty` |
| `proftpd-anonymous` | Adds the `<Anonymous ~ftp>` block so anonymous FTP answers |
| `xvnc-open` | Restarts Xtightvnc with an open display (`-ac`) and a valid font path |
| `shellshock-cgi` | Installs the deliberately vulnerable `/usr/lib/cgi-bin/status` bash CGI |
| `mutillidae-rfi-payload` | Installs `/var/www/ms2_rfi.txt`, the remote-include payload |
| `php-allow-url-include` | Sets `allow_url_include = On` in both php.ini files and restarts Apache |
| `mutillidae-database` | Runs the mutillidae setup page (populates `owasp10`) and mirrors it into `metasploit` (the schema the app reads) |
| `dvwa-dom-page` | Installs the canonical DVWA DOM XSS page; the DVWA build shipped in the image predates `xss_d` |
| `bind-udp-fallback` | Installs and starts the python2.5 `/usr/local/sbin/lz_dns_server.py` so `dig @<target>` returns answered A records (named cannot capset in a container) |
| `nfs-mountd-fallback` | Starts userspace `rpc.mountd` (plus portmap and an `/` export entry) so `showmount -e` answers without kernel nfsd |
| `rlogin-root-trust` | Writes `+ +` to `/root/.rhosts`, allows the loopback client in `hosts.allow` for rsh/rlogin and starts xinetd so the container-local root client reaches the trusted r-services |

To run the migrations by hand:

```bash
python3 -c "from modules.metasploitable_migrations import apply_migrations; print(apply_migrations('lazyown-lab-metasploitable'))"
```

The subnet prefix defaults to `172.17.0.` and can be changed with
`apply_migrations(container, subnet="192.168.7.")` when the lab network
differs. `atomic_clean --hard` destroys the container; recreating it
with `lab start metasploitable` re-applies every migration.

### Headless browser vectors

Three vectors execute their payload in a real browser session instead
of detecting a server-side reflection:

- `ms2_dvwa_xss_dom` — loads the DVWA DOM XSS page with an attribute
  breakout payload (`'></select><script>...`) and beacons the cookie to
  a local capture listener.
- `ms2_twiki_xss` — the TWiki `bin/oops` endpoint reflects `param1`
  unescaped; the headless browser executes the beacon script.
- `ms2_mutillidae_csrf` — the capture listener serves an attacker page
  whose form auto-submits a blog entry, then a mysql check verifies the
  entry persisted.

They need chromium, chromedriver and the selenium Python package
(`sudo apt install -y chromium chromium-driver python3-selenium`). The
spec commands resolve the system interpreter explicitly
(`env PATH=/usr/bin:/bin:/usr/sbin:/sbin python3`) because the project
virtualenv may lack these packages.

### Verified matrix state

With the migrations applied, every tablet in the 45-vector matrix runs
through `atomic_exploit_bridge run --feed` on a docker lab (fresh
container, all migrations from a bare image).

Three vectors historically failed on Docker limitations; each now has a
sixth lab-side fallback migration that makes the vector validate:

- `ms2_dns_recursion` — bind still cannot capset inside a container,
  so `bind-udp-fallback` serves answered A records over UDP/53 from a
  python2.5 responder (`/usr/local/sbin/lz_dns_server.py`).
- `ms2_nfs_exports` — kernel nfsd still needs a module the container
  lacks, so `nfs-mountd-fallback` starts userspace `rpc.mountd`
  (enough for `showmount -e` to list `/`).
- `ms2_rlogin_trust` — non-root clients still cannot reserve a source
  port below 1024, so `rlogin-root-trust` trusts the container-local
  root client (`/root/.rhosts` with `+ +` and 127.0.0.1 entries in
  `hosts.allow`) and the spec falls back to `rsh` and to
  `docker exec lazyown-lab-metasploitable sh -c 'rsh -l root 127.0.0.1 id'`.
  Operator-host runs that need root on the source port use
  `sudo` (an elevated `retry loop --sudo` session provides it).

### Shell attribution

Shell sessions are per-vector: `modules/atomic_exploit_bridge.py` keeps
a port-ownership registry (`_PORT_OWNERS`) so a shell opened by one
spec is never adopted and misattributed by another. `live_sessions()`
reports the owning spec id for every cached session.

## Gym catalogue and run state

The gamified gym catalogue lives in `gyms/*.yaml` (one file per gym).
`lazy_orchestrator` exposes the same catalogue in its **Gyms** tab:
`space` starts the selected gym (or stops its active runs), `a` creates a
definition, `e` edits the raw YAML with validation, and `d` deletes it
after confirmation. A definition with active runs cannot be deleted.

Active runs are persisted in `sessions/world_model.json` under the
`gyms` section, not in per-operator files. Run identifiers are stable
(`gym0001`, `gym0002`, ...), so status survives sessions and can be
queried directly:

```bash
gym list
gym start first_implant --target 172.20.0.20
gym status
gym status gym0001
gym stop gym0001
gym stop first_implant
gym stop                      # stop every active gym
gym submit gym0001 --techniques implant_deploy,beacon_callback
gym top
```

`gym status` lists every active run with its run id, operator, elapsed
time and target. `gym stop` without arguments stops every active gym;
with a run id, challenge id or display name it stops only the matching
runs. `gym submit` requires a run id when more than one gym is active.

A shell opened with `atomic_shell` is not a gym run. `gym status` shows
live shells and compromised hosts as engagement context, but scoring
starts only with an explicit `gym start`. Hosts outside the current
`rhost` are ignored rather than shown as engagement state. If an old
world model holds stale loopback hosts, remove one explicitly:

```bash
rm_wm_host 127.0.0.1
python3 -m modules.world_model reset-host 10.0.0.5
```

`rm_wm_host` is the shell alias for `python3 -m modules.world_model
remove-host <ip>` (declared in `cli/aliases.yaml`).

## Adding a vector


1. Add the exploit YAML under `exploits/`.
2. Add the chain YAML under `chains/`, extending the gym base.
3. Add the index entry to `playbooks/gym_metasploitable.yaml`.
4. Run `gym_ms2 validate` and `pytest tests/test_metasploitable_gym.py`.

When the vector needs a lab adjustment (a service, a config flag, a
payload file), add it to `modules/metasploitable_migrations.py` as a new
idempotent migration so fresh gym containers get it automatically on
`lab start metasploitable`.

`tools/generate_metasploitable_gym.py` holds the catalogue table used to
regenerate the shipped files when several vectors change at once.

## Tests

`tests/test_metasploitable_gym.py` pins index completeness, exploit and
chain loadability, dry-run resolution without unresolved tokens and clear
errors for a broken matrix. `tests/test_apt_chain_integration.py` pins the
real cmd2 path: raw output visible, no boolean leak, interactive shell on
the calling thread. `tests/test_lab_target_visibility.py` pins the IP and
assign line in `lab start` and `lab status`.
