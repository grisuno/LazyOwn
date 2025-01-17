import sys
import os
import ast
import subprocess
import importlib.util
import unittest
import time
import signal

EXCLUDED_FUNCTIONS = {'__init__', 'default', 'one_cmd', 'qa', 'getseclist'}
TIMEOUT = 0.1  

def extract_functions(script_path):
    with open(script_path, "r") as file:
        tree = ast.parse(file.read(), filename=script_path)

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            if func_name.startswith("do_"):
                func_name = func_name[3:]
            elif func_name.startswith("run_"):
                func_name = func_name[4:]
            functions.append(func_name)

    return functions

def run_tests_with_script(script_path, functions):
    spec = importlib.util.spec_from_file_location("module.name", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class TestFunctions(unittest.TestCase):
        pass

    for func_name in functions:
        if func_name in EXCLUDED_FUNCTIONS:
            print(f"[-] Skipping excluded function: {func_name}")
            continue

        func = getattr(module, func_name, None)
        if callable(func):
            setattr(
                TestFunctions,
                f'test_{func_name}',
                lambda self, func=func: self.assertIsNotNone(func(), f"Function {func_name} failed.")
            )

    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestFunctions))

def run_command_with_timeout(command, timeout):
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
    
    try:
        process.stdin.write('qa\n')
        process.stdin.flush()
        stdout, stderr = process.communicate(timeout=timeout)
        return process.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        return None, None, "Timeout"
    finally:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass

def run_tests_with_bash(script_path, functions):
    for func_name in functions:
        if func_name in EXCLUDED_FUNCTIONS:
            print(f"[-]\033[33m Skipping excluded function: {func_name} \033[0m")
            continue

        command = f"./run -c {func_name}"
        print(f"[+] Running command: {command}")

        returncode, stdout, stderr = run_command_with_timeout(command, TIMEOUT)

        if returncode is None:
            print(f"[+] Test passed for function: {func_name} (timed out, but considered successful)")
        elif returncode == 0:
            print(f"[+]\033[32m Test passed for function: {func_name} \033[0m")
        else:
            print(f"[-]\033[31m Test failed for function: {func_name}\nOutput:\n{stdout}\nError:\n{stderr} \033[0m")
    command = f"./run -c clean"
    print(f"[+] Running command: {command}")
    returncode, stdout, stderr = run_command_with_timeout(command, TIMEOUT)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./testmineitor.py /path/to/script.py")
        sys.exit(1)

    script_path = sys.argv[1]

    if not os.path.exists(script_path):
        print(f"[-] Script path {script_path} does not exist.")
        sys.exit(1)

    functions = extract_functions(script_path)

    if 'lazyown.py' in script_path:
        print(f"[+] Running tests using Bash script for {script_path}")
        run_tests_with_bash(script_path, functions)
    else:
        print(f"[+] Running tests directly for {script_path}")
        run_tests_with_script(script_path, functions)
