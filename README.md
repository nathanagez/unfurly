# unfurly

Unfurls Instagram reel links posted in Slack into a video that plays inside Slack.

When someone posts an `instagram.com/reel/...` link, the Slack app replaces the link preview with a
video player. A Lambda function downloads the reel, stores it in S3 behind CloudFront for about a day,
and calls `chat.unfurl` with a Block Kit video block.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Background

Not everyone in a Slack workspace has an Instagram account, so a shared reel often goes unwatched.
unfurly plays it where the conversation happens.

unfurly downloads reels with [yt-dlp](https://github.com/yt-dlp/yt-dlp) through Instagram's web
endpoints, without an account. Meta's terms prohibit automated collection without permission, and the
reels belong to their creators. Use it for personal or internal sharing, keep the one-day retention,
and read [ADR 1](docs/adr/0001-download-reels-with-yt-dlp.md) before you build on it. unfurly is not
affiliated with Meta, Instagram, or Slack.

## Install

Requires `uv`, the AWS CLI v2, the AWS SAM CLI, Python 3, and AWS credentials for the target account.

```bash
uv sync
```

## Usage

Deploy to an AWS account in `us-east-1`, with the CloudFront domain as the public domain. The first
command stores the Slack credentials: placeholders are fine until the Slack app exists.

```bash
./scripts/set-slack-credentials.sh
sam build
sam deploy --guided
./scripts/render-slack-manifest.sh
```

Create the Slack app from the rendered manifest, then run `./scripts/set-slack-credentials.sh` again
with its signing secret and bot token. Post a reel link in a channel to see the video. The full
procedure, including a custom domain, is in
[How to deploy unfurly to an AWS account](docs/how-to/how-to-deploy-to-an-aws-account.md).

## Documentation

- How-to:
  - [How to deploy unfurly to an AWS account](docs/how-to/how-to-deploy-to-an-aws-account.md)
  - [How to create the Slack app](docs/how-to/how-to-create-the-slack-app.md)
  - [How to deploy with GitHub Actions](docs/how-to/how-to-deploy-with-github-actions.md)
  - [How to re-enable unfurly after the kill switch](docs/how-to/how-to-re-enable-after-the-kill-switch.md)
  - [How to remove unfurly from an AWS account](docs/how-to/how-to-remove-unfurly-from-an-aws-account.md)
- Reference: [Configuration](docs/reference/configuration.md)
- Explanation: [About the architecture and its costs](docs/explanation/about-architecture-and-costs.md)
- Decisions: [docs/adr](docs/adr/)

## Contributing

Issues and pull requests are welcome. Use a Conventional Commits title for pull requests:
release-please creates releases from the commit history. Run the checks that CI runs before you push:

```bash
uv run ruff format --check src tests && uv run ruff check src tests && uv run mypy src tests && uv run pytest
sam validate --lint --region us-east-1
```

## License

[MIT](LICENSE) © Nathan Agez
