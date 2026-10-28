from typing import Any

from slack_sdk import WebClient

from shared.entities import DownloadedReel, PublishedReel, UnfurlJob
from shared.ports import LinkUnfurler

_MAX_TITLE_LENGTH = 199
_MAX_AUTHOR_LENGTH = 49


class SlackLinkUnfurler(LinkUnfurler):
    def __init__(self, *, web_client: WebClient, provider_name: str) -> None:
        self._web_client = web_client
        self._provider_name = provider_name

    def unfurl(self, *, job: UnfurlJob, reel: DownloadedReel, published: PublishedReel) -> None:
        block = _video_block(reel=reel, published=published, provider_name=self._provider_name)
        self._web_client.chat_unfurl(
            channel=job.channel, ts=job.message_ts, unfurls={job.reel_url: {"blocks": [block]}}
        )


def _video_block(*, reel: DownloadedReel, published: PublishedReel, provider_name: str) -> dict[str, Any]:
    return {
        "type": "video",
        "title": {"type": "plain_text", "text": reel.title[:_MAX_TITLE_LENGTH]},
        "title_url": published.player_url,
        "video_url": published.player_url,
        "thumbnail_url": published.thumbnail_url,
        "alt_text": reel.title,
        "author_name": reel.author[:_MAX_AUTHOR_LENGTH],
        "provider_name": provider_name,
    }
