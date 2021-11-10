# coding: utf-8
# @Time : 9/20/21 5:08 PM


setting = {
    "mysql": {
        "host": "127.0.0.1",
        "port": 3306,
        "db": "crawl",
        "user": "shino",
        "password": "shino",
    },

    "redis": {
        "host": "127.0.0.1",
        "port": 6379,
        "db": 1,
        "user": None,
        "password": None,
        "max_conn": 200,
        "seed_withdraw": 11,
    },

    "rabbitmq": {
        "host": "127.0.0.1",
        "port": 5672,
        "user": "shino",
        "password": "shino",
        "vhost": "/",
        "queue_distributor_to_downloader": "download_req",
        "queue_downloader_to_extractor": "download_rsp",
        "queue_seed_generator_to_distributor": "seed",
        "queue_extractor_to_downloader": "extract_to_crawl",
        "queue_extractor_to_cleaner": "extract_info",
        "queue_cleaner_to_saver": "clean_info",
    }
}