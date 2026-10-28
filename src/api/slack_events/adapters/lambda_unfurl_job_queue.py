import json
from dataclasses import asdict
from typing import TYPE_CHECKING

from shared.entities import UnfurlJob
from shared.ports import UnfurlJobQueue

if TYPE_CHECKING:
    from mypy_boto3_lambda import LambdaClient


class LambdaUnfurlJobQueue(UnfurlJobQueue):
    def __init__(self, *, lambda_client: LambdaClient, function_name: str) -> None:
        self._lambda_client = lambda_client
        self._function_name = function_name

    def enqueue(self, *, job: UnfurlJob) -> None:
        self._lambda_client.invoke(
            FunctionName=self._function_name,
            InvocationType="Event",
            Payload=json.dumps(asdict(job)).encode(),
        )
