# modules: saas_attacks

*Community 11 | 7 files | cohesion 0.86*

## Definition

This community groups 7 file(s) rooted at `modules` with dominant language py (cohesion 0.86). Central symbols: `AWSAttackEngine`, `AWSConfig`, `CloudAttackCommandSet`, `CrossCloudAttackEngine`, `CrossCloudConfig`, `EntraIDAttackEngine`, `EntraIDConfig`, `GCPAttackEngine`. Core file: `modules/saas_attacks.py` (15 symbols). Documented purpose: Cloud attack commands — Azure AD/Entra ID, AWS, GCP, Kubernetes, cross-cloud, SaaS.  Provides: entra_attack            — Entra ID device code phishing, OAuth co.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/cloud_attacks.py` | py | utility | 7 | yes |
| `modules/aws_attacks.py` | py | utility | 11 | yes |
| `modules/cross_cloud.py` | py | utility | 10 | yes |
| `modules/entra_id_attacks.py` | py | utility | 12 | yes |
| `modules/gcp_attacks.py` | py | utility | 11 | yes |
| `modules/k8s_attacks.py` | py | utility | 11 | yes |
| `modules/saas_attacks.py` | py | utility | 15 | yes |

## Key Symbols

- `CloudAttackCommandSet` (class, `cli/commands/cloud_attacks.py:17`) `class CloudAttackCommandSet(LazyOwnCommandSet)` - Cloud and SaaS attack operations.
- `do_entra_attack` (method, `cli/commands/cloud_attacks.py:23`) `def do_entra_attack(self, line)` - Microsoft Entra ID / Azure AD attack operations.
- `do_aws_privesc` (method, `cli/commands/cloud_attacks.py:125`) `def do_aws_privesc(self, line)` - AWS privilege escalation and enumeration.
- `do_gcp_privesc` (method, `cli/commands/cloud_attacks.py:215`) `def do_gcp_privesc(self, line)` - GCP privilege escalation and enumeration.
- `do_k8s_attack` (method, `cli/commands/cloud_attacks.py:302`) `def do_k8s_attack(self, line)` - Kubernetes attack — RBAC enumeration, pod escape, etcd, persistence.
- `do_cross_cloud` (method, `cli/commands/cloud_attacks.py:387`) `def do_cross_cloud(self, line)` - Cross-cloud identity federation attacks.
- `do_saas_enum` (method, `cli/commands/cloud_attacks.py:470`) `def do_saas_enum(self, line)` - Enumerate SaaS platforms — M365, Google Workspace, Salesforce, Slack, ServiceNow.
- `AWSConfig` (class, `modules/aws_attacks.py:57`) `class AWSConfig` - Configuration for AWS attack operations.
- `AWSAttackEngine` (class, `modules/aws_attacks.py:79`) `class AWSAttackEngine` - Execute AWS privilege escalation and enumeration attacks.
- `__init__` (method, `modules/aws_attacks.py:90`) `def __init__(self, config)`
- `enumerate_iam_permissions` (method, `modules/aws_attacks.py:94`) `def enumerate_iam_permissions(self)` - Enumerate IAM permissions for the current user/role.
- `lambda_backdoor` (method, `modules/aws_attacks.py:126`) `def lambda_backdoor(self, function_name)` - Plan a Lambda backdoor for privilege escalation.
- `sts_role_chain` (method, `modules/aws_attacks.py:154`) `def sts_role_chain(self, target_role_arn)` - Enumerate and exploit STS AssumeRole privilege escalation chains.
- `ec2_user_data_exfil` (method, `modules/aws_attacks.py:180`) `def ec2_user_data_exfil(self)` - Extract sensitive data from EC2 instance user data and metadata.
- `s3_enumeration` (method, `modules/aws_attacks.py:205`) `def s3_enumeration(self)` - Enumerate S3 buckets and their permissions.
- `cloudformation_drift` (method, `modules/aws_attacks.py:234`) `def cloudformation_drift(self)` - Exploit CloudFormation for privilege escalation.
- `ec2_ssm_session_abuse` (method, `modules/aws_attacks.py:263`) `def ec2_ssm_session_abuse(self)` - Abuse SSM to gain shell access to EC2 instances.
- `summary` (method, `modules/aws_attacks.py:282`) `def summary(self)`
- `CrossCloudConfig` (class, `modules/cross_cloud.py:30`) `class CrossCloudConfig` - Configuration for cross-cloud identity attacks.
- `CrossCloudAttackEngine` (class, `modules/cross_cloud.py:54`) `class CrossCloudAttackEngine` - Execute cross-cloud identity federation attacks.
- `__init__` (method, `modules/cross_cloud.py:64`) `def __init__(self, config)`
- `azure_saml_to_aws` (method, `modules/cross_cloud.py:67`) `def azure_saml_to_aws(self)` - Abuse Azure AD SAML federation to gain AWS access.
- `gcp_oidc_to_azure` (method, `modules/cross_cloud.py:104`) `def gcp_oidc_to_azure(self)` - Abuse GCP OIDC federation to gain Azure access.
- `aws_oidc_to_gcp` (method, `modules/cross_cloud.py:133`) `def aws_oidc_to_gcp(self)` - Abuse AWS OIDC federation to gain GCP access.
- `multi_cloud_imds_harvesting` (method, `modules/cross_cloud.py:167`) `def multi_cloud_imds_harvesting(self)` - Harvest metadata from all cloud providers simultaneously.
- `entra_id_to_gcp_workforce_federation` (method, `modules/cross_cloud.py:204`) `def entra_id_to_gcp_workforce_federation(self)` - Exploit Entra ID to GCP workforce identity federation.
- `detect_cross_cloud_federation` (method, `modules/cross_cloud.py:234`) `def detect_cross_cloud_federation(self)` - Detect cross-cloud federation configurations for attack surface mapping.
- `summary` (method, `modules/cross_cloud.py:258`) `def summary(self)`
- `EntraIDConfig` (class, `modules/entra_id_attacks.py:56`) `class EntraIDConfig` - Configuration for Entra ID attack operations.
- `EntraIDAttackEngine` (class, `modules/entra_id_attacks.py:80`) `class EntraIDAttackEngine` - Execute Entra ID attacks against Azure AD / Microsoft 365 tenants.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 6
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- [EXTRACTED] depends_on community 11 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/cloud_attacks.py imports cli/commands/_base.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: saas_attacks changed?
- Should modules: saas_attacks be split, given cohesion 0.86?

## Sources

- `cli/commands/cloud_attacks.py`
- `modules/aws_attacks.py`
- `modules/cross_cloud.py`
- `modules/entra_id_attacks.py`
- `modules/gcp_attacks.py`
- `modules/k8s_attacks.py`
- `modules/saas_attacks.py`
