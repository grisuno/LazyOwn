"""Red Team Gym — gamified pentest training mode.

Integrates with the existing ELO/karma system in
:mod:`cli.engagement_hooks` and extends :mod:`cli.commands.lab`
Docker scenarios with challenge objectives, scoring, and leaderboards.

Each challenge defines a specific objective, success criteria, a
time-based speed score, a stealth score (based on techniques that
avoid EDR triggers), and a technique-diversity bonus.

Completion awards bonus ELO that is added via the existing
``aumentar_elo`` / ``_award_elo`` pipeline.

Definitions are YAML files under ``gyms/`` (see :mod:`modules.gym_registry`).
Active runs are persisted in the world model, so status and stop work
across sessions and are addressable by stable run ids.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from modules.gym_registry import (
    create_definition,
    delete_definition,
    get_active_runs,
    load_definitions,
    pop_run,
    scan_definitions,
    start_run,
    stop_runs,
    update_definition_yaml,
)

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
GYM_DIR = SESSIONS_DIR / "gym"
GYM_LEADERBOARD = GYM_DIR / "leaderboard.json"
GYM_CHALLENGES = GYM_DIR / "challenges.json"


GYM_DEFAULT_DEFINITIONS: dict[str, dict[str, Any]] = {
    "first_blood_web": {
        "id": "first_blood_web",
        "name": "First Blood — Web",
        "description": "Exploit the DVWA SQL Injection page without using sqlmap. Dump the users table manually.",
        "scenario": "wordpress",
        "objective": "Extract all rows from the 'users' table via manual SQL injection.",
        "difficulty": "easy",
        "phases": ["enum", "exploit"],
        "required_techniques": ["sqli_manual"],
        "bonus_techniques": ["csrf_bypass", "waf_bypass"],
        "max_points": 1000,
        "speed_bonus_max": 300,
        "stealth_bonus_max": 200,
        "technique_diversity_bonus": 200,
        "hints": [
            "Try: ' OR '1'='1",
            "Use UNION SELECT to enumerate columns",
            "Check information_schema.tables",
        ],
        "success_check": "SELECT user,password FROM users",
        "elo_bonus": 150,
    },
    "first_blood_smb": {
        "id": "first_blood_smb",
        "name": "First Blood — SMB",
        "description": "Enumerate SMB shares on Metasploitable2, find a writable share, and upload a reverse shell.",
        "scenario": "metasploitable",
        "chain": "gym_metasploitable_samba_usermap",
        "objective": "List all SMB shares, find writable one, upload a payload.",
        "difficulty": "easy",
        "phases": ["enum", "exploit"],
        "required_techniques": ["smb_enum", "payload_upload"],
        "bonus_techniques": ["reverse_shell", "persistence"],
        "max_points": 1000,
        "speed_bonus_max": 300,
        "stealth_bonus_max": 200,
        "technique_diversity_bonus": 200,
        "hints": [
            "smbclient -L //RHOST",
            "Check for 'tmp' or 'opt' share",
            "Use smbmap or enum4linux",
        ],
        "success_check": "writable share found and payload uploaded",
        "elo_bonus": 150,
    },
    "ad_kerberoast": {
        "id": "ad_kerberoast",
        "name": "Kerberoast the Domain",
        "description": "In the AD lab, enumerate domain users, find a user with SPN set, request a TGS, and crack it offline.",
        "scenario": "ad-lab",
        "objective": "Kerberoast a domain account and crack the TGS hash.",
        "difficulty": "medium",
        "phases": ["enum", "cred"],
        "required_techniques": ["kerberoast", "hash_crack"],
        "bonus_techniques": ["asreproast", "bloodhound_enum", "ldap_enum"],
        "max_points": 1500,
        "speed_bonus_max": 400,
        "stealth_bonus_max": 300,
        "technique_diversity_bonus": 400,
        "hints": [
            "GetNPUsers.py or look for users without preauth",
            "GetUserSPNs.py for kerberoastable accounts",
            "hashcat -m 13100 for TGS hashes",
            "BloodHound: Find Shortest Path to Domain Admins",
        ],
        "success_check": "TGS hash cracked",
        "elo_bonus": 300,
    },
    "juice_shop_xss": {
        "id": "juice_shop_xss",
        "name": "Juice Shop XSS Chain",
        "description": "Find and exploit a stored XSS in Juice Shop to steal another user's session, then escalate to admin.",
        "scenario": "juice-shop",
        "objective": "Chain stored XSS to session theft and admin access.",
        "difficulty": "medium",
        "phases": ["enum", "exploit", "cred"],
        "required_techniques": ["xss_stored", "session_hijack"],
        "bonus_techniques": ["csrf", "idor", "sqli"],
        "max_points": 1500,
        "speed_bonus_max": 400,
        "stealth_bonus_max": 300,
        "technique_diversity_bonus": 400,
        "hints": [
            "The search bar and feedback form are good places to start",
            "Try <img src=x onerror=alert(document.cookie)>",
            "Check /administration after getting admin cookie",
        ],
        "success_check": "admin session cookie obtained",
        "elo_bonus": 250,
    },
    "metasploitable_full_chain": {
        "id": "metasploitable_full_chain",
        "name": "Full Kill-Chain: Metasploitable",
        "description": "Complete the full kill-chain against Metasploitable2: recon, enum, exploit, post-exploit, privesc, and exfil.",
        "scenario": "metasploitable",
        "objective": "Gain root on Metasploitable2 and exfiltrate /etc/shadow.",
        "difficulty": "hard",
        "phases": ["recon", "enum", "exploit", "postexp", "privesc", "exfil"],
        "required_techniques": ["service_enum", "exploit", "privesc_linux", "data_exfil"],
        "bonus_techniques": ["persistence", "pivoting", "log_cleanup"],
        "max_points": 3000,
        "speed_bonus_max": 600,
        "stealth_bonus_max": 500,
        "technique_diversity_bonus": 900,
        "hints": [
            "Nmap shows many vulnerable services",
            "vsftpd 2.3.4 has a well-known backdoor",
            "Distccd and UnrealIRCd are also vulnerable",
            "After shell: try 'uname -a' and check kernel exploits",
        ],
        "success_check": "root shell and /etc/shadow contents obtained",
        "elo_bonus": 500,
    },
    "tomcat_rce": {
        "id": "tomcat_rce",
        "name": "Tomcat Manager RCE",
        "description": "Bruteforce Tomcat Manager credentials, deploy a WAR reverse shell, and get command execution.",
        "scenario": "tomcat",
        "chain": "gym_metasploitable_ms2_tomcat_manager",
        "objective": "Deploy a malicious WAR file via Tomcat Manager and get a reverse shell.",
        "difficulty": "medium",
        "phases": ["enum", "exploit"],
        "required_techniques": ["cred_bruteforce", "war_deploy"],
        "bonus_techniques": ["reverse_shell", "jsp_shell"],
        "max_points": 1200,
        "speed_bonus_max": 350,
        "stealth_bonus_max": 250,
        "technique_diversity_bonus": 300,
        "hints": [
            "Default creds: tomcat:s3cret or admin:admin",
            "Use msfvenom to create a WAR payload",
            "Deploy via /manager/html or /manager/text",
        ],
        "success_check": "reverse shell obtained from deployed WAR",
        "elo_bonus": 200,
    },
    "struts_ognl": {
        "id": "struts_ognl",
        "name": "Struts OGNL Injection",
        "description": "Exploit CVE-2017-5638 (OGNL injection) on Apache Struts2 to achieve RCE.",
        "scenario": "struts",
        "objective": "Execute arbitrary commands via OGNL injection and get a reverse shell.",
        "difficulty": "hard",
        "phases": ["enum", "exploit"],
        "required_techniques": ["cve_exploit", "command_injection"],
        "bonus_techniques": ["reverse_shell", "waf_bypass"],
        "max_points": 1500,
        "speed_bonus_max": 400,
        "stealth_bonus_max": 300,
        "technique_diversity_bonus": 400,
        "hints": [
            "Content-Type header is the injection point",
            "OGNL expression: %{(#_='multipart/form-data')...}",
            "Search for CVE-2017-5638 PoCs on exploit-db",
        ],
        "success_check": "RCE via OGNL injection achieved",
        "elo_bonus": 300,
    },
    "stealth_no_scan": {
        "id": "stealth_no_scan",
        "name": "Ghost Protocol",
        "description": "Complete the Metasploitable full chain WITHOUT running any port scanner (nmap, masscan, etc.). Use only passive recon and targeted probing.",
        "scenario": "metasploitable",
        "objective": "Root the box without ever running a full port scan. Use banner grabbing, targeted connections, OSINT.",
        "difficulty": "hard",
        "phases": ["recon", "enum", "exploit", "postexp", "privesc"],
        "required_techniques": ["passive_recon", "banner_grab", "targeted_exploit"],
        "bonus_techniques": ["osint", "social_eng", "living_off_land"],
        "max_points": 3500,
        "speed_bonus_max": 500,
        "stealth_bonus_max": 1200,
        "technique_diversity_bonus": 800,
        "hints": [
            "curl, netcat, telnet — one port at a time",
            "Check /robots.txt on port 80",
            "What services run on common ports by convention?",
            "Searchsploit for known services on Metasploitable2",
        ],
        "success_check": "root without running nmap or masscan",
        "elo_bonus": 600,
    },
    "first_implant": {
        "id": "first_implant",
        "name": "First Implant — Range",
        "description": "Deploy the Go beacon to ws01 (172.20.0.20) in the ad-mini range and get a callback on the C2.",
        "scenario": "ad-mini",
        "objective": "Build the beacon with redirector fallback URLs, deliver it to ws01, and receive a beacon callback.",
        "difficulty": "easy",
        "phases": ["c2", "exploit"],
        "required_techniques": ["implant_deploy", "beacon_callback"],
        "bonus_techniques": ["redirector_use", "persistence"],
        "max_points": 1000,
        "speed_bonus_max": 300,
        "stealth_bonus_max": 200,
        "technique_diversity_bonus": 200,
        "hints": [
            "lab range start ad-mini, then lab range verify ad-mini to prove root",
            "Get a root shell: USER backdoor:) / PASS anything on 127.0.0.1:2121, shell lands on 127.0.0.1:6200",
            "Or login: ssh -p 2222 msfadmin@127.0.0.1 (password msfadmin)",
            "From the shell, curl the beacon from your C2 (/s/<binary>) and run it",
            "Check c2_beacons for the callback",
        ],
        "success_check": "beacon callback visible in c2_beacons",
        "elo_bonus": 150,
    },
    "lateral_ad": {
        "id": "lateral_ad",
        "name": "Lateral Move — Range AD",
        "description": "From the ws01 implant, enumerate the range DC and move laterally with SMB/WinRM techniques.",
        "scenario": "ad-mini",
        "objective": "Enumerate shares/users on 172.20.0.10 and achieve lateral execution to the DC.",
        "difficulty": "medium",
        "phases": ["enum", "lateral", "cred"],
        "required_techniques": ["smb_enum", "lateral_movement"],
        "bonus_techniques": ["kerberoast", "pth", "bloodhound_enum"],
        "max_points": 1500,
        "speed_bonus_max": 400,
        "stealth_bonus_max": 300,
        "technique_diversity_bonus": 400,
        "hints": [
            "Use the beacon portscan + smbclient against 172.20.0.10",
            "Look for weakRangeAdmin credentials in shares",
            "wmiexec/psexec style lateral techniques apply here",
        ],
        "success_check": "command execution on the range DC",
        "elo_bonus": 300,
    },
    "vault_exfil": {
        "id": "vault_exfil",
        "name": "Vault Exfil — Range",
        "description": "Use QuantumVault tradecraft from the range implant to stage and exfiltrate a loot bundle.",
        "scenario": "ad-mini",
        "objective": "Stage /etc/shadow equivalent loot on ws01 and exfiltrate it through the beacon.",
        "difficulty": "medium",
        "phases": ["exfil", "c2"],
        "required_techniques": ["data_staging", "data_exfil"],
        "bonus_techniques": ["compression", "encryption", "log_cleanup"],
        "max_points": 1500,
        "speed_bonus_max": 400,
        "stealth_bonus_max": 300,
        "technique_diversity_bonus": 400,
        "hints": [
            "Stage loot under /tmp on ws01 first",
            "Use the beacon upload/exfil path, not scp",
            "Clean logs after exfil for the stealth bonus",
        ],
        "success_check": "loot bundle received in sessions/uploads",
        "elo_bonus": 300,
    },
}


def reload_challenge_definitions(directory: Path | str | None = None) -> dict[str, dict[str, Any]]:
    """Reload YAML definitions, falling back to the embedded catalogue.

    Args:
        directory: Override for tests; defaults to ``gyms/``.

    Returns:
        The active definition mapping.
    """
    global GYM_CHALLENGE_DEFINITIONS
    loaded = load_definitions(directory)
    GYM_CHALLENGE_DEFINITIONS = loaded or GYM_DEFAULT_DEFINITIONS
    return GYM_CHALLENGE_DEFINITIONS


GYM_CHALLENGE_DEFINITIONS = load_definitions() or GYM_DEFAULT_DEFINITIONS


@dataclass
class GymAttempt:
    """A single challenge attempt with scoring."""

    challenge_id: str
    username: str
    started_at: float = 0.0
    completed_at: float = 0.0
    success: bool = False
    speed_score: int = 0
    stealth_score: int = 0
    technique_score: int = 0
    total_score: int = 0
    techniques_used: list[str] = field(default_factory=list)
    elo_awarded: int = 0


def _ensure_gym_dir() -> None:
    """Create the gym data directory."""
    GYM_DIR.mkdir(parents=True, exist_ok=True)


def _load_leaderboard() -> dict[str, dict[str, Any]]:
    """Load the persistent leaderboard.

    Returns:
        Dict mapping operator name to stats.
    """
    _ensure_gym_dir()
    if not GYM_LEADERBOARD.exists():
        return {}
    try:
        with open(GYM_LEADERBOARD) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_leaderboard(board: dict[str, dict[str, Any]]) -> None:
    """Persist the leaderboard.

    Args:
        board: Leaderboard data dict.
    """
    _ensure_gym_dir()
    with open(GYM_LEADERBOARD, "w") as f:
        json.dump(board, f, indent=2)


def _get_username() -> str:
    """Get the current operator username from the CLI auth session.

    Returns:
        Username string, falling back to 'anonymous'.
    """
    try:
        from modules.cli_auth import get_current_operator

        op = get_current_operator()
        if op:
            return op
    except ImportError:
        pass

    try:
        state_path = SESSIONS_DIR / "engagement_state.json"
        if state_path.exists():
            with open(state_path) as f:
                state = json.load(f)
            return state.get("operator", "anonymous")
    except Exception:
        pass

    return "anonymous"


def definition_rows() -> list[dict[str, Any]]:
    """Return one row per gym YAML file, including invalid files."""
    return scan_definitions()


def create_gym(
    gym_id: str,
    *,
    name: str = "",
    scenario: str = "metasploitable",
    objective: str = "",
    description: str = "",
    difficulty: str = "easy",
    chain: str = "",
    phases: list[str] | None = None,
    hints: list[str] | None = None,
    max_points: int = 1000,
    elo_bonus: int = 100,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Create a gym definition YAML and reload the catalogue."""
    try:
        path = create_definition(
            gym_id,
            name=name,
            scenario=scenario,
            objective=objective,
            description=description,
            difficulty=difficulty,
            chain=chain,
            phases=phases,
            hints=hints,
            max_points=max_points,
            elo_bonus=elo_bonus,
            overwrite=overwrite,
        )
    except (FileExistsError, ValueError, OSError) as exc:
        return {"success": False, "error": str(exc)}
    reload_challenge_definitions()
    return {"success": True, "path": str(path)}


