#!/usr/bin/env python3
"""
LazyOwn AI Agent - Ultimate Edition
Improvements: anti-hang timeout, memory management, argument validation and anti-loop.
"""

import argparse
import ast
import contextlib
import importlib.util
import inspect
import io
import json
import logging
import os
import queue
import sys
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

try:
    from .logging_config import configure, get_logger  # noqa: F401
except ImportError:
    from logging_config import configure

# ===== MODEL IMPORTS =====
# Ensure ai_model.py is in the same directory or on PYTHONPATH
try:
    from ai_model import AIModel
    from llm_factory import BACKEND_GROQ, BACKEND_OLLAMA, get_llm_backend
except ImportError:
    try:
        from modules.ai_model import AIModel
        from modules.llm_factory import BACKEND_GROQ, BACKEND_OLLAMA, get_llm_backend
    except ImportError:
        print("Error: Could not import ai_model or llm_factory. Ensure modules/ are on PYTHONPATH.")
        sys.exit(1)


_PROVIDER_ALIAS = {
    "groq": BACKEND_GROQ,
    "deepseek": BACKEND_OLLAMA,
    "ollama": BACKEND_OLLAMA,
}

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║  LazyOwn AI Agent - Ultimate Edition                     ║
║  • Anti-Loop & Memory Management                         ║
║  • Threaded Execution with Timeout                       ║
║  • Argument Validation                                   ║
╚═══════════════════════════════════════════════════════════╝
"""

# ===== GLOBAL CONFIGURATION =====
MAX_OUTPUT_LENGTH = 3000  # Maximum characters per tool response
COMMAND_TIMEOUT = 60  # Maximum seconds to execute a command
MAX_HISTORY_MSGS = 15  # Memory window (messages)


def configure_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO
    configure(level=level, console=True, file=False)


# ===== ROBUST AGENT TOOL =====
class AgentTool:
    """Executable tool with validation and truncation."""

    def __init__(
        self, name: str, description: str, func: Callable, parameters: dict[str, Any], required: list[str] = None
    ):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = {"type": "object", "properties": parameters, "required": required or list(parameters.keys())}

    def to_api_format(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {"name": self.name, "description": self.description, "parameters": self.parameters},
        }

    def execute(self, **kwargs) -> str:
        """Execute with argument validation and clear formatting."""
        # 1. Argument validation
        try:
            sig = inspect.signature(self.func)
            # Only validate when the function accepts specific kwargs
            # (Wrapper functions usually accept generic **kwargs, but this helps when direct)
            bound = sig.bind_partial(**kwargs)
            bound.apply_defaults()
        except TypeError as e:
            msg = f"Parameter error invoking {self.name}: {e}"
            logging.error(msg)
            return msg

        # 2. Execution
        try:
            result = self.func(**kwargs)
            result_str = str(result)

            # 3. Output truncation (context management)
            if len(result_str) > MAX_OUTPUT_LENGTH:
                cut_len = len(result_str) - MAX_OUTPUT_LENGTH
                result_str = (
                    result_str[:MAX_OUTPUT_LENGTH]
                    + f"\n\n[... OUTPUT TRUNCATED: {cut_len} chars omitted to save memory ...]"
                )

            output = f"""[*] COMMAND EXECUTED: {self.name}
RESULT:
{result_str}

