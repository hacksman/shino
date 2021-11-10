# coding: utf-8
# @Time : 7/8/21 11:01 AM

import os
import re
import six
import argparse
import base64
import json
import collections

from math import ceil
from os import path, listdir


def base64_encode_json(obj):
    order_data = collections.OrderedDict()
    for k in sorted(obj.keys()):
        order_data[k] = obj[k]
    return base64.encodebytes(bytes(json.dumps(order_data), "utf-8"))


def base64_decode_json(string):
    return json.loads(base64.b64decode(string))


class _PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return json.JSONEncoder.default(self, obj)
        return "<function or lambda>"


def json_format(obj, single_line=False):
    if single_line:
        return json.dumps(obj, sort_keys=True, ensure_ascii=False, cls=_PythonObjectEncoder)  # 排序并且缩进两个字符输出
    return json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False, cls=_PythonObjectEncoder)  # 排序并且缩进两个字符输出


def root_path(current_path=None, pattern=None):
    DEFAULT_ROOT_FILENAME_MATCH_PATTERN = '.git|requirements.txt|.gitignore'

    current_path = current_path or os.getcwd()
    current_path = path.abspath(path.normpath(path.expanduser(current_path)))
    pattern = pattern or DEFAULT_ROOT_FILENAME_MATCH_PATTERN

    if not path.isdir(current_path):
        current_path = path.dirname(current_path)

    def find_root_path(current_path, pattern=None):
        if isinstance(pattern, six.string_types):
            pattern = re.compile(pattern)

        detecting = True

        while detecting:
            file_names = listdir(current_path)
            found_more_files = bool(len(file_names) > 0)

            if not found_more_files:
                return None

            root_file_names = filter(pattern.match, file_names)
            root_file_names = list(root_file_names)

            found_root = bool(len(root_file_names) > 0)

            if found_root:
                return current_path

            found_system_root = bool(current_path == path.sep)

            if found_system_root:
                return None

            current_path = path.abspath(path.join(current_path, '..'))

    return find_root_path(current_path, pattern)


def get_all_args(set_env="local_4_prod"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", dest="env", default=set_env, help="env: local, dev, prod")
    args = parser.parse_args()
    return args


class Pager:

    def __init__(self, page, page_size, start=1, total=0):
        self.page = page
        self.page_size = page_size
        self.start = start
        self.total = total

    @property
    def total_page(self):
        if self.page_size == 0:
            return 0
        else:
            return int(ceil(self.total / self.page_size))

    @property
    def has_prev(self):
        return self.page > self.start

    @property
    def has_next(self):
        return self.total_page > self.page

    @property
    def prev_page(self):
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def next_page(self):
        if not self.has_next:
            return None
        return self.page + 1

    @property
    def iter_page(self):
        for num in range(self.start, self.total_page + 1):
            yield num
