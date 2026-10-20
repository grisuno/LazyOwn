# LazyOwn Architecture and Execution Flows

[Back to index](index.md)

## Architecture Overview

37 components stacked in 9 dependency tiers (weighted Eades-Lin-Smyth ordering: arrows point from dependent to dependency, top to bottom). Labels are import counts, thick arrows the top quartile; 30 transitively implied edges are omitted. Dashed red arrows are upward dependencies: the smallest set of imports that closes every cycle and breaks the layering. Cyan components hold entry points. Interactive version: `readmenator-apidocs/index.html#/flows`.

Upward dependencies to fix first: `cli` -> `cli/commands` (40 imports); `modules: lazy_loop` -> `modules: autonomous_daemon` (36 imports); `cli/commands` -> `modules: autonomous_daemon` (32 imports); `cli` -> `modules: autonomous_daemon` (30 imports); `cli` -> `modules: lazy_loop` (22 imports); `modules: autonomous_daemon` -> `modules: lazyc2` (16 imports); `cli/commands` -> `modules: lazy_loop` (13 imports); `cli` -> `modules: lazyc2` (13 imports); `modules: lazyown_facts` -> `modules: lazy_loop` (13 imports); `static/js` -> `cli/commands` (11 imports); `static/js` -> `modules: autonomous_daemon` (10 imports); `modules: lazyown_facts` -> `cli/commands` (10 imports); `modules: lazyown_facts` -> `modules: autonomous_daemon` (9 imports); `modules: dashboard_engine` -> `modules: autonomous_daemon` (9 imports); `skills/hermes-lazyown` -> `cli/commands` (5 imports); `modules: dashboard_engine` -> `cli/commands` (5 imports); `modules: dashboard_engine` -> `modules: lazy_loop` (5 imports); `modules: surface_graph` -> `cli/commands` (4 imports); `cli/commands` -> `modules: lazyc2` (3 imports); `cli` -> `static/js` (3 imports); `modules: lazy_loop` -> `modules: lazyc2` (3 imports); `skills/claude_md_orchestrator` -> `modules: autonomous_daemon` (2 imports); `skills/hermes-lazyown` -> `modules: autonomous_daemon` (2 imports); `modules: opsec_scorer` -> `modules: autonomous_daemon` (2 imports); `modules: opsec_scorer` -> `cli/commands` (2 imports); `modules: lazyown_facts` -> `modules: lazyc2` (2 imports); `skills/claude_md_orchestrator` -> `cli/commands` (1 imports); `skills/hermes-lazyown` -> `modules: lazy_loop` (1 imports); `modules: opsec_scorer` -> `modules: lazy_loop` (1 imports); `modules: opsec_scorer` -> `modules: lazyc2` (1 imports); `cli` -> `modules: lazyown_facts` (1 imports); `static/js` -> `modules: lazy_loop` (1 imports); `static/js` -> `modules: lazyc2` (1 imports); `modules: lazyown_facts` -> `static/js` (1 imports); `modules: surface_graph` -> `modules: autonomous_daemon` (1 imports); `modules: surface_graph` -> `modules: lazy_loop` (1 imports); `modules: surface_graph` -> `modules: lazyc2` (1 imports)

