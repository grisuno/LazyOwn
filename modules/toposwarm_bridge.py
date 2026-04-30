#!/usr/bin/env python3
"""
modules/toposwarm_bridge.py
============================
Local brain bridge: connects LazyOwn to the TopoSwarm router when cloud LLMs
(Groq / Ollama / Claude Code) are unavailable.

TopoSwarm is a 2M-parameter quaternionic toroidal model trained specifically
on LazyOwn tool traces.  It routes natural-language operator prompts to the
correct LazyOwn tool + argument without any external API call.

Fallback hierarchy this module implements
-----------------------------------------
  cloud LLMs available?  →  use them (not this module)
              ↓ no
  TopoSwarm model loaded? →  neural routing (16-40% acc, improving)
              ↓ no
  keyword routing only    →  regex/keyword matching (~80% acc on common phrases)

Public API
----------
  bridge = TopoSwarmBridge()
  result = bridge.route("scan open ports on 10.10.11.78")
  # result.tool_name  → "lazyown_run_command"
  # result.arg        → "set rhost 10.10.11.78\\nlazynmap"
  # result.confidence → 0.92
  # result.backend    → "toposwarm_model" | "toposwarm_keyword"

  # For the hive autonomous loop: execute the routed tool via the bridge
  output = bridge.execute(result)

  # Check availability
  bridge.available      → True/False
  bridge.model_loaded   → True/False
"""

from __future__ import annotations

import importlib.util
import json
import logging
import os
import subprocess
import sys
import uuid
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

log = logging.getLogger("toposwarm_bridge")

# ── Paths ──────────────────────────────────────────────────────────────────────

_LAZYOWN_DIR   = Path(__file__).resolve().parent.parent
_TOPOSWARM_DIR = Path(os.environ.get(
    "TOPOSWARM_DIR",
    _LAZYOWN_DIR.parent / "py" / "toposwarm",
))
_ORCHESTRATOR  = _TOPOSWARM_DIR / "toposwarm_lazyown_orchestrator.py"
_CHECKPOINT    = _TOPOSWARM_DIR / "checkpoints_toposwarm" / "latest" / "model.safetensors"
_ROUTING_HEAD  = _TOPOSWARM_DIR / "checkpoints_toposwarm" / "routing_head.pt"


# ── Value objects ──────────────────────────────────────────────────────────────

@dataclass
class RoutedCall:
    """Result of a routing decision."""
    tool_name:  str
    arg:        str
    confidence: float
    backend:    str          # "toposwarm_model" | "toposwarm_keyword" | "error"
    raw_prompt: str = ""
    result_id:  str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def lazyown_command(self) -> str:
        """Return the LazyOwn shell command string to execute this tool call."""
        if self.tool_name == "lazyown_run_command":
            return self.arg
        if self.tool_name == "lazyown_set_config":
            key, _, val = self.arg.partition("=")
            return f"set {key.strip()} {val.strip()}"
        # Generic: use the arg as a shell command
        return self.arg or self.tool_name.replace("lazyown_", "")


# ── Keyword routing (no model needed) ─────────────────────────────────────────

