# LazyOwn vs Other Open-Source Red Team Frameworks

Honest, side-by-side comparison. Updated 2026-05-17.

If you find a row that is inaccurate, open an issue. We will fix it. We would
rather lose a tick than mislead an operator.

---

## At a glance

| Capability | LazyOwn | Sliver | Havoc | Mythic | Empire 5.x | Caldera | Metasploit |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Active OSS development | yes | yes | yes | yes | yes | yes | yes |
| License | GPLv3 | GPLv3 | GPLv3 | BSD-3 | BSD-3 | Apache-2 | BSD-3 |
| Single-binary install path | yes | yes | partial | container only | yes | partial | yes |
| Operator CLI (interactive) | yes (cmd2) | yes | partial | partial | yes | no (web) | yes |
| Operator web UI | yes (Flask) | no | yes (Qt) | yes (React) | yes (Starkiller) | yes | no |
| Multi-operator collaboration | yes (SSE + locks) | yes (multiplayer) | yes | yes | partial | yes | no (msfrpcd) |
| Windows beacon (in-memory) | yes (Go + C) | yes | yes (Demon) | yes (many) | yes | yes (sandcat) | yes |
| Linux beacon | yes (Go + C) | yes | partial | yes | yes (Starkiller) | yes (sandcat) | yes |
| macOS beacon | yes (Go) | yes | no | yes | partial | yes | yes |
| **Linux BOF support** | **yes (ELF dlopen)** | **no** | **no** | **no** | **no** | **no** | **no** |
| Windows BOF support | partial (via beacon.yaml addon) | yes (COFF loader) | yes | yes (apollo, athena) | partial | no | no |
| Malleable C2 HTTP profile | yes | yes | yes | yes (via containers) | partial | partial | yes (advanced) |
| DNS C2 | yes (built-in resolver) | yes | partial | yes | yes | no | yes |
| TLS / mTLS | yes (self-signed + mTLS-ready) | yes | yes | yes | yes | partial | yes |
| Built-in phishing engine | yes (templates + SMTP + tracker) | no | no | no | partial | no | no (msfvenom only) |
| Recon / scanning suite bundled | yes (nmap, gobuster, ffuf, enum4linux, responder, etc.) | no | no | no | partial | no | partial |
| MITRE ATT&CK adversary emulation | yes (`playbooks/apt_*.yaml`) | no | no | partial | no | **yes (primary use case)** | partial |
| Automated kill-chain loop | yes (`autonomous_daemon`) | no | no | no | no | yes (operations) | no |
| LLM-assisted operator (built-in) | **yes** (Groq, Ollama, Claude via MCP) | no | no | no | no | no | no |
| Multi-agent AI (hive-mind / MoE) | **yes** (SWAN + hive_mind) | no | no | no | no | no | no |
| MCP server for Claude / agents | **yes (95+ tools)** | no | no | no | no | no | no |
| Knowledge graph navigation | yes (`graphify-out/`) | no | no | no | no | no | no |
| Knowledge bases (GTFOBins, LOLBas, ATT&CK) | yes (parquet) | no | no | no | no | partial | yes (modules db) |
| Plugin system | yes (YAML addons + Lua + .tool) | yes (armory + extensions) | yes (modules) | yes (containers) | yes (modules) | yes (plugins) | yes (modules) |
| Reporting (auto-generated) | yes (Markdown + DOCX + executive JSON) | no | no | no | no | yes | partial |
| Decoy / deception landing site | yes (canary, webcam capture) | no | no | no | no | no | no |
| Container image (official) | yes (`lazyown-docker/`) | yes | yes | yes (compose) | yes | yes | yes |
| Active campaign state on disk | yes (`sessions/`) | yes | yes | yes | yes | yes | yes (db) |
| Free for commercial use | yes (GPLv3) | yes | yes | yes | yes | yes | yes (community) |

Legend: yes = first-class, partial = present but limited or experimental, no = not implemented.

---

## Where LazyOwn wins today

