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
/graphify . --update          # incremental, code-only changes go through AST
```

The advisor caches the loaded graph by `(path, mtime)` so a fresh
`/graphify` rebuild is picked up automatically on the next CLI command or
MCP tool call without restarting any process.

---

# Graph Report - .  (2026-05-19, post-refactor)

## Recent refactor (2026-05-19)

The graph reflects four targeted code changes designed to reduce coupling
and eliminate dead security helpers. Cross-reference each finding with
the god-node and community sections below.

| Change | Code seam | Graph signal |
|--------|-----------|--------------|
| LLM factory consolidation | `modules/llm_factory.py` + `core.protocols.LLMBackend` import | `AIModel` is now a god node (#5, 60 edges) — the abstraction is wired into production, not just tests |
| Security validator deduplication | `lazyc2.py` imports from `lazyc2/security/validators` | The previously isolated `lazyc2/security/validators.py` joins the main component instead of standing alone |
| Vulnerability pipeline closure | `utils.VulnerabilityScanner.persist()` + `do_vulns` writes `sessions/vulns_<rhost>.json` | New edges from `do_vulns` → `VulnerabilityScanner.persist` → `skills/lazyown_mcp_helpers.get_target_context` |
| Security service wiring | `lazyc2.py` consumes `SecretKeyManager` and `AESKeyManager` from `lazyc2/security/services` | `SecretKeyManager` and `AESKeyManager` are no longer orphan nodes — they have inbound edges from `lazyc2.py` |

## Corpus Check
- 11 files · ~1,000 words (incremental refactor delta only)
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2498 nodes · 4529 edges · 482 communities detected
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 1453 edges (avg confidence: 0.65)
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
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]
- [[_COMMUNITY_Community 99|Community 99]]
- [[_COMMUNITY_Community 100|Community 100]]
- [[_COMMUNITY_Community 101|Community 101]]
- [[_COMMUNITY_Community 102|Community 102]]
- [[_COMMUNITY_Community 103|Community 103]]
- [[_COMMUNITY_Community 104|Community 104]]
- [[_COMMUNITY_Community 105|Community 105]]
- [[_COMMUNITY_Community 106|Community 106]]
- [[_COMMUNITY_Community 107|Community 107]]
- [[_COMMUNITY_Community 108|Community 108]]
- [[_COMMUNITY_Community 109|Community 109]]
- [[_COMMUNITY_Community 110|Community 110]]
- [[_COMMUNITY_Community 111|Community 111]]
- [[_COMMUNITY_Community 112|Community 112]]
- [[_COMMUNITY_Community 113|Community 113]]
- [[_COMMUNITY_Community 114|Community 114]]
- [[_COMMUNITY_Community 115|Community 115]]
- [[_COMMUNITY_Community 116|Community 116]]
- [[_COMMUNITY_Community 117|Community 117]]
- [[_COMMUNITY_Community 118|Community 118]]
- [[_COMMUNITY_Community 119|Community 119]]
- [[_COMMUNITY_Community 120|Community 120]]
- [[_COMMUNITY_Community 121|Community 121]]
- [[_COMMUNITY_Community 122|Community 122]]
- [[_COMMUNITY_Community 123|Community 123]]
- [[_COMMUNITY_Community 124|Community 124]]
- [[_COMMUNITY_Community 125|Community 125]]
- [[_COMMUNITY_Community 126|Community 126]]
- [[_COMMUNITY_Community 127|Community 127]]
- [[_COMMUNITY_Community 128|Community 128]]
- [[_COMMUNITY_Community 129|Community 129]]
- [[_COMMUNITY_Community 130|Community 130]]
- [[_COMMUNITY_Community 131|Community 131]]
- [[_COMMUNITY_Community 132|Community 132]]
- [[_COMMUNITY_Community 133|Community 133]]
- [[_COMMUNITY_Community 134|Community 134]]
- [[_COMMUNITY_Community 135|Community 135]]
- [[_COMMUNITY_Community 136|Community 136]]
- [[_COMMUNITY_Community 137|Community 137]]
- [[_COMMUNITY_Community 138|Community 138]]
- [[_COMMUNITY_Community 139|Community 139]]
- [[_COMMUNITY_Community 140|Community 140]]
- [[_COMMUNITY_Community 141|Community 141]]
- [[_COMMUNITY_Community 142|Community 142]]
- [[_COMMUNITY_Community 143|Community 143]]
- [[_COMMUNITY_Community 144|Community 144]]
- [[_COMMUNITY_Community 145|Community 145]]
- [[_COMMUNITY_Community 146|Community 146]]
- [[_COMMUNITY_Community 147|Community 147]]
- [[_COMMUNITY_Community 148|Community 148]]
- [[_COMMUNITY_Community 149|Community 149]]
- [[_COMMUNITY_Community 150|Community 150]]
- [[_COMMUNITY_Community 151|Community 151]]
- [[_COMMUNITY_Community 152|Community 152]]
- [[_COMMUNITY_Community 153|Community 153]]
- [[_COMMUNITY_Community 154|Community 154]]
- [[_COMMUNITY_Community 155|Community 155]]
- [[_COMMUNITY_Community 156|Community 156]]
- [[_COMMUNITY_Community 157|Community 157]]
- [[_COMMUNITY_Community 158|Community 158]]
- [[_COMMUNITY_Community 159|Community 159]]
- [[_COMMUNITY_Community 160|Community 160]]
- [[_COMMUNITY_Community 161|Community 161]]
- [[_COMMUNITY_Community 162|Community 162]]
- [[_COMMUNITY_Community 163|Community 163]]
- [[_COMMUNITY_Community 164|Community 164]]
- [[_COMMUNITY_Community 165|Community 165]]
- [[_COMMUNITY_Community 166|Community 166]]
- [[_COMMUNITY_Community 167|Community 167]]
- [[_COMMUNITY_Community 168|Community 168]]
- [[_COMMUNITY_Community 169|Community 169]]
- [[_COMMUNITY_Community 170|Community 170]]
- [[_COMMUNITY_Community 171|Community 171]]
- [[_COMMUNITY_Community 172|Community 172]]
- [[_COMMUNITY_Community 173|Community 173]]
- [[_COMMUNITY_Community 174|Community 174]]
- [[_COMMUNITY_Community 175|Community 175]]
- [[_COMMUNITY_Community 176|Community 176]]
- [[_COMMUNITY_Community 177|Community 177]]
- [[_COMMUNITY_Community 178|Community 178]]
- [[_COMMUNITY_Community 179|Community 179]]
- [[_COMMUNITY_Community 180|Community 180]]
- [[_COMMUNITY_Community 181|Community 181]]
- [[_COMMUNITY_Community 182|Community 182]]
- [[_COMMUNITY_Community 183|Community 183]]
- [[_COMMUNITY_Community 184|Community 184]]
- [[_COMMUNITY_Community 185|Community 185]]
- [[_COMMUNITY_Community 186|Community 186]]
- [[_COMMUNITY_Community 187|Community 187]]
- [[_COMMUNITY_Community 188|Community 188]]
- [[_COMMUNITY_Community 189|Community 189]]
- [[_COMMUNITY_Community 190|Community 190]]
- [[_COMMUNITY_Community 191|Community 191]]
- [[_COMMUNITY_Community 192|Community 192]]
- [[_COMMUNITY_Community 193|Community 193]]
- [[_COMMUNITY_Community 194|Community 194]]
- [[_COMMUNITY_Community 195|Community 195]]
- [[_COMMUNITY_Community 196|Community 196]]
- [[_COMMUNITY_Community 197|Community 197]]
- [[_COMMUNITY_Community 198|Community 198]]
- [[_COMMUNITY_Community 199|Community 199]]
- [[_COMMUNITY_Community 200|Community 200]]
- [[_COMMUNITY_Community 201|Community 201]]
- [[_COMMUNITY_Community 202|Community 202]]
- [[_COMMUNITY_Community 203|Community 203]]
- [[_COMMUNITY_Community 204|Community 204]]
- [[_COMMUNITY_Community 205|Community 205]]
- [[_COMMUNITY_Community 206|Community 206]]
- [[_COMMUNITY_Community 207|Community 207]]
- [[_COMMUNITY_Community 208|Community 208]]
- [[_COMMUNITY_Community 209|Community 209]]
- [[_COMMUNITY_Community 210|Community 210]]
- [[_COMMUNITY_Community 211|Community 211]]
- [[_COMMUNITY_Community 212|Community 212]]
- [[_COMMUNITY_Community 213|Community 213]]
- [[_COMMUNITY_Community 214|Community 214]]
- [[_COMMUNITY_Community 215|Community 215]]
- [[_COMMUNITY_Community 216|Community 216]]
- [[_COMMUNITY_Community 217|Community 217]]
- [[_COMMUNITY_Community 218|Community 218]]
- [[_COMMUNITY_Community 219|Community 219]]
- [[_COMMUNITY_Community 220|Community 220]]
- [[_COMMUNITY_Community 221|Community 221]]
- [[_COMMUNITY_Community 222|Community 222]]
- [[_COMMUNITY_Community 223|Community 223]]
- [[_COMMUNITY_Community 224|Community 224]]
- [[_COMMUNITY_Community 225|Community 225]]
- [[_COMMUNITY_Community 226|Community 226]]
- [[_COMMUNITY_Community 227|Community 227]]
- [[_COMMUNITY_Community 228|Community 228]]
- [[_COMMUNITY_Community 229|Community 229]]
- [[_COMMUNITY_Community 230|Community 230]]
- [[_COMMUNITY_Community 231|Community 231]]
- [[_COMMUNITY_Community 232|Community 232]]
- [[_COMMUNITY_Community 233|Community 233]]
- [[_COMMUNITY_Community 234|Community 234]]
- [[_COMMUNITY_Community 235|Community 235]]
- [[_COMMUNITY_Community 236|Community 236]]
- [[_COMMUNITY_Community 237|Community 237]]
- [[_COMMUNITY_Community 238|Community 238]]
- [[_COMMUNITY_Community 239|Community 239]]
- [[_COMMUNITY_Community 240|Community 240]]
- [[_COMMUNITY_Community 241|Community 241]]
- [[_COMMUNITY_Community 242|Community 242]]
- [[_COMMUNITY_Community 243|Community 243]]
- [[_COMMUNITY_Community 244|Community 244]]
- [[_COMMUNITY_Community 245|Community 245]]
- [[_COMMUNITY_Community 246|Community 246]]
- [[_COMMUNITY_Community 247|Community 247]]
- [[_COMMUNITY_Community 248|Community 248]]
- [[_COMMUNITY_Community 249|Community 249]]
- [[_COMMUNITY_Community 250|Community 250]]
- [[_COMMUNITY_Community 251|Community 251]]
- [[_COMMUNITY_Community 252|Community 252]]
- [[_COMMUNITY_Community 253|Community 253]]
- [[_COMMUNITY_Community 254|Community 254]]
- [[_COMMUNITY_Community 255|Community 255]]
- [[_COMMUNITY_Community 256|Community 256]]
- [[_COMMUNITY_Community 257|Community 257]]
- [[_COMMUNITY_Community 258|Community 258]]
- [[_COMMUNITY_Community 259|Community 259]]
- [[_COMMUNITY_Community 260|Community 260]]
- [[_COMMUNITY_Community 261|Community 261]]
- [[_COMMUNITY_Community 262|Community 262]]
- [[_COMMUNITY_Community 263|Community 263]]
- [[_COMMUNITY_Community 264|Community 264]]
- [[_COMMUNITY_Community 265|Community 265]]
- [[_COMMUNITY_Community 266|Community 266]]
- [[_COMMUNITY_Community 267|Community 267]]
- [[_COMMUNITY_Community 268|Community 268]]
- [[_COMMUNITY_Community 269|Community 269]]
- [[_COMMUNITY_Community 270|Community 270]]
- [[_COMMUNITY_Community 271|Community 271]]
- [[_COMMUNITY_Community 272|Community 272]]
- [[_COMMUNITY_Community 273|Community 273]]
- [[_COMMUNITY_Community 274|Community 274]]
- [[_COMMUNITY_Community 275|Community 275]]
- [[_COMMUNITY_Community 276|Community 276]]
- [[_COMMUNITY_Community 277|Community 277]]
- [[_COMMUNITY_Community 278|Community 278]]
- [[_COMMUNITY_Community 279|Community 279]]
- [[_COMMUNITY_Community 280|Community 280]]
- [[_COMMUNITY_Community 281|Community 281]]
- [[_COMMUNITY_Community 282|Community 282]]
- [[_COMMUNITY_Community 283|Community 283]]
- [[_COMMUNITY_Community 284|Community 284]]
- [[_COMMUNITY_Community 285|Community 285]]
- [[_COMMUNITY_Community 286|Community 286]]
- [[_COMMUNITY_Community 287|Community 287]]
- [[_COMMUNITY_Community 288|Community 288]]
- [[_COMMUNITY_Community 289|Community 289]]
- [[_COMMUNITY_Community 290|Community 290]]
- [[_COMMUNITY_Community 291|Community 291]]
- [[_COMMUNITY_Community 292|Community 292]]
- [[_COMMUNITY_Community 293|Community 293]]
- [[_COMMUNITY_Community 294|Community 294]]
- [[_COMMUNITY_Community 295|Community 295]]
- [[_COMMUNITY_Community 296|Community 296]]
- [[_COMMUNITY_Community 297|Community 297]]
- [[_COMMUNITY_Community 298|Community 298]]
- [[_COMMUNITY_Community 299|Community 299]]
- [[_COMMUNITY_Community 300|Community 300]]
- [[_COMMUNITY_Community 301|Community 301]]
- [[_COMMUNITY_Community 302|Community 302]]
- [[_COMMUNITY_Community 303|Community 303]]
- [[_COMMUNITY_Community 304|Community 304]]
- [[_COMMUNITY_Community 305|Community 305]]
- [[_COMMUNITY_Community 306|Community 306]]
- [[_COMMUNITY_Community 307|Community 307]]
- [[_COMMUNITY_Community 308|Community 308]]
- [[_COMMUNITY_Community 309|Community 309]]
- [[_COMMUNITY_Community 310|Community 310]]
- [[_COMMUNITY_Community 311|Community 311]]
- [[_COMMUNITY_Community 312|Community 312]]
- [[_COMMUNITY_Community 313|Community 313]]
- [[_COMMUNITY_Community 314|Community 314]]
- [[_COMMUNITY_Community 315|Community 315]]
- [[_COMMUNITY_Community 316|Community 316]]
- [[_COMMUNITY_Community 317|Community 317]]
- [[_COMMUNITY_Community 318|Community 318]]
- [[_COMMUNITY_Community 319|Community 319]]
- [[_COMMUNITY_Community 320|Community 320]]
- [[_COMMUNITY_Community 321|Community 321]]
- [[_COMMUNITY_Community 322|Community 322]]
- [[_COMMUNITY_Community 323|Community 323]]
- [[_COMMUNITY_Community 324|Community 324]]
- [[_COMMUNITY_Community 325|Community 325]]
- [[_COMMUNITY_Community 326|Community 326]]
- [[_COMMUNITY_Community 327|Community 327]]
- [[_COMMUNITY_Community 328|Community 328]]
- [[_COMMUNITY_Community 329|Community 329]]
- [[_COMMUNITY_Community 330|Community 330]]
- [[_COMMUNITY_Community 331|Community 331]]
- [[_COMMUNITY_Community 332|Community 332]]
- [[_COMMUNITY_Community 333|Community 333]]
- [[_COMMUNITY_Community 334|Community 334]]
- [[_COMMUNITY_Community 335|Community 335]]
- [[_COMMUNITY_Community 336|Community 336]]
- [[_COMMUNITY_Community 337|Community 337]]
- [[_COMMUNITY_Community 338|Community 338]]
- [[_COMMUNITY_Community 339|Community 339]]
- [[_COMMUNITY_Community 340|Community 340]]
- [[_COMMUNITY_Community 341|Community 341]]
- [[_COMMUNITY_Community 342|Community 342]]
- [[_COMMUNITY_Community 343|Community 343]]
- [[_COMMUNITY_Community 344|Community 344]]
- [[_COMMUNITY_Community 345|Community 345]]
- [[_COMMUNITY_Community 346|Community 346]]
- [[_COMMUNITY_Community 347|Community 347]]
- [[_COMMUNITY_Community 348|Community 348]]
- [[_COMMUNITY_Community 349|Community 349]]
- [[_COMMUNITY_Community 350|Community 350]]
- [[_COMMUNITY_Community 351|Community 351]]
- [[_COMMUNITY_Community 352|Community 352]]
- [[_COMMUNITY_Community 353|Community 353]]
- [[_COMMUNITY_Community 354|Community 354]]
- [[_COMMUNITY_Community 355|Community 355]]
- [[_COMMUNITY_Community 356|Community 356]]
- [[_COMMUNITY_Community 357|Community 357]]
- [[_COMMUNITY_Community 358|Community 358]]
- [[_COMMUNITY_Community 359|Community 359]]
- [[_COMMUNITY_Community 360|Community 360]]
- [[_COMMUNITY_Community 361|Community 361]]
- [[_COMMUNITY_Community 362|Community 362]]
- [[_COMMUNITY_Community 363|Community 363]]
- [[_COMMUNITY_Community 364|Community 364]]
- [[_COMMUNITY_Community 365|Community 365]]
- [[_COMMUNITY_Community 366|Community 366]]
- [[_COMMUNITY_Community 367|Community 367]]
- [[_COMMUNITY_Community 368|Community 368]]
- [[_COMMUNITY_Community 369|Community 369]]
- [[_COMMUNITY_Community 370|Community 370]]
- [[_COMMUNITY_Community 371|Community 371]]
- [[_COMMUNITY_Community 372|Community 372]]
- [[_COMMUNITY_Community 373|Community 373]]
- [[_COMMUNITY_Community 374|Community 374]]
- [[_COMMUNITY_Community 375|Community 375]]
- [[_COMMUNITY_Community 376|Community 376]]
- [[_COMMUNITY_Community 377|Community 377]]
- [[_COMMUNITY_Community 378|Community 378]]
- [[_COMMUNITY_Community 379|Community 379]]
- [[_COMMUNITY_Community 380|Community 380]]
- [[_COMMUNITY_Community 381|Community 381]]
- [[_COMMUNITY_Community 382|Community 382]]
- [[_COMMUNITY_Community 383|Community 383]]
- [[_COMMUNITY_Community 384|Community 384]]
- [[_COMMUNITY_Community 385|Community 385]]
- [[_COMMUNITY_Community 386|Community 386]]
- [[_COMMUNITY_Community 387|Community 387]]
- [[_COMMUNITY_Community 388|Community 388]]
- [[_COMMUNITY_Community 389|Community 389]]
- [[_COMMUNITY_Community 390|Community 390]]
- [[_COMMUNITY_Community 391|Community 391]]
- [[_COMMUNITY_Community 392|Community 392]]
- [[_COMMUNITY_Community 393|Community 393]]
- [[_COMMUNITY_Community 394|Community 394]]
- [[_COMMUNITY_Community 395|Community 395]]
- [[_COMMUNITY_Community 396|Community 396]]
- [[_COMMUNITY_Community 397|Community 397]]
- [[_COMMUNITY_Community 398|Community 398]]
- [[_COMMUNITY_Community 399|Community 399]]
- [[_COMMUNITY_Community 400|Community 400]]
- [[_COMMUNITY_Community 401|Community 401]]
- [[_COMMUNITY_Community 402|Community 402]]
- [[_COMMUNITY_Community 403|Community 403]]
- [[_COMMUNITY_Community 404|Community 404]]
- [[_COMMUNITY_Community 405|Community 405]]
- [[_COMMUNITY_Community 406|Community 406]]
- [[_COMMUNITY_Community 407|Community 407]]
- [[_COMMUNITY_Community 408|Community 408]]
- [[_COMMUNITY_Community 409|Community 409]]
- [[_COMMUNITY_Community 410|Community 410]]
- [[_COMMUNITY_Community 411|Community 411]]
- [[_COMMUNITY_Community 412|Community 412]]
- [[_COMMUNITY_Community 413|Community 413]]
- [[_COMMUNITY_Community 414|Community 414]]
- [[_COMMUNITY_Community 415|Community 415]]
- [[_COMMUNITY_Community 416|Community 416]]
- [[_COMMUNITY_Community 417|Community 417]]
- [[_COMMUNITY_Community 418|Community 418]]
- [[_COMMUNITY_Community 419|Community 419]]
- [[_COMMUNITY_Community 420|Community 420]]
- [[_COMMUNITY_Community 421|Community 421]]
- [[_COMMUNITY_Community 422|Community 422]]
- [[_COMMUNITY_Community 423|Community 423]]
- [[_COMMUNITY_Community 424|Community 424]]
- [[_COMMUNITY_Community 425|Community 425]]
- [[_COMMUNITY_Community 426|Community 426]]
- [[_COMMUNITY_Community 427|Community 427]]
- [[_COMMUNITY_Community 428|Community 428]]
- [[_COMMUNITY_Community 429|Community 429]]
- [[_COMMUNITY_Community 430|Community 430]]
- [[_COMMUNITY_Community 431|Community 431]]
- [[_COMMUNITY_Community 432|Community 432]]
- [[_COMMUNITY_Community 433|Community 433]]
- [[_COMMUNITY_Community 434|Community 434]]
- [[_COMMUNITY_Community 435|Community 435]]
- [[_COMMUNITY_Community 436|Community 436]]
- [[_COMMUNITY_Community 437|Community 437]]
- [[_COMMUNITY_Community 438|Community 438]]
- [[_COMMUNITY_Community 439|Community 439]]
- [[_COMMUNITY_Community 440|Community 440]]
- [[_COMMUNITY_Community 441|Community 441]]
- [[_COMMUNITY_Community 442|Community 442]]
- [[_COMMUNITY_Community 443|Community 443]]
- [[_COMMUNITY_Community 444|Community 444]]
- [[_COMMUNITY_Community 445|Community 445]]
- [[_COMMUNITY_Community 446|Community 446]]
- [[_COMMUNITY_Community 447|Community 447]]
- [[_COMMUNITY_Community 448|Community 448]]
- [[_COMMUNITY_Community 449|Community 449]]
- [[_COMMUNITY_Community 450|Community 450]]
- [[_COMMUNITY_Community 451|Community 451]]
- [[_COMMUNITY_Community 452|Community 452]]
- [[_COMMUNITY_Community 453|Community 453]]
- [[_COMMUNITY_Community 454|Community 454]]
- [[_COMMUNITY_Community 455|Community 455]]
- [[_COMMUNITY_Community 456|Community 456]]
- [[_COMMUNITY_Community 457|Community 457]]
- [[_COMMUNITY_Community 458|Community 458]]
- [[_COMMUNITY_Community 459|Community 459]]
- [[_COMMUNITY_Community 460|Community 460]]
- [[_COMMUNITY_Community 461|Community 461]]
- [[_COMMUNITY_Community 462|Community 462]]
- [[_COMMUNITY_Community 463|Community 463]]
- [[_COMMUNITY_Community 464|Community 464]]
- [[_COMMUNITY_Community 465|Community 465]]
- [[_COMMUNITY_Community 466|Community 466]]
- [[_COMMUNITY_Community 467|Community 467]]
- [[_COMMUNITY_Community 468|Community 468]]
- [[_COMMUNITY_Community 469|Community 469]]
- [[_COMMUNITY_Community 470|Community 470]]
- [[_COMMUNITY_Community 471|Community 471]]
- [[_COMMUNITY_Community 472|Community 472]]
- [[_COMMUNITY_Community 473|Community 473]]
- [[_COMMUNITY_Community 474|Community 474]]
- [[_COMMUNITY_Community 475|Community 475]]
- [[_COMMUNITY_Community 476|Community 476]]
- [[_COMMUNITY_Community 477|Community 477]]
- [[_COMMUNITY_Community 478|Community 478]]
- [[_COMMUNITY_Community 479|Community 479]]
- [[_COMMUNITY_Community 480|Community 480]]
- [[_COMMUNITY_Community 481|Community 481]]

## God Nodes (most connected - your core abstractions)
1. `OllamaModel` - 512 edges
2. `LazyOwnShell` - 211 edges
3. `is_binary_present()` - 73 edges
4. `copy2clip()` - 64 edges
5. `AIModel` - 60 edges
6. `run()` - 54 edges
7. `get_credentials()` - 50 edges
8. `get_users_dic()` - 41 edges
9. `decode()` - 40 edges
10. `decoy()` - 35 edges

## Surprising Connections (you probably didn't know these)
- `AIModel` --uses--> `Carga las variables desde payload.json`  [INFERRED]
  /home/grisun0/LazyOwn/modules/ai_model.py → /home/grisun0/LazyOwn/modules/yaml_generator.py
- `OllamaModel` --uses--> `A custom interactive shell for the LazyOwn Framework.      This class extends th`  [INFERRED]
  /home/grisun0/LazyOwn/modules/ai_model.py → /tmp/lazyown-graphify-input/lazyown.py
- `OllamaModel` --uses--> `Initializer for the LazyOwnShell class.          This method sets up the initial`  [INFERRED]
  /home/grisun0/LazyOwn/modules/ai_model.py → /tmp/lazyown-graphify-input/lazyown.py
- `OllamaModel` --uses--> `Handles undefined commands, including aliases.          This method checks if a`  [INFERRED]
  /home/grisun0/LazyOwn/modules/ai_model.py → /tmp/lazyown-graphify-input/lazyown.py
- `OllamaModel` --uses--> `Intercepta comandos para expandir placeholders en aliases.         Maneja tanto`  [INFERRED]
  /home/grisun0/LazyOwn/modules/ai_model.py → /tmp/lazyown-graphify-input/lazyown.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.0
Nodes (467): OllamaModel, Ollama-hosted local backend.      Communicates with a local Ollama daemon via it, Yield streamed completion chunks for ``prompt``.          Args:             prom, Attach strace to a running process and log output to a file.          This funct, Helper method to wrap text to fit within specified width., Executes commands defined in a lazyscript file.          This function reads a s, Relanza la aplicación actual utilizando `proxychains` para enrutar el tráfico, Generates a Python one-liner to execute shellcode from a given URL.          Thi (+459 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (422): do_acknowledgearp(), do_acknowledgeicmp(), do_aclpwn_py(), do_ad_ldap_enum(), do_addalias(), do_addcli(), do_addhosts(), do_addspn_py() (+414 more)

### Community 2 - "Community 2"
Cohesion: 0.01
Nodes (334): BaseResolver, FileSystemEventHandler, add_dynamic_data(), _add_security_headers(), adversary(), aicmd(), aicmd_deepseek(), aicmd_view() (+326 more)

### Community 3 - "Community 3"
Cohesion: 0.01
Nodes (309): BaseHTTPRequestHandler, HTTPServer, search(), do_adsso_spray(), do_adversary(), do_aes_pe(), do_ai_playbook(), do_banners() (+301 more)

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (100): ABC, AgentRunner, AgentTool, ASTToolExtractor, CommandMetadata, configure_logging(), extract_commands_from_file(), interactive_mode() (+92 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (48): api_listeners(), api_listeners_create(), List all configured C2 listeners and their runtime status., Create a new listener., do_listener(), do_process_scans(), do_suggest_next(), audit_tasks() (+40 more)

### Community 6 - "Community 6"
Cohesion: 0.04
Nodes (38): Serve nmap HTML report assets from the sessions directory over HTTPS.      All u, webserver_report(), do_engage(), do_pipeline(), do_recommend_next(), AESKeyManager, Security services for the LazyOwn C2 web layer.  Services encapsulate stateful s, Read a file as text after path validation.          Args:             relative_p (+30 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (23): do_config_banner(), do_listaliases(), do_notify(), do_pop(), do_wizard(), Command to trigger a toastr-like notification.         Usage: notify <type> <mes, Display a toastr-like notification in the terminal with adaptive sizing., Print a session-start pro tip and handle first-run setup.          If ``sessions (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (25): Run the internal module GROQ AI located at `modules/lazysearch_bot.py` with the, Run the Metadata extractor internal module located at `modules/lazyown_metaextra, Run the internal module located at `modules/lazyownclient.py` with the specified, Run the internal module located at `modules/lazyownserver.py` with the specified, Run the internal module located at `modules/lazybotnet.py` with the specified pa, Run the internal module located at `modules/lazylfi2rce.py` with the specified p, Run the internal module located at `modules/lazybotcli.py` with the specified pa, Run the internal module located at `modules/lazyown_burpfuzzer.py` with the spec (+17 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (13): do_vulns(), Escáner de vulnerabilidades que busca y muestra información sobre CVEs.      Att, Inicializa el escáner con las cabeceras HTTP predefinidas., Busca CVEs basados en un servicio específico.          Args:             service, Search the NVD for CVEs matching a service banner and persist results.      The, Añade detalles adicionales a la información del CVE.          Args:, Initialize the scanner with configurable network and storage knobs.          Arg, Imprime una tabla bonita con detalles de CVEs.          Args:             cves_d (+5 more)

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (6): do_add2find(), do_rmfromfind(), Internal function to execute commands.          This method attempts to execute, Guarda un nuevo comando en user_commands.json, Carga los comandos personalizados desde user_commands.json, Guarda un nuevo comando en user_commands.json

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (4): Return a chat completion using native role separation.          Overrides the de, Fall through to the payload-aware completer for unhandled commands., Tab-complete the palette command using the live command index.          Position, Run the internal module located at `modules/lazybrutesshuserenum.py` with the sp

### Community 12 - "Community 12"
Cohesion: 0.29
Nodes (5): main(), Loads all YAML plugins from the 'lazyaddons/' directory.          This method sc, Registers a YAML plugin as a new command.          This method creates a dynamic, Loads all YAML plugins from the 'lazyaddons/' directory.          This method sc, Register a YAML addon as a shell command.          Reads the optional ``category

### Community 13 - "Community 13"
Cohesion: 0.5
Nodes (3): do_get_avaible_actions(), Devuelve una lista de acciones disponibles usando introspección de cmd2., Devuelve una lista de acciones disponibles usando introspección de cmd2.

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Security constants and validation patterns for the LazyOwn C2 web layer.  All re

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Generates an offensive playbook using:         1. Nmap scan results (CSV)

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Return a non-streaming completion for ``prompt``.

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): Yield streaming completion chunks for ``prompt``.

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Command to trigger a toastr-like notification.         Usage: notify <type> <mes

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Handle the end-of-file (EOF) condition.          This method is called when the

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Guided first-run setup wizard — configure rhost, lhost, domain, wordlists and mo

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Print a single-line operator context: rhost, lhost, domain, phase, os, creds.

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Show ELO score, karma rank and exploration progress for this operator.

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Search across all previous command outputs and session logs.          Searches i

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Get or set the current kill-chain phase.          When called without arguments,

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Capture a quick operator note attached to the current target and phase.

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Show a unified table of all captured credentials and hashes.          Reads ever

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Record a newly discovered pivot target or show the pivot chain.          When yo

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): View and manage the task queue from sessions/tasks.json.          Tasks are crea

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): List nmap scan files in sessions/ with age, size, and open ports.          Witho

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Print a unified operational situation report.          Aggregates in one view: t

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): assign a parameter value, persist to payload.json and refresh aliases.

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Show the current parameter values, sorted and aligned.          Rendering is del

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Browse the operator command catalogue grouped by kill-chain phase.          The

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Fuzzy search the graphify knowledge graph for nodes by label.          Usage: ``

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Show graph neighbors of a node or command from the graphify graph.          Usag

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Show the most-connected nodes ("god nodes") from the graph.          Usage: ``go

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Suggest next commands by walking the graph from recent activity.          Usage:

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Recommend the next command using policy engine + graph advisor.          Runs tw

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Show exploration coverage and addon/tool suggestions per service.          Reads

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): Launch the full-screen LazyOwn operator dashboard (Textual TUI).          Opens

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (1): Print the multi-operator collaboration join URL and SSE endpoint.          Outpu

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): Drive a single target through the full kill-chain in one command.          Usage

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): Declarative composition layer: run a YAML pipeline of LazyOwn commands.

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): Lists all available scripts in the modules directory.          This method print

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): Runs a specific LazyOwn script.          This method executes a script from the

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): Runs the internal module `modules/lazysearch.py`.          This method executes

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (1): Run the internal module located at `modules/LazyOwnExplorer.py`.          This m

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (1): Run the internal module located at `modules/lazyown.py`.          This method ex

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (1): Run the internal module located at `modules/update_db.sh`.          This method

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (1): Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (1): Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (1): Run the internal module located at `modules/lazywerkzeug.py` in debug mode.

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (1): Run the internal module located at `modules/lazygat.sh`. to gathering the sistem

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (1): Runs the internal module `modules/lazynmap.sh` with discovery mode.          Thi

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (1): Runs the internal module `modules/lazynmap.sh` with target mode.          OS det

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (1): Run the sniffer internal module located at `modules/lazysniff.py` with the speci

