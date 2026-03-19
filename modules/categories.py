"""
modules/categories.py
=====================
cmd2 command category strings for LazyOwn.

Extracted from utils.py so they can be imported independently
without pulling in the full utils dependency tree.

Usage:
    from modules.categories import recon_category, scanning_category
"""

recon_category                = "01. Reconnaissance"
scanning_category             = "02. Scanning & Enumeration"
exploitation_category         = "03. Exploitation"
post_exploitation_category    = "04. Post-Exploitation"
persistence_category          = "05. Persistence"
privilege_escalation_category = "06. Privilege Escalation"
credential_access_category    = "07. Credential Access"
lateral_movement_category     = "08. Lateral Movement"
exfiltration_category         = "09. Data Exfiltration"
command_and_control_category  = "10. Command & Control"
reporting_category            = "11. Reporting"
miscellaneous_category        = "12. Miscellaneous"
ai_category                   = "16. Artificial Intelligence"

# Lua/Addon/Adversary categories (string literals used in lazyown.py)
lua_plugin_category    = "13. Lua Plugin"
yaml_addon_category    = "14. Yaml Addon."
adversary_category     = "15. Adversary YAML."

ALL_CATEGORIES = [
    recon_category,
    scanning_category,
    exploitation_category,
    post_exploitation_category,
    persistence_category,
    privilege_escalation_category,
    credential_access_category,
    lateral_movement_category,
    exfiltration_category,
    command_and_control_category,
    reporting_category,
    miscellaneous_category,
    lua_plugin_category,
    yaml_addon_category,
    adversary_category,
    ai_category,
]

# Mapping from short name (used in policy engine) to full category string
SHORT_TO_CATEGORY = {
    "recon":       recon_category,
    "scanning":    scanning_category,
    "enum":        scanning_category,
    "exploit":     exploitation_category,
    "post":        post_exploitation_category,
    "persistence": persistence_category,
    "privesc":     privilege_escalation_category,
    "credential":  credential_access_category,
    "lateral":     lateral_movement_category,
    "exfil":       exfiltration_category,
    "c2":          command_and_control_category,
    "reporting":   reporting_category,
    "misc":        miscellaneous_category,
    "ai":          ai_category,
}

CATEGORY_TO_SHORT = {v: k for k, v in SHORT_TO_CATEGORY.items()}
