import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from slack_sdk import WebClient

from shared.entities import UnfurlJob
from shared.slack_credentials import load_slack_credentials
from workers.unfurl_reel.adapters.s3_media_store import S3MediaStore
from workers.unfurl_reel.adapters.slack_link_unfurler import SlackLinkUnfurler
from workers.unfurl_reel.adapters.yt_dlp_reel_downloader import YtDlpReelDownloader
from workers.unfurl_reel.use_cases.unfurl_reel import UnfurlReel

SLACK_PARAMETER_NAME = os.environ["SLACK_PARAMETER_NAME"]
MEDIA_BUCKET_NAME = os.environ["MEDIA_BUCKET_NAME"]
PUBLIC_BASE_URL = os.environ["PUBLIC_BASE_URL"]
UNFURL_PROVIDER_NAME = os.environ["UNFURL_PROVIDER_NAME"]

logger = Logger()
reel_downloader = YtDlpReelDownloader()
media_store = S3MediaStore(
    s3_client=boto3.client("s3"), bucket_name=MEDIA_BUCKET_NAME, public_base_url=PUBLIC_BASE_URL
)


@logger.inject_lambda_context
def lambda_handler(event: dict[str, Any], _context: LambdaContext) -> None:
    job = UnfurlJob(channel=event["channel"], message_ts=event["message_ts"], reel_url=event["reel_url"])
    logger.info("Unfurling reel", extra={"channel": job.channel})

    slack_credentials = load_slack_credentials(parameter_name=SLACK_PARAMETER_NAME)
    unfurl_reel = UnfurlReel(
        reel_downloader=reel_downloader,
        media_store=media_store,
        link_unfurler=SlackLinkUnfurler(
            web_client=WebClient(token=slack_credentials.bot_token), provider_name=UNFURL_PROVIDER_NAME
        ),
    )

    with TemporaryDirectory() as work_dir:
        unfurl_reel.execute(job=job, work_dir=Path(work_dir))
