# Outcome sinks

One module per shared surface. Every sink exposes `apply(event)` and
returns a boolean. The outcome bus owns ordering, deduplication and
failure isolation; a sink never calls another sink.

| Module | Surface | Notes |
|--------|---------|-------|
| `world_model.py` | `sessions/world_model.json` | hosts, services, vulns, credentials, notes |
| `killchain.py` | `modules/killchain.py` | advances the unified phase |
| `routing.py` | `modules/lazy_intel.py` | routing priors and dataset rows |
| `c2_surfaces.py` | `sessions/banners.json`, `cves.json`, `notes.txt` | dashboard tables |
| `objectives.py` | `sessions/objectives.jsonl` | actionable follow-up queue |
| `event_bus.py` | `sessions/events.jsonl` | universal event envelope |
| `intel_graph.py` | `sessions/intel_summary.json` | fused intel graph summary |
| `attack_graph.py` | `sessions/intel_summary.json` | attack surface graph summary |
| `report.py` | `sessions/sessionLazyOwn.json` | terminal report refresh |
| `campaign_db.py` | `sessions/db/lazyown.db` | opt-in campaign mirror |
| `world_diff.py` | `sessions/lazy_changes.jsonl` | per-host snapshot diffs |
| `beacon_dispatch.py` | `sessions/beacon_dispatch_<host>.txt` | stages the catch-back command |
| `chain_feed.py` | `sessions/lazy/activity_<task>.jsonl`, `exp_<task>.json` | streams `chain_step` events into the loop |

Heavy sinks (`intel_graph`, `attack_graph`, `report`) run only for event
kinds that can change their content. `campaign_db` is opt-in through the
event sink list so routine loop traffic never opens the database.
`chain_feed` only accepts `chain_step` events: chain steps publish with
the explicit sink list `["chain_feed", "event_bus"]`, so the other sinks
never see per-step traffic.
