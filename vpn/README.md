# vpn

VPN configuration storage for engagement connectivity. Place OpenVPN `.ovpn`
files or WireGuard `.conf` files here to manage target network access.

This directory is intentionally excluded from git. VPN credentials must never
be committed to the repository.

## Usage

```bash
# Connect to a HackTheBox VPN
sudo openvpn vpn/htb_lab.ovpn

# Or from within LazyOwn
(LazyOwn) > assign vpn_file vpn/htb_lab.ovpn
(LazyOwn) > lazynmap       # runs after VPN is confirmed up
```

The framework reads `payload.json["vpn_file"]` to know which VPN config to
reference. Set it with:

```
(LazyOwn) > assign vpn_file vpn/your_config.ovpn
```

## File naming convention

Use descriptive names that identify the platform and date:

```
htb_lab_2026-05.ovpn
tryhackme_2026-05.ovpn
client_engagement_2026.ovpn
```

## Security note

VPN configuration files often contain embedded certificates and pre-shared
keys. Never commit them to version control. The `.gitignore` at the repo root
excludes this entire directory.