### Community 57 - "Community 57"
Cohesion: 1.0
Nodes (1): Run the sniffer ftp internal module located at `modules/lazyftpsniff.py` with th

### Community 58 - "Community 58"
Cohesion: 1.0
Nodes (1): Run the internal module to search netbios vuln victims, located at `modules/lazy

### Community 59 - "Community 59"
Cohesion: 1.0
Nodes (1): Run the internal module located at `modules/lazyhoneypot.py` with the specified

### Community 60 - "Community 60"
Cohesion: 1.0
Nodes (1): Run the internal module to create Oneliners with Groq AI located at `modules/laz

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (1): Load parameters from a specified payload JSON file.          This function loads

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (1): Exit the command line interface.          This function prompts the user to conf

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (1): Fix permissions for LazyOwn shell scripts.          This function adjusts the fi

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (1): Run LazyOwn webshell server.          This function starts a web server that ser

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (1): Retrieve and display file capabilities on the system.          This function use

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (1): Get the SecLists wordlist from GitHub.          This function downloads and extr

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (1): Interacts with SMB shares using the `smbclient` command to perform the following

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (1): Interacts with SMB shares using the `smbclient` command to perform the following

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (1): Interacts with SMB shares using the `smbclient.py` command to perform the follow

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (1): smbmap -H 10.10.10.3 [OPTIONS]         Uses the `smbmap` tool to interact with S

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (1): sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (1): Executes the Impacket PSExec tool to attempt remote execution on the specified t

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (1): Executes the Impacket PSExec tool to attempt remote execution on the specified t

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (1): Executes the `rpcdump.py` script to dump RPC services from a target host.

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (1): Executes the `dig` command to query DNS information.          1. Retrieves the D

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): Copies a file from the ExploitDB directory to the sessions directory.          1

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (1): Performs DNS enumeration using `dnsenum` to identify subdomains for a given doma

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (1): Performs DNS enumeration using `dnsmap` to discover subdomains for a specified d

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (1): Performs a web technology fingerprinting scan using `whatweb`.          1. Execu

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (1): Performs enumeration of information from a target Linux/Unix system using `enum4

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (1): Performs network scanning using `nbtscan` to discover NetBIOS names and addresse

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (1): Executes the `rpcclient` command to interact with a remote Windows system over R

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (1): Runs the `nikto` tool to perform a web server vulnerability scan against the spe

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (1): Runs the `finalrecon` tool to perform a web server vulnerability scan against th

### Community 85 - "Community 85"
Cohesion: 1.0
Nodes (1): Uses `openssl s_client` to connect to a specified host and port, allowing for te

### Community 86 - "Community 86"
Cohesion: 1.0
Nodes (1): Search all exploit sources and map findings to the next LazyOwn command.

### Community 87 - "Community 87"
Cohesion: 1.0
Nodes (1): Uses `wfuzz` to perform fuzzing based on provided parameters. This function supp

### Community 88 - "Community 88"
Cohesion: 1.0
Nodes (1): Searches for packages on Launchpad based on the provided search term and extract

### Community 89 - "Community 89"
Cohesion: 1.0
Nodes (1): Uses `gobuster` for directory and virtual host fuzzing based on provided paramet

### Community 90 - "Community 90"
Cohesion: 1.0
Nodes (1): Adds an entry to the `/etc/hosts` file, mapping an IP address to a domain name.

### Community 91 - "Community 91"
Cohesion: 1.0
Nodes (1): Execute CrackMapExec (CME) for SMB enumeration and authentication attempts again

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (1): Dumps LDAP information using `ldapdomaindump` with credentials from a file.

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (1): Perform LDAP enumeration using bloodhound-python with credentials from a file.

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (1): Perform a ping to check host availability and infer the operating system based o

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (1): Try gospider for web spidering.          This function executes the `gospider` t

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (1): Executes an ARP scan using `arp-scan`.          This function performs an ARP sc

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (1): Executes the LazyPwn script.          This function runs the `lazypwn.py` script

### Community 98 - "Community 98"
Cohesion: 1.0
Nodes (1): Fixes file permissions and line endings in the project directories.          Thi

### Community 99 - "Community 99"
Cohesion: 1.0
Nodes (1): Sets up an SMB server using Impacket and creates an SCF file for SMB share acces

### Community 100 - "Community 100"
Cohesion: 1.0
Nodes (1): Uses sqlmap to perform SQL injection testing on a given URL or request file (you

### Community 101 - "Community 101"
Cohesion: 1.0
Nodes (1): Runs a small proxy server to modify HTTP requests on the fly.          This func

### Community 102 - "Community 102"
Cohesion: 1.0
Nodes (1): Creates a web shell disguised as a `.jpg` file in the `sessions` directory.

### Community 103 - "Community 103"
Cohesion: 1.0
Nodes (1): Creates a bash reverse shell script in the `sessions` directory with the specifi

### Community 104 - "Community 104"
Cohesion: 1.0
Nodes (1): Creates a PowerShell reverse shell script in the `sessions` directory with the s

### Community 105 - "Community 105"
Cohesion: 1.0
Nodes (1): Creates a `hash.txt` file in the `sessions` directory with the specified hash va

### Community 106 - "Community 106"
Cohesion: 1.0
Nodes (1): Creates a `credentials.txt` file in the `sessions` directory with the specified

### Community 107 - "Community 107"
Cohesion: 1.0
Nodes (1): Creates a `cookie.txt` file in the `sessions` directory with the specified cooki

### Community 108 - "Community 108"
Cohesion: 1.0
Nodes (1): Downloads resources into the `sessions` directory.          This function perfor

### Community 109 - "Community 109"
Cohesion: 1.0
Nodes (1): Downloads and sets up exploits in the `external/.exploits/` directory and starts

### Community 110 - "Community 110"
Cohesion: 1.0
Nodes (1): Runs the `dirsearch` tool to perform directory and file enumeration on a specifi

### Community 111 - "Community 111"
Cohesion: 1.0
Nodes (1): Runs John the Ripper with a specified wordlist and options.          This functi

### Community 112 - "Community 112"
Cohesion: 1.0
Nodes (1): Runs Hashcat with specified attack mode and hash type using a wordlist.

### Community 113 - "Community 113"
Cohesion: 1.0
Nodes (1): Runs Responder on a specified network interface with elevated privileges.

### Community 114 - "Community 114"
Cohesion: 1.0
Nodes (1): Displays IP addresses of network interfaces and copies the IP address from the `

