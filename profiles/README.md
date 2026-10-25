# Scan Profiles

Predefined scan profiles for LazyOwn reconnaissance and assessment pipelines.

| Profile | File | Purpose |
|---------|------|---------|
| Attack Surface | `attack_surface.yaml` | Full external/internal attack surface enumeration |
| Cloud Assessment | `cloud_scan.yaml` | Cloud infrastructure discovery (AWS, GCP, Azure) |
| Supply Chain | `supply_chain_scan.yaml` | Third-party and supply chain risk assessment |
| Example | `example.yaml` | Template with all available scanning options |

Usage: `pipeline run <profile_name>` from the LazyOwn CLI.
