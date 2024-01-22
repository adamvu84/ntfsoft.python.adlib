"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

from selenium import webdriver
import time


def ad_webdriver_get_page_source(logger, webdriver, url, should_retry=True,
                                 max_retry_time=3, sleep_time=10):
    get_page_ok = False
    retry_time = 0
    while True:
        try:
            webdriver.get(url)
            time.sleep(10)
            get_page_ok = True
            break
        except Exception as e:
            if str(e).find("Reached error page") > 0:
                logger.error("Bi block roi")
            else:
                logger.error(str(e))
            if should_retry:
                retry_time += 1
                time.sleep(sleep_time)
                if retry_time > max_retry_time:
                    break
            else:
                break
    if get_page_ok:
        return webdriver.page_source
    else:
        return ''


def ad_webdriver_get_source(bin_location, logger, url, should_retry=True,
                            max_retry_time=3, sleep_time=10):
    try:
        logger.info('start get url = ' + url)
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        # r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        options.binary_location = bin_location
        driver = webdriver.Firefox(options=options)
        get_page_ok = False
        retry_time = 0
        while True:
            try:
                driver.get(url)
                time.sleep(10)
                get_page_ok = True
                break
            except Exception as e:
                if str(e).find("Reached error page") > 0:
                    logger.error("Bi block roi")
                else:
                    logger.error(str(e))
                if should_retry:
                    retry_time += 1
                    time.sleep(sleep_time)
                    if retry_time > max_retry_time:
                        break
                else:
                    break
        s = driver.page_source
        driver.close()
        logger.info('end get url')
    except Exception as e:
        raise Exception('ad_webdriver_get_source: ' + str(e))
    if get_page_ok:
        return s
    else:
        return ''
