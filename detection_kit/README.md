# LazyOwn Detection Kit

Defensive indicators for the LazyOwn C2 and beacon wire surface, packaged
the way the ARTEX continuation ships its rules: Sigma (log sources),
Suricata (network) and a MISP event import. The kit lets defenders and
researchers detect LazyOwn-style beacon traffic in their own networks,
and gives LazyOwn operators a hard guardrail: every rule must never fire
outside the declared lab segment.

## Contents

| Path | What it is |
|------|------------|
| `sigma/` | Six rules: beacon check-in (`POST /report/`), binary staging (`GET /stage/beacon`), log exfil (`/log/<data>`), dashboard polling (`/api/data`, `/api/beacon_results/`, `/gettasks`), HMAC `X-Signature` header. |
| `suricata/lazyown.rules` | The same six signals as Suricata rules, local sid range `9000001-9000006`. |
| `misp/lazyown_surface.json` | One MISP event with the URL/method/header attributes for a SIEM/TIP import. |
| `build_kit.py` | Packs everything into `dist/lazyown_detection_kit_<version>.tar.gz` with a SHA-256 sidecar for the GitHub release. |
| `../yara_rules/` | The existing YARA corpus (implant/rat families) already shipped with the framework. |
| SARIF | `readmenator . --sarif` emits code-security findings in SARIF for GitHub code scanning. |

## Verify the routes before you publish

The rules mirror the live Flask routes in `lazyc2.py`
(`/report/`, `/stage/beacon`, `/log/<data>`, `/api/data`,
`/api/beacon_results/<id>`, `/gettasks` plus the malleable
`<prefix>/report/` variants) and the beacon wire contract (HMAC-SHA256
body signature in `X-Signature`, default on). If you malleable-rewrite
the default paths in a campaign, regenerate the kit from your own
listener first.

## Build a release artefact

```bash
python detection_kit/build_kit.py 1.0.0
```

Output lands in `detection_kit/dist/` (gitignored). Attach the tarball
and its `.sha256` to the next GitHub release so defenders do not need to
clone the repository to consume the rules.

## Using the rules

- Sigma: drop into a Sigma-capable backend (Elastic, Splunk, LimaCharlie)
  and scope `webserver` logs from your edge or lab egress.
- Suricata: include as `detect-engine`/rule file; keep `$HOME_NET` as your
  lab segment and alert on any hit outside it.
- MISP: import `misp/lazyown_surface.json` as an event and publish to your
  TIP with the `lab-only` warning tag retained.

All six rules ship `falsepositives` guidance: the check-in and staging
endpoints can exist in legitimate apps, so scope first, alert second.
