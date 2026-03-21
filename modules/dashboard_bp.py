#!/usr/bin/env python3
"""
modules/dashboard_bp.py
========================
Real-time SOC dashboard as a Flask Blueprint.

Registration (one line in lazyc2.py after app creation):
    from modules.dashboard_bp import dashboard_bp
    app.register_blueprint(dashboard_bp)

Then visit: http://localhost:4444/dashboard/
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, jsonify, render_template_string

# ---------------------------------------------------------------------------
# Blueprint definition
# ---------------------------------------------------------------------------
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# ---------------------------------------------------------------------------
# Session file paths
# ---------------------------------------------------------------------------
_SESSIONS_DIR = Path(__file__).parent.parent / "sessions"


# ---------------------------------------------------------------------------
# MITRE ATT&CK tactic mapping (from categories.py)
# ---------------------------------------------------------------------------
TACTICS = [
    ("01", "Reconnaissance",       "recon"),
    ("02", "Scanning & Enum",      "scanning"),
    ("03", "Exploitation",         "exploit"),
    ("04", "Post-Exploitation",    "post"),
    ("05", "Persistence",          "persistence"),
    ("06", "Privilege Escalation", "privesc"),
    ("07", "Credential Access",    "credential"),
    ("08", "Lateral Movement",     "lateral"),
    ("09", "Data Exfiltration",    "exfil"),
    ("10", "C2",                   "c2"),
    ("11", "Reporting",            "reporting"),
    ("12", "Miscellaneous",        "misc"),
    ("13", "Lua Plugins",          "lua"),
    ("14", "YAML Addons",          "yaml"),
    ("15", "Adversary YAML",       "adversary"),
    ("16", "AI",                   "ai"),
]


# ---------------------------------------------------------------------------
# Internal data aggregation
# ---------------------------------------------------------------------------

def _read_jsonl(path: Path, last_n: int = 0) -> list:
    """Read a .jsonl file, optionally returning only the last N lines."""
    if not path.exists():
        return []
    records = []
    try:
        lines = path.read_text(errors="replace").splitlines()
        if last_n > 0:
            lines = lines[-last_n:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                pass
    except Exception:
        pass
    return records


def _read_json(path: Path) -> dict | list:
    """Read a JSON file; return empty dict on any error."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(errors="replace"))
    except Exception:
        return {}


def _count_lines(path: Path) -> int:
    """Count non-empty lines in a text file."""
    if not path.exists():
        return 0
    try:
        return sum(1 for ln in path.read_text(errors="replace").splitlines() if ln.strip())
    except Exception:
        return 0


