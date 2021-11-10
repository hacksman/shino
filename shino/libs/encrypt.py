# coding: utf-8
# @Time : 9/8/21 9:39 AM

import hashlib
import ctypes

from shino.libs.python import to_bytes


def md5_i64(text):
    m = hashlib.md5()
    m.update(to_bytes(text))
    return ctypes.c_int64(int(m.hexdigest()[8:-8], 16)).value


def gen_md5(text):
    return hashlib.md5(to_bytes(text)).hexdigest()
