# How to deploy unfurly to an AWS account

This guide shows you how to deploy the unfurly stack from your machine to any AWS account. To
deploy from GitHub Actions instead, see [How to deploy with GitHub Actions](how-to-deploy-with-github-actions.md).

## Before you start

- `uv`, the AWS CLI v2, the AWS SAM CLI, and Python 3.
- Credentials for the target account, for example through `AWS_PROFILE`.
- The stack deploys to `us-east-1` only, because CloudFront requires its certificate and its web ACL
  there. The template rejects any other Region.
- An account can hold three CloudFront Free plans. If the account already uses three, answer
  `PAY_AS_YOU_GO` to the `CloudFrontPricingPlan` prompt.

## Steps

1. Store the Slack credentials in SSM Parameter Store. If you have not created the Slack app, enter
   placeholders: you store the real values in step 4.

   ```bash
   ./scripts/set-slack-credentials.sh /unfurly/slack
   ```

2. Build the functions:

   ```bash
   sam build
   ```

3. Deploy:

   ```bash
   sam deploy --guided
   ```

   - To use the CloudFront domain, leave `DomainName` and `HostedZoneId` empty. To use a custom
     domain, set both. The hosted zone must be a public Route 53 zone in the same account.
   - When SAM asks whether `SlackEventsFunction` may have no authorization defined, answer `y`: Slack
     calls the function URL, and the function verifies the Slack signature itself.
   - To keep the answers for this account, save them under a configuration environment when the
     prompt asks. Later deployments then run with `sam deploy --config-env <name>`.

4. [Create the Slack app](how-to-create-the-slack-app.md). That guide stores the real Slack
   credentials.

5. Post a reel link in a channel of the workspace. The link preview turns into a video player within
   a few seconds.

If you deploy under another stack name than `unfurly`, pass that name to the scripts.
