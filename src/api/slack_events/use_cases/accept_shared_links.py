import re
from dataclasses import dataclass

from shared.entities import UnfurlJob
from shared.ports import UnfurlJobQueue

_SENT_MESSAGE_SOURCE = "conversations_history"
_REEL_URL = re.compile(r"^https://(www\.)?instagram\.com/reels?/[A-Za-z0-9_-]+")


@dataclass(frozen=True, kw_only=True)
class SharedLinks:
    source: str | None
    channel: str
    message_ts: str
    urls: list[str]


class AcceptSharedLinks:
    def __init__(self, *, unfurl_job_queue: UnfurlJobQueue) -> None:
        self._unfurl_job_queue = unfurl_job_queue

    def execute(self, *, shared_links: SharedLinks) -> None:
        if shared_links.source != _SENT_MESSAGE_SOURCE:
            return

        for url in shared_links.urls:
            if not _REEL_URL.match(url):
                continue
            self._unfurl_job_queue.enqueue(
                job=UnfurlJob(channel=shared_links.channel, message_ts=shared_links.message_ts, reel_url=url)
            )
