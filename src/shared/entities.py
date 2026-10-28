from dataclasses import dataclass
from pathlib import Path

_DEFAULT_AUTHOR_HANDLE = "instagram"


@dataclass(frozen=True, kw_only=True)
class UnfurlJob:
    channel: str
    message_ts: str
    reel_url: str


@dataclass(frozen=True, kw_only=True)
class DownloadedReel:
    shortcode: str
    author_handle: str | None
    caption: str
    video_path: Path
    thumbnail_path: Path

    @property
    def author(self) -> str:
        return f"@{self.author_handle or _DEFAULT_AUTHOR_HANDLE}"

    @property
    def title(self) -> str:
        return " ".join(self.caption.split()) or f"Reel by {self.author}"


@dataclass(frozen=True, kw_only=True)
class PublishedReel:
    player_url: str
    thumbnail_url: str
