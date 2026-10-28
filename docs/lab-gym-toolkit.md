# Lab Gym Toolkit

Disposable, lab-only attack surfaces plus the knowledge tools adopted
from the open awesome-redteam collection. Everything here runs against
machines the framework itself creates; nothing targets infrastructure
you do not own. Recent commits covered by this guide: the winbox gym
bootstrap, the AD Docker gym, the lab-only scope guard, the lazycreds
knowledge base, the lazyoob canary, the web exploitation playbook and
the lazykerninc addon.

## AD lab gym on Docker

`ad-lab` is a single disposable Samba Active Directory DC container
(`nowsci/samba-domain`): Kerberos 88, LDAP 389, SMB 445, Kpasswd 749.
It boots in roughly ninety seconds and `lab stop ad-lab` removes it.
No ports are published to the host; the gym attacks the container IP
on the Docker bridge directly.

    lab start ad-lab            # pull, boot, wait for the DC, create fixtures
    gym start ad_lab_apt        # registers the run, boots the lab, auto-launches the chain
    lab stop ad-lab             # destroy

The scenario carries its environment (domain `lazylab.local`) and
documented fixture passwords as constants in `modules/lab_runtime.py`.
`start()` waits for the DC, then idempotently creates the `svc_sql`
service account with an SPN. `--privileged` is required: Samba sysvol
ACL provisioning denies it otherwise.

The matrix mirrors the Metasploitable 2 gym: five vectors, one exploit
spec and one chain each, plus the golden path.

| Vector | MITRE | What it proves |
|--------|-------|----------------|
| `ad_ldap_enum` | T1069.002 | LDAP naming contexts and users |
| `ad_smb_shares` | T1135 | SMB share discovery |
| `ad_rid_cycling` | T1087.001 | Domain users via RID cycling |
| `ad_samr_enum` | T1087.002 | Domain users with zero credentials (null session) |
| `ad_default_creds` | T1110.001 | Default credential confirmed against SMB |

Golden path: `apt_chain apt_ad_lab <container-ip>`. Evidence checkers
added to `ctf_capture`: `kerberos_ticket` (masked), `domain_enum`,
`smb_shares`. The Kerberoast vector was replaced by the SAMR
null-session enum because impacket TGS requests against this Samba KDC
fail with `KRB_AP_ERR_INAPP_CKSUM`; the limitation is documented, not
hidden.

## WinBox gym: self-healing bootstrap

The Windows lab (`winbox`, headless Windows VM via libvirt) is the
second gym scenario. `gym start winbox_windows_apt` runs the full
bootstrap and every stage streams live output; long child stages echo
through a pty so colours and console output survive, and transcripts
land in `sessions/winbox/*.log`.

Stage order: install, prereqs, snapshot gate, ISO download, VM build,
recovery, boot, provisioning invariant, resolve. Two behaviours make it
resilient:

- Mid-install recovery: when the upstream `winbox setup` exits on an
  in-flight install, the module waits for the guest to shut down, then
  completes winbox phases 2-4 (offline virt-customize injection,
  boot-for-provisioning, network filter, `clean` snapshot) through the
  upstream internals with the process locale forced to C. A dirty NTFS
  disk after a forced stop is repaired with `ntfsfix`. A full rebuild
  is the explicit, loud fallback.
- Provisioning invariant: after boot, the Z: drive probe runs with
  retries; a missing drive triggers one idempotent `winbox provision`
  re-run and a re-probe. Nothing is silently skipped: every stage
  records ok/fail in the returned `stages` map and the CLI prints the
  stage table.

All winbox and virsh children run with `LANG=C LC_ALL=C` and VM state
strings are normalised through canonical aliases (English and Spanish),
so no state gate depends on shell locale.

## Gym chain auto-launch

`gym start <challenge>` auto-launches the challenge chain whenever the
lab is up and the chain resolved, for every scenario with a chain and
an IP (Docker containers, the WinBox VM). `--no-chain` suppresses it.
The chain target is the resolved lab IP; `rhost` is bound before the
first step.