def save_gym_yaml(gym_id: str, text: str) -> dict[str, Any]:
    """Validate and persist raw YAML for one gym definition."""
    try:
        path = update_definition_yaml(gym_id, text)
    except (FileNotFoundError, ValueError, OSError) as exc:
        return {"success": False, "error": str(exc)}
    reload_challenge_definitions()
    return {"success": True, "path": str(path)}


def delete_gym(gym_id: str, *, allow_active: bool = False) -> dict[str, Any]:
    """Delete one gym definition unless it has active runs."""
    result = delete_definition(gym_id, allow_active=allow_active)
    if result.get("success"):
        reload_challenge_definitions()
    return result


def list_challenges() -> dict[str, dict[str, Any]]:
    """Return all defined gym challenges with metadata.

    Returns:
        Dict mapping challenge ID to definition.
    """
    definitions = reload_challenge_definitions()
    result: dict[str, dict[str, Any]] = {}
    for cid, chal in definitions.items():
        result[cid] = {
            "id": chal["id"],
            "name": chal["name"],
            "description": chal["description"],
            "difficulty": chal["difficulty"],
            "scenario": chal["scenario"],
            "chain": chal.get("chain", ""),
            "phases": chal["phases"],
            "max_points": chal["max_points"],
            "elo_bonus": chal["elo_bonus"],
        }
    return result


