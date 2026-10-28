from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL

from shared.entities import DownloadedReel
from shared.ports import ReelDownloader

_PROGRESSIVE_MP4 = "b[ext=mp4]"


class ThumbnailNotDownloadedError(Exception):
    def __init__(self, *, shortcode: str) -> None:
        super().__init__(f"yt-dlp did not download a thumbnail for reel {shortcode}")


class YtDlpReelDownloader(ReelDownloader):
    def download(self, *, reel_url: str, target_dir: Path) -> DownloadedReel:
        with YoutubeDL(_options(target_dir=target_dir)) as youtube_dl:
            info: dict[str, Any] = youtube_dl.extract_info(reel_url, download=True)

        return DownloadedReel(
            shortcode=info["id"],
            author_handle=info.get("channel"),
            caption=info.get("description") or "",
            video_path=Path(info["requested_downloads"][0]["filepath"]),
            thumbnail_path=_thumbnail_path(info=info),
        )


def _thumbnail_path(*, info: dict[str, Any]) -> Path:
    thumbnail_file = next((thumb["filepath"] for thumb in info["thumbnails"] if "filepath" in thumb), None)
    if thumbnail_file is None:
        raise ThumbnailNotDownloadedError(shortcode=info["id"])
    return Path(thumbnail_file)


def _options(*, target_dir: Path) -> dict[str, Any]:
    return {
        "format": _PROGRESSIVE_MP4,
        "outtmpl": str(target_dir / "%(id)s.%(ext)s"),
        "writethumbnail": True,
        "cachedir": False,
        "quiet": True,
        "noprogress": True,
    }
