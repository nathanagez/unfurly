#!/usr/bin/env bash
set -euo pipefail

parameter_name="${1:-/unfurly/slack}"

umask 077
credentials_file="$(mktemp)"
trap 'rm -f "$credentials_file"' EXIT

read -r -s -p "Slack bot token (xoxb-...): " SLACK_BOT_TOKEN
echo
read -r -s -p "Slack signing secret: " SLACK_SIGNING_SECRET
echo
export SLACK_BOT_TOKEN SLACK_SIGNING_SECRET

python3 -I -c '
import json, os, sys
json.dump(
    {"slack_bot_token": os.environ["SLACK_BOT_TOKEN"], "slack_signing_secret": os.environ["SLACK_SIGNING_SECRET"]},
    open(sys.argv[1], "w"),
)
' "$credentials_file"

aws ssm put-parameter \
  --region us-east-1 \
  --name "$parameter_name" \
  --type SecureString \
  --tier Standard \
  --overwrite \
  --value "file://$credentials_file" \
  --query Version --output text >/dev/null

echo "Stored Slack credentials in SSM parameter $parameter_name"