# (keyword, tool_name, default_arg)  — ordered longest-match wins
# IMPORTANT: more-specific entries must appear BEFORE shorter overlapping ones
_KEYWORD_MAP: dict[str, tuple[str, str]] = {
    # ── Autonomous / hive (must be before generic "status"/"report") ──────────
    "inject objective":        ("lazyown_autonomous_inject", ""),
    "inject new objective":    ("lazyown_autonomous_inject", ""),
    "inject obj":              ("lazyown_autonomous_inject", ""),
    "new objective":           ("lazyown_autonomous_inject", ""),
    "autonomous start":        ("lazyown_autonomous_start", ""),
    "start autonomous":        ("lazyown_autonomous_start", ""),
    "autonomous mode":         ("lazyown_autonomous_start", ""),
    "autonomous daemon":       ("lazyown_autonomous_start", ""),
    "autonomous stop":         ("lazyown_autonomous_stop", ""),
    "stop autonomous":         ("lazyown_autonomous_stop", ""),
    "autonomous status":       ("lazyown_autonomous_status", ""),
    "daemon status":           ("lazyown_autonomous_status", ""),
    "auto loop":               ("lazyown_auto_loop", ""),
    "autonomous events":       ("lazyown_autonomous_events", ""),
    # ── Hive mind ─────────────────────────────────────────────────────────────
    "hive spawn":              ("lazyown_hive_spawn", ""),
    "spawn drone":             ("lazyown_hive_spawn", ""),
    "spawn hive":              ("lazyown_hive_spawn", ""),
    "spawn.*drone":            ("lazyown_hive_spawn", ""),   # regex-like hint
    "drone.*parallel":         ("lazyown_hive_spawn", ""),
    "hive.*parallel":          ("lazyown_hive_spawn", ""),
    "parallel drone":          ("lazyown_hive_spawn", ""),
    "hive status":             ("lazyown_hive_status", ""),
    "hive recall":             ("lazyown_hive_recall", ""),
    "hive plan":               ("lazyown_hive_plan", ""),
    "hive collect":            ("lazyown_hive_collect", ""),
    # ── Reporting (before generic "report") ───────────────────────────────────
    "situation report":        ("lazyown_campaign_sitrep", ""),
    "campaign sitrep":         ("lazyown_campaign_sitrep", ""),
    "campaign status":         ("lazyown_campaign_sitrep", ""),
    "full status":             ("lazyown_campaign_sitrep", ""),
    "sitrep":                  ("lazyown_campaign_sitrep", ""),
    "campaign overview":       ("lazyown_campaign_sitrep", ""),
    "engagement status":       ("lazyown_campaign_sitrep", ""),
    "what.*accomplished":      ("lazyown_campaign_sitrep", ""),
    "generate report":         ("lazyown_generate_report", ""),
    "pentest report":          ("lazyown_generate_report", ""),
    "final report":            ("lazyown_generate_report", ""),
    "attack timeline":         ("lazyown_timeline", ""),
    "red team timeline":       ("lazyown_timeline", ""),
    "campaign lessons":        ("lazyown_campaign_lessons", ""),
    "lessons learned":         ("lazyown_campaign_lessons", ""),
    # ── Intel / recommendations ───────────────────────────────────────────────
    "what should.*next":       ("lazyown_recommend_next", ""),
    "what to do.*after":       ("lazyown_recommend_next", ""),
    "next step":               ("lazyown_recommend_next", ""),
    "recommend next":          ("lazyown_recommend_next", ""),
    "best next":               ("lazyown_recommend_next", ""),
    "recommend":               ("lazyown_recommend_next", ""),
    "what next":               ("lazyown_recommend_next", ""),
    "after.*access":           ("lazyown_recommend_next", ""),
    # ── C2 (more specific before generic "status") ────────────────────────────
    "c2 server.*up":           ("lazyown_c2_status", ""),
    "c2 server.*running":      ("lazyown_c2_status", ""),
    "c2.*running":             ("lazyown_c2_status", ""),
    "c2.*up":                  ("lazyown_c2_status", ""),
    "c2 status":               ("lazyown_c2_status", ""),
    "c2.*alive":               ("lazyown_c2_status", ""),
    "command.*control.*up":    ("lazyown_c2_status", ""),
    "beacon":                  ("lazyown_get_beacons", ""),
    "implant":                 ("lazyown_get_beacons", ""),
    "session":                 ("lazyown_list_sessions", ""),
    # ── Recon ─────────────────────────────────────────────────────────────────
    "port scan":               ("lazyown_run_command", "lazynmap"),
    "nmap":                    ("lazyown_run_command", "lazynmap"),
    "lazynmap":                ("lazyown_run_command", "lazynmap"),
    "scan.*port":              ("lazyown_run_command", "lazynmap"),
    "escanear":                ("lazyown_run_command", "lazynmap"),
    "scan":                    ("lazyown_run_command", "lazynmap"),
    "enumerate smb":           ("lazyown_run_command", "lazysmbscan"),
    "smb share":               ("lazyown_run_command", "lazysmbscan"),
    "smb enum":                ("lazyown_run_command", "lazysmbscan"),
    "smb scan":                ("lazyown_run_command", "lazysmbscan"),
    "gobuster":                ("lazyown_run_command", "lazygobuster"),
    "enum4linux":              ("lazyown_run_command", "lazyenum4linux"),
    "bloodhound":              ("lazyown_run_command", "lazybloodhound"),
    "nikto":                   ("lazyown_run_command", "lazynikto"),
    "wpscan":                  ("lazyown_run_command", "lazywpscan"),
    # ── Config ────────────────────────────────────────────────────────────────
    "set rhost":               ("lazyown_set_config", "rhost="),
    "set lhost":               ("lazyown_set_config", "lhost="),
    "set port":                ("lazyown_set_config", "lport="),
    "set domain":              ("lazyown_set_config", "domain="),
    "show config":             ("lazyown_get_config", ""),
    "current config":          ("lazyown_get_config", ""),
    "get config":              ("lazyown_get_config", ""),
    # ── Credentials (after autonomous_inject so "hash" doesn't override) ──────
    "credentials":             ("lazyown_credentials", ""),
    "creds":                   ("lazyown_credentials", ""),
    "captured.*password":      ("lazyown_credentials", ""),
    "found.*password":         ("lazyown_credentials", ""),
    "ntlm hash":               ("lazyown_credentials", ""),
    "password":                ("lazyown_credentials", ""),
    # ── Exploits ──────────────────────────────────────────────────────────────
    "searchsploit":            ("lazyown_searchsploit", ""),
    "search.*exploit":         ("lazyown_searchsploit", ""),
    "find exploit":            ("lazyown_searchsploit", ""),
    "vuln analysis":           ("lazyown_c2_vuln_analysis", ""),
    "vulnerability":           ("lazyown_c2_vuln_analysis", ""),
    "cve search":              ("lazyown_cve_search", ""),
    "cve lookup":              ("lazyown_cve_search", ""),
}


