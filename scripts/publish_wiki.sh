#!/usr/bin/env bash
#
# Publish LazyOwn documentation to the GitHub wiki.
#
# The wiki is a separate git repository (https://github.com/grisuno/LazyOwn.wiki.git).
# This script clones it (or pulls latest), regenerates pages from the
# documentation that already exists in this repository, commits, and pushes.
#
# Usage:
#   bash scripts/publish_wiki.sh [--dry-run] [--no-push] [--wiki-dir <path>]
#
#   --dry-run        Generate pages locally without committing or pushing.
#   --no-push        Commit locally but do not push to GitHub.
#   --wiki-dir <p>   Directory for the wiki checkout (default: /tmp/lazyown-wiki).
#
# Idempotent: re-running it refreshes every page from current sources.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WIKI_URL="https://github.com/grisuno/LazyOwn.wiki.git"
WIKI_DIR="/tmp/lazyown-wiki"
DRY_RUN=0
PUSH=1

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=1; PUSH=0; shift ;;
        --no-push) PUSH=0; shift ;;
        --wiki-dir) WIKI_DIR="$2"; shift 2 ;;
        --wiki-dir=*) WIKI_DIR="${1#--wiki-dir=}"; shift ;;
        -h | --help) grep '^#' "$0" | grep -v '^#!' | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "[ERROR] Unknown option: $1" >&2; exit 2 ;;
    esac
done

log() { echo "[$1] $2"; }
fail() { log "ERROR" "$1" >&2; exit 1; }

command -v git >/dev/null 2>&1 || fail "git is required."
command -v gh >/dev/null 2>&1 || fail "gh is required (https://cli.github.com)."
gh auth status >/dev/null 2>&1 || fail "gh is not authenticated. Run: gh auth login"

gh auth setup-git >/dev/null 2>&1 || log WARN "gh auth setup-git failed; continuing with existing git credentials."

if [[ -d "$WIKI_DIR/.git" ]]; then
    log INFO "Updating existing wiki checkout at $WIKI_DIR."
    git -C "$WIKI_DIR" pull --ff-only || fail "Could not fast-forward the wiki checkout."
else
    log INFO "Cloning wiki into $WIKI_DIR."
    git clone "$WIKI_URL" "$WIKI_DIR" || fail "Could not clone the wiki. Create at least one page via the GitHub web UI first."
fi

cd "$WIKI_DIR"
WIKI_BRANCH="$(git branch --show-current)"
log INFO "Wiki branch: ${WIKI_BRANCH:-HEAD (detached)}"

