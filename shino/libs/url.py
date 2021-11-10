# coding: utf-8
# @Time : 9/9/21 10:45 AM


from furl import furl


def get_origin_path(url):
    f_url = furl(url)
    url_origin_path = f_url.origin + f_url.path.asdict().get("encoded", "")
    return url_origin_path
