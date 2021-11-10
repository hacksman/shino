# coding: utf-8
# @Time : 9/9/21 10:40 AM


import os

import multiprocessing

import grpc

from multiprocessing import Process

from shino.libs.log_ext import LogExt

from concurrent import futures

from signal import (SIGTERM, SIGINT, signal)

from google.protobuf.json_format import MessageToDict

from protos.gen.extractor_pb2_grpc import (ExtractServiceServicer, add_ExtractServiceServicer_to_server)

from shino.extractor.extract_handle import ExtractHandle

from shino.extractor.extract_processor import ExtractProcessor

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


class ExtractorService(ExtractServiceServicer):

    def __init__(self, extract_handler):
        self.extract_handler = extract_handler

    def extract(self, request, context):
        ext_dict = MessageToDict(request, preserving_proto_field_name=True)
        extract_msg = self.extract_handler.extract(ext_dict)
        return extract_msg


def serve():
    extract_handler = ExtractHandle(conf_info)

    extract_job = ExtractProcessor(conf_info)

    job_event = multiprocessing.Event()
    job_process = Process(target=extract_job.do_job, args=(job_event,))
    job_process.start()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=conf_info["service_max_works"]))
    add_ExtractServiceServicer_to_server(ExtractorService(extract_handler), server)
    server.add_insecure_port(f"[::]:{conf_info['service_port']}")
    server.start()

    def handle_sigterm(*_):
        log.info(f"{dir_name} received shut down signal")
        job_event.set()
        all_rpc_done_event = server.stop(conf_info["service_stop_wait"])
        all_rpc_done_event.wait(conf_info["service_stop_wait"])
        log.success(f"{dir_name} shut down gracefully!")

    signal(SIGTERM, handle_sigterm)
    signal(SIGINT, handle_sigterm)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
