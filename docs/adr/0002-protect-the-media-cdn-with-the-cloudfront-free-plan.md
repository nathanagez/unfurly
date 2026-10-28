# 2. Protect the media CDN with the CloudFront Free plan

## Status

Accepted

## Context

The media distribution is public: anyone who knows or guesses a reel identifier can download its
video. With pay-as-you-go pricing, traffic beyond the 1 TB monthly free tier costs $0.085 per GB in
the United States, with no upper bound. A download loop could produce a large bill.

CloudFront flat-rate plans bundle the CDN, AWS WAF, DDoS protection, Route 53 DNS, and S3 storage
credits for a monthly price with no overage charges. The Free plan costs $0 and allows 1 million
requests and 100 GB of transfer per month. An account can hold three Free plans. A plan requires a
WAF web ACL on the distribution, and the plan includes that web ACL.

AWS WAF also offers rate-based rules, but outside a plan they cost a monthly fee per web ACL and per
rule.

The figures come from the AWS Price List API and the
[CloudFront flat-rate pricing plans](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/flat-rate-pricing-plan.html)
documentation, read on 2026-10-28.

## Decision

We will subscribe the media distribution, its web ACL, and the custom domain's hosted zone to the
CloudFront Free flat-rate plan, through the `AWS::PricingPlanManager::Subscription` resource. The
`CloudFrontPricingPlan` parameter can opt out for accounts that already use their three Free plans.

## Consequences

- The media CDN cannot produce an overage bill. Under prolonged excess traffic, AWS can slow down
  delivery instead.
- The hosted zone attached to the plan stops being billed separately.
- The web ACL must stay associated while the distribution is on the plan. Opting out of the plan
  without removing the web ACL would bill the web ACL at pay-as-you-go rates. The template removes both
  together.
- The plan does not cover the Slack events function URL. ADR 3 bounds that cost.
