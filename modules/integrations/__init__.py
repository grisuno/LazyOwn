"""LazyOwn integrations — bridges to external platforms and tools.

Public API
----------
- :class:`MISPIntegration` — export findings to MISP via REST API
- :class:`NucleiBridge` — translate target context into Nuclei scans
- :class:`SearchsploitBridge` — query ExploitDB for matching exploits
"""

from modules.integrations.misp_export import MISPExporter
from modules.integrations.nuclei_bridge import NucleiBridge
from modules.integrations.searchsploit import SearchsploitClient

__all__ = [
    "MISPExporter",
    "NucleiBridge",
    "SearchsploitClient",
]
