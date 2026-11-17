"""Interactive LLM chat assistant for the LazyOwn shell.

Standalone companion launched by the ``llm`` LazyAddon
(``python3 lazyllmchat.py``). It drops the operator into an interactive
loop that runs LazyOwn or shell commands, reads the current session
context, and asks the configured LLM backend for tactical analysis and
next steps.

Backend selection is delegated to :func:`modules.llm_factory.try_get_llm_backend`,
so the assistant honours the single ``llm_backend`` key in
``payload.json`` (groq, ollama, openai, anthropic, deepseek, opencode or
auto) together with its model and API-key slots. No provider is
instantiated directly here.
"""

import contextlib
import importlib.util
import io
import os
import queue
import subprocess
import sys
import threading

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

try:
    from modules.llm_factory import load_payload, try_get_llm_backend
except ModuleNotFoundError:
    try:
        from llm_factory import load_payload, try_get_llm_backend
    except ModuleNotFoundError:
        print("Failed to import modules.llm_factory. Run from the LazyOwn repo.")
        sys.exit(1)

SHELL_COMMAND_TIMEOUT_SEC = 60
SYSTEM_COMMAND_TIMEOUT_SEC = 60
MAX_HISTORY_TURNS = 3
CONTEXT_TAIL_LINES = 10
SEPARATOR_WIDTH = 60


