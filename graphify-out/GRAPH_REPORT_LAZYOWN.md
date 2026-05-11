# Graph Report — LazyOwn (graphify)

## How to use this graph

The graph data in `graph_lazyown.json` is consumed by `cli/graph_advisor.py`
and surfaced through three integration points so both human operators and
MCP agents can query it without re-reading the JSON.

### CLI (cmd2 shell)

| Command | Purpose |
|---------|---------|
| `graph_search <query> [limit]` | Fuzzy-rank nodes by label/id/source file. |
| `neighbors <node> [depth] [limit]` | Walk the graph outward from a node. |
| `god_nodes [N]` | Show the top-N most connected nodes (core abstractions). |
| `suggest_next [seeds...] [N]` | Recommend the next commands by walking outward from recent activity (reads `sessions/LazyOwn_session_report.csv` when no seeds are given). |
| *did-you-mean recovery* | An unknown `do_*` command now prints up to three closest matches sourced from the graph + the fuzzy command index. |

### MCP (Claude Code, Claude web, any MCP-compatible agent)

| Tool | Purpose |
|------|---------|
| `lazyown_graph_summary` | Node/edge/community counts + the resolved graph path. Call once per session. |
| `lazyown_graph_search` | Fuzzy node search with a `budget_tokens` cap so the response never blows context. |
| `lazyown_graph_neighbors` | Layered adjacency walk with edge relation/confidence; agents use it to chain commands intelligently. |
| `lazyown_graph_suggest_next` | Next-step recommendation from recent activity, scored by inverse graph distance with exponential decay. |

All four tools degrade gracefully when the graph is missing: they return a
JSON object with `"available": false` and a `reason` instructing the
operator to run `/graphify .` to rebuild.

### Refresh the graph

```bash
/graphify .                   # full rebuild
/graphify . --update           # incremental, code-only changes go through AST
```

The advisor caches the loaded graph by `(path, mtime)` so a fresh
`/graphify` rebuild is picked up automatically on the next CLI command or
MCP tool call without restarting any process.

---

# Graph Report - /tmp/lazyown-graphify-input  (2026-05-06)

## Corpus Check
- 14 files · ~243,644 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1537 nodes · 2912 edges · 14 communities detected
- Extraction: 59% EXTRACTED · 41% INFERRED · 0% AMBIGUOUS · INFERRED: 1182 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `OllamaModel` - 497 edges
2. `LazyOwnShell` - 124 edges
3. `is_binary_present()` - 71 edges
4. `copy2clip()` - 62 edges
5. `get_credentials()` - 48 edges
6. `run()` - 47 edges
7. `get_users_dic()` - 39 edges
8. `decode()` - 37 edges
9. `decoy()` - 34 edges
10. `get_domain()` - 25 edges

## Surprising Connections (you probably didn't know these)
- `A custom interactive shell for the LazyOwn Framework.      This class extends th` --uses--> `OllamaModel`  [INFERRED]
  /tmp/lazyown-graphify-input/lazyown.py → /tmp/lazyown-graphify-input/ai_model.py
- `Initializer for the LazyOwnShell class.          This method sets up the initial` --uses--> `OllamaModel`  [INFERRED]
  /tmp/lazyown-graphify-input/lazyown.py → /tmp/lazyown-graphify-input/ai_model.py
- `Logs the command execution details to a CSV file.          :param cmd_name: The` --uses--> `OllamaModel`  [INFERRED]
  /tmp/lazyown-graphify-input/lazyown.py → /tmp/lazyown-graphify-input/ai_model.py
- `Handles undefined commands, including aliases.          This method checks if a` --uses--> `OllamaModel`  [INFERRED]
  /tmp/lazyown-graphify-input/lazyown.py → /tmp/lazyown-graphify-input/ai_model.py
- `Internal function to execute commands.          This method attempts to execute` --uses--> `OllamaModel`  [INFERRED]
  /tmp/lazyown-graphify-input/lazyown.py → /tmp/lazyown-graphify-input/ai_model.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.0
Nodes (431): OllamaModel, Attach strace to a running process and log output to a file.          This funct, Executes commands defined in a lazyscript file.          This function reads a s, Relanza la aplicación actual utilizando `proxychains` para enrutar el tráfico, Generates a Python one-liner to execute shellcode from a given URL.          Thi, This function executes the web security scanning tool Skipfish         using the, Create a Windows DLL file using MinGW-w64 or a Blazor DLL for Linux.          Th, Performs a web seo fingerprinting scan using `lazyseo.py`.          1. Executes (+423 more)

