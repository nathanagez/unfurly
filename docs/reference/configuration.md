# Configuration

## Stack parameters

| Parameter | Default | Description |
|---|---|---|
| `DomainName` | empty | Custom domain for the player pages. Empty uses the CloudFront domain. |
| `HostedZoneId` | empty | Public Route 53 hosted zone of `DomainName`. Required when `DomainName` is set. |
| `SlackParameterName` | `/unfurly/slack` | SecureString SSM parameter with the Slack credentials. Must start with `/`. |
| `CloudFrontPricingPlan` | `FREE` | `FREE` subscribes the distribution and a web ACL to the CloudFront Free flat-rate plan. `PAY_AS_YOU_GO` creates neither. |
| `UnfurlProviderName` | `unfurly` | Provider name that Slack shows on each video unfurl. |
| `KillSwitchInvocationThreshold` | `500` | Slack events function invocations per five minutes that trigger the kill switch. |

The stack deploys to `us-east-1` only.

## Stack outputs

| Output | Description |
|---|---|
| `SlackEventsRequestUrl` | Request URL for the Slack app Event Subscriptions. |
| `PublicDomain` | Domain of the player pages. Register it as a Slack app unfurl domain. |
| `SlackParameterName` | SSM parameter that holds the Slack credentials. |
| `SlackEventsFunctionName` | Function that the kill switch disables. |

## Slack credentials parameter

A SecureString parameter in the standard tier, encrypted with the `aws/ssm` key, whose value is:

```json
{"slack_bot_token": "xoxb-...", "slack_signing_secret": "..."}
```

`scripts/set-slack-credentials.sh` creates the parameter. The stack does not. The functions cache the
value for five minutes.

## Functions

| Function | Memory | Timeout | Reserved concurrency | Notes |
|---|---|---|---|---|
| `SlackEventsFunction` | 512 MB | 10 s | 2 | Public function URL, verifies the Slack signature. |
| `UnfurlReelFunction` | 1024 MB | 120 s | 3 | Invoked asynchronously, no retry. |
| `KillSwitchFunction` | 128 MB | 10 s | none | Invoked by `SlackEventsFloodAlarm`. |

All functions run Python 3.14 on arm64 and send only `WARN` and above Lambda system logs.

## Retention

| Data | Retention |
|---|---|
| Media bucket objects | Expire one day after upload. S3 removes them within the following day. |
| Slack events and unfurl reel logs | One day. |
| Kill switch logs | Seven days. |

Log groups are named `/unfurly/<stack-name>/slack-events`, `/unfurl-reel`, and `/kill-switch`.

## GitHub Actions variables

Variables of the GitHub environment that the `deploy` workflow targets:

| Variable | Required | Description |
|---|---|---|
| `AWS_DEPLOY_ROLE_ARN` | Yes | `DeployRoleArn` output of the OIDC role stack. |
| `DOMAIN_NAME` | No | Value of `DomainName`. Unset uses the CloudFront domain. |
| `HOSTED_ZONE_ID` | With `DOMAIN_NAME` | Value of `HostedZoneId`. |
| `STACK_NAME` | No | Stack name. Defaults to `unfurly`. |
| `SLACK_PARAMETER_NAME` | No | Value of `SlackParameterName`. Defaults to `/unfurly/slack`. |
| `CLOUDFRONT_PRICING_PLAN` | No | Value of `CloudFrontPricingPlan`. Defaults to `FREE`. |
| `UNFURL_PROVIDER_NAME` | No | Value of `UnfurlProviderName`. Defaults to `unfurly`. |
| `KILL_SWITCH_INVOCATION_THRESHOLD` | No | Value of `KillSwitchInvocationThreshold`. Defaults to `500`. |

Repository variable:

| Variable | Description |
|---|---|
| `RELEASE_DEPLOY_ENVIRONMENT` | Environment that each release deploys to. Unset disables deployment on release. |

## OIDC role stack

`deploy/github-oidc-role.yaml` creates the role that the `deploy` workflow assumes.

| Parameter | Default | Description |
|---|---|---|
| `GitHubRepository` | `nathanagez/unfurly` | Repository allowed to assume the role, as `owner/name`. |
| `GitHubEnvironment` | none | GitHub environment allowed to assume the role. |
| `CreateOidcProvider` | `true` | `false` when the account already has the GitHub identity provider. |

| Output | Description |
|---|---|
| `DeployRoleArn` | Role ARN for the `AWS_DEPLOY_ROLE_ARN` variable. |

## Scripts

| Script | Description |
|---|---|
| `scripts/set-slack-credentials.sh [parameter-name]` | Prompts for the bot token and the signing secret, and stores them in SSM. |
| `scripts/render-slack-manifest.sh [stack-name]` | Prints the Slack app manifest with the stack's request URL and public domain. |
