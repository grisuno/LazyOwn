# LazyOwn launch kit. Copy-paste for HN, Reddit, X, Discord, LinkedIn.

## Hacker News (Show HN)

Title: Show HN: LazyOwn – OSS red-team C2 with Linux BOF, YARA/Nuclei marketplaces, 153 MCP tools

Body:
I built LazyOwn, a GPLv3 red-team framework (741 CLI commands, multi-operator
C2, phishing engine). Three things no other OSS C2 has in one place:
1. Linux BOF support (ELF dlopen beacon),
2. built-in YARA + Nuclei marketplaces (one-command install),
3. a 153-tool MCP server so Claude/agents can run engagements.
Try without installing: docker run -it ghcr.io/grisuno/lazyown:latest
Golden path: ping > lazynmap > auto_populate > facts_show > recommend_next,
or just: engage <ip>. Honest comparison vs Sliver/Havoc/Mythic/Caldera/MSF in
COMPARISON.md. Roast my architecture, I read everything.

## Reddit r/netsec, r/hacking, r/redteam

Title: [OSS] LazyOwn – 741-command red-team framework with AI agents and Linux BOF beacon

Body: 5-min quickstart in QUICKSTART.md, 80/20 guide in ESSENTIALS.md,
full HTB Lame walkthrough in docs/examples/. Docker one-liner, wizard setup,
multi-operator collab. Looking for contributors: YARA/Nuclei templates are
good-first-issues. GPLv3, Kali/Parrot/Docker.

## X / Twitter thread

1/ LazyOwn: OSS red-team C2 with Linux BOF, YARA+Nuclei marketplaces, 153 MCP
tools for AI agents. docker run -it ghcr.io/grisuno/lazyown:latest
2/ Golden path: ping > lazynmap > auto_populate > facts_show >
recommend_next. Or one command: engage <ip>.
3/ Multi-operator collab + phishing engine + auto reports (md/docx).
Demo GIFs in README. Comparison vs Sliver/Mythic/Havoc in COMPARISON.md.
4/ Contributors wanted: one-command YARA/Nuclei template PRs. Good first
issues labeled. GPLv3.

## Discord / LinkedIn

LazyOwn v0.2.161: autonomous auto_pwn, hunt recon, YARA+Nuclei marketplaces,
ELO/badges, session encryption, 7 APT playbooks. Docker-ready, MCP-native
for Claude. QUICKSTART 5 min. Stars/forks welcome, issues answered.
