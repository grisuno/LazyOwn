"""Unified LLM client for the LazyOwn framework.

Consolidates the 10+ redundant LLM integration modules into a single
factory-based client supporting Groq, OpenAI, local models (Ollama/LM Studio),
and task-specific specializations.
"""

import json
import os
from typing import Any, Dict, List, Optional, Tuple


try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class UnifiedLLMClient:
    """Factory-based LLM client supporting multiple backends.

    Supports Groq, OpenAI, and local (Ollama) backends with task-specific
    configurations (red team ops, vulnerability analysis, phishing, reports).

    Args:
        backend: LLM backend ('groq', 'openai', 'ollama', 'local').
        api_key: API key for cloud backends.
        model: Model name to use.
        base_url: Base URL for OpenAI-compatible or local endpoints.
        temperature: Sampling temperature (0.0 to 1.0).
        max_tokens: Maximum tokens in the response.
        system_prompt: Default system prompt.
    """

    BACKENDS = ('groq', 'openai', 'ollama', 'local')
    TASKS = ('redop', 'vuln', 'phish', 'report', 'agent', 'search', 'general')

    def __init__(
        self,
        backend: str = 'groq',
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None,
    ):
        if backend not in self.BACKENDS:
            raise ValueError(f"Backend must be one of {self.BACKENDS}")

        self.backend = backend
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt or self._default_system_prompt()

        self._model = model or self._default_model(backend)
        self._client = self._create_client(backend, api_key, base_url)

        self._task_prompts: Dict[str, str] = {
            'redop': self._redop_system_prompt(),
            'vuln': self._vuln_system_prompt(),
            'phish': self._phish_system_prompt(),
            'report': self._report_system_prompt(),
            'agent': self._agent_system_prompt(),
        }

    def _default_model(self, backend: str) -> str:
        """Return the default model for each backend."""
        models = {
            'groq': 'llama-3.3-70b-versatile',
            'openai': 'gpt-4o-mini',
            'ollama': 'llama3.2',
            'local': 'llama3.2',
        }
        return models.get(backend, 'llama3.2')

    def _create_client(
        self, backend: str, api_key: Optional[str], base_url: Optional[str]
    ) -> Any:
        """Create the appropriate client for the backend."""
        if backend == 'groq':
            if not HAS_GROQ:
                raise ImportError("groq library is required. Install with: pip install groq")
            return Groq(api_key=api_key or os.environ.get('GROQ_API_KEY'))

        elif backend == 'openai':
            if not HAS_OPENAI:
                raise ImportError("openai library is required. Install with: pip install openai")
            return openai.OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY'),
                base_url=base_url,
            )

        elif backend in ('ollama', 'local'):
            if not HAS_OPENAI:
                raise ImportError("openai library is required. Install with: pip install openai")
            return openai.OpenAI(
                api_key='ollama',
                base_url=base_url or 'http://localhost:11434/v1',
            )

        return None

    def _default_system_prompt(self) -> str:
        """Return the default LazyOwn system prompt."""
        return (
            "You are LazyOwn, a red team operator assistant. "
            "You provide penetration testing guidance, exploit analysis, "
            "and security assessment support. Always operate ethically "
            "within authorized boundaries."
        )

    def _redop_system_prompt(self) -> str:
        """Return the Red Team operations system prompt."""
        return (
            "You are a Red Team operations specialist. "
            "Analyze the target environment, identify attack paths, "
            "suggest exploitation techniques, and plan lateral movement. "
            "Think like an adversary. Consider stealth, persistence, and "
            "operational security. Output structured attack plans."
        )

    def _vuln_system_prompt(self) -> str:
        """Return the vulnerability analysis system prompt."""
        return (
            "You are a vulnerability researcher. "
            "Analyze service banners, software versions, and configurations "
            "to identify known vulnerabilities. Map findings to CVE IDs. "
            "Provide exploit suggestions with CVSS scores and remediation steps."
        )

    def _phish_system_prompt(self) -> str:
        """Return the phishing campaign system prompt."""
        return (
            "You are a social engineering specialist for authorized "
            "penetration testing. Design phishing pretexts, craft emails, "
            "and suggest payload delivery methods. Focus on effectiveness "
            "while maintaining professional and convincing communication."
        )

    def _report_system_prompt(self) -> str:
        """Return the reporting system prompt."""
        return (
            "You are a penetration testing report writer. "
            "Generate executive summaries, technical findings, "
            "remediation recommendations, and risk assessments. "
            "Use professional language. Organize by severity. "
            "Include evidence references."
        )

    def _agent_system_prompt(self) -> str:
        """Return the autonomous agent system prompt."""
        return (
            "You are an autonomous penetration testing agent. "
            "Given a target and current state, determine the next optimal "
            "action. Consider reconnaissance, enumeration, exploitation, "
            "and post-exploitation phases. Output a single command or "
            "action. Be decisive and accurate."
        )

    def set_task(self, task: str) -> None:
        """Set the task-specific system prompt.

        Args:
            task: One of 'redop', 'vuln', 'phish', 'report', 'agent', or 'general'.
        """
        if task in self._task_prompts:
            self.system_prompt = self._task_prompts[task]
        elif task == 'general':
            self.system_prompt = self._default_system_prompt()

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Tuple[str, int, int]:
        """Send a chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'.
            temperature: Override default temperature.
            max_tokens: Override default max tokens.

        Returns:
            Tuple of (response_text, input_tokens, output_tokens).
        """
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens

        if not any(m.get('role') == 'system' for m in messages):
            messages.insert(0, {'role': 'system', 'content': self.system_prompt})

        if self.backend == 'groq':
            return self._chat_groq(messages, temp, max_tok)
        else:
            return self._chat_openai_compatible(messages, temp, max_tok)

    def _chat_groq(
        self, messages: List[Dict], temperature: float, max_tokens: int
    ) -> Tuple[str, int, int]:
        """Chat completion via Groq API."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        choice = response.choices[0]
        return (
            choice.message.content or '',
            response.usage.prompt_tokens if response.usage else 0,
            response.usage.completion_tokens if response.usage else 0,
        )

    def _chat_openai_compatible(
        self, messages: List[Dict], temperature: float, max_tokens: int
    ) -> Tuple[str, int, int]:
        """Chat completion via OpenAI or compatible API."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        choice = response.choices[0]
        return (
            choice.message.content or '',
            response.usage.prompt_tokens if response.usage else 0,
            response.usage.completion_tokens if response.usage else 0,
        )

    def prompt(
        self,
        user_prompt: str,
        task: Optional[str] = None,
        context: Optional[str] = None,
    ) -> str:
        """Send a single prompt and return the response.

        Args:
            user_prompt: The user's prompt text.
            task: Optional task specialization.
            context: Optional additional context to include.

        Returns:
            The model's response text.
        """
        if task:
            self.set_task(task)

        messages = [{'role': 'user', 'content': user_prompt}]

        if context:
            messages.insert(0, {
                'role': 'system',
                'content': f"Context:\n{context}",
            })

        response, _, _ = self.chat(messages)
        return response

    def analyze_vulnerability(
        self, service_name: str, version: str, port: int
    ) -> str:
        """Analyze a service for known vulnerabilities.

        Args:
            service_name: Service name (e.g., 'Apache httpd').
            version: Version string (e.g., '2.4.49').
            port: Port number.

        Returns:
            Analysis report text.
        """
        self.set_task('vuln')
        prompt = (
            f"Analyze the following service for vulnerabilities:\n"
            f"Service: {service_name}\n"
            f"Version: {version}\n"
            f"Port: {port}\n\n"
            f"List relevant CVEs, exploitation techniques, and known exploits."
        )
        return self.prompt(prompt)

    def plan_attack_path(
        self, target_info: str, objectives: str
    ) -> str:
        """Generate an attack path plan based on target information.

        Args:
            target_info: String describing the target environment.
            objectives: Attack objectives.

        Returns:
            Structured attack plan text.
        """
        self.set_task('redop')
        prompt = (
            f"Target Information:\n{target_info}\n\n"
            f"Objectives:\n{objectives}\n\n"
            f"Generate a step-by-step attack plan covering reconnaissance, "
            f"initial access, privilege escalation, lateral movement, "
            f"and data exfiltration."
        )
        return self.prompt(prompt)

    def generate_phishing_email(
        self, target_name: str, target_role: str, context: str
    ) -> str:
        """Generate a phishing email template.

        Args:
            target_name: Target person's name.
            target_role: Target person's role.
            context: Scenario context (reason for contact).

        Returns:
            Phishing email body text.
        """
        self.set_task('phish')
        prompt = (
            f"Generate a convincing phishing email for:\n"
            f"Name: {target_name}\n"
            f"Role: {target_role}\n"
            f"Context: {context}\n\n"
            f"Include subject line, body, and attachment mention. "
            f"Make it professional and urgent."
        )
        return self.prompt(prompt)

    def generate_report(
        self, findings: str, target_name: str
    ) -> str:
        """Generate a penetration test report.

        Args:
            findings: Bullet list of findings.
            target_name: Name of the target organization.

        Returns:
            Report text.
        """
        self.set_task('report')
        prompt = (
            f"Generate a penetration testing report for {target_name}.\n\n"
            f"Findings:\n{findings}\n\n"
            f"Include: executive summary, methodology, findings by severity, "
            f"and remediation recommendations."
        )
        return self.prompt(prompt)

    def next_action(self, state: str) -> str:
        """Determine the next autonomous action.

        Args:
            state: Current engagement state description.

        Returns:
            Recommended next action text.
        """
        self.set_task('agent')
        prompt = (
            f"Current engagement state:\n{state}\n\n"
            f"What is the single best next action? Output only the command "
            f"or tool name."
        )
        return self.prompt(prompt)


def create_llm_client(
    backend: str = 'groq',
    api_key: Optional[str] = None,
    task: str = 'general',
    **kwargs,
) -> UnifiedLLMClient:
    """Factory function to create a configured LLM client.

    Args:
        backend: LLM backend ('groq', 'openai', 'ollama').
        api_key: API key for cloud backends.
        task: Task specialization.
        **kwargs: Additional parameters passed to UnifiedLLMClient.

    Returns:
        Configured UnifiedLLMClient instance.
    """
    client = UnifiedLLMClient(backend=backend, api_key=api_key, **kwargs)
    if task != 'general':
        client.set_task(task)
    return client