### Community 1 - "Community 1"
Cohesion: 0.01
Nodes (332): do_acknowledgearp(), do_acknowledgeicmp(), do_aclpwn_py(), do_ad_ldap_enum(), do_addspn_py(), do_addusers(), do_allin(), do_alterx() (+324 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (201): BaseHTTPRequestHandler, HTTPServer, search(), do_adsso_spray(), do_aes_pe(), do_ai_playbook(), do_arjun(), do_banners() (+193 more)

### Community 3 - "Community 3"
Cohesion: 0.02
Nodes (148): FileSystemEventHandler, aicmd_deepseek(), aicmd_view(), analyze_behavioral_data(), analyze_campaign_progress(), api_data(), aumentar_elo(), aumentar_elo_route() (+140 more)

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (104): add_dynamic_data(), authenticate(), check_auth(), create_route(), dynamic_route(), ensure_sessions_dir(), favicon(), get_client_ip() (+96 more)

### Community 5 - "Community 5"
Cohesion: 0.04
Nodes (38): BaseResolver, api_dashboard(), CustomDNSResolver, Aggregated JSON dashboard: beacons, campaign, events, facts summary., start_dns_server(), AESKeyManager, Security services for the LazyOwn C2 web layer.  Services encapsulate stateful s, Read a file as text after path validation.          Args:             relative_p (+30 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (40): decrypt_data(), get_data(), load_data(), Lectura continua del PTY y envío por WebSocket, Prevent CSV injection by prefixing formula-starting values., read_and_forward_pty_output(), read_and_forward_pty_output_c2(), receive_result() (+32 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (12): ABC, AIModel, GroqModel, for_command_analysis(), for_direct_query(), LazyOwnLLMChat, LazyOwnPromptRenderer, LazyOwnShellBridge (+4 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (9): do_ip2asn(), IP2ASN, Open and parse the IP-to-ASN file., Parse the reader stream, handling both regular and gzipped files., Parse the TSV data and load it into memory., Return the ASN associated with the given IP address., Check if the given index contains the IP., Get the AS name by ASN. (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (13): send_command(), do_process_scans(), do_transform(), Processes a single scan CSV file., Processes a single vulnerability CSV file., add(), detect_delimiter(), handle() (+5 more)

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (7): do_vulns(), Escáner de vulnerabilidades que busca y muestra información sobre CVEs.      Att, Inicializa el escáner con las cabeceras HTTP predefinidas., Busca CVEs basados en un servicio específico.          Args:             service, Añade detalles adicionales a la información del CVE.          Args:, Imprime una tabla bonita con detalles de CVEs.          Args:             cves_d, VulnerabilityScanner

### Community 11 - "Community 11"
Cohesion: 0.5
Nodes (2): Run the internal module located at `modules/lazyown_burpfuzzer.py` with the spec, Run a command and print output in real-time          This method executes a give

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Security constants and validation patterns for the LazyOwn C2 web layer.  All re

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): Generates an offensive playbook using:         1. Nmap scan results (CSV)

## Knowledge Gaps
- **558 isolated node(s):** `Security services for the LazyOwn C2 web layer.  Services encapsulate stateful s`, `Manages the Flask secret key lifecycle.      Generates a cryptographically secur`, `Return an existing secret key or generate and persist a new one.          Return`, `Provides safe file read/write operations with path traversal protection.      Al`, `Resolve a relative path safely within the base directory.          Args:` (+553 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (2 nodes): `Security constants and validation patterns for the LazyOwn C2 web layer.  All re`, `constants.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Generates an offensive playbook using:         1. Nmap scan results (CSV)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OllamaModel` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 6`, `Community 7`, `Community 9`, `Community 11`?**
  _High betweenness centrality (0.534) - this node is a cross-community bridge._
- **Why does `LazyOwnShell` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 5`, `Community 6`, `Community 9`, `Community 11`?**
  _High betweenness centrality (0.344) - this node is a cross-community bridge._
- **Why does `decode()` connect `Community 6` to `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 8`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 492 inferred relationships involving `OllamaModel` (e.g. with `LazyOwnShellBridge` and `SessionContextProvider`) actually correct?**
  _`OllamaModel` has 492 INFERRED edges - model-reasoned connections that need verification._
- **Are the 58 inferred relationships involving `LazyOwnShell` (e.g. with `Handler` and `CustomDNSResolver`) actually correct?**
  _`LazyOwnShell` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Are the 69 inferred relationships involving `is_binary_present()` (e.g. with `.run_lazymsfvenom()` and `do_nikto()`) actually correct?**
  _`is_binary_present()` has 69 INFERRED edges - model-reasoned connections that need verification._
- **Are the 59 inferred relationships involving `copy2clip()` (e.g. with `do_getcap()` and `do_smbclient()`) actually correct?**
  _`copy2clip()` has 59 INFERRED edges - model-reasoned connections that need verification._