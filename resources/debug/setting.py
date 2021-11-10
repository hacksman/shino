# coding: utf-8
# @Time : 9/20/21 5:08 PM

setting = {
    "downloader": {
        "middleware_module": "shino.downloader",
        "middlewares": ["default", "useragent", "headers"],
        "default_request_params": {
            "method": "get",
            "download_type": "simple",
            "time_out": 60,
            "retry_times": 5,
            "check_size": 100,
            "verify": False
        },
        "service_port": 50061,
        "mode": 'debug'
    },
    "seed_generator": {
        'dynamic_url_module': 'shino.seed_generator.modifier',
        "mode": "debug"
    },
    "extractor": {
        "service_port": 50062,
        "mode": "debug"
    },
    "cleaner": {
        "service_port": 50063,
        "mode": "debug"
    },
    "saver": {
        "service_port": 50064,
        "mode": "debug"
    },
}