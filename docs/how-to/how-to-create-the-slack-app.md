# How to create the Slack app

This guide shows you how to create the Slack app for a deployed unfurly stack and connect the two.
If you deployed under another stack name than `unfurly`, replace it in the commands.

1. Render the manifest from the stack outputs:

   ```bash
   ./scripts/render-slack-manifest.sh unfurly > /tmp/unfurly-manifest.yaml
   ```

   The manifest registers `instagram.com` and the stack's `PublicDomain` as unfurl domains. Slack
   requires the video player domain in that list.

2. In [Your Apps](https://api.slack.com/apps) on the Slack API site, choose **Create New App**, then
   **From a manifest**. Select the workspace and paste the rendered manifest.

3. In **Basic Information**, copy the **Signing Secret**.

4. In **Install App**, choose **Install to Workspace**, then copy the **Bot User OAuth Token**.

5. Store both values in SSM Parameter Store:

   ```bash
   ./scripts/set-slack-credentials.sh /unfurly/slack
   ```

6. Wait five minutes, the time the functions cache the credentials. Then, in
   **Event Subscriptions**, choose **Retry** next to the request URL until it shows **Verified**,
   and choose **Save Changes**.

If the request URL check fails, read the Slack events function logs:

```bash
aws logs tail /unfurly/unfurly/slack-events --region us-east-1 --since 10m
```
