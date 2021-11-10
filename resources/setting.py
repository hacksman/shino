# -*- coding:utf-8 -*-

setting = {
    "libs": {
        "fetch": {
            "proxy_http_url": "http://user_name:password@uri:port",

            # 请求重试相关参数
            # 请求超时时长
            "default_req_timeout": 5,
            # 最大重试请求次数
            "max_retry_req_times": 3,
            # 重试下次请求时，最小等待时长
            "retry_random_min_wait": 1000,  # ms
            # 重试下次请求时，最大等待时长
            "retry_random_max_wait": 5000,  # ms
        }
    }
}
