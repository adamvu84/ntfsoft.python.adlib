"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import requests as rq
import json


def send_telegram_message(message: str,
                          chat_id: str,
                          api_key: str,
                          parse_mode: str='HTML'):

    headers = {'Content-Type': 'application/json',
               'Proxy-Authorization': 'Basic base64'}
    data_dict = {'chat_id': chat_id,
                 'text': message,
                 'parse_mode': parse_mode,
                 'disable_notification': True}
    data = json.dumps(data_dict)
    url = f'https://api.telegram.org/bot{api_key}/sendMessage'
    response = rq.post(url, data=data, headers=headers)
    return response