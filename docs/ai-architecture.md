## Advanced AI Architecture (MoE + RL + SWAN + Hive Mind)

LazyOwn integrates a world-class multi-agent AI stack that adapts and improves through every engagement:

### Mixture of Experts (MoE) — `modules/moe_router.py`

Five LLM experts are registered with capability tags, base weights, and cost tiers:

| Expert | Backend | Strengths |
|--------|---------|-----------|
| `groq_fast` | Groq llama-3.1-8b-instant | Recon, enumeration, rapid decisions |
| `groq_powerful` | Groq llama-3.3-70b-versatile | Exploitation, post-ex, complex reasoning |
| `groq_deepseek_r1` | Groq deepseek-r1-distill-llama-70b | Privilege escalation, step-by-step reasoning |
| `ollama_reason` | Ollama deepseek-r1:1.5b | Offline, privacy-safe, detailed analysis |
| `groq_gemma` | Groq gemma2-9b-it | Lateral movement, credential analysis |

Routing uses temperature-scaled softmax (`T = max(0.5, 1.5/(1+calls/50))`) over adjusted weights. Weights self-adjust via exponential moving average of per-expert reward over time.

### Reinforcement Learning from Models (RLM) — `modules/rl_trainer.py`

Tabular Q-learning trains the routing policy over engagement sessions:

```
State:  (task_type, engagement_phase, recent_reward_bucket)
Action: expert_id
Reward: r_raw - λ * detection_prob * |r_raw|    (λ=0.5)
Update: Q(s,a) ← Q(s,a) + α * [r + γ * max_a' Q(s',a') - Q(s,a)]
```

Hyperparameters: α=0.10, γ=0.90, ε_start=0.20, ε_min=0.05, ε_decay=0.995. Epsilon-greedy exploration decays per update. Q-values persist to `sessions/expert_qvalues.json` across sessions.

### SWAN Orchestrator — `skills/swan_agent.py`

The top-level integration layer wires MoE + RL + Detection Oracle + Hive Memory:

- `swan_run`: single-expert execution with RL-guided routing and post-execution Q-update
- `swan_ensemble`: N experts in parallel via ThreadPoolExecutor, synthesised by `WeightedTextAggregator`
- `OutcomeEvaluator`: reward = 0 when detection probability ≥ 70% (detection-aware reward shaping)
- Every result stored in Hive Memory (ChromaDB) for cross-session learning

### Detection Oracle (Blue Team Mirror) — `modules/detection_oracle.py`

Predicts detection probability **before** execution using 17 Sigma-lite rules covering:
credential access (LSASS, SAM, DCSync), lateral movement (PsExec, WMI, evil-winrm), privilege escalation (token impersonation, named pipes), exploitation, recon, C2, and brute force.

Probability aggregation: `P(detect) = 1 - ∏(1 - P_i)` across all triggered rules.

### Purple Team Closed Loop — `modules/auto_purple.py`

Automated red-vs-blue measurement loop that executes offensive actions, queries LazyOwnBT for detection, and feeds results back to the Detection Oracle for calibration.

```bash
(LazyOwn) > purple_exec nmap -sV 10.10.11.5 recon    # execute + detect
(LazyOwn) > purple_score                              # show detection rates
(LazyOwn) > purple_report                             # export CSV + JSON
(LazyOwn) > purple_dashboard                          # Textual TUI
```

**Detection methods:**

| Method | What it checks |
|--------|----------------|
| `ai_test` | LazyOwnBT ML model prediction |
| `proc_scan` | Suspicious process names |
| `net_scan` | Unusual connections/ports |
| `log_analyze` | Auth/syslog anomalies |
| `fim_scan` | File integrity changes |
| `redteam_hunt` | Threat hunting patterns |
| `sigma_rules` | 10 Sigma rules (mimikatz, reverse shell, privesc, nmap, webshell, /etc/shadow, cron, SMB, exfil, injection) |

**Sigma rules detection engine** (LazyOwnBT `lazyownbt/detection.py`):

| ID | Rule | Level |
|----|------|-------|
| LAZYOWN-001 | Mimikatz Credential Dump | critical |
| LAZYOWN-002 | Reverse Shell Pattern | critical |
| LAZYOWN-003 | Privilege Escalation via Sudo | high |
| LAZYOWN-004 | Nmap Scan Detected | medium |
| LAZYOWN-005 | Webshell Execution | critical |
| LAZYOWN-006 | Process Injection | high |
| LAZYOWN-007 | /etc/shadow Access | critical |
| LAZYOWN-008 | Cron Persistence | high |
| LAZYOWN-009 | Lateral Movement SMB | high |
| LAZYOWN-010 | Data Exfiltration | high |

**Output files:**
- `sessions/purple_dataset.csv` — ML training dataset
- `sessions/purple_audit.jsonl` — full audit log
- `sessions/detection_feedback.jsonl` — oracle calibration

