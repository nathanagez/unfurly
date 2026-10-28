from shared.entities import UnfurlJob
from shared.ports import UnfurlJobQueue


class FakeUnfurlJobQueue(UnfurlJobQueue):
    def __init__(self) -> None:
        self.jobs: list[UnfurlJob] = []

    def enqueue(self, *, job: UnfurlJob) -> None:
        self.jobs.append(job)
