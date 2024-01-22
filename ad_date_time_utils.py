"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

from datetime import datetime


def ad_date_time_vn():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def ad_date_sql():
    return datetime.now().strftime("%Y-%m-%d")


def ad_to_sql_date(a_date):
    return a_date.strftime("%Y-%m-%d")


def ad_date_time_sql():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ad_shortdate_str():
    return datetime.now().strftime("%Y%m%d")


def ad_cur_time():
    return datetime.now()


def ad_time_as_int():
    return int(datetime.now().timestamp())
