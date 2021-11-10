# coding: utf-8
# @Time : 9/16/21 10:43 AM

from dataclasses import dataclass, field, fields


@dataclass(init=False)
class SchInfo:
    _id: str
    name: str
    api: str
    seed_url: str
    appoint_crontab: str
    switch: str
    is_once: int
    method: str = 'get'
    post_data: dict = field(default=None, repr=False)
    get_from: str = field(default=None, repr=False)
    get_from_conf: dict = field(default=None, repr=False)
    get_from_filter: dict = field(default=None, repr=False)
    post_from: str = field(default=None, repr=False)
    post_from_conf: dict = field(default=None, repr=False)
    post_from_filter: dict = field(default=None, repr=False)
    priority: int = field(default=4, repr=False)
    interval: int = field(default=0, repr=False)
    get_many: dict = field(default=None, repr=False)
    post_many: dict = field(default=None, repr=True)

    def __init__(self, **kwargs):
        self.names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in self.names:
                setattr(self, k, v)

