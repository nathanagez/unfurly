from dataclasses import dataclass

from aws_lambda_powertools.utilities.parameters import get_parameter

_CACHE_SECONDS = 300


@dataclass(frozen=True, kw_only=True)
class SlackCredentials:
    bot_token: str
    signing_secret: str


def load_slack_credentials(*, parameter_name: str) -> SlackCredentials:
    value: dict[str, str] = get_parameter(
        parameter_name, transform="json", decrypt=True, max_age=_CACHE_SECONDS
    )
    return SlackCredentials(bot_token=value["slack_bot_token"], signing_secret=value["slack_signing_secret"])
