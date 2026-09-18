# modules

*Community 3 | 7 files | cohesion 0.88*

## Definition

This community groups 7 file(s) rooted at `modules` with dominant language py (cohesion 0.88). Central symbols: `ACEntry`, `ACLTarget`, `ActiveDirectoryCommandSet`, `DACLAbuseEngine`, `DelegationAttackPath`, `DelegationEnumerator`, `DelegationTarget`, `DiamondTicketConfig`. Core file: `modules/kerberos_core.py` (35 symbols). Documented purpose: Active Directory attack commands — Kerberos, tickets, delegation, DACL, GPO, kerberoasting.  Provides: kerberos_ticket         — Forge silver/golden/diamond/sap.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/active_directory.py` | py | infrastructure | 8 | yes |
| `modules/dacl_abuse.py` | py | infrastructure | 15 | yes |
| `modules/delegation_attacks.py` | py | utility | 12 | yes |
| `modules/gpo_abuse.py` | py | infrastructure | 16 | yes |
| `modules/kerberoasting.py` | py | utility | 18 | yes |
| `modules/kerberos_core.py` | py | utility | 35 | yes |
| `modules/kerberos_tickets.py` | py | utility | 34 | yes |

## Key Symbols

- `ActiveDirectoryCommandSet` (class, `cli/commands/active_directory.py:18`) `class ActiveDirectoryCommandSet(LazyOwnCommandSet)` - Kerberos, delegation, DACL, GPO, and Kerberoasting attacks.
- `do_kerberos_ticket` (method, `cli/commands/active_directory.py:24`) `def do_kerberos_ticket(self, line)` - Forge Kerberos tickets for persistence and lateral movement.
- `do_delegation_enum` (method, `cli/commands/active_directory.py:139`) `def do_delegation_enum(self, line)` - Enumerate Kerberos delegation configurations.
- `do_delegation_attack` (method, `cli/commands/active_directory.py:175`) `def do_delegation_attack(self, line)` - Display computed delegation attack paths with exploitation commands.
- `do_dacl_abuse` (method, `cli/commands/active_directory.py:199`) `def do_dacl_abuse(self, line)` - Enumerate and exploit dangerous AD DACL/SACL entries.
- `do_gpo_abuse` (method, `cli/commands/active_directory.py:233`) `def do_gpo_abuse(self, line)` - Enumerate and exploit Group Policy Objects.
- `do_kerberoast` (method, `cli/commands/active_directory.py:277`) `def do_kerberoast(self, line)` - Advanced Kerberoasting — AES-only mode, targeted SPN enumeration.
- `do_adcs_esc` (method, `cli/commands/active_directory.py:324`) `def do_adcs_esc(self, line)` - Check Active Directory Certificate Services for ESC1-ESC13 vulnerabilities.
- `ACEntry` (class, `modules/dacl_abuse.py:67`) `class ACEntry` - A single Access Control Entry in an AD object's DACL/SACL.
- `ACLTarget` (class, `modules/dacl_abuse.py:91`) `class ACLTarget` - An AD object with exploitable ACEs.
- `DACLAbuseEngine` (class, `modules/dacl_abuse.py:113`) `class DACLAbuseEngine` - Identify and exploit dangerous DACL/SACL entries on AD objects.
- `__init__` (method, `modules/dacl_abuse.py:136`) `def __init__(self, domain, domain_sid, acl_data)`
- `parse_bloodhound_acls` (method, `modules/dacl_abuse.py:143`) `def parse_bloodhound_acls(self, edges)` - Parse BloodHound edge data to extract exploitable ACLs.
- `parse_raw_aces` (method, `modules/dacl_abuse.py:182`) `def parse_raw_aces(self, raw_nthashes)` - Parse raw ACE data from ntSecurityDescriptor parsing.
- `compute_attack_chains` (method, `modules/dacl_abuse.py:224`) `def compute_attack_chains(self)` - Generate exploitation plans for all discovered ACL targets.
- `adminsdholder_abuse_plan` (method, `modules/dacl_abuse.py:289`) `def adminsdholder_abuse_plan(self, target_sid)` - Generate an AdminSDHolder abuse plan.
- `dcsync_rights_assignment_plan` (method, `modules/dacl_abuse.py:316`) `def dcsync_rights_assignment_plan(self, target_sid, domain_dn)` - Generate a DCSync rights assignment plan.
- `owner_takeover_plan` (method, `modules/dacl_abuse.py:346`) `def owner_takeover_plan(self, target_dn, attacker_sid)` - Generate an ownership takeover plan.
- `_is_dangerous_ace` (method, `modules/dacl_abuse.py:377`) `def _is_dangerous_ace(ace)`
- `_calculate_severity` (method, `modules/dacl_abuse.py:382`) `def _calculate_severity(target)`
- `_guess_object_type` (method, `modules/dacl_abuse.py:395`) `def _guess_object_type(dn)`
- `_extract_cn` (method, `modules/dacl_abuse.py:412`) `def _extract_cn(dn)`
- `summary` (method, `modules/dacl_abuse.py:416`) `def summary(self)` - Return a summary of all DACL/SACL abuse findings.
- `DelegationTarget` (class, `modules/delegation_attacks.py:32`) `class DelegationTarget` - A delegation-enabled account or computer.
- `DelegationAttackPath` (class, `modules/delegation_attacks.py:63`) `class DelegationAttackPath` - A delegation-based attack path from source to target.
- `DelegationEnumerator` (class, `modules/delegation_attacks.py:85`) `class DelegationEnumerator` - Enumerate Kerberos delegation configurations from Active Directory.
- `__init__` (method, `modules/delegation_attacks.py:98`) `def __init__(self, domain, raw_ldap_output)`
- `enumerate_from_uac_flags` (method, `modules/delegation_attacks.py:104`) `def enumerate_from_uac_flags(self, accounts)` - Enumerate delegation targets from parsed account data.
- `parse_bloodhound_output` (method, `modules/delegation_attacks.py:149`) `def parse_bloodhound_output(self, bloodhound_json)` - Parse BloodHound JSON output for delegation data.
- `find_unconstrained_targets` (method, `modules/delegation_attacks.py:179`) `def find_unconstrained_targets(self)` - Return all accounts with unconstrained delegation enabled.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 9
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/active_directory.py imports cli/commands/_base.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules changed?
- Should modules be split, given cohesion 0.88?

## Sources

- `cli/commands/active_directory.py`
- `modules/dacl_abuse.py`
- `modules/delegation_attacks.py`
- `modules/gpo_abuse.py`
- `modules/kerberoasting.py`
- `modules/kerberos_core.py`
- `modules/kerberos_tickets.py`