[END OF RESULT]"""

            logging.debug(f"[*] {self.name} executed successfully")
            return output

        except Exception as e:
            error_msg = f"[!] EXECUTION ERROR in {self.name}: {str(e)}"
            logging.error(error_msg)
            return error_msg


# ===== AST EXTRACTOR (no major changes) =====
@dataclass
class CommandMetadata:
    name: str
    docstring: str
    params: list[str]
    has_args: bool


class ASTToolExtractor:
    """Intelligent extractor using AST."""

    @staticmethod
    def extract_commands_from_file(file_path: str, prefix: str = "do_") -> list[CommandMetadata]:
        if not os.path.exists(file_path):
            logging.warning(f"File not found: {file_path}")
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError as e:
            logging.error(f"Syntax error in target script: {e}")
            return []

        commands = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith(prefix):
                cmd_name = node.name[len(prefix) :]
                docstring = ast.get_docstring(node) or f"Execute command {cmd_name}"

                params = []
                has_args = False
                for arg in node.args.args:
                    if arg.arg not in ("self", "cls"):
                        params.append(arg.arg)
                        if arg.arg in ("line", "args", "statement"):
                            has_args = True

                commands.append(
                    CommandMetadata(name=cmd_name, docstring=docstring.strip()[:500], params=params, has_args=has_args)
                )

        logging.info(f"Extracted {len(commands)} commands from shell.")
        return commands


# ===== AGENT RUNNER =====
def _tool_call_snapshot(tool_call) -> dict:
    """Flatten one SDK/SimpleNamespace tool call into a plain JSON dict.

    The raw object is not JSON-serializable, so persisting it in the
    conversation history breaks the ConversationStore save.
    """
    function = getattr(tool_call, "function", None)
    return {
        "id": str(getattr(tool_call, "id", "") or ""),
        "type": str(getattr(tool_call, "type", "function") or "function"),
        "function": {
            "name": str(getattr(function, "name", "") or ""),
            "arguments": str(getattr(function, "arguments", "") or ""),
        },
    }


class AgentRunner:
    """Agent engine with per-tool usage limit (anti-spam)."""

    def __init__(self, model: Any, system_prompt: str = None, max_iterations: int = 10):
        self.model = model
        self.max_iterations = max_iterations
        self.tools: dict[str, AgentTool] = {}
        self.conversation_history: list[dict[str, Any]] = []
        self.last_tool_calls = []

        # --- NEW: per-tool usage control ---
        self.tool_usage_count: dict[str, int] = {}
        self.executed_commands = set()

        self.system_prompt = system_prompt or "You are a helpful assistant."
        self._reset_history()

    def _reset_history(self):
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

    def _manage_memory(self):
        """Keep the context window clean."""
        MAX_HISTORY = 12
        if len(self.conversation_history) > MAX_HISTORY:
            logging.info("Trimming memory...")
            # Keep the system prompt and the latest messages
            self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-(MAX_HISTORY - 1) :]

    def register_tool(self, tool: AgentTool):
        self.tools[tool.name] = tool

    def register_tool_from_instance(self, func: Callable):
        """Wrap a plain function as an AgentTool using its signature and docstring."""
        sig = inspect.signature(func)
        parameters = {}
        required = []
        for pname, param in sig.parameters.items():
            parameters[pname] = {"type": "string", "description": f"Parameter {pname}"}
            if param.default is inspect.Parameter.empty:
                required.append(pname)
        tool = AgentTool(
            name=func.__name__,
            description=(func.__doc__ or func.__name__).strip(),
            func=func,
            parameters=parameters,
            required=required,
        )
        self.register_tool(tool)

    def register_tools_from_metadata(self, commands: list[CommandMetadata], executor: Callable[[str], str]):
        # (This part stays the same as in the previous implementation)
        for cmd in commands:

            def make_executor(cmd_name):
                def wrapper(command: str = "", **kwargs) -> str:
                    full_cmd = f"{cmd_name} {command}".strip()
                    return executor(full_cmd)

                return wrapper

            if cmd.has_args or not cmd.params:
                parameters = {"command": {"type": "string", "description": f"Arguments for {cmd.name}"}}
                required = ["command"]
            else:
                parameters = {p: {"type": "string", "description": f"Param {p}"} for p in cmd.params}
                required = cmd.params

            tool = AgentTool(
                name=f"cmd_{cmd.name}",
                description=cmd.docstring,
                func=make_executor(cmd.name),
                parameters=parameters,
                required=required,
            )
            self.register_tool(tool)

    def get_tools_for_api(self) -> list[dict[str, Any]] | None:
        if not self.tools:
            return None
        return [tool.to_api_format() for tool in self.tools.values()]

    def run(self, user_input: str) -> str:
        # Reset counters on every new main instruction
        self.conversation_history.append({"role": "user", "content": user_input})

        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            self._manage_memory()
            logging.info(f"STEP {iteration}/{self.max_iterations}")

            response = self._call_model()
            tool_calls = getattr(response.choices[0].message, "tool_calls", None)

            if not tool_calls:
                return response.choices[0].message.content

            # Process tool calls
            for tool_call in tool_calls:
                # Feed the result back into the history
                self._process_tool_call(tool_call)

        return f"Step limit reached ({self.max_iterations}). Review what you found."

    def _call_model(self):
        # Inject the anti-loop reminder dynamically if commands already ran
        current_context = list(self.conversation_history)

        # If nmap already ran, add a strong reminder
        if self.tool_usage_count.get("cmd_nmap", 0) > 0:
            current_context.append(
                {
                    "role": "system",
                    "content": "SYSTEM: You already scanned. Do NOT use nmap again. Analyze the open ports and use a different specific tool (e.g., curl, gobuster, smbclient) or give your final report.",
                }
            )

        candidates: list[str] = []
        try:
            from modules.llm_factory import groq_model_chain, is_model_missing_error

            candidates = [name for name in groq_model_chain() if name != self.model.model]
        except Exception:
            is_model_missing_error = None  # type: ignore[assignment]

        last_error: Exception | None = None
        for model_name in [self.model.model, *candidates]:
            try:
                if getattr(self, "stream_enabled", False):
                    response = self._stream_call(model_name, current_context)
                else:
                    response = self.model.client.chat.completions.create(
                        model=model_name,
                        messages=current_context,
                        tools=self.get_tools_for_api(),
                        tool_choice="auto",
                        temperature=0.1,
                    )
                self.model.model = model_name
                return response
            except Exception as e:
                last_error = e
                if is_model_missing_error is None or not is_model_missing_error(e):
                    logging.error(f"API error: {e}")
                    raise
                logging.warning(f"Model {model_name} unavailable, trying fallback")
        if last_error is not None:
            raise last_error
        raise RuntimeError("no model candidates available")

    def _stream_call(self, model_name: str, messages: list, max_tokens: int = 0):
        """One model turn with ``stream=True``, reassembling the reply.

        OpenAI-compatible streams deliver content, reasoning and tool
        calls as deltas. This assembles them back into the response
        shape the base loop expects and forwards content/reasoning
        fragments to ``delta_sink`` for live reporting.

        Args:
            model_name: Model id to call.
            messages: Conversation context.
            max_tokens: Optional token cap for providers that accept it.

        Returns:
            A response-like namespace with ``choices[0].message``.
        """
        from types import SimpleNamespace

        request: dict = {
            "model": model_name,
            "messages": messages,
            "tools": self.get_tools_for_api(),
            "tool_choice": "auto",
            "temperature": 0.1,
            "stream": True,
        }
        if max_tokens:
            request["max_tokens"] = max_tokens
        stream = self.model.client.chat.completions.create(**request)
        content_parts: list[str] = []
        think_parts: list[str] = []
        tool_parts: dict[int, dict] = {}
        for chunk in stream:
            choices = getattr(chunk, "choices", None) or []
            if not choices:
                continue
            delta = getattr(choices[0], "delta", None)
            if delta is None:
                continue
            content = getattr(delta, "content", None)
            if content:
                content_parts.append(str(content))
                self._emit_delta("delta", str(content))
            reasoning = getattr(delta, "reasoning_content", None)
            if reasoning:
                think_parts.append(str(reasoning))
            for call in getattr(delta, "tool_calls", None) or []:
                index = int(getattr(call, "index", 0) or 0)
                entry = tool_parts.setdefault(index, {"id": "", "name": "", "arguments": ""})
                call_id = getattr(call, "id", None)
                if call_id:
                    entry["id"] = str(call_id)
                function = getattr(call, "function", None)
                if function is not None:
                    part_name = getattr(function, "name", None)
                    if part_name:
                        entry["name"] += str(part_name)
                    part_args = getattr(function, "arguments", None)
                    if part_args:
                        entry["arguments"] += str(part_args)
        if think_parts:
            self._emit_delta("think", "".join(think_parts)[:1500])
        message = SimpleNamespace(content="".join(content_parts) or None, tool_calls=None)
        if tool_parts:
            message.tool_calls = [
                SimpleNamespace(
                    id=entry["id"] or f"call_{index}",
                    type="function",
                    function=SimpleNamespace(name=entry["name"], arguments=entry["arguments"]),
                )
                for index, entry in sorted(tool_parts.items())
            ]
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    def _emit_delta(self, kind: str, text: str) -> None:
        """Forward streamed fragments to the sink, throttled to one per second."""
        sink = getattr(self, "delta_sink", None)
        if sink is None:
            return
        state = getattr(self, "_delta_state", None)
        if state is None:
            state = {"chars": 0, "last": 0.0}
            self._delta_state = state
        state["chars"] += len(text or "")
        if kind == "think":
            sink(kind, f"reasoning: {text[:1200]}")
            return
        now = time.monotonic()
        if now - state["last"] < 1.0:
            return
        state["last"] = now
        sink(kind, f"streaming... {state['chars']} chars")

    def _process_tool_call(self, tool_call):
        tool_name = tool_call.function.name

        # --- IMPROVED ANTI-LOOP LOGIC ---
        # 1. Increment the global counter for that tool
        usage = self.tool_usage_count.get(tool_name, 0) + 1
        self.tool_usage_count[tool_name] = usage

        # 2. Check the hard limit (max 2 times per tool, nmap max 1)
        limit = 1 if "nmap" in tool_name else 2

        if usage > limit:
            logging.warning(f"Blocking {tool_name} (excessive use: {usage})")
            result = f"""SYSTEM: DO NOT RUN {tool_name} AGAIN.
