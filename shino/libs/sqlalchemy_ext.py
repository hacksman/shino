# coding: utf-8
# @Time : 9/9/21 11:06 AM


from sqlalchemy import inspect
from sqlalchemy.orm import mapper


class SqlalchemyExt:

    @classmethod
    def obj_to_dict(cls, obj):
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    @classmethod
    def dict_to_obj(cls, results, to_class):
        obj = to_class()
        for r in results.keys():
            obj.__setattr__(r, results[r])
        return obj

    @classmethod
    def get_model_by_table(cls, base, engine, table_name):
        base.metadata.reflect(engine)
        table = base.metadata.tables[table_name]
        t = type(table_name, (object,), dict())
        mapper(t, table)
        base.metadata.clear()
        return t