def _keyword_route(prompt: str) -> Optional[RoutedCall]:
    """Return a RoutedCall from keyword/pattern matching, or None if no match."""
    import re as _re
    low = prompt.lower()
    best_tool, best_arg, best_key_len = None, "", 0
    for kw, (tool, arg) in _KEYWORD_MAP.items():
        # Support simple wildcards (* in key → regex .*) for broader matching
        if ".*" in kw:
            pat = kw.replace(".*", r".*")
            matched = bool(_re.search(pat, low))
        else:
            matched = kw in low
        if matched and len(kw) > best_key_len:
            best_tool, best_arg, best_key_len = tool, arg, len(kw)
    if best_tool is None:
        return None
    # Try to extract an IP from the prompt
    import re
    ip_match = re.search(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", prompt)
    if ip_match:
        ip = ip_match.group(1)
        if best_tool == "lazyown_run_command" and best_arg in ("lazynmap", "lazygobuster"):
            best_arg = f"set rhost {ip}\n{best_arg}"
        elif best_tool == "lazyown_set_config" and best_arg.startswith("rhost="):
            best_arg = f"rhost={ip}"
    return RoutedCall(
        tool_name=best_tool,
        arg=best_arg,
        confidence=0.75,
        backend="toposwarm_keyword",
        raw_prompt=prompt,
    )


# ── Neural routing (uses trained TopoSwarm model) ─────────────────────────────

def _load_toposwarm_modules():
    """Dynamically import from the TopoSwarm repo."""
    if not _TOPOSWARM_DIR.exists():
        return None, None, None
    for name, path in [
        ("topo_swarm_agent",  _TOPOSWARM_DIR / "topo_swarm_agent.py"),
        ("toposwarm_continual_trainer", _TOPOSWARM_DIR / "toposwarm_continual_trainer.py"),
        ("lazyown_dataset_gen", _TOPOSWARM_DIR / "lazyown_dataset_generator.py"),
    ]:
        if name not in sys.modules:
            if not path.exists():
                return None, None, None
            spec = importlib.util.spec_from_file_location(name, path)
            mod  = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            try:
                spec.loader.exec_module(mod)
            except Exception as e:
                log.debug("TopoSwarm module load failed: %s", e)
                return None, None, None
    return (
        sys.modules.get("topo_swarm_agent"),
        sys.modules.get("toposwarm_continual_trainer"),
        None,
    )


# ── Online Feedback Loop ───────────────────────────────────────────────────────

_FEEDBACK_FILE = _LAZYOWN_DIR / "sessions" / "toposwarm_feedback.jsonl"


class OnlineFeedbackLoop:
    """
    Collects user feedback on routing decisions and applies it immediately.

    Positive feedback:
      → Hebbian update on routing_head.liquid.W_fast (instant, no backprop)
      → Stored as a positive example for the next --finetune run

    Negative feedback:
      → Stored as a hard-negative for the next --finetune run
      → No model update (we don't want to reinforce the wrong decision)

    Non-blocking: feedback() is fire-and-forget. If the user doesn't call it,
    the flow continues unchanged. Feedback persists to disk so it survives
    across sessions and is automatically picked up by --finetune.

    Usage:
        result = bridge.route("scan 10.10.11.78")
        # ... execute tool ...
        bridge.feedback(result.result_id, good=True,  comment="correct tool")
        bridge.feedback(result.result_id, good=False, comment="wrong, should be hive_spawn")
    """

    def __init__(self, maxsize: int = 1000) -> None:
        self._pending:   Dict[str, Dict[str, Any]] = {}   # result_id → pending entry
        self._positives: deque = deque(maxlen=maxsize)
        self._negatives: deque = deque(maxlen=maxsize)
        self._feedback_file = _FEEDBACK_FILE
        self._feedback_file.parent.mkdir(parents=True, exist_ok=True)

    def register(
        self,
        result:      RoutedCall,
        hidden:      Optional[Any] = None,   # torch.Tensor hidden state (optional)
    ) -> None:
        """Register a routing result as pending feedback."""
        self._pending[result.result_id] = {
            "result_id":  result.result_id,
            "prompt":     result.raw_prompt,
            "tool_name":  result.tool_name,
            "confidence": result.confidence,
            "backend":    result.backend,
            "hidden":     hidden,           # kept in-memory only (not serialised)
        }

    def feedback(
        self,
        result_id:    str,
        good:         bool,
        comment:      str  = "",
        routing_head: Any  = None,    # RoutingHead instance for Hebbian update
    ) -> bool:
        """
        Apply feedback for a routing decision.

        Returns True if the result_id was found, False otherwise.
        Never raises — this is fire-and-forget.
        """
        entry = self._pending.pop(result_id, None)
        if entry is None:
            log.debug("feedback: result_id %s not found (already consumed or expired)",
                      result_id)
            return False

        record = {
            "result_id":  result_id,
            "prompt":     entry["prompt"],
            "tool_name":  entry["tool_name"],
            "confidence": entry["confidence"],
            "good":       good,
            "comment":    comment,
        }

        if good:
            self._positives.append(record)
            # Immediate Hebbian update: strengthen hidden → tool association
            hidden = entry.get("hidden")
            if hidden is not None and routing_head is not None:
                try:
                    import torch
                    liq = getattr(routing_head, "liquid", None)
                    if liq is not None and hasattr(liq, "hebbian_update"):
                        label = routing_head.label(entry["tool_name"])
                        if label >= 0:
                            liq.hebbian_update(
                                hidden.unsqueeze(0),
                                torch.tensor([label], dtype=torch.long,
                                             device=hidden.device),
                            )
                            log.debug("Hebbian update applied: %s → %s",
                                      entry["prompt"][:50], entry["tool_name"])
                except Exception as e:
                    log.debug("Hebbian update failed: %s", e)
        else:
            self._negatives.append(record)
            log.debug("Negative feedback stored: %s → %s (comment: %s)",
                      entry["prompt"][:50], entry["tool_name"], comment)

        # Persist to disk for --finetune pickup
        try:
            with self._feedback_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            log.debug("Feedback write failed: %s", e)

        return True

    def pending_count(self) -> int:
        return len(self._pending)

    def stats(self) -> Dict[str, int]:
        return {
            "pending":   len(self._pending),
            "positives": len(self._positives),
            "negatives": len(self._negatives),
        }

    def load_feedback_for_training(self) -> tuple:
        """
        Load persisted feedback for --finetune.
        Returns (positive_records, negative_records) as ToolBench-format dicts.
        """
        positives, negatives = [], []
        if not self._feedback_file.exists():
            return positives, negatives
        for line in self._feedback_file.read_text(encoding="utf-8").splitlines():
            try:
                entry = json.loads(line)
                record = {
                    "instruction": entry["prompt"],
                    "api_list": [{"tool_name": entry["tool_name"],
                                  "api_name":  entry["tool_name"] + "_endpoint",
                                  "api_description": entry["tool_name"],
                                  "required_parameters": [{"name": "arg", "type": "STRING"}],
                                  "optional_parameters": []}],
                    "answer":  f"[TOOL_CALL: {entry['tool_name']}()] [user feedback]",
                    "domain":  "Security/Feedback",
                    "_good":   entry["good"],
                }
                (positives if entry["good"] else negatives).append(record)
            except Exception:
                pass
        return positives, negatives


# ── Bridge class ───────────────────────────────────────────────────────────────

class TopoSwarmBridge:
    """
    Stateful bridge to the TopoSwarm local router.

    Lazy-loads the model on first use so import cost is zero when TopoSwarm
    is not needed (Groq/Ollama available).
    """

    def __init__(self) -> None:
        self._model       = None
        self._tok         = None
        self._head        = None
        self._cfg         = None
        self._agent_mod   = None
        self._ct_mod      = None
        self._loaded      = False
        self._load_failed = False
        self.feedback_loop = OnlineFeedbackLoop()

    @property
    def available(self) -> bool:
        """True if TopoSwarm directory exists (even if model not loaded)."""
        return _ORCHESTRATOR.exists()

    @property
    def model_loaded(self) -> bool:
        return self._loaded and self._model is not None

    def _try_load(self) -> bool:
        """Attempt to load model + routing head. Returns True on success."""
        if self._loaded or self._load_failed:
            return self._loaded
        if not _CHECKPOINT.exists():
            log.debug("TopoSwarm checkpoint not found at %s", _CHECKPOINT)
            self._load_failed = True
            return False
        agent_mod, ct_mod, _ = _load_toposwarm_modules()
        if agent_mod is None:
            self._load_failed = True
            return False
        try:
            import logging as _lg
            cfg   = agent_mod.SwarmConfig()
            tok   = agent_mod.BPETokenizer(cfg)
            model = agent_mod.TopoSwarmModel(cfg)
            ckpt  = agent_mod.CheckpointManager(cfg, _lg.getLogger("toposwarm"))
            ckpt.load(model, device=cfg.DEVICE)
            model.eval()
            head = None
            if _ROUTING_HEAD.exists() and ct_mod:
                try:
                    head = ct_mod.RoutingHead.load(cfg.D_MODEL, str(_ROUTING_HEAD))
                    head = head.to(cfg.DEVICE)
                    head.eval()
                    log.info("TopoSwarm routing head loaded (%d tools)", head.n_tools)
                except Exception as e:
                    log.debug("Routing head load failed: %s — using LM token routing", e)
            self._model, self._tok, self._cfg = model, tok, cfg
            self._head = head
            self._agent_mod, self._ct_mod = agent_mod, ct_mod
            self._loaded = True
            log.info("TopoSwarm model loaded from %s", _CHECKPOINT)
            return True
        except Exception as exc:
            log.warning("TopoSwarm model load failed: %s", exc)
            self._load_failed = True
            return False

    def _neural_route(self, prompt: str) -> Optional[RoutedCall]:
        """Use the neural model to route a prompt. Returns None on failure."""
        if not self._try_load():
            return None
        import torch
        try:
            instr_ids = self._tok.encode(prompt[:512])[-self._cfg.MAX_SEQ_LEN:]
            ids = torch.tensor([instr_ids], dtype=torch.long)
            with torch.no_grad():
                out = self._model(ids, berry_phase=0.0)
            if self._head is not None:
                # Use dedicated routing head via hook
                captured = []
                def _hook(m, i, o):
                    captured.append(o[0, -1, :].detach())
                h = self._model.norm_out.register_forward_hook(_hook)
                with torch.no_grad():
                    self._model(ids, berry_phase=0.0)
                h.remove()
                if captured:
                    hidden     = captured[0]       # [d_model] — saved for Hebbian
                    rlogits    = self._head(hidden.unsqueeze(0))[0]
                    import torch.nn.functional as F
                    probs      = F.softmax(rlogits, dim=-1)
                    top_prob, top_idx = probs.max(dim=-1)
                    tool_name  = self._head.tool_names[top_idx.item()]
                    confidence = top_prob.item()
                    result = RoutedCall(
                        tool_name=tool_name,
                        arg="",
                        confidence=confidence,
                        backend="toposwarm_model",
                        raw_prompt=prompt,
                    )
                    # Register for potential feedback (hidden state saved)
                    self.feedback_loop.register(result, hidden=hidden)
                    return result
            # Fallback: LM head token prediction
            logits = out["logits"][0, -1,
                     self._cfg.TOOL_TOKEN_OFFSET:
                     self._cfg.TOOL_TOKEN_OFFSET + self._cfg.TOOL_VOCAB_SIZE]
            import torch.nn.functional as F
            probs = F.softmax(logits, dim=-1)
            top_prob, top_off = probs.max(dim=-1)
            # Reverse-lookup tool name from token offset
            tool_token = self._cfg.TOOL_TOKEN_OFFSET + top_off.item()
            # Scan known tool names for a match
            for tool_name in _KEYWORD_MAP:
                if self._tok.tool_token(
                    next((t for t in _KEYWORD_MAP if _KEYWORD_MAP[t][0] == tool_name), tool_name)
                ) == tool_token:
                    break
            return RoutedCall(
                tool_name="lazyown_run_command",
                arg="",
                confidence=top_prob.item(),
                backend="toposwarm_model",
                raw_prompt=prompt,
            )
        except Exception as exc:
            log.debug("Neural routing failed: %s", exc)
            return None

    def feedback(self, result_id: str, good: bool, comment: str = "") -> bool:
        """
        Optional user feedback on a routing decision.

        Non-blocking — safe to call in a fire-and-forget fashion.
        Positive feedback → immediate Hebbian update on routing head.
        Negative feedback → stored as hard-negative for next --finetune.

        Returns True if the result_id was found, False if expired/unknown.

        Example:
            result = bridge.route("scan 10.10.11.78")
            # ... execute, check output ...
            bridge.feedback(result.result_id, good=True)
            bridge.feedback(result.result_id, good=False,
                            comment="should have been hive_spawn")
        """
        return self.feedback_loop.feedback(
            result_id    = result_id,
            good         = good,
            comment      = comment,
            routing_head = self._head,
        )

    def route(self, prompt: str) -> RoutedCall:
        """
        Route an operator prompt to a LazyOwn tool call.

        Tries neural routing first (if model loaded), then keyword routing.
        Always returns a RoutedCall — never raises.
        Each result has a `result_id` you can pass to bridge.feedback().
        """
        # 1. Try neural routing
        result = self._neural_route(prompt)
        if result and result.confidence >= 0.15:
            return result
        # 2. Keyword routing
        kw = _keyword_route(prompt)
        if kw:
            # Register keyword results too (no hidden state for Hebbian)
            self.feedback_loop.register(kw)
            return kw
        # 3. Default: run_command with prompt as-is
        return RoutedCall(
            tool_name="lazyown_run_command",
            arg=prompt,
            confidence=0.10,
            backend="toposwarm_keyword",
            raw_prompt=prompt,
        )

    def execute_via_orchestrator(self, prompt: str, no_model: bool = False) -> str:
        """
        Execute a prompt through the full TopoSwarm orchestrator (subprocess).
        Returns the output string. Used by the autonomous loop.
        """
        if not _ORCHESTRATOR.exists():
            return f"[TopoSwarm] Orchestrator not found at {_ORCHESTRATOR}"
        cmd = [sys.executable, str(_ORCHESTRATOR), "--prompt", prompt]
        if no_model:
            cmd.append("--no-model")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True, text=True,
                timeout=60,
                cwd=str(_TOPOSWARM_DIR),
            )
            out = result.stdout.strip()
            err = result.stderr.strip()
            return out or err or "[TopoSwarm] no output"
        except subprocess.TimeoutExpired:
            return "[TopoSwarm] timeout after 60s"
        except Exception as exc:
            return f"[TopoSwarm] error: {exc}"


# ── Module-level singleton ─────────────────────────────────────────────────────

_bridge: Optional[TopoSwarmBridge] = None


def get_bridge() -> TopoSwarmBridge:
    """Return the module-level TopoSwarmBridge singleton (lazy init)."""
    global _bridge
    if _bridge is None:
        _bridge = TopoSwarmBridge()
    return _bridge
