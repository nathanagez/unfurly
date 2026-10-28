from abc import ABC, abstractmethod
from pathlib import Path

from shared.entities import DownloadedReel, PublishedReel, UnfurlJob


class UnfurlJobQueue(ABC):
    @abstractmethod
    def enqueue(self, *, job: UnfurlJob) -> None: ...


class ReelDownloader(ABC):
    @abstractmethod
    def download(self, *, reel_url: str, target_dir: Path) -> DownloadedReel: ...


class MediaStore(ABC):
    @abstractmethod
    def publish(self, *, reel: DownloadedReel) -> PublishedReel: ...


class LinkUnfurler(ABC):
    @abstractmethod
    def unfurl(self, *, job: UnfurlJob, reel: DownloadedReel, published: PublishedReel) -> None: ...
