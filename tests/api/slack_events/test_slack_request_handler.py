import json
import time
from http import HTTPStatus
from typing import Any

from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent
from slack_sdk.signature import SignatureVerifier

from api.slack_events.slack_request_handler import SlackRequestHandler
from api.slack_events.use_cases.accept_shared_links import AcceptSharedLinks
from shared.testing.fakes import FakeUnfurlJobQueue

SIGNING_SECRET = "test-signing-secret"
LINK_SHARED_PAYLOAD = {
    "type": "event_callback",
    "event": {
        "type": "link_shared",
        "source": "conversations_history",
        "channel": "C123",
        "message_ts": "1730000000.000100",
        "links": [{"domain": "instagram.com", "url": "https://www.instagram.com/reel/CDUMkliABpa/"}],
    },
}


class TestSlackRequestHandler:
    def test_rejects_a_request_with_an_invalid_signature(self) -> None:
        handler, queue = setup()
        request = signed_request(payload=LINK_SHARED_PAYLOAD)
        request["headers"]["x-slack-signature"] = "v0=forged"

        response = handler.handle(request=LambdaFunctionUrlEvent(request))

        assert response["statusCode"] == HTTPStatus.UNAUTHORIZED
        assert queue.jobs == []

    def test_answers_the_url_verification_challenge(self) -> None:
        handler, _ = setup()
        request = signed_request(payload={"type": "url_verification", "challenge": "abc123"})

        response = handler.handle(request=LambdaFunctionUrlEvent(request))

        assert response["statusCode"] == HTTPStatus.OK
        assert response["body"] == "abc123"

    def test_acknowledges_a_slack_retry_without_queuing_the_reel_again(self) -> None:
        handler, queue = setup()
        request = signed_request(payload=LINK_SHARED_PAYLOAD)
        request["headers"]["x-slack-retry-num"] = "1"

        response = handler.handle(request=LambdaFunctionUrlEvent(request))

        assert response["statusCode"] == HTTPStatus.OK
        assert queue.jobs == []


def signed_request(*, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload)
    timestamp = str(int(time.time()))
    signature = SignatureVerifier(signing_secret=SIGNING_SECRET).generate_signature(
        timestamp=timestamp, body=body
    )
    return {
        "headers": {"x-slack-request-timestamp": timestamp, "x-slack-signature": signature},
        "body": body,
        "isBase64Encoded": False,
    }


def setup() -> tuple[SlackRequestHandler, FakeUnfurlJobQueue]:
    queue = FakeUnfurlJobQueue()
    handler = SlackRequestHandler(
        signature_verifier=SignatureVerifier(signing_secret=SIGNING_SECRET),
        accept_shared_links=AcceptSharedLinks(unfurl_job_queue=queue),
    )
    return handler, queue
