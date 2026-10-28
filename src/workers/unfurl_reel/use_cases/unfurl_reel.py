from pathlib import Path

from shared.entities import UnfurlJob
from shared.ports import LinkUnfurler, MediaStore, ReelDownloader


class UnfurlReel:
    def __init__(
        self, *, reel_downloader: ReelDownloader, media_store: MediaStore, link_unfurler: LinkUnfurler
    ) -> None:
        self._reel_downloader = reel_downloader
        self._media_store = media_store
        self._link_unfurler = link_unfurler

    def execute(self, *, job: UnfurlJob, work_dir: Path) -> None:
        reel = self._reel_downloader.download(reel_url=job.reel_url, target_dir=work_dir)
        published = self._media_store.publish(reel=reel)
        self._link_unfurler.unfurl(job=job, reel=reel, published=published)