You have already used this tool {usage - 1} times.
You must move forward. Use a different tool or finish the analysis.
If you already have the information, answer the user."""
        else:
            # Normal execution
            try:
                args = json.loads(tool_call.function.arguments)
            except (json.JSONDecodeError, TypeError) as exc:
                logging.warning("Failed to parse tool call arguments for %s: %s", tool_name, exc)
                args = {}

            # Check for an exact duplicate
            cmd_key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
            if cmd_key in self.executed_commands:
                result = "[!] ERROR: Command already executed exactly. Do not repeat."
            else:
                self.executed_commands.add(cmd_key)
                if tool_name in self.tools:
                    logging.info(f"Running {tool_name} (attempt {usage})")
                    result = self.tools[tool_name].execute(**args)
                else:
                    result = "Tool not found."

        # Store in history (flat snapshot: the raw SDK object is not
        # JSON-serializable and would break ConversationStore persistence).
        self.conversation_history.append(
            {"role": "assistant", "content": None, "tool_calls": [_tool_call_snapshot(tool_call)]}
        )
        self.conversation_history.append(
            {"role": "tool", "tool_call_id": tool_call.id, "name": tool_name, "content": result}
        )


# ===== SHELL WRAPPER WITH TIMEOUT =====
class LazyOwnShellWrapper:
    """Wrapper that executes commands in safe threads."""

    def __init__(self, script_path: str):
        self.script_path = os.path.abspath(script_path)
        self.script_dir = os.path.dirname(self.script_path)
        self.shell = None
        self.commands: list[CommandMetadata] = []
        self._load_shell()

    def _load_shell(self):
        self.commands = ASTToolExtractor.extract_commands_from_file(self.script_path)

        try:
            sys.path.insert(0, self.script_dir)
            spec = importlib.util.spec_from_file_location("lazyown", self.script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the shell class dynamically
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                # Look for a class with do_* methods
                if isinstance(attr, type) and any(m.startswith("do_") for m in dir(attr)):
                    self.shell = attr()
                    logging.info(f"Shell loaded successfully: {attr_name}")
                    break
        except Exception as e:
            logging.error(f"Error loading shell module: {e}")
        finally:
            if self.script_dir in sys.path:
                sys.path.remove(self.script_dir)

    def execute_command(self, command: str) -> str:
        """Execute a command with a timeout using threading."""
        if not self.shell:
            return "Shell unavailable"

        result_queue = queue.Queue()

        def target():
            capture = io.StringIO()
            try:
                with contextlib.redirect_stdout(capture):
                    if hasattr(self.shell, "onecmd_plus_hooks"):
                        self.shell.onecmd_plus_hooks(command)
                    elif hasattr(self.shell, "onecmd"):
                        self.shell.onecmd(command)
                    else:
                        print("Error: shell has no onecmd method")
                result_queue.put(capture.getvalue())
            except Exception as e:
                result_queue.put(f"Error executing command: {e}")

        # Start the thread
        t = threading.Thread(target=target)
        t.start()

        # Wait with the timeout
        t.join(timeout=COMMAND_TIMEOUT)

        if t.is_alive():
            logging.error(f"TIMEOUT in command: {command}")
            return f"TIMEOUT: command '{command}' exceeded {COMMAND_TIMEOUT} seconds. It may be waiting for input or hung."

        try:
            return result_queue.get_nowait() or "Command executed (no visible output)"
        except queue.Empty:
            return "[!] Unknown error: No response from thread."

    def get_commands_summary(self) -> str:
        # Simplified summary for the prompt
        names = [c.name for c in self.commands]
        return ", ".join(names[:50]) + ("..." if len(names) > 50 else "")


# ===== VULNBOT CLI =====
class VulnBotCLI:
    def __init__(self, provider: str, mode: str, debug: bool, script_path: str):
        self.provider = provider
        self.script_dir = os.getcwd()
        self.knowledge_base_file = "knowledge_base.json"

        configure_logging(debug)

        self.model = self._load_model()
        self.shell_wrapper = LazyOwnShellWrapper(script_path)
        self.agent = None
        self._setup_agent()

    def _load_model(self) -> AIModel:
        """Instantiate the LLM backend mapped to ``self.provider``.

        Returns:
            A configured :class:`AIModel` instance.

        Raises:
            LLMBackendNotSupportedError: When ``self.provider`` does not
                map to a known backend.
            LLMBackendUnavailableError: When the resolved backend cannot
                be constructed from the current environment.
        """
        backend = _PROVIDER_ALIAS.get(self.provider, self.provider)
        return get_llm_backend(backend=backend)

    def _setup_agent(self):
        total_cmds = len(self.shell_wrapper.commands)
        summary = self.shell_wrapper.get_commands_summary()

        # Improved prompt with ReAct logic (think before acting)
        system_prompt = f"""You are LazyOwn, an expert autonomous AI pentester.