**Linux BOF.** As of 2026-05-17 LazyOwn is the only open-source C2 framework
shipping a Beacon Object File runtime for Linux targets. BOFs are compiled
as position-independent ELF shared objects and loaded via `dlopen` into the
running beacon. The `datap` API is source-compatible with the Windows BOF
contract, so porting an existing BOF means swapping Win32 calls for Linux
syscalls or libc equivalents. See `docs/PORTING_BOFS_TO_LINUX.md`.

**Adversary emulation.** Seven YAML profiles ship under `playbooks/`: APT28,
APT29, APT41, Conti, FIN7, Lazarus, and LockBit. Each maps to MITRE group
IDs and references published CTI. Replay one with `playbook_run apt_apt28`.

**AI-native operations.** Every other framework treats LLMs as an add-on. In
LazyOwn the model orchestrates the engagement: `autonomous_daemon` drives a
reward-shaped kill chain, `swan_ensemble` routes tasks through a mixture of
experts, and `hive_spawn` runs role-specialised drones in parallel. The MCP
server exposes 95+ tools to Claude Code so the operator can drive the whole
framework from a conversational interface.

**Breadth in a single repo.** Recon, exploitation, lateral movement,
credential access, persistence, C2, phishing, and reporting all ship in one
install. No glue between four projects, no separate framework for each
phase.

**Reproducible campaign state.** Everything lands in `sessions/`. Restart
the shell, restore the directory on another box, and the campaign keeps
going. Reporting reads the same artefacts the operator does.

---

## Where the alternatives win today

**Sliver.** More mature implant ecosystem on Windows. COFF loader for
Windows BOFs is battle-tested. Better support for cross-compilation of
implants out of the box. If your engagement is Windows-only and you do not
need AI orchestration, Sliver is a strong default.

**Havoc.** Best-in-class operator desktop UI. The Demon agent has excellent
Windows tradecraft. If your team values a polished native GUI over a web
dashboard plus CLI, Havoc is the better visual experience.

**Mythic.** Containerised payload architecture lets you mix language-agnostic
agents (Apollo, Athena, Poseidon, Medusa). If you need to swap implants per
target environment, Mythic's model is more flexible than LazyOwn's
single-beacon-family approach.

**Caldera.** MITRE-funded, designed around adversary emulation as the
primary use case. If your engagement is purple-team or detection
validation rather than penetration testing, Caldera's operation/adversary
abstractions map more directly to that workflow.

**Metasploit.** Largest exploit module library and the deepest history of
hardening. If you need exploits for a specific CVE today, Metasploit is
still the fastest path.

**Empire 5.x.** Most polished PowerShell tradecraft for legacy Windows
estates. If your scope is heavily AD-focused on Windows-only targets,
Empire's modules remain very strong.

---

## When NOT to pick LazyOwn

- **You need a stable Cobalt-Strike-shaped Windows engagement and nothing
  else.** Sliver or Havoc will feel more familiar.
- **You require FedRAMP/government certification.** None of the OSS C2s
  qualify; you need a commercial product.
- **You operate without internet access and cannot use a hosted LLM.** The
  AI features degrade gracefully (Ollama is supported locally), but the full
  experience assumes Groq or another API. Without any LLM, the differentiator
  shrinks to recon breadth and Linux BOF.
- **You want a desktop GUI as the primary interface.** LazyOwn ships
  `lazygui/` and a Textual TUI, but Havoc's Qt UI is more polished today.

---

## Roadmap to close known gaps

Tracked in GitHub issues, summarised here:

- Windows COFF loader parity with Sliver inside the Go beacon.
- ARM/IoT beacon (`blackzincbeacon`) for embedded targets.
- Operator handbook with screenshots and a guided demo engagement.
- Reproducible end-to-end demo video pinned to the README.
- Signed releases (cosign) and SBOM publication.
- Plugin marketplace index at addons.lazyown.io.

---

## How we keep this honest

Every claim in the table above is testable from the repo. If you can show
an addon, route, or `do_*` command that contradicts a "no", we owe you a
patch. Pull requests against this file are welcome.