def _resolve_active_run(selector: str = "", operator: str = "") -> tuple[dict[str, Any] | None, str]:
    """Resolve one run, falling back to the only global run when needed."""
    definitions = reload_challenge_definitions()
    runs = get_active_runs(selector=selector, operator=operator)
    if not runs and not selector:
        runs = get_active_runs(selector="", operator="")
    if not runs:
        return None, "No active gym. Start one with 'gym start <challenge_id>'."
    if len(runs) > 1:
        ids = ", ".join(str(run.get("run_id", "")) for run in runs)
        return None, f"Multiple active gyms ({ids}); pass a run id."
    run = runs[0]
    definition = definitions.get(str(run.get("challenge_id", "")))
    if definition:
        run["definition"] = definition
    return run, ""


def start_challenge(challenge_id: str, target: str = "", spin_lab: bool = True) -> dict[str, Any]:
    """Begin a gym challenge and persist the run in the world model.

    When ``spin_lab`` is set the challenge's scenario container is also
    started through :mod:`modules.lab_runtime` (best effort: Docker
    missing or an unknown scenario never fails the run registration;
    the result then keeps the manual ``lab start`` hint).

    Args:
        challenge_id: ID from the YAML catalogue.
        target: Optional engagement target stored with the run.
        spin_lab: Also spin up the scenario target container.

    Returns:
        Dict with the run id, challenge info, lab info and next steps.
    """
    definitions = reload_challenge_definitions()
    chal = definitions.get(str(challenge_id or "").strip())
    if chal is None:
        return {"success": False, "error": f"Unknown challenge: {challenge_id}"}
    started = start_run(
        challenge_id,
        definitions,
        target=target,
        operator=_get_username(),
    )
    if not started.get("success"):
        return started
    run = dict(started.get("run", {}))
    active = get_active_runs()
    lab: dict[str, Any] = {}
    lab_started = False
    if spin_lab:
        lab = _spin_scenario(chal.get("scenario", ""))
        lab_started = bool(lab.get("success"))
    result = {
        "success": True,
        "run_id": str(run.get("run_id", "")),
        "already_active": bool(started.get("already_active")),
        "active_count": len(active),
        "challenge": {
            "id": chal["id"],
            "name": chal["name"],
            "description": chal["description"],
            "objective": chal["objective"],
            "difficulty": chal["difficulty"],
            "scenario": chal["scenario"],
            "chain": chal.get("chain", ""),
            "max_points": chal["max_points"],
            "phases": chal["phases"],
            "hints": chal.get("hints", []),
        },
        "started_at": run.get("started_at", 0.0),
        "target": run.get("target", ""),
        "message": (
            f"Challenge '{chal['name']}' started. Run 'lab range start ad-mini' to spin up the range."
            if chal["scenario"] == "ad-mini"
            else f"Challenge '{chal['name']}' started. Run 'lab start {chal['scenario']}' to spin up the target."
        ),
        "next_steps": (
            [
                "lab range start ad-mini",
                "assign rhost <ws01-ip from range start output>",
                "lazynmap",
            ]
            if chal["scenario"] == "ad-mini"
            else [
                f"lab start {chal['scenario']}",
                "assign rhost 127.0.0.1",
                "lazynmap",
            ]
            + ([f"apt_chain {chal['chain']} <target>"] if chal.get("chain") else [])
        ),
    }
    if lab:
        result["lab"] = lab
        container_ip = str(lab.get("ip", "") or "")
        if lab_started and container_ip:
            result["message"] = (
                f"Challenge '{chal['name']}' started. Lab '{chal['scenario']}' is up on {container_ip}."
            )
            result["next_steps"] = (
                [
                    f"assign rhost {container_ip}",
                    "lazynmap",
                ]
                + ([f"apt_chain {chal['chain']} {container_ip}"] if chal.get("chain") else [])
                + ([f"assign rhost {target}", "lazynmap"] if target else [])
            )
    return result


