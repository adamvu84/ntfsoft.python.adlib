"""
Created on 27/05/2022 01:17

@author: Anh Duc
"""

import os
from os import listdir
from os.path import isfile, join, dirname
import io
import ntpath
import errno
import re
import json
from datetime import datetime, date
import logging
import configparser
from logging.handlers import TimedRotatingFileHandler

def ad_today():
    return date.today()


def ad_date_sql():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")


def ad_shortdate_str():
    now = datetime.now()
    return now.strftime("%Y%m%d")


def ad_datetime_str():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")


def ad_cur_time():
    return datetime.now()


def ad_time_as_int():
    return int(datetime.now().timestamp())


def ad_get_current_hour():
    now = datetime.now()
    return now.hour


def ad_sub_str(a_text, sign="", first_marker="", second_marker="", cut=False):
    sub_text = ""
    b_text = a_text
    if sign != "":
        sign_pos = a_text.find(sign)
        if sign_pos == -1:
            return sub_text, a_text
        b_text = a_text[sign_pos + len(sign):]

    if first_marker == "":
        first_pos = 0
    else:
        first_pos = b_text.find(first_marker)

    if first_pos == -1:
        return sub_text, b_text

    first_pos = first_pos + len(first_marker)

    if second_marker == "":
        sub_text = b_text[first_pos:]
    else:
        second_pos = b_text.find(second_marker, first_pos)
        if second_pos == -1:
            return sub_text, b_text
        sub_text = b_text[first_pos:second_pos]

    if cut:
        second_pos = second_pos + len(second_marker)
        a_text = b_text[second_pos:]

    return sub_text, a_text


def ad_replace_substr(a_text, sign="", first_marker="", second_marker="",
                      str_to_find="", str_to_replace=""):
    if sign != '':
        sign_pos = a_text.find(sign)
        if sign_pos == -1:
            return a_text
    else:
        sign_pos = 0

    if first_marker != '':
        first_pos = a_text.find(first_marker, sign_pos)
        if first_pos == -1:
            return a_text
    else:
        first_pos = sign_pos

    if second_marker != '':
        second_pos = a_text.find(second_marker, first_pos)
        if second_pos == -1:
            return a_text
    else:
        second_pos = len(a_text) - 1

    third_pos = a_text.find(str_to_find, first_pos, second_pos)
    if third_pos == -1:
        return a_text
    else:
        return a_text[:third_pos] + str_to_replace
    + a_text[third_pos + len(str_to_find):]


def ad_safe_open_w(path, is_append=False):
    ad_mkdir_p(os.path.dirname(path))
    if is_append:
        return open(path, 'a')
    return open(path, 'w+')


def ad_safe_open_b(path, is_append=False):
    ad_mkdir_p(os.path.dirname(path))
    if is_append:
        return open(path, 'ab')
    return open(path, 'wb')


def ad_mkdir_p(path):
    if path == "":
        return
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def ad_save_text(txt, write_to, is_append=False):
    write_mode = 'wb'
    if is_append:
        write_mode += 'a'
    with open(write_to, write_mode) as fp:
        fp.write(txt.encode('utf-8'))


def ad_write_file(string_to_be_written, file_to_write, is_append=False):
    text_file = ad_safe_open_w(file_to_write, is_append)
    text_file.write(string_to_be_written)
    text_file.close()


def ad_write_file_u(string_to_be_written, file_to_write, is_append=False):
    text_file = ad_safe_open_b(file_to_write, is_append)
    text_file.write(string_to_be_written)
    text_file.close()


def ad_write_dict_to_file(a_dict, file_to_write, write_utf8=True):
    s = json.dumps(a_dict)
    if write_utf8:
        s = s.encode('utf-8')
    text_file = ad_safe_open_b(file_to_write)
    text_file.write(s)
    text_file.close()


def ad_read_file(file_to_read, read_utf8=True):
    if read_utf8:
        f = io.open(file_to_read, mode="r", encoding="utf-8")
    else:
        f = io.open(file_to_read, mode="r", encoding="utf-8")
    s = f.read()
    f.close()
    return s


def ad_read_file_to_list(file_to_read, read_utf8=True):
    if not os.path.isfile(file_to_read):
        return []

    if read_utf8:
        read_encoding = 'utf-8'
    else:
        read_encoding = ''
    a_list = []
    with open(file_to_read, mode="r", encoding=read_encoding) as file:
        for line in file:
            a_list.append(line.strip())
    return a_list


def ad_move_file(source, dest):
    os.rename(source, dest)


def ad_list_files(path_to_list, file_pattern=''):
    if path_to_list == "":
        path_to_list = os.getcwd()
    if file_pattern == '':
        return [join(path_to_list, f) for f in listdir(path_to_list)
                if isfile(join(path_to_list, f))]
    else:
        return [join(path_to_list, f) for f in listdir(path_to_list) if
                isfile(join(path_to_list, f)) and (re.match(file_pattern, f))]


def ad_list_dirs(path_to_dir, dir_pattern=''):
    if path_to_dir == "":
        path_to_dir = os.getcwd()
    list_dir = next(os.walk(path_to_dir))[1]
    if dir_pattern == '':
        return [join(path_to_dir, d) for d in list_dir]
    else:
        return [join(path_to_dir, d) for d in list_dir if (re.match(dir_pattern, d))]


def ad_append_path(root_path, appended_part):
    return os.path.join(root_path, '') + appended_part

def ad_extract_filename(file_path):
    return ntpath.basename(file_path)


def ad_init_log(logger_name, file_path):
    parent_directory = dirname(file_path)
    ad_mkdir_p(parent_directory)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # Create handlers
    fhandler = TimedRotatingFileHandler(file_path, when="midnight", interval=1, encoding='utf8')
    fhandler.setLevel(logging.INFO)
    fhandler.suffix = "%Y%m%d"
    # Create formatters and add it to handlers
    f_format = logging.Formatter(
        fmt='%(asctime)s %(levelname)s [line %(lineno)d]: %(message)s')
    fhandler.setFormatter(f_format)

    # Add handlers to the logger
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.addHandler(fhandler)
    return logger


def find_in_array(arr, item):
    try:
        return arr.index(item)
    except ValueError as ve:
        return -1


def to_float(a_string):
    try:
        return round(float(a_string), 2)
    except Exception as e:
        return 0


def to_sql_date(a_date_string, original_date_format):
    a_date = datetime.strptime(a_date_string, original_date_format)
    return a_date.strftime("%Y-%m-%d")


def ad_read_tuple_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return tuple(data) if isinstance(data, list) else None
    except Exception as e:
        print(f"Error reading from file: {e}")
        return None


def ad_save_tuple_to_file(data, filename='tuple.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error saving to file: {e}")


def ad_dump_json_to_file(data, filename='data.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving to file: {e}")


def read_app_config(config_file_path, section, key):
    try:
        config_parser = configparser.RawConfigParser(allow_no_value=True)
        config_parser.read(config_file_path)
        return config_parser.get(section, key)
    except Exception as e:
        print(f"Error read_app_config: {e}")
        return None


def read_config_section(config_file_path, section):
    try:
        config_parser = configparser.RawConfigParser(allow_no_value=True)
        config_parser.read(config_file_path)
        for sec in config_parser.sections():
            if sec == section:
                return dict(config_parser.items(sec))
        return None
    except Exception as e:
        print(f"Error read_config_section: {e}")
        return None
