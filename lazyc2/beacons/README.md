# lazyc2.beacons

Beacon domain contracts for the C2 server. This package owns the on-disk
state that the C2 routes, the CLI and the autonomous loop share, so every
surface reads and writes the same queue format.

## Files

| File | Purpose |
|------|---------|
| `store.py` | `BeaconStore` (queue, result history, malleable recon markers) and `BeaconPathError`. |
| `service.py` | `send_command` / `receive_result` pipelines (check-in side effects, CSV log, engagement + conditional hooks, bidirectional ingest) over an injected `BeaconRuntime`. |

## Contract

`BeaconStore(base_dir)` is the single implementation for:

- `queue_path` / `load_queue` / `save_queue` / `enqueue` / `pop_next`:
  FIFO command queue at `<base_dir>/cmd_<safe_id>.json` (JSON array of
  command strings).
- `append_record` / `read_records` / `history_path`: delegation to
  `modules.beacon_history`, the canonical result-history store.
- `recon_state_dir` / `recon_state_path` / `load_recon_state` /
  `save_recon_state`: per-beacon malleable recon markers at
  `<base_dir>/sessions/<safe_id>/c2/recon_state.json`.

Security invariants:

- Client ids pass `modules.security_sanitizers.sanitize_client_id`; only
  `[A-Za-z0-9_-]` survives.
- Every resolved path is confined under the configured base directory;
  symlink escapes raise `BeaconPathError`.
- Queue and marker writes are atomic (temp file plus `os.replace`), so a
  crashed writer never leaves a half-written JSON document.
- No module-level mutable state: the store is a frozen dataclass, so tests
  can bind an isolated base directory.

## Wiring

`lazyc2.py` keeps the public helper names (`_secure_command_queue_path`,
`_enqueue_malleable_command`, `_append_beacon_record`, ...) and delegates
them to a `BeaconStore` bound to `ALLOWED_DIRECTORY`. The `/command/`
route handlers stay in the monolith as thin adapters calling
`lazyc2.beacons.service.send_command` / `.receive_result` over a
`BeaconRuntime` built by `_beacon_runtime()`, so tests can keep
monkeypatching `lazyc2.send_command` / `lazyc2.receive_result`. The
service module never imports `lazyc2` (no cycles): every dependency is
injected through the runtime. The previously registered
`lazyc2/blueprints/beacon.py` was a shadowed duplicate and was removed.

## Tests

`tests/test_beacons_store.py`.
