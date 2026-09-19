"""Generate LazyOwn demo GIFs without external services."""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 800, 450
BG = (13, 17, 23)
FG = (0, 255, 0)
ACCENT = (0, 200, 255)
DIM = (140, 140, 140)


def font(size=20):
    """Resolve a monospace font with stdlib fallback."""
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render(lines, path, hold=30):
    """Render terminal line-by-line frames."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fnt = font(18)
    frames = []
    for count in range(1, len(lines) + 1):
        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)
        draw.text((20, 14), "LazyOwn - demo", font=fnt, fill=ACCENT)
        y = 55
        for prev in lines[:count]:
            draw.text((20, y), prev[:52], font=fnt, fill=FG if prev.startswith("(") else DIM)
            y += 26
        frames.append(img)
        frames.append(img.copy())
    for _ in range(hold):
        frames.append(frames[-1].copy())
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=400, loop=0)
    print(f"wrote {path} ({len(frames)} frames)")


GOLDEN = [
    "$ git clone https://github.com/grisuno/LazyOwn.git && cd LazyOwn",
    "$ bash install.sh",
    "(LazyOwn) > doctor   # all green",
    "(LazyOwn) > wizard   # auto-detects lhost",
    "(LazyOwn) > assign rhost 10.10.11.5",
    "(LazyOwn) > ping && lazynmap && auto_populate && facts_show",
    "(LazyOwn) > recommend_next  # ranked next steps",
    "(LazyOwn) > engage 10.10.11.5  # one-command auto-pwn",
]
C2 = [
    "(LazyOwn) > blacksandbeacon  # Linux BOF-capable beacon addon",
    "(LazyOwn) > c2_quickstart  # AES key + beacon one-liners",
    "(LazyOwn) > collab_join alice  # multi-operator team server",
    "# https://<lhost>:<c2_port>/collab/?operator=alice",
    "(LazyOwn) > campaign  # shared campaign state",
    "(LazyOwn) > pentest_report  # auto-generated report",
]
MCP = [
    "$ claude mcp add lazyown python3 ./skills/lazyown_mcp.py",
    "claude > lazyown_session_init()  # JSON SITREP",
    "claude > lazyown_recommend_next()  # 3-5 ranked cmds",
    "claude > lazyown_run_command('lazynmap', dry_run=true)",
    "# 153 tools: recon, C2, phishing, playbooks, reporting",
]


def main():
    """Render the three core GIFs."""
    out = "assets/demo"
    render(GOLDEN, f"{out}/golden-path.gif")
    render(C2, f"{out}/c2-collab.gif")
    render(MCP, f"{out}/mcp-ai.gif")


if __name__ == "__main__":
    main()
