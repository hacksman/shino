# coding: utf-8

from exception import ConfigException


class GlobalSetting(object):
    _env = {}

    @staticmethod
    def env(env=None):
        if env:
            from conf.property import PropertiesCenter
            PropertiesCenter(env)
            GlobalSetting._env = env

            return GlobalSetting
        else:
            return GlobalSetting._env


class Env(object):
    DEBUG = "debug"
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
    LOCAL_TO_PROD = "local_to_prod"
    LOCAL_TO_DEV = "local_to_dev"

    @staticmethod
    def get(env):
        if env == "debug":
            return Env.DEBUG

        if env == "local":
            return Env.LOCAL

        elif env == "dev":
            return Env.DEV

        elif env == "prod":
            return Env.PROD

        elif env == "local_to_prod":
            return Env.LOCAL_TO_PROD

        elif env == "local_to_dev":
            return Env.LOCAL_TO_DEV

        raise ConfigException("Env error, env={}".format(env))