```mermaid
flowchart TB
    classDef cycle fill:#1f1530,stroke:#f472b6,color:#fce7f3,stroke-width:2px;
    classDef default fill:#111827,stroke:#38bdf8,color:#e5e7eb;
    classDef entry fill:#0e7490,stroke:#22d3ee,color:#ecfeff,stroke-width:2px;
    subgraph lane_0["Tier 1 - entry / orchestration"]
        direction LR
        n_c13["modules: kerberos_core<br/>7 files, 138 symbols<br/>Core / utility"]:::default
        n_c14["modules: saas_attacks<br/>7 files, 77 symbols<br/>Core / utility"]:::default
        n_c15["modules: polymorphic_engine<br/>6 files, 89 symbols<br/>Core / utility"]:::default
        n_c6["lazygui/panels<br/>51 files, 405 symbols<br/>Core / utility"]:::entry
        n_d_tools["tools<br/>4 files, 15 symbols<br/>Core / utility"]:::default
        n_d_tests["tests<br/>3 files, 9 symbols<br/>Presentation / entry"]:::default
        n_d_static["static<br/>2 files, 4 symbols<br/>Core / utility"]:::default
        n_d_source["source<br/>1 files, 0 symbols<br/>Core / utility"]:::default
        n_d_skills["skills<br/>5 files, 659 symbols<br/>Core / utility"]:::default
        n_d_scripts["scripts<br/>22 files, 72 symbols<br/>Core / utility"]:::default
        n_d_plugins["plugins<br/>26 files, 45 symbols<br/>Infrastructure"]:::default
        n_d_modules["modules<br/>76 files, 612 symbols<br/>Core / utility"]:::default
        n_d_lazyown_docker["lazyown-docker<br/>3 files, 14 symbols<br/>Core / utility"]:::entry
        n_d_deploy["deploy<br/>1 files, 2 symbols<br/>Core / utility"]:::default
        n_d_contrib["contrib<br/>22 files, 133 symbols<br/>Core / utility"]:::default
        n_d__claude[".claude<br/>1 files, 0 symbols<br/>Infrastructure"]:::default
        n_d__root_["(root)<br/>13 files, 60 symbols<br/>Core / utility"]:::entry
        n_c23["tools<br/>2 files, 4 symbols<br/>Core / utility"]:::default
        n_c22["scripts: migrate_lazyown<br/>1 files, 6 symbols<br/>Core / utility"]:::default
        n_c21["scripts: check_contract_manifest<br/>1 files, 13 symbols<br/>Core / utility"]:::default
        n_c20["poc_tui<br/>2 files, 33 symbols<br/>Infrastructure"]:::default
        n_c19["modules/backdoor<br/>2 files, 6 symbols<br/>Core / utility"]:::default
        n_c18["scripts: journal<br/>2 files, 16 symbols<br/>Core / utility"]:::default
        n_c17["tests<br/>1 files, 1 symbols<br/>Business logic"]:::default
    end
    subgraph lane_1["Tier 2"]
        direction LR
        n_c4["modules: lazyc2<br/>55 files, 1088 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_2["Tier 3"]
        direction LR
        n_c0["modules: autonomous_daemon<br/>118 files, 2788 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_3["Tier 4"]
        direction LR
        n_c3["modules: lazy_loop<br/>63 files, 1545 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_4["Tier 5"]
        direction LR
        n_c1["cli/commands<br/>118 files, 2041 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_5["Tier 6"]
        direction LR
        n_c8["modules: surface_graph<br/>10 files, 159 symbols<br/>Core / utility"]:::cycle
        n_c5["static/js<br/>37 files, 644 symbols<br/>Core / utility"]:::cycle
        n_c12["modules: opsec_scorer<br/>7 files, 93 symbols<br/>Core / utility"]:::cycle
        n_c11["skills/hermes-lazyown<br/>12 files, 158 symbols<br/>Core / utility"]:::entry
        n_c16["contrib/legacy<br/>4 files, 15 symbols<br/>Core / utility"]:::default
    end
    subgraph lane_6["Tier 7"]
        direction LR
        n_c9["modules: dashboard_engine<br/>11 files, 97 symbols<br/>Core / utility"]:::cycle
        n_c10["skills/claude_md_orchestrator<br/>13 files, 152 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_7["Tier 8"]
        direction LR
        n_c7["modules: lazyown_facts<br/>15 files, 306 symbols<br/>Core / utility"]:::cycle
    end
    subgraph lane_8["Tier 9 - foundation"]
        direction LR
        n_c2["cli<br/>64 files, 1345 symbols<br/>Core / utility"]:::entry
    end
    n_c0 ==>|"57"| n_c3
    n_c1 -->|"2"| n_c11
    n_c1 -->|"3"| n_c12
    n_c1 -->|"1"| n_c16
    n_c1 ==>|"15"| n_c5
    n_c1 ==>|"4"| n_c8
    n_c13 -->|"1"| n_c1
    n_c14 -->|"1"| n_c1
    n_c15 -->|"1"| n_c1
    n_c3 ==>|"37"| n_c1
    n_c4 ==>|"34"| n_c0
    n_c5 -->|"1"| n_c10
    n_c5 -->|"1"| n_c9
    n_c6 -->|"1"| n_c4
    n_c7 -->|"3"| n_c2
    n_c8 -->|"1"| n_c2
    n_c9 -->|"1"| n_c7
    n_c4 <-.-|"16 upward"| n_c0
    n_c0 <-.-|"32 upward"| n_c1
    n_c3 <-.-|"13 upward"| n_c1
    n_c4 <-.-|"3 upward"| n_c1
    n_c0 <-.-|"2 upward"| n_c10
    n_c1 <-.-|"1 upward"| n_c10
    n_c0 <-.-|"2 upward"| n_c11
    n_c1 <-.-|"5 upward"| n_c11
    n_c3 <-.-|"1 upward"| n_c11
    n_c0 <-.-|"2 upward"| n_c12
    n_c1 <-.-|"2 upward"| n_c12
    n_c3 <-.-|"1 upward"| n_c12
    n_c4 <-.-|"1 upward"| n_c12
    n_c0 <-.-|"30 upward"| n_c2
    n_c1 <-.-|"40 upward"| n_c2
    n_c3 <-.-|"22 upward"| n_c2
    n_c4 <-.-|"13 upward"| n_c2
    n_c5 <-.-|"3 upward"| n_c2
    n_c7 <-.-|"1 upward"| n_c2
    n_c0 <-.-|"36 upward"| n_c3
    n_c4 <-.-|"3 upward"| n_c3
    n_c0 <-.-|"10 upward"| n_c5
    n_c1 <-.-|"11 upward"| n_c5
    n_c3 <-.-|"1 upward"| n_c5
    n_c4 <-.-|"1 upward"| n_c5
    n_c0 <-.-|"9 upward"| n_c7
    n_c1 <-.-|"10 upward"| n_c7
    n_c3 <-.-|"13 upward"| n_c7
    n_c4 <-.-|"2 upward"| n_c7
    n_c5 <-.-|"1 upward"| n_c7
    n_c0 <-.-|"1 upward"| n_c8
    n_c1 <-.-|"4 upward"| n_c8
    n_c3 <-.-|"1 upward"| n_c8
    n_c4 <-.-|"1 upward"| n_c8
    n_c0 <-.-|"9 upward"| n_c9
    n_c1 <-.-|"5 upward"| n_c9
    n_c3 <-.-|"5 upward"| n_c9
    linkStyle 17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53 stroke:#f87171,stroke-width:2px;
    n_c13 ~~~ n_c4
    n_c4 ~~~ n_c0
    n_c0 ~~~ n_c3
    n_c3 ~~~ n_c1
    n_c1 ~~~ n_c8
    n_c8 ~~~ n_c9
    n_c9 ~~~ n_c7
    n_c7 ~~~ n_c2
```

