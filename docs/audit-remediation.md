# Audit Remediation Record

Scope: remediation of the externally reported code-audit critique (ZONE.CI,
release 0.2.160) against the current `dev` branch, in order P0 (crypto and
identity), P1 (noise), P2 (artifacts), P3 (TLS pinning and BOF provenance),
P4 (operability and hygiene).

## P0 — Crypto and identity

| Defect | Where it was | Fix |
|--------|---------------|-----|
| Beacon HMAC verification shipped disabled | `core/payload_schema.py` default `c2_require_beacon_hmac=False` | Default flipped to `True`; verification now guards both the beacon polling GET (`send_command`) and the result POST (`receive_result`) in `lazyc2.py` through `_beacon_signature_guard()` |
| Signing key was a published schema constant | `rat_key` default `82e672ae…` in `core/payload_schema.py` | Default is now empty; `core.config.ensure_rat_key()` generates a random 32-byte key with `secrets.token_hex`, persists it to `payload.json` on first use (C2 boot, signature guard, implant build) and rotates the published legacy key automatically |
| Implant never signed beacon traffic | `sessions/implant/implant_crypt.go` | `signWireBody()` computes HMAC-SHA256 over the exact wire body (raw multipart bytes, or base64-encoded packet bytes) and sets `X-Signature` on every beacon request |
| Implant depended on plaintext `/config.json` for required values | `loadBeaconConfig()` returned `FATAL` on failure | `seedConfigDefaults()` seeds reverse-shell port, rhost, debug flag and scan ports from baked-in template constants (`{reverse_shell_port}`, `{beacon_scan_ports}`, `{lhost}`); the config fetch is now advisory only |
| `rat_key` not wired into the builder context | `modules/c2_builder.py` | Context now carries `rat_key` (read from a fresh `payload.json`), `reverse_shell_port` and `beacon_scan_ports` |

## P1 — Noise and flag discipline

| Defect | Fix |
|--------|-----|
| linpeas/winpeas queued automatically on every check-in | New payload flags `auto_privesc_on_checkin` and `auto_discover_on_checkin` (default `False`); the auto-queues in `lazyc2.py` only run when the operator enables them |
| No operator surface for those knobs | `cli/orchestrator_assets_tabs.py` `CONFIG_FIELDS` exposes `c2_require_beacon_hmac`, `auto_privesc_on_checkin`, `auto_discover_on_checkin` in the `lazy_orchestrator` config tab |

## P2 — Artifact identity leaks

| Defect | Where it was | Fix |
|--------|---------------|-----|
| Kernel rootkit baked in the operator IP `10.10.14.10` | `modules/rootkit/rootkit.c` and `rootkit.c.bkp.c` | `LISTENER_IP`, `LISTENER_PORT`, `HIDDEN_PROCESS_NAME`, `HIDDEN_FILE_NAME` are now `#ifndef`-guarded with inert defaults; operable values come from `Makefile` `ccflags-y` defines |
| Operator username baked into user-mode loaders | `modules/rootkit/mrhyde*.c` | `HIDE_USER` / `HIDE_DIR` guarded with neutral defaults |
| Windows backdoor registry run key named `Hacked` | `modules/backdoor/backdoor.c` | Run key value is `RUNKEY_NAME`, `#ifndef`-guarded with the bland default `SystemMaintenance` |
| Backdoor popped a `MessageBox` claiming compromise on connect | same | Removed |

## P3 — TLS and provenance

| Item | Fix |
|------|-----|
| Beacon TLS accepted anything | `implant_crypt.go` transport now dials through `github.com/refraction-networking/utls` (`DialTLSContext`), so the ClientHello carries a real browser fingerprint (`HelloChrome_Auto`, `HelloFirefox_Auto`, `HelloIOS_Auto`, `HelloEdge_Auto` chosen at random per implant run) instead of Go's stock TLS stack — JA3 is no longer "simulating" |
| BOF capability provenance | The BOF runtime lives in the external `blacksandbeacon` repository and is lazily loaded through `lazyaddons/blacksandbeacon_bof.yaml`; this repo ships the loader metadata only. Documented here and in `README.md` |

## P4 — Operability

| Item | Where | Why |
|------|-------|-----|
| `hygiene_audit` command | `cli/commands/audit.py` | One command aggregates the P0-P2 posture into `sessions/hygiene_report.json` |
| `audit_hygiene` chain | `chains/audit_hygiene.yaml` | Runs the hygiene audit and the remediation `set` commands as one repeatable chain step |
| Sanctioned config writer | `utils.lazyown_set_config()` | Single audited path for programmatic payload writes outside `do_assign` / `do_set`; also fixes the latent import in `cli/commands/phishing_wizard.py` |

