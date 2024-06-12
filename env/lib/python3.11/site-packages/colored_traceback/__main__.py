import os
import sys
import colored_traceback

colored_traceback.add_hook()

# Check that a script was passed in.
if len(sys.argv) <= 1:
    raise SystemExit("Usage: python -m colored_traceback my_script.py")

# Check that the script exists.
script_path = sys.argv[1]
if not os.path.exists(script_path):
    raise SystemExit("Error: '%s' does not exist" % script_path)

# Replace colored_traceback's dir with script's dir in the module search path.
sys.path[0] = os.path.dirname(script_path)

# Remove colored_traceback from the arg list.
del sys.argv[0]

with open(script_path) as script_file:
    code = compile(script_file.read(), script_path, 'exec')
    variables = {}
    exec(code, variables, variables)
