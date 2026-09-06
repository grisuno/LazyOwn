"""Canonical prompt-template and knowledge-base contract for LLM consumers.

Owns every task-domain prompt template used by the Groq chat family and the
structured helpers (truncation, knowledge-base CRUD, relevance filtering,
payload/event context loading) that were previously duplicated across the
retired ``modules.legacy.lazygptcli*`` scripts.

This module is pure: it never imports a vendor SDK, never performs network
calls, and never reads process environment directly. All filesystem locations
and tunables are resolved through :class:`LlmPromptConfig` so tests can point
every read/write at temporary fixtures.

Usage::

    from modules.llm_prompts import LlmPromptConfig, KnowledgeStore

    config = LlmPromptConfig(project_root="/tmp/x")
    store = config.knowledge_store("vuln")
    kb = store.relevant("nmap output", limit=5)
    prompt = config.render("vuln", "raw nmpa output", context=ctx)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

PROMPT_MAX_CHARS = 18000
KNOWLEDGE_TAIL_LIMIT = 5

DEFAULT_SYSTEM_PROMPT = "You are a helpful penetration testing assistant."

KB_FILE_NAMES = {
    "oneliner": "knowledge_base.json",
    "script": "knowledge_base_script.json",
    "search": "knowledge_base_search.json",
    "vuln": "knowledge_base_vuln.json",
    "redop": "knowledge_base_redop.json",
}

PAYLOAD_KEY_ORDER = (
    "start_user",
    "start_pass",
    "rhost",
    "lhost",
    "domain",
    "subdomain",
    "wordlist",
    "usrwordlist",
)

_REPORT_CONTEXT_BASENAMES = (
    "sessionLazyOwn.json",
    "body_report.json",
    "tasks.json",
    "users.json",
)

_ONE_LINER_MODEL = "llama3-70b-8192"
_ADVERSARY_MODEL = "llama3-70b-8192"

_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


def default_project_root() -> str:
    """Return the repository root that owns the LLM prompt configuration.

    Returns:
        Absolute path to the LazyOwn repository root.
    """
    return os.path.abspath(os.path.join(_MODULE_DIR, os.pardir))


def resolve_model(model: str | None) -> str:
    """Resolve an explicit model or fall back to the randomized Groq model.

    Args:
        model: Explicit Groq model identifier or None.

    Returns:
        The model to send to the chat completion endpoint.
    """
    if model:
        return model
    try:
        from modules.colors import retModel

        return retModel()
    except Exception:
        return _ONE_LINER_MODEL


def truncate_message(message: str, max_chars: int = PROMPT_MAX_CHARS) -> str:
    """Truncate a message with an ellipsis marker when it exceeds the limit.

    Args:
        message: Source text.
        max_chars: Maximum allowed character length.

    Returns:
        Truncated text, or the original when it fits within ``max_chars``.
    """
    if len(message) <= max_chars:
        return message
    return message[:max_chars] + "..."


@dataclass(frozen=True)
class LlmPromptConfig:
    """Resolved filesystem and behavioural configuration for prompt rendering.

    Attributes:
        project_root: Repository root used to locate payload, event and session
            artefacts.
        kb_dir: Directory that stores the knowledge-base JSON files.
        payload_path: Absolute path to payload.json.
        event_config_path: Absolute path to event_config.json or None.
        sessions_dir: Directory that stores per-session plan history.
    """

    project_root: str
    kb_dir: str = field(default="")
    payload_path: str = field(default="")
    event_config_path: str = field(default="")
    sessions_dir: str = field(default="")

    @classmethod
    def from_defaults(cls, project_root: str | None = None) -> LlmPromptConfig:
        """Build a config rooted at the given project root.

        Args:
            project_root: Repository root override; defaults to the detected
                repository root.

        Returns:
            A fully-resolved :class:`LlmPromptConfig`.
        """
        root = project_root or default_project_root()
        kb_dir = os.environ.get("LAZYOWN_KB_DIR", os.path.join(root, "modules"))
        return cls(
            project_root=root,
            kb_dir=kb_dir,
            payload_path=os.path.join(root, "payload.json"),
            event_config_path=os.path.join(root, "event_config.json"),
            sessions_dir=os.path.join(root, "sessions"),
        )

    def knowledge_base_path(self, domain: str) -> str:
        """Return the absolute path for a knowledge-base domain file.

        Args:
            domain: One of the keys in :data:`KB_FILE_NAMES`.

        Returns:
            Absolute path to the knowledge-base JSON file.
        """
        return os.path.join(self.kb_dir, KB_FILE_NAMES[domain])

    def load_payload_context(self) -> dict[str, str]:
        """Load the operator context keyed by :data:`PAYLOAD_KEY_ORDER`.

        Returns:
            Mapping of every payload key to its value or an empty string.
        """
        data: dict[str, Any] = {}
        if self.payload_path:
            try:
                with open(self.payload_path, encoding="utf-8") as handle:
                    data = json.load(handle)
            except (OSError, json.JSONDecodeError):
                data = {}
        return {key: str(data.get(key, "")) for key in PAYLOAD_KEY_ORDER}

    def load_event_tool_output(self, event_name: str) -> str:
        """Load tool output attached to a named event in event_config.json.

        Args:
            event_name: Event whose ``tool_output`` path should be read.

        Returns:
            File content, or an empty string when no event or file matches.
        """
        if not self.event_config_path:
            return ""
        try:
            with open(self.event_config_path, encoding="utf-8") as handle:
                events = json.load(handle).get("events", [])
        except (OSError, json.JSONDecodeError):
            return ""
        for event in events:
            if event.get("name") == event_name:
                tool_output = event.get("tool_output", "")
                if tool_output and os.path.exists(tool_output):
                    try:
                        with open(tool_output, encoding="utf-8") as handle:
                            return handle.read()
                    except OSError:
                        return ""
        return ""

    def load_plan_history(self) -> str:
        """Load the session plan history text if present.

        Returns:
            Plan file content, or an empty string when unavailable.
        """
        plan_path = os.path.join(self.sessions_dir, "plan.txt")
        if not os.path.exists(plan_path):
            return ""
        try:
            with open(plan_path, encoding="utf-8") as handle:
                return handle.read()
        except OSError:
            return ""

    def load_report_context(self) -> dict[str, Any]:
        """Load the JSON artefacts consumed by the report template.

        Returns:
            Mapping of basename to its parsed JSON content.
        """
        ctx: dict[str, Any] = {}
        for basename in _REPORT_CONTEXT_BASENAMES:
            path = os.path.join(self.project_root, basename)
            if basename in ("sessionLazyOwn.json", "tasks.json"):
                path = os.path.join(self.sessions_dir, basename)
            if basename == "body_report.json":
                path = os.path.join(self.project_root, "static", basename)
            try:
                with open(path, encoding="utf-8") as handle:
                    ctx[basename] = json.load(handle)
            except (OSError, json.JSONDecodeError):
                ctx[basename] = {}
        return ctx

    def knowledge_store(self, domain: str) -> KnowledgeStore:
        """Build a knowledge store bound to a domain file.

        Args:
            domain: Knowledge-base domain key.

        Returns:
            A :class:`KnowledgeStore` reading and writing the domain file.
        """
        return KnowledgeStore(self.knowledge_base_path(domain))

    def render(
        self,
        template: str,
        base_prompt: str,
        *,
        kb_lines: list[str] | None = None,
    ) -> str:
        """Render a named template with shared knowledge and context.

        Args:
            template: Template key in :data:`TEMPLATES`.
            base_prompt: Operator prompt substituted into the template.
            kb_lines: Relevant knowledge lines; latest ones are embedded.

        Returns:
            Fully rendered system prompt string.
        """
        builder = TEMPLATES[template]
        kb_text = render_kb_tail(kb_lines or [])
        return builder(base_prompt, kb_text, self)


def render_kb_tail(lines: list[str]) -> str:
    """Join the most recent knowledge lines for embedding into a prompt.

    Args:
        lines: Candidate knowledge strings.

    Returns:
        Newline-joined tail of the input limited by
        :data:`KNOWLEDGE_TAIL_LIMIT`.
    """
    if not lines:
        return ""
    return "\n".join(lines[-KNOWLEDGE_TAIL_LIMIT:])


class KnowledgeStore:
    """List-of-dict knowledge base persisted as JSON on disk."""

    def __init__(self, path: str) -> None:
        """Initialize a store bound to a single JSON file.

        Args:
            path: Absolute path of the knowledge-base file.
        """
        self.path = path

    def load(self) -> list[dict[str, str]]:
        """Load the knowledge-base records from disk.

        Returns:
            List of ``{"prompt", "response"}`` records; empty on any read error.
        """
        try:
            with open(self.path, encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, list):
                return [entry for entry in data if isinstance(entry, dict)]
        except (OSError, json.JSONDecodeError):
            pass
        return []

    def save(self, records: list[dict[str, str]]) -> None:
        """Persist a full record list to disk, creating parent directories.

        Args:
            records: List of knowledge-base records to write.
        """
        parent = os.path.dirname(self.path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(records, handle, indent=2)

    def add(self, prompt: str, response: str) -> None:
        """Append a prompt/response record to the knowledge base.

        Args:
            prompt: Operator prompt that produced the response.
            response: Model response to remember.
        """
        records = self.load()
        records.append({"prompt": prompt, "response": response})
        self.save(records)

    def relevant(self, prompt: str, limit: int = KNOWLEDGE_TAIL_LIMIT) -> list[str]:
        """Return knowledge responses whose text shares keywords with the prompt.

        Args:
            prompt: Query used to select relevant records.
            limit: Maximum number of responses to return.

        Returns:
            List of matching knowledge responses.
        """
        keywords = set(prompt.lower().split())
        matches: list[str] = []
        for entry in self.load():
            text = f"{entry.get('prompt', '')} {entry.get('response', '')}".lower()
            if keywords and any(keyword in text for keyword in keywords):
                matches.append(entry.get("response", ""))
        return matches[:limit]


def _payload_block(config: LlmPromptConfig) -> str:
    ctx = config.load_payload_context()
    lines = []
    for key in PAYLOAD_KEY_ORDER:
        lines.append(f"{key}: {ctx[key]}")
    return "\n".join(lines)


def _prompt_oneliner(base_prompt: str, kb_text: str, config: LlmPromptConfig) -> str:
    del config
    return (
        "Create a coherent command or script in a single line to achieve the goal "
        "specified by the user. Use tools like nmap, curl, wget, python, perl, ruby, "
        "powershell, bash, netcat, sqlmap, hydra, john, metasploit, msfvenom, "
        "crackmapexec, impacket, evil-winrm, chisel, socat, etc.\n"
        "The command must be executable in a terminal (Linux or Windows).\n"
        "Return the exact command in a single line. Do not wrap in markdown code fences.\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Respond only with the requested command and nothing else. "
        "Do not provide explanations, just the exact command to copy and paste."
    )


def _prompt_script(base_prompt: str, kb_text: str, config: LlmPromptConfig) -> str:
    del config
    return (
        "Create a script that meets the following requirements:\n"
        "- Functionality\n- Language\n- Architecture\n- Refactoring\n\n"
        "Context for red team and pentesting:\n"
        "- Ethical: Must only be used with proper authorization\n"
        "- Legal: Compliance with local laws is mandatory\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Respond only with the requested script and nothing else. "
        "Do not provide explanations, just the exact script to copy and paste."
    )


def _prompt_adversary(base_prompt: str, kb_text: str, config: LlmPromptConfig) -> str:
    del config
    return (
        "Chatbot Prompt for Adversary Emulation using Atomic Red Team Framework\n\n"
        "Objective: To provide detailed information about a specific adversary technique "
        "defined by the Atomic Red Team framework.\n\n"
        "Technique Name\nMITRE Technique ID\nDescription\nSupported Platforms\n"
        "Execution Commands\nDetection Methods\n"
        "All testing must be conducted in authorized environments. "
        "The purpose is for ethical security research.\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Respond only with the requested technical details and commands."
    )


def _prompt_general(base_prompt: str, kb_text: str, config: LlmPromptConfig) -> str:
    return (
        "Analyze the following prompt and provide assistance by suggesting commands "
        "or strategies. The context is a simulated red team operation where we act as "
        "ethical hackers performing authorized penetration testing.\n\n"
        f"Knowledge base:\n{_payload_block(config)}\n"
        f"{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "All exercises are conducted in private labs with explicit authorization. "
        "Provide clear, actionable commands and strategies."
    )


def _prompt_search(base_prompt: str, kb_text: str, config: LlmPromptConfig) -> str:
    del config
    return (
        "investigating and analyzing techniques, tools, and strategies used in red teaming, "
        "pentesting, and APT. The RESEARCH should be able to provide up-to-date information, "
        "identify emerging trends, and offer practical recommendations.\n\n"
        "Analysis of Techniques and Tools\nThreat Intelligence\nVulnerability Analysis\n"
        "Trend Analysis\nCase Studies\nRecommendations\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Provide comprehensive analysis and actionable recommendations."
    )


def _prompt_vuln(base_prompt: str, kb_text: str, config: LlmPromptConfig) -> str:
    ctx = config.load_payload_context()
    return (
        "Analyze the following NMAP output generated by Nmap and use a vulnerability "
        "assessment template to identify vulnerabilities. Based on your analysis, "
        "generate a detailed action plan for penetration testing.\n\n"
        f"rhost: {ctx['rhost']}\n"
        "If EXIST VALID USERS of KERBRUTE show me in your RESPONSE.\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Provide a detailed vulnerability assessment and penetration testing action plan."
    )


def _prompt_task(base_prompt: str, kb_text: str, config: LlmPromptConfig) -> str:
    ctx = config.load_payload_context()
    return (
        "Analyze the following Task output json generated to task assessment template "
        "to identify What tasks do I have left to do according to the given JSON template? "
        "please give me a porcent of completitud, and You can provide me with commands "
        f"to perform this tasks {base_prompt} here the ip {ctx['rhost']} and domain: {ctx['domain']}\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        "Provide task completion percentage and suggested next commands."
    )


def _prompt_redop(base_prompt: str, kb_text: str, config: LlmPromptConfig) -> str:
    del config
    return (
        "Objective: Evaluate the status of any Red Team operation using provided JSON "
        "database parameters and compare it with real-world operations.\n\n"
        "Instructions:\n"
        "Review JSON Database: Examine parameters, credentials, hashes, timestamps, notes, plan, and implants.\n"
        "Assess Operation Status: Credential Harvesting, Vulnerability Identification, Implant Deployment, "
        "Reconnaissance, Post-Exploitation, Documentation.\n"
        "Compare with Real-World Operations: Effectiveness, Stealth, Impact, Remediation.\n\n"
        f"Knowledge base:\n{kb_text}\n\n"
        f"[[ {base_prompt} ]]\n\n"
        "Provide a thorough evaluation and recommendations."
    )


TEMPLATES = {
    "oneliner": _prompt_oneliner,
    "script": _prompt_script,
    "adversary": _prompt_adversary,
    "general": _prompt_general,
    "search": _prompt_search,
    "vuln": _prompt_vuln,
    "task": _prompt_task,
    "redop": _prompt_redop,
}

TEMPLATE_MODELS = {
    "oneliner": _ONE_LINER_MODEL,
    "adversary": _ADVERSARY_MODEL,
}

TEMPLATE_KB_DOMAINS = {
    "oneliner": "oneliner",
    "script": "script",
    "adversary": "script",
    "general": "script",
    "search": "search",
    "vuln": "vuln",
    "task": "vuln",
    "redop": "redop",
}
