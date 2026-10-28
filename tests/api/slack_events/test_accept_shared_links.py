from api.slack_events.use_cases.accept_shared_links import AcceptSharedLinks, SharedLinks
from shared.entities import UnfurlJob
from shared.testing.fakes import FakeUnfurlJobQueue

REEL_URL = "https://www.instagram.com/reel/CDUMkliABpa/"


class TestAcceptSharedLinks:
    def test_queues_one_job_per_reel_link_of_a_sent_message(self) -> None:
        use_case, queue = setup()
        other_reel_url = "https://instagram.com/reels/Chunk8-jurw/?igsh=abc"

        use_case.execute(shared_links=shared_links(urls=[REEL_URL, other_reel_url]))

        assert queue.jobs == [
            UnfurlJob(channel="C123", message_ts="1730000000.000100", reel_url=REEL_URL),
            UnfurlJob(channel="C123", message_ts="1730000000.000100", reel_url=other_reel_url),
        ]

    def test_ignores_links_typed_in_the_composer(self) -> None:
        use_case, queue = setup()

        use_case.execute(shared_links=shared_links(urls=[REEL_URL], source="composer"))

        assert queue.jobs == []

    def test_ignores_instagram_links_that_are_not_reels(self) -> None:
        use_case, queue = setup()

        use_case.execute(shared_links=shared_links(urls=["https://www.instagram.com/instagram/"]))

        assert queue.jobs == []


def shared_links(*, urls: list[str], source: str = "conversations_history") -> SharedLinks:
    return SharedLinks(source=source, channel="C123", message_ts="1730000000.000100", urls=urls)


def setup() -> tuple[AcceptSharedLinks, FakeUnfurlJobQueue]:
    queue = FakeUnfurlJobQueue()
    return AcceptSharedLinks(unfurl_job_queue=queue), queue
