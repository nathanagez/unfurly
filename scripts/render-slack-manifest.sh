#!/usr/bin/env bash
set -euo pipefail

stack_name="${1:-unfurly}"
repository_root="$(cd "$(dirname "$0")/.." && pwd)"

stack_output() {
  aws cloudformation describe-stacks \
    --region us-east-1 \
    --stack-name "$stack_name" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" \
    --output text
}

request_url="$(stack_output SlackEventsRequestUrl)"
public_domain="$(stack_output PublicDomain)"

sed \
  -e "s#{{REQUEST_URL}}#${request_url}#" \
  -e "s#{{PUBLIC_DOMAIN}}#${public_domain}#" \
  "$repository_root/slack/manifest.template.yaml"
