# -*- coding: utf-8 -*-
from json import loads as json_loads

from requests import get as requests_get

from Aureid.api_calls.core import HEADERS, BASE_URL
from Aureid.logging import rich_log


def get_message(channel_id: str, message_id: str) -> dict or None:
    req = requests_get(
        f'{BASE_URL}/channels/{channel_id}/messages/{message_id}',
        headers=HEADERS
    )
    res = json_loads(req.content)
    if req.status_code != 200:
        rich_log.critical(res['code'])
        rich_log.critical(res['message'])
        return None
    return res['message']
