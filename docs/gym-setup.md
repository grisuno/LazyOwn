# Metasploitable 2 Gym — System Setup

How to configure a machine so the Metasploitable 2 practice gym works
out of the box: prerequisites, the automatic lab migrations, the
headless browser vectors, the state-at-rest password and the verified
vector matrix.

Target audience: an operator who just cloned the repository and wants
the gym running. For the catalogue internals (index, chains, adding
vectors) read `docs/metasploitable-gym.md`.

---

## Prerequisites

| Dependency | Install | Why |
|------------|---------|-----|
| Docker | `sudo apt install docker.io && sudo systemctl start docker` | The gym runs in a container |
| Chromium + driver | `sudo apt install -y chromium chromium-driver` | The browser-backed exploit specs drive a real browser |
| Selenium (system Python) | `sudo apt install -y python3-selenium` | The browser specs are plain `python3 -c` scripts using selenium |
| `sshpass` | `sudo apt install -y sshpass` | Specs verify shells over SSH with `sshpass -e` |
| `hydra`, `mysql`, `nmap`, `msfconsole` | ship with Kali/Parrot; on Debian install `hydra mysql-client nmap metasploit-framework` | Used by the corresponding specs |

Install them once:

```bash
sudo apt install -y docker.io chromium chromium-driver python3-selenium sshpass
```

No user-specific absolute paths are required; everything reads
`payload.json` and the repo layout.

---

## Spin up the gym

```bash
(LazyOwn) > lab start metasploitable
(LazyOwn) > assign rhost <container-ip>
```

`lab start metasploitable` pulls the image, starts the container, starts
Apache and then applies the gym migrations automatically. The console
prints one line per migration step:

```
[*] Applying gym migrations...
    [ ok ] core-services
    [skip] rservices-access: already applied
    ...
```

The migrations are idempotent: on every subsequent `lab start` they
detect the fixes and skip. Running `atomic_clean --hard` destroys the
container; recreating it re-applies everything.

---

## What the migrations install

`modules/metasploitable_migrations.py` ships an ordered list of
idempotent fixes for the stock `tleemcjr/metasploitable2` image, which
boots only a subset of the services the matrix needs:

| Migration | Fix |
|-----------|-----|
| `core-services` | Starts apache2, xinetd, proftpd, postfix, mysql, portmap, samba, postgresql, tomcat and distccd |
| `rservices-access` | Adds telnet/rlogin/rsh/exec entries for the docker subnet to `/etc/hosts.allow`, adds `pts/0-5` to `/etc/securetty` |
| `proftpd-anonymous` | Adds the `<Anonymous ~ftp>` block so anonymous FTP answers |
| `xvnc-open` | Restarts Xtightvnc with an open display (`-ac`) and a valid font path |
| `shellshock-cgi` | Installs the deliberately vulnerable `/usr/lib/cgi-bin/status` bash CGI |
| `mutillidae-rfi-payload` | Installs `/var/www/ms2_rfi.txt`, the remote-include payload |
| `php-allow-url-include` | Sets `allow_url_include = On` in both php.ini files and restarts Apache |
| `mutillidae-database` | Runs the mutillidae setup page (populates `owasp10`) and mirrors it into `metasploit`, the schema the app reads |
| `dvwa-dom-page` | Installs the canonical DVWA DOM XSS page; the image's DVWA build predates `xss_d` |

The subnet prefix defaults to `172.17.0.` (the default docker bridge).
Change it in code when the lab network differs:

```python
from modules.metasploitable_migrations import apply_migrations
apply_migrations("lazyown-lab-metasploitable", subnet="192.168.7.")
```

---

## Run the vectors

Each vector has one exploit YAML and one chain. The chain binds the
target, scans once (reusing `sessions/scan_<rhost>.nmap.xml`), runs the
exploit with `--feed` and refreshes every surface:

```bash
(LazyOwn) > apt_chain gym_metasploitable_ms2_dvwa_sqli --target <ip> --json
(LazyOwn) > apt_chain gym_metasploitable_ms2_samba_usermap --target <ip> --json
(LazyOwn) > apt_chain gym_metasploitable_ms2_tomcat_manager --target <ip> --json
```

Outcomes land in `sessions/outcomes.jsonl` (one event per attempt) and
the world model advances the host to `owned`. Inspect the per-vector
state:

```bash
(LazyOwn) > facts_show
(LazyOwn) > gym status
```

### Headless browser vectors

Three vectors execute their payload in a real browser session; the
capture listener binds on the attacker host, so the default
`lhost 127.0.0.1` from the chain works without any routing setup:

- `ms2_dvwa_xss_dom` — DVWA DOM XSS page with an attribute breakout
  payload (`'></select><script>...`); the beacon image request proves
  the JavaScript executed.
- `ms2_twiki_xss` — the TWiki `bin/oops` endpoint reflects `param1`
  unescaped; the headless browser executes the beacon.
- `ms2_mutillidae_csrf` — the listener serves an attacker page whose
  form auto-submits a blog entry; a mysql check then verifies the
  entry persisted.

These specs call the system interpreter explicitly
(`env PATH=/usr/bin:/bin:/usr/sbin:/sbin python3`) so they work even
when the project virtualenv lacks selenium.

---

## State-at-rest password

Session state (`sessions/world_model.json`) encrypts at rest on shell
close (PBKDF2HMAC + Fernet, see `cli/auto_crypto.py`). On startup the
shell decrypts it transparently. The password resolution order:

1. `LAZYOWN_MASTER_PASSWORD` environment variable (export it in the
   session or in a wrapper script when you want an explicit password);
2. the authenticated CLI operator, derived as `lazyown:<operator>` —
   the same key material the login session uses, so MCP subprocesses
   and background loops read the encrypted state without extra setup.

Nothing else to configure: when you log in as an operator the state
decrypts automatically; external tools reading `sessions/world_model.json`
get the plaintext view through the same fallback.

---

## Verified matrix

With the migrations applied, 42 of the 45 shipped vectors yield a shell
(verified per-vector via `apt_chain` and the outcome bus). The three
remaining failures are Docker limitations, not framework gaps:

| Vector | Limitation |
|--------|------------|
| `ms2_dns_recursion` | bind9 cannot start inside the container (capset blocked by the container runtime) |
| `ms2_nfs_exports` | nfsd needs a kernel module the container lacks |
| `ms2_rlogin_trust` | rlogin requires a privileged source port (below 1024) |

---

## Troubleshooting

**`No module named 'telnetlib'` inside specs** — the project virtualenv
runs Python 3.13+, where telnetlib was removed from the standard
library. The shipped telnet spec uses plain sockets, so this only
affects custom specs that still import telnetlib; rewrite them with
`socket` like `exploits/ms2_telnet_default_creds.yaml`.

**Playwright raises `Connection closed while reading from the driver`**
— the Debian `python3-playwright` package lacks its node driver. The
browser specs use selenium + `/usr/bin/chromedriver` instead, which is
why `chromium-driver` is in the prerequisite list.

**bind9 refuses to start (`capset failed`)** — expected inside Docker;
`ms2_dns_recursion` stays an honest failure.

**Empty sweep reports** — make sure `payload.json` has `rhost` set and
`lab start metasploitable` ran at least once so the migrations seeded
the services.

**MCP tools not appearing** — restart the MCP client; register the
server with `bash scripts/setup_hermes_mcp.sh`.
