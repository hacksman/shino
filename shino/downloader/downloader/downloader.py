# coding: utf-8
# @Time : 9/9/21 9:48 AM

from shino.downloader.downloader.simple import SimpleDownloader


class Downloader:

    def __init__(self, conf):
        self.conf = conf
        self.log = conf.get("log")
        self.downloaders = {
            "simple": SimpleDownloader(conf),
        }

    def download(self, req):
        downloader = self.downloaders.get(req.get('download_type'))
        if downloader:
            res = downloader.download(req)
        else:
            res = self.downloaders.get("simple").download(req)
        if res:
            self.log.info(f"{downloader.__class__.__name__} has download:{req.get('url')}")
        return res

    def stop(self):
        if not self.downloaders:
            return
        for _, downloader in self.downloaders.items():
            downloader.stop()