write_home() {
    cat > Home.md <<'EOF'
# LazyOwn Wiki

> **748 CLI commands. Multi-operator C2. 153 MCP tools for AI agents. The only OSS C2 with Linux BOF support + built-in YARA/Nuclei marketplaces.**

## Install in one command

```bash
curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh | bash
```

The installer clones into `~/LazyOwn`, installs dependencies, then asks whether to start a normal `./run` session or the full `fast_run_as_r00t.sh` stack. See [[Installation]] for options.

## Start here

| Page | Content |
|------|---------|
| [[Installation]] | One-liner, manual install, launch modes |
| [[Quickstart]] | From fresh clone to first engagement (5 minutes) |
| [[Essentials]] | The 18 commands that cover 80% of engagements |
| [[Cheatsheet]] | The next 40 frequent commands by goal |
| [[Architecture]] | How the framework is organized (consumers) |
| [[Collaboration]] | Multi-operator C2: SSE stream, publish, target locks |
| [[Beacons]] | Linux BOF beacon: build, deliver, port from Windows |
| [[C2-and-API]] | Web C2 dashboard and REST API |
| [[Plugins-Marketplace]] | YAML addons, Lua plugins, YARA + Nuclei |

Full 748-command reference: [COMMANDS.md](https://github.com/grisuno/LazyOwn/blob/main/COMMANDS.md).
Main repository: [grisuno/LazyOwn](https://github.com/grisuno/LazyOwn).
EOF
}

write_installation() {
    cat > Installation.md <<'EOF'
# Installation

## One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh | bash
```

With options (forwarded through the pipe):

```bash
curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh | bash -s -- --with-tools --dir ~/pentest/LazyOwn
```

| Option | Effect |
|--------|--------|
| `--dir <path>` | Install directory (default `~/LazyOwn`) |
| `--branch <name>` | Git branch (default `main`) |
| `--with-tools` | apt-install gobuster, ffuf, enum4linux, seclists, responder, ... |
| `--with-ollama` | Install the local Ollama runtime |
| `--with-ml` | Install the heavy torch/CUDA + sklearn stack (~2 GB) |
| `--existing update\|clean\|abort` | Existing-checkout policy without prompting |
| `--profile light\|full` | Install profile: `full` (default) or `light` (shell + C2 + recon core, no analytics/AI stack; runtime equivalent: `LAZYOWN_PROFILE=light`) |
| `--run-mode normal\|fast\|none` | Launch mode without prompting |
| `--no-run` | Install only, do not launch |

If `~/LazyOwn` already exists, the installer asks whether to update in place (`git pull` + reinstall), do a clean reinstall (backing up `payload.json` to `/tmp` first), use another directory, or abort.

## Manual install

```bash
git clone https://github.com/grisuno/LazyOwn.git && cd LazyOwn
bash install.sh        # virtualenv + pinned dependencies + C2 certificates
./run                  # launches the shell; first run offers the setup wizard
```

`install.sh` is idempotent: re-running it updates in place.

## Launch modes

- `./run` — normal interactive session.
- `sudo ./fast_run_as_r00t.sh` — full stack as root (C2, VPN, tmux services).

After install, run `doctor` inside the shell to verify, then `wizard` for guided setup. See [[Quickstart]].
EOF
}

write_c2_api() {
    {
        echo "# C2 and REST API"
        echo ""
        echo "## Web C2 dashboard"
        echo ""
        cat "$REPO_ROOT/docs/c2.md"
        echo ""
        echo "## REST API"
        echo ""
        echo "Versioned endpoints live under \`/api/v1\` (see [openapi.yaml](https://github.com/grisuno/LazyOwn/blob/main/docs/openapi.yaml)):"
        echo ""
        echo "| Method | Endpoint | Purpose |"
        echo "|--------|----------|---------|"
        echo "| GET | \`/api/v1/health\` | Service and subsystem status |"
        echo "| GET | \`/api/v1/targets\` | Hosts in scope (from the campaign database) |"
        echo "| GET | \`/api/v1/results\` | Beacon task results |"
        echo "| GET | \`/api/v1/campaigns\` | Autonomous campaign status |"
        echo "| POST | \`/api/v1/webhooks\` | Register result webhooks |"
        echo ""
        echo "Mutating endpoints require a tenant API key (see \`core/api_authz.py\`)."
    } > C2-and-API.md
}

write_plugins() {
    {
        echo "# Plugins and Marketplace"
        echo ""
        echo "## Plugins"
        echo ""
        tail -n +2 "$REPO_ROOT/plugins/README.md"
        echo ""
        echo "## LazyAddons"
        echo ""
        tail -n +2 "$REPO_ROOT/lazyaddons/README.md"
    } > Plugins-Marketplace.md
}

write_sidebar() {
    cat > _Sidebar.md <<'EOF'
## LazyOwn

- [[Home]]
- [[Installation]]
- [[Quickstart]]
- [[Essentials]]
- [[Cheatsheet]]
- [[Architecture]]
- [[Collaboration]]
- [[Beacons]]
- [[C2-and-API]]
- [[Plugins-Marketplace]]

[Repository](https://github.com/grisuno/LazyOwn) · [Full command reference](https://github.com/grisuno/LazyOwn/blob/main/COMMANDS.md)
EOF
}

write_footer() {
    cat > _Footer.md <<'EOF'
*Generated from the [LazyOwn repository docs](https://github.com/grisuno/LazyOwn) by `scripts/publish_wiki.sh`. Do not edit here — edit the source and re-run the script.*
EOF
}

log INFO "Generating wiki pages."
write_home
write_installation
cp "$REPO_ROOT/QUICKSTART.md" Quickstart.md
cp "$REPO_ROOT/ESSENTIALS.md" Essentials.md
cp "$REPO_ROOT/CHEATSHEET.md" Cheatsheet.md
cp "$REPO_ROOT/CORE.md" Architecture.md
cp "$REPO_ROOT/docs/collaboration.md" Collaboration.md
cp "$REPO_ROOT/docs/beacons-linux-bof.md" Beacons.md
write_c2_api
write_plugins
write_sidebar
write_footer

if [[ "$DRY_RUN" -eq 1 ]]; then
    log INFO "Dry run: pages generated in $WIKI_DIR, nothing committed."
    git status --short
    exit 0
fi

git add -A
if git diff --cached --quiet; then
    log INFO "Wiki is already up to date. Nothing to commit."
    exit 0
fi

GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-LazyOwn Agent}"
GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-agent@lazyown.local}"
export GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL
GIT_COMMITTER_NAME="${GIT_COMMITTER_NAME:-$GIT_AUTHOR_NAME}"
GIT_COMMITTER_EMAIL="${GIT_COMMITTER_EMAIL:-$GIT_AUTHOR_EMAIL}"
export GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL

git commit -q -m "Docs: refresh wiki pages from repository docs" || fail "Commit failed."
log OK "Committed wiki refresh."

if [[ "$PUSH" -eq 1 ]]; then
    git push origin "$WIKI_BRANCH" || fail "Push failed. Check token scopes (needs Contents read/write)."
    log OK "Wiki pushed: https://github.com/grisuno/LazyOwn/wiki"
else
    log INFO "Skipping push (--no-push). Push later from $WIKI_DIR."
fi