### Community 115 - "Community 115"
Cohesion: 1.0
Nodes (1): Displays IP addresses of network interfaces and prints the IP address from the `

### Community 116 - "Community 116"
Cohesion: 1.0
Nodes (1): Copies the remote host (rhost) to the clipboard and updates the command prompt.

### Community 117 - "Community 117"
Cohesion: 1.0
Nodes (1): Updates the command prompt to include the remote host (rhost) and current workin

### Community 118 - "Community 118"
Cohesion: 1.0
Nodes (1): Open a Powerlevel10k-style wizard to toggle prompt segments.          Arrow keys

### Community 119 - "Community 119"
Cohesion: 1.0
Nodes (1): Copies a Python reverse shell command to the clipboard.          This function g

### Community 120 - "Community 120"
Cohesion: 1.0
Nodes (1): Copies a reverse shell payload to the clipboard.          This function generate

### Community 121 - "Community 121"
Cohesion: 1.0
Nodes (1): Copies a malicious image tag payload to the clipboard.          This function cr

### Community 122 - "Community 122"
Cohesion: 1.0
Nodes (1): Creates a Visual Basic Script (VBS) to attempt to disable antivirus settings.

### Community 123 - "Community 123"
Cohesion: 1.0
Nodes (1): Downloads ConPtyShell and prepares a PowerShell command for remote access.

### Community 124 - "Community 124"
Cohesion: 1.0
Nodes (1): Runs `pwncat-cs` with the specified port for listening.          This function s

### Community 125 - "Community 125"
Cohesion: 1.0
Nodes (1): Runs `pwncat` with the specified port for listening. SELFINJECT          This fu

### Community 126 - "Community 126"
Cohesion: 1.0
Nodes (1): Automates command execution based on a list of aliases and commands.          1.

### Community 127 - "Community 127"
Cohesion: 1.0
Nodes (1): Executes a shell command directly from the LazyOwn interface.          This func

### Community 128 - "Community 128"
Cohesion: 1.0
Nodes (1): Executes a shell command directly from the LazyOwn interface.          This func

### Community 129 - "Community 129"
Cohesion: 1.0
Nodes (1): Displays the current working directory and lists files, and copies the current d

### Community 130 - "Community 130"
Cohesion: 1.0
Nodes (1): Exits the application quickly without confirmation.          This function perfo

### Community 131 - "Community 131"
Cohesion: 1.0
Nodes (1): Configures the system to ignore ARP requests by setting a kernel parameter.

### Community 132 - "Community 132"
Cohesion: 1.0
Nodes (1): Configures the system to ignore ICMP echo requests by setting a kernel parameter

### Community 133 - "Community 133"
Cohesion: 1.0
Nodes (1): Configures the system to acknowledge ARP requests by setting a kernel parameter.

### Community 134 - "Community 134"
Cohesion: 1.0
Nodes (1): Configures the system to respond to ICMP echo requests by setting a kernel param

### Community 135 - "Community 135"
Cohesion: 1.0
Nodes (1): Displays the current date and time, and runs a custom shell script.          Thi

### Community 136 - "Community 136"
Cohesion: 1.0
Nodes (1): Lists all open TCP and UDP ports on the local system.          This function per

### Community 137 - "Community 137"
Cohesion: 1.0
Nodes (1): Connects to an SSH host using credentials from a file and a specified port.

### Community 138 - "Community 138"
Cohesion: 1.0
Nodes (1): Connects to an ftp host using credentials from a file and a specified port.

### Community 139 - "Community 139"
Cohesion: 1.0
Nodes (1): Generates a command to display TCP and UDP ports and copies it to the clipboard.

### Community 140 - "Community 140"
Cohesion: 1.0
Nodes (1): Connect to a VPN by selecting from available .ovpn files.          This function

### Community 141 - "Community 141"
Cohesion: 1.0
Nodes (1): Create an SSH private key file and connect to a remote host using SSH.

### Community 142 - "Community 142"
Cohesion: 1.0
Nodes (1): Start a web server using Python 3 and display relevant network information.

### Community 143 - "Community 143"
Cohesion: 1.0
Nodes (1): Copy payloads to clipboard for Local File Inclusion (LFI) attacks.          This

### Community 144 - "Community 144"
Cohesion: 1.0
Nodes (1): Sends an email using `swaks` (Swiss Army Knife for SMTP).          This method c

### Community 145 - "Community 145"
Cohesion: 1.0
Nodes (1): Run `impacket-samrdump` to dump SAM data from specified ports.          This fun

### Community 146 - "Community 146"
Cohesion: 1.0
Nodes (1): Encode a string for URL.          This function takes a string as input, encodes

### Community 147 - "Community 147"
Cohesion: 1.0
Nodes (1): Decode a URL-encoded string.          This function takes a URL-encoded string a

### Community 148 - "Community 148"
Cohesion: 1.0
Nodes (1): Performs a Lynis audit on the specified remote system.          This function ex

### Community 149 - "Community 149"
Cohesion: 1.0
Nodes (1): Performs an SNMP check on the specified target host.          This function exec

### Community 150 - "Community 150"
Cohesion: 1.0
Nodes (1): Performs an SNMP check on the specified target host.          This function exec

### Community 151 - "Community 151"
Cohesion: 1.0
Nodes (1): Encodes a string using the specified shift value and substitution key.

### Community 152 - "Community 152"
Cohesion: 1.0
Nodes (1): Decode a string using the specified shift value and substitution key.          T

### Community 153 - "Community 153"
Cohesion: 1.0
Nodes (1): Display the credentials stored in the `credentials.txt` file and copy the passwo

### Community 154 - "Community 154"
Cohesion: 1.0
Nodes (1): Discover active hosts in a subnet by performing a ping sweep.          This meth

### Community 155 - "Community 155"
Cohesion: 1.0
Nodes (1): Scan all ports on a specified host to identify open ports.          This method

### Community 156 - "Community 156"
Cohesion: 1.0
Nodes (1): Scan all ports on a specified host to identify open ports and associated service

### Community 157 - "Community 157"
Cohesion: 1.0
Nodes (1): Apply a ROT (rotation) substitution cipher to the given string.          This fu

### Community 158 - "Community 158"
Cohesion: 1.0
Nodes (1): Apply a ROT (rotation) substitution cipher to the given extension.          This

### Community 159 - "Community 159"
Cohesion: 1.0
Nodes (1): Uses Hydra to perform a brute force attack on a specified HTTP service with a us

### Community 160 - "Community 160"
Cohesion: 1.0
Nodes (1): Uses medusa to perform a brute force attack on a specified ssh service with a us

### Community 161 - "Community 161"
Cohesion: 1.0
Nodes (1): Perform an Nmap scan using a specified script and port.          :param line: A

### Community 162 - "Community 162"
Cohesion: 1.0
Nodes (1): Applies various obfuscations to a given command line string to create multiple o

### Community 163 - "Community 163"
Cohesion: 1.0
Nodes (1): Enumerates SMTP users using the `smtp-user-enum` tool with the VRFY method.

### Community 164 - "Community 164"
Cohesion: 1.0
Nodes (1): Starts the SSH service and displays its status.          1. Executes the command

### Community 165 - "Community 165"
Cohesion: 1.0
Nodes (1): Provides help to find and display information about Nmap scripts.          1. Ch

### Community 166 - "Community 166"
Cohesion: 1.0
Nodes (1): Search for commands matching the given parameter in the cmd interface and option

### Community 167 - "Community 167"
Cohesion: 1.0
Nodes (1): Helps to find hash types in Hashcat by searching through its help output.

### Community 168 - "Community 168"
Cohesion: 1.0
Nodes (1): Deletes files and directories in the `sessions` directory, excluding specified f

### Community 169 - "Community 169"
Cohesion: 1.0
Nodes (1): Automates the execution of pwntomate tools on XML configuration files.

### Community 170 - "Community 170"
Cohesion: 1.0
Nodes (1): Prints all configured aliases and their associated commands.          1. Retriev

### Community 171 - "Community 171"
Cohesion: 1.0
Nodes (1): Starts `tcpdump` to capture ICMP traffic on the specified interface.          1.

### Community 172 - "Community 172"
Cohesion: 1.0
Nodes (1): Starts packet capture using `tcpdump` on the specified interface.          1. Ch

### Community 173 - "Community 173"
Cohesion: 1.0
Nodes (1): Analyzes a packet capture file using `tshark` based on the provided remote host

### Community 174 - "Community 174"
Cohesion: 1.0
Nodes (1): Reads credentials from a file, encrypts the password, and executes the RDP conne

### Community 175 - "Community 175"
Cohesion: 1.0
Nodes (1): Encodes a given string into Base64 format.          1. Encodes the input string:

### Community 176 - "Community 176"
Cohesion: 1.0
Nodes (1): Decodes a Base64 encoded string.          1. Decodes the Base64 string:

### Community 177 - "Community 177"
Cohesion: 1.0
Nodes (1): Creates and copies a shell command to add a new user `grisun0`, assign a passwor

### Community 178 - "Community 178"
Cohesion: 1.0
Nodes (1): Creates and copies a PowerShell command to add a new user `grisun0`, assign a pa

### Community 179 - "Community 179"
Cohesion: 1.0
Nodes (1): Encodes a given payload into a Base64 encoded string suitable for Windows PowerS

### Community 180 - "Community 180"
Cohesion: 1.0
Nodes (1): Creates a base64 encoded payload specifically for Windows to execute a PowerShel

### Community 181 - "Community 181"
Cohesion: 1.0
Nodes (1): Creates a base64 encoded PowerShell reverse shell payload specifically for Windo

### Community 182 - "Community 182"
Cohesion: 1.0
Nodes (1): Creates a base64 encoded ASP reverse shell payload and copies it to the clipboar

### Community 183 - "Community 183"
Cohesion: 1.0
Nodes (1): Copies a command to the clipboard for downloading and running Rubeus.          1

### Community 184 - "Community 184"
Cohesion: 1.0
Nodes (1): Sets up and runs a `socat` tunnel with SOCKS4A proxy support.          1. If no

### Community 185 - "Community 185"
Cohesion: 1.0
Nodes (1): Automates the setup and execution of Chisel server and client for tunneling and

### Community 186 - "Community 186"
Cohesion: 1.0
Nodes (1): Automates various Metasploit tasks including scanning for vulnerabilities, setti

### Community 187 - "Community 187"
Cohesion: 1.0
Nodes (1): Encrypts a file using XOR encryption.          1. Splits the provided `line` int

### Community 188 - "Community 188"
Cohesion: 1.0
Nodes (1): Decrypts a file using XOR encryption.          1. Splits the provided `line` int

### Community 189 - "Community 189"
Cohesion: 1.0
Nodes (1): Ejecuta un comando para listar las conexiones SSH activas.          Este método

### Community 190 - "Community 190"
Cohesion: 1.0
Nodes (1): Attach strace to a running process and log output to a file.          This funct

### Community 191 - "Community 191"
Cohesion: 1.0
Nodes (1): Executes commands defined in a lazyscript file.          This function reads a s

### Community 192 - "Community 192"
Cohesion: 1.0
Nodes (1): Relanza la aplicación actual utilizando `proxychains` para enrutar el tráfico

### Community 193 - "Community 193"
Cohesion: 1.0
Nodes (1): Generates a Python one-liner to execute shellcode from a given URL.          Thi

### Community 194 - "Community 194"
Cohesion: 1.0
Nodes (1): This function executes the web security scanning tool Skipfish         using the

### Community 195 - "Community 195"
Cohesion: 1.0
Nodes (1): Create a Windows DLL file using MinGW-w64 or a Blazor DLL for Linux.          Th

### Community 196 - "Community 196"
Cohesion: 1.0
Nodes (1): Performs a web seo fingerprinting scan using `lazyseo.py`.          1. Executes

### Community 197 - "Community 197"
Cohesion: 1.0
Nodes (1): Execute the PadBuster command for padding oracle attacks.          This function

### Community 198 - "Community 198"
Cohesion: 1.0
Nodes (1): Scans for hosts with SMB service open on port 445 in the specified target networ

### Community 199 - "Community 199"
Cohesion: 1.0
Nodes (1): Automates the exploitation of the Cacti version 1.2.26 vulnerability         usi

### Community 200 - "Community 200"
Cohesion: 1.0
Nodes (1): Handles the creation of temporary files for users and passwords based on a small

### Community 201 - "Community 201"
Cohesion: 1.0
Nodes (1): Set up and run ngrok on a specified local port. If ngrok is not installed, it wi

### Community 202 - "Community 202"
Cohesion: 1.0
Nodes (1): This function generates a PowerShell script that retrieves saved Wi-Fi passwords

### Community 203 - "Community 203"
Cohesion: 1.0
Nodes (1): Executes a Shellshock attack against a target.          This function constructs

### Community 204 - "Community 204"
Cohesion: 1.0
Nodes (1): This function generates a PowerShell script that retrieves reverse shell over ht

### Community 205 - "Community 205"
Cohesion: 1.0
Nodes (1): Interactive Morse Code Converter.          This function serves as an interface

### Community 206 - "Community 206"
Cohesion: 1.0
Nodes (1): Fetch URLs from the Wayback Machine for a given website.         The URL is take

### Community 207 - "Community 207"
Cohesion: 1.0
Nodes (1): Manage C2 listeners: list, add, start, stop, remove.          Usage:

### Community 208 - "Community 208"
Cohesion: 1.0
Nodes (1): Toggle or query Docker sandbox mode.          When ``sandboxed`` is ``true`` in

### Community 209 - "Community 209"
Cohesion: 1.0
Nodes (1): Handles the process of sending a spoofed ARP packet to a specified IP address wi

### Community 210 - "Community 210"
Cohesion: 1.0
Nodes (1): Asks the user for the URL, database, table, and columns, and then executes the P

### Community 211 - "Community 211"
Cohesion: 1.0
Nodes (1): Generates an SSH key pair with RSA 4096-bit encryption. If no name is provided,

### Community 212 - "Community 212"
Cohesion: 1.0
Nodes (1): Generate a custom dictionary using the `crunch` tool.          This function cre

### Community 213 - "Community 213"
Cohesion: 1.0
Nodes (1): Fetches and displays malware information from the MalwareBazaar API based on the

### Community 214 - "Community 214"
Cohesion: 1.0
Nodes (1): Download a malware sample from MalwareBazaar using its SHA256 hash.          Thi

### Community 215 - "Community 215"
Cohesion: 1.0
Nodes (1): Run an SSL scan on the specified remote host.          This function initiates a

### Community 216 - "Community 216"
Cohesion: 1.0
Nodes (1): This function constructs and executes a command for the 'cewl' tool.         It

### Community 217 - "Community 217"
Cohesion: 1.0
Nodes (1): This function constructs and executes a command for the 'dmitry' tool.         I

### Community 218 - "Community 218"
Cohesion: 1.0
Nodes (1): Executes the graudit command to perform a static code analysis with the specifie

### Community 219 - "Community 219"
Cohesion: 1.0
Nodes (1): Connects to the msfrpcd daemon and allows remote control of Metasploit.

### Community 220 - "Community 220"
Cohesion: 1.0
Nodes (1): Executes a Nuclei scan on a specified target URL or host.          Usage:

### Community 221 - "Community 221"
Cohesion: 1.0
Nodes (1): Executes a parsero scan on a specified target URL or host.          Usage:

### Community 222 - "Community 222"
Cohesion: 1.0
Nodes (1): Executes the Sherlock tool to find usernames across social networks.          Th

### Community 223 - "Community 223"
Cohesion: 1.0
Nodes (1): Executes trufflehog to search for secrets in a given Git repository URL.

### Community 224 - "Community 224"
Cohesion: 1.0
Nodes (1): Generate a PHP backdoor using Weevely, protected with the given password.

### Community 225 - "Community 225"
Cohesion: 1.0
Nodes (1): Connect to PHP backdoor using Weevely, protected with the given password.

### Community 226 - "Community 226"
Cohesion: 1.0
Nodes (1): Executes a changeme scan on a specified target URL or host.          Usage:

### Community 227 - "Community 227"
Cohesion: 1.0
Nodes (1): Performs enumeration of information from a target system using `enum4linux-ng`.

### Community 228 - "Community 228"
Cohesion: 1.0
Nodes (1): Executes a web server fuzzing script with user-provided parameters.          Thi

### Community 229 - "Community 229"
Cohesion: 1.0
Nodes (1): Executes a payload creation framework for the retrieval and execution of arbitra

### Community 230 - "Community 230"
Cohesion: 1.0
Nodes (1): Starts the Sliver server and generates a client configuration file for connectin

### Community 231 - "Community 231"
Cohesion: 1.0
Nodes (1): Generates a certificate authority (CA), client certificate, and client key.

### Community 232 - "Community 232"
Cohesion: 1.0
Nodes (1): Executes the Kerbrute tool to enumerate user accounts against a specified target

### Community 233 - "Community 233"
Cohesion: 1.0
Nodes (1): Execute the dacledit.py command for a specific user or all users listed in the u

### Community 234 - "Community 234"
Cohesion: 1.0
Nodes (1): Execute the bloodyAD.py command for a specific user or all users listed in the u

### Community 235 - "Community 235"
Cohesion: 1.0
Nodes (1): Execute the Evil-WinRM tool for authentication attempts on a specified target us

### Community 236 - "Community 236"
Cohesion: 1.0
Nodes (1): Requests a Ticket Granting Ticket (TGT) using the Impacket tool with provided cr

### Community 237 - "Community 237"
Cohesion: 1.0
Nodes (1): Performs enumeration of users from a target system using `apache-users`.

### Community 238 - "Community 238"
Cohesion: 1.0
Nodes (1): Creates a backdoored executable using `backdoor-factory`.          This function

### Community 239 - "Community 239"
Cohesion: 1.0
Nodes (1): Tests WebDAV server configurations using `davtest`.          This function check

### Community 240 - "Community 240"
Cohesion: 1.0
Nodes (1): Generates payloads using MSFvenom Payload Creator (MSFPC).          This functio

### Community 241 - "Community 241"
Cohesion: 1.0
Nodes (1): Generates payloads using Ivy with various options. Ivy is a payload creation fra

### Community 242 - "Community 242"
Cohesion: 1.0
Nodes (1): Execute the tor.sh script with the specified port or default to port 80 if no po

### Community 243 - "Community 243"
Cohesion: 1.0
Nodes (1): Generates a wordlist based on a target name and a list of characters, with vario

### Community 244 - "Community 244"
Cohesion: 1.0
Nodes (1): Traces the DNS information for a given domain using the FreeDNS service. (using

### Community 245 - "Community 245"
Cohesion: 1.0
Nodes (1): Generates payloads using Veil-Evasion with various options. Veil-Evasion is a pa

### Community 246 - "Community 246"
Cohesion: 1.0
Nodes (1): Generates payloads using PowerShell Empire with various options.          :param

### Community 247 - "Community 247"
Cohesion: 1.0
Nodes (1): Runs evil-ssdp with various options and user-selected templates.          :param

### Community 248 - "Community 248"
Cohesion: 1.0
Nodes (1): Runs Shellfire with various options and allows generating payloads.          :pa

### Community 249 - "Community 249"
Cohesion: 1.0
Nodes (1): Generates a graph from JSON payload files containing URL, RHOST, and RPORT.

### Community 250 - "Community 250"
Cohesion: 1.0
Nodes (1): Executes netexec with various options for network protocol operations.

### Community 251 - "Community 251"
Cohesion: 1.0
Nodes (1): Executes ScareCrow with various options for bypassing EDR solutions and executin

### Community 252 - "Community 252"
Cohesion: 1.0
Nodes (1): Generate email permutations based on a full name and domain, then save them to a

### Community 253 - "Community 253"
Cohesion: 1.0
Nodes (1): Executes EyeWitness to capture screenshots from a list of URLs.         You need

### Community 254 - "Community 254"
Cohesion: 1.0
Nodes (1): Run secretsdump.py with the provided domain, username, password, and IP address.

### Community 255 - "Community 255"
Cohesion: 1.0
Nodes (1): Run GetUserSPNs.py with the provided domain, username, password, and IP address.

### Community 256 - "Community 256"
Cohesion: 1.0
Nodes (1): Perform password spraying using crackmapexec with the provided parameters.

### Community 257 - "Community 257"
Cohesion: 1.0
Nodes (1): Perform port scanning using vscan with the provided parameters.          :param

### Community 258 - "Community 258"
Cohesion: 1.0
Nodes (1): Attempt to exploit the Shellshock vulnerability (CVE-2014-6271, CVE-2014-7169).

### Community 259 - "Community 259"
Cohesion: 1.0
Nodes (1): Generate a reverse shell in various programming languages.          This functio

### Community 260 - "Community 260"
Cohesion: 1.0
Nodes (1): Executes the 'alterx' command for subdomain enumeration on the provided domain.

### Community 261 - "Community 261"
Cohesion: 1.0
Nodes (1): Execute the AlliN.py tool with various scan modes and parameters.          This

### Community 262 - "Community 262"
Cohesion: 1.0
Nodes (1): Execute the Dr0p1t tool to create a stealthy malware dropper.          This func

### Community 263 - "Community 263"
Cohesion: 1.0
Nodes (1): Install and execute the git-dumper tool to download Git repository content.

### Community 264 - "Community 264"
Cohesion: 1.0
Nodes (1): Generate and execute a PowerShell command stager to run a .ps1 script.

### Community 265 - "Community 265"
Cohesion: 1.0
Nodes (1): Search the shell-storm API for shellcodes using the provided keywords.

### Community 266 - "Community 266"
Cohesion: 1.0
Nodes (1): Automates the setup and execution of Ligolo server and client for tunneling and

### Community 267 - "Community 267"
Cohesion: 1.0
Nodes (1): Opens or creates the users.txt file in the sessions directory for editing using

### Community 268 - "Community 268"
Cohesion: 1.0
Nodes (1): Execute the windapsearch tool to perform Active Directory Domain enumeration thr

### Community 269 - "Community 269"
Cohesion: 1.0
Nodes (1): Decrypts TightVNC passwords using Metasploit.          This function demonstrate

### Community 270 - "Community 270"
Cohesion: 1.0
Nodes (1): Execute the Shadowsocks tool to create a secure tunnel for network traffic.

### Community 271 - "Community 271"
Cohesion: 1.0
Nodes (1): Extracts usernames from a JSON output generated by go-windapsearch and appends t

### Community 272 - "Community 272"
Cohesion: 1.0
Nodes (1): Generate a downloader command for files in the sessions directory.          This

### Community 273 - "Community 273"
Cohesion: 1.0
Nodes (1): Executes an LDAP search against a target remote host (rhost) and saves the resul

### Community 274 - "Community 274"
Cohesion: 1.0
Nodes (1): Automates the EternalBlue (MS17-010) exploitation process using Metasploit.

### Community 275 - "Community 275"
Cohesion: 1.0
Nodes (1): Search for a CVE using the CIRCL API.          This function sends a GET request

### Community 276 - "Community 276"
Cohesion: 1.0
Nodes (1): Compresses the 'sessions' folder and encodes it into a video using the lazyown_i

### Community 277 - "Community 277"
Cohesion: 1.0
Nodes (1): HttpFileServer version 2.3. Vulnerable using the module rejetto_hfs_exec of meta

### Community 278 - "Community 278"
Cohesion: 1.0
Nodes (1): SMB CVE-2008-4250. Vulnerable using the module ms08_067_netapi of metasploit

### Community 279 - "Community 279"
Cohesion: 1.0
Nodes (1): Try to check if Vulnerable using the module passed by argument of lazyown exampl

### Community 280 - "Community 280"
Cohesion: 1.0
Nodes (1): (CVE-2017-7269). Vulnerable using the module iis_webdav_upload_asp of metasploit

### Community 281 - "Community 281"
Cohesion: 1.0
Nodes (1): Opens or creates the file using line in the sessions directory for editing using

### Community 282 - "Community 282"
Cohesion: 1.0
Nodes (1): Runs `nc` with the specified port for listening.          This function starts a

### Community 283 - "Community 283"
Cohesion: 1.0
Nodes (1): Runs `nc` with rlwrap  the specified port for listening.          This function

### Community 284 - "Community 284"
Cohesion: 1.0
Nodes (1): Create a new JSON payload file based on the template provided in payload.json.

### Community 285 - "Community 285"
Cohesion: 1.0
Nodes (1): Executes the XSS (Cross-Site Scripting) vulnerability testing procedure

### Community 286 - "Community 286"
Cohesion: 1.0
Nodes (1): Executes an Arjun scan on the specified URL for parameter discovery.          Th

### Community 287 - "Community 287"
Cohesion: 1.0
Nodes (1): Transforms the input string based on user-defined casing style.          This co

### Community 288 - "Community 288"
Cohesion: 1.0
Nodes (1): duckyspark Compiles and uploads an .ino sketch to a Digispark device using Ardui

### Community 289 - "Community 289"
Cohesion: 1.0
Nodes (1): Generate usernames using the username-anarchy tool based on user input.

### Community 290 - "Community 290"
Cohesion: 1.0
Nodes (1): Command emp3r0r Downloads and sets up the Emperor server for local exploitation.

### Community 291 - "Community 291"
Cohesion: 1.0
Nodes (1): Handles the creation and serialization of a template helper.          This funct

### Community 292 - "Community 292"
Cohesion: 1.0
Nodes (1): Command gospherus: Clones and uses the Gopherus tool to generate gopher payloads

### Community 293 - "Community 293"
Cohesion: 1.0
Nodes (1): Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scan

### Community 294 - "Community 294"
Cohesion: 1.0
Nodes (1): Create multiple JSON payload files based on a CSV input file from HackerOne.

### Community 295 - "Community 295"
Cohesion: 1.0
Nodes (1): List all .kdbx files in the 'sessions' directory, let the user select one, and r

### Community 296 - "Community 296"
Cohesion: 1.0
Nodes (1): Open a .kdbx file and print the titles and contents of all entries. The password

### Community 297 - "Community 297"
Cohesion: 1.0
Nodes (1): Attempts to connect to an MSSQL server using the mssqlclient.py tool with Window

### Community 298 - "Community 298"
Cohesion: 1.0
Nodes (1): Executes the GetADUsers.py script to retrieve Active Directory users.          T

### Community 299 - "Community 299"
Cohesion: 1.0
Nodes (1): Crack a Cisco Type 7 password hash and display the plaintext.          This comm

### Community 300 - "Community 300"
Cohesion: 1.0
Nodes (1): Command loxs: Installs and runs Loxs for multi-vulnerability web application sca

### Community 301 - "Community 301"
Cohesion: 1.0
Nodes (1): Command blazy: Installs and runs blazy for multi-vulnerability web application s

### Community 302 - "Community 302"
Cohesion: 1.0
Nodes (1): Command parth: Installs and runs Parth for discovering vulnerable URLs and param

### Community 303 - "Community 303"
Cohesion: 1.0
Nodes (1): Command breacher: Installs and runs Breacher for finding admin login pages and E

### Community 304 - "Community 304"
Cohesion: 1.0
Nodes (1): Command xsstrike: Installs and runs XSStrike for finding XSS vulnerabilities.

### Community 305 - "Community 305"
Cohesion: 1.0
Nodes (1): Command penelope: Installs and runs Penelope for handling reverse and bind shell

### Community 306 - "Community 306"
Cohesion: 1.0
Nodes (1): Open a new window within a tmux session using the LazyOwn RedTeam Framework.

### Community 307 - "Community 307"
Cohesion: 1.0
Nodes (1): Open a new window within a tmux session using the LazyOwn RedTeam Framework.

### Community 308 - "Community 308"
Cohesion: 1.0
Nodes (1): Command adgetpass: Generates a PowerShell script to extract credentials from Azu

### Community 309 - "Community 309"
Cohesion: 1.0
Nodes (1): Command openredirex: Clones, installs, and runs OpenRedirex for testing open red

### Community 310 - "Community 310"
Cohesion: 1.0
Nodes (1): Command feroxbuster: Installs and runs Feroxbuster for performing forced browsin

### Community 311 - "Community 311"
Cohesion: 1.0
Nodes (1): Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target O

### Community 312 - "Community 312"
Cohesion: 1.0
Nodes (1): Command sireprat: Automates the setup and usage of SirepRAT to perform various a

### Community 313 - "Community 313"
Cohesion: 1.0
Nodes (1): Generates hosts.txt, urls.txt, domains.txt, and targets.txt from multiple JSON p

### Community 314 - "Community 314"
Cohesion: 1.0
Nodes (1): Converts shellcode to SYLK format and saves the result to a file.          This

### Community 315 - "Community 315"
Cohesion: 1.0
Nodes (1): Command magicrecon: Automates the setup and usage of MagicRecon to perform vario

### Community 316 - "Community 316"
Cohesion: 1.0
Nodes (1): Command cubespraying: Automates the installation and usage of CubeSpraying for p

### Community 317 - "Community 317"
Cohesion: 1.0
Nodes (1): Run samdump2 with the SAM and SYSTEM file          :param line: This parameter i

### Community 318 - "Community 318"
Cohesion: 1.0
Nodes (1): Command stormbreaker: Automates the installation and usage of Storm-Breaker for

### Community 319 - "Community 319"
Cohesion: 1.0
Nodes (1): Command upload_bypass: Automates the installation and execution of Upload_Bypass

### Community 320 - "Community 320"
Cohesion: 1.0
Nodes (1): Converts hexadecimal data from a file to plain text.          Opens a text edito

### Community 321 - "Community 321"
Cohesion: 1.0
Nodes (1): Command rpcmap_py: Executes rpcmap.py commands to enumerate MSRPC interfaces.

### Community 322 - "Community 322"
Cohesion: 1.0
Nodes (1): Command serveralive2: Uses Impacket to connect to a remote MSRPC interface and r

### Community 323 - "Community 323"
Cohesion: 1.0
Nodes (1): List all .zip files in the 'sessions' directory, let the user select one, and ru

### Community 324 - "Community 324"
Cohesion: 1.0
Nodes (1): Command createusers_and_hashs: Extracts usernames and hashes from a dump file.

### Community 325 - "Community 325"
Cohesion: 1.0
Nodes (1): Command pykerbrute: Automates the installation and execution of PyKerbrute for b

### Community 326 - "Community 326"
Cohesion: 1.0
Nodes (1): Run reg.py with specified parameters to query the registry.          :param line

### Community 327 - "Community 327"
Cohesion: 1.0
Nodes (1): Identify hash type using nth after retrieving it with get_hash().          :para

### Community 328 - "Community 328"
Cohesion: 1.0
Nodes (1): Generate a list of possible passwords by filling each asterisk in the input with

### Community 329 - "Community 329"
Cohesion: 1.0
Nodes (1): Checks if the script is running with superuser (sudo) privileges, and if not,

### Community 330 - "Community 330"
Cohesion: 1.0
Nodes (1): Serve linpeas.sh via HTTP and print the one-liner to run on the target.

### Community 331 - "Community 331"
Cohesion: 1.0
Nodes (1): Serve winPEAS via HTTP and print the one-liner to run on the target.          Lo

### Community 332 - "Community 332"
Cohesion: 1.0
Nodes (1): Run Linux Exploit Suggester against the current target's kernel info.          R

### Community 333 - "Community 333"
Cohesion: 1.0
Nodes (1): Print SUID/SGID enumeration commands for the current target OS.          Outputs

### Community 334 - "Community 334"
Cohesion: 1.0
Nodes (1): Serve pspy (process spy without root) via HTTP for the target to download.

### Community 335 - "Community 335"
Cohesion: 1.0
Nodes (1): Look up a binary in GTFOBins / LOLBas and show exploitation techniques.

### Community 336 - "Community 336"
Cohesion: 1.0
Nodes (1): Ask the AI a question with current session context pre-loaded.          Injects

### Community 337 - "Community 337"
Cohesion: 1.0
Nodes (1): Executes the Impacket netview tool to list network shares on a specified target.

### Community 338 - "Community 338"
Cohesion: 1.0
Nodes (1): Executes the Impacket WMIExec tool to run commands on a target system using WMI.

### Community 339 - "Community 339"
Cohesion: 1.0
Nodes (1): Extracts open ports and IP address information from a specified file.          T

### Community 340 - "Community 340"
Cohesion: 1.0
Nodes (1): Schedules a command to run at a specified time.          This function allows us

### Community 341 - "Community 341"
Cohesion: 1.0
Nodes (1): Executes the PEzor tool to pack executables or shellcode with custom configurati

### Community 342 - "Community 342"
Cohesion: 1.0
Nodes (1): Executes the Impacket Mimikatz tool to interact with a target system for credent

### Community 343 - "Community 343"
Cohesion: 1.0
Nodes (1): Executes the RDP check tool to verify credentials or hash-based authentication o

### Community 344 - "Community 344"
Cohesion: 1.0
Nodes (1): Executes the MQTT check tool to verify credentials on a target system with optio

### Community 345 - "Community 345"
Cohesion: 1.0
Nodes (1): Executes the LookupSID tool to perform SID enumeration on a target system.

### Community 346 - "Community 346"
Cohesion: 1.0
Nodes (1): Executes the Scavenger tool for multi-threaded post-exploitation scanning on tar

### Community 347 - "Community 347"
Cohesion: 1.0
Nodes (1): Performs various checks on a selected binary to gather information and protectio

### Community 348 - "Community 348"
Cohesion: 1.0
Nodes (1): Executes the Impacket lookupsid tool to enumerate SIDs on a target system.

### Community 349 - "Community 349"
Cohesion: 1.0
Nodes (1): Executes the Certipy tool to interact with Active Directory Certificate Services

### Community 350 - "Community 350"
Cohesion: 1.0
Nodes (1): Executes the MSDT Follina exploit tool to create malicious documents for exploit

### Community 351 - "Community 351"
Cohesion: 1.0
Nodes (1): Executes the Swaks (Swiss Army Knife for SMTP) tool to send test emails for phis

### Community 352 - "Community 352"
Cohesion: 1.0
Nodes (1): Executes ad-ldap-enum to enumerate Active Directory objects (users, groups, comp

### Community 353 - "Community 353"
Cohesion: 1.0
Nodes (1): Unzips a specified file from the sessions directory.          This function atte

### Community 354 - "Community 354"
Cohesion: 1.0
Nodes (1): Executes the reGeorg tool for HTTP(s) tunneling through a SOCKS proxy.

### Community 355 - "Community 355"
Cohesion: 1.0
Nodes (1): Reduces a wordlist based on the specified password length.          This functio

### Community 356 - "Community 356"
Cohesion: 1.0
Nodes (1): Executes the pyWhisker tool for manipulating the msDS-KeyCredentialLink attribut

### Community 357 - "Community 357"
Cohesion: 1.0
Nodes (1): Executes the Impacket owneredit tool for manipulating ownership of Active Direct

### Community 358 - "Community 358"
Cohesion: 1.0
Nodes (1): Executes the net rpc group addmem command to add a user to a specified group in

### Community 359 - "Community 359"
Cohesion: 1.0
Nodes (1): Executes the Pass-the-Hash (PTH) Net tool to change the password of an Active Di

### Community 360 - "Community 360"
Cohesion: 1.0
Nodes (1): Executes the gettgtpkinit.py tool from PKINITtools to request a TGT using Kerber

### Community 361 - "Community 361"
Cohesion: 1.0
Nodes (1): Executes the getnthash.py tool from PKINITtools to retrieve the NT hash using a

### Community 362 - "Community 362"
Cohesion: 1.0
Nodes (1): Executes the gets4uticket.py tool from PKINITtools to request an S4U2Self servic

### Community 363 - "Community 363"
Cohesion: 1.0
Nodes (1): Executes the aclpwn.py tool to find and exploit ACL paths for privilege escalati

### Community 364 - "Community 364"
Cohesion: 1.0
Nodes (1): Executes the addspn.py tool to manage Service Principal Names (SPNs) on Active D

### Community 365 - "Community 365"
Cohesion: 1.0
Nodes (1): Executes the dnstool.py tool to modify Active Directory-integrated DNS records.

### Community 366 - "Community 366"
Cohesion: 1.0
Nodes (1): Executes the printerbug.py tool to trigger the SpoolService bug via RPC backconn

### Community 367 - "Community 367"
Cohesion: 1.0
Nodes (1): Executes the krbrelayx.py tool for Kerberos relaying or unconstrained delegation

### Community 368 - "Community 368"
Cohesion: 1.0
Nodes (1): Executes the autobloody tool for automating Active Directory privilege escalatio

### Community 369 - "Community 369"
Cohesion: 1.0
Nodes (1): Uploads a file to Gofile storage.          This function performs the following

### Community 370 - "Community 370"
Cohesion: 1.0
Nodes (1): We open a Netcat listener on port 443 and attempt to exploit NodeJS deserializat

### Community 371 - "Community 371"
Cohesion: 1.0
Nodes (1): Initiates a reverse MSSQL shell by starting an HTTP server to handle incoming co

### Community 372 - "Community 372"
Cohesion: 1.0
Nodes (1): Executes the targetedKerberoast tool for extracting Kerberos service tickets.

### Community 373 - "Community 373"
Cohesion: 1.0
Nodes (1): Executes the pyOracle2 tool for performing padding oracle attacks.          This

### Community 374 - "Community 374"
Cohesion: 1.0
Nodes (1): Creates and deploys a paranoid Meterpreter payload and listener with SSL/TLS pin

### Community 375 - "Community 375"
Cohesion: 1.0
Nodes (1): Exploits a potential Local File Inclusion (LFI) vulnerability by crafting

### Community 376 - "Community 376"
Cohesion: 1.0
Nodes (1): Executes the GreatSCT tool for generating payloads that bypass antivirus and app

### Community 377 - "Community 377"
Cohesion: 1.0
Nodes (1): Executes the SEToolKit workflow to generate a Meterpreter payload         and co

### Community 378 - "Community 378"
Cohesion: 1.0
Nodes (1): Uses the jwt_tool to analyze, tamper, or exploit JSON Web Tokens (JWTs).

### Community 379 - "Community 379"
Cohesion: 1.0
Nodes (1): Uses the darkarmour tool to generate an undetectable version of a PE executable.

### Community 380 - "Community 380"
Cohesion: 1.0
Nodes (1): Executes Osmedeus scans with guided input for various scanning scenarios.

### Community 381 - "Community 381"
Cohesion: 1.0
Nodes (1): Executes Metabigor commands for OSINT and scanning tasks with guided input or pr

### Community 382 - "Community 382"
Cohesion: 1.0
Nodes (1): Command to get ASN for a given IP address.

### Community 383 - "Community 383"
Cohesion: 1.0
Nodes (1): Executes Atomic Red Team tests based on user-selected platform and test.

### Community 384 - "Community 384"
Cohesion: 1.0
Nodes (1): Generates and synchronizes atomic agent scripts.          Parameters:         li

### Community 385 - "Community 385"
Cohesion: 1.0
Nodes (1): Executes a multi-step APT simulation plan based on Atomic Red Team test IDs.

### Community 386 - "Community 386"
Cohesion: 1.0
Nodes (1): List, validate, and run APT playbooks based on public threat reports.          U

### Community 387 - "Community 387"
Cohesion: 1.0
Nodes (1): Interacts with the MITRE ATT&CK framework using the STIX 2.0 format.          Th

### Community 388 - "Community 388"
Cohesion: 1.0
Nodes (1): Generates a playbook that integrates Atomic Red Team tests and MITRE ATT&CK tech

### Community 389 - "Community 389"
Cohesion: 1.0
Nodes (1): Generates a playbook from your custom technique database.         Usage: my_play

### Community 390 - "Community 390"
Cohesion: 1.0
Nodes (1): Executes a BBOT scan to perform various reconnaissance tasks.          This func

### Community 391 - "Community 391"
Cohesion: 1.0
Nodes (1): Executes Amass to perform a passive enumeration on a given domain.          This

### Community 392 - "Community 392"
Cohesion: 1.0
Nodes (1): Applies various filtering techniques to the given command line by modifying each

### Community 393 - "Community 393"
Cohesion: 1.0
Nodes (1): Exploits a target by injecting a malicious payload and collecting admin informat

### Community 394 - "Community 394"
Cohesion: 1.0
Nodes (1): Encode a given payload into UTF-16 escape sequences.          This function take

### Community 395 - "Community 395"
Cohesion: 1.0
Nodes (1): Executes the Impacket dcomexec tool to run commands on a remote system using DCO

### Community 396 - "Community 396"
Cohesion: 1.0
Nodes (1): Sets up a local pip repository to serve Python packages for installation on a co

### Community 397 - "Community 397"
Cohesion: 1.0
Nodes (1): Creates a comprehensive local APT repository with enhanced dependency resolution

### Community 398 - "Community 398"
Cohesion: 1.0
Nodes (1): Executes the httprobe tool to probe domains for working HTTP and HTTPS servers.

### Community 399 - "Community 399"
Cohesion: 1.0
Nodes (1): Automates EyeWitness installation and execution without requiring user input.

### Community 400 - "Community 400"
Cohesion: 1.0
Nodes (1): Processes HTML content from a specified URL using the pup utility and a default

### Community 401 - "Community 401"
Cohesion: 1.0
Nodes (1): Performs reconnaissance on a specified domain using crt.sh (the target must be v

### Community 402 - "Community 402"
Cohesion: 1.0
Nodes (1): Executes Dig Dug to inflate the size of an executable file, leveraging pre-confi

### Community 403 - "Community 403"
Cohesion: 1.0
Nodes (1): Performs a password spray attack on Azure Active Directory Seamless Single Sign-

### Community 404 - "Community 404"
Cohesion: 1.0
Nodes (1): Searches for default credentials associated with a specific product or vendor, u

### Community 405 - "Community 405"
Cohesion: 1.0
Nodes (1): Exploits OpenSSH vulnerability CVE-2023-38408 via the PKCS#11 feature of the ssh

### Community 406 - "Community 406"
Cohesion: 1.0
Nodes (1): Executes the `lazypyautogui.py` script with optional arguments.         This ope

### Community 407 - "Community 407"
Cohesion: 1.0
Nodes (1): Generates an Excel 4.0 (XLM) macro from a provided C# source file using EXCELntD

### Community 408 - "Community 408"
Cohesion: 1.0
Nodes (1): Executes the Spraykatz tool to retrieve credentials on Windows machines and larg

### Community 409 - "Community 409"
Cohesion: 1.0
Nodes (1): Installs and starts the Caldera server.          This function:             - Cl

### Community 410 - "Community 410"
Cohesion: 1.0
Nodes (1): Import CALDERA abilities into LazyOwn playbooks.          Usage:             cal

### Community 411 - "Community 411"
Cohesion: 1.0
Nodes (1): Export a LazyOwn playbook to CALDERA ability YAML.          Usage:             c

### Community 412 - "Community 412"
Cohesion: 1.0
Nodes (1): Synchronizes the system clock with a specified NTP server.          This method

### Community 413 - "Community 413"
Cohesion: 1.0
Nodes (1): Executes the Impacket ticketer tool to create a golden ticket.          This fun

### Community 414 - "Community 414"
Cohesion: 1.0
Nodes (1): Displays a list of useful links and allows the user to select and copy a link to

### Community 415 - "Community 415"
Cohesion: 1.0
Nodes (1): Synchronizes the local "sessions" directory to a remote host using rsync, levera

### Community 416 - "Community 416"
Cohesion: 1.0
Nodes (1): Executes the pre2k tool to query the domain for pre-Windows 2000 machine account

### Community 417 - "Community 417"
Cohesion: 1.0
Nodes (1): Executes the gMSADumper tool to read and parse gMSA password blobs accessible by

### Community 418 - "Community 418"
Cohesion: 1.0
Nodes (1): Executes the dploot tool to loot DPAPI related secrets from local or remote targ

### Community 419 - "Community 419"
Cohesion: 1.0
Nodes (1): Extract and display banners from XML files in the 'sessions' directory.

### Community 420 - "Community 420"
Cohesion: 1.0
Nodes (1): Generates an obfuscated payload to evade AV detection using the payloadGenerator

### Community 421 - "Community 421"
Cohesion: 1.0
Nodes (1): Converts a binary file to a shellcode string in C or Nim format.          This f

### Community 422 - "Community 422"
Cohesion: 1.0
Nodes (1): Show the Hacker News in the terminal.          Parameters:             line (str

### Community 423 - "Community 423"
Cohesion: 1.0
Nodes (1): Search the NVD for CVEs matching a service banner and persist findings.

### Community 424 - "Community 424"
Cohesion: 1.0
Nodes (1): Trasnform file .exe into binary file.          Args:             line (str): Rut

### Community 425 - "Community 425"
Cohesion: 1.0
Nodes (1): Trasnform file .exe into donut binary file.          Args:             line (str

### Community 426 - "Community 426"
Cohesion: 1.0
Nodes (1): Genera y ejecuta pruebas de Atomic Red Team usando el C2.          Parameters:

### Community 427 - "Community 427"
Cohesion: 1.0
Nodes (1): Sube un archivo al C2.          Parameters:         file_path (str): Ruta del ar

### Community 428 - "Community 428"
Cohesion: 1.0
Nodes (1): upload command in the client using the C2 to upload a file          Parameters:

### Community 429 - "Community 429"
Cohesion: 1.0
Nodes (1): Descarga un archivo desde el C2.          Parameters:         file_name (str): N

### Community 430 - "Community 430"
Cohesion: 1.0
Nodes (1): Download a file from the C2.          Parameters:         line (str): Command in

### Community 431 - "Community 431"
Cohesion: 1.0
Nodes (1): Ejecuta un comando en el cliente usando el C2.          Parameters:         comm

### Community 432 - "Community 432"
Cohesion: 1.0
Nodes (1): Exec command in the client using the C2. download: command you must put the file

### Community 433 - "Community 433"
Cohesion: 1.0
Nodes (1): Obfuscates a PowerShell script using various techniques.         by @JoelGMSec h

### Community 434 - "Community 434"
Cohesion: 1.0
Nodes (1): Executes the D3m0n1z3dShell tool for persistence in Linux.          This functio

### Community 435 - "Community 435"
Cohesion: 1.0
Nodes (1): Copies the local "sessions" directory to a remote host using scp, leveraging ssh

### Community 436 - "Community 436"
Cohesion: 1.0
Nodes (1): Configures the local machine with internet access to act as an APT proxy for a m

### Community 437 - "Community 437"
Cohesion: 1.0
Nodes (1): Configures the local machine with internet access to act as a pip proxy for a ma

### Community 438 - "Community 438"
Cohesion: 1.0
Nodes (1): Configures the local machine with internet access to act as a proxy for a machin

### Community 439 - "Community 439"
Cohesion: 1.0
Nodes (1): Checks for updates by comparing the local version with the remote version.

### Community 440 - "Community 440"
Cohesion: 1.0
Nodes (1): Executes wmiexec-pro with various options for WMI operations.          This func

### Community 441 - "Community 441"
Cohesion: 1.0
Nodes (1): Generates or updates a JSON file to be used as a database.          The JSON fil

### Community 442 - "Community 442"
Cohesion: 1.0
Nodes (1): Convert shellcode into an ELF file and infect it.          This function takes a

### Community 443 - "Community 443"
Cohesion: 1.0
Nodes (1): Perform Remote Execution Command trow ssh using grisun0 user, see help grisun0

### Community 444 - "Community 444"
Cohesion: 1.0
Nodes (1): Clone a website and serve the files in sessions/{url_cloned}.         Args:

### Community 445 - "Community 445"
Cohesion: 1.0
Nodes (1): Send special string to trigger a reverse shell, with the command 'c2 client_name

### Community 446 - "Community 446"
Cohesion: 1.0
Nodes (1): Configures and starts a listener for a specified victim.          This function

### Community 447 - "Community 447"
Cohesion: 1.0
Nodes (1): Configures and starts a listener for a specified victim.          This function

### Community 448 - "Community 448"
Cohesion: 1.0
Nodes (1): Retrieves detailed information about an IP address using the ARIN API.

### Community 449 - "Community 449"
Cohesion: 1.0
Nodes (1): Creates a systemd service file for a specified binary and generates a script to

### Community 450 - "Community 450"
Cohesion: 1.0
Nodes (1): Creates a systemd service file for a specified binary and generates a script to

### Community 451 - "Community 451"
Cohesion: 1.0
Nodes (1): Sends a magic packet to the Chinese malware.         The function extracts rhost

### Community 452 - "Community 452"
Cohesion: 1.0
Nodes (1): Download a file from the command and control (C2) server.          This function

### Community 453 - "Community 453"
Cohesion: 1.0
Nodes (1): Execute a command to interact with the GROQ API using the provided API key.

### Community 454 - "Community 454"
Cohesion: 1.0
Nodes (1): Display C and ASM code side by side in a curses-based interface.          This f

### Community 455 - "Community 455"
Cohesion: 1.0
Nodes (1): Executes the camphish tool for Grab cam shots from target's phone front camera o

### Community 456 - "Community 456"
Cohesion: 1.0
Nodes (1): Executes the hound tool for Hound is a simple and light tool for information gat

### Community 457 - "Community 457"
Cohesion: 1.0
Nodes (1): Obfuscates a shell script by encoding it in Base64 and prepares a command to dec

### Community 458 - "Community 458"
Cohesion: 1.0
Nodes (1): Load the session from the sessionLazyOwn.json file and display the status of var

### Community 459 - "Community 459"
Cohesion: 1.0
Nodes (1): Perform lateral movement by downloading and installing LazyOwn on a remote Linux

### Community 460 - "Community 460"
Cohesion: 1.0
Nodes (1): Executes the Commix tool for detecting and exploiting command injection vulnerab

### Community 461 - "Community 461"
Cohesion: 1.0
Nodes (1): Add a client to execute c2 commands          Parameters:             line (str):

### Community 462 - "Community 462"
Cohesion: 1.0
Nodes (1): LazyOwn RedTeam Adversary Emulator, you can configure your own adversaries in ad

### Community 463 - "Community 463"
Cohesion: 1.0
Nodes (1): Ofuscate a string into Go code.

### Community 464 - "Community 464"
Cohesion: 1.0
Nodes (1): Get list de supported acctions.

### Community 465 - "Community 465"
Cohesion: 1.0
Nodes (1): Convert a binary path to x64 little-endian hex code for shellcode injection.

### Community 466 - "Community 466"
Cohesion: 1.0
Nodes (1): Convert raw hex payload from msfvenom into NASM-compatible shellcode format.

### Community 467 - "Community 467"
Cohesion: 1.0
Nodes (1): Generates an offensive playbook using:         1. Nmap scan results (CSV)

### Community 468 - "Community 468"
Cohesion: 1.0
Nodes (1): Create a basic synthetic playbook from Nmap CSV when LLM fails.          Usage:

### Community 469 - "Community 469"
Cohesion: 1.0
Nodes (1): Extract YAML from an existing debug file and try to create a playbook.

### Community 470 - "Community 470"
Cohesion: 1.0
Nodes (1): Generates an MP4 video from PNG images found in the sessions/captured_images dir

### Community 471 - "Community 471"
Cohesion: 1.0
Nodes (1): Converts the Python REMCOMSVC byte string from remcomsvc.py to Golang byte slice

### Community 472 - "Community 472"
Cohesion: 1.0
Nodes (1): Processes CSV files with scan results and vulnerability data to generate a Shoda

### Community 473 - "Community 473"
Cohesion: 1.0
Nodes (1): Execute adversary from YAML in lazyadversaries/*.yaml         Syntax: adversary

### Community 474 - "Community 474"
Cohesion: 1.0
Nodes (1): Generate shellcode in C format using msfvenom for either a custom command or a r

### Community 475 - "Community 475"
Cohesion: 1.0
Nodes (1): Open a centered popup in the current tmux session to execute a shell command.

### Community 476 - "Community 476"
Cohesion: 1.0
Nodes (1): Add a new alias with support for placeholders like {rhost}, {lhost}, {lport}, et

### Community 477 - "Community 477"
Cohesion: 1.0
Nodes (1): List all available aliases.

### Community 478 - "Community 478"
Cohesion: 1.0
Nodes (1): Add a new custom command to the 'find' system, saved in user_commands.json.

### Community 479 - "Community 479"
Cohesion: 1.0
Nodes (1): Remove a custom command by index (as shown in 'find').          Only removes use

### Community 480 - "Community 480"
Cohesion: 1.0
Nodes (1): Encrypt with AES and random key to PE EXE file, to usage with loaders.

### Community 481 - "Community 481"
Cohesion: 1.0
Nodes (1): Enable or disable the IA assitant (use DeepSeek in local).

## Knowledge Gaps
- **1205 isolated node(s):** `Security services for the LazyOwn C2 web layer.  Services encapsulate stateful s`, `Manages the Flask secret key lifecycle.      Generates a cryptographically secur`, `Return an existing secret key or generate and persist a new one.          Return`, `Provides safe file read/write operations with path traversal protection.      Al`, `Resolve a relative path safely within the base directory.          Args:` (+1200 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 14`** (2 nodes): `Security constants and validation patterns for the LazyOwn C2 web layer.  All re`, `constants.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Generates an offensive playbook using:         1. Nmap scan results (CSV)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Return a non-streaming completion for ``prompt``.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `Yield streaming completion chunks for ``prompt``.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Command to trigger a toastr-like notification.         Usage: notify <type> <mes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Handle the end-of-file (EOF) condition.          This method is called when the`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Guided first-run setup wizard — configure rhost, lhost, domain, wordlists and mo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Print a single-line operator context: rhost, lhost, domain, phase, os, creds.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Show ELO score, karma rank and exploration progress for this operator.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Search across all previous command outputs and session logs.          Searches i`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Get or set the current kill-chain phase.          When called without arguments,`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Capture a quick operator note attached to the current target and phase.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Show a unified table of all captured credentials and hashes.          Reads ever`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Record a newly discovered pivot target or show the pivot chain.          When yo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `View and manage the task queue from sessions/tasks.json.          Tasks are crea`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `List nmap scan files in sessions/ with age, size, and open ports.          Witho`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Print a unified operational situation report.          Aggregates in one view: t`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `assign a parameter value, persist to payload.json and refresh aliases.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Show the current parameter values, sorted and aligned.          Rendering is del`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Browse the operator command catalogue grouped by kill-chain phase.          The`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Fuzzy search the graphify knowledge graph for nodes by label.          Usage: ```
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Show graph neighbors of a node or command from the graphify graph.          Usag`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Show the most-connected nodes ("god nodes") from the graph.          Usage: ``go`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `Suggest next commands by walking the graph from recent activity.          Usage:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Recommend the next command using policy engine + graph advisor.          Runs tw`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `Show exploration coverage and addon/tool suggestions per service.          Reads`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `Launch the full-screen LazyOwn operator dashboard (Textual TUI).          Opens`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `Print the multi-operator collaboration join URL and SSE endpoint.          Outpu`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Drive a single target through the full kill-chain in one command.          Usage`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `Declarative composition layer: run a YAML pipeline of LazyOwn commands.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `Lists all available scripts in the modules directory.          This method print`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `Runs a specific LazyOwn script.          This method executes a script from the`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `Runs the internal module `modules/lazysearch.py`.          This method executes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `Run the internal module located at `modules/LazyOwnExplorer.py`.          This m`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `Run the internal module located at `modules/lazyown.py`.          This method ex`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `Run the internal module located at `modules/update_db.sh`.          This method`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `Run the internal module located at `modules/lazywerkzeug.py` in debug mode.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `Run the internal module located at `modules/lazygat.sh`. to gathering the sistem`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (1 nodes): `Runs the internal module `modules/lazynmap.sh` with discovery mode.          Thi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `Runs the internal module `modules/lazynmap.sh` with target mode.          OS det`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `Run the sniffer internal module located at `modules/lazysniff.py` with the speci`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (1 nodes): `Run the sniffer ftp internal module located at `modules/lazyftpsniff.py` with th`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (1 nodes): `Run the internal module to search netbios vuln victims, located at `modules/lazy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (1 nodes): `Run the internal module located at `modules/lazyhoneypot.py` with the specified`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (1 nodes): `Run the internal module to create Oneliners with Groq AI located at `modules/laz`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (1 nodes): `Load parameters from a specified payload JSON file.          This function loads`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `Exit the command line interface.          This function prompts the user to conf`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `Fix permissions for LazyOwn shell scripts.          This function adjusts the fi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `Run LazyOwn webshell server.          This function starts a web server that ser`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `Retrieve and display file capabilities on the system.          This function use`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `Get the SecLists wordlist from GitHub.          This function downloads and extr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (1 nodes): `Interacts with SMB shares using the `smbclient` command to perform the following`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `Interacts with SMB shares using the `smbclient` command to perform the following`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `Interacts with SMB shares using the `smbclient.py` command to perform the follow`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (1 nodes): `smbmap -H 10.10.10.3 [OPTIONS]         Uses the `smbmap` tool to interact with S`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `sudo impacket-GetNPUsers mist.htb/ -no-pass -usersfile sessions/users.txt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `Executes the Impacket PSExec tool to attempt remote execution on the specified t`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `Executes the Impacket PSExec tool to attempt remote execution on the specified t`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `Executes the `rpcdump.py` script to dump RPC services from a target host.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `Executes the `dig` command to query DNS information.          1. Retrieves the D`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `Copies a file from the ExploitDB directory to the sessions directory.          1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `Performs DNS enumeration using `dnsenum` to identify subdomains for a given doma`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `Performs DNS enumeration using `dnsmap` to discover subdomains for a specified d`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `Performs a web technology fingerprinting scan using `whatweb`.          1. Execu`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `Performs enumeration of information from a target Linux/Unix system using `enum4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `Performs network scanning using `nbtscan` to discover NetBIOS names and addresse`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Executes the `rpcclient` command to interact with a remote Windows system over R`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (1 nodes): `Runs the `nikto` tool to perform a web server vulnerability scan against the spe`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (1 nodes): `Runs the `finalrecon` tool to perform a web server vulnerability scan against th`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `Uses `openssl s_client` to connect to a specified host and port, allowing for te`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 86`** (1 nodes): `Search all exploit sources and map findings to the next LazyOwn command.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 87`** (1 nodes): `Uses `wfuzz` to perform fuzzing based on provided parameters. This function supp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 88`** (1 nodes): `Searches for packages on Launchpad based on the provided search term and extract`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `Uses `gobuster` for directory and virtual host fuzzing based on provided paramet`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 90`** (1 nodes): `Adds an entry to the `/etc/hosts` file, mapping an IP address to a domain name.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (1 nodes): `Execute CrackMapExec (CME) for SMB enumeration and authentication attempts again`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `Dumps LDAP information using `ldapdomaindump` with credentials from a file.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `Perform LDAP enumeration using bloodhound-python with credentials from a file.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (1 nodes): `Perform a ping to check host availability and infer the operating system based o`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (1 nodes): `Try gospider for web spidering.          This function executes the `gospider` t`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (1 nodes): `Executes an ARP scan using `arp-scan`.          This function performs an ARP sc`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (1 nodes): `Executes the LazyPwn script.          This function runs the `lazypwn.py` script`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 98`** (1 nodes): `Fixes file permissions and line endings in the project directories.          Thi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (1 nodes): `Sets up an SMB server using Impacket and creates an SCF file for SMB share acces`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 100`** (1 nodes): `Uses sqlmap to perform SQL injection testing on a given URL or request file (you`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 101`** (1 nodes): `Runs a small proxy server to modify HTTP requests on the fly.          This func`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (1 nodes): `Creates a web shell disguised as a `.jpg` file in the `sessions` directory.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (1 nodes): `Creates a bash reverse shell script in the `sessions` directory with the specifi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 104`** (1 nodes): `Creates a PowerShell reverse shell script in the `sessions` directory with the s`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (1 nodes): `Creates a `hash.txt` file in the `sessions` directory with the specified hash va`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 106`** (1 nodes): `Creates a `credentials.txt` file in the `sessions` directory with the specified`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (1 nodes): `Creates a `cookie.txt` file in the `sessions` directory with the specified cooki`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (1 nodes): `Downloads resources into the `sessions` directory.          This function perfor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 109`** (1 nodes): `Downloads and sets up exploits in the `external/.exploits/` directory and starts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 110`** (1 nodes): `Runs the `dirsearch` tool to perform directory and file enumeration on a specifi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 111`** (1 nodes): `Runs John the Ripper with a specified wordlist and options.          This functi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 112`** (1 nodes): `Runs Hashcat with specified attack mode and hash type using a wordlist.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 113`** (1 nodes): `Runs Responder on a specified network interface with elevated privileges.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 114`** (1 nodes): `Displays IP addresses of network interfaces and copies the IP address from the ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 115`** (1 nodes): `Displays IP addresses of network interfaces and prints the IP address from the ``
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 116`** (1 nodes): `Copies the remote host (rhost) to the clipboard and updates the command prompt.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 117`** (1 nodes): `Updates the command prompt to include the remote host (rhost) and current workin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 118`** (1 nodes): `Open a Powerlevel10k-style wizard to toggle prompt segments.          Arrow keys`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 119`** (1 nodes): `Copies a Python reverse shell command to the clipboard.          This function g`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 120`** (1 nodes): `Copies a reverse shell payload to the clipboard.          This function generate`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 121`** (1 nodes): `Copies a malicious image tag payload to the clipboard.          This function cr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 122`** (1 nodes): `Creates a Visual Basic Script (VBS) to attempt to disable antivirus settings.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 123`** (1 nodes): `Downloads ConPtyShell and prepares a PowerShell command for remote access.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 124`** (1 nodes): `Runs `pwncat-cs` with the specified port for listening.          This function s`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 125`** (1 nodes): `Runs `pwncat` with the specified port for listening. SELFINJECT          This fu`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 126`** (1 nodes): `Automates command execution based on a list of aliases and commands.          1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 127`** (1 nodes): `Executes a shell command directly from the LazyOwn interface.          This func`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 128`** (1 nodes): `Executes a shell command directly from the LazyOwn interface.          This func`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 129`** (1 nodes): `Displays the current working directory and lists files, and copies the current d`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 130`** (1 nodes): `Exits the application quickly without confirmation.          This function perfo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 131`** (1 nodes): `Configures the system to ignore ARP requests by setting a kernel parameter.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 132`** (1 nodes): `Configures the system to ignore ICMP echo requests by setting a kernel parameter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 133`** (1 nodes): `Configures the system to acknowledge ARP requests by setting a kernel parameter.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 134`** (1 nodes): `Configures the system to respond to ICMP echo requests by setting a kernel param`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 135`** (1 nodes): `Displays the current date and time, and runs a custom shell script.          Thi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 136`** (1 nodes): `Lists all open TCP and UDP ports on the local system.          This function per`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 137`** (1 nodes): `Connects to an SSH host using credentials from a file and a specified port.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 138`** (1 nodes): `Connects to an ftp host using credentials from a file and a specified port.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 139`** (1 nodes): `Generates a command to display TCP and UDP ports and copies it to the clipboard.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 140`** (1 nodes): `Connect to a VPN by selecting from available .ovpn files.          This function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 141`** (1 nodes): `Create an SSH private key file and connect to a remote host using SSH.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 142`** (1 nodes): `Start a web server using Python 3 and display relevant network information.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 143`** (1 nodes): `Copy payloads to clipboard for Local File Inclusion (LFI) attacks.          This`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 144`** (1 nodes): `Sends an email using `swaks` (Swiss Army Knife for SMTP).          This method c`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 145`** (1 nodes): `Run `impacket-samrdump` to dump SAM data from specified ports.          This fun`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 146`** (1 nodes): `Encode a string for URL.          This function takes a string as input, encodes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 147`** (1 nodes): `Decode a URL-encoded string.          This function takes a URL-encoded string a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 148`** (1 nodes): `Performs a Lynis audit on the specified remote system.          This function ex`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 149`** (1 nodes): `Performs an SNMP check on the specified target host.          This function exec`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 150`** (1 nodes): `Performs an SNMP check on the specified target host.          This function exec`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 151`** (1 nodes): `Encodes a string using the specified shift value and substitution key.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 152`** (1 nodes): `Decode a string using the specified shift value and substitution key.          T`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 153`** (1 nodes): `Display the credentials stored in the `credentials.txt` file and copy the passwo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 154`** (1 nodes): `Discover active hosts in a subnet by performing a ping sweep.          This meth`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 155`** (1 nodes): `Scan all ports on a specified host to identify open ports.          This method`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 156`** (1 nodes): `Scan all ports on a specified host to identify open ports and associated service`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 157`** (1 nodes): `Apply a ROT (rotation) substitution cipher to the given string.          This fu`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 158`** (1 nodes): `Apply a ROT (rotation) substitution cipher to the given extension.          This`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 159`** (1 nodes): `Uses Hydra to perform a brute force attack on a specified HTTP service with a us`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 160`** (1 nodes): `Uses medusa to perform a brute force attack on a specified ssh service with a us`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 161`** (1 nodes): `Perform an Nmap scan using a specified script and port.          :param line: A`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 162`** (1 nodes): `Applies various obfuscations to a given command line string to create multiple o`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 163`** (1 nodes): `Enumerates SMTP users using the `smtp-user-enum` tool with the VRFY method.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 164`** (1 nodes): `Starts the SSH service and displays its status.          1. Executes the command`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 165`** (1 nodes): `Provides help to find and display information about Nmap scripts.          1. Ch`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 166`** (1 nodes): `Search for commands matching the given parameter in the cmd interface and option`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 167`** (1 nodes): `Helps to find hash types in Hashcat by searching through its help output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (1 nodes): `Deletes files and directories in the `sessions` directory, excluding specified f`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 169`** (1 nodes): `Automates the execution of pwntomate tools on XML configuration files.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 170`** (1 nodes): `Prints all configured aliases and their associated commands.          1. Retriev`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 171`** (1 nodes): `Starts `tcpdump` to capture ICMP traffic on the specified interface.          1.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 172`** (1 nodes): `Starts packet capture using `tcpdump` on the specified interface.          1. Ch`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 173`** (1 nodes): `Analyzes a packet capture file using `tshark` based on the provided remote host`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 174`** (1 nodes): `Reads credentials from a file, encrypts the password, and executes the RDP conne`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 175`** (1 nodes): `Encodes a given string into Base64 format.          1. Encodes the input string:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 176`** (1 nodes): `Decodes a Base64 encoded string.          1. Decodes the Base64 string:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 177`** (1 nodes): `Creates and copies a shell command to add a new user `grisun0`, assign a passwor`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 178`** (1 nodes): `Creates and copies a PowerShell command to add a new user `grisun0`, assign a pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 179`** (1 nodes): `Encodes a given payload into a Base64 encoded string suitable for Windows PowerS`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 180`** (1 nodes): `Creates a base64 encoded payload specifically for Windows to execute a PowerShel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 181`** (1 nodes): `Creates a base64 encoded PowerShell reverse shell payload specifically for Windo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 182`** (1 nodes): `Creates a base64 encoded ASP reverse shell payload and copies it to the clipboar`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 183`** (1 nodes): `Copies a command to the clipboard for downloading and running Rubeus.          1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 184`** (1 nodes): `Sets up and runs a `socat` tunnel with SOCKS4A proxy support.          1. If no`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 185`** (1 nodes): `Automates the setup and execution of Chisel server and client for tunneling and`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 186`** (1 nodes): `Automates various Metasploit tasks including scanning for vulnerabilities, setti`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 187`** (1 nodes): `Encrypts a file using XOR encryption.          1. Splits the provided `line` int`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 188`** (1 nodes): `Decrypts a file using XOR encryption.          1. Splits the provided `line` int`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 189`** (1 nodes): `Ejecuta un comando para listar las conexiones SSH activas.          Este método`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 190`** (1 nodes): `Attach strace to a running process and log output to a file.          This funct`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 191`** (1 nodes): `Executes commands defined in a lazyscript file.          This function reads a s`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 192`** (1 nodes): `Relanza la aplicación actual utilizando `proxychains` para enrutar el tráfico`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 193`** (1 nodes): `Generates a Python one-liner to execute shellcode from a given URL.          Thi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 194`** (1 nodes): `This function executes the web security scanning tool Skipfish         using the`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 195`** (1 nodes): `Create a Windows DLL file using MinGW-w64 or a Blazor DLL for Linux.          Th`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 196`** (1 nodes): `Performs a web seo fingerprinting scan using `lazyseo.py`.          1. Executes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 197`** (1 nodes): `Execute the PadBuster command for padding oracle attacks.          This function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 198`** (1 nodes): `Scans for hosts with SMB service open on port 445 in the specified target networ`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 199`** (1 nodes): `Automates the exploitation of the Cacti version 1.2.26 vulnerability         usi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 200`** (1 nodes): `Handles the creation of temporary files for users and passwords based on a small`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 201`** (1 nodes): `Set up and run ngrok on a specified local port. If ngrok is not installed, it wi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 202`** (1 nodes): `This function generates a PowerShell script that retrieves saved Wi-Fi passwords`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 203`** (1 nodes): `Executes a Shellshock attack against a target.          This function constructs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 204`** (1 nodes): `This function generates a PowerShell script that retrieves reverse shell over ht`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 205`** (1 nodes): `Interactive Morse Code Converter.          This function serves as an interface`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 206`** (1 nodes): `Fetch URLs from the Wayback Machine for a given website.         The URL is take`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 207`** (1 nodes): `Manage C2 listeners: list, add, start, stop, remove.          Usage:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 208`** (1 nodes): `Toggle or query Docker sandbox mode.          When ``sandboxed`` is ``true`` in`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 209`** (1 nodes): `Handles the process of sending a spoofed ARP packet to a specified IP address wi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 210`** (1 nodes): `Asks the user for the URL, database, table, and columns, and then executes the P`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 211`** (1 nodes): `Generates an SSH key pair with RSA 4096-bit encryption. If no name is provided,`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 212`** (1 nodes): `Generate a custom dictionary using the `crunch` tool.          This function cre`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 213`** (1 nodes): `Fetches and displays malware information from the MalwareBazaar API based on the`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (1 nodes): `Download a malware sample from MalwareBazaar using its SHA256 hash.          Thi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 215`** (1 nodes): `Run an SSL scan on the specified remote host.          This function initiates a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 216`** (1 nodes): `This function constructs and executes a command for the 'cewl' tool.         It`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (1 nodes): `This function constructs and executes a command for the 'dmitry' tool.         I`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 218`** (1 nodes): `Executes the graudit command to perform a static code analysis with the specifie`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (1 nodes): `Connects to the msfrpcd daemon and allows remote control of Metasploit.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 220`** (1 nodes): `Executes a Nuclei scan on a specified target URL or host.          Usage:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 221`** (1 nodes): `Executes a parsero scan on a specified target URL or host.          Usage:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (1 nodes): `Executes the Sherlock tool to find usernames across social networks.          Th`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (1 nodes): `Executes trufflehog to search for secrets in a given Git repository URL.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 224`** (1 nodes): `Generate a PHP backdoor using Weevely, protected with the given password.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (1 nodes): `Connect to PHP backdoor using Weevely, protected with the given password.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (1 nodes): `Executes a changeme scan on a specified target URL or host.          Usage:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 227`** (1 nodes): `Performs enumeration of information from a target system using `enum4linux-ng`.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 228`** (1 nodes): `Executes a web server fuzzing script with user-provided parameters.          Thi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (1 nodes): `Executes a payload creation framework for the retrieval and execution of arbitra`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 230`** (1 nodes): `Starts the Sliver server and generates a client configuration file for connectin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 231`** (1 nodes): `Generates a certificate authority (CA), client certificate, and client key.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (1 nodes): `Executes the Kerbrute tool to enumerate user accounts against a specified target`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 233`** (1 nodes): `Execute the dacledit.py command for a specific user or all users listed in the u`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 234`** (1 nodes): `Execute the bloodyAD.py command for a specific user or all users listed in the u`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (1 nodes): `Execute the Evil-WinRM tool for authentication attempts on a specified target us`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (1 nodes): `Requests a Ticket Granting Ticket (TGT) using the Impacket tool with provided cr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (1 nodes): `Performs enumeration of users from a target system using `apache-users`.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (1 nodes): `Creates a backdoored executable using `backdoor-factory`.          This function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 239`** (1 nodes): `Tests WebDAV server configurations using `davtest`.          This function check`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 240`** (1 nodes): `Generates payloads using MSFvenom Payload Creator (MSFPC).          This functio`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 241`** (1 nodes): `Generates payloads using Ivy with various options. Ivy is a payload creation fra`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 242`** (1 nodes): `Execute the tor.sh script with the specified port or default to port 80 if no po`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (1 nodes): `Generates a wordlist based on a target name and a list of characters, with vario`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 244`** (1 nodes): `Traces the DNS information for a given domain using the FreeDNS service. (using`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (1 nodes): `Generates payloads using Veil-Evasion with various options. Veil-Evasion is a pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 246`** (1 nodes): `Generates payloads using PowerShell Empire with various options.          :param`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (1 nodes): `Runs evil-ssdp with various options and user-selected templates.          :param`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 248`** (1 nodes): `Runs Shellfire with various options and allows generating payloads.          :pa`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 249`** (1 nodes): `Generates a graph from JSON payload files containing URL, RHOST, and RPORT.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (1 nodes): `Executes netexec with various options for network protocol operations.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 251`** (1 nodes): `Executes ScareCrow with various options for bypassing EDR solutions and executin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 252`** (1 nodes): `Generate email permutations based on a full name and domain, then save them to a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (1 nodes): `Executes EyeWitness to capture screenshots from a list of URLs.         You need`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 254`** (1 nodes): `Run secretsdump.py with the provided domain, username, password, and IP address.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 255`** (1 nodes): `Run GetUserSPNs.py with the provided domain, username, password, and IP address.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (1 nodes): `Perform password spraying using crackmapexec with the provided parameters.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (1 nodes): `Perform port scanning using vscan with the provided parameters.          :param`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (1 nodes): `Attempt to exploit the Shellshock vulnerability (CVE-2014-6271, CVE-2014-7169).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 259`** (1 nodes): `Generate a reverse shell in various programming languages.          This functio`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 260`** (1 nodes): `Executes the 'alterx' command for subdomain enumeration on the provided domain.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (1 nodes): `Execute the AlliN.py tool with various scan modes and parameters.          This`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (1 nodes): `Execute the Dr0p1t tool to create a stealthy malware dropper.          This func`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (1 nodes): `Install and execute the git-dumper tool to download Git repository content.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (1 nodes): `Generate and execute a PowerShell command stager to run a .ps1 script.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 265`** (1 nodes): `Search the shell-storm API for shellcodes using the provided keywords.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 266`** (1 nodes): `Automates the setup and execution of Ligolo server and client for tunneling and`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 267`** (1 nodes): `Opens or creates the users.txt file in the sessions directory for editing using`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 268`** (1 nodes): `Execute the windapsearch tool to perform Active Directory Domain enumeration thr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (1 nodes): `Decrypts TightVNC passwords using Metasploit.          This function demonstrate`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 270`** (1 nodes): `Execute the Shadowsocks tool to create a secure tunnel for network traffic.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 271`** (1 nodes): `Extracts usernames from a JSON output generated by go-windapsearch and appends t`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 272`** (1 nodes): `Generate a downloader command for files in the sessions directory.          This`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 273`** (1 nodes): `Executes an LDAP search against a target remote host (rhost) and saves the resul`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (1 nodes): `Automates the EternalBlue (MS17-010) exploitation process using Metasploit.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 275`** (1 nodes): `Search for a CVE using the CIRCL API.          This function sends a GET request`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 276`** (1 nodes): `Compresses the 'sessions' folder and encodes it into a video using the lazyown_i`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (1 nodes): `HttpFileServer version 2.3. Vulnerable using the module rejetto_hfs_exec of meta`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 278`** (1 nodes): `SMB CVE-2008-4250. Vulnerable using the module ms08_067_netapi of metasploit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 279`** (1 nodes): `Try to check if Vulnerable using the module passed by argument of lazyown exampl`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 280`** (1 nodes): `(CVE-2017-7269). Vulnerable using the module iis_webdav_upload_asp of metasploit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (1 nodes): `Opens or creates the file using line in the sessions directory for editing using`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 282`** (1 nodes): `Runs `nc` with the specified port for listening.          This function starts a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 283`** (1 nodes): `Runs `nc` with rlwrap  the specified port for listening.          This function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 284`** (1 nodes): `Create a new JSON payload file based on the template provided in payload.json.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 285`** (1 nodes): `Executes the XSS (Cross-Site Scripting) vulnerability testing procedure`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 286`** (1 nodes): `Executes an Arjun scan on the specified URL for parameter discovery.          Th`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 287`** (1 nodes): `Transforms the input string based on user-defined casing style.          This co`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 288`** (1 nodes): `duckyspark Compiles and uploads an .ino sketch to a Digispark device using Ardui`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 289`** (1 nodes): `Generate usernames using the username-anarchy tool based on user input.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 290`** (1 nodes): `Command emp3r0r Downloads and sets up the Emperor server for local exploitation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 291`** (1 nodes): `Handles the creation and serialization of a template helper.          This funct`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 292`** (1 nodes): `Command gospherus: Clones and uses the Gopherus tool to generate gopher payloads`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 293`** (1 nodes): `Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 294`** (1 nodes): `Create multiple JSON payload files based on a CSV input file from HackerOne.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 295`** (1 nodes): `List all .kdbx files in the 'sessions' directory, let the user select one, and r`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 296`** (1 nodes): `Open a .kdbx file and print the titles and contents of all entries. The password`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 297`** (1 nodes): `Attempts to connect to an MSSQL server using the mssqlclient.py tool with Window`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 298`** (1 nodes): `Executes the GetADUsers.py script to retrieve Active Directory users.          T`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 299`** (1 nodes): `Crack a Cisco Type 7 password hash and display the plaintext.          This comm`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 300`** (1 nodes): `Command loxs: Installs and runs Loxs for multi-vulnerability web application sca`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 301`** (1 nodes): `Command blazy: Installs and runs blazy for multi-vulnerability web application s`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 302`** (1 nodes): `Command parth: Installs and runs Parth for discovering vulnerable URLs and param`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 303`** (1 nodes): `Command breacher: Installs and runs Breacher for finding admin login pages and E`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 304`** (1 nodes): `Command xsstrike: Installs and runs XSStrike for finding XSS vulnerabilities.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 305`** (1 nodes): `Command penelope: Installs and runs Penelope for handling reverse and bind shell`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 306`** (1 nodes): `Open a new window within a tmux session using the LazyOwn RedTeam Framework.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 307`** (1 nodes): `Open a new window within a tmux session using the LazyOwn RedTeam Framework.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 308`** (1 nodes): `Command adgetpass: Generates a PowerShell script to extract credentials from Azu`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 309`** (1 nodes): `Command openredirex: Clones, installs, and runs OpenRedirex for testing open red`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 310`** (1 nodes): `Command feroxbuster: Installs and runs Feroxbuster for performing forced browsin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 311`** (1 nodes): `Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target O`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 312`** (1 nodes): `Command sireprat: Automates the setup and usage of SirepRAT to perform various a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 313`** (1 nodes): `Generates hosts.txt, urls.txt, domains.txt, and targets.txt from multiple JSON p`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 314`** (1 nodes): `Converts shellcode to SYLK format and saves the result to a file.          This`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 315`** (1 nodes): `Command magicrecon: Automates the setup and usage of MagicRecon to perform vario`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 316`** (1 nodes): `Command cubespraying: Automates the installation and usage of CubeSpraying for p`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 317`** (1 nodes): `Run samdump2 with the SAM and SYSTEM file          :param line: This parameter i`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 318`** (1 nodes): `Command stormbreaker: Automates the installation and usage of Storm-Breaker for`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 319`** (1 nodes): `Command upload_bypass: Automates the installation and execution of Upload_Bypass`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 320`** (1 nodes): `Converts hexadecimal data from a file to plain text.          Opens a text edito`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 321`** (1 nodes): `Command rpcmap_py: Executes rpcmap.py commands to enumerate MSRPC interfaces.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 322`** (1 nodes): `Command serveralive2: Uses Impacket to connect to a remote MSRPC interface and r`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 323`** (1 nodes): `List all .zip files in the 'sessions' directory, let the user select one, and ru`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 324`** (1 nodes): `Command createusers_and_hashs: Extracts usernames and hashes from a dump file.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 325`** (1 nodes): `Command pykerbrute: Automates the installation and execution of PyKerbrute for b`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 326`** (1 nodes): `Run reg.py with specified parameters to query the registry.          :param line`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 327`** (1 nodes): `Identify hash type using nth after retrieving it with get_hash().          :para`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 328`** (1 nodes): `Generate a list of possible passwords by filling each asterisk in the input with`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 329`** (1 nodes): `Checks if the script is running with superuser (sudo) privileges, and if not,`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 330`** (1 nodes): `Serve linpeas.sh via HTTP and print the one-liner to run on the target.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 331`** (1 nodes): `Serve winPEAS via HTTP and print the one-liner to run on the target.          Lo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 332`** (1 nodes): `Run Linux Exploit Suggester against the current target's kernel info.          R`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 333`** (1 nodes): `Print SUID/SGID enumeration commands for the current target OS.          Outputs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 334`** (1 nodes): `Serve pspy (process spy without root) via HTTP for the target to download.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 335`** (1 nodes): `Look up a binary in GTFOBins / LOLBas and show exploitation techniques.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 336`** (1 nodes): `Ask the AI a question with current session context pre-loaded.          Injects`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 337`** (1 nodes): `Executes the Impacket netview tool to list network shares on a specified target.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 338`** (1 nodes): `Executes the Impacket WMIExec tool to run commands on a target system using WMI.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 339`** (1 nodes): `Extracts open ports and IP address information from a specified file.          T`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 340`** (1 nodes): `Schedules a command to run at a specified time.          This function allows us`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 341`** (1 nodes): `Executes the PEzor tool to pack executables or shellcode with custom configurati`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 342`** (1 nodes): `Executes the Impacket Mimikatz tool to interact with a target system for credent`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 343`** (1 nodes): `Executes the RDP check tool to verify credentials or hash-based authentication o`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 344`** (1 nodes): `Executes the MQTT check tool to verify credentials on a target system with optio`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 345`** (1 nodes): `Executes the LookupSID tool to perform SID enumeration on a target system.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 346`** (1 nodes): `Executes the Scavenger tool for multi-threaded post-exploitation scanning on tar`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 347`** (1 nodes): `Performs various checks on a selected binary to gather information and protectio`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 348`** (1 nodes): `Executes the Impacket lookupsid tool to enumerate SIDs on a target system.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 349`** (1 nodes): `Executes the Certipy tool to interact with Active Directory Certificate Services`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 350`** (1 nodes): `Executes the MSDT Follina exploit tool to create malicious documents for exploit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 351`** (1 nodes): `Executes the Swaks (Swiss Army Knife for SMTP) tool to send test emails for phis`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 352`** (1 nodes): `Executes ad-ldap-enum to enumerate Active Directory objects (users, groups, comp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 353`** (1 nodes): `Unzips a specified file from the sessions directory.          This function atte`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 354`** (1 nodes): `Executes the reGeorg tool for HTTP(s) tunneling through a SOCKS proxy.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 355`** (1 nodes): `Reduces a wordlist based on the specified password length.          This functio`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 356`** (1 nodes): `Executes the pyWhisker tool for manipulating the msDS-KeyCredentialLink attribut`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 357`** (1 nodes): `Executes the Impacket owneredit tool for manipulating ownership of Active Direct`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 358`** (1 nodes): `Executes the net rpc group addmem command to add a user to a specified group in`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 359`** (1 nodes): `Executes the Pass-the-Hash (PTH) Net tool to change the password of an Active Di`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 360`** (1 nodes): `Executes the gettgtpkinit.py tool from PKINITtools to request a TGT using Kerber`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 361`** (1 nodes): `Executes the getnthash.py tool from PKINITtools to retrieve the NT hash using a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 362`** (1 nodes): `Executes the gets4uticket.py tool from PKINITtools to request an S4U2Self servic`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 363`** (1 nodes): `Executes the aclpwn.py tool to find and exploit ACL paths for privilege escalati`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 364`** (1 nodes): `Executes the addspn.py tool to manage Service Principal Names (SPNs) on Active D`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 365`** (1 nodes): `Executes the dnstool.py tool to modify Active Directory-integrated DNS records.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 366`** (1 nodes): `Executes the printerbug.py tool to trigger the SpoolService bug via RPC backconn`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 367`** (1 nodes): `Executes the krbrelayx.py tool for Kerberos relaying or unconstrained delegation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 368`** (1 nodes): `Executes the autobloody tool for automating Active Directory privilege escalatio`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 369`** (1 nodes): `Uploads a file to Gofile storage.          This function performs the following`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 370`** (1 nodes): `We open a Netcat listener on port 443 and attempt to exploit NodeJS deserializat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 371`** (1 nodes): `Initiates a reverse MSSQL shell by starting an HTTP server to handle incoming co`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 372`** (1 nodes): `Executes the targetedKerberoast tool for extracting Kerberos service tickets.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 373`** (1 nodes): `Executes the pyOracle2 tool for performing padding oracle attacks.          This`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 374`** (1 nodes): `Creates and deploys a paranoid Meterpreter payload and listener with SSL/TLS pin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 375`** (1 nodes): `Exploits a potential Local File Inclusion (LFI) vulnerability by crafting`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 376`** (1 nodes): `Executes the GreatSCT tool for generating payloads that bypass antivirus and app`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 377`** (1 nodes): `Executes the SEToolKit workflow to generate a Meterpreter payload         and co`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 378`** (1 nodes): `Uses the jwt_tool to analyze, tamper, or exploit JSON Web Tokens (JWTs).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 379`** (1 nodes): `Uses the darkarmour tool to generate an undetectable version of a PE executable.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 380`** (1 nodes): `Executes Osmedeus scans with guided input for various scanning scenarios.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 381`** (1 nodes): `Executes Metabigor commands for OSINT and scanning tasks with guided input or pr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 382`** (1 nodes): `Command to get ASN for a given IP address.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 383`** (1 nodes): `Executes Atomic Red Team tests based on user-selected platform and test.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 384`** (1 nodes): `Generates and synchronizes atomic agent scripts.          Parameters:         li`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 385`** (1 nodes): `Executes a multi-step APT simulation plan based on Atomic Red Team test IDs.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 386`** (1 nodes): `List, validate, and run APT playbooks based on public threat reports.          U`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 387`** (1 nodes): `Interacts with the MITRE ATT&CK framework using the STIX 2.0 format.          Th`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 388`** (1 nodes): `Generates a playbook that integrates Atomic Red Team tests and MITRE ATT&CK tech`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 389`** (1 nodes): `Generates a playbook from your custom technique database.         Usage: my_play`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 390`** (1 nodes): `Executes a BBOT scan to perform various reconnaissance tasks.          This func`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 391`** (1 nodes): `Executes Amass to perform a passive enumeration on a given domain.          This`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 392`** (1 nodes): `Applies various filtering techniques to the given command line by modifying each`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 393`** (1 nodes): `Exploits a target by injecting a malicious payload and collecting admin informat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 394`** (1 nodes): `Encode a given payload into UTF-16 escape sequences.          This function take`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 395`** (1 nodes): `Executes the Impacket dcomexec tool to run commands on a remote system using DCO`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 396`** (1 nodes): `Sets up a local pip repository to serve Python packages for installation on a co`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 397`** (1 nodes): `Creates a comprehensive local APT repository with enhanced dependency resolution`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 398`** (1 nodes): `Executes the httprobe tool to probe domains for working HTTP and HTTPS servers.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 399`** (1 nodes): `Automates EyeWitness installation and execution without requiring user input.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 400`** (1 nodes): `Processes HTML content from a specified URL using the pup utility and a default`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 401`** (1 nodes): `Performs reconnaissance on a specified domain using crt.sh (the target must be v`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 402`** (1 nodes): `Executes Dig Dug to inflate the size of an executable file, leveraging pre-confi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 403`** (1 nodes): `Performs a password spray attack on Azure Active Directory Seamless Single Sign-`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 404`** (1 nodes): `Searches for default credentials associated with a specific product or vendor, u`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 405`** (1 nodes): `Exploits OpenSSH vulnerability CVE-2023-38408 via the PKCS#11 feature of the ssh`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 406`** (1 nodes): `Executes the `lazypyautogui.py` script with optional arguments.         This ope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 407`** (1 nodes): `Generates an Excel 4.0 (XLM) macro from a provided C# source file using EXCELntD`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 408`** (1 nodes): `Executes the Spraykatz tool to retrieve credentials on Windows machines and larg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 409`** (1 nodes): `Installs and starts the Caldera server.          This function:             - Cl`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 410`** (1 nodes): `Import CALDERA abilities into LazyOwn playbooks.          Usage:             cal`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 411`** (1 nodes): `Export a LazyOwn playbook to CALDERA ability YAML.          Usage:             c`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 412`** (1 nodes): `Synchronizes the system clock with a specified NTP server.          This method`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 413`** (1 nodes): `Executes the Impacket ticketer tool to create a golden ticket.          This fun`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 414`** (1 nodes): `Displays a list of useful links and allows the user to select and copy a link to`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 415`** (1 nodes): `Synchronizes the local "sessions" directory to a remote host using rsync, levera`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 416`** (1 nodes): `Executes the pre2k tool to query the domain for pre-Windows 2000 machine account`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 417`** (1 nodes): `Executes the gMSADumper tool to read and parse gMSA password blobs accessible by`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 418`** (1 nodes): `Executes the dploot tool to loot DPAPI related secrets from local or remote targ`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 419`** (1 nodes): `Extract and display banners from XML files in the 'sessions' directory.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 420`** (1 nodes): `Generates an obfuscated payload to evade AV detection using the payloadGenerator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 421`** (1 nodes): `Converts a binary file to a shellcode string in C or Nim format.          This f`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 422`** (1 nodes): `Show the Hacker News in the terminal.          Parameters:             line (str`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 423`** (1 nodes): `Search the NVD for CVEs matching a service banner and persist findings.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 424`** (1 nodes): `Trasnform file .exe into binary file.          Args:             line (str): Rut`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 425`** (1 nodes): `Trasnform file .exe into donut binary file.          Args:             line (str`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 426`** (1 nodes): `Genera y ejecuta pruebas de Atomic Red Team usando el C2.          Parameters:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 427`** (1 nodes): `Sube un archivo al C2.          Parameters:         file_path (str): Ruta del ar`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 428`** (1 nodes): `upload command in the client using the C2 to upload a file          Parameters:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 429`** (1 nodes): `Descarga un archivo desde el C2.          Parameters:         file_name (str): N`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 430`** (1 nodes): `Download a file from the C2.          Parameters:         line (str): Command in`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 431`** (1 nodes): `Ejecuta un comando en el cliente usando el C2.          Parameters:         comm`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 432`** (1 nodes): `Exec command in the client using the C2. download: command you must put the file`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 433`** (1 nodes): `Obfuscates a PowerShell script using various techniques.         by @JoelGMSec h`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 434`** (1 nodes): `Executes the D3m0n1z3dShell tool for persistence in Linux.          This functio`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 435`** (1 nodes): `Copies the local "sessions" directory to a remote host using scp, leveraging ssh`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 436`** (1 nodes): `Configures the local machine with internet access to act as an APT proxy for a m`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 437`** (1 nodes): `Configures the local machine with internet access to act as a pip proxy for a ma`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 438`** (1 nodes): `Configures the local machine with internet access to act as a proxy for a machin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 439`** (1 nodes): `Checks for updates by comparing the local version with the remote version.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 440`** (1 nodes): `Executes wmiexec-pro with various options for WMI operations.          This func`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 441`** (1 nodes): `Generates or updates a JSON file to be used as a database.          The JSON fil`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 442`** (1 nodes): `Convert shellcode into an ELF file and infect it.          This function takes a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 443`** (1 nodes): `Perform Remote Execution Command trow ssh using grisun0 user, see help grisun0`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 444`** (1 nodes): `Clone a website and serve the files in sessions/{url_cloned}.         Args:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 445`** (1 nodes): `Send special string to trigger a reverse shell, with the command 'c2 client_name`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 446`** (1 nodes): `Configures and starts a listener for a specified victim.          This function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 447`** (1 nodes): `Configures and starts a listener for a specified victim.          This function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 448`** (1 nodes): `Retrieves detailed information about an IP address using the ARIN API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 449`** (1 nodes): `Creates a systemd service file for a specified binary and generates a script to`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 450`** (1 nodes): `Creates a systemd service file for a specified binary and generates a script to`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 451`** (1 nodes): `Sends a magic packet to the Chinese malware.         The function extracts rhost`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 452`** (1 nodes): `Download a file from the command and control (C2) server.          This function`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 453`** (1 nodes): `Execute a command to interact with the GROQ API using the provided API key.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 454`** (1 nodes): `Display C and ASM code side by side in a curses-based interface.          This f`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 455`** (1 nodes): `Executes the camphish tool for Grab cam shots from target's phone front camera o`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 456`** (1 nodes): `Executes the hound tool for Hound is a simple and light tool for information gat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 457`** (1 nodes): `Obfuscates a shell script by encoding it in Base64 and prepares a command to dec`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 458`** (1 nodes): `Load the session from the sessionLazyOwn.json file and display the status of var`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 459`** (1 nodes): `Perform lateral movement by downloading and installing LazyOwn on a remote Linux`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 460`** (1 nodes): `Executes the Commix tool for detecting and exploiting command injection vulnerab`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 461`** (1 nodes): `Add a client to execute c2 commands          Parameters:             line (str):`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 462`** (1 nodes): `LazyOwn RedTeam Adversary Emulator, you can configure your own adversaries in ad`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 463`** (1 nodes): `Ofuscate a string into Go code.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 464`** (1 nodes): `Get list de supported acctions.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 465`** (1 nodes): `Convert a binary path to x64 little-endian hex code for shellcode injection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 466`** (1 nodes): `Convert raw hex payload from msfvenom into NASM-compatible shellcode format.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 467`** (1 nodes): `Generates an offensive playbook using:         1. Nmap scan results (CSV)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 468`** (1 nodes): `Create a basic synthetic playbook from Nmap CSV when LLM fails.          Usage:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 469`** (1 nodes): `Extract YAML from an existing debug file and try to create a playbook.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 470`** (1 nodes): `Generates an MP4 video from PNG images found in the sessions/captured_images dir`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 471`** (1 nodes): `Converts the Python REMCOMSVC byte string from remcomsvc.py to Golang byte slice`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 472`** (1 nodes): `Processes CSV files with scan results and vulnerability data to generate a Shoda`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 473`** (1 nodes): `Execute adversary from YAML in lazyadversaries/*.yaml         Syntax: adversary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 474`** (1 nodes): `Generate shellcode in C format using msfvenom for either a custom command or a r`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 475`** (1 nodes): `Open a centered popup in the current tmux session to execute a shell command.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 476`** (1 nodes): `Add a new alias with support for placeholders like {rhost}, {lhost}, {lport}, et`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 477`** (1 nodes): `List all available aliases.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 478`** (1 nodes): `Add a new custom command to the 'find' system, saved in user_commands.json.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 479`** (1 nodes): `Remove a custom command by index (as shown in 'find').          Only removes use`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 480`** (1 nodes): `Encrypt with AES and random key to PE EXE file, to usage with loaders.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 481`** (1 nodes): `Enable or disable the IA assitant (use DeepSeek in local).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OllamaModel` connect `Community 0` to `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 7`, `Community 8`, `Community 10`, `Community 11`, `Community 12`, `Community 13`?**
  _High betweenness centrality (0.260) - this node is a cross-community bridge._
- **Why does `LazyOwnShell` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 10`, `Community 11`, `Community 12`, `Community 13`?**
  _High betweenness centrality (0.247) - this node is a cross-community bridge._
- **Why does `add()` connect `Community 5` to `Community 2`, `Community 3`, `Community 4`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 505 inferred relationships involving `OllamaModel` (e.g. with `LazyOwnShellBridge` and `SessionContextProvider`) actually correct?**
  _`OllamaModel` has 505 INFERRED edges - model-reasoned connections that need verification._
- **Are the 135 inferred relationships involving `LazyOwnShell` (e.g. with `OllamaModel` and `Handler`) actually correct?**
  _`LazyOwnShell` has 135 INFERRED edges - model-reasoned connections that need verification._
- **Are the 69 inferred relationships involving `is_binary_present()` (e.g. with `.run_lazymsfvenom()` and `do_nikto()`) actually correct?**
  _`is_binary_present()` has 69 INFERRED edges - model-reasoned connections that need verification._
- **Are the 59 inferred relationships involving `copy2clip()` (e.g. with `do_getcap()` and `do_smbclient()`) actually correct?**
  _`copy2clip()` has 59 INFERRED edges - model-reasoned connections that need verification._