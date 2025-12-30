"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import requests as rq
import json

_session = rq.Session()

def send_telegram_message(message: str,
                          chat_id: str,
                          api_key: str,
                          parse_mode: str='HTML'):

    headers = {'Content-Type': 'application/json',
               'Proxy-Authorization': 'Basic base64'}
    data_dict = {'chat_id': chat_id,
                 'text': message,
                 'parse_mode': parse_mode,
                 'disable_notification': False}
    data = json.dumps(data_dict)
    url = f'https://api.telegram.org/bot{api_key}/sendMessage'
    response = _session.post(url, data=data, headers=headers, timeout=(5, 20))
    return response


def send_telegram_photo(message: str,
                          chat_id: str,
                          api_key: str,
                          photo_path: str,
                          parse_mode: str='HTML'):

    # headers = {'Content-Type': 'multipart/form-data',
    #            'Proxy-Authorization': 'Basic base64'}
    data_dict = {'chat_id': chat_id,
                 'caption': message,
                 'parse_mode': parse_mode,
                 'disable_notification': False}
    # data = json.dumps(data_dict)
    url = f'https://api.telegram.org/bot{api_key}/sendPhoto'
    response = rq.post(url, data=data_dict, files={'photo': open(photo_path, mode='rb')})
    return response