# -*- coding:utf-8 -*-

from loguru import logger
from glom import glom


class PropertiesFiles:
    DB_SETTING = "db_setting"
    SETTING = "setting"


class PropertiesLoader:

    @staticmethod
    def load(env, setting_file):
        common_setting = PropertiesLoader._load(f"resources.{setting_file}")
        env_setting = PropertiesLoader._load(f"resources.{env.lower()}.{setting_file}")

        if common_setting and isinstance(common_setting, dict) \
                and env_setting and isinstance(env_setting, dict):
            common_setting.update(env_setting)
            return common_setting

        return env_setting or common_setting

    @staticmethod
    def _load(module_name):
        try:
            import importlib
            xx_module = importlib.import_module(module_name)
            return getattr(xx_module, "setting")
        except ImportError as e:
            logger.warning(f"ImportError module {module_name}")


class PropertiesCenter:
    _DB_SETTING = {}
    _SETTING = {}

    def __init__(self, env):
        db_setting = PropertiesLoader.load(env, PropertiesFiles.DB_SETTING)
        PropertiesCenter._DB_SETTING.update(db_setting)

        setting = PropertiesLoader.load(env, PropertiesFiles.SETTING)
        PropertiesCenter._SETTING.update(setting)

    @staticmethod
    def get(key):
        return glom(PropertiesCenter._SETTING, key)

    @staticmethod
    def get_db(key):
        return glom(PropertiesCenter._DB_SETTING, key)

