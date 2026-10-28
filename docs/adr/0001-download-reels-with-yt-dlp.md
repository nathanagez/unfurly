# 1. Download reels with yt-dlp

## Status

Accepted

## Context

Instagram offers no public API to fetch a reel posted by another account. The Instagram Graph API
only covers the business accounts that the caller manages. Paid scraping providers exist, but they
add a recurring cost and a third party that sees every shared link.

yt-dlp is an open source downloader with a maintained Instagram extractor. It calls the same web
endpoints as a logged-out browser. Tests from AWS Lambda in `us-east-1` succeeded without cookies.
Tests from a residential IPv4 address were refused, while IPv6 succeeded.

Meta's terms prohibit automated collection without permission, and the downloaded reels belong to
their creators.

## Decision

We will download reels with yt-dlp in the unfurl reel function, without an Instagram account or
cookies, and keep each download for about one day.

## Consequences

- unfurly costs nothing beyond AWS and needs no Instagram credentials.
- Instagram can block the approach at any time, by changing its endpoints or by refusing AWS
  addresses. A yt-dlp update fixes the first case. The second has no fix without cookies.
- The project is not suitable for a commercial product: it copies content without the rights to it.
  A version for sale would embed Instagram's official player instead of downloading the video.
- Short retention limits the copies that exist, but does not remove the terms of service concern.