def _spin_scenario(scenario: str) -> dict[str, Any]:
    """Spin up one lab scenario container, best effort.

    Args:
        scenario: Scenario key from ``LAB_SCENARIOS`` (empty and range
            scenarios like ``ad-mini`` are skipped).

    Returns:
        The :mod:`modules.lab_runtime` start mapping, or ``{}`` when the
        scenario is not a spin-up-able lab.
    """
    scenario = str(scenario or "").strip()
    if not scenario or scenario == "ad-mini":
        return {}
    try:
        from modules import lab_runtime

        if scenario not in lab_runtime.LAB_SCENARIOS or not lab_runtime.docker_available():
            return {}
        return lab_runtime.start(scenario)
    except Exception:
        return {}


def submit_challenge(
    techniques_used: list[str] | None = None,
    success: bool = True,
    run_id: str = "",
) -> dict[str, Any]:
    """Submit a completed challenge for scoring.

    Args:
        techniques_used: List of technique identifiers used.
        success: Whether the challenge was completed successfully.
        run_id: Optional run id, challenge id or gym name. Required when
            more than one gym is active.

    Returns:
        Dict with score breakdown and leaderboard position.
    """
    definitions = reload_challenge_definitions()
    run, error = _resolve_active_run(run_id, _get_username())
    if run is None:
        return {"success": False, "error": error}
    challenge_id = str(run.get("challenge_id", ""))
    chal = definitions.get(challenge_id)
    if chal is None:
        stop_runs(str(run.get("run_id", "")))
        return {"success": False, "error": f"Challenge definition not found: {challenge_id}"}
    removed, remove_error = pop_run(str(run.get("run_id", "")), definitions=definitions)
    if removed is None:
        return {"success": False, "error": remove_error}
    run = removed
    username = str(run.get("operator", "")) or _get_username()
    started_at = float(run.get("started_at", 0.0) or 0.0)
    elapsed = max(0.0, time.time() - started_at)
    techniques = techniques_used or []

    if success:
        speed_score = _calc_speed_score(elapsed, chal.get("speed_bonus_max", 300))
        stealth_score = _calc_stealth_score(techniques, chal.get("stealth_bonus_max", 200))
        technique_score = _calc_technique_score(techniques, chal, chal.get("technique_diversity_bonus", 200))
        elo_bonus = chal.get("elo_bonus", 150)
    else:
        speed_score = 0
        stealth_score = 0
        technique_score = 0
        elo_bonus = 0

    total = speed_score + stealth_score + technique_score

    attempt = GymAttempt(
        challenge_id=challenge_id,
        username=username,
        started_at=started_at,
        completed_at=time.time(),
        success=success,
        speed_score=speed_score,
        stealth_score=stealth_score,
        technique_score=technique_score,
        total_score=total,
        techniques_used=techniques,
        elo_awarded=elo_bonus,
    )

    _update_leaderboard(attempt)
    _award_gym_elo(username, elo_bonus)

    result = {
        "success": True,
        "run_id": str(run.get("run_id", "")),
        "challenge_id": challenge_id,
        "challenge": chal["name"],
        "completed": success,
        "elapsed_seconds": int(elapsed),
        "scores": {
            "speed": speed_score,
            "stealth": stealth_score,
            "technique_diversity": technique_score,
            "total": total,
            "max_possible": chal["max_points"],
        },
        "elo_awarded": elo_bonus,
        "techniques_used": techniques,
        "rank": _get_rank(username),
    }
    try:
        from modules.outcome_bus import record_event

        record_event(
            kind="report",
            target=str(run.get("target", "") or ""),
            title=f"gym {challenge_id}",
            description=f"{chal['name']}: {'completed' if success else 'failed'} score={total}",
            severity="high" if success else "low",
            success=success,
            source="redteam_gym",
            artifacts=[str(GYM_LEADERBOARD)],
            sinks=["event_bus", "c2_surfaces"],
            metadata={
                "challenge": challenge_id,
                "run_id": str(run.get("run_id", "")),
                "score": total,
                "techniques": techniques,
            },
        )
    except Exception:
        pass

    return result


