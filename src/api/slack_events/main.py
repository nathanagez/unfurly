import os
from typing import Any

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from slack_sdk.signature import SignatureVerifier

from api.slack_events.adapters.lambda_unfurl_job_queue import LambdaUnfurlJobQueue
from api.slack_events.slack_request_handler import SlackRequestHandler
from api.slack_events.use_cases.accept_shared_links import AcceptSharedLinks
from shared.slack_credentials import load_slack_credentials

SLACK_PARAMETER_NAME = os.environ["SLACK_PARAMETER_NAME"]
UNFURL_REEL_FUNCTION_NAME = os.environ["UNFURL_REEL_FUNCTION_NAME"]

logger = Logger()
accept_shared_links = AcceptSharedLinks(
    unfurl_job_queue=LambdaUnfurlJobQueue(
        lambda_client=boto3.client("lambda"), function_name=UNFURL_REEL_FUNCTION_NAME
    )
)


@logger.inject_lambda_context
def lambda_handler(event: dict[str, Any], _context: LambdaContext) -> dict[str, Any]:
    slack_credentials = load_slack_credentials(parameter_name=SLACK_PARAMETER_NAME)
    slack_request_handler = SlackRequestHandler(
        signature_verifier=SignatureVerifier(signing_secret=slack_credentials.signing_secret),
        accept_shared_links=accept_shared_links,
    )
    return slack_request_handler.handle(request=LambdaFunctionUrlEvent(event))
