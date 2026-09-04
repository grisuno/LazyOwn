"""Mutation gate for C2 route-level auth boundaries.

Removes the ``@requires_auth_or_session`` guard from one representative
operator endpoint and asserts ``tests/test_c2_route_auth.py`` kills the
mutant. Survival means an operator surface can drift back to anonymous
without the suite noticing.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MUTATIONS = {
    "graph_unprotected": {
        "old": "@app.route('/graph')\n@requires_auth_or_session\n",
        "new": "@app.route('/graph')\n",
    },
    "config_json_unprotected": {
        "old": "@app.route('/config.json')\n@requires_auth_or_session\n",
        "new": "@app.route('/config.json')\n",
    },
}


def _run_tests() -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_c2_route_auth.py", "-q"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(BASE_DIR),
    )
    return result.returncode == 0


def main() -> int:
    path = BASE_DIR / "lazyc2.py"
    original = path.read_text(encoding="utf-8")
    backups: dict[str, str] = {}

    try:
        if not _run_tests():
            print("FAIL: baseline tests do not pass.")
            return 1
        print("PASS: baseline tests pass.")

        killed = 0
        survived = 0
        for name, mut in MUTATIONS.items():
            content = original
            if mut["old"] not in content:
                print(f"SKIP {name}: target not found.")
                continue
            path.write_text(content.replace(mut["old"], mut["new"], 1), encoding="utf-8")
            mutant_pass = _run_tests()
            path.write_text(original, encoding="utf-8")
            if mutant_pass:
                survived += 1
                print(f"SURVIVED {name}")
            else:
                killed += 1
                print(f"KILLED   {name}")

        print(f"Results: {killed} killed, {survived} survived")
        return 0 if survived == 0 else 1
    finally:
        path.write_text(original, encoding="utf-8")
        if _run_tests():
            print("Restored: baseline tests pass.")
        else:
            print("ERROR: restoration failed.")
            return 2


if __name__ == "__main__":
    sys.exit(main())