def stop_challenges(selector: str = "") -> dict[str, Any]:
    """Stop one gym by id/name/run id, or every gym when selector is empty.

    After the runs are removed from the world model, each scenario
    container without any remaining active run is stopped through
    :mod:`modules.lab_runtime` so gym machines never outlive their runs.

    Args:
        selector: Optional run id, challenge id or gym name. Empty stops
            every active run.

    Returns:
        The stop result with the stopped run rows and a ``labs`` key.
    """
    result = stop_runs(selector)
    labs = _teardown_stopped_scenarios(result.get("stopped", []) or [])
    if labs:
        result["labs"] = labs
    return result


def _teardown_stopped_scenarios(stopped: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Stop scenario containers whose gym runs are all gone.

    Args:
        stopped: The stopped run rows (challenge_id included).

    Returns:
        Mapping of scenario to the lab_runtime stop result.
    """
    scenarios: list[str] = []
    for run in stopped:
        definition = reload_challenge_definitions().get(str(run.get("challenge_id", ""))) or {}
        scenario = str(definition.get("scenario", "") or "").strip()
        if scenario and scenario not in scenarios and scenario != "ad-mini":
            scenarios.append(scenario)
    if not scenarios:
        return {}
    labs: dict[str, dict[str, Any]] = {}
    try:
        from modules import lab_runtime

        remaining = {
            str(row.get("challenge_id", ""))
            for row in get_active_runs()
        }
        remaining_scenarios = {
            str((reload_challenge_definitions().get(cid) or {}).get("scenario", "") or "").strip()
            for cid in remaining
        }
        for scenario in scenarios:
            if scenario in remaining_scenarios:
                continue
            labs[scenario] = lab_runtime.stop(scenario)
    except Exception:
        return labs
    return labs


def _same_engagement(ip: str, target: str) -> bool:
    """Return True when a host belongs to the current engagement target.

    Exact target wins. Private targets also accept their /24 so a lab
    network with several hosts stays visible, while loopback addresses
    never leak into a non-loopback engagement.
    """
    candidate = str(ip or "").strip()
    wanted = str(target or "").strip()
    if not wanted:
        return True
    if candidate == wanted:
        return True
    try:
        import ipaddress

        host = ipaddress.ip_address(candidate)
        goal = ipaddress.ip_address(wanted)
        if goal.is_loopback:
            return host.is_loopback
        if host.is_loopback or host.version != goal.version:
            return False
        return host in ipaddress.ip_network(f"{wanted}/24", strict=False)
    except ValueError:
        return candidate.lower() == wanted.lower()


def engagement_context(target: str = "") -> dict[str, Any]:
    """Return in-scope phase, compromised hosts and live shells.

    Gym runs are explicit; this context explains when the operator has a
    shell or a compromised host but no gym is tracking it. Hosts outside
    the current target (for example stale loopback fixtures) are counted
    separately and never shown as engagement state.

    Args:
        target: Current engagement target; falls back to payload ``rhost``.

    Returns:
        Dict with ``phase``, ``hosts``, ``host_states``, ``live_shells``
        and ``ignored_hosts``.
    """
    wanted = str(target or "").strip()
    if not wanted:
        try:
            from core.config import load_payload

            wanted = str((load_payload() or {}).get("rhost", "") or "").strip()
        except Exception:
            wanted = ""
    context: dict[str, Any] = {
        "phase": "",
        "target": wanted,
        "hosts": [],
        "host_states": {},
        "live_shells": [],
        "ignored_hosts": [],
    }
    compromised: list[tuple[str, str]] = []
    try:
        from modules.world_model import get_world_model

        snapshot = get_world_model().snapshot()
        context["phase"] = str(snapshot.get("phase", "") or "")
        for ip, host in (snapshot.get("hosts") or {}).items():
            state = str(host.get("state", "")).lower()
            if state in ("exploited", "owned"):
                compromised.append((str(ip), state))
    except Exception:
        pass
    live_targets = set()
    try:
        from modules.atomic_exploit_bridge import live_sessions

        context["live_shells"] = live_sessions()
        live_targets = {str(row.get("target", "")) for row in context["live_shells"]}
    except Exception:
        pass
    for ip, state in sorted(compromised):
        if _same_engagement(ip, wanted) or ip in live_targets:
            context["hosts"].append(ip)
            context["host_states"][ip] = state
        else:
            context["ignored_hosts"].append(ip)
    return context


def get_active_challenges() -> list[dict[str, Any]]:
    """Return every active gym run across operators."""
    definitions = reload_challenge_definitions()
    rows: list[dict[str, Any]] = []
    for run in get_active_runs():
        row = dict(run)
        definition = definitions.get(str(row.get("challenge_id", "")))
        if definition:
            row["definition"] = definition
        rows.append(row)
    return rows


def _calc_speed_score(elapsed_seconds: float, max_bonus: int) -> int:
    """Calculate speed score — faster = higher.

    Args:
        elapsed_seconds: Time taken in seconds.
        max_bonus: Maximum possible speed bonus.

    Returns:
        Speed score (0 to max_bonus).
    """
    if elapsed_seconds <= 0:
        return max_bonus
    minutes = elapsed_seconds / 60.0
    if minutes < 5:
        return max_bonus
    if minutes > 120:
        return 0
    factor = max(0.0, 1.0 - (minutes - 5) / 115.0)
    return int(max_bonus * factor)


def _calc_stealth_score(techniques: list[str], max_bonus: int) -> int:
    """Calculate stealth score — fewer noisy techniques = higher.

    Args:
        techniques: List of technique identifiers used.
        max_bonus: Maximum bonus points.

    Returns:
        Stealth score (0 to max_bonus).
    """
    noisy_techniques = {"nmap_full_scan", "masscan", "bruteforce", "dos", "password_spray_large"}
    noise_count = len(set(techniques) & noisy_techniques)
    penalty = noise_count * (max_bonus // 3)
    return max(0, max_bonus - penalty)


def _calc_technique_score(techniques: list[str], chal: dict[str, Any], max_bonus: int) -> int:
    """Calculate technique diversity score.

    Args:
        techniques: List of technique identifiers used.
        chal: Challenge definition.
        max_bonus: Maximum diversity bonus.

    Returns:
        Diversity score (0 to max_bonus).
    """
    required = set(chal.get("required_techniques", []))
    bonus = set(chal.get("bonus_techniques", []))

    used = set(techniques)
    required_met = len(used & required) / max(1, len(required))
    bonus_hit = len(used & bonus)

    score = int(max_bonus * (0.5 * required_met + 0.5 * min(1.0, bonus_hit / max(1, len(bonus)))))
    return score


def _update_leaderboard(attempt: GymAttempt) -> None:
    """Update the persistent leaderboard with a completed attempt.

    Args:
        attempt: Completed gym attempt.
    """
    board = _load_leaderboard()
    username = attempt.username

    if username not in board:
        board[username] = {
            "username": username,
            "total_score": 0,
            "challenges_completed": 0,
            "elo_from_gym": 0,
            "best_challenge": "",
            "best_score": 0,
            "recent": [],
        }

    entry = board[username]
    entry["total_score"] += attempt.total_score
    if attempt.success:
        entry["challenges_completed"] += 1
    entry["elo_from_gym"] += attempt.elo_awarded

    if attempt.total_score > entry["best_score"]:
        entry["best_score"] = attempt.total_score
        entry["best_challenge"] = attempt.challenge_id

    entry["recent"].append(
        {
            "challenge": attempt.challenge_id,
            "success": attempt.success,
            "score": attempt.total_score,
            "elo": attempt.elo_awarded,
            "timestamp": attempt.completed_at,
        }
    )
    entry["recent"] = entry["recent"][-20:]

    _save_leaderboard(board)


def _award_gym_elo(username: str, elo_bonus: int) -> None:
    """Award ELO to the user via the existing engagement hooks system.

    Args:
        username: Operator username.
        elo_bonus: ELO delta to award.
    """
    if elo_bonus <= 0:
        return

    try:
        from cli.engagement_hooks import get_karma_name

        state_path = SESSIONS_DIR / "engagement_state.json"
        if state_path.exists():
            with open(state_path) as f:
                state = json.load(f)
            state["elo"] = state.get("elo", 0) + elo_bonus
            state["elo_session_delta"] = state.get("elo_session_delta", 0) + elo_bonus
            state["last_karma_name"] = get_karma_name(state["elo"])
            with open(state_path, "w") as f:
                json.dump(state, f, indent=2)
    except Exception:
        pass


def _get_rank(username: str) -> int:
    """Get the leaderboard rank for a user.

    Args:
        username: Operator username.

    Returns:
        1-indexed rank position.
    """
    board = _load_leaderboard()
    sorted_users = sorted(board.items(), key=lambda x: x[1].get("total_score", 0), reverse=True)
    for rank, (name, _) in enumerate(sorted_users, 1):
        if name == username:
            return rank
    return len(sorted_users) + 1


def show_leaderboard(top_n: int = 15) -> list[dict[str, Any]]:
    """Return the top N players from the leaderboard.

    Args:
        top_n: Maximum number of entries to return.

    Returns:
        List of leaderboard entries sorted by total_score descending.
    """
    board = _load_leaderboard()
    sorted_users = sorted(board.items(), key=lambda x: x[1].get("total_score", 0), reverse=True)

    result: list[dict[str, Any]] = []
    for rank, (name, entry) in enumerate(sorted_users[:top_n], 1):
        result.append(
            {
                "rank": rank,
                "username": name,
                "total_score": entry.get("total_score", 0),
                "challenges_completed": entry.get("challenges_completed", 0),
                "elo_from_gym": entry.get("elo_from_gym", 0),
                "best_score": entry.get("best_score", 0),
            }
        )
    return result


def get_active_challenge(run_id: str = "") -> dict[str, Any] | None:
    """Return one active challenge, preferring the current operator.

    Args:
        run_id: Optional run id, challenge id or gym name.

    Returns:
        Active challenge dict or None. When no selector is given and only
        one gym is active globally, that run is returned even if the
        operator label changed between sessions.
    """
    definitions = reload_challenge_definitions()
    run, _error = _resolve_active_run(run_id, _get_username())
    if run is None:
        return None
    challenge_id = str(run.get("challenge_id", ""))
    chal = definitions.get(challenge_id) or run.get("definition") or {}
    return {
        "active": True,
        "run_id": str(run.get("run_id", "")),
        "challenge_id": challenge_id,
        "name": chal.get("name", run.get("name", challenge_id)),
        "objective": chal.get("objective", ""),
        "operator": str(run.get("operator", "")),
        "target": str(run.get("target", "")),
        "started_at": float(run.get("started_at", 0.0) or 0.0),
        "elapsed_seconds": int(run.get("elapsed_seconds", 0) or 0),
        "hint": (chal.get("hints") or [None])[0],
    }


def record_external_attempt(
    challenge_id: str,
    success: bool,
    elo_bonus: int = 150,
    techniques: list[str] | None = None,
) -> dict[str, Any]:
    """Record a scored attempt for a challenge not defined in the catalog.

    Lets external modules (for example the ExploitGym integration) feed the
    shared ELO/leaderboard pipeline without requiring a challenge
    definition or an active in-flight challenge.

    Args:
        challenge_id: Identifier recorded on the leaderboard (e.g.
            ``exploitgym:<task_id>``).
        success: Whether the attempt succeeded.
        elo_bonus: ELO delta to award on success (``0`` on failure).
        techniques: Technique identifiers used.

    Returns:
        Dict with ``success``, ``challenge``, ``completed``, ``elo_awarded``
        and ``rank``.
    """
    username = _get_username()
    elapsed = 0.0
    total = elo_bonus if success else 0

    attempt = GymAttempt(
        challenge_id=challenge_id,
        username=username,
        started_at=time.time(),
        completed_at=time.time(),
        success=success,
        speed_score=0,
        stealth_score=0,
        technique_score=0,
        total_score=total,
        techniques_used=techniques or [],
        elo_awarded=elo_bonus if success else 0,
    )

    _update_leaderboard(attempt)
    _award_gym_elo(username, elo_bonus if success else 0)

    return {
        "success": True,
        "challenge": challenge_id,
        "completed": success,
        "elapsed_seconds": int(elapsed),
        "elo_awarded": elo_bonus if success else 0,
        "rank": _get_rank(username),
    }


def main():
    """CLI entry point — show gym leaderboard from command line."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        challenges = list_challenges()
        for _cid, chal in sorted(challenges.items()):
            print(f"  {chal['name']} [{chal['difficulty']}] - {chal['description']}")
    else:
        board = show_leaderboard()
        if not board:
            print("Leaderboard is empty.")
        else:
            for entry in board:
                print(f"  #{entry['rank']} {entry['username']}: {entry['total_score']} pts")


if __name__ == "__main__":
    main()


__all__ = [
    "GYM_CHALLENGE_DEFINITIONS",
    "GYM_DEFAULT_DEFINITIONS",
    "create_gym",
    "definition_rows",
    "delete_gym",
    "get_active_challenge",
    "get_active_challenges",
    "list_challenges",
    "record_external_attempt",
    "reload_challenge_definitions",
    "save_gym_yaml",
    "show_leaderboard",
    "start_challenge",
    "stop_challenges",
    "submit_challenge",
]
