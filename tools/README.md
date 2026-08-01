# tools — Pwntomate legacy `.tool` format

This directory holds 69 pwntomate service-triggered job files in the legacy
`.tool` JSON format. These are auto-dispatched when nmap discovers matching
ports or services on a target.

**This format is legacy / deprecated for new integrations.** All new tool
integrations should use the YAML format in `lazyaddons/` instead, which
provides richer metadata, parameter substitution, install/execute split,
OS/target declaration, and MCP auto-registration.

## How it works

1. `do_lazynmap` finishes and writes `sessions/scan_<rhost>.nmap.xml`.
2. The pwntomate engine reads the XML and walks each open port.
3. For each port, it looks up matching `.tool` files by service name and port
   number.
4. Matched jobs are queued and executed sequentially. Output lands in
   `sessions/<ip>/<port>/<tool>/*.txt`.

## JSON schema

Each `.tool` file is a JSON object with the following fields:

```json
{
  "toolname": "string (required) — display name of the tool",
  "command": "string (required) — shell command template with {token} placeholders",
  "trigger": ["string", "…"] (required) — list of nmap service names or port numbers that trigger this tool; use ["all"] for every service",
  "active": true | false (required) — whether pwntomate dispatches this tool",
  "category": "string (optional) — kill-chain category (e.g. \"02. Scanning & Enumeration\")",
  "description": "string (optional) — human-readable summary"
}
```

### Placeholder tokens

| Token | Value |
|-------|-------|
| `{ip}` / `{rhost}` | Target IP |
| `{port}` / `{rport}` | Target port |
| `{proto}` | Protocol (tcp/udp) |
| `{outputdir}` | Base output directory (`sessions/<ip>/<port>/`) |
| `{wordlist}` | Directory brute-force wordlist path |
| `{lhost}` | Attacker IP |
| `{lport}` | Reverse-shell listener port |
| `{domain}` | Target domain |
| `{toolname}` | The tool's display name |

### Example

```json
{
  "toolname": "Example Tool",
  "command": "echo \"proto{s}://{ip}:{port}\" > {outputdir}/{toolname}.txt",
  "trigger": ["all"],
  "active": false,
  "category": "02. Scanning & Enumeration",
  "description": "Pwntomate tool: Example Tool — triggers on ['all']"
}
```

## Output location

All pwntomate output lands under `sessions/<target_ip>/<port>/<tool>/`.
The `bridge_suggest` and `threat_model` MCP tools read from this tree.

## Migrating to lazyaddons

To convert a `.tool` file to the modern `lazyaddons/` YAML format:

1. Create `lazyaddons/<toolname>.yaml` following the schema in
   `lazyaddons/README.md`.
2. Map `command` to `tool.execute_command`, `trigger` to the top-level
   `trigger:` list, and fill in `author`, `version`, `params`, `os`, and
   `category` metadata.
3. Set `active: false` in the `.tool` file (rather than deleting it) so
   existing pwntomate scan histories remain readable.
4. Verify the new addon registers correctly with `reload_addons` and
   `search <toolname>` in the CLI.