**Note:** For production use, integrate with a real SIEM (Wazuh, Elastic SIEM, Splunk) via auditd log forwarding. The built-in Sigma rules are for offline testing only.

### Hive Mind — `skills/hive_mind.py`

Multi-agent queen+drone architecture with shared memory:
- **QueenBrain** (Claude): high-level orchestration + ConsensusProtocol for high-risk actions
- **DronePool** (Groq/Ollama): parallel execution of recon/exploit/cred/lateral/privesc tasks
- **HiveMemory**: ChromaDB semantic + SQLite episodic + Parquet long-term storage
- **EpisodeReflectionEngine**: post-campaign lesson extraction stored as `sessions/campaign_lessons.jsonl`

### Autonomous Campaign Intelligence (ACI) — `skills/aci_planner.py`

**The first C2 framework that plans, executes, and learns autonomously.**

ACI bridges the gap between a natural-language engagement goal and a fully
autonomous execution loop. No competitor (Cobalt Strike, Sliver, Havoc,
Metasploit) does this end-to-end:

```
Operator: "Compromise the domain controller at corp.internal
           starting from a phishing foothold on 10.10.11.5"
         ↓
ACI Planner ──► MITRE ATT&CK decomposition (LLM-backed, static fallback)
                 recon → exploit → exec → privesc → cred → lateral → report
         ↓
ObjectiveStore ─► 20+ concrete objectives injected into sessions/objectives.jsonl
         ↓
auto_loop / autonomous_daemon ─► executes each objective autonomously
         ↓
ACIEngine monitors ─► detects stalled phases (blocked_count ≥ 3)
         ↓
ACIReplan ──► LLM generates alternative techniques for blocked phases
         ↓
ACIReflector ──► appends lessons to sessions/campaign_lessons.jsonl
                 feeds back into the next engagement
```

**Three MCP tools:**

| Tool | What it does |
|------|-------------|
| `lazyown_aci_plan` | Decompose a goal → ATT&CK plan → inject objectives |
| `lazyown_aci_status` | Live phase breakdown, completion %, replan recommendation |
| `lazyown_aci_replan` | Force adaptive replan when stalled; auto-generates lessons |

**Quick-start:**

```python
# 1. Submit the engagement goal
lazyown_aci_plan(
    goal="Compromise the DC at corp.internal",
    target="10.10.11.5",
    scope=["10.10.11.0/24"],
    domain="corp.internal",
    os_hint="windows",
)

# 2. Start autonomous execution
lazyown_auto_loop(target="10.10.11.5", max_steps=20)

# 3. Monitor progress
lazyown_aci_status()

# 4. When blocked (blocked_count >= 3)
lazyown_aci_replan(reason="Kerberoasting blocked by AV, try AS-REP roasting")
```

**What makes ACI unique vs. other tools:**

- Cobalt Strike / Sliver / Havoc are C2 frameworks — the operator plans every step
- Metasploit has automation but no intelligence
- CALDERA emulates fixed ATT&CK procedures but can't adapt to novel environments
- **ACI plans, executes, replans, and learns — continuously, across engagements**

**Persistence:**

| File | Contents |
|------|----------|
| `sessions/aci_plan.json` | Active plan: phases, objectives, completion state |
| `sessions/aci_history.jsonl` | Archived completed/abandoned plans |
| `sessions/campaign_lessons.jsonl` | Lessons extracted by ACIReflector |

**CLI usage (standalone):**

```bash
python3 skills/aci_planner.py plan "Compromise DC" --target 10.10.11.5 --os windows
python3 skills/aci_planner.py status
python3 skills/aci_planner.py replan "technique blocked"
python3 skills/aci_planner.py reflect
```

### Autonomous Daemon — `skills/autonomous_daemon.py`

Four asyncio roles in a single process — no Claude required between steps:

```
Role 1 — ObjectiveLoop      : watches objectives.jsonl, takes + executes
Role 2 — ExecutionEngine    : 6-layer cascade per step, RL Q-table feedback
  Reactive → Parquet → Bridge → SWAN(MoE+RL) → LLM → Fallback
Role 3 — WorldModelWatcher  : graph centrality + pivot candidate tracking
Role 4 — DroneCoordinator   : hive drone spawning on recon/cred/service findings
```

Enable SWAN in the daemon: `export AUTO_USE_SWAN=1` before starting.

ACI feeds into the daemon: objectives injected by `lazyown_aci_plan` are picked
up automatically by Role 1 (ObjectiveLoop) — no additional configuration needed.

### Graph-Based Reasoning — `modules/world_model.py`

NetworkGraph tracks all discovered relationships (hosts, services, credentials, trust paths) and computes normalized degree centrality to surface pivot candidates. The top-3 candidates are injected into every `to_context_string()` call, ensuring the autonomous loop always knows the highest-value lateral movement targets.
