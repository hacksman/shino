# coding: utf-8
# @Time : 9/16/21 10:43 AM

from dataclasses import dataclass, field, fields


@dataclass
class SchInfo:
    _id: int
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

    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            current_val = self.__getattribute__(name)
            if current_val and not isinstance(current_val, field_type):
                current_type = type(current_val)
                raise TypeError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")

    def __init__(self, **kwargs):
        self.names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in self.names:
                setattr(self, k, v)
        self.__post_init__()

