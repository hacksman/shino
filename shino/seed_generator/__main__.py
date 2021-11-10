# coding: utf-8
# @Time : 9/8/21 9:35 AM

import os

import multiprocessing

from multiprocessing.managers import BaseManager

from shino.libs.log_ext import LogExt

from shino.seed_generator.seed_gen_handle import SeedGenHandle

from signal import (SIGINT, SIGTERM, signal)

from shino.seed_generator.seed_gen_processor import SeedGenProcessor

from collections import OrderedDict

from conf import PropertiesCenter, GlobalSetting

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--env",
                    choices=["debug", "local", "dev", "prod", "local_to_dev", "local_to_prod"],
                    help="set env[debug、local、dev、prod、local_to_dev、local_to_prod]"
                    )

args = parser.parse_args()

if not args.env:
    raise Exception(f"u must set env args for config")

GlobalSetting.env(args.env)

conf_info = PropertiesCenter.get(os.path.basename(os.path.dirname(__file__)))

dir_name = os.path.basename(os.path.dirname(__file__))

log_name = f"{dir_name}.log"

log = LogExt(log_name).get_logger

conf_info["log"] = log

conf_info["db"] = PropertiesCenter._DB_SETTING


class CustomOrderDict(OrderedDict):

    def get_len(self):
        return self.__len__()

    def get_dict(self):
        return dict(self)


def main():
    job_event = multiprocessing.Event()

    seed_gen_job = SeedGenProcessor(conf_info)

    seed_gen_handle = SeedGenHandle(conf_info)

    base_manager = BaseManager()
    base_manager.register("CustomOrderDict", CustomOrderDict)
    base_manager.start()

    share_order_dict = base_manager.CustomOrderDict()

    seed_producer = multiprocessing.Process(target=seed_gen_job.seed_produce, args=(share_order_dict, job_event))
    seed_consumer = multiprocessing.Process(target=seed_gen_job.seed_consume, args=(share_order_dict, job_event))

    seed_producer.start()
    seed_consumer.start()

    log.info(f"main pid={os.getpid()}")

    def handle_sigterm(*_):
        log.info(f"{dir_name} received shutdown signal")
        job_event.set()
        seed_gen_handle.withdraw_seed(share_order_dict)
        log.success(f"{dir_name} shut down gracefully")

    signal(SIGINT, handle_sigterm)
    signal(SIGTERM, handle_sigterm)

    seed_producer.join()
    seed_consumer.join()


if __name__ == '__main__':
    main()
