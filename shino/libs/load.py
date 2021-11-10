# coding: utf-8
# @Time : 9/9/21 9:56 AM
import importlib.util

from importlib import import_module
from pkgutil import iter_modules


def load_obj(path, prefix="", suffix=""):
    cls_dict = {}
    mods = walk_modules(path)
    for mod in mods:
        if hasattr(mod, "__path__"):
            continue
        mod_name = mod.__name__.split(".")[-1]
        for k, c in vars(mod).items():
            if k.lower() == f"{prefix}{mod_name.lower()}{suffix}":
                cls_dict[mod_name] = c
                break
    return cls_dict


def walk_modules(path):
    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, "__path__"):
        for _, sub_path, is_pkg in iter_modules(mod.__path__):
            full_path = f"{path}.{sub_path}"
            if is_pkg:
                mods += walk_modules(full_path)
            else:
                sub_mod = import_module(full_path)
                mods.append(sub_mod)
    return mods