## Lab-only scope guard

The autonomous loop treats an empty scope as lab-only by default
(`modules/lazy_scope.py`, wired into the loop's scope check): RFC1918
targets and lab scenarios pass, public targets are blocked until the
operator records an explicit scope in `sessions/scope_allow.txt`.
Fail-closed on unresolved hosts; the verdict is recorded as loop
activity (`scope-lab-default`).

## lazycreds: default-credential knowledge base

Search-and-export layer over ~3.4k vendor/user/password triples from
the open DefaultCreds-Cheat-Sheet (MIT), shipped as
`modules/data/default_creds.csv` and loaded by `modules/lazy_creds.py`.
Pure file reads; no network.

    lazycreds <query>           # vendor or username substring search
    lazycreds --top 10          # most repeated pairs, ranked for sprays
    lazycreds --export file     # user:pass lines for hydra/medusa/spray tools

Programmatic surface for chains and gym exploits: `search`, `candidates`,
`export_pairs`. The AD gym's `ad_default_creds` vector uses it for
context alongside the live credential check.

## lazyoob: OOB callback canary

Local HTTP canary for blind SSRF and RCE confirmation. Binds to `lhost`
from payload.json, serves unique token paths `/oob/<token>`, records
hits in memory and mirrors them to `sessions/oob_hits.jsonl`. It never
parses or proxies anything.

    lazyoob start [host] [port] # start listener (defaults: lhost, ephemeral)
    lazyoob url [token]         # the callback URL to inject into payloads
    lazyoob hits [token]        # observed callbacks, newest last
    lazyoob stop                # shut down, report hit count

Chain pattern: `lazyoob start`, run the payload with the callback URL,
`lazyoob hits <token>`.

## Web exploitation playbook

`playbooks/web_exploitation_awesome.yaml` distils the awesome-redteam
web flows into technique steps: 40x bypass (alternate verbs, header and
proxy confusion, path normalisation) and SQL injection discovery
(error, boolean, time-based probes). It loads through the standard
playbook engine:

    apt_playbook list
    apt_playbook run web_exploitation_awesome

`AptPlaybookEngine` globs `playbooks/*.yaml`, so the recommendation
surface (PlaybookSignal) offers it to the autonomous loop like any
other playbook.

## lazykerninc addon: CVE-2026-40369 lab evidence

`lazyaddons/lazy_kernel_increment.yaml` packages the public kernel
address-increment PoC (upstream credit: Ori Nimron) as a lab-only
command: it cross-compiles with mingw-w64, stages through the WinBox
shared folder and executes inside the lab VM only. The
`chains/apt_winbox_kerninc.yaml` chain wraps it with snapshot
containment, guest liveness and event-log evidence.

Validated end to end against the Windows 11 lab VM: the PoC bugchecked
the guest with `0x50` at `0xffff800041424344`, matching the published
claim (events 1001/41/6008). Snapshot containment: pre-kerninc, run,
post-kerninc.

## Where things live

| Piece | Files |
|-------|-------|
| AD gym | `modules/ad_gym.py`, `playbooks/gym_ad_lab.yaml`, `exploits/ad_lab_*.yaml`, `chains/gym_ad_lab_*.yaml`, `chains/apt_ad_lab.yaml`, `gyms/ad_*.yaml` |
| WinBox gym | `modules/winbox_gym.py`, `cli/commands/winbox_gym.py` |
| Scope guard | `modules/lazy_scope.py`, `modules/lazy_loop.py` |
| lazycreds | `modules/lazy_creds.py`, `modules/data/default_creds.csv`, `cli/commands/lazy_creds.py` |
| lazyoob | `modules/lazy_oob.py`, `cli/commands/lazy_oob.py` |
| Web playbook | `playbooks/web_exploitation_awesome.yaml` |
| Kerninc addon | `lazyaddons/lazy_kernel_increment.yaml`, `chains/apt_winbox_kerninc.yaml` |
