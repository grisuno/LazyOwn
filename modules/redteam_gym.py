"""Red Team Gym — gamified pentest training mode.

Integrates with the existing ELO/karma system in
:mod:`cli.engagement_hooks` and extends :mod:`cli.commands.lab`
Docker scenarios with challenge objectives, scoring, and leaderboards.

Each challenge defines a specific objective, success criteria, a
time-based speed score, a stealth score (based on techniques that
avoid EDR triggers), and a technique-diversity bonus.

Completion awards bonus ELO that is added via the existing
``aumentar_elo`` / ``_award_elo`` pipeline.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
GYM_DIR = SESSIONS_DIR / "gym"
GYM_LEADERBOARD = GYM_DIR / "leaderboard.json"
GYM_CHALLENGES = GYM_DIR / "challenges.json"


GYM_CHALLENGE_DEFINITIONS: dict[str, dict[str, Any]] = {
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
}


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


def list_challenges() -> dict[str, dict[str, Any]]:
    """Return all defined gym challenges with metadata.

    Returns:
        Dict mapping challenge ID to definition.
    """
    result: dict[str, dict[str, Any]] = {}
    for cid, chal in GYM_CHALLENGE_DEFINITIONS.items():
        result[cid] = {
            "id": chal["id"],
            "name": chal["name"],
            "description": chal["description"],
            "difficulty": chal["difficulty"],
            "scenario": chal["scenario"],
            "phases": chal["phases"],
            "max_points": chal["max_points"],
            "elo_bonus": chal["elo_bonus"],
        }
    return result


def start_challenge(challenge_id: str) -> dict[str, Any]:
    """Begin a gym challenge and track start time.

    Args:
        challenge_id: ID from GYM_CHALLENGE_DEFINITIONS.

    Returns:
        Dict with challenge info and started status.
    """
    if challenge_id not in GYM_CHALLENGE_DEFINITIONS:
        return {"success": False, "error": f"Unknown challenge: {challenge_id}"}

    chal = GYM_CHALLENGE_DEFINITIONS[challenge_id]
    username = _get_username()

    attempt = GymAttempt(
        challenge_id=challenge_id,
        username=username,
        started_at=time.time(),
    )

    _ensure_gym_dir()
    active_path = GYM_DIR / f"active_{username}.json"
    with open(active_path, "w") as f:
        json.dump(
            {
                "challenge_id": challenge_id,
                "username": username,
                "started_at": attempt.started_at,
            },
            f,
        )

    result = {
        "success": True,
        "challenge": {
            "id": chal["id"],
            "name": chal["name"],
            "description": chal["description"],
            "objective": chal["objective"],
            "difficulty": chal["difficulty"],
            "scenario": chal["scenario"],
            "max_points": chal["max_points"],
            "phases": chal["phases"],
            "hints": chal.get("hints", []),
        },
        "started_at": attempt.started_at,
        "message": f"Challenge '{chal['name']}' started. Run 'lab start {chal['scenario']}' to spin up the target.",
        "next_steps": [
            f"lab start {chal['scenario']}",
            "assign rhost 127.0.0.1",
            "lazynmap",
        ],
    }

    return result


def submit_challenge(
    techniques_used: list[str] | None = None,
    success: bool = True,
) -> dict[str, Any]:
    """Submit a completed challenge for scoring.

    Args:
        techniques_used: List of technique identifiers used.
        success: Whether the challenge was completed successfully.

    Returns:
        Dict with score breakdown and leaderboard position.
    """
    username = _get_username()
    active_path = GYM_DIR / f"active_{username}.json"

    if not active_path.exists():
        return {"success": False, "error": "No active challenge. Start one with 'gym start <challenge_id>'."}

    with open(active_path) as f:
        active = json.load(f)

    challenge_id = active.get("challenge_id", "")
    started_at = active.get("started_at", 0.0)

    if challenge_id not in GYM_CHALLENGE_DEFINITIONS:
        return {"success": False, "error": "Active challenge definition not found."}

    chal = GYM_CHALLENGE_DEFINITIONS[challenge_id]
    elapsed = time.time() - started_at

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

    active_path.unlink()

    result = {
        "success": True,
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

    return result


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


def get_active_challenge() -> dict[str, Any] | None:
    """Return the currently active challenge for this operator, if any.

    Returns:
        Active challenge dict or None.
    """
    username = _get_username()
    active_path = GYM_DIR / f"active_{username}.json"
    if not active_path.exists():
        return None
    try:
        with open(active_path) as f:
            active = json.load(f)
        challenge_id = active.get("challenge_id", "")
        chal = GYM_CHALLENGE_DEFINITIONS.get(challenge_id)
        if not chal:
            return None
        return {
            "active": True,
            "challenge_id": challenge_id,
            "name": chal["name"],
            "objective": chal["objective"],
            "started_at": active.get("started_at", 0),
            "elapsed_seconds": int(time.time() - active.get("started_at", time.time())),
            "hint": chal.get("hints", [None])[0],
        }
    except Exception:
        return None


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
            print(f"  {chal['name']} [{chal['difficulty']}] — {chal['description']}")
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
    "list_challenges",
    "start_challenge",
    "submit_challenge",
    "show_leaderboard",
    "get_active_challenge",
    "record_external_attempt",
    "GYM_CHALLENGE_DEFINITIONS",
]