def _aggregate_data() -> dict:
    """
    Build the full dashboard data snapshot from session files.
    Returns a structured dict consumed by both the HTML page (via JS fetch)
    and the /dashboard/api/data endpoint.
    """
    sessions = _SESSIONS_DIR

    # -- Events ---------------------------------------------------------------
    events_raw = _read_jsonl(sessions / "events.jsonl", last_n=20)
    recent_events = []
    for ev in events_raw:
        recent_events.append({
            "timestamp": ev.get("timestamp", ev.get("ts", "")),
            "type":      ev.get("event_type", ev.get("type", "UNKNOWN")),
            "detail":    ev.get("suggest", ev.get("detail", ev.get("description", ""))),
            "severity":  ev.get("severity", "info"),
        })

    # -- Tactic event counts for MITRE grid -----------------------------------
    tactic_counts: dict[str, int] = {t[2]: 0 for t in TACTICS}
    all_events = _read_jsonl(sessions / "events.jsonl")
    for ev in all_events:
        cat = ev.get("category", ev.get("tactic", ""))
        if cat in tactic_counts:
            tactic_counts[cat] += 1
        # Also attempt a rough keyword match on event_type
        etype = ev.get("event_type", "").lower()
        for tactic_key in tactic_counts:
            if tactic_key in etype:
                tactic_counts[tactic_key] = tactic_counts[tactic_key] + 1
                break

    # -- Objectives -----------------------------------------------------------
    objectives_raw = _read_jsonl(sessions / "objectives.jsonl")
    objectives = []
    objectives_done = 0
    for obj in objectives_raw:
        done = bool(obj.get("done", obj.get("completed", obj.get("status", "") == "done")))
        if done:
            objectives_done += 1
        objectives.append({
            "id":          obj.get("id", ""),
            "title":       obj.get("title", obj.get("objective", obj.get("description", ""))),
            "description": obj.get("description", ""),
            "done":        done,
            "priority":    obj.get("priority", "normal"),
        })

    # -- Policy facts (hosts) -------------------------------------------------
    raw_facts = _read_json(sessions / "policy_facts.json")
    hosts = []
    if isinstance(raw_facts, dict):
        for host_ip, hdata in raw_facts.items():
            if not isinstance(hdata, dict):
                continue
            services_raw = hdata.get("services", {})
            services_list = (
                list(services_raw.keys()) if isinstance(services_raw, dict)
                else services_raw if isinstance(services_raw, list)
                else []
            )
            hosts.append({
                "ip":              host_ip,
                "os":              hdata.get("os_hint", hdata.get("os", "")),
                "services":        services_list,
                "service_count":   len(services_list),
                "credential_count": len(hdata.get("credentials", [])),
                "vuln_count":      len(hdata.get("vulnerabilities", [])),
            })

    # -- Credentials ----------------------------------------------------------
    cred_count = _count_lines(sessions / "credentials.txt")

    # -- Campaign -------------------------------------------------------------
    campaign = _read_json(sessions / "campaign.json")
    if not isinstance(campaign, dict):
        campaign = {}

    # -- Beacons (best-effort from campaign or placeholder) -------------------
    # The real beacon data lives in results{} dict inside lazyc2.py runtime;
    # we expose a static count from campaign.json if present.
    active_beacons = campaign.get("active_beacons", [])
    beacon_count = campaign.get("beacon_count", len(active_beacons))

    # -- Assemble -------------------------------------------------------------
    return {
        "generated_at":    datetime.now(tz=timezone.utc).isoformat(),
        "beacon_count":    beacon_count,
        "active_beacons":  active_beacons,
        "hosts_discovered": len(hosts),
        "credentials_found": cred_count,
        "objectives_done":  objectives_done,
        "objectives_total": len(objectives),
        "tactic_counts":   tactic_counts,
        "recent_events":   recent_events,
        "hosts":           hosts,
        "objectives":      objectives,
        "campaign":        campaign,
    }


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------
_DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>LazyOwn SOC Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0d1117;
  --surface:#161b22;
  --surface2:#1c2128;
  --border:#30363d;
  --accent:#00ff88;
  --accent-dim:#00cc6a;
  --text:#e6edf3;
  --text-muted:#8b949e;
  --danger:#ff4c4c;
  --warn:#ffa726;
  --info:#4fc3f7;
  --radius:6px;
  --font:'Courier New',Courier,monospace;
}
html,body{background:var(--bg);color:var(--text);font-family:var(--font);font-size:14px;line-height:1.5;min-height:100vh}
a{color:var(--accent);text-decoration:none}

/* ---- Header ---- */
.header{
  display:flex;align-items:center;justify-content:space-between;
  background:var(--surface);border-bottom:1px solid var(--border);
  padding:12px 24px;position:sticky;top:0;z-index:100;
}
.header-title{font-size:18px;font-weight:700;letter-spacing:.04em;color:var(--accent)}
.header-title span{color:var(--text);font-weight:400}
.header-meta{display:flex;align-items:center;gap:16px;font-size:12px;color:var(--text-muted)}
.pulse{
  width:8px;height:8px;border-radius:50%;background:var(--accent);
  display:inline-block;animation:blink 1.6s ease-in-out infinite;
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.refresh-counter{color:var(--text-muted)}

/* ---- Layout ---- */
.container{padding:20px 24px;max-width:1600px;margin:0 auto}
.section{margin-bottom:28px}
.section-title{
  font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--text-muted);border-bottom:1px solid var(--border);
  padding-bottom:6px;margin-bottom:14px;
}

/* ---- Stats row ---- */
.stats-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}
.stat-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:16px 18px;
}
.stat-label{font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px}
.stat-value{font-size:28px;font-weight:700;color:var(--accent);letter-spacing:.02em}
.stat-sub{font-size:11px;color:var(--text-muted);margin-top:2px}

