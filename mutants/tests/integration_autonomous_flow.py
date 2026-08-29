import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT / "modules"))

from moe_router import get_router  # noqa: E402
from obs_parser import get_parser  # noqa: E402
from session_rag import get_rag  # noqa: E402
from world_model import get_world_model  # noqa: E402


def test_autonomous_flow_integration():
    """
    Simulates a simplified autonomous flow to verify module integration.
    """
    # 1. Initialize modules
    router = get_router()
    wm = get_world_model()
    rag = get_rag()
    parser = get_parser()

    # Reset state for clean test
    wm.reset()

    # 2. Simulate discovery of a cloud host
    cloud_output = "arn:aws:iam::123456789012:role/ReadOnlyRole discovered on 10.0.0.5"
    obs = parser.parse(cloud_output, host="10.0.0.5", tool="cloud_scanner")
    assert obs.has("cloud_role")

    # 3. Update World Model
    wm.update_from_findings(obs.findings)
    host = wm.add_host("10.0.0.5")
    assert host.cloud_metadata["iam_role"] == "arn:aws:iam::123456789012:role/ReadOnlyRole"

    # 4. Route task using MoE
    # We bypass the availability check for the test by looking at the expert pool directly
    # since we don't have a real API key in the test environment.
    expert = next(e for e in router._experts if "cloud_enum" in e.capabilities)
    assert expert.expert_id == "groq_cloud"

    # 5. Verify RAG (assuming it's initialized/ready even if empty)
    stats = rag.stats()
    assert "backend" in stats

if __name__ == "__main__":
    pytest.main([__file__])
