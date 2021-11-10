# coding: utf-8
# @Time : 9/9/21 9:39 AM

import argparse

import os

import grpc

import multiprocessing

from signal import signal, SIGTERM, SIGINT

from shino.libs.log_ext import LogExt

from concurrent import futures

from multiprocessing import Process

from protos.gen.downloader_pb2_grpc import (DownloadServiceServicer, add_DownloadServiceServicer_to_server)

from google.protobuf.json_format import MessageToDict

from shino.downloader.download_handle import DownloadHandler

from shino.downloader.download_processor import DownloadProcessor

from conf import PropertiesCenter, GlobalSetting

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


class DownloaderService(DownloadServiceServicer):

    def __init__(self, download_handler):
        self.download_handler = download_handler

    def download(self, request, context):
        req_dict = MessageToDict(request, preserving_proto_field_name=True)
        res = self.download_handler.download(req_dict)
        res_dict = MessageToDict(res, preserving_proto_field_name=True)
        del res_dict["content"]
        return res


def serve():
    downloader_handler = DownloadHandler(conf_info)

    download_job = DownloadProcessor(conf_info)

    job_event = multiprocessing.Event()
    job_process = Process(target=download_job.do_job, args=(job_event,))
    job_process.start()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=conf_info["service_max_works"]))
    add_DownloadServiceServicer_to_server(DownloaderService(downloader_handler), server)
    server.add_insecure_port(f"[::]:{conf_info['service_port']}")
    server.start()

    def handle_sigterm(*_):
        log.info(f"{dir_name} received shutdown signal")
        job_event.set()
        all_rpc_done_event = server.stop(conf_info["service_stop_wait"])
        all_rpc_done_event.wait(conf_info["service_stop_wait"])
        log.success(f"{dir_name} shut down gracefully")

    signal(SIGINT, handle_sigterm)
    signal(SIGTERM, handle_sigterm)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