## Session-scoped secret rotation (follow-up wave)

| Fix | Where | Contract |
|-----|-------|----------|
| Rotative session keys | `core/session_secrets.py` | `rotate_session_secrets()` regenerates `aes_key` (32 bytes, `sessions/key.aes`, 0600), `rat_key` (64 hex) and `session_magic` (32 hex) with `secrets`/`os.urandom` and persists them; `ensure_session_secrets()` creates them when missing or placeholder-valued, and force-rotates when `rotate_keys_on_boot` is on |
| C2 rotates on boot | `lazyc2.py` module bootstrap | When `rotate_keys_on_boot=True` every C2 process start issues a fresh key set — old artifacts stop authenticating, matching the burned-implant assumption |
| Guard follows rotation live | `lazyc2.py` `_beacon_signature_guard()` | The expected `rat_key` is re-read from `payload.json` on every request, and `encrypt_data`/`decrypt_data` reload `sessions/key.aes` when its bytes change, so out-of-process rotation never strands a running C2 |
| `clean` rotates keys | `cli/commands/shellsys.py` `do_clean` | Artifact sweep now deletes `sessions/key.aes` and `sessions/c2_lab.json` (rendered artifacts, snapshots) and then rotates all three session secrets |
| Sleep obfuscation is real and configurable | `implant_crypt.go` | `obfuscatedSleep()` splits every sleep into 2-6 fragments with random extensions and scrubs an 8 KiB scratch buffer between fragments; jitter bounds come from `sleep_jit_enabled`, `sleep_jit_pct_min/max` (rendered as template constants); `randomActivationDelay()` waits a random Go-duration between `sleep_activation_delay_min/max` before the first poll |
| Persistence is configurable | `implant_crypt.go` | Cron schedule (`persistence_cron_schedule`), systemd unit/Windows task/macOS label (`persistence_service_name`) are template constants instead of the hardcoded `* * * * *` / `system-maintenance` |
| Rootkit listener is per-deployment | `modules/c2_builder.py` | The builder renders `sessions/rootkit_Makefile` (and `sessions/rootkit_lkm.c`) carrying the engagement `rhost`/`rport` as `LISTENER_IP`/`LISTENER_PORT` defines |
| Magic string per session | `sessions/implant/listener.go`, `monrevlin.go` | The hardcoded `grisiscomebacksayknokknok` trigger is now the `{session_magic}` template constant, rotated with the session |
| Config writes merge | `core/config.py` `save_payload()` | Concurrent writers (shell `assign` while the C2 rotates) merge over the on-disk payload instead of overwriting it with a stale dict — previously an `assign` could silently revert rotated keys |
| Operator knobs | `cli/orchestrator_assets_tabs.py` | Config tab exposes `rotate_keys_on_boot`, sleep-jitter and persistence fields |
| Placeholder coverage | `lazyc2/addon_creator.py`, `skills/lazyaddon-creator/SKILL.md` | Every new key is accepted by the addon-creator validator and documented in the skill known-keys block |

## E2E validation (gym + apt_chain)

Ran against a live Metasploitable 2 container (`172.17.0.2`) via
`python lazyown.py --headless --json-output --run-chain "apt_chain apt_chain <target> --to-step step_75ccc2b4"`:

- scan XML reused, exploit sweep adopted a live `ms2_ingreslock` shell;
- `c2_server start` booted the C2, which rotated all session secrets on boot;
- `c2_deploy` staged and launched the signed lab agent via `ms2_ingreslock`
  (`client=msf-172-17-0-2`), `running=True`;
- the agent's first beacon passed the HMAC guard (HTTP 200 on both the
  malleable GET and the result POST) and results stream into
  `sessions/msf-172-17-0-2.records.jsonl` with `user=root`;
- `c2_loot` exfiltrated `/etc/shadow` (1233 bytes) through the rotated AES key;
- the full chain finished 11/11 steps `ok`.

## Verification

- `core.session_secrets` rotate/ensure/mirror: `tests/test_session_secrets.py` (6 tests), `tests/test_implant_session_secrets.py` (7 tests).
- `python -m py_compile lazyc2.py`, `pytest tests/test_audit_remediation.py`, targeted auth/hardening suites.
- Rendered implant builds for linux (`go build main.go loader_linux.go`) and windows (MinGW cross-build); backdoor renders and passes `x86_64-w64-mingw32-gcc -fsyntax-only`.
- `chains/audit_hygiene.yaml` loads and resolves through `modules.chain_registry`.