---

## Execution Flows

Entry points are scored from `__main__` guards, `main` functions, entry-style names and files, and call-graph sources. Each flow walks resolved calls in call-site order (depth <= 4, <= 40 steps); numbers give the call order, dashed arrows revisit an already expanded callee, red arrows are recursion. Interactive version with zoom and per-node docs: `readmenator-apidocs/index.html#/flows`.

### `server.main`

`modules/backdoor/server.c:10`, score 13: `main` in a compiled-language file; entry-style name `main`; defined in entry file `server.c`.

Call tree:

```mermaid
flowchart LR
    classDef entry fill:#0e7490,stroke:#22d3ee,color:#ecfeff,stroke-width:2px;
    classDef external fill:#1a1530,stroke:#a78bfa,color:#ede9fe;
    n_modules_backdoor_server_c__main["server.main<br/>server.c:10"]:::entry
    n_modules_lazy_loop_py__bind["lazy_loop.TrafficLog.bind<br/>Attach traffic digest to a finding like bind_...<br/>lazy_loop.py:1721"]:::external
    n_modules_lazy_loop_py___normalize_refs["lazy_loop.TrafficLog._normalize_refs<br/>Upgrade legacy string refs to role/note dicts...<br/>lazy_loop.py:1752"]:::external
    n_modules_lazy_loop_py___now["lazy_loop._now<br/>Return current epoch seconds.<br/>lazy_loop.py:738"]:::external
    n_cli_autosuggest_py__accept["autosuggest.AutoSuggestEngine.accept<br/>Return the active command string and clear th...<br/>autosuggest.py:309"]:::external
    n_modules_backdoor_backdoor_c__bzero["backdoor.bzero<br/>backdoor.c:14"]:::external
    n_modules_backdoor_server_c__main -.->|"recursion"| n_modules_backdoor_server_c__main
    n_modules_backdoor_server_c__main -->|"1"| n_modules_lazy_loop_py__bind
    n_modules_lazy_loop_py__bind -->|"1"| n_modules_lazy_loop_py___normalize_refs
    n_modules_lazy_loop_py__bind -->|"2"| n_modules_lazy_loop_py___now
    n_modules_backdoor_server_c__main -->|"2"| n_cli_autosuggest_py__accept
    n_modules_backdoor_server_c__main -->|"3"| n_modules_backdoor_backdoor_c__bzero
    linkStyle 0 stroke:#f87171,stroke-width:2px;
```

