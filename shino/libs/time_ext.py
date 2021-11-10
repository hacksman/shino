# coding: utf-8
# @Time : 9/8/21 9:47 AM


import arrow

from datetime import (datetime, timedelta)
from pytz import timezone


class TimeExt:

    @classmethod
    def datetime_to_human(cls, t=None, fmt="%Y-%m-%d %H:%M:%S", only_date=False):
        t = arrow.now() if not t else t
        fmt = fmt if not only_date else "%Y-%m-%d"
        return t.strftime(fmt)

    @classmethod
    def timestamp_to_human(cls, t=None, fmt="%Y-%m-%d %H:%M:%S"):
        t = arrow.now().timestamp if (t != 0 and not t) else t
        time_now = arrow.get(t).shift(hours=+8).strftime(fmt)
        return time_now

    @classmethod
    def human_date_to_timestamp(cls, t=None):
        time_stamp = arrow.get(t).shift(hours=-8).timestamp
        return time_stamp

    @classmethod
    def human_date_to_datetime(cls, t=None, fmt="%Y-%m-%d %H:%M:%S"):
        date_time = datetime.strptime(t or cls.timestamp_to_human(), fmt)
        return date_time

    @classmethod
    def datetime_timedelta(cls, before_datetime, seconds):
        date_time = before_datetime + timedelta(seconds=seconds)
        return date_time

    @classmethod
    def convert_playtime(cls, seconds):
        return str(timedelta(seconds=seconds))

    @classmethod
    def datetime_now(cls):
        return datetime.now()

    @classmethod
    def datetime_start(cls, t=None, date_type="day"):
        t = t if t else cls.datetime_now()
        return arrow.get(t).floor(date_type).datetime

    @classmethod
    def datetime_end(cls, t=None, date_type="day"):
        t = t if t else cls.datetime_now()
        return arrow.get(t).ceil(date_type).datetime

    @classmethod
    def human_date_yesterday_start(cls, floor="day", only_date=False):
        time_stamp = arrow.now().shift(days=-1).floor(floor).timestamp
        return cls.timestamp_to_human(time_stamp) if not only_date else cls.human_datetime_only_date(
            cls.timestamp_to_human(time_stamp))

    @classmethod
    def human_date_yesterday_end(cls, floor="day", only_date=False):
        time_stamp = arrow.now().shift(days=-1).ceil(floor).timestamp
        return cls.timestamp_to_human(time_stamp) if not only_date else cls.human_datetime_only_date(
            cls.timestamp_to_human(time_stamp))

    @classmethod
    def human_datetime_only_date(cls, t):
        try:
            t = t.split(" ")[0]
            return t
        except ValueError as e:
            print(e)

    @classmethod
    def human_date_to_ios_date(cls, t=None, fmt=None):
        t = cls.datetime_to_human() if not t else t
        t_datetime = cls.human_date_to_datetime(t, fmt=fmt)
        return cls.localize(t_datetime)

    @classmethod
    def ios_date_end(cls, t=None, date_type="day"):
        t = cls.ios_datetime() if not t else t
        return arrow.get(t).ceil(date_type).datetime

    @classmethod
    def ios_date_start(cls, t=None, date_type="day"):
        t = cls.ios_datetime() if not t else t
        return arrow.get(t).floor(date_type).datetime

    @classmethod
    def ios_datetime(cls, t=None):
        t = arrow.now(tz="Asia/Shanghai") if not t else t
        return t.datetime

    @classmethod
    def localize(cls, t=None):
        return cls.ios_datetime() if not t else timezone("Asia/Shanghai").localize(t)

    @classmethod
    def human_range_date(cls, start, end, fmt="YYYY-MM-DD"):
        start_date = arrow.get(start, fmt)
        end_date = arrow.get(end, fmt)
        date_list = []
        while start_date <= end_date:
            date_list.append(start_date.format(fmt))
            start_date = start_date.shift(days=1)
        return date_list
