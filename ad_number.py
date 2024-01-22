"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

def float_to_vnd(a_float, remove_decimal=True):
    a_str = '{:0,.2f}'.format(a_float).replace('.', '#').replace(',', '.').replace('#', ',')
    if remove_decimal:
        a_str = a_str.replace(',00', '')
    return a_str


def float_to_usd(a_float):
    return '${:0,.2f}'.format(a_float)


def vnd_to_float(a_vnd_str):
    return float(a_vnd_str.replace('.', '').replace(',', '.'))


def usd_to_float(a_usd_str):
    return float(a_usd_str.replace('$', '').replace(',', ''))
