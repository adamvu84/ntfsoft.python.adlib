"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import urllib.request
import urllib.parse
import requests as rq
import time
import ssl


def ad_download_file(url, file_to_write):
    """
    Dowload file from url and save to file_to_write

    Parameters
    ----------
    url : string
        url to a file.
    file_to_write : string
        full path to file to be written.

    Returns
    -------
    None.

    """
    urllib.request.urlretrieve(url, file_to_write)


def ad_download_page(url, decode_utf8=True, encoding='utf-8'):
    """
    Download a page

    Parameters
    ----------
    url : string

    Returns
    -------
    binary string
        source code of webpage.

    """
    resp = urllib.request.urlopen(url)
    if decode_utf8:
        return resp.read().decode(encoding)
    else:
        return resp.read()


def ad_read_page(logger, url, should_retry=False,
                 max_retry_time=3, sleep_time=10, should_decode=False):
    retry_time = 0
    s = ''
    while True:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'})
            f = urllib.request.urlopen(req)
            s = f.read()
            break
        except Exception as e:
            if str(e).find("Reached error page") > 0:
                logger.error("Bi block roi")
            else:
                logger.error('ad_read_page: ' + str(e))
            if should_retry:
                retry_time += 1
                time.sleep(sleep_time)
                if retry_time > max_retry_time:
                    break
            else:
                break
    if should_decode:
        return s.decode()
    else:
        return s


def ad_open_page(url, check_ssl_certification = True):
    if check_ssl_certification:
        return urllib.request.urlopen(url)
    else:
        return urllib.request.urlopen(url, context=ssl.SSLContext())


def ad_encode_url(url):
    return urllib.request.quote(url.encode('utf8'), ':/')


def ad_encode_string(a_string):
    return urllib.parse.quote_plus(a_string)


def ad_request_json(url):
    try:
        return rq.get(url).json()
    except:
        return None;


def ad_post_request(logger, url, data, add_headers = {}):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
    }
    headers.update(add_headers)
    response = rq.post(
        url,
        headers=headers,
        data=data)
    if response.ok:
        return response.json()
    else:
        try:
            # Attempt to parse the error response as JSON
            error_json = response.json()
            logger.error("ad_post_request.Error JSON:")
            logger.error(error_json)
        except ValueError:
            # If parsing as JSON fails, print the raw content
            logger.error("ad_post_request.Error Content:")
            logger.error(response.text)
        return None


def ad_get_request_json(logger, url, data, headers = {}):
    response = rq.get(
        url,
        headers=headers)
    if response.ok:
        return response.json()
    else:
        try:
            # Attempt to parse the error response as JSON
            error_json = response.json()
            logger.error("ad_post_request.Error JSON:")
            logger.error(error_json)
            return error_json
        except ValueError:
            # If parsing as JSON fails, print the raw content
            logger.error("ad_post_request.Error Content:")
            logger.error(response.text)
            return None