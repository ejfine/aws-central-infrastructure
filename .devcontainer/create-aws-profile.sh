#!/usr/bin/env sh
set -ex

mkdir -p ~/.aws
cat >> ~/.aws/config <<EOF
[profile central-infra]
sso_session = org
sso_account_id = 038462771856
sso_role_name = LowRiskAccountAdminAccess
region = us-east-1

[profile identity-center]
sso_session = org
sso_account_id = 872515268414
sso_role_name = LowRiskAccountAdminAccess
region = us-east-1

[sso-session org]
sso_start_url = https://d-9067c20053.awsapps.com/start
sso_region = us-east-1
sso_registration_scopes = sso:account:access

[profile localstack]
region=us-east-1
output=json
endpoint_url = http://localstack:4566
EOF
cat >> ~/.aws/credentials <<EOF
[localstack]
aws_access_key_id=test
aws_secret_access_key=test
EOF
