# 3. Bound the Slack events cost with a kill switch

## Status

Accepted

## Context

Slack delivers events to a public HTTPS endpoint, which is a Lambda function URL without AWS
authentication. Every request runs the function, even one that fails the Slack signature check, so a
flood of requests bills Lambda requests, duration, and logs. The CloudFront Free plan that protects
the media CDN does not cover this endpoint.

The alternatives considered:

- **API Gateway with throttling** caps the request rate but bills each request, including throttled
  ones beyond the free tier, and adds a component.
- **CloudFront and WAF in front of the function URL** would put the endpoint under the Free plan, but
  requests that pass the WAF still run the function, and a distributed flood passes rate rules.
- **A billing budget** alerts hours after the spend, because billing data arrives late, and does not
  stop anything.

## Decision

We will cap the Slack events function's reserved concurrency, limit its system logs to warnings, and
add a CloudWatch alarm on its invocations that invokes a kill switch function. The kill switch sets
the function's reserved concurrency to `0`.

## Consequences

- A flood costs a few minutes of capped invocations before the kill switch stops the function.
- The alarm stays within the CloudWatch free tier, and the kill switch function runs once per alarm.
- When the kill switch fires, unfurly stops unfurling until someone restores the concurrency.
- A legitimate burst above `KillSwitchInvocationThreshold` also trips the kill switch. The parameter
  makes the threshold adjustable per deployment.
