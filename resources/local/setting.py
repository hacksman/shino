# -*- coding:utf-8 -*-

setting = {
    "downloader": {
        "middleware_module": "shino.downloader",
        "middlewares": ["default", "useragent", "headers"],
        "default_request_params": {
            "method": "get",
            "download_type": "simple",
            # 重试请求随机休息时长
            "next_retry_sleep": (2, 4),
            "time_out": 60,
            "retry_times": 5,
            "check_size": 100,
            "verify": False
        },
        "service_max_works": 10,
        "service_port": 50061,
        "service_stop_wait": 30,
    },
    "seed_generator": {
        'dynamic_url_module': 'shino.seed_generator.modifier'
    },
    "extractor": {
        "service_max_works": 10,
        "service_port": 50062,
        "service_stop_wait": 30,
    },
    "cleaner": {
        "service_max_works": 10,
        "service_port": 50063,
        "service_stop_wait": 30,
    },
    "saver": {
        "service_max_works": 10,
        "service_port": 50064,
        "service_stop_wait": 30,
    },
}
