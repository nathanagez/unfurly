# How to re-enable unfurly after the kill switch

This guide shows you how to restore the Slack events function after the kill switch sets its reserved
concurrency to `0`. Until then, reel links stay plain links. If you deployed under another stack name
than `unfurly`, replace it in the commands.

1. Check why the alarm fired:

   ```bash
   aws logs tail /unfurly/unfurly/kill-switch --region us-east-1 --since 1d
   aws cloudwatch describe-alarm-history --region us-east-1 \
     --alarm-name "$(aws cloudformation describe-stack-resource --region us-east-1 \
       --stack-name unfurly --logical-resource-id SlackEventsFloodAlarm \
       --query StackResourceDetail.PhysicalResourceId --output text)"
   ```

2. When the flood is over, restore the `ReservedConcurrentExecutions` value of `SlackEventsFunction`
   in `template.yaml` (2):

   ```bash
   aws lambda put-function-concurrency --region us-east-1 \
     --function-name "$(aws cloudformation describe-stacks --region us-east-1 --stack-name unfurly \
       --query "Stacks[0].Outputs[?OutputKey=='SlackEventsFunctionName'].OutputValue" --output text)" \
     --reserved-concurrent-executions 2
   ```

3. Post a reel link to confirm that the preview turns into a video.

If legitimate traffic trips the kill switch, raise `KillSwitchInvocationThreshold` and deploy again.
From GitHub Actions, set the `KILL_SWITCH_INVOCATION_THRESHOLD` environment variable.
