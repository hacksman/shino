# coding: utf-8
# @Time : 9/9/21 10:40 AM


import json
import math
from copy import deepcopy

from furl import furl
from glom import glom
from lxml.etree import fromstring, HTMLParser

from shino.libs.encrypt import gen_md5
from shino.libs.mysql_ext import MysqlExt
from protos.gen.downloader_pb2 import DownloadReq
from protos.gen.extractor_pb2 import ExtractInfo
from shino.libs.url import get_origin_path
from shino.libs.misc import Pager


class ExtractHandle:

    def __init__(self, conf):
        self.log = conf["log"]

        self.mysql_conf = glom(conf, "db.mysql")

        self.mysql = MysqlExt(**self.mysql_conf)

    def extract_detail(self, result, rules):

        def _pack_json(result, rules):
            item = {}

            for p_rule in rules:

                if p_rule.get("$value_type") == "raw":
                    if p_rule.get("$parse_method") == "json":
                        item[p_rule.get("$name")] = glom(result, p_rule.get("$parse_rule"))
                    elif p_rule.get("$parse_method") == "none":
                        item[p_rule.get("$name")] = p_rule.get("$parse_rule")
                    else:
                        item[p_rule.get("$name")] = result.xpath(p_rule.get("$parse_rule"))

                elif p_rule.get("$value_type") == "recursion":
                    if p_rule.get("$parse_method") == "json":
                        tmp_result = glom(result, p_rule.get("$parse_rule"))
                        total_result = []
                        for per_r in tmp_result:
                            total_result.append(_pack_json(per_r, p_rule.get("$each")))
                        item[p_rule.get("$name")] = total_result
                    elif p_rule.get("$parse_method") == "none":
                        item[p_rule.get("$name")] = p_rule.get("$parse_rule")
                    else:
                        tmp_result = result.xpath(p_rule.get("$parse_rule"))
                        total_result = []
                        for per_r in tmp_result:
                            total_result.append(_pack_json(per_r, p_rule.get("$each")))
                        item[p_rule.get("$name")] = total_result
            return item

        def _unpack_datas(result: dict) -> list:
            if "__datas__" not in result:
                return [result]

            item_results = []
            all_item = result.pop("__datas__")

            for per_item in all_item:
                if "__datas__" in per_item:
                    tmp_datas = per_item.pop("__datas__")
                    for per_tmp_data in tmp_datas:
                        tmp_item = _unpack_datas(per_tmp_data)
                        for per_tmp_item in tmp_item:
                            item_results.append({**per_tmp_item, **per_item})
                else:
                    item_results.append({**result, **per_item})

            return item_results

        pack_result = _pack_json(result, rules)
        return _unpack_datas(pack_result)

    def pre_extract(self, res_info):
        return res_info

    def get_parse_rules(self, res_info):
        if not isinstance(res_info, dict):
            return []
        api = res_info["req_info"]['api']
        rules = [_ for _ in self.mysql.select_many(f'select * from _parse_detail where `api`="{api}"')]
        return rules

    def get_list_rule_by_id(self, list_parse_id):
        if not isinstance(list_parse_id, int):
            return {}
        result = self.mysql.select_one(f"select * from _parse_list where `_id`={list_parse_id}")
        return result

    def extract(self, res_info):
        rules = self.get_parse_rules(res_info)

        links = []
        extract_data = []
        topic_id = -1
        for per_rule in rules:
            if per_rule.get("data_rule"):
                parse_content = self.extract_content(res_info, per_rule)
                extract_data.append(parse_content)
                topic_id = per_rule.get('topic_id', -1)
            if per_rule.get("url_rule"):
                parse_url = self.extract_content(res_info, per_rule, link_type="URL")
                links.append(parse_url)
        return ExtractInfo(batch_no=res_info.get("batch_no"),
                           api=res_info.get("api"),
                           ex_status="1",
                           topic_id=topic_id,
                           extract_data=json.dumps(extract_data),
                           links=json.dumps(links))

    def extract_content(self, res_info, rule, link_type="CONTENT"):
        if link_type == "CONTENT":
            parse_rule = rule.get("data_rule")
        elif link_type == "SUB_URL":
            parse_rule = rule.get("url_rule")
        elif link_type == "PAGE_TOTAL":
            parse_rule = rule.get("total_cnt_match_rule")
        else:
            return []
        if not parse_rule:
            return []
        if isinstance(parse_rule, str):
            parse_rule = json.loads(parse_rule)
        if "text/html" in res_info["content_type"].lower():
            res_content = fromstring(res_info['content'], parser=HTMLParser())
        elif "application/json" in res_info["content_type"].lower():
            res_content = json.loads(res_info['content'])
        else:
            res_content = None
        if not res_content:
            self.log.warning(f"something error happened")
            return []
        results = self.extract_detail(res_content, parse_rule)
        return results

    def pack_extract_data(self, res_info, rule, parse_results):
        batch_no = res_info['req_info']["batch_no"]
        api = res_info['req_info']["api"]
        ex_status = '1'
        topic_id = rule.get("topic_id")
        extract_data = json.dumps(parse_results)

        extract_info = ExtractInfo(batch_no=batch_no,
                                   api=api,
                                   ex_status=ex_status,
                                   topic_id=topic_id,
                                   extract_data=extract_data)
        return extract_info

    def get_page_now(self, res_info, page_field):
        req_url = res_info['url']
        url_query_params = dict(furl(req_url).query.params)
        if page_field in url_query_params:
            page_now = int(url_query_params[page_field])
            return page_now
        post_data = res_info["req_info"].get("post_data", {})
        if page_field in post_data:
            page_now = int(post_data[page_field])
            return page_now

    def _gen_page_req(self, res_info, page_field, page):
        req_info = deepcopy(glom(res_info, "req_info"))
        req_url = req_info["url"]
        url_query_params = dict(furl(req_url).query.params)
        if page_field in url_query_params:
            f_req_url = furl(req_url)
            f_req_url.args[page_field] = page
            req_url = f_req_url.url
        else:
            if page_field not in req_info.get("post_data"):
                return None
            else:
                post_data = res_info["post_data"]
                post_data[page_field] = page
                req_info["post_data"] = post_data
        req_info["url"] = req_url
        return DownloadReq(**req_info)

    def gen_page_req(self, res_info, rule):
        list_parse_id = rule.get('list_parse_id')
        if not list_parse_id:
            return []
        parse_list_rule = self.get_list_rule_by_id(list_parse_id)
        if not parse_list_rule:
            self.log.warning(f"failed to get list parse rule.\tlist_parse_id={list_parse_id}")
            return []
        start_page = parse_list_rule.get("start_page")
        page_filed = parse_list_rule["page_field"]
        page_now = self.get_page_now(res_info, page_filed)
        if not page_now:
            self.log.warning(f"failed to get page now.\tlist_parse_id={list_parse_id}")
            return []
        if not start_page == page_now:
            return []
        page_size = parse_list_rule["page_size"]
        total_cnt_extract = self.extract_content(res_info, parse_list_rule, link_type="PAGE_TOTAL")
        if not total_cnt_extract:
            self.log.warning(f"failed total page count extract.\tparse_list_rule={parse_list_rule}")
            return []

        total_cnt_raw = total_cnt_extract[0].get("total_cnt")
        max_page = parse_list_rule["max_page"]
        if not total_cnt_raw:
            self.log.warning(f"failed get total page cnt")
            if max_page == -1:
                return []
            else:
                total_cnt = max_page * page_size
        else:
            total_cnt_raw = int(total_cnt_raw)
            if max_page == -1:
                total_cnt = total_cnt_raw
            else:
                page_total = math.ceil(total_cnt_raw / page_size)
                smaller_page = min(max_page, page_total)
                total_cnt = smaller_page * page_size

        pager = Pager(page_now, page_size, page_now + 1, total_cnt)
        all_page_req = [self._gen_page_req(res_info, page_filed, page) for page in pager.iter_page]
        all_page_req = list(filter(lambda x: x is not None, all_page_req))
        return all_page_req

    def gen_sub_page_req(self, res_info, sub_links_raw):
        req_info = deepcopy(glom(res_info, "req_info"))
        download_req_results = []
        for per_sub in sub_links_raw:
            url = per_sub.pop("url")
            method = "post" if any(s.startswith("_$post_") for s in per_sub.keys()) else "get"
            get_params = {k[6:]: per_sub[k] for k in filter(lambda x: x.startswith("_$get_"), per_sub)}
            post_params = {k[7:]: per_sub[k] for k in filter(lambda x: x.startswith("_$post_"), per_sub)}
            if get_params:
                url = furl(url).add(get_params).url
            api = get_origin_path(url)
            batch_no = req_info["batch_no"]
            new_batch_no = f"{batch_no.split('_')[0]}_{gen_md5(api)}"

            req_item = {
                "batch_no": new_batch_no,
                "api": api,
                "url": url,
                "method": method,
            }
            if req_info.get("download_type"):
                req_item["download_type"] = req_info["download_type"]
            if req_info.get(f"retry_times"):
                req_item["retry_times"] = req_info["retry_times"]
            if req_info.get("time_out"):
                req_item["time_out"] = req_info["time_out"]
            if post_params:
                req_item["post_data"] = json.dumps(post_params)
            if req_info.get("use_proxy"):
                req_item["use_proxy"] = req_info["use_proxy"]

            download_req = DownloadReq(**req_item)
            download_req_results.append(download_req)
            del req_item
        return download_req_results
