# Install profiles: `light` vs `full`

LazyOwn ships two install profiles. `full` is the default and preserves every
current behavior. `light` is shell + C2 + recon core for constrained machines,
quick triage, or operators who never touch the AI features.

| Capability | `full` (default) | `light` |
|------------|------------------|---------|
| Interactive shell (`./run`), 748 commands | yes | yes |
| C2 server, beacons, phishing, collab | yes | yes |
| Recon, enum, exploit, AD tooling | yes | yes |
| Session reports (`pandas`), parquet KBs (`pyarrow`), graphs (`networkx`) | yes | no |
| LLM backends (`groq`, wizard provider step) | yes | no (step skipped) |
| ML stack (`--with-ml`: torch, sklearn) | opt-in | opt-in |

## Select at install time

```bash
bash install.sh --profile light     # requirements-light.txt
bash install.sh                     # full (default)
```

Forwarded through the one-liner:

```bash
curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh | bash -s -- --profile light
```

## Select at runtime

```bash
LAZYOWN_PROFILE=light ./run
```

`doctor` applies the same rule: under `light` it does not require `pandas`,
`pyarrow`, `networkx`, or `groq`. An unknown value fails loudly (`ValueError`,
surfaced as a `doctor` warning) instead of silently changing behavior.

Missing packages degrade only their own feature — the shell keeps running.
Audit any install without launching the shell with `python3 -m core.dependencies`.
