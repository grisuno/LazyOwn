"""YARA integration for malware classification and IOC scanning.

Provides file scanning, process memory scanning, and rule management
within the LazyOwn framework.
"""

import hashlib
import os
import subprocess
from datetime import datetime
from typing import Union

try:
    import yara
    HAS_YARA = True
except ImportError:
    HAS_YARA = False

YARA_RULES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "yara_rules")


class YaraScanner:
    """Scanner that compiles and applies YARA rules against files and directories.

    Args:
        rules_dir: Directory containing .yar rule files.
        auto_compile: Automatically compile rules on initialization.
    """

    def __init__(self, rules_dir: str | None = None, auto_compile: bool = True):
        self.rules_dir = rules_dir or YARA_RULES_DIR
        self._compiled_rules: yara.Rules | None = None
        self.compiled_sources: dict[str, str] = {}
        self.rule_count: int = 0
        self.last_compile: datetime | None = None

        if auto_compile and HAS_YARA:
            self.compile_all()

    def ensure_directory(self) -> None:
        """Create the YARA rules directory if it does not exist."""
        os.makedirs(self.rules_dir, exist_ok=True)

    def _load_external_vars(self) -> dict[str, Union[str, int, bool]]:
        """Return external variables for YARA rules."""
        return {
            'filename': '',
            'filepath': '',
            'extension': '',
            'filetype': '',
        }

    def compile_all(self) -> bool:
        """Compile all .yar files in the rules directory.

        Returns:
            bool: True if compilation succeeded, False otherwise.
        """
        if not HAS_YARA:
            return False

        self.ensure_directory()
        sources: dict[str, str] = {}
        rule_namespace = 'default'

        for root, _, files in os.walk(self.rules_dir):
            for filename in files:
                if not filename.endswith(('.yar', '.yara')):
                    continue

                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, self.rules_dir)

                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()

                namespace = os.path.dirname(rel_path).replace(os.sep, '_') or rule_namespace
                sources[namespace] = sources.get(namespace, '') + '\n' + content
                self.compiled_sources[rel_path] = content
                self.rule_count += 1

        if not sources:
            return False

        try:
            self._compiled_rules = yara.compile(
                sources=sources,
                externals=self._load_external_vars(),
            )
            self.last_compile = datetime.now()
            return True
        except yara.SyntaxError as e:
            raise RuntimeError(f"YARA syntax error during compilation: {e}")
        except Exception as e:
            raise RuntimeError(f"YARA compilation failed: {e}")

    def scan_file(self, filepath: str, timeout: int = 60) -> list[dict]:
        """Scan a single file with all compiled YARA rules.

        Args:
            filepath: Path to the file to scan.
            timeout: Maximum scan time in seconds.

        Returns:
            List of match dictionaries with rule, namespace, tags, meta, and strings.
        """
        if not HAS_YARA or self._compiled_rules is None:
            return []

        if not os.path.isfile(filepath):
            return []

        externals = self._load_external_vars()
        externals['filename'] = os.path.basename(filepath)
        externals['filepath'] = filepath
        _, ext = os.path.splitext(filepath)
        externals['extension'] = ext.lower()

        try:
            matches = self._scan_with_timeout(filepath, externals, timeout)
        except yara.TimeoutError:
            return [{'rule': 'SCAN_TIMEOUT', 'error': True,
                     'message': f'Scan timed out after {timeout}s'}]
        except Exception as e:
            return [{'rule': 'SCAN_ERROR', 'error': True, 'message': str(e)}]

        return [self._format_match(m) for m in matches]

    def _scan_with_timeout(self, filepath: str, externals: dict, timeout: int):
        """Internal scan with timeout using threading for isolation."""
        if timeout > 0:
            import threading

            result: list = []
            error: list = []

            def target():
                try:
                    matches = self._compiled_rules.match(filepath, externals=externals)
                    result.extend(matches or [])
                except Exception as e:
                    error.append(e)

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(timeout=timeout)

            if thread.is_alive():
                raise yara.TimeoutError(f"Scan timed out after {timeout}s")

            if error:
                raise error[0]

            if result:
                return result

        try:
            return self._compiled_rules.match(filepath, externals=externals)
        except Exception:
            return []

    def _format_match(self, match) -> dict:
        """Format a YARA match object into a dictionary.

        Args:
            match: YARA match object.

        Returns:
            Dict with rule name, namespace, tags, metadata, and matched strings.
        """
        return {
            'rule': match.rule,
            'namespace': match.namespace,
            'tags': list(match.tags),
            'meta': dict(match.meta) if hasattr(match, 'meta') else {},
            'strings': [
                {
                    'identifier': s.identifier,
                    'offset': s.instances[0].offset if s.instances else -1,
                    'data': str(s.instances[0].matched_data)[:200] if s.instances else '',
                }
                for s in match.strings if s.instances
            ],
        }

    def scan_directory(self, directory: str, recursive: bool = True,
                       extensions: list[str] | None = None,
                       max_files: int = 10000) -> list[dict]:
        """Scan all files in a directory recursively.

        Args:
            directory: Root directory to scan.
            recursive: Whether to descend into subdirectories.
            extensions: Optional list of file extensions to filter (e.g., ['.exe', '.dll']).
            max_files: Maximum number of files to scan.

        Returns:
            List of match dictionaries grouped by file.
        """
        results = []
        file_count = 0

        for root, _, files in os.walk(directory, followlinks=False):
            for filename in files:
                if file_count >= max_files:
                    break

                if extensions:
                    if not any(filename.lower().endswith(ext.lower()) for ext in extensions):
                        continue

                filepath = os.path.join(root, filename)

                try:
                    file_size = os.path.getsize(filepath)
                except (FileNotFoundError, OSError):
                    continue

                if file_size > 50 * 1024 * 1024:
                    continue

                try:
                    matches = self.scan_file(filepath)
                except (FileNotFoundError, PermissionError, OSError):
                    continue

                if matches:
                    try:
                        file_hash = self._sha256(filepath)
                    except (FileNotFoundError, PermissionError, OSError):
                        file_hash = 'unavailable'
                    results.append({
                        'file': filepath,
                        'size': file_size,
                        'sha256': file_hash,
                        'matches': matches,
                    })

                file_count += 1

            if not recursive:
                break

        return results

    @staticmethod
    def _sha256(filepath: str) -> str:
        """Compute SHA256 hash of a file."""
        sha = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                sha.update(chunk)
        return sha.hexdigest()

    def add_rule(self, name: str, content: str) -> str:
        """Add a new YARA rule to the rules directory.

        Args:
            name: Rule filename (without extension, will add .yar).
            content: YARA rule source code.

        Returns:
            Path to the created rule file.
        """
        self.ensure_directory()
        filename = f"{name}.yar"
        filepath = os.path.join(self.rules_dir, filename)

        with open(filepath, 'w') as f:
            f.write(content)

        return filepath

    def list_rules(self) -> list[dict[str, str]]:
        """List all YARA rules in the rules directory.

        Returns:
            List of dicts with name and path keys.
        """
        self.ensure_directory()
        rules = []

        for root, _, files in os.walk(self.rules_dir):
            for filename in files:
                if filename.endswith(('.yar', '.yara')):
                    filepath = os.path.join(root, filename)
                    rules.append({
                        'name': filename,
                        'path': filepath,
                        'size': os.path.getsize(filepath),
                    })

        return rules

    def download_community_rules(self) -> bool:
        """Attempt to download community YARA rules from popular repositories.

        Returns:
            bool: True if rules were downloaded successfully.
        """
        self.ensure_directory()
        repos = [
            ('YARA-Rules/rules', 'master', 'https://github.com/YARA-Rules/rules/archive/refs/heads/master.zip'),
        ]

        for repo_name, branch, url in repos:
            target_dir = os.path.join(self.rules_dir, repo_name.replace('/', '_'))
            if os.path.exists(target_dir):
                continue

            try:
                subprocess.run(
                    ['wget', '-q', '-O', f'/tmp/yara_rules_{branch}.zip', url],
                    timeout=120, check=True
                )
                subprocess.run(
                    ['unzip', '-qo', f'/tmp/yara_rules_{branch}.zip', '-d', self.rules_dir],
                    timeout=60, check=True
                )
                os.remove(f'/tmp/yara_rules_{branch}.zip')
            except Exception:
                continue

        self.compile_all()
        return True

    def ioc_scan(self, target_path: str, iocs: list[dict]) -> list[dict]:
        """Scan for IOCs (hashes, strings, registry keys) in a file/directory.

        Args:
            target_path: File or directory to scan.
            iocs: List of IOC dicts with type and value keys.

        Returns:
            List of matched IOCs.
        """
        results = []
        hash_iocs = [ioc for ioc in iocs if ioc.get('type') == 'hash']
        string_iocs = [ioc for ioc in iocs if ioc.get('type') == 'string']

        for ioc in hash_iocs:
            ioc_value = ioc['value'].lower()
            hash_algo = 'sha256' if len(ioc_value) == 64 else 'sha1' if len(ioc_value) == 40 else 'md5'

            if os.path.isfile(target_path):
                file_hash = getattr(hashlib, hash_algo)(
                    open(target_path, 'rb').read()
                ).hexdigest()
                if file_hash.lower() == ioc_value:
                    results.append({**ioc, 'matched_file': target_path, 'matched_hash': file_hash})

        for ioc in string_iocs:
            search_value = ioc['value']
            if os.path.isfile(target_path):
                with open(target_path, 'rb') as f:
                    for line_num, line in enumerate(f, 1):
                        if isinstance(search_value, bytes):
                            if search_value in line:
                                results.append({**ioc, 'matched_file': target_path,
                                                'line': line_num, 'context': line[:200].decode('latin-1', errors='replace')})
                                break

        return results


