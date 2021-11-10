# coding: utf-8
# @Time : 7/8/21 11:00 AM

import os

from loguru import logger

from shino.libs.misc import root_path


single_logger = {}


class LogExt(object):
    # 存放目录名称
    folder = f'{root_path()}/logs'

    __default_file_name = "default.log"

    def __init__(self, filename=None, folder=None, **kwargs):

        self.file_name = filename

        if filename not in single_logger:

            filename = filename or self.__default_file_name

            self.folder = folder or self.folder

            if not os.path.exists(self.folder):
                os.mkdir(self.folder)

            self.file = f"{self.folder}/{filename}"

            retention = kwargs.get("retention") or 10

            rotation = kwargs.get("rotation") or "10 MB"

            level = kwargs.get('level', 'INFO')

            self.i = logger.add(self.file, retention=retention, rotation=rotation, level=level)

            single_logger[self.file_name] = logger

    @property
    def get_logger(self):
        return single_logger[self.file_name]
