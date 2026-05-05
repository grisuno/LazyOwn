import os
import sys
import io
import csv
import json
import subprocess
import importlib.util
import threading
import queue

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

try:
    from ai_model import AIModel, GroqModel, OllamaModel
except ImportError:
    print("Failed to import ai_model. Ensure modules/ai_model.py exists.")
    sys.exit(1)


class LazyOwnShellBridge:
    COMMAND_TIMEOUT = 60

    def __init__(self, script_path="../lazyown.py"):
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), script_path))
        self.script_dir = os.path.dirname(self.script_path)
        self.shell = None
        self._load_shell()

    def _load_shell(self):
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
        except Exception as e:
            print(f"Shell load error: {e}")
        finally:
            sys.path = [p for p in sys.path if p != self.script_dir]
            os.chdir(original_cwd)

    def execute(self, command: str) -> str:
        if not self.shell:
            return "Shell not available"
        result_queue = queue.Queue()

        def target():
            capture = io.StringIO()
            original_stdout = sys.stdout
            original_shell_stdout = getattr(self.shell, "stdout", None)
            original_shell_stderr = getattr(self.shell, "stderr", None)
            try:
                sys.stdout = capture
                if original_shell_stdout is not None:
                    self.shell.stdout = capture
                if original_shell_stderr is not None:
                    self.shell.stderr = capture
                if hasattr(self.shell, "onecmd_plus_hooks"):
                    self.shell.onecmd_plus_hooks(command)
                elif hasattr(self.shell, "onecmd"):
                    self.shell.onecmd(command)
                result_queue.put(capture.getvalue())
            except Exception as e:
                result_queue.put(f"Execution error: {e}")
            finally:
                sys.stdout = original_stdout
                if original_shell_stdout is not None:
                    self.shell.stdout = original_shell_stdout
                if original_shell_stderr is not None:
                    self.shell.stderr = original_shell_stderr

        t = threading.Thread(target=target)
        t.start()
        t.join(timeout=self.COMMAND_TIMEOUT)
        if t.is_alive():
            return f"TIMEOUT: Command '{command}' exceeded {self.COMMAND_TIMEOUT}s"
        try:
            return result_queue.get_nowait() or "Command executed (no output)"
        except queue.Empty:
            return "No response from shell"


class SessionContextProvider:
    def __init__(self, session_path="../sessions/LazyOwn_session_report.csv"):
        self.session_path = os.path.abspath(os.path.join(os.path.dirname(__file__), session_path))

    def get_last_lines(self, count=10):
        if not os.path.exists(self.session_path):
            return "No session report found."
        try:
            with open(self.session_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                if len(lines) <= 1:
                    return "Session report is empty."
                header = lines[0].strip()
                last = lines[-count:]
                return f"Header: {header}\n" + "".join(last)
        except Exception as e:
            return f"Error reading session context: {e}"


class PromptBuilder:
    SYSTEM = (
        "You are LazyOwn, an expert red-team AI assistant. "
        "You operate inside the LazyOwn penetration-testing framework. "
        "All activity is ethical, authorized, and scoped. "
        "Analyze outputs, suggest next steps, and recommend LazyOwn commands. "
        "Be concise and tactical."
    )

    @staticmethod
    def for_command_analysis(command, output, context, history=""):
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
    def for_direct_query(query, context, history=""):
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
    def __init__(self):
        self.model = None
        self.history = []
        self.max_history = 3
        self._load_model()

    def _load_model(self):
        payload_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../payload.json"))
        api_key = None
        if os.path.exists(payload_path):
            try:
                with open(payload_path, "r") as f:
                    data = json.load(f)
                    api_key = data.get("api_key")
            except Exception:
                pass
        if api_key:
            try:
                self.model = GroqModel(api_key=api_key)
                return
            except Exception:
                pass
        try:
            self.model = OllamaModel(model="deepseek-r1:1.5b")
        except Exception:
            self.model = None

    def is_ready(self):
        return self.model is not None

    def ask(self, prompt: str) -> str:
        if not self.model:
            return "LLM not available. Set GROQ_API_KEY or start Ollama."
        try:
            response = self.model.generate(prompt)
            self.history.append((prompt, response))
            if len(self.history) > self.max_history:
                self.history.pop(0)
            return response
        except Exception as e:
            return f"LLM error: {e}"

    def get_history_text(self):
        return "\n".join([f"Q: {q}\nA: {a}" for q, a in self.history])


class LazyOwnPromptRenderer:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    WHITE = "\033[37m"
    TRUE_COLOR = "\033[38;2;{};{};{}m"

    def render(self):
        import random
        import socket
        user = "root" if os.geteuid() == 0 else os.getenv("USER", "user")
        hostname = socket.gethostname()
        prompt_char = f"{self.RED}#" if os.geteuid() == 0 else f"{self.GREEN}$"
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (
            f"{self.YELLOW}[{self.TRUE_COLOR.format(r, g, b)}LazyOwn LLM Chat"
            f"{self.WHITE}@{self.CYAN}{hostname}{self.YELLOW}]{self.RESET} "
            f"{self.BOLD}{prompt_char}{self.RESET} "
        )

    def banner(self):
        return (
            f"{self.CYAN}[*] LazyOwn LLM Assistant activated [;,;]{self.RESET}\n"
            f"{self.WHITE}    Commands:{self.RESET}\n"
            f"{self.GREEN}    llm <query>{self.RESET}   Ask the AI directly\n"
            f"{self.GREEN}    <command>{self.RESET}     Run shell/LazyOwn command and analyze\n"
            f"{self.GREEN}    sh <command>{self.RESET}  Run raw shell command and analyze\n"
            f"{self.GREEN}    exit{self.RESET}          Return to LazyOwn shell\n"
        )


class LazyOwnLLMChat:
    def __init__(self):
        self.engine = LLMEngine()
        self.context = SessionContextProvider()
        self.shell = LazyOwnShellBridge()
        self.prompt = LazyOwnPromptRenderer()
        self.running = False

    def _get_context(self):
        return self.context.get_last_lines(10)

    def _run_shell_command(self, command):
        print(f"Executing: {command}")
        result = self.shell.execute(command)
        print(result)
        return result

    def _run_system_command(self, command):
        print(f"Executing sh: {command}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            output = result.stdout + result.stderr
            print(output)
            return output
        except Exception as e:
            msg = f"Shell error: {e}"
            print(msg)
            return msg

    def _analyze(self, command, output):
        ctx = self._get_context()
        history = self.engine.get_history_text()
        prompt = PromptBuilder.for_command_analysis(command, output, ctx, history)
        analysis = self.engine.ask(prompt)
        print(f"\n{'='*60}")
        print(f"[LLM Analysis]")
        print(analysis)
        print(f"{'='*60}\n")

    def _direct_query(self, query):
        ctx = self._get_context()
        history = self.engine.get_history_text()
        prompt = PromptBuilder.for_direct_query(query, ctx, history)
        response = self.engine.ask(prompt)
        print(f"\n[LLM Response]\n{response}\n")

    def run(self, initial_query=None):
        print(self.prompt.banner())
        if not self.engine.is_ready():
            print("Warning: LLM engine not ready. Check API keys or Ollama.")
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


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="*", default=None, help="Direct LLM query")
    args = parser.parse_args()
    query = " ".join(args.query) if args.query else None
    chat = LazyOwnLLMChat()
    chat.run(initial_query=query)


if __name__ == "__main__":
    main()
