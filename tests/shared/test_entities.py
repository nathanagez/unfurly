from pathlib import Path

from shared.entities import DownloadedReel


class TestDownloadedReel:
    def test_uses_the_caption_on_a_single_line_as_title(self) -> None:
        reel = downloaded_reel(caption="Mountain lake\n\nclose by   to practice SUP")

        assert reel.title == "Mountain lake close by to practice SUP"

    def test_falls_back_to_the_author_when_the_caption_is_empty(self) -> None:
        reel = downloaded_reel(caption="  \n ")

        assert reel.title == "Reel by @clippedinandfree"

    def test_credits_instagram_when_the_author_handle_is_unknown(self) -> None:
        reel = downloaded_reel(author_handle=None)

        assert reel.author == "@instagram"


def downloaded_reel(
    *, caption: str = "I definitely need a mountain lake", author_handle: str | None = "clippedinandfree"
) -> DownloadedReel:
    return DownloadedReel(
        shortcode="CDUMkliABpa",
        author_handle=author_handle,
        caption=caption,
        video_path=Path("/tmp/CDUMkliABpa.mp4"),
        thumbnail_path=Path("/tmp/CDUMkliABpa.jpg"),
    )
