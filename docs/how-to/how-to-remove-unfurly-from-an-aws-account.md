# How to remove unfurly from an AWS account

This guide shows you how to delete the unfurly stack and its Slack credentials from an account.
If you deployed under another stack name than `unfurly`, replace it in the commands.

1. Empty the media bucket. CloudFormation cannot delete a bucket that still holds reels:

   ```bash
   aws s3 rm --recursive "s3://$(aws cloudformation describe-stack-resource --region us-east-1 \
     --stack-name unfurly --logical-resource-id MediaBucket \
     --query StackResourceDetail.PhysicalResourceId --output text)"
   ```

2. Delete the stack:

   ```bash
   sam delete --stack-name unfurly --region us-east-1
   ```

3. Delete the Slack credentials:

   ```bash
   aws ssm delete-parameter --region us-east-1 --name /unfurly/slack
   ```

4. In [Your Apps](https://api.slack.com/apps) on the Slack API site, delete the unfurly app.
