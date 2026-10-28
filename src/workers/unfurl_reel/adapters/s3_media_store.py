import mimetypes
from html import escape
from pathlib import Path
from typing import TYPE_CHECKING

from shared.entities import DownloadedReel, PublishedReel
from shared.ports import MediaStore

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client

_DEFAULT_CONTENT_TYPE = "application/octet-stream"


class S3MediaStore(MediaStore):
    def __init__(self, *, s3_client: S3Client, bucket_name: str, public_base_url: str) -> None:
        self._s3_client = s3_client
        self._bucket_name = bucket_name
        self._public_base_url = public_base_url

    def publish(self, *, reel: DownloadedReel) -> PublishedReel:
        video_key = f"reels/{reel.shortcode}.mp4"
        thumbnail_key = f"reels/{reel.shortcode}{reel.thumbnail_path.suffix}"
        player_key = f"v/{reel.shortcode}"

        self._s3_client.upload_file(
            str(reel.video_path), self._bucket_name, video_key, ExtraArgs={"ContentType": "video/mp4"}
        )
        self._s3_client.upload_file(
            str(reel.thumbnail_path),
            self._bucket_name,
            thumbnail_key,
            ExtraArgs={"ContentType": _content_type(path=reel.thumbnail_path)},
        )
        self._s3_client.put_object(
            Bucket=self._bucket_name,
            Key=player_key,
            Body=_player_page(title=reel.title, video_path=f"/{video_key}", poster_path=f"/{thumbnail_key}"),
            ContentType="text/html; charset=utf-8",
        )

        return PublishedReel(
            player_url=f"{self._public_base_url}/{player_key}",
            thumbnail_url=f"{self._public_base_url}/{thumbnail_key}",
        )


def _content_type(*, path: Path) -> str:
    content_type, _ = mimetypes.guess_type(path.name)
    return content_type or _DEFAULT_CONTENT_TYPE


def _player_page(*, title: str, video_path: str, poster_path: str) -> str:
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>html,body{{margin:0;height:100%;overflow:hidden;background:#000}}video{{width:100%;height:100%;object-fit:contain}}</style>
</head>
<body><video src="{video_path}" poster="{poster_path}" controls playsinline></video></body>
</html>
"""