class LazyOwnShellBridge:
    """Load the LazyOwn cmd2 shell in-process and dispatch commands to it.

    The bridge imports ``lazyown.py`` without its persistent history so
    commands can be executed programmatically and their captured output
    returned as a string.
    """

    def __init__(self, script_path: str = "../lazyown.py") -> None:
        """Resolve the shell module path and load the shell instance.

        Args:
            script_path: Path to ``lazyown.py`` relative to this module.
        """
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), script_path))
        self.script_dir = os.path.dirname(self.script_path)
        self.shell = None
        self._load_shell()

    def _load_shell(self) -> None:
        """Import the LazyOwn shell class and instantiate it once."""
        original_cwd = os.getcwd()
        os.chdir(self.script_dir)
        try:
            import cmd2
            original_init = cmd2.Cmd.__init__

            def no_history_init(self_, *args, **kwargs):
                kwargs.pop("startup_script", None)
                kwargs.pop("persistent_history_file", None)
                return original_init(self_, *args, **kwargs)

            cmd2.Cmd.__init__ = no_history_init
            sys.path.insert(0, self.script_dir)
            spec = importlib.util.spec_from_file_location("lazyown", self.script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and any(m.startswith("do_") for m in dir(attr)):
                    try:
                        self.shell = attr()
                    except Exception:
                        pass
                    break

            cmd2.Cmd.__init__ = original_init
        except Exception as exc:
            print(f"Shell load error: {exc}")
        finally:
            sys.path = [p for p in sys.path if p != self.script_dir]
            os.chdir(original_cwd)

    def execute(self, command: str) -> str:
        """Run a command through the loaded shell and capture its output.

        Args:
            command: The LazyOwn or shell command line to dispatch.

        Returns:
            Captured stdout text, a timeout notice, or an error string.
        """
        if not self.shell:
            return "Shell not available"
        result_queue: queue.Queue = queue.Queue()

        def target():
            capture = io.StringIO()
            original_shell_stdout = getattr(self.shell, "stdout", None)
            original_shell_stderr = getattr(self.shell, "stderr", None)
            try:
                with contextlib.redirect_stdout(capture):
                    if original_shell_stdout is not None:
                        self.shell.stdout = capture
                    if original_shell_stderr is not None:
                        self.shell.stderr = capture
                    if hasattr(self.shell, "onecmd_plus_hooks"):
                        self.shell.onecmd_plus_hooks(command)
                    elif hasattr(self.shell, "onecmd"):
                        self.shell.onecmd(command)
                    result_queue.put(capture.getvalue())
            except Exception as exc:
                result_queue.put(f"Execution error: {exc}")
            finally:
                if original_shell_stdout is not None:
                    self.shell.stdout = original_shell_stdout
                if original_shell_stderr is not None:
                    self.shell.stderr = original_shell_stderr

        worker = threading.Thread(target=target)
        worker.start()
        worker.join(timeout=SHELL_COMMAND_TIMEOUT_SEC)
        if worker.is_alive():
            return f"TIMEOUT: Command '{command}' exceeded {SHELL_COMMAND_TIMEOUT_SEC}s"
        try:
            return result_queue.get_nowait() or "Command executed (no output)"
        except queue.Empty:
            return "No response from shell"


class SessionContextProvider:
    """Provide the tail of the LazyOwn session report as model context."""

    def __init__(self, session_path: str = "../sessions/LazyOwn_session_report.csv") -> None:
        """Resolve the session report path relative to this module.

        Args:
            session_path: Path to the CSV session report.
        """
        self.session_path = os.path.abspath(os.path.join(os.path.dirname(__file__), session_path))

    def get_last_lines(self, count: int = CONTEXT_TAIL_LINES) -> str:
        """Return the header plus the last ``count`` report rows.

        Args:
            count: Number of trailing rows to include.

        Returns:
            A human-readable context block, or a notice when the report
            is missing or empty.
        """
        if not os.path.exists(self.session_path):
            return "No session report found."
        try:
            with open(self.session_path, "r", encoding="utf-8", errors="ignore") as handle:
                lines = handle.readlines()
            if len(lines) <= 1:
                return "Session report is empty."
            header = lines[0].strip()
            last = lines[-count:]
            return f"Header: {header}\n" + "".join(last)
        except Exception as exc:
            return f"Error reading session context: {exc}"


class PromptBuilder:
    """Assemble system-grounded prompts for analysis and direct queries."""

    SYSTEM = (
        "You are LazyOwn, an expert red-team AI assistant. "
        "You operate inside the LazyOwn penetration-testing framework. "
        "All activity is ethical, authorized, and scoped. "
        "Analyze outputs, suggest next steps, and recommend LazyOwn commands. "
        "Be concise and tactical."
    )

    @staticmethod
    def for_command_analysis(command: str, output: str, context: str, history: str = "") -> str:
        """Build a prompt that asks the model to analyze command output.

        Args:
            command: The command that was executed.
            output: Captured output from the command.
            context: Recent session context block.
            history: Prior analysis turns, if any.

        Returns:
            The assembled prompt string.
        """
        prompt = f"{PromptBuilder.SYSTEM}\n\n"
        if context:
            prompt += f"Recent session context:\n{context}\n\n"
        if history:
            prompt += f"Previous analysis:\n{history}\n\n"
        prompt += f"Command executed: {command}\n"
        prompt += f"Output:\n{output}\n\n"
        prompt += (
            "Provide a brief tactical analysis: key findings, risks, "
            "and the next 1-3 LazyOwn commands or shell actions to run. "
            "If the output is empty, note that."
        )
        return prompt

    @staticmethod
    def for_direct_query(query: str, context: str, history: str = "") -> str:
        """Build a prompt for a free-form operator query.

        Args:
            query: The operator's question.
            context: Recent session context block.
            history: Prior analysis turns, if any.

        Returns:
            The assembled prompt string.
        """
        prompt = f"{PromptBuilder.SYSTEM}\n\n"
        if context:
            prompt += f"Recent session context:\n{context}\n\n"
        if history:
            prompt += f"Previous analysis:\n{history}\n\n"
        prompt += f"Operator query: {query}\n\n"
        prompt += (
            "Answer the query with tactical recommendations. "
            "Suggest relevant LazyOwn commands if applicable."
        )
        return prompt


class LLMEngine:
    """Resolve the configured backend and answer prompts with history.

    The backend is obtained from
    :func:`modules.llm_factory.try_get_llm_backend`, so the ``llm_backend``
    key in ``payload.json`` selects the provider (including opencode and
    anthropic) and the budget proxy is applied transparently.
    """

    def __init__(self) -> None:
        """Load the backend and initialize the rolling history buffer."""
        self.model = None
        self.history: list[tuple[str, str]] = []
        self.max_history = MAX_HISTORY_TURNS
        self._load_model()

    def _load_model(self) -> None:
        """Select a backend through the factory, degrading to ``None``."""
        try:
            config = load_payload()
        except Exception:
            config = None
        self.model = try_get_llm_backend(config=config)

    def is_ready(self) -> bool:
        """Report whether a usable backend was resolved.

        Returns:
            True when a backend is available.
        """
        return self.model is not None

    def ask(self, prompt: str) -> str:
        """Send a prompt to the backend and record the exchange.

        Args:
            prompt: The fully assembled prompt.

        Returns:
            The model response, or a guidance string when no backend is
            available or the call fails.
        """
        if not self.model:
            return (
                "LLM not available. Set 'llm_backend' and the matching API key "
                "in payload.json, or start Ollama for a local backend."
            )
        try:
            response = self.model.generate(prompt)
            self.history.append((prompt, response))
            if len(self.history) > self.max_history:
                self.history.pop(0)
            return response
        except Exception as exc:
            return f"LLM error: {exc}"

    def get_history_text(self) -> str:
        """Return the rolling history formatted for prompt inclusion.

        Returns:
            A newline-joined transcript of recent prompt/response pairs.
        """
        return "\n".join(f"Q: {q}\nA: {a}" for q, a in self.history)


class LazyOwnPromptRenderer:
    """Render the ANSI prompt line and the activation banner."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    WHITE = "\033[37m"
    TRUE_COLOR = "\033[38;2;{};{};{}m"
    COLOR_MAX = 255

    def render(self) -> str:
        """Build the per-turn colored prompt string.

        Returns:
            The ANSI-decorated prompt the input loop displays.
        """
        import random
        import socket

        hostname = socket.gethostname()
        prompt_char = f"{self.RED}#" if os.geteuid() == 0 else f"{self.GREEN}$"
        red = random.randint(0, self.COLOR_MAX)
        green = random.randint(0, self.COLOR_MAX)
        blue = random.randint(0, self.COLOR_MAX)
        return (
            f"{self.YELLOW}[{self.TRUE_COLOR.format(red, green, blue)}LazyOwn LLM Chat"
            f"{self.WHITE}@{self.CYAN}{hostname}{self.YELLOW}]{self.RESET} "
            f"{self.BOLD}{prompt_char}{self.RESET} "
        )

    def banner(self) -> str:
        """Return the help banner shown on activation.

        Returns:
            The multi-line banner string.
        """
        return (
            f"{self.CYAN}[*] LazyOwn LLM Assistant activated [;,;]{self.RESET}\n"
            f"{self.WHITE}    Commands:{self.RESET}\n"
            f"{self.GREEN}    llm <query>{self.RESET}   Ask the AI directly\n"
            f"{self.GREEN}    <command>{self.RESET}     Run shell/LazyOwn command and analyze\n"
            f"{self.GREEN}    sh <command>{self.RESET}  Run raw shell command and analyze\n"
            f"{self.GREEN}    exit{self.RESET}          Return to LazyOwn shell\n"
        )


class LazyOwnLLMChat:
    """Interactive loop tying the shell, context, backend and renderer."""

    def __init__(self) -> None:
        """Construct the collaborators the interactive loop relies on."""
        self.engine = LLMEngine()
        self.context = SessionContextProvider()
        self.shell = LazyOwnShellBridge()
        self.prompt = LazyOwnPromptRenderer()
        self.running = False

    def _get_context(self) -> str:
        """Return the current session context tail."""
        return self.context.get_last_lines(CONTEXT_TAIL_LINES)

    def _run_shell_command(self, command: str) -> str:
        """Dispatch a command through the LazyOwn shell and echo output.

        Args:
            command: The LazyOwn or shell command line.

        Returns:
            The captured output.
        """
        print(f"Executing: {command}")
        result = self.shell.execute(command)
        print(result)
        return result

    def _run_system_command(self, command: str) -> str:
        """Run a raw shell command in a subprocess and echo output.

        Args:
            command: The raw shell command line.

        Returns:
            Combined stdout and stderr, or an error string.
        """
        print(f"Executing sh: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=SYSTEM_COMMAND_TIMEOUT_SEC,
            )
            output = result.stdout + result.stderr
            print(output)
            return output
        except Exception as exc:
            message = f"Shell error: {exc}"
            print(message)
            return message

    def _analyze(self, command: str, output: str) -> None:
        """Ask the backend to analyze a command's output and print it.

        Args:
            command: The command that produced the output.
            output: The captured command output.
        """
        ctx = self._get_context()
        history = self.engine.get_history_text()
        prompt = PromptBuilder.for_command_analysis(command, output, ctx, history)
        analysis = self.engine.ask(prompt)
        print("\n" + "=" * SEPARATOR_WIDTH)
        print("[LLM Analysis]")
        print(analysis)
        print("=" * SEPARATOR_WIDTH + "\n")

    def _direct_query(self, query: str) -> None:
        """Answer a free-form operator query and print the response.

        Args:
            query: The operator's question.
        """
        ctx = self._get_context()
        history = self.engine.get_history_text()
        prompt = PromptBuilder.for_direct_query(query, ctx, history)
        response = self.engine.ask(prompt)
        print(f"\n[LLM Response]\n{response}\n")

    def run(self, initial_query: str | None = None) -> None:
        """Run the interactive assistant loop until the operator exits.

        Args:
            initial_query: Optional query answered before the loop starts.
        """
        print(self.prompt.banner())
        if not self.engine.is_ready():
            print("Warning: LLM engine not ready. Check 'llm_backend' and API keys or Ollama.")
        self.running = True
        if initial_query:
            self._direct_query(initial_query)
        while self.running:
            try:
                user_input = input(self.prompt.render()).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting LLM chat.")
                break
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Returning to LazyOwn shell...")
                break
            if user_input.lower().startswith("llm "):
                self._direct_query(user_input[4:].strip())
                continue
            if user_input.lower().startswith("sh "):
                output = self._run_system_command(user_input[3:].strip())
            else:
                output = self._run_shell_command(user_input)
            if output.strip():
                self._analyze(user_input, output)


def main() -> None:
    """Parse arguments and launch the interactive assistant."""
    import argparse

    parser = argparse.ArgumentParser(description="LazyOwn interactive LLM chat assistant.")
    parser.add_argument("query", nargs="*", default=None, help="Direct LLM query")
    args = parser.parse_args()
    query = " ".join(args.query) if args.query else None
    chat = LazyOwnLLMChat()
    chat.run(initial_query=query)


if __name__ == "__main__":
    main()
