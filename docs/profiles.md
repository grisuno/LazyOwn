# Install profiles: `light` vs `full`

LazyOwn ships two install profiles. `full` is the default and preserves every
current behavior. `light` is shell + C2 + recon core for constrained machines,
quick triage, or operators who never touch the AI features.

| Capability | `full` (default) | `light` |
|------------|------------------|---------|
| Interactive shell (`./run`), full command set | yes | yes |
| C2 server, beacons, phishing, collab | yes | yes |
| Recon, enum, exploit, AD tooling | yes | yes |
| Local LLM / OpenAI-compatible client (loop, llama.cpp, Ollama) | yes | yes |
| Session reports (`pandas`), parquet KBs (`pyarrow`), graphs (`networkx`), STIX | `analytics` extra | no |
| Cloud LLM backends (`groq`, `anthropic`) | `ai` extra | no |
| Cloud recon/exfil (`boto3`) | `cloud` extra | no |
| Keyword RAG index (in base; no vector store) | — | no |
| ML stack (`--with-ml`: torch, sklearn, seaborn) | opt-in | opt-in |

## Dependency tiering

`pyproject.toml` is the single source of truth. The base `dependencies` are
exactly the light core (shell + C2 + recon/exploit); everything heavier lives
in a named extra:

| Extra | Packages | Purpose |
|-------|----------|---------|
| `analytics` | pandas, pyarrow, numpy, networkx, stix2 | reports, parquet KBs, graphs |
| `ai` | groq, anthropic | cloud LLM providers |
| `cloud` | boto3 | cloud-provider recon and exfiltration |
| `rag` | — | retired: the vector store was removed; keyword index is built-in |
| `ml` | torch, torchvision, torchaudio, scikit-learn, seaborn, joblib | heavy ML stack |

The three lock files are regenerated from `pyproject.toml` by resolving it in a
clean virtualenv (never `pip freeze` of a working env) — see
`scripts/regen_locks.sh`:

- `requirements-light.txt` = base, resolved as a strict subset of the full lock.
- `requirements.txt` = `.[analytics,ai,cloud,rag]` (full core, no ML).
- `requirements-ml.txt` = the `.[ml]` additions on top of the full lock.

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
