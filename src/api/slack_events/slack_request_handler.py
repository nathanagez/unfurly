import json
from http import HTTPStatus
from typing import Any

from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent
from slack_sdk.signature import SignatureVerifier

from api.slack_events.use_cases.accept_shared_links import AcceptSharedLinks, SharedLinks


class SlackRequestHandler:
    def __init__(
        self, *, signature_verifier: SignatureVerifier, accept_shared_links: AcceptSharedLinks
    ) -> None:
        self._signature_verifier = signature_verifier
        self._accept_shared_links = accept_shared_links

    def handle(self, *, request: LambdaFunctionUrlEvent) -> dict[str, Any]:
        body = request.decoded_body or ""
        if not self._signature_verifier.is_valid(
            body=body,
            timestamp=request.headers.get("x-slack-request-timestamp"),
            signature=request.headers.get("x-slack-signature"),
        ):
            return _text_response(status=HTTPStatus.UNAUTHORIZED, text="invalid signature")

        if request.headers.get("x-slack-retry-num") is not None:
            return _text_response(status=HTTPStatus.OK, text="")

        payload = json.loads(body)
        if payload["type"] == "url_verification":
            return _text_response(status=HTTPStatus.OK, text=payload["challenge"])

        if payload["type"] == "event_callback" and payload["event"]["type"] == "link_shared":
            self._accept_shared_links.execute(shared_links=_to_shared_links(event=payload["event"]))
        return _text_response(status=HTTPStatus.OK, text="")


def _to_shared_links(*, event: dict[str, Any]) -> SharedLinks:
    return SharedLinks(
        source=event.get("source"),
        channel=event["channel"],
        message_ts=event["message_ts"],
        urls=[link["url"] for link in event["links"]],
    )


def _text_response(*, status: HTTPStatus, text: str) -> dict[str, Any]:
    return {"statusCode": status.value, "headers": {"content-type": "text/plain"}, "body": text}
