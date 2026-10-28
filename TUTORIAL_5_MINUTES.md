# LazyOwn in 5 minutes

A complete engagement loop with three commands and zero configuration.
No AI providers, no MCP servers, no lab containers: if you have
LazyOwn installed and an authorized target, this works.

Only rule: you must own authorization for the target you point this at.

## 1. Install (2 minutes)

```bash
curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh -o /tmp/bootstrap.sh \
  && bash /tmp/bootstrap.sh
```

Already cloned? Then:

```bash
cd LazyOwn
bash install.sh    # virtualenv + pinned dependencies + C2 certificates
./run              # launches the LazyOwn shell
```

First boot opens a setup wizard; press enter through it and you are
done. The default install is light. If `doctor` turns anything red it
prints the exact install line for the missing piece.

## 2. Point at the target (30 seconds)

Inside the `(LazyOwn) >` shell:

```text
doctor                  # preflight check
wizard                  # guided config, auto-detects your IP
assign rhost 10.10.10.5 # your authorized target
```

## 3. Recon to next-step recommendation (90 seconds)

```text
ping                    # is the target alive, which OS
lazynmap                # full port + service scan
auto_populate           # parse the scan into structured facts
facts_show              # what do we know now
recommend_next          # the 3-5 highest-ranked next commands
```

That is the whole engine: every scan writes artefacts under `sessions/`,
the facts feed the recommenders, and the recommender stays one command
ahead of you.

## 4. Exploit and verify (60 seconds)

Pick the vector `recommend_next` surfaced, for example:

```text
search 445              # searchsploit for the exposed service
auto_loop               # autonomous recon+scan+exploit chain
```

Prefer manual control? Run the specific exploit verb it suggested.

## 5. Persist and hand off (30 seconds)

```text
note            # quick note into the session store
db_notes        # list the notes you collected
lazyreport      # structured report from the session facts
```

## Where to go next

- [`ESSENTIALS.md`](ESSENTIALS.md) — the 18 commands that cover 80% of engagements.
- [`CHEATSHEET.md`](CHEATSHEET.md) — ~40 frequent commands by user goal.
- [`docs/autonomous-loop.md`](docs/autonomous-loop.md) — when you are
  ready for hands-free operation: `auto_loop` can drive this whole
  tutorial for you, with pacing, fallback chains and resumable
  checkpoints.
- [`docs/mcp-setup.md`](docs/mcp-setup.md) — optional: connect an AI
  agent to the same engine.

You never have to go further. Everything above — install, scan, attack,
report — works exactly like this on every engagement.