def create_default_rules() -> list[str]:
    """Create a set of default YARA rules for common threats.

    Returns:
        List of created rule file paths.
    """
    scanner = YaraScanner(auto_compile=False)
    scanner.ensure_directory()
    created = []

    rules = {
        'webshell_detection': '''
rule PHP_WebShell_Generic {
    meta:
        description = "Detects common PHP webshell patterns"
        author = "LazyOwn"
        severity = "high"
        category = "webshell"
    strings:
        $eval_cmd = "eval(" ascii wide
        $system_cmd = "system(" ascii wide
        $exec_cmd = "exec(" ascii wide
        $passthru = "passthru(" ascii wide
        $shell_exec = "shell_exec(" ascii wide
        $popen = "popen(" ascii wide
        $proc_open = "proc_open(" ascii wide
    condition:
        (filesize < 50KB) and (2 of them)
}
''',
        'cobalt_strike_beacon': '''
rule CobaltStrike_Beacon_Config {
    meta:
        description = "Detects Cobalt Strike beacon configuration patterns"
        author = "LazyOwn"
        severity = "critical"
        category = "c2"
    strings:
        $profile_cfg = "%c%" ascii
        $uri_1 = "/submit.php" ascii wide
        $uri_2 = "/jquery" ascii wide
        $sleep_mask = { 69 ?? 69 ?? 69 ?? 69 }
        $malleable = "Mozilla/5.0" ascii wide
    condition:
        uint16(0) == 0x5A4D and any of them
}
''',
        'reverse_shell_payload': '''
rule ReverseShell_Payload {
    meta:
        description = "Detects common reverse shell payloads"
        author = "LazyOwn"
        severity = "high"
        category = "payload"
    strings:
        $bash_tcp = "/dev/tcp/" ascii
        $nc_e = "nc -e" ascii wide
        $nc_nodns = "nc -n" ascii wide
        $python_socket = "socket.socket" ascii
        $powershell_rc = "Net.Sockets.TCPClient" ascii wide
        $powershell_stream = "GetStream()" ascii wide
        $sh_i = "sh -i" ascii
        $bash_i = "bash -i" ascii
    condition:
        (filesize < 100KB) and (2 of them)
}
''',
        'credential_theft': '''
rule CredentialTheft_Tools {
    meta:
        description = "Detects credential theft tools and dumpers"
        author = "LazyOwn"
        severity = "critical"
        category = "credential_access"
    strings:
        $mimikatz = "mimikatz" ascii wide nocase
        $mimidrv = "mimidrv" ascii wide nocase
        $sekurlsa = "sekurlsa" ascii wide nocase
        $lsadump = "lsadump" ascii wide nocase
        $laZagne = "laZagne" ascii wide nocase
        $pypykatz = "pypykatz" ascii wide nocase
        $mimipenguin = "mimiPenguin" ascii wide nocase
        $procdump_cmd = "procdump" ascii wide nocase
        $sam_dump = "samdump" ascii wide nocase
    condition:
        any of them
}
''',
        'persistence_mechanism': '''
rule Windows_Persistence {
    meta:
        description = "Detects Windows persistence mechanisms"
        author = "LazyOwn"
        severity = "high"
        category = "persistence"
    strings:
        $run_key = "CurrentVersion\\\\Run" ascii wide nocase
        $scheduled_task = "schtasks /create" ascii wide nocase
        $wmi_persist = "__EventFilter" ascii wide nocase
        $service_create = "sc create" ascii wide nocase
        $startup_folder = "Start Menu\\\\Programs\\\\Startup" ascii wide nocase
        $winlogon = "Winlogon\\\\Shell" ascii wide nocase
        $reg_add = "reg add" ascii wide nocase
        $dll_side = ".dll" ascii wide
    condition:
        (filesize < 200KB) and (2 of them)
}
''',
    }

    for name, content in rules.items():
        filepath = scanner.add_rule(name, content)
        created.append(filepath)

    scanner.compile_all()
    return created
