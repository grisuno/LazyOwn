"""Cloud attack command set.

Commands for cloud provider enumeration, metadata harvesting, storage
bucket discovery, and IAM reconnaissance across AWS, Azure, and GCP.
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.categories import miscellaneous_category
from utils import (
    BLUE,
    GREEN,
    RED,
    RESET,
    YELLOW,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)

CLOUD_CATEGORY = "17. Cloud Attacks"


class CloudCommandSet(LazyOwnCommandSet):
    """Cloud attack phase commands."""

    phase = "cloud"
    category = CLOUD_CATEGORY

    def _get_cloud_scanner(self):
        try:
            from modules.lazycloud import CloudScanner
            return CloudScanner(
                target_domain=self.params.get("domain", ""),
                timeout=float(self.params.get("cloud_timeout", 5.0)),
            )
        except ImportError as exc:
            print_error(f"Cloud module not available: {exc}")
            return None

    @cmd2.with_category(CLOUD_CATEGORY)
    def do_cloud_metadata(self, _line):
        """Harvest cloud instance metadata (AWS IMDS, Azure, GCP).

        Attempts to read cloud instance metadata from all three major
        providers. Discovers IAM credentials, SSH keys, user-data
        scripts, and managed identity tokens.

        Usage: cloud_metadata
        """
        scanner = self._get_cloud_scanner()
        if scanner is None:
            return

        print_msg(f"{BLUE}[*] Harvesting cloud metadata...{RESET}")
        results = scanner.quick_metadata()

        if not results:
            print_warn("No cloud metadata endpoints responded. Not running on a cloud instance.")
            return

        for result in results:
            provider = result.get("provider", "unknown").upper()
            print_succ(f"{GREEN}[+] {provider} metadata accessible{RESET}")
            metadata = result.get("metadata", {})
            for key, value in metadata.items():
                if isinstance(value, dict):
                    print_msg(f"    {key}: {json.dumps(value, indent=6)}")
                elif isinstance(value, str) and len(value) > 120:
                    print_msg(f"    {key}: {value[:120]}...")
                else:
                    print_msg(f"    {key}: {value}")

            credentials = result.get("credentials", {})
            if credentials:
                print_succ(f"{GREEN}[+] {provider} credentials harvested!{RESET}")
                for role, creds in credentials.items():
                    if isinstance(creds, dict):
                        print_msg(f"    Role: {role}")
                        print_msg(f"      AccessKeyId: {creds.get('AccessKeyId', 'N/A')[:20]}...")
                        print_msg(f"      Expiration: {creds.get('Expiration', 'N/A')}")
                    else:
                        print_msg(f"    Role: {role} -> {creds}")

                creds_file = os.path.join(self.params.get("sessions_dir", "sessions"), "cloud_credentials.txt")
                with open(creds_file, "w") as f:
                    json.dump(results, f, indent=2, default=str)
                print_succ(f"Credentials written to {creds_file}")

    @cmd2.with_category(CLOUD_CATEGORY)
    def do_cloud_buckets(self, line):
        """Enumerate cloud storage buckets for a given prefix.

        Checks AWS S3, Azure Blob Storage, and GCP Storage buckets
        derived from the target prefix for public accessibility.

        Usage:
            cloud_buckets <prefix>
            cloud_buckets mycompany
        """
        prefix = line.strip()
        if not prefix:
            domain = self.params.get("domain", "")
            if domain:
                prefix = domain.split(".")[0]
                print_msg(f"Using domain prefix: {prefix}")
            else:
                print_error("Usage: cloud_buckets <prefix>")
                return

        scanner = self._get_cloud_scanner()
        if scanner is None:
            return

        print_msg(f"{BLUE}[*] Enumerating cloud storage for prefix '{prefix}'...{RESET}")
        results = scanner.quick_buckets(prefix)

        if not results:
            print_warn("No buckets found.")
            return

        public = [r for r in results if r.get("public")]
        accessible = [r for r in results if r.get("accessible")]

        print_msg(f"{'='*70}")
        print_msg(f"  Buckets checked : {len(results)}")
        print_msg(f"  Accessible      : {len(accessible)}")
        print_msg(f"  Public          : {len(public)}")
        print_msg(f"{'='*70}")

        if public:
            print_succ(f"\n{GREEN}[+] PUBLIC BUCKETS:{RESET}")
            for bucket in public:
                print_msg(f"  {GREEN}{bucket.get('url', bucket.get('bucket', '?'))}{RESET}")
        if accessible and not public:
            print_msg(f"\n{YELLOW}[*] Accessible but not public:{RESET}")
            for bucket in accessible:
                print_msg(f"  {bucket.get('bucket', '?')}: {bucket.get('message', bucket.get('url', ''))}")

    @cmd2.with_category(CLOUD_CATEGORY)
    def do_cloud_scan(self, line):
        """Full cloud security scan: metadata + buckets + IAM enumeration.

        Usage:
            cloud_scan <prefix>
            cloud_scan mycompany
        """
        prefix = line.strip()
        if not prefix:
            domain = self.params.get("domain", "")
            if domain:
                prefix = domain.split(".")[0]
            else:
                prefix = self.params.get("rhost", "company").replace(".", "")

        scanner = self._get_cloud_scanner()
        if scanner is None:
            return

        print_msg(f"{BLUE}[*] Starting full cloud security scan for '{prefix}'...{RESET}")
        results = scanner.full_scan(
            target_prefix=prefix,
            sessions_dir=self.params.get("sessions_dir", "sessions"),
        )

        summary = results.get("summary", {})
        print_msg(f"{'='*70}")
        print_msg(f"  Cloud Scan Summary — {results.get('timestamp', '')}")
        print_msg(f"{'='*70}")
        print_msg(f"  Buckets checked        : {summary.get('total_buckets_checked', 0)}")
        print_msg(f"  Accessible buckets     : {summary.get('accessible_buckets', 0)}")
        print_msg(f"  Public buckets         : {summary.get('public_buckets', 0)}")
        print_msg(f"  Metadata providers     : {summary.get('metadata_providers_found', 0)}")
        print_msg(f"  Credentials harvested  : {summary.get('credentials_harvested', False)}")
        print_msg(f"  MITRE techniques       : {', '.join(summary.get('mitre_techniques', []))}")
        print_msg(f"{'='*70}")
        print_succ(f"Full results saved to sessions/cloud_scan_{prefix}.json")

    @cmd2.with_category(CLOUD_CATEGORY)
    def do_cloud_iam(self, _line):
        """Enumerate cloud IAM roles and policies.

        Attempts to enumerate IAM users, roles, and policies when
        valid cloud credentials are present in the environment.

        Usage: cloud_iam
        """
        print_msg(f"{BLUE}[*] Checking for cloud IAM enumeration capabilities...{RESET}")

        methods: list[tuple[str, str]] = []

        import os as _os
        if _os.environ.get("AWS_ACCESS_KEY_ID") and _os.environ.get("AWS_SECRET_ACCESS_KEY"):
            methods.append(("aws", "aws iam list-users && aws iam list-roles && aws iam list-policies --scope Local"))
        if _os.environ.get("AZURE_CLIENT_ID") and _os.environ.get("AZURE_CLIENT_SECRET"):
            methods.append(("azure", "az ad user list --query '[].{User:userPrincipalName}' -o table && az role definition list --query '[].{Role:roleName}' -o table"))
        if _os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or _os.path.exists(_os.path.expanduser("~/.config/gcloud/application_default_credentials.json")):
            methods.append(("gcp", "gcloud projects list && gcloud iam service-accounts list"))

        if not methods:
            print_warn("No cloud credentials found in environment.")
            print_msg("Set AWS_ACCESS_KEY_ID / AZURE_CLIENT_ID / GOOGLE_APPLICATION_CREDENTIALS to enable IAM enumeration.")
            return

        for provider, cmd in methods:
            print_succ(f"\n{GREEN}[+] {provider.upper()} credentials detected{RESET}")
            print_msg(f"  Command: {cmd}")
            ans = input(f"  Run {provider} IAM enumeration? [y/N]: ").strip().lower()
            if ans == "y":
                os.system(cmd)


import json


__all__ = ["CloudCommandSet"]
