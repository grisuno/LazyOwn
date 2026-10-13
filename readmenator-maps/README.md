<!-- readmenator:folder-readme -->
# readmenator-maps

Interactive maps gallery: a self-contained static site with system maps, the 2D/3D force-graph explorer, the edge bundle explorer, flow diagrams, component diagrams, the overview video and the documentation set. It can be served as-is (for example as the GitHub Pages root).

Generated offline by ReadMenator (static analysis, zero LLM tokens). Files here are rewritten on every run, so do not edit them by hand. To keep a hand-written README in this folder instead, delete the first line of this file.

## Contents

| Path | What it is |
|---|---|
| `index.html` | Gallery home: start here |
| `architecture.html` | Architecture map (files by layer, resolved imports) |
| `workflow.html` | Workflow map (delivery path across layers) |
| `sequence.html` | Sequence map (participants and call messages) |
| `dataflow.html` | Dataflow map (sources, transforms, stores) |
| `lifecycle.html` | Lifecycle map (layer states and transitions) |
| `graph-force.html` | Force-graph explorer: 2D/3D, inspector, reach, paths, lenses, source viewer |
| `graph-bundle.html` | Edge bundle explorer: circle and sphere views of every import |
| `flows.html` | Interactive architecture tiers and execution flows |
| `components.html` | Component diagrams |
| `vendor/` | Vendored graph engine used offline by the explorer |
| `md/` | Markdown copies shown in the gallery document drawer |
| `llms.txt` | Agent entry point listing every document |
| `readmenator.mp4` | Overview video |
| `readmenator-poster.jpg` | Video poster frame |

## How to use

- Open `readmenator-maps/index.html` in a browser; maps load vis.js from a CDN, explorers work offline.
- Large pages embed their data gzip-compressed; any current Chrome, Edge, Firefox or Safari decodes it natively.

## Regenerate

    readmenator . diagrams --full
    readmenator . --rebuild