/* ---- MITRE grid ---- */
.tactic-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px}
.tactic-cell{
  border-radius:var(--radius);padding:10px 12px;
  background:var(--surface2);border:1px solid var(--border);
  transition:border-color .2s;cursor:default;
}
.tactic-cell.has-events{border-color:var(--accent-dim)}
.tactic-num{font-size:10px;color:var(--text-muted);margin-bottom:2px}
.tactic-name{font-size:12px;font-weight:600;color:var(--text)}
.tactic-count{
  margin-top:6px;font-size:18px;font-weight:700;
  color:var(--surface2);
}
.tactic-cell.has-events .tactic-count{color:var(--accent)}
.tactic-bar{
  height:3px;border-radius:2px;background:var(--border);margin-top:6px;overflow:hidden
}
.tactic-bar-fill{height:100%;background:var(--accent);transition:width .4s}

/* ---- Two-column layout ---- */
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:900px){.two-col{grid-template-columns:1fr}}

/* ---- Cards ---- */
.card{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:16px;
}

/* ---- Tables ---- */
.data-table{width:100%;border-collapse:collapse;font-size:13px}
.data-table th{
  text-align:left;padding:8px 10px;
  font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--text-muted);border-bottom:1px solid var(--border);
  background:var(--surface2);
}
.data-table td{
  padding:7px 10px;border-bottom:1px solid #1e242b;
  vertical-align:top;word-break:break-word;
}
.data-table tr:last-child td{border-bottom:none}
.data-table tr:hover td{background:var(--surface2)}
.badge{
  display:inline-block;padding:1px 6px;border-radius:3px;
  font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;
}
.badge-info{background:#0d2a3b;color:var(--info)}
.badge-high{background:#3b0d0d;color:var(--danger)}
.badge-warn{background:#3b2500;color:var(--warn)}
.badge-ok{background:#0d2b1a;color:var(--accent)}

/* ---- Beacons list ---- */
.beacon-list{list-style:none;display:flex;flex-direction:column;gap:6px}
.beacon-item{
  display:flex;align-items:center;gap:10px;
  background:var(--surface2);border:1px solid var(--border);
  border-radius:var(--radius);padding:8px 12px;font-size:13px;
}
.beacon-dot{width:7px;height:7px;border-radius:50%;background:var(--accent);flex-shrink:0}
.beacon-id{font-weight:600;color:var(--accent);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.beacon-seen{color:var(--text-muted);font-size:11px}

/* ---- Objectives ---- */
.obj-list{list-style:none;display:flex;flex-direction:column;gap:6px}
.obj-item{
  display:flex;align-items:flex-start;gap:10px;
  background:var(--surface2);border:1px solid var(--border);
  border-radius:var(--radius);padding:8px 12px;
}
.obj-check{
  width:16px;height:16px;border-radius:3px;border:2px solid var(--border);
  flex-shrink:0;margin-top:2px;display:flex;align-items:center;justify-content:center;
}
.obj-check.done{background:var(--accent);border-color:var(--accent);color:#0d1117}
.obj-check.done::after{content:'\2713';font-size:11px;font-weight:700;line-height:1}
.obj-title{font-size:13px;color:var(--text)}
.obj-title.done{color:var(--text-muted);text-decoration:line-through}
.obj-desc{font-size:11px;color:var(--text-muted);margin-top:2px}

/* ---- Chart container ---- */
.chart-wrap{position:relative;height:220px}

/* ---- Empty state ---- */
.empty{color:var(--text-muted);font-size:13px;padding:16px 0;text-align:center}

/* ---- Status bar ---- */
.status-bar{
  font-size:11px;color:var(--text-muted);padding:6px 24px;
  border-top:1px solid var(--border);display:flex;gap:16px;flex-wrap:wrap;
}
</style>
</head>
<body>

<!-- ================================================================== Header -->
<header class="header">
  <div class="header-title">LazyOwn <span>SOC Dashboard</span></div>
  <div class="header-meta">
    <span><span class="pulse"></span></span>
    <span id="last-updated">Initializing...</span>
    <span class="refresh-counter">Next refresh: <span id="countdown">5</span>s</span>
    <span id="connection-status" class="badge badge-info">LOADING</span>
  </div>
</header>

<!-- ================================================================== Main -->
<div class="container">

  <!-- Stats row -->
  <div class="section">
    <div class="section-title">Operational Status</div>
    <div class="stats-grid" id="stats-grid">
      <div class="stat-card"><div class="stat-label">Active Beacons</div><div class="stat-value" id="s-beacons">--</div></div>
      <div class="stat-card"><div class="stat-label">Hosts Discovered</div><div class="stat-value" id="s-hosts">--</div></div>
      <div class="stat-card"><div class="stat-label">Credentials Found</div><div class="stat-value" id="s-creds">--</div></div>
      <div class="stat-card"><div class="stat-label">Objectives</div><div class="stat-value" id="s-obj">--</div><div class="stat-sub" id="s-obj-sub"></div></div>
    </div>
  </div>

  <!-- MITRE ATT&CK coverage grid -->
  <div class="section">
    <div class="section-title">MITRE ATT&CK Coverage</div>
    <div class="tactic-grid" id="tactic-grid"></div>
  </div>

  <!-- Events chart + Active beacons -->
  <div class="two-col section">
    <div class="card">
      <div class="section-title">Event Activity (last 20)</div>
      <div class="chart-wrap"><canvas id="events-chart"></canvas></div>
    </div>
    <div class="card">
      <div class="section-title">Active Beacons</div>
      <ul class="beacon-list" id="beacon-list"><li class="empty">No beacons registered.</li></ul>
    </div>
  </div>

  <!-- Recent Events table -->
  <div class="section card">
    <div class="section-title">Recent Events</div>
    <div id="events-table-wrap">
      <div class="empty">Loading...</div>
    </div>
  </div>

  <!-- Host Facts + Objectives -->
  <div class="two-col section">
    <div class="card">
      <div class="section-title">Host Facts</div>
      <div id="hosts-table-wrap"><div class="empty">No host facts yet.</div></div>
    </div>
    <div class="card">
      <div class="section-title">Objectives</div>
      <ul class="obj-list" id="obj-list"><li class="empty">No objectives loaded.</li></ul>
    </div>
  </div>

</div><!-- /container -->

<footer class="status-bar">
  <span>LazyOwn SOC Dashboard</span>
  <span id="footer-campaign"></span>
  <span id="footer-gen"></span>
</footer>

<script>
(function() {
  "use strict";

  // ---- Config ---------------------------------------------------------------
  const API_URL     = "/dashboard/api/data";
  const POLL_EVERY  = 5000;   // ms

  // ---- MITRE tactic metadata ------------------------------------------------
  const TACTICS = [
    ["01","Reconnaissance",       "recon"],
    ["02","Scanning & Enum",      "scanning"],
    ["03","Exploitation",         "exploit"],
    ["04","Post-Exploitation",    "post"],
    ["05","Persistence",          "persistence"],
    ["06","Privilege Escalation", "privesc"],
    ["07","Credential Access",    "credential"],
    ["08","Lateral Movement",     "lateral"],
    ["09","Data Exfiltration",    "exfil"],
    ["10","C2",                   "c2"],
    ["11","Reporting",            "reporting"],
    ["12","Miscellaneous",        "misc"],
    ["13","Lua Plugins",          "lua"],
    ["14","YAML Addons",          "yaml"],
    ["15","Adversary YAML",       "adversary"],
    ["16","AI",                   "ai"],
  ];

  // ---- Chart.js instance ----------------------------------------------------
  let eventsChart = null;

  function initChart() {
    const ctx = document.getElementById("events-chart").getContext("2d");
    eventsChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: [],
        datasets: [{
          label: "Events",
          data: [],
          backgroundColor: "rgba(0,255,136,0.55)",
          borderColor: "#00ff88",
          borderWidth: 1,
          borderRadius: 3,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#161b22",
            borderColor: "#30363d",
            borderWidth: 1,
            titleColor: "#e6edf3",
            bodyColor: "#8b949e",
          }
        },
        scales: {
          x: {
            ticks: { color: "#8b949e", maxRotation: 45, font: { size: 10 } },
            grid: { color: "#1e242b" }
          },
          y: {
            ticks: { color: "#8b949e", stepSize: 1, font: { size: 10 } },
            grid: { color: "#1e242b" },
            beginAtZero: true
          }
        }
      }
    });
  }

  // ---- Badge helper ---------------------------------------------------------
  function severityBadge(sev) {
    sev = (sev || "info").toLowerCase();
    const cls = sev === "high" || sev === "critical" ? "badge-high"
              : sev === "warn" || sev === "medium"    ? "badge-warn"
              : sev === "ok"   || sev === "success"   ? "badge-ok"
              : "badge-info";
    return `<span class="badge ${cls}">${esc(sev)}</span>`;
  }

  function esc(s) {
    if (s === null || s === undefined) return "";
    return String(s)
      .replace(/&/g,"&amp;")
      .replace(/</g,"&lt;")
      .replace(/>/g,"&gt;")
      .replace(/"/g,"&quot;");
  }

  function fmtTs(ts) {
    if (!ts) return "";
    try {
      const d = new Date(ts);
      if (isNaN(d.getTime())) return esc(ts);
      return d.toISOString().replace("T"," ").slice(0,19);
    } catch(e) { return esc(ts); }
  }

  // ---- Render functions -----------------------------------------------------

  function renderStats(d) {
    document.getElementById("s-beacons").textContent = d.beacon_count  ?? 0;
    document.getElementById("s-hosts").textContent   = d.hosts_discovered ?? 0;
    document.getElementById("s-creds").textContent   = d.credentials_found ?? 0;
    const done  = d.objectives_done  ?? 0;
    const total = d.objectives_total ?? 0;
    document.getElementById("s-obj").textContent     = `${done}/${total}`;
    document.getElementById("s-obj-sub").textContent = total > 0
      ? `${Math.round((done/total)*100)}% complete`
      : "";
  }

  function renderTacticGrid(counts) {
    const grid = document.getElementById("tactic-grid");
    const maxCount = Math.max(1, ...Object.values(counts || {}));
    let html = "";
    TACTICS.forEach(([num, name, key]) => {
      const count = (counts && counts[key]) ? counts[key] : 0;
      const hasEv = count > 0;
      const pct   = Math.round((count / maxCount) * 100);
      html += `
        <div class="tactic-cell${hasEv ? " has-events" : ""}">
          <div class="tactic-num">${esc(num)}</div>
          <div class="tactic-name">${esc(name)}</div>
          <div class="tactic-count">${count}</div>
          <div class="tactic-bar"><div class="tactic-bar-fill" style="width:${pct}%"></div></div>
        </div>`;
    });
    grid.innerHTML = html;
  }

  function renderEventsTable(events) {
    const wrap = document.getElementById("events-table-wrap");
    if (!events || events.length === 0) {
      wrap.innerHTML = '<div class="empty">No events recorded yet.</div>';
      return;
    }
    let rows = "";
    events.slice().reverse().forEach(ev => {
      rows += `<tr>
        <td style="white-space:nowrap;color:var(--text-muted)">${fmtTs(ev.timestamp)}</td>
        <td>${esc(ev.type)}</td>
        <td>${esc(ev.detail)}</td>
        <td>${severityBadge(ev.severity)}</td>
      </tr>`;
    });
    wrap.innerHTML = `
      <table class="data-table">
        <thead><tr>
          <th>Timestamp</th><th>Type</th><th>Detail</th><th>Severity</th>
        </tr></thead>
        <tbody>${rows}</tbody>
      </table>`;
  }

  function renderHostsTable(hosts) {
    const wrap = document.getElementById("hosts-table-wrap");
    if (!hosts || hosts.length === 0) {
      wrap.innerHTML = '<div class="empty">No host facts yet.</div>';
      return;
    }
    let rows = "";
    hosts.forEach(h => {
      const svcs = Array.isArray(h.services)
        ? h.services.slice(0,6).map(s => `<span class="badge badge-info">${esc(s)}</span>`).join(" ")
        : "";
      rows += `<tr>
        <td style="color:var(--accent);white-space:nowrap">${esc(h.ip)}</td>
        <td>${esc(h.os) || "<span style='color:var(--text-muted)'>unknown</span>"}</td>
        <td>${svcs || `<span style='color:var(--text-muted)'>${h.service_count || 0}</span>`}</td>
        <td style="text-align:center">${h.credential_count || 0}</td>
        <td style="text-align:center">${h.vuln_count || 0}</td>
      </tr>`;
    });
    wrap.innerHTML = `
      <table class="data-table">
        <thead><tr>
          <th>IP</th><th>OS</th><th>Services</th><th>Creds</th><th>Vulns</th>
        </tr></thead>
        <tbody>${rows}</tbody>
      </table>`;
  }

  function renderBeacons(beacons) {
    const list = document.getElementById("beacon-list");
    if (!beacons || beacons.length === 0) {
      list.innerHTML = '<li class="empty">No beacons registered.</li>';
      return;
    }
    let html = "";
    beacons.forEach(b => {
      const id   = typeof b === "object" ? (b.id || b.beacon_id || JSON.stringify(b)) : b;
      const seen = typeof b === "object" ? (b.last_seen || b.ts || "") : "";
      html += `<li class="beacon-item">
        <span class="beacon-dot"></span>
        <span class="beacon-id">${esc(String(id))}</span>
        ${seen ? `<span class="beacon-seen">${fmtTs(seen)}</span>` : ""}
      </li>`;
    });
    list.innerHTML = html;
  }

  function renderObjectives(objectives) {
    const list = document.getElementById("obj-list");
    if (!objectives || objectives.length === 0) {
      list.innerHTML = '<li class="empty">No objectives loaded.</li>';
      return;
    }
    let html = "";
    objectives.forEach(obj => {
      const done = Boolean(obj.done);
      html += `<li class="obj-item">
        <div class="obj-check${done ? " done" : ""}"></div>
        <div>
          <div class="obj-title${done ? " done" : ""}">${esc(obj.title)}</div>
          ${obj.description && obj.description !== obj.title
            ? `<div class="obj-desc">${esc(obj.description)}</div>` : ""}
        </div>
      </li>`;
    });
    list.innerHTML = html;
  }

  function renderChart(events) {
    if (!eventsChart || !events) return;
    // Build a tally by type from the last 20 events
    const tally = {};
    (events || []).forEach(ev => {
      const t = ev.type || "UNKNOWN";
      tally[t] = (tally[t] || 0) + 1;
    });
    const labels = Object.keys(tally);
    const data   = Object.values(tally);
    eventsChart.data.labels   = labels;
    eventsChart.data.datasets[0].data = data;
    eventsChart.update("none");
  }

  // ---- Main render ----------------------------------------------------------
  function renderAll(d) {
    renderStats(d);
    renderTacticGrid(d.tactic_counts || {});
    renderEventsTable(d.recent_events || []);
    renderHostsTable(d.hosts || []);
    renderBeacons(d.active_beacons || []);
    renderObjectives(d.objectives || []);
    renderChart(d.recent_events || []);

    // Footer
    const camp = d.campaign || {};
    const campName = camp.name || camp.campaign || "";
    document.getElementById("footer-campaign").textContent =
      campName ? `Campaign: ${campName}` : "";
    document.getElementById("footer-gen").textContent =
      d.generated_at ? `Data at: ${fmtTs(d.generated_at)}` : "";

    // Header
    document.getElementById("last-updated").textContent =
      "Last refresh: " + new Date().toLocaleTimeString();
    document.getElementById("connection-status").textContent = "LIVE";
    document.getElementById("connection-status").className   = "badge badge-ok";
  }

  // ---- Polling --------------------------------------------------------------
  let countdownVal  = 5;
  let pollTimer     = null;
  let countdownTimer = null;

  function startCountdown() {
    countdownVal = Math.round(POLL_EVERY / 1000);
    clearInterval(countdownTimer);
    countdownTimer = setInterval(function() {
      countdownVal = Math.max(0, countdownVal - 1);
      const el = document.getElementById("countdown");
      if (el) el.textContent = countdownVal;
    }, 1000);
  }

  function fetchData() {
    fetch(API_URL)
      .then(function(resp) {
        if (!resp.ok) throw new Error("HTTP " + resp.status);
        return resp.json();
      })
      .then(function(data) {
        renderAll(data);
      })
      .catch(function(err) {
        console.warn("Dashboard fetch error:", err);
        document.getElementById("connection-status").textContent = "ERROR";
        document.getElementById("connection-status").className   = "badge badge-high";
      })
      .finally(function() {
        startCountdown();
        pollTimer = setTimeout(fetchData, POLL_EVERY);
      });
  }

  // ---- Init -----------------------------------------------------------------
  document.addEventListener("DOMContentLoaded", function() {
    initChart();
    fetchData();
  });

})();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@dashboard_bp.route("/")
def dashboard_index():
    """Render the main SOC dashboard HTML page."""
    return render_template_string(_DASHBOARD_HTML)


@dashboard_bp.route("/api/data")
def dashboard_api_data():
    """
    JSON snapshot of all dashboard data.

    Reads directly from sessions/ files so it can be used even without
    the full lazyc2.py runtime context (e.g. during testing).
    """
    return jsonify(_aggregate_data())
