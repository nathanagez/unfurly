# How to deploy with GitHub Actions

This guide shows you how to deploy unfurly with the `deploy` workflow, on demand or on each
release. Each target AWS account maps to one GitHub environment.

## Set up an account

1. In the target account, deploy the OIDC role:

   ```bash
   aws cloudformation deploy \
     --region us-east-1 \
     --stack-name unfurly-github-oidc \
     --template-file deploy/github-oidc-role.yaml \
     --capabilities CAPABILITY_IAM \
     --parameter-overrides GitHubEnvironment=production
   ```

   - If the repository is not `nathanagez/unfurly`, add `GitHubRepository=<owner>/<name>`.
   - If the account already has the `token.actions.githubusercontent.com` identity provider, add
     `CreateOidcProvider=false`.

2. Read the role ARN:

   ```bash
   aws cloudformation describe-stacks --region us-east-1 --stack-name unfurly-github-oidc \
     --query "Stacks[0].Outputs[?OutputKey=='DeployRoleArn'].OutputValue" --output text
   ```

3. In the repository settings, create a GitHub environment with the same name, for example
   `production`. To approve each deployment, add required reviewers to it.

4. Add the environment variables listed in
   [Configuration](../reference/configuration.md#github-actions-variables). Only
   `AWS_DEPLOY_ROLE_ARN` is required.

5. Store the Slack credentials in the account with step 1 of
   [How to deploy unfurly to an AWS account](how-to-deploy-to-an-aws-account.md).

## Deploy

- **On demand:** run the `deploy` workflow from the **Actions** tab and pick the environment.
- **On each release:** set the repository variable `RELEASE_DEPLOY_ENVIRONMENT` to the environment
  name. When release-please publishes a release, the `release-please` workflow deploys the release tag
  to that environment.

After the first deployment, [create the Slack app](how-to-create-the-slack-app.md). Pass the
`STACK_NAME` value to `render-slack-manifest.sh` if you changed it.