Cross-file sequence:

```mermaid
sequenceDiagram
    autonumber
    participant p_modules_backdoor_server_c as server.c
    participant p_modules_lazy_loop_py as lazy_loop.py
    participant p_cli_autosuggest_py as autosuggest.py
    participant p_modules_backdoor_backdoor_c as backdoor.c
    p_modules_backdoor_server_c->>p_modules_lazy_loop_py: TrafficLog.bind()
    p_modules_backdoor_server_c->>p_cli_autosuggest_py: AutoSuggestEngine.accept()
    p_modules_backdoor_server_c->>p_modules_backdoor_backdoor_c: bzero()
```

### `amsi.main`

`modules/amsi.c:428`, score 11: `main` in a compiled-language file; entry-style name `main`.

Call tree:

```mermaid
flowchart LR
    classDef default fill:#111827,stroke:#38bdf8,color:#e5e7eb;
    classDef entry fill:#0e7490,stroke:#22d3ee,color:#ecfeff,stroke-width:2px;
    n_modules_amsi_c__main["amsi.main<br/>amsi.c:428"]:::entry
    n_modules_amsi_c__LoadNtFunctions["amsi.LoadNtFunctions<br/>Función para cargar las funciones dinámicamente<br/>amsi.c:38"]:::default
    n_modules_amsi_c__AMS1patch_OpenSession_jne["amsi.AMS1patch_OpenSession_jne<br/>Técnica de Saad, también conocido como @D1rkM...<br/>amsi.c:66"]:::default
    n_modules_amsi_c__NT_SUCCESS["amsi.NT_SUCCESS<br/>amsi.c:11"]:::default
    n_modules_amsi_c__AMS1patch_OpenSession_ret["amsi.AMS1patch_OpenSession_ret<br/>2<br/>amsi.c:116"]:::default
    n_modules_amsi_c__AMS1patch_ScanBuffer_ret["amsi.AMS1patch_ScanBuffer_ret<br/>3<br/>amsi.c:166"]:::default
    n_modules_amsi_c__AMS1patch_RastaMouse["amsi.AMS1patch_RastaMouse<br/>4<br/>amsi.c:215"]:::default
    n_modules_amsi_c__AMS1patch_E_ACCESSDENIED["amsi.AMS1patch_E_ACCESSDENIED<br/>5<br/>amsi.c:274"]:::default
    n_modules_amsi_c__AMS1patch_E_HANDLE["amsi.AMS1patch_E_HANDLE<br/>6<br/>amsi.c:326"]:::default
    n_modules_amsi_c__AMS1patch_E_OUTOFMEMORY["amsi.AMS1patch_E_OUTOFMEMORY<br/>7<br/>amsi.c:378"]:::default
    n_modules_amsi_c__main -.->|"recursion"| n_modules_amsi_c__main
    n_modules_amsi_c__main -->|"1"| n_modules_amsi_c__LoadNtFunctions
    n_modules_amsi_c__LoadNtFunctions -.->|"recursion"| n_modules_amsi_c__LoadNtFunctions
    n_modules_amsi_c__main -->|"2"| n_modules_amsi_c__AMS1patch_OpenSession_jne
    n_modules_amsi_c__AMS1patch_OpenSession_jne -.->|"recursion"| n_modules_amsi_c__AMS1patch_OpenSession_jne
    n_modules_amsi_c__AMS1patch_OpenSession_jne -->|"1"| n_modules_amsi_c__NT_SUCCESS
    n_modules_amsi_c__main -->|"3"| n_modules_amsi_c__AMS1patch_OpenSession_ret
    n_modules_amsi_c__AMS1patch_OpenSession_ret -.->|"recursion"| n_modules_amsi_c__AMS1patch_OpenSession_ret
    n_modules_amsi_c__AMS1patch_OpenSession_ret -.-> n_modules_amsi_c__NT_SUCCESS
    n_modules_amsi_c__main -->|"4"| n_modules_amsi_c__AMS1patch_ScanBuffer_ret
    n_modules_amsi_c__AMS1patch_ScanBuffer_ret -.->|"recursion"| n_modules_amsi_c__AMS1patch_ScanBuffer_ret
    n_modules_amsi_c__AMS1patch_ScanBuffer_ret -.-> n_modules_amsi_c__NT_SUCCESS
    n_modules_amsi_c__main -->|"5"| n_modules_amsi_c__AMS1patch_RastaMouse
    n_modules_amsi_c__AMS1patch_RastaMouse -.->|"recursion"| n_modules_amsi_c__AMS1patch_RastaMouse
    n_modules_amsi_c__AMS1patch_RastaMouse -.-> n_modules_amsi_c__NT_SUCCESS
    n_modules_amsi_c__main -->|"6"| n_modules_amsi_c__AMS1patch_E_ACCESSDENIED
    n_modules_amsi_c__AMS1patch_E_ACCESSDENIED -.->|"recursion"| n_modules_amsi_c__AMS1patch_E_ACCESSDENIED
    n_modules_amsi_c__AMS1patch_E_ACCESSDENIED -.-> n_modules_amsi_c__NT_SUCCESS
    n_modules_amsi_c__main -->|"7"| n_modules_amsi_c__AMS1patch_E_HANDLE
    n_modules_amsi_c__AMS1patch_E_HANDLE -.->|"recursion"| n_modules_amsi_c__AMS1patch_E_HANDLE
    n_modules_amsi_c__AMS1patch_E_HANDLE -.-> n_modules_amsi_c__NT_SUCCESS
    n_modules_amsi_c__main -->|"8"| n_modules_amsi_c__AMS1patch_E_OUTOFMEMORY
    n_modules_amsi_c__AMS1patch_E_OUTOFMEMORY -.->|"recursion"| n_modules_amsi_c__AMS1patch_E_OUTOFMEMORY
    n_modules_amsi_c__AMS1patch_E_OUTOFMEMORY -.-> n_modules_amsi_c__NT_SUCCESS
    linkStyle 0,2,4,7,10,13,16,19,22 stroke:#f87171,stroke-width:2px;
```

