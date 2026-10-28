import os
from typing import Any

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

TARGET_FUNCTION_NAME = os.environ["TARGET_FUNCTION_NAME"]
DISABLED_CONCURRENCY = 0

logger = Logger()
lambda_client = boto3.client("lambda")


@logger.inject_lambda_context
def lambda_handler(event: dict[str, Any], _context: LambdaContext) -> None:
    lambda_client.put_function_concurrency(
        FunctionName=TARGET_FUNCTION_NAME, ReservedConcurrentExecutions=DISABLED_CONCURRENCY
    )
    logger.warning(
        "Kill switch disabled target function",
        extra={"function_name": TARGET_FUNCTION_NAME, "alarm_name": event["alarmData"]["alarmName"]},
    )
