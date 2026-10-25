## Multi-Operator Collaboration

LazyOwn's collab layer provides real-time team server functionality via
Server-Sent Events (SSE). It activates automatically when `lazyc2.py` starts.

**Browser dashboard** — open in any browser on the team:
```
https://<lhost>:<c2_port>/collab/?operator=<your_handle>
```

**Terminal SSE stream**:
```bash
curl --insecure -N "https://<lhost>:<c2_port>/collab/stream?operator=alice" | jq .
```

**Publish a finding to all operators**:
```bash
curl --insecure -sk -X POST https://<lhost>:<c2_port>/collab/publish \
  -H "Content-Type: application/json" \
  -d '{"type":"finding","operator":"alice","payload":{"target":"10.10.11.5","detail":"root via CVE-2024-xxxx"}}'
```

**Lock a target** (prevents two operators running the same tool):
```bash
curl --insecure -sk -X POST https://<lhost>:<c2_port>/collab/lock \
  -H "Content-Type: application/json" \
  -d '{"target":"10.10.11.5","operator":"alice","ttl_secs":300}'
```

| Endpoint | Method | Description |
|---|---|---|
| `/collab/` | GET | Multi-operator browser dashboard |
| `/collab/stream?operator=<name>` | GET (SSE) | Real-time event stream |
| `/collab/operators` | GET | Active operator list |
| `/collab/publish` | POST | Broadcast a structured event |
| `/collab/lock` | POST | Acquire advisory target lock |
| `/collab/unlock` | POST | Release target lock |
| `/collab/locks` | GET | All active locks |
| `/collab/history?n=100` | GET | Last N events |

From the CLI: `collab_join <handle>` prints all URLs for a given operator.

---