### `exp.main`

`modules/exp.c:620`, score 11: `main` in a compiled-language file; entry-style name `main`.

Call tree:

```mermaid
flowchart LR
    classDef default fill:#111827,stroke:#38bdf8,color:#e5e7eb;
    classDef entry fill:#0e7490,stroke:#22d3ee,color:#ecfeff,stroke-width:2px;
    classDef external fill:#1a1530,stroke:#a78bfa,color:#ede9fe;
    n_modules_exp_c__main["exp.main<br/>exp.c:620"]:::entry
    n_modules_exp_c__prepare_root_shell["exp.prepare_root_shell<br/>exp.c:559"]:::default
    n_modules_exp_c__create_dummy_file["exp.create_dummy_file<br/>exp.c:564"]:::default
    n_modules_exp_c__create_priv_file["exp.create_priv_file<br/>exp.c:572"]:::default
    n_modules_exp_c__sema_up["exp.sema_up<br/>exp.c:610"]:::default
    n_skills_lazyown_session_py__fork["lazyown_session.SessionTranscript.fork<br/>Create a new transcript forked from this one.<br/>lazyown_session.py:227"]:::external
    n_skills_lazyown_session_py__SessionTranscript["lazyown_session.SessionTranscript<br/>Append-only JSONL session transcript.<br/>lazyown_session.py:71"]:::external
    n_skills_lazyown_session_py__get_recent["lazyown_session.SessionTranscript.get_recent<br/>Return the last n events.<br/>lazyown_session.py:143"]:::external
    n_skills_lazyown_session_py__append["lazyown_session.SessionTranscript.append<br/>Append a single event.<br/>lazyown_session.py:106"]:::external
    n_skills_lazyown_session_py___redact_sensitive["lazyown_session._redact_sensitive<br/>Return #96;#96;value#96;#96; with known-sensitive keys re...<br/>lazyown_session.py:47"]:::external
    n_modules_exp_c__set_cpu_affinity["exp.set_cpu_affinity<br/>exp.c:438"]:::default
    n_modules_exp_c__do_error_exit["exp.do_error_exit<br/>exp.c:161"]:::default
    n_modules_exp_c__userland_T["exp.userland_T<br/>exp.c:605"]:::default
    n_modules_exp_c__setup_modprobe_payload["exp.setup_modprobe_payload<br/>exp.c:601"]:::default
    n_modules_exp_c__write_new_modprobe["exp.write_new_modprobe<br/>exp.c:582"]:::default
    n_modules_exp_c__unshare_setup["exp.unshare_setup<br/>exp.c:297"]:::default
    n_modules_exp_c__bye["exp.bye<br/>exp.c:155"]:::default
    n_modules_exp_c__set_stable_table_and_set["exp.set_stable_table_and_set<br/>exp.c:322"]:::default
    n_modules_exp_c__set_trigger_set_and_overwrite["exp.set_trigger_set_and_overwrite<br/>exp.c:385"]:::default
    n_modules_exp_c__spray_keyring["exp.spray_keyring<br/>exp.c:172"]:::default
    n_modules_exp_c__add_key["exp.add_key<br/>exp.c:147"]:::default
    n_modules_exp_c__get_keyring_leak["exp.get_keyring_leak<br/>exp.c:248"]:::default
    n_modules_exp_c__main -.->|"recursion"| n_modules_exp_c__main
    n_modules_exp_c__main -->|"1"| n_modules_exp_c__prepare_root_shell
    n_modules_exp_c__prepare_root_shell -.->|"recursion"| n_modules_exp_c__prepare_root_shell
    n_modules_exp_c__prepare_root_shell -->|"1"| n_modules_exp_c__create_dummy_file
    n_modules_exp_c__create_dummy_file -.->|"recursion"| n_modules_exp_c__create_dummy_file
    n_modules_exp_c__prepare_root_shell -->|"2"| n_modules_exp_c__create_priv_file
    n_modules_exp_c__create_priv_file -.->|"recursion"| n_modules_exp_c__create_priv_file
    n_modules_exp_c__main -->|"2"| n_modules_exp_c__sema_up
    n_modules_exp_c__sema_up -.->|"recursion"| n_modules_exp_c__sema_up
    n_modules_exp_c__main -->|"3"| n_skills_lazyown_session_py__fork
    n_skills_lazyown_session_py__fork -->|"1"| n_skills_lazyown_session_py__SessionTranscript
    n_skills_lazyown_session_py__fork -->|"2"| n_skills_lazyown_session_py__get_recent
    n_skills_lazyown_session_py__fork -->|"3"| n_skills_lazyown_session_py__append
    n_skills_lazyown_session_py__append -->|"1"| n_skills_lazyown_session_py___redact_sensitive
    n_skills_lazyown_session_py___redact_sensitive -.->|"recursion"| n_skills_lazyown_session_py___redact_sensitive
    n_modules_exp_c__main -->|"4"| n_modules_exp_c__set_cpu_affinity
    n_modules_exp_c__set_cpu_affinity -.->|"recursion"| n_modules_exp_c__set_cpu_affinity
    n_modules_exp_c__set_cpu_affinity -->|"1"| n_modules_exp_c__do_error_exit
    n_modules_exp_c__do_error_exit -.->|"recursion"| n_modules_exp_c__do_error_exit
    n_modules_exp_c__main -->|"5"| n_modules_exp_c__userland_T
    n_modules_exp_c__userland_T -.->|"recursion"| n_modules_exp_c__userland_T
    n_modules_exp_c__main -->|"6"| n_modules_exp_c__setup_modprobe_payload
    n_modules_exp_c__setup_modprobe_payload -.->|"recursion"| n_modules_exp_c__setup_modprobe_payload
    n_modules_exp_c__setup_modprobe_payload -->|"1"| n_modules_exp_c__write_new_modprobe
    n_modules_exp_c__write_new_modprobe -.->|"recursion"| n_modules_exp_c__write_new_modprobe
    n_modules_exp_c__write_new_modprobe -.-> n_modules_exp_c__do_error_exit
    n_modules_exp_c__main -->|"7"| n_modules_exp_c__unshare_setup
    n_modules_exp_c__unshare_setup -.->|"recursion"| n_modules_exp_c__unshare_setup
    n_modules_exp_c__main -.-> n_modules_exp_c__do_error_exit
    n_modules_exp_c__main -->|"8"| n_modules_exp_c__bye
    n_modules_exp_c__bye -.->|"recursion"| n_modules_exp_c__bye
    n_modules_exp_c__main -->|"9"| n_modules_exp_c__set_stable_table_and_set
    n_modules_exp_c__set_stable_table_and_set -.->|"recursion"| n_modules_exp_c__set_stable_table_and_set
    n_modules_exp_c__main -->|"10"| n_modules_exp_c__set_trigger_set_and_overwrite
    n_modules_exp_c__set_trigger_set_and_overwrite -.->|"recursion"| n_modules_exp_c__set_trigger_set_and_overwrite
    n_modules_exp_c__main -->|"11"| n_modules_exp_c__spray_keyring
    n_modules_exp_c__spray_keyring -.->|"recursion"| n_modules_exp_c__spray_keyring
    n_modules_exp_c__spray_keyring -.-> n_modules_exp_c__bye
    n_modules_exp_c__spray_keyring -->|"1"| n_modules_exp_c__add_key
    n_modules_exp_c__main -->|"12"| n_modules_exp_c__get_keyring_leak
    linkStyle 0,2,4,6,8,14,16,18,20,22,24,27,30,32,34,36 stroke:#f87171,stroke-width:2px;
```

Cross-file sequence:

```mermaid
sequenceDiagram
    autonumber
    participant p_modules_exp_c as exp.c
    participant p_skills_lazyown_session_py as lazyown_session.py
    p_modules_exp_c->>p_skills_lazyown_session_py: SessionTranscript.fork()
```

---
