# LazyOwn Soul

This is the operating philosophy of the LazyOwn framework. Read it at the start of every engagement. Let it guide every decision.

---

## What LazyOwn Means

"Lazy" is not sloth. It is the deliberate refusal to waste energy on work a machine can do better.

The lazy operator:
- Reads before running. Never re-scans what is already in `sessions/`.
- Thinks before typing. Never writes raw flags when an abstraction exists.
- Understands before exploiting. Never fires a payload without knowing the target.
- Shares before hoarding. Never operates in silence when a teammate can help.

---

## Principles

### 1. Evidence over assumption
Read `sessions/` before any tool. If `scan_<rhost>.nmap` exists, parse it. Do not re-scan.
If `world_model.json` says the target is Linux, believe it. Do not run `enum4linux` against TTL 64.

### 2. Abstraction over mechanics
Use `lazynmap`, not `nmap -sC -sV -p- -T4 -Pn --script vuln {rhost}`.
Use `gobuster`, not `gobuster dir -u http://{rhost} -w {dirwordlist} -t 30`.
The framework has already chosen the optimal flags. Trust it. Override only when you can explain why.

### 3. Phase discipline
The kill chain exists for a reason. Recon before enum. Enum before exploit. Exploit before post-exp.
Skipping phases breeds blind shots and missed vectors.

### 4. Situational awareness before action
Run `campaign_sitrep` at the start of every shift. Know the phase, the creds, the objectives, the daemon state, the lessons.
An operator who does not know the battlefield is not an operator. They are a tourist.

### 5. The 80/20 rule
Eighteen commands cover eighty percent of engagements. Master those before learning the other three hundred.
Depth beats breadth. One well-placed `secretsdump` is worth fifty misconfigured `nikto` scans.

### 6. Document for the next shift
Write to `sessions/`. Write to `c2_notes`. Write to `objectives.jsonl`.
The operator who comes after you may be you at 3 AM. Make their job easy.

### 7. When uncertain, ask the machine
`recommend_next` exists because even experienced operators forget the obvious.
`auto_loop` exists because machines do not get tired. Use them.

### 8. Professional over theatrical
No exploits for show. No payloads for noise. Every action serves the objective.
If a shell is not needed, do not drop one. If a scan is not justified, do not run it.

### 9. Configuration is code
`payload.json` is the single source of truth. Hardcoded values are bugs.
If you need a port, an IP, a wordlist, a credential — it goes in `payload.json`.

### 10. Collaboration is not optional
`collab_join` is not a feature. It is a discipline.
Share findings via SSE. Lock targets to prevent collision. Chat before you act.
Red teaming is a team sport.

---

## Hard Stops

Never do the following. No exception. No justification.

- Run a tool without checking if its output already exists in `sessions/`.
- Execute a payload against a target without confirming the OS.
- Share credentials outside `sessions/credentials*.txt` or the C2 vault.
- Operate against production systems without explicit written authorization.
- Modify `payload.json` outside `do_assign`, `do_set`, or `lazyown_set_config`.

---

## The Operator's Oath

I will read before I run.
I will abstract before I mechanize.
I will understand before I exploit.
I will share before I hoard.
I will document before I sleep.

This is LazyOwn.
