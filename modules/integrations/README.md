# modules/integrations

Bridge modules that connect LazyOwn to external platforms and tools. Each
file implements a single integration and exposes a clean Python API that the
CLI and the MCP layer can call without knowing the external system's details.

## Files

| File | Integration | MCP tool |
|------|-------------|----------|
| `misp_export.py` | MISP threat intelligence platform. Formats engagement findings as MISP events and pushes them to a configured MISP instance via the REST API. | `lazyown_misp_export` |
| `nuclei_bridge.py` | Nuclei vulnerability scanner. Translates LazyOwn target context into Nuclei invocation arguments, parses the JSON output, and writes findings to `sessions/<ip>/nuclei/`. | — |
| `searchsploit.py` | ExploitDB / Searchsploit CLI wrapper. Queries for exploits matching a service name and version. Returns structured results consumed by `lazyown_searchsploit`. | `lazyown_searchsploit` |
| `__init__.py` | Package marker. Re-exports the three integration classes. |

## Adding an integration

1. Create `modules/integrations/<platform>.py`.
2. Expose one public class with at minimum a `run(target, config)` method.
3. Keep all external API calls inside the class — never in module-level code.
4. Add a corresponding MCP tool in `skills/lazyown_mcp.py` if the integration
   should be reachable from Claude.
5. Write at least 5 unit tests in `tests/test_integrations.py`.
