# -*- coding: utf-8 -*-
from Aureid.config import BOT_TOKEN

BASE_URL = 'https://www.guilded.gg/api/v1'
HEADERS = {
    'Authorization': f'Bearer {BOT_TOKEN}',
    'Accept': 'application/json',
    'Content-type': 'application/json'
}
