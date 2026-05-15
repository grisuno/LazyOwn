# parquets

Columnar knowledge bases in Apache Parquet format. Read at query time by
`skills/lazyown_parquet_db.py` via the MCP tool `lazyown_parquet_query`.
Never modified during an engagement — treat as read-only reference data.

## Files

| File | Rows | Description |
|------|------|-------------|
| `techniques.parquet` | ~750 | MITRE ATT&CK techniques: ID, name, tactic, platform, description. |
| `techniques_enriched.parquet` | ~750 | Same as above plus detection notes, data sources, and mitigation IDs. |
| `binarios.parquet` | ~250 | GTFOBins index: binary name, function (shell, upload, download, sudo, etc.), command template. |
| `detalles.parquet` | ~250 | GTFOBins detail: full command examples and notes per binary/function pair. |
| `lolbas_index.parquet` | ~180 | LOLBas index: binary name, type, OS version, description. |
| `lolbas_details.parquet` | ~180 | LOLBas detail: full command examples per binary. |

## Querying from MCP

```
lazyown_parquet_query(mode="context", phase="enum", target="10.10.11.5")
lazyown_parquet_query(mode="gtfobins", binary="find")
lazyown_parquet_query(mode="lolbas", binary="certutil")
lazyown_parquet_query(mode="attack", tactic="persistence", platform="linux")
```

## Querying from Python

```python
import pandas as pd
df = pd.read_parquet("parquets/techniques.parquet")
linux_persistence = df[(df.tactic == "persistence") & (df.platform.str.contains("Linux"))]
```

## Updating the knowledge bases

The parquet files are generated from public upstream datasets. To rebuild:

```bash
# Rebuild MITRE ATT&CK parquets from the STIX JSON
python scripts/build_attack_parquet.py

# Rebuild GTFOBins parquets from the upstream YAML corpus
python scripts/build_gtfobins_parquet.py
```

These scripts are not included in the default install because the upstream
datasets are large. Use the pre-built files in normal operation.

## Session knowledge base

A seventh parquet, `sessions/session_knowledge.parquet`, is written during
engagements to store discovered facts (services, credentials, findings) in
columnar format for fast cross-session queries. It is excluded from git.
