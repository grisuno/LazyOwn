# lazyadversaries

YAML adversary simulation profiles used by the `apt_playbooks` module and the
autonomous daemon. Each file maps a named threat actor or malware family to a
sequence of MITRE ATT&CK techniques backed by Atomic Red Team test IDs.

Distinct from `playbooks/` in scope: files here are authoritative threat actor
profiles (static reference data). Files in `playbooks/` are engagement-specific
attack plans generated or customised per target.

## Files

| File | Threat actor | Primary MITRE tactics |
|------|-------------|----------------------|
| `apt_apt28.yaml` | APT28 / Fancy Bear (GRU) | Credential access, lateral movement, exfiltration |
| `apt_apt29.yaml` | APT29 / Cozy Bear (SVR) | Persistence, defense evasion, C2 |
| `apt_apt41.yaml` | APT41 (dual espionage + financial) | Initial access, execution, privilege escalation |
| `apt_conti.yaml` | Conti ransomware group | Execution, lateral movement, impact |
| `apt_fin7.yaml` | FIN7 / Carbanak | Spearphishing, credential access, collection |
| `apt_lazarus.yaml` | Lazarus Group (North Korea) | Supply chain, financial theft, destructive ops |
| `apt_lockbit.yaml` | LockBit ransomware | Lateral movement, data encryption, extortion |

## Profile YAML structure

```yaml
apt_name: apt28
description: "APT28 (Fancy Bear) — GRU Unit 26165 TTPs based on published CTI"
mitre_groups: ["G0007"]
references:
  - "https://attack.mitre.org/groups/G0007/"
phases:
  - phase: credential_access
    techniques:
      - technique_id: T1003.001
        name: LSASS Memory Dump
        atomic_ids: ["T1003.001-1", "T1003.001-2"]
        platforms: ["windows"]
        detection_notes: "Monitor for lsass.exe handle access with PROCESS_VM_READ"
```

## How the autonomous daemon uses these

During an engagement, the daemon reads the active adversary profile from
`sessions/world_model.json` (`current_adversary` field). It filters techniques
by the target OS (`os_id` from `payload.json`) and selects the next executable
technique based on the current kill-chain phase.

To set the adversary simulation profile:

```
(LazyOwn) > assign current_adversary apt29
```

Or via MCP:

```
lazyown_set_config(key="current_adversary", value="apt29")
```

## Adding a profile

1. Create `lazyadversaries/apt_<name>.yaml` following the structure above.
2. Add `mitre_groups` IDs for attribution links.
3. Map each technique to at least one Atomic Red Team test ID where available.
4. Mark platform-specific techniques explicitly — the daemon skips Windows
   techniques against Linux targets.
5. Run `python scripts/update_apt_atomic_ids.py` to resolve and cache Atomic
   test metadata.
