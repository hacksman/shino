# coding: utf-8
# @Time : 9/18/21 10:56 AM

from furl import furl


class BaseModifier:

    @staticmethod
    def _post_add(url, value):
        if not isinstance(value, dict):
            raise ValueError(f"post data must receive a dict,got {type(value).__name__}")
        url_split = url.split("|")
        url_post_data = ""
        idx = -1
        for idx, url_info in enumerate(url_split[1:]):
            if "post_data" in url_info:
                url_post_data = url_info
                break
        if not url_post_data:
            raise Exception(f"post_add need post data before")

        post_data_char, post_data = url_post_data.split(":")
        need_add_post_data = "&".join([f"{a}={b}" for a, b in value.items()])
        post_data = f"{post_data_char}:{post_data}&{need_add_post_data}"

        url_split[idx + 1] = post_data
        final_url = "|".join(url_split)
        return final_url

    @staticmethod
    def _query_add(url, value):
        if not isinstance(value, dict):
            raise ValueError(f"query data must dict, but got {type(value).__name__}")
        url_split = url.split("|")
        url = url_split[0]
        f_url = furl(url)
        f_url.add(value)
        f_url = f_url.tostr(query_dont_quote=[",", ":", "[", "]"])
        url_split[0] = f_url
        final_url = "|".join(url_split)
        return final_url