OBJECTIVE: Analyze vulnerabilities and exploit them ethically.

TOOLS ({total_cmds} available):
{summary}

GOLDEN RULES:
1. THINKING (Thought): Before acting, briefly explain WHY you choose that tool.
2. ACCURACY: If a command fails, read the error and fix the arguments.
3. ANTI-LOOP: Never repeat the same command with the same arguments if you already have a result.
4. ECONOMY: Use at most 5 steps. If you have the information, finish with a summary.
5. SYNTAX: Use the provided functions to execute (e.g., cmd_nmap).

If the result is very long, focus on open ports or critical vulnerabilities.
"""
        self.agent = AgentRunner(self.model, system_prompt, max_iterations=8)

        if self.shell_wrapper.commands:
            self.agent.register_tools_from_metadata(self.shell_wrapper.commands, self.shell_wrapper.execute_command)
        else:
            logging.warning("No commands detected in provided file.")

    def process_request(self, user_input: str) -> str:
        return self.agent.run(user_input)


# ===== INTERACTIVE MODE =====
def interactive_mode(bot: VulnBotCLI):
    print("\n[Interactive LazyOwn Mode]")
    print("Enter your objective (e.g., 'Scan 10.10.10.5 and look for SMB')")
    print("Type 'exit' to finish.\n")

    while True:
        try:
            u_input = input("LazyOwn > ").strip()
            if u_input.lower() in ("exit", "quit"):
                break
            if not u_input:
                continue

            response = bot.process_request(u_input)
            print(f"\n[*] AGENT:\n{response}\n")
            print("-" * 60)

        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Main loop error: {e}")


# ===== MAIN =====
def parse_args():
    parser = argparse.ArgumentParser(description="LazyOwn AI Agent - Ultimate")
    parser.add_argument("--script", "-s", type=str, default="lazyown.py", help="Python script with a CMD class")
    parser.add_argument("--provider", "-p", default="groq", choices=["groq", "deepseek"])
    parser.add_argument("--debug", "-d", action="store_true")
    # Optional: direct instruction mode
    parser.add_argument("--instruction", "-i", type=str, help="Direct instruction (non-interactive)")
    return parser.parse_args()


def main():
    print(BANNER)
    args = parse_args()

    if not os.path.exists(args.script):
        print(f"Error: file does not exist: {args.script}")
        sys.exit(1)

    try:
        bot = VulnBotCLI(args.provider, "console", args.debug, args.script)

        if args.instruction:
            print(f"[*] Executing instruction: {args.instruction}")
            res = bot.process_request(args.instruction)
            print("\nFINAL RESULT:\n", res)
        else:
            interactive_mode(bot)

    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
